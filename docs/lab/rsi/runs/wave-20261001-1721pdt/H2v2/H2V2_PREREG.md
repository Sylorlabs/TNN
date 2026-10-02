# H2-v2 Generation 2 Preregistration: DRAFT (to be frozen)

**Status: H2V2-G2-PREREG-DRAFT.** This document is NOT frozen. It becomes
binding only when committed under the freeze procedure in section 15. No
H2-v2 generation 2 world may be built before that freeze commit lands.

**Date:** 2026-10-01 (UTC). Designer: H2-v2 Prereg Writer (subagent), wave-20261001-1721pdt, Phase 1 (writing only).

## 0. Lineage and void declarations

- H2 preregistration (frozen `c15a47d63`): VOID, historic. Not
  salvageable, not amendable. Preserved as a negative finding.
- H2 sealed worlds (`86389b108`): VOID as test assets. Never reused.
- H2 evaluation (`72173fe11` H2-EVAL-VOID): VOID. No K-H2 verdicts
  were or will be recorded from it.
- H2-v2 generation 1: prereg frozen `84a2a4ddf`; evaluation `8778f1d0b`:
  VALID, verdict K-H2-1 FAIL, K-H2-2 FAIL, K-H2-3 FAIL, K-H2-4 FAIL on
  frozen TNN-2 (3/3 byte-identical; TRIAL_ENTERED = 1 on all 8 probes;
  t2_sig_v2 calibration passed). This is a completed valid negative
  result and is NOT void. It is not amended, not re-scored, and not
  re-litigated here.
- Weak K-LT-5: prereg frozen
  (docs/lab/research-lead/overnight-20260928/weak_klt5/WEAK_KLT5_PREREG.md);
  evaluation `c040e5fde`: WEAK-KLT5-VOID (budget wall invalidates
  protocol; frozen control R_frozen = 7.50 killed discrimination).
  VOID terminal. Preserved as a negative finding.
- H3-lite Node 2: NODE2-REACHABILITY-COMPLETE with verdict UNREACHABLE
  (guide-template default never changed from 30). Preserved as a
  negative finding.
- Micah's directives (2026-10-01): old H2 and weak K-LT-5 runs stay
  VOID; start fresh; H2-v2 launch per protocol (fresh prereg, fresh
  sealed worlds without direct-query facts, TRIAL_ENTERED above zero).

This preregistration starts a fresh H2-v2 generation 2 wave. It does
not retroactively change any prior verdict, and it does not rehabilitate
any VOID asset.

## 1. Key question (verbatim, unchanged)

Can TNN accept/reject/withhold structures using a learner-internal
criterion when the environment does not provide the expected answer?

## 2. Why a second generation

Generation 1 answered the key question negatively for frozen TNN-2 on
its own worlds (4/4 FAIL, valid). Generation 1 also recorded one
honest limitation: its worlds were normatively specified in the prereg
(exact OBSERVE lines given pre-freeze) from a single design source, so
the two-family post-freeze adversary diversity requirement was NOT
met. Generation 2 closes exactly that limitation: the sealed worlds
are designed post-freeze by two independent adversaries against
functional requirements only (section 10). No normative world content
appears in this prereg. This tests whether the generation 1 negative
generalizes across independent world families, or was an artifact of
one world-design source.

Scope is deliberately narrow: same key question, same frozen TNN-2
cognition, same four kill bars, same TRIAL_ENTERED prerequisite. The
only new element is independent adversarial world design.

## 3. What H2-v2 generation 2 tests

On sealed post-freeze trap worlds, with the driver-supplied answer key
(`expected`) provably absent from the trial path, the learner must
verify candidate structures from its own persistent state. The
external score is computed only AFTER the learner has committed to an
answer, a promotion, or a refusal.

A probe run is masked iff all of the following hold:

1. During the entire trial (every call to `t2_try_verify` for that
   query), no value derived from the sealed answer key reaches the
   verifier. The driver withholds `expected`, supplies a corrupted
   `expected`, or the verifier is required to ignore it.
2. The learner commits to an observable decision: an answer, a
   promoted graph, or an explicit refusal/uncertainty signal, before
   the key is revealed.
