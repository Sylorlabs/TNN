#!/usr/bin/env python3
"""gen_keys.py -- INDEPENDENT answer-key derivation for RSI-2 teaching verification.

Provenance: NO hardcoded scenario->answer map. Keys are derived mechanically
from the teaching sources (LESSONS / SCENARIOS in src/teach.py):

  * Principle matching: for each scenario, max token-overlap between the
    scenario text and each lesson's IS+USED+RULE text. Tokens are
    [A-Za-z0-9_]+ runs, len>=4, lowercased, minus the stopword set read
    from apparatus/work/teach_sweep.py (EN_STOP | ZAG_KW -- read, not
    retyped). Comparison is strictly-greater, so the first max wins
    (lowest lesson index). This mirrors deliberation verify_classify's
    kb_overlap comparison rule.
  * STEPS: JUDGMENT tokens of the S1..S6 lessons in lesson order,
    lowercased -- derived from the KB, not from a literal.
  * IMPROVES_IF / TRAP / DESIGN: the top-2 content tokens from
    (scenario tokens INTERSECT matched-lesson IS+USED+RULE tokens),
    ranked by (scenario term-frequency desc, lesson term-frequency desc,
    alphabetical asc).

Writes work/teach/keys.txt in the existing format and prints a derivation
report. Zero randomness; fully deterministic.

Usage: gen_keys.py            (writes work/teach/keys.txt, prints report)
       imported by teach.py --build to write keys without a KEYS dict.
"""
import importlib.util
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # autonomous_run_2
WORK = os.path.join(ROOT, 'work', 'teach')
APP_WORK = os.path.join(ROOT, 'apparatus', 'work')


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Import LESSONS and SCENARIOS from src/teach.py (import has no side
# effects; build only runs under --build).
_teach = _load_module(os.path.join(HERE, 'teach.py'), 'gen_keys_teach_src')
# Stopwords read from apparatus/work/teach_sweep.py (EN_STOP | ZAG_KW).
_sweep = _load_module(os.path.join(APP_WORK, 'teach_sweep.py'),
                      'gen_keys_sweep_src')
STOPWORDS = _sweep.STOPWORDS

LESSONS = _teach.LESSONS
SCENARIOS = _teach.SCENARIOS
SLOT_ORDER = ['IMPROVES_IF', 'STEPS', 'TRAP', 'DESIGN']
TOKEN_RE = re.compile(r'[A-Za-z0-9_]+')


def content_tokens(text):
    """Tokens len>=4, lowercased, minus stopwords."""
    toks = []
    for m in TOKEN_RE.finditer(text):
        t = m.group(0)
        if len(t) >= 4:
            tl = t.lower()
            if tl not in STOPWORDS:
                toks.append(tl)
    return toks


def lesson_match_text(lesson):
    """The text verify_classify matches against: IS + USED + RULE."""
    _lid, _judg, is_t, used, rule = lesson
    return is_t + ' ' + used + ' ' + rule


def scenario_file_text(vid, title, text):
    """Byte-identical to the file teach.py --build writes."""
    return "SCENARIO: %s\nTITLE: %s\n%s\n" % (vid, title, text)


def match_lesson(vid):
    """Principle matching for one scenario.

    Returns (best_index, best_overlap, scores) where scores is a list of
    (lesson_id, overlap) in lesson order. Strictly-greater comparison =>
    first max wins (lowest lesson index), mirroring verify_classify.
    """
    scen = next(s for s in SCENARIOS if s[0] == vid)
    _vid, title, text = scen
    stoks = content_tokens(scenario_file_text(vid, title, text))
    best_i, best_sc = -1, -1
    scores = []
    for i, lesson in enumerate(LESSONS):
        eset = set(content_tokens(lesson_match_text(lesson)))
        sc = sum(1 for t in stoks if t in eset)
        scores.append((lesson[0], sc))
        if sc > best_sc:
            best_sc, best_i = sc, i
    return best_i, best_sc, scores


def steps_key():
    """STEPS key: JUDGMENT tokens of the S1..S6 lessons, in lesson order."""
    s_lessons = sorted(
        [L for L in LESSONS if L[0][0] == 'S'],
        key=lambda L: int(L[0][1:].split('-')[0]))
    return [L[1].lower() for L in s_lessons]


def derive_keys():
    """Derive the full key table. Returns (keys, report_rows)."""
    steps = steps_key()
    keys = {}
    report = []
    for vid, title, text in SCENARIOS:
        best_i, best_sc, scores = match_lesson(vid)
        lesson = LESSONS[best_i]
        stoks = content_tokens(scenario_file_text(vid, title, text))
        ltoks = content_tokens(lesson_match_text(lesson))
        sset, lset = set(stoks), set(ltoks)
        inter = sset & lset
        s_tf = Counter(t for t in stoks if t in lset)
        l_tf = Counter(t for t in ltoks if t in sset)
        ranked = sorted(inter, key=lambda t: (-s_tf[t], -l_tf[t], t))
        top2 = ranked[:2]
        keys[vid] = {'IMPROVES_IF': list(top2), 'STEPS': list(steps),
                     'TRAP': list(top2), 'DESIGN': list(top2)}
        report.append({
            'vid': vid, 'lesson': lesson[0], 'overlap': best_sc,
            'scores': scores, 'ranked': ranked,
            's_tf': dict(s_tf), 'l_tf': dict(l_tf),
        })
    return keys, report


def write_keys(keys, path):
    """Write keys.txt in the existing format."""
    with open(path, 'w') as f:
        for vid, _title, _text in SCENARIOS:
            f.write("%s:\n" % vid)
            for slot in SLOT_ORDER:
                f.write("  %s: %s\n" % (slot, ' '.join(keys[vid][slot])))


def main():
    keys, report = derive_keys()
    os.makedirs(WORK, exist_ok=True)
    out = os.path.join(WORK, 'keys.txt')
    write_keys(keys, out)
    print("keys written: %s" % out)
    print("--- derivation report ---")
    for row in report:
        print("%s -> matched %s (overlap %d)" %
              (row['vid'], row['lesson'], row['overlap']))
        detail = ' '.join("%s=%d" % (lid, sc) for lid, sc in row['scores'])
        print("    per-lesson overlap: %s" % detail)
        basis = ', '.join("%s(scen_tf=%d,lesson_tf=%d)" %
                          (t, row['s_tf'][t], row['l_tf'][t])
                          for t in row['ranked'])
        print("    intersection ranked: %s" % (basis if basis else '(empty)'))
        for slot in SLOT_ORDER:
            print("    %s: %s" % (slot, ' '.join(keys[row['vid']][slot])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
