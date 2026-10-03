# PREREG: NT-CAPACITY-SWEEP -- the assoc pin's opportunity-cost curve (CAP=20/22/24)

## 1. Question

NT-TEACHASSOC (ASSOC-CONFIRMED) established: D6 (same-subject
teaching-stream association pin, W=20) rescues the residual chain
(avail160 0->4) at CAP=22 with a measured 50% false-positive rate
(the decoy chain is pinned and protected despite never being used).
NT-TEACHASSOC-CTRL confirmed attribution (D6 inert without
exploratory queries -> residual NOT rescued). The honest boundary
recorded in NT-TEACHASSOC Section 9: "at CAP=20 (1.25x) the four
assoc pins structurally displace an A-link on pass 2 (every R=0
slot pinned), which would break K2. Pinning useless entries has
opportunity cost."

This lane quantifies that cost as a capacity curve. Three arms run
the NT-TEACHASSOC world verbatim except for capacity:

- ARM20: CAP=20 (25 keys / 20 slots = 1.25x). Predicted: the rescue
  holds (avail160=4) but the four assoc pins displace A-link 118 on
  pass 2 -> u=3, forget=1, phev=1. The opportunity cost is real and
  exactly characterized.
- ARM22: CAP=22 (1.14x). Predicted: byte-exact reproduction of the
  NT-TEACHASSOC frozen numbers (regression bar).
- ARM24: CAP=24 (1.04x). Predicted: the rescue holds (avail160=4),
  zero opportunity cost (u=4, forget=0, phev=0), lower pressure
  (nevict=10); the pins are redundant for the residual but still
  protect the decoy (FP cost persists).

Key questions frozen: (a) at what capacity does the opportunity
cost become unacceptable (A-link displaced)? (b) is there a
capacity where D6's benefit outweighs its cost? (c) what is the
shape of the tradeoff curve?

## 2. Subject (frozen)

Learner: the NT-TEACHASSOC learner verbatim (D1 victim
checkpoints, D4 min-reads/max-ins base comparator, D5
revision-target pinning via per-slot pendtgt, D6 association pin
via tick/qstart_obs/W=20, sticky except cleared by in-place
revision; eviction skips D5-pinned OR assoc-pinned slots with the
D4 fallback unchanged). The ONLY change is capacity
parameterization: `cl_new(ns)` allocates the memory layout for the
passed ns (all region accessors are already ns-relative; the fixed
3380-byte allocation becomes `20+ns*44+1728+288+ns*4+288`, which
equals 3380 at ns=22). No rule, workload, tick model, window,
oracle, or probe change. With ns=22 the learner reduces exactly to
the NT-TEACHASSOC binary's learner.

Three arms, one binary, sequential in main(): R6-CAP20,
R6-CAP22, R6-CAP24. Single K arm (K=6) per capacity, as
NT-TEACHASSOC. W=20 frozen.

## 3. Workload (frozen)

NT-TEACHASSOC Section 3 verbatim at all three capacities:
phase-1 trainA (14 A links), final probeA, exploratory episode
(q(160),q(161),q(170),q(171) at ticks 52..55, all miss, all
observed), 6 fixed passes of teachB (K-pass = pass 1 only:
15 teachings at ticks 56..70 in LAST order; other passes 10
teachings), per-pass probes q(100) vs 152 and q(160) vs 162,
then retest/bprobe/resprobe. Key inventory is capacity-invariant:
14 A-links + 6 FREQ novels + 4 assoc-chain keys (160,161,170,171)
+ 1 RARE (148) = 25 keys. Pressures: 25/20 = 1.25x, 25/22 =
1.14x, 25/24 = 1.04x. Teach ticks for the assoc-chain installs
are capacity-invariant (66,67,68,69; gap 14 <= W=20), so all four
assoc pins fire on every arm.

## 4. Protocol (frozen)

- `run_arm(CAP, K=6, ...)`: cl_new(CAP); trainA; probeA;
  exploratory queries; 6 passes (teachB + q(100)/q(160) probes);
  retest; bprobe; resprobe; assoc stats; eviction histogram
  (100..171); per-arm output block tagged R6-CAP20 / R6-CAP22 /
  R6-CAP24.
