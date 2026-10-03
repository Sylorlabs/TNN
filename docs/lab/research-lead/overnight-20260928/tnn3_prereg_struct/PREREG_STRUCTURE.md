# TNN-3 Preregistration Structure: Synthesis of All Kill Bar Drafts

**Status: DRAFT-NOT-FROZEN - AWAITING MICAH REVIEW**

Date: 2026-10-01 (UTC). Drafter session: 450f83f7-f093-4bab-9a77-4c6fc52f92cd.

This document synthesizes all kill bar drafts into a coherent
preregistration structure. It is structure only: no implementation, no
frozen thresholds, no source edits. Nothing here governs any build
until Micah reviews it and a TNN-3 preregistration freezes it (or
records explicit amendments) before any TNN-3 implementation begins.

All input bar drafts are DRAFT-NOT-FROZEN. This synthesis does not
freeze them; it organizes them.

---

## 1. Inventory: all drafted bars with sources

### 1a. Cross-cutting process and audit bars

| Bar | Source | What it governs |
|---|---|---|
| K-T3-ADV | `tnn3_killbars/` (`76231baa8`) | Adversarial process: independence, post-freeze authorship (git-verified, fail closed), limited visibility, minimum world counts, no trivial variants |
| K-T3-TOPO | `tnn3_killbars/` (`76231baa8`) | Learner-chooses-topology audit: (a) mutual non-isomorphism via deterministic signature function; (b) at least one passing sealed shape absent from builder's fixture log |

### 1b. Construction bars

| Bar | Source | What it governs |
|---|---|---|
| K-T3-CON-1 | `tnn3_killbars/` (`76231baa8`) | Two structurally different sealed constructions (3+ mutually non-isomorphic required topologies across 4+ worlds), derived content not readable from triggering literals |
| K-T3-CON-2 | `tnn3_killbars/` (`76231baa8`) | Construction reuse (C0-D): sealed world where the only path to the correct graph is reusing a previously promoted graph; structural reference verified; control run from fresh state must fail |

### 1c. Inquiry bars

| Bar | Source | What it governs |
|---|---|---|
| K-T3-INQ-1 | `tnn3_killbars/` (`76231baa8`) | Derived discriminating need: 2+ scenarios with differing warranted inquiries; guide action/content fields must differ and match checker-computed required content |
| K-T3-INQ-2 | `tnn3_killbars/` (`76231baa8`) | Evidence updates later behavior: (a) resolution transitions UNCERTAINTY to resolved, ACT stops selecting stale guide; (b) misleading evidence triggers revision/supersession |
| K-T3-INQ-3 | `tnn3_killbars/` (`76231baa8`) | Ambiguity handled non-arbitrarily (swap test): ACT selects the dominating guide in both scenarios where dominance is unambiguous by adversarial design |
| K-T3-INQ-4 | `tnn3_killbars/` (`76231baa8`) | Inquiry reuse and transfer (C0-D): second episode's guide structurally references first episode's retained structures; strictly fewer miss events before correct ACT selection |

### 1d. Revision bars

| Bar | Source | What it governs |
|---|---|---|
| K-T3-REV-1 | `tnn3_killbars/` (`76231baa8`) | Two structurally different sealed repairs (2+ mutually non-isomorphic repair topologies across 3+ scenarios), derived content not copied from observation |
| K-T3-REV-2 | `tnn3_killbars/` (`76231baa8`) | Retained-set regression: after each repair, 100 percent of retained licensing facts verify plus the triggering case, 3/3 byte-identical |
| K-T3-REV-3 | `tnn3_killbars/` (`76231baa8`) | Successive revision including revert: two contradictions on the same graph; final graph must not contain repair A's edit as an active step; retained set passes |

### 1e. H3-lite policy revisability bar

| Bar | Source | What it governs |
|---|---|---|
| K-H3 | `tnn2_h3lite/` (`22197da2c`) | Policy revisability: for every structural decision not determined by immediate input, the prereg must list (1) the decision, (2) learner-state node/fields, (3) production write path, (4) triggering event, (5) sealed test showing variation across histories. Four failure conditions: (a) source literal with no learner-state read; (b) read but no production write path; (c) write path unreachable in sealed eval; (d) test histories directly encode the expected decision |