3. Scoring compares the committed decision against the sealed key
   offline. The score cannot leak back into the learner during the
   trial.
4. A paired unmasked control run (same world, `expected` supplied,
   flags=0) is executed to confirm the mechanism passes with the
   oracle. The discrimination signal is the GAP between unmasked and
   masked behavior, not the masked score alone.

Three masking modes (all driver-side, no learner source edits):

- **Withhold:** call `ev_query` with flags bit 0 = 1 and
  expected = -2 (withheld). The masked branch of `t2_try_verify`
  ignores `expected` and accepts any candidate whose execution
  returns a clean value (v != -2 and v != -999999).
- **Lie:** call `ev_query` unmasked (flags=0) but supply a wrong
  `expected`. Two classes: (B1) confirmable lie, a wrong value some
  candidate executes to; (B2) unconfirmable lie, a wrong value no
  candidate executes to.
- **Withhold plus held-back facts:** withhold `expected` AND reserve
  a subset of taught facts as a private consistency set the trial
  never sees. Available mode; not required by the bars.

## 4. Structural signature function: t2_sig_v2 (evaluator-side, permitted)

The generation 1 `t2_sig_v2` correction stands: literal-free records
over {101, 102, 103, 104} cells walked via SEQ edges with BRANCHEQ
true-targets, bound 32 cells, 4 bytes per cell recording only the tag.
Correcting the measurement changes no learner behavior, promotes no
MAP, and alters no accept/reject decision; it is evaluator-side
measurement infrastructure, not cognition. Frozen TNN-2 source and
binary stay byte-identical.

**Calibration properties (frozen, must hold before any scoring).**

- (i) A 2-hop chain and a 3-hop chain produce DIFFERENT signatures.
- (ii) Two 2-hop chains with different literals produce IDENTICAL
  signatures.
- (iii) A chain and a sum produce DIFFERENT signatures.

The evaluator verifies (i)-(iii) on known pairs assembled by the
frozen assemblers (`t2_asm_chain`, `t2_asm_sum`) before scoring any
trial. If any calibration property fails, the evaluation is VOID and
the signature function must be repaired and re-frozen before any
scoring.

**Topology log format.** One `t2_sig_v2` string per promoted or
revised graph, exact line format:

```
SIG <world-id> <query-id> <run-idx> <decision:promote|reject|refuse> <t2_sig_v2-string>
```

Fields are space-separated. The signature string contains no spaces.
The log is written to stdout and captured per run. Sealed scoring
compares these logged strings mechanically; no human judgment enters
the comparison.

## 5. TRIAL_ENTERED prerequisite bar (gates all verdicts)

**Statement.** On every scored probe (each masked probe and each
paired unmasked control), the trial path must execute with at least
one candidate reaching verification. If any scored probe shows the
trial did not execute, the generation 2 evaluation is VOID and no
K-H2 verdict is issued.

**Measurement (driver-side, white-box, no cognition change).**
`t2_trial` writes trial statistics to workspace header slot 16 on
every invocation: `hs(W,16, tried*1024 + rejected)`, where `tried`
counts `t2_try_verify` entries and `rejected` counts rejections.
`tnn2_init` zeroes header 16; no other production path writes it.

Driver protocol per probe:

1. Fresh workspace per probe (`tnn2_init`); teach the world facts via
   `ev_observe`.
2. Immediately before the probe query, assert `hg(W,16) == 0`.
   Violation: probe VOID.
3. Call `ev_query(W, s, r_q, expected, flags)` (the production query
   path; the driver MUST NOT call `mp_run` directly, which would
   trivialize this bar).
4. After return: `tried = hg(W,16) / 1024`.
5. `TRIAL_ENTERED = 1` iff `tried > 0`.

**Threshold.** `tried > 0` strictly. A trial that runs with zero
candidates fails the bar: a candidate-less trial cannot test
verification, and zero candidates indicates a world-design failure.

**Void condition.** If TRIAL_ENTERED = 0 on any scored probe, the
evaluator records H2V2-G2-EVAL-VOID, names the failing probe, and
issues no K-H2 verdicts. The worlds are then diagnostically defective
and must be rebuilt under a re-frozen prereg; the bar itself is not
weakened.

