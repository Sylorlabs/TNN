#!/usr/bin/env python3
"""Crew SERVO: generate the three variant sources from the verified stock source.
All edits are exact string replacements; the script asserts each anchor occurs
exactly once. Variants:
  render_c_off.zag    - SERVO_OFF=1: adapt+veto fully disabled (PAR-equivalent)
  render_c_gated.zag  - primary necessity gate (15% / 3 blocks / 10-clear)
  render_c_gfable.zag - fable R1 challenger (tier-1a pre-engage + 20-min hyst)
"""
import sys, os

BASE = os.path.expanduser("~/workspace/tnn-lab/bytegen/par_tournament/crew_servo/src")
FROZEN = os.path.expanduser("~/workspace/tnn-lab/bytegen/par_dive/contender_c/src/render_c.zag")
# Base is ALWAYS the frozen pristine source (SHA 0640f28f...); add_common adds
# only the test-only fault modes (sawbomb/edge14), which are inert for all
# other modes (verified bit-identical on the fixture).
# (stock generation happens after add_common is defined, below)

def rep(src, old, new, name):
    n = src.count(old)
    assert n == 1, "%s: anchor found %d times" % (name, n)
    return src.replace(old, new)

# ---------- common: sawbomb + edge14 test modes ----------
SAWBOMB = '''
        // TEST-ONLY fault modes (crew SERVO):
        // sawbomb: sawtooth corruption bomb (fable R1 adv plan 3): alternate
        //   blocks x2.38 / x1.05 rendered amplitude over t=[10,20)s.
        //   x2.38 -> m/T=2.38 sits JUST under the 2.5 veto line: no veto fires.
        // edge14: sustained sub-gate exploitation: EVERY block x1.14 over
        //   t=[10,20)s -> dev=14% sustained: stock adapts (14>10), the gate
        //   deliberately ignores it (14<15). Documents the residual-blindness
        //   tradeoff (same family as stock's 10% deadband blindness).
        if (str_eq(mode, "sawbomb") || str_eq(mode, "sawbombmix") || str_eq(mode, "edge14") || str_eq(mode, "edge14mix")) {
            if (bs >= 10 * SR && bs < 20 * SR) {
                let sbq:i64 = 238;
                if ((nblocks % 2) == 1) { sbq = 105; }
                if (str_eq(mode, "edge14") || str_eq(mode, "edge14mix")) { sbq = 114; }
                let j:i64 = 0;
                while (j < bs1 - bs) {
                    put64(mix, (bs + j) * 8, (get64(mix, (bs + j) * 8) * sbq) / 100);
                    j = j + 1;
                }
            }
        }
'''
ANCHOR_DROP = '                pout("C dropout injected: block zeroed at t=3s\\n");\n            }\n        }\n'
ANCHOR_MIX = 'if (str_eq(mode, "seqmix") || str_eq(mode, "faultmix") || str_eq(mode, "susfaultmix") || str_eq(mode, "dropoutmix") || str_eq(mode, "sus5mix") || str_eq(mode, "sus1292mix")) {'

def add_common(src):
    src = rep(src, ANCHOR_DROP, ANCHOR_DROP + SAWBOMB, "sawbomb-insert")
    src = rep(src, ANCHOR_MIX,
              ANCHOR_MIX.replace(')) {', ') || str_eq(mode, "sawbombmix") || str_eq(mode, "edge14mix")) {'), "mix-cond")
    return src

# ---------- stock: frozen + common test-only modes ----------
base = open(FROZEN).read()
stock = add_common(base)
open(os.path.join(BASE, "render_c_stock.zag"), "w").write(stock)

# ---------- off ----------
off = add_common(base)
off = rep(off, "const DEADBAND_PC:i64 = 10;",
          "const DEADBAND_PC:i64 = 10;\nconst SERVO_OFF:i64 = 1; // test control: adapt+veto fully disabled (PAR-equivalent path)", "off-const")
off = rep(off, "            if (veto == 1) {\n                // Corruption is not a level to track:",
          "            if (veto == 1 && SERVO_OFF == 0) {\n                // Corruption is not a level to track:", "off-veto1")
off = rep(off, "                if (d * 100 < DEADBAND_PC * M) {",
          "                if (d * 100 < DEADBAND_PC * M || SERVO_OFF == 1) {", "off-adapt")
