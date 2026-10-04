# Comparison Protocol: CLA-1 vs contlearn2

Date: 2026-09-30. Worker: Architecture Comparison Protocol Designer.
Status: PROTOCOL-FROZEN (design only; no implementation, no runs).
Verdict label target: ARCH-COMPARISON-PROTOCOL-COMPLETE.

## 1. Purpose and authority

Micah's ruling: run CLA-1 and contlearn2 as temporary competing
architectures, compare them on seven dimensions (capability; source
delta; number of state formats; number of handlers/modes/bridges;
transfer; freeze-challenge performance; ability to create new
capability without source edits), prefer the architecture producing
MORE capability from LESS researcher-authored machinery, then converge
on one direction.

This document is the frozen prereg for that comparison. Execution
workers implement and run under separate preregs that cite this
protocol; no bar in this document may be altered after results are
seen. Any amendment is committed transparently and re-frozen before
the affected phase runs.

The two competitors:

- **CLA-1**: prereg `b4f61ff8a`, file
  `continuing_learner/PREREG_CLA1.md`. PRIMARY architecture.
  One node store plus typed edges, six generic primitives, one
  learner-owned structural workspace, one generic event stream
  (TEACH/QUERY/ACT/OBSERVE), zero semantic cases/modes/bridges
  by design. Implementation does not yet exist; it is built under
  its own prereg before this comparison can run.
- **contlearn2**: prereg `2f9eddc5e`, implementation `179b4a950`,
  result `LEARNER-EXTENDED` (`continuing_learner/CL2_RESULT.md`).
  Schema-based continuing learner: instance store, kind-1
  (uniform default) and kind-2 (default plus single exception)
  schema forms, accuracy ledger plus consecutive-rejection
  retirement triggers, discovery/gate/refit machinery. Bounded
  L1/L2 by its own honest scope statement. Currently the
  control/competitor.

## 2. Standing question

> Which architecture produces more capability from less
> researcher-authored machinery?

Capability-source delta is the master metric. Every dimension below
is a facet of it.

## 3. Phase structure

### Phase 0: Readiness (gating)

Neither phase 1-3 may begin until both gates hold.

- **Gate G0a (CLA-1 implementable):** a CLA-1 implementation exists,
  built under the frozen prereg `b4f61ff8a`, and passes that
  prereg's kill bars K1-K3 (architecture completely specified,
  zero task-specific handlers/semantic cases/modes/bridges by
  source inspection, pure Zag plus shell, dash-clean, paper
  untouched). If the implementation fails its prereg, the
  comparison is not run; the implementation is fixed or the
  comparison is declared premature. Comparing a broken
  implementation against a working one proves nothing.
- **Gate G0b (determinism):** both frozen binaries produce
  byte-identical output on 3/3 runs of a fixed smoke script,
  exit 0, zero stderr. Non-determinism voids any scored phase.
- **Gate G0c (blindness):** the sealed new-capability battery
  (section 7) is hashed and committed before either
  implementation is finalized for the comparison, and neither
  architecture's builders have read the world contents. Builder
  blindness is certified in writing. Broken blindness voids
  phase 3.

### Phase 1: Static metrics (D2, D3, D4)

Source inspection only. No runs. Performed by an auditor worker
using the same grep-inventory method as the One-System audit
(`f2684204b`).

### Phase 2: Live capability runs (D1, D5, D6)

Both frozen binaries run the capability battery, the transfer
probes, and the original 9 freeze worlds. Binary hash verified
before every world (same discipline as run phase `97b28e6a6`:
mismatch exits VOID). Persistent state across worlds in protocol
order. No task labels at any layer. 3/3 byte-identical runs
required for every scored measurement.

### Phase 3: Sealed new-capability battery (D7)

Both frozen binaries, full blindness, protocol order, persistent
state, hash verification before every world. This is the
highest-weight phase.

### Phase 4: Decision

Apply the decision rule in section 8. Report per-dimension
scores, the weighted total, the capability-density check, and
the convergence recommendation. The recommendation is advisory:
Micah makes the final convergence call.

## 4. Dimension D1: Capability

**What is measured:** frozen probe scores across capability
families, both architectures, same events, same drivers.

