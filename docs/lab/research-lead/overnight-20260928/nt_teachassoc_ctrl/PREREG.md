# PREREG: NT-TEACHASSOC-CTRL -- no-exploratory control arm for the D6 association signal

## 1. Question

NT-TEACHASSOC (ASSOC-CONFIRMED, 2026-10-03) showed that the D6
teaching-stream association pin rescues the residual chain
(avail160 0 -> 4) in a world where the teaching stream carries the
dependence: an exploratory query episode (q(160), q(161), q(170),
q(171), all miss) stamps qstart_obs for the four chain subjects, and
keys taught within W=20 ticks of those stamps get assoc-pinned
through the pass-1 eviction.

The causal attribution question: was the rescue actually due to the
exploratory queries, or would some other factor (the D6 code being
present, the CAP=22 capacity point, the decoy teachings, the
per-pass q(160) probes) have protected the chain anyway?

This lane runs the control: the NT-TEACHASSOC world EXACTLY, minus
the exploratory episode. D6's code stays in the binary. With no
exploratory queries, no install of (160,1), (161,1), (170,1), or
(171,1) can ever see a finite qstart_obs for its subject, so D6 is
provably inert (apin = 0) and the learner reduces behaviorally to
the D5 learner at every eviction decision. The residual chain must
NOT be rescued.

Predicted verdict: CTRL-CONFIRMED (K1-K7 all 1).

## 2. Subject (frozen)

### 2.1 Learner

The NT-TEACHASSOC learner VERBATIM, including the D6 association-pin
rule and all its state (tick, qstart_obs init -1000000, W=20, assoc
pin field 10, ev_scan skippin=1 skipping D5-pinned OR assoc-pinned,
revision clearing assoc). D6 is IN the binary under test -- that is
the point of the control: the inertness claim is about the RULE
never firing, not about the code being absent.

### 2.2 Inertness argument (frozen)

- The only teaches of subjects 160/161/170/171 occur in teachB's
  rare branch (pass 1 only; r == 0 iff pass == 1 with K=6).
- Every harness query before the pass-1 teaches is a phase-1 probe
  of a subject in {100,103,104,107,108,111,114,117} (nthq). None is
  160/161/170/171.
- Therefore at every install of (160,1), (161,1), (170,1),
  (171,1), qstart_obs[subj] = -1000000 (init) and
  t - qstart_obs[subj] >> 20, so the D6 pin condition can never
  fire. No assoc pin is ever granted: apin = 0 provably.
- The per-pass q(160) probes stamp qstart_obs[160] only AFTER the
  pass-1 installs; no reinstall of any chain subject ever occurs
  (161/170/171 are never re-taught; 160 is never evicted). So the
  probes cannot retroactively arm D6.
- With zero assoc pins granted, the eviction scan's skippin=1 pass
  admits exactly the D5-admitted set: the learner is behaviorally
  NT-RESIDUAL's D5 learner at every eviction decision.

### 2.3 Capacity

CAP=22, identical to NT-TEACHASSOC. Key inventory identical: 14
A-links + 6 FREQ novels + 4 assoc-chain keys (160,161,170,171) + 1
RARE (148) = 25 keys, 1.14x pressure.

### 2.4 What is NOT new

No rule changes. The ONLY delta from NT-TEACHASSOC is the removal
of the four exploratory h_query calls in run_arm. Everything else
(learner, oracles, teach order, probes, retest, bprobe, resprobe,
EVHIST, assoc stats) is verbatim.

## 3. Workload (frozen)

NT-TEACHASSOC Section 3 verbatim EXCEPT the exploratory episode is
deleted. In particular:

- Phase 1: trainA + final probeA, NTNL-verbatim (ttcA=2,
  probeA=8). No exploratory queries follow.
