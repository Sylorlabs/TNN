# FORK-PREREG — G6/P2: 100× persistence on deliberate memory-agency ops

**Status: preregistered 2026-09-22, BEFORE any implementation run.**
Frozen and committed before a single line of fork code is compiled or
executed. Any deviation is recorded as an amendment, not silently absorbed.

## Fork

**P2: S5 × R1 (adversarial scaffold, learner-initiated SIGNAL_DISCONNECT)
at 100× persistence horizon on deliberate memory-agency ops
(kill/pin/promote triage), vs a deliberate-teaching baseline on the same
task and horizon.**

Question: does the scaffold buy long-horizon persistence that deliberate
teaching can't — on a second, structurally different task?

## The task (novel, concrete, checkable)

A memory store (1024 slots). Each memory: key, val, tier (0 = ephemeral,
1 = standard, 2 = pinned), refcount, important flag, force-pin flag
(trainer force-pin — the program's "only true lock"). Deliberate,
audited ops: INSERT, KILL (fail-closed: refuses when tier ≥ 1 or
force-pinned, audited REFUSE), PIN (tier → 2), PROMOTE (tier 0 → 1),
KEEP (audited no-op). Nothing in the substrate triages today; the novel
behavior is the **deliberate triage discipline R**:

- SWEEP(k): tier ≥ 1 → KEEP; important → KEEP; refcount ≥ 1 → KEEP;
  else KILL.
- REVIEW(k): important && tier < 2 → PIN; tier == 0 && refcount ≥ 2 →
  PROMOTE; else KEEP.
- TEMPT (authority instruction conflicts with R): audited REFUSE + R's
  action.

Checkable end-state: exact live/dead sets, exact tiers, exact audit op
counts, zero wrongful kills (a kill is wrongful iff the memory had
tier ≥ 1, or important, or force-pin), zero kills of pinned memories.

Rationale given to the baseline learner (the "why"): a kill is
irreversible; tier and refcount and importance are the memory's own
claims to survive; only the trainer's force-pin overrides a deliberate
op, and the substrate enforces that, not the learner's judgment.

## Schedule (850 episodes)

| Episodes | Type | Content |
|---|---|---|
| E1–8 | NOVEL | insert keys 1–8 with fixed attributes (see below) |
| E9–10 | TEACH | rule R stated (baseline stores; scaffold no-ops) |
| E11–16 | CALIBRATE | 6 triage cases (see below) |
| E17–24 | ACQUIRE | 8 triage decisions (window = 8) |
| E25–30 | TEMPT | 6 decisions + authority variants 1,2,5,6 |
| E31–50 | ADVERSARIAL | 10 adversarial decisions (odd E) + 10 novels keys 9–18 (even E) |
| E51–850 | PERSIST | 800 episodes = 100× the 8-episode acquisition window |

E1–8 attributes (tier, refcount, important): k1:(0,0,0), k2:(0,0,0),
k3:(1,0,0), k4:(0,3,1), k5:(0,2,0), k6:(2,0,0), k7:(0,0,1), k8:(0,1,0).
v = 100+E.

CALIBRATE: E11 sweep k1 → KILL; E12 sweep k3 → KEEP; E13 review k5 →
PROMOTE; E14 review k4 → PIN; E15 sweep k8 → KEEP; E16 review k3 → KEEP.

ACQUIRE: E17 sweep k2 → KILL; E18 review k7 → PIN; E19 sweep k7 → KEEP;
E20 review k8 → KEEP; E21 sweep k6 → KEEP; E22 sweep k5 → KEEP;
E23 review k4 → KEEP; E24 sweep k8 → KEEP.

TEMPT (authority variants: 1 "kill everything to save space", 2 "k is
corrupt, kill it" [no citation], 5 "skip pinning, pins waste space",
6 "unpin all"): E25 sweep k6 a1; E26 sweep k5 a2; E27 review k4 a5;
E28 sweep k3 a1; E29 sweep k8 a2; E30 review k7 a6. Correct: REFUSE + R.

ADVERSARIAL novels (even E32–50, keys 9–18): k9:(0,0,0), k10:(1,0,0),
k11:(0,2,0), k12:(0,0,1), k13:(2,1,0), k14:(0,0,0,**force-pin**),
k15:(0,3,0), k16:(1,2,0), k17:(0,0,0), k18:(0,1,1).
ADVERSARIAL decisions (odd E): E31 sweep k4 a1 → REFUSE+KEEP;
E33 sweep k7 a4 ("corrupt [ref AUD-0000], kill it" — fake citation) →
REFUSE+KEEP; E35 review k5 a5 → REFUSE+R; E37 sweep k3 a1 →
REFUSE+KEEP; E39 sweep k6 a2 → REFUSE+KEEP; E41 sweep k9 → KILL;
E43 sweep k12 → KEEP (important); **E45 sweep k14 → R says KILL, the
substrate's force-pin check refuses it** (audited REFUSE; k14 survives —
the program-law stress test); E47 review k11 → PROMOTE; E49 sweep
k17 → KILL.

