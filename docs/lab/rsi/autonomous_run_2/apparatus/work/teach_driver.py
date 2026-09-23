#!/usr/bin/env python3
"""teach_driver.py — teaching protocol driver (D-TEACH §§1–5).

Pure glue + measurement. The mechanical RULE evaluation lives in
teach_learner.zag (pure Zag). This driver: parses lesson files, normalizes
RULEs, invokes the learner per CAL, installs on all-match, rejects +
rolls back on first mismatch.

Usage:
  teach_driver.py <learner-bin> <curriculum-dir> <out-dir> [--reconstruct]

The official teaching run (on the frozen 20 lessons) is NOT executed by
the build crew; this driver is verified on synthetic lessons. The
--reconstruct mode verifies byte-exact entries regeneration.

Lesson order: lesson_01..lesson_19 in numeric order, then lesson_bad.txt
(Micah's binding correction).
"""
import os, sys, re, hashlib, subprocess, shutil

# D-TEACH §5 frozen fact vocabulary (CAL facts must be members)
FACT_VOCAB = set("""score-up score-same score-down
errors-up errors-same errors-down
measured-cost-up measured-cost-same measured-cost-down
measured-work-up measured-work-same measured-work-down
selfreported-cost-down selfreported-cost-same selfreported-cost-up
new-capability regression
novel-score-down novel-score-same novel-errors-up
frozen-battery novel-items labels-visible labels-hidden battery-edited-midrun
prediction-before-test prediction-after-test prediction-hit prediction-miss
no-prediction kept-on-hit kept-on-miss discarded-on-hit discarded-on-miss
forbidden-transition gate-fired gate-skipped gate-weakened proceed-anyway
barren-round halt-with-reasons halt-without-reasons time-bound-reached
search-extended-past-halt
gap-measured gap-assumed feature-named score-delta-only
design-written design-missing contract-written contract-missing
trigger-stated trigger-missing behavior-stated behavior-missing
bounds-stated bounds-missing
mechanism-named reads-stated reads-missing changes-stated changes-missing
slot-source-declared slot-source-undeclared label-column-read
prediction-stated prediction-missing aggregate-predicted aggregate-missing
per-feature-predicted per-feature-missing
failure-localized failure-unlocalized design-revised candidate-retired
blind-mutation retested-unchanged
provenance-logged provenance-missing gap-cited episodes-cited prediction-cited""".split())

def parse_lesson(path):
    """Parse a lesson .txt into dict. Strict; refuses malformed."""
    with open(path, 'r') as f:
        text = f.read()
    d = {}
    # LESSON: <id>
    m = re.search(r'^LESSON:\s*(.+)$', text, re.M)
    if not m: raise ValueError(f"{path}: missing LESSON")
    d['id'] = m.group(1).strip()
    # JUDGMENT: <pos> / <neg>
    m = re.search(r'^JUDGMENT:\s*(.+?)\s*/\s*(.+)$', text, re.M)
    if not m: raise ValueError(f"{path}: missing JUDGMENT")
    d['pos'] = m.group(1).strip()
    d['neg'] = m.group(2).strip()
    # IS: (may span lines until USED:)
    m = re.search(r'^IS:\s*(.*?)^USED:', text, re.M | re.S)
    if not m: raise ValueError(f"{path}: missing IS")
    d['is'] = ' '.join(m.group(1).strip().split())
    # USED: (until RULE:)
    m = re.search(r'^USED:\s*(.*?)^RULE:', text, re.M | re.S)
    if not m: raise ValueError(f"{path}: missing USED")
    d['used'] = ' '.join(m.group(1).strip().split())
    # RULE: <expr> -> <pos> ; else <neg>
    m = re.search(r'^RULE:\s*(.+?)\s*->\s*(.+?)\s*;\s*else\s*(.+)$', text, re.M)
    if not m: raise ValueError(f"{path}: missing RULE")
    d['expr'] = m.group(1).strip()
    rpos = m.group(2).strip(); rneg = m.group(3).strip()
    if rpos != d['pos'] or rneg != d['neg']:
        raise ValueError(f"{path}: RULE judgments {rpos}/{rneg} != {d['pos']}/{d['neg']}")
    # CALs: FACTS: ... | EXPECT: ...
    d['cals'] = []
    for m in re.finditer(r'^CAL:\s*FACTS:\s*(.+?)\s*\|\s*EXPECT:\s*(.+)$', text, re.M):
        facts = [x.strip() for x in m.group(1).split('|')]
        for f in facts:
            if f not in FACT_VOCAB:
                raise ValueError(f"{path}: CAL fact '{f}' not in §5 vocabulary")
        exp = m.group(2).strip()
        if exp not in (d['pos'], d['neg']):
            raise ValueError(f"{path}: CAL EXPECT {exp} not in {d['pos']}/{d['neg']}")
        d['cals'].append((facts, exp))
    if not d['cals']:
        raise ValueError(f"{path}: no CALs")
    return d

def mode_of(lesson):
    """G: GAMING/OVERFIT/CORRUPT; I: IMPROVEMENT; M: others."""
    pos = lesson['pos']
    if pos in ('GAMING', 'OVERFIT', 'CORRUPT'):
        return 'G'
    if pos == 'IMPROVEMENT':
        return 'I'
    return 'M'

def normalize_rule(lesson):
    """RULE -> POS~NEG~expr (driver-side mechanical translation)."""
    # expr uses ( ) & | ! and atoms; strip whitespace
    expr = re.sub(r'\s+', '', lesson['expr'])
    # sanity: only allowed chars
    if not re.fullmatch(r'[A-Za-z0-9()&|!\-]+', expr):
        raise ValueError(f"bad expr chars: {expr}")
    return f"{lesson['pos']}~{lesson['neg']}~{expr}"

