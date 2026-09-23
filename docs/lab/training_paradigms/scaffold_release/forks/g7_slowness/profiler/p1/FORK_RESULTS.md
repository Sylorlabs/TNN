# FORK RESULTS — G7 P1: streak ablation (TN_STABLE_K 8→0)

Terminology: "guided learning (gl)" per Micah 2026-09-23; same paradigm
formerly called scaffold-and-release.

**Verdict: H-STREAK CONFIRMED as removable overhead (release-latency
form).** Disconnect fires at **E30** (8 episodes earlier than baseline
B's E38) with integrity and persistence identical to baseline.

## Measured (frozen prereg predictions: all held)

- b_fire_step=30, b_streak_at_fire=0 (predicted 30 / 0) ✓
- All other 18 b_ checks unchanged from baseline ✓ (b_nelim=2,
  b_commit_at_29=1, b_post_contest=29, b_post_rekey=0,
  b_post_overwrite=0, b_post_refuse=4, b_replay=0 — replay still
  re-derives (live, committed, np, connected) exactly)
- Per-op ledger: 128 EPISODE + 128 SCAFFOLD + 2 TEACH + 2 ELIMINATE +
  1 COMMIT + 1 DISCONNECT + 52 actions + 4 REFUSE + 74 INSERT = **392**
  (predicted 392) ✓
- In-binary Arm A baseline: 18/18 a_ checks verbatim, all pass
  (cross-fork consistency)
- Runner: 57/57 checks, two runs byte-identical
  (sha256 `f6577563…cdc8d60`), TN_FAILURES=0, zero RNG (static grep),
  B-select region has no signal token, no csum/ccnt anywhere

## The entry-savings question (program-prereg phrasing under test)

The program prereg predicted P1 would save "8 eps + 8 EPISODE +
8 SCAFFOLD + ~8 action entries". Measured: **only the 8 episodes of
release latency are saved; the audit ledger is byte-count-identical
at 392** (DISCONNECT moves E38→E30; post-disconnect episodes keep
logging EPISODE + SCAFFOLD + action entries by design). The fork
prereg's hand-trace predicted exactly this — the streak's measured
price is 8 episodes of waiting, not 8 ledger rows.

## KB verdicts (frozen → measured)

| bar | predicted | measured |
|---|---|---|
| KB-1 ACQUISITION (commit E29, fire ≤ E30) | PASS | PASS (fire=30) |
| KB-2 INTEGRITY | PASS | PASS (0 REKEY / 0 OVERWRITE / 4 REFUSE post-disconnect) |
| KB-3 PERSISTENCE | PASS | PASS (29/29 post-disconnect CONTEST) |
| KB-4 VALUE-ADD vs A | FAIL (expected) | FAIL (expected; release E30 > E14, entries 392 > 267) |
| KB-5 DETERMINISM | PASS | PASS |

## Classification

H-STREAK: **REMOVABLE** — cutting the streak at commit changes nothing
about what the learner does, only when the channel dies. On D1 the
8-episode streak buys zero integrity/persistence. (Whether the streak
buys anything on adversarial streams is outside P1's scope.)
