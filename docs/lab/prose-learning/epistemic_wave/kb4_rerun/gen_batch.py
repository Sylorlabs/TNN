#!/usr/bin/env python3
"""KB4 §4(a) — batch file generator.

Reads the frozen raw_results.json. Emits, per approach, a batch file for the
deliberative install gate with lines:
    stim_idx \t judg_idx \t confidence \t source_id

- stim_idx: deterministic integer per (task, logical fixture). The logical
  fixture strips the variant path: "t1_colordisc/adversarial/p000.img" ->
  ("colordisc","p000"). Same stimulus across variants shares the index,
  which is what the §6 L4/L8 contract requires.
- judg_idx: deterministic integer per judgment string.
- Order: the raw file order — per (approach,task): primary fixtures in
  order, then noise, then adversarial. This is the frozen file order and
  the order the §6 contract assumes (earlier variants establish the
  endorsed judgment; later variants are checked against it).
- source_id: 1 (single sense per run).
- NO ground truth in the batch. Truth is emitted separately for scoring.

Also emits:
  truth.json — {(approach, stim_idx, line_no): {truth, correct, variant, ...}}
  mappings.json — idx -> label maps.
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = "/home/hatch/workspace/tnn-lab/senses/rebuild/harness/results/raw_results.json"
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
VARIANTS = ["primary", "noise", "adversarial"]

def logical_fixture(task, fixture_path):
    # "t1_colordisc/adversarial/p000.img" -> "p000"
    base = fixture_path.rsplit("/", 1)[-1]
    if base.endswith(".img"):
        base = base[:-4]
    return "%s/%s" % (task, base)

def main():
    with open(SRC) as f:
        data = json.load(f)
    runs = data["runs"]

    # deterministic ID assignment in first-seen order over the frozen file order
    stim_id = {}
    judg_id = {}
    def sid(task, fx):
        k = logical_fixture(task, fx)
        if k not in stim_id:
            stim_id[k] = len(stim_id)
        return stim_id[k]
    def jid(j):
        if j not in judg_id:
            judg_id[j] = len(judg_id)
        return judg_id[j]

    truth = {}
    for tag in ("A", "B"):
        # frozen file order: JSON order filtered to approach, which is
        # per task: primary, noise, adversarial (see survey).
        ar = [r for r in runs if r["approach"] == tag]
        lines = []
        for ln, r in enumerate(ar):
            s = sid(r["task"], r["fixture"])
            j = jid(r["judgment"])
            lines.append("%d\t%d\t%d\t1" % (s, j, r["confidence"]))
            truth["%s/%d" % (tag, ln)] = {
                "stim": logical_fixture(r["task"], r["fixture"]),
                "stim_idx": s, "judg_idx": j,
                "truth": r["truth"], "correct": r["correct"],
                "variant": r["variant"], "task": r["task"],
                "judgment": r["judgment"], "confidence": r["confidence"],
            }
        with open(os.path.join(ROOT, "batch_%s.txt" % tag), "w") as f:
            f.write("\n".join(lines) + "\n")
        print("batch_%s.txt: %d lines, %d stimuli" % (tag, len(lines), len(stim_id)))

    with open(os.path.join(ROOT, "truth.json"), "w") as f:
        json.dump(truth, f, indent=1)
    with open(os.path.join(ROOT, "mappings.json"), "w") as f:
        json.dump({
            "stimuli": {v: k for k, v in stim_id.items()},
            "judgments": {v: k for k, v in judg_id.items()},
        }, f, indent=1)
    print("stimuli:", len(stim_id), "judgments:", len(judg_id))

if __name__ == "__main__":
    main()
