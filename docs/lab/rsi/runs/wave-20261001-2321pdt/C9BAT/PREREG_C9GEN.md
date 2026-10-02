# PREREG: Corrected causal battery generator (C9GEN, wave-20261001-2321pdt)

Status: FROZEN PREREG. Committed alone before any generator,
gamer, experimenter, or scorer implementation, binary, dev
battery, or evaluation run. Any change to the design below
requires a dated amendment committed alone before the changed
code runs. Commit-order rule: this file's commit must strictly
precede every implementation commit in this lane.

## 1. Objective

Build a CORRECTED causal (C9) battery generator as a NEW
candidate instrument, addressing the ARENA2 negative finding:
the frozen arena C9 battery is broken by design (12/12
observations satisfy x==y==z by enforced CHECK 1, zero
intervention turns, discrim items always list the true chain
first with key = chain[0], so the only 3/3 mechanism is
question-format parsing and the honest causal answer UNKNOWN
scores 0).

This instrument is a CANDIDATE only. It does not replace the
frozen arena battery. Whether any future wave adopts it is a
governance decision outside this lane. No L3 claim, no
TNN-beats-LLM claim, no canonical-score claim is made here.

## 2. Frozen design parameters

SEED_DEV = 777001337 (dev battery seed; fixed)
NWORLDS = 24 (dev battery worlds; N = 24 scored items)
NOBS = 400 (observational turns per world)
KDO = 60 (do() queries per intervention variable per world)
PFLIP_NUM = 5, PFLIP_DEN = 100 (edge noise p = 0.05)
HI = 0.75 (experimenter high-agreement threshold; fractions
compared as agree*100 >= 75*count in integer arithmetic)

RNG: the same LCG as the arena world_gen.zag
(s = s*6364136223846793005 + 1442695040888963407, 8-byte
little-endian state buffer, rng_range via modulo), seeded
once from SEED_DEV. The single RNG stream is the only
entropy source. No per-item hand authoring.

## 3. World model (c9gen)

Variables X=0, Y=1, Z=2, binary.

3.1 True chain: Fisher-Yates shuffle of [0,1,2] driven by the
seeded RNG. chain[0] = root, chain[1] = middle,
chain[2] = leaf. All 6 permutations reachable; none
hand-picked.

3.2 Observational turns: sample root bit from rng_range(2);
each downstream node copies its parent bit and flips it
iff rng_range(100) < 5. Emitted as
{"t":"c","x":0,"y":1,"z":0}.
The observation distribution carries genuine correlational
structure: adjacent chain pairs agree with probability
0.95, endpoint pairs with probability 0.9025, so the
middle node is statistically identifiable from
observations (chain identified up to reversal; direction
requires intervention). Nothing enforces x==y==z; the
broken battery's CHECK 1 exactness is gone by design.

3.3 Intervention turns: for each world, KDO=60 do() turns on
X then KDO=60 do() turns on Z, values alternating 1,0,1,0...
Each do() turn {"t":"do","var":"X","val":1} is immediately
followed by its outcome turn
{"t":"do_out","x":1,"y":1,"z":0}, computed by intervened
ancestral sampling in chain order root, middle, leaf:
the intervened node is fixed to val; a non-intervened
root draws rng_range(2); a non-intervened downstream node
copies its (possibly intervened) parent and flips iff
rng_range(100) < 5. The do() outcomes discriminate chain
direction: do(root) moves all descendants; do(leaf) moves
nothing; do(middle) moves only its downstream side.

3.4 Discrim item: candidates = the true chain string plus
one alternative drawn uniformly by the RNG from the other
5 permutations, listed in RNG coin-flip order. Item line:
{"t":"q","cap":9,"q":"discrim|X->Y->Z|Z->X->Y"}.
Chain strings are built programmatically from single
variable names plus "->"; no full chain-string literal
appears in the generator source. The key file records
the true chain string per item. The key is never
chain[0] positionally: the scored answer is the full
chain string and the true chain is equally likely to be
listed first or second.

3.5 Turn order per world: NOBS obs turns, 2*KDO do/do_out
pairs, then the single discrim question. Worlds are
independent: all per-world draws come from the one
seeded stream in fixed order, so the whole artifact is a
pure function of SEED_DEV.

3.6 Outputs (in the given outdir): turns.jsonl, key.txt
(one "idx|chain" line per item), worlds.txt (per-world
audit: true chain, alt, which listed first), manifest.txt
(params and counts).

## 4. Negative control (c9gamer)

Implements the broken battery's exact exploit as a
negative control. Modes:
- old: parse the first candidate after "discrim|", emit
  its first variable (e.g. "Z"). This is the mechanism
  that scored 3/3 on the frozen battery.
- first: emit the first candidate's full chain string.
- second: emit the second candidate's full chain string.
The gamer reads only turns.jsonl. It uses zero
experience and builds zero causal structure.

## 5. Reference experimenter (c9exp)

A simple experiment-driven causal learner. Reads only
turns.jsonl. Single pass per world: accumulates do_out
agreement counts keyed by the pending do(var,val), and
on the question line runs the frozen two-stage protocol:

Stage 1: tX = fraction of do(X,v) turns with y==v;
tZ = fraction of do(Z,v) turns with y==v.
- tX >= HI and tZ >= HI: Y is the leaf. Stage 2a.
- tX < HI and tZ < HI: Y is the root. Stage 2b.
- else: split. tX > tZ infers X->Y->Z; tZ > tX infers
  Z->Y->X; exact tie replies UNKNOWN.