**Battery structure (frozen here; exact probe instances are
preregistered by the phase-2 execution worker under this
protocol's authority):**

| Family | Capability | Probes | Pass bar |
|---|---|---|---|
| F1 | concept association (W1-class) | 12 | >= 10 |
| F2 | procedure induction (W2-class) | 8 | >= 6 |
| F3 | causal law construction (W3-class) | 10 | >= 7 |
| F4 | change and revert (W4-class) | 6 | >= 5 |
| F5 | contradiction handling (W5-class) | 8 | >= 6 |
| F6 | synthetic language induction (W8-class) | 9 | >= 7 |
| F7 | representational structure (W9-class) | 12 | >= 9 |

Total: 73 probes. Families run sequentially in ONE stream per
architecture (continuing-learner semantics: no reset between
families, no task labels). Each probe is deterministic; a probe
counts only if 3/3 runs agree byte-identically.

**Score:** total probes passed / 73, plus per-family pass/fail.

**Discriminating result:** absolute difference >= 4 probes on the
73-probe total, with the leader also passing >= 1 more family
bar than the other. **Tie:** difference <= 3 probes, or both
architectures fail every construction family (F2, F3, F6-novel,
F7), in which case D1 measures only storage and is noted as
non-discriminating on the frontier.

## 5. Dimension D2: Source delta

**What is measured:** researcher-authored machinery each
architecture carries.

**Procedure:**

1. Identify the cognition source files for each architecture:
   the .zag files implementing the learner core, excluding
   drivers, harnesses, world files, tests, and docs. The file
   list is committed before counting.
2. Count lines with `wc -l` (shell only). Record total
   cognition source lines per architecture.
3. Record the One-System accounting per architecture: new
   hardcoded semantic cases, modes, bridges, task-specific
   handlers, learner-state structures created. CLA-1's prereg
   already binds its direction (net-negative vs the summed
   surviving-mechanism sources); contlearn2's accounting comes
   from its implementation.
4. Compute capability density: (D1 probes passed + D6 worlds
   passed) per 100 cognition source lines.

**Discriminating result:** the architecture with higher
capability density wins, provided the density ratio is >= 1.5
in its favor AND its absolute capability (D1+D6) is not lower.
A smaller codebase that does less is not a win; the ruling is
MORE capability from LESS machinery. **Tie:** density ratio
< 1.5, or the denser architecture scores lower on absolute
capability.

## 6. Dimension D3: Number of state formats

**What is measured:** distinct persistent state formats the
learner writes to and reads from across restarts.

**Procedure:** enumerate by source inspection plus the
architecture's own documentation. A format is one record
layout with its own read/write path. CLA-1 claims one (the
node store); its utility ledger, dependency graph, protection
set, and experience log are node-type conventions inside that
store, not separate formats, and the auditor verifies this
claim. contlearn2's formats are counted as found (instance
store, schema records by kind, accuracy ledger, counters).

**Discriminating result:** fewer formats wins, but only if D1
capability is not lower. One format that cannot hold the
capability is not a win. **Tie:** equal counts, or the
fewer-format architecture loses on D1.

## 7. Dimension D4: Handlers, modes, bridges

**What is measured:** architectural special-case machinery.

**Procedure:** the One-System audit method (`f2684204b`):
systematic grep over all .zag sources for handler-like dispatch
on task or world identity, `_MODE` identifiers, bridge
functions, and router codes. Each distinct mechanism is
counted and named. Counts are committed with the grep evidence.

**Discriminating result:** fewer total special mechanisms wins
at equal or greater D1 capability. Zero vs nonzero on any
single category (modes, bridges, task-specific handlers) is
automatically discriminating in favor of zero, regardless of
the total, provided D1 is not lower. **Tie:** equal totals
with equal category profiles.

## 8. Dimension D5: Transfer

**What is measured:** whether learned capability survives a
changed surface representation, without source edits and
without retraining from scratch.

**Procedure:**

1. Train each architecture on family F-train (concept
   association probes in surface S1: one ID range, one
   relation-code mapping).
