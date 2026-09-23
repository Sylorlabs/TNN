# READER-BLOCKED Specs (Agent D, wave 2)

Precise, checkable assertions from N1–N10 that **cannot run yet**: they target
`docs/generations/R33/runs/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl`
(15,871,908 bytes, blob `ceda86509a9e22db8783567f65e377ab860f13da`) and its
sibling `parent-r27-accepted-policy.json`, and no Zag-native reader exists for
the pickle (its class modules, e.g. `r27_experiments`, are not in the repo).

Each spec below names the exact assertion, the expected value (taken from the
wave-1 schema map), and what unblocks it. When the native reader lands,
implement each as a Zag test and move it into `wb_whitebox_tests.zag` —
then delete the stub here. A stub that lingers after its unblocker exists is
a process violation (see `docs/lab/wave1/history/DO_NOT_REPEAT.md`).

**Unblocker for all of §1–§7:** a Zag-native pickle reader built from
`docs/lab/wave1/brain/STATE_SCHEMA.md` that can walk the 121,094-node object
graph and report (class, key-set, shapes) without executing domain code.

## 1. N1 — no optimizer state (artifact)

- Assert: zero keys in the full node graph matching
  `optimizer|momentum|lr_scheduler|weight_decay`; zero `grad_fn` payloads.
- Expected: 0 matches (wave-1 sweep of all 121,094 nodes found none).
- Native half already proven: `no_implicit_drift_*` in the suite.

## 2. N2 — no gradient payloads (artifact)

- Assert: zero stored `.grad` tensors; all 76 torch Parameters have empty
  `backward_hooks` (OrderedDicts with zero items).
- Expected: 0 grad payloads; 76/76 empty hook dicts.
- Honest caveat (from the schema): `requires_grad=True` is set on the 76
  Parameters, so torch *autograd could* flow if someone called `.backward()`.
  The checkable architectural claim is: no optimizer ever attaches, no
  gradients are ever stored. A future native test should also assert that no
  code path in the lab ever invokes a backward pass.
- Native half already proven: `no_implicit_drift_*`, `update_exact_*`.

## 3. N3 — learning is structural (artifact)

- Assert: every one of the 58 `self_revision_history` entries matches
  `(diagnosis, proposal, base_accuracy, candidate_accuracy,
  compute_multiplier, decision, authorship)` — except the final entry, which
  uses the newer `(owner, diagnosis, proposal, decision, evidence)` variant
  (flagged in the schema §10.5; the test must accept both and report which
  variant each entry used).
- Assert: zero entries describe a gradient step.
- Native half already proven: `rev_*` (the decision rule's logic).

## 4. N4 — trace ops are symbolic (artifact)

- Assert: all 435 `Trace.ops` are tuples of symbolic opcodes over cue
  vectors; none is a weight delta or a parameter vector.
- Assert: every `Trace.provenance` is `'SELF_VERIFIED'` or a recorded
  alternative — no `UNVERIFIED` trace may be counted as learning evidence.
- Native half already proven: `trace_*` (the op semantics' properties).

## 5. N5 — lineage nesting invariant (artifact)

- Assert the 5-deep chain exactly:
  `R27State(60423) → R26State(60249) → R25AcceptedState(57285) →
  R24AcceptedState(41144) → R23State(29344)`,
  each level's `base_state` (or equivalent) holding the next level down.
- Assert each level carries the prior level's sha256 under its documented key
  (`r26_sha256`, `r25_sha256`, `r24_sha256`, `r23_sha256`, `r22_lineage_sha256`)
  and that the linked digest matches the embedded state's recomputed digest.
- Assert `newborn_restarts == 0` at all 5 levels; `development_step`
  monotonic non-decreasing outward→inward (29344 ≤ 41144 ≤ 57285 ≤ 60249 ≤ 60423).
- Native half already proven: `lineage_*` (the chaining logic).

## 6. N6 — canonical invariants (artifact)

- Assert `format == 'TNN_PRE_V1_R27_GENERAL_LEARNING'`,
  `development_step == 60423`, `newborn_restarts == 0`,
  `r26_sha256 == 'df3acde273aa682642d13763a24208ff1dbb42968313cbe2a4256f7ccbc1f839'`.
- No native half exists — these are constants of the artifact itself.

## 7. N7 — tensor containment (artifact)

- Assert torch Parameters exist ONLY inside the named perceptual components
  (`ConvWordNet` ×4, `EntityHeadNet`, `RawConvSpeechPAM` ×2, speech/video
  PAMs); types restricted to `Conv1d/Linear/GRU/Embedding/LayerNorm`; count
  == 76; none at brain level (no Parameter under `architecture`,
  `self_revision_history`, memory components, or the `Trace` set).
- Assert total tensor storage < 25% of artifact bytes
  (wave-1: 3.26 MB / 15.87 MB ≈ 20%).
- No native half exists — the native learner has no tensors at all.

## 8. N10 — ledger consistency (artifact)

- Assert every `active_promotions` / `rolled_back` / `shadow_partial` entry
  in `parent-r27-accepted-policy.json` corresponds to a
  `self_revision_history` decision with a matching outcome
  (PROMOTE ↔ active, rollback ↔ rolled_back).
- Assert the 5 rolled-back entries
  (`CATEGORY_METRIC`, `AFFORDANCE_GENERALIZATION`,
  `VISUAL_DEBATE_EXTRA_VIEW`, `PROTECTED_GENERALISTS`, +1) each have a
  revision entry whose decision is not PROMOTE.
- Native half already proven: `ledger_*` (the consistency logic).

## 9. Open questions that become tests once the reader exists

From the schema §10, in testable form:
- `teacher_dependence` on `MutableStudent`: assert the field exists, is
  numeric, and its value is recorded (H-09 hook) — then specify the
  withdrawal experiment it enables.
- `Trace.sources` id registry: assert every source id in the 435 traces
  resolves in the (to-be-found) registry; unresolved ids fail the test.
- The 76 perceptual Parameters' learning process is undocumented — when it
  is documented, add a test asserting the documented process contains no
  optimizer attachment (N1/N2 extended to provenance).