- Build: `znc ntsweep_full.zag -o ntsweep_bin` under
  safebin-only PATH.
- Run `ntsweep_bin` 3 times (-> ntsweep_run1/2/3.txt). Require
  byte-identical (cmp) across all 3; record sha256 of runs,
  binary, source.
- Per-arm kill bars are computed in-binary from the frozen
  numbers in Sections 5/7 and printed per arm; the overall
  verdict is printed last.

## 5. Frozen predictions (hand-derived by tracing the frozen rules)

Phase 1 and the exploratory episode are capacity-invariant:
ttcA=2, probeA=8, tick=56 after exploratory, zero assoc pins in
phase 1, qstart_obs[160]=52,[161]=53,[170]=54,[171]=55.
Post-phase-1 reads: 100:3, 101:6, 103:3, 104:3, 105:6, 107:3,
108:3, 109:3, 111:3, 112:3, 114:3, 115:3, 117:3, 118:3.
Install order (ins): 100:1,101:2,103:3,104:4,105:5,107:6,108:7,
109:8,111:9,112:10,114:11,115:12,117:13,118:14.

### 5.1 ARM20 (CAP=20) -- the opportunity-cost arm

Pass 1 (teaches 56..70): 100@56 (ref 0->1, pt[100-slot]=148),
104@57 (ref 0->1, pt[104-slot]=130), 101@58,105@59 (sup 2->3),
130@60..144@65 installs (ins 15..20, ap=0; nkeys=20=CAP).
160@66: EVICT #1: pinned={130:D5} (assoc: none yet installed);
R=0 unpinned {131,140,141,143,144} -> max ins -> 144.
Install 160 (ins 21, ap=1). 161@67: EVICT #2: pinned={130,160};
victim 143. Install 161 (ins 22, ap=1). 170@68: EVICT #3:
pinned={130,160,161}; victim 141. Install 170 (ins 23, ap=1).
171@69: EVICT #4: pinned +170; victim 140. Install 171 (ins 24,
ap=1). 148@70: EVICT #5: pinned={130,160,161,170,171}; R=0
unpinned {131} -> victim 131. Install 148 (ins 25, ap=0).
nevict=5. Installed: 14 A + {130,160,161,170,171,148}.
Absent: {131,140,141,143,144}. Probes: q(100) MISS (p1=0),
q(160) HIT (r1=1; reads 160:1,161:1).

Pass 2 (teaches 73..82): 100@73 (ref 1->2, pt=148), 104@74
(ref 1->2, pt=130), 101@75,105@76 (sup 3->4), 130@77 (agree
sup 1->2). 131@78: restore -> EVICT #6: D5-pinned={130,148}
(pt[100-slot]=148 and pt[104-slot]=130, both slots valid);
assoc-pinned={160,161,170,171}; ALL R=0 slots are pinned, so
the victim comes from R=3 A-links -> max ins -> 118 (ins 14).
**This is the structural displacement: A-link 118 is evicted
to make room for the assoc pins.** evh(118)=1. Install 131
(ins 26, ap=0; restored sup=1 -> update agree -> sup=2).
140@79: restore -> EVICT #7: R=0 unpinned {131} -> victim 131.
141@80: -> EVICT #8: victim 140. 143@81: -> EVICT #9: victim
141. 144@82: -> EVICT #10: victim 143. nevict=10. Installed:
13 A (118 gone) + {130,148,160,161,170,171} + {144}. Absent:
{118,131,140,141,143}. Probes: q(100) MISS (p2=0; sup=2,ref=2),
q(160) HIT (r2=1).

Pass 3 (teaches 85..94): 100@85 REVISE ->148 (sup=1,ref=0,
pt=0,assoc cleared); 104@86 REVISE ->130; 101@87,105@88
(sup 4->5); 130@89 (agree sup 2->3). 131@90: restore ->
EVICT #11: no D5 pins (pt all 0); R=0 {130,148,144} -> max ins
-> 144. 140@91: -> EVICT #12: victim 131. 141@92: -> EVICT
#13: victim 140. 143@93: -> EVICT #14: victim 141. 144@94:
absent -> restore -> EVICT #15: victim 143. nevict=15.
Installed: 13 A + {130,148,160,161,170,171} + {144}.
Probes: q(100) HIT (p3=1; 100->148->152), q(160) HIT (r3=1).

