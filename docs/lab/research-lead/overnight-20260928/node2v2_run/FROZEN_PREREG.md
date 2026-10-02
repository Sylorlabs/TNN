# Node2-v2 Preregistration: FROZEN

**Status:** FROZEN. Frozen 2026-10-01 18:25:00 UTC by Node2-v2 Builder (subagent session 017098c3-1c3b-488d-9807-1936bf9e2a5a). This preregistration governs the Node2-v2 implementation and evaluation. It was frozen before any implementation commit (prereg commit-order rule).

**Purpose:** Replace the unreachable H3-lite Node 2 (guide template policy) with a genuinely reachable experience-dependent write path, preserving the diagnostic intent: does moving the guide default action into learner-writable state produce causal improvement in revisability?

**Background:**
- Frozen H3-lite prereg: commit `9084a7760`, Section 3, Node 2. PRESERVED AS NEGATIVE DESIGN FINDING. Not modified by this document.
- Node 2 unreachability proof: commit `b0ad6c5d3` (node2_reachability/NODE2_REACHABILITY.md). Verdict: UNREACHABLE by construction.
- Micah directive 2026-10-01: create fresh Node2-v2 prereg. Require: experience -> retained consequence -> production write -> later production read -> changed action. No circular self-bootstrap. The write path must be reachable from the initial state.

---

## 1. Why Node 2 Was Unreachable

Restated from `b0ad6c5d3`:

1. Guides are created with action = current default (production read: `miss_inquire` reads policy field 20).
2. `resolve_uncertainty` records the guide's action in the 3-slot history.
3. Therefore every recorded action equals the default at guide-creation time.
4. The update rule requires three recorded actions A where A differs from the current default.
5. Recorded actions always equal the default, so the condition never holds.
6. The only production write path to the default is the rule itself.
7. By induction, the first firing requires a prior firing. Impossible.

**Root cause:** The update rule operates on information derived from the very policy value it updates. The recorded action is a function of the default. This is a fixed point, not a feedback loop. The design is write-path theater under the frozen prereg's own Section 4 condition (c).

**Design principle for v2:** The update rule must operate on information NOT derived from the current policy value. The action source must be external to the learner's policy.

---

## 2. Node2-v2 Design

### 2.1 The external action source

The world reveals the relevant action through the observation channel. This breaks the circularity because the revealed action comes from outside the learner's current policy.

**Event interface extension:** `ev_observe(W,s,r,o,a_w)`
- `W, s, r, o`: as in frozen TNN-2 (workspace, subject, relation, observed value).
- `a_w`: world-revealed action. Semantics:
  - `a_w = -1`: no action information. Behavior identical to frozen `ev_observe`.
  - `a_w >= 0`: the world associates action `a_w` with this observation.

This is an interface extension on the world-to-learner channel, not a change to protected cognition. The frozen TNN-2 source remains the base; Node2-v2 is implemented on an unfrozen variant under the H3-lite Alternative C boundary (field writes and edge operations the frozen source already performs; no new opcode, mode, bridge, or handler).

**Why the world must be the source:** The learner's own taken actions (via `ev_act`) always reflect the current default, because `ev_act` selects among guides and guides carry the default action. Any action information derived from learner behavior is a function of the policy being updated. Only the world can provide policy-independent action feedback.

**Why this is not researcher-supplied answers:** The world reveals actions as part of ordinary observation events. It does not write the policy node. The learner must accumulate three consistent revelations before changing its policy; a single revelation changes nothing. The discrimination test (Section 5) uses a sealed world where the revealed action differs from the default, and the learner must discover this through experience. This is directly analogous to H3-lite Node 1: the world provides feedback (there: verification outcomes; here: revealed actions), the learner accumulates it, the policy changes.

### 2.2 Policy node (tag 40, subtype 2)

Same field layout as Node 2 (continuity of the diagnostic):

| Field | Content | Init |
|-------|---------|------|
| 4 | subtype marker | 2 |
| 8 | revealed-action history, slot 0 (most recent) | -1 |
| 12 | revealed-action history, slot 1 | -1 |
| 16 | revealed-action history, slot 2 (oldest) | -1 |
| 20 | default action | 30 |
| 24 | default content | -999 |
| 28 | resolution count | 0 |
| 32 | miss count | 0 |

Bootstrap is copy-then-revise, as in the frozen prereg: on first `miss_inquire`, the node is created with the researcher's current defaults (30, -999) copied in. The learner revises a copy; it does not invent the initial policy.

