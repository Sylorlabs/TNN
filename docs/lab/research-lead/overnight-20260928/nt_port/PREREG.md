# PREREG: NT-PORT -- Port D1+D2 to the shared continuing-learner substrate

## 1. Question

NT-D2 (C431 PASS) closed the NT series on the minimal surrogate: D1's
preserve-evidence across eviction/re-insertion plus D2's evict-youngest
(LIFO) comparator preserve NT1's selective-retention pattern under
capacity pressure (revision 6/6, FORGET=0, nevict=41, all victims novel
keys). NT-D2 PREREG Section 10 states the honest boundary: ML1/ML0 are
minimal surrogates, not TNN's production substrate; the PASS
characterizes the D1+D2 rule-set, not TNN-as-built.

This lane asks the bridge question: do the D1+D2 rules transfer from
the minimal surrogate to the shared continuing-learner substrate?
Concretely: implement ONLY the D1+D2 memory rules on the continuing
learner's associative instance memory, run a realistic
continuing-learning sequence (sequential lifetime phases with capacity
pressure, world change, novelty, and staleness -- not the NT2 battery),
and check whether the NT1 selective-retention pattern survives with
the same discriminated signatures. An ablation arm (same substrate,
D1+D2 removed) must reproduce the NT2 failure signature on this
substrate; otherwise the apparatus cannot discriminate and no PASS is
allowed.

### 1.1 Substrate selection (recorded pre-implementation)

The shared continuing-learner substrate is
`continuing_learner/contlearn2.zag`: one continuing learner,
associative instance memory of slots, sequential phases, single
main(), no resets, no task labels, pure Zag. It is the substrate whose
memory CAN fill and evict, so the D1+D2 rules (evidence revision,
checkpoint/restore, eviction ordering) have a minimal host.

NOT selected: `lane-contlife/.../contlife.zag` (H-CONTLIFE-1). Its
memory is a hash table with overflow relocation and owner-gated
overwrite; it has no per-entry evidence counters and no revision
rule, so hosting D1+D2 there would require inventing evidence
machinery -- a redesign, not a minimal port. It is recorded as a
future port target, out of scope here.

NOT ported: contlearn2's schema discovery/verify/retire machinery
(kind-1/kind-2 schemas, gates, ledger). That is an orthogonal
capability; the 8-domain schema workload has no contradictions and no
capacity pressure, so D1/D2 dynamics could never fire under it and the
port would be vacuous. The port keeps the substrate's skeleton
(helpers, slot table, associative lookup, sequential phases, single
output buffer idiom) and replaces its memory management with D1+D2.

## 2. Subject (the port: D1+D2 rules only, minimal)

### 2.1 Ported memory rules (frozen)

Slot fields (32 bytes): 0 subj, 4 rel, 8 obj, 12 dom, 16 valid,
20 sup, 24 ref, 28 ins. Key = (subj, rel). `dom` = install-phase
provenance (1 or 2), stamped on every installation; entry metadata,
never consulted by learner decisions except storage.

- Evidence update (NT-frozen rule, ported to (subj,rel) keys): on a
  teaching event for a PRESENT entry, taught obj matches stored obj
  -> sup++; taught obj differs -> ref++, and if ref > sup -> REVISE
  to (new obj, sup=1, ref=0), in place. Revision does NOT touch `ins`.
- D1 (preserve-evidence): on eviction, checkpoint (valid=1, obj,
  sup, ref) keyed by (subj, rel). On insertion of an absent key with
  a valid checkpoint, install the checkpointed (obj, sup, ref), stamp
  dom = current phase, then run the frozen update step with the
  taught obj. On insertion with no valid checkpoint, install fresh
  (taught obj, sup=1, ref=0).
- D2 (evict-youngest): arena holds `ins_seq`, zero-initialized. On
  EVERY installation (fresh and D1-restore alike): ins_seq++,
  slot.ins = ins_seq. Eviction victim = occupied slot with MAXIMUM
  `ins`. `ins` unique per installation; no tie-break. Revision in
  place does not touch `ins`; eviction does not touch survivors.
- Predict: entry present and sup > ref -> stored obj; else -1.
- Capacity CAP = 20 slots.

