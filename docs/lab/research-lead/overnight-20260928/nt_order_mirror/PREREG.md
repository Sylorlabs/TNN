# PREREG: NT-ORDER-MIRROR -- order-dependence mirror of NT-LOWVALUE-BOUNDARY: RARE link taught FIRST

## 1. Question

NT-LOWVALUE-BOUNDARY established LIABILITY-CONFIRMED: D2
(evict-youngest, max-ins victim) is a liability for
genuinely-useful-but-infrequently-reinforced links under capacity
pressure, with availability ~= 1/K over passes 3-6 (4/2/1/0 for
K=1,2,3,6). The attributed mechanism (white-box, from the eviction
histogram): the RARE link (148,1)->152 was taught LAST in ascending
order, so each D1-restore re-installed it YOUNG (fresh max ins);
the FREQ background churn then evicted the youngest first, which
was the just-restored RARE link. Tenure protection never engaged
because re-installation kept resetting its age: the churn trap.

This lane is the order-dependence mirror, recommended (not
preregistered) in the NTLV REPORT: teach the RARE link FIRST
instead of last among phase-2 teachings. Question: does the
mechanism explanation survive the mirror? Specifically:

(a) Do the frozen D1+D2 rules predict tenure-protection for the
    first-taught RARE link (avail = 4/4 for all K)?
(b) If confirmed: installation recency (not reinforcement
    frequency) is the true determinant of D2 victimhood, and the
    churn-trap account is causally correct.
(c) If NOT confirmed: the mechanism is more complex than the
    churn-trap account, and the NTLV attribution must be revised.

The prediction is derived from the frozen rules, not a new
hypothesis: a first-installed novel link receives the LOWEST novel
ins of the pass; every later novel installation (fresh or D1
restore) stamps a higher ins; D2's victim is the MAXIMUM ins, so
the first-taught RARE link can never be the youngest entry while
any later-installed novel is present. Its age is never reset by
re-installation on non-teach passes (it is simply not re-taught),
and on re-teach passes it is re-installed first, before the churn
re-youths the others. Tenure protection should engage from the
first installation.

## 2. Subject (frozen)

The NT-LOWVALUE-BOUNDARY subject verbatim: the continuing-learner
skeleton (associative instance memory, sequential lifetime phases,
single main(), no resets, no task labels) with ONLY the D1+D2 memory
rules installed. Slot fields (32 bytes): 0 subj, 4 rel, 8 obj,
12 dom, 16 valid, 20 sup, 24 ref, 28 ins. Key = (subj, rel).
rel = 1 throughout. `dom` = install-phase provenance, entry
metadata, never consulted by learner decisions. Arena holds
nentries, nevict, ins_seq, nslots.

- Evidence update (NT-frozen rule): on a teaching event for a PRESENT
  entry, taught obj matches stored obj -> sup++; taught obj differs ->
  ref++, and if ref > sup -> REVISE to (new obj, sup=1, ref=0), in
  place. Revision does NOT touch `ins`.
- D1 (preserve-evidence): on eviction, checkpoint (valid=1, obj, sup,
  ref) keyed by subj. On insertion of an absent key with a valid
  checkpoint, install the checkpointed (obj, sup, ref), stamp dom =
  current phase, then run the frozen update step with the taught obj.
  On insertion with no valid checkpoint, install fresh (taught obj,
  sup=1, ref=0).
- D2 (evict-youngest): arena holds `ins_seq`, zero-initialized. On
  EVERY installation (fresh and D1-restore alike): ins_seq++,
  slot.ins = ins_seq. Eviction victim = occupied slot with MAXIMUM
  `ins`. `ins` unique per installation; no tie-break. Revision in
  place does not touch `ins`; eviction does not touch survivors.
