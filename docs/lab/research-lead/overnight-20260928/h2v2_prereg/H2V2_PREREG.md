# H2-v2 Preregistration: DRAFT (to be frozen)

**Status: H2V2-PREREG-DRAFT.** This document is NOT frozen. It becomes
binding only when committed under the freeze procedure in section 15.
No H2-v2 world may be built before that freeze commit lands.

**Date:** 2026-10-01 (UTC). Designer: H2-v2 Prereg Designer (subagent).

---

## 0. Lineage and void declaration

- H2 preregistration (frozen `c15a47d63`): VOID, historic. Not
  salvageable, not amendable. Preserved as a negative finding.
- H2 sealed worlds (`86389b108`): VOID as test assets. Never reused.
- H2 evaluation (`72173fe11` H2-EVAL-VOID): VOID. No K-H2 verdicts
  were or will be recorded from it.
- Micah's H2-v2 directive (2026-10-01): start H2-v2 fresh. Frozen
  TNN-2 cognition unchanged. Evaluator-side `t2_sig` correction is
  permitted (measurement infrastructure, not cognition). Fresh
  preregistration. Fresh sealed H2 worlds. Worlds MUST omit direct
  query FACTs that let `activate()` short-circuit the trial.
  TRIAL_ENTERED > 0 is a prerequisite bar. If the trial path does not
  execute, no H2 verdict may be issued. Original H2 worlds and results
  remain VOID historically.

This preregistration supersedes the H2 prereg for all future H2 work.
It does not retroactively validate anything from the VOID wave.

---

## 1. Key question (verbatim from Micah's ruling, unchanged)

Can TNN accept/reject/withhold structures using a learner-internal
criterion when the environment does not provide the expected answer?

---

## 2. What H2-v2 changes relative to H2 (VOID)

Three repairs, each traceable to a named failure in `72173fe11`:

**R1. Evaluator-side `t2_sig` correction.** The frozen `t2_sig`
(`tnn2.zag` line 511) records `(tag, literal)` per cell, violating its
own specification ("Literals are EXCLUDED"). H2-v2 uses `t2_sig_v2`,
a driver-side function with identical traversal but literal-free
records (section 4). `t2_sig` is called only inside the frozen
self-test `t_t2_revise` (line 1287-1290); no production path
(`ev_query`, `ev_observe`, `ev_teach`, `ev_act`, `t2_trial`,
`mp_run`, `revise_on_contradict`) calls it. The correction changes
measurement, not cognition. Frozen TNN-2 source and binary are
untouched.

**R2. Worlds that force trial execution.** Every H2 world contained
direct OBSERVE facts for the query `(s, r)`, so `activate(W,s,r)`
(`tnn2.zag` line 140) returned a direct fact and `ev_query` (line 813)
returned before `mp_run` was ever called. The trial never ran on any
H2 probe. H2-v2 worlds contain ZERO facts with
(subject = query_s, relation = query_r) (section 10, hard
constraint). Chain evidence uses a distinct chain relation
`r_c != r_q`, rooted at the query subject. `t2_gather` (line 442) is
relation-agnostic: it extends paths via any fact whose field-20
(subject) matches, so chains assemble while `activate` misses. This
matches the frozen self-test `t_t2_trial_reject` (line 1227), which
uses mixed relations and reaches the trial through the same miss path.

**R3. TRIAL_ENTERED > 0 prerequisite bar.** A driver-measured,
white-box prerequisite that gates every verdict (section 5). If the
trial path does not execute on any scored probe, the H2-v2 evaluation
is VOID and no K-H2 verdict is issued.

**Preserved from H2:** the key question, the four kill bars K-H2-1
through K-H2-4 with identical parameters (N=2, M=50pp, F=1.0), the
three masking modes, the SIG log discipline, the H2-before-H1-widening
ordering constraint, the guard clauses, and the explicit non-claims.

---

## 3. What H2-v2 tests

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
  (line 501-503) ignores `expected` and accepts any candidate whose
  execution returns a clean value (v != -2 and v != -999999).
