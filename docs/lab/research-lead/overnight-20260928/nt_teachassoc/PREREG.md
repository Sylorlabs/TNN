# PREREG: NT-TEACHASSOC -- teaching-stream association signal for the residual case

## 1. Question

NT-RESIDUAL (RESIDUAL-CONFIRMED) established that the rare-but-useful
link (160,1)->161, (161,1)->162 -- never a contradiction target, entry-
locally identical to doomed FREQ novels at the pass-1 eviction, query
stream untouched before eviction, in-degree 0 -- is fundamentally
unpredicted by any learner-available signal in THAT workload. Its
recommended follow-up #1: "A teaching-stream association lane: protect
keys taught adjacent (in the teaching stream) to keys the learner has
observed as query starts. This is the only remaining learner-available
signal class this workload's design leaves untested, and it would need
a world where the teaching stream carries the dependence."

This lane builds that world and tests that signal:

(a) Does a same-subject teaching-stream association pin (D6) protect
    the residual chain through the pass-1 eviction, rescuing its
    future usefulness? Predicted: YES (avail160=4, evh(160)=evh(161)=0).
(b) Is the signal learner-available (no oracle, no task labels)?
    By construction: YES (Section 2.3); the REPORT argues it.
(c) What is the false-positive rate? A decoy chain (170,1)->171,
    (171,1)->172 is taught with IDENTICAL stream-adjacency to observed
    query starts but is never queried for usefulness. Predicted: the
    signal protects it anyway -- 2 of 4 assoc-pinned entries never
    contribute to a successful query (FP rate 50%). The signal is a
    question-answer association detector, not a usefulness detector.
(d) Does D5 keep working on the revision target in the same run
    (dissociation: D6 covers the residual, D5 covers 148, neither
    covers FREQ)? Predicted: YES (avail100=4, evh(148)=0).

## 2. Subject (frozen)

### 2.1 Base learner

The NT-RESIDUAL learner verbatim (continuing-learner skeleton,
associative instance memory, sequential lifetime phases, single
main(), no resets, no task labels): D1 preserved (victim
checkpoints), D4 base comparator (min-reads victim, max-ins
tie-break), D5 revision-target pinning via per-slot pendtgt
(unchanged). CAP=22 (see 2.4). Slot fields gain one: assoc pin
(field 10). All NT-RESIDUAL mechanics (cl_find, cl_first_empty,
slot_pinned, ev_scan, cl_evict_d5, cl_update, cl_insert, cl_learn,
cl_predict, q2) are otherwise verbatim.

### 2.2 The new rule under test: D6 (association pin)

Learner state additions (all in the L block, all learner-side):
- `tick`: global event counter, incremented once per teach event
  and once per query event, starting at 0.
- `qstart_obs[s]`: last tick at which subject s was observed as a
  query start (any harness query event: exploratory, per-pass
  probe, retest -- the learner observes every query it processes).
  Initialized to -1000000 (never observed).
- Frozen window W=20.

Rule (frozen): at INSTALL time of key (s,r) (fresh install or D1
restore), at teach tick t, set the entry's assoc pin iff
t - qstart_obs[s] <= W. The pin is sticky for the entry's lifetime
except it is cleared by in-place revision (ref>sup branch of
cl_update). Update path (key already present): pin untouched.

Eviction (frozen): the D5 victim scan's skippin=1 pass now skips
slots that are D5-pinned OR assoc-pinned; the D4 fallback
(skippin=0) is unchanged (admits all).

### 2.3 Learner-availability argument (frozen)

D6 uses only: the teach event stream (subject, tick), the query
event stream the learner itself processes (query starts, ticks),
and learner state derived from them. No oracle: the harness never
tells the learner which keys are useful, which will be queried, or
what the exploratory episode means. No task labels: no phase
markers, no "question"/"answer" tags, no usefulness labels. The
exploratory episode is ordinary query events (all miss); the
learner cannot distinguish them from any other query. Whether
"asked-then-taught" predicts future usefulness is a regularity the
WORLD provides (Section 3), not information the harness injects.

### 2.4 Capacity

CAP=22. Key inventory: 14 A-links + 6 FREQ novels + 4 assoc-chain
keys (160,161,170,171) + 1 RARE (148) = 25 keys. Pressure
25/22 = 1.14x, matched to NT-RESIDUAL's 1.15x. (At CAP=20 the four
assoc pins structurally displace an A-link on pass 2 -- the
signal's opportunity cost -- breaking retention; that sensitivity
is recorded in Section 9, not frozen here.)