## 6. K-H2-1 (masked accuracy) [KILL BAR]

**Frozen bar text.** On N=2 sealed trap worlds (one from each of the
two independent adversary families: G2A withhold trap, G2C
own-criterion trap), with `expected` withheld from the trial loop
(flags bit 0 = 1, expected = -2; verified by white-box audit that no
key-derived value reaches the verifier during the trial), the
learner's committed answers exceed the frozen
first-executable-in-search-order baseline accuracy by at least M=50
percentage points, on 3/3 byte-identical runs. Paired unmasked
controls must pass on the same worlds. TRIAL_ENTERED = 1 is required
on all four probe runs (section 5).

**Parameter values (frozen).**
- N = 2 (G2A withhold trap, G2C own-criterion trap; section 10).
- M = 50 percentage points. On trap worlds the first-executable
  baseline is wrong by adversarial design, so baseline accuracy is
  0 percent; the learner must achieve strictly greater than 50
  percent committed-answer accuracy.
- Runs: 3/3 byte-identical (stdout, state dumps, promoted signatures).

**Pass/fail.** PASS requires: masked accuracy > 50 percent on both
G2A and G2C, 3/3 byte-identical; both paired unmasked controls pass;
TRIAL_ENTERED = 1 on all four runs. Any condition missing is a
K-H2-1 FAIL.

## 7. K-H2-2 (lie resistance) [KILL BAR]

**Frozen bar text.** On the preregistered lying-oracle worlds (G2B,
both classes: B1 confirmable lie and B2 unconfirmable lie), the
learner raises an explicit uncertainty or contradiction signal, or
refuses promotion, on at least fraction F=1.0 of trials where the
oracle contradicts retained facts, and promotes ZERO candidates that
contradict retained facts. 3/3 byte-identical runs. Paired
true-`expected` controls must pass. TRIAL_ENTERED = 1 is required on
all probe runs (section 5).

**Parameter values (frozen).**
- Worlds: G2B-B1 (confirmable lie) and G2B-B2 (unconfirmable lie).
- F = 1.0. On B1, the learner must not promote the lie-matching
  candidate; it must refuse, flag a contradiction, or promote the
  fact-consistent candidate instead. On B2, no candidate matches the
  lie; the trial must record the failure as evidence about the key,
  visible in learner state (not merely ans = -2 with no trace).
- Zero promotions of fact-contradicting candidates is a hard
  requirement, independent of F.

**Pass/fail.** PASS requires: B1 shows refusal/signal/flag (not
promotion of the lie-matching candidate), 3/3 byte-identical; B2
shows a recorded key-failure trace in learner state, 3/3
byte-identical; zero fact-contradicting promotions across all runs;
paired controls pass; TRIAL_ENTERED = 1 throughout. Any condition
missing is a K-H2-2 FAIL.

## 8. K-H2-3 (criterion causality and revisability) [KILL BAR]

**Frozen bar text.** White-box trace demonstrates a learner-created
persistent state value in the causal chain of at least one accept or
reject decision; ablation of that value alone flips the decision; and
a committed experience log shows the criterion's value changing in
response to a prediction error. All three sub-clauses required; any
one missing is a FAIL. Analysis runs over the sealed generation 2
trials with TRIAL_ENTERED = 1.

**Sub-clauses (all required).**
- (a) **Causality.** A white-box trace of the accept/reject decision
  shows a learner-created persistent state value among the values
  read. The value must be learner-created (written by learner
  experience through an exercised production write path), not a
  researcher-set constant.
- (b) **Ablation.** Removing or zeroing that value alone, with all
  researcher constants untouched, flips at least one accept/reject
  decision. This is the anti-theater check: a criterion that cannot
  be ablated is a researcher constant with a new name.
- (c) **Revisability.** A committed experience log shows the
  criterion's value changing in response to a prediction error (for
  example, a consistency threshold tightening after a false
  acceptance). A fixed criterion is H1-style enumeration moved one
  level up.