- Predict: entry present and sup > ref -> stored obj; else -1.
- 2-hop query q(s): p1 = predict(s,1); if p1 < 0 -> -1;
  p2 = predict(p1,1); if p2 < 0 -> -1; else p2. The chaining procedure
  is fixed machinery; the KNOWLEDGE (links) is learned. No semantic
  labels anywhere; nodes/links are bare integers.
- Capacity CAP = 20 slots. The comparator is generic: installation
  order only, no task identity, no importance flags, no protection
  rules, no modes.

The learner is UNTOUCHED vs NT-LOWVALUE-BOUNDARY (verbatim port of
the NT-PORT-PRESSURE D1+D2 code). The ONLY change in the entire lane
is the phase-2 teach order (Section 4).

## 3. Workload (frozen numeric inventory; opaque identifiers)

NT-LOWVALUE-BOUNDARY verbatim. Family A: 14 links, 8 chains with
shared substructure: 100->101, 101->102, 103->101, 104->105,
105->106, 107->105, 108->109, 109->110, 111->112, 112->113,
114->115, 115->116, 117->118, 118->119. Query starts QS =
{100,103,104,107,108,111,114,117}. ANSA =
{102,102,106,106,110,113,116,119}.

Phase-2 teachings per pass (THE MIRROR CHANGE): the RARE link is
taught FIRST, then the rest in ascending subj order:
- RARE (genuinely useful, infrequently reinforced), on pass p iff
  (p-1) mod K == 0, taught FIRST: (148,1)->152.
- Then ascending: C (contradicted), every pass: (100,1)->148,
  (104,1)->130; NC (agreed), every pass: (101,1)->102, (105,1)->106;
  FREQ (frequently-reinforced novel), every pass: (130,1)->131,
  (131,1)->132, (140,1)->141, (141,1)->142, (143,1)->144,
  (144,1)->145. Novel 2-hop chains: q(130) = 132, q(140) = 142,
  q(143) = 145.

The RARE link is GENUINELY USEFUL exactly as in NTLV: after
revision, q(100) = 100 -> 148 -> 152, so the scored c-query q(100)
requires link (148,1)->152 to be present. It is NOT re-taught every
pass (period K; K = 6 means taught once, on pass 1 only).

ANSB (correct 2-hop answers under family B): q(100) -> 152,
q(104) -> 131, all others ANSA.

Retest partitions of the 8 A queries (NTLV verbatim logic):
- C: starts 100, 104. Correct: ANSB (152, 131; revised).
- NC: starts 103, 107. Correct: ANSA = ANSB (102, 106; retained).
- U: starts 108, 111, 114, 117. Correct: ANSA (110, 113, 116, 119).
- FORGET = C queries answering neither ANSA nor ANSB, plus NC/U
  queries answering not-ANSA (absent link -> -1 counts as forgotten).

Capacity accounting (unchanged): 14 A links + 7 novel subjs
(130,131,140,141,143,144,148) = 21 distinct (subj,rel) keys > CAP 20.
Pressure ratio 21/20 = 1.05x. Exactly 1 key must be absent at any
time. A-links hold ins 1..14 forever (revision is in place;
re-teaching a present link never touches ins), so every novel
installation (ins >= 15) is younger than every A-link: D2 can never
select a phase-1 link while any novel link is present, hence
phev = 0 structurally.

Arms (each on a FRESH learner; the period selector is a harness
condition, not a cognitive mode): P1 (K=1), P2 (K=2), P3 (K=3),
P6 (K=6). M = 6 phase-2 passes, fixed, all arms.

## 4. Protocol (frozen)

- `trainA`: repeat passes over the 14 A links (ascending subj); after
  each pass probe the 8 queries. Criterion = 8/8 correct for 2
  consecutive passes. Max 50 passes (fail-safe; hitting it = arm
  FAIL). Returns passes used. Predicted: ttcA = 2, probeA = 8, all arms.
