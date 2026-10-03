# PREREG: NT-CAPACITY-TIPPOINT -- locating the exact opportunity-cost tipping point (CAP=21)

## 1. Question

NT-CAPACITY-SWEEP (CURVE-CONFIRMED) measured the D6 assoc pin's
opportunity-cost curve at three capacities: CAP=20 (cost YES:
A-link 118 displaced, u=3, forget=1, phev=1, nevict=30), CAP=22
(clean: u=4, forget=0, phev=0, nevict=22), CAP=24 (clean, nevict=10).
The retention cost is a step function (YES at 20, NO at 22/24), but
CAP=21 was never run: the exact integer tipping point is not located.

This lane runs CAP=21 (25 keys / 21 slots = 1.19x) in the
NT-TEACHASSOC world verbatim except capacity, plus a CAP=22
regression arm in the same binary. Key questions frozen: (a) at
CAP=21 does the opportunity cost appear (118 displaced, u=3,
forget=1) or is the arm clean like CAP=22 (u=4, forget=0)?
(b) what is the exact integer CAP threshold where the cost appears?
(c) what is the mechanistic explanation (pinned slots vs available
R=0 slots at the critical eviction)?

## 2. Subject (frozen)

Learner: the NT-CAPACITY-SWEEP learner verbatim (D1 victim
checkpoints, D4 min-reads/max-ins base comparator, D5
revision-target pinning via per-slot pendtgt, D6 association pin
via tick/qstart_obs/W=20, sticky except cleared by in-place
revision; eviction skips D5-pinned OR assoc-pinned slots with the
D4 fallback unchanged). The ONLY change is the arm list:
`run_arm` is called with CAP=21 and CAP=22 (regression).
No rule, workload, tick model, window, oracle, or probe change.
With CAP=22 the binary reduces exactly to the sweep's ARM22.

Two arms, one binary, sequential in main(): R6-CAP21 (the tipping
arm), R6-CAP22 (regression of the sweep's ARM22 numbers). Single K
arm (K=6) per capacity, as NT-TEACHASSOC. W=20 frozen.

## 3. Workload (frozen)

NT-TEACHASSOC Section 3 verbatim at both capacities: phase-1
trainA (14 A links), final probeA, exploratory episode (q(160),
q(161), q(170), q(171) at ticks 52..55, all miss, all observed),
6 fixed passes of teachB (K-pass = pass 1 only: 15 teachings at
ticks 56..70 in LAST order; other passes 10 teachings), per-pass
probes q(100) vs 152 and q(160) vs 162, then retest/bprobe/resprobe.
Key inventory is capacity-invariant: 14 A-links + 6 FREQ novels +
4 assoc-chain keys (160,161,170,171) + 1 RARE (148) = 25 keys.
Pressures: 25/21 = 1.19x, 25/22 = 1.14x. Teach ticks for the
assoc-chain installs are capacity-invariant (66,67,68,69; gap 14
<= W=20), so all four assoc pins fire on both arms.

## 4. Protocol (frozen)

- `run_arm(CAP, K=6, ...)`: cl_new(CAP); trainA; probeA;
  exploratory queries; 6 passes (teachB + q(100)/q(160) probes);
  retest; bprobe; resprobe; assoc stats; eviction histogram
  (100..171); per-arm output block tagged R6-CAP21 / R6-CAP22.
- Build: `znc nttip_full.zag -o nttip_bin` under safebin-only PATH.
- Run `nttip_bin` 3 times (-> nttip_run1/2/3.txt). Require
  byte-identical (cmp) across all 3; record sha256 of runs,
  binary, source.
- Per-arm kill bars are computed in-binary from the frozen
  numbers in Sections 5/7 and printed per arm; the overall
  verdict is printed last.

## 5. Frozen prediction (hand-derived by tracing the frozen rules)

Phase 1 and the exploratory episode are capacity-invariant:
ttcA=2, probeA=8, tick=56 after exploratory, zero assoc pins in
phase 1, qstart_obs[160]=52,[161]=53,[170]=54,[171]=55.
Post-phase-1 reads: 100:3, 101:6, 103:3, 104:3, 105:6, 107:3,
108:3, 109:3, 111:3, 112:3, 114:3, 115:3, 117:3, 118:3.
Install order (ins): 100:1,101:2,103:3,104:4,105:5,107:6,108:7,
109:8,111:9,112:10,114:11,115:12,117:13,118:14.

### 5.1 ARM21 (CAP=21) -- the tipping arm. Predicted: CLEAN.

Pass 1 (teaches 56..70): 100@56 (ref 0->1, pt[100-slot]=148),
104@57 (ref 0->1, pt[104-slot]=130), 101@58,105@59 (sup 2->3),
130@60..144@65 installs (ins 15..20; nkeys=20<21 at 160@66, so
160 installs with NO eviction, ins 21, ap=1, nkeys=21).
161@67: EVICT #1: pinned={130:D5}; R=0 unpinned
{131,140,141,143,144} -> max ins -> 144. Install 161 (ins 22,
ap=1). 170@68: EVICT #2: pinned={130,160}; victim 143 (ins 19).
Install 170 (ins 23, ap=1). 171@69: EVICT #3: pinned={130,160,
161}; victim 141 (ins 18). Install 171 (ins 24, ap=1). 148@70:
EVICT #4: pinned={130,160,161,170,171}; R=0 unpinned {131,140}
-> max ins -> 140 (ins 17). Install 148 (ins 25, ap=0).
nevict=4. Installed: 14 A + {130,131,148} + {160,161,170,171}.
Absent: {140,141,143,144}. Probes: q(100) MISS (p1=0), q(160)
HIT (r1=1; reads 160:1,161:1).