2. In the same continuing stream (no reset, no source edits),
   probe on family F-test (same underlying regularities,
   surface S2: permuted ID ranges, remapped relation codes,
   different arity encoding). 12 probes, pass bar >= 8.
3. Transfer ratio = (F-test score) / (F-train score), both as
   fractions. A transfer ratio is meaningful only if F-train
   score >= 8/12; otherwise the architecture had nothing to
   transfer and D5 is recorded as NOT-APPLICABLE for it.

**Discriminating result:** transfer ratio >= 0.6 vs < 0.4 is
discriminating. **Tie:** both ratios within 0.2 of each other,
or both NOT-APPLICABLE.

## 9. Dimension D6: Freeze-challenge performance

**What is measured:** both architectures on the original 9
Core Freeze Challenge worlds, under the identical discipline
that produced `97b28e6a6`.

**Procedure:**

1. Worlds: the 9 sealed world files from the run phase
   (designs `e806d634e` and `6d185ebce`), hashes re-verified
   MATCH before running.
2. Binary hash of each architecture verified before every
   world via the same `run_world.sh` discipline (mismatch
   exits VOID). Persistent state across worlds in protocol
   order W1..W9. No task labels.
3. Interface mapping, committed before running:
   - CLA-1: OBSERVE maps to a TEACH event, QUERY maps to a
     QUERY event, ACT maps to an ACT event with CHOICE read
     from the action channel. Native mapping; no bridge.
   - contlearn2: OBSERVE(s,r,o) maps to its learn path,
     QUERY(s,r) maps to its query path
     (instance-first-then-schema). The mapping is generic
     (no world-id or task branching in the driver; verified
     by inspection).
   - ACT events for contlearn2: contlearn2 has no action
     channel, so it cannot emit CHOICE. Action-dependent
     probes (W6 inquiry attribution, W7 planning) score 0
     for contlearn2, annotated ARCHITECTURE-ABSENT. This is
     not a scoring penalty invented by the protocol; it is
     the honest measurement of a missing channel, and it is
     legitimate comparative evidence about generality.
4. Scoring: per-world WORLD-PASS/WORLD-FAIL on the original
   bars, plus total probes correct across all 9 worlds.
   3/3 byte-identical runs required.

**Discriminating result:** difference >= 2 world passes, or
difference >= 6 total probes with the leader ahead on at
least two world families. **Tie:** same world-pass count and
total-probe difference <= 5.

## 10. Dimension D7: New capability without source edits

This is the highest-weight dimension. It operationalizes the
mandate: the architecture must create cognitive structure its
programmers did not supply.

**Procedure:**

1. Both binaries are frozen and hash-sealed. No source edits
   from this point for either architecture.
2. Sealed battery: capability families neither architecture
   has demonstrated. The approved FW1-FW9 worlds
   (`200387b42`, once implemented and sealed) are the
   designated battery, subject to Gate G0c blindness. If FW
   worlds were seen by either architecture's builders, a
   fresh post-freeze adversary set is designed instead; the
   protocol does not bend on blindness.
3. Run both frozen binaries through the battery in protocol
   order, persistent state, hash verification before every
   world, 3/3 byte-identical runs.
4. Measure per world: (a) probe scores on the world's bars;
   (b) white-box structural evidence: did the learner create
   a new structural form? For CLA-1, the prereg's P4
   criterion applies: a node-type topology not enumerated in
   `b4f61ff8a`. For contlearn2, the criterion is a schema
   form beyond kind-1/kind-2 (a third kind), or equivalent
   structural novelty in its own state vocabulary. The
   criterion for each architecture is committed before the
   runs, in that architecture's own terms, and judged by an
   independent white-box inspector.
5. Anti-menu check: a new form counts only if it was not
   enumerated in the architecture's prereg AND it is reused
   on at least one later probe (existence without reuse is
   storage, not capability).

**Discriminating result:** one architecture demonstrates a
capability family the other cannot (passes the family bar
while the other scores <= 25%), WITH the new structure
visible in learner state and reused, and zero source edits.
That is a clean win on D7 regardless of other dimensions.
**Tie:** both fail all new families (the frontier is beyond
both; the program needs redesign, not convergence), or both
pass the same families.