Stage 2a (Y leaf; true chain is X->Z->Y or Z->X->Y):
sXZ = fraction of do(X,v) turns with z==v;
sZX = fraction of do(Z,v) turns with x==v.
sXZ > sZX infers X->Z->Y, else Z->X->Y
(tie replies UNKNOWN).

Stage 2b (Y root; true chain is Y->X->Z or Y->Z->X):
same sXZ, sZX. sXZ > sZX infers Y->X->Z, else Y->Z->X
(tie replies UNKNOWN).

The reply per question is the inferred full chain
string (e.g. "X->Y->Z"), built from the inferred
(root,middle,leaf) indices. The experimenter never
opens key.txt, worlds.txt, or manifest.txt; it parses
only the turn stream. It performs no threshold tuning:
HI=0.75 is frozen here, and all comparisons use fixed
integer arithmetic.

Statistical design note (why 24/24 is expected, not a
guarantee): with p=0.05 and KDO=60, a tracking pair
agrees with probability 0.95 per turn and a
non-tracking pair with probability 0.5. Binomial tail
bounds: P(binomial(60,0.95) < 45) < 1e-8;
P(binomial(60,0.5) >= 45) < 6e-5;
P(binomial(60,0.905) < 45) < 3e-5. The dominant
per-item misclassification risk is a 0.5-mean fraction
crossing HI (about 6e-5) or a 0.905-mean fraction
falling below HI (about 3e-5), each of which can flip
the stage-1 branch. Union bound over the few
comparisons per item gives per-item error below 2e-4;
over 24 items the expected number of errors is below
0.005. The realized 24/24 run is the kill bar (G2).

## 6. Scorer (c9score)

Reads key.txt and a replies file (one reply per line,
aligned to question order), prints "SCORE a/b" plus
per-item mismatch lines. Pure Zag, deterministic.

## 7. Kill bars (frozen; never move after this commit)

G1 (format gamer scores 0): c9gamer mode old scores
0/24 on the dev battery.
G2 (reference experimenter): c9exp scores 24/24 on the
dev battery (strictly greater than 0, satisfying the
"cAN score >0" requirement with a genuine
experiment-driven learner).
G3 (determinism): 3/3 runs of c9gen with SEED_DEV
produce byte-identical turns.jsonl, key.txt,
worlds.txt, and manifest.txt (sha256 equal across the
three runs).
G4 (genericity): no per-item hand authoring. Audit:
grep of c9gen.zag for full chain-string literals
("X->Y->Z", "X->Z->Y", "Y->X->Z", "Y->Z->X",
"Z->X->Y", "Z->Y->X") returns zero hits; the true
chain, the alternative, the candidate order, all
observation bits, and all do() outcomes are drawn from
the seeded RNG stream. The single-variable names X, Y,
Z and the "->" joiner are format scaffolding, not
answers.
G5 (pure Zag): `which python3` prints nothing at lane
start (recorded in NAMECHECK.md Step 0) and at lane
end; zero non-safebin executable invocations in this
lane. Any forbidden invocation is PROCESS-FAIL and
voids the verdict.
G6 (candidate-order randomization): c9gamer mode first
scores strictly less than 24/24 AND c9gamer mode
second scores strictly less than 24/24, i.e. no fixed
positional rule recovers the key; the true chain is
not always listed first or always listed second.
G7 (honest UNKNOWN scores 0): an all-"UNKNOWN" replies
file scores 0/24 with c9score.
G8 (scope honesty): the validation report and
JUDGE_BRIEF.md state explicitly that C9GEN is a
candidate instrument, not a replacement for the frozen
arena battery; no L3, substrate, or score claim is
made; adoption is a future governance decision.

GEN-PASS requires G1 through G8 all PASS. Any bar
failing yields GEN-FAIL with the killing evidence
named. Kill bars never move after freezing; a broken
prereg is amended transparently and re-frozen, never
salvaged.

## 8. Evaluation protocol (frozen)

8.1 Build c9gen, c9gamer, c9exp, c9score from the
committed lane sources with the pinned znc; record
binary sha256 values.
8.2 Run c9gen SEED_DEV into dev/, dev2/, dev3/ (three
runs); sha256sum the four output files in each dir;
G3 passes iff all three runs agree byte for byte.
8.3 Run c9gamer (modes old, first, second) on
dev/turns.jsonl; score each replies file against
dev/key.txt with c9score. G1: old = 0/24. G6: first
< 24/24 and second < 24/24.
8.4 Run c9exp on dev/turns.jsonl; score against
dev/key.txt. G2: 24/24.
8.5 Score an all-"UNKNOWN" replies file (24 lines)
against dev/key.txt. G7: 0/24.
8.6 Audits: grep for chain-string literals in
c9gen.zag (G4); `which python3` at lane end (G5);
byte scan for em-dash in lane docs with
check_no_dash.sh before every doc commit.
8.7 Write DEV_VALIDATION.md with the numbers, binary
hashes, file hashes, and the per-bar verdicts; write
JUDGE_BRIEF.md with the provenance header.

## 9. Scope reminders (frozen)

C9GEN tests whether a corrected instrument CAN exist
with the properties the frozen battery lacks; it does
not certify any learner as causal in general, and a
24/24 by the reference experimenter is evidence about
the instrument (it admits a genuine experiment-driven
solution), not evidence that any TNN subsystem is L3.
The experimenter is deliberately simple on purpose:
it is a calibration tool for the battery, not a
cognitive claim.

FROZEN 2026-10-01 PDT. Lane: wave-20261001-2321pdt/C9BAT.
