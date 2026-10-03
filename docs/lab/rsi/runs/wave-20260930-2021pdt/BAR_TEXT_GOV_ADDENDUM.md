# Governance addendum: adversary bar-text procedure (wave 20260930-2021pdt)

Standing rule adopted from the 11:21 recovery debate M1 (F3a3 ADOPTED
with caveat; JUDGE_1121_RECOVERY.md). It governs every future
adversary-authored bar text in the loop.

1. Fixture-collision pre-check. Before any adversary bar text is
   frozen, the author runs a collision pre-check on the declared
   fixtures (disjointness of declared sets, satisfiability of the
   bar text against the fixtures). The pre-check result is recorded
   with the freeze. A bar text frozen without a pre-check is not a
   frozen bar.

2. Author independence. Adversary families are authored by a party
   with no stake in the mechanism under test. The mechanism builder
   may not author the adversary family for its own candidate.

3. Exhausted declaration sets. Once a declared disjoint set is
   exhausted (the 11:21 set {k,m,r,v} is declared exhausted), the
   next round requires a fresh disjoint set. Reusing an exhausted
   set is a process violation and voids the round's verdict.

4. Corrections are textual only. After results, bar-text corrections
   may address disjointness or satisfiability only. Corrections that
   lower a threshold or narrow a behavioral demand are
   threshold-lowering and are forbidden; they void the verdict and
   require re-freeze and re-run.

Rationale (from the M1 debate): the F3a3 mechanism passed every
behavioral bar across three rounds, but the passing run faced the
third draft of the bar text. The caveat does not kill the verdict;
it fixes the procedure so future verdicts do not need one.

This addendum is governance documentation, not a mechanism change.
No kill bar is weakened by it.
