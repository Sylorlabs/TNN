# H2 Preregistration: FROZEN

**Status: H2-PREREG-FROZEN**

Date: 2026-10-01 (UTC). Freezer session: H2 Prereg Freezer (subagent).

This document freezes kill bars K-H2-1 through K-H2-4 per Micah's H2 ruling
(2026-10-01 07:10 PDT). It freezes ONLY these four bars. It does not freeze
the full TNN-3 preregistration, which awaits H2/H3-lite/reuse evidence per
the ruling.

**Ordering rule.** This freeze commit strictly precedes any H2 evaluation.
No H2 probe run, masked or unmasked, may begin before this commit lands.
The evaluator is authorized to open the sealed H2 worlds only after this
freeze (see section 10).

---

## 1. Key question (verbatim from Micah's ruling)

Can TNN accept/reject/withhold structures using a learner-internal criterion
when the environment does not provide the expected answer?

---

## 2. Roadmap ordering constraint

H2 MUST precede H1 widening. Do not build a larger grammar until the key
question in section 1 is answered. Widening the constructor while the
acceptance oracle remains would build a larger finite menu under the same
generous acceptance test, which is the treadmill Micah forbade (roadmap
`67a420cca`, Risk 3; treadmill guard `1646b9732`, warning sign 5).

No H1 construction work (new assemblers, new templates, expanded search
families, capability-shaped operators) may begin until K-H2-1 through K-H2-4
have been evaluated and their results recorded, whatever the outcome.

---

## 3. What H2 tests

On sealed post-freeze trap worlds, with the driver-supplied answer key
(`expected`) provably absent from the trial path, the learner must verify
candidate structures from its own persistent state. The external score is
computed only AFTER the learner has committed to an answer, a promotion,
or a refusal.

A probe run is masked iff all of the following hold:

1. During the entire trial (every call to `t2_try_verify` for that query),
   no value derived from the sealed answer key reaches the verifier. The
   driver withholds `expected`, supplies a corrupted `expected`, or the
   verifier is required to ignore it.
2. The learner commits to an observable decision: an answer, a promoted
   graph, or an explicit refusal/uncertainty signal, before the key is
   revealed.
3. Scoring compares the committed decision against the sealed key offline.
   The score cannot leak back into the learner during the trial.
4. A paired unmasked control run (same world, `expected` supplied, flags=0)
   is executed to confirm the mechanism passes with the oracle. The
   discrimination signal is the GAP between unmasked and masked behavior,
   not the masked score alone.

Three masking modes (all driver-side, no learner source edits):

- **Withhold:** call `mp_run` with flags bit 0 = 1. The masked branch of
  `t2_try_verify` ignores `expected` and accepts any candidate whose
  execution returns a clean value (v != -2 and v != -999999).
- **Lie:** call `mp_run` unmasked (flags=0) but supply a wrong `expected`.
  Two classes: (B1) confirmable lie, a wrong value some candidate executes
  to; (B2) unconfirmable lie, a wrong value no candidate executes to.
- **Withhold plus held-back facts:** withhold `expected` AND reserve a
  subset of taught facts as a private consistency set the trial never sees.

---

## 4. K-H2-1 (masked accuracy) [KILL BAR]

**Frozen bar text.** On N=2 sealed trap worlds (H2A and H2C, the
withhold-mode worlds from the sealed set), with `expected` withheld from
the trial loop (verified by white-box audit that no key-derived value
reaches the verifier during the trial), the learner's committed answers
exceed the frozen first-executable-in-search-order baseline accuracy by at
least M=50 percentage points, on 3/3 byte-identical runs. Paired unmasked
controls must pass on the same worlds.

**Parameter values (frozen).**
- N = 2 (H2A withhold trap, H2C own-criterion trap; see section 9).
- M = 50 percentage points. On trap worlds the first-executable baseline
  is wrong by adversarial design, so baseline accuracy is 0%; the learner
  must achieve strictly greater than 50% committed-answer accuracy.
- Runs: 3/3 byte-identical (stdout, state dumps, promoted signatures).

