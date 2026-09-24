#!/usr/bin/env python3
"""CRITIC 4 (anti-servo-gate): generate X (MEE) and XY (X + veto-feed) sources
from the VERIFIED gated source (byte-identical to crew_servo's committed
render_c_gated.zag, SHA c1eca96a...). All edits are exact string replacements
with occurrence asserts."""
import os

BASE = os.path.expanduser("~/workspace/par_critics/anti_servo/src")

def rep(src, old, new, name):
    n = src.count(old)
    assert n == 1, "%s: anchor found %d times" % (name, n)
    return src.replace(old, new)

gated = open(os.path.join(BASE, "render_c_gated.zag")).read()

# ---------- X: model-error exclusion (MEE) ----------
x = gated
x = rep(x,
        "        let ghyst:i64 = 0;  // fable tier-2: blocks remaining in minimum-active\n",
        "        let ghyst:i64 = 0;  // fable tier-2: blocks remaining in minimum-active\n"
        "        let Tprev:i64 = 0;  // CRITIC4-X: previous-block plan target (slew evidence)\n",
        "x-state")
x = rep(x,
        "        // st: 0 idle (deadband) | 1 adapt | 2 veto-re-measure | 3 silence-hold\n"
        "        let st:i64 = 0;\n",
        "        // st: 0 idle (deadband) | 1 adapt | 2 veto-re-measure | 3 silence-hold\n"
        "        let st:i64 = 0;\n"
        "        let slew_ok:i64 = 1; // CRITIC4-X: 1 = block is gate evidence\n",
        "x-stdecl")
x = rep(x,
        "                if (veto == 0) {\n"
        "                    if (gs == 0) {\n",
        "                // CRITIC4-X (MEE): model-error exclusion. If the plan\n"
        "                // model itself slewed by more than the deviation\n"
        "                // threshold within one block, the block's analytic T\n"
        "                // is not trustworthy evidence (attack/release model\n"
        "                // error). Same treatment as vetoed blocks: the open/\n"
        "                // close counters are neither incremented nor reset.\n"
        "                // No new constant: reuses GATE_DEV_PC (15%).\n"
        "                // (slew_ok declared at block scope above; Tprev is\n"
        "                // region-scoped gate state.)\n"
        "                slew_ok = 1;\n"
        "                if (veto == 0) {\n"
        "                    let tmax:i64 = T;\n"
        "                    if (Tprev > tmax) { tmax = Tprev; }\n"
        "                    if (tmax > 0) {\n"
        "                        let tslew:i64 = T - Tprev;\n"
        "                        if (tslew < 0) { tslew = 0 - tslew; }\n"
        "                        if (tslew * 100 > GATE_DEV_PC * tmax) { slew_ok = 0; }\n"
        "                    }\n"
        "                }\n"
        "                Tprev = T;\n"
        "                if (veto == 0 && slew_ok == 1) {\n"
        "                    if (gs == 0) {\n",
        "x-fsm")
x = rep(x,
        '        pout(" gs=");\n        pout(i64s(gs));\n        pout("\\n");\n',
        '        pout(" gs=");\n        pout(i64s(gs));\n        pout(" ts=");\n        pout(i64s(slew_ok));\n        pout("\\n");\n',
        "x-trace")
open(os.path.join(BASE, "render_c_x.zag"), "w").write(x)

# ---------- XY: X + veto-feed (parked §5.1 follow-up, design comparison) ----------
# XY v2 (2026-09-24): the veto-feed must feed X's FULL FSM (MEE included).
# v1 skipped the slew computation on vetoed blocks (slew_ok defaulted to 1),
# so vetoed blocks ran a gated-style FSM without model-error exclusion —
# XY-sus1292 replayed the GATED-clean trajectory (0.36 dsum) instead of the
# X-clean one (0.00). v2 computes slew on every non-silence block (T is
# plan-derived, well-defined under veto) and feeds vetoed blocks through
# the same MEE-qualified FSM. X itself is unchanged (vetoed blocks skipped).
xy = x
xy = rep(xy,
         "                slew_ok = 1;\n"
         "                if (veto == 0) {\n"
         "                    let tmax:i64 = T;\n"
         "                    if (Tprev > tmax) { tmax = Tprev; }\n"
         "                    if (tmax > 0) {\n"
         "                        let tslew:i64 = T - Tprev;\n"
         "                        if (tslew < 0) { tslew = 0 - tslew; }\n"
         "                        if (tslew * 100 > GATE_DEV_PC * tmax) { slew_ok = 0; }\n"
         "                    }\n"
         "                }\n"
         "                Tprev = T;\n",
         "                // CRITIC4-XY v2: slew is plan-derived (T), so it is\n"
         "                // well-defined on vetoed blocks too — compute it\n"
         "                // unconditionally so the veto-feed runs X's full\n"
         "                // FSM (MEE included), not a gated-style bypass.\n"
         "                slew_ok = 1;\n"
         "                let tmax:i64 = T;\n"
         "                if (Tprev > tmax) { tmax = Tprev; }\n"
         "                if (tmax > 0) {\n"
         "                    let tslew:i64 = T - Tprev;\n"
         "                    if (tslew < 0) { tslew = 0 - tslew; }\n"
         "                    if (tslew * 100 > GATE_DEV_PC * tmax) { slew_ok = 0; }\n"
         "                }\n"
         "                Tprev = T;\n",
         "xy-slew")
xy = rep(xy,
         "                if (veto == 0 && slew_ok == 1) {\n"
         "                    if (gs == 0) {\n",
         "                // CRITIC4-XY: veto-feed (parked §5.1 follow-up, DESIGN\n"
         "                // COMPARISON ONLY — the law 'vetoed blocks are not\n"
         "                // evidence' stands until Micah's word). The veto\n"
         "                // re-measures the block's plan-pure render bit-exactly\n"
         "                // (render_block_tmp + same integer scaling), so the\n"
         "                // dev on vetoed blocks is clean evidence: feed it to\n"
         "                // the FSM instead of skipping vetoed blocks. v3:\n"
         "                // the veto only changes WHERE dev comes from\n"
         "                // (bit-exact remeasure); MEE (slew_ok) applies to\n"
         "                // vetoed blocks exactly as to clean ones.\n"
         "                if (slew_ok == 1) {\n"
         "                    if (gs == 0) {\n",
         "xy-fsm")
open(os.path.join(BASE, "render_c_xy.zag"), "w").write(xy)

print("wrote X and XY")
for v in ["render_c_x.zag", "render_c_xy.zag"]:
    print(v, os.path.getsize(os.path.join(BASE, v)), "bytes")
