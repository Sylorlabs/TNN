#!/usr/bin/env python3
"""PAM round-3 crew 5: emit f5_conf_d.zag / f5_conf_r.zag from f5_full.zag.

Exact string surgery on the frozen mechanism source (committed,
SHA c825d65c52da9b40 per RT-2 extraction): the ONLY changes are
(1) the header comment, (2) core_hit -> organ_confirm, (3) the
confirmation call site, (4) SANITY baselines (script-computed,
spec_r3.json), (5) organ R's true-memory load. Everything else —
I/O, guards, output format, delay accounting — is byte-identical logic.

Fails loud if any anchor string is not found exactly once.
"""
import sys

SRC = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_fullmech/f5_full.zag"
OUTD = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_r3/f5_conf_d.zag"
OUTR = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_r3/f5_conf_r.zag"

src = open(SRC).read()


def sub_once(text, old, new, label):
    n = text.count(old)
    assert n == 1, "%s: anchor found %d times" % (label, n)
    return text.replace(old, new, 1)


# ---------------- shared header ----------------
old_header = src[:src.index('fn z_cstr')]
new_header_d = '''@import("R33_NATIVE_IO_V1.zag")

// f5_conf_d.zag — F5 confirmation ORGAN D (discriminative).
//
// Frozen block predicate (F5) + a deliberate re-inspection organ. No
// temporal crops, no quorum, no coherence vote. Three deliberate
// re-inspections, each naming its alternative:
//   R1 trap-signature test: WITHHOLD iff within the tight trap box
//      (|dconf|<=34, |dmeas|<=58 = 2x the exemplar-cluster span) of a
//      known trap exemplar — "is this the KNOWN false?";
//   R2 true-plausibility test: WITHHOLD iff outside the true-support box
//      conf 650..940, meas 2200..6700 (empirical min/max of the 300 NEAR
//      standing knowledge) — "could a genuine true percept look so?";
//   R3 discrimination: CONFIRM_INSTALL iff not-the-trap AND
//      true-plausible. Fail closed otherwise.
// Prereg: round2/f5_r3/PREREG_F5_R3_CONFIRM.md (committed alone).
//
// argv[1]: ledger (18-field NEAR/FAR or 17-field BACKTEST, as f5_full).
// argv[2]: exemplar bank TSV (seq, fam, conf, measure; tab-separated).
//
// TRUTH FIREWALL: the decision path (f5_block -> organ_confirm) takes ONLY
// (family stem, conf, measure) plus frozen standing knowledge. The truth
// field is parsed solely for offline scoring counters and the battery's
// judgment==truth construction assert; it NEVER enters a decision.
// Review aid: no function in the decision path receives a truth argument.
//
// Delay: allowed -> 0; confirmed -> 3; withheld -> -1 (=infinite).
// stdout: one line per trial:
//   <trial>\\t<fixture>\\t<set>\\t<BLOCKED|ALLOWED>\\t<exseq|->\\t<CONFIRM_INSTALL|WITHHOLD|->\\t<delay>
// then the summary block (SETSUM / BACKTEST / DELAYBAR / HIST / SERIAL / SANITY).
//
// znc landmine notes (from workspace AGENTS.md): no []i32 casts (parallel []u8
// arenas with explicit little-endian put/get64); no slice == ; no .* on
// non-pointers; no bare blocks; shallow nesting only; no identifier named try.

'''
new_header_r = new_header_d.replace(
    "// f5_conf_d.zag — F5 confirmation ORGAN D (discriminative).",
    "// f5_conf_r.zag — F5 confirmation ORGAN R (recognition).").replace(
    '''// Frozen block predicate (F5) + a deliberate re-inspection organ. No
// temporal crops, no quorum, no coherence vote. Three deliberate
// re-inspections, each naming its alternative:
//   R1 trap-signature test: WITHHOLD iff within the tight trap box
//      (|dconf|<=34, |dmeas|<=58 = 2x the exemplar-cluster span) of a
//      known trap exemplar — "is this the KNOWN false?";
//   R2 true-plausibility test: WITHHOLD iff outside the true-support box
//      conf 650..940, meas 2200..6700 (empirical min/max of the 300 NEAR
//      standing knowledge) — "could a genuine true percept look so?";
//   R3 discrimination: CONFIRM_INSTALL iff not-the-trap AND
//      true-plausible. Fail closed otherwise.''',
    '''// Frozen block predicate (F5) + a deliberate re-inspection organ. No
// temporal crops, no quorum, no coherence vote. One deliberate
// re-inspection against standing memory: the organ carries the 300 NEAR
// (conf,meas) coords as its memory of known-true percepts (frozen at
// build, argv[3]). CONFIRM_INSTALL iff a remembered true percept lies
// within eps=5 on both axes — "do I RECOGNIZE this as a true percept?".
// Fail closed otherwise.''').replace(
    '''// argv[1]: ledger (18-field NEAR/FAR or 17-field BACKTEST, as f5_full).
// argv[2]: exemplar bank TSV (seq, fam, conf, measure; tab-separated).''',
    '''// argv[1]: ledger (18-field NEAR/FAR or 17-field BACKTEST, as f5_full).
// argv[2]: exemplar bank TSV (seq, fam, conf, measure; tab-separated).
// argv[3]: true-memory TSV (conf, meas per line; the 300 NEAR coords).''')