- Phase 2: 6 FIXED passes. Per pass: teach 148 FIRST iff
  (pass-1) mod K == 0, then teach 100, 101, 104, 105, 130, 131,
  140, 141, 143, 144 in ascending subj order. After EACH pass, probe
  q(100) vs 152 (the RARE-usefulness probe; read-only, no state
  change). avail(K) = number of passes p in {3,4,5,6} with
  q(100) == 152 (passes 1-2 are pre-revision; q(100) cannot be 152
  there).
- After pass 6: NTLV-style retest (c/nc/u/forget); bprobe =
  (q(130)==132) + (q(140)==142) + (q(143)==145), /3; record nevict,
  per-subj eviction histogram (bins 100..150), phev (evictions of
  subjs 100..119), evh(148) (white-box: is the RARE link ever the
  D2 victim?).

## 5. Frozen predictions (hand-derived by tracing the frozen rules)

Notation: A-links occupy slots 0..13, ins 1..14, all (obj, sup=2,
ref=0) after phase 1. Novel slots 14..19. The mirror trace differs
from NTLV only in that 148 is installed first among novels each
re-teach pass, so the revolving churn pair becomes 143/144 and 148
keeps the lowest novel ins of the pass.

### 5.1 Arm P1 (K=1; RARE every pass, taught first)

Pass 1: 148 absent -> fresh install slot 14, ins 15, (152,1,0).
100 -> ref=1; 104 -> ref=1; 101,105 -> sup=3. Novel:
130(16),131(17),140(18),141(19),143(20) fill slots 15..19;
144 -> arena full -> evict max-ins = 143(20) -> install 144
(ins 21), fresh (145,1,0); checkpoint 143 = (144,1,0). nevict = 1.
Present novel: 130,131,140,141,144,148. Absent: 143.

Pass 2: 148 present -> sup=2. 100 -> ref=2; 104 -> ref=2;
101,105 -> sup=4; FREQ present -> sup=2. 143 absent -> D1 restore
(144,1,0) -> sup=2; evict max-ins: 144(21) -> install 143 (ins 22);
checkpoint 144 = (145,1,0). 144 absent -> restore (145,1,0) ->
sup=2; evict max-ins: 143(22) -> install 144 (ins 23); checkpoint
143 = (144,2,0). nevict = 3.
Present: 130,131,140,141,144,148. Absent: 143.

Pass 3: 148 -> sup=3. 100 -> ref=3 > sup=2 -> REVISE in place ->
(100,1)->148, (sup=1,ref=0), ins untouched (1). 104 -> ref=3 > 2 ->
REVISE -> (104,1)->130, ins untouched (4). 101,105 -> sup=5;
FREQ -> sup=3. 143 absent -> restore (144,2,0) -> sup=3; evict
144(23) -> 143(24); checkpoint 144 = (145,2,0). 144 absent ->
restore (145,2,0) -> sup=3; evict 143(24) -> 144(25); checkpoint
143 = (144,3,0). nevict = 5.
Present: 130,131,140,141,144,148. Probe q(100): 100->148 (sup=1)
-> 152 (sup=3) = 152. OK.

Pass 4: 148 -> sup=4. 100 -> sup=2; 104 -> sup=2; 101,105 -> sup=6;
FREQ -> sup=4. 143 -> restore -> sup=4; evict 144(25) -> 143(26).
144 -> restore -> sup=4; evict 143(26) -> 144(27). nevict = 7.
Probe q(100) = 152. OK.

Pass 5: 148 -> sup=5. 100 -> sup=3; 104 -> sup=3; FREQ -> sup=5.
143 -> restore -> sup=5; evict 144(27) -> 143(28). 144 -> restore
-> sup=5; evict 143(28) -> 144(29). nevict = 9. Probe OK.

Pass 6: 148 -> sup=6. 100 -> sup=4; 104 -> sup=4; FREQ -> sup=6.
143 -> restore -> sup=6; evict 144(29) -> 143(30). 144 -> restore
-> sup=6; evict 143(30) -> 144(31). nevict = 11. Probe OK.