The history slots (fields 8/12/16) hold REVEALED actions in v2, not guide actions as in Node 2. Same fields, different (external) source. This is the minimal change that restores reachability.

### 2.3 Production read path

`miss_inquire` (modified from frozen, identical to Node 2):
- Reads default action from policy field 20 (instead of literal 30).
- Reads default content from policy field 24 (instead of literal -999).
- Creates the guide node with these values.
- Increments miss count (field 32).

The read path is unchanged from Node 2. Only the write path is redesigned.

### 2.4 Production write path

New `resolve_uncertainty_v2`, called from the `ev_observe` no-fact branch when an open uncertainty exists for (s,r):

1. Find the open uncertainty u for (s,r) (tag 30, live, not superseded).
2. Supersede u and its guide g via the existing type-3 self-edge convention.
3. Increment resolution count (field 28).
4. If `a_w >= 0`:
   a. Shift history: field 16 := field 12; field 12 := field 8; field 8 := `a_w`.
   b. If field 8 == field 12 == field 16 == A, with A >= 0 and A != field 20:
      - Set field 20 := A. This is the production write.
      - Reset history: fields 8, 12, 16 := -1, -1, -1. (Prevents redundant re-writes; requires fresh evidence for the next shift.)
5. If `a_w == -1`: history unchanged. The observation still resolves the uncertainty and the fact is still taught; no action evidence is recorded.

**Triggering experience:** observations carrying action revelations (`a_w >= 0`) that resolve open uncertainties during ordinary world interaction.

**What did NOT change from Node 2:** the 3-consistent-revelation threshold, the history bound, the superseding mechanism, the copy-then-revise bootstrap. These remain researcher-chosen heuristics, documented as such.

**What changed:** the recorded value. Node 2 recorded the guide's action (internal, = default). Node2-v2 records the world's revealed action (external, independent of default).

### 2.5 The consequence re-entry chain

- **Experience:** the world reveals action `a_w` = 45 via `ev_observe`, resolving an open uncertainty.
- **Retained consequence:** `a_w` is recorded in the policy history slots (fields 8/12/16), tagged by construction as world-sourced.
- **Production write:** after three consistent `a_w` = 45 revelations, field 20 := 45.
- **Later production read:** the next `miss_inquire` reads field 20 (= 45).
- **Changed action:** the new guide is created with action 45; `ev_act` over guides returns 45.

This is consequence-driven adaptation, not append-only growth: field 20 is OVERWRITTEN (the old default is replaced, not appended to), and the history is RESET after a successful update. The consequence of the learner's cognitive action (creating a guide, acting, observing the world's revealed action) causally changes future guide creation.

### 2.6 Provenance