### 2.5 What is NOT new

D1/D2/D3/D4/D5 rules and their lanes are untouched. D6 is additive:
it only ever ADDS pin eligibility; with qstart_obs all -INF it is
inert and the learner reduces exactly to NT-RESIDUAL's D5 learner.

## 3. Workload (frozen numeric inventory; opaque identifiers)

NT-RESIDUAL Section 3 verbatim, PLUS:

- EXPLORATORY EPISODE (the teaching-stream dependence): immediately
  after phase 1 (after trainA + the final probeA), the harness
  issues four query events: q(160), q(161), q(170), q(171), in that
  order. All miss (nothing taught yet). They are read-only w.r.t.
  knowledge, increment no reads, but ARE observed query starts:
  qstart_obs[160], qstart_obs[161], qstart_obs[170],
  qstart_obs[171] are stamped. This is the world's dependence:
  questions about new subjects precede teachings about them.
- DECOY chain: (170,1)->171 and (171,1)->172, agree-only, taught on
  K-passes only (pass 1 at K=6), in the LAST teach block right after
  the residual pair: order ..., 160, 161, 170, 171, 148. NEVER
  contradicted. NEVER probed for usefulness (no q(170) probe exists
  anywhere in the protocol). Stream-adjacency to observed query
  starts is IDENTICAL to the residual pair (gap 14 ticks, Section 5);
  future usefulness differs (oracle): q(160) is probed every pass,
  q(170) never.
- RESIDUAL chain: (160,1)->161, (161,1)->162 as NT-RESIDUAL
  (agree-only, K-passes, LAST position before 148), now followed by
  the decoy pair.
- Phase-2 per-pass probes: q(100) vs 152 AND q(160) vs 162 (as
  NT-RESIDUAL). No q(170) probe.

Teach order on K-passes (LAST): C (100->148, 104->130), NC
(101->102, 105->106), FREQ (130->131, 131->132, 140->141,
141->142, 143->144, 144->145), RESIDUAL (160->161, 161->162),
DECOY (170->171, 171->172), RARE (148->152). 15 teachings.

ANSB, ansa, isC, isNC, retest partitions, bprobe, resprobe: as
NT-RESIDUAL. Retest white-box additions: dec_present =
((170,1) and (171,1) both installed at end); res_present =
((160,1) and (161,1) both installed at end); apin = number of
valid slots with assoc pin at end; nassoc_useless = assoc-pinned
valid slots with reads==0 at end (learner-available: reads>0 iff
the entry ever contributed to a successful predict).

## 4. Protocol (frozen)

- `trainA`: NT-RESIDUAL verbatim (14 A links ascending; probe 8
  queries per pass; criterion 8/8 twice; max 50). Predicted:
  ttcA=2, probeA=8. All teach/query events go through the
  tick-stamping wrappers h_teach/h_query (Section 2.2); semantics
  otherwise unchanged.
- Exploratory: h_query(160), h_query(161), h_query(170),
  h_query(171).
- Phase 2: 6 FIXED passes. Per pass: teachB (Section 3 order);
  then probe q(100) vs 152 (flag p_p) and q(160) vs 162 (flag
  r_p), both via h_query (observed). avail100 = passes 3..6 with
  q(100)==152; avail160 = passes 3..6 with q(160)==162.
- After pass 6: retest (c/nc/u/forget), bprobe, resprobe
  (q(160)==162); record nevict, per-subj eviction histogram
  (100..165), phev, evh(148), evh(118), evh(160), evh(161),
  evh(170), evh(171), apin, dec_present, res_present,
  nassoc_useless.

## 5. Frozen predictions (hand-derived by tracing the frozen rules)

Tick model (frozen): tick starts 0; h_teach stamps t=tick then
tick++; h_query stamps qstart_obs[s]=tick then tick++.

### 5.1 Phase 1 + exploratory

Phase 1 is NTNL-verbatim: after ttcA=2 passes + final probeA,
slots 0..13 hold the 14 A links (sup=2,ref=0,reinf=2,ins 1..14),
nkeys=14. Ticks: pass-1 teaches 0..13, probes 14..21; pass-2
teaches 22..35, probes 36..43; final probeA 44..51; tick=52.
No installs see a finite qstart_obs (all -INF during phase-1
installs) -> zero assoc pins in phase 1.
Exploratory at ticks 52,53,54,55: qstart_obs[160]=52,
qstart_obs[161]=53, qstart_obs[170]=54, qstart_obs[171]=55;
tick=56. All four miss; no reads change.

