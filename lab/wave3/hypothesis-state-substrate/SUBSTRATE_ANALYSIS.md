# SUBSTRATE_ANALYSIS — what hypothesis-state v1 ACTUALLY stores and computes

Investigator: Wave-3, slug `hypothesis-state-substrate`. Date: 2026-09-19.
Source read in full from the repo (branch `tnn-native-lab`):
`docs/generations/R34/runs/R34_NATIVE_QUALIFICATION_STAGE_20260916/r34_hypothesis_state_v1.zag`
(git blob `91d7f540390a12b06acd9bef468e6bc723096374`, 4883 bytes).
Local copy kept at `./r34_hypothesis_state_v1.zag` for audit. The survey's
one-line summary ("pairwise contrastive credit", wave2/ruleslab/RULES_SURVEY.md §6)
is accurate but incomplete — the file is mostly a different machine than the summary suggests.

## 1. What it stores

| State | Type | Owner | Role |
|---|---|---|---|
| `support[]` | f64 per slot, `capacity` slots | substrate | running evidence accumulator |
| `active[]` | i32 flag per slot | substrate | slot lifecycle |
| `weights[]` | f32, `feature_dim` | **caller-owned, learned** | maps evidence features → support delta |
| `evidence[]` | f32, `capacity × feature_dim` | caller-supplied per step | per-hypothesis feature vectors |
| `retention` | f64 scalar in [0,1] | **caller-owned** | stickiness of old support |
| `learning_rate`, `strength` | f64 scalars | caller-supplied | pairwise credit gain |

The header comment is explicit and honest: *"It stores no human labels, task
names, graph edges, evaluator answers, or fixed UNKNOWN threshold."*
Confirmed from source: there is no label, task, or threshold anywhere in the file.

## 2. What it computes (every function, from source)

- `r34h1_dot` — checked dot product `w·x` with finite checks on every
  multiply-add. Pure arithmetic helper.
- `r34h1_observe` — for each active slot:
  `support[h] = retention·support[h] + dot(weights, evidence_h)`.
  This is an EMA-style evidence accumulator. Note: `retention` is
  caller-owned — the substrate does not prescribe stickiness.
- `r34h1_rank` — reports `top_slot, second_slot, top_score, second_score,
  margin, active_count`. The comment is the key sentence of the whole file:
  *"This reports evidence and margin only; it intentionally does not force
  SAME/DIFFERENT/UNKNOWN from a researcher-authored threshold."*
  **v1 deliberately refuses to define a commit rule.**
- `r34h1_pairwise_credit` — `w[i] += learning_rate·strength·(features_a[i] −
  features_b[i])`. Pure Hebbian-style contrast between two feature vectors.
  No error term, no normalization, no target. The caller chooses A/B "from
  lived consequences"; the module never sees a task label.
- `r34h1_activate` / `r34h1_deactivate` — slot lifecycle. Deactivation zeroes
  support. **Deactivation is caller-driven; there is no refutation rule** —
  nothing in v1 decides *when* a hypothesis dies.
- `r34h1_state_equal` — exact bitwise state comparison (determinism aid).

Error codes: `R34H1_OK/BAD/SHAPE/NUMERIC/RANGE` (−340101…−340104). All
functions `@noalloc`. No RNG anywhere in the file (already compliant with
the program no-RNG law — nothing to remove).

## 3. What it does NOT do (the gaps this investigation fills)

1. **No commit rule.** `r34h1_rank` computes margin and stops. The entire
   "when does the system act on a hypothesis" question is unanswered.
2. **No refutation rule.** Slots die only when the caller says so. There is
   no notion of evidence *against* a hypothesis as distinct from low support.
3. **No hypothesis content.** Hypotheses are bare slots with feature vectors.
   Nothing represents what a hypothesis *claims* — so nothing can contradict it.
4. **No audit.** Activation/deactivation/credit leave no record of *why*.
   The R27 target semantics (diagnosis → proposal → measured PROMOTE/rollback,
   brain/STATE_SCHEMA.md §6) require an audited deliberate op; v1 has none.
5. **The support dynamics are score machinery.** `retention·support + w·x`
   is an additive score accumulator with a caller-owned decay — structurally
   a score table with one row per hypothesis. Any commit rule built on
   `support`/`margin` would be argmax-with-extra-steps.

## 4. Mapping: v1 → HSS (the wired version, `hss.zag`)

| v1 piece | HSS treatment | Rationale |
|---|---|---|
| `r34h1_activate/deactivate` lifecycle | kept as `hss_activate` + refutation path (same active-flag semantics) | sound, minimal |
| `support[]` accumulator | replaced by `conf[]` u32 confirmation counters, **audit-only, causally inert** | quarantines the score machinery out of decisions |
| `r34h1_observe` (EMA + dot) | replaced by logical observe: contradiction → refute; confirmation → count; else consistent | evidence as logic, not weighted sum |
| `r34h1_rank` (no commit rule) | replaced by `hss_commit`: commit iff exactly one hypothesis is active | the missing rule, as logic |
| `r34h1_pairwise_credit` | **not used** | Hebbian contrast updates caller weights; this investigation needs no learned weights — evidence contribution is logical |
| `r34h1_state_equal` | not needed (no float state); determinism proven by byte-identical reruns | — |
| (missing) refutation rule | **added**: observed bit contradicts a defining claim bit → deactivate + audit | the core new logic |
| (missing) vacuous-hypothesis gate | **added**: `sig == 0` → `HSS_VACUOUS` refusal + audit | unfalsifiable hypotheses are not hypotheses (Popper gate, logic not threshold) |
| (missing) audit | **added**: 64-entry op log (ACTIVATE/OBSERVE/COMMIT/HOLD/UNCOMMIT/REFUSE), fail-closed on overflow | R27-style deliberate audited ops |

Audit encoding note: the audit `slot` field stores `slot+1` (0 = "no slot",
used by HOLD) because the u32 packing helpers require non-negative values.

## 5. The commit rule (logic, not threshold)

- **Refute** iff an observation directly contradicts a *defining claim* of the
  hypothesis: `claim_bit(index) == 1 && observed_bit == 0` → deactivate.
  No score, no margin, no count of confirmations involved.
- **Commit** iff exactly one hypothesis remains active (`active_count == 1`),
  regardless of its confirmation count (even zero). Commit is a deliberate
  op: it appends a COMMIT audit entry and sets the committed slot.
- **Hold** (deliberate non-commit) iff `active_count != 1`, with the count
  recorded in the audit entry. This is abstention earned from non-uniqueness
  of survivors — not from a probability bucket (DO_NOT_REPEAT.md §8.4).
- **Uncommit** iff the committed hypothesis is later refuted, or a new rival
  becomes active. Commitment is revocable; it is not a sticky threshold crossing.
- Confirmation counters exist so the trial can *see* support; the static
  check in the runner proves they do not enter the commit region.

## 6. Scale dimension (program law §1)

Per-observation cost: O(active hypotheses), one integer compare each.
Per-commit cost: O(capacity) scan. Memory: 16 bytes/slot + fixed 1 KiB audit.
100x hypotheses (800 slots) is arithmetically trivial. The honest scale risks
are structural, not arithmetic, and are stated in PREREG.md: hypothesis
*generation* is out of scope (next step: wire to native-structural-revision
proposals); adversarial non-refuting sequences yield perpetual HOLD (correct
abstention, no progress); the 64-entry audit is fail-closed, not a long-horizon
solution (next scale test: 1000 slots / 100k observations with sealed audit
segments + digest, measuring HOLD correctness under adversarial curricula).
