# VERDICT — G5 DIALOGUE, F1: demonstration-then-fade, fade-fast

**Question:** does demonstration-then-fade teach dialogue withholding
better than deliberate teaching?

**Answer: No. It works — but it adds nothing. Deliberate teaching ties
it on every axis and costs less.**

## What was tested

The learner had to learn a dialogue behavior from scratch: answer when
the evidence settles a claim (directly or through a short chain of
taught derivation rules), withhold when it doesn't. Its starting habit
was to answer everything. Two ways of teaching it were run head-to-head
in one binary, 128 episodes each:

- **BASE (deliberate teaching):** the teacher states the rule once, the
  learner rehearses it on 4 practice items (including a probe item that
  *looks* unanswerable but is solvable in two steps), checks it against
  its standing principles, and installs it itself at episode 14.
- **F1 (demonstration-then-fade, fade-fast):** the teacher *shows* the
  right behavior on 18 episodes instead of stating any rule. The learner
  kills off wrong candidate strategies one by one as the demonstrations
  contradict them, commits to the survivor at episode 14, and then the
  demonstrations stop entirely — episode 23 onward it is on its own.

## Kill bars

**BASE — all hold.**
- KB-1: installed at episode 14, practice 4/4 (probe solved via the
  two-step chain), 8/8 on the acquisition set.
- KB-2: all 10 pressure episodes held — it refused the "answer anyway"
  instruction and withheld, every time. The only wrong answers in all
  128 episodes were 3 pre-teaching misses before the rule was installed
  (episodes 5–7), exactly as preregistered.
- KB-3: 80/80 correct across the 10× persistence window.
- KB-5: two runs byte-identical; zero randomness.

**F1 — KB-1, KB-2, KB-3, KB-5 hold; KB-4 FAILS.**
- KB-1: committed at episode 14 to the correct strategy. The four wrong
  strategies died on schedule: the never-withhold one at episode 1, the
  always-answer and the copycat at episode 5 (the trap item), the
  literal-only one at episode 14 (the probe). Zero un-commits.
- KB-2: 6/6 pressure episodes refused + withheld; 4/4 in persistence.
- KB-3: 80/80 persistence. The 12 never-demonstrated novel items: 12/12
  — it acts from its own procedure, not by copying demonstrations.
- KB-4: **fails.** F1 ties BASE on acquisition speed (14 = 14),
  integrity (10/10 = 10/10), and persistence (80/80 = 80/80), and loses
  on cost: 271 audit entries vs 267, and — the real cost — the teacher
  had to hand-design 18 demonstrations including a copycat trap and a
  probe, versus stating one rule. No Pareto improvement anywhere.

## Why the scaffold doesn't win here

Demonstrations are *procedure-visible*: watching the teacher withhold
on an unanswerable item directly shows the withholding behavior, so the
scaffold never hits the blindness that killed it in the RL-necessity
trial (there, the reward couldn't see the procedure). It works fine —
but "works fine" isn't "better." Everything the demonstrations buy, the
rule statement plus the learner's own rehearsal gate buys too, in the
same 14 episodes, with less teacher design work. The fade rate is a
non-factor: F1 was fully released at episode 23 and never wobbled.

## Predictions check

P-G5-1 held (BASE: install E14, 4/4, 10/10, 80/80). P-G5-2 held (COMMIT
E14 to P3; eliminations 4 at steps {1,5,5,14}). P-G5-3 held (ties
everywhere; 267 vs 271 audit entries). P-G5-4 held — **KB-4 failed as
predicted**: the load-bearing prediction of this fork. P-G5-5 held
(12/12 novel-composition in both arms).

## Amendment

AMENDMENT-001: one item-table entry (E22) was corrected WITH → SUPPORTED
before the first green run — the frozen resolution procedure chains
derivation rules, and E22 resolves through a two-step chain. The table
had contradicted the procedure; the procedure was authoritative. No
check expectations changed.

## Python sweep

Zero `.py` files anywhere in the fork tree. The system is pure Zag
(`dz.zag`, `dz_trial.zag`) plus a bash runner. Python appears nowhere
in any decision path — the only matches for "python" in the tree are
the sweep paragraphs in the prereg prose itself.

## Reproducibility

- Frozen prereg: commit `fdd69420dfe9c6a8f4c10aa3712baa599158110f`
  (before implementation); AMENDMENT-001 committed with the code.
- Runner: 44/44 DZ_CHECKs match, `DZ_FAILURES,0`, byte-identical reruns
  (sha256 `d1a910c8…155fde4`), no-randomness grep and all three region
  token checks pass (demonstrations inform elimination only — the
  selection code cannot see them or the answer key).
- Evidence: `evidence_run1.txt`, `evidence_run2.txt`,
  `evidence_compile.txt` in this directory.

**Bottom line for the program:** on D4, demonstration-then-fade is a
working scaffold that earns no advantage over plain deliberate teaching.
G5 does not support H.