## 11. Scoring and decision rule

Per-dimension verdicts: +1 (CLA-1 wins), -1 (contlearn2 wins),
0 (tie or not-applicable).

Weights: D7 = 3, D1 = 2, D6 = 2, D2 = 1, D3 = 1, D4 = 1,
D5 = 1. Total range: -11 to +11.

**Converge on CLA-1** iff ALL of the following hold:

- (a) weighted total >= +4;
- (b) D7 >= 0 (CLA-1 does not lose the key discriminator);
- (c) D2 + D3 + D4 >= 0 (CLA-1 does not carry more
  researcher-authored machinery while claiming the
  architectural high ground);
- (d) Gate G0a held (the CLA-1 implementation passed its own
  prereg; we are comparing a valid implementation).

**Converge on contlearn2** iff weighted total <= -4. This
means the extension approach demonstrated more capability
from less or equal machinery, and the clean-substrate
direction is not paying for itself.

**Send both back** (no convergence) iff:

- (i) weighted total is in (-4, +4): the comparison did not
  discriminate;
- (ii) D7 is 0 for both with both failing all new families:
  neither architecture creates new capability without source
  edits, so the frontier is beyond both and convergence
  would be premature;
- (iii) any gate failed or any phase was invalidated
  (blindness broken, non-determinism, Python contamination,
  prereg violated): the comparison is void, not tied;
- (iv) CLA-1's implementation never passes its prereg kill
  bars: there is no valid CLA-1 competitor yet.

**Capability-density sanity check:** compute (D1 probes + D6
worlds passed) per 100 cognition lines for each architecture.
If the weighted vote and the density ranking disagree, the
phase-4 report must explain the disagreement explicitly and
the recommendation is downgraded to provisional.

## 12. Governance

1. Pure Zag for all research logic: drivers, scorers, world
   generators, analyzers, verifiers. Shell exists only to
   invoke znc, execute binaries, run git, and move or copy
   files. No shell/awk/sed/grep scripts as substitute
   research programs. Any Python invocation at any stage
   voids the phase in which it occurred; disclosure does not
   cure it.
2. Prereg-first: this protocol is frozen before any
   comparison work. Phase execution workers write their own
   preregs citing this protocol; no bar moves after results.
3. Sealing: world files hashed (sha256) and committed before
   the architectures under test are finalized. Binary hashes
   recorded at freeze and verified before every world.
4. Determinism: 3/3 byte-identical runs, exit 0, zero stderr,
   for every scored measurement. Anything less is unscored.
5. Commits stay local on tnn-native-lab. Owned paths only,
   explicit pathspecs, git status inspected before every
   commit. The contaminated paper is never touched.
6. No em dashes in any file. Byte-checked before commit.
7. The comparison does not authorize tuning either
   architecture to the test worlds. FW1-FW9 are
   evaluator/adversary assets, not design hints (ruling A).
   Any evidence of tuning voids the phase.

## 13. What this protocol does not decide

- The CLA-1 implementation itself (separate worker, under
  prereg `b4f61ff8a`).
- The FW1-FW9 world implementation and sealing (separate
  task; design approved at `200387b42`).
- The exact probe instances for D1 families and D5 surfaces
  (preregistered by the phase-2 execution worker under this
  protocol's authority).
- The final convergence call, which is Micah's.
- Whether a third architecture should enter the comparison;
  this protocol covers exactly the two named competitors.

## 14. Kill bars for this protocol document

- K1: this document completely specifies the comparison:
  phases and gates, all seven dimensions with concrete
  measurement procedures, discriminating-vs-tie criteria per
  dimension, the weighted decision rule with all three
  outcomes, the freeze-challenge procedure with the
  interface mapping for both architectures, the
  new-capability battery procedure with white-box criteria,
  and governance. Committed alone before any comparison
  work exists.
- K2: the document contains zero implementation, zero runs,
  zero scores, and zero tuning guidance for either
  architecture. It specifies measurement only.
- K3: pure markdown, dash-clean by shell-only byte check,
  contaminated paper verified zero-diff, zero Python at
  every step, commits local with explicit pathspecs under
  arch_comparison/ only.