# ---------------- organ functions (replace core_hit) ----------------
old_core = src[src.index('// Re-inspection predicate'):src.index('fn ob_add')]
organ_d = '''// Organ D: three deliberate re-inspections with named alternatives.
// R1: trap-signature test — WITHHOLD iff within the tight trap box
// (|dconf|<=34, |dmeas|<=58) of a known trap exemplar.
// R2/R3: CONFIRM_INSTALL iff inside the true-support box
// (conf 650..940, meas 2200..6700); WITHHOLD otherwise. Fail closed.
// Returns 1 = CONFIRM_INSTALL, 2 = WITHHOLD.
fn organ_confirm(cs:[]u8, sl:i32, conf:i64, meas:i64, ex_stem:[]u8, ex_slen:[]u8, ex_conf:[]u8, ex_meas:[]u8, nex:i32) i32 {
    let e:i32 = 0;
    while(e < nex) {
        let esl:i32 = a_get64(ex_slen, e * 8) as i32;
        let stem_ok:i32 = 0;
        if(esl == sl) { stem_ok = beq(ex_stem[e * 8 .. e * 8 + 8], esl, cs, sl); }
        let conf_ok:i32 = 0;
        if(stem_ok == 1 && iabs(conf - a_get64(ex_conf, e * 8)) <= 34) { conf_ok = 1; }
        let meas_ok:i32 = 0;
        if(conf_ok == 1 && iabs(meas - a_get64(ex_meas, e * 8)) <= 58) { meas_ok = 1; }
        if(meas_ok == 1) { return 2; }
        e = e + 1;
    }
    if(conf >= 650 && conf <= 940 && meas >= 2200 && meas <= 6700) { return 1; }
    return 2;
}

'''
organ_r = '''// Organ R: recognition against standing true-memory (the 300 NEAR
// coords, frozen at build, loaded from argv[3]). CONFIRM_INSTALL iff a
// remembered true percept lies within eps=5 on both axes — "do I
// RECOGNIZE this as a true percept?". Fail closed.
// Returns 1 = CONFIRM_INSTALL, 2 = WITHHOLD.
fn organ_confirm(conf:i64, meas:i64, mem_conf:[]u8, mem_meas:[]u8, nmem:i32) i32 {
    let k:i32 = 0;
    while(k < nmem) {
        let dc:i64 = iabs(conf - a_get64(mem_conf, k * 8));
        let dm:i64 = iabs(meas - a_get64(mem_meas, k * 8));
        if(dc <= 5 && dm <= 5) { return 1; }
        k = k + 1;
    }
    return 2;
}

'''

# ---------------- confirmation call site ----------------
old_site = '''                if(blocked == 1) {
                    qk = qk + 1;
                    let rep:i32 = 0;
                    if(core_hit(cs, sl, conf - 10, meas - 200, ex_stem, ex_slen, ex_conf, ex_meas, nex) == 1) { rep = rep + 1; }
                    if(core_hit(cs, sl, conf, meas, ex_stem, ex_slen, ex_conf, ex_meas, nex) == 1) { rep = rep + 1; }
                    if(core_hit(cs, sl, conf + 10, meas + 200, ex_stem, ex_slen, ex_conf, ex_meas, nex) == 1) { rep = rep + 1; }
                    if(rep >= 2) { dec = 2; delay = -1; }
                    if(rep < 2) { dec = 1; delay = 3; }
                }'''
new_site_d = '''                if(blocked == 1) {
                    qk = qk + 1;
                    let org:i32 = organ_confirm(cs, sl, conf, meas, ex_stem, ex_slen, ex_conf, ex_meas, nex);
                    if(org == 2) { dec = 2; delay = -1; }
                    if(org == 1) { dec = 1; delay = 3; }
                }'''
