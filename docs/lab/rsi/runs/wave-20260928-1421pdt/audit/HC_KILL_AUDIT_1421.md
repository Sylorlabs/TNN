# Governance audit: H-C kill at the salt commit (wave-20260928-1421pdt)

Audit item carried from the 2026-09-28 repo inspection (standing memory):
possible H-C kill governance violation. The K-HC4 bar may have been
redefined post-hoc at the salt commit.

Scope: read-only git archaeology on Micah's own commits. Nothing of his
was edited, built, run, or re-presented. This audit judges the
governance record only.

## Timeline

- `a95e0d50c` (2026-09-27 18:03 -0700, micahcooley): "H-C trace
  anti-unification (hypo_c): pure-Zag implementation + evidence".
  Implements H-C; hypo_c/BUILD.md freezes the K-HC verdict table.
- `57d055bbb` (2026-09-27 19:24 -0700, micahcooley): "combiner_arch salt
  testing: H-A killed (K-HA-8), H-C killed (K-HC-4), H-B survives".
  Add-only commit: docs/lab/composition/combiner_arch/testing/ with
  TESTING.md applying the kill bars to the salt battery results.

## The K-HC4 bar as frozen (a95e0d50c, BUILD.md section 6)

- K-HC4 (learn the D1 six): PASS (with D1, D2).
- The D1 six: reverse, dupfirst, rotleft, droplast, upperfirst, sortchars.
  The bar was marked PASS with the implementer's documented deviations D1
  (R-equivalence as global byte-map indistinguishability) and D2
  (F-equivalence skipping out-of-bounds lengths).
- The same BUILD.md (section 5) records swap-first-last (r7) as a
  "genuine grammar limitation" of the committed implementation: fixed
  START/END roles cannot express length-relative "middle" uniformly.

## The K-HC4 bar as applied (57d055bbb, TESTING.md)

- TESTING.md line 138: the P3 4/8 result (4 swap-first-last probes
  withhold W5; 4 sort-descending correct) is called "the known
  frozen-spec conflict: the committed H-C withholds W5 on
  swap-first-last, contradicting K-HC4's 'minimum capability includes
  swap-first-last.'"
- TESTING.md kill bars: "K-HC4 FIRES. Minimum capability includes
  swap-first-last; H-C withholds it (0/8 on swapfl probes, W5)."
- Verdict: H-C is KILLED by K-HC4.
- TESTING.md also applies K-HC5 ("sequential chaining must be 100% on
  learnable links"), K-HC6 ("clean-trained score cannot drop on any salt
  family"), and K-HC7 (nondeterminism). K-HC5 counted as a miss but not a
  wrong-emission kill; K-HC6/K-HC7 did not fire.

## Evidence trail (git pickaxe, scoped to docs/lab/composition/combiner_arch/)

- The phrase "minimum capability includes" first appears in the tree at
  `57d055bbb` (the salt commit itself). `git log --all -S "minimum
  capability includes"` returns only 57d055bbb.
- "K-HC5" first appears in the tree at `57d055bbb`. No prior freeze
  commit for K-HC5, K-HC6, or K-HC7 exists in the combiner_arch record.
- "K-HC4" appears in combiner_arch only at `a95e0d50c` and `57d055bbb`.
- The cited source document "H-C HYPOTHESIS.md" (TESTING.md cites its
  section 5 for the clean-teaching protocol) is absent from the tree:
  `git ls-tree -r --name-only 57d055bbb -- docs/lab/composition/` returns
  zero files matching "hypothesis". The implementation commit's message
  references "hyp/hypo_c/HYPOTHESIS.md", which is likewise not in the tree.

## Finding

On the committed record, the K-HC4 applied at the salt commit is not the
K-HC4 frozen 81 minutes earlier. The frozen bar was "learn the D1 six"
(PASS with D1/D2 deviations); the applied bar is "minimum capability
includes swap-first-last" (FIRES, kills H-C), with the defining phrase
first appearing in the salt commit itself. Three further kill bars
(K-HC5, K-HC6, K-HC7) were applied with no freeze commit in the record.
The one caveat: the referenced HYPOTHESIS.md is missing from the tree,
so the audit cannot exclude that the swap-first-last clause existed in a
document that was never committed. On evidence in the tree, the change
is confirmed.

## Governance consequence

A kill bar redefined after freezing cannot ground a clean frozen-bar
kill. Under loop governance the H-C kill as recorded at 57d055bbb is
UNVERIFIABLE as a frozen-bar kill: the bar that fired was not the bar
that was frozen. The recommendation is: strike the kill as a governance
verdict, or re-run H-C under the original frozen bar (K-HC4 = "learn the
D1 six" with the recorded D1/D2 deviations, which passed). This is
Micah's own frontier experiment; the loop records the finding and banks
the recommendation, it does not decide his verdict. The audit does not
weaken any bar; it documents the change and moves on.

Status: finding CONFIRMED-ON-RECORD, recommendation banked to Micah.
Not adopted as a loop decision; no verdict of his is altered by this wave.