Pass 4 (teaches 97..106): steady state. 131 restore ->
EVICT #16: victim 144; 140 -> #17: victim 131; 141 -> #18:
victim 140; 143 -> #19: victim 141; 144 -> #20: victim 143.
nevict=20. Probes HIT/HIT (p4=1, r4=1).

Pass 5: identical: EVICTs #21..#25 (144,131,140,141,143).
nevict=25. p5=1, r5=1.

Pass 6: identical: EVICTs #26..#30 (144,131,140,141,143).
nevict=30. p6=1, r6=1.

Retest: q(100)=152 HIT; q(104): 104->130 (sup 4) ->131=ansb
HIT -> c=2. NC: q(103),q(107) HIT -> nc=2. U: q(108),q(111),
q(114) HIT; q(117): 117->118, then cl_find(118,1) -> -1
(118 evicted pass 2, never restored -- teachB never teaches
118) -> MISS -> u=3, forget=1. bprobe: q(130): 130->131,
predict(131,1) -> -1 (131 absent at end) -> MISS; q(140),
q(143) absent -> MISS -> bprobe=0. resprobe: q(160)=162 HIT=1.

Frozen ARM20 summary: ttcA=2, probeA=8, nevict=30, phev=1;
p1..p6 = 0,0,1,1,1,1 (avail100=4);
r1..r6 = 1,1,1,1,1,1 (avail160=4);
c=2, nc=2, u=3, forget=1, bprobe=0, resprobe=1;
apin=4, dec=1, res=1, useless=2 (fprate=50);
evh(160)=evh(161)=evh(170)=evh(171)=evh(148)=0, evh(118)=1;
EVHIST: 118=1, 131=6, 140=6, 141=6, 143=6, 144=5 (sum 30).

### 5.2 ARM22 (CAP=22) -- the regression arm

Byte-exact reproduction of the NT-TEACHASSOC frozen numbers
(PREREG Section 5.8 as amended): ttcA=2, probeA=8, nevict=22,
phev=0; p1..p6 = 0,0,1,1,1,1 (avail100=4);
r1..r6 = 1,1,1,1,1,1 (avail160=4);
c=2, nc=2, u=4, forget=0, bprobe=1, resprobe=1;
apin=4, dec=1, res=1, useless=2 (fprate=50);
evh(148)=evh(118)=evh(160)=evh(161)=evh(170)=evh(171)=0;
EVHIST: 140=5, 141=6, 143=6, 144=5 (sum 22).

### 5.3 ARM24 (CAP=24) -- the slack arm

Pass 1 (teaches 56..70): installs 130..171 fill nkeys to 24
(ins 15..24; 160/161/170/171 ap=1 at ticks 66..69).
148@70: nkeys=24=CAP -> EVICT #1: pinned={130:D5}
+{160,161,170,171:assoc}; R=0 unpinned {131,140,141,143,144}
-> max ins -> 144. Install 148 (ins 25, ap=0). nevict=1.
Installed: 14 A + {130,131,140,141,143} + {160,161,170,171,148}.
Absent: {144}. Probes: q(100) MISS (p1=0), q(160) HIT (r1=1).

Pass 2 (teaches 73..82): 100@73 (ref 1->2, pt=148), 104@74
(ref 1->2, pt=130), 101@75,105@76 (sup 3->4),
130@77..143@81 agrees (sup 1->2). 144@82: absent -> restore
-> EVICT #2: D5-pinned={130,148}; assoc={160,161,170,171};
R=0 unpinned {131,140,141,143} -> max ins -> 143.
Install 144 (ins 26, ap=0; restored sup=1 -> sup=2).
nevict=2. Installed: 14 A + {130,131,140,141,144} + pins + 148.
Absent: {143}. Probes: q(100) MISS (p2=0), q(160) HIT (r2=1).