Pass 2 (teaches 73..82): 100@73 (ref 1->2, pt=148), 104@74
(ref 1->2, pt=130), 101@75,105@76 (sup 3->4), 130@77 (agree sup
2->3). 131@78: 131 IS INSTALLED (it survived pass 1) -> agree
sup 2->3, NO eviction. 140@79: restore -> EVICT #5:
D5-pinned={130,148}, assoc-pinned={160,161,170,171}; the single
unpinned R=0 slot is 131 (reads 0; all 14 A-links have R>=3:
100:4,101:7,105:6, rest 3) -> victim 131. Install 140 (ins 26,
restored sup=2 -> agree sup=3). 141@80: -> EVICT #6: R=0
unpinned {140 (ins 26)} -> victim 140. Install 141 (ins 27,
sup 3). 143@81: -> EVICT #7: victim 141. Install 143 (ins 28,
sup 3). 144@82: -> EVICT #8: victim 143. Install 144 (ins 29,
sup 3). nevict=8. Installed: 14 A + {130,148,144} + pins.
Absent: {131,140,141,143}. Probes: q(100) MISS (p2=0; sup=2,
ref=2), q(160) HIT (r2=1).

Pass 3 (teaches 85..94): 100@85 REVISE ->148 (sup=1,ref=0,
pt=0,assoc cleared); 104@86 REVISE ->130; 101@87,105@88
(sup 4->5); 130@89 (agree sup 3->4). 131@90: restore ->
EVICT #9: no D5 pins (pt all 0); assoc={160,161,170,171}; R=0
unpinned {130 (ins 15),148 (ins 25),144 (ins 29)} -> max ins
-> 144. Install 131 (ins 30; ck sup=3 -> agree sup=4).
140@91: -> EVICT #10: R=0 {130,148,131 (ins 30)} -> victim
131. Install 140 (ins 31, sup 4). 141@92: -> EVICT #11:
victim 140 (ins 31). Install 141 (ins 32, sup 4). 143@93:
-> EVICT #12: victim 141. Install 143 (ins 33, sup 4).
144@94: -> EVICT #13: victim 143. Install 144 (ins 34, sup 4).
nevict=13. Installed: 14 A + {130,148,144} + pins. Absent:
{131,140,141,143}. Probes: q(100) HIT (p3=1; 100->148->152;
reads 148:1), q(160) HIT (r3=1).

Pass 4 (teaches 97..106): 100@97 (sup 1->2), 104@98 (sup 1->2),
101@99,105@100 (sup 5->6), 130@101 (agree sup 4->5). 131@102:
restore -> EVICT #14: R=0 unpinned {130 (ins 15),144 (ins 34);
148 has R=1} -> victim 144. Install 131 (ins 35; ck sup=4 ->
agree sup=5). 140@103: -> EVICT #15: R=0 {130,131 (ins 35)}
-> victim 131. Install 140 (ins 36, sup 5). 141@104: ->
EVICT #16: victim 140. Install 141 (ins 37, sup 5). 143@105:
-> EVICT #17: victim 141. Install 143 (ins 38, sup 5).
144@106: -> EVICT #18: victim 143. Install 144 (ins 39,
sup 5). nevict=18. Probes HIT/HIT (p4=1, r4=1; reads 148:2).

