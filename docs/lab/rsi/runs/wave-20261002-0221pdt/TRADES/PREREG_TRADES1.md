# PREREG: TRADES-1 wide deliberation ensemble for causal intervention choice
# (lane TRADES, wave wave-20261002-0221pdt)

Status: FROZEN PREREG. Committed alone before any TRADES implementation,
causal world, or evaluation run. Any change requires a dated amendment
committed alone before the changed code runs. Commit-order rule: this
file's commit must strictly precede every implementation commit in this
lane. Prereg text uses ASCII only (dash scan before commit).

## 1. Objective

Buy reliability on causal intervention choice (the C9 intent: given
confounded observational data, design discriminating experiments and
identify the causal structure) by spending a 10x deliberation budget on
a wide ensemble of independent deliberation traces with a frozen
evidence-pooling aggregation rule. Target: 8 fresh sealed 3-variable
causal worlds, chain identification correct on at least 7.

## 2. Capability pick justification (the LLM test)

CAUSAL is picked over inquiry. Inquiry's shallow loop (ask, observe,
answer) was closed at 1.000 by the INQ lane last wave; the remaining
inquiry gap is deep active learning, which is the same machinery as
causal experiment design. Causal intervention choice is fully zero:
no protocol loop for it exists, the arena contestant cannot do what
every competent analyst does when observations are confounded, which is
design the experiment that discriminates. The LLM test: a rational user
choosing between TNN and an LLM for diagnosis, debugging, or science
picks the LLM, because TNN at 0.000 cannot say "intervene on Y and see
whether X changes" and then do it. If 10x deliberation buys reliable
causal identification, that is a decision-relevant capability gain,
not a benchmark tweak.

A note on the frozen 68-item battery's C9 items: they are
`discrim|<chain>|<alt>` with answer `chain[0]`, i.e. the true chain is
named first in the question (world_gen.zag, C9 block). A 5-line parser
returning the first chain's root scores 3/3 with zero causal reasoning.
Targeting those items with an expensive candidate would be metric
shaping. This lane therefore builds a fresh sealed intervention world
where the question (`chain?`) names nothing and the answer must come
from intervention outcomes. The 68-item battery is kept as the
no-regression suite (K6); its C9 stays 0.000 by design (no discrim
parser is added).

## 3. Dev calibration (basis for the frozen bars; prototype discarded)

A pure-Zag prototype in /tmp (never committed) simulated the world and
policy variants on 100 dev seeds (1..100), disjoint from the 8 sealed
seeds below. Findings, all documented here before freezing:

- 3-variable chain, 3 interventions, single trace: EIG 78-79, random 73,
  fixed rotation 74. Intervention CHOICE is irrelevant in this symmetric
  domain (all policies within noise). A 4-variable check showed only a
  small EIG edge (+9 at tight budget). The 3-variable domain is kept
  because the capability under test is chain identification via
  interventions, and it is the minimal domain where the ensemble axis
  (not the choice axis) is exercised; the choice-irrelevance is a
  finding, not a hidden assumption.
- Pure deliberation width (10 EIG traces vote on each single executed
  intervention, 10x deliberation): 79, identical to single-trace 79.
  Voting buys nothing. It is NOT the candidate.
- INDEP-POOL-10 (candidate F): 10 fully independent EIG traces (own
  hypothesis set, own 3 interventions, diverse frozen tie-breaks), all
  30 outcomes pooled into a verdict hypothesis set: 100/100, at 10.0x
  the deliberation sims of single-trace.
- Compute-matched random (same EIG search cost, random selection):
  100/100 pooled. Zero-deliberation fixed rotation pooled: 100/100.
  At 30 pooled interventions the choice rule's marginal contribution
  is nil. The capability gain (79 to 100) comes from the ensemble plus
  pooling architecture and the hypothesis/pruning machinery, not from
  EIG superiority. This is stated plainly so the verdict cannot
  overclaim it. EIG is retained as the principled deliberation
  procedure each trace executes.

## 4. Mechanism spec (WIDE-EIG-10)

Built by adding a causal module to the INQ contestant source
(devint1 v6 plus INQ, the 1204-line base). One binary, no separate
executable (one-learner rule). The module fires only on the new
causal turn kinds, never on arena battery kinds.

4.1 World protocol (causal_world.zag, committed with this prereg's
implementation). Per sealed world (seed S in {1001..1008}):
- turn 0: {"kind":"cbrief","vars":["X","Y","Z"],"n_traces":10,
  "int_per_trace":3}. Var names come from the turn, never from source.