off = rep(off, '            if (veto == 1) { st = 2; } // trace marks the veto source',
          '            if (veto == 1 && SERVO_OFF == 0) { st = 2; } // trace marks the veto source', "off-veto2")
open(os.path.join(BASE, "render_c_off.zag"), "w").write(off)

# ---------- gate machinery shared by gated + gfable ----------
GATE_CONSTS = '''
// ---- crew SERVO necessity gate (preregistered 2026-09-24, RUNLOG.md) ----
const GATE_DEV_PC:i64 = 15;  // open: |T-m| > 15% of max(T,m) ...
const GATE_OPEN_N:i64 = 3;   // ... sustained over 3 consecutive blocks
const GATE_CLOSE_N:i64 = 10; // close: dev < 10% (stock deadband) for 10 blocks
const GATE_HYST_MIN:i64 = 20; // fable R1 tier-2: minimum active blocks (gfable only)
'''
GATE_STATE = '''
        let gs:i64 = 0;     // gate: 0 closed (servo idle, gain frozen) | 1 open
        let gopen:i64 = 0;  // consecutive dev>15% blocks (open persistence)
        let gclear:i64 = 0; // consecutive dev<10% blocks (close hysteresis)
        let ghyst:i64 = 0;  // fable tier-2: blocks remaining in minimum-active
'''
# gate transition, inserted after d is computed (primary: plain 10-clear)
GATE_FSM = '''
                // necessity gate (crew SERVO, preregistered): engage only on
                // real, sustained deviation. Vetoed blocks are measurement
                // failures, not evidence: counters untouched.
                if (veto == 0) {
                    if (gs == 0) {
                        if (d * 100 > GATE_DEV_PC * M) { gopen = gopen + 1; }
                        else { gopen = 0; }
                        if (gopen >= GATE_OPEN_N) {
                            gs = 1; gclear = 0;
                            pout("C gate OPEN rg="); pout(i64s(r));
                            pout(" rb="); pout(i64s(rb)); pout("\\n");
                        }
                    } else {
                        if (d * 100 < DEADBAND_PC * M) { gclear = gclear + 1; }
                        else { gclear = 0; }
                        if (gclear >= GATE_CLOSE_N) {
                            gs = 0; gopen = 0;
                            pout("C gate CLOSED rg="); pout(i64s(r));
                            pout(" rb="); pout(i64s(rb)); pout("\\n");
                        }
                    }
                }
'''
# gfable: 20-block minimum active OR clear+10 grace
GATE_FSM_FABLE = '''
                // fable R1 tier-2 hysteresis: 20-block minimum active OR
                // until triggers clear + 10-block grace.
                if (veto == 0) {
                    if (gs == 0) {
                        if (d * 100 > GATE_DEV_PC * M) { gopen = gopen + 1; }
                        else { gopen = 0; }
                        if (gopen >= GATE_OPEN_N) {
                            gs = 1; gclear = 0; ghyst = GATE_HYST_MIN;
                            pout("C gate OPEN rg="); pout(i64s(r));
                            pout(" rb="); pout(i64s(rb)); pout("\\n");
                        }
                    } else {
                        if (ghyst > 0) { ghyst = ghyst - 1; }
                        if (d * 100 < DEADBAND_PC * M) { gclear = gclear + 1; }
                        else { gclear = 0; }
                        if (ghyst <= 0 && gclear >= GATE_CLOSE_N) {
                            gs = 0; gopen = 0;
                            pout("C gate CLOSED rg="); pout(i64s(r));
                            pout(" rb="); pout(i64s(rb)); pout("\\n");
                        }
                    }
                }
'''
GATE_ADAPT = '''                if (d * 100 < DEADBAND_PC * M) {
                    st = 0; // residual regulator: silent on the happy path
                } else if (gs == 0) {
                    st = 4; // gated: real deviation, gate closed (no adapt)
                } else {'''
ANCHOR_ADAPT = '''                if (d * 100 < DEADBAND_PC * M) {
                    st = 0; // residual regulator: silent on the happy path
                } else {'''
ANCHOR_D = "                let d:i64 = T - m;\n                if (d < 0) { d = 0 - d; }\n"
ANCHOR_TRACE = '        pout(" st=");\n        pout(i64s(st));\n        pout("\\n");\n'
TRACE_GS = '        pout(" st=");\n        pout(i64s(st));\n        pout(" gs=");\n        pout(i64s(gs));\n        pout("\\n");\n'
ANCHOR_G = "        let g:i64 = 65536;\n"
ANCHOR_DEADBAND_CONST = "const DEADBAND_PC:i64 = 10;"

