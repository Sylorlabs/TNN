# Failure Retention Analysis

**Status:** ANALYSIS ONLY. DRAFT-NOT-FROZEN. No implementation designed or proposed.
**Date:** 2026-10-01
**Frozen source:** `tnn2_build/tnn2.zag` (1591 lines, SHA-256 `a29972ca...`), read-only.
Cognition region: lines 1-917. Test battery begins at line 918.
**Verdict:** FAILURE-RETENTION-COMPLETE

---

## 0. Thesis

TNN-2 generates failure experience constantly and discards all of it. The
abandonment analysis (`ae76a60a7`) states the gap precisely: "the gap is not
missing experience but missing retention of experience about failure." This
document inventories every failure signal in frozen cognition, characterizes
exactly how each is discarded, defines what retention would mean, and ranks
the missing machinery by difficulty.

The pattern is consistent with the prior two "write half" findings: inquiry
built the write half of a goal system (goal origination, `3bf4d7bb4`); the
event log and trial stats are the write half of failure retention. In all
three cases the read half is missing, and the write half alone changes zero
production behavior.

---

## 1. Failure signal inventory

Seven distinct failure event classes in frozen cognition. All line numbers
refer to `tnn2_build/tnn2.zag`, cognition region (1-917).

### F1. Trial candidate rejection (`t2_try_verify`, lines 497-508)

Two distinct failure modes at the point of failure:

- Line 498: `if(root<0){return -2;}` -- candidate graph could not be assembled
  (invalid root). Information available: the attempted assembly parameters
  (caller context), subject `s0`.
- Line 507: `return -2;` after `set32(st,4,get32(st,4)+1);` -- candidate
  executed but failed verification. Information available: candidate root node
  id, executed value `v`, `expected`, `masked` flag, subject `s0`.

The `st` buffer counts tried (offset 0) and rejected (offset 4). These counts
survive the call: `t2_trial` packs them into header field 16 (line ~660:
`hs(W,16,get32(st,0)*1024+get32(st,4))`).

Discarded at this level: which candidate failed and why. The two modes
collapse into the same -2. Downstream code cannot distinguish "could not
build" from "built but wrong."

### F2. Trial exhaustion (`t2_trial`, lines 586-660)

All candidates tried in fixed order (chains k=2..4, then sums, then counts,
then single hops); none verified. Returns -2.

Information available at the point of failure: tried count, rejected count
(packed in hdr+16), the full (s, r, expected, masked, dc, di) query context,
and implicitly the set of candidates attempted (reconstructible from the
fixed search order and the gather results, but not recorded).

This is the failure the decline-signal analysis calls "pipeline exhaust."
The -2 it returns is indistinguishable from F1, F4, and F6 downstream.

### F3. Revision failure (`t2_revise_graph`, lines 706-749)

Five distinct 0-return sites, each a different failure with different
information:

- Line 717: `if(stale<0){return 0;}` -- no stale SETREG step found via
  provenance walk. Information: MAP id `m`, fact node, old/new values. The
  provenance graph did not contain the expected link.
- Line 723: `if(g<0){return 0;}` -- no BRANCHEQ guard pointing at the stale
  step. Information: same context; the graph topology did not match the
  single-schema assumption.
- Line 725: `let ly:i32=t2_lit(W,new_o); if(ly<0){return 0;}` -- literal
  allocation failed. Information: resource exhaustion during repair.
- Line 726: `let nst:i32=t2_set(W,0,ly); if(nst<0){return 0;}` -- SETREG cell
  allocation failed. Information: resource exhaustion during repair.
- Line 739: `return 0;` after re-execution produced -999999 -- the repaired
  graph does not execute. Information: the repair was structurally completed
  but semantically broken; the graph was reverted.

This is the richest failure signal in the system: five modes, each with MAP
id, fact provenance, and values attached. It is also the most thoroughly
discarded (see D1 below).

### F4. Bootstrap disagreement (`bootstrap_miss`, lines 763-787)

