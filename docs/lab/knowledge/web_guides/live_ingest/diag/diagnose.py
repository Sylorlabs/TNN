#!/usr/bin/env python3
"""LI-1 refusal diagnoser probe. Glue only — no reasoning; it replays verdict
inputs through the webg binary and reads the emitted gate signatures.

Ledger format (run_li.py): R|<cid>|<gate>|<claim>|<reason>|<urls>
Workdirs: <outdir>/work/<cid>/{need.txt,pages.txt,verdict.out}; state at <outdir>/state.

Usage: diagnose.py <refusal_ledger.txt> <outdir> [webg_bin]
Re-derives the gate for every refusal from the binary's own output and reports:
ledger gate, derived gate, why-chain, and a classification recommendation
(LEGITIMATE vs BUG-CANDIDATE with evidence). Mismatches are flagged.
"""
import os, re, subprocess, sys, hashlib

def parse_ledger(path):
    entries = []
    with open(path) as f:
        for ln, line in enumerate(f, 1):
            line = line.rstrip('\n')
            if not line.strip() or line.startswith('#'):
                continue
            p = line.split('|')
            e = {'line': ln, 'raw': line, 'cid': p[1] if len(p) > 1 else '',
                 'gate': p[2] if len(p) > 2 else '', 'claim': p[3] if len(p) > 3 else '',
                 'reason': p[4] if len(p) > 4 else '', 'urls': p[5] if len(p) > 5 else ''}
            entries.append(e)
    return entries

def signatures(out):
    sig = {
        'inj_flags': re.findall(r'^FLAG\|INJECTION\|(\S+)', out, re.M),
        'dispute_flags': re.findall(r'^FLAG\|DISPUTE\|(\S+)', out, re.M),
        'src_gate': re.findall(r'^GATE\|SRC_INDEPENDENCE\|(.*)$', out, re.M),
        'uncheckable': 'ANSWER|UNCHECKABLE' in out,
        'unchecked': re.findall(r'^UNCHECKED\|(\S+)', out, re.M),
        'answer': None,
        'claims': re.findall(r'^CLAIM\|\d+\|([^|]*)\|', out, re.M),
    }
    m = re.search(r'^ANSWER\|(.*)$', out, re.M)
    if m:
        sig['answer'] = m.group(1)
    return sig

def derive_gate(sig, ledger_gate):
    """Map output signatures to the gate that fired (binary's own evidence)."""
    if sig['answer'] is not None and sig['answer'] != 'UNCHECKABLE':
        return 'INSTALLED', 'claim corroborated with provenance'
    if not sig['uncheckable']:
        return 'UNKNOWN', 'no ANSWER|UNCHECKABLE line (check rc/stderr for crash)'
    if sig['inj_flags'] and not sig['unchecked'] and not sig['src_gate']:
        return 'INJECTION_FLAG', 'injection-flagged page(s) %s excluded; nothing else to corroborate' % ','.join(sig['inj_flags'])
    if sig['src_gate']:
        return 'NO_CORROBORATION', 'winning cluster {%s} collapses to 1 distinct host < MIN-SOURCES=2 (SRC_INDEPENDENCE)' % sig['src_gate'][0]
    if sig['inj_flags']:
        return 'NO_CORROBORATION', 'injection-flagged page(s) %s excluded; remaining pages below corroboration bar' % ','.join(sig['inj_flags'])
    if sig['unchecked']:
        return 'NO_CORROBORATION', 'winning cluster < MIN-SOURCES=2 (fragmented sentence-selection or single-source)'
    return 'NO_CORROBORATION', 'cluster_best returned zero sentences (no query-overlap sentence on any included page)'

