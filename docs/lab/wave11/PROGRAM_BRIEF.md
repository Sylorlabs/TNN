# TNN Program Brief for wave11 investigators (2026-09-20)

You are an investigator in the TNN ("True Neural Network") research program, owned by Micah.
TNN is NOT an LLM, transformer, or tensor machine. It is a native-code (Zag language, Linux)
deterministic cognitive architecture. Read this whole file before designing anything.

## Standing program laws
1. **No randomness in AI decision paths.** No random exploration, no random tie-breaks, no
   stochastic policies. (One dated exception exists — see AMENDMENT_2026-09-20_RNG_ARM_B.md.)
2. **Reproducibility = byte-identical output from full logged state.** Not input alone: the
   complete internal state is logged, and replaying input + logged state must reproduce outputs
   byte-identically.
3. **Real mechanisms, real learners, native Zag.** No stubs as headline evidence; no Python
   where Zag is possible.
4. **Debates design trials; trials settle debates; kill criteria are binding** and preregistered
   BEFORE building.
5. **No-free-lunch:** benchmark alternatives hard; never promote preferences.
6. **Deliberate repair beats wholesale removal.** Fix mechanisms; don't trash them.
7. **RL/reward is red-team machinery only**, never the learning paradigm. Learning is
   scaffold-and-release with learner-initiated SIGNAL_DISCONNECT; learned = persists after disconnect.
8. **Memory is deliberate:** add, kill, pin, promote, demote, strengthen, weaken — all deliberate
   ops. Strength is set by judgment, never accumulated passively. Only a human/trainer force-pin
   is irreversible, and it is audited and visible.
9. **Felt intensity is dead.** The "feeling of importance" mechanism was retired 2026-09-20
   (K4 harm + K3' restatement fired): it was redundant with naive counting and mildly harmful.
   Do not propose feeling-based designs without addressing the retirement evidence.

## What TNN already has (proven, committed evidence on branch tnn-native-lab)
- **Deliberate memory substrate** (MA1: 58/58): deliberate kill/pin/promote, CORE unkillable,
  staged autonomy gates, append-only audit with replay to exact state.
- **Context switching as memory partitions** (11/11): contexts are deliberately managed partitions.
- **Eliminative hypothesis logic**: hypotheses die by evidence, not by vote.
- **Native reasoning control** (RC1/RC2/RC3: 40/40 at 1x/10x/100x episodes): TNN controls 100% of
  its reasoning machinery, 0% of the constitution (ledger, gates, self-change rules). It refused
  self-changes weakening integrity; a lying self-change was caught by post-change verification
  and rolled back.
- **Integrity under attack** (wave5/6): 137/137 checks, 1440/1440 trap-correct over thousands of
  genuinely attractive temptations at 10x/100x. Load-bearing: eliminative verification,
  learner-initiated disconnect, deliberative standards. Ledger/checker PROVE; they don't cause.
- **Debate/revision** (22/22): false-knowledge TNN revised all false claims against world records;
  truthful TNN uncorrupted. Limit: needs authoritative world records.
- **Five-organ integration** (in progress): C5 composition leak found and repaired (composition
  now distinguishes refuted material from live belief). C7 metric broken (double-counting —
  withdrawn as dead end). S100 scale leg stays gated.
- **Trust tiers** (wave9): H1 suspensive-contradiction-hold amendment survived; scheme holds.
- **Known hole (accepted, to be attacked):** truthful but sensor-deceivable — sustained
  observation spoofing breaks the hold. Micah accepts this may be the best achievable without
  hardcoding, but wants fixes tested and honest reports if none hold.
- **Perception:** audio and vision remain NOT_QUALIFIED. The old 76 torch perceptual parameters
  were proven unrecoverable (imported into git, never produced by committed code).
- **Scale so far:** RC3 at 100x episodes passed. Toolchain limit: no single slice > 2^25 bytes
  (33,554,432) can be indexed — chunking with identical logical semantics is the validated
  workaround. Target: 1000x episodes and long-horizon developmental runs.

## Micah's variation goal (the reason wave11 exists)
"i dont want TNN to always give the same output for same input — that gives more hardcoded
intelligence vibes — but at the same time it shouldn't be rng."
Humans don't roll dice, but they also don't give identical outputs to identical inputs: they
differ because their internal state differs. Target: **output = f(input, FULL internal state)**,
with state evolving lawfully. Same full state → byte-identical output. Different lawful state →
legitimately different expression. What MAY vary: expression, phrasing, path taken to a
conclusion, ordering, elaboration depth. What MUST NOT vary: verdicts, memory decisions
(kill/pin/promote), integrity refusals, ledger contents.

## Your deliverable
Write ONE markdown file with exactly these sections:
1. **Slice** — your assigned slice, one line.
2. **Falsifiable claim** — a claim phrased so a trial could kill it. No untestable prose.
3. **Design** — the concrete mechanism/spec (Zag-flavored pseudocode welcome). Precise enough
   that a builder could implement it without inventing semantics.
4. **Kill bar** — prereg-style: the exact numeric/logical condition whose firing kills the idea.
5. **Honesty notes** — where your design is weakest, what could go wrong, what you are NOT claiming.
6. **Next build step** — the single most informative thing to build/test next for this slice.

Rules: never propose RNG in a decision path (except Track 2, the fenced arm). Never propose
re-running completed cells or changing prereg rules. Cite committed evidence paths where you
lean on prior results (docs/lab/waveN/... on the branch). Keep it tight: 60–120 lines.
