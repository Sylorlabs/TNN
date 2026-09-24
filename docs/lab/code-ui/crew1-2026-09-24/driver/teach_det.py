#!/usr/bin/env python3
"""Teaching determinism experiment (T1).

Runs the full teach phase TWICE from identical pristine card snapshots
and compares every byte: consult.log, results.json, and final card state.

Pristine = cards as frozen before the real teaching run (template
corrections applied, but WITHOUT the teaching-installed LEARN lines
fieldbang=! and nonnull=!).

Steps:
  1. Snapshot current (learned) cards -> cards_learned_snapshot/
  2. Strip the two LEARN lines -> pristine
  3. run.py teach -> save run A (consult.log, results.json, cards)
  4. Restore pristine
  5. run.py teach -> save run B
  6. Byte-compare A vs B; report SHA-256s
  7. Restore learned cards (from step 1)

Usage: teach_det.py   (run from ts-teaching/)
"""
import os, shutil, subprocess, hashlib, sys, json

ROOT = os.path.expanduser("~/workspace/code-ui/ts-teaching")
EXP = ROOT + "/runlog/teach_det"
LEARN_LINES = {"U4-classes.card": "fieldbang=!\n",
               "U6-dom.card": "nonnull=!\n"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def strip_learn(card):
    p = os.path.join(ROOT, "cards", card)
    t = open(p).read()
    line = LEARN_LINES.get(card, "")
    if line and ("## LEARNED\n" + line) in t:
        t = t.replace("## LEARNED\n" + line, "## LEARNED\n", 1)
        open(p, "w").write(t)
        return True
    return False


def snap_cards(dest):
    d = os.path.join(EXP, dest)
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)
    for c in sorted(os.listdir(ROOT + "/cards")):
        shutil.copy(ROOT + "/cards/" + c, d + "/" + c)
    return d


def run_teach(tag):
    d = os.path.join(EXP, tag)
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)
    p = subprocess.run(["python3", "-u", ROOT + "/driver/run.py", "teach"],
                       capture_output=True, text=True, cwd=ROOT + "/driver")
    open(d + "/driver.out", "w").write(p.stdout + p.stderr)
    if p.returncode != 0:
        print("teach %s FAILED rc=%d" % (tag, p.returncode))
        print(p.stdout[-2000:] + p.stderr[-2000:])
        sys.exit(1)
    for f in ("consult.log", "results.json"):
        shutil.copy(ROOT + "/runlog/teach/" + f, d + "/" + f)
    snap_cards(tag + "_cards")
    print("teach %s done" % tag)


def main():
    if os.path.exists(EXP):
        shutil.rmtree(EXP)
    os.makedirs(EXP)
    # 1. snapshot learned state
    snap_cards("cards_learned_snapshot")
    print("learned snapshot saved")
    # 2. pristine
    for c in ("U4-classes.card", "U6-dom.card"):
        assert strip_learn(c), "learn line not found in " + c
    print("cards reset to pristine")
    snap_cards("cards_pristine")
    # 3-5. two teach runs
    run_teach("runA")
    for c in ("U4-classes.card", "U6-dom.card"):
        assert strip_learn(c), "learn line not found in " + c + " (runB reset)"
    run_teach("runB")
    # 6. compare
    files = ["consult.log", "results.json"]
    all_same = True
    for f in files:
        a, b = EXP + "/runA/" + f, EXP + "/runB/" + f
        same = open(a, "rb").read() == open(b, "rb").read()
        print("%s identical: %s  shaA=%s shaB=%s" %
              (f, same, sha(a)[:16], sha(b)[:16]))
        all_same = all_same and same
    ca = sorted(os.listdir(EXP + "/runA_cards"))
    for c in ca:
        same = open(EXP + "/runA_cards/" + c, "rb").read() == \
            open(EXP + "/runB_cards/" + c, "rb").read()
        if not same:
            print("CARD DIFFERS:", c)
            all_same = False
    print("all card states identical:", all_same)
    print("OVERALL:", "DETERMINISTIC" if all_same else "NONDETERMINISM FOUND")
    # 7. restore learned cards
    for c in sorted(os.listdir(EXP + "/cards_learned_snapshot")):
        shutil.copy(EXP + "/cards_learned_snapshot/" + c, ROOT + "/cards/" + c)
    print("learned cards restored")
    # also restore the canonical teach runlog from runA (identical to runB)
    for f in ("consult.log", "results.json"):
        shutil.copy(EXP + "/runA/" + f, ROOT + "/runlog/teach/" + f)
    json.dump({"deterministic": all_same,
               "sha_consult": sha(EXP + "/runA/consult.log"),
               "sha_results": sha(EXP + "/runA/results.json")},
              open(EXP + "/verdict.json", "w"), indent=1)


if __name__ == "__main__":
    main()
