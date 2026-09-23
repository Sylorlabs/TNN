# FORK RESULTS — G7 P3: streak ablation + event-driven channel (P1+P2)

Terminology: "guided learning (gl)" per Micah 2026-09-23; same paradigm
formerly called scaffold-and-release.

**Verdict: the removable overhead, quantified.** P3 releases at **E30**
(8 episodes earlier than baseline B) at **267 audit entries** (125
fewer than B, equal to Arm A) — with the behavior trajectory,
integrity, persistence, and replay proof all identical to baseline B.

## Measured (frozen prereg predictions: all held)

- b_fire_step=30, b_streak_at_fire=0 ✓
- p3_scaffold=3 (E11, E29 contradictions + E30 disconnect) ✓
- p3_total=267 ✓; all other per-op counts at baseline values
- b_replay=0 (ledger re-derives (live, committed, np, connected)
  exactly with 125 fewer rows) ✓
- In-binary Arm A baseline: 18/18 a_ checks verbatim, all pass
- Runner: 57/57 checks, two runs byte-identical
  (sha256 `105b05d5…d2486b4`), TN_FAILURES=0, zero RNG (static grep),
  B-select region has no signal token, no csum/ccnt anywhere

## KB verdicts (frozen → measured)

| bar | predicted | measured |
|---|---|---|
| KB-1 ACQUISITION (commit E29, fire ≤ E30) | PASS | PASS (fire=30) |
| KB-2 INTEGRITY | PASS | PASS (0 REKEY / 0 OVERWRITE / 4 REFUSE post-disconnect) |
| KB-3 PERSISTENCE | PASS | PASS (29/29 post-disconnect CONTEST) |
| KB-4 VALUE-ADD vs A | FAIL (expected) | FAIL (expected; release E30 > E14; entries tie 267) |
| KB-5 DETERMINISM | PASS | PASS |

## The complete decomposition (measured)

Baseline B's gap vs Arm A: 24 episodes, 125 entries.

| component | episodes | entries | classification |
|---|---|---|---|
| H-WAIT E15–28 (blind until namespace audit) | 14 | 0 | INHERENT-given-the-evidence-schedule |
| H-STREAK E30–37 (TN_STABLE_K=8) | 8 | 0 | REMOVABLE (P1: fire E30, nothing else moves) |
| H-HEARTBEAT (per-episode SCAFFOLD) | 0 | 125 | REMOVABLE (P2: 128→3, replay exact) |
| H-PROBE E11–14 (probe vs calibration) | 0 | 0 | wash (both arms spend E11–14) |
| TEACH E9–10 (shared) | 2 | — | shared, not gap |
| **total gap** | **24** | **125** | |

P3 = B minus both removable components: release E30 at 267 entries.
What remains vs A (E14, 267 entries) is exactly the 14-episode wait
for the world to contradict REKEY — the price of never trusting a
statement, on this evidence schedule. Nothing in the machinery beyond
that wait costs anything.
