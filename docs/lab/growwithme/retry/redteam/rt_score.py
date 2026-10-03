#!/usr/bin/env python3
"""INDEPENDENT re-scoring of the M3 retry gate table (Crew 3 red team).
Written from the rubric description alone (70% distinctive-word overlap),
not from Crew 2's scorer. Runs against Crew 3's own fresh run outputs.
"""
import re, pathlib, sys

REPRO = pathlib.Path.home() / "workspace/growwithme_retry/redteam/repro"
RESEAL = pathlib.Path.home() / "workspace/growwithme_retry/redteam/docs/lab/growwithme/retry/probes_resealed"

STOP = set("""the and for with from that this are was were has have had will would can could
should must may might shall not no yes its his her their our your than then when where what which
who whom whose why how all any both each few more most other some such only own same too very just also
a an of to in on is it as at be by or if do does did""".split())

def load_keys(session):
    text = (RESEAL / f"immediate_S{session}.md").read_text()
    out = []
    for m in re.finditer(r"### (\S+)\nQ: .*?\nKey: (.*?)\n", text, re.DOTALL):
        out.append((m.group(1), m.group(2).split("\n")[0].strip()))
    return out

def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def strip_note(a):
    return re.sub(r"\s*\[m3:.*?\]\s*$", "", a).strip()

def score(ans, key):
    na, nk = norm(strip_note(ans)), norm(key)
    if nk in na or na in nk:
        return True
    kw = [w for w in nk.split() if len(w) > 3 and w not in STOP]
    if not kw:
        return nk in na
    return sum(1 for w in kw if w in na) / len(kw) >= 0.70

def main():
    grand_ok = True
    for arm, bar, gate in (("D", 0.95, "C1"), ("N", 0.90, "C2")):
        print(f"Arm {arm} ({gate} >= {bar}):")
        arm_ok = True
        for s in range(1, 7):
            keys = load_keys(s)
            lines = (REPRO / f"{arm}_rt1/probe_immediate_S{s}.txt").read_text().splitlines()
            ans = [l[5:].strip() for l in lines if l.startswith("A || ")]
            assert len(ans) == len(keys) == 18, f"S{s}: {len(ans)} vs {len(keys)}"
            hits = sum(1 for a, (_, k) in zip(ans, keys) if score(a, k))
            acc = hits / 18
            ok = acc >= bar
            arm_ok &= ok
            print(f"  S{s}: {hits}/18 = {acc:.3f} [{'PASS' if ok else 'FAIL'}]")
        print(f"  => {gate}: {'PASS' if arm_ok else 'FAIL'}")
        grand_ok &= arm_ok
    print("OVERALL:", "PASS" if grand_ok else "FAIL (VOID)")
    return 0 if grand_ok else 1

sys.exit(main())
