# PREREG: C9 world-generator D5 fix (C9D5FIX, wave-20261002-0521pdt, ARENA lane)

Status: FROZEN PREREG. Committed alone before any D5-fixed generator
source, binary, world, check tool, or validation run in this lane.
Any change to the design below requires a dated amendment committed
alone before the changed code runs. Commit-order rule: this file's
commit must strictly precede every implementation commit in this
lane. Kill bars never move after this commit.

## 1. Objective and the defect being fixed

The 0221pdt C9FIX validation (C9GEN_FIX.md) reported G4 PARTIAL: the
true chain is listed first in all 3 C9 discrim questions in the
contestant-visible turns.jsonl. That report diagnosed the cause as
seed luck ("the frozen seed yields rng_bit=1,1,1"). Re-examination of
the validated fixrun1 artifacts shows that diagnosis is wrong and a
deeper defect, D5, is the actual cause:

- fixrun1/battery.json C9 questions: item25 `discrim|X->Z->Y|X->Y->Z`
  (true first), item26 `discrim|X->Z->Y|Y->X->Z` (true first),
  item27 `discrim|Y->Z->X|X->Z->Y` (alternative first).
  Per the frozen F4 mapping (heads(1) = true first), the actual
  seeded coin flip draws under the frozen seed are 1,1,0, not 1,1,1.
- fixrun1/turns.jsonl C9 questions: item25, item26, item27 ALL list
  the true chain first.
- Root cause in world_gen_c9fix.zag: the battery emission path
  (lines 534-543) honors the coin flip; the turn-replay emission path
  (lines 753-767, which builds the contestant-visible turns.jsonl
  from the itq replay arrays) rebuilds the question as
  `discrim|<true>|<alternative>` unconditionally, never drawing or
  consulting the flip. The replay path therefore ignores F4.

