# PREREG: NT-PORT-PRESSURE (E8.1) -- the NT1 rule on the continuing learner under capacity pressure, with rule-structured families

## 1. Question

NT1 (negative_transfer/REPORT.md, PASS) showed selective retention
EMERGES from entry-local error-driven evidence revision with dedicated
addressing: no protection flags, no task labels, no freeze commands.
NT-PORT (PORT-PASS) ported the rule set (D1 preserve-evidence +
D2 evict-youngest) to the shared continuing-learner substrate at 1.3x
pressure; NT-PRESSURE (PORT-PASS-ALL) scaled the envelope to 5x. All
three batteries used memorized key-value associations. Their shared
honest boundary: the families are bare key-value pairs, not structured
knowledge.

This lane (FRONTIER-AUDIT E8.1) asks the remaining untested question:
does the rule preserve RULE-STRUCTURED families under capacity
pressure? Family A is a taught graph of 2-hop chains with SHARED
SUBSTRUCTURE (two chains share one link; a query answer requires
composing two links, so one corrupted link breaks the answer). Family B
contradicts a subset of A links (including first links of chains that
share their second link), agrees on the shared links, leaves other
chains untouched, and adds novel chains. Then re-ask A. Capacity cap
forces evictions (nevict > 0 required by a bar).

Arms (each on a FRESH learner; `arm` is a harness condition selector,
not a cognitive mode): PORT (the ported rule set, D1+D2, associative
dedicated addressing), NOADDR (identical update rule, overlapping
address map, the ML0-style fragility control), FRESH (PORT rules, reset
between families: the no-lifetime-memory baseline).

## 2. Subject (frozen)

### 2.1 Ported memory rules (from NT-PORT, unchanged)

Slot fields (32 bytes): 0 subj, 4 rel, 8 obj, 12 dom, 16 valid,
20 sup, 24 ref, 28 ins. Key = (subj, rel). `dom` = install-phase
provenance, stamped on every installation; entry metadata, never
consulted by learner decisions. Arena holds nentries, nevict,
ins_seq, nslots. rel = 1 throughout.

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
- Capacity CAP = 20 slots (PORT/FRESH). The comparator is generic:
  installation order only, no task identity, no importance flags, no
  protection rules, no modes.

### 2.2 NOADDR arm (overlapping address map; ML0-style fragility control)

Same substrate, same update rule, same 2-hop query procedure, but the
address map overlaps: slot(subj) = subj-100 for subj in 100..119;
subj 130 -> slot 30; subj 131 -> slot 31; novel chain subjs alias onto
A-only (never-taught-in-B) slots: 140->8, 141->9, 143->11, 144->12,
146->14, 147->15, 149->17, 150->18. Table has 32 slots; 24 distinct
keys map to 16 distinct slots, so eviction never fires (nevict = 0 by
construction) and D1 never engages. A later write to an aliased slot
DESTROYS the earlier entry. This is a legitimate alternative
architecture class (fixed overlapping storage), not sabotage: it
learns each family in isolation but is predicted to destroy
multi-hop structure under B training.

### 2.3 FRESH arm (no-lifetime-memory baseline)

PORT rules, but the learner is RESET between families: train A to
criterion (records ttcA_fresh), reset to a fresh learner, train B to
criterion (records ttcB_fresh), probe the 14 B links, retest the 8 A
queries. Shows what B-learning alone preserves (nothing A-only).

### 2.4 Everything else frozen

Deterministic: fixed ascending subj order per pass, no RNG. One
continuing learner per arm, single main(), no resets except the
FRESH arm's preregistered between-family reset, no task labels.
Eviction histogram (measurement-only; bins for subjs 100..150)
influences no learner decision.

## 3. Rule-structured families (frozen numeric inventory; opaque identifiers)

rel = 1 throughout. LINKA(subj) is the family-A link oracle:
100->101, 101->102, 103->101, 104->105, 105->106, 107->105,
108->109, 109->110, 111->112, 112->113, 114->115, 115->116,
117->118, 118->119. Eight 2-hop chains; A1 (100->101->102) and A2
(103->101->102) SHARE the link (101)->102; A3 (104->105->106) and A4
(107->105->106) SHARE the link (105)->106. 14 distinct links.

Query starts QS = {100,103,104,107,108,111,114,117}. Correct answers:
ANSA: 102,102,106,106,110,113,116,119. ANSB: 132,102,133,106,110,113,116,119.

