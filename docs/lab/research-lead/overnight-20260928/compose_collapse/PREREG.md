# PREREG: H1+H2 Collapse -- Do Typed Contracts and Value Composition Reduce to One Operation?

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Step 0) strictly precedes all implementation.

## 1. Question

H1 (learned typed contracts) and H2 (value-level function composition) both solve
4 structurally different cross-domain pairs with unmodified logic
(`composition_canonical/CONSOLIDATION.md`, commit `8ed0b7c06`).
Micah's standing direction: determine by comparative/adversarial experiment whether
one mechanism subsumes the other or their principles collapse into ONE general
composition operation, with no COMPOSE_MODE and no researcher mode flag.

## 2. Mechanism sketches (from the canonical record)

H1: per-MAP type signatures learned from probe_kind observations
(NODE = appears as a fact subject, else NUM), finalized by majority at n>=2.
Composer admits single A iff sig(A).in==kin and sig(A).out==kout; admits pair
(A,B) iff sig(A).in==kin, sig(A).out==sig(B).in, sig(B).out==kout. Execute, verify.

H2: ordered class-pair trial execution. Stage 1 executes class c1 on the subject,
producing an intermediate VALUE observed in the trace; stage 2 executes class c2
on the intermediate; success iff the pipeline result equals expected. Classes are
researcher-defined (WALK, COUNT, MAYBE, IDENT); the working pair is discovered.

## 3. Candidate unified operation U (frozen)

Behavior-contract composition. Each MAP carries a CONTRACT: the SET of observed
(input-kind, output-kind) pairs from its teaching executions, stored as kind-set
bitmasks (bit0=NODE, bit1=NUM). One admission rule, always active, no mode flag:

- Single A admitted iff kin is compatible with A.inmask and kout with A.outmask.
- Pair (A,B), A!=B, admitted iff kin compatible with A.inmask, A.outmask
  INTERSECTS B.inmask (nonempty), and kout compatible with B.outmask.
- Compatibility: an EMPTY kind-set (no observations) is compatible with every
  kind; otherwise the kind bit must be present.
- Execution rule: try admitted singles in MAP-id order, then admitted pairs in
  (a,b) id order; each trial executes and verifies end-to-end. Intermediate
  values are logged (H2-style trace).
- WIDENING (frozen part of the single rule): if every admitted candidate fails,
  the composer retries the filter-REJECTED ordered pairs in (a,b) id order,
  exactly once per query, and logs WIDEN=1. Triggered solely by learner-observed
  exhaustive failure, not by any researcher flag.

Reduction claims (frozen):
- R1: Restricting U's kind-sets to majority singletons (finalize at n>=2, no
  unobserved-fallback, no widening) yields EXACTLY H1's admission and behavior.
  Implemented as the faithful H1 arm; the uc_uni.zag vs uc_h1.zag source delta
  is exactly the admission rule.
- R2: Deleting U's kind filter (admit everything) yields EXACTLY H2's admission
  and behavior (trial execution over ordered pairs). Implemented as the
  UNI-NOKIND arm, a one-line ablation of uc_uni.zag.

## 4. Operational definition of "collapse into one operation" (frozen)

H1 and H2 collapse into one operation iff ALL of the following hold:
(a) U's source contains no flag, mode, or branch selecting H1-like vs H2-like
    behavior; one admission rule and one execution rule are always active.
(b) The H1 arm (R1 restriction) reproduces H1's exact answer-and-try profile on
    every problem below.
(c) The UNI-NOKIND arm (R2 restriction) reproduces H2's exact answer-and-try
    profile on every problem below.
(d) U with both subcomponents passes all five problems, including the
    discriminators where the learned contract misleads (P2b, via widening) and
    the contract-growth problem (P5).

Verdict mapping (frozen):
- (a)-(d) all hold: SUBSUMPTION. H1 and H2 are restrictions of one
  behavior-contract composition operation. H1 = contract as static kind summary
  (cheap admission); H2 = contract as dynamic execution (discovery + fallback).
- (b) holds but (c) fails, or U fails P2b: GENUINE DISTINCTION. The boundary is
  then stated as the contract-coverage condition (Section 7), a
  learner-discoverable condition, not a researcher mode.
- Build failure or nondeterminism: UNDECIDED, with the decisive experiment named.

## 5. Discriminating problems (frozen worlds)

Shared: kinds 1=NODE (value appears as a fact subject) else 2=NUM. Behaviors are
installed as previously-learned MAPs (behavior induction is not under test;
signature/contract learning and composition are). Teaching = recording kind
observations from successful teaching executions only. One candidate TRIAL =
one single-MAP execution or one ordered-pair pipeline execution. 3/3
byte-identical runs per arm.

