#!/usr/bin/env python3
"""Generate H5/H6 composite gates from the generated h3 (shares its plumbing)."""
import re

SRC = "/tmp/hardening/src/vgate_h3.zag"
t3 = open(SRC).read()

START = "                if(pr == 1) {"
END = "            hist_n = hist_put"
assert t3.count(START) == 1, "start anchor not unique"
i0 = t3.index(START)
i1 = t3.index(END)
old_region = t3[i0:i1]

# ---------------- H5 decision block ----------------
H5 = '''                if(pr == 1) {
                    // FAIL: never installed; stored as negative evidence.
                    if(nm == 0 && nn < 256) {
                        t_put64(neg_j, (tc * 256 + nn as i32) * 8, jc);
                        t_put64(neg_m, (tc * 256 + nn as i32) * 8, meas);
                        t_put64(neg_n, tc * 8, nn + 1);
                    }
                    disp = "NEGATIVE_EVIDENCE";
                    if(nm == 1) { det = "dup"; } else { det = "stored"; }
                } else if(pr == 2) {
                    // UNRESOLVED: withheld; suppressed on negative match.
                    if(nm == 1) {
                        disp = "SUPPRESSED";
                        det = "neg";
                    } else {
                        disp = "WITHHELD";
                        det = "unresolved";
                    }
                } else {
                    // PASS. R3: every install path requires prog=PASS,
                    // pred=1, conf>=700, attested G agreement (R1+R2).
                    let r3:i32 = 0;
                    if(pr == 0 && pred == 1 && conf >= 700 && jg >= 0 && jg == jc && confg >= 700 && att_ok == 1) { r3 = 1; }
                    if(pred == 0) {
                        disp = "WITHHELD";
                        det = "pred0";
                    } else if(nm == 1) {
                        disp = "SUPPRESSED";
                        det = "neg";
                    } else if(r3 == 0) {
                        disp = "WITHHELD";
                        det = "no-attested-agreement";
                    } else if(t_get64(perm_on, tc * 8) == 1) {
                        let pj:i64 = t_get64(perm_j, tc * 8);
                        let pm:i64 = t_get64(perm_m, tc * 8);
                        let pc:i64 = t_get64(perm_c, tc * 8);
                        if(jc == pj && iabs(pm - meas) <= tol) {
                            disp = "CORROBORATED";
                            det = "perm";
                        } else if(jc != pj) {
                            // R4 adjudication: historical corroboration
                            // (cf1: prior PASS same-class trial within tol)
                            // + challenger margin mrgF = conf-challenger -
                            // conf-incumbent >= T3=100.
                            let corr:i32 = has_corr(hist_tc, hist_jc, hist_pr, hist_meas, hist_n, tc, jc, meas, tol);
                            let mrg:i64 = conf - pc;
                            if(corr == 1 && mrg >= 100) {
                                let olds:i64 = t_get64(perm_s, tc * 8);
                                t_put64(perm_j, tc * 8, jc);
                                t_put64(perm_m, tc * 8, meas);
                                t_put64(perm_s, tc * 8, seq);
                                t_put64(perm_c, tc * 8, conf);
                                t_put64(prov_on, tc * 8, 0);
                                disp = "REVISE_INSTALL";
                                let tmp:[]u8 = nio_alloc(160);
                                let q:i32 = ob_add(tmp, 0, "adj_r4 oldj=");
                                q = ob_add(tmp, q, _zag_i64_to_str(pj));
                                q = ob_add(tmp, q, " oldm=");
                                q = ob_add(tmp, q, _zag_i64_to_str(pm));
                                q = ob_add(tmp, q, " oldseq=");
                                q = ob_add(tmp, q, _zag_i64_to_str(olds));
                                q = ob_add(tmp, q, " mrg=");
                                q = ob_add(tmp, q, _zag_i64_to_str(mrg));
                                let c2:i32 = 0;
                                while(c2 < q) { fb2[256 + c2] = tmp[c2]; c2 = c2 + 1; }
                                nio_free(tmp);
                                det = fb2[256..256 + q];
                            } else {
                                disp = "CONFLICT_WITHHELD";
                                let tmp:[]u8 = nio_alloc(96);
                                let q:i32 = ob_add(tmp, 0, "adj_r4_hold perm_seq=");
                                q = ob_add(tmp, q, _zag_i64_to_str(t_get64(perm_s, tc * 8)));
                                let c2:i32 = 0;
                                while(c2 < q) { fb2[256 + c2] = tmp[c2]; c2 = c2 + 1; }
                                nio_free(tmp);
                                det = fb2[256..256 + q];
                            }
                        } else {
                            disp = "WITHHELD";
                            det = "perm-measure-divergent";
                        }
                    } else if(t_get64(prov_on, tc * 8) == 1) {
                        let pj:i64 = t_get64(prov_j, tc * 8);
                        let pm:i64 = t_get64(prov_m, tc * 8);
                        if(jc == pj && iabs(pm - meas) <= tol) {
                            // corroboration: permanence (r3 already holds)
                            t_put64(perm_on, tc * 8, 1);
                            t_put64(perm_j, tc * 8, jc);
                            t_put64(perm_m, tc * 8, meas);
                            t_put64(perm_s, tc * 8, seq);
                            t_put64(perm_c, tc * 8, conf);
                            t_put64(prov_on, tc * 8, 0);
                            disp = "PERMANENT_INSTALL";
                            det = "corroborated";
                        } else if(jc != pj) {
                            // conflict: reverse the provisional, install new
                            let old:i64 = t_get64(prov_s, tc * 8);
                            t_put64(prov_j, tc * 8, jc);
                            t_put64(prov_m, tc * 8, meas);
                            t_put64(prov_s, tc * 8, seq);
                            disp = "PROVISIONAL_INSTALL";
                            let tmp:[]u8 = nio_alloc(96);
                            let q:i32 = ob_add(tmp, 0, "reversed_old=");
                            q = ob_add(tmp, q, _zag_i64_to_str(old));
                            let c2:i32 = 0;
                            while(c2 < q) { fb2[256 + c2] = tmp[c2]; c2 = c2 + 1; }
                            nio_free(tmp);
                            det = fb2[256..256 + q];
                        } else {
                            disp = "WITHHELD";
                            det = "prov-measure-divergent";
                        }
                    } else {
                        t_put64(prov_on, tc * 8, 1);
                        t_put64(prov_j, tc * 8, jc);
                        t_put64(prov_m, tc * 8, meas);
                        t_put64(prov_s, tc * 8, seq);
                        disp = "PROVISIONAL_INSTALL";
                        det = "new";
                    }
                }
            } else {
                disp = "WITHHELD";
                det = "bad-record";
            }
'''

h5 = t3[:i0] + H5 + t3[i1:]
h5 = h5.replace('"H3"', '"H5"').replace("vgate_h3", "vgate_h5")
h5 = h5.replace("// vgate_h3.zag — PAM v2 hardening fork H3: PREREG_V2-IE_AMEND1.",
                "// vgate_h5.zag — PAM v2 hardening fork H5 (R1-R4 composite): PREREG_V2-IE_AMEND1.")
open("/tmp/hardening/src/vgate_h5.zag", "w").write(h5)
print("h5 written", len(h5))

# ---------------- H6 decision block (no provisional installs) ----------------
H6 = H5.replace('''                    } else if(t_get64(prov_on, tc * 8) == 1) {
                        let pj:i64 = t_get64(prov_j, tc * 8);
                        let pm:i64 = t_get64(prov_m, tc * 8);
                        if(jc == pj && iabs(pm - meas) <= tol) {
                            // corroboration: permanence (r3 already holds)
                            t_put64(perm_on, tc * 8, 1);
                            t_put64(perm_j, tc * 8, jc);
                            t_put64(perm_m, tc * 8, meas);
                            t_put64(perm_s, tc * 8, seq);
                            t_put64(perm_c, tc * 8, conf);
                            t_put64(prov_on, tc * 8, 0);
                            disp = "PERMANENT_INSTALL";
                            det = "corroborated";
                        } else if(jc != pj) {
                            // conflict: reverse the provisional, install new
                            let old:i64 = t_get64(prov_s, tc * 8);
                            t_put64(prov_j, tc * 8, jc);
                            t_put64(prov_m, tc * 8, meas);
                            t_put64(prov_s, tc * 8, seq);
                            disp = "PROVISIONAL_INSTALL";
                            let tmp:[]u8 = nio_alloc(96);
                            let q:i32 = ob_add(tmp, 0, "reversed_old=");
                            q = ob_add(tmp, q, _zag_i64_to_str(old));
                            let c2:i32 = 0;
                            while(c2 < q) { fb2[256 + c2] = tmp[c2]; c2 = c2 + 1; }
                            nio_free(tmp);
                            det = fb2[256..256 + q];
                        } else {
                            disp = "WITHHELD";
                            det = "prov-measure-divergent";
                        }
                    } else {
                        t_put64(prov_on, tc * 8, 1);
                        t_put64(prov_j, tc * 8, jc);
                        t_put64(prov_m, tc * 8, meas);
                        t_put64(prov_s, tc * 8, seq);
                        disp = "PROVISIONAL_INSTALL";
                        det = "new";
                    }''',
'''                    } else if(t_get64(uc_on, tc * 8) == 1) {
                        // unconfirmed candidate: install permanent only on
                        // corroborated second observation within tolerance.
                        let uj:i64 = t_get64(uc_j, tc * 8);
                        let um:i64 = t_get64(uc_m, tc * 8);
                        if(jc == uj && iabs(um - meas) <= tol) {
                            t_put64(perm_on, tc * 8, 1);
                            t_put64(perm_j, tc * 8, jc);
                            t_put64(perm_m, tc * 8, meas);
                            t_put64(perm_s, tc * 8, seq);
                            t_put64(perm_c, tc * 8, conf);
                            t_put64(uc_on, tc * 8, 0);
                            disp = "PERMANENT_INSTALL";
                            det = "corroborated-second";
                        } else {
                            // latest observation becomes the candidate
                            t_put64(uc_j, tc * 8, jc);
                            t_put64(uc_m, tc * 8, meas);
                            t_put64(uc_c, tc * 8, conf);
                            disp = "WITHHELD";
                            det = "unconfirmed";
                        }
                    } else {
                        t_put64(uc_on, tc * 8, 1);
                        t_put64(uc_j, tc * 8, jc);
                        t_put64(uc_m, tc * 8, meas);
                        t_put64(uc_c, tc * 8, conf);
                        disp = "WITHHELD";
                        det = "unconfirmed";
                    }''')

h6 = t3[:i0] + H6 + t3[i1:]
# add uc arenas + zeroing
old_arena = "    let perm_c:[]u8 = nio_alloc(48);\n"
new_arena = ("    let perm_c:[]u8 = nio_alloc(48);\n"
             "    let uc_on:[]u8 = nio_alloc(48);\n"
             "    let uc_j:[]u8 = nio_alloc(48);\n"
             "    let uc_m:[]u8 = nio_alloc(48);\n"
             "    let uc_c:[]u8 = nio_alloc(48);\n")
assert h6.count(old_arena) == 1
h6 = h6.replace(old_arena, new_arena, 1)
old_init = """        t_put64(perm_c, t * 8, 0);
        t = t + 1;"""
new_init = """        t_put64(perm_c, t * 8, 0);
        t_put64(uc_on, t * 8, 0);
        t = t + 1;"""
assert h6.count(old_init) == 1
h6 = h6.replace(old_init, new_init, 1)
h6 = h6.replace('"H3"', '"H6"').replace("vgate_h3", "vgate_h6")
h6 = h6.replace("// vgate_h3.zag — PAM v2 hardening fork H3: PREREG_V2-IE_AMEND1.",
                "// vgate_h6.zag — PAM v2 hardening fork H6 (R1-R4, no provisional): PREREG_V2-IE_AMEND1.")
open("/tmp/hardening/src/vgate_h6.zag", "w").write(h6)
print("h6 written", len(h6))