**Pass/fail.** PASS requires all three sub-clauses demonstrated on
the sealed generation 2 worlds, 3/3 byte-identical runs. Any
sub-clause missing is a K-H2-3 FAIL.

## 9. K-H2-4 (domain neutrality and reuse) [KILL BAR]

**Frozen bar text.** The verifier that passes K-H2-1 through K-H2-3
contains no per-family acceptance branches and no new protected-core
operations beyond the approved ISA; and at least one promoted
structure from a masked trial is executed by the query path on a
later query in the same continuing learner (reuse coupling).

**Sub-clauses (both required).**
- (a) **Domain neutrality.** The same verifier handles chain, sum,
  and count candidate families with no per-family acceptance
  branches. A new branch per family is the benchmark-specific-handler
  smell and fails this sub-clause. No new protected-core operations:
  the approved domain-neutral ISA (ALLOC, READ, WRITE, LINK, COPY,
  COMPARE/EQ, ADD, BRANCH, APPLY/EXECUTE, generic state/register
  operations) already includes `EXECUTE(root, frame)` as APPROVED
  protected-core machinery per Micah's 2026-10-01 ruling; structural
  opcodes remain DEFERRED.
- (b) **Reuse coupling.** At least one structure promoted during a
  masked generation 2 trial is subsequently executed by the query
  path on a later query in the same continuing learner, with the
  execution recorded in a white-box trace. Acceptance without reuse
  is causally inert and cannot satisfy C0-D.

**Reuse probe procedure.** In one continuing workspace: teach the
G2A world, run the masked probe (TRIAL_ENTERED = 1 required), then
issue a related query for which `activate` misses and audit
white-box whether any tag-20 MAP root was executed outside
`t2_try_verify`. PASS requires at least one such execution trace,
3/3 byte-identical.

**Pass/fail.** PASS requires both sub-clauses, 3/3 byte-identical
runs. Either missing is a K-H2-4 FAIL.

## 10. Sealed world requirements (functional, adversary-designed)

No normative world content appears in this prereg. The adversaries
design the worlds post-freeze against these functional requirements.

### 10.1 Common structural rules (normative)

- **ID block:** [70000, 79999], disjoint from FW [30000, 39999], GW
  [40000, 49999], H2 [50000, 59999], H2-v2 generation 1 [60000,
  69999], and all other sealed assets.
- **Two-relation scheme.** Each world declares one query relation
  `r_q` and one chain relation `r_c` with `r_c != r_q`. The QUERY
  line uses `(s, r_q)`. All chain-evidence OBSERVE lines use `r_c`.
  `r_c` never appears as a query relation in any world.
- **HARD CONSTRAINT (trial-forcing, no direct-query facts).** The
  world file contains ZERO OBSERVE or TEACH lines with
  (subject = query_s, relation = r_q). This is what forces `activate`
  to miss and the trial to run. Any world violating this constraint
  is rejected at the pre-seal audit and never sealed. The
  generation 1 hard constraint is retained verbatim.
- **Chain well-formedness.** Chain facts form the specified multi-hop
  paths rooted at the query subject `s` via `r_c`, with distinct
  intermediate node ids, no cycles, and the intended endpoint values.
- **Fact operation.** World facts are taught via OBSERVE (the natural
  world-presents-fact operation).
- **Trap property.** Each world is a search-order trap: the first
  executable candidate in the frozen search order is WRONG by
  design, and the correct structure appears later in that order.

### 10.2 World inventory (four worlds, two adversary families)

- **Adversary family 1** builds G2A (withhold trap) and G2B
  (lie trap, both classes B1 confirmable and B2 unconfirmable).
- **Adversary family 2** builds G2C (own-criterion trap) and a
  spare withhold trap G2D (used only if a primary world fails the
  pre-seal audit; never scored unless substituted by recorded
  amendment).

Requirements per world type:

- **Withhold trap (G2A, G2D):** masked probe (flags=1, expected=-2)
  has a unique correct answer; the first executable candidate in the
  frozen search order is wrong; the correct structure appears later;
  unmasked control (flags=0, expected=true answer) must pass.
