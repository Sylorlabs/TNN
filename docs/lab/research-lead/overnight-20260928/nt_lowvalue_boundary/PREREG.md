# PREREG: NT-LOWVALUE-BOUNDARY -- the "genuinely low-value" boundary: useful but infrequently-reinforced links under D1+D2

## 1. Question

NT-PORT-PRESSURE (E8.1, PORT-PASS-STRUCT) ported the NT1 rule set
(D1 preserve-evidence + D2 evict-youngest) to rule-structured
families (2-hop chains with shared substructure) at 1.2x pressure.
All 14 evictions were confined to novel links re-taught EVERY pass:
forget-free churn, phev = 0. Its preregistered open boundary, restated
in the lane task: whether LIFO's tenure principle holds when novel
links are NOT re-taught every pass.

This lane probes the "genuinely low-value" boundary: some novel links
are GENUINELY USEFUL (a scored query depends on them) but NOT
re-taught every pass (infrequent reinforcement, period K). Questions:

(a) Does D2 (evict-youngest, max-ins victim) evict them? Is LIFO
    tenure a liability for useful-but-infrequent links?
(b) What is the tradeoff: how infrequent can reinforcement be before
    the link is lost (unavailable when queried)?

Mechanism under test (predicted from the frozen rules, not a new
hypothesis): D2's victim is the most recently INSTALLED entry.
A link re-installed by D1-restore on a re-teach pass is born YOUNG
(max ins). Background churn from frequently-reinforced links then
evicts the youngest first. So an infrequently-reinforced link that is
re-installed late in teach order never accumulates tenure: each
re-teach resets its age, and the churn evicts it within ~1 pass.
Tenure protection cannot engage for it. Predicted signature:
availability of the rare link collapses as K grows, while the
eviction histogram names the rare link as a repeat victim and no
phase-1 link is ever evicted (phev = 0).

## 2. Subject (frozen)

The NT-PORT-PRESSURE subject verbatim: the continuing-learner
skeleton (associative instance memory, sequential lifetime phases,
single main(), no resets, no task labels) with ONLY the D1+D2 memory
rules installed. Slot fields (32 bytes): 0 subj, 4 rel, 8 obj,
12 dom, 16 valid, 20 sup, 24 ref, 28 ins. Key = (subj, rel).
rel = 1 throughout. `dom` = install-phase provenance, stamped on
every installation; entry metadata, never consulted by learner
decisions. Arena holds nentries, nevict, ins_seq, nslots.

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

The ONLY novelty vs NT-PORT-PRESSURE is the workload and the
re-teach regime (Sections 3-4). The learner is untouched.

## 3. Workload (frozen numeric inventory; opaque identifiers)

Family A: NT-PORT-PRESSURE verbatim. 14 links, 8 chains with shared
substructure (A1/A2 share (101)->102; A3/A4 share (105)->106):
100->101, 101->102, 103->101, 104->105, 105->106, 107->105,
108->109, 109->110, 111->112, 112->113, 114->115, 115->116,
117->118, 118->119. Query starts QS = {100,103,104,107,108,111,
114,117}. ANSA = {102,102,106,106,110,113,116,119}.

Phase-2 teachings per pass, ascending subj order:
- C (contradicted links), every pass: (100,1)->148, (104,1)->130.
- NC (agreed links), every pass: (101,1)->102, (105,1)->106.
- FREQ (frequently-reinforced novel links), every pass:
  (130,1)->131, (131,1)->132, (140,1)->141, (141,1)->142,
  (143,1)->144, (144,1)->145.
  Novel 2-hop chains: q(130) = 132, q(140) = 142, q(143) = 145.
  Note (130,1)->131 also supports the revised q(104).
- RARE (genuinely useful, infrequently reinforced), on pass p iff
  (p-1) mod K == 0: (148,1)->152.

The RARE link is GENUINELY USEFUL: after revision, q(100) =
100 -> 148 -> 152, so the scored c-query q(100) requires link
(148,1)->152 to be present. It is NOT re-taught every pass
(period K; K = 6 means taught once, on pass 1 only).

ANSB (correct 2-hop answers under family B): q(100) -> 152,
q(104) -> 131, all others ANSA.