Two failure modes:

- Line 771: `if(cnt<2){return -2;}` -- fewer than 2 prior observations with
  relation `r`. Information: the actual count, the relation, the query.
  This is "insufficient evidence."
- Line 787: `return -2;` -- observations exist but disagree (or the k
  threshold not met). Information: the observed values in `ex_o`, the count,
  the unanimity flag `inv`, the threshold `k`. This is "evidence against."

Both collapse to -2. The distinction between "not enough evidence" and
"conflicting evidence" -- arguably the most decision-relevant distinction in
the system -- is erased at the return.

### F5. Resource exhaustion (`alloc_node`, lines 87-99)

Returns -1 when no free node slot exists and `evict_node` fails. Propagated
through approximately 20 call sites in cognition as -1 returns or silent
early returns (lines 99, 116, 130, 264, 299, 311, 339, 343, 347, 351, 355,
359, 366-369, 382-386, 392, 401, 405, 425, 534, 563, 717-739 passim).

Information available at the point of failure: which allocation was
attempted, in which function, in service of which (s, r) or repair. None of
it is recorded. A -1 from "node table full during miss_inquire" is
indistinguishable from a -1 from "literal allocation failed during revision."

Note: resource exhaustion is the only failure class that is also a system
health signal. Its discard means the system cannot distinguish "I cannot
learn this" from "I have no room to learn this."

### F6. Activation miss (`activate`, lines 140-152)

Returns -1 (`best<0`) when no live non-superseded FACT matches (s, r).
Information available: the (s, r) pair, and implicitly the candidate facts
that were scanned and rejected (bid too low, superseded, wrong key) -- none
recorded.

This miss triggers the entire downstream pipeline (trial, bootstrap,
inquire). It is the most frequent failure event and the entry point for F1,
F2, F4. The miss itself carries no memory: the next identical query repeats
the identical scan.

### F7. Event log entries (`log_ev`, lines 285-290)

The log records failure events: every `log_ev` call with `p1=0` marks a
failure (lines 834, 854, 862, 899). The log entry contains a timestamp
(`hg(W,0)`), event kind `k`, and four payload fields.

This is the system's only cross-cutting failure record. It is write-only in
cognition (see D3).

---

## 2. Discard characterization

### D1. Return-value discard (hard discard)

`t2_revise_graph` returns 0 on all five failure modes. The sole production
caller is `revise_on_contradict` (line 699): a bare call with the return
value discarded.

```zag
if(hit==1){t2_revise_graph(W,m,factn,old_o,new_o);}
```

Consequences, verified by reading `revise_on_contradict` (lines 685-704):
the stale MAP persists unrepaired; the contradicting observation is taught
as a new fact anyway (line 700+); the next contradiction on the same fact
re-fires the identical repair attempt. There is no record that a repair was
attempted and failed. The abandonment analysis correctly identifies this as
the "re-fire" loop: pursuit neither advances nor terminates.

This is the single most information-dense discard in the system. F3's five
modes, with MAP id and provenance attached, vanish into a void call.

### D2. Reason collapse (soft discard)

The -2 returned by F1, F2, F4, and F6 (via `ev_query` line 834) is
indistinguishable downstream. `ev_query` (lines 813-835) sequences
activate, trial, bootstrap, and miss on successive -2s, but no branch knows
*why* the previous stage failed:

- Trial cannot know whether activate missed for lack of facts or because all
  facts were superseded.
- Bootstrap cannot know whether trial failed for lack of candidates or
  failed verification.
- `miss_inquire` cannot know whether this (s, r) has missed once or a
  hundred times.

The decline-signal analysis (`9e0ae81d1`) identified this as the -2
overloading problem: five situations, one integer. The minus-two
disambiguation worker (active) is measuring the frequencies.

### D3. Write-only instrumentation (theater discard)

Three separate write paths record failure information that no production
code reads:

