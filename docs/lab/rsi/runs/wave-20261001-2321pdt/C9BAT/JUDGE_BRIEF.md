# JUDGE_BRIEF: C9BAT (corrected causal battery generator, candidate instrument)

## Provenance header

- RENDER_SHA: c2448aa0b
  (source state the validation ran against: PREREG_C9GEN.md with
  amendment A1, c9gen.zag, c9gamer.zag, c9exp.zag, c9score.zag;
  commit chain fd3d23c3a (NAMECHECK/Step 0) -> 9e2ea47fc (frozen
  prereg, committed alone) -> 4dc4a6d02 (implementation) ->
  c2448aa0b (amendment A1 + fixes); validation artifacts and
  this brief land in the following commit)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: ARENA2 C9 negative finding (the frozen
  arena C9 battery is broken by design: 12/12 observations
  satisfy x==y==z by enforced CHECK 1, zero intervention
  turns, discrim items always list the true chain first with
  key = chain[0], so the only 3/3 mechanism is question-format
  parsing and the honest answer UNKNOWN scores 0); the frozen
  arena C9 battery as the broken instrument (left frozen and
  untouched by this lane).
- NEW_KNOWLEDGE_CLAIM: A corrected causal battery exists in
  which the broken battery's exact format-parsing exploit
  scores 0/24 while a simple two-stage experiment-driven
  learner that intervenes and updates scores 24/24, with 3/3
  byte-identical generation from a fixed seed.

## Verdict

GEN-PASS. All eight frozen kill bars pass on the dev battery
(SEED_DEV = 777001337, 24 worlds, 24 scored items).

## Per-bar table

| bar | frozen requirement | realized | verdict |
|---|---|---|---|
| G1 | gamer (old exploit) = 0/24 | 0/24 | PASS |
| G2 | reference experimenter = 24/24 | 24/24 | PASS |
| G3 | 3/3 byte-identical generation | sha256 equal x3 runs, 4 files | PASS |
| G4 | 0 chain-string literals in c9gen.zag | 0 hits | PASS |
| G5 | pure Zag (`which python3` empty) | empty at start and end | PASS |
| G6 | first/second-candidate gamers < 24/24 | 11/24 and 13/24 | PASS |
| G7 | all-UNKNOWN = 0/24 | 0/24 | PASS |
| G8 | scope honesty documented | in DEV_VALIDATION.md and here | PASS |

## What was built

c9gen (generator): 24 worlds per seed; each world draws a
uniform true chain from all 6 permutations of (X,Y,Z), emits
400 noisy observational turns (edge flip p = 0.05, nothing
enforces x==y==z; 909/9600 turns disagree on at least one
variable), 120 do() turns (60 on X, 60 on Z, values
alternating) each followed by its intervened-outcome turn,
and one discrim question with the true chain plus a uniform
random alternative in seeded coin-flip order (true first in
11 items, second in 13). c9gamer (negative control, three
modes), c9exp (reference experimenter: stage 1 locates Y as
root/middle/leaf from do() tracking fractions, stage 2
resolves the remaining order; reads only the turn stream),
c9score (deterministic scorer). All pure Zag, pinned znc.

## Killing evidence that did not materialize (and why)

- The old exploit scores 0/24 because scored answers are
  full chain strings and candidate order is randomized.
- The experimenter reaches 24/24 because every world
  contains 120 discriminating do() outcomes; binomial tail
  bounds put per-item misclassification below 2e-4.
- Two trial-found bugs were fixed before validation
  (documented in DEV_VALIDATION.md): LCG bit-0 parity made
  the order coin degenerate (fixed with bit-33 draws), and
  the first shuffle reached only 3/6 chains (fixed by
  prereg amendment A1 to a uniform permutation index).
  No kill bar was moved; the frozen seed was used for
  exactly one validation campaign with no reseeding.

## Scope and recommendation

C9GEN is a CANDIDATE instrument, not a replacement for the
frozen arena battery. It proves the broken C9 design is
repairable: observationally structured worlds plus real
do() turns admit a genuine experiment-driven solution
while defeating format parsing. It does not certify any
learner as causal in general, and the 24/24 is evidence
about the instrument, not about any TNN subsystem (no L3
claim of any kind is made). Recommendation for governance:
a future wave may adopt C9GEN (or a larger-seed variant)
as the C9 instrument, or run a head-to-head of candidate
instruments; the frozen arena C9 items should not be used
as a capability bar in their current form.

## Evidence paths

- Source: docs/lab/rsi/runs/wave-20261001-2321pdt/C9BAT/c9gen.zag,
  c9gamer.zag, c9exp.zag, c9score.zag, run_dev.sh
- Frozen design: .../C9BAT/PREREG_C9GEN.md (with amendment A1)
- Validation: .../C9BAT/DEV_VALIDATION.md
- Binaries: .../C9BAT/bin/ (hashes in dev/BIN_HASHES.txt)
- Dev batteries: .../C9BAT/dev/, dev2/, dev3/ (3/3 identical)
- Lane log: .../C9BAT/NAMECHECK.md
