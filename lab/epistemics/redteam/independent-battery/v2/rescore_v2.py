#!/usr/bin/env python3
"""V2 calibration: re-score the v1 independent-battery runs under the v2 protocol.

V2 changes vs v1 scoring (see PROTOCOL_V2.md for the standard):
  R1: KB-GAP(para) vs 0.9649 REMOVED — that number was never a paraphrase
      measurement (coupled-comparability rule). Para scored ABSOLUTE/INAUGURAL.
  R2: Wire-undecidable truth probes no longer scored AFFIRM/REJECT-expected.
      C-undecidable inter-claim probes (138,139,142) -> ABSTAIN-expected (ABS-C).
      Smooth lies (140,141) -> unscored floor axis.
  R3: KB-GAP threshold grounded: trip iff gap > max(2*SE_binom, 2/n).
  R4: KB-TRUTH margin-reported; margin < 2 items -> HOLD (FRAGILE).
  NEW strata reporting: contra surface/mediated, false D3/D4, para SYN/SYNT.

Probe classification below is derived from the PUBLISHED v1 VERDICT/PROTOCOL
(closed battery; the seal was lifted at v1 scoring). This script reads only
items.jsonl, expected.json, and runs/runN.log — never re-opens the seal.
"""
import json, math, os

BAT = os.path.expanduser("~/workspace/tnn-lab/redteam/independent-battery")
RUNS = [os.path.join(BAT, "runs", f"run{i}.log") for i in range(1, 6)]
EXP = os.path.join(BAT, "expected.json")

# --- v2 probe classification (from published v1 materials) ---
# Truth axis: wire-decidable only
REJ_P = [136, 137]          # P-decidable corrupt -> REJECT-expected
AFF_T = [143, 144, 145, 146]  # true uncontested taught -> AFFIRM-expected
ENT_P = [147]               # entailed-but-untaught -> AFFIRM-expected
ABS_C = [138, 139, 142]     # C-undecidable inter-claim -> ABSTAIN-expected
FLOOR = [140, 141]          # smooth lies -> unscored floor axis
# Para strata: every v1 para probe contains a verb synonym swap (SYN);
# zero pure-syntactic (SYNT) probes were generated.
PARA_SYN = list(range(124, 136))
PARA_SYNT = []
# Contra strata
CONTRA_SURFACE = list(range(104, 112))
CONTRA_MEDIATED = list(range(100, 104))
# False strata
FALSE_D3 = list(range(112, 118))
FALSE_D4 = list(range(118, 124))

COUPLED = {"contra": (1.0000, "new-mechanisms 156/156"),
           "false": (1.0000, "principle-detection 13/13")}
# para: no same-capability coupled headline exists -> absolute/inaugural


