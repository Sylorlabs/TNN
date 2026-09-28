# ATTACK LOG — delete-strong cite-consumption red team
Binary: /home/hatch/workspace/strength-port/redteam/port_rt_bin | Mode: G only
Date: 2026-09-26. Every sequence executed TWICE; determinism verdict per sequence.
Note: driver echoes argv token 'G' as 'RT 0 G -999' (mode flag, not an op).

## [O8] o8_kill
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o8_kill =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O8] o8_del
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST DEL
===== o8_del =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST DEL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 DEL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_del_cite_count,4,4
CL_CHECK,ck_del_cite_distinct,4,4
CL_CHECK,ck_del_justify,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O8] o8_killt
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILLT
===== o8_killt =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILLT
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILLT 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O8] o8_ow
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW50
===== o8_ow =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW50
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 OW50 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O8] o8_add0
tokens: G ADD0 JUST KILL
===== o8_add0 =====
tokens: G ADD0 JUST KILL
RT 0 ADD0 0
RT 1 JUST 0
RT 2 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_cite_count,0,0
CL_CHECK,ck_cite_distinct,0,0
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O8] o8_price25
tokens: G ADD25 CITE7 JUST KILL
===== o8_price25 =====
tokens: G ADD25 CITE7 JUST KILL
RT 0 ADD25 0
RT 1 CITE7 0
RT 2 JUST 0
RT 3 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,1,1
CL_CHECK,ck_cite_distinct,1,1
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O8] o8_price100
tokens: G ADD100 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o8_price100 =====
tokens: G ADD100 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD100 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O1] o1_same
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o1_same =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE0 0
RT 9 CITE1 0
RT 10 CITE2 0
RT 11 CITE3 0
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O1] o1_del
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST DEL ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o1_del =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST DEL ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 DEL 0
RT 7 ADD90 0
RT 8 CITE0 0
RT 9 CITE1 0
RT 10 CITE2 0
RT 11 CITE3 0
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_del_cite_count,4,4
CL_CHECK,ck_del_cite_distinct,4,4
CL_CHECK,ck_del_justify,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O1] o1_killt
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILLT ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o1_killt =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILLT ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILLT 0
RT 7 ADD90 0
RT 8 CITE0 0
RT 9 CITE1 0
RT 10 CITE2 0
RT 11 CITE3 0
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O1] o1_ow
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 SLOT3 ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o1_ow =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 SLOT3 ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 OW0 0
RT 7 SLOT3 0
RT 8 ADD90 0
RT 9 CITE0 0
RT 10 CITE1 0
RT 11 CITE2 0
RT 12 CITE3 0
RT 13 JUST 0
RT 14 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O1] o1_partial
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL ADD90 CITE0 CITE4 CITE5 CITE6 JUST KILL
===== o1_partial =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL ADD90 CITE0 CITE4 CITE5 CITE6 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE0 0
RT 9 CITE4 0
RT 10 CITE5 0
RT 11 CITE6 0
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O2] o2_wedge
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILL DEL KILLT OW0 RB
===== o2_wedge =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILL DEL KILLT OW0 RB
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 CITE4 0
RT 6 JUST 0
RT 7 KILL 109
RT 8 DEL 109
RT 9 KILLT 109
RT 10 OW0 109
RT 11 RB 108
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O2] o2_wedge_otherslot
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT3 ADD90 CITE10 CITE11 CITE12 CITE13 JUST KILL
===== o2_wedge_otherslot =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT3 ADD90 CITE10 CITE11 CITE12 CITE13 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 CITE4 0
RT 6 JUST 0
RT 7 KILL 109
RT 8 SLOT3 0
RT 9 ADD90 0
RT 10 CITE10 0
RT 11 CITE11 0
RT 12 CITE12 0
RT 13 CITE13 0
RT 14 JUST 0
RT 15 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O3] o3_basic
tokens: G ADD90 ADD90 SLOT2 CITE0 CITE1 CITE2 CITE3 JUST KILL SLOT3 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o3_basic =====
tokens: G ADD90 ADD90 SLOT2 CITE0 CITE1 CITE2 CITE3 JUST KILL SLOT3 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 ADD90 0
RT 2 SLOT2 0
RT 3 CITE0 0
RT 4 CITE1 0
RT 5 CITE2 0
RT 6 CITE3 0
RT 7 JUST 0
RT 8 KILL 0
RT 9 SLOT3 0
RT 10 CITE0 0
RT 11 CITE1 0
RT 12 CITE2 0
RT 13 CITE3 0
RT 14 JUST 0
RT 15 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O3] o3_interleaved
tokens: G ADD90 ADD90 SLOT2 CITE5 CITE6 CITE7 CITE8 JUST SLOT3 CITE5 CITE6 CITE7 CITE8 JUST KILL SLOT2 KILL
===== o3_interleaved =====
tokens: G ADD90 ADD90 SLOT2 CITE5 CITE6 CITE7 CITE8 JUST SLOT3 CITE5 CITE6 CITE7 CITE8 JUST KILL SLOT2 KILL
RT 0 ADD90 0
RT 1 ADD90 0
RT 2 SLOT2 0
RT 3 CITE5 0
RT 4 CITE6 0
RT 5 CITE7 0
RT 6 CITE8 0
RT 7 JUST 0
RT 8 SLOT3 0
RT 9 CITE5 0
RT 10 CITE6 0
RT 11 CITE7 0
RT 12 CITE8 0
RT 13 JUST 0
RT 14 KILL 0
RT 15 SLOT2 0
RT 16 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O3] o3_alias
tokens: G ADD90 ADD90 SLOT2 CITE0 CITE1 CITE2 CITE3 JUST KILL SLOT3 CITE4294967296 CITE4294967297 CITE4294967298 CITE4294967299 JUST KILL
===== o3_alias =====
tokens: G ADD90 ADD90 SLOT2 CITE0 CITE1 CITE2 CITE3 JUST KILL SLOT3 CITE4294967296 CITE4294967297 CITE4294967298 CITE4294967299 JUST KILL
RT 0 ADD90 0
RT 1 ADD90 0
RT 2 SLOT2 0
RT 3 CITE0 0
RT 4 CITE1 0
RT 5 CITE2 0
RT 6 CITE3 0
RT 7 JUST 0
RT 8 KILL 0
RT 9 SLOT3 0
RT 10 CITE4294967296 0
RT 11 CITE4294967297 0
RT 12 CITE4294967298 0
RT 13 CITE4294967299 0
RT 14 JUST 0
RT 15 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O4] o4_weak0_1cite
tokens: G ADD90 WEAK0 CITE0 JUST KILL
===== o4_weak0_1cite =====
tokens: G ADD90 WEAK0 CITE0 JUST KILL
RT 0 ADD90 0
RT 1 WEAK0 0
RT 2 CITE0 0
RT 3 JUST 0
RT 4 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O4] o4_weak0_zerocites
tokens: G ADD90 WEAK0 JUST KILL
===== o4_weak0_zerocites =====
tokens: G ADD90 WEAK0 JUST KILL
RT 0 ADD90 0
RT 1 WEAK0 0
RT 2 JUST 0
RT 3 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O4] o4_weak0_fullpay
tokens: G ADD90 WEAK0 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o4_weak0_fullpay =====
tokens: G ADD90 WEAK0 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 WEAK0 0
RT 2 CITE0 0
RT 3 CITE1 0
RT 4 CITE2 0
RT 5 CITE3 0
RT 6 JUST 0
RT 7 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O4] o4_str_up_1cite
tokens: G ADD10 STR90 CITE0 JUST KILL
===== o4_str_up_1cite =====
tokens: G ADD10 STR90 CITE0 JUST KILL
RT 0 ADD10 0
RT 1 STR90 0
RT 2 CITE0 0
RT 3 JUST 0
RT 4 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O4] o4_str_down
tokens: G ADD90 STR50 CITE0 JUST KILL
===== o4_str_down =====
tokens: G ADD90 STR50 CITE0 JUST KILL
RT 0 ADD90 0
RT 1 STR50 0
RT 2 CITE0 0
RT 3 JUST 0
RT 4 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O5] o5_dup_lo
tokens: G ADD90 CITE0 CITE4294967296
===== o5_dup_lo =====
tokens: G ADD90 CITE0 CITE4294967296
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE4294967296 111
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O5] o5_dup_hi
tokens: G ADD90 CITE4294967296 CITE0
===== o5_dup_hi =====
tokens: G ADD90 CITE4294967296 CITE0
RT 0 ADD90 0
RT 1 CITE4294967296 0
RT 2 CITE0 111
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O5] o5_dup_2p33
tokens: G ADD90 CITE8589934592 CITE0
===== o5_dup_2p33 =====
tokens: G ADD90 CITE8589934592 CITE0
RT 0 ADD90 0
RT 1 CITE8589934592 0
RT 2 CITE0 111
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O5] o5_dup_p1
tokens: G ADD90 CITE4294967297 CITE1
===== o5_dup_p1 =====
tokens: G ADD90 CITE4294967297 CITE1
RT 0 ADD90 0
RT 1 CITE4294967297 0
RT 2 CITE1 111
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O5] o5_spend_alias
tokens: G ADD90 CITE4294967296 CITE4294967297 CITE4294967298 CITE4294967299 JUST KILL ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o5_spend_alias =====
tokens: G ADD90 CITE4294967296 CITE4294967297 CITE4294967298 CITE4294967299 JUST KILL ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 CITE4294967296 0
RT 2 CITE4294967297 0
RT 3 CITE4294967298 0
RT 4 CITE4294967299 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE0 0
RT 9 CITE1 0
RT 10 CITE2 0
RT 11 CITE3 0
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O5] o5_reject_i32p1
tokens: G ADD90 CITE2147483648
===== o5_reject_i32p1 =====
tokens: G ADD90 CITE2147483648
RT 0 ADD90 0
RT 1 CITE2147483648 2001
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O5] o5_reject_u32m1
tokens: G ADD90 CITE4294967295
===== o5_reject_u32m1 =====
tokens: G ADD90 CITE4294967295
RT 0 ADD90 0
RT 1 CITE4294967295 2001
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O5] o5_accept_i32max
tokens: G ADD90 CITE2147483647
===== o5_accept_i32max =====
tokens: G ADD90 CITE2147483647
RT 0 ADD90 0
RT 1 CITE2147483647 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O6] o6_td_down_1cite
tokens: G ADD90 TD25 CITE0 JUST KILL
===== o6_td_down_1cite =====
tokens: G ADD90 TD25 CITE0 JUST KILL
RT 0 ADD90 0
RT 1 TD25 0
RT 2 CITE0 0
RT 3 JUST 0
RT 4 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O6] o6_td_down_full
tokens: G ADD90 TD25 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o6_td_down_full =====
tokens: G ADD90 TD25 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 TD25 0
RT 2 CITE0 0
RT 3 CITE1 0
RT 4 CITE2 0
RT 5 CITE3 0
RT 6 JUST 0
RT 7 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O6] o6_td_up_1cite
tokens: G ADD25 TD90 CITE0 JUST KILL
===== o6_td_up_1cite =====
tokens: G ADD25 TD90 CITE0 JUST KILL
RT 0 ADD25 0
RT 1 TD90 0
RT 2 CITE0 0
RT 3 JUST 0
RT 4 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O6] o6_td_up_full
tokens: G ADD25 TD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o6_td_up_full =====
tokens: G ADD25 TD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD25 0
RT 1 TD90 0
RT 2 CITE0 0
RT 3 CITE1 0
RT 4 CITE2 0
RT 5 CITE3 0
RT 6 JUST 0
RT 7 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O6] o6_td100
tokens: G ADD90 TD100 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o6_td100 =====
tokens: G ADD90 TD100 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 TD100 0
RT 2 CITE0 0
RT 3 CITE1 0
RT 4 CITE2 0
RT 5 CITE3 0
RT 6 JUST 0
RT 7 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O6] o6_td_rb
tokens: G ADD90 TD50 RB
===== o6_td_rb =====
tokens: G ADD90 TD50 RB
RT 0 ADD90 0
RT 1 TD50 0
RT 2 RB 113
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O7] o7_recite
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL RB CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o7_recite =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL RB CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 RB 0
RT 8 CITE0 111
RT 9 CITE1 111
RT 10 CITE2 111
RT 11 CITE3 111
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O7] o7_rb_unspend
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL RB SLOT3 ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o7_rb_unspend =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL RB SLOT3 ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 RB 0
RT 8 SLOT3 0
RT 9 ADD90 0
RT 10 CITE0 0
RT 11 CITE1 0
RT 12 CITE2 0
RT 13 CITE3 0
RT 14 JUST 0
RT 15 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O7] o7_ow_rb
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 RB SLOT3 ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o7_ow_rb =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 RB SLOT3 ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 OW0 0
RT 7 RB 0
RT 8 SLOT3 0
RT 9 ADD90 0
RT 10 CITE0 0
RT 11 CITE1 0
RT 12 CITE2 0
RT 13 CITE3 0
RT 14 JUST 0
RT 15 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O7] o7_del_rb
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST DEL RB SLOT3 ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== o7_del_rb =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST DEL RB SLOT3 ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 DEL 0
RT 7 RB 0
RT 8 SLOT3 0
RT 9 ADD90 0
RT 10 CITE0 0
RT 11 CITE1 0
RT 12 CITE2 0
RT 13 CITE3 0
RT 14 JUST 0
RT 15 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_del_cite_count,4,4
CL_CHECK,ck_del_cite_distinct,4,4
CL_CHECK,ck_del_justify,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O7] o7_stacked
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL RB RB
===== o7_stacked =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL RB RB
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 RB 0
RT 8 RB 108
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O7] o7_fresh_after_rb
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL RB CITE4 CITE5 CITE6 CITE7 JUST KILL ADD90 CITE4 CITE5 CITE6 CITE7 JUST KILL
===== o7_fresh_after_rb =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL RB CITE4 CITE5 CITE6 CITE7 JUST KILL ADD90 CITE4 CITE5 CITE6 CITE7 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 RB 0
RT 8 CITE4 0
RT 9 CITE5 0
RT 10 CITE6 0
RT 11 CITE7 0
RT 12 JUST 0
RT 13 KILL 0
RT 14 ADD90 0
RT 15 CITE4 0
RT 16 CITE5 0
RT 17 CITE6 0
RT 18 CITE7 0
RT 19 JUST 0
RT 20 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O7] o7_rb_refused
tokens: G ADD90 KILL RB RB WEAK50 RB
===== o7_rb_refused =====
tokens: G ADD90 KILL RB RB WEAK50 RB
RT 0 ADD90 0
RT 1 KILL 109
RT 2 RB 108
RT 3 RB 108
RT 4 WEAK50 0
RT 5 RB 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [O7] o7_rb_empty
tokens: G RB
===== o7_rb_empty =====
tokens: G RB
RT 0 RB 108
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] price0_probe
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 JUST KILL
===== price0_probe =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 OW0 0
RT 7 JUST 0
RT 8 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_cite_count,0,0
CL_CHECK,ck_cite_distinct,0,0
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] price0_fresh4
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 CITE4 CITE5 CITE6 CITE7 JUST KILL
===== price0_fresh4 =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 CITE4 CITE5 CITE6 CITE7 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 OW0 0
RT 7 CITE4 0
RT 8 CITE5 0
RT 9 CITE6 0
RT 10 CITE7 0
RT 11 JUST 0
RT 12 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] price0_nojust
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 KILL
===== price0_nojust =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 OW0 0
RT 7 KILL 110
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] price0_spentride
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL ADD0 CITE0 CITE1 CITE2 CITE3 JUST KILL
===== price0_spentride =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL ADD0 CITE0 CITE1 CITE2 CITE3 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD0 0
RT 8 CITE0 0
RT 9 CITE1 0
RT 10 CITE2 0
RT 11 CITE3 0
RT 12 JUST 0
RT 13 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,0,0
CL_CHECK,ck_cite_distinct,0,0
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_overpay
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILL
===== x_overpay =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 CITE4 0
RT 6 JUST 0
RT 7 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_price50_over
tokens: G ADD50 CITE0 CITE1 CITE2 JUST KILL
===== x_price50_over =====
tokens: G ADD50 CITE0 CITE1 CITE2 JUST KILL
RT 0 ADD50 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 JUST 0
RT 5 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_price25_over
tokens: G ADD25 CITE0 CITE1 JUST KILL
===== x_price25_over =====
tokens: G ADD25 CITE0 CITE1 JUST KILL
RT 0 ADD25 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 JUST 0
RT 4 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_del_over
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST DEL
===== x_del_over =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST DEL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 CITE4 0
RT 6 JUST 0
RT 7 DEL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_killt_over
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILLT
===== x_killt_over =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILLT
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 CITE4 0
RT 6 JUST 0
RT 7 KILLT 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_killn
tokens: G ADD90 KILLN
===== x_killn =====
tokens: G ADD90 KILLN
RT 0 ADD90 0
RT 1 KILLN 113
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_doublekill
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL KILL
===== x_doublekill =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 KILL 103
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_insuff
tokens: G ADD90 CITE0 JUST KILL
===== x_insuff =====
tokens: G ADD90 CITE0 JUST KILL
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 JUST 0
RT 3 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_rb_cite
tokens: G ADD90 CITE0 RB
===== x_rb_cite =====
tokens: G ADD90 CITE0 RB
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 RB 108
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_rb_just
tokens: G ADD90 JUST RB
===== x_rb_just =====
tokens: G ADD90 JUST RB
RT 0 ADD90 0
RT 1 JUST 0
RT 2 RB 108
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_rb_weak
tokens: G ADD90 WEAK50 RB
===== x_rb_weak =====
tokens: G ADD90 WEAK50 RB
RT 0 ADD90 0
RT 1 WEAK50 0
RT 2 RB 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_rb_ow
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 RB
===== x_rb_ow =====
tokens: G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 RB
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 OW0 0
RT 7 RB 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_str_cap
tokens: G ADD90 STR125
===== x_str_cap =====
tokens: G ADD90 STR125
RT 0 ADD90 0
RT 1 STR125 2001
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_slot1
tokens: G SLOT1 ADD90 CITE0
===== x_slot1 =====
tokens: G SLOT1 ADD90 CITE0
RT 0 SLOT1 0
RT 1 ADD90 0
RT 2 CITE0 101
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_slot0
tokens: G SLOT0 ADD90 CITE0
===== x_slot0 =====
tokens: G SLOT0 ADD90 CITE0
RT 0 SLOT0 0
RT 1 ADD90 0
RT 2 CITE0 101
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_slot3
tokens: G SLOT3 ADD90 CITE0
===== x_slot3 =====
tokens: G SLOT3 ADD90 CITE0
RT 0 SLOT3 0
RT 1 ADD90 0
RT 2 CITE0 103
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


## [OBS] x_slot99
tokens: G SLOT99 ADD90 CITE0
===== x_slot99 =====
tokens: G SLOT99 ADD90 CITE0
RT 0 SLOT99 0
RT 1 ADD90 0
RT 2 CITE0 2001
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
== second run: DETERMINISTIC ==