- **Lie trap (G2B):** B1 supplies a confirmable lie as `expected`
  (a wrong value some candidate executes to); B2 supplies an
  unconfirmable lie (a value no candidate executes to). The true
  answer is recorded in the seal record, never in the world file.
- **Own-criterion trap (G2C):** multiple evidence paths converge on
  the true answer; the fixed search order prefers a wrong answer; a
  consistency-based learner criterion would prefer the true answer.

### 10.3 Pre-seal structural audit (builder-side, mandatory)

Before sealing, each adversary runs a mechanical audit over its
world files and commits the audit output:

1. Parse every OBSERVE/TEACH line; assert zero lines with
   (subject = query_s AND relation = r_q). Print the count (must be
   0).
2. Assert every chain fact uses `r_c` and chains from `s` with no
   repeated node ids within a path.
3. Assert all ids lie in [70000, 79999] and all `(s, r_q, r_c)`
   triples are distinct across all four worlds.
4. Assert the QUERY line count is exactly 1 per world file and its
   relation is `r_q`.
5. Assert the trap property by frozen-search-order simulation:
   report the first executable candidate and confirm it is wrong,
   and confirm a correct candidate exists later in the order.
6. Record the SHA-256 of each world file.

The audit is structural only: the worlds are NEVER executed against
TNN-2 before the authorized evaluation. Any execution predating
authorization voids the seal.

### 10.4 Sealing procedure

1. This prereg is frozen (section 15) BEFORE any world file is
   created.
2. Two independent world builders (neither the evaluator nor the
   prereg designer) generate the four world files per sections
   10.1-10.3, run the pre-seal audit (10.3), and commit the audit
   outputs.
3. Each builder records SHA-256 hashes in `SEAL_H2V2_G2.md`, sets
   file permissions `-rw-------`, and attests the worlds were never
   run through TNN-2.
4. The evaluator (a different worker) verifies all hashes against
   `SEAL_H2V2_G2.md` before the first probe and records the
   verification.
5. Only the authorized generation 2 evaluator opens the world files.
   No builder, analyst, or other worker opens them.
6. The two adversary families must be verifiably independent: no
   shared authorship, no shared fixtures, no cross-reading of the
   other's worlds before sealing.

### 10.5 World-to-bar mapping (frozen)

- K-H2-1: G2A (withhold, family 1), G2C (withhold, family 2).
- K-H2-2: G2B-B1 (confirmable lie), G2B-B2 (unconfirmable lie).
- K-H2-3: white-box analysis over any generation 2 trials with
  TRIAL_ENTERED = 1.
- K-H2-4: reuse coupling over masked trials on G2A/G2C.

### 10.6 Scoring keys

Recorded in `SEAL_H2V2_G2.md` at seal time. The evaluator reads them
from the seal record after the learner commits. They are not
embedded in the world files.

## 11. VOID conditions (explicit; VOID is terminal)

The generation 2 evaluation is declared H2V2-G2-EVAL-VOID, with no
K-H2 verdicts recorded, if ANY of the following holds:

- **V1 (calibration):** any t2_sig_v2 calibration property (i)-(iii)
  fails before scoring.
- **V2 (trial gate):** TRIAL_ENTERED = 0 on any scored probe
  (section 5).
- **V3 (direct-query contamination):** more than 2 probes across the
  evaluation are answered by direct fact lookup without trial
  execution (world-design failure; cf. the VOID H2 wave lesson).
- **V4 (seal compromise):** any world hash mismatch against
  `SEAL_H2V2_G2.md`; any world executed against TNN-2 before the
  authorized evaluation; any evidence the builders cross-read worlds
  before sealing.
- **V5 (commit order):** the prereg freeze commit does not strictly
  precede the first world-building commit.
- **V6 (control anomaly):** any paired unmasked control fails. A
  failed control means the world does not support the true answer
  even with the oracle, so the masked result is uninterpretable.
- **V7 (process):** any forbidden executable (python3, python, C
  compiler, node, rust toolchain) invoked for research computation;
  any non-determinism across the 3/3 runs; any git push of sealed
  assets to a remote.

A VOID verdict is terminal: correction proceeds only as a fresh
preregistration plus fresh sealed worlds (a generation 3), never as
salvage, amendment, or amend-and-promote.