Family B teachings (14, ascending subj order per pass):
- C (contradicted links): (100,1)->130, (104,1)->131. New chain
  answers: q(100) = 132 via novel link (130,1)->132; q(104) = 133 via
  novel link (131,1)->133.
- NC (agreed links): (101,1)->102, (105,1)->106 (the SHARED links,
  taught with the same obj).
- N (novel links): (130,1)->132, (131,1)->133, (140,1)->141,
  (141,1)->142, (143,1)->144, (144,1)->145, (146,1)->147,
  (147,1)->148, (149,1)->150, (150,1)->151.

Retest partitions of the 8 A queries:
- C: starts 100, 104. Correct retest answer: ANSB (132, 133; revised).
- NC: starts 103, 107. Correct retest answer: ANSA = ANSB (102, 106;
  retained; their chains share links with contradicted chains).
- U: starts 108, 111, 114, 117. Correct retest answer: ANSA
  (110, 113, 116, 119; untouched).
- FORGET = C queries answering neither ANSA nor ANSB, plus NC/U
  queries answering not-ANSA (absent link -> -1 counts as forgotten).

Capacity accounting: 24 distinct (subj,rel) keys > CAP 20. Pressure
ratio 24/20 = 1.2x. A stable retain-everything solution does not
exist; eviction must fire, so any retention pattern is attributable
to the rules.

## 4. Protocol (frozen)

- `trainA`: repeat passes over the 14 A links (ascending subj); after
  each pass probe the 8 queries. Criterion = 8/8 correct for 2
  consecutive passes. Max 50 passes (fail-safe; hitting it = arm
  FAIL). Returns passes used.
- PORT/NOADDR: trainA (records ttcA, probeA); 3 FIXED passes of the 14
  B teachings in ascending subj order; retest the 8 A queries;
  record nevict, eviction histogram, phev (evictions of phase-1-link
  subjs 100..119, from the histogram).
- FRESH: trainA (records ttcA_fresh); RESET to a fresh learner;
  `trainB`: repeat passes over the 14 B teachings; after each pass
  probe all 14 B links; criterion = 14/14 for 2 consecutive passes;
  max 50 (fail-safe). Records ttcB_fresh, bprobe_fresh; retest the 8
  A queries on the B-only learner.

## 5. Frozen predictions (hand-derived by tracing the frozen rules)

### 5.1 PORT arm (D1+D2)

Phase 1: no pressure (14 < 20). TTC_A = 2, probeA = 8/8, nevict = 0.
Slots 0..13 hold the 14 A links, ins 1..14, all (obj, sup=2, ref=0).

Phase 2, pass 1 (order: 100,104,101,105,130,131,140,141,143,144,
146,147,149,150): 100 -> ref=1; 104 -> ref=1; 101 -> sup=3;
105 -> sup=3; 130..144 fill slots 14..19 (ins 15..20); 146 evicts 144
(ins 20, revolving door on slot 19); 147 evicts 146; 149 evicts 147;
150 evicts 149. nevict = 4. Present: 14 A-links + 130,131,140,141,
143,150. Checkpoints: 144,146,147,149 at (obj,1,0).

Phase 2, pass 2: 100 -> ref=2; 104 -> ref=2 (no revise: 2 > 2 false);
101,105 -> sup=4; 130,131,140,141,143 hits -> sup=2; 144 absent ->
D1 restore (145,1,0) -> sup=2, victim 150 (ins 24); 146 absent ->
restore -> sup=2, victim 144 (ins 25); 147 absent -> restore ->
sup=2, victim 146 (ins 26); 149 absent -> restore -> sup=2, victim
147 (ins 27); 150 absent -> restore (151,1,0) -> sup=2, victim 149
(ins 28). nevict = 9.

Phase 2, pass 3: 100 -> ref=3 > sup=2 -> REVISE in place ->
(100,1)->130, (sup=1, ref=0), ins untouched; 104 -> ref=3 > 2 ->
REVISE -> (104,1)->131; 101,105 -> sup=5; 130,131,140,141,143 ->
sup=3; 144,146,147,149,150 absent -> restore + revolving door
(victims 150,144,146,147,149; ins 30..34). nevict = 14.