P1 MIXED-KIND (H1-fail / H2-pass predicted; tests majority-vote freezing).
Facts: (31,81,32),(32,81,33),(33,81,34),(34,82,101),(34,82,102);
(51,81,52),(52,81,53),(53,82,111),(53,82,112),(53,82,113);
(41,81,42),(42,81,43); (63,83,64),(64,83,65); (73,83,74),(74,83,75);
(43,84,1),(65,84,1),(75,84,1); sealed (61,81,62),(62,81,63).
MAPs: X=MAYBE(81,82) id0 (walk r81 to endpoint; if endpoint has r82 facts return
their count else return the endpoint); Y=WALK(83) id1.
Teaching: X: 31->2 (NUM), 51->3 (NUM), 41->43 (NODE). Majority out=NUM,
sig(X)=NODE->NUM. Y: 63->65 (NODE), 73->75 (NODE). sig(Y)=NODE->NODE.
Sealed Z=(61,93)->65. kin=1, kout=1.
Correct: X(61)=63 (NODE, minority kind), Y(63)=65.
Predictions: H1: pair (X,Y) rejected (NUM!=NODE); Y-alone admitted, fails.
ANS=-2 TRIES=1. H2: (MAYBE,WALK) trial 1. ANS=65 TRIES=1 INTER=63.
UNI: kind-sets X in{1} out{1,2}, Y in{1} out{1}: singles X fail, Y fail,
pair (X,Y) admitted via set intersection. ANS=65 TRIES=3 INTER=63.
NOKIND: ANS=65 TRIES=3 INTER=63.

P2a SINGLE-SHOT REPRESENTATIVE (H1-fail / H2-pass; tests the n>=2 rule).
Facts: teach (31,81,32),(32,81,33),(33,81,34),(34,82,101),(34,82,102);
sealed (41,81,42),(42,81,43),(43,81,44),(44,82,45),(45,82,46).
MAPs: X=WALK(81) id0, Y=COUNT(82) id1, D1=IDENT id2, D2=COUNT(81) id3.
Teaching (ONE observation each, kind-representative: X 31->34 NODE,
Y 34->2, D1 31->31, D2 31->1).
Sealed Z=(41,93)->2. kin=1, kout=2.
Predictions: H1: no finalized signatures (n=1<2). ANS=-2 TRIES=0.
H2: (WALK,COUNT) trial 1. ANS=2 TRIES=1 INTER=44.
UNI: singles Y fail, D2 fail; pair (X,Y) admitted. ANS=2 TRIES=3 INTER=44.
NOKIND: 4 singles + (X,Y). ANS=2 TRIES=5 INTER=44.

P2b SINGLE-SHOT NON-REPRESENTATIVE (H1-fail / H2-pass / UNI-via-widening;
tests contract coverage; the sharpest discriminator).
Facts: teach (11,81,12),(12,81,13),(13,81,14); (70,82,71),(70,82,72);
(31,81,32); sealed (41,81,42),(42,81,43),(43,81,44),(44,82,45),(45,82,46).
MAPs: X=WALK(81) id0, Y=COUNT(82) id1, D1=IDENT id2, D2=COUNT(81) id3.
Teaching (one each): X 11->14 (out NUM, not kind-representative of the sealed
intermediate 44/NODE), Y 70->2, D1 31->31, D2 31->1.
Sealed Z=(41,93)->2. kin=1, kout=2.
Predictions: H1: ANS=-2 TRIES=0. H2: ANS=2 TRIES=1 INTER=44.
UNI: admitted singles X,Y,D2 fail (3); admitted pairs (D1,X),(D1,Y),(D1,D2)
fail (3); WIDEN=1; rejected pair (X,Y) succeeds. ANS=2 TRIES=7 INTER=44.
NOKIND: ANS=2 TRIES=5 INTER=44.