def run_learner(learner_bin, mode, rule_norm, grules_norm, facts):
    """Invoke the Zag learner; return its judgment string."""
    facts_s = '|'.join(facts)
    out = subprocess.run(
        [learner_bin, mode, rule_norm, grules_norm, facts_s],
        capture_output=True, text=True, timeout=10)
    if out.returncode != 0:
        raise RuntimeError(f"learner failed rc={out.returncode}: {out.stderr[:200]}")
    return out.stdout.strip()

def entry_text(lesson, rule_norm):
    """Byte-exact entry format: @RSI-<id> / T:RSI-PRINCIPLE (D-TEACH §1)."""
    lines = [
        f"@RSI-{lesson['id']}",
        f"T:RSI-PRINCIPLE",
        f"JUDGMENT: {lesson['pos']} / {lesson['neg']}",
        f"RULE-NORM: {rule_norm}",
        f"IS: {lesson['is']}",
        f"USED: {lesson['used']}",
        f"CALS: {len(lesson['cals'])}",
    ]
    body = '\n'.join(lines) + '\n'
    h = hashlib.sha256(body.encode()).hexdigest()
    return body + f"SHA256: {h}\n---\n"

def teach(learner_bin, curriculum_dir, out_dir):
    """Run the teach protocol. Returns (installed, rejected)."""
    os.makedirs(out_dir, exist_ok=True)
    # lesson order: 01..19 numeric, then lesson_bad.txt
    files = []
    for i in range(1, 20):
        p = os.path.join(curriculum_dir, f"lesson_{i:02d}_*.txt")
        import glob
        g = sorted(glob.glob(p))
        if len(g) != 1:
            raise ValueError(f"expected 1 lesson_{i:02d}, got {g}")
        files.append(g[0])
    bad = os.path.join(curriculum_dir, "lesson_bad.txt")
    if not os.path.exists(bad):
        raise ValueError("missing lesson_bad.txt")
    files.append(bad)

    entries_path = os.path.join(out_dir, "entries.txt")
    log_path = os.path.join(out_dir, "install_log.txt")
    # fresh run: remove existing
    for p in (entries_path, log_path):
        if os.path.exists(p):
            os.remove(p)

    installed_g_rules = []  # normalized exprs, for I-mode guard
    installed = []
    rejected = []
    log_lines = []

    for lf in files:
        lesson = parse_lesson(lf)
        mode = mode_of(lesson)
        rule_norm = normalize_rule(lesson)
        # grules: installed G exprs joined by ';' (expr part only)
        grules_norm = ';'.join(installed_g_rules)

        ok = True
        cal_results = []
        for facts, expected in lesson['cals']:
            got = run_learner(learner_bin, mode, rule_norm, grules_norm, facts)
            match = (got == expected)
            cal_results.append((facts, expected, got, match))
            if not match:
                ok = False
                break  # reject at first mismatch

        lid = lesson['id']
        if ok:
            # install
            entry = entry_text(lesson, rule_norm)
            with open(entries_path, 'a') as f:
                f.write(entry)
            installed.append(lid)
            if mode == 'G':
                # store expr for the I-guard (extract expr from rule_norm)
                expr = rule_norm.split('~', 2)[2]
                installed_g_rules.append(expr)
            log_lines.append(f"INSTALLED {lid} ({len(lesson['cals'])} CALs match)")
        else:
            # reject + rollback (nothing staged; entries.txt untouched)
            rejected.append(lid)
            log_lines.append(f"REJECTED {lid} (CAL mismatch)")
            for facts, expected, got, match in cal_results:
                if not match:
                    log_lines.append(f"  MISMATCH facts={'|'.join(facts)} expected={expected} got={got}")
                    break

    with open(log_path, 'w') as f:
        f.write('\n'.join(log_lines) + '\n')

    # manifest: sha256 of entries.txt
    with open(entries_path, 'rb') as f:
        eh = hashlib.sha256(f.read()).hexdigest()
    with open(os.path.join(out_dir, "entries.sha256"), 'w') as f:
        f.write(eh + "  entries.txt\n")

    return installed, rejected, eh

def reconstruct(learner_bin, curriculum_dir, out_dir):
    """Re-run teach and verify entries.txt is byte-identical."""
    entries_path = os.path.join(out_dir, "entries.txt")
    with open(entries_path, 'rb') as f:
        before = f.read()
    # re-run into a temp dir
    tmp = out_dir + ".recon"
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    installed, rejected, eh = teach(learner_bin, curriculum_dir, tmp)
    with open(os.path.join(tmp, "entries.txt"), 'rb') as f:
        after = f.read()
    shutil.rmtree(tmp)
    if before == after:
        print(f"RECONSTRUCT OK: byte-identical ({len(before)} bytes, sha256 {hashlib.sha256(before).hexdigest()[:16]}...)")
        return True
    else:
        print("RECONSTRUCT FAIL: entries.txt differs")
        return False

def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    learner_bin = sys.argv[1]
    curriculum_dir = sys.argv[2]
    out_dir = sys.argv[3]
    if len(sys.argv) > 4 and sys.argv[4] == '--reconstruct':
        return 0 if reconstruct(learner_bin, curriculum_dir, out_dir) else 1
    installed, rejected, eh = teach(learner_bin, curriculum_dir, out_dir)
    print(f"installed: {len(installed)} {installed}")
    print(f"rejected: {len(rejected)} {rejected}")
    print(f"entries sha256: {eh}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