- Phase 2: 6 fixed passes of teachB (K=6; rare branch on pass 1
  only: C, NC, FREQ, RESIDUAL (160,1)->161, (161,1)->162, DECOY
  (170,1)->171, (171,1)->172, RARE (148,1)->152, LAST), then
  per-pass probes q(100) vs 152 and q(160) vs 162 via h_query.
- Decoy chain IS taught (identical world); it is never probed for
  usefulness.
- The residual chain IS taught, agree-only, and IS genuinely
  useful: q(160) is probed every pass expecting 162.
- retest, bprobe (q(130)/q(140)/q(143)), resprobe (q(160)==162),
  nevict, EVHIST (100..171), phev, evh(148), evh(118), evh(160),
  evh(161), evh(170), evh(171), apin, dec_present, res_present,
  nassoc_useless: all as NT-TEACHASSOC.

## 4. Frozen predictions (hand-derived by tracing the frozen rules)

Tick model (frozen, NT-TEACHASSOC verbatim): tick starts 0;
h_teach stamps t=tick then tick++; h_query stamps
qstart_obs[s]=tick then tick++.

### 4.1 Phase 1

NT-TEACHASSOC 5.1 verbatim minus the exploratory stamps: pass-1
teaches 0..13, probes 14..21; pass-2 teaches 22..35, probes
36..43; final probeA 44..51; tick=52. ttcA=2, probeA=8. Slots
0..13 hold the 14 A-links (ins 1..14); all 14 have reads=3 (every
A subject is a 1- or 2-hop participant in the 8 probe queries x 3
probe rounds: hops are {100,101},{103,101},{104,105},{107,105},
{108,109},{111,112},{114,115},{117,118}). No installs see a
finite qstart_obs -> zero assoc pins. No -INF check needed
elsewhere: D6 inert.

### 4.2 Pass 1 (15 teachings at ticks 52..66)

100: update (ref 0->1, pt=148). 104: update (ref 0->1, pt=130).
101: agree (sup 2->3). 105: agree (sup 3->4). 130: install
(ins 15, nkeys 15, ap=0). 131: install (16, ap=0). 140: install
(17, ap=0). 141: install (18, ap=0). 143: install (19, ap=0).
144: install (20, ap=0). 160: nkeys=20<22 -> install (ins 21,
ap=0; qstart_obs[160]=-INF). 161: nkeys=21<22 -> install
(ins 22, ap=0; qstart_obs[161]=-INF). 170: nkeys=22=CAP ->
EVICT #1: D5-pinned = {130} (pt[104]=130; pt[100]=148 not
installed); assoc-pinned = {} (D6 inert). Admitted min-reads:
R=0 slots are {131,140,141,143,144,160,161} (all 14 A-links
have reads=3) -> max ins -> 161. Victim=161. Install 170
(ins 23, ap=0). 171: EVICT #2: admitted R=0
{131,140,141,143,144,160,170} -> max ins -> 170. Victim=170.
Install 171 (ins 24, ap=0). 148: EVICT #3: admitted R=0
{131,140,141,143,144,160,171} -> max ins -> 171. Victim=171.
Install 148 (ins 25, ap=0; qstart_obs[148]=-INF).
End of pass 1: nevict=3. Installed: 14 A +
{130,131,140,141,143,144} + {160,148} (22). Absent:
{161,170,171}. apin granted: 0.
Probes: q(100): 100->101->102 =102, MISS (p1=0). q(160):
160->161 (reads(160)=1), 161 absent -> MISS (r1=0).

### 4.3 Pass 2 (teaches: 100,104,101,105,130,131,140,141,143,144)

100: ref 1->2, pt=148. 104: ref 1->2, pt=130. 101: sup 3->4.
105: sup 4->5. 130,131,140,141,143,144: all present -> agree
(sup 1->2). No installs, no evictions (141/143 were never
evicted, unlike NT-TEACHASSOC). nevict=3.
Probes: q(100): sup=2,ref=2 -> -1, MISS (p2=0). q(160): MISS
(r2=0; reads(160)=2).

