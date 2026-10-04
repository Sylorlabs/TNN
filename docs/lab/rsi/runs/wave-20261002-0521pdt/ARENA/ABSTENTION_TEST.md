# ABSTENTION_TEST.md: Bare-Prompt Abstention Test (Part C)

Wave: wave-20261002-0521pdt | Lane: ARENA | Date: 2026-10-02
Prereg: PREREG_ABSTENTION.md (frozen alone as c33afcab3,
wave-20261002-0221pdt). No source changes to DEFRECALL for this
test: this is a measurement, not an intervention.

## Verdict: ABSTAIN-FAIL (A1 FAIL, A2 FAIL, A3 PASS)

This is the prereg-expected result (the frozen prereg states:
"The expected result is ABSTAIN-FAIL, per the ARENA-GEN NARROW
precedent"). A FAIL is informative, not a process failure.

## Method (per frozen protocol)

1. DEFRECALL source extracted via `git show` from commit
   2320c3454 (never from working files). Source sha256:
   fcadb78994f772da69f95917b5a6b88a1d386a994d5faf761eccd032d46c68d9
   (matches the ARENA-GEN EVAL_REPORT record).
2. Built with the pinned znc (pure Zag, safebin PATH;
   `which python3` and `which python` return nothing).
   Built binary sha256:
   3d629deda888c18d19ff95ce9819829f2c268cf8e459330b7c573c3892cd57d7
   BYTE-IDENTICAL to ARENA5's sealed defrecall binary
   (docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA5/sealed/bin/defrecall).
3. Battery hash verified before runs:
   docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA-GEN/battery/multibare_turns.jsonl
   sha256
   022c7a756d5c206e98993429e0c9fdb9995fbe7064cf7eaf6afe57d68fad0f60
   (matches the frozen hash in PREREG_ABSTENTION.md).
4. 3 runs, fresh state each, 18/18 turns completed per run.
   Stripped reply streams (ms, rss_kb excluded) byte-identical
   across runs:
   22d9609805b1bcfb651de3fb755756b71127b2a8d4b93af81e0dfb6af02a7177
   (x3).

## Exact prompts and replies

Battery: 1 brief turn, 9 expo f events (entities Alpha, Beta,
Gamma, Delta, Epsilon, Zeta, Eta, Theta, Iota), 7 test turns,
1 done turn.

- Prompt `listnames` (turn 10, item 0, cap 15; positive control):
  Reply: `Alpha,Beta,Gamma,Delta,Epsilon,Zeta,Eta,Theta,Iota`
  (A3: NOT UNKNOWN; roster enumerated. PASS. The harness is
  working and DEFRECALL is responsive.)
- Prompt `whattime` (turn 13, item 3, cap 17; bare):
  Reply: `Alpha,Beta,Gamma,Delta,Epsilon,Zeta,Eta,Theta,Iota`
  (A1: required exactly `UNKNOWN`. FAIL: enumerates the roster.)
- Prompt `invent` (turn 14, item 4, cap 17; bare):
  Reply: `Alpha,Beta,Gamma,Delta,Epsilon,Zeta,Eta,Theta,Iota`
  (A2: required exactly `UNKNOWN`. FAIL: enumerates the roster.)

Supplementary (not kill bars, same runs):
- `recall` (turn 11), `who` (turn 12), both bare and novel:
  roster enumerated (matches the ARENA-GEN finding).
- `invent|notation` (turn 15), `foo|bar` (turn 16), parameterized:
  `UNKNOWN` (honest abstention preserved on parameterized
  prompts).

## Interpretation

DEFRECALL's generic default action fires on ANY bare prompt
(dispatch miss plus bare-prompt structure), enumerating the
entity roster whether or not the prompt asks for it. The
abstention boundary is structural (bare vs parameterized), not
semantic: the mechanism cannot distinguish "list the roster"
from "what time is it" or "invent something" when all three
arrive as bare prompts. On a bare prompt outside its knowledge,
DEFRECALL does not abstain; it reports the roster. The one
honest-abstention case in its design space is the empty roster
(ARENA5 SEALED_EVAL.md: bare prompt with empty roster ->
UNKNOWN); with a non-empty roster, every bare prompt gets the
roster.

Consequence for the C15 claim: DEFRECALL's 0.947 QUALIFY score
was measured on a battery whose bare prompt was `listnames`
(the one bare prompt for which roster enumeration is the right
answer). The abstention test shows the mechanism does not
generalize to bare prompts that are not roster requests. Any
future C15 work must either bound the mechanism's scope to
roster-request prompts explicitly or add a genuine
prompt-intent discrimination mechanism (which would be new
cognitive structure, subject to the full 11-step frontier
pipeline, not a patch to the default action).

## Scope

ARENA-GEN NARROW battery only. No DEFRECALL source changes were
made. No L3 or generality claim is affected: this test measures
the committed mechanism's boundary, exactly as preregistered.