- **Lie:** call `ev_query` unmasked (flags=0) but supply a wrong
  `expected`. Two classes: (B1) confirmable lie, a wrong value some
  candidate executes to; (B2) unconfirmable lie, a wrong value no
  candidate executes to.
- **Withhold plus held-back facts:** withhold `expected` AND reserve
  a subset of taught facts as a private consistency set the trial
  never sees. Available mode; not required by the bars.

---

## 4. Structural signature function: t2_sig_v2 (evaluator-side correction)

**What was wrong.** The frozen `t2_sig` resolves, for tags 101/102,
the literal node id at field 8 and records its field-20 value (`lv`)
into the signature. Two graphs differing only in literals therefore
produce different signatures, violating calibration property (ii)
and the specification's literal-exclusion requirement.

**The fix (driver-side only).** `t2_sig_v2(W, root, sig)`:

- Walk from `root` following SEQ edges, with BRANCHEQ (tag 102)
  true-targets via field 12. Bound 32 cells. A cell is valid iff its
  tag is in {101, 102, 103, 104}; otherwise the walk stops.
- Per cell, record ONLY the tag. No literal node is dereferenced; no
  payload value enters the signature.
- Layout: `sig[n*4] = tag` (4 bytes per cell). Returns the cell count.
- The traversal order, tag validity rule, 32-cell bound, and SEQ /
  BRANCHEQ edge conventions are identical to the frozen `t2_sig`.
  The sole change is the removal of literal resolution.

**Why this is permitted.** `t2_sig` is invoked only by the frozen
self-test `t_t2_revise`; it is measurement scaffolding, not
production cognition. Correcting it changes no learner behavior,
promotes no MAP, and alters no accept/reject decision. Per Micah's
directive, evaluator-side measurement correction is allowed while
frozen cognition stays byte-identical.

**Calibration properties (frozen, must hold before any scoring).**

- (i) A 2-hop chain and a 3-hop chain produce DIFFERENT signatures.
- (ii) Two 2-hop chains with different literals produce IDENTICAL
  signatures.
- (iii) A chain and a sum produce DIFFERENT signatures.

The evaluator verifies (i)-(iii) on known pairs assembled by the
frozen assemblers (`t2_asm_chain`, `t2_asm_sum`) before scoring any
H2-v2 trial. If any calibration property fails, the evaluation is
VOID and the signature function must be repaired and re-frozen before
any H2-v2 scoring.

**Topology log format.** One `t2_sig_v2` string per promoted or
revised graph, exact line format:

```
SIG <world-id> <query-id> <run-idx> <decision:promote|reject|refuse> <t2_sig_v2-string>
```

Fields are space-separated. The signature string contains no spaces.
The log is written to stdout and captured per run. The sealed
evaluation compares these logged strings mechanically; no human
judgment enters the comparison.

---

## 5. TRIAL_ENTERED prerequisite bar (new, gates all verdicts)

**Statement.** On every scored probe (each masked probe and each
paired unmasked control), the trial path must execute with at least
one candidate reaching verification. If any scored probe shows the
trial did not execute, the H2-v2 evaluation is VOID and no K-H2-1
through K-H2-4 verdict is issued.

**Measurement (driver-side, white-box, no cognition change).**
`t2_trial` writes trial statistics to workspace header slot 16 on
every invocation: `hs(W,16, tried*1024 + rejected)` (line 664), where
`tried` counts `t2_try_verify` entries and `rejected` counts
rejections. `tnn2_init` zeroes header 16 (line 909); no other
production path writes it.

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

**Why this bar is sound.** `t2_try_verify` increments `tried` on
entry, before execution; any verification attempt, accepted or
rejected, is counted. Promotion requires a non-(-2) return from
`t2_try_verify`, so `tried > 0` is necessary for any promotion. If
`activate` had short-circuited the query, `mp_run` would never be
called and `tried` would stay 0. Therefore `tried > 0` proves jointly:
(a) `activate` missed, (b) `t2_trial` executed, (c) at least one
candidate reached the verifier. This is exactly the conjunction the
VOID H2 wave lacked.