Retest partitions of the 8 A queries (NTPP verbatim logic):
- C: starts 100, 104. Correct: ANSB (152, 131; revised).
- NC: starts 103, 107. Correct: ANSA = ANSB (102, 106; retained).
- U: starts 108, 111, 114, 117. Correct: ANSA (110, 113, 116, 119).
- FORGET = C queries answering neither ANSA nor ANSB, plus NC/U
  queries answering not-ANSA (absent link -> -1 counts as forgotten).

Capacity accounting: 14 A links + 7 novel subjs
(130,131,140,141,143,144,148) = 21 distinct (subj,rel) keys > CAP 20.
Pressure ratio 21/20 = 1.05x. Exactly 1 key must be absent at any
time; any absence pattern beyond that, and WHICH key is absent, is
attributable to the rules. A-links hold ins 1..14 forever (revision
is in place; re-teaching a present link never touches ins), so every
novel installation (ins >= 15) is younger than every A-link: D2 can
never select a phase-1 link while any novel link is present, hence
phev = 0 structurally.

Arms (each on a FRESH learner; the period selector is a harness
condition, not a cognitive mode): P1 (K=1, RARE every pass; the
NTPP-regime control), P2 (K=2), P3 (K=3), P6 (K=6, RARE taught once).
M = 6 phase-2 passes, fixed, all arms.

## 4. Protocol (frozen)

- `trainA`: repeat passes over the 14 A links (ascending subj); after
  each pass probe the 8 queries. Criterion = 8/8 correct for 2
  consecutive passes. Max 50 passes (fail-safe; hitting it = arm
  FAIL). Returns passes used. Predicted: ttcA = 2, probeA = 8, all arms.
- Phase 2: 6 FIXED passes. Per pass, teachings in ascending subj
  order: 100, 101, 104, 105, 130, 131, 140, 141, 143, 144, then 148
  iff (pass-1) mod K == 0. After EACH pass, probe q(100) vs 152
  (the RARE-usefulness probe; read-only, no state change).
  avail(K) = number of passes p in {3,4,5,6} with q(100) == 152
  (passes 1-2 are pre-revision; q(100) cannot be 152 there).
- After pass 6: NTPP-style retest (c/nc/u/forget); bprobe =
  (q(130)==132) + (q(140)==142) + (q(143)==145), /3; record nevict,
  per-subj eviction histogram (bins 100..150), phev (evictions of
  subjs 100..119).

## 5. Frozen predictions (hand-derived by tracing the frozen rules)

Notation: A-links occupy slots 0..13, ins 1..14, all (obj, sup=2,
ref=0) after phase 1. Novel slots 14..19.

### 5.1 Arm P1 (K=1; RARE every pass)

Pass 1: 100 -> ref=1; 104 -> ref=1; 101,105 -> sup=3. Novel:
130(15),131(16),140(17),141(18),143(19),144(20) fill slots 14..19;
148 -> evict max-ins = 144(20) -> install 148 (ins 21), fresh
(152,1,0); checkpoint 144 = (145,1,0). nevict = 1. Present novel:
130,131,140,141,143,148. Absent: 144.

Pass 2: 100 -> ref=2; 104 -> ref=2; 101,105 -> sup=4; FREQ present ->
sup=2. 144 absent -> D1 restore (145,1,0) -> sup=2; evict max-ins:
148(21) -> install 144 (ins 22); checkpoint 148 = (152,1,0).
148 absent -> restore (152,1,0) -> sup=2; evict max-ins: 144(22) ->
install 148 (ins 23); checkpoint 144 = (145,2,0). nevict = 3.
Present: 130,131,140,141,143,148. Absent: 144.

Pass 3: 100 -> ref=3 > sup=2 -> REVISE in place -> (100,1)->148,
(sup=1,ref=0), ins untouched (1). 104 -> ref=3 > 2 -> REVISE ->
(104,1)->130, ins untouched (4). 101,105 -> sup=5; FREQ -> sup=3.
144 absent -> restore (145,2,0) -> sup=3; evict 148(23) -> 144(24);
checkpoint 148 = (152,2,0). 148 absent -> restore (152,2,0) -> sup=3;
evict 144(24) -> 148(25); checkpoint 144 = (145,3,0). nevict = 5.
Present: 130,131,140,141,143,148. Probe q(100): 100->148 (sup=1) ->
152 (sup=3) = 152. OK.

