# REDTEAM_SELF: H5R2-SYNTH red team (pre-registered attacks, scored)

Lane: HPI, wave-20261002-0221pdt. The prereg froze three
self-attacks (section 9). Each is scored against the sealed evidence
below. The standing question: is the gate a genuine discriminator or
does it relabel ties?

## Attack 1 (relabeling ties): STANDS

The attack: on every tied-provenance conflict the only
protocol-grounded correctness criterion (the update-reading on
same-key revisions) forces H and N to diverge rather than tie; where
they tie, no criterion crowns S's answer; S would relabel ties, not
resolve them.

Evidence: on the 8 DT probes H and N tie at 8/8 DT-FIRST with
byte-identical full stdout (n_t1 == h_t1, n_t2 == h_t2). S scores 0/8
on the favored answer (8/8 DT-LATER), contradicting the frozen F2
semantics that the DT family extends. S does not resolve the tie; it
picks the other side of it. The DT bar (0 > 8) fails. The attack
stands unrefuted.

## Attack 2 (newest-bias): CONFIRMED

The attack: the decoy family was designed so that the newest live
fact is the wrong anchor; any newest-flavored rule must fail it.
Passing the separator while failing the decoy shows S is a bias, not
a better provenance policy.

Evidence: S scores 8/8 SEP-NEW on the separator (agreeing with N),
then 0/8 "D ok" with 8/8 D-DECOY-FAIL on the decoy family and 0/8
"CD ok" with 8/8 CD-DECOY-FAIL on the chained family. The bias
agrees with the update-reading on re-teach keys and disagrees
everywhere else, exactly as the attack predicted. The decoy worlds
are not adversarial-by-brokenness (8/8 D-ANS ok on both families, all
decoy facts answerable). The attack is confirmed.

## Attack 3 (F2 regression): CONFIRMED

The attack: the built-in battery's F2 test freezes
composition-preserving (first-taught) order for masked
disambiguation; S breaks it; a gate that regresses the frozen
battery cannot be called strictly stronger.

Evidence: S scores 45/46, failing exactly t_f2. The attack is
confirmed.

## The genuine-discriminator question: answered

Is the gate a genuine discriminator or does it relabel ties? The
sealed evidence says both worse things: it relabels ties (DT: 0/8
vs the 8/8 H/N tie) AND it introduces newest-bias regressions on
families the existing gates already pass (decoy, chained, battery
F2). The 2321pdt open question is answered negatively: no pure
tie-breaking rule along the newest axis can strictly dominate both
existing gates, because the decoy family already falsifies the
newest axis itself. The decoy family discriminates "newest-live"
from "provenance-correct" against any newest-flavored rule, not just
against the recency heuristic it was built for.

## What the experiment does not show (scope discipline, Q5)

- It does not re-litigate H5R2's BUILD-PASS, which stands within its
  frozen battery scope.
- It does not crown any of the three tie-breaking rules as the
  correct provenance policy in general. The verdict reports only
  which rule won on the tested families.
- The re-teach separator family remains an explicit open gap in
  H5R2's scope, not a retroactive bar. S agreeing with N on the
  separator (8/8 SEP-NEW) does not promote S: agreement on one
  family is not strict dominance, and S fails three other families.
- Oldest-first and newest-first are both enumeration artifacts of
  the same node-id order read in opposite directions. The experiment
  discriminates tie-breaking policies without crowning one (the
  2321pdt honest caveat, carried).

## Recommended next

The named synthesis hypothesis (newest-live among all live) is
killed by its own kill bars. Per the standing rule against
repairing along one axis, the next hypothesis in this lineage
should not be another tie-breaking rule (maximin-oldest,
score-weighted, per-site variants); those are the same axis. The
informative next step is a structurally different discriminator on
tied-provenance conflicts, or an explicit statement that the
tied-provenance conflict class has no protocol-grounded resolution
and the research effort moves to families where correctness is
grounded (revisions, contradictions, decoys). Queued for the
parent: H5R2-SYNTH2 direction decision.