Pass 3 (teaches 85..94): 100@85 REVISE ->148; 104@86 REVISE
->130; 101@87,105@88 (sup 4->5); 130@89..141@92 agrees
(sup 2->3). 143@93: absent -> restore -> EVICT #3: no D5 pins;
R=0 {130,131,140,141,144,148} -> max ins -> 144 (ins 26).
Install 143 (ins 27, sup 2). 144@94: absent -> restore ->
EVICT #4: R=0 {130,131,140,141,148,143} -> max ins -> 143
(ins 27). Install 144 (ins 28; restored sup=2 -> sup=3).
nevict=4. Installed: 14 A + {130,131,140,141,144} + pins + 148.
Absent: {143}. Probes: q(100) HIT (p3=1), q(160) HIT (r3=1;
reads 148:1).

Pass 4 (teaches 97..106): 143@105: restore -> EVICT #5:
R=0 {130,131,140,141,144} (148: R=1) -> max ins -> 144
(ins 28). Install 143 (ins 29, sup 3). 144@106: absent ->
restore -> EVICT #6: victim 143 (ins 29). Install 144
(ins 30, sup 4). nevict=6. p4=1, r4=1.

Pass 5: identical: EVICTs #7 (144), #8 (143). nevict=8.
p5=1, r5=1.

Pass 6: identical: EVICTs #9 (144), #10 (143). nevict=10.
p6=1, r6=1.

Retest: c=2 (100->148->152; 104->130 (sup 4) ->131),
nc=2, u=4 (all A links intact, 118 never evicted),
forget=0. bprobe: q(130)=132 HIT; q(140): 140->141->142 HIT
(140 and 141 both installed at end); q(143) absent MISS ->
bprobe=2. resprobe=1.

Frozen ARM24 summary: ttcA=2, probeA=8, nevict=10, phev=0;
p1..p6 = 0,0,1,1,1,1 (avail100=4);
r1..r6 = 1,1,1,1,1,1 (avail160=4);
c=2, nc=2, u=4, forget=0, bprobe=2, resprobe=1;
apin=4, dec=1, res=1, useless=2 (fprate=50);
evh(160)=evh(161)=evh(170)=evh(171)=evh(148)=evh(118)=0;
EVHIST: 143=5, 144=5 (sum 10).

Trace-derived observation (NOT a frozen bar, NOT directly
tested by this lane): at CAP=24 the residual's reads alone
would likely keep it safe (it is never an eviction candidate
after pass 1), so D6's rescue benefit is redundant there while
its FP cost (decoy protected, apin=4, useless=2) persists;
without D6 the pass-1 victim would have been 171 (youngest
R=0), not 144. The lane tests what D6 DOES at CAP=24, not the
no-D6 counterfactual.

## 6. Assembly, build, run (frozen)

- Single source file `ntsweep_full.zag`: the NT-TEACHASSOC
  learner/oracles verbatim EXCEPT (a) `cl_new(ns)` allocates
  `20+ns*44+1728+288+ns*4+288` bytes (ns-relative; 3380 at
  ns=22), (b) `run_arm` takes CAP and calls `cl_new(CAP)`,
  (c) `main` runs the three arms sequentially
  (R6-CAP20, R6-CAP22, R6-CAP24), (d) per-arm kill bars per
  Section 7 computed in-binary and printed. Tag NTSWEEP.
- Build: `znc ntsweep_full.zag -o ntsweep_bin` under
  safebin-only PATH.
- Run `ntsweep_bin` 3 times; outputs `ntsweep_run1.txt`,
  `ntsweep_run2.txt`, `ntsweep_run3.txt`. Require byte-identical
  (cmp) and record sha256.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic
  output only via the single-buffer cursor helpers + one
  `_zag_raw_syscall` write (never `_zag_print`); no `!(A && B)`
  in while conditions (De Morgan); if-nesting mirrors the
  frozen NT-TEACHASSOC template shapes (flat, 1-deep); no
  `[]u8 as *u8` casts (thread `_zag_malloc as *u8`).

## 7. Frozen kill bars

Per-arm bars; all exact. (out offsets as NT-TEACHASSOC:
0 ttcA, 4 probeA, 8 nevict, 12 c, 16 nc, 20 u, 24 forget,
28 phev, 32 bprobe, 36 avail100, 64 evh148, 68 evh118,
72 avail160, 100 evh160, 104 evh161, 108 resprobe, 112 apin,
116 dec, 120 res, 124 useless, 128 evh170, 132 evh171,
136 evh140, 140 evh141, 144 evh143, 148 evh144; plus
out+152 evh118? no -- evh118 is at 68. evh131 is NOT in the
out array; the in-binary S5 check reads it via evh_get.)