**Void condition.** If TRIAL_ENTERED = 0 on any scored probe, the
evaluator records H2V2-EVAL-VOID, names the failing probe, and issues
no K-H2 verdicts. The worlds are then diagnostically defective and
must be rebuilt under a re-frozen prereg; the bar itself is not
weakened.

---

## 6. K-H2-1 (masked accuracy) [KILL BAR]

**Frozen bar text.** On N=2 sealed trap worlds (H2A-v2 and H2C-v2, the
withhold-mode worlds from the sealed set), with `expected` withheld
from the trial loop (flags bit 0 = 1, expected = -2; verified by
white-box audit that no key-derived value reaches the verifier during
the trial), the learner's committed answers exceed the frozen
first-executable-in-search-order baseline accuracy by at least M=50
percentage points, on 3/3 byte-identical runs. Paired unmasked
controls must pass on the same worlds. TRIAL_ENTERED = 1 is required
on all four probe runs (section 5).

**Parameter values (frozen).**
- N = 2 (H2A-v2 withhold trap, H2C-v2 own-criterion trap; section 10).
- M = 50 percentage points. On trap worlds the first-executable
  baseline is wrong by adversarial design, so baseline accuracy is
  0%; the learner must achieve strictly greater than 50%
  committed-answer accuracy.
- Runs: 3/3 byte-identical (stdout, state dumps, promoted signatures).

**Pass/fail.** PASS requires: masked accuracy > 50% on both H2A-v2
and H2C-v2, 3/3 byte-identical; both paired unmasked controls pass;
TRIAL_ENTERED = 1 on all four runs. Any condition missing is a
K-H2-1 FAIL.

---

## 7. K-H2-2 (lie resistance) [KILL BAR]

**Frozen bar text.** On the preregistered lying-oracle worlds (H2B-v2,
both classes: B1 confirmable lie and B2 unconfirmable lie), the
learner raises an explicit uncertainty or contradiction signal, or
refuses promotion, on at least fraction F=1.0 of trials where the
oracle contradicts retained facts, and promotes ZERO candidates that
contradict retained facts. 3/3 byte-identical runs. Paired
true-`expected` controls must pass. TRIAL_ENTERED = 1 is required on
all probe runs (section 5).

**Parameter values (frozen).**
- Worlds: H2B-v2-B1 (confirmable lie) and H2B-v2-B2 (unconfirmable
  lie).
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

---

## 8. K-H2-3 (criterion causality and revisability) [KILL BAR]

**Frozen bar text.** White-box trace demonstrates a learner-created
persistent state value in the causal chain of at least one accept or
reject decision; ablation of that value alone flips the decision; and
a committed experience log shows the criterion's value changing in
response to a prediction error. All three sub-clauses required; any
one missing is a FAIL. Analysis runs over the sealed H2-v2 trials
with TRIAL_ENTERED = 1.

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
the sealed H2-v2 worlds, 3/3 byte-identical runs. Any sub-clause
missing is a K-H2-3 FAIL.

---

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
  protected-core machinery per Micah's 2026-10-01 ruling; it is not
  pending and no status document may list it as such. Structural
  opcodes remain DEFERRED.
- (b) **Reuse coupling.** At least one structure promoted during a
  masked H2-v2 trial is subsequently executed by the query path on a
  later query in the same continuing learner, with the execution
  recorded in a white-box trace. Acceptance without reuse is causally
  inert and cannot satisfy C0-D.

**Reuse probe procedure.** In one continuing workspace: teach
H2A-v2, run the masked probe (TRIAL_ENTERED = 1 required), then issue
a related query for which `activate` misses and audit white-box
whether any tag-20 MAP root was executed outside `t2_try_verify`.
PASS requires at least one such execution trace, 3/3 byte-identical.

**Pass/fail.** PASS requires both sub-clauses, 3/3 byte-identical
runs. Either missing is a K-H2-4 FAIL.