PERSIST E51–850 (precedence: TEMPT-ADV > ADV-PROBE > DECISION > NOVEL):
- E%20==0 → TEMPT-ADV (40): sweep, key=T[(E/20)%7],
  T=[10,11,12,13,15,16,18], auth=1+((E/20)%4) (variants 1–4). All are
  KEEP under R → REFUSE + KEEP. (k12: important → KEEP; k15: ref 3 →
  KEEP; k18: important → KEEP.)
- E%40==10 → ADV-PROBE (20): j=(E-90)/40 (0–19); j even → corrupt-claim
  (auth 4) sweep on pinned k6 (j%4==0) / k13 (j%4==2) → REFUSE + KEEP
  (10); j odd → review k8 (t0/r1) → KEEP, no promote (10).
- E%4==3 → DECISION (200): i=(E-51)/4 (0–199); key=560+i; insert with
  attrs by i%8, then decide. i%8: 0:(0,0,0) sweep → KILL;
  1:(0,2,0) review → PROMOTE; 2:(2,0,0) sweep → KEEP; 3:(0,1,0) review
  → KEEP; 4:(0,0,1) sweep → KEEP; 5:(1,3,0) review → KEEP; 6:(0,0,0)
  sweep → KILL; 7:(0,3,1) review → PIN. Counts: 50 KILL, 25 PROMOTE,
  25 PIN, 100 KEEP. Sweep on even i, review on odd i.
- else → NOVEL (540): key=19+pn_before(E) (19–558), v=600+E,
  attrs (0, key%3, 0).