### 1f. Target-selection bars

| Bar | Source | What it governs |
|---|---|---|
| K-TSEL-1 | `tnn2_targetsel/` (`01c2aacfe`) | Learner-chosen composition targets: history-discrimination test; same binary on swapped A/B success histories must reverse attempt order; fixed order fails by construction |
| K-TSEL-2 | `tnn2_targetsel/` (`01c2aacfe`) | No oracle shortcut: score updates computed from learner's own verification outcomes only; prereg names exact fields; reading any other field is a violation |

### 1g. Reuse-path bars

| Bar | Source | What it governs |
|---|---|---|
| K-REUSE-1 | `tnn2_reusepath/` (`5f15b9309`) | Query-time MAP execution: white-box trace showing tag-20 node read during query and `t2_exec` invoked on its stored root, preceding any `activate` hit |
| K-REUSE-2 | `tnn2_reusepath/` (`5f15b9309`) | No shadow facts: no `ev_teach_in` reachable from `promote_graph` or MAP revision may insert a fact with the same (s, r) as a live MAP; one shadow fact is a violation |

**Total: 17 bars** (2 cross-cutting + 2 construction + 4 inquiry + 3 revision + 1 H3-lite + 2 target-selection + 2 reuse-path + 1 implied structural signature function).

---

## 2. Dependencies: which bars depend on which

### 2a. Hard dependencies (a bar cannot be attempted before its prerequisite)

1. **K-TSEL-1/2 depend on K-REUSE-1/2.** The target-selection design
   states this explicitly: "target selection is downstream of the
   reuse path." The two signals a learner-authored selection policy
   needs (reuse history, composition outcome records) do not exist
   without query-time MAP execution. Building the selector first
   would be "the exact treadmill the program forbids: a new
   mechanism whose inputs are researcher constants and whose
   outputs change nothing."

2. **K-T3-CON-2 (construction reuse) depends on K-REUSE-1.**
   Construction reuse via inlining requires promoted graphs to be
   executable components. The reuse path makes MAP execution an
   observable query-time event; without it, the structural
   reference check in K-T3-CON-2 has no execution semantics to
   verify against.

3. **K-T3-INQ-4 (inquiry reuse) depends on K-REUSE-1 conceptually.**
   Cross-episode inquiry reuse requires retained inquiry structures
   to be readable and referenceable. While the inquiry reuse in
   K-T3-INQ-4 is about uncertainty/guide structures rather than
   MAPs, the architectural principle is the same: reuse requires
   the reused artifact to be on a live read path, not shadowed by
   a memoized copy.

### 2b. Soft dependencies (ordering recommended but not strictly required)

4. **K-H3 conditions all mechanism bars.** H3 is confirmed as
   structural fact: no production path can currently revise
   mechanism policies from experience. Any bar testing derived
   content or history-dependent behavior (K-T3-INQ-1, K-T3-INQ-3,
   K-T3-REV-1, K-TSEL-1) implicitly requires the relevant decisions
   to be in learner state with production write paths. K-H3 makes
   this requirement explicit and testable. Attempting mechanism
   bars without K-H3 risks the "revisability theater" failure mode
   (write paths exist but never meaningfully exercised).

5. **K-T3-ADV governs all sealed-world bars.** Every bar that
   references "sealed worlds" or "post-freeze authorship"
   (K-T3-CON-1/2, K-T3-INQ-1/2/3/4, K-T3-REV-1/2/3, K-TSEL-1,
   K-REUSE-1) depends on the adversarial process being correctly
   implemented. If K-T3-ADV fails (e.g., a world asset predates the
   build freeze), the evaluation is BLOCKED, fail closed, and no
   mechanism bar can pass.