Frozen P1: ttcA = 2, probeA = 8, nevict = 11, phev = 0.
EVHIST nonzero: 143 = 6 (pass 1 once + passes 2-6 once each as the
victim of 144's restore), 144 = 5 (passes 2-6 once each as the
victim of 143's restore). evh(148) = 0: the RARE link is NEVER the
D2 victim. Sum = 11.
Per-pass q(100)==152: p1 0, p2 0, p3 1, p4 1, p5 1, p6 1 -> avail = 4.
Retest: c = 2/2 (q(100) = 152 via present 148; q(104) = 131 via
104->130->131); nc = 2/2; u = 4/4; forget = 0. bprobe = 2/3
(q(130) OK, q(140) OK, q(143): 143 absent at end -> -1).

### 5.2 Arm P2 (K=2; RARE on passes 1,3,5, taught first)

Pass 1: identical to P1 pass 1. nevict = 1. Present:
148(15),130(16),131(17),140(18),141(19),144(21). Absent: 143.
(100: ref=1; 104: ref=1.)

Pass 2 (no 148): 100 -> ref=2; 104 -> ref=2; 101,105 -> sup=4;
FREQ -> sup=2. 143 absent -> restore (144,1,0) -> sup=2; evict
144(21) -> 143(22); checkpoint 144 = (145,1,0). 144 absent ->
restore (145,1,0) -> sup=2; evict 143(22) -> 144(23); checkpoint
143 = (144,2,0). nevict = 3.
Present: 148(15),130,131,140,141,144(23). Absent: 143.

Pass 3 (148 taught): 148 present -> sup=2. 100 -> ref=3 > 2 ->
REVISE -> ->148 (sup=1,ref=0). 104 -> ref=3 > 2 -> REVISE -> ->130.
101,105 -> sup=5; FREQ -> sup=3. 143 absent -> restore (144,2,0)
-> sup=3; evict 144(23) -> 143(24); checkpoint 144 = (145,2,0).
144 absent -> restore (145,2,0) -> sup=3; evict 143(24) -> 144(25);
checkpoint 143 = (144,3,0). nevict = 5.
Present: 148,130,131,140,141,144. Probe q(100): 100->148 (sup=1)
-> 152 (sup=2) = 152. OK.

Pass 4 (no 148): 148 untouched (sup=2). 100 -> sup=2; 104 -> sup=2;
101,105 -> sup=6; FREQ -> sup=4. 143 absent -> restore (144,3,0)
-> sup=4; evict 144(25) -> 143(26); checkpoint 144 = (145,3,0).
144 absent -> restore (145,3,0) -> sup=4; evict 143(26) -> 144(27);
checkpoint 143 = (144,4,0). nevict = 7.
Present: 148,130,131,140,141,144. Absent: 143.
Probe q(100): 100->148 (sup=2), 148->152 (sup=2) = 152. OK.
(THE MIRROR DIFFERENCE: in NTLV, 148 was evicted on non-teach
passes and the probe missed; here 148 is never evicted, so the
probe hits.)

Pass 5 (148 taught): 148 -> sup=3. 100 -> sup=3; 104 -> sup=3;
101,105 -> sup=7; FREQ -> sup=5. 143 absent -> restore (144,4,0)
-> sup=5; evict 144(27) -> 143(28); checkpoint 144 = (145,4,0).
144 absent -> restore (145,4,0) -> sup=5; evict 143(28) -> 144(29);
checkpoint 143 = (144,5,0). nevict = 9.
Present: 148,130,131,140,141,144. Probe OK.

Pass 6 (no 148): 100 -> sup=4; 104 -> sup=4; FREQ -> sup=6.
143 absent -> restore (144,5,0) -> sup=6; evict 144(29) -> 143(30);
checkpoint 144 = (145,5,0). 144 absent -> restore (145,5,0) ->
sup=6; evict 143(30) -> 144(31); checkpoint 143 = (144,6,0).
nevict = 11. Present: 148,130,131,140,141,144. Absent: 143.
Probe q(100): 100->148 (sup=4), 148->152 (sup=3) = 152. OK.

Frozen P2: ttcA = 2, probeA = 8, nevict = 11, phev = 0.
EVHIST: 143 = 6, 144 = 5, evh(148) = 0. Sum = 11.
Per-pass q(100)==152: 0,0,1,1,1,1 -> avail = 4.
Retest: c = 2/2 (q(100) = 152, q(104) = 131); nc = 2/2; u = 4/4;
forget = 0. bprobe = 2/3 (143 absent at end).

### 5.3 Arm P3 (K=3; RARE on passes 1,4, taught first)

Pass 1: as P1. nevict = 1. Present: 148(15),130,131,140,141,144(21).
Absent: 143. (100: ref=1; 104: ref=1.)
Pass 2 (no 148): 100 -> ref=2; 104 -> ref=2. 143 -> restore ->
sup=2; evict 144(21) -> 143(22). 144 -> restore -> sup=2; evict
143(22) -> 144(23). nevict = 3.
Present: 148(15),130,131,140,141,144(23). Absent: 143.
Pass 3 (no 148): 100 -> ref=3 > 2 -> REVISE -> ->148 (sup=1).
104 -> REVISE -> ->130. 101,105 -> sup=5; FREQ -> sup=3.
143 -> restore -> sup=3; evict 144(23) -> 143(24). 144 -> restore
-> sup=3; evict 143(24) -> 144(25). nevict = 5.
Probe q(100): 100->148 (sup=1), 148->152 (sup=1, taught only on
pass 1 so far; 1 > ref=0) = 152. OK.
Pass 4 (148 taught): 148 -> sup=2. 100 -> sup=2; 104 -> sup=2;
101,105 -> sup=6; FREQ -> sup=4. 143 -> restore -> sup=4; evict
144(25) -> 143(26). 144 -> restore -> sup=4; evict 143(26) ->
144(27). nevict = 7. Probe OK.
Pass 5 (no 148): 100 -> sup=3; 104 -> sup=3; FREQ -> sup=5.
143 -> restore -> sup=5; evict 144(27) -> 143(28). 144 -> restore
-> sup=5; evict 143(28) -> 144(29). nevict = 9.
Probe: 100->148 (sup=3), 148->152 (sup=2) = 152. OK.
Pass 6 (no 148): 100 -> sup=4; 104 -> sup=4; FREQ -> sup=6.
143 -> restore -> sup=6; evict 144(29) -> 143(30). 144 -> restore
-> sup=6; evict 143(30) -> 144(31). nevict = 11. Probe OK.

Frozen P3: ttcA = 2, probeA = 8, nevict = 11, phev = 0.
EVHIST: 143 = 6, 144 = 5, evh(148) = 0. Sum = 11.
Per-pass q(100)==152: 0,0,1,1,1,1 -> avail = 4.
Retest: c = 2/2; nc = 2/2; u = 4/4; forget = 0. bprobe = 2/3.

### 5.4 Arm P6 (K=6; RARE on pass 1 only, taught first)

Pass 1: as P1. nevict = 1. Present: 148(15),130,131,140,141,144(21).
Absent: 143.
Pass 2: 100 -> ref=2; 104 -> ref=2. 143 -> restore -> sup=2; evict
144(21) -> 143(22). 144 -> restore -> sup=2; evict 143(22) ->
144(23). nevict = 3.
Present: 148(15),130,131,140,141,144(23). Absent: 143.
Passes 3-6: 100 revises on pass 3 (->148, sup=1), then sup = 2,3,4;
104 revises (->130), then sup = 2,3,4; FREQ present throughout, sup
grows to 6; 143/144 revolve as in P3 (2 evictions per pass);
148 never re-taught (sup stays 1) and never evicted. nevict = 11.
All per-pass probes: pass 3: 100->148 (sup=1), 148->152 (sup=1 >
ref=0) = 152 OK; passes 4-6 OK likewise (100's sup grows; 148's
sup stays 1, still > ref=0). Series: 0,0,1,1,1,1 -> avail = 4.

Frozen P6: ttcA = 2, probeA = 8, nevict = 11, phev = 0.
EVHIST: 143 = 6, 144 = 5, evh(148) = 0. Sum = 11.
Retest: c = 2/2 (q(100) = 152 via 148 sup=1; q(104) = 131);
nc = 2/2; u = 4/4; forget = 0. bprobe = 2/3.

### 5.5 Predicted mechanism (directional: MIRROR-CONFIRMED)

D2 evicts by installation recency, not reinforcement frequency. The
RARE link (148), taught FIRST among phase-2 teachings, is installed
with the LOWEST novel ins of each re-teach pass; every subsequent
novel installation (fresh FREQ links, then the 143/144 revolving
restores) stamps a strictly higher ins. The max-ins victim is
therefore never 148: evh(148) = 0 on all arms, and the churn moves
entirely to the 143/144 pair (EVHIST 143=6, 144=5 on every arm).
Tenure protection engages from the first installation because 148's
age is never reset on non-teach passes (it is simply absent from the
teach list, not re-installed young). Availability over passes 3-6
is 4/4 for every K: the RARE link is present whenever queried, even
when taught only once (K=6, sup=1 suffices for predict since
ref=0). If this trace reproduces exactly, installation recency --
not frequency -- is confirmed as the true determinant of D2
victimhood, and the NTLV churn-trap attribution is causally
validated by its mirror image.

## 6. Assembly, build, run (frozen)

- Single source file `ntom_full.zag`: canonical helpers (z_alloc,
  get32, set32, o_app, o_i64, o_nl, o_flush; copied verbatim from the
  frozen ntlv template), learner fns (D1+D2; cl_* bodies verbatim
  from ntlv_full.zag), oracle fns (linka, ntha, nthq, ansa, ansb,
  isC, isNC per NTLV; bsub/bobj cover the 10 ascending non-RARE
  phase-2 teachings), 2-hop query fn, teachA, teachB(K,pass) with
  THE SOLE LANE CHANGE (148 taught first iff (pass-1) mod K == 0,
  then the 10 ascending), per-pass probe, retest, phev, main
  running the 4 arms (P1/P2/P3/P6) sequentially. No other source.
- Build: `znc ntom_full.zag -o ntom_bin` under safebin-only PATH.
- Run `ntom_bin` 3 times; outputs `ntom_run1.txt`, `ntom_run2.txt`,
  `ntom_run3.txt`. Require byte-identical (cmp) and record sha256.
- Output lines (all numeric, "NTOM " prefix): per arm
  ttcA/probeA/nevict/phev, per-pass q(100)==152 flags p1..p6 and
  avail, retest partition scores (c/nc/u/forget), bprobe (/3),
  nonzero eviction-histogram bins, and K1..K6 verdict bits plus a
  verdict line.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic output
  only via the single-buffer cursor helpers + one `_zag_raw_syscall`
  write (never `_zag_print`); no `!(A && B)` in while conditions
  (De Morgan); if-nesting at most 3 deep with hoisted call results;
  no `[]u8 as *u8` casts (thread `_zag_malloc as *u8`).

## 7. Frozen kill bars

- K1 (learnability; else VOID): ttcA in 1..50 AND probeA = 8 for ALL
  four arms. Else VOID (families not learnable; redesign, do not
  reinterpret).
- K2 (retention of uncontested structure): nc = 2 AND u = 4 for ALL
  four arms.
- K3 (THE MIRROR BAR: order-dependent availability): avail = 4, 4,
  4, 4 for P1, P2, P3, P6 respectively (exact; Section 5). This is
  the frozen tenure-protection prediction: installation recency, not
  frequency, determines D2 victimhood.
- K4 (final revision outcome): c = 2 AND forget = 0 for ALL four
  arms (the RARE link is present at retest in every arm, including
  K=6 taught once).
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): nevict = 11, 11, 11, 11 for P1, P2, P3, P6;
  phev = 0 for ALL arms (no phase-1-link subj ever evicted);
  evh(148) == 0 for ALL arms (white-box: D2 NEVER evicted the
  first-taught RARE link); EVHIST exact: 143 = 6 AND 144 = 5 for
  ALL arms (the churn moves entirely to the 143/144 revolving pair).