ARM20 (R6-CAP20):
- S1 (learnability; else arm VOID): ttcA in 1..50 AND probeA=8.
- S2 (rescue holds): avail160=4 AND resprobe=1 AND evh160=0
  AND evh161=0.
- S3 (FP cost confirmed): dec=1 AND useless=2.
- S4 (opportunity-cost signature): phev=1 AND evh118=1 AND
  u=3 AND forget=1 AND nc=2 AND c=2.
- S5 (pressure exact): nevict=30 AND evh148=0 AND evh131=6
  AND evh140=6 AND evh141=6 AND evh143=6 AND evh144=5 AND
  bprobe=0.
- Arm verdict: COST-CONFIRMED iff S1..S5 all 1; else
  OFF-TRACE (REPORT names the failing bars).

ARM22 (R6-CAP22; regression of NT-TEACHASSOC K1-K7):
- R1: ttcA in 1..50 AND probeA=8.
- R2: nc=2 AND u=4.
- R3: avail160=4 AND resprobe=1 AND evh160=0 AND evh161=0.
- R4: c=2 AND forget=0.
- R5: nevict=22 AND evh148=0 AND phev=0 AND evh140=5 AND
  evh141=6 AND evh143=6 AND evh144=5.
- R6: avail100=4 AND nevict>0.
- R7: dec=1 AND useless=2.
- Arm verdict: REPRODUCED iff R1..R7 all 1; else
  REGRESSION-FAIL.

ARM24 (R6-CAP24):
- T1 (learnability; else arm VOID): ttcA in 1..50 AND probeA=8.
- T2 (rescue holds): avail160=4 AND resprobe=1 AND evh160=0
  AND evh161=0.
- T3 (FP cost confirmed): dec=1 AND useless=2.
- T4 (no opportunity cost): phev=0 AND evh118=0 AND u=4 AND
  forget=0 AND nc=2 AND c=2.
- T5 (pressure exact): nevict=10 AND evh148=0 AND evh143=5
  AND evh144=5 AND bprobe=2.
- Arm verdict: SLACK-CONFIRMED iff T1..T5 all 1; else
  OFF-TRACE (REPORT names the failing bars).

## 8. Verdict mapping (frozen)

- Any arm with its S1/R1/T1 = 0 -> SWEEP-VOID (apparatus
  broken; no curve reading).
- ARM22 != REPRODUCED -> SWEEP-REGRESSION-FAIL (the baseline
  moved; the curve is uninterpretable).
- ARM20 != COST-CONFIRMED -> report the actual ARM20 numbers;
  the displacement prediction is falsified as traced.
- ARM24 != SLACK-CONFIRMED -> report the actual ARM24 numbers;
  the slack prediction is falsified as traced.
- Else -> CURVE-CONFIRMED: the opportunity-cost curve is
  exactly as traced -- rescue at all three capacities;
  unacceptable opportunity cost (A-link displaced, u=3,
  forget=1) at CAP=20 only; clean rescue at CAP=22;
  redundant-but-harmless pins at CAP=24 (FP cost persists).

Predicted verdict: CURVE-CONFIRMED.

## 9. Honest boundaries (frozen)

- The sweep varies capacity ONLY. W=20, K=6, M=6, contradiction
  magnitude, decoy design, and exploratory gap (14 ticks) are
  all fixed. The curve is a 3-point slice, not a general
  capacity law.
- The 50% FP rate is world-relative (one decoy chain, never
  used), as in NT-TEACHASSOC; it is identical on all three arms
  by construction of the decoy.
- No no-D6 control arms are run in this lane; the CAP=24
  redundancy observation in Section 5.3 is trace-derived
  reasoning, explicitly not a tested counterfactual.
- The LINKS are memorized associations; no rule induction
  tested; no L2/L3 claim.
- evh131 is checked in-binary via evh_get (it has no out-array
  slot in the NT-TEACHASSOC layout); all other checked
  quantities use the frozen out offsets.
- This is a non-ledger task (claim minting paused): no ledger
  update whatever the verdict.