Pass 4: 100 -> sup=2; 104 -> sup=2; 101,105 -> sup=6; FREQ -> sup=4.
144 -> restore (145,3,0) -> sup=4; evict 148(25) -> 144(26).
148 -> restore (152,3,0) -> sup=4; evict 144(26) -> 148(27).
nevict = 7. Probe q(100) = 152. OK.

Pass 5: 100 -> sup=3; 104 -> sup=3; FREQ -> sup=5. 144 -> restore ->
sup=5; evict 148(27) -> 144(28). 148 -> restore -> sup=5;
evict 144(28) -> 148(29). nevict = 9. Probe OK.

Pass 6: 100 -> sup=4; 104 -> sup=4; FREQ -> sup=6. 144 -> restore ->
sup=6; evict 148(29) -> 144(30). 148 -> restore -> sup=6;
evict 144(30) -> 148(31). nevict = 11. Probe OK.

Frozen P1: ttcA = 2, probeA = 8, nevict = 11, phev = 0.
EVHIST nonzero: 144 = 6 (pass 1 once + passes 2-6 once each as the
victim of 148's restore), 148 = 5 (passes 2-6 once each as the victim
of 144's restore). Sum = 11.
Per-pass q(100)==152: p1 0, p2 0, p3 1, p4 1, p5 1, p6 1 -> avail = 4.
Retest: c = 2/2 (q(100) = 152 via present 148; q(104) = 131 via
104->130->131); nc = 2/2; u = 4/4; forget = 0. bprobe = 2/3
(q(130) OK, q(140) OK, q(143): 144 absent -> -1).

### 5.2 Arm P2 (K=2; RARE on passes 1,3,5)

Pass 1: identical to P1 pass 1. nevict = 1. Present:
130,131,140,141,143,148. Absent: 144. (100: ref=1; 104: ref=1.)

Pass 2 (no 148): 100 -> ref=2; 104 -> ref=2; 101,105 -> sup=4;
FREQ -> sup=2. 144 absent -> restore (145,1,0) -> sup=2; evict
max-ins: 148(21) -> 144(22); checkpoint 148 = (152,1,0). nevict = 2.
Present: 130,131,140,141,143,144. Absent: 148.

Pass 3 (148 taught): 100 -> ref=3 > 2 -> REVISE -> ->148. 104 ->
ref=3 > 2 -> REVISE -> ->130. 101,105 -> sup=5; FREQ -> sup=3;
144 present -> sup=3. 148 absent -> restore (152,1,0) -> sup=2; evict
max-ins: 144(22) -> 148(23); checkpoint 144 = (145,3,0). nevict = 3.
Present: 130,131,140,141,143,148. Probe q(100) = 152. OK.

Pass 4 (no 148): 100 -> sup=2; 104 -> sup=2; 101,105 -> sup=6;
FREQ -> sup=4. 144 absent -> restore (145,3,0) -> sup=4; evict
148(23) -> 144(24); checkpoint 148 = (152,2,0). nevict = 4.
Present: 130,131,140,141,143,144. Absent: 148. Probe q(100): 148
absent -> -1. MISS.

Pass 5 (148 taught): 100 -> sup=3; 104 -> sup=3; 101,105 -> sup=7;
FREQ -> sup=5; 144 present -> sup=5. 148 absent -> restore (152,2,0)
-> sup=3; evict 144(24) -> 148(25); checkpoint 144 = (145,5,0).
nevict = 5. Present: 130,131,140,141,143,148. Probe OK.

Pass 6 (no 148): 100 -> sup=4; 104 -> sup=4; FREQ -> sup=6. 144 absent
-> restore (145,5,0) -> sup=6; evict 148(25) -> 144(26); checkpoint
148 = (152,3,0). nevict = 6. Present: 130,131,140,141,143,144.
Absent: 148. Probe MISS.

Frozen P2: ttcA = 2, probeA = 8, nevict = 6, phev = 0.
EVHIST: 144 = 3 (passes 1,3,5), 148 = 3 (passes 2,4,6). Sum = 6.
Per-pass q(100)==152: 0,0,1,0,1,0 -> avail = 2.
Retest: c = 1/2 (q(100): 148 absent -> -1, neither 102 nor 152;
q(104) = 131 OK); nc = 2/2; u = 4/4; forget = 1. bprobe = 3/3
(144 present at end).

### 5.3 Arm P3 (K=3; RARE on passes 1,4)

Pass 1: as P1. nevict = 1. Present: 130,131,140,141,143,148.
Pass 2 (no 148): 100 -> ref=2; 104 -> ref=2. 144 -> restore -> sup=2;
evict 148(21) -> 144(22). nevict = 2. Present:
130,131,140,141,143,144. Absent: 148.
Pass 3 (no 148): 100 -> ref=3 > 2 -> REVISE -> ->148. 104 -> REVISE
-> ->130. 144 present -> sup=3. No evictions. nevict = 2. Probe
q(100): 148 absent -> MISS.
Pass 4 (148 taught): 100 -> sup=2; 104 -> sup=2; 101,105 -> sup=7;
FREQ -> sup=4; 144 present -> sup=4. 148 absent -> restore (152,1,0)
-> sup=2; evict 144(22) -> 148(23). nevict = 3. Present:
130,131,140,141,143,148. Probe OK.
Pass 5 (no 148): 100 -> sup=3; 104 -> sup=3; FREQ -> sup=5. 144 absent
-> restore (145,4,0) -> sup=5; evict 148(23) -> 144(24). nevict = 4.
Present: 130,131,140,141,143,144. Absent: 148. Probe MISS.
Pass 6 (no 148): 100 -> sup=4; 104 -> sup=4; FREQ -> sup=6; 144 present
-> sup=6. No evictions. nevict = 4. Probe MISS.

Frozen P3: ttcA = 2, probeA = 8, nevict = 4, phev = 0.
EVHIST: 144 = 2 (passes 1,4), 148 = 2 (passes 2,5). Sum = 4.
Per-pass q(100)==152: 0,0,0,1,0,0 -> avail = 1.
Retest: c = 1/2; nc = 2/2; u = 4/4; forget = 1. bprobe = 3/3.

### 5.4 Arm P6 (K=6; RARE on pass 1 only)

Pass 1: as P1. nevict = 1. Present: 130,131,140,141,143,148.
Pass 2: 144 -> restore -> sup=2; evict 148(21) -> 144(22). nevict = 2.
Present: 130,131,140,141,143,144. Absent: 148.
Passes 3-6: 100 revises on pass 3 (->148), then sup = 2,3,4; 104
revises (->130), then sup = 2,3,4; FREQ present throughout, sup grows
to 6; 144 present, sup to 6. Zero evictions passes 3-6. nevict = 2.
All per-pass probes MISS (148 never restored).

Frozen P6: ttcA = 2, probeA = 8, nevict = 2, phev = 0.
EVHIST: 144 = 1, 148 = 1. Sum = 2.
Per-pass q(100)==152: 0,0,0,0,0,0 -> avail = 0.
Retest: c = 1/2; nc = 2/2; u = 4/4; forget = 1. bprobe = 3/3.

### 5.5 Predicted mechanism (directional: LIABILITY-CONFIRMED)

D2 evicts by installation recency. The RARE link (148), taught last
in ascending order, is re-installed YOUNG on every re-teach pass
(D1 restore stamps a fresh max ins). On every non-teach pass the
FREQ background churn (the 144/148 revolving pair) evicts the
youngest entry, which is 148. So the genuinely-useful-but-
infrequently-reinforced link is unavailable on every pass after its
re-teach: availability over passes 3-6 = 4,2,1,0 for K=1,2,3,6.
Tenure protection never engages for it because re-installation keeps
resetting its age: the churn trap. The final retest shows c = 2/2
only for K=1; K >= 2 lose q(100) (c = 1/2, forget = 1) although
revision itself completed (100 -> 148 revised correctly; the second
link is what is missing). The tradeoff: the link is lost ~1 pass
after each re-teach; availability ~= 1/K over the scored window.
There is no safe infrequent regime under this order and pressure:
even K=2 halves availability.

## 6. Assembly, build, run (frozen)

- Single source file `ntlv_full.zag`: canonical helpers (z_alloc,
  get32, set32, o_app, o_i64, o_nl, o_flush; copied verbatim from the
  frozen nt_port_pressure template), learner fns (D1+D2, arm=0 only;
  cl_* bodies verbatim), oracle fns (linka, ntha, nthq, ansa as NTPP;
  new bsub/bobj/bsubn for the Section 3 inventory; ansb/isC/isNC per
  Section 3), 2-hop query fn, teachA/teachB(K,pass), per-pass probe,
  retest, phev, main running the 4 arms (P1/P2/P3/P6) sequentially.
  No other source.
- Build: `znc ntlv_full.zag -o ntlv_bin` under safebin-only PATH.
- Run `ntlv_bin` 3 times; outputs `ntlv_run1.txt`, `ntlv_run2.txt`,
  `ntlv_run3.txt`. Require byte-identical (cmp) and record sha256.
- Output lines (all numeric): per arm ttcA/probeA/nevict/phev,
  per-pass q(100)==152 flags p1..p6 and avail, retest partition
  scores (c/nc/u/forget), bprobe (/3), nonzero eviction-histogram
  bins, and K1..K6 verdict bits plus a verdict line.
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
- K3 (the boundary bar: availability tradeoff): avail = 4, 2, 1, 0
  for P1, P2, P3, P6 respectively (exact; Section 5).
- K4 (final revision outcome): P1: c = 2 AND forget = 0; P2, P3, P6:
  c = 1 AND forget = 1.
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): nevict = 11, 6, 4, 2 for P1, P2, P3, P6; phev = 0
  for ALL arms (no phase-1-link subj ever evicted); evh(148) > 0 for
  ALL arms (white-box: D2 demonstrably evicted the RARE link).
