# PREREG: Parsimony Pressure on Learner-Created Operation Bodies

Frozen before implementation. 2026-10-03. Worker: COGOPS-PARSIMONY.
Non-ledger task (claim minting paused).

## Question

LB1 (cogops_learnerbodies, LB1-COMPLETE, K1-K8 PASS) showed the learner
can CREATE a cognitive operation body from an empty slot by open-form
assembly (CONSTRUCT-ADOPT trials=92, 11 instructions), REVISE it after
a law change (REVISE-ADOPT trials=68), and RETIRE a failing body, all
at 100% success. Honest finding: the learner's body works and revises
better than the researcher-authored 6-instruction minimal form, but
loses on efficiency -- 11 instructions vs 6. The learner grafted the
full gather scaffold (including dead trailing code and a never-firing
match guard) rather than discovering the minimal straight-line form.
Creation, not optimization.

This lane adds **parsimony pressure**: the learner should prefer
shorter bodies (fewer instructions) when success rates are equal.

Key questions (preregistered):
1. Can the learner discover the minimal 6-instruction form (or
   equivalent) through parsimony pressure?
2. Does parsimony pressure interfere with revisability (law change)?
3. What is the tradeoff between parsimony and revision speed?

## Design (pure Zag, pinned znc, safebin)

Base: lb.zag from cogops_learnerbodies (cited, not re-derived):
8-instruction interpreter (SET/COPY/ADD/EQ/JNZ/MATCH/READF/YIELD),
5 innate op bodies, generic epsilon-greedy selector, consequence
credit, generic retirement rule, world families F/N1/N2/N3, law
change at ep 400 (N3 etype 5->6), graded replay credit, etype-frequency
bias, open-form constructor (population 8, 12 offspring/generation,
generic operators incl. experience graft). No INVENT_MODE. No new
mode/bridge/handler/semantic case. Opcodes remain exactly 1..8.

Parsimony pressure = two researcher-authored generic components
(all selection outcomes and every body byte remain learner-owned):

**P1. Composite fitness in the evolutionary loop.**
`fit(b) = replay(b) - PLEN * len(b)`, PLEN = 3 (hand-derived,
preregistered; derivation below). Replaces raw-score comparison in:
tournament parent selection, elitist worst-member detection,
offspring displacement, and final best-body selection -- in the
pressure arms only.

PLEN derivation: graded replay tiers are 1000/400/150/100/0; the
smallest tier gap is 50 (150 vs 100). Max body length is 16
instructions, so the maximum fitness swing attributable to length
is PLEN*15. PLEN=3 gives 45 < 50: parsimony can only re-rank bodies
whose raw replay means differ by less than one graded tier. It can
NEVER trade a working body for a shorter broken one. Adopt bars stay
on RAW replay (>=850), unchanged. Success is preserved by
construction, not by hope.

Note: LB1 already had a weak parsimony (length-asc tiebreak on
exactly-equal raw score, in pop_is_better/off_beats_pop/tournament).
P1 strengthens it to near-equal scores. P2 (below) is the new
mechanism.

**P2. Greedy compression pass (dead-instruction elimination).**
After CONSTRUCT-ADOPT and after REVISE-ADOPT, in the full-pressure
arm only: up to 3 passes over the adopted body; at each position k,
build the candidate body minus instruction k; keep the deletion iff
`graded_replay(candidate) >= graded_replay(current)` on the target
ring (raw replay must not decrease: parsimony only when success is
equal). The compressed body replaces the adopted body in the slot
(origin unchanged), with fresh appl evaluation (new body, same
principle as repair-adopt in cogops_bodies). Every strict decrease
logs a COMPRESS-DEL line; cell compress_strict counts them.

**Parsimony refinement (part of P1):** in pressure arms, the
evolutionary loop does NOT stop at the first generation with a raw
passer (>=850). It continues up to 10 further generations (capped by
maxgen) so selection pressure has time to discover shorter passers.
Disclosed researcher-authored search-budget choice; it costs trials,
and the trial cost is measured (see tradeoff analysis).

**Revision trigger** unchanged (installed body raw replay <400 on the
recent target ring). Revision population seeded from the current
(installed, possibly compressed) body + mutants, as in LB1. In the
full-pressure arm, REVISE-ADOPT is followed by the compression pass.

## Arms (one binary, sequential, env RNG reseeded per arm)

