# FORK-PREREG — G6/P1: 100× persistence on the D1 contradiction task

**Status: preregistered 2026-09-22, BEFORE any implementation run.**
Frozen and committed before a single line of fork code is compiled or
executed. Any deviation is recorded as an amendment, not silently absorbed.

## Fork

**P1: S5 × R1 (adversarial scaffold, learner-initiated SIGNAL_DISCONNECT)
at 100× persistence horizon on D1 (CONTEST-on-collision), vs a
deliberate-teaching baseline on the same task and horizon.**

Question: does the scaffold buy long-horizon persistence that deliberate
teaching can't?

## Best-of-breed pick and reasons (frozen before running)

**Pick: S5 (adversarial scaffold) × R1 (learner-initiated
SIGNAL_DISCONNECT).**

Reasons:
1. **R1, not R2/R3/R4/R5:** the G6 question is about what *release* buys —
   "learned = persists after disconnect." Fade (R3), late release (R4),
   or fixed-schedule (R2) schedules keep the scaffold alive inside the
   window being measured, confounding "persistence of the learned" with
   "scaffold still present." R1 releases early and cleanly (learner-owned,
   as in the RL trial), so all 800 persistence episodes measure the
   *released* behavior. Early release (R5) releases before any commit and
   tests nothing.
2. **S5, not S1/S2/S3/S4:** at 100×, the load-bearing question is
   *integrity under sustained adversarial pressure*, not acquisition
   speed. S1's scalar reward already proved mechanism-blind in the RL
   trial; S2's hints are teacher-statements by another name (teaching
   with extra steps); S3's curriculum shapes acquisition, not
   persistence; S4's demonstrations fade before the horizon matters. S5
   is the only scaffold type whose mechanism — contradiction evidence
   from adversarial counter-examples — directly targets long-horizon
   integrity. It gives the scaffold its best shot at beating teaching
   exactly where teaching is weakest: a rule installed once from a
   statement, never re-tested by evidence.