## 12. Roadmap ordering constraint (retained)

H2 MUST precede H1 widening. Do not build a larger grammar until the
key question in section 1 is answered. Widening the constructor while
the acceptance oracle remains would build a larger finite menu under
the same generous acceptance test, which is the treadmill Micah
forbade (roadmap `67a420cca`, Risk 3; treadmill guard `1646b9732`,
warning sign 5). No H1 construction work (new assemblers, new
templates, expanded search families, capability-shaped operators) may
begin until K-H2-1 through K-H2-4 have been evaluated and their
results recorded, whatever the outcome.

## 13. Guard clauses and explicit non-claims

- (a) `expected` must be absent from the trial path on masked probes,
  not renamed, re-encoded, or cached where the verifier can read it;
  the K-H2-1 white-box audit checks the actual data flow.
- (b) No bar may be weakened after results are seen; a broken prereg
  is amended transparently and re-frozen. The frozen parameters
  (N=2, M=50pp, F=1.0, tried > 0) are not negotiable post hoc.
- (c) All prior verdicts stand: H2 and weak K-LT-5 remain VOID;
  generation 1 remains a valid 4/4 FAIL. Nothing here rehabilitates
  or re-scores them.
- (d) Passing K-H2-1 through K-H2-4 establishes learner-internal
  verification. It does not by itself establish L3, C0-B, C0-C, SUF,
  or cognitive reuse, which require the independent post-freeze
  generality battery and the reuse-path evidence.
- (e) Per Micah's H3-lite ruling applied to H2: passing K-H2 does NOT
  establish learner-authored procedures. It does NOT establish SUF by
  itself. It does NOT establish L3.
- (f) Q6 (retain C0-A): nothing in K-H2-1 through K-H2-4 weakens or
  restates the C0-A regression bars. TNN-2's genuine C0-A
  achievements stand as the regression baseline. K-H2-4(b) reuse
  coupling extends toward C0-D without claiming it.

## 14. Predicted TNN-2 outcome (for the record, not a bar)

Frozen TNN-2 is predicted to FAIL all four bars again (replication of
the generation 1 negative under independent world families):

- K-H2-1: FAIL. The masked branch accepts the FIRST candidate with a
  clean execution value in the fixed researcher search order; on
  trap worlds the first executable candidate is wrong by design.
- K-H2-2: FAIL. No oracle-vs-facts comparison exists on the
  verification path; the lie is absorbed (B1) or dropped silently
  (B2).
- K-H2-3: FAIL. The accept decision reads exactly three inputs (v,
  expected, masked flag); no learner-created criterion value exists
  to ablate or revise.
- K-H2-4: FAIL. Promoted graphs never execute at query time
  (`ev_query` reads only tag-1 facts, never tag-20 MAPs); reuse
  coupling is absent by construction.

A 4/4 FAIL replication would confirm the generation 1 negative
generalizes across independent adversary families. A surprise PASS
on any bar would be a genuine update and must survive the full
adversarial scrutiny of sections 4-9 before being credited.

These predictions do not govern the evaluation. The evaluator scores
what the frozen binary does.

## 15. Freeze procedure

1. This DRAFT is reviewed; the freeze commit message begins
   `H2V2-G2-PREREG-FROZEN`.
2. The freeze commit strictly precedes: world building, the pre-seal
   audit, sealing, calibration, and any probe execution. Any
   generation 2 world file, audit output, or probe run predating the
   freeze commit is void.
3. Commit-order self-check: the prereg freeze commit timestamp must
   be strictly earlier than the first world-building commit. The
   world builders record both hashes in the seal record.
4. After freezing, this document is not edited. Amendments require a
   new transparent amendment record and re-freeze; the original
   freeze stands as history.

## Verdict

**H2V2-G2-PREREG-DRAFT.** Awaiting freeze per section 15. On freezing,
K-H2-1 through K-H2-4, the TRIAL_ENTERED prerequisite, the
t2_sig_v2 correction, the two-family post-freeze adversary world
requirements, and the VOID conditions above become binding for the
H2-v2 generation 2 scientific wave.