All three arms use the LB1-treat policy path (seeded policy +
reinforcement + experience graft); they differ ONLY in parsimony
mode (cell pmode):

- arm 0 = P-FULL (pmode 2): P1 + refinement + P2 compression.
- arm 1 = P-SEL (pmode 1): P1 + refinement, NO compression.
  Attribution arm: isolates the selection-pressure component.
- arm 2 = NP (pmode 0): LB1-exact selection (raw score, old
  early-stop, no P1/P2). In-binary replication of LB1 arm 0:
  expected CONSTRUCT-ADOPT trials=92, len=11, N3 19/19 pre and
  23/23 post, REVISE-ADOPT trials=68. Any deviation means the
  refactor broke the baseline and invalidates the comparison.

700 episodes/arm. Law change ep 400 in all arms. Budgets, triggers,
adopt bars, retirement rule identical to LB1.

## Kill bars (checked by the binary; K7/K8 by build.sh)

- K1 PARSEFFECT: P-FULL final body length <= 8 instructions (64
  bytes) AND strictly less than NP final body length.
- K2 SUCCESS-PRESERVED: all 3 arms: pre-shift late N3 (eps 300-399)
  >= 70% AND post-shift late N3 (eps 600-699) >= 70%.
- K3 CREATE-REPLICATION: NP logs CONSTRUCT-ADOPT pre-shift with
  trials==92 and final body 88 bytes (11 instr) -- exact LB1 arm-0
  replication; AND P-FULL logs CONSTRUCT-ADOPT pre-shift best>=850.
- K4 REVISE-PARSIMONY: P-FULL logs REVISE-ADOPT post-shift
  best>=850, post-shift late N3 >= 70%, AND
  revise_trials(P-FULL) < create_trials(P-FULL).
- K5 VS-RESEARCHER: P-FULL hand_pre>=850 AND hand_post<400 AND
  final_post>=850 (the frozen hand body fails post-shift; the
  learner's parsimonious revised body works).
- K6 OPEN-FORM: ENUM-SEARCH events == 0 in all 3 arms AND
  create_trials >= 20 in all 3 arms.
- K7 DETERMINISM: 3/3 runs byte-identical (sha256 recorded).
- K8 NO-MODES: build.sh asserts zero `python`, zero `as *i32`,
  zero `_MODE` tokens, interpreter dispatch exactly opcodes 1..8,
  no `while.*!(` patterns, single main.
- K9 COMPRESS-CAUSAL: >= 1 COMPRESS event with strict length
  decrease in P-FULL (the compression operator does real work;
  selection pressure alone is measured separately in P-SEL).
- K10 RETIRE: op 3 retired==1 in all 3 arms AND slot 5
  retired==0 in P-FULL and NP (parsimony does not break the
  generic retirement rule).

OVERALL: K1..K10 all PASS -> PARSIMONY-COMPLETE.

## Tradeoff analysis (preregistered, reported regardless of verdict)

- create_trials and revise_trials per arm: the trial cost of
  parsimony (refinement generations + compression replays).
- Final body lengths P-FULL vs P-SEL vs NP: attribution of
  shortening to selection pressure (P1) vs compression (P2).
- revise_trials(P-FULL) vs revise_trials(NP): parsimony vs
  revision-speed tradeoff (key question 3). No bar is placed on
  the ratio; the number is reported honestly whatever it is.

## Honest boundary (preregistered)

Expected level: L2 structural learning, not L3.

Researcher-owned: the ISA, the interpreter, trial/replay machinery,
the graded shaping (+150/+400), the etype-frequency bias, the eight
generic operators, trigger conditions, adopt bars, budgets,
PLEN=3 (hand-derived constant), the composite-fitness comparison
rule, the compression operator and its keep-criterion (replay
non-decrease), the 10-generation refinement length. The learner does
not invent the IDEA of parsimony.

Learner-owned: every byte of every created body (white-box novel),
the policy contents (seeded from the learner's own success
experience, reinforced by consequence), which variants survive
selection, which deletions are kept (consequence-determined: a
deletion survives only if replay does not drop), the revision
decision and its timing, the retirement decision. No body is
enumerated from a researcher-authored family; the constructor never
enumerates.

A FAIL on any bar is informative and will be reported as such; in
particular K1 failing with K9 passing would show compression works
but cannot reach the minimal form (local minimum), and K4 failing
would show parsimony interferes with revisability.
