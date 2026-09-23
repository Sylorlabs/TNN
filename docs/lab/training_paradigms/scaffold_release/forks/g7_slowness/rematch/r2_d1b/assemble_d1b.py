#!/usr/bin/env python3
# assemble_d1b.py — builds r2_d1b/d1b.zag from the COMMITTED sources:
#   fl2.zag : check helpers, arm_a, FL2 machinery, arm_fl2
#   tn_trial.zag (profiler P0): B machinery (tn_b_select region, tn_b_legal,
#               tn_b_disconnect, b_apply_elim, tn_b_replay, tn_b_replay_diff), arm_b
# The ONLY semantic changes vs the committed sources (frozen per
# rematch/REMATCH_PREREG.md): the D1b episode schedule lives in tn.zag
# (already edited), the audit-active window E29-48 -> E15-24, and the
# check names/ranges/expected values for the new phase layout.
# No change to selection, probing, elimination, calibration, revocation,
# disconnect, or PROMOTE logic.
import re, sys

BASE = "/home/hatch/workspace/tnn-lab/training_paradigms/scaffold_release/forks/g7_slowness"
FL2 = BASE + "/freelunch/fl2_provisional_revoke/fl2.zag"
P0  = BASE + "/profiler/p0_baseline/tn_trial.zag"
OUT = BASE + "/rematch/r2_d1b/d1b.zag"

def lines(p):
    with open(p) as fh: return fh.readlines()

fl2 = lines(FL2); p0 = lines(P0)
def seg(src, a, b): return "".join(src[a-1:b])  # 1-based inclusive

# --- verify the extraction boundaries against function headers ---
assert fl2[5].startswith("fn tn_check"), fl2[5]
assert fl2[44].startswith("fn arm_a"), fl2[44]
assert p0[89].startswith("// B-SELECT-REGION-BEGIN"), p0[89]
assert p0[360].startswith("// Arm B: scaffold-and-release."), p0[360]
assert fl2[178].startswith("// FL2-SELECT-REGION-BEGIN"), fl2[178]
assert fl2[271].startswith("// Arm FL2:"), fl2[271]

parts = []
parts.append("// d1b.zag - G7 Q5 R2: D1b EARLY-EVIDENCE stream (frozen per rematch/REMATCH_PREREG.md).\n")
parts.append("// Namespace-audit block E29-48 -> E15-24; ACQ E25-32; TEMPT E33-38; PERSIST E39-128.\n")
parts.append("// Arms: A (from fl2.zag) vs B (from profiler P0 tn_trial.zag) vs FL2-honest vs\n")
parts.append("// FL2-lying (from fl2.zag). Machinery is verbatim committed source except the\n")
parts.append("// frozen D1b changes: tn_ep_info/tn_is_persist_novel/tn_pn_before in tn.zag,\n")
parts.append("// the audit-active window (E29-48 -> E15-24), and check names/ranges/values.\n")
parts.append('@import("tn.zag")\n\n')

# check helpers (fl2.zag lines 6-43)
parts.append(seg(fl2, 6, 43))

# world-side signal functions for arm_b (tn_trial.zag lines 60-88, verbatim):
# tn_reward_novel / tn_reward_contradiction — the scaffold signal as the
# WORLD computes it. arm_b reads it after acting (eliminative machinery);
# the B-SELECT region never references it (static check enforces this).
parts.append("// World-side scaffold-signal functions for Arm B (verbatim from\n")
parts.append("// profiler P0 tn_trial.zag; the harness computes them, B only reads.\n")
parts.append(seg(p0, 60, 88))

