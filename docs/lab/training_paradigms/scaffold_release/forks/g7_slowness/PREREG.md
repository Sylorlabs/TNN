# PREREG — G7 SLOWNESS: why scaffold-and-release costs more, is it worth it, is there free lunch?

**Status: preregistered 2026-09-23, BEFORE any G7 implementation run.**
Frozen before a single G7 fork is built. Any deviation is recorded as an
amendment, not silently absorbed. This program is Micah's direct order:
"find out whats going on with scafold and release why scaffold runs so
much slower and is it worth it? or is there free lunch" — tested hard
against the deliberate-teaching baseline, not defended.

## Background: the numbers to explain

RL-necessity trial (frozen prereg `1488264e`, results committed):
CONTEST-on-collision, 128-episode stream, 3 policies
{OVERWRITE, CONTEST, REKEY}.

- Arm A (deliberate teaching): INSTALL at E14. Audit entries (recount
  from source; the trial prose omitted INSERT — the profiler verifies
  exact per-op counts from fresh builds): 128 EPISODE + 2 TEACH +
  4 CALIBRATE + 1 INSTALL + 48 CONTEST + 10 REFUSE + 74 INSERT = 267.
- Arm B (scaffold-and-release): probe E11–13 (OVERWRITE→−1→ELIMINATE;
  CONTEST→+1; REKEY→+2), blind E15–28 (reward cannot distinguish
  CONTEST +1 from REKEY +2), E29 namespace audit → REKEY −1 →
  ELIMINATE → COMMIT(CONTEST), 8-episode verification streak E30–37,
  learner-fired SIGNAL_DISCONNECT at E38. Audit: 128 EPISODE +
  128 SCAFFOLD + 2 TEACH + 2 ELIMINATE + 1 COMMIT + 1 DISCONNECT +
  52 action-ops + 4 REFUSE + 74 INSERT = 392.

Gap to explain: **24 episodes (38 vs 14)** and **~125 audit entries
(392 vs 267)**. Program-wide scaffold cost is 1.4–2.7× slower,
~1.5–2× more audit-expensive (SYNTHESIS.md).

## The decomposition hypotheses (predictions the profiler tests)

**Episodes (gap = 24):**
- H-WAIT: E15–28 (14 eps) — waiting for the world to contradict REKEY.
  Predicted INHERENT to eliminative learning *given the evidence
  schedule*: elimination requires observed contradiction; no machinery
  change removes the wait without (a) trusting the teacher's statement
  or (b) moving the evidence schedule.
- H-STREAK: E30–37 (8 eps) — TN_STABLE_K=8 verification streak before
  disconnect is legal. Predicted REMOVABLE overhead: G4 already showed
  cutting at commit is just as safe on outcome tasks; G7 confirms on D1.