### 4.4 Pass 3 (same 10 teaches)

100: ref 2->3 > sup=2 -> REVISE ->148 (sup=1,ref=0,pt=0, assoc
cleared [was 0]). 104: ref 2->3 > 2 -> REVISE ->130
(sup=1,ref=0,pt=0). 101: sup 4->5. 105: sup 5->6. 130,131,140,
141,143,144: agree (sup 2->3). nevict=3.
Probes: q(100): 100->148, 148->152 (reads(148)=1) =152, HIT
(p3=1). q(160): MISS (r3=0; reads(160)=3).

### 4.5 Passes 4-6 (same 10 teaches; all agree/update, no installs)

No evictions. Probes: q(100) HIT (p4=p5=p6=1; reads(148)=4 by
end). q(160) MISS (r4=r5=r6=0; reads(160)=6 by end).

### 4.6 Retest / end-of-run

avail100 = p3+p4+p5+p6 = 4. avail160 = 0.
C: q(100)=152 HIT; q(104): 104->130 (sup=4), 130->131 (sup=6)
=131=ANSB HIT. c=2. NC: q(103),q(107) HIT. nc=2. U:
q(108),q(111),q(114),q(117) HIT (118 never evicted). u=4.
forget=0. bprobe: q(130)=132 HIT (130->131->132); q(140)=142
HIT; q(143)=145 HIT. bprobe=3. resprobe: q(160)=162 MISS =0.
dec_present=0 (170,171 absent). res_present=0 (161 absent).
Assoc stats: apin=0, nassoc_useless=0 (no assoc pins exist).
EVHIST: 161=1, 170=1, 171=1 (sum=3=nevict); all other bins 0,
in particular evh(148)=0, evh(118)=0, evh(160)=0, evh(140)=0,
evh(141)=0, evh(143)=0, evh(144)=0. phev=0 (no 100..119
eviction).

Frozen summary: ttcA=2, probeA=8, nevict=3, phev=0;
p1..p6 = 0,0,1,1,1,1 (avail100=4);
r1..r6 = 0,0,0,0,0,0 (avail160=0);
c=2, nc=2, u=4, forget=0, bprobe=3, resprobe=0;
apin=0, dec_present=0, res_present=0, nassoc_useless=0;
evh(160)=0, evh(161)=1, evh(170)=1, evh(171)=1.

Note on the NT-RESIDUAL comparison (frozen): this arm runs
NT-TEACHASSOC's world at CAP=22, not NT-RESIDUAL's CAP=20
world, so nevict (3 vs 12) and the EVHIST bins differ
mechanically (at CAP=22 the youngest-of-R=0 victim on pass 1
is 161, then the incoming 170, then the incoming 171; 160
survives but can never answer because its continuation 161 is
gone and never returns). The frozen reproduction claim is
mechanism-level: the residual is NOT rescued -- avail160=0,
resprobe=0, the (161,1) link is evicted on pass 1 and never
returns -- exactly NT-RESIDUAL's headline finding, with D6
provably inert (apin=0).

## 5. Assembly, build, run (frozen)

- Single source file `ntctrl_full.zag`: NT-TEACHASSOC's
  `ntteach_full.zag` verbatim EXCEPT: (a) the four exploratory
  h_query calls in run_arm are deleted; (b) output tag NTTEACH ->
  NTTCTRL; (c) the fprate print is guarded (apin=0 prints
  fprate=0; no division by zero); (d) kill bars / verdict codes
  rewritten per Section 6. No learner rule touched.
- Build: `znc ntctrl_full.zag -o ntctrl_bin` under safebin-only
  PATH.