**Pass/fail.** PASS requires: masked accuracy > 50% on both H2A and H2C,
3/3 byte-identical; both paired unmasked controls pass. Any condition
missing is a K-H2-1 FAIL.

---

## 5. K-H2-2 (lie resistance) [KILL BAR]

**Frozen bar text.** On the preregistered lying-oracle worlds (H2B, both
classes: B1 confirmable lie and B2 unconfirmable lie), the learner raises
an explicit uncertainty or contradiction signal, or refuses promotion, on
at least fraction F=1.0 of trials where the oracle contradicts retained
facts, and promotes ZERO candidates that contradict retained facts.
3/3 byte-identical runs. Paired true-`expected` controls must pass.

**Parameter values (frozen).**
- Worlds: H2B-B1 (confirmable lie) and H2B-B2 (unconfirmable lie).
- F = 1.0. On B1, the learner must not promote the lie-matching candidate;
  it must refuse, flag a contradiction, or promote the fact-consistent
  candidate instead. On B2, no candidate matches the lie; the trial must
  record the failure as evidence about the key, visible in learner state
  (not merely ans = -2 with no trace).
- Zero promotions of fact-contradicting candidates is a hard requirement,
  independent of F.

**Pass/fail.** PASS requires: B1 shows refusal/signal/flag (not promotion
of the lie-matching candidate), 3/3 byte-identical; B2 shows a recorded
key-failure trace in learner state, 3/3 byte-identical; zero
fact-contradicting promotions across all runs; paired controls pass. Any
condition missing is a K-H2-2 FAIL.

---

## 6. K-H2-3 (criterion causality and revisability) [KILL BAR]

**Frozen bar text.** White-box trace demonstrates a learner-created
persistent state value in the causal chain of at least one accept or
reject decision; ablation of that value alone flips the decision; and a
committed experience log shows the criterion's value changing in response
to a prediction error. All three sub-clauses required; any one missing
is a FAIL.

**Sub-clauses (all required).**
- (a) **Causality.** A white-box trace of the accept/reject decision shows
  a learner-created persistent state value among the values read. The
  value must be learner-created (written by learner experience through an
  exercised production write path), not a researcher-set constant.
- (b) **Ablation.** Removing or zeroing that value alone, with all
  researcher constants untouched, flips at least one accept/reject
  decision. This is the anti-theater check: a criterion that cannot be
  ablated is a researcher constant with a new name.
- (c) **Revisability.** A committed experience log shows the criterion's
  value changing in response to a prediction error (for example, a
  consistency threshold tightening after a false acceptance). A fixed
  criterion is H1-style enumeration moved one level up.

**Pass/fail.** PASS requires all three sub-clauses demonstrated on the
sealed H2 worlds, 3/3 byte-identical runs. Any sub-clause missing is a
K-H2-3 FAIL.

---

## 7. K-H2-4 (domain neutrality and reuse) [KILL BAR]

**Frozen bar text.** The verifier that passes K-H2-1 through K-H2-3
contains no per-family acceptance branches and no new protected-core
operations; and at least one promoted structure from a masked trial is
executed by the query path on a later query in the same continuing
learner (reuse coupling).

**Sub-clauses (both required).**
- (a) **Domain neutrality.** The same verifier handles chain, sum, and
  count candidate families with no per-family acceptance branches. A new
  branch per family is the benchmark-specific-handler smell and fails
  this sub-clause. No new protected-core operations (per Micah's
  protected-core ruling: Alternative C; structural opcodes DEFERRED).
- (b) **Reuse coupling.** At least one structure promoted during a masked
  H2 trial is subsequently executed by the query path (`ev_query` or its
  successor) on a later query in the same continuing learner, with the
  execution recorded in a white-box trace. Acceptance without reuse is
  causally inert and cannot satisfy C0-D.

**Pass/fail.** PASS requires both sub-clauses, 3/3 byte-identical runs.
Either missing is a K-H2-4 FAIL.

---

## 8. Structural signature function (Q3: single fixed function)

