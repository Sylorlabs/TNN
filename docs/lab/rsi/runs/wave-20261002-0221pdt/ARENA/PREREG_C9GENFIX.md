# PREREG: C9 world-generator fix (C9FIX, wave-20261002-0221pdt, ARENA lane part B)

Status: FROZEN PREREG. Committed alone before any fixed-generator
source, binary, world, check tool, or validation run in this lane.
Any change to the design below requires a dated amendment committed
alone before the changed code runs. Commit-order rule: this file's
commit must strictly precede every implementation commit in this
lane. Kill bars never move after this commit.

## 1. Objective and the defect being fixed

The frozen arena C9 battery is broken by design (ARENA2 negative
finding, wave-20261001-2321pdt, confirmed in this lane's
NAMECHECK.md Step 1):
- D1: world_gen.zag CHECK 1 enforces x==y==z in all 12 causal
  observations. The chain permutation is observationally
  unidentifiable by construction.
- D2: the battery contains zero intervention turns. The original
  C9 protocol (choose a discriminating intervention, observe,
  eliminate) was never implemented.
- D3: discrim items always list the true chain first
  (world_gen.zag lines 487-517 emission loop), and the answer key
  is chain[0] (a single variable). The only 3/3 mechanism is
  "parse the first candidate, emit its first variable": zero
  experience, zero causal structure, a benchmark-format exploit
  rejected under the no-gaming rule. The honest causal answer
  (UNKNOWN, direction unidentifiable) scores 0.

