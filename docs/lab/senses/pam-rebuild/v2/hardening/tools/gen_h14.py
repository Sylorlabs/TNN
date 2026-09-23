#!/usr/bin/env python3
"""Generate H1-H4 gate sources from the landed V2-A/V2-D gates (deterministic)."""
import sys

VA = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/v2/forks/V2-A/src/vgate_a.zag"
VD = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/v2/forks/V2-D/src/vgate_d.zag"
OUT = "/tmp/hardening/src"

HELPERS = '''
// ---------------- channel attestation (amendment R2) ----------------
// Registered-channel key (frozen test registration; amendment A1.2 R2).
fn ch_key() []u8 { return "PAMV2-REG-CHANNEL-2026-09-23"; }
// verify attestation: recompute hex(sha256(KEY|seq|fixture|jG|confG)) and
// compare against the sidecar entry. Returns 1 iff valid.
fn att_verify(seq:i64, fx:[]u8, fxn:i32, jg:i64, confg:i64, want:[]u8) i32 {
    let ib:[]u8 = nio_alloc(512);
    let p:i32 = ob_add(ib, 0, ch_key());
    p = ob_add(ib, p, "|");
    p = ob_add(ib, p, _zag_i64_to_str(seq));
    p = ob_add(ib, p, "|");
    p = ob_addn(ib, p, fx, fxn);
    p = ob_add(ib, p, "|");
    p = ob_add(ib, p, _zag_i64_to_str(jg));
    p = ob_add(ib, p, "|");
    p = ob_add(ib, p, _zag_i64_to_str(confg));
    let dg:[]u8 = nio_alloc(32);
    let hx:[]u8 = "";
    if(ns_sha256(ib[0..p], dg) == 0) { hx = ns_hex(dg); }
    nio_free(ib);
    nio_free(dg);
    if(hx.len != 64 || want.len != 64) { return 0; }
    let i:i32 = 0;
    while(i < 64) {
        if(hx[i] != want[i]) { return 0; }
        i = i + 1;
    }
    return 1;
}

// ---------------- trial history (amendment R4) ----------------
// append-only log of (tcode, jcode, prog, measure) per trial.
fn hist_put(ht:[]u8, hj:[]u8, hp:[]u8, hm:[]u8, n:i64, tc:i32, jc:i64, pr:i32, meas:i64) i64 {
    if(n >= 4096) { return n; }
    t_put64(ht, n as i32 * 8, tc as i64);
    t_put64(hj, n as i32 * 8, jc);
    t_put64(hp, n as i32 * 8, pr as i64);
    t_put64(hm, n as i32 * 8, meas);
    return n + 1;
}
// cf1-class corroboration: >=1 PRIOR trial, same task, same jcode,
// prog=PASS, |measure| within tol.
fn has_corr(ht:[]u8, hj:[]u8, hp:[]u8, hm:[]u8, n:i64, tc:i32, jc:i64, meas:i64, tol:i64) i32 {
    let i:i64 = 0;
    while(i < n) {
        if(t_get64(ht, i as i32 * 8) == tc as i64 && t_get64(hj, i as i32 * 8) == jc
           && t_get64(hp, i as i32 * 8) == 0 && iabs(t_get64(hm, i as i32 * 8) - meas) <= tol) {
            return 1;
        }
        i = i + 1;
    }
    return 0;
}
'''