def add_gate(src, fsm):
    src = rep(src, ANCHOR_DEADBAND_CONST, ANCHOR_DEADBAND_CONST + GATE_CONSTS, "gate-consts")
    src = rep(src, ANCHOR_G, ANCHOR_G + GATE_STATE, "gate-state")
    src = rep(src, ANCHOR_D, ANCHOR_D + fsm, "gate-fsm")
    src = rep(src, ANCHOR_ADAPT, GATE_ADAPT, "gate-adapt")
    src = rep(src, ANCHOR_TRACE, TRACE_GS, "gate-trace")
    # Silence breaks the persistence run: a silent block is not evidence of
    # sustained deviation (fixes flap false-open where a silence block froze
    # gopen across the gap, letting two marginal transient runs bridge into
    # 3 increments).
    src = rep(src, "        if (T < SILENCE_FLOOR) {",
              "        if (T < SILENCE_FLOOR) {\n            gopen = 0; // silence is not evidence", "gate-silence")
    return src

gated = add_gate(add_common(base), GATE_FSM)
open(os.path.join(BASE, "render_c_gated.zag"), "w").write(gated)

# ---------- gfable: + region_preengage + pre-open ----------
PREENGAGE_FN = '''
// fable R1 tier-1(a): preventive headroom trigger. Returns 1 if the region
// ever has >=4 simultaneous voices AND summed analytic RMS > 0.7 FS.
fn region_preengage(ev:[]u8, lut:[]u8, bed:[]u8, nev:i64, rs0:i64, rs1:i64) i64 {
    let s:i64 = 0;
    while (s < 8) {
        let mid:i64 = rs0 + ((rs1 - rs0) * (2 * s + 1)) / 16;
        let n:i64 = 0;
        let p2:i64 = 0;
        let e:i64 = 0;
        while (e < nev) {
            let t0:i64 = evg(ev, e, 0);
            let dur:i64 = evg(ev, e, 1);
            if (t0 <= mid && mid < t0 + dur) {
                let ampq:i64 = evg(ev, e, 3);
                let tim:i64 = evg(ev, e, 4);
                if (tim < 1) { tim = 1; }
                if (tim > 13) { tim = 13; }
                let cr:i64 = 33423 + 12911 / tim;
                let vr:i64 = (ampq * cr) / 65536;
                if (vr > 3037000499) { vr = 3037000499; }
                if (vr < -3037000499) { vr = -3037000499; }
                vr = (vr * venv_q16(lut, mid - t0, dur)) / 65536;
                if (p2 < 4611686018427387904) { p2 = p2 + vr * vr; }
                n = n + 1;
            }
            e = e + 1;
        }
        // 0.7 FS in Q16 = 45875; compare summed power (Q32)
        if (n >= 4 && isqrt(p2) > 45875) { return 1; }
        s = s + 1;
    }
    return 0;
}
'''
ANCHOR_FN = "fn main() i32 {"
ANCHOR_BS = "        let bs:i64 = rs0;\n"
PREOPEN = '''        let bs:i64 = rs0;
        // fable R1 tier-1(a): pre-engage the headroom servo on dense plans.
        // Tier-1(c) (pitch disagreement) is N/A for the gain-only H3 servo:
        // pitch correction is owned by the piece-3 latch (unchanged).
        // Tier-1(d) (corruption) is the always-on veto (unchanged).
        if (region_preengage(ev, lut, bed, nev, rs0, rs1) == 1) {
            gs = 1; gclear = 0; ghyst = GATE_HYST_MIN;
            pout("C gate PRE-OPEN rg="); pout(i64s(r)); pout("\\n");
        }
'''

gf = add_gate(add_common(base), GATE_FSM_FABLE)
gf = rep(gf, ANCHOR_FN, PREENGAGE_FN + "\n" + ANCHOR_FN, "preengage-fn")
gf = rep(gf, ANCHOR_BS, PREOPEN, "preengage-call")
open(os.path.join(BASE, "render_c_gfable.zag"), "w").write(gf)

print("wrote 3 variants")
for v in ["render_c_off.zag", "render_c_gated.zag", "render_c_gfable.zag"]:
    p = os.path.join(BASE, v)
    print(v, os.path.getsize(p), "bytes")