- Run `ntctrl_bin` 3 times; outputs `ntctrl_run1.txt`,
  `ntctrl_run2.txt`, `ntctrl_run3.txt`. Require byte-identical
  (cmp) and record sha256.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic output
  only via the single-buffer cursor helpers + one
  `_zag_raw_syscall` write (never `_zag_print`); no `!(A && B)`
  in while conditions (De Morgan); if-nesting mirrors the frozen
  NT-TEACHASSOC template shapes (flat, 1-deep); no `[]u8 as *u8`
  casts (thread `_zag_malloc as *u8`).

## 6. Frozen kill bars

- K1 (learnability; else VOID): ttcA in 1..50 AND probeA = 8.
  Else VOID.
- K2 (retention of uncontested structure): nc = 2 AND u = 4.
- K3 (D6 inertness): apin = 0 exact. (No assoc pin ever
  granted: the D6 rule never fired.)
- K4 (final revision outcome): c = 2 AND forget = 0.
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): nevict = 3 (exact); evh(148) = 0 (D5 pin holds
  on the revision target); phev = 0; EVHIST exact: evh(161)=1,
  evh(170)=1, evh(171)=1, evh(160)=0, evh(140)=0, evh(141)=0,
  evh(143)=0, evh(144)=0.
- K6 (discriminative validity): avail100 = 4 AND nevict > 0.
- K7 (no-rescue confirmation): avail160 = 0 AND resprobe = 0
  AND evh(161) = 1 (the residual chain is not rescued: (161,1)
  evicted on pass 1, never returns, q(160) never answers).

## 7. Verdict mapping (frozen)

Checked in order; first match wins:

- K1 = 0 -> VOID.
- K6 = 0 -> INCONCLUSIVE (apparatus cannot discriminate).
- K4 = 0 -> INFORMATIVE-FAIL (revision/final-outcome off-trace).
- K5 = 0 -> FAIL-PRESSURE (eviction discipline violated).
- K3 = 0 -> CONTAMINATION: D6 granted an assoc pin with no
  exploratory episode. The inertness claim is false; something
  other than query-start adjacency arms the pin. REPORT
  characterizes the actual pins.
- K2 = 0 -> RETENTION-BREAK: uncontested structure lost in the
  control arm.
- K7 = 0 -> RESCUE-ANOMALY: the residual chain was rescued (or
  partially rescued) WITHOUT the exploratory episode,
  contradicting the dependence claim. REPORT characterizes.
- else -> CTRL-CONFIRMED: D6 provably inert (apin=0) and the
  residual not rescued (avail160=0, resprobe=0, evh(161)=1) in
  the no-exploratory arm -- the rescue in NT-TEACHASSOC is
  attributable to the exploratory queries, not to D6's mere
  presence, the capacity point, the decoy teachings, or the
  per-pass probes.

Predicted verdict: CTRL-CONFIRMED (K1-K7 all 1).

## 8. Honest boundaries (frozen)

- This control varies exactly one factor (the exploratory
  episode). It does not test D6's behavior in worlds with
  partial exploratory coverage (e.g. q(160) only), different W,
  or different capacity points.
- apin=0 is the mechanism-level inertness demonstration. The
  per-pass q(160) probes DO stamp qstart_obs[160] (learner-
  observed query starts); the frozen claim is that no install
  ever occurs within W ticks after such a stamp, which the
  binary demonstrates by granting zero pins.
- nevict=3 (not NT-RESIDUAL's 12) and bprobe=3 (not 2) are the
  mechanical consequences of CAP=22 with the decoy teachings;
  they are frozen predictions, not discrepancies.
- The LINKS are memorized associations; no rule induction
  tested; no L2/L3 claim.
- Single capacity point (CAP=22, 1.14x); single contradiction
  magnitude; M=6 fixed; single arm (R6, K=6).
- D1 checkpoints for 161/170/171 exist (evidence preserved) but
  are never consulted: PRESENCE failure, not evidence loss (as
  in NT-RESIDUAL).
- New rule = new lane: D1-D6 and their lanes are untouched;
  this lane's binary is control-only.
- This is a non-ledger task (claim minting paused): no ledger
  update whatever the verdict.
