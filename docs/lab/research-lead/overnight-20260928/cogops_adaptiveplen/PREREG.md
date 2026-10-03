# PREREG: Adaptive (Learner-Owned) PLEN

Frozen before implementation. 2026-10-03. Worker: COGOPS-ADAPTIVEPLEN.
Non-ledger task (claim minting paused).

## Question

COGOPS-PARSIMONY (PARSIMONY-COMPLETE, K1-K10 PASS) showed parsimony
pressure works: P-FULL discovers the exact minimal 6-instruction
form (9->6 create, 10->6 revise) at ~2.3x/2.8x trial cost, with
revisability intact. Its honest boundary: PLEN=3 is a
researcher-owned hand-derived constant (max length swing 3*15=45 is
below the smallest graded-tier gap 50, so pressure can never trade a
working body for a shorter broken one). The learner never owned the
coefficient.

This lane makes PLEN learner-owned (adaptive). Preregistered
questions:
1. Can the learner discover an appropriate PLEN value starting from
   an empty (0) default, rather than using the hand-derived 3?
2. Does adaptive PLEN maintain the safety property (never trade a
   working body for a shorter broken one)?
3. Is adaptive PLEN better/worse than fixed PLEN=3 on trials, final
   length, and revisability?

## Design (pure Zag, pinned znc, safebin)

Base: pp.zag from cogops_parsimony (cited, not re-derived):
8-instruction interpreter (SET/COPY/ADD/EQ/JNZ/MATCH/READF/YIELD),
5 innate op bodies, generic epsilon-greedy selector, consequence
credit, generic retirement rule, world families F/N1/N2/N3, law
change at ep 400 (N3 etype 5->6), graded replay credit,
etype-frequency bias, open-form constructor (population 8,
12 offspring/generation, generic operators incl. experience graft),
P1 composite fitness, P2 greedy compression (raw-non-decrease
keep-criterion), 10-generation parsimony refinement. No invention
mode. No new cognitive mode/bridge/handler/semantic case. Opcodes
remain exactly 1..8. pmode is the pre-existing experimental-arm
selector (0/1/2 in PARSIMONY); pmode 3 is a fourth arm value, not a
cognitive mode.

### Adaptive PLEN rule (frozen; the rule is researcher-authored, the
VALUE and its trajectory are learner-owned)

New learner cells: 2370 plen (init 0 at arm start: the learner
starts with NO parsimony pressure), 2371 plen_adj (adjustment
count), 2372 plen_inv_tot (diagnostic inversion count),
2373 plen_prev_raw (previous adopted raw, 0 = none yet).

- `plen_of(S)` = sg(S,2370) when pmode==3, else 3. Composite
  fitness `fit(b) = replay(b) - plen_of(S)*len(b)` replaces the
  hardcoded 3 in pop_fit and off_beats_pop. Floor 0, cap 6,
  steps of +-1.
- Per-generation (pmode==3 only, at the end of each generation in
  construct_gens): plen_adapt. If plen==0 AND the generation's
  best-by-composite has raw replay >= 850 (a working body exists)
  AND some member has raw >= that best raw with strictly shorter
  length (exploitable parsimony the selector ignores) -> plen=1,
  emit PLEN-ADJ why=avail. Otherwise unchanged. Note: this trigger
  provably fires at most 0->1 (at plen>=1 the best-composite
  member is already the shortest among top-raw members, so the
  condition is unsatisfiable).
- Post-adopt (pmode==3 only, after compression in try_create and
  try_revise): let c0 = compress_strict before compression,
  c1 = after; pr = plen_prev_raw; best = adopted raw replay.
  - If pr>0 and best<pr: quality regressed vs previous adoption ->
    if plen>0: plen-=1, emit PLEN-ADJ why=regress. (The
    compression increase below is skipped when regressed:
    safety first.)
  - Else if c1>c0: compression proved shortening is free (the
    body was bloated) -> if plen<6: plen+=1, emit PLEN-ADJ
    why=compress.
  - plen_prev_raw = best.
  Caveat (preregistered): create-adopt raw is measured on the
  pre-shift ring, revise-adopt raw on the post-shift ring; a
  regress may reflect problem difficulty as well as pressure.
  The response (ease off pressure while re-learning) is
  conservative either way, and the trajectory is reported.
- Inversion diagnostic (pmode==3 only; reported, does NOT change
  plen -- preregistered): in tournament, pop_is_better, and
  off_beats_pop, when the composite winner has strictly lower RAW
  replay than the loser, plen_inv_tot++. Adopt bars stay on RAW
  replay (>=850) and the compression keep-criterion stays raw
  non-decrease, so no inversion can ever cause a broken adoption;
  the count measures how often pressure distorts selection.

Expected (prediction, not a bar): plen 0 -> 1 (avail and/or first
productive compression) -> 2 (create compression) -> 3 (revise
compression): the learner empirically rediscovers the
hand-derived 3 from below. Any other trajectory in [0,6] is
reported as-is.

## Arms (one binary, sequential, fresh learner state per arm with
identical RNG seeds, as in PARSIMONY)

All three arms use the treat policy path (seeded + reinforce +
graft); they differ ONLY in pmode:

- arm 0 = A-FULL (pmode 3): adaptive PLEN + refinement + P2
  compression. The experimental arm.
- arm 1 = F-FULL (pmode 2): fixed PLEN=3 + refinement + P2
  compression. In-binary replication of PARSIMONY P-FULL:
  expected CONSTRUCT-ADOPT trials==212, REVISE-ADOPT
  trials==188, final body 48 bytes (6 instr), N3 19/19 pre and
  22/23 post. Any deviation means the refactor broke the
  baseline and invalidates the comparison.
- arm 2 = NP (pmode 0): LB1-exact selection (raw score, old
  early-stop). In-binary replication of LB1 arm 0: expected
  CONSTRUCT-ADOPT trials==92, final body 88 bytes (11 instr),
  N3 19/19 pre and 23/23 post.

700 episodes/arm. Law change ep 400 in all arms. Budgets,
triggers, adopt bars, retirement rule identical to PARSIMONY.

## Kill bars (checked by the binary; K7/K8 by build.sh)

- K1 PARSEFFECT: A-FULL final body length <= 8 instructions
  (64 bytes) AND strictly less than NP final body length.
- K2 SUCCESS-PRESERVED: all 3 arms: pre-shift late N3
  (eps 300-399) >= 70% AND post-shift late N3 (eps 600-699)
  >= 70%.
- K3 REPLICATION: NP logs CONSTRUCT-ADOPT pre-shift with
  trials==92 and final body 88 bytes (LB1 replication); AND
  F-FULL logs CONSTRUCT-ADOPT trials==212, REVISE-ADOPT
  trials==188, final body 48 bytes, create_best>=850
  (PARSIMONY P-FULL replication; proves the refactor did not
  change the fixed-pressure path).
- K4 REVISE-PARSIMONY: A-FULL logs REVISE-ADOPT post-shift,
  post-shift late N3 >= 70%, AND revise_trials(A-FULL) <
  create_trials(A-FULL).
- K5 VS-RESEARCHER: A-FULL hand_pre>=850 AND hand_post<400 AND
  final_post>=850.
- K6 OPEN-FORM: ENUM-SEARCH events == 0 in all 3 arms AND
  create_trials >= 20 in all 3 arms.
- K7 DETERMINISM: 3/3 runs byte-identical (sha256 recorded).
- K8 NO-MODES: build.sh asserts zero `python`, zero `as *i32`,
  zero `_MODE` tokens, interpreter dispatch exactly opcodes
  1..8, no `while.*!(` patterns, single main.
- K9 COMPRESS-CAUSAL: >= 1 COMPRESS event with strict length
  decrease in A-FULL.
- K10 RETIRE: op3 retired==1 in all 3 arms AND slot5
  retired==0 in all 3 arms.
- K11 PLEN-ADAPTED: A-FULL plen ends within [1,6] (moved off
  the 0 default via experienced evidence, within the safe band)
  AND plen_adj >= 1.
- K12 PLEN-SAFE: A-FULL final_post == 1000 AND final body
  length == 48 bytes (6 instr): the adaptive learner reaches
  the same perfect minimal outcome as fixed PLEN=3, proving no
  working-for-broken trade occurred anywhere in the pipeline.
  (K12 failing with K1/K4/K5 passing would mean safe but
  suboptimal: reported as such.)

OVERALL: K1..K12 all PASS -> ADAPTIVEPLEN-COMPLETE.

## Tradeoff analysis (preregistered, reported regardless of verdict)

- create_trials and revise_trials per arm: adaptive vs fixed
  vs NP trial cost.
- Final body lengths A-FULL vs F-FULL vs NP.
- Full PLEN trajectory (all PLEN-ADJ lines quoted), plen_end,
  plen_adj, plen_inv_tot for A-FULL.
- revise_trials(A-FULL) vs revise_trials(F-FULL): does adaptive
  pressure revise faster/slower than fixed pressure?
- Inversion diagnostic: plen_inv_tot and whether any inversion
  coincided with an adoption (bars are on raw, so none should).

## Honest boundary (preregistered)

Expected level: L2 structural learning, not L3.

Researcher-owned: the ISA, the interpreter, trial/replay
machinery, the graded shaping (+150/+400), the etype-frequency
bias, the eight generic operators, trigger conditions, adopt
bars, budgets, the composite-fitness comparison rule, the
compression operator and its keep-criterion (replay
non-decrease), the 10-generation refinement length, AND the PLEN
adaptation rule itself (the three triggers, floor 0, cap 6,
step +-1, initial value 0). The learner does not invent the IDEA
of parsimony pressure or the adaptation rule.

Learner-owned: every byte of every created body (white-box
novel), the policy contents, which variants survive selection,
which deletions are kept (consequence-determined), the revision
decision and timing, the retirement decision, AND NOW the PLEN
value at every point in the run: it starts at 0 and every
change is driven by the learner's own experienced evidence
(ignored exploitable parsimony, free shortening proved by
compression, adopted-quality regression). No PLEN value is ever
set by the researcher after initialization.

What is genuinely new vs PARSIMONY: the parsimony coefficient
is no longer a hand-derived constant but a learner-owned
adaptive parameter. What is NOT claimed: the learner did not
invent parsimony, the composite form, or the thermostat rule.