---

## 10. Sealed world requirements

### 10.1 Common structural rules (normative)

- **ID block:** [60000, 69999], disjoint from FW [30000, 39999], GW
  [40000, 49999], H2 [50000, 59999], and all other sealed assets.
- **Two-relation scheme.** Each world declares one query relation
  `r_q` and one chain relation `r_c` with `r_c != r_q`. The QUERY
  line uses `(s, r_q)`. All chain-evidence OBSERVE lines use `r_c`.
  `r_c` never appears as a query relation in any world.
- **HARD CONSTRAINT (trial-forcing).** The world file contains ZERO
  OBSERVE or TEACH lines with (subject = query_s, relation = r_q).
  This is what forces `activate` to miss and the trial to run. Any
  world violating this constraint is rejected at the pre-seal audit
  and never sealed.
- **Chain well-formedness.** Chain facts form the specified multi-hop
  paths rooted at the query subject `s` via `r_c`, with distinct
  intermediate node ids, no cycles, and the intended endpoint values.
- **Fact operation.** World facts are taught via OBSERVE (the natural
  world-presents-fact operation), matching the H2 trap-world
  semantics.
- **Trap preservation.** Each world is a search-order trap: the first
  executable candidate in the frozen search order (chains k=2..4 in
  `t2_gather` BFS order, then single hops; sums are inert in
  production because no tag-8 node exists) is WRONG by design, and
  the correct structure appears later in that order.

### 10.2 H2A-v2: withhold trap

- s = 60001, r_q = 60051, r_c = 60052.
- OBSERVE 60001 60052 60002
- OBSERVE 60002 60052 60003 (2-hop; wrong answer 60003)
- OBSERVE 60001 60052 60011
- OBSERVE 60011 60052 60012
- OBSERVE 60012 60052 60013 (3-hop; true answer 60013)
- QUERY 60001 60051 60013

Masked probe: flags=1, expected=-2. Unmasked control: flags=0,
expected=60013. Sealed true answer: 60013.

Mechanics check: `t2_gather` BFS order tries the 2-hop
[60001,60002,60003] before the 3-hop; masked mode accepts the first
clean execution (60003, WRONG); unmasked mode rejects 60003 and
promotes the 3-hop (60013, CORRECT).

### 10.3 H2B-v2: lie trap

**B1 (confirmable lie).** s = 60101, r_q = 60151, r_c = 60152.
- OBSERVE 60101 60152 60102
- OBSERVE 60102 60152 60103 (true answer 60103)
- OBSERVE 60101 60152 60111
- OBSERVE 60111 60152 60112 (lie value 60112)
- QUERY 60101 60151 60112

The QUERY expected field carries the LIE (60112). The sealed true
answer (60103) is recorded in the seal record, not in the world file.
Probe: flags=0, expected=60112 (corrupted oracle). Paired control:
flags=0, expected=60103 (true oracle).

**B2 (unconfirmable lie).** s = 60121, r_q = 60151, r_c = 60152.
- OBSERVE 60121 60152 60122
- OBSERVE 60122 60152 60123 (true answer 60123)
- QUERY 60121 60151 69999

The QUERY expected field carries 69999, a value no candidate
produces. Sealed true answer: 60123. Probe: flags=0,
expected=69999. Paired control: flags=0, expected=60123.

### 10.4 H2C-v2: own-criterion trap

- s = 60201, r_q = 60251, r_c = 60252.
- OBSERVE 60201 60252 60202
- OBSERVE 60202 60252 60203 (2-hop; 60203)
- OBSERVE 60201 60252 60211
- OBSERVE 60211 60252 60212
- OBSERVE 60212 60252 60213 (3-hop path 1 to 60213)
- OBSERVE 60201 60252 60221
- OBSERVE 60221 60252 60222
- OBSERVE 60222 60252 60213 (3-hop path 2 to 60213)
- OBSERVE 60201 60252 60231
- OBSERVE 60231 60252 60232
- OBSERVE 60232 60252 60213 (3-hop path 3 to 60213)
- QUERY 60201 60251 60213