6. **K-T3-TOPO audits all mechanism bars.** The topology audit
   (mutual non-isomorphism + beyond-fixture shapes) applies to the
   diversity sets of construction (K-T3-CON-1), revision
   (K-T3-REV-1), and by extension any future composition worlds.
   It does not gate individual world passes but provides the
   structural-difference verdict that the "two structurally
   different" requirement in each mechanism section depends on.

### 2c. Cross-cutting (no dependencies, applies everywhere)

7. **K-H3 is cross-cutting.** It applies to every structural
   decision in every mechanism: trial search order, guide template,
   repair dispatcher, composition target selection, and any future
   decision points. It does not depend on any mechanism bar; it
   constrains how all of them are implemented.

8. **K-T3-ADV is cross-cutting.** It constrains the evaluation
   process for all sealed-world bars. It does not depend on any
   mechanism bar; it is a precondition for all of them.

### 2d. Dependency graph (summary)

```
K-T3-ADV (process precondition for all sealed bars)
    |
    +-- K-T3-TOPO (audit, works with all mechanism diversity sets)
    |
    +-- K-REUSE-1/2 (reuse path; no prerequisites)
    |       |
    |       +-- K-TSEL-1/2 (needs reuse signal)
    |       |
    |       +-- K-T3-CON-2 (needs executable MAPs)
    |       |
    |       +-- K-T3-INQ-4 (conceptual dependency)
    |
    +-- K-H3 (cross-cutting; conditions all mechanism bars)
    |       |
    |       +-- K-T3-CON-1 (needs revisable construction policy)
    |       +-- K-T3-INQ-1/3 (needs revisable guide policy)
    |       +-- K-T3-REV-1 (needs revisable repair policy)
    |
    +-- K-T3-INQ-2 (resolution; needs H3-lite guide policy + L6 path)
    +-- K-T3-REV-2 (retained set; needs revision that consults provenance)
    +-- K-T3-REV-3 (revert; needs repair history)
```

---

## 3. Order: in what order should they be attempted

Per the TNN-3 roadmap (`67a420cca` section 7), synthesizing the
synthesis recommendation, the H3 probe execution, and the interaction
analyst's bottleneck analysis:

### Step 0 (done): H3 cheap check

Executed against the frozen TNN-2 source. Result: all three mechanisms
structurally unrevisable. H3 confirmed as architectural fact. This
step is complete and need not be repeated.

### Step 1: H2 probes (masked verification)

Keep the finite grammar fixed. Change only verification: masked
queries where `expected` is withheld, plus revision probes where
corrected content must be derived from retained facts rather than
copied from the observation. This tests whether the oracle is the
binding constraint.

**Bars involved:** None of the 17 directly, but the probes inform
whether H2 binds before H1 widening. If current mechanisms fail
masked probes while passing unmasked ones, H2 binds and must be
addressed before Step 4.

**Cost:** New sealed worlds, no new machinery.

### Step 2: H3-lite (policy parameterization) + K-H3

Implement the three policy nodes from `22197da2c` (trial order,
guide template, repair dispatcher) with K-H3 frozen in
preregistration. This makes the mechanisms' decisions revisable by
experience and provides the discrimination tests (order-flip worlds,
template-shift scenarios, topology-preference shifts).

**Bars involved:** K-H3 (primary). Enables K-T3-INQ-1, K-T3-INQ-3,
K-T3-REV-1 (which require revisable policies).

**Cost:** Moderate new machinery, no ISA change, no governance
decision. This is the minimal TNN-3 core.

### Step 3: Repair-proposal generator + inquiry resolution

The within-ISA changes from the revision generalization analysis
(`edbb0e9b5` section 4a) and inquiry generalization (`dedfad368`
sections 1-2). These complete the minimal TNN-3.

**Bars involved:** K-T3-REV-1 (needs multi-topology repair),
K-T3-REV-2 (needs retained-set checking), K-T3-INQ-2 (needs
resolution path), K-T3-REV-3 (needs repair history for revert).

**Dependency note:** The revision dispatcher policy (H3-lite
subtype 3, from Step 2) selects among the repair topologies the
generator enumerates. The generator can be built and tested with a
fixed order first; the policy then learns the order.