Per the kill-bar review recommendation (Q3), one single structural
signature function is fixed in this frozen preregistration. It is used
for all graph-identity comparisons in K-H2-1 through K-H2-4 (promoted
graph signatures, baseline comparisons, ablation identity).

**Function name.** `t2_sig`, as implemented in the frozen TNN-2 source
(commit `f4de7ff46`, file `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`).

**Specification.** `t2_sig` computes a canonical string over a promoted
graph's cells encoding: cell tags in canonical traversal order, edge
types (structural link fields), per-node step counts, and the adjacency
shape. Literals (subject/object/value payloads) are EXCLUDED from the
signature: two graphs differing only in literals must produce identical
signatures.

**Calibration properties (frozen, must hold).**
- (i) A 2-hop chain and a 3-hop chain produce DIFFERENT signatures.
- (ii) Two 2-hop chains with different literals produce IDENTICAL
  signatures.
- (iii) A chain and a sum produce DIFFERENT signatures.

The evaluator must verify properties (i)-(iii) on known pairs before
scoring any H2 trial. If any calibration property fails, the evaluation
is void and the signature function must be repaired and re-frozen before
any H2 scoring.

## 8b. Topology log format (Q2: explicit format)

Per the kill-bar review recommendation (Q2), the evaluator logs one
`t2_sig` string per promoted graph and per revised graph, in this exact
line format:

```
SIG <world-id> <query-id> <run-idx> <decision:promote|reject|refuse> <t2_sig-string>
```

Fields are space-separated. `<t2_sig-string>` contains no spaces. The log
is written to stdout and captured per run. The sealed evaluation compares
these logged strings mechanically; no human judgment enters the
comparison.

---

## 9. Sealed worlds and adversary protocol

**Sealed set.** Three trap worlds, built by the Trap World Builder
(commit `86389b108`), sealed in `h2_trapworlds/SEAL_H2.md`:

- H2A (withhold trap): SHA-256
  `be358e7ae423d55d99018288f9a6e14c72b2e86d649637652e1eb22a0ddf7499`
- H2B (lie trap): SHA-256
  `6cac9f6b22c8e303e75bfadac0cd13459ce1e0c64a999c25c8a0b0e2ca31ca6c`
- H2C (own-criterion trap): SHA-256
  `2b721d49e0f04e9aef915eaec69fa9d5ec3db71c5c8d0293eafa75418eb846ba`

ID range [50000, 59999], disjoint from FW [30000, 39999] and GW
[40000, 49999]. File permissions `-rw-------` (root only). The worlds have
never been run through TNN-2 (verified by the H2 readiness checker,
`6384c51df`).

**World-to-bar mapping (frozen).**
- K-H2-1: H2A (withhold), H2C (withhold plus held-back facts).
- K-H2-2: H2B-B1 (confirmable lie), H2B-B2 (unconfirmable lie).
- K-H2-3: white-box analysis over any of H2A/H2B/H2C trials.
- K-H2-4: reuse coupling over masked trials on H2A/H2C.

**Scoring keys.** The true answers for offline scoring are recorded in
`SEAL_H2.md` (commit `86389b108`). The evaluator reads them from the seal
record after the learner has committed. They are not reproduced here.

**Honest limitation (recorded).** The draft bar text anticipated worlds
"drawn from at least two independently designed world families" with the
"adversary designs post-freeze." The sealed set contains three worlds
from a single trap-world builder, designed pre-freeze but sealed and
never executed against TNN-2. The two-family diversity requirement is
NOT met by this sealed set. This freeze proceeds per Micah's explicit
authorization to use the already-sealed worlds. Future H2 evaluations
should use two independent post-freeze adversaries.

---

## 10. Evaluator authorization (seal opening)

This freeze commit authorizes the H2 probe evaluator to open the sealed
H2 world files (`h2a_world.txt`, `h2b_world.txt`, `h2c_world.txt`).

Authorization conditions:
1. This freeze commit (`H2-PREREG-FROZEN`) strictly precedes the first
   H2 probe execution. Any probe run predating this commit is void.
2. Only the authorized H2 probe evaluator may open the world files. No
   builder, analyst, or other worker shall open them.