Three independent 3-hop paths converge on 60213 (the true answer);
one 2-hop path yields 60203. Masked probe: flags=1, expected=-2.
Unmasked control: flags=0, expected=60213. A consistency-based
learner criterion would prefer 60213 (evidence multiplicity 3 vs 1);
the fixed search order prefers 60203.

### 10.5 Pre-seal structural audit (builder-side, mandatory)

Before sealing, the world builder runs a mechanical audit over each
world file and commits the audit output:

1. Parse every OBSERVE/TEACH line; assert zero lines with
   (subject = query_s AND relation = r_q). Print the count (must be
   0).
2. Assert every chain fact uses `r_c` and chains from `s` with no
   repeated node ids within a path.
3. Assert all ids lie in [60000, 69999] and all `(s, r_q, r_c)`
   triples are distinct across worlds.
4. Assert the QUERY line count is exactly 1 per world file and its
   relation is `r_q`.
5. Record the SHA-256 of each world file.

The audit is structural only: the worlds are NEVER executed against
TNN-2 before the authorized evaluation. Any execution predating
authorization voids the seal.

### 10.6 Sealing procedure

1. This prereg is frozen (section 15) BEFORE any world file is
   created.
2. An independent world builder (not the evaluator, not the prereg
   designer) generates the three world files per sections 10.1-10.4,
   runs the pre-seal audit (10.5), and commits the audit output.
3. The builder records SHA-256 hashes in `SEAL_H2V2.md`, sets file
   permissions `-rw-------`, and attests the worlds were never run
   through TNN-2.
4. The evaluator (a different worker) verifies all three hashes
   against `SEAL_H2V2.md` before the first probe and records the
   verification.
5. Only the authorized H2-v2 evaluator opens the world files. No
   builder, analyst, or other worker opens them.

**Honest limitation (recorded).** The draft bar text anticipated
worlds from at least two independently designed world families with
an adversary designing post-freeze. The H2-v2 sealed set is specified
normatively in this prereg (single design source, pre-freeze
specification, sealed and never executed). The two-family diversity
requirement is NOT met. This limitation is recorded, not waived;
future H2 evaluations should use two independent post-freeze
adversaries.

### 10.7 World-to-bar mapping (frozen)

- K-H2-1: H2A-v2 (withhold), H2C-v2 (withhold).
- K-H2-2: H2B-v2-B1 (confirmable lie), H2B-v2-B2 (unconfirmable lie).
- K-H2-3: white-box analysis over any H2-v2 trials with
  TRIAL_ENTERED = 1.
- K-H2-4: reuse coupling over masked trials on H2A-v2/H2C-v2.

### 10.8 Scoring keys

True answers: H2A-v2 = 60013, H2B-v2-B1 = 60103, H2B-v2-B2 = 60123,
H2C-v2 = 60213. Recorded in `SEAL_H2V2.md` at seal time. The
evaluator reads them from the seal record after the learner commits.
They are not embedded in the world files (except as the control
`expected` values noted above).

---

## 11. Driver and evaluation requirements

- **Pure Zag.** All research computation, scoring, world parsing,
  and analysis in Zag. Safebin mandatory; `python3`/`python` must not
  resolve in the worker PATH. Shell only to invoke `znc`, run
  binaries, do git operations, and move files. Any forbidden
  executable invocation is PROCESS-FAIL for the wave.
- **Frozen cognition.** The evaluation binary links the frozen
  TNN-2 source (SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  canonical C160 `cabe77934541571c5313f65af2257d03a74b5bfe`) with
  only `main` replaced by the driver harness. The driver verifies
  byte-identity of the cognition source before building.
- **Production query path.** The driver calls `ev_query` for every
  probe. It MUST NOT call `mp_run` or `t2_trial` directly.
- **Fresh workspace per probe.** `tnn2_init` before teaching each
  world; learner state is not carried across probes except in the
  dedicated K-H2-4(b) reuse probe.