GATT_READ = '''    // channel-attestation sidecar: lines "seq|hex64" (amendment R2)
    let gb2:[]u8 = nio_alloc(1048576);
    let gn2:i64 = z_read(a2, gb2, 1048576);
    let gtab:[]u8 = nio_alloc(4096 * 64);
    let ghas:[]u8 = nio_alloc(4096);
    if(gn2 > 0) {
        let gp:i64 = 0;
        while(gp < gn2) {
            let ge:i64 = gp;
            while(ge < gn2 && gb2[ge as i32] != 10) { ge = ge + 1; }
            let gs:i64 = gp;
            while(gs < ge && gb2[gs as i32] != 124) { gs = gs + 1; }
            if(gs < ge) {
                let sq:i64 = atoi(gb2[gp as i32 .. gs as i32], (gs - gp) as i32);
                if(sq >= 0 && sq < 4096 && ge - gs - 1 >= 64) {
                    let k:i32 = 0;
                    while(k < 64) {
                        gtab[sq as i32 * 64 + k] = gb2[(gs + 1 + k as i64) as i32];
                        k = k + 1;
                    }
                    ghas[sq as i32] = 1;
                }
            }
            gp = ge + 1;
        }
    }
    nio_free(gb2);
'''

ARENAS = '''    // trial history + incumbent-confidence arenas (amendment R4)
    let hist_tc:[]u8 = nio_alloc(4096 * 8);
    let hist_jc:[]u8 = nio_alloc(4096 * 8);
    let hist_pr:[]u8 = nio_alloc(4096 * 8);
    let hist_meas:[]u8 = nio_alloc(4096 * 8);
    let hist_n:i64 = 0;
    let perm_c:[]u8 = nio_alloc(48);
'''

def rep_once(text, old, new, tag):
    n = text.count(old)
    assert n == 1, f"{tag}: anchor found {n}x (expected 1)"
    return text.replace(old, new, 1)

def common_a(text, tag, approach):
    # header
    old_head = "// vgate_a.zag \u2014 PAM v2 fork V2-A: H2-style gate + conflict-adjudication layer."
    assert old_head in text, f"{tag}: header anchor missing"
    text = text.replace(old_head,
        f"// vgate_h{tag[-1]}.zag \u2014 PAM v2 hardening fork {approach}: PREREG_V2-IE_AMEND1.", 1)
    # helpers after iabs
    old_iabs = "fn iabs(x:i64) i64 {\n    if(x < 0) { return 0 - x; }\n    return x;\n}"
    text = rep_once(text, old_iabs, old_iabs + HELPERS, tag + ":iabs")
    # CLI: 3 args
    old_cli = '''    let a1:[]u8 = _zag_arg(1);
    let a2:[]u8 = _zag_arg(2);
    if(a1.len == 0 || a2.len == 0) {
        let ob:[]u8 = nio_alloc(128);
        let pos:i32 = ob_kv(ob, 0, "approach", "V2-A");
        pos = ob_kv(ob, pos, "error", "usage: vgate_a <records> <ledger>");'''
    new_cli = f'''    let a1:[]u8 = _zag_arg(1);
    let a2:[]u8 = _zag_arg(2);
    let a3:[]u8 = _zag_arg(3);
    if(a1.len == 0 || a2.len == 0 || a3.len == 0) {{
        let ob:[]u8 = nio_alloc(128);
        let pos:i32 = ob_kv(ob, 0, "approach", "{approach}");
        pos = ob_kv(ob, pos, "error", "usage: vgate_h{tag[-1]} <records> <gatt> <ledger>");'''
    text = rep_once(text, old_cli, new_cli, tag + ":cli")
    # gatt read + arenas before output buffers
    old_ob = "    // output buffers: dispositions to stdout, ledger to file"
    text = rep_once(text, old_ob, GATT_READ + old_ob, tag + ":gatt")
    # arena declarations before the init loop (which zeroes them)
    old_neg = "    let neg_n:[]u8 = nio_alloc(48);\n"
    text = rep_once(text, old_neg, old_neg + ARENAS, tag + ":arenas")
    # zero perm_c in init loop
    old_init = """        t_put64(neg_n, t * 8, 0);
        t = t + 1;"""
    new_init = """        t_put64(neg_n, t * 8, 0);
        t_put64(perm_c, t * 8, 0);
        t = t + 1;"""
    text = rep_once(text, old_init, new_init, tag + ":init")
    # ledger on a3
    text = rep_once(text, "let lfd:i64 = z_write_open(a2);",
                    "let lfd:i64 = z_write_open(a3);", tag + ":ledger")
    # per-record attestation check after confg parse
    old_cg = """            nf = field(line, llen, 12, fnum);
            let confg:i64 = atoi(fnum, nf);"""
    new_cg = old_cg + """
            let att_ok:i32 = 0;
            if(jg >= 0 && seq >= 0 && seq < 4096 && ghas[seq as i32] == 1) {
                att_ok = att_verify(seq, fxb, fxlen, jg, confg,
                    gtab[seq as i32 * 64 .. seq as i32 * 64 + 64]);
            }"""
    text = rep_once(text, old_cg, new_cg, tag + ":attok")
    # history record before disposition emission
    old_dep = "                        // disposition line: seq|tcode|fixture|disposition|detail|truth"
    new_dep = ("            hist_n = hist_put(hist_tc, hist_jc, hist_pr, hist_meas, hist_n, tc, jc, pr, meas);\n"
               + old_dep)
    text = rep_once(text, old_dep, new_dep, tag + ":hist")
    # rename approach/error/final strings
    text = text.replace('"V2-A"', f'"{approach}"').replace("vgate_a", f"vgate_h{tag[-1]}")
    return text