- K6 (discriminative validity): avail(P1) = 4 (the probe passes when
  the link is present; not a broken probe) AND nevict > 0 for ALL
  arms (pressure actually exercised). If K6 fails the apparatus
  cannot discriminate -> INCONCLUSIVE at the lane level.

## 8. Verdict mapping (frozen)

Checked in order; first match wins:

- K1 = 0 -> VOID.
- K6 = 0 -> INCONCLUSIVE (apparatus cannot discriminate).
- K2 = 0 -> FAIL-RETENTION (the A-retention machinery broke under
  the new order; not a mechanism result).
- K5 = 0 -> FAIL-PRESSURE (eviction discipline violated: a phase-1
  link evicted, or the RARE link ever evicted, or eviction counts /
  histogram off-trace).
- K4 = 0 -> INFORMATIVE-FAIL (revision/final-outcome off-trace;
  mechanism deeper than the mirror account).
- K3 = 0 -> ORDER-IRRELEVANT (the tenure-protection prediction failed
  as stated; installation recency is NOT the determinant under D2,
  or the mechanism is more complex than the churn-trap account;
  REPORT.md characterizes the actual curve; no recency claim may be
  made).
- else -> MIRROR-CONFIRMED: installation recency, not reinforcement
  frequency, is the true determinant of D2 victimhood. The
  first-taught RARE link tenure-protects (avail 4/4 for all K =
  1,2,3,6); D2 never selects it (evh(148) = 0 on all arms); the
  churn moves to the 143/144 revolving pair (EVHIST 143=6, 144=5).
  The NTLV churn-trap attribution is causally validated by its
  mirror image.