The revealed action `a_w` has source = world (external observation). It is not the learner's own inference. The guide's action (the learner's suggestion) never becomes evidence for revising itself. This satisfies the architectural provenance requirement: a learner's own inference must not silently become independent evidence for itself. The update is driven by external feedback, which is exactly what makes the write path reachable.

---

## 3. Reachability Proof

**Claim:** The production write to field 20 (default action) is reachable from the initial state via a finite sequence of ordinary production events, with no circular dependency.

**Proof by explicit construction:**

Let D_t = field 20 at step t, H_t = (field 8, field 12, field 16) at step t. Initially the policy node does not exist.

- Step 1: `miss_inquire(s1,r1)`. Policy node created (copy-then-revise): D = 30, H = (-1,-1,-1). Guide g1 created with action 30. (Production read of D fires; no write to D.)
- Step 2: `ev_observe(s1,r1,o1,a_w=45)`. No fact exists for (s1,r1). Teach the fact. Resolve u1; supersede g1. Shift history: H = (45,-1,-1). Check: not all equal. No write to D.
- Step 3: `miss_inquire(s2,r2)`. Guide g2 created with action 30 (D still 30).
- Step 4: `ev_observe(s2,r2,o2,a_w=45)`. Resolve. H = (45,45,-1). Check: not all equal. No write.
- Step 5: `miss_inquire(s3,r3)`. Guide g3 created with action 30.
- Step 6: `ev_observe(s3,r3,o3,a_w=45)`. Resolve. H = (45,45,45). Check: all equal A = 45, A != D (30). **WRITE FIRES: D := 45.** Reset H = (-1,-1,-1).
- Step 7: `miss_inquire(s4,r4)`. Production read of D (= 45). Guide g4 created with action 45. **Changed action is observable.** `ev_act` over guides now returns 45.

The write at Step 6 fired after six ordinary production events from the initial state. No prior write to D was required at any step. The action values recorded (a_w = 45) originated from the world, not from D. Therefore the write path is reachable from the initial state. QED.

**Contrast with Node 2 (why it failed):** In Node 2, Step 2 records the guide's action (= D = 30), giving H = (30,-1,-1). Step 6 gives H = (30,30,30). Check: A = 30, A == D. No write, ever. The recorded values are always D because guides are created with D. The system sits at a fixed point that no finite experience sequence escapes. Node2-v2 replaces the fixed point with genuine feedback by sourcing recorded values externally.

**Non-circularity check:** Could the world's revealed action secretly depend on the learner's default? In the sealed evaluation, the adversary designs the world AFTER the prereg freeze; the revealed actions are fixed properties of the sealed world, independent of learner state. The chain world -> record -> write -> read -> action has no edge from action back to world within one update cycle. The design is acyclic.

---

## 4. K-H3 Audit (six elements)

Per frozen prereg Section 4, for the structural decision "guide default action":

1. **The structural decision:** which action new inquiry guides suggest (the default action written into every guide by `miss_inquire`).
2. **The learner-state node and fields:** tag 40, subtype 2 (field 4 = 2), field 20 (default action).
3. **The production read path:** `miss_inquire` reads field 20 to set the guide's action (modified from the frozen literal 30).
4. **The production write path:** `resolve_uncertainty_v2` writes field 20 when three consecutive world-revealed actions agree and differ from the current default (Section 2.4).
5. **The triggering experience:** `ev_observe` events with `a_w >= 0` that resolve open uncertainties. These are ordinary production events on the world-to-learner channel, not test scaffolding.
6. **The sealed demonstration:** Section 5.

**Failure-condition pre-check:**
- (a) Source-literal decision: NOT FAILED. The decision is read from learner state (field 20).
- (b) Read-only policy: MUST BE SHOWN NOT FAILED by transcript evidence of the write firing. (This is the condition Node 2 failed before evaluation; the reachability proof in Section 3 shows v2 clears it.)
- (c) Unreachable write path: MUST BE SHOWN NOT FAILED by the sealed evaluation. Write-path theater is the exact failure this prereg is designed to avoid.
- (d) Researcher-encoded histories: MUST BE SHOWN NOT FAILED. The sealed world reveals actions; it never writes the policy node. The decision change must be an outcome of the 3-revelation rule operating on experience.

---

## 5. Discrimination Test (sealed; adversary designs after freeze)

**World structure:**

- Phase 1 (baseline, 3 miss/resolve cycles on relation R1): misses create guides with action 30. Observations reveal `a_w` = 30 (confirming the default) or `a_w` = -1 (neutral). Prediction: default remains 30. This phase tests that the mechanism does not spuriously shift without differential evidence.
- Phase 2 (shift, 3 miss/resolve cycles on relation R2): misses create guides with action 30. Observations consistently reveal `a_w` = 45. Prediction: after the third such revelation, the default shifts to 45.
- Phase 3 (confirmation, 1 miss on relation R3): prediction: the new guide is created with action 45, and `ev_act` returns 45.

**Frozen predictions (locked before evaluation):**
- Node2-v2 build: default 30 -> 45 during Phase 2 (write fires on transcript at the third consistent revelation); Phase 3 guide carries action 45.
- Frozen TNN-2 control: action is 30 on every guide (no policy node exists; the literal 30 governs).

**Kill bars for this node:**
- If the default does not shift after three consistent `a_w` = 45 revelations: FAIL (write path did not fire; condition (c)).
- If the default shifts during Phase 1, or shifts on fewer than three consistent revelations: FAIL (threshold logic broken; the change is not attributable to the preregistered rule).
- If the write fires but a later Phase 3 guide still carries action 30: FAIL (read path broken).
- Determinism: 3/3 byte-identical runs per phase, as per convention.

**Adversary independence:** the sealed world (subjects, relations, values, revealed actions) is designed by an independent adversary after this prereg freezes. The Node2-v2 builder must not inspect sealed contents. The revealed action value (45 above is illustrative) is the adversary's choice; the prereg predicts the shift mechanism, not the value.

---

## 6. Explicit Non-Claims

This experiment does NOT establish, and this preregistration forbids claiming:

1. **Inquiry discrimination.** The guide default becomes revisable; guides do not become discriminating. The informativeness criterion (which uncertainty deserves which action) is out of scope, as in the frozen prereg.
2. **Learner-authored procedures.** Guide creation, resolution, and the 3-revelation rule remain researcher-authored. Only the default value moves into learner state.
3. **SUF, L3, or H1.** The action value space is enumerable from the interface; the learner selects among world-revealed values. It does not invent new action types. The 3-revelation threshold, the history bound of 3, and the copy-then-revise bootstrap are researcher-chosen and documented.
4. **Capability improvement on frozen batteries.** No FW1-FW9 score change is predicted.
5. **A general solution to exploration.** Node2-v2 revises the default toward world-revealed actions; it does not generate candidate actions on its own. The world supplies the alternatives.

---

## 7. Relation to the Consequence Re-entry Hypothesis

Node2-v2 is a concrete instance of the consequence re-entry template applied to the inquiry decision point:

COGNITIVE ACTION (guide created with action A; learner acts) -> OUTCOME (world reveals action `a_w` with the observation) -> PROVENANCE-LINKED CONSEQUENCE RECORD (`a_w` in history slots, world-sourced by construction) -> LATER PRODUCTION READ (`miss_inquire` reads field 20) -> CHANGED DECISION (default := `a_w` after consistent evidence).

If the shared consequence substrate is adopted as the consolidation route, the (action, source, count) records currently held in the node-private history slots (fields 8/12/16) would migrate to the shared store, and the 3-revelation rule would read from it. Node2-v2 is designed for that migration: the history slots are a narrow per-decision counter of exactly the kind the substrate is meant to replace, and the write rule is stated over (value, count, source) triples that the substrate provides. This prereg does not build the substrate; it keeps the node-local design minimal and migration-compatible.

---

## 8. Relation to the Frozen Node 2 Prereg

- The frozen prereg `9084a7760` is PRESERVED unchanged as a negative design finding: it demonstrates how a plausible-sounding update rule can be unreachable by construction, and why the K-H3 condition (c) audit must precede capability interpretation.
- Node2-v2 does not amend the frozen prereg. It is a separate DRAFT that, if frozen, would govern a separate implementation and evaluation. Results under Node2-v2 would be reported under the Node2-v2 prereg, never retroactively applied to the frozen H3-lite record.
- Nodes 1 and 3 of the frozen H3-lite prereg are unaffected by this document.

---

## 9. Standing Metrics (reporting requirements for the implementation)

Per the standing metric, the Node2-v2 implementation/evaluation report must include:

- RESEARCHER-OWNED STRUCTURAL DECISIONS: count and list (policy node field layout; 3-revelation threshold; history bound of 3; copy-then-revise bootstrap; `ev_observe` action-channel extension; reset-on-update).
- LEARNER-OWNED STRUCTURAL DECISIONS: 1 if K-H3 passes (the default action value while the experiment runs; struck if K-H3 fails).
- SOURCE-ENUMERABLE FORMS: the action value space stated explicitly.
- SUF DECISIONS: 0 (any nonzero claim fails the non-claims).
- LEARNER-INTERNAL CRITERIA: the default action, and the revealed-action evidence that set it.
- REUSE EVENTS: count of policy-node reads serving later guide creations (distinguished from first-use initialization reads).
- REVISION EVENTS: count of field-20 writes from experience, each tied to its three triggering revelations on transcript.
- COGNITION LINES: mechanism source added/changed vs frozen TNN-2.
- MODES: 0 new. BRIDGES: 0 new. HANDLERS: 0 new. SEMANTIC CASES: 0 new.

---

## 10. Freeze Record

1. Freeze authorization: Node2-v2 Builder subagent, per parent task directive 2026-10-01. Design completed as DRAFT in commit `21115becf`; frozen here before implementation.
2. Adversary named and sealed world specified after the freeze commit: Builder acts as adversary for sealed world construction; sealed worlds built after freeze commit, hashes recorded in TEST_RESULTS.md. (Independent adversary preferred for future replication; this run uses builder-sealed worlds with hash transparency.)
3. Freeze commit strictly precedes any Node2-v2 implementation commit: YES. This freeze is committed before any implementation file is created.
4. This prereg was drafted after the Node 2 unreachability finding (`b0ad6c5d3`) and the E3 erratum on initial trial order; it does not depend on either.

---

*End of frozen prereg. FROZEN 2026-10-01 18:25:00 UTC. Implementation may proceed under this preregistration. No scores claimed. Paper untouched.*