Pass 5 (teaches 109..118): 100@109 (sup 2->3), 104@110
(sup 2->3), 101@111,105@112 (sup 6->7), 130@113 (agree sup
5->6). 131@114: -> EVICT #19: R=0 {130 (ins 15),144 (ins 39)}
-> victim 144. Install 131 (ins 40, sup 6). 140@115: ->
EVICT #20: R=0 {130,131 (ins 40)} -> victim 131. Install 140
(ins 41, sup 6). 141@116: -> #21: victim 140. Install 141
(ins 42, sup 6). 143@117: -> #22: victim 141. Install 143
(ins 43, sup 6). 144@118: -> #23: victim 143. Install 144
(ins 44, sup 6). nevict=23. p5=1, r5=1 (reads 148:3).

Pass 6 (teaches 121..130): 100@121 (sup 3->4), 104@122
(sup 3->4), 101@123,105@124 (sup 7->8), 130@125 (agree sup
6->7). 131@126: -> EVICT #24: R=0 {130 (ins 15),144 (ins 44)}
-> victim 144. Install 131 (ins 45; ck sup=6 -> agree sup=7).
140@127: -> EVICT #25: R=0 {130,131 (ins 45)} -> victim 131.
Install 140 (ins 46, sup 7). 141@128: -> #26: victim 140.
Install 141 (ins 47, sup 7). 143@129: -> #27: victim 141.
Install 143 (ins 48, sup 7). 144@130: -> #28: victim 143.
Install 144 (ins 49, sup 7). nevict=28. p6=1, r6=1 (reads
148:4).

Retest: q(100)=152 HIT; q(104): 104->130 (sup 4) -> stored
obj 131 = ansb HIT (the second hop returns the stored obj;
no 131 entry is required) -> c=2. NC: q(103),q(107) HIT ->
nc=2. U: q(108),q(111),q(114) HIT; q(117): 117->118 (118
installed, sup 2>ref 0) ->119 = ansa HIT -> u=4, forget=0.
bprobe: q(130): 130->131 stored, then cl_find(131,1) -> -1
(131 absent at end) -> MISS; q(140), q(143) absent -> MISS
-> bprobe=0. resprobe: q(160)=162 HIT=1.

Frozen ARM21 summary: ttcA=2, probeA=8, nevict=28, phev=0;
p1..p6 = 0,0,1,1,1,1 (avail100=4);
r1..r6 = 1,1,1,1,1,1 (avail160=4);
c=2, nc=2, u=4, forget=0, bprobe=0, resprobe=1;
apin=4, dec=1, res=1, useless=2 (fprate=50);
evh(160)=evh(161)=evh(170)=evh(171)=evh(148)=evh(118)=0;
EVHIST: 131=5, 140=6, 141=6, 143=6, 144=5 (sum 28).

### 5.2 ARM22 (CAP=22) -- the regression arm

Byte-exact reproduction of the NT-CAPACITY-SWEEP ARM22 frozen
numbers: ttcA=2, probeA=8, nevict=22, phev=0;
p1..p6 = 0,0,1,1,1,1 (avail100=4);
r1..r6 = 1,1,1,1,1,1 (avail160=4);
c=2, nc=2, u=4, forget=0, bprobe=1, resprobe=1;
apin=4, dec=1, res=1, useless=2 (fprate=50);
evh(148)=evh(118)=evh(160)=evh(161)=evh(170)=evh(171)=0;
EVHIST: 140=5, 141=6, 143=6, 144=5 (sum 22).

### 5.3 The mechanistic threshold (frozen reasoning)

Pass-1 eviction demand is 25 - CAP (11 novel keys into CAP-14
free slots). Pass-1 victims, in max-ins order among the R=0
unpinned novels, are 144, 143, 141, 140, 131 (ins 20, 19, 18,
17, 16). Key 131 is the 5th victim, so 131 survives pass 1
iff 25 - CAP <= 4, i.e. CAP >= 21.

If 131 is evicted in pass 1 (CAP <= 20), then at pass 2's first
restore (131@78) every R=0 slot is pinned: D5 pins {130,148}
plus assoc pins {160,161,170,171} cover all six R=0 slots, and
all 14 A-links have R>=3. The D4 min-reads/max-ins scan then
takes the youngest R=3 A-link, 118 (ins 14). 118 is never
restored (teachB never teaches it): u=3, forget=1, phev=1.

If 131 survives pass 1 (CAP >= 21), every pass-2-and-later
eviction finds at least one unpinned R=0 slot (131 itself,
then the rotating novel; 130 is a permanent R=0 unpinned
backstop after pass-3 revision clears the D5 pins), so no
A-link is ever an eviction candidate: phev=0, u=4, forget=0.