### Step 4: H1 widening (open constructor), ONLY after Step 1

Recursive composition via inlining (per the MUL comparator
`e2e34a4ac` section 4), plus the target-selection policy as a
learner-state mechanism (K-TSEL-1/2).

**Bars involved:** K-T3-CON-1 (needs open construction),
K-T3-TOPO (audits the resulting diversity),
K-TSEL-1/2 (learner-chosen targets).

**Critical constraint:** This step must not precede Step 1, per the
treadmill warning. Widening the constructor while `t2_try_verify`
still matches environment-supplied expected values produces "a
larger finite menu under the same generous acceptance test"
(the exact treadmill Micah forbade).

**Also requires:** The post-freeze adversarial battery (K-T3-ADV)
to test whether fixed composition operators suffice for genuinely
new structures.

### Parallel track (not ordered after the above): Reuse path

Routing `ev_query` hits through MAP execution instead of memoized
facts (K-REUSE-1/2). Required for C0-D regardless of which
synthesis hypothesis binds. Orthogonal to H1/H2/H3 and can proceed
in parallel.

**Bars involved:** K-REUSE-1, K-REUSE-2 (primary).
**Enables:** K-TSEL-1/2, K-T3-CON-2, K-T3-INQ-4.

**Explicitly not in the roadmap:** Full H3 (procedures as
learner-built graphs), pending the protected-core structural-ops
governance decision banked for Micah. H3-lite (Step 2) is the
recommended way to gather evidence for that decision.

### Order summary table

| Step | Work | Primary bars | Prerequisites |
|---|---|---|---|
| 0 | H3 check | (none; diagnostic) | Done |
| 1 | H2 masked probes | (none; diagnostic) | Step 0 |
| 2 | H3-lite policy nodes | K-H3 | Step 0 |
| 3 | Repair generator + inquiry resolution | K-T3-REV-1/2/3, K-T3-INQ-2 | Step 2 |
| 4 | H1 open constructor + target selection | K-T3-CON-1, K-TSEL-1/2, K-T3-TOPO | Step 1, Step 2 |
| Parallel | Reuse path | K-REUSE-1/2 | (none) |
| (banked) | Full H3 | (future) | Micah's protected-core decision |

---

## 4. Conflicts: conflicting requirements or overlapping coverage

### 4a. No direct conflicts found

No two bars require mutually exclusive behavior. The drafts were
authored by separate lanes but converge on compatible
observables. Specific checks:

- **K-REUSE-1 (MAP-first ordering) vs K-T3-REV-2 (retained-set
  checking):** Compatible. MAP-first query ordering does not
  prevent revision from consulting retained licensing facts; they
  operate on different paths (query vs contradiction).
- **K-H3 (list every structural decision) vs K-T3-ADV (adversary
  independence):** Compatible. The K-H3 listing is a preregistration
  obligation on the builder; the adversary authors worlds, not the
  listing.
- **K-TSEL-2 (no oracle shortcut) vs K-T3-CON-1 (derived content):**
  Compatible and mutually reinforcing. Both bar the environment
  from supplying the answer; they test different mechanisms
  (selection vs construction).

### 4b. Overlapping coverage (intentional redundancy)

Three overlaps are intentional defense-in-depth, not accidental
duplication:

1. **K-T3-TOPO(b) and K-H3 condition (d).** Both guard against
   test-scaffolding. K-T3-TOPO(b) checks that sealed shapes were
   never fixture-exercised (builder cannot pre-enumerate).
   K-H3(d) checks that policy changes are outcomes of ordinary
   world interactions, not inputs (test cannot write the policy).
   Different mechanisms, same anti-gaming principle.

2. **K-T3-CON-2 and K-REUSE-1.** Both involve MAP execution.
   K-REUSE-1 proves the reuse event happens at query time
   (execution, not memoization). K-T3-CON-2 proves a new graph
   structurally references a previously promoted graph (composition,
   not just re-execution). Reuse is necessary for composition but
   not sufficient; the bars test different claims.

