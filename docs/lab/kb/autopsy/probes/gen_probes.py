#!/usr/bin/env python3
"""KB4 autopsy probe batch generators (harness-side; the gates are pure Zag).

Reads the frozen kb4_rerun truth.json (scorer-side truth; the probe gates
never see correctness — only stim/judgment/confidence/variant fields).

P-A1 (cross-sense corroboration): combined batch over the 924 common
  (stim, variant) keys present in BOTH approaches:
    stim_idx \t judgA_idx \t judgB_idx \t confidence \t variant
  variant: 0=primary, 1=noise, 2=adversarial. stim/judg IDs reuse the frozen
  mappings.json. Confidence: A's (the field is unscored; kept for format).
  Gate never sees 'correct'.

P-A2 (variant-split stimulus binding): per-approach batches with the
  stimulus slot re-keyed as slot = stim_idx*3 + variant_id, so an
  adversarial judgment NEVER "conflicts" with the primary judgment — each
  (stimulus, perturbation) pair is its own epistemic item. The gate binary
  is bit-identical logic to kb4_gate.zag; only the representation changed.
  Format unchanged: slot \t judg_idx \t confidence \t source_id,
  run with nstim = 370*3 = 1110.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RERUN = "/home/hatch/workspace/tnn-lab/prose-learning/epistemic_wave/kb4_rerun"
VARID = {"primary": 0, "noise": 1, "adversarial": 2}

def main():
    truth = json.load(open(os.path.join(RERUN, "truth.json")))
    mappings = json.load(open(os.path.join(RERUN, "mappings.json")))
    stim_name_to_idx = {v: int(k) for k, v in mappings["stimuli"].items()}
    judg_name_to_idx = {v: int(k) for k, v in mappings["judgments"].items()}

    A, B = {}, {}
    for k, v in truth.items():
        tag, _ = k.split("/")
        key = (v["stim"], v["variant"])
        (A if tag == "A" else B)[key] = v
    common = sorted(set(A) & set(B))
    print("common (stim,variant) keys:", len(common))

    # ---- P-A1 combined batch ----
    lines = []
    pa1_truth = {}  # line_no -> {stim, variant, a_correct, b_correct, agree...}
    for ln, key in enumerate(common):
        a, b = A[key], B[key]
        s = stim_name_to_idx[a["stim"]]
        ja = judg_name_to_idx[a["judgment"]]
        jb = judg_name_to_idx[b["judgment"]]
        vr = VARID[a["variant"]]
        lines.append("%d\t%d\t%d\t%d\t%d" % (s, ja, jb, a["confidence"], vr))
        pa1_truth[str(ln)] = {
            "stim": a["stim"], "variant": a["variant"],
            "a_correct": a["correct"], "b_correct": b["correct"],
            "agree": a["judgment"] == b["judgment"],
            # adversarial truth for scoring: installed judgment is the
            # agreed one; correct iff both correct (they agree by install)
            "adv_correct": a["correct"] and b["correct"],
        }
    open(os.path.join(HERE, "pbatch_pa1.txt"), "w").write("\n".join(lines) + "\n")
    json.dump(pa1_truth, open(os.path.join(HERE, "pa1_truth.json"), "w"), indent=1)
    print("pbatch_pa1.txt:", len(lines), "lines")

    # ---- P-A2 re-slotted batches (per approach) ----
    for tag, D in (("A", A), ("B", B)):
        # keep the frozen per-approach line order: rebuild from truth keys
        tkeys = sorted([k for k in truth if k.startswith(tag + "/")],
                       key=lambda k: int(k.split("/")[1]))
        lines = []
        for k in tkeys:
            v = truth[k]
            slot = stim_name_to_idx[v["stim"]] * 3 + VARID[v["variant"]]
            j = judg_name_to_idx[v["judgment"]]
            lines.append("%d\t%d\t%d\t1" % (slot, j, v["confidence"]))
        open(os.path.join(HERE, "pbatch_pa2_%s.txt" % tag), "w").write(
            "\n".join(lines) + "\n")
        print("pbatch_pa2_%s.txt:" % tag, len(lines), "lines, 1110 slots")

if __name__ == "__main__":
    main()