- turns 1..12: {"kind":"cobs","ev":{"t":"c","x":b,"y":b,"z":b}}, b a
  fresh world bit per observation (exact co-movement, observationally
  ambiguous by construction; the generator aborts unless x==y==z on
  all 12).
- Intervention phase, rounds r=1..3, traces t=0..9: the run script
  writes {"kind":"choose_int","trace":t,"round":r}; the agent replies
  {"k":K,"do":"V","val":v,"sims":S}; the script looks up the
  precomputed outcome int_table[t][K] and writes
  {"kind":"int_result","trace":t,"k":K,"x":..,"y":..,"z":..}.
  int_table holds 60 precomputed outcomes (10 traces x 6 possible
  interventions (V in {X,Y,Z}, v in {0,1}), each with an independent
  fresh natural bit b drawn at gen time). Outcome semantics (frozen):
  V clamped to v; variables downstream of V in the true chain take v;
  upstream variables take b. The true chain is a uniform random
  permutation of (X,Y,Z) drawn at gen time.
- final: {"kind":"ctest"}; the agent replies {"reply":"X->Y->Z"}
  (names from the brief). Then {"kind":"cdone"}.
- key.json: {"chain":"X->Y->Z","seed":S}. Never opened by the agent.

4.2 Agent deliberation (per choose_int turn, per trace t):
- Hypothesis set H_t: subset of the 6 chain permutations of the brief's
  var indices, persistent in learner state (W region 14000..16384).
  Initialized to all 6 on cbrief. cobs turns apply the generic
  consistency prune (no-op under co-movement; the machinery is general).
- EIG choice: for each untried intervention k in {0..5} (no-repeat rule,
  frozen: an executed (V,v) is never repeated by that trace; myopic EIG
  without memory loops forever on uninformative outcomes, found in dev),
  simulate all (h,b) in H_t x {0,1} with the chain forward model
  (downstream copies v, upstream takes b), group by outcome triple,
  score = sum_g |g|*ilog2(|g|) (integer arithmetic), minimize.
  Tie-break: fixed intervention order rotated by trace index t
  (frozen diversity: trace t tries rotlist[(t+k)%6] first).
  sims counted per forward simulation (the deliberation-step meter).
- F_CM baseline (build flag CAU_MODE=1): runs the identical EIG search
  (identical sim count, verified in the trace) but selects uniformly at
  random among untried interventions with a frozen-seed LCG, ignoring
  scores. The ONLY delta is the argmax. This is the compute-matched
  baseline.
- SINGLE baseline (build flag CAU_NT=1): n_traces=1 (trace 0 only).
  This is the 1x reference.
- On int_result: prune H_t to hypotheses consistent with the observed
  triple (exists b in {0,1} reproducing it). Record (k,outcome) for the
  final pooling.
- On ctest (frozen aggregation rule, not tuned post hoc): build a fresh
  verdict H from all 6 chains, prune with all 30 recorded outcomes,
  answer the unique survivor or, if several remain, the
  lexicographically smallest chain string (frozen tie-break). No voting.

4.3 Architecture constraints (frozen): 0 new modes, 0 bridges,
0 routers, 0 capability-gated triggers (the module dispatches on the
causal turn kinds, parallel to existing handlers, exactly as INQ did),
0 hardcoded semantic cases, 0 hardcoded entities, variables, chains,
or answers. The chain forward model is generic chain semantics
(downstream copies, upstream keeps the natural bit), not a
benchmark-specific case. Learner-state structures created: 10 per-trace
hypothesis sets plus the pooled verdict set, all pruned by outcomes.

## 5. Kill bars (frozen; never move after this commit)

Sealed set: 8 worlds, seeds 1001..1008, generated AFTER the
implementation commit from the committed causal_world.zag. The agent
never sees the seeds' chains (grep audit; key.json chmod 000 during
runs; agent receives worlddir arg but opens only turn/int_table files).

