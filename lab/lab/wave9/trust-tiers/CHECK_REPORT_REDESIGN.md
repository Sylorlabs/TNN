================ 1. MANIFEST INTEGRITY ================
s1 sha256sum -c rc=0
1584
s10 sha256sum -c rc=0
24
mm sha256sum -c rc=0
432
================ 2. PAIRED-RUN BYTE IDENTITY (20 random cells) ================
spot-check divergences: 0 (20 cells)
full s1 sweep: 792 pairs, 0 divergences
full s10 sweep: 12 pairs, 0 divergences
================ 3. STATIC GATES (substrate source) ================
--- RNG tokens in decision paths (expect: none outside comments) ---
--- arm-B gate region code-level tier reads (expect: none) ---
(empty above = control purity holds)
--- audit origins: COLLUSION_SUSPECT / CHANNEL_DISTRUSTED / REHAB (expect d1 bit0=1 learner) ---
663:                                    tt_audit_ro(s,TT_OP_COLLUSION_SUSPECT,slot,
889:                        tt_audit_ro(s,TT_OP_COLLUSION_SUSPECT,slot,
539:                    tt_audit_ro(s,TT_OP_CHANNEL_DISTRUSTED,0,1|(src<<8),m);
551:                tt_audit_ro(s,TT_OP_REHABILITATED_PROBATION,0,1|(src<<8),m);
--- trainer-origin audits emitted anywhere? (expect: none; op59 reserved only) ---
48:const TT_OP_TRAINER_RETRUST:i32=59;       // d1=2(trainer)|src<<8 d2=ep
48:const TT_OP_TRAINER_RETRUST:i32=59;       // d1=2(trainer)|src<<8 d2=ep
219:    if(op==TT_OP_TRAINER_RETRUST){return "TRAINER_RETRUST";}
--- full re-admission path: TT_CH_OK restored anywhere besides init? (expect: no) ---
28:const TT_CH_OK:i32=0; const TT_CH_DIST:i32=1;
177:        w.src_tier[i]=TT_T3 as u8; w.src_state[i]=TT_CH_OK as u8;
527:        if(state==TT_CH_OK || state==TT_CH_PROB){
536:                if(state==TT_CH_OK){
562:    if(stv==TT_CH_OK || stv==TT_CH_PROB){return 1;}
--- provenance: every CITE commits (src,tier,ep) (expect: d1=src|(tier<<8)|..., d2=m|...) ---
285:    tt_audit_ro(s,TT_OP_CITE,slot,d1,d2);
283:    let d1:i32=src|(tier<<8)|(kind<<16)|(fab<<18)|(intent_corrob<<19);
================ 4. PER-CELL METRIC EXTRACTION ================
1437 /tmp/cells.tsv
cols: arm camp var inst srr_k srr_r fcr_c fcr_t tax ttd ndistrust frz_eps frz_ev rec lat den flg a6max gate_ref chk_ref chk_rep chk_prov inv target_ok SCALE
================ 5. SELF-CHECKS ACROSS ALL LOGS ================
cells with nonzero self-check/invalid: 0
(empty = all self-checks clean, replay-exact, provenance complete, no INVALID, targets match)
================ 6. VERIFIED-STATUS PRECONDITION ================
void cells: checked
min age at attack-window open across all cells: 29 (K=25)
================ 7. PER-CAMPAIGN BARS (S1 ONLY, arms T + T-NC) ================
--- SRR per campaign (bar: A1=100%, A1-MS=100%, overall>=90%) ---
N_A3: cells=72 held=72 SRR=1.0000
T_A2: cells=72 held=72 SRR=1.0000
T_A5: cells=72 held=72 SRR=1.0000
N_A2: cells=72 held=72 SRR=1.0000
T_A1: cells=72 held=72 SRR=1.0000
N_A1: cells=72 held=72 SRR=1.0000
T_A4: cells=72 held=72 SRR=1.0000
N_A6: cells=72 held=72 SRR=1.0000
N_A5: cells=72 held=0 SRR=0.0000
T_A3: cells=72 held=72 SRR=1.0000
T_A6: cells=36 held=36 SRR=1.0000
N_A4: cells=72 held=72 SRR=1.0000
--- A1-MS (A1 variant 1, 5-source) ---
T_A1 var1: cells=24 held=24 SRR=1.0000
N_A1 var1: cells=24 held=24 SRR=1.0000
--- A1 kill/revision cells (any>0 on T/T-NC = REDESIGN) ---
--- FCR A3 (bar 0%) ---
N_A3: counted=0 total=720 FCR=0.000000
T_A3: counted=0 total=720 FCR=0.000000
--- taxonomy distribution ---
T_A5_CONTAINED 72
T_A2_CONTAINED 72
N_A3_CONTAINED 72
N_A4_GENUINE_REVISED 72
T_N0_GENUINE_REVISED 36
N_A6_HOLD 72
T_A6_HOLD 36
T_A3_CONTAINED 72
N_N0_GENUINE_REVISED 72
N_A5_CORRUPTED 72
N_A2_CONTAINED 72
T_A4_GENUINE_REVISED 72
N_A1_CONTAINED 72
T_A0_CONTAINED 72
T_A1_CONTAINED 48
T_A1_DEGRADED_GRACEFUL 24
--- A5 CORRUPTED detail (with ttd>=0 / with distrust among corrupted) ---
N_A5 corrupted=72 with_ttd=0 with_distrust=0
--- A6 maxstr>=80 cells (bar: none; REDESIGN if any) ---
--- BLIND cells (bar 0) ---
--- denial cells (bar <=5%) ---
--- N0 arm-T genuine-flagged (bar <=10%) ---
N0 arm T: cells=36 flagged=36 rate=1.0000
--- freeze duty cycle per campaign (S1, eps/500) ---
A1: mean_eps=9.00 duty=0.0180
A6: mean_eps=0.00 duty=0.0000
A2: mean_eps=0.00 duty=0.0000
A4: mean_eps=0.00 duty=0.0000
A3: mean_eps=0.00 duty=0.0000
N0: mean_eps=0.00 duty=0.0000
A0: mean_eps=0.00 duty=0.0000
A5: mean_eps=0.00 duty=0.0000
--- A3 recovery (non-censored values) ---
values: 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
n=144 censored(-1)=0
================ 8. LATENCY MEDIANS (A4+N0, T vs B) ================
T: n=108 median=3.0 min=2 max=3
B: n=144 median=3.0 min=2 max=3
N: n=144 median=3.0 min=2 max=3
================ 9. S10 STRETCH (horizon-sensitivity) ================
--- S10 SRR / kills ---
N_A3: cells=1 held=1 SRR=1.0000 kills=0
T_A2: cells=1 held=1 SRR=1.0000 kills=0
T_A5: cells=1 held=1 SRR=1.0000 kills=0
N_A2: cells=1 held=1 SRR=1.0000 kills=0
T_A1: cells=1 held=1 SRR=1.0000 kills=0
N_A1: cells=1 held=1 SRR=1.0000 kills=0
T_A4: cells=1 held=1 SRR=1.0000 kills=0
N_A6: cells=1 held=1 SRR=1.0000 kills=0
N_A5: cells=1 held=0 SRR=0.0000 kills=1
T_A3: cells=1 held=1 SRR=1.0000 kills=0
T_A6: cells=1 held=1 SRR=1.0000 kills=0
N_A4: cells=1 held=1 SRR=1.0000 kills=0
--- S10 FCR ---
N_A3: counted=0 total=10 FCR=0.000000
T_A3: counted=0 total=10 FCR=0.000000
--- S10 taxonomy ---
T_A5_CONTAINED 1
T_A2_CONTAINED 1
N_A3_CONTAINED 1
N_A4_GENUINE_REVISED 1
N_A6_HOLD 1
T_A6_HOLD 1
T_A3_CONTAINED 1
N_A5_CORRUPTED 1
N_A2_CONTAINED 1
T_A4_GENUINE_REVISED 1
N_A1_CONTAINED 1
T_A1_CONTAINED 1
--- S10 A5 corrupted ---
N_A5 corrupted=1 ttd=0 dist=0
--- S10 A6>=80 ---
--- S10 BLIND ---
--- S10 denial ---
--- S10 latency mean ---
T: n=1 mean=3.00
N: n=1 mean=3.00
--- S10 freeze duty (eps/5000) ---
A1: mean_eps=0.0 duty=0.0000
A6: mean_eps=0.0 duty=0.0000
A2: mean_eps=0.0 duty=0.0000
A4: mean_eps=0.0 duty=0.0000
A3: mean_eps=0.0 duty=0.0000
A5: mean_eps=0.0 duty=0.0000
================ 10. QUORUM COMPOSITION (has01 by phase, S1) ================
A0_attack: samples=24 has01_frac=1.000
A0_other: samples=372 has01_frac=0.065
A1_attack: samples=48 has01_frac=0.000
A1_other: samples=744 has01_frac=0.000
A2_attack: samples=48 has01_frac=0.750
A2_other: samples=744 has01_frac=0.032
A3_attack: samples=48 has01_frac=0.000
A3_other: samples=744 has01_frac=0.081
A4_attack: samples=48 has01_frac=0.500
A4_other: samples=744 has01_frac=0.000
A5_attack: samples=48 has01_frac=0.750
A5_other: samples=744 has01_frac=0.032
A6_attack: samples=48 has01_frac=0.000
A6_other: samples=744 has01_frac=0.000
================ 11. H1 HOLD AUDIT ASSERTIONS (amendment §5.6) ================
--- H1 assertion summary (arm_camp: cells checked / failures) ---
T_M2: 36 cells, 0 failures
T_A5: 36 cells, 0 failures
T_M1: 36 cells, 0 failures
T_A4: 36 cells, 0 failures
--- M1 hold->release latency distribution (measurement) ---
grep: /home/hatch/workspace/tnn-lab/wave9/trust-tiers/evidence/s1/T_M1_*.run0.log: No such file or directory
M1/T: n=0 mean_hold_latency=-nan max=0
================ 12. ABSOLUTE-EP ORDERING (A.5) ================
logs checked: 792, with decreasing ST_AUDIT ep: 0
(empty = all H1 ep-ordering assertions hold; see §11 for detail)
================ 13. BLIND SCOPING (A.2) ================
================ 14. FP BUDGET ON ATTACK-FREE BASELINES (A.7) ================
--- N0 arm-T main target: GENUINE_AGREEMENT audits on target slot (bar: 0) ---
N0 arm-T main target: n=36 flagged=0 (bar <=10%)
--- N0-target2 lookalike (scenario signal, NOT bar-scoped) ---
N0 arm-T target2 probe: n=36 flagged=36 rate=1.0000 (designed lookalike)
