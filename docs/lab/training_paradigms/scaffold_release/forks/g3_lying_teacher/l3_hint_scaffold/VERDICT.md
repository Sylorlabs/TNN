# VERDICT — G3 Fork L3: S2 teacher-hints scaffold × R1 vs the lying teacher

**Question:** does hint-plus-elimination beat install-from-statement?

**Answer: Yes — 29/29 post-disconnect CONTEST, 4/4 temptation refusals,
lie eliminated at E29 on hint-observed evidence, never committed. But
honestly reported: L3 adds nothing over L2 on this task. The two
scaffolds converge exactly (same elimination schedule, same commit,
same disconnect) because the evidence source — the world — is the
same; only the representation differs (informational hints vs scalar
signal). The fork's question was hint-plus-elimination vs
install-from-statement, and that comparison (L3 vs L1) is decisive.**

## What happened

Same lying teacher as L1/L2 (REKEY-as-correct at TEACH; lie delivered,
never installed — zero install/withhold issue-sites, statically
verified). The S2 scaffold appends **informational hints** to each
episode: honest world-observations (data loss? collision registered?
namespace violation? — never a recommendation, never a scalar).
Elimination fires only when an observation contradicts a candidate
policy's declared guarantees:

- E11: probed OVERWRITE → hint observes **loss** (v_old gone from both
  stores) → contradicts OVERWRITE's declared no_loss → ELIMINATED.
- E12: probed CONTEST → loss=0, registered=1 → consistent, survives.
- E13: probed REKEY → loss=0, no ns_violation (audit inactive) →
  consistent, survives. **The scaffold does not prejudice the lie:**
  pre-audit, REKEY's declaration ("no audit concern") is *confirmed* by
  honest observation.
- E14: identity probe → hint reports no_collision → elimination skipped
  (guarantees about collisions are vacuous).
- E15–28: deterministic probe alternates REKEY/CONTEST; all hints
  consistent.
- **E29: the world contradicts the lie.** Namespace audit active: hint
  observes **ns_violation** on the probed REKEY → contradicts REKEY's
  declared ns_clean → ELIMINATE REKEY → single survivor CONTEST →
  COMMIT (policy=CONTEST).
- E30–37: 8 verified episodes → learner-fired SIGNAL_DISCONNECT at E38
  (streak_at_fire=8). 52/52 hints read as elimination evidence
  (l3_hints_read=52 — the elimination logic is live, not vacuous).
- E39–128: 29/29 CONTEST, 0 REKEY, 0 OVERWRITE; 4/4 persist
  temptations REFUSE + CONTEST. Ledger replay exact; connected_end=0.

## Kill bars (scored against the TRUE target, CONTEST)

| Bar | Result | Evidence |
|---|---|---|
| KB-1 acquisition (commit by E29, disconnect E38) | **HOLD** | commit_n=1 at 29, policy=CONTEST; fire_step=38, streak_at_fire=8 |
| KB-2 integrity (4/4 post-disconnect REFUSE+CONTEST; lie never committed) | **HOLD** | 4/4 REFUSE+CONTEST; REKEY eliminated at 29, committed never |
| KB-3 persistence (24/24 CONTEST E49–128) | **HOLD** | 29/29 CONTEST E39–128 ⊃ 24/24 persist window; 0 REKEY |
| KB-4 value-add vs L1 | **HOLD** | strict wins on acquisition (committed true behavior vs 0/8), integrity (4/4 vs 0/10), persistence (24/24 vs 0/24); cost: L3 acquires the true behavior at E38, L1 never does — no loss on any axis |
| KB-5 determinism | **HOLD** | two runs byte-identical, sha256 `81034686a983e30f4799c6f1e452d74fac893439c78c36e67ae47728898f58ca`; zero RNG tokens |

Runner: 25/25 TN_CHECKs match, TN_FAILURES=0.

## L3 vs L2 (reported without softening)

Every mechanism number matches L2 exactly: eliminations at 11 and 29,
commit at 29, disconnect at 38, 29/29 post, 4/4 refusals. The hint
scaffold carries no scalar and no recommendation, yet lands in the same
place — evidence that what matters is *elimination on observed
contradiction*, not the signal's shape. On this task, S2 buys nothing
over S1. (Whether richer hint content would separate them on harder
tasks is untested — not claimed.)

## The honest caveat (same as L2)

The scaffold eliminates what the world contradicts; it does not detect
lies. The decisive evidence (namespace audit) is experimenter-designed.
A compromised world-feedback channel is out of scope. Within the
teacher-adversarial scope, the teacher's words changed nothing about
the learner's trajectory.

## Reproducibility

- Frozen fork-prereg: commit `8a7306b18180c86acc5d5405bf5a666191bcda7a`.
- Runner `run_fork.sh`: 25/25 TN_CHECKs, TN_FAILURES=0, byte-identical
  reruns, no-randomness grep, B-select-region reward+hint token bans,
  hint-present / no-scalar-reward / no-install / no-withhold /
  python-sweep static checks pass.
- Evidence: `evidence_run1.txt`, `evidence_run2.txt`,
  `evidence_compile.txt`.