The comparator is generic and domain-neutral: installation order
only, no task identity, no importance flags, no protection rules, no
modes. The checkpoint table and `ins` are learner state (own prior
evidence / own installation order), containing no oracle information.

### 2.2 Ablation arm (same substrate, D1+D2 removed)

Arm ABL: identical substrate, workload, and update rule, but:
eviction victim = occupied slot with minimum (sup - ref), tie-break
lowest slot index (the NT2 comparator); NO checkpoint table --
every insertion installs fresh (taught obj, sup=1, ref=0) and
eviction discards evidence. `ins` is not maintained. This is the
substrate's memory WITHOUT the two rules, isolating exactly what
D1+D2 contribute.

### 2.3 Everything else frozen

Deterministic: fixed ascending subject order per pass, no RNG. One
continuing learner per arm, fresh, single main(), no resets, no task
labels. Eviction histogram (measurement-only, 30 bins, subjects
100..129) influences no learner decision.

## 3. Realistic continuing-learning sequence (frozen numeric inventory; opaque identifiers)

Subjects are integers; objs are integers; rel = 1 throughout. No
semantic labels anywhere in code or output.

- O1(k) = 200 + ((k*37 + 11) mod 64), for all k. (Oracle, phase 1.)
- O2(k) = 200 + (((O1(k)-200)+32) mod 64) for contradicted subjects,
  guaranteed different from O1(k). (Oracle, phase 2.)
- Phase 1 ("early experience"): 16 subjects 100..115, obj O1(k).
  Train to criterion: repeat passes; after each pass probe all 16.
  Criterion = 16/16 correct for 2 consecutive passes. Max 50 passes
  (fail-safe; hitting it = arm FAIL). Records TTC1.
- Phase 2 ("world change + novel experience"): 3 FIXED passes over,
  in ascending order: C (contradicted) subjects 100..105 taught
  O2(k); K (kept/agreed) subjects 106..109 taught O1(k); N (novel)
  subjects 120..129 taught O1(k). U (untouched) subjects 110..115
  are never taught in phase 2.
- Retention probe: query all 26 subjects. Score C (100..105) vs O2,
  K (106..109) vs O1, U (110..115) vs O1, N presence (120..129).
  FORGET = subjects among C+K+U answering neither their
  phase-1-correct nor (for C) their phase-2-correct obj
  (absent -> -1 counts as forgotten).

