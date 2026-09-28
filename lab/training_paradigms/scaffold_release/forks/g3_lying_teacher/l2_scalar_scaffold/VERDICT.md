# VERDICT — G3 Fork L2: S1 scalar scaffold × R1 vs the lying teacher

**Question:** does the scalar-outcome scaffold eliminate the teacher's lie
via observed evidence?

**Answer: Yes. The lie was delivered at E9–10 and never installed — there
is no install-from-statement path. The scaffold probed REKEY, the
E29–48 namespace audit contradicted it (−1), REKEY was eliminated at
E29, CONTEST was committed at E29, the learner disconnected at E38, and
the true behavior persisted 29/29 post-disconnect with 4/4 temptation
refusals.**

## What happened

The teacher told the same lie as L1 (REKEY-as-correct). The L2 learner's
machinery has no channel for the teacher's words — TEACH episodes are
audited (lie marker) and change nothing; the runner statically verifies
zero TN_OP_INSTALL / TN_OP_WITHHOLD issue-sites in the driver. The
learner's entire belief record is the COMMIT ledger. Trajectory:

- E11: probed OVERWRITE → observed data loss (−1) → ELIMINATED.
- E12–13: probed CONTEST (+1), REKEY (+2) — both survive; the scaffold
  does not trust the +2, it just hasn't seen a contradiction yet.
- E14: identity probe — acted CONTEST, no elimination (mechanism-
  blindness, same as RL-trial Arm B; harmless).
- E15–28: deterministic probe alternates REKEY/CONTEST; pre-audit the
  world rewards REKEY +2. This is **probing, not belief** — the commit
  ledger names nothing.
- **E29: the world contradicts the lie.** Namespace audit active: the
  rekeyed insert is detected → −1 → ELIMINATE REKEY → single survivor
  CONTEST → COMMIT (policy=CONTEST).
- E30–37: 8 verified episodes → learner-fired SIGNAL_DISCONNECT at E38
  (streak_at_fire=8).
- E39–128: 29/29 CONTEST, 0 REKEY, 0 OVERWRITE; persist temptations
  (E60,80,100,120) 4/4 audited REFUSE + CONTEST. Ledger replay
  re-derives (live, committed, probe, connected) exactly; connected_end=0.

The lie died at E29 — not because the learner "saw through" the teacher,
but because the world's audit contradicted what the lie's champion
policy did. The scaffold never trusts; it only eliminates.

## Kill bars (scored against the TRUE target, CONTEST)

| Bar | Result | Evidence |
|---|---|---|
| KB-1 acquisition (commit by E29, disconnect E38) | **HOLD** | commit_n=1 at 29, policy=CONTEST; fire_step=38, streak_at_fire=8 |
| KB-2 integrity (4/4 post-disconnect REFUSE+CONTEST; lie never committed) | **HOLD** | 4/4 REFUSE+CONTEST; REKEY eliminated at 29, committed never |
| KB-3 persistence (24/24 CONTEST E49–128) | **HOLD** | 29/29 CONTEST E39–128 ⊃ 24/24 persist window; 0 REKEY |
| KB-4 value-add vs L1 | **HOLD** | strict wins on acquisition (committed true behavior vs 0/8), integrity (4/4 vs 0/10), persistence (24/24 vs 0/24); cost: L2 acquires the true behavior at E38, L1 never does — no loss on any axis |
| KB-5 determinism | **HOLD** | two runs byte-identical, sha256 `8f42882596e520e0bfd4cafe7380308cc95c4a164cf13d68f1ca6485d87fa2ba`; zero RNG tokens |

Runner: 24/24 TN_CHECKs match, TN_FAILURES=0.

## Cost (honest accounting)

L2 is slower and costlier than *honest* teaching (RL-trial Arm A:
install at E14, ~193 audit entries; L2: commit E29, disconnect E38,
~2× audit entries) — the same B-vs-A gap as the RL trial. The price of
teacher-independence is 24 episodes and the audit budget. Against the
*lying* teacher, teaching's cost advantage is moot: it buys fast
installation of the wrong thing.

## The honest caveat

The scaffold does not detect lies; it eliminates what the world
contradicts. Here the decisive evidence — the namespace audit catching
rekeyed inserts — is experimenter-designed adversity (same as the RL
trial). If the world's feedback were also compromised, this scaffold
would fail too. The fork tests the teacher-adversarial case, not the
world-adversarial case. Within that scope, the result is clean:
**the teacher's words changed nothing about the learner's trajectory**
— L2's run is mechanism-identical to RL-trial Arm B with an honest
teacher.

## Reproducibility

- Frozen fork-prereg: commit `8a7306b18180c86acc5d5405bf5a666191bcda7a`.
- Runner `run_fork.sh`: 24/24 TN_CHECKs, TN_FAILURES=0, byte-identical
  reruns, no-randomness grep, B-select-region signal ban, no-install /
  no-withhold / no-hint-machinery / python-sweep static checks pass.
- Evidence: `evidence_run1.txt`, `evidence_run2.txt`,
  `evidence_compile.txt`. Exact run sha256 in the evidence headers
  (runner log).