### 5.2 Pass 1 (K-pass; 15 teachings at ticks 56..70)

100@56: update (ref 0->1, pt=148). 104@57: update (ref 0->1,
pt=130). 101@58, 105@59: agree (sup 2->3). 130@60: install
(ins 15, ap=0; qstart_obs[130]=-INF). 131@61 (ins 16), 140@62
(17), 141@63 (18), 143@64 (19), 144@65 (20): installs, ap=0.
160@66: nkeys=20<22 -> install (ins 21); gap 66-52=14 <= 20 ->
ap=1. 161@67: install (ins 22); gap 67-53=14 -> ap=1.
170@68: nkeys=22 -> EVICT #1: pinned = {130: D5 via pt[104]}
+ {160,161: assoc}; admitted min-reads: R=0 unpinned
{131,140,141,143,144} -> max ins -> 144. Install 170 (ins 23);
gap 68-54=14 -> ap=1. 171@69: EVICT #2: pinned {130,160,161,
170}; R=0 unpinned {131,140,141,143} -> 143. Install 171
(ins 24); gap 69-55=14 -> ap=1. 148@70: EVICT #3: pinned
{130,160,161,170,171}; R=0 unpinned {131,140,141} -> 141.
Install 148 (ins 25); qstart_obs[148]=-INF -> ap=0.
End of pass 1: nevict=3. Installed: 14 A + {130,131,140} +
{160,161,170,171,148} (22). Absent: {141,143,144}.
Probes: q(100)@71: 100->101 (R100++), 101->102 (R101++) =102,
MISS (p1=0). q(160)@72: 160->161 (R160=1), 161->162 (R161=1)
=162, HIT (r1=1).

### 5.3 Pass 2 (teaches at 73..82; no K-teachings)

100: ref 1->2, pt=148. 104: ref 1->2, pt=130. 101,105: sup 3->4.
130: agree (sup 1->2). 131: agree (sup 1->2). 140: agree (sup
1->2). 141: absent -> D1 restore -> EVICT #4: pinned = {130,
148: D5} + {160,161,170,171: assoc}; admitted R=0: {131,140}
(unpinned) -> max ins -> 140. Install 141 (ap=0). 143: restore
-> EVICT #5: R=0 unpinned {131,141} -> 141. Install 143.
144: restore -> EVICT #6: R=0 unpinned {131,143} -> 143.
Install 144.
End of pass 2: nevict=6. Installed: 14 A + {130,131} +
{160,161,170,171,148} + {144}. Absent: {140,141,143}.
Probes: q(100)@83: predict(100,1): sup=2,ref=2 -> -1, MISS
(p2=0). q(160)@84: HIT (R160=2,R161=2; r2=1).

### 5.4 Pass 3 (teaches 85..94)

100: ref 2->3 > sup=2 -> REVISE ->148 (sup=1,ref=0,pt=0,
assoc cleared [was 0]). 104: ref 2->3 > 2 -> REVISE ->130
(sup=1,ref=0,pt=0). 101,105: sup 4->5. 130: agree (sup 2->3).
131: agree (sup 2->3). 140: absent -> restore -> EVICT #7:
pinned = {160,161,170,171: assoc} (D5: pt all 0); admitted R=0
{130,131,148,144} -> max ins -> 144. Install 140. 141: restore
-> EVICT #8: R=0 {130,131,148,140} -> 140. Install 141. 143:
restore -> EVICT #9: R=0 {130,131,148,141} -> 141. Install 143.
144: present -> agree.
End of pass 3: nevict=9. Installed: 14 A + {130,131} +
{160,161,170,171,148} + {143}. Absent: {140,141,144}.
Probes: q(100)@95: 100->148 (R100++), 148->152 (R148=1) =152,
HIT (p3=1). q(160)@96: HIT (r3=1; R160=3,R161=3).

### 5.5 Pass 4 (teaches 97..106)

