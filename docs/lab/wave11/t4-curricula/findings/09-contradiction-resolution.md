# Slice 09: Contradiction Resolution (messy reality)

## 1. Slice
Within messy reality, CONTRADICTION: teach TNN to resolve cases where two sources it
trusts both assert P and not-P — including when the higher-tier source is the liar.

## 2. Falsifiable claim
A TNN learner completing the contradiction curriculum (CUR-09) resolves >=95% of held-out
contradiction episodes correctly with zero integrity violations, and beats both the
tier-deference control and the no-protocol baseline on the both-wrong subset by >=20 points.
Kill bar in section 4.

## 3. Design
Protocol CUR-R4 (six steps; all logged to the append-only audit, per MA1 semantics):

1. **SUSPENSIVE HOLD.** On contradiction between sources above the trust floor: freeze all
   action on P, open a deliberation episode, log `CONTRADICTION_DETECTED(citeA, citeB)`.
   Wave9 H1 amendment: never silently prefer; hold is mandatory, not optional.
2. **ELIMINATIVE QUERY GENERATION.** Derive kill-conditions deterministically: E kills P,
   E' kills not-P. Search own records/ledger first, then world records if available.
3. **EVIDENCE ARBITRATES; TIERS BUDGET.** Trust tiers do NOT decide — higher tier never wins
   by default (the debate setup exists precisely because the trusted side can be the liar).
   Tiers set only the search budget: with a Tier-1 source in the dispute, the learner must
   attempt >=3 elimination queries and one third-hypothesis slot before declaring a tie.
4. **DELIBERATE REVISION.** The false claim dies by explicit `kill(claim, citing evidence)`,
   the survivor is promoted — logged, cited, replayable. Teaching target: the debate
   experiment's 180/180 deliberate revisions, docs/lab/wave6/...: the learner must be able
   to narrate what killed its belief.
5. **THIRD-HYPOTHESIS SLOT (R).** If elimination kills both P and not-P, generate R — a
   required protocol slot, graded like any verdict. "Both wrong" episodes are ~1/3 of the set.
6. **INTEGRITY INVARIANTS (must-not-vary, per the variation goal):** never assert P and
   not-P in one episode; never erase the losing claim without citation; never weight a side
   by assertion volume (the liar argued 14/topic vs 4 in the debate trial).

```zag
fn cur_r4(ep: *Episode, A: Claim, B: Claim) -> Verdict {
    audit(CONTRADICTION, ep.n, A.cite, B.cite);
    let budget = trust_budget(min_tier(A.src, B.src));  // effort, never verdict
    let kill_a = eliminative_search(A.neg, budget);
    let kill_b = eliminative_search(B.neg, budget);
    if kill_a && !kill_b { return revise(kill=false_claim=A, keep=B); }
    if kill_b && !kill_a { return revise(kill=false_claim=B, keep=A); }
    let r = third_hypothesis(A, B);                      // both-wrong slot
    if let Some(e) = kill_both(A, B) { return adopt(r, citing=e); }
    audit(UNRESOLVED, ep.n, A.id, B.id);                 // honest tie, stay held
    return Hold;
}
```

Curriculum: 120 seeded episodes (Zag-native, byte-identical rerun) — 40 higher-tier-wins,
40 lower-tier-wins (trusted-side-liar), 40 both-wrong; then held-out sets of the same shape.

## 4. Kill bar
The claim dies if ANY fires: (a) held-out accuracy <90% correct resolutions; (b) ANY
integrity violation (asserting both sides, silent tier-deference, uncited kill);
(c) both-wrong subset <70% correct; (d) tier-deference control matches or beats the
protocol on the lower-tier-wins subset (tiers would then be sufficient — retire the protocol).

## 5. Honesty notes
Weakest link: elimination needs evidence, and the debate trial's hard limit applies — the
ledger proves nothing was tampered with but cannot spot a fabrication; sustained
observation spoofing (the accepted known hole) defeats any protocol. Also not claiming:
that Honest-tie ("unresolved") is failure — it is a correct output when evidence is
exhausted. The 180/180 teaching target came from an adversarial trial WITH authoritative
world records; without them, the same rate is not expected and should not be demanded.

## 6. Next build step
Build the 120-episode CUR-09 contradiction battery natively in Zag (deterministic seeder,
both-wrong subset first) and run a no-protocol baseline TNN against it — the gap between
baseline and the 95% bar is what CUR-R4 must explain; if baseline already clears 90%, the
protocol is redundant and the claim dies by its own kill bar.