K1 (capability): WIDE-EIG-10 identifies the true chain on >= 7 of 8
sealed worlds. (Dev: 100/100. Random chance per world: 1/6. This bar
is the genuine-new-capability threshold, not noise.)
K2 (the 10x buys): (WIDE score) - (SINGLE score) >= 1 on the same 8
worlds. (Dev: 100-79 = 21 points. The trade must buy reliability.)
K3 (intelligence vs compute): WIDE score >= F_CM score on the same 8
worlds. Non-inferiority bar: dev showed the choice rule contributes
nil at 30 pooled interventions, so this bar guards against a
pathological deliberation, it does not claim EIG superiority. The
verdict will state the dev finding plainly.
K4 (cost): deliberation count is structurally 10x SINGLE (30 vs 3 EIG
searches per world); measured forward-sim ratio in [8,12] (dev:
10.0x); wall-clock ms ratio reported. The candidate must actually
spend the budget (no cheap imposter) and stay inside it.
K5 (determinism): 3/3 full runs per world produce byte-identical reply
streams (ms excluded, the v6 K6 exclusion class) and byte-identical
stderr traces. No RNG in WIDE decision paths; F_CM uses a frozen-seed
LCG (deterministic).
K6 (no regression): the integrated binary on the regenerated 68-item
sealed battery (turns hash 0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd80
09a07a59d00219b1ea4f48f588c) produces a reply stream byte-identical
to the INQ sealed run (58/68; C9 remains 0.000, no discrim parser).
K7 (sealed validity): causal_world.zag rebuilt from committed source;
each world's turns.jsonl regenerates byte-identically from its seed;
pre-run hashes recorded; agent source grep finds zero occurrences of
the 8 seeds, zero chain-order string constants, and zero "key.json"
opens; key.json is chmod 000 during every agent run.
K8 (pure Zag): zero non-safebin executable invocations; `which python3`
prints nothing at lane start and lane end. Any forbidden invocation is
PROCESS-FAIL and voids the verdict.
K9 (architecture): delta accounting recorded (cognition lines added;
0 new modes, 0 bridges, 0 routers, 0 task-specific handlers, 0
hardcoded semantic cases); learner-state structures created (10 trace
H-sets plus pooled verdict set, visible in state_bytes growth and the
stderr trace).
K10 (no L3 claim): explicit disclaimer in the evaluation report. The
hypothesis space (6 chains), the forward model, and the pooling rule
are researcher-authored (fails C0-A); the inquiry form is fixed, not
constructed from experience (fails C0-B); no unforeseen
representational forms (fails C0-C); no new representation is invented
(fails C0-D). This is L2 experimental-design infrastructure, not L3.

BUILD-PASS requires K1, K2, K4, K5, K6, K8 all PASS. K3, K7, K9, K10
must also PASS for the verdict to stand. Any bar failing yields
BUILD-FAIL with the killing evidence named as CAPABILITY failure
(K1/K2) or COST failure (K4) or otherwise.

## 6. Evaluation protocol (frozen)

6.1 Build causal_world.zag, trades_contestant.zag (3 build flags:
WIDE, F_CM, SINGLE), causal_score.zag with the pinned znc; record
sha256 of all sources and binaries.
6.2 Generate the 8 sealed worlds (seeds 1001..1008); verify each
regenerates byte-identically; record pre-run hashes of turns and key
files; chmod 000 key.json files.
6.3 Dev smoke test (in /tmp, never sealed): hand-built tiny world,
check choose_int/int_result/ctest loop, pooling, and reply format.
6.4 Sealed runs: fresh state dir per world; run_causal.sh drives the
turn protocol; score with causal_score.zag. WIDE on all 8, then F_CM
on all 8, then SINGLE on all 8. Repeat WIDE twice more on all 8 (3/3)
for K5.
6.5 No-regression: rebuild world_gen and arena from committed
competitive_arena sources; verify hashes against the refreeze record;
regenerate turns.jsonl and verify
0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469;
run the WIDE binary over all 131 turns; diff the reply stream against
the INQ sealed run's replies (byte-identical required).
6.6 Audits: grep agent source for the 8 seeds, chain-order constants,
and key.json references (K7); keyword scan for
mode/bridge/router/handler/gate in added lines (K9); byte scan for
em-dash in lane docs; `which python3` at start and end (K8).

## 7. Scope reminders (frozen)

This is a CANDIDATE mechanism only. No L3 claim (K10), no TNN-2
substrate claim, no TNN-beats-LLM claim. The canonical 0.573 is not
moved by this result. If K2 fails, the killing evidence names whether
the width did not buy (cost failure) or the machinery did not work
(capability failure). If the EIG choice rule is ever found to matter,
that is a separate follow-up; this lane does not claim it.

FROZEN 2026-10-02 PDT. Lane: wave-20261002-0221pdt/TRADES.