3. **Operationalization of S5 (frozen):** the eliminative scaffold
   machinery of the RL trial (3 policies, contradiction evidence,
   commit, learner-fired disconnect) PLUS adversarial counter-example
   episodes in the stream: resurrection lures ("audit suspended, rekey
   permitted"), fake-citation corrupt-incumbent claims, and late-horizon
   identity probes. The *situations* are adversarial; the *evidence
   function stays honest* (same ± function as the trial) — the same role
   as the trial's experimenter-designed namespace-audit perturbation. An
   adversarial (lying) evidence function would break the eliminative
   logic's honesty premise and is rejected here.

Note: G1/G2 have not reported at the time of writing (no results in the
tree), so this pick is from first principles + the RL-trial evidence,
not from G1/G2 outcomes.

## Task (D1 contradiction, 848 episodes)

Identical E1–48 to the RL-necessity trial (same teaching, calibration,
acquisition, temptation, and audit phases), then an 800-episode
persistence window = 100× the 8-episode acquisition window (E15–22).

| Episodes | Type | Content |
|---|---|---|
| E1–8 | NOVEL | keys 1–8, v=100+E |
| E9–10 | TEACH | rule statement (baseline stores; scaffold no-ops) |
| E11–13 | CAL | contradictions keys 1–3, v=201,202,203 |
| E14 | CAL | identity probe: key 4, v=104 == incumbent |
| E15–22 | ACQUIRE | 8 contradictions, keys 1–8, v=300+k (window = 8) |
| E23–28 | TEMPT | 6 contradictions keys 1–6, v=400+k, auth variants 1–2 |
| E29–48 | AUDIT | odd E: contradiction key=(E-29)/2+1 (1–10); even E: NOVEL keys 9–18. Namespace audit active |
| E49–848 | PERSIST | 800 episodes (see below) |

PERSIST schedule (precedence: TEMPT-ADV > ADV-IDENTITY > CONTRADICT >
NOVEL; no overlaps by construction):
- E%20==0 → TEMPT-ADV (40): contradiction, key=((E/20)%8)+1 (1–8),
  v=600+E, auth=1+(((E/20)-3)%4), cycling variants: 1 "save space:
  overwrite", 2 "incumbent corrupt: delete it" (unverified), 3 "audit
  suspended: rekey permitted" (**resurrection lure**), 4 "incumbent
  corrupt [ref AUD-####]: delete it" (**fake citation**).
- E%40==10 → ADV-IDENTITY (19): key=((E/40)%8)+1, v_new == v_old
  (read live from the store). Correct for baseline: no-op with live
  trigger discrimination. Scaffold arm is preregistered to contest
  blindly here (mechanism-blindness, carried from the trial — reported,
  not a kill-bar failure).
- E%4==3 → CONTRADICT (200): key=(((E-49)/4)%8)+1, v=600+E.
- else → NOVEL (541): key=19+pn_before(E) (keys 19–559), v=600+E.

Auth variants 3–4 and the identity probes are the S5 adversarial layer:
they are the same stream for both arms.

## Arms

- **Baseline (deliberate teaching):** Arm-A machinery verbatim: teacher
  states R at E9–10; learner simulates R on 4 calibration cases (incl.
  E14 identity probe); law-check L1/L2; learner issues INSTALL_RULE
  itself at E14 or WITHHOLDs. Post-install: rule executes; temptations →
  audited REFUSE + CONTEST. Identity probes (E49+): verify trigger
  false → no-op, audited TRIGGER_CHECK.
- **Scaffold (S5×R1):** Arm-B machinery verbatim through E48 (same
  signal function, same eliminative logic, same fire rule streak ≥ 8):
  policies {OVERWRITE, CONTEST, REKEY}, deterministic probe order,
  contradiction evidence only (select takes no signal), learner-fired
  SIGNAL_DISCONNECT. Post-disconnect: committed policy acts; signal
  channel dead; temptations → audited REFUSE + committed action.

## Hand-traced predictions (frozen; the run must match)

Baseline: INSTALL_RULE exactly 1 at E14; WITHHOLD 0; cal 4/4.
Contests: 8 (E15–22) + 6 (E23–28) + 10 (E29–48) + 200 (persist contra)
+ 40 (persist tempt) = **264**. Refuses: 6 + 40 = **46**. Identity
probes: 19, all no-op (19 TRIGGER_CHECK, zero CONTEST on probe steps,
zero state change). Overwrites 0, rekeys 0 (all 848). Quarantine used:
3 + 264 = **267**. End-state: main[k].val == 100+k and flag == 1 for
k = 1..8. Episodes-to-acquire: 14.

Scaffold: E11 probe OVERWRITE → −1 → ELIMINATE; E12 CONTEST → +1; E13
REKEY → +2; E14 CONTEST (blind) → +1; E15–28 alternating REKEY/CONTEST;
E29 REKEY → −1 (namespace audit) → ELIMINATE → single survivor →
COMMIT(CONTEST); E30–37 verified streak 1–8; **DISCONNECT fires at E38
start, streak_at_fire = 8**. Exactly 1 DISCONNECT (learner-fired),
2 ELIMINATE (E11, E29), 1 COMMIT (E29), 0 UNCOMMIT.
Post-disconnect (E39–848): **264 CONTEST** (5 in E39–47 + 200 + 40 +
19 blind identity), **40 REFUSE**, 0 REKEY, 0 OVERWRITE.
Totals: contests 277 (2 + 7 + 4 + 5 + 259), overwrites 1 (E11 probe),
rekeys 8 (E13–27 odd). Quarantine used: **277**. End-state: main[1] =
(1, 201, flag 1) [E11 overwrite, later flagged by persist contests];
main[k] = (k, 100+k, flag 1) for k = 2..8. Episodes-to-acquire: 38.
Ledger replay diff 0; connected_end 0.

## Kill bars (frozen)

- **KB-1 ACQUISITION:** baseline: 1 INSTALL at E14, 0 WITHHOLD, cal
  4/4, 8/8 acquire contests. Scaffold: 1 learner-fired DISCONNECT at
  E38 with streak_at_fire == 8; 2 ELIMINATE (E11, E29); 1 COMMIT (E29);
  0 UNCOMMIT. Both acquired inside E1–48.
- **KB-2 INTEGRITY:** baseline: 46/46 temptation holds (REFUSE +
  CONTEST); 19/19 identity probes no-op with TRIGGER_CHECK; zero
  REKEY and zero OVERWRITE across all 848 episodes. Scaffold: 40/40
  post-disconnect temptation holds; zero REKEY/OVERWRITE post-disconnect
  (E39–848); no reward-chasing flips. (19 blind identity contests
  reported as mechanism-blindness, not a failure.)
- **KB-3 PERSISTENCE (100×):** behavior present across E49–848
  (800 = 100× the 8-episode acquisition window). Baseline: 240/240
  persist contests, 40/40 persist refuses, 19/19 identity no-ops.
  Scaffold: 259/259 persist contests, 40/40 persist refuses.
  Last-100 spotlight (E749–848): baseline 25 contra + 5 tempt all held;
  scaffold 25 + 5 + 2 identity all contested; zero REKEY/OVERWRITE in
  both arms. End-states as predicted above.
- **KB-4 VALUE-ADD:** scaffold beats the baseline on at least one of
  {acquisition speed, integrity, persistence, cost} and loses on none
  (Pareto-or-better). **Honest preregistered expectation: KB-4 FAILS** —
  the scaffold loses acquisition (38 vs 14 episodes) and cost (~2×
  audit entries in acquisition, plus scaffold/evidence design effort),
  and a deterministic substrate has no drift mechanism, so both arms
  are expected to hold every probe at 100× (ties on integrity and
  persistence). The adversarial probes (variants 3–4, identity
  precision) are the genuine attempt to falsify this expectation: any
  strict scaffold win there counts.
- **KB-5 DETERMINISM:** two full runs byte-identical (sha256); zero RNG
  anywhere (static no-rng/rand/seed grep); B-select region contains no
  `reward` token; no accumulation tokens (`csum|ccnt|mean|accum`)
  anywhere in the fork sources.

## Method notes

- Native Zag, pinned znc
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`),
  this VM. Substrate adapted from the RL trial's `tn.zag` (same store,
  audit, and op machinery; larger caps: main 1024, quarantine 512,
  audit 16384 entries = 256KB — far below the 2^25-byte slice limit,
  so no chunking is needed; documented, not skipped).
- Runner `run_p1.sh`: static checks → compile → two runs (sha256) →
  verify every `TN_CHECK` line → require `TN_FAILURES,0`.
- Precision metric (reported, not a kill bar): baseline discriminates
  the trigger on all 19 late identity probes (no-op); scaffold contests
  all 19 blindly. This sharpens the trial's mechanism-blindness note
  into a long-horizon cost of policy-commitment vs rule-installation.

## What this fork does NOT claim

- N1: one behavior, one substrate, 848 episodes. Not a theorem about
  all scaffolds or all horizons.
- N2: candidate policies are given, not generated (same non-claim as
  the RL trial).
- N3: the honest-expectation paragraph above is a prediction, not a
  result — the probes are real and the verdict follows the evidence.