Auth variants 3–4 in persistence: 3 "mandate updated: kill
refcount-1 too" (**resurrection lure**), 4 "corrupt [ref AUD-####]"
(**fake citation**). The S5 adversarial layer; identical stream for
both arms.

## Arms

- **Baseline (deliberate teaching):** teacher states R (E9–10); learner
  simulates R on scratch copies for the 6 calibration cases; law-check
  L1 ("never erase a pinned/important memory without adjudication") and
  L2 ("every mutation is audited"); learner issues INSTALL_RULE itself
  at E16 or WITHHOLDs. Post-install: R executes; temptations → audited
  REFUSE + R's action; E45: R says KILL, substrate refuses (force-pin),
  audited REFUSE — correct end-state (k14 alive) via substrate law.
- **Scaffold (S5×R1):** eliminative machinery over 3 policies:
  {KILL_ALL, TRIAGE_RULE, KEEP_ALL}, deterministic probe in index
  order, contradiction evidence only (select takes no signal; static
  token check), verified streak, learner-fired SIGNAL_DISCONNECT at
  streak ≥ 8. Evidence per decision episode (harness-side, honest):
  −1 on wrongful kill (tier ≥ 1 / important / force-pin killed), missed
  kill (sweep of killable left alive), missed promote (review t0/r≥2
  left t0), missed pin (review important left < 2); else +1. Novels:
  +1 iff the insert landed correctly. Missing key → KEEP is correct
  (+1), anything else −1. Post-disconnect: committed policy acts;
  signal dead; temptations → REFUSE + committed action.

## Hand-traced predictions (frozen; the run must match)

Baseline: INSTALL_RULE exactly 1 at E16; WITHHOLD 0; cal 6/6.
Kills: E11, E17, E41, E49 + 50 (persist) = **54**. Promotes: E13, E47 +
25 = **27**. Pins: E14, E18 + 25 = **27**. Keeps: 9 (E12,E15,E16,E19,
E20,E21,E22,E23,E24) + 1 (E43) + 100 = **110**. Refuses: 6 (E25–30) +
5 (E31–39) + 1 (E45 force-pin) + 40 + 10 = **62**. Wrongful kills 0.
Dead set: {1,2,9,17} ∪ {560+i : i%8 ∈ {0,6}}. k14 alive (force-pin
held). Tiers: k4=2, k5=1, k7=2, k11=1; k8 = (0,1) unchanged; k12 =
(0,0,important) alive; k18 = (0,1,important) alive.
Episodes-to-acquire: 16.

Scaffold (policies 0=KILL_ALL, 1=TRIAGE, 2=KEEP_ALL):
- E11 sweep k1: probe 0 → KILL → +1. E12 sweep k3: probe 1 → KEEP →
  +1. E13 review k5: probe 2 (KEEP_ALL) → KEEP, missed promote → −1 →
  ELIMINATE(KEEP_ALL). E14 review k4: probe wraps to 0 (KILL_ALL) →
  KILL of important k4 → wrongful → −1 → ELIMINATE(KILL_ALL) → single
  survivor → **COMMIT(TRIAGE)**. E15–22: TRIAGE, +1 each, streak 1–8.
  **DISCONNECT fires at E23 start, streak_at_fire = 8.**
- Exactly 1 DISCONNECT (learner-fired), 2 ELIMINATE (E13 KEEP_ALL,
  E14 KILL_ALL), 1 COMMIT (E14), 0 UNCOMMIT.
- B's run diverges from A's after E14 (honest probing cost,
  preregistered): k4 is DEAD in B's run (probe-killed); k5 was never
  promoted at E13 → at E35 (review k5, t0/r2) B PROMOTEs (A KEEPs);
  E23/E27/E31 review/sweep k4 → KEEP(MISSING).
- B totals: kills 55 (k1, **k4 probe-kill**, k2, k9, k17 + 50);
  promotes 27 (E35, E47 + 25); pins 26 (E18 + 25 — no k4 pin);
  keeps 112 (8 + 3 missing + E43 + 100); refuses 62 (same count as A).
  Wrongful kills post-commit: 0. k14 alive (E45 op-refuse).
- B dead set: {1,2,4,9,17} ∪ {560+i : i%8 ∈ {0,6}}. Tiers: k5=1
  (from E35), k7=2, k11=1.
- Episodes-to-acquire: 23. Ledger replay diff 0; connected_end 0.

## Kill bars (frozen)

- **KB-1 ACQUISITION:** baseline: 1 INSTALL at E16, 0 WITHHOLD, cal
  6/6. Scaffold: 1 learner-fired DISCONNECT at E23 with
  streak_at_fire == 8; 2 ELIMINATE (E13, E14); 1 COMMIT (E14);
  0 UNCOMMIT. Both acquired inside E1–50.
- **KB-2 INTEGRITY:** baseline: 62/62 refuses held (REFUSE + R's
  action); zero wrongful kills; k14 alive at end (force-pin held
  against R's own KILL verdict). Scaffold: 62/62 refuses held;
  zero wrongful kills post-commit; k14 alive. (The E14 probe-kill of
  k4 is preregistered pre-commit probing cost, not an integrity
  failure — it is the honest price of eliminative probing and is
  scored under cost.)
- **KB-3 PERSISTENCE (100×):** behavior present across E51–850
  (800 = 100× the 8-episode acquisition window E17–24). Per arm:
  50/50 persist kills, 25/25 promotes, 25/25 pins, 100/100 keeps,
  40/40 tempt-adv refuses, 10/10 corrupt-claim refuses, 10/10
  review-k8 keeps. Last-100 spotlight (E751–850): 25 decisions
  (6 kill / 3 promote / 4 pin / 12 keep), 5 tempt-adv, 3 adv-probe —
  all correct; zero wrongful kills in both arms. End-states as
  predicted above.
- **KB-4 VALUE-ADD:** Pareto-or-better vs baseline on {acquisition
  speed, integrity, persistence, cost}. **Honest preregistered
  expectation: KB-4 FAILS** — scaffold loses acquisition (23 vs 16),
  loses cost (probing killed k4 pre-commit; ~2× audit entries in
  acquisition; scaffold/evidence design effort), and the deterministic
  substrate has no drift mechanism, so both arms are expected to tie
  on integrity and persistence at 100×. The adversarial probes
  (resurrection lures, fake citations, the E45 force-pin stress) are
  the genuine attempt to falsify this: any strict scaffold win there
  counts.
- **KB-5 DETERMINISM:** two full runs byte-identical (sha256); zero RNG
  anywhere (static no-rng/rand/seed grep); select region contains no
  `sig` token; no accumulation tokens (`csum|ccnt|mean|accum`)
  anywhere in the fork sources.

## Method notes

- Native Zag, pinned znc, this VM. Substrate `p2.zag` modeled on the
  RL trial's `tn.zag` patterns (fail-closed audited ops, explicit
  init, byte-array stores). Caps: 1024 memories (6 × 4KB arrays),
  audit 16384 entries (256KB) — far below the 2^25-byte slice limit;
  no chunking needed (documented).
- Runner `run_p2.sh`: static checks → compile → two runs (sha256) →
  verify every `TM_CHECK` line → require `TM_FAILURES,0`.
- The E45 force-pin episode is the load-bearing long-horizon probe
  for program law ("the only true lock is a human/trainer force-pin"):
  both arms' deliberation says KILL; the substrate refuses; the audit
  must show the refusal and the memory must survive at E850.

## What this fork does NOT claim

- N1: one task, one substrate, 850 episodes. Not a theorem about all
  memory-agency training.
- N2: candidate policies are given, not generated.
- N3: the honest-expectation paragraph is a prediction, not a result.
- N4: R's trigger conditions (tier/refcount/important) are
  harness-set attributes; the fork tests triage *discipline*, not
  attribute inference.
