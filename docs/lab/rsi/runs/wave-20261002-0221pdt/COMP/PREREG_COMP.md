# PREREG_COMP: Composition comparative adversarial battery (COMP lane)

Wave: wave-20261002-0221pdt. Lane: COMP. Worker: subagent b5bfde8a.
Frozen: 2026-10-02 (this commit contains ONLY this file).
Status: FROZEN. Implementation must follow this spec exactly. Any design
change requires transparent amendment and re-freeze, never silent edit.

## Amendment A1 (pre-implementation, 2026-10-02)

D's candidate ordering changed from MAP-id order to longest-applicable-
prefix first (k0 from 4 down to 1; ties by MAP id; then gather order),
with full backtracking. Rationale: maximal-reuse bias is the general
principle (fewer segments = simpler composites); C already validates it
(cc_candidates orders by decreasing relseq length); without it D cannot
subsume C's composite-reuse behavior, which would make the subsumption
test unfair to the collapse thesis. D remains: no compose stage, no
compose flag, no rebind stage. Kill bars unchanged. Predictions updated:
D REUSE PASS via (MAP_Z, Y).

## 0. Question

Owner decision 2026-10-02: composition is a core TNN frontier. Three
mechanisms independently showed X+Y->Z composition:

- A: contract/plen chaining via compose_try (honestly L2 structural-reuse)
- B: co-use type-15 LINK edges written by episode success
- C: constraint-driven assembly from MAP relation sequences (DFS, 3-seg cap)

Owner ruling: do NOT permanently integrate three separate composition
engines. Determine whether one mechanism subsumes the others or their
principles collapse into ONE general composition operation. The final
learner must not need COMPOSE_MODE; composition should arise because
existing structures satisfy parts of a new goal.

Prior work (same day, composition_compare/REPORT.md): C subsumes A/B on
arity (C handles 3 structures, A/B are pair-bound); collapse proposed via
C's DFS with pluggable applicability; all three FAIL partial
applicability (atomic MAP assumption) and unsupervised composition
(expected-answer required). This battery goes further: different domains,
revision/reuse of composites, adversarial subsumption-breakers, and a new
candidate single operation D with no compose flag or stage.

## 1. Mechanisms under test

Binaries (each = frozen TNN-2 substrate + one mechanism + shared driver):

- bin A: cmp_full_a.zag lines 1-1859 verbatim (SHA
  fbb4e80d32e8a1d210fd2b4cd985c759717843fa28b85b01ff1abffe3c6b7275),
  plus new adversarial driver. A = plen-contract pair search.
- bin B: cmp_full_b.zag lines 1-1865 verbatim (SHA
  5729296d8d79dbfb4dd7f597fb0bd60a8a06a03322d5baeeac38cecc0b4ce0c5),
  plus driver with co-use episodes. B = type-15 co-use pair staging.
- bin C: cmp_full_c.zag lines 1-1985 verbatim (SHA
  a6845b9e83398c683d105ecdabf23efce0f65c4f5306a8acd1d74b56f02d3f0f),
  plus driver. C = constraint DFS, researcher 3-segment cap.
- bin C0: bin C with exactly one line changed: compose_on() returns 0.
  Mode-flag control: proves whether C's composition depends on the
  flagged compose_try stage.
- bin D (NEW, this wave): frozen substrate lines 1-1677 of cmp_full_c
  (base SHA 0e2cafe2e61952f3a715732adb2a8bdfdf5c3a2a9f4d331d576df8a24acb0ccd
  + shared rebind base) + new patch_d implementing ONE general operation
  `satisfy`, plus driver. NO compose_try, NO compose flag, NO rebind_try
  in D's pipeline.

### 1.1 D design (frozen)

`satisfy` = recursive goal-part satisfaction. It is the single miss path
in D's ev_query: activate -> satisfy -> trial(mp_run) -> bootstrap.