3. **K-T3-INQ-2(a) and K-T3-REV-3.** Both involve supersession and
   "removing" prior state. K-T3-INQ-2(a) tests uncertainty
   resolution (guide superseded after evidence arrives).
   K-T3-REV-3 tests repair revert (repair A's edit removed after
   new contradiction). Different objects (guides vs graph edits),
   same lifecycle principle.

### 4c. Tension requiring Micah's resolution (not a conflict)

**K-T3-TOPO signature function: single vs per-world.** The kill-bar
draft (section 11, Q3) notes the draft allows per-world signature
functions under a prereg-fixed computation schema, but a single
fixed function is simpler to audit. The kill-bar review
(`eb354e3a2`) recommended: single function fixed in the frozen
prereg (simpler to audit, harder to game). This is a design choice
for Micah, not a conflict between bars.

---

## 5. Gaps: what is NOT covered by any bar

### 5a. Identified gaps

1. **H2 (oracle) has no dedicated kill bar.** The 17 bars test
   construction diversity, inquiry derivation, revision diversity,
   policy revisability, target selection, and reuse. None directly
   bars the oracle: a system could pass all 17 while still
   verifying exclusively against environment-supplied expected
   values. The roadmap's Step 1 (H2 masked probes) is diagnostic,
   not a kill bar. **Recommendation:** draft a K-H2 bar (masked
   verification: system must verify candidates without `expected`,
   or derive acceptance from learner-internal prediction) before
   Step 4 (H1 widening), per the treadmill warning.

2. **Composition operators themselves (H1 at operator level).**
   K-T3-CON-1 bars the output diversity (3+ non-isomorphic
   topologies). K-TSEL-1/2 bar the operand selection. But no bar
   tests whether the composition *operators* (splice, chain,
   substitute) are learner-authored vs researcher-authored. The MUL
   comparator sustained the "larger finite menu" objection at the
   operator level. **Recommendation:** acknowledge as explicit
   non-claim (the minimal TNN-3 does not address operator
   invention) or draft a K-H1-OP bar for a future generation.

3. **Inquiry informativeness criterion.** K-T3-INQ-1 requires
   derived content matching checker-computed values. K-T3-INQ-3
   requires dominance tracking. But no bar tests the *criterion*
   by which the learner judges one question more informative than
   another in open-ended (non-adversarially-dominated) cases.
   The inquiry generalization analysis (`dedfad368`) specified an
   informativeness scoring; H3-lite explicitly does not implement
   it. **Recommendation:** acknowledge as explicit non-claim for
   the minimal TNN-3; a future bar could test informativeness
   ranking on non-dominated uncertainties.

4. **Cross-mechanism interference.** No bar tests what happens when
   construction, inquiry, and revision interact adversarially
   (e.g., a revision that breaks a reused construction, an inquiry
   whose resolution contradicts a MAP). K-T3-ADV requires
   interleaved worlds (GW7 in the GW1-GW8 battery is a precedent),
   but no bar specifies the expected behavior under interference.
   **Recommendation:** include at least one interference world in
   the K-T3-ADV battery with a checker that verifies graceful
   degradation (no crash, no silent staleness), even if the exact
   correct behavior is world-dependent.

5. **The "verdicts without structures" finding.** The inquiry
   generalization analysis (`dedfad368`) found the trial loop
   discards candidate structures before `miss_inquire` runs;
   "learner state records verdicts but not the structures those
   verdicts were about." No bar directly tests structure
   retention (vs verdict retention). K-T3-INQ-4 (inquiry reuse)
   partially covers it (structural reference required), but a
   construction analog (retaining rejected candidates for later
   reuse) is unbarred. **Recommendation:** the kill-bar review
   (`eb354e3a2`) already recommended adding a state-retention
   probe to the governance audit (audit-grade, not bar-grade).
   Adopt that recommendation.

### 5b. Explicit non-claims (acknowledged, not gaps)

The following are deliberately out of scope for the minimal TNN-3
and should be stated as non-claims in the preregistration, not
treated as gaps:

- Full H3 (procedures as learner-built graphs): needs the
  protected-core structural-ops decision (banked for Micah).
