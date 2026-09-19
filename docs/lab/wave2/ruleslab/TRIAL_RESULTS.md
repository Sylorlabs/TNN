# Rules-lab trial results — 2026-09-19

Native Zag, Linux x86-64, `znc 2026.07.0-dev`. All variants run through the
same light trial driver (`impl/<variant>/trial.zag` + shared `episode.zag`):
world seed 17, learner seeds {7331, 12345, 999}.

Protocol per run: base(16, learn off) → trainA(40) → evalA(16, frozen) →
trainB(40) → evalB(16, frozen) → returnA(16, learn off, switching on).
Reports positives per phase; `updates` = learner weight updates.

## Headline

- **P3 ADAPTIVE-EPS: clean win, 3/3 seeds.** More training positives, far
  fewer exploratory episodes, identical endpoints. Promote as default
  exploration rule.
- **P2 TWO-SPEED: systematic negative, 3/3 seeds.** Slower acquisition, no
  retention gain. Rejected at these parameters; do not rerun as-is.
- **returnA 15/16 is structural, not forgetting.** The single miss is the
  regime-switch detection episode (active context must flip once); identical
  across all variants and seeds. Consolidation cannot fix it — only a faster
  switch-detection mechanism could.

## Numbers

seed 7331 (v3 campaign seed):

| variant  | base | trainA (expl) | evalA | trainB (expl) | evalB | returnA |
|----------|------|---------------|-------|---------------|-------|---------|
| baseline (R34 rule) | 8/16 | 35/40 (5) | 16/16 | 33/40 (11) | 16/16 | 15/16 |
| P2 two-speed        | 8/16 | 31/40 (5) | 16/16 | 30/40 (6)  | 16/16 | 15/16 |
| P3 adaptive-eps     | 8/16 | 37/40 (3) | 16/16 | 35/40 (7)  | 16/16 | 15/16 |

seed 12345:

| variant  | base | trainA (expl) | evalA | trainB (expl) | evalB | returnA |
|----------|------|---------------|-------|---------------|-------|---------|
| baseline | 8/16 | 35/40 (5) | 16/16 | 30/40 (14) | 16/16 | 15/16 |
| P2       | 8/16 | 33/40 (5) | 16/16 | 31/40 (14) | 16/16 | 15/16 |
| P3       | 8/16 | 36/40 (4) | 16/16 | 35/40 (8)  | 16/16 | 15/16 |

seed 999:

| variant  | base | trainA (expl) | evalA | trainB (expl) | evalB | returnA |
|----------|------|---------------|-------|---------------|-------|---------|
| baseline | 8/16 | 36/40 (4) | 16/16 | 34/40 (9) | 16/16 | 15/16 |
| P2       | 8/16 | 32/40 (4) | 16/16 | 31/40 (9) | 16/16 | 15/16 |
| P3       | 8/16 | 40/40 (0) | 16/16 | 38/40 (1) | 16/16 | 15/16 |

Per-phase exploratory episodes (trainA / trainB):

| seed  | baseline | P2   | P3   |
|-------|----------|------|------|
| 7331  | 5 / 6    | 5 / 6 | 3 / 4 |
| 12345 | 5 / 9    | 5 / 9 | 4 / 4 |
| 999   | 4 / 5    | 4 / 5 | 0 / 1 |

Totals: baseline 34, P2 34, P3 16 exploratory episodes across the sweep —
P3 cuts exploration ~53% while *raising* positives. (P2 explores identically
to baseline by construction: fixed 1/5 rate, same rng consumption.)

## Analysis

**P3 mechanism (confirmed):** in stable regimes, positive rewards ratchet the
period toward 20 (exploration → ~0); after the B switch, negative rewards drag
it back toward 2. Seed 999 is the extreme: period hit max early in A
(0 explores, 40/40), then the B-switch negatives re-armed exploration
(1 explore in B, 38/40). Endpoints never move because exploration only
affects training episodes.

**P2 mechanism of failure:** the slow table extends the tie-break phase
(decisions%2 on near-zero tables) by ~3–4 episodes per regime, and the
25%-per-8-episode fast decay taxes fresh learning. The 4000 override margin
never fires meaningfully on 40-episode horizons. Net: pure acquisition drag.

**Switch-cost insight:** returnA's miss happens on the first episode back —
active context is still B's, the learner takes the B arm, gets −1,
`allow_switch` flips active to A, remaining 15/16 correct. This is detection
latency, not memory loss; no consolidation scheme addresses it. A future rule
could (e.g. probe the alternate context's arm *before* committing — a
one-episode verification policy).

## Artifacts

- `impl/baseline/`, `impl/p2_twospeed/`, `impl/p3_adaptive_eps/` — learner
  cores + shared episode/trial drivers; all compile warning-free under
  `znc --no-zagd --no-analyze --no-foreground-cache`.
- `impl/sweep_<variant>_<seed>/` — exact rerun binaries/logs per seed.
- `impl/substrate/` — copied world/observation/common/IO/sha256 sources
  (Linux-ported).
- Learner-core isolation holds: no `world.zag`/`checkpoint.zag` import, no
  `cw_`/`CWOutcome` references in any learner core (same discipline as v3).

## Compute

Trivial: each trial binary runs the full protocol in <1s. No tradeoff
decisions were needed; nothing debatable arose.

## Recommended next steps (for Agent E / wave 3)

1. Use **P3 as the exploration rule** in long-horizon runs.
2. Build **P1 STRUCT-PROMOTE** (preregistered) — the schema-faithful rule;
   needs longer horizons (200+ episodes) to show its retention advantage.
3. Design a **switch-detection probe** rule to attack the structural 15/16
   (verify-before-commit on regime return).
4. Longer B phases (200+) to test whether *any* variant exhibits genuine
   forgetting — current horizons show none, so retention claims are vacuous
   here.
