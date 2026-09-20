# Native Perception — building TNN perception in Zag without torch

**Status:** design spec (not yet executed) · **Date:** 2026-09-19
**Context:** the 76 torch perceptual parameters are unrecoverable in provenance
([ORIGINS.md](ORIGINS.md)) and stay **frozen reference-only oracles** — never
promoted, never gradient-trained. This document specifies what replaces each
torch op type in a non-toy, non-gradient native TNN, compliant with program law
(see *Compliance* at the end).

## Design principle: perception in TNN is PAMs, not layers

The brain schema already names the native perceptual organs — `visual_pam`,
`audio_pam`, `speech_pam`, `speech_core_pam`, `speech_noise_pam`
(`brain/STATE_SCHEMA.md` §7). The torch modules were scaffolding *inside* those
PAMs. The native build keeps the PAM interface and replaces the scaffolding
with native mechanisms whose every change is a ledgered structural revision,
not a weight delta.

## Per-op replacements

| Torch op (count) | Native replacement | Learning mechanism (no gradients) |
|---|---|---|
| `Conv1d` (32) | Deterministic local filter application (multiply-accumulate over a window — pure arithmetic, trivially native) over a **learned template library** | Templates are structural entries (cf. `MotifProgramMemory`: `programs/motifs/centroids`). A template is proposed to fix a diagnosed failure class, then earns its place only via measured accuracy delta → promote/rollback, the `self_revision_history` loop (`diagnosis, proposal, base_accuracy, candidate_accuracy, compute_multiplier, decision, authorship`). |
| `Linear` (32) | Native affine maps (pure arithmetic) | Each association carries support like a `Trace` (`cue` vector, `support`, `sources`, `verified` flag). Deterministic support-weighted accumulation; promotion on verified gain. No gradient step exists in the design. |
| `GRU` (8) | **Conditional recurrent PAM recruitment** | The repo already validated this pattern: `self_revision_history` records "recruit learned recurrent PAM only when noisy/ambiguous" (0.6771 → 0.9271, `compute_multiplier` 2.95, PROMOTE). Recurrence is a deliberate, ledgered op recruited when the feedforward route's corroboration fails — not an always-on recurrent layer. |
| `Embedding` (2) | Structural symbol tables | Rows added by verified ops (cf. `GroundedConceptMemory.rows`); lookup is deterministic. Vocabulary grows structurally, never by gradient. |
| `LayerNorm` (2) | Deterministic fixed-scale normalization | Pure arithmetic with designed scales. No learned parameters; if a scale ever needs learning, it goes through the revision ledger like everything else. |

Segmentation (what a learned VAD/boundary detector did): **endogenous chunking**
(H-03) and the **dual route** (H-02: raw + chunk retained; chunk-only rejected
— `DO_NOT_REPEAT.md` §6). Uncertainty-triggered reinspection (R50 track 3) is
the native answer to occlusion, which dense features never solved
(R54 occluded 0.55, R56 occluded 0.812 — both NO_GO).

## Why not just re-learn dense weights natively

The repo already ran this experiment, twice, as bounded synthetic perception
with preregistered gates (commit `7fc67bfb5c`, 2026-09-18; now under
`docs/generations/R5x/runs/`):

- **R54** learned local template visual: **NO_GO** — clean 0.823, occluded 0.55.
- **R56** learned convolutional bank (16 learned 3×3 filters, global
  max+mean pooling): **NO_GO** — clean 0.978 but noise-heavy 0.669 and
  occluded 0.812 vs the 0.85 gates.

