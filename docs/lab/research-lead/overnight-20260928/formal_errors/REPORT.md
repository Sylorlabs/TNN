# REPORT: Formal Errors and Constraint Understanding

## Verdict: FORMAL-ERRORS-COMPLETE

## Question

Constitution Sections 7 and 27: if TNN genuinely understands a formal
system, that understanding should constrain behavior. Errors that should
become impossible once relevant understanding is complete must be
identified, and their architectural cause found (not excused as
"intelligence sometimes makes mistakes").

## Method

Three formal constraints, each with: (a) a teaching phase demonstrating
mastery, (b) a test phase counting formal errors, (c) a causal treatment
that consults learner-state knowledge the base ignores. Control = frozen
TNN-2 base. Treatment = base plus three patches (redefined `t2_trial`
for F1/F2, redefined `t2_exec` for F3). 3/3 byte-identical runs per arm.

## F1: Relation purity of sums (type constraint)

World rule: r=72 answers are sums of r=70 facts only. r=71 facts are
distractors that never belong in a correct sum.

Teaching (expected-based trial, 4 subjects): 4/4 correct. Each trial
rejected 4 mixed sums before accepting the pure sum. The learner
experienced 16 mixed-sum rejections. All 4 promoted MAPs used r=70
facts only (DEP provenance in learner state).

Test (masked trial, 4 new subjects):

| | Control | Treatment |
|---|---|---|
| Promoted answer | 25 (mixed) | 15 (pure) |
| Mixed-relation DEP facts | 1 | 0 |
| Formal errors | 4/4 | 0/4 |
| Teaching rejects per subject | 4,4,4,4 | 4,0,0,0 |

The control promotes a sum containing an r=71 fact despite 16 prior
rejections of mixed sums. The treatment filters sum facts to relations
licensed by the learner's own prior MAPs for r=72 (DEP provenance);
after the first teaching subject it proposes zero mixed sums.

Cause: `t2_gather_sum` is relation-blind by construction. The constraint
is present in learner state (MAP provenance) but the generator has no
path to consult it. Consequences do not re-enter generation.

## F2: Structural form consistency

World rule: r=60 is single-hop. Answers come from single facts, never
sums.

Teaching (expected-based, 10 subjects, no comb): 10/10 correct. All 10
promoted MAPs are 2-cell single-hop graphs (verified by cell walk).

Test (masked trial, 4 new subjects with 3 facts each, comb enabled):

| | Control | Treatment |
|---|---|---|
| Promoted form | sum graph (66-75 cells) | single-hop (2 cells) |
| Promoted answer | 66,69,72,75 | 21,22,23,24 |
| Formal errors | 4/4 | 0/4 |
| Contradictions on observe | 4/4 | 0/4 |
| Teaching rejects per subject | 1 (x10) | 1,0,0,... |

The control tries sums before single hops (fixed order) and masked
acceptance promotes the sum, violating the relation's established form.
Later observation contradicts all 4 (proving wrong answers). The
treatment tries single hops first when the learner's MAPs for r are
majority single-hop; rejects drop to zero after the first subject.

Cause: fixed candidate order ignores the relation's form knowledge in
learner state. The learner knows r=60 is single-hop (10 MAPs) but the
generator does not consult this.

## F3: Referential integrity under eviction

Teaching: 4-link chain MAP promoted for (1,50). Mastery: 10/10
re-executions correct.

Pressure: 1100 unrelated teaches (forces evictions).

Audit (both arms): 8/8 literal nodes dead or repurposed. The verified
executable MAP was structurally destroyed by referentially-blind
eviction.

| | Control | Treatment |
|---|---|---|
| Literals destroyed | 8/8 | 8/8 |
| Integrity check before exec | none | FE-INTEGRITY-REFUSE |
| Re-execution result | -999999 (fails during exec) | -999999 (refused pre-exec) |

The control attempts execution on the corrupted graph and fails
mid-execution. The treatment's integrity walk (using learner-state
liveness flags) detects the corruption and refuses before executing.

Cause: `evict_node` deletes nodes without fixing references;
`execute` has no structural-integrity precondition. A guard cell whose
literal was evicted reads stale or repurposed memory. The liveness
information needed to detect this is in learner state but never
consulted before execution.

## Standing metrics

- RESEARCHER-OWNED: the three world rules, patch logic (relation
  filter, form-ordered search, integrity walk), audit helpers.
- LEARNER-OWNED: all MAPs, their DEP provenance (which determines the
  F1 filter), their cell counts (which determine the F2 ordering), all
  answers, all liveness flags.
- The patches do not learn the constraints. They consult learner-state
  knowledge the base ignores. The finding is architectural: the base
  has no path by which this knowledge constrains generation,
  search order, or execution.
- COGNITION LINES: patch ~200, audit ~120, driver ~130.
- MODES/BRIDGES/HANDLERS/SEMANTIC CASES: 0/0/0/0.

## Architectural gaps (causes, not excuses)

1. Consequences do not re-enter generation. 16 rejections of mixed
   sums leave the generator unchanged (F1).
2. Search order does not adapt to learned form knowledge. 10
   single-hop precedents do not reorder the trial (F2).
3. No referential integrity invariant. Eviction silently destroys
   verified executable structure; execution does not validate (F3).

## Performance note (Section 17 relevance)

Rejected sum candidates leave dead cells and edges. `seq_nx` scans
all 4096 edge slots per cell per execution step. Dead-candidate
accumulation makes later trials superlinearly slower (subject 0: fast;
subject 2: 46s CPU for one trial). This is a scaling hazard independent
of the formal-error findings.

## Limits

- The three world rules are researcher-defined. The learner induces
  them from examples; it is not told the rules.
- The treatments are researcher-authored consultations of
  learner-owned knowledge, not learner-discovered consultations.
  Whether TNN can learn to consult its own provenance is open.
- F3's corruption was total (8/8). Partial corruption (wrong silent
  answers vs loud failure) was not separately measured.
- Chain family and sum family only. No test of invented constraints.

## Deliverables

- `fe_base.zag`: byte-identical copy of frozen base (cmp-verified).
- `fe_audit.zag`: read-only audit helpers (both arms).
- `fe_patch.zag`: treatment redefinitions (treatment arm only).
- `fe_driver.zag`: three-phase experiment driver.
- `fe_build.sh`: assembly script (strips redefined base functions).
- `fe_full_ctl.zag`, `fe_full_trt.zag`: assembled sources.
- `fe_ctl_bin`, `fe_trt_bin`: compiled binaries.
- `fe_ctl_run1/2/3.txt`, `fe_trt_run1/2/3.txt`: 3/3 byte-identical runs.
  - Control SHA-256: `a51cada35d25677a6ebd40b7bee6bfd4df46d4d4ab36ca6ee82b9706931eb979`
  - Treatment SHA-256: `71caac7992118634882a41d44a0f5d9f22f3d7bdb8a241e6780fff6b991d4095`
