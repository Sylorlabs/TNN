#!/usr/bin/env python3
"""Score C1/C2 immediate recall for the M3 retry.
Uses re-sealed keys from probes_resealed/immediate_S*.md (keys unchanged from frozen).
Strips [m3: ...] notes from answers before scoring.
Scoring criterion: 70% distinctive-word overlap (same as Phase 2 calibration scorer).
"""
import re, pathlib, sys

RETRY = pathlib.Path.home() / "workspace/growwithme_retry"

def load_keys(session):
    """Returns list of (qid, key) from re-sealed immediate probe md. Uses the
    original 'Key:' (not the 'S7 key:' which is post-correction)."""
    md = RETRY / f"probes_resealed/immediate_S{session}.md"
    text = md.read_text()
    keys = []
    # Pattern: ### <QID>-Q\nQ: ...\nKey: <key>\n (key may be followed by S7 key line)
    for m in re.finditer(r"### (\S+)\nQ: .*?\nKey: (.*?)\n", text, re.DOTALL):
        qid = m.group(1)
        key = m.group(2).strip()
        # If key spans multiple lines, take only first (S7 key is separate)
        key = key.split("\n")[0].strip()
        keys.append((qid, key))
    return keys

def normalize(s):
    s = s.lower()
    s = re.sub(r"[`'\"]", "", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def strip_m3_note(answer):
    """Remove the [m3: ...] deliberation note from the answer."""
    return re.sub(r"\s*\[m3:.*?\]\s*$", "", answer).strip()

def score_answer(answer, key):
    na = normalize(strip_m3_note(answer))
    nk = normalize(key)
    if nk in na or na in nk:
        return 1.0
    stop = {"the", "and", "for", "with", "from", "that", "this", "are", "was", "were", "has", "have", "had", "will", "would", "can", "could", "should", "must", "may", "might", "shall", "not", "no", "yes", "its", "his", "her", "their", "our", "your", "than", "then", "when", "where", "what", "which", "who", "whom", "whose", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "only", "own", "same", "too", "very", "just", "also"}
    kw = [w for w in nk.split() if len(w) > 3 and w not in stop]
    if not kw:
        return 1.0 if nk in na else 0.0
    hit = sum(1 for w in kw if w in na)
    return 1.0 if hit / len(kw) >= 0.7 else 0.0

def main():
    print("M3 Retry Calibration: C1/C2 immediate recall")
    print("=" * 70)
    results = {}
    all_pass = True
    for arm, bar, gate in [("D", 0.95, "C1"), ("N", 0.90, "C2")]:
        print(f"\nArm {arm} ({gate} bar: >={bar:.2f}):")
        results[arm] = {}
        for s in range(1, 7):
            keys = load_keys(s)
            ans_path = RETRY / f"runs/{arm}_run1/probe_immediate_S{s}.txt"
            answers = [l[5:].strip() for l in ans_path.read_text().splitlines() if l.startswith("A || ")]
            if len(answers) != len(keys):
                print(f"  S{s}: MISMATCH ({len(answers)} answers, {len(keys)} keys)")
                all_pass = False
                continue
            scores = [score_answer(a, k) for a, (_, k) in zip(answers, keys)]
            acc = sum(scores) / len(scores)
            status = "PASS" if acc >= bar else "FAIL"
            if acc < bar:
                all_pass = False
            results[arm][s] = (acc, sum(scores), len(scores), status)
            print(f"  S{s}: {acc:.3f} ({int(sum(scores))}/{len(scores)}) [{status}]")
    print("\n" + "=" * 70)
    # Detail misses
    for arm in ["D", "N"]:
        print(f"\nArm {arm} misses:")
        for s in range(1, 7):
            keys = load_keys(s)
            ans_path = RETRY / f"runs/{arm}_run1/probe_immediate_S{s}.txt"
            answers = [l[5:].strip() for l in ans_path.read_text().splitlines() if l.startswith("A || ")]
            for (qid, key), ans in zip(keys, answers):
                if score_answer(ans, key) < 1.0:
                    print(f"  S{s} {qid}:")
                    print(f"    Key: {key[:100]}")
                    print(f"    Ans: {strip_m3_note(ans)[:100]}")
    print("\n" + "=" * 70)
    print("C1 (D):", "PASS" if all(results["D"][s][3]=="PASS" for s in range(1,7)) else "FAIL")
    print("C2 (N):", "PASS" if all(results["N"][s][3]=="PASS" for s in range(1,7)) else "FAIL")
    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())