- Applicability: MAP m is applicable from value s at prefix length k iff
  m's relation sequence R[0..k) (extracted structurally, same function as
  C's cc_relseq) matches the relations of a live-fact path from s
  (enumerated via t2_gather, ALL groundings, not just first).
- Selection: for each live MAP (id order), k from full length down to 1,
  every grounding. First success in DFS order wins; full backtracking
  across MAPs, prefix lengths, and groundings.
  (A1: longest-applicable-prefix first: k0 from 4 down to 1 outer loop,
  then MAP id order, then grounding order; full backtracking.)
- Supervised (expected >= 0): apply grounding, terminal vt; if vt ==
  expected, record segment; else recurse satisfy(vt) with visited-set
  cycle guard; on unwind assemble segments (t2_asm_chain per segment,
  SEQ-link), sanity-execute, verify vs expected, promote as one MAP with
  LINK14 provenance to used MAPs. Depth bound = learner policy header
  (pol_get, default 8 if unset); visited values block cycles (principled
  termination independent of the bound).
- Unsupervised (expected < 0): greedy fixpoint. Repeatedly apply the
  longest applicable prefix whose terminal value is novel; stop at
  fixpoint (no novel progress) or 12 iterations. Assemble, sanity-execute,
  promote with actual terminal. No expected value is ever consulted.
- Single-structure queries are handled by the SAME operation (one
  applicable segment reaching the goal); there is no separate rebind
  stage and no compose stage. This is the no-COMPOSE_MODE realization:
  composition is what goal-part satisfaction does when one structure is
  not enough.

D differs from C behaviorally in exactly three frozen ways: (1) prefix
application (partial structure satisfaction), (2) multi-grounding with
backtracking (vs t2_lu_first single grounding), (3) unsupervised fixpoint
(vs immediate -2). No segment-count cap (policy bound 8 + cycle guard).

## 2. Domains (structurally different, not relabelings)

- D1 ARITH: linear increment chains, distinct rel per component.
- D2 BRANCH: nodes with multiple outgoing same-rel edges (distractors).
- D3 HOPS: atomic single-hop MAPs (finest-grained composition).
- D4 NOISE: D1 world plus 40 distractor facts sharing Z subjects/rels
  (dead-end values 9100+), taught AFTER Z facts.

Training pattern (all tests): ev_teach component facts; query each
component on a novel relation (71, 72, ...) which promotes one MAP per
component via trial; 30 gap-noise facts (5000+i, 60+(i%10), 6000+i);
teach goal facts; query goal on novel relation 70. The driver never names
which MAPs to use. expected = the query protocol target (post-hoc
feedback per the frozen E-ruling), NOT paired X+Y->Z supervision; the
NOSUP test removes even that.

## 3. Test battery (frozen thresholds)

Notation: q(s,r,exp) = ev_query. PASS/FAIL per test is mechanical.

- COMP3 (D1): X=[1,1] (11-12-13), Y=[2,2] (21-22-23), W=[3,3,3]
  (31-32-33-34). Z: 101-1->102-1->103-2->104-2->105-3->106-3->107-3->108.
  q(101,70,108). PASS iff ans==108.