P3 CANONICAL REPLAY (positive collapse: one implementation reproduces H1's
admission profile AND H2's execution trace with no mode switch).
Facts: teach (11,81,12),(12,81,13),(13,81,14),(14,82,141);
(15,81,16),(16,81,17),(17,81,18),(18,82,181),(18,82,182);
(50,82,51),(51,82,52),(52,82,53); (60,82,61),(61,82,62),(62,82,63),(63,82,64);
(21,81,22); sealed (31,81,32),(32,81,33),(33,81,34),(34,82,35),(35,82,36).
MAPs: X=WALK(81) id0, Y=COUNT(82) id1, D1=IDENT id2, D2=COUNT(81) id3.
Teaching (n=2 each): X 11->14, 15->18 (1->1); Y 50->3, 60->4 (1->2);
D1 21->21, 21->21 (1->1); D2 11->1, 15->1 (1->2).
Sealed Z=(31,93)->2. kin=1, kout=2.
Predictions: H1: Y fail, D2 fail, (X,Y) success. ANS=2 TRIES=3.
H2: (WALK,COUNT) trial 1. ANS=2 TRIES=1 INTER=34.
UNI: same admission as H1 (all kind-sets singleton). ANS=2 TRIES=3 INTER=34.
NOKIND: 4 singles + (X,Y). ANS=2 TRIES=5 INTER=34.

P5 CONTRACT GROWTH (UNI only; L2 connection: the contract is learner-owned
state that adapts admission from experience, no researcher mode).
Continue the P2b arena after Z is solved. Add facts
(51,81,52),(52,81,53),(53,82,54),(53,82,55),(53,82,56).
Sealed Z2=(51,93)->3. kin=1, kout=2.
Prediction: X.outmask is now {1,2} (observations 11->14 NUM and 41->44 NODE),
so pair (X,Y) is admitted WITHOUT widening. ANS=3 TRIES=4 INTER=53.
Census lines: CENSUS m=0 inmask=1 outmask=3 n=2; m=1 inmask=1 outmask=2 n=2;
m=2 inmask=1 outmask=1 n=1; m=3 inmask=1 outmask=2 n=2.
Z1 TRIES (7) > Z2 TRIES (4): the same mechanism exhibits H2-like discovery on
first contact and H1-like pruning after its contract grows.

## 6. Frozen kill bars

- K1 P1: H1 (-2,1); H2 (65,1)+INTER=63; UNI (65,3)+INTER=63;
  NOKIND (65,3)+INTER=63. 3/3 each.
- K2 P2a: H1 (-2,0); H2 (2,1)+INTER=44; UNI (2,3)+INTER=44;
  NOKIND (2,5)+INTER=44. 3/3 each.
- K3 P2b: H1 (-2,0); H2 (2,1)+INTER=44; UNI (2,7)+INTER=44+WIDEN=1;
  NOKIND (2,5)+INTER=44. 3/3 each.
- K4 P3: H1 (2,3); H2 (2,1)+INTER=34; UNI (2,3)+INTER=34;
  NOKIND (2,5)+INTER=34. 3/3 each.
- K5 P5: UNI (3,4)+INTER=53; census lines exactly as in Section 5;
  Z1 TRIES=7 > Z2 TRIES=4. 3/3.
- K6 DETERMINISM: every arm 3/3 byte-identical; sha256 digests recorded.
- K7 NO-MODE AUDIT: uc_uni.zag contains no flag/mode/branch selecting H1-like
  vs H2-like behavior. Admission is one rule (kind-set compatibility +
  failure-triggered widening). The H2 arm's behavior classes are
  researcher-defined (declared honest boundary, as in canonical H2); the
  working class pair is discovered, never given.
- K8 HYGIENE: zero em/en dash bytes in all docs; safebin toolchain guard
  attested in NAMECHECK.md Step 0; pure Zag for all scientific computation.

## 7. Predicted boundary if distinction verdict

If U fails P2b (no widening path) the boundary is: H1/H2 collapse only under
CONTRACT COVERAGE (every instance kind the composition actually exercises was
observed during teaching). Coverage is learner-discoverable: after executing
stage 1, the learner observes the intermediate kind and can test membership in
the contract sets; systematic coverage failures are observable in the trace.
The decisive next experiment would then be a coverage-triggered admission
widening (drop the filter when contract-admitted candidates exhaust), which is
exactly the frozen WIDENING rule; its success or failure on P2b decides full
vs partial collapse.

## 8. Honest boundaries (pre-declared)

- Behaviors (WALK/COUNT/MAYBE/IDENT) are installed as previously-learned MAPs;
  behavior induction is not under test (same standing as canonical H1).
- Expected answers verify final acceptance (canonical boundary, all four pairs).
- H2 arm's behavior classes are researcher-defined; the pair is discovered.
- P2a uses kind-representative single observations; the contract's coverage
  precondition is stated, not smuggled (P2b tests its violation).
- Chain/star fact geometries only; the planning-composition frontier
  (SUM to PLAN) is out of scope.

## 9. Implementation plan (frozen order)

1. uc_base.zag: output buffer + cursor helpers + single raw-syscall flush;
   arena; fact store; probe_kind; walk/count/maybe/ident; MAP table;
   observe/teach; world setups P1/P2a/P2b/P3/P5-extra.
2. Arm files (each: base + composer + main): uc_h1.zag, uc_h2.zag, uc_uni.zag.
   uc_nokind.zag generated from uc_uni.zag by one-line sed
   (kind_filter_on return 1 -> 0); diff verified to be exactly that line.
3. Assemble with cat, compile with the pinned znc, run 3x each, record sha256.
4. REPORT.md with verdict per Section 4 mapping.

Zag pitfalls observed: no `as *i32` + slice construction in functions (use the
[]u8 z_alloc pattern); no _zag_print for dynamic content (single preallocated
buffer, cursor helpers, one _zag_raw_syscall flush; verify stdout bytes);
`as []f64`/`as []i64` len not rescaled (not used); if-nesting kept at most 3
(pair-trial logic hoisted into helpers); no `!(A && B)` in while conditions;
no WAV I/O in this task.