Capacity accounting: 26 distinct (subj,rel) > CAP 20. Pressure ratio
26/20 = 1.3x (one step above NT-D2's 1.2x). A stable
retain-everything solution does not exist; eviction must fire, so any
retention pattern is attributable to the rules.

## 4. Frozen predictions (hand-derived by tracing the frozen ported rules)

### 4.1 MAIN arm (D1+D2)

Phase 1: no pressure (16 < 20). TTC1 = 2, probe 16/16, nevict = 0.
Slots 0..15 hold 100..115 as (O1, sup=2, ref=0), ins 1..16.

Phase 2, pass 1: 100..105 -> ref=1 (mismatch, no revise).
106..109 -> sup=3. 120..123 fill slots 16..19 (ins 17..20).
124..129: table full; victims by max ins = 123 (ins 20), then the
just-installed subject each time (revolving door on slot 19):
victims 123,124,125,126,127,128, each checkpointed (O1,1,0). Slot 19
ends as 129 (O1,1,0, ins 26). 6 evictions.

Phase 2, pass 2: 100..105 -> ref=2 (2 > 2 false, no revise).
106..109 -> sup=4. 120..122 hits -> sup=2. 123 absent -> D1 restore
(O1,1,0) -> update -> (O1,2,0); victim = 129 (max ins 26); 123 at
slot 19 (ins 27). 124..128 absent -> restore, each evicting the
current newest (victims 123,124,125,126,127); 129 absent -> restore
(O1,1,0) -> (O1,2,0), evicting 128 (ins 32), slot 19 ins 33.
7 evictions.

Phase 2, pass 3: 100..105 -> ref=3 > sup=2 -> REVISE in place ->
(O2,1,0), ins 1..6 untouched (the comparator never sees the reset).
106..109 -> sup=5. 120..122 -> sup=3. 123..129 absent -> restore +
revolving door on slot 19 (victims 129,123,124,125,126,127,128).
7 evictions.

End state: 100..105 = (O2,1,0); 106..109 = (O1,5,0);
110..115 = (O1,2,0) never evicted, never taught in phase 2;
120..122 = (O1,3,0); 129 = (O1,3,0); 123..128 absent (evicted this
pass, would return on a next teaching).

Frozen numeric predictions, MAIN:
- TTC1 = 2, phase-1 probe = 16/16, nevict = 20, nentries = 20.
- Eviction histogram (subject=count, nonzero only): 123=3, 124=3,
  125=3, 126=3, 127=3, 128=3, 129=2; all other subjects 0 (in
  particular 100..115 = 0: NO phase-1 subject is ever evicted).
  Sum = 20.
- Retention: C_VB = 6/6 (all answer O2), K_OK = 4/4, U_OK = 6/6,
  N present = 4/10 (120,121,122,129), FORGET = 0.

K2 derivation: under the FORGET = 0 regime, C+K+U = 16 subjects are
pinned, leaving 4 slots for 10 N subjects; each of the 3 passes
teaches all 10 N subjects -> at least 6 absent teachings per pass ->
pigeonhole lower bound 18. Predicted 20 = 18 + 2 traced revolving-door
overhead (in passes 2 and 3, the re-inserted subject 123 evicts the
resident subject 129, which is re-taught later in the same pass).
All 20 victims are N subjects; zero phase-1 subjects evicted.

### 4.2 ABL arm (no D1, lowest-net eviction)

Phase 1 identical: TTC1 = 2, probe 16/16, nevict = 0.

Phase 2, pass 1: 100..105 -> (O1,2,1) net=1. 106..109 -> (O1,3,0).
120..123 -> slots 16..19 (O1,1,0). 124: victim = lowest net (min
net=1 among slots 0..5 and 16..19), slot-index tie-break -> slot 0
(100); evict 100 (evidence discarded, no checkpoint); install 124.
125..129: victims slot 0 each time (124,125,126,127,128 -- the
just-installed subject has net=1 = minimum). 6 evictions.

Phase 2, pass 2: 100 absent -> evict 129 (slot 0, net=1 tie-break);
install 100 fresh (O2,1,0). 101..105 present -> (O1,2,2) net=0.
106..109 -> sup=4. 120..123 -> sup=2. 124 absent -> victim min net=0
-> slot 1 (101); install 124. 125..128 absent -> evict 102,103,104,
105 (slots 2..5). 129 absent -> min net=1 among slots 0..5 ->
slot 0 (100); evict 100; install 129. 7 evictions.

Phase 2, pass 3: 100..105 all absent (100 evicted end of pass 2):
each insert evicts the just-installed predecessor at slot 0
(victims 129,100,101,102,103,104). 106..109 -> sup=5. 120..123 ->
sup=3. 124..128 present -> sup=2. 129 absent -> victim min net=1 ->
slot 0 (105); evict 105; install 129. 7 evictions.

Frozen numeric predictions, ABL:
- TTC1 = 2, phase-1 probe = 16/16, nevict = 20, nentries = 20.
- Eviction histogram (nonzero only): 100=3, 101=2, 102=2, 103=2,
  104=2, 105=2, 124=1, 125=1, 126=1, 127=1, 128=1, 129=2.
  Sum = 20. C subjects ARE evicted (100..105 appear); U subjects
  (110..115) never are.
- Retention: C_VB = 0/6 (all C subjects absent -> -1), K_OK = 4/4,
  U_OK = 6/6, N present = 10/10, FORGET = 6 (the six contradicted
  subjects, forgotten).

Note the transfer moral, predicted: MAIN and ABL have the SAME
eviction count (20) with OPPOSITE victim sets -- the count was never
the measure; the victim set is. ABL reproduces the NT2 failure
signature (eviction preempts revision; contradicted subjects
forgotten) on the production substrate.

### Predicted mechanism (directional prediction: PORT-PASS)

D1's restore lets ref accumulate across eviction boundaries so
revision fires (pass 3); D2's LIFO comparator protects the revised
entries structurally (revised C subjects are old, ins 1..6; the reset
is invisible to the comparator) and protects untouched U subjects
(ins 11..16, far older than any N subject). All churn concentrates
on N subjects, which are re-taught every pass: evicting them is
forget-free by construction. The NT1 selective-retention pattern
(ret
...[truncated 3576 chars]