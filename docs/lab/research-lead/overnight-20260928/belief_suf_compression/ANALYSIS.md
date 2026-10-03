# ANALYSIS: BELIEF-SUF-COMPRESSION

Worker: BELIEF-SUF-COMPRESSION subagent, 2026-10-03.
Lane: docs/lab/research-lead/overnight-20260928/belief_suf_compression/
Status: analysis per frozen PREREG.md (commit
1afbdfa44dcf4fcdc9e3e8483296276ba2c887cf).
Non-ledger task; nothing minted. No mechanism code modified
(verified: git status shows zero tracked-file modifications).
Style: hyphens only, no em/en dashes.

## 0. Verdict

**NON-DUP.** The belief layer and L3-SUF-1 resolution records do not
duplicate each other, and neither subsumes the other, under the frozen
criteria (PREREG.md sections 3-5). Each fails the other's home-turf
scenario for structural reasons, verified by a pure-Zag decision-logic
model (model/bsc.zag, 3/3 byte-identical, sha256
cdad30dd73e76f07389a7ee4f32a2667bb5ae68aac2fe840f263e83c03641c5c).
They are complementary epistemic mechanisms at different granularities
with different update algebras, different evidence inputs, different
dynamics, and different action vocabularies. No merge is recommended.
The honest partial overlaps are named in section 6; none licenses
merging the decision logic.

## 1. D1: record subjects differ in kind (DUP fails)

- Belief records attach to **claim-bearing nodes**: B-FACT (tag-1 fact
  nodes), B-STRUCT (tag-20 MAPs), B-COMP (MAP_Z composites), B-META
  (meta-rows). The record endorses a claim *about the world* that a
  structure carries: "(s, r, v) holds", "count MAP over (s, r) yields
  v". One record per node id; the subject is the structure's claim.
- SUF resolution records attach to **elements of the learner's own
  constructed form**: query elements (pairs / triples) of an
  intermediate the learner built. The record tracks falsification of
  the learner's own hypotheses *about its own representation*: "for
  element e, the values not yet falsified by my experience are {...}".
  The subject is interior to a structure, not a structure's claim.

Neither direction is lossless. Beliefs have no per-element-of-a-form
records: a MAP's interior (which of its elements are determined vs
fabricated) is invisible to R1-R7, which see only the MAP's claim,
its licensing set, and its run counters. SUF has no per-claim
endorsement records: it never adjudicates between two competing
structures, never weighs corroboration runs, never reads provenance
liveness. A "unified record" would need a subject-type flag
distinguishing claim-nodes from form-elements, which is two record
kinds sharing a table, not one mechanism.

## 2. D2: update algebras differ in kind (DUP fails)

- Belief updates are **accumulative and scalar**: R2 adds INC_HI/INC_LO
  with saturation at 255; R3 subtracts DEC with floor at 0; R4 scales
  proportionally with licensing liveness; R5 halves on revision; R6
  takes the min over type-14 successors (network propagation with
  fixpoint dynamics, per type-14 reachability component per BP-8);
  absorption is per-channel with saturation and order-sensitivity
  (BP-8: same-fact match+contradict nets 90/0/1 with R2-then-R3 order
  pinned; two type-7s collapse to one R2).
- SUF updates are **eliminative and set-theoretic**: per-element
  surviving-value sets shrink by falsification; the state IS the set
  (bitmask), not a scalar; l_surviving is a pure function of
  commutative-OR-accumulated consequence-log flags, permutation
  invariant (A-ORDER in the red-team report). No runs, no saturation,
  no propagation, no fixpoint, no channels. Evidence ingestion is
  order-independent boolean accumulation; belief ingestion is
  order-sensitive saturated channel absorption. Different ingestion
  semantics, not different parameters.

The steelman map (PREREG.md section 4) fails line by line:

- "RESOLVED(v) = high b_sup": a high-b_sup MAP can carry fabricated
  interior content (T-A below). RESOLVED is a per-element elimination
  verdict; b_sup is a per-claim accumulation verdict. Mapping
  popcount to a scalar loses the fabrication-blocking property, which
  is the whole point of the SUF record.
- "UNRESOLVED = low b_sup": low b_sup is a passive consequence that
  still permits selection (R7 picks argmax eff among candidates; a
  low-but-above-bar candidate commits). UNRESOLVED is an explicitly
  represented, audited state that (a) blocks a code path (no path
  from UNRESOLVED to a predicted value; fabrication impossible by
  construction), (b) drives probes (UNRESOLVED elements are probe
  targets), and (c) is the L3 invention content itself (first mark
  strictly after a committed-prediction REJECT, with rejected
  alternatives in the trace). A scalar cannot carry (a)-(c).
- "FALSIFIED-ALL = b_sup 0": the actions point in opposite
  directions. b_sup 0 retires the structure terminally (never
  selected again). FALSIFIED-ALL at form scale escalates: try
  ARITY-LIFT/GUARD/UNION/PROJECT in fixed order, adopt the first
  consistent composition. Termination vs hypothesis-space expansion.
  Verified divergent in the model (S-D).
- "form-scale sole-survivor = R7 argmax": sole-survivor is a
  unanimity/elimination criterion (adopt ONLY IF sole survivor;
  two survivors means no adoption, escalate or defer). R7 is a
  maximization criterion (pick the best-supported candidate even if
  several are viable). Different decision rules, different outcomes
  on the same candidate set.

## 3. D3: cross-failure tests (each fails the other's home turf)

T-A (RK-B world, belief-layer only). The learner induces a form;
evidentially unseen elements are tie-break-filled at full confidence.
The belief layer does NOT prevent the confident-wrong commit:
beliefs attach to the structure's claim as a whole; the fabrication
is interior to the endorsed claim; no TEST disconfirms it (R3 never
fires); no licensing fact dies (R4 never fires); d_self starts at 255
and moves only through experienced self-amplification failure, which
has not happened yet. R7 selects confidently. The kill the SUF
mechanism was built to prevent (RK-B: 0/6 fabrication) is invisible
to R1-R7. Model S-A: belief b_sup=130, R7 SELECT=1; SUF
UNRESOLVED, ABSTAIN=0; DIVERGE=1.

T-B (K3a/S1 world, SUF only). All type-1 licensing facts of a
composite's components are tombstoned; no TEST or stakes outcome
touches the composite's elements. SUF records do NOT degrade: the
consequence log records TESTs and stakes outcomes per element;
licensing-fact tombstones are not consequence-log events (the
red-team report confirms l_surviving is a pure function of
consequence-log flags). Surviving sets are unchanged; RESOLVED
elements keep predicting. The failure the belief layer was built to
prevent (K3a: dead composite still used, silently, wrong-relation)
is invisible to resolution records. Model S-B: belief b_sup=0,
retired, R7 abstain; SUF still RESOLVED(0), PREDICT=1; DIVERGE=1.

Both frozen predictions held (model BSC-RESULT=1, 3/3 byte-identical).
The sanity arm S-C shows the model is not rigged to diverge: with a
determined element and healthy licensing, both predict (AGREE=1).

## 4. D4: action vocabularies differ (DUP fails)

- Belief abstention (R7 -3): fires when max eff across peer
  candidates is below a learner-adjusted global bar. It is a
  *relative* gate over a *candidate set*.
- SUF abstention: fires *per element* on non-sole-survival
  (UNRESOLVED), per form on non-sole-survival (defer/escalate), and
  on kb-loaded forms lacking THIS-world evidence (DATA-UNTRUSTED
  deferral). It is an *absolute* gate on the prediction rule, plus a
  reuse gate with no belief analogue (a kb-loaded form with high
  historical b_sup would be R7-selected confidently; that is exactly
  the RK-C bug, 0/6).
- Belief retirement is terminal; SUF form-falsification escalates
  (section 2, S-D).
- Beliefs propagate weakening along the type-14 graph (R6, fixpoint);
  SUF has no propagation: marks are per-element independent, and
  "propagation" across scales is three separate applications of one
  principle, not message passing.
- SUF targets probes at UNRESOLVED elements (interventional action);
  beliefs have no probe-targeting action (selection only).

Triggers, directions, and dynamics all differ. DUP fails at D4.

## 5. Category argument: machinery vs invented structure

Beyond D1-D4, the two sit at different levels of the L-taxonomy, and
merging them would be a category error. The belief DESIGN.md is
explicit (section 6): the update rules R1-R7 are researcher-designed
generic machinery; what is learned is the belief CONTENT. The SUF
resolution record is the *learner-invented intermediate* under L3
test: even the form of the record (that UNRESOLVED needs explicit
representation) is the invention being adjudicated (SUF-KC0A/KC0B,
A-TRIGGER/A-SEARCH green in the red-team report). Folding SUF records
into the belief layer reclassifies the invention as machinery and
destroys the L3 claim under test. "SUF records are just beliefs" is
subsumption by redefinition: it would require adding per-element
subjects, eliminative updates, probe actions, and escalation to the
belief layer, at which point "belief" means "any learner-owned
record" and the subsumption is vacuous.