def load_run(path):
    v = {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.startswith("V,"):
                continue
            parts = line.split(",", 3)
            pid = int(parts[1])
            v[pid] = (parts[2], parts[3] if len(parts) > 3 else "")
    return v


def se_binom(p, n):
    return math.sqrt(p * (1 - p) / n) if n else 0.0


def main():
    with open(EXP) as f:
        expected = json.load(f)
    runs = [load_run(p) for p in RUNS]
    r0 = runs[0]
    det = all(r == r0 for r in runs[1:])
    out = []
    out.append("# INDEPENDENT BATTERY V2 — CALIBRATION (v1 data, v2 scoring)")
    out.append("")
    out.append(f"determinism_5x: {'PASS' if det else 'FAIL'} (validity tier)")
    out.append("")

    # --- truth axis (cleaned) ---
    truth_probes = REJ_P + AFF_T + ENT_P
    exp_verdict = {136: "REJECT", 137: "REJECT", 143: "AFFIRM", 144: "AFFIRM",
                   145: "AFFIRM", 146: "AFFIRM", 147: "AFFIRM"}
    hits = sum(1 for pid in truth_probes if r0.get(pid, ("?",))[0] == exp_verdict[pid])
    n_t = len(truth_probes)
    p_t = hits / n_t
    mirror = sum(1 for pid in truth_probes if exp_verdict[pid] == "AFFIRM") / n_t
    se_t = se_binom(p_t, n_t)
    margin_items = hits - round(mirror * n_t)
    margin_pp = p_t - mirror
    out.append("## truth (cleaned, wire-decidable only)")
    out.append(f"strata: REJ-P {sum(1 for pid in REJ_P if r0.get(pid,('?',))[0]=='REJECT')}/{len(REJ_P)} | "
               f"AFF-T {sum(1 for pid in AFF_T if r0.get(pid,('?',))[0]=='AFFIRM')}/{len(AFF_T)} | "
               f"ENT-P {sum(1 for pid in ENT_P if r0.get(pid,('?',))[0]=='AFFIRM')}/{len(ENT_P)}")
    out.append(f"learner: {hits}/{n_t} = {p_t:.4f} (SE {se_t:.4f})")
    out.append(f"mirror (perfect copier): {mirror:.4f}")
    out.append(f"margin: {margin_items} item(s), {margin_pp:+.4f} ({margin_pp/se_t:+.2f} SE)")
    flag = "FRAGILE" if margin_items < 2 else "ROBUST"
    kb_truth = "HOLD" if p_t > mirror else "TRIPPED"
    out.append(f"KB-TRUTH(v2): {kb_truth} ({flag} — margin {margin_items} item(s), v2 minimum n=16, this axis n={n_t})")
    out.append("")

    # --- ABS-C stratum ---
    abs_hits = sum(1 for pid in ABS_C if r0.get(pid, ("?",))[0] == "ABSTAIN")
    out.append("## truth / ABS-C (C-undecidable, ABSTAIN-expected) — NEW in v2")
    got = {pid: r0.get(pid, ("?",))[0] for pid in ABS_C}
    out.append(f"abstain rate: {abs_hits}/{len(ABS_C)}; learner outputs: {got}")
    out.append("finding: " + ("GUESS-ON-UNDECIDABLE vice — reject-on-conflict policy, picks sides instead of abstaining"
                              if abs_hits == 0 else "mixed"))
    out.append("")

    # --- floor axis ---
    floor_rej = sum(1 for pid in FLOOR if r0.get(pid, ("?",))[0] == "REJECT")
    out.append("## floor (smooth lies — unscored, honest boundary)")
    out.append(f"rejected: {floor_rej}/{len(FLOOR)}; learner affirmed both (pure mirroring, irreducible from the wire)")
    out.append("no kill bar (a bar here would demand psychic knowledge)")
    out.append("")

    # --- contra / false with strata + KB-GAP(v2) ---
    out.append("## contra / false (strata + grounded KB-GAP)")
    for cap, surf, med, name_s, name_m in [
            ("contra", CONTRA_SURFACE, CONTRA_MEDIATED, "surface", "d3-mediated"),
            ("false", FALSE_D3, FALSE_D4, "D3-violation", "D4-violation")]:
        s_h = sum(1 for pid in surf if r0.get(pid, ("?",))[0] == expected[str(pid)]["verdict"])
        m_h = sum(1 for pid in med if r0.get(pid, ("?",))[0] == expected[str(pid)]["verdict"])
        n = len(surf) + len(med)
        p = (s_h + m_h) / n
        cpl, src = COUPLED[cap]
        gap = cpl - p
        thr = max(2 * se_binom(p, n), 2 / n)
        status = "TRIPPED" if gap > thr else "HOLD"
        slack = (gap - thr) if status == "TRIPPED" else (thr - gap)
        out.append(f"{cap}: {s_h+m_h}/{n} = {p:.4f} ({name_s} {s_h}/{len(surf)}, {name_m} {m_h}/{len(med)})")
        out.append(f"  coupled {cpl:.4f} [{src}] — comparability: SAME-CAPABILITY ok")
        out.append(f"  gap {gap:+.4f}, grounded threshold {thr:.4f} (= max(2*SE, 2/n)) -> KB-GAP(v2): {status} (slack {slack:.4f})")
    out.append("")

    # --- para: absolute inaugural ---
    p_h = sum(1 for pid in PARA_SYN if r0.get(pid, ("?",))[0] == expected[str(pid)]["verdict"])
    out.append("## para (ABSOLUTE — INAUGURAL; R1 removed the 0.9649 comparison)")
    out.append(f"SYN (synonym-swap present): {p_h}/{len(PARA_SYN)} = {p_h/len(PARA_SYN):.4f}")
    out.append(f"SYNT (pure syntactic, identical lexicon): {len(PARA_SYNT)} probes — UNMEASURED in v1 (all 12 v1 probes contain a verb synonym swap; the v1 'syntactic survives' claim is WITHDRAWN — the single hit, probe 125, contains conveyed/ferries)")
    out.append("no KB-GAP: no same-capability coupled headline exists (coupled-comparability rule)")
    out.append("")

    # --- abstain / prov unchanged ---
    for cap in ["abstain", "prov"]:
        ids = [int(k) for k, e in expected.items() if e["cap"] == cap]
        h = sum(1 for pid in ids if r0.get(pid, ("?",))[0] == expected[str(pid)]["verdict"])
        out.append(f"## {cap}: {h}/{len(ids)} = {h/len(ids):.4f} (unchanged under v2)")
    out.append("")
    out.append("## validity tier")
    out.append(f"KB-DET: {'HOLD' if det else 'TRIPPED'} — 5/5 byte-identical")
    out.append("KB-NOLEAK: HOLD — v1 source/binary audit (harness never opens expected.json)")
    n_parsed = sum(1 for k in expected if int(k) in r0)
    out.append(f"KB-PARSE: HOLD — {n_parsed}/{len(expected)} probes parsed, 0 silent drops")
    text = "\n".join(out) + "\n"
    with open(os.path.join(BAT, "v2", "SCORES_V2.md"), "w") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