new_site_r = '''                if(blocked == 1) {
                    qk = qk + 1;
                    let org:i32 = organ_confirm(conf, meas, mem_conf, mem_meas, nmem);
                    if(org == 2) { dec = 2; delay = -1; }
                    if(org == 1) { dec = 1; delay = 3; }
                }'''

# ---------------- SANITY baselines (script-computed, spec_r3.json) ----------------
old_san = '''    if(n_near > 0) {
        if(b_near != 110) { san = 0; }
        if(c_near != 50) { san = 0; }
        if(w_near != 60) { san = 0; }
    }'''
new_san_d = '''    if(n_near > 0) {
        if(b_near != 110) { san = 0; }
        if(c_near != 103) { san = 0; }
        if(w_near != 7) { san = 0; }
    }'''
new_san_r = '''    if(n_near > 0) {
        if(b_near != 110) { san = 0; }
        if(c_near != 110) { san = 0; }
        if(w_near != 0) { san = 0; }
    }'''
old_san_bt = '''    if(n_bt > 0) {
        if(wf_bt != 8) { san = 0; }
        if(ef_bt != 1) { san = 0; }
        if(tb_bt != 0) { san = 0; }
    }'''
new_san_bt_d = '''    if(n_bt > 0) {
        if(wf_bt != 5) { san = 0; }
        if(ef_bt != 1) { san = 0; }
        if(tb_bt != 0) { san = 0; }
    }'''
new_san_bt_r = '''    if(n_bt > 0) {
        if(wf_bt != 8) { san = 0; }
        if(ef_bt != 1) { san = 0; }
        if(tb_bt != 0) { san = 0; }
    }'''

# ---------------- organ R memory load (insert after bank load) ----------------
old_bank_tail = '''    // ---- scan ledger ----
    let lb:[]u8 = nio_alloc(200000);'''
new_bank_tail_r = '''    // ---- load true-memory bank (organ R standing knowledge; max 300) ----
    let memfile:[]u8 = _zag_arg(3);
    if(memfile.len == 0) { return 14; }
    let mb:[]u8 = nio_alloc(16384);
    let mn:i64 = z_read(memfile, mb, 16384);
    if(mn < 0) { return 15; }
    let mnn:i32 = mn as i32;
    let mem_conf:[]u8 = nio_alloc(300 * 8);
    let mem_meas:[]u8 = nio_alloc(300 * 8);
    let nmem:i32 = 0;
    let m_i:i32 = 0;
    while(m_i < mnn) {
        let m_ls:i32 = m_i;
        while(m_i < mnn && (mb[m_i] as i32) != 10) { m_i = m_i + 1; }
        let m_le:i32 = m_i;
        if(m_i < mnn) { m_i = m_i + 1; }
        if(m_le > m_ls && nmem < 300) {
            if((mb[m_le - 1] as i32) == 13) { m_le = m_le - 1; }
            let mf0:i32 = getf_sep(mb, m_ls, m_le, 0, 9, tmp);
            a_put64(mem_conf, nmem * 8, p_atoi(tmp, 0, mf0));
            let mf1:i32 = getf_sep(mb, m_ls, m_le, 1, 9, tmp);
            a_put64(mem_meas, nmem * 8, p_atoi(tmp, 0, mf1));
            nmem = nmem + 1;
        }
    }

    // ---- scan ledger ----
    let lb:[]u8 = nio_alloc(200000);'''

d = src
d = sub_once(d, old_header, new_header_d, "header")
d = sub_once(d, old_core, organ_d, "core_hit->organ_d")
d = sub_once(d, old_site, new_site_d, "call site")
d = sub_once(d, old_san, new_san_d, "sanity near")
d = sub_once(d, old_san_bt, new_san_bt_d, "sanity bt")
open(OUTD, "w").write(d)

r = src
r = sub_once(r, old_header, new_header_r, "header")
r = sub_once(r, old_core, organ_r, "core_hit->organ_r")
r = sub_once(r, old_site, new_site_r, "call site")
r = sub_once(r, old_san, new_san_r, "sanity near")
r = sub_once(r, old_san_bt, new_san_bt_r, "sanity bt")
r = sub_once(r, old_bank_tail, new_bank_tail_r, "memory load")
open(OUTR, "w").write(r)

print("emitted:", OUTD, OUTR)