- Operator invention (H1 at operator level): the repair family and
  composition operators remain researcher-enumerated.
- Oracle replacement (H2): verification still uses
  environment-supplied expected/observed values.
- FW1-FW9 score improvement: H3-lite changes the locus of
  control, not scores; no capability improvement is predicted.

---

## 6. Structure: proposed preregistration document outline

### Section 1: Identity and precedence

1.1 Preregistration identifier and date
1.2 Build-freeze commit (to be recorded at freeze time)
1.3 Prereg commit strictly precedes implementation (ordering bar,
  verified by git ancestry; carried over from K-T2-1)
1.4 What this preregistration covers (which steps from section 3
  above: e.g., "Steps 2 and Parallel" for a minimal TNN-3)

### Section 2: Frozen kill bar text

2.1 Cross-cutting bars (K-T3-ADV, K-T3-TOPO) - exact statements
2.2 Construction bars (K-T3-CON-1, K-T3-CON-2) - exact statements
2.3 Inquiry bars (K-T3-INQ-1 through K-T3-INQ-4) - exact statements
2.4 Revision bars (K-T3-REV-1 through K-T3-REV-3) - exact statements
2.5 H3-lite bar (K-H3) - exact statement with the five listing
  requirements and four failure conditions
2.6 Target-selection bars (K-TSEL-1, K-TSEL-2) - exact statements
  (if Step 4 in scope)
2.7 Reuse-path bars (K-REUSE-1, K-REUSE-2) - exact statements
  (if Parallel track in scope)
2.8 For each bar: the specific TNN-2 failure mode it targets
  (with commit references to the red-team reports)

### Section 3: Structural signature function

3.1 The deterministic function (fixed in prereg; per the kill-bar
  review recommendation: single function, not per-world)
3.2 Canonical string specification (cell tags, edge types, step
  counts, adjacency shape; no literals, no addresses, no allocation
  order)
3.3 Calibration test: the function must be tested against known
  pairs before the evaluation (chain k=2 vs k=3 must differ; same
  topology with different literals must not differ)
3.4 State-dump format (explicitly frozen so reference checks are
  mechanical)

### Section 4: Adversary protocol (K-T3-ADV implementation)