- COMP5 (D1b): X,Y,W as above + V=[4,4] (41-42-43) + U=[5,5] (51-52-53).
  Z5: 101..111, r1x2 r2x2 r3x2 r4x2 r5x2 (10 steps). q(101,70,111).
  PASS iff ans==111. (Tests morning open Q4: C's 3-cap removed in D.)
- COMP2 (canonical 2-structure): X=[1,1], Y=[2,2]. Z2:
  101-1->102-1->103-2->104-2->105. q(101,70,105). PASS iff ans==105.
  B runs co-use episodes first (fresh chains 61-62-63 r1, 63-64-65 r2
  via ev_cq chain=0/1, morning pattern); driver emits couse15 count.
- B-ABL (B only): COMP2 setup, then cb_del_couse() before the goal
  query. PASS iff ans==105. Predicted FAIL; proves B's composition is
  caused by co-use history.
- D2-COMP: X=[1,1] with distractor (12,1,912) taught FIRST (dead end);
  Y=[2,2] with distractor (22,2,922) first. Z:
  101-1->102-1->103-2->104-2->105 (correct facts first).
  q(101,70,105). PASS iff ans==105.
- D3-COMP3h: atomic X=[1] (11-12), Y=[2] (21-22), W=[3] (31-32). Z:
  101-1->102-2->103-3->104. q(101,70,104). PASS iff ans==104.
- D4-COMP: COMP3 setup + 40 distractors (101+(i%8), 1+(i%3), 9100+i)
  taught after Z facts. q(101,70,108). PASS iff ans==108.
- PART (partial applicability): X=[1,1,1,1] plen 5 (11..15);
  Y=[2] (21-22). Z: 101-1->102-1->103-2->104 (needs 2 of X's 4 steps).
  q(101,70,104). PASS iff ans==104 AND the promoted composite's
  extracted relseq == [1,1,2] (proves prefix use, not whole-X).
  No dedicated glue path is provided; the mechanism must use part of X.
- NOSUP (no expected-answer supervision): COMP3 setup. q(101,70,-1).
  PASS iff a composite MAP for (101,70) is promoted AND its extracted
  relseq == [1,1,2,2,3,3,3] in order AND its 7 step values equal the
  taught Z values 101..108 AND terminal == 108. (Experimenter-verified;
  the mechanism sees no target.)
- REV (revision of composite): X=[1,1], Y=[2,2]; Z:
  101-1->102-1->103-2->104-2->105; q(101,70,105) -> MAP_Z.
  R1: MAP count +1 (composite exists). R2: q(101,70,105) again ->
  ans==105 (first-class direct reuse via activate). R3:
  ev_observe(104,2,99) contradicts a licensing fact of MAP_Z.
  R4: q(101,70,99). PASS iff R1 and R2 hold and R4 ans==99
  (stale=105, absent=-2). Tests: composite is first-class, survives
  contradiction via the generic revision operator, stays usable.
- REUSE (composite as component): X=[1,1], Y=[2,2]; compose Z as in
  REV (101..105, rel 70) -> MAP_Z relseq [1,1,2,2]. Q:
  301-1->302-1->303-2->304-2->305-2->306-2->307. q(301,70,307).
  PASS iff ans==307 AND the new composite has a provenance edge
  (type 1, 14, or 15) to MAP_Z. B gets only its standard atomic-pair
  episodes (no episode can co-use the composite; predicted B FAIL,
  informative about history-gating).
- ADV-A (adversarial A-win attempt): X=[1,1] clean; Y=[2,2] clean; Z:
  distractor (103,2,904) taught FIRST, then (904,2,905), then correct
  101-1->102-1->103, (103,2,104), (104,2,105). t2_lu_first(103,2)
  returns the distractor branch. q(101,70,105). PASS iff ans==105.
  If A passes and C/D fail, A's exhaustive grounding search is a unique
  capability and collapse is refuted on that axis.
- SINGLE (one-operation control): X=[1,1] trained (11-12-13, rel 71).
  Fresh: 61-1->62-1->63. q(61,71,63). PASS iff ans==63. For D this must
  go through satisfy (no rebind stage exists in D).
- C0-COMP3: bin C0 on COMP3 setup. Predicted ans==-2 (FAIL). Proves C's
  composition depends on the flagged compose_try stage.

Per-binary test lists: A: all except C0, B-ABL (12). B: all except C0
(13, incl B-ABL). C: all except C0, B-ABL (12). C0: C0-COMP3 only.
D: all except C0, B-ABL (12).

## 4. Frozen kill bars

- KB1 determinism: each of the 5 binaries is run 3 times; stdout must be
  byte-identical across the 3 runs (sha256 equal). Any mismatch voids
  that binary's results for the wave.
- KB2 subsumption: D passes every (domain,test) that C passes; D passes
  every test that A passes; D passes every test that B passes. Failure on
  any axis is reported as the specific axis (no averaging).
- KB3 strict extension: D passes at least 2 tests that C fails
  (predicted: PART, NOSUP; also COMP5, D3-COMP3h where C's cap binds).
- KB4 no-COMPOSE_MODE: (a) D's patch contains zero code occurrences of
  "compose" (comments explaining the absence allowed; verified by grep);
  D's ev_query pipeline is exactly activate -> satisfy -> trial ->
  bootstrap with no flag, no mode, no separate compose stage.
  (b) C0 fails COMP3 (ans==-2), proving C-as-built is flag-dependent.
- KB5 architecture accounting: zero new modes, zero new bridges, zero
  new handlers, zero new semantic cases, zero new opcodes; ISA unchanged
  (4 ops: 101-104); no new MAP/edge types (D uses LINK14 provenance,
  already in use by B/C). Report: cognition lines added (patch_d code
  lines; driver/shim/assembly counted separately as harness, not
  cognition), verified by line counts and grep.
- KB6 battery validity (all must hold, else BUILD-FAIL for the affected
  comparison): B passes COMP2 (canonical B works; couse15>=1 emitted);
  B-ABL fails (history is causal for B); C passes COMP3 (canonical C
  works); A passes COMP2 (canonical A works); D passes SINGLE (satisfy
  covers the one-structure case).
- KB7 collapse decision: COLLAPSE-SUPPORTED iff KB1-KB6 hold and no
  mechanism shows a test where it passes and D fails. If A or B passes
  any test D fails -> COLLAPSE-REFUTED on that axis, naming the
  indispensable signal (e.g. exhaustive grounding, co-use history).
  Either outcome is reported; the verdict line is BUILD-PASS/BUILD-FAIL
  only (build = battery built and run per this prereg), never SURVIVES.

Predictions (not kill bars; recorded to check calibration, never to move
bars): A: COMP2 PASS, D2 PASS, ADV-A PASS, PART FAIL, NOSUP FAIL, rest
pair-bound FAIL, REUSE PASS, REV PASS, SINGLE PASS. B: COMP2 PASS, B-ABL
FAIL, others FAIL (pair-bound), REV PASS, REUSE FAIL, SINGLE PASS.
C: COMP3/COMP2/D2/D4/REV/REUSE/SINGLE PASS; COMP5/D3h/PART/NOSUP/ADV-A
FAIL. C0: FAIL. D: all 12 PASS.

## 5. Implementation constraints (frozen)

- Pure Zag only. Safebin PATH. No Python. Forbidden executable =
  automatic PROCESS-FAIL with immediate disclosure.
- Substrate frozen: base SHA
  0e2cafe2e61952f3a715732adb2a8bdfdf5c3a2a9f4d331d576df8a24acb0ccd;
  mechanism code for A/B/C reused verbatim from the morning's tested
  artifacts (cmp_full SHAs in section 1). No edits to substrate logic.
- Lane writes only under docs/lab/rsi/runs/wave-20261002-0221pdt/COMP/.
  Commits: this prereg ALONE first; implementation second (explicit
  pathspec, never git add -A, never push).
- Bug fixes allowed only if they do not change this design or these
  bars; any design change = transparent amendment + re-freeze.
- Loop docs: hyphens only (no em/en dashes); check_no_dash.sh before
  each commit.

## 6. Deliverables

NAMECHECK.md (Step 0 done), this PREREG_COMP.md (frozen alone),
implementation (patch_d.zag, shims, driver.zag, asm.sh), COMPARATIVE_EVAL.md
(full matrix + numbers), REDTEAM_SELF.md (is D just C renamed? does PART
smuggle researcher glue? is the collapse claim circular?), VERDICT line
(BUILD-PASS/BUILD-FAIL only).