100,104,101,105: hits/agrees. 130: agree (sup 3->4). 131: agree
(sup 3->4). 140: restore -> EVICT #10: pinned {160,161,170,171};
admitted R=0 {130,131,143} (148: R=1) -> max ins -> 143.
Install 140. 141: restore -> EVICT #11: R=0 {130,131,140} ->
140. Install 141. 143: present -> agree. 144: restore -> EVICT
#12: R=0 {130,131,141} -> 141. Install 144.
End of pass 4: nevict=12. Installed: 14 A + {130,131} +
{160,161,170,171,148} + {144}. Absent: {140,141,143}.
Probes: q(100) HIT (p4=1; R148=2). q(160) HIT (r4=1).

### 5.6 Pass 5 (teaches 109..118)

140: restore -> EVICT #13: R=0 {130,131,144} -> 144. Install
140. 141: restore -> EVICT #14: R=0 {130,131,140} -> 140.
Install 141. 143: restore -> EVICT #15: R=0 {130,131,141} ->
141. Install 143. 144: present -> agree.
End of pass 5: nevict=15. Installed: 14 A + {130,131} +
{160,161,170,171,148} + {143}. Absent: {140,141,144}.
Probes: q(100) HIT (p5=1). q(160) HIT (r5=1).

### 5.7 Pass 6 (teaches 121..130)

140: restore -> EVICT #16: R=0 {130,131,143} -> 143. Install
140. 141: restore -> EVICT #17: R=0 {130,131,140} -> 140.
Install 141. 143: present -> agree. 144: restore -> EVICT #18:
R=0 {130,131,141} -> 141. Install 144.
End of pass 6: nevict=18. Installed: 14 A + {130,131} +
{160,161,170,171,148} + {144}. Absent: {140,141,143}.
Probes: q(100) HIT (p6=1). q(160) HIT (r6=1).

### 5.8 Retest

C: q(100)=152 HIT; q(104): 104->130 (sup=4), 130->131 (sup=6)
=131=ANSB HIT. c=2. NC: q(103),q(107) HIT. nc=2. U:
q(108),q(111),q(114),q(117) HIT (118 never evicted). u=4.
forget=0. bprobe: q(130)=132 HIT (130->131->132); q(140):
absent MISS; q(143): absent MISS. bprobe=1. resprobe:
q(160)=162 HIT =1.
Assoc stats at end: apin=4 (160,161,170,171); reads: 160:7,
161:7 (6 pass probes + resprobe), 170:0, 171:0 ->
nassoc_useless=2; dec_present=1; res_present=1.
EVHIST: 140=5 (p2,p3,p4,p5,p6), 141=6 (p1..p6), 143=4
(p1,p2,p4,p6), 144=3 (p1,p3,p5); sum=18. evh(148)=0,
evh(118)=0, evh(160)=0, evh(161)=0, evh(170)=0, evh(171)=0.
phev=0.

Frozen summary: ttcA=2, probeA=8, nevict=18, phev=0;
p1..p6 = 0,0,1,1,1,1 (avail100=4);
r1..r6 = 1,1,1,1,1,1 (avail160=4);
c=2, nc=2, u=4, forget=0, bprobe=1, resprobe=1;
apin=4, dec_present=1, res_present=1, nassoc_useless=2.

## 6. Assembly, build, run (frozen)

- Single source file `ntteach_full.zag`: the NT-RESIDUAL learner
  verbatim (D1+D4+D5) PLUS D6 (Section 2.2): 20-byte header
  (tick at 16), 44-byte slots (assoc at field 10), qstart_obs
  region (66x4, init -1000000); h_teach/h_query wrappers on ALL
  teach/query call sites; ev_scan skips D5-pinned OR assoc-pinned;
  revision clears assoc. Oracles: NT-RESIDUAL verbatim PLUS
  exploratory episode (post-phase-1), decoy teaches (170,1)->171,
  (171,1)->172 on K-passes after the residual pair; CAP=22.
  Tag NTTEACH. Single arm R6 (K=6).
- Build: `znc ntteach_full.zag -o ntteach_bin` under safebin-only
  PATH.
- Run `ntteach_bin` 3 times; outputs `ntteach_run1.txt`,
  `ntteach_run2.txt`, `ntteach_run3.txt`. Require byte-identical
  (cmp) and record sha256.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic output
  only via the single-buffer cursor helpers + one
  `_zag_raw_syscall` write (never `_zag_print`); no `!(A && B)`
  in while conditions (De Morgan); if-nesting mirrors the frozen
  NT-RESIDUAL template shapes (flat, 1-deep); no `[]u8 as *u8`
  casts (thread `_zag_malloc as *u8`).

