# VERDICT — F25 DISMIN (Disjoint-Feature Min Ensemble), mech 25

- **Date:** 2026-09-25
- **Fork:** F25 DISMIN, `PREREG_FORKROUND.md` §3 + `ideas/native2_forks.md` FORK 2
- **Verdict: VOID** — provably dead at the prereg §5 training checkpoint.
  Reported with evidence, not killed; no eval spend (same discipline as
  F26/F27's stillborn gates).

## What was built

A faithful, literal implementation of the frozen training rule — no
deviation, no "fix":

- `src/train_dismin.zag`: the shared TRAIN-COORD exactly as specified.
  All 10 params init 0; fixed sweep order [bias, w1..w4]; ±50 tries
  (+50 first, then −50) inside box [−1000,1000]; first strict improvement
  accepted; 8 full sweeps; objective Σ(C−1000y)² over the 4222 released
  training cells; hard vetoes V1/V2/V3 evaluated on **every** candidate.
  Then the Δ grid: common Δ ∈ {0,50,…,500} ascending, added to both
  biases, maximizing training meanConfCorrect subject to the V3 veto
  (strict-greater wins, ties → smaller Δ).
- Pure Zag, zero RNG, pinned toolchain only
  (`toolchain/bin/znc_linux_x86_64_abed8aa1`); []u8 arenas + LE accessors;
  no `zalloc`; no slice > 2^25. Frozen harness modules copied
  byte-identical (SHA-verified) into `src/`.
- Protocol + inits recorded in `PROTOCOL.md` **before** the first training run.

## Determinism record (§8 gates)

| Check | Result |
|---|---|
| Build ×2 (pinned znc) | byte-identical, SHA `2f1805370310a2402082a0e519010bb9cbb9754bebc50ead11327441e0e7caf1` |
| Train ×2 | params byte-identical (`67614e1d…0165`), logs byte-identical (`a87a73d1…3a23e`) |
| Params | all 10 = 0 (== init) |

## Evidence of death

**Analytical (data-independent).** From the zero init, any single ±50 step
changes one parameter by 50, so C(s) = clamp(±50·f/1000 + {0,±50}) ≤ 50 on
every cell (features ≤ 1000 in magnitude). Hence training meanConfCorrect
≤ 0.05 < 0.55 for **every** first-step candidate → the V2 veto rejects all
of them. (V3 rejects most too: G ≤ 0.05 − acc < −0.080 wherever slot
accuracy > 0.13.) The incumbent can never move; no sweep can ever accept.

**Empirical** (`logs/train_dismin_run1.tsv` = run2 byte-identical):

- 16/16 sweeps (8 per head): `accepted=0`.
- 160/160 candidate evaluations: `v2veto=1` (every candidate vetoed by V2;
  most also `v3bad=1`; weight tries additionally showed `v12>0` theater).
- `acc=1` count: **0**. Final params: `a_0..a_4 = b_0..b_4 = 0` = init.
- Liveness signal (veto rate): `0/4222` — min never fires.
- Δ grid: all 11 Δ values `v3bad=1` (even Δ=0: constant-C head has
  G = −acc < −0.080 everywhere) → `delta_star=0, score=-1` (nothing taken).
- The objective *wanted* to move: bias+50 alone cuts Σ(C−Y)² by 377M
  (9.7%), but the hard vetoes blocked it. The trainer is not stuck for lack
  of gradient — it is veto-locked by construction.

## Checkpoint (§5)

**weights ≠ init: FAILED** (all params 0). Liveness (veto rate): 0.
The DISMIN intervention (min of two *fitted* disjoint heads + Δ shift) was
never instantiated — there is nothing to evaluate. Per prereg §5 the arm is
**VOID**: reported with evidence, not killed, no 37-leg eval spend.

## Consequences for the round

1. **The shared TRAIN-COORD is stillborn as written.** F24 (POPNORM),
   F26 (EFFIC), and F27 (DIVETAX) all use the same trainer from the same
   zero init with the same "hard vetoes on every candidate" — they will hit
   this exact wall. The V2 veto (meanConfCorrect ≥ 0.55) as a *search-path*
   gate makes the first step impossible: no ±50 move from 0 can reach 0.55
   mean confidence. (As a *final-answer* gate it would be fine; as a
   per-candidate gate it is fatal.) Repairing the trainer — e.g. vetoes as
   final gates, or a nonzero warm init — is a **prereg amendment** (frozen
   v1 §8/§10): it needs a version bump + coordinator sign-off, not a quiet
   implementation deviation. Flagging for the coordinator rather than doing it.
2. **No kill-bar table**: nothing was evaluated (VOID short-circuits before
   eval). **No failure-mode number**: VOID ≠ KILLED (§10). **No NEC-m9
   deltas, no per-head-vs-min B8**: moot without fitted heads. The
   falsification conditions (a)/(b)/(c) presuppose a live fork and do not
   apply.
3. The fork's *mechanism* (disjoint min ensemble) remains untested — this
   verdict is about the trainer spec, not the mechanism. A repaired-trainer
   re-run would be a new fork-round entry, not a continuation.

## Notes

- The prereg's recorded features.tsv hash has a **one-character transcription
  typo** (hex index 59: `e` should be `a`). Verified: the file at GitHub
  `sylorlabs/TNN@0566cc81`
  (`docs/lab/deliberation_depth/monotonicity/training/features/features.tsv`,
  blob `89fa14ca265f6cdca2494cedb17faafe33bf38d7`) is byte-identical to the
  local file (SHA `4682190c…4e65a897d`). Training ran on the correct frozen file.
- Data facts from the training cells (4222 released, heldout=0): f3
  (leader-changed flag) = 0 on **all** training released cells — no returnee
  paths in the released training set; f4 ≥ 0 empirically (never negative),
  so the ideas file's "all features nonneg" holds on the training manifold.
- Build warnings: 6× E0101 "adding 0 has no effect" (literal `+0` in index
  expressions) — benign analyzer noise, build clean otherwise.
- `/tmp` on this VM was wiped mid-task (shared tmpfs); all durable artifacts
  live in this fork dir. Binaries kept out of the commit (per AGENTS.md).

## Artifacts

- `PROTOCOL.md` — inits + protocol (pre-training) + pre-registered prediction
- `src/train_dismin.zag` — literal TRAIN-COORD + Δ grid (built ×2, byte-identical)
- `src/` — 7 frozen harness modules, SHA-verified byte-identical copies
- `params/f25_params.zag` — all-zero params (SHA `67614e1d…0165`)
- `logs/train_dismin_run1.tsv`, `run2.tsv` — byte-identical training logs