Hence the step function: opportunity cost appears iff
CAP <= 20; the arm is clean iff CAP >= 21. The exact integer
threshold where the cost appears is CAP=20, and CAP=21 is
predicted CLEAN. This lane tests that prediction.

## 6. Assembly, build, run (frozen)

- Single source file `nttip_full.zag`: the NT-CAPACITY-SWEEP
  source verbatim EXCEPT `main` runs two arms (R6-CAP21 with
  bars U1-U5, R6-CAP22 with bars R1-R7) instead of three.
  Tag prefix NTSWEEP retained (same binary family).
- Build: `znc nttip_full.zag -o nttip_bin` under safebin-only
  PATH.
- Run `nttip_bin` 3 times; outputs `nttip_run1.txt`,
  `nttip_run2.txt`, `nttip_run3.txt`. Require byte-identical
  (cmp) and record sha256.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic
  output only via the single-buffer cursor helpers + one
  `_zag_raw_syscall` write (never `_zag_print`); no `!(A && B)`
  in while conditions (De Morgan); if-nesting mirrors the
  frozen NT-CAPACITY-SWEEP template shapes (flat, 1-deep); no
  `[]u8 as *u8` casts (thread `_zag_malloc as *u8`).

## 7. Frozen kill bars

Per-arm bars; all exact. (out offsets as NT-CAPACITY-SWEEP:
0 ttcA, 4 probeA, 8 nevict, 12 c, 16 nc, 20 u, 24 forget,
28 phev, 32 bprobe, 36 avail100, 64 evh148, 68 evh118,
72 avail160, 100 evh160, 104 evh161, 108 resprobe, 112 apin,
116 dec, 120 res, 124 useless, 128 evh170, 132 evh171,
136 evh140, 140 evh141, 144 evh143, 148 evh144, 152 evh131.)

ARM21 (R6-CAP21):
- U1 (learnability; else arm VOID): ttcA in 1..50 AND probeA=8.
- U2 (rescue holds): avail160=4 AND resprobe=1 AND evh160=0
  AND evh161=0.
- U3 (FP cost confirmed): dec=1 AND useless=2.
- U4 (tipping signature, CLEAN predicted): phev=0 AND evh118=0
  AND u=4 AND forget=0 AND nc=2 AND c=2.
- U5 (pressure exact): nevict=28 AND evh148=0 AND evh131=5
  AND evh140=6 AND evh141=6 AND evh143=6 AND evh144=5 AND
  bprobe=0.
- Arm verdict: TIP-CLEAN-AT-21 iff U1..U5 all 1;
  TIP-COST-AT-21 iff U1=U2=U3=1 AND phev=1 AND evh118=1 AND
  u=3 AND forget=1; else OFF-TRACE (REPORT names the failing
  bars and the actual numbers).

ARM22 (R6-CAP22; regression of NT-CAPACITY-SWEEP ARM22):
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

## 8. Verdict mapping (frozen)

- U1=0 or R1=0 -> TIP-VOID (apparatus broken; no tipping
  reading).
- ARM22 != REPRODUCED -> TIP-REGRESSION-FAIL (the baseline
  moved; the CAP=21 reading is uninterpretable).
- ARM21 = TIP-CLEAN-AT-21 -> TIPPOINT-LOCATED-AT-20: the
  opportunity cost appears at CAP=20 and at no higher tested
  capacity; the exact integer threshold where the cost appears
  is CAP=20 (cost iff CAP <= 20, clean iff CAP >= 21, on the
  tested 20/21/22 slice).
- ARM21 = TIP-COST-AT-21 -> TIPPOINT-ABOVE-21: the cost
  appears at CAP=21 too; the tipping point lies between 21
  and 22.
- Else -> TIP-OFF-TRACE: report the actual ARM21 numbers; the
  hand-derived trace is falsified as written.

Predicted verdict: TIPPOINT-LOCATED-AT-20.

## 9. Honest boundaries (frozen)

- The lane varies capacity ONLY (CAP=21 plus the CAP=22
  regression). W=20, K=6, M=6, contradiction magnitude, decoy
  design, and exploratory gap (14 ticks) are all fixed. The
  threshold claim is a 3-point slice (20/21/22), not a general
  capacity law; CAP=23 untested.
- The 50% FP rate is world-relative (one decoy chain, never
  used), identical by construction; it does not generalize
  beyond this decoy design.
- No no-D6 control arms are run in this lane.
- The LINKS are memorized associations; no rule induction
  tested; no L2/L3 claim.
- evh131 is checked in-binary via evh_get (out offset 152);
  all other checked quantities use the frozen out offsets.
- This is a non-ledger task (claim minting paused): no ledger
  update whatever the verdict.
