#!/usr/bin/env python3
"""PACKAGE 2 glue: prepare frozen channel-shootout inputs from the corpus.

Reads: prose-learning/epistemic_wave/kb4_rerun/{truth.json,mappings.json},
       kb/autopsy/SPLIT_MANIFEST.json
Writes (kb/autopsy/channels/inputs/):
  stimclass.txt   stim_idx \t class_idx (0=colordisc 1=colorconst 2=shapetrans
                  3=pitchdisc 4=timbredisc 5=motiondir)
  split.txt       stim_idx \t 0=CALIBRATION 1=TEST 2=unused(no adversarial fixture)
  variant_A.txt   line_no \t variant (0=primary 1=noise 2=adversarial), sense A
  variant_B.txt   same, sense B
  calrows_A.txt   calibration adversarial fixtures, sense A:
                  stim_idx \t class \t agree(Ja==Jp) \t conf_a \t conf_p
                  \t preserved(adv truth==prim truth) \t correct(Ja)
                  \t pcorrect(Jp)
  calrows_B.txt   same, sense B

ANTI-GAMING: only the variant field (structural) is taken from truth.json
for the variant maps; correct/truth columns are emitted ONLY for
calibration-split rows. No test truth is written anywhere.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, "..", "..", "prose-learning", "epistemic_wave", "kb4_rerun")
CORPUS = os.path.normpath(CORPUS)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inputs")
CLASSES = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
CIX = {c: i for i, c in enumerate(CLASSES)}
VIX = {"primary": 0, "noise": 1, "adversarial": 2}

def main():
    os.makedirs(OUT, exist_ok=True)
    truth = json.load(open(os.path.join(CORPUS, "truth.json")))
    man = json.load(open(os.path.join(ROOT, "SPLIT_MANIFEST.json")))

    split = {}   # (task, stim_idx) -> 0/1
    for task in CLASSES:
        for s in man["calibration"][task]:
            split[(task, s)] = 0
        for s in man["test"][task]:
            split[(task, s)] = 1

    # per sense: line_no -> record; per (sense, stim) per variant -> record
    rec = {}     # (sense, line_no) -> v
    per = {}     # (sense, stim_idx, variant) -> v
    for k, v in truth.items():
        sense, ln = k.split("/")
        ln = int(ln)
        rec[(sense, ln)] = v
        per[(sense, v["stim_idx"], v["variant"])] = v

    with open(os.path.join(OUT, "stimclass.txt"), "w") as f:
        for s in sorted({v["stim_idx"] for v in truth.values()}):
            task = next(v["task"] for v in truth.values() if v["stim_idx"] == s)
            f.write("%d\t%d\n" % (s, CIX[task]))
    with open(os.path.join(OUT, "split.txt"), "w") as f:
        for s in sorted({v["stim_idx"] for v in truth.values()}):
            task = next(v["task"] for v in truth.values() if v["stim_idx"] == s)
            f.write("%d\t%d\n" % (s, split.get((task, s), 2)))

    nlines = {}
    for sense in ("A", "B"):
        nlines[sense] = max(ln for (se, ln) in rec if se == sense) + 1
        with open(os.path.join(OUT, "variant_%s.txt" % sense), "w") as f:
            for ln in range(nlines[sense]):
                f.write("%d\t%d\n" % (ln, VIX[rec[(sense, ln)]["variant"]]))

    for sense in ("A", "B"):
        rows = []
        for k, v in truth.items():
            se, _ = k.split("/")
            if se != sense or v["variant"] != "adversarial":
                continue
            if split.get((v["task"], v["stim_idx"])) != 0:
                continue
            p = per[(sense, v["stim_idx"], "primary")]
            agree = 1 if v["judg_idx"] == p["judg_idx"] else 0
            pres = 1 if v["truth"] == p["truth"] else 0
            rows.append((v["stim_idx"], CIX[v["task"]], agree,
                         v["confidence"], p["confidence"], pres,
                         1 if v["correct"] else 0, 1 if p["correct"] else 0))
        rows.sort()
        with open(os.path.join(OUT, "calrows_%s.txt" % sense), "w") as f:
            for r in rows:
                f.write("\t".join(map(str, r)) + "\n")
        print("calrows_%s: %d rows" % (sense, len(rows)))

    # sanity: every TEST adversarial fixture must have a noise line, same sense
    nbad = 0
    for k, v in truth.items():
        se, _ = k.split("/")
        if v["variant"] != "adversarial":
            continue
        if split.get((v["task"], v["stim_idx"])) != 1:
            continue
        if (se, v["stim_idx"], "noise") not in per:
            nbad += 1
            print("MISSING noise", k)
    print("test adv fixtures missing noise:", nbad)
    assert nbad == 0
    print("inputs written to", OUT)

if __name__ == "__main__":
    main()