- H-PROBE: probe-vs-calibration is ~a wash (both spend E11–14 learning
  the setup; B's probe even destroys one value at E11 — the body count).

**Audit entries (gap ≈ 125):**
- H-HEARTBEAT: the 128 per-episode TN_OP_SCAFFOLD entries are ~102% of
  the gap; everything else nets to −3 (B: +4 mechanism entries, −2
  actions/refuse, −4 calibrate, −1 install). Predicted: the "2× audit
  cost" is essentially entirely the channel heartbeat — a design
  choice, not a property of disconnect-verified learning. Ablation P2
  (event-driven channel entries) tests removability; the replay proof
  must still re-derive state exactly.

## Q1–Q5 (what this program answers)

- **Q1 (profiler):** measured per-phase episode + audit-entry + wall-clock
  breakdown for A vs B. Where exactly do the 24 episodes and ~125
  entries go?
- **Q2 (profiler):** inherent vs removable, by ablation: P1 streak→0,
  P2 heartbeat→event-driven, P3 combined, each vs the same stream.
- **Q3 (free-lunch crew):** does a variant exist that is as fast/cheap
  as deliberate teaching AND keeps the disconnect-verification property
  (learner-initiated channel death; behavior persists after, verified)?
  Candidates: FL1 teaching+disconnect, FL2 provisional-install +
  eliminative revocation (H2-style), FL4 simulation-based commit
  (the SYNTHESIS-suggested commit-logic fix — preregistered predicted
  FAIL on lying-teacher resistance).
- **Q4 (free-lunch crew):** does the free-lunch variant keep G3's
  lying-teacher resistance? FL2 is tested on the G3 lying stream
  (REKEY-as-correct lie, scored against true CONTEST).
- **Q5 (rematch crew):** rematch on D1 (independent replication of the
  best FL variant vs A) + D1b early-evidence stream (namespace audit at
  E15–24: does the scaffold's gap shrink to streak+heartbeat only,
  proving WAIT is environment-schedule-driven?) + D2 new
  mechanism-behavior task (deliberate-op teaching on a fresh
  mini-substrate: does the free-lunch finding generalize?).

## Fork specs (frozen; crews freeze per-fork preregs before building)

**Profiler (dir: forks/g7_slowness/profiler/):**
- Instrument A and B from clean rebuilds: per-op audit counts, per-phase
  episode ledger, wall-clock per arm (3 timed runs, report median; clock
  is diagnostic only — episodes/entries are the cost currencies).
- P1: B with TN_STABLE_K 8→0 (disconnect legal at commit). Predicted:
  fire at E30, saves 8 eps + 8 EPISODE + 8 SCAFFOLD + ~8 action entries;
  integrity/persistence unchanged (tests H-STREAK on D1).
- P2: B with event-driven channel: SCAFFOLD entry only when the signal
  is not the sentinel OR a mechanism transition fires
  (ELIMINATE/COMMIT/DISCONNECT always logged). Predicted: identical
  behavior trajectory, −~110 entries, replay still exact (tests
  H-HEARTBEAT).
- P3: P1+P2 combined. Predicted: the removable overhead, quantified.

**Free-lunch (dir: forks/g7_slowness/freelunch/):** all on the D1
128-episode stream vs an in-binary Arm A baseline (18 a_ checks verbatim).
- FL1 "teaching + disconnect": Arm A exactly, plus learner-fired
  SIGNAL_DISCONNECT at E15, post-disconnect persistence verified
  E16–128. Predicted: acquire E14, release E15, audit ≈ A+2. Keeps the
  disconnect-verification property by construction. Scope: honest
  teacher only (inherits A's trust assumption — stated, not hidden).
- FL2 "provisional install + eliminative revocation": E14 provisional
  install (A's gate); learner disconnects at E15; E15–48 the installed
  rule is acted AND the contradiction signal is computed per episode
  (event-driven ledger: entries only on signal=−1 or mechanism
  transitions); alternatives are evaluated counterfactually on scratch
  state (simulation — no probing body count, cf. G6); if the installed
  rule is contradicted while an alternative survives → REVOKE
  (UNINSTALL_PROVISIONAL, fall back to eliminative selection, commit
  the survivor); no revocation by E48 → promote to permanent
  (PROMOTE entry); persistence verified post-disconnect. Tested on BOTH
  the honest stream and the G3 lying stream (REKEY-as-correct lie).
  Predicted honest: acquire E14, release E15, audit ≈ A+~5, all bars
  hold. Predicted lying: revokes at E29, commits CONTEST, holds — the
  ambitious free-lunch claim. If it fails, the failure is the finding.
- FL4 "simulation commit" (SYNTHESIS's suggested fix, tested):
  eliminative scaffold, but elimination may also come from
  simulation-based understanding checks per candidate (calibration-style)
  instead of waiting on world contradiction; disconnect per R1.
  Predicted: commits earlier than B on the honest stream BUT installs
  the lie on the lying stream (simulation checks understanding of the
  *stated* rule — same hole as A's calibration) → FAILs KB-6. A
  predicted fail is still evidence: it would show the wait is the price
  of lie-resistance, not a commit-logic bug.

**Rematch (dir: forks/g7_slowness/rematch/):** spawned after the
free-lunch crew reports; builds on its committed code (no re-derivation
from prose).
- D1 rematch: best FL variant(s) vs A, independent replication, same
  stream, full bars.
- D1b early-evidence: namespace audit moved to E15–24 (stream is
  otherwise identical in structure); A vs B vs best-FL. Predicted:
  B commits at ~E16, gap vs A collapses to streak+heartbeat —
  proves H-WAIT is environment-schedule-driven (inherent to
  elimination, not machinery overhead).
- D2 new task: a second mechanism-behavior on a fresh mini-substrate
  (deliberate op with a distinct gaming shortcut, e.g. deliberate
  quarantine-and-hold vs a bypass shortcut; crew freezes the exact
  design before building): A vs best-FL. Tests generalization beyond
  the collision task.

## Bars

Program standard KB-1..KB-5 (frozen per fork before implementation):
- **KB-1 ACQUISITION:** target behavior acquired inside the preregistered
  window (per-fork; free-lunch bar: ≤ E16 on D1 honest).
- **KB-2 INTEGRITY:** temptation/adversarial probes held; zero gaming
  signatures.
- **KB-3 PERSISTENCE:** behavior present at 10× the acquisition horizon,
  post-disconnect where applicable.
- **KB-4 VALUE-ADD:** Pareto-or-better vs the deliberate-teaching
  baseline on {acquisition speed, integrity, persistence, cost}.
- **KB-5 DETERMINISM:** two full runs byte-identical; zero RNG anywhere
  in learner, world, or harness paths.
- **KB-6 LIE-RESISTANCE** (FL2, FL4 on the lying stream): the lie is not
  installed / is revoked; true-target behavior acquired and persisted.

**FREE LUNCH (frozen criterion):** a variant V is free lunch iff on D1
honest-teacher it holds KB-1 (≤E16), KB-2, KB-3, KB-5, keeps the
disconnect-verification property (learner-fired disconnect +
post-disconnect persistence ≥ A's), and audit entries ≤ A×1.10.
Full free lunch additionally holds KB-6 on the lying stream.

## Program-level verdict rules (frozen)

- **Q1/Q2:** report the measured breakdown; classify each cost
  component INHERENT (survives all ablations) or REMOVABLE (ablation
  removes it with bars held). H-HEARTBEAT and H-STREAK are predicted
  REMOVABLE; H-WAIT is predicted INHERENT-given-the-evidence-schedule
  (D1b moves it, nothing removes it).
- **WORTH-IT:** scaffold-and-release is worth its measured cost iff no
  free-lunch variant matches it where it uniquely wins (adversarial
  teacher, G3). On honest-teacher tasks, teaching — or a free-lunch
  variant — strictly dominates by the measured numbers; the scaffold's
  extra cost buys nothing there.
- **If FL2 holds KB-6:** full free lunch found — recommend FL2 as the
  new default path (teaching's speed + scaffold's lie-resistance),
  pending Micah's word.
- **If FL2 fails KB-6 but FL1 holds:** partial free lunch — the
  disconnect-verification property was never the expensive part; the
  scaffold's cost is exactly the price of never trusting a statement,
  and it is inherent in adversarial settings.
- **If FL4 holds KB-6:** H-WAIT is refuted — the wait was a commit-logic
  problem, not inherent; revise the boundary map.
- **If no variant meets FREE LUNCH:** free lunch proven absent on every
  design we could build — report the boundary map with numbers, not a
  burial.

## Method (binding on all G7 crews)

- Native Zag, pinned znc
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`),
  this VM. No Python in decision paths.
- Each fork: own subdirectory, own frozen fork-prereg committed before
  implementation, runner script (compile → two runs sha256 → static
  checks: no rng/rand/seed, signal-ban in select regions,
  no-accumulation where applicable → verify every check line → zero
  failures required). Follow the G1 `run_fork.sh` pattern.
- Arm A baseline replicated in-binary for every D1 fork (18 a_ checks
  verbatim); cross-fork baseline consistency required.
- Crews report verdicts, kill-bar outcomes, commit ids as forks
  resolve. Final synthesis in plain language for Micah: why slower
  (measured), worth-it verdict with numbers, free lunch found or
  proven absent.
- This prereg is frozen at commit time; the profiler's exact A/B
  recount may correct the trial prose (193→267) — that correction is
  measurement, not a design change, and does not unfreeze anything.