def classify(cid, ledger_gate, derived_gate, why, sig, workdir):
    """Recommend LEGITIMATE vs BUG-CANDIDATE. Conservative: anything the
    evidence cannot resolve is LEGITIMATE; only positive evidence of a
    misfiring gate / crash / parse failure is a BUG-CANDIDATE."""
    if derived_gate == 'INSTALLED':
        return 'BUG-CANDIDATE', 'ledger records a refusal but the replay INSTALLED the claim — ledger/driver mismatch or non-determinism'
    if derived_gate == 'UNKNOWN':
        return 'BUG-CANDIDATE', 'no verdict output — likely CRASH or malformed input; inspect rc/stderr'
    if ledger_gate in ('UNSUPPORTED_FETCH', 'SELECT_EMPTY'):
        return 'LEGITIMATE', 'driver-level: no usable pages; nothing for the instrument to resolve'
    if ledger_gate == 'PARSE_FAIL':
        return 'BUG-CANDIDATE', 'sentence-split produced zero sentences — check splitter vs page content (malformed-input handling)'
    if ledger_gate == 'CRASH':
        return 'BUG-CANDIDATE', 'nonzero rc from the instrument — crash, investigate'
    if ledger_gate == 'INTEGRITY_VIOLATION':
        return 'LEGITIMATE', 'glue veto held: claim cited an injection-flagged page; install refused (defense in depth)'
    if derived_gate == 'INJECTION_FLAG':
        return 'LEGITIMATE', 'page carried injected instructions; exclusion is load-bearing law'
    # NO_CORROBORATION family: legitimate iff the evidence as processed cannot
    # resolve the claim. Flag for human review only if the same normalized
    # sentence plausibly appears on >=2 pages but clustering split them.
    return 'LEGITIMATE', why + ' — evidence cannot resolve the claim under the frozen >=2-independent-pages rule'

def main():
    ledger, outdir = sys.argv[1], sys.argv[2]
    webg = sys.argv[3] if len(sys.argv) > 3 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', '..', 'webg')
    webg = os.path.normpath(webg)
    state_dir = os.path.join(outdir, 'state')
    entries = parse_ledger(ledger)
    rep = ['# LI-1 refusal diagnosis (probe)', '', f'ledger: {ledger}',
           f'outdir: {outdir}', f'webg: {webg}', f'entries: {len(entries)}', '']
    counts = {}
    for e in entries:
        cid = e['cid']
        wd = os.path.join(outdir, 'work', cid)
        vout = os.path.join(wd, 'verdict.out')
        rep.append(f'## {cid} (ledger line {e["line"]})')
        rep.append(f'- ledger gate: {e["gate"]}')
        rep.append(f'- claim: {e["claim"][:160]}')
        rep.append(f'- reason: {e["reason"][:200]}')
        rep.append(f'- urls: {e["urls"][:200]}')
        derived, why = 'NOT-REPLAYED', 'no verdict.out in workdir'
        sig = None
        if os.path.exists(vout):
            with open(vout) as f:
                out = f.read()
            sig = signatures(out)
            derived, why = derive_gate(sig, e['gate'])
            # live replay for determinism check
            nf = os.path.join(wd, 'need.txt')
            pf = os.path.join(wd, 'pages.txt')
            qf = os.path.join(wd, 'query.out')
            query = ''
            if os.path.exists(qf):
                for l in open(qf):
                    if l.startswith('QUERY|'):
                        query = l.split('|', 1)[1].strip()
                        break
            if os.path.exists(nf) and os.path.exists(pf) and os.path.isdir(state_dir):
                r = subprocess.run([webg, 'verdict', state_dir, nf, pf, 'FACT', query],
                                   capture_output=True, text=True)
                if r.stdout != out:
                    rep.append('- DETERMINISM-WARNING: live replay output differs from verdict.out')
                    rep.append('  live_sha=%s filed_sha=%s' % (
                        hashlib.sha256(r.stdout.encode()).hexdigest()[:12],
                        hashlib.sha256(out.encode()).hexdigest()[:12]))
                else:
                    rep.append('- replay: byte-identical to filed verdict.out')
        cls, clwhy = classify(cid, e['gate'], derived, why, sig, wd)
        rep.append(f'- derived gate: {derived}')
        rep.append(f'- why: {why}')
        rep.append(f'- classification: **{cls}** — {clwhy}')
        if e['gate'] not in ('', derived) and derived not in ('NOT-REPLAYED', 'INSTALLED', 'UNKNOWN'):
            # allow ledger NO_CORROBORATION to cover INJECTION_FLAG-driven withholds
            # (driver records the inj flags in the reason field)
            if not (e['gate'] == 'NO_CORROBORATION' and derived in ('INJECTION_FLAG', 'NO_CORROBORATION')):
                rep.append(f'- MISMATCH: ledger={e["gate"]} derived={derived}')
        counts[cls] = counts.get(cls, 0) + 1
        rep.append('')
    rep.append('## totals')
    for k, v in sorted(counts.items()):
        rep.append(f'- {k}: {v}')
    sys.stdout.write('\n'.join(rep) + '\n')

if __name__ == '__main__':
    main()