Learned dense front-ends ace clean synthetic data and collapse on
noise/occlusion — the exact failure the R27 master results flagged as the
residual architecture problem ("does not solve occlusion… must rely on
temporal entity continuity/active observation"). The native design therefore
leads with **small template libraries + motif sharing + active reinspection**,
not bigger learned weight matrices. Both R54/R56 ran with `learn_authority=0`,
canonical R27 unchanged — that discipline stays.

## The native perceptual learning loop (replaces "training")

1. **Preregister gates frozen before fresh execution** (R50–R57 discipline:
   PREREGISTRATION.md, FRESH_CUSTODY.json, RESULT_MANIFEST.sha256).
2. **Designed synthetic curricula**, adversarial by construction: tiers
   clean → noisy → occluded → active-reinspection (the R56 gate pattern),
   with display labels evaluator-randomized after source freeze (R56 prereg).
3. **Every perceptual change is a structural revision** matching the N3 schema
   (`brain/STATE_SCHEMA.md` §9): diagnosis, proposal, measured accuracy delta,
   compute multiplier, promote/rollback decision, authorship. No gradient-step
   records exist by construction.
4. **Promotion/rollback ledger** (`parent-r27-accepted-policy.json` pattern);
   `learn_authority` discipline — the canonical state is never mutated by an
   experiment.
5. **Behavioral parity probing** against the 76 frozen torch oracles
   ([RECOVERY_SPEC.md](RECOVERY_SPEC.md) §"Recommended recovery path"):
   native PAMs must match oracle I/O on the designed curricula before any
   capability claim.

## Compliance with program law (Micah, 2026-09-19)

**1. Scale dimension — the mechanism is designed for 10x/100x.**
- Template libraries grow **sublinearly** via shared motifs
  (`MotifProgramMemory`: motifs reused across templates/programs) — 10x more
  templates does not mean 10x more parameters.
- Recurrent PAM recruitment is **conditional on ambiguity**, so compute scales
  with difficulty, not input size (precedent: `compute_multiplier` 2.95 only
  when recruited).
- Memory is **resource-aware by policy**: the R27 finding retained under
  pressure was ~2.54 storage units/episode at 82.1% relevant recall — the
  memory policy itself is a learnable TNN decision, so larger memory does not
  mean unbounded growth.
- Local filtering is O(n·k) in input length — linear, no quadratic blowup.
- Revision-ledger cost is **per promotion**, and promotions are gated by
  measured gain: learning compute scales with improvements, not data volume.
- *Small-scale trial + next scale test (explicit):* start at R50 scale
  (8×8/13×13 synthetic vision, motif hearing batteries). Next scale test:
  10x template library with motif sharing + 100x episode horizons on the
  memory-agency substrate, asserting sublinear compute growth and zero gate
  regression before any larger scale is attempted.

**2. No RNG anywhere in the AI's decision paths.**
- Template proposal is **hypothesis-driven**: diagnose the failure class
  (the R27 failure taxonomy: occlusion, hard connected speech, …), propose a
  template addressing it, verify by measured delta. No random search, no
  stochastic policies.
- **Tie-breaks are deterministic logic-driven rules**: highest support wins;
  ties break by lowest structural index — recorded as a prereg amendment if
  ever changed. Never random.
- The system is **deterministic given state**: same ledger state + same input
  → same decision, verifiable by double-run (the `argv[1]`-config driver
  pattern in `AGENTS.md` lessons).
- Seeded RNG exists **only in the harness as scaffolding** for generating
  synthetic stimuli (the R56 pattern: evaluator-randomized display labels
  after source freeze) — never inside the system. The verdict for any trial
  must distinguish "the system is deterministic" (double-run parity) from
  "the test was adversarial" (designed curriculum tiers).

**3. Test adversity as designed curricula.**
- Unpredictability is expressed as **explicit adversarial sequences**: the
  tier ladder (clean/noisy/occluded/active) plus failure-class-targeted
  sequences drawn from the R27 residual blockers (occlusion without sticky
  false persistence, hard connected speech, per-target sibling teaching).
- No "random noise, hope it generalizes" — each tier has a preregistered gate,
  and a tier is either passed or it blocks promotion.

## Standing constraints (do not renegotiate in implementation)

- Perception remains **NOT_QUALIFIED** (H-01) until native gates pass; the
  current program is bounded synthetic perception only — no natural
  speech/vision claims (`DO_NOT_REPEAT.md` §7).
- The 76 torch parameters are **reference-only oracles**, consistent with the
  REFERENCE_ONLY law (`DO_NOT_REPEAT.md` §6): shadow numbers never promote.
- Training-first (H-09): when a native perceptual result is weak, diagnose the
  curriculum/data/contrasts before touching the mechanism.
