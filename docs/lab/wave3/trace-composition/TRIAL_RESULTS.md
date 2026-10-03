# TRIAL_RESULTS — trace-composition (Wave 3)

**Date:** 2026-09-19 · **Platform:** Linux x86-64 · **Runner:**
`run_comp.sh` · **Evidence:**
`EVIDENCE_20260920T002106Z/` (compile/run stdouts, exits, summary,
RECEIPT, static-check outputs)

## Verdict: POSITIVE (within preregistered scope)

All four preregistered falsification gates hold on the native trial:
**F1** soundness clean (every composite's `apply()` matched the
independent reference oracle element-wise, incl. boundary values and u8
wraparound); **F2** structural refusal clean (all 8 adversarial
should-refuse cases refused with the correct distinct status and left no
usable composite behind); **F3** determinism clean (byte-identical rebuilds,
byte-identical double binary runs, static no-RNG check passes on
comment-stripped system source); **H4** reuse demonstrated (named-op
composites store 4 op slots vs 8 expanded, identical semantics).

## Key evidence (92/92 CL_CHECK lines pass, `COMP_FAILURES,0`, exit 0)

- **Soundness:** `g2_seq_oracle`, `g4_branch_oracle`, `g6_nested_oracle`,
  `g8_deep_oracle`, `g9_oracle` all `1,1` — composite execution equals the
  independent direct executor on all cues. Hand spot-checks agree:
  `g8_spot_50,176,176` (8-op fold hand-computed), `g4_spot_100_else,44,44`
  (strict-`>` predicate boundary at 100), `g1_wrap_200,144,144` (u8
  wraparound).
- **Provenance closure:** `g2_sources,3,3` (union), `g4_sources,14,14`
  (3-way union), `g6_seq_named_sources,68,68` (union through a named-use),
  `g2_provenance,2,2` / `g4_provenance,2,2` (PROV_COMPOSED), all
  `verified=1`.
- **Structural refusal (ADV suite):** `g3_poison_refused,2101,2101`
  (unverified middle link of a 5-fold), `g3_forged_refused,2101,2101`
  (verified=1 with tampered provenance), `g4_smuggler_refused,2102,2102`
  (MAP_MUL trace as branch predicate), `g4_unver_arm_refused,2101,2101`,
  `g5_squat_refused,2103,2103` (name collision; registry count still 1 and
  `g5_squat_unchanged,1,1`), `g5_unver_refused,2101,2101`,
  `g5_unknown_name,2104,2104`, `g8_capacity_refused,2105,2105` (8+1>8).
  Every refusal also asserted the output record invalid
  (`verified=0, provenance=0, nops=0`) and, for the fold case, the
  accumulator untouched (`g3_acc_untouched,1,1`).
- **Determinism (A2/A3):** `g7_rebuild_identical,1,1` (same composite built
  twice into one slot, byte-identical 92-byte records);
  `double_run_identical=true` (two full binary runs, byte-identical
  stdout); `no_randomness=true` (static grep over comment-stripped
  `comp.zag`: no rng/random/srand/time/raw-syscall tokens);
  `no_banned_mechanisms=true` (no score tables / RL / reward tokens).
- **Reuse leverage (H4):** `g9_flat_nops,8,8` vs `g9_named_nops,4,4`,
  `g9_same_semantics,1,1`, `g9_footprint_shrinks,1,1` — abstraction is
  reuse, not just concatenation.

## Honest amendment (recorded, not silently rerun)

The first run (EVIDENCE_20260920T002045Z) had **1 failed check**:
`g6_nested_oracle,0,1`. Root cause was a **harness setup bug, not a
composition bug**: the use-site trace for name 11 (slot 36) was never
defined in `tc_setup` — the slot held an empty record, so `apply` returned
the cue unchanged and the oracle comparison correctly failed. The oracle
did its job. Fixed by adding the missing trace definition; the static
runner check was also tightened the same run (comment-stripping, after its
first version false-positived on the word "RNG" in code comments). Reran
from scratch: 92/92 pass. The failed first run's evidence bundle is kept.

## What this does NOT show (scope discipline)

- Substrate analog only: lab-canonical v1 opcodes on hand-built traces,
  not the 435 real R27 traces (native pickle reader still blocked).
- Three opcodes prove a **composition mechanism**, not general capability.
  The claim "capability builds up this way" is supported at the mechanism
  level (sound + refusal + reuse); generality across richer op vocabularies
  is untested.
- Trial scale is small (128-d cues, 64-trace store, 32-name registry,
  8-op cap). The scaling argument is analytic (§5 of COMPOSITION.md):
  O(cue_len) application + O(nops) sequencing + O(N_names) linear registry
  scan, linear memory — no per-element state, no N×N tables, no randomness
  at any scale.

## Determinism vs adversity (A3, as required)

- "The system is deterministic": byte-identical rebuilds, byte-identical
  double runs, zero RNG/time/syscall tokens in system source — the system
  cannot behave differently on the same state, by construction.
- "The test was adversarial": all adversity was designed, not sampled —
  poisoned-middle fold, provenance forgery, predicate smuggling, name
  squatting, strict-boundary cues, u8 wraparound cues, capacity overflow,
  unknown-name application. The system passed a hostile curriculum, not a
  random one.

## Next step (do not repeat at this scale)

**S2 scale test** (preregistered): 512-d cues (R27's native cue dimension),
256-trace store, 64-name registry, 64-op composite cap, full ADV suite
replayed 1:1, plus a timing assertion that seq/apply scale linearly in
cue_len. If S2 holds, **S3**: 1000 traces / 128 names. Separately: extend
the opcode vocabulary toward predicate families richer than FILTER_GT
(e.g. relational ops) to test whether the predicate-class structural test
generalizes — that is the next real threat to the BRANCH operator.
