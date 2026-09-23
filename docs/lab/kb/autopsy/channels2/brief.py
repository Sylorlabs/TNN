#!/usr/bin/env python3
"""Writes out_tcp/verdict_brief.txt from scores_tcp.json (STEP 6 output)."""
import json, os

CHAN = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(CHAN, "scores_tcp.json")))
M = S["metrics"]
P = M["pooled"]
L = []
A = L.append

A("KB4 C2 TRANSFORM-CONSISTENCY PROBE — VERDICT BRIEF")
A("(prereg: kb/autopsy/channels2/PREREG_FROZEN_TCP.md; scorer: pure Zag, cross-checked)")
A("")
A("Two-run determinism check:")
A("  verdict lines byte-identical run1==run2 : %s" % S["two_run_check"]["verdict_lines_identical"])
A("  transform SHA256 lists identical      : %s" % S["two_run_check"]["transform_sha256_identical"])
A("Zag/Python count cross-check errors     : %d" % S["cross_check"]["n_errors"])
A("")
if S.get("void"):
    A("VOID: %s" % S["void"])
    open(os.path.join(CHAN, "out_tcp", "verdict_brief.txt"), "w").write("\n".join(L) + "\n")
    raise SystemExit
A("F3 calibration gate (primaries, P(C)>=0.95 => >=89/93):")
for s in ("A", "B"):
    fc = S["counts_full"]["sense"][s]
    pc = fc["calc"] / fc["caln"] if fc["caln"] else None
    A("  sense %s: cal P(C)=%s (%d/%d) -> %s" % (
        s, ("%.4f" % pc) if pc is not None else "n/a", fc["calc"],
        fc["caln"], "PASS" if S["F3"][s] else "FAIL -> VOID"))
A("")
A("Per-(sense,task) consistency:")
A("  sense task        cal_P(C)  test_P(C)  test_P(C|Y=1)  test_P(C|Y=0)   n  vacuous")
for s in ("A", "B"):
    for t in ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]:
        c = M["cells"]["%s/%s" % (s, t)]
        def f(x):
            return "  n/a " if x is None else "%6.3f" % x
        A("  %s     %-10s %s   %s      %s       %s    %3d  %s" % (
            s, t, f(c["cal_P_C"]), f(c["test_P_C"]), f(c["P_C_given_Y1"]),
            f(c["P_C_given_Y0"]), c["n"], "VACUOUS" if c["vacuous"] else ""))
A("")
A("Pooled TEST metrics (n=%d):" % P["n_test"])
def h(x, suffix=""):
    return ("%.4f" % x) + suffix if x is not None else "n/a"
A("  F1  pooled I(V;Y)            = %s bits  (champion frozen 0.1483; bar <=0.15 kills C2)" % h(P["bits"]))
A("  F2-primary pooled P(C|Y=0)   = %s  (bar >=0.70 fires)" % h(M["F2_primary"]))
A("  F2-A2 (non-vacuous cells)    = %s  (n_Y0=%d)" % (
    ("%.4f" % M["F2_A2"]) if M["F2_A2"] is not None else "n/a (all cells vacuous)",
    M["F2_A2_n"]))
A("  F4  pooled false-install     = %s  (bar >=0.15 kills C2)" % h(P["false_install_rate"]))
A("  pooled P(C)                  = %s" % h(P["P_C"]))
A("  pooled P(C|Y=1)              = %s" % h(P["P_C_given_Y1"]))
A("  pooled resolution accuracy   = %s" % h(P["resolution_accuracy"]))
A("  prior H(Y)                   = %s bits" % h(P["H_adv_correct"]))
A("")
A1 = M["A1"]
A("A1 stacking vs frozen (a)+(c) champion:")
A("  I((champion_vac, C2_v); Y) = %.4f bits" % A1["joint_bits"])
A("  frozen champion bits       = %.4f" % A1["champion_bits_frozen"])
A("  champion bits, same rows   = %.4f" % A1["champion_bits_same_rows"])
A("  incremental (vs frozen)    = %+.4f bits" % A1["incremental_bits"])
A("  incremental (vs same rows) = %+.4f bits" % A1["incremental_bits_same_rows"])
A("")
A("Per-sense TEST metrics:")
for s in ("A", "B"):
    q = M["sense"][s]
    if s in S["F3"]["voided_senses"]:
        A("  sense %s: VOID (F3 failed) — contributes nothing" % s)
        continue
    def g(x):
        return "n/a" if x is None else "%.4f" % x
    A("  sense %s: bits=%s  P(C|Y=0)=%s  false_install=%s  racc=%s" % (
        s, g(q["bits"]), g(q["P_C_given_Y0"]), g(q["false_install_rate"]), g(q["resolution_accuracy"])))
A("")
# §7 branch naming
f1_fire = P["bits"] <= 0.15
f2_fire = M["F2_primary"] is not None and M["F2_primary"] >= 0.70
f2a2_fire = M["F2_A2"] is not None and M["F2_A2"] >= 0.70
f4_fire = P["false_install_rate"] >= 0.15
f3a, f3b = M["sense"]["A"]["F3_pass"], M["sense"]["B"]["F3_pass"]
deploy = (P["bits"] > 0.15 and P["false_install_rate"] < 0.15
          and M["F2_primary"] is not None and M["F2_primary"] < 0.70 and f3a and f3b)
A("§7 BRANCH:")
if not (f3a and f3b):
    A("  F3 VOID: sense %s fails calibration gate — its TCP results are void; the other sense's results stand alone." %
      "/".join([s for s, ok in (("A", f3a), ("B", f3b)) if not ok]))
    A("  Branch on the remaining (non-void) results:")
if f2_fire and f2a2_fire:
    A("  F2 FIRES CLEANLY (§8-A2 satisfied: primary>=0.70 and A2>=0.70).")
    A("  -> abandon ALL judgment-side channels; all resources to C1-class channels.")
elif f2_fire and not f2a2_fire and M["F2_A2"] is not None:
    A("  F2 fires on VACUOUS CELLS ONLY: primary>=0.70 but A2<0.70.")
    A("  -> C2 killed on the technicality; family NOT retired; C3 mandatory; vacuous cells: %s" % M["vacuous_cells"])
elif M["F2_A2"] is None:
    A("  EVERY CELL VACUOUS: C2 void as a measurement; C3 decides.")
elif deploy:
    A("  C2 DEPLOYS: bits>0.15, false-install<0.15, F2<0.70, F3 passed.")
    A("  -> first deployable channel; scale toward C1.")
elif f1_fire:
    A("  F1 FIRES without F2 (bits<=0.15).")
    A("  -> C1 is the only remaining direction; C3 mandatory before retirement talk.")
    if f4_fire:
        A("  (F4 also fires: false-install>=0.15.)")
else:
    A("  NO CLEAN BRANCH: bits=%.4f, F2=%.4f, F4=%.4f — report to post-result debate." % (
        P["bits"], M["F2_primary"] if M["F2_primary"] is not None else -1, P["false_install_rate"]))
A("")
A("Post-result debate input: numbers above; TCP_VERDICT.md is NOT written by this probe.")

open(os.path.join(CHAN, "verdict_brief.txt"), "w").write("\n".join(L) + "\n")
print("\n".join(L))