- **3/3 byte-identical runs** for every scored probe (stdout, state
  dumps, SIG log).
- **Pinned compiler.** `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- **Calibration first.** `t2_sig_v2` calibration (section 4) precedes
  all scoring; failure voids the evaluation.
- **Prerequisite second.** TRIAL_ENTERED (section 5) is checked on
  every scored probe; any zero voids the evaluation with no verdicts.

---

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

---

## 13. Guard clauses and explicit non-claims

- (a) `expected` must be absent from the trial path on masked probes,
  not renamed, re-encoded, or cached where the verifier can read it;
  the K-H2-1 white-box audit checks the actual data flow.
- (b) No bar may be weakened after results are seen; a broken prereg
  is amended transparently and re-frozen. The frozen parameters
  (N=2, M=50pp, F=1.0, tried > 0) are not negotiable post hoc.
- (c) The original H2 worlds, prereg, and evaluation remain VOID
  historically. Nothing in H2-v2 rehabilitates them; H2-v2 results
  stand or fall on the fresh seal alone.
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

---

## 14. Predicted TNN-2 outcome (for the record, not a bar)

Frozen TNN-2 is predicted to FAIL all four bars (from source reading;
the trial now executes, so these are genuine behavioral predictions):

- K-H2-1: FAIL. The masked branch accepts the FIRST candidate with a
  clean execution value in the fixed researcher search order; on trap
  worlds the first executable candidate is wrong by design. Predicted
  masked accuracy 0% on both H2A-v2 and H2C-v2.
- K-H2-2: FAIL. No oracle-vs-facts comparison exists on the
  verification path; the lie is absorbed (B1: lie-matching candidate
  promoted) or dropped silently (B2: no key-failure trace).
- K-H2-3: FAIL. The accept decision reads exactly three inputs (v,
  expected, masked flag); the DOF map records zero pure-learner
  decisions. No learner-created criterion value exists to ablate or
  revise.
- K-H2-4: FAIL. Promoted graphs never execute at query time
  (`ev_query` reads only tag-1 facts, never tag-20 MAPs); reuse
  coupling is absent.

These predictions do not govern the evaluation. The evaluator scores
what the frozen binary does.

---

## 15. Freeze procedure

1. This DRAFT is reviewed; the freeze commit message begins
   `H2V2-PREREG-FROZEN`.
2. The freeze commit strictly precedes: world building, the pre-seal
   audit, sealing, calibration, and any probe execution. Any H2-v2
   world file, audit output, or probe run predating the freeze commit
   is void.
3. Commit-order self-check: the prereg freeze commit timestamp must
   be strictly earlier than the first world-building commit. The
   world builder records both hashes in the seal record.
4. After freezing, this document is not edited. Amendments require a
   new transparent amendment record and re-freeze; the original
   freeze stands as history.

---

## Lineage

- H2 probe design: `4631c5918` (H2-PROBE-DESIGN-COMPLETE).
- K-H2 draft synthesis: `36e5a70e1`. Kill-bar review Q1-Q6:
  `eb354e3a2` (KILLBAR-REVIEW-COMPLETE).
- H2 readiness: `6384c51df`. Trap-world seal (VOID): `86389b108`.
- H2 prereg frozen (VOID, historic): `c15a47d63`.
- H2 evaluation (VOID): `72173fe11` (t2_sig calibration failed;
  trial never ran on H2 worlds).
- Micah's H2 ruling: 2026-10-01 07:10 PDT.
- Micah's H2-v2 directive: 2026-10-01 (fresh wave; see section 0).
- Micah's protected-core ISA ruling: 2026-09-30 (EXECUTE approved).
- Roadmap ordering: `67a420cca`. Treadmill guard: `1646b9732`.

---

## Verdict

**H2V2-PREREG-DRAFT.** Awaiting freeze per section 15. On freezing,
K-H2-1 through K-H2-4, the TRIAL_ENTERED prerequisite, the
`t2_sig_v2` correction, and the sealed-world requirements above
become binding for the H2-v2 scientific wave.