## 9. Honest boundaries (frozen)

- The LINKS are memorized associations; what is rule-STRUCTURED is
  the family (taught 2-hop chains with shared substructure; answers
  require composing links). No rule INDUCTION tested; no L2/L3
  claim. Retention/revision/eviction dynamics over structured
  knowledge only.
- Single capacity point (CAP=20, 1.05x); single contradiction
  magnitude; M=6 fixed, so the availability curve conflates period
  with final-pass phase alignment by construction (the per-pass
  probe series is what separates frequency from phase).
- The ONLY difference vs NT-LOWVALUE-BOUNDARY is the phase-2 teach
  order of the RARE link (first vs last). The learner (D1+D2) is a
  verbatim port; no rule, constant, or comparator was touched. Any
  behavioral difference between the lanes is attributable to teach
  order alone.
- 148's final sup differs by arm (6/3/2/1 for K=1/2/3/6) but all
  satisfy sup > ref = 0, so predict is unaffected: the mirror tests
  PRESENCE (availability), not evidence strength. D1's evidence
  preservation is not exercised here beyond the 143/144 checkpoints.
- A usefulness-aware policy could pin 148 and sacrifice a FREQ link
  instead; D2 has no usefulness signal. The mirror does not redeem
  D2: it confirms D2 is purely recency-driven, which is exactly the
  mechanism the liability claim rests on. Tenure-protection here is
  luck of install order, not usefulness-awareness.
- Port covers the associative instance memory only (NT-PORT
  boundary stands).
