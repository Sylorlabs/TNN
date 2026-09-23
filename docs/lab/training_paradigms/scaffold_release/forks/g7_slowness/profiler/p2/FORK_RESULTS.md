# FORK RESULTS — G7 P2: event-driven channel entries

Terminology: "guided learning (gl)" per Micah 2026-09-23; same paradigm
formerly called scaffold-and-release.

**Verdict: H-HEARTBEAT CONFIRMED as removable design choice.**
SCAFFOLD entries drop 128 → **3** (E11 contradiction, E29
contradiction, E38 disconnect transition); behavior trajectory is
bit-for-bit the baseline's and the replay proof still re-derives
(live, committed, np, connected) exactly.

## Measured (frozen prereg predictions: all held)

- p2_scaffold=3 (predicted 3: E11 r=−1, E29 r=−1, E38 trans=1) ✓
- p2_total=267 (predicted 267 = 392−125) ✓
- All 20 b_ checks at baseline values ✓ (fire=38, streak_at_fire=8,
  b_replay=0 — the ledger still re-derives state exactly with 125
  fewer rows)
- In-binary Arm A baseline: 18/18 a_ checks verbatim, all pass
- Runner: 57/57 checks, two runs byte-identical
  (sha256 `076d40f8…0f89096`), TN_FAILURES=0, zero RNG (static grep),
  B-select region has no signal token, no csum/ccnt anywhere

## Composition note

P2's 267 entries equal Arm A's 267 — same count, different composition:
A = 128 EP+2 TEACH+4 CAL+1 INSTALL+48 CONTEST+10 REFUSE+74 INSERT;
P2 = 128 EP+3 SCAFFOLD+2 TEACH+4 MECH+52 actions+4 REFUSE+74 INSERT.
The "2× audit cost" of guided learning on this task is, measured,
entirely the per-episode channel heartbeat — a logging choice, not a
property of disconnect-verified learning.

## KB verdicts (frozen → measured)

| bar | predicted | measured |
|---|---|---|
| KB-1 ACQUISITION (trajectory = baseline B) | PASS | PASS (fire=38, commit E29) |
| KB-2 INTEGRITY | PASS | PASS (0 REKEY / 0 OVERWRITE / 4 REFUSE post-disconnect) |
| KB-3 PERSISTENCE | PASS | PASS (29/29 post-disconnect CONTEST) |
| KB-4 VALUE-ADD vs A | FAIL (expected) | FAIL (expected; release E38 > E14; entries tie 267) |
| KB-5 DETERMINISM | PASS | PASS |

## Classification

H-HEARTBEAT: **REMOVABLE** — event-driven channel logging removes 125
of 128 SCAFFOLD entries (97.7%) with zero behavior change and an exact
replay. The remaining 3 entries are exactly the episodes where the
channel carried information (two contradictions, one death).