- **Trial stats** (hdr+16): written by `t2_trial` at every trial. Read only
  at line 1232, which is in the test battery (`t_t2_trial_reject`), not
  cognition. Zero production readers in lines 1-917. Theater instance T3,
  confirmed by source.
- **Event log** (`log_ev`): written at every event including failures.
  The log head `hg(W,28)` is read only at line 286, inside `log_ev` itself,
  to append. No production code reads any log entry. Zero production
  readers. Theater instance T4.
- **UNCERTAINTY nodes** (tag 30): written by `miss_inquire` per miss.
  The T30 ablation (`408bcfaa5`) empirically confirmed zero production
  behavior change when all are zeroed. Theater instance T5.

The pattern: the system *writes* failure experience in three places and
*reads* it in zero. The write half exists; the read half does not. This is
structurally identical to the inquiry finding (write half of a goal system,
no read path).

### D4. No counters (absence discard)

Exhaustive grep of cognition (lines 1-917) for `attempt`, `retry`,
`fail_cnt`, `n_fail`, `give_up`, `giveup`, `abandon`, `consecutiv`: zero
matches. There is no per-pursuit, per-query, or per-structure failure count
anywhere in the system.

The one quantitative failure record (trial tried/rejected in hdr+16) is
global to the workspace, overwritten per trial, and unread in production.
It cannot answer "how many times has *this* pursuit failed" because it does
not key by pursuit.

### D5. Silent propagation (context discard)

The -1 from `alloc_node` (F5) propagates through ~20 call sites without
accumulating context. By the time it surfaces (as a -1 return from
`ev_teach`, a silent return from `miss_inquire`, or a 0 from
`t2_revise_graph`), the information "which allocation, in which function,
for which purpose" is gone. The caller cannot distinguish resource
exhaustion from structural failure, and therefore cannot respond
differently (e.g., evict-then-retry vs. abandon).

---

## 3. Is any failure information retained? (The accidental remainder)

For completeness: four things that *are* retained, and why each is
insufficient for failure-driven decisions.

**R1. CON edges from contradiction.** `ev_observe` links a type-3
(self, self) edge on contradiction (line ~845), and `contradict_map` does
the same for MAPs. `activate` skips superseded facts; `bid` subtracts CON.
This is the ONE failure signal with a production read path. Limitations:
binary (contradicted or not, no gradation); about facts, not pursuits; no
count of *how many* contradictions; no record of *failed repairs* (D1
erases those).

**R2. Trial stats in hdr+16.** Retained but global, overwritten per trial,
unread in production. Cannot key by pursuit.

**R3. Event log entries.** Retained (up to 128 entries) but unread in
production. Contains timestamps and payloads that *could* reconstruct
failure histories, but nothing does.

**R4. UNCERTAINTY nodes.** Retained per (s, r) miss, but write-only and
unkeyed for lookup (no production query by (s, r) key). The dedup analysis
(`8510e327b`) and T30 ablation (`408bcfaa5`) confirm: outside every
production decision's causal chain.

Net: the system retains failure *marks* (R1) but not failure *experience*
(what was tried, how it failed, how often). R1 is a tombstone, not a
memory.

---

## 4. What retention would mean

### 4.1 Definition

Failure-experience retention = persistent, queryable records of *what was
attempted, how it failed, and in what context*, keyed so that future
decisions about the same pursuit can consult them.

Minimal viable form (supports abandonment criterion A1, "repeated failure"):

- **Key:** the pursuit. For TNN-2's query-driven architecture, the natural
  key is the (s, r) pair of the miss, or the MAP id of the failed repair.
- **Content:** a consecutive-failure count and the most recent failure mode.
- **Write path:** incremented on each failure event (F1-F6) for that key;
  reset on success.
- **Read path:** consulted before re-attempting (trial, revision, inquiry);
  when count exceeds a threshold, the pursuit is abandoned rather than
  retried.

This is deliberately minimal: one counter and one mode per pursuit, with a
production read path. Everything beyond this (history, context, graded
modes) is an extension, not a prerequisite.

