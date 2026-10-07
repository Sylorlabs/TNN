# Fast membership-order falsifier — preregistration

Base: fetched origin lane/ownership, 91b2acc29731135a143adf27c00400174550eaf1.
Private branch: fast/method-identifiability. No ownership worktree edits.
Inspected P6-struct PREREG and precond.zag, not REPORT.md.

## QUESTION
Does p6struct/precond.zag compute exact membership when a child has two
locally successful expansions, or does rule order change the accepted language?

## COMPETING HYPOTHESES
H-exact: membership existentially considers complete derivations; rule order
cannot change acceptance.
H-greedy: match returns the first child endpoint, cannot backtrack after a
parent suffix fails, and can reject valid strings depending on rule order.

## MINIMUM WORLD
A0 -> A1 4; A1 -> 3 | 3 4; A2 has no rules.
Both orders of A1 alternatives denote the same language.
Root A0 language is exactly {3 4, 3 4 4}.
Union over all nonterminals is exactly {3, 3 4, 3 4 4}.
All other strings over terminals 3..6, lengths 1..4, are invalid.

## CONTROLS
- Reuse the fetched matcher unchanged, including bounds and union wrapper.
- Exhaust all 340 terminal strings, not just positive cases.
- Independently hand-derived flat exact-sequence oracle, not matcher-generated labels.
- Swap alternative order without changing grammar content.
- Repeat with terminal bijection 3<->6, 4<->5; NT identities unchanged.
- Empty-table ablation should reject everything (not accept everything).
- Forward output must belong to the exact root language, but generation here
  returns one witness, not an exhaustive enumeration of the language.

## EXPECTED DISCRIMINATOR
H-exact: both orders, both terminal renamings: rooted accepts=2, union accepts=3,
zero false positives and false negatives over 340 queries.
H-greedy: short-first rooted accepts=1, union accepts=2; long-first rooted
accepts=1, union accepts=3. Root errors differ by order. No false positives.
Terminal renaming preserves these errors. Empty table accepts=0.

## RUN / ACCEPTANCE
Pure Zag for all scientific computation. Shell only assembles an unchanged
source prefix with a new driver and orchestrates fresh build/run/hash/diff.
Source pure-zag.sh, record environment and compiler SHA. Compile gates each run.
Three fresh builds; record binary SHA and require byte-identical raw stdout.
Driver exit 0 means experiment instrumentation and predicted greedy signature
verified, NOT that the matcher passed. Unexpected signature exits nonzero.
Exact artifacts in this directory: PREREG.md, driver.zag, probe.zag,
environment.txt, provenance.txt, compile1..3.txt, run1..3.txt, REPORT.md.
Generated executable probe is not canonical source and will not be committed.

## WHAT IT KILLS / DOES NOT KILL
If H-greedy: kills exact-membership claims for this implementation on grammars
with overlapping alternatives; does not kill production representations,
all parsers, the original single-alternative fixture, or structural learning.
This is a harness audit, not a test of an implemented TNN learner or L3.

## NEXT QUESTION
Before induction: can a corrected matcher represent all child endpoints and
remain correct under rule-order permutations, renaming, recursion, and bounds?