## 7. Frozen kill bars

- K1 (learnability; else VOID): ttcA in 1..50 AND probeA = 8.
  Else VOID.
- K2 (retention of uncontested structure): nc = 2 AND u = 4.
- K3 (the D6 rescue bar): avail160 = 4 AND resprobe = 1 AND
  evh(160) = 0 AND evh(161) = 0 (exact; Section 5.8).
- K4 (final revision outcome): c = 2 AND forget = 0.
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): nevict = 18 (exact); evh(148) = 0 (D5 pin holds);
  phev = 0; EVHIST exact: evh(140)=5, evh(141)=6, evh(143)=4,
  evh(144)=3.
- K6 (discriminative validity): avail100 = 4 (the D5-covered probe
  still passes; not a broken probe) AND nevict > 0 (pressure
  actually exercised).
- K7 (false-positive control confirmation): dec_present = 1 AND
  nassoc_useless = 2 (the decoy chain was assoc-pinned and
  survived to end-of-run despite never contributing to a
  successful query -- the signal's FP cost materialized as
  designed).

## 8. Verdict mapping (frozen)

Checked in order; first match wins:

- K1 = 0 -> VOID.
- K6 = 0 -> INCONCLUSIVE (apparatus cannot discriminate).
- K4 = 0 -> INFORMATIVE-FAIL (revision/final-outcome off-trace).
- K5 = 0 -> FAIL-PRESSURE (eviction discipline violated).
- K3 = 0 -> NO-RESCUE: D6 did not protect the residual link
  (it was evicted or never answered); the teaching-stream
  association signal fails even where the stream carries the
  dependence. REPORT characterizes the actual curve.
- K2 = 0 -> FIX-WITH-COST: the assoc pins bought the residual at
  the price of uncontested-structure retention.
- K7 = 0 -> FP-UNCONFIRMED: the decoy control did not materialize
  as designed (decoy not protected, or useless-count off);
  the FP measurement is uninterpretable. REPORT characterizes.
- else -> ASSOC-CONFIRMED: D6's teaching-stream association pin
  protects the residual chain through eviction pressure
  (avail160=4, zero evictions of 160/161) while D5 still covers
  the revision target in the same run -- and the signal's
  false-positive cost is measured, not hidden: 2 of 4
  assoc-pinned entries (the decoy chain) never contribute to a
  successful query (FP rate 50%).

Predicted verdict: ASSOC-CONFIRMED (K1-K7 all 1).

## 9. Honest boundaries (frozen)

- The LINKS are memorized associations; what is rule-STRUCTURED
  is the family. No rule induction tested; no L2/L3 claim.
- Single capacity point (CAP=22, 1.14x); single contradiction
  magnitude; M=6 fixed; single arm (R6, K=6).
- The 50% FP rate is world-relative: it measures THIS world's
  decoy design (one asked-then-taught chain that is never used).
  It does not establish a general FP rate for the signal class.
  The honest claim is directional: the signal cannot distinguish
  "asked then taught, later used" from "asked then taught, never
  used" -- future usefulness is not in the observable stream.
- Capacity sensitivity (exploratory, not frozen): at CAP=20
  (1.25x) the four assoc pins structurally displace an A-link on
  pass 2 (all R=0 slots pinned), breaking K2. The signal has
  opportunity cost; pinning useless entries (the decoy) is not
  free. A capacity sweep is recommended follow-up, not run here.
- Same-subject adjacency is the frozen operationalization of
  "taught adjacent to observed query starts". Chain continuation
  beyond the queried subject is NOT covered by D6 as frozen
  (this world supplies qstart_obs for both chain subjects via the
  exploratory episode; a world that only ever queries q(160)
  would leave (161,1) unprotected -- see follow-up).
- No-exploratory control arm not run: with qstart_obs all -INF,
  D6 is provably inert (the rule's condition can never fire) and
  the learner reduces to NT-RESIDUAL's D5 learner; recommended
  as a cheap follow-up, not frozen here.
- D1 checkpoints for 160/161/170/171 exist if evicted (never are).
- New rule = new lane: D1/D2/D3/D4/D5 and their lanes are
  untouched by this work; D6 lives only in this lane's binary.
- This is a non-ledger task (claim minting paused): no ledger
  update whatever the verdict.