### 4.2 How retained failures would be used

**U1. Abandonment (A1).** The direct consumer. N consecutive failures on a
pursuit → stop retrying. This is the missing middle "stop" from the
abandonment analysis. Without retained failures, A1 cannot be stated; the
criterion needs a count, and no count exists (D4).

**U2. Repeat-avoidance.** Before assembling a trial candidate, check whether
an identical candidate failed for this (s, r). Currently the fixed search
order re-attempts identical candidates on every identical miss. (Note: this
requires candidate identity, which the collapsed -2 does not provide; it
depends on un-collapsing F1's two modes at minimum.)

**U3. Decline input.** The decline analysis found no "should I answer?"
gate. Failure history is the natural input to such a gate: a pursuit with a
long failure record is a candidate for declining rather than guessing
(particularly in masked mode, where the trial currently accepts any
executable value).

**U4. Repair triage.** The discarded F3 modes distinguish "no stale step
found" (wrong blame target) from "repaired graph does not execute"
(structural repair failure) from "allocation failed" (resource problem).
Retained, these would direct different responses: re-blame, abandon repair
strategy, or free resources. Currently all five produce the same silent
re-fire.

**U5. Forgetting input.** The forgetting analysis needs to know what has
been abandoned to reclaim its structures safely. Retained failure records
are the input to principled forgetting: reclaim structures of abandoned
pursuits first, protect structures of live pursuits. Currently eviction is
blind to pursuit liveness (see fossil census, active).

### 4.3 The write-half/read-half framing

The system already has three write paths for failure information (D3). The
gap is not the absence of writing but the absence of reading. Any retention
proposal must include both halves to avoid a fourth theater instance:

- A counter with no production read path is T3 (trial stats) again.
- A log with no production reader is T4 (event log) again.
- A node with no production query path is T5 (UNCERTAINTY) again.

The theater audit's lesson applies directly: the unit of progress is not "a
place where failures are recorded" but "a record that a production decision
consults." The minimal retention in 4.1 is specified as a read-path-first
construct for this reason.

---

## 5. Gap analysis (ranked by difficulty)

### G1. Per-pursuit failure counters (least hard; new machinery required)

What is missing: a node or field keyed by pursuit (s, r) or MAP id, holding
a consecutive-failure count, with increment-on-failure and reset-on-success
in the production path.

Why it is not trivial: TNN-2 has no keyed lookup by (s, r) for non-FACT
nodes. `activate` queries FACTs by (s, r); there is no equivalent for
arbitrary bookkeeping nodes. Building one is new machinery (a small index
or a scan convention), not a parameter tweak. The counter must also live
through eviction without corrupting (see eviction corruption, `986c52fdc`:
integer field references are invisible to the evictor).

Treadmill risk: LOW if the counter is generic (any pursuit, any failure).
MEDIUM if per-failure-type counters proliferate into a taxonomy.

### G2. Failure-mode vocabulary (medium; treadmill risk)

What is missing: a retained record of *how* a pursuit failed, not just
*that* it failed. The five F3 modes and two F4 modes are the natural seed
vocabulary.

Treadmill risk: HIGH. A researcher-enumerated failure taxonomy
("verification-failed," "no-stale-step," "insufficient-evidence") is one
step from a researcher-enumerated repair dispatch -- the exact treadmill the
no-patch rule forbids. The honest version is a learner-derived vocabulary,
which does not exist. Any fixed vocabulary should be treated as provisional
scaffolding with an explicit retirement condition, not as architecture.

The minimal A1 criterion needs only the count (G1), not the mode. G2 is
required for U2 (repeat-avoidance) and U4 (repair triage), not for
abandonment itself. This ordering matters: build G1 before G2.

### G3. Failure history with temporal context (hard)

What is missing: *when* failures occurred and *in what learner-state
context*. A count answers "how many"; a history answers "is it getting
worse" (abandonment criterion A2, "no progress") and "did something change"
(premise undermined, A3).

What blocks it: TNN-2 has no temporal index over experience. The event log
has timestamps (`hg(W,0)`) but is write-only and capped at 128 entries. A
per-pursuit history needs either an unbounded append structure (resource
problem under the fixed 1024-node budget) or a compressed summary
(summarizing is itself a cognitive decision -- who chooses what to keep?).

### G4. Graded failure (hard; interacts with contradiction design)

What is missing: failure is currently binary (CON edge or not; -2 or not).
A pursuit that failed verification by a small margin is treated identically
to one with no candidates at all. Graded failure would let the system
distinguish "close, keep trying" from "hopeless, abandon."

What blocks it: the contradiction mechanism is binary by construction
(type-3 self-edge). Grading requires either a weighted contradiction
(a new edge semantic) or a separate confidence channel (the missing
correctness signal from the verification-criterion analysis, `c2a48bee6`).
This gap is downstream of the verification gap: you cannot grade failure
without a correctness-substitute computation.

### G5. Learner-owned failure categories (hardest; L3 territory)

What is missing: the system defining its own failure kinds from experience
rather than using researcher-enumerated modes. Example: discovering that
"chain candidates fail on this relation but count candidates succeed" is a
useful category, without the researcher predefining "chain" and "count" as
failure kinds.

Why it is hardest: this requires the representation-learning machinery
that is the primary frontier (generic executable representation substrate).
It is not a failure-retention problem per se; it is the L3 problem
reflected in the failure domain. Listed here to mark the asymptote, not as
a near-term target.

---

## 6. Relation to the three "stop" analyses

The abandonment analysis frames decline, abandonment, and forgetting as
three missing "stops" ordered by reversibility. Failure retention is the
shared prerequisite:

| Stop | Needs from failure retention |
|------|------------------------------|
| Decline (stop answering) | U3: failure history as gate input ("this pursuit keeps failing; withhold") |
| Abandonment (stop trying) | U1: consecutive-failure count as the A1 criterion input |
| Forgetting (stop keeping) | U5: abandoned-pursuit list as the safe-reclaim set |

Currently all three stops are missing, and the common cause is visible in
this inventory: the system generates the experience (F1-F7 fire constantly)
but retains none of it in queryable form (D1-D5). The one-bit summary from
the abandonment analysis holds: the gap is retention, not experience.

Note the dependency direction: retention enables the stops; the stops do
not enable retention. This means failure retention (G1 at minimum) is
upstream of all three stop capabilities. It is also upstream of the
verification gap's Component B (threshold with read and write paths):
a threshold on what, if not failure experience?

---

## 7. What this analysis does not claim

- It does not design the retention mechanism. G1-G5 are gap statements
  with difficulty rankings, not proposals.
- It does not claim G1 alone would produce abandonment. A counter with a
  source-fixed threshold N is a researcher decision, not a learner-owned
  one (abandonment analysis, A1 honest note). G1 enables the *statement*
  of A1; learner-owned thresholds are a further gap.
- It does not claim the F1-F7 inventory is exhaustive. It covers the
  cognition region (lines 1-917) by function-level reading and keyword
  grep. Opcode-level failures inside `t2_exec` (e.g., guard mismatches
  during execution) are candidate signals not inventoried here; they
  belong to a execution-failure sub-analysis if needed.
- It does not propose fixing D1 by using the `t2_revise_graph` return
  value. That would be a local patch; the structural point is that no
  consumer for failure information exists anywhere in the architecture.

---

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (analysis only; nothing built)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0 added
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0 added
- MODES: 0
- BRIDGES: 0
- HANDLERS: 0
- SEMANTIC CASES: 0

Failure signals inventoried: 7 (F1-F7). Discard mechanisms: 5 (D1-D5).
Accidentally retained: 4 (R1-R4), of which 1 (R1) has a production read path.
Gaps ranked: 5 (G1-G5). New machinery proposed: none.