Frozen numeric predictions, PORT:
- ttcA = 2, probeA = 8, nevict = 14, phev = 0.
- EVHIST (nonzero only): 144=3, 146=3, 147=3, 149=3, 150=2; sum 14;
  all victims novel subjs; zero phase-1-link subjs evicted.
- RET: c = 2/2 (100->130->132, 104->131->133), nc = 2/2
  (103->101->102, 107->105->106), u = 4/4, forget = 0.
- nevict derivation: 12 pigeonhole lower bound under FORGET = 0
  (14 teachings/pass, 14 pinned phase-1 links, 6 free slots, 10 novel
  links -> >= 4 absent teachings per pass x 3 passes) + 2 traced
  revolving-door overhead in passes 2 and 3 (the re-inserted 144
  evicts 150, re-taught later in the same pass).

### 5.2 NOADDR arm (overlapping map)

Phase 1: ttcA = 2, probeA = 8/8, nevict = 0. Slots hold the 14 A
links at 0,1,3,4,5,7,8,9,11,12,14,15,17,18.

Phase 2, pass 1: 100 (slot 0) -> ref=1; 104 (slot 4) -> ref=1;
101 (slot 1) -> sup=3; 105 (slot 5) -> sup=3; 130 (slot 30),
131 (slot 31) created; 140 -> slot 8 DESTROYS (108,1)->109; 141 ->
slot 9 DESTROYS (109,1)->110; 143 -> slot 11 DESTROYS (111,1)->112;
144 -> slot 12 DESTROYS (112,1)->113; 146 -> slot 14 DESTROYS
(114,1)->115; 147 -> slot 15 DESTROYS (115,1)->116; 149 -> slot 17
DESTROYS (117,1)->118; 150 -> slot 18 DESTROYS (118,1)->119.
Passes 2-3: 100,104 -> ref=2 then revise in pass 3 (in place);
101,105 -> sup=5; novel slots -> sup=3. B-link probe = 14/14 (B's
own keys all have dedicated slots; only A-only links destroyed).

Frozen numeric predictions, NOADDR:
- ttcA = 2, probeA = 8, nevict = 0, bprobe = 14.
- RET: c = 2/2 (revision works: contradicted keys have dedicated
  slots), nc = 2/2 (shared links survive: B agrees on them), u = 0/4
  (A5: 108->141->142; A6: 111->144->145; A7: 114->147->148; A8:
  117->150->151), forget = 4.
- Structural failure signature: four untouched 2-hop chains destroyed
  by novel-key aliasing; multi-hop answers fail although no
  contradiction touched them.

### 5.3 FRESH arm (reset between families)

trainA: ttcA_fresh = 2. Reset. trainB on the B-only learner: 14
links, no pressure (14 < 20): ttcB_fresh = 2, bprobe_fresh = 14.
Retest: q(100) = 132 (B), q(104) = 133 (B); q(103), q(107), q(108),
q(111), q(114), q(117) -> -1 (links absent).

Frozen numeric predictions, FRESH:
- ttcA_fresh = 2, ttcB_fresh = 2, bprobe_fresh = 14.
- RET: c = 2/2, nc = 0/2, u = 0/4, forget = 6. The no-lifetime-memory
  baseline: B-learning alone preserves nothing A-only.

### Predicted mechanism (directional prediction: PORT-PASS-STRUCT)

D1's restore lets ref accumulate across eviction boundaries so
revision fires (pass 3); D2's LIFO comparator protects the revised
entries structurally (revised C links are old, ins 1..6; the reset is
invisible to the comparator) and protects untouched/shared U/NC links
(ins 7..14, far older than any N link). All churn concentrates on N
links, which are re-taught every pass: evicting them is forget-free
by construction. The NT1 selective-retention pattern transfers to
rule-structured families: revision completes on contradicted chains,
shared-substructure chains retain through the agreed shared links,
untouched chains are never eviction candidates, and nothing is
needlessly forgotten. NOADDR shows the failure is in addressing, not
the update rule; FRESH shows retention comes from lifetime memory,
not from B containing the answers.

## 6. Assembly, build, run (frozen)

- Single source file `ntpp_full.zag`: canonical helpers (z_alloc,
  get32, set32, o_app, o_i64, o_nl, o_flush; copied verbatim from the
  frozen nt_port template), learner fns (parameterized slot count and
  arm), oracle fns (linka, ansa, ansb, B teaching tables), 2-hop
  query fn, protocol fns, main. No other source.