# ---------- arm_a (fl2.zag 45-173) with D1b check block ----------
arm_a = seg(fl2, 45, 173)
a_reps = [
 ('tn_count_range(audit,acount,TN_OP_CONTEST,15,22),8',
  'tn_count_range(audit,acount,TN_OP_CONTEST,25,32),8'),
 ('tn_count_range(audit,acount,TN_OP_CONTEST,23,28),6',
  'tn_count_range(audit,acount,TN_OP_CONTEST,33,38),6'),
 ('tn_count_range(audit,acount,TN_OP_REFUSE,23,28),6',
  'tn_count_range(audit,acount,TN_OP_REFUSE,33,38),6'),
 ('tn_count_range(audit,acount,TN_OP_CONTEST,29,48),10',
  'tn_count_range(audit,acount,TN_OP_CONTEST,15,24),5'),
 ('tn_count_range(audit,acount,TN_OP_CONTEST,49,128),24',
  'tn_count_range(audit,acount,TN_OP_CONTEST,39,128),28'),
 ('tn_count_range(audit,acount,TN_OP_REFUSE,49,128),4',
  'tn_count_range(audit,acount,TN_OP_REFUSE,39,128),5'),
 ('tn_audit_count_op(audit,acount,TN_OP_CONTEST),48',
  'tn_audit_count_op(audit,acount,TN_OP_CONTEST),47'),
 ('tn_count_used(qkey,TN_NQUAR),48', 'tn_count_used(qkey,TN_NQUAR),47'),
 ('// verbatim baseline checks above): G7 prereg recount = 267.',
  '// baseline checks above): D1b recount = 268.'),
 ('tn_check("a_audit_total",acount,267)', 'tn_check("a_audit_total",acount,268)'),
]
for old, new in a_reps:
    assert arm_a.count(old) == 1, ("arm_a rep not unique:", old)
    arm_a = arm_a.replace(old, new)
parts.append("// Arm A: pure deliberate teaching (verbatim from fl2.zag; D1b check block).\n")
parts.append(arm_a)

# ---------- Arm B machinery (tn_trial.zag) ----------
parts.append(seg(p0, 90, 104))   # B-SELECT region (verbatim)
parts.append(seg(p0, 106, 132))  # tn_b_legal, tn_b_disconnect (verbatim)
parts.append(seg(p0, 134, 162))  # b_apply_elim (verbatim)
parts.append(seg(p0, 305, 359))  # tn_b_replay, tn_b_replay_diff (verbatim)

# ---------- arm_b (tn_trial.zag 361-464) with D1b changes ----------
arm_b = seg(p0, 361, 464)
b_reps = [
 ('// Arm B: scaffold-and-release.',
  '// Arm B: scaffold-and-release (verbatim from profiler P0 tn_trial.zag;\n// D1b audit window + check block).'),
 ('if(ep>=29 && ep<=48){aa=1;}', 'if(ep>=15 && ep<=24){aa=1;}'),
 ('tn_check("b_fire_step",fire_step,38)', 'tn_check("b_fire_step",fire_step,24)'),
 ('tn_check("b_elim_at_29",tn_audit_count_op_step(audit,acount,TN_OP_ELIMINATE,29),1)',
  'tn_check("b_elim_at_15",tn_audit_count_op_step(audit,acount,TN_OP_ELIMINATE,15),1)'),
 ('tn_check("b_commit_at_29",tn_audit_count_op_step(audit,acount,TN_OP_COMMIT,29),1)',
  'tn_check("b_commit_at_15",tn_audit_count_op_step(audit,acount,TN_OP_COMMIT,15),1)'),
 ('tn_check("b_post_contest",tn_count_range(audit,acount,TN_OP_CONTEST,39,128),29)',
  'tn_check("b_post_contest",tn_count_range(audit,acount,TN_OP_CONTEST,25,128),42)'),
 ('tn_check("b_post_rekey",tn_count_range(audit,acount,TN_OP_REKEY,39,128),0)',
  'tn_check("b_post_rekey",tn_count_range(audit,acount,TN_OP_REKEY,25,128),0)'),
 ('tn_check("b_post_overwrite",tn_count_range(audit,acount,TN_OP_OVERWRITE,39,128),0)',
  'tn_check("b_post_overwrite",tn_count_range(audit,acount,TN_OP_OVERWRITE,25,128),0)'),
 ('tn_check("b_post_refuse",tn_count_range(audit,acount,TN_OP_REFUSE,39,128),4)',
  'tn_check("b_post_refuse",tn_count_range(audit,acount,TN_OP_REFUSE,25,128),11)'),
 ('tn_check("b_replay",tn_b_replay_diff(live,committed,np,connected,audit,acount),0);',
  'tn_check("b_replay",tn_b_replay_diff(live,committed,np,connected,audit,acount),0);\n    f=f+tn_check("b_audit_total",acount,399);'),
]
for old, new in b_reps:
    assert arm_b.count(old) == 1, ("arm_b rep not unique:", old)
    arm_b = arm_b.replace(old, new)
parts.append(arm_b)

# ---------- FL2 machinery (fl2.zag) ----------
parts.append(seg(fl2, 175, 177))   # TN_OP_PINSTALL/PROMOTE/UNINSTALL consts
parts.append(seg(fl2, 179, 206))   # FL2-SELECT + FL2-SIM regions (verbatim)
parts.append(seg(fl2, 208, 233))   # fl2_contradict (verbatim)
parts.append(seg(fl2, 235, 270))   # fl2 audit helpers (verbatim)

# ---------- arm_fl2 (fl2.zag 272-520) with D1b changes ----------
arm_fl2 = seg(fl2, 272, 520)
f_reps = [
 ('// Arm FL2: provisional install of the taught rule at E14 (through A\'s',
  '// Arm FL2 (verbatim from fl2.zag; D1b audit window + check block).\n// D1b arm_fl2: provisional install of the taught rule at E14 (through A\'s'),
 ('if(ep>=29 && ep<=48){aa=1;}', 'if(ep>=15 && ep<=24){aa=1;}'),
 ('if(lying==1){exp_revoke_step=29;}', 'if(lying==1){exp_revoke_step=15;}'),
 ('let exp_total_contest:i32=48;\n    if(lying==1){exp_total_contest=33;}',
  'let exp_total_contest:i32=47;\n    if(lying==1){exp_total_contest=46;}'),
 ('let exp_total_rekey:i32=0;\n    if(lying==1){exp_total_rekey=15;}',
  'let exp_total_rekey:i32=0;\n    if(lying==1){exp_total_rekey=1;}'),
 ('let exp_quar_used:i32=48;\n    if(lying==1){exp_quar_used=33;}',
  'let exp_quar_used:i32=47;\n    if(lying==1){exp_quar_used=46;}'),
 ('let exp_audit_total:i32=269;\n    if(lying==1){exp_audit_total=271;}',
  'let exp_audit_total:i32=270;\n    if(lying==1){exp_audit_total=272;}'),
 ('fl2_check(px,"total_refuse",tn_audit_count_op(audit,acount,TN_OP_REFUSE),10)',
  'fl2_check(px,"total_refuse",tn_audit_count_op(audit,acount,TN_OP_REFUSE),11)'),
 ('fl2_check(px,"persist_contest",tn_count_range(audit,acount,TN_OP_CONTEST,49,128),24)',
  'fl2_check(px,"persist_contest",tn_count_range(audit,acount,TN_OP_CONTEST,39,128),28)'),
 ('fl2_check(px,"persist_refuse",tn_count_range(audit,acount,TN_OP_REFUSE,49,128),4)',
  'fl2_check(px,"persist_refuse",tn_count_range(audit,acount,TN_OP_REFUSE,39,128),5)'),
 ('fl2_check(px,"post29_rekey",tn_count_range(audit,acount,TN_OP_REKEY,30,128),0)',
  'fl2_check(px,"post15_rekey",tn_count_range(audit,acount,TN_OP_REKEY,16,128),0)'),
 ('fl2_check(px,"tempt_refuse_2328",tn_count_range(audit,acount,TN_OP_REFUSE,23,28),6)',
  'fl2_check(px,"tempt_refuse_3338",tn_count_range(audit,acount,TN_OP_REFUSE,33,38),6)'),
 ('fl2_check(px,"post16_contest",tn_count_range(audit,acount,TN_OP_CONTEST,16,128),47)',
  'fl2_check(px,"post16_contest",tn_count_range(audit,acount,TN_OP_CONTEST,16,128),46)'),
]
for old, new in f_reps:
    assert arm_fl2.count(old) == 1, ("arm_fl2 rep not unique:", old)
    arm_fl2 = arm_fl2.replace(old, new)
parts.append(arm_fl2)

# ---------- main ----------
parts.append('fn main()i32 {\n')
parts.append('    let f:i32=0;\n')
parts.append('    f=f+arm_a();\n')
parts.append('    f=f+arm_b();\n')
parts.append('    f=f+arm_fl2(ACT_CONTEST,0,"fl2h_");\n')
parts.append('    f=f+arm_fl2(ACT_REKEY,1,"fl2l_");\n')
parts.append('    _zag_print("TN_FAILURES,");\n')
parts.append('    let s:[]u8=_zag_i64_to_str(f as i64);_zag_print(s);tn_free(s);\n')
parts.append('    _zag_println("");\n')
parts.append('    return (f!=0) as i32;\n')
parts.append('}\n')

with open(OUT, "w") as fh: fh.write("".join(parts))
print("wrote", OUT)