- K6 (discriminative validity): avail(P1) = 4 (the probe passes when
  the link is present; not a broken probe) AND nevict > 0 for ALL
  arms (pressure actually exercised). If K6 fails the apparatus
  cannot discriminate -> INCONCLUSIVE at the lane level.

## 8. Verdict mapping (frozen)

Checked in order; first match wins:

- K1 = 0 -> VOID.
- K6 = 0 -> INCONCLUSIVE (apparatus cannot discriminate).
- K2 = 0 -> FAIL-RETENTION (the A-retention machinery broke under
  the new workload; not a boundary result).
- K5 = 0 -> FAIL-PRESSURE (eviction discipline violated: a phase-1
  link evicted, or the RARE link never evicted, or eviction counts
  off-trace).
- K4 = 0 -> INFORMATIVE-FAIL (revision/final-outcome off-trace;
  mechanism deeper than the boundary).
- K3 = 0 -> NO-LIABILITY (the liability-direction availability
  prediction failed as stated; REPORT.md characterizes the actual
  curve; no liability claim may be made).
- else -> LIABILITY-CONFIRMED: D2's evict-youngest is a liability
  for genuinely-useful-but-infrequently-reinforced links under
  capacity pressure. Availability 4/4, 2/4, 1/4, 0/4 across
  K = 1, 2, 3, 6: the RARE link is lost ~1 pass after each re-teach
  (churn trap: D1 re-installation resets its tenure; D2 evicts the
  youngest). Tradeoff: availability ~= 1/K over the scored window;
  no safe infrequent regime at this pressure and teach order.

## 9. Honest boundaries (frozen)

- The LINKS are memorized associations; what is rule-STRUCTURED is
  the family (taught 2-hop chains with shared substructure; answers
  require composing links). No rule INDUCTION tested; no L2/L3
  claim. Retention/revision/eviction dynamics over structured
  knowledge only.
- Single capacity point (CAP=20, 1.05x); single contradiction
  magnitude; the RARE link is taught LAST in ascending order (its
  youth at re-teach is load-bearing for the mechanism; a
  first-taught RARE link would tenure-protect instead -- that is a
  separate experiment, not this one).
- The availability curve conflates reinforcement period with final-
  pass phase alignment by construction (M=6 fixed); the per-pass
  probe series is what separates frequency from phase.
- A usefulness-aware policy could pin 148 and sacrifice a FREQ link
  instead; D2 has no usefulness signal. The liability named here is
  D2's usefulness-blindness manifesting as a churn trap for
  infrequently-reinforced links, not a claim that any policy could
  retain everything (pigeonhole: 21 keys, 20 slots).
- Port covers the associative instance memory only (NT-PORT
  boundary stands).