D5: turns.jsonl C9 candidate order ignores the seeded coin flip;
battery.json and turns.jsonl disagree on item27 (and would disagree
whenever a tails is drawn). The generator's own comment at the
replay section ("replay (cap,q) per item for turn emission;
scorer cross-checks turns against battery.json; any divergence
aborts") states the violated intent.

The fix (this prereg): make the turn-replay path honor the same
per-item coin flip as the battery path, via a stored flip array.
The frozen seed 71503461337030 is UNCHANGED: with D5 fixed, the
frozen seed's actual draws (1,1,0) satisfy the G4 order criterion
(true_listed_first = 2/3). No seed reselection is needed or performed;
selecting a new seed to satisfy G4 would have been seed-shopping
against a misdiagnosed cause.

This remains an instrument fix, not a learner claim. The fixed
generator is a candidate instrument; the frozen competitive_arena/
tree is never modified; no L3, substrate, or canonical-score claim
is made; adoption is a future governance decision.

## 2. Frozen design (world_gen_c9d5fix.zag)

Base: byte-identical copy of the 0221pdt world_gen_c9fix.zag
(sha256 edc7215213fff34f72a81350160d0f283d96e3305c1b177f308de14f38abb502,
tracked in docs/lab/rsi/runs/wave-20261002-0221pdt/ARENA/).
Exactly three surgical edits, all confined to the C9 discrim
emission; the seed literal (line 277) is untouched:

E1 (store flips): after the `vn` declaration in the C9 battery
section, add `let dflip:[]u8=z_alloc(3);` holding one byte per C9
item: 1 = true chain listed first, 0 = alternative listed first.

E2 (record flip): in the battery emission C9 loop, immediately after
`let flip:i32=rng_bit(rng);`, add `dflip[altc]=flip as u8;`.
(`altc` is 0,1,2 for the three emitted items at that point, and the
replay loop below visits the same three alternatives in the same
order, so the indices align.)

E3 (honor flip in replay): in the turn-replay C9 loop, replace the
fixed true-first question construction with flip-ordered
construction: if `dflip[altc]==1`, emit `discrim|<true>|<alt>`
(identical form to the battery path); else emit
`discrim|<alt>|<true>` (identical form to the battery path).
No new chain-string literals are introduced; the flip array holds
order bits only.

E4 (diff confinement): `diff` of world_gen_c9d5fix.zag against the
base shows changes only in the regions named in E1-E3. Verified and
recorded in the eval.

## 3. Expected behavior (frozen)

E1: 3/3 runs of world_gen_c9d5fix with the frozen seed produce
byte-identical battery.json, answer_key.json, idmap.json,
exposure.jsonl, exposure_tnn.jsonl, briefing files, and
turns.jsonl (sha256 equal across runs).
E2: the world has 68 items and 291 turns.
E3: the 3 C9 keys are full chain strings ("X->Z->Y" x3 under the
frozen seed); each key equals one of the two candidates in its
question.
E4: in turns.jsonl, the true chain is listed first in exactly 2 of
the 3 C9 questions (flips 1,1,0 under the frozen seed), and the
turns.jsonl C9 questions are string-identical to the battery.json
C9 questions (D5 consistency).
E5: the old format exploit (first candidate, first variable)
scores 0/3 on the fixed world.
E6: the honest interventional protocol (c9fix_check.zag rebuilt in
this lane from the 0221pdt committed source, reading only the turn
stream) recovers the true chain on all 3 items.

## 4. Kill bars (frozen; never move after this commit)

G1 (determinism): E1 holds; sha256 equal across 3 runs for all
output files.
G2 (defect D1 still fixed): no CHECK 1 exactness in the fixed
source; at least one observation in the generated world has a
variable disagreement (noise present).
G3 (defect D2 still fixed): turns.jsonl contains exactly 80
{"t":"do"} and 80 {"t":"do_out"} expo turns (40 per variable on X
then Z), each do_out immediately following its do turn, with the
intervened variable fixed to the do val in every pair.
G4 (defect D3 fixed and D5 fixed): the 3 C9 keys are full chain
strings (no single-variable keys); in turns.jsonl the true chain
is not always listed first (true_listed_first <= 2; expected
exactly 2 under the frozen seed); the turns.jsonl C9 questions are
string-identical to the battery.json C9 questions; the old exploit
scores 0/3 (E5).
G5 (honest recoverability): E6 holds; the check tool recovers 3/3
chains reading only the turn stream.
G6 (genericity): grep of world_gen_c9d5fix.zag for full
chain-string literals ("X->Y->Z", "X->Z->Y", "Y->X->Z",
"Y->Z->X", "Z->X->Y", "Z->Y->X") returns zero hits; the diff
against the base touches only E1-E3.
G7 (pure Zag): `which python3` prints nothing at lane start
(NAMECHECK.md Step 0) and at lane end; zero non-safebin
executable invocations in this lane. Any forbidden invocation is
PROCESS-FAIL and voids the verdict.
G8 (scope honesty): C9D5FIX_EVAL.md states explicitly that the
fixed generator is a candidate instrument, not a replacement for
the frozen arena battery; no L3, substrate, or canonical-score
claim is made; adoption is a future governance decision; the
frozen competitive_arena/ tree is unmodified (verified by
git status on that tree).

GEN-PASS requires G1 through G8 all PASS. Any bar failing yields
GEN-FAIL with the killing evidence named.

## 5. Evaluation protocol (frozen)

5.1 Copy the 0221pdt world_gen_c9fix.zag to this lane as
world_gen_c9d5fix.zag; verify sha256
edc7215213fff34f72a81350160d0f283d96e3305c1b177f308de14f38abb502
before editing; apply only E1-E3; record the diff.
5.2 Build world_gen_c9d5fix with the pinned znc; record binary
sha256. Build c9fix_check from the 0221pdt committed
c9fix_check.zag source in this lane; record binary sha256.
5.3 Generate fixrun2/ three times from a clean state; verify G1
(byte-identical sha256 across runs).
5.4 Validate G2-G6 against fixrun2 (source inspection, turn
counts, question string comparison battery vs turns, exploit
score, check-tool recovery).
5.5 Write C9D5FIX_EVAL.md with the GEN-PASS/GEN-FAIL verdict line,
the exact flip pattern observed, and the corrected diagnosis note
(actual draws 1,1,0; prior "1,1,1 seed luck" diagnosis falsified
by the battery.json evidence).

## 6. Notes

- Pure Zag only. The seed is unchanged, so this prereg performs no
  seed selection of any kind.
- The D5 correction is owed to the 0221pdt C9GEN_FIX.md diagnosis:
  its G4 PARTIAL verdict stands (the turns-visible order was
  degenerate), but the attributed cause is corrected here with
  artifact evidence.
- Part A (C9 causal contestant sealed eval) and Part C (abstention
  test) proceed on their already-frozen preregs; the D5-fixed world
  (fixrun2) is available as a supplementary eval substrate but the
  frozen verdicts run on their preregistered substrates.