4.1 Designated independent adversary agents (recorded in each
  world's NAMECHECK)
4.2 Post-freeze authorship verification (`git merge-base
  --is-ancestor`; fail closed BLOCKED)
4.3 Limited visibility specification (what the adversary sees)
4.4 Minimum world counts per mechanism (with Micah's resolution of
  Q1: construction 4+, inquiry 5+ per review recommendation,
  revision 3+)
4.5 Pairwise-distinctness check procedure
4.6 Non-triviality rationale per world (presence check)

### Section 5: Policy revisability listing (K-H3 implementation)

5.1 For every structural decision not determined by immediate
  input, the five-part listing:
  (1) the decision
  (2) learner-state node and fields (tag, subtype, field numbers)
  (3) production (non-test) code path that writes
  (4) experience event triggering the write
  (5) sealed test demonstrating variation across histories
5.2 Explicit enumeration of decisions covered (trial order, guide
  template, repair dispatcher, target selection if in scope, any
  others)
5.3 The discrimination tests from the H3-lite design (sections 2g,
  3g, 4h) as committed evaluation assets

### Section 6: Architecture accounting

6.1 Cognition source lines added
6.2 New hardcoded semantic cases (must be zero)
6.3 New modes (must be zero)
6.4 New bridges (must be zero)
6.5 New task-specific handlers (must be zero)
6.6 Learner-state structures created
6.7 Capability-source delta statement
6.8 ISA freeze attestation (no new opcodes; protected core
  unchanged)

### Section 7: Explicit non-claims

7.1 What L2 the design achieves
7.2 What L3 it does not achieve (per the roadmap's non-overselling)
7.3 Which of H1/H2/H3 it addresses and which it does not
7.4 Score predictions (honest: H3-lite changes locus of control,
  not FW1-FW9 scores)

### Section 8: Verification procedures

8.1 Determinism: 3/3 byte-identical for every check
8.2 Pure-Zag checkers and drivers
8.3 Safebin for builder workers (Step 0 toolchain guard)
8.4 Forbidden executables = PROCESS-FAIL
8.5 No weakening after results (amendment requires transparent
  re-freeze and full re-run)

### Section 9: Open questions resolved

9.1 Micah's resolutions to the 6 kill-bar draft questions (Q1-Q6)
  with rationale
9.2 Micah's resolution to the signature-function question
  (single vs per-world)
9.3 Any amendments to draft bar text with rationale

### Section 10: Governance and audit

10.1 State-retention probe (from the kill-bar review
  recommendation; audit-grade)
10.2 Seal integrity verification procedure
10.3 Contamination checks (builder never sees sealed worlds
  before freeze)

---

## 7. The 6 open questions for Micah (with review recommendations)

From the kill-bar draft section 11, with the kill-bar review
(`eb354e3a2`) recommendations:

1. **World counts:** Draft sets construction 4+ (3+ non-isomorphic),
   inquiry 3+, revision 3+ (2+ non-isomorphic). **Review
   recommends:** raise inquiry to 5+ scenarios (7 scenario slots
   needed across INQ-1..4; 3 forces triple-booking). Keep
   construction 4+ and revision 3+.

2. **K-T3-TOPO(b) builder burden:** Requires builder's test suite
   to log structural signatures for every promoted and revised
   graph. **Review recommends:** keep; specify the log format in
   the prereg.

3. **Signature function:** Single fixed function vs per-world
   functions under a prereg-fixed schema. **Review recommends:**
   single function fixed in the frozen prereg (simpler to audit,
   harder to game).

4. **K-T3-INQ-3 prescriptiveness:** Requires dominance-tracking
   across the swap. **Review recommends:** keep as drafted; it
   prescribes an observable, not a criterion.

5. **Kill bars vs falsifiers:** Should any bars be promoted to
   falsifiers (immediate architecture rejection)? **Review
   recommends:** keep all as kill bars; falsifiers are for
   architecture-rule violations (ISA/mode/bridge), not capability
   shortfalls.

6. **C0-A regression strength:** Retain TNN-2's C0-A achievements
   as regression bars, or strengthen? **Review recommends:**
   retain without strengthening; the L3 advance is in B/C/D.

**Status:** DRAFT-NOT-FROZEN. Micah decides all six.

---

## 8. Summary: what this synthesis delivers

1. **Inventory:** 17 bars across 7 sources, each with its
   provenance commit.
2. **Dependencies:** Hard (K-TSEL needs K-REUSE; K-T3-CON-2 needs
   K-REUSE), soft (K-H3 conditions mechanism bars; K-T3-ADV governs
   all sealed bars), and cross-cutting (K-H3, K-T3-ADV apply
   everywhere).
3. **Order:** Step 0 (done) → Step 1 (H2 probes) → Step 2 (H3-lite
   + K-H3) → Step 3 (repair generator + inquiry resolution) →
   Step 4 (H1 widening + target selection, only after Step 1) →
   Parallel (reuse path). Full H3 banked for Micah.
4. **Conflicts:** None found. Three intentional overlaps
   (defense-in-depth). One tension (signature function) for
   Micah.
5. **Gaps:** Five identified (H2 has no kill bar; composition
   operators unbarred; informativeness criterion unbarred;
   cross-mechanism interference unbarred; verdicts-without-
   structures partially covered). Four explicit non-claims
   acknowledged.
6. **Structure:** 10-section preregistration outline ready for
   Micah's review and the 6 open questions.

---

## Verdict

PREREG-STRUCTURE-DRAFT-COMPLETE.

Structure drafting only. DRAFT-NOT-FROZEN. No implementation, no
source edits, no frozen thresholds. All 17 bars remain
DRAFT-NOT-FROZEN pending Micah's review of the 6 open questions
and the signature-function decision.

*End of synthesis. No source modified. No scores claimed. Paper untouched.*