Related: beliefs are first-order epistemics (endorsement of claims
about the world); SUF records are second-order epistemics (the
learner's graded state about its own representation). The belief
design's core separation is structure-live vs learner-endorses; the
SUF design's is form-exists vs learner-knows-it-is-determined. Two
different separations.

## 6. Honest partial overlaps (PARTIAL, not DUP/SUB)

Three real commonalities, none licensing a merge:

P1. Shared design pattern: epistemic/endorsement state is
learner-owned and distinct from structural existence. This is the
belief design's central move (DESIGN.md section 2) and also SUF's
(form exists vs determined). It is a pattern, worth naming once in
architecture notes, not a duplicated mechanism.

P2. Abstention as a protocol message shape. Both mechanisms need a
"no commitment" output the harness handles (R7's -3; SUF's ABSTAIN,
which the prereg notes is a protocol message, not a learner mode).
The triggers differ (section 4); unifying the message shape is a
harness convention, not mechanism compression.

P3. The one credible partial compression: a shared
**evidence-ingestion substrate**. Both mechanisms read event streams:
beliefs read channel events plus provenance liveness (type-1 death,
type-14 structure); SUF reads per-element consequence taint (TESTs,
stakes outcomes). One ledger with both event kinds, read by two
independent decision logics, is conceivable. Against: the event
kinds are disjoint in practice (provenance liveness is not a
consequence; stakes outcomes are not licensing events), the
ingestion semantics differ (order-sensitive saturated channels vs
order-independent boolean accumulation), and both mechanisms are
mid-experiment with independent frozen test programs; merging
substrates now would tangle two sealed batteries for no decision
gain. Verdict: possible future substrate unification, not mechanism
duplication; not recommended now.

## 7. What genuine compression would require

Per the frozen criteria, a future claim that one mechanism subsumes
the other must demonstrate, not assert: (a) a lossless map covering
per-element subjects AND per-claim subjects; (b) one update algebra
that yields both accumulative runs with saturation AND eliminative
sets with fabrication-blocking; (c) decision coincidence on T-A and
T-B (each mechanism's home-turf kill must be prevented by the
unified mechanism); (d) preservation of the L3 test status of the
SUF record (the invention must remain attributable to the learner,
not absorbed into machinery). Nothing in the current evidence meets
(a)-(d).

## 8. Recommendation

Do NOT merge. Keep both mechanisms. For priority 10 (architecture
compression), this pair is a negative result: the compression
opportunity is elsewhere. The shared pattern (P1) should be named
once in architecture documentation so future mechanisms reuse the
pattern deliberately instead of rediscovering it. If substrate
pressure ever forces it, P3 is the only honest compression surface,
and it must preserve both decision logics and both test programs.

## 9. Provenance and governance

- Prereg commit: 1afbdfa44dcf4fcdc9e3e8483296276ba2c887cf
  (PREREG.md + NAMECHECK.md alone; no analysis artifact existed).
  PREREG.md section 9 anticipated filling commit hashes into the
  prereg; the hashes are recorded here instead so the frozen file
  stays byte-identical. Analysis commit hash to be filled at commit
  time below.
- Analysis commit: <filled at commit time>.
- Computational verification: model/bsc.zag (self-contained, pure
  Zag), model/build.sh; binary sha256
  8e88e64f6ff7cbf8cb88fce54094c385fbb0aed8ce568accb0f82a49497e27a5;
  rebuild identical; runs/run1-3.txt 3/3 byte-identical, sha256
  cdad30dd73e76f07389a7ee4f32a2667bb5ae68aac2fe840f263e83c03641c5c;
  all stdout bytes hand-verified against the documented rules
  (S-A 130/1/UNRESOLVED/abstain; S-B 0/retired/abstain vs
  RESOLVED(0)/predict; S-C agree; S-D retire-terminal vs escalate).
- Toolchain: safebin PATH throughout; `which python3`/`which python`
  empty at build and run; pinned znc 2026.07.0-dev; znc defect
  workarounds honored (sound alloc pattern, single output buffer +
  cursor emits, one _zag_raw_syscall, shallow if-nesting, no
  negated-conjunction while conditions, no unconfirmed bit ops).
- Read-only on belief_provenance*/, l3_suf_intermediate/,
  l3_suf_redteam/. Zero tracked files modified outside this lane.
- No em/en dash bytes in lane files (hyphens only).
- Non-ledger task: nothing minted.