The fix (queued line: "randomize candidate order; add real
intervention turns; C9 stays a sealed zero until the fix lands"):
a corrected world generator world_gen_c9fix.zag living in this
lane directory. It does NOT modify the frozen
competitive_arena/world_gen.zag (that tree stays byte-identical;
verified by git status in the validation). Whether any future
wave adopts the fixed generator is a governance decision outside
this lane. No L3 claim, no TNN-beats-LLM claim, no
canonical-score claim is made here. This is an instrument fix,
not a learner claim.

## 2. Frozen design (world_gen_c9fix.zag)

Base: a byte-identical copy of the frozen world_gen.zag
(sha256 c4c8340c818e6848c88e34f1989bf382ff097c69a71d6621c6bf28b58dc85211
per the refreeze record), with surgical edits confined to the
causal subsystem plus the two RNG helpers below. The seed stays
71503461337030 (line 265 unchanged). All draws come from the
single seeded LCG stream in fixed order; the generator is a pure
function of the seed.

RNG helpers added (method from the committed C9BAT c9gen.zag,
which fixed the arena LCG bit-0 degeneracy):
- rng_bit(rng): returns bit 33 of rng_next (0/1, no parity degeneracy).
- rng_flip(rng): returns 1 iff rng_range(rng,2000) < 100 (edge flip
  p = 0.05 with better bit quality than a %2 draw).

Causal edits:
F1 (chain draw): the Fisher-Yates shuffle (lines 365-368) is
replaced by a uniform permutation index pi0 = rng_range(rng,6000)/1000
into the 6-slot permutation table (the same table the C9 items
section already defines; it is moved earlier and reused). All 6
permutations of (X,Y,Z) are reachable; none hand-picked. This is
the C9BAT amendment-A1 method, which fixed Fisher-Yates reaching
only 3 of 6 permutations.

F2 (observations): the 12 observations are drawn by ancestral
sampling in chain order: root bit from rng_bit; each downstream
node copies its parent bit and flips iff rng_flip returns 1.
obs[i*3+v] holds variable v in {0:X,1:Y,2:Z} order. CHECK 1 (exact
co-movement enforcement, lines 376-382) is REMOVED. Nothing
enforces x==y==z; the observation distribution carries genuine
correlational structure (adjacent chain pairs agree w.p. 0.95,
endpoint pairs w.p. 0.9025), identifying the chain up to reversal.
The noise rate p=0.05 is a generator parameter, NOT disclosed in
any contestant-visible briefing.

F3 (intervention turns): KDO = 40 do() turns on X, then KDO = 40
do() turns on Z (frozen count). Values alternate 1,0,1,0,....
Each do() turn is immediately followed by its outcome turn.
Turn formats (mirroring the existing causal obs emission into
all three artifacts):
- turns.jsonl / exposure.jsonl:
  {"t":"do","var":"X","val":1}
  {"t":"do_out","x":1,"y":1,"z":0}
- exposure_tnn.jsonl:
  {"t":"do","seq":[varidx,val]} with varidx 0 for X, 2 for Z
  {"t":"do_out","seq":[x,y,z]}
Outcome computation: intervened ancestral sampling in chain
order root, middle, leaf. The intervened node is fixed to val; a
non-intervened root draws rng_bit; a non-intervened downstream
node copies its (possibly intervened) parent and flips iff
rng_flip returns 1. The do() outcomes discriminate chain
direction: do(root) moves all descendants; do(leaf) moves
nothing; do(middle) moves only its downstream side. KDO=40 is
frozen; the statistical basis is in section 5.

F4 (discrim items): 3 items, one per alternative (the first 3
permutations of the table that differ from the true chain,
deterministic given the RNG-drawn chain; no hand-picking).
Per item, a seeded coin flip (rng_bit) decides candidate order:
heads the true chain is listed first, tails the alternative is
listed first. Question format unchanged in shape:
"discrim|<c1>|<c2>" where each candidate is a full chain string
built programmatically from single variable names plus "->".
The answer key for each C9 item is the FULL true chain string
(e.g. "X->Y->Z"), not chain[0]. This kills the old exploit:
"parse the first candidate, emit its first variable" can no
longer match any key.

F5 (proofs and briefing): proofs.json replaces the
"causal_exactness: 12/12 observations satisfy X==Y==Z" line with
"causal_noise: 12 observations via ancestral sampling, per-edge
flip p=0.05; exact co-movement NOT enforced (C9FIX removes
CHECK 1)." The "likelihood gap = 0 nats" line is replaced with
"consequence: chain direction identifiable from the do/do_out
intervention turns; observations alone identify the chain up to
reversal." A "c9fix:" line records the candidate-order
randomization, the full-chain keys, and the KDO=40 count. The
natural-language briefing sentence "You will observe facts,
relations, Zem words, and causal observations across turns."
gains "and causal interventions (do/do_out pairs)". No other
briefing content changes. The noise rate is not disclosed to
the contestant anywhere.

F6 (untouched): all non-causal subsystems (entities, Zem, C1-C8,
C10-C16 items, test-block layout, 68-item count, turn kinds
outside the causal block) are byte-identical in logic to the
frozen source; only the RNG stream position differs downstream
of the causal draws, so names and words differ, which is
expected for a corrected world family.

## 3. Expected behavior (frozen)

E1: 3/3 runs of world_gen_c9fix with the frozen seed produce
byte-identical battery.json, answer_key.json, idmap.json,
exposure.jsonl, exposure_tnn.jsonl, briefing files, and
turns.jsonl (sha256 equal across runs).
E2: the world has 68 items and 291 turns (131 + 160 new
intervention turns).
E3: the 3 C9 keys are full chain strings; each is one of the
two candidates in its question; the true chain is listed
first in a coin-flip-randomized subset of the 3 items (not
always first).
E4: the old format exploit (first candidate, first variable)
scores 0/3 on the fixed world.
E5: an honest interventional protocol (the C9BAT two-stage
protocol with HI=0.75, reading only turns.jsonl; implemented
in the check tool c9fix_check.zag, which may read key.txt
SOLELY to compare) recovers the true chain on all 3 items.
This is instrument calibration (the world admits a genuine
experiment-driven solution), not a learner claim. The
contestant mechanism in part A reimplements the protocol
independently and never opens the key; part A's prereg will
disclose this validation.

## 4. Kill bars (frozen; never move after this commit)

G1 (determinism): E1 holds; sha256 equal across 3 runs for
all output files.
G2 (defect D1 fixed): no CHECK 1 exactness in the fixed
source (grep "CAUSAL EXACTNESS" returns zero hits); the
12 observations are drawn by the noisy ancestral sampler
(source inspection); at least one observation in the
generated world has a variable disagreement (noise present).
G3 (defect D2 fixed): the generated turns.jsonl contains
exactly 80 {"t":"do"} and 80 {"t":"do_out"} expo turns
(40 per variable on X then Z), each do_out immediately
following its do turn, with the intervened variable fixed
to the do val in every pair (verified by the check tool).
G4 (defect D3 fixed): the 3 C9 keys are full chain strings
(no single-variable keys); the true chain is not always
listed first across the 3 items (coin flip honored); the
old exploit scores 0/3 (E4).
G5 (honest recoverability): E5 holds; the check tool
recovers 3/3 chains reading only the turn stream.
G6 (genericity): no per-item hand authoring. Audit: grep of
world_gen_c9fix.zag for full chain-string literals
("X->Y->Z", "X->Z->Y", "Y->X->Z", "Y->Z->X", "Z->X->Y",
"Z->Y->X") returns zero hits; the true chain, the
alternatives, the candidate order, all observation bits,
and all do() outcomes are drawn from the seeded RNG
stream. Single variable names X, Y, Z and the "->" joiner
are format scaffolding, not answers. The diff of the
fixed source against the frozen source touches only the
causal subsystem, the two RNG helpers, and the
proof/briefing lines named in F5.
G7 (pure Zag): `which python3` prints nothing at lane start
(NAMECHECK.md Step 0) and at lane end; zero non-safebin
executable invocations in this lane. Any forbidden
invocation is PROCESS-FAIL and voids the verdict.
G8 (scope honesty): C9GEN_FIX.md states explicitly that the
fixed generator is a candidate instrument, not a
replacement for the frozen arena battery; no L3,
substrate, or canonical-score claim is made; adoption is a
future governance decision; the frozen
competitive_arena/ tree is unmodified.

GEN-PASS requires G1 through G8 all PASS. Any bar failing
yields GEN-FAIL with the killing evidence named.

## 5. Statistical basis for KDO=40 (frozen)

Two-stage protocol (C9BAT section 5), HI=0.75 (need >= 30/40
agreements). Binomial tail bounds: P(Bin(40,0.95) <= 29) < 1e-9
(tracking pair crossing below HI); P(Bin(40,0.5) >= 30) < 1.5e-3
(non-tracking pair crossing above HI); stage-2 comparison
P(s_wrong >= s_right) < 1e-5 (0.9025-mean vs 0.5-mean gap,
sd ~0.092). Dominant per-item misclassification risk is a
0.5-mean fraction crossing HI (~1.3e-3); union over the few
comparisons per item gives per-item error below 2e-3; over 3
items the expected number of errors is below 0.006. The
realized 3/3 run is the kill bar (G5). This is a design
calculation, not a guarantee; a failure is honest evidence.

## 6. Evaluation protocol (frozen)

6.1 Copy the frozen world_gen.zag to this lane as
world_gen_c9fix.zag (byte-identical copy verified by hash
before editing); apply only the F1-F6 edits; record the
diff stat.
6.2 Build world_gen_c9fix with the pinned znc; record binary
sha256. Build the check tool c9fix_check.zag (pure Zag:
parses turns.jsonl, runs the two-stage protocol per the
3 C9 questions, prints inferred chains; compares against
key.txt only for the validation report; also verifies
G2/G3/G4 counts).
6.3 Run the fixed generator 3x into fixrun1/2/3; sha256sum
all output files; G1 passes iff all three agree byte for byte.
6.4 Run the old exploit (parse first candidate, emit its
first variable) on the fixed turns; score against the fixed
key with a pure-Zag scorer (or the rebuilt frozen arena
scorer on the fixed world); G4 requires 0/3.
6.5 Run c9fix_check on fixrun1; G5 requires 3/3 recovered.
6.6 Audits: grep for chain-string literals in
world_gen_c9fix.zag (G6); grep "CAUSAL EXACTNESS" (G2);
`which python3` at lane end (G7); git status on
competitive_arena/ (G8); byte scan for em-dash in lane docs
with check_no_dash.sh before each commit.
6.7 Write C9GEN_FIX.md with the numbers, binary hashes, file
hashes, diff stat, and per-bar verdicts.

## 7. Scope reminders (frozen)

The fixed generator tests whether a corrected instrument CAN
exist with the properties the frozen battery lacks; it does
not certify any learner as causal in general, and a 3/3 by
the check tool is evidence about the instrument (it admits a
genuine experiment-driven solution), not evidence that any
TNN subsystem is L3. The check tool is deliberately simple on
purpose: a calibration tool for the battery, not a cognitive
claim. The frozen arena battery is untouched; its C9 stays a
sealed zero. C9GEN (the 24-world candidate from C9BAT) is a
separate instrument and is not modified here.

FROZEN 2026-10-02 PDT. Lane: wave-20261002-0221pdt/ARENA, part B.