- Build: `znc ntpp_full.zag -o ntpp_bin` under safebin-only PATH.
- Run `ntpp_bin` 3 times; outputs `ntpp_run1.txt`, `ntpp_run2.txt`,
  `ntpp_run3.txt`. Require byte-identical (cmp) and record sha256.
- Output lines (all numeric): per arm ttcA/probeA/nevict/phev,
  retest partition scores (c/nc/u/forget), nonzero eviction-histogram
  bins (PORT), B-link probe (NOADDR/FRESH), and per-lane K1..K5
  verdict bits plus a verdict line.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic output
  only via the single-buffer cursor helpers + one `_zag_raw_syscall`
  write (never `_zag_print`); no `!(A && B)` in while conditions
  (De Morgan); if-nesting at most 3 deep with hoisted call results;
  no `[]u8 as *u8` casts (thread `_zag_malloc as *u8`).

## 7. Frozen kill bars

- K1 (learnability; else VOID): ttcA_port in 1..50 AND probeA_port
  = 8 AND ttcB_fresh in 1..50 AND bprobe_fresh = 14. Else VOID
  (families not learnable; redesign, do not reinterpret).
- K2 (PORT retention of uncontested structure): nc_port = 2 AND
  u_port = 4.
- K3 (PORT selective revision, not erasure): c_port = 2 AND
  forget_port = 0.
- K4 (pressure exercised, eviction discipline): nevict_port = 14
  AND phev_port = 0 (all 14 victims novel subjs; no live
  phase-1-link structure evicted; white-box check via histogram).
- K5 (discriminative validity): (u_noaddr != 4 OR forget_noaddr != 0)
  AND (nc_fresh != 2 OR u_fresh != 4). Predicted: NOADDR u = 0/4,
  forget = 4 (structural aliasing failure); FRESH nc = 0/2, u = 0/4
  (no-lifetime-memory failure). If NOADDR passed K2+K3 AND FRESH
  passed K2, the apparatus cannot detect fragility -> INCONCLUSIVE
  at the lane level, never PORT-PASS-STRUCT.

## 8. Verdict mapping (frozen)

- K1 fails -> **VOID** (redesign families).
- K1 holds, K5 fails -> **INCONCLUSIVE** (apparatus lacks
  discriminative power; PORT-PASS-STRUCT forbidden).
- K2 or K3 fails (PORT) -> **FAIL-RETENTION** (the rule does not
  preserve rule-structured families; report which partition
  degraded and the histogram-derived mechanism).
- K4 fails (K1-K3, K5 hold) -> **FAIL-PRESSURE** (eviction escaped
  the N set or exceeded the traced minimum, or pressure was not
  exercised).
- K1..K5 all hold -> **PORT-PASS-STRUCT**: the NT1 rule (ported as
  D1+D2) preserves rule-structured families with shared substructure
  under capacity pressure; fragility is isolated to addressing
  (NOADDR) and to the absence of lifetime memory (FRESH).

## 9. Honest boundaries (pre-declared)

- The LINKS are memorized associations; what is rule-STRUCTURED is
  the family: taught 2-hop chains with shared substructure, where a
  query answer requires composing two learned links. No rule
  INDUCTION is tested; no L2/L3 claim. The battery measures
  retention/revision/eviction dynamics over structured knowledge.
- Single capacity point (CAP=20, 1.2x); single contradiction
  magnitude; pressure-envelope scaling already covered by
  NT-PRESSURE (to 5x, memorized pairs).
- The port covers the continuing learner's associative instance
  memory only (NT-PORT boundary stands: contlearn2 schema machinery
  and H-CONTLIFE-1 hash-table memory remain unported).
- The eviction histogram is measurement-only; the checkpoint table
  and `ins` are learner state (own prior evidence / own installation
  order), containing no oracle/task information.
- Whether LIFO's tenure principle holds when novel links are NOT
  re-taught every pass remains the preregistered open boundary
  (NT-PORT honest boundaries); NOT tested here.
- NOADDR's 32-slot table vs PORT's 20-slot table: the arm
  difference under test is the address map (overlapping vs
  associative+d2), not capacity; NOADDR never fills its table, so
  capacity cannot explain its failure signature.

## 10. Amendment record (transparent; committed before implementation)

(none yet)