ADJUD_A = """            if(ind == 1 && _zag_strcmp(disp, "CONFLICT_WITHHELD") == 1) {
                let oldj:i64 = t_get64(perm_j, tc * 8);
                let oldm:i64 = t_get64(perm_m, tc * 8);
                let olds:i64 = t_get64(perm_s, tc * 8);
                t_put64(perm_j, tc * 8, jc);
                t_put64(perm_m, tc * 8, meas);
                t_put64(perm_s, tc * 8, seq);
                t_put64(prov_on, tc * 8, 0);
                disp = "REVISE_INSTALL";
                let tmp:[]u8 = nio_alloc(128);
                let q:i32 = ob_add(tmp, 0, "adj_ind oldj=");
                q = ob_add(tmp, q, _zag_i64_to_str(oldj));
                q = ob_add(tmp, q, " oldm=");
                q = ob_add(tmp, q, _zag_i64_to_str(oldm));
                q = ob_add(tmp, q, " oldseq=");
                q = ob_add(tmp, q, _zag_i64_to_str(olds));
                let c2:i32 = 0;
                while(c2 < q) { fb2[256 + c2] = tmp[c2]; c2 = c2 + 1; }
                nio_free(tmp);
                det = fb2[256..256 + q];
            }"""

def adj_block(det_prefix, extra_puts="", extra_det=""):
    return f"""            if(_zag_strcmp(disp, "CONFLICT_WITHHELD") == 1) {{
                @@COND@@
                    let oldj:i64 = t_get64(perm_j, tc * 8);
                    let oldm:i64 = t_get64(perm_m, tc * 8);
                    let olds:i64 = t_get64(perm_s, tc * 8);
                    t_put64(perm_j, tc * 8, jc);
                    t_put64(perm_m, tc * 8, meas);
                    t_put64(perm_s, tc * 8, seq);{extra_puts}
                    t_put64(prov_on, tc * 8, 0);
                    disp = "REVISE_INSTALL";
                    let tmp:[]u8 = nio_alloc(160);
                    let q:i32 = ob_add(tmp, 0, "{det_prefix} oldj=");
                    q = ob_add(tmp, q, _zag_i64_to_str(oldj));
                    q = ob_add(tmp, q, " oldm=");
                    q = ob_add(tmp, q, _zag_i64_to_str(oldm));
                    q = ob_add(tmp, q, " oldseq=");
                    q = ob_add(tmp, q, _zag_i64_to_str(olds));{extra_det}
                    let c2:i32 = 0;
                    while(c2 < q) {{ fb2[256 + c2] = tmp[c2]; c2 = c2 + 1; }}
                    nio_free(tmp);
                    det = fb2[256..256 + q];
                }}
            }}"""

IND_A = "            let ind:i32 = 0;\n            if(jg >= 0 && jg == jc && confg >= 700 && conf >= 700) { ind = 1; }"

import os
os.makedirs(OUT, exist_ok=True)

# ---- H1: from vgate_d, prog-gated ind ----
t = open(VD).read()
t = rep_once(t,
    "if(jg >= 0 && jg == jc && confg >= 700 && conf >= 700) { ind = 1; }",
    "if(pr == 0 && jg >= 0 && jg == jc && confg >= 700 && conf >= 700) { ind = 1; }",
    "H1:ind")
t = t.replace('"V2-D"', '"H1"').replace("vgate_d", "vgate_h1")
t = t.replace("// vgate_d.zag \u2014 PAM v2 fork V2-D: confidence-separation gate.",
              "// vgate_h1.zag \u2014 PAM v2 hardening fork H1 (prog-requirement): PREREG_V2-IE_AMEND1.")
open(f"{OUT}/vgate_h1.zag", "w").write(t)
print("h1 written", len(t))

# ---- H2: vgate_a + R1 + R2 (auth), base path unchanged ----
t = common_a(open(VA).read(), "H2", "H2")
t = rep_once(t, IND_A,
    "            let ind:i32 = 0;\n            if(pr == 0 && jg >= 0 && jg == jc && confg >= 700 && conf >= 700 && att_ok == 1) { ind = 1; }",
    "H2:ind")
open(f"{OUT}/vgate_h2.zag", "w").write(t)
print("h2 written", len(t))

# ---- H3: vgate_a + R1 + R2 + R4 adjudication (corroboration + margin) ----
t = common_a(open(VA).read(), "H3", "H3")
t = rep_once(t, IND_A,
    "            let ind:i32 = 0;\n            if(pr == 0 && jg >= 0 && jg == jc && confg >= 700 && conf >= 700 && att_ok == 1) { ind = 1; }",
    "H3:ind")
cond = """                let corr:i32 = has_corr(hist_tc, hist_jc, hist_pr, hist_meas, hist_n, tc, jc, meas, tol_of(tc));
                let mrg:i64 = conf - t_get64(perm_c, tc * 8);
                if(ind == 1 && corr == 1 && mrg >= 100) {"""
t = rep_once(t, ADJUD_A, adj_block("adj_r4",
    extra_puts="\n                    t_put64(perm_c, tc * 8, conf);",
    extra_det='\n                    q = ob_add(tmp, q, " mrg=");\n                    q = ob_add(tmp, q, _zag_i64_to_str(mrg));'
    ).replace("@@COND@@", cond), "H3:adj")
# store incumbent confidence on promotion to permanent
t = rep_once(t,
    """                            t_put64(perm_s, tc * 8, seq);
                            t_put64(prov_on, tc * 8, 0);
                            disp = "PERMANENT_INSTALL";""",
    """                            t_put64(perm_s, tc * 8, seq);
                            t_put64(perm_c, tc * 8, conf);
                            t_put64(prov_on, tc * 8, 0);
                            disp = "PERMANENT_INSTALL";""",
    "H3:permc")
open(f"{OUT}/vgate_h3.zag", "w").write(t)
print("h3 written", len(t))

# ---- H4: vgate_a + R1 + corroboration-only revision (no auth, no margin) ----
t = common_a(open(VA).read(), "H4", "H4")
t = rep_once(t, IND_A,
    "            let ind:i32 = 0;\n            if(pr == 0 && jg >= 0 && jg == jc && confg >= 700 && conf >= 700) { ind = 1; }",
    "H4:ind")
cond = """                let corr:i32 = has_corr(hist_tc, hist_jc, hist_pr, hist_meas, hist_n, tc, jc, meas, tol_of(tc));
                if(ind == 1 && corr == 1) {"""
t = rep_once(t, ADJUD_A, adj_block("adj_h4").replace("@@COND@@", cond), "H4:adj")
open(f"{OUT}/vgate_h4.zag", "w").write(t)
print("h4 written", len(t))