3. The evaluator verifies all three SHA-256 hashes against `SEAL_H2.md`
   before the first run and records the verification.
4. The frozen TNN-2 binary (`f4de7ff46`) is the evaluation target. No
   source modifications, no recompilation, no new binaries for the
   learner. Driver-side probe harnesses only.

---

## 11. Bar framing and C0-A (Q4, Q5, Q6)

- **Q5 (kill bars, not falsifiers).** K-H2-1 through K-H2-4 are KILL
  BARS. Each is a conjunctive requirement: any sub-clause failing is a
  bar FAIL. They are not promoted to falsifiers.
- **Q4 (keep as drafted).** The bar text above retains the draft
  structure (four sub-clauses, guard clauses) with parameters frozen
  (N=2, M=50pp, F=1.0) and the Q2/Q3 instrumentation specified. No
  bar was weakened in freezing.
- **Q6 (retain C0-A).** Nothing in K-H2-1 through K-H2-4 weakens or
  restates the C0-A regression bars. TNN-2's genuine C0-A achievements
  stand as the regression baseline. K-H2-4(b) reuse coupling extends
  toward C0-D without claiming it.
- **Q1 (inquiry scenarios 5+).** The Q1 recommendation targets the
  inquiry bars (INQ-1..4), not K-H2. K-H2's scenario count is fixed by
  the sealed set (4 probe scenarios: H2A-withhold, H2C-withhold,
  H2B-B1-lie, H2B-B2-lie). This is recorded, not inflated.

**Guard clauses (frozen).**
- (a) `expected` must be absent from the trial path, not renamed,
  re-encoded, or cached where the verifier can read it; the K-H2-1
  white-box audit checks the actual data flow.
- (b) No bar may be weakened after results are seen; a broken prereg
  is amended transparently and re-frozen.
- (c) Passing K-H2-1 through K-H2-4 establishes learner-internal
  verification. It does not by itself establish L3, C0-B, C0-C, SUF,
  or cognitive reuse, which require the independent post-freeze
  generality battery and the reuse-path evidence.

**Explicit non-claims (per Micah's H3-lite ruling, applied to H2).**
Passing K-H2 does NOT establish learner-authored procedures. It does
NOT establish SUF by itself. It does NOT establish L3.

---

## 12. Predicted TNN-2 outcome (for the record, not a bar)

Frozen TNN-2 is predicted to FAIL all four sub-clauses (from source
reading in `4631c5918`, section 5):

- K-H2-1: the masked branch accepts the FIRST candidate with a clean
  execution value in the fixed researcher search order; on trap worlds
  the first executable candidate is wrong by design.
- K-H2-2: no oracle-vs-facts comparison exists on the verification path;
  the lie is absorbed (B1) or dropped silently (B2).
- K-H2-3: the accept decision reads exactly three inputs (v, expected,
  masked flag); the DOF map records zero pure-learner decisions.
- K-H2-4: promoted graphs never execute at query time
  (`ev_query` reads only tag-1 facts, never tag-20 MAPs).

These predictions do not govern the evaluation. The evaluator scores
what the frozen binary does.

---

## 13. Lineage

- H2 probe design: `4631c5918` (H2-PROBE-DESIGN-COMPLETE).
- K-H2 draft synthesis: `36e5a70e1` (gap bars, Gap 1).
- Kill-bar review Q1-Q6: `eb354e3a2` (KILLBAR-REVIEW-COMPLETE).
- H2 readiness: `6384c51df` (H2-READINESS-COMPLETE).
- Trap-world seal: `86389b108` (H2-TRAPWORLDS-COMPLETE).
- Micah's H2 ruling: 2026-10-01 07:10 PDT (overnight results reviewed).
- Roadmap ordering: `67a420cca` (H2 probes Step 1, before H1 widening Step 4).
- Treadmill guard: `1646b9732` (warning sign 5: H1 widening before H2).

---

## Verdict

**H2-PREREG-FROZEN.** K-H2-1 through K-H2-4 are frozen as written above.
This freeze strictly precedes any H2 evaluation. The evaluator is
authorized to open the seal under section 10 conditions.
