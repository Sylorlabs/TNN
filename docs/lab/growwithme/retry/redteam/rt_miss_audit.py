#!/usr/bin/env python3
"""Crew 3 red team: independent miss-classification audit of the M3 retry.
For every C1/C2 miss, verify from the agent's own m3-deliberation traces:
  - verdict class: tie-withhold vs wrong-candidate (single/union)
  - whether the right fact was in the top-k candidate set (coverage deficit check)
"""
import re, pathlib, sys

REPRO = pathlib.Path.home() / "workspace/growwithme_retry/redteam/repro"
RESEAL = pathlib.Path.home() / "workspace/growwithme_retry/redteam/docs/lab/growwithme/retry/probes_resealed"

STOP = set("""the and for with from that this are was were has have had will would can could
should must may might shall not no yes its his her their our your than then when where what which
who whom whose why how all any both each few more most other some such only own same too very just also
a an of to in on is it as at be by or if do does did""".split())

def load_probes(session):
    """qid -> (question, key) from re-sealed md (original Key:)."""
    text = (RESEAL / f"immediate_S{session}.md").read_text()
    out = {}
    for m in re.finditer(r"### (\S+)\nQ: (.*?)\nKey: (.*?)\n", text, re.DOTALL):
        qid, q, key = m.group(1), m.group(2).strip(), m.group(3).split("\n")[0].strip()
        out[qid] = (q, key)
    return out

def norm(s):
    s = s.lower(); s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def strip_note(a):
    return re.sub(r"\s*\[m3:.*?\]\s*$", "", a).strip()

def score(ans, key):
    na, nk = norm(strip_note(ans)), norm(key)
    if nk in na or na in nk: return True
    kw = [w for w in nk.split() if len(w) > 3 and w not in STOP]
    if not kw: return nk in na
    return sum(1 for w in kw if w in na) / len(kw) >= 0.70

def load_traces(session):
    """ref-prefix -> list of (considered, evidence, verdict)."""
    text = (REPRO / f"D_rt1/snapshot_S{session}.txt").read_text()
    out = {}
    pat = re.compile(r"TRACE \d+ \|\| kind=m3-deliberation \|\| ref=(.*?) \|\| considered=(.*?) \|\| evidence=(.*?) \|\| verdict=(.*?) \|\| reason=")
    for m in pat.finditer(text):
        ref, cons, ev, ver = m.group(1), m.group(2), m.group(3), m.group(4)
        cands = re.findall(r"(F\d+-\d+):(\d+)", cons)
        more = re.search(r"\+(\d+) more", cons)
        out.setdefault(ref, []).append((cands, int(more.group(1)) if more else 0, ev, ver))
    return out

def main():
    n_tie = n_wrong = n_covdef = n_total = 0
    rows = []
    for s in range(1, 7):
        probes = load_probes(s)
        qids = list(probes.keys())
        lines = (REPRO / f"D_rt1/probe_immediate_S{s}.txt").read_text().splitlines()
        ans = [l[5:].strip() for l in lines if l.startswith("A || ")]
        qlines = [l[5:].strip() for l in (REPRO / "probes" / f"immediate_S{s}.q").read_text().splitlines() if l.startswith("Q || ")]
        traces = load_traces(s)
        assert len(ans) == len(qids) == len(qlines) == 18, (s, len(ans), len(qids), len(qlines))
        for qid, a, q in zip(qids, ans, qlines):
            question, key = probes[qid]
            assert q == question, (s, qid)
            if score(a, key):
                continue
            n_total += 1
            right_fid = qid[:-2]  # "F1-01-Q" -> "F1-01"
            ref = q[:40]
            cands_list = traces.get(ref, [])
            # find trace whose candidate evidence matches; take the last matching one
            # (traces accumulate; immediate probes are administered once per session,
            #  but S7/other batteries may reuse question prefixes - match by full prefix)
            match = cands_list[-1] if cands_list else None
            if match is None:
                rows.append((s, qid, "NO-TRACE", right_fid, "?", a[:60]))
                continue
            cands, more, ev, ver = match
            cand_fids = [f for f, _ in cands]
            covered = right_fid in cand_fids
            if not covered and more == 0:
                n_covdef += 1
                cls = "COVERAGE-DEFICIT"
            elif "tie-withhold" in ver:
                n_tie += 1
                cls = f"tie-withhold (nc>={len(cands)}{'+'+str(more) if more else ''}, right-in-set={covered})"
            else:
                n_wrong += 1
                winner = ver.replace("single ", "").replace("union ", "").split("+")[0].strip()
                cls = f"wrong-candidate winner={winner} (right-in-set={covered})"
            rows.append((s, qid, cls, right_fid, ev[:90], a[:60]))
    print(f"total misses: {n_total} | tie-withhold: {n_tie} | wrong-candidate: {n_wrong} | coverage-deficit: {n_covdef}")
    print()
    for r in rows:
        print(f"S{r[0]} {r[1]}: {r[2]}\n    ev: {r[4]}\n    ans: {r[5]}")
    return 0

sys.exit(main())
