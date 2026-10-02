# ACT Bid Directionality: Analysis and Recommendation

**Verdict: ACT-BID-ANALYZED.** Recommend option (a): align ACT `bid()`
to directional (incoming-only) counting, matching CLA-2 `evcount()`.

## The divergence (confirmed)

ACT `bid()` (act.zag lines 125-137):
```
if(f==a){ hit=1; }   // outgoing: node is SOURCE
if(t==a){ hit=1; }   // incoming: node is TARGET
```
Counts edges in both directions.

CLA-2 `evcount()` (cla2.zag lines 340-352):
```
if(eg(W,e,8)==n){    // field 8 is target: incoming only
```
Counts incoming edges only.

Integration spec A3 (INCOMPAT-3): "The core already computes
bid(node) for eviction; ACT reuses the same function." This is
currently false.

## Semantic analysis

The bid is defined (A11) as a signed count over evidence edge
types: SUPPORTS/CONFIRMS/USE +1, CONTRADICTS -1. The word
"evidence" carries the semantics: the bid measures evidence
FOR the node.

An outgoing SUPPORTS edge from guide G to outcome O means "G
asserts that action A supports outcome O." This is G's CLAIM
about the world. It is G's content, not evidence for G.

Evidence FOR G would be:
- S -> G via SUPPORTS: another structure supports G.
- OBS -> G via CONFIRMS: an observation confirms G worked.
- U -> G via USE: G was used successfully.
- X -> G via CONTRADICTS: evidence G is wrong.

Counting outgoing edges conflates a node's claims with its
credibility. A guide that makes ten predictions, all wrong,
would outbid a guide that makes one prediction, confirmed.
That inverts the meaning of "evidence bid."

## The consequence-edge concern

Prereg section 2(d) specifies that ACTION-GUIDE nodes link
SUPPORTS to outcome nodes ("taking this action supports
reaching that outcome"). Under bidirectional counting, these
consequence edges inflate the guide's own bid. Under
directional counting, they do not.

This is correct, not a loss. The consequence edges are the
guide's predictive content. Whether those predictions are
RIGHT is recorded directionally:
- Correct prediction -> incoming CONFIRMS from the observed
  outcome (bid +1).
- Wrong prediction -> incoming CONTRADICTS from the observed
  outcome (bid -1).

The guide's predictive success is fully captured by incoming
edges. We do not need to count the predictions themselves.
Counting predictions rewards verbosity, not accuracy.

## The informativeness objection (steelmanned)

One could argue: a guide with rich consequence structure is
more useful for planning than a "blind" guide, so outgoing
edges should count for SELECTION even if not for retention.

Response: this conflates two distinct selection criteria.
1. Credibility (is this guide correct?): measured by incoming
   evidence. This is the bid.
2. Informativeness (does this guide say what to expect?):
   measured by outgoing consequence structure. This is not
   the bid.

If informativeness is wanted as a selection criterion, it
should be specified as a separate term or tie-breaker, not
smuggled into the "evidence bid." The integration spec's
architectural compression goal (A3: "the same bid governs
both") requires one function with one meaning.

## Why not amend the spec for bidirectional (option b)

Amending the spec to authorize bidirectional counting would:
- Redefine "evidence bid" to mean "embeddedness," a weaker
  and less principled concept.
- Break the A3 compression: ACT's bid and CLA-2's bid would
  be different functions, and retention vs selection could
  disagree on the same node.
- Reward prediction verbosity over prediction accuracy.
- Require re-justifying every downstream use of the bid
  (eviction, standing, selection) under the new semantics.

No test or prereg prediction requires bidirectional counting.
The red team confirmed all 24 ACT tests pass under directional
semantics (all test evidence is incoming).

## Why not a hybrid (option c)

Any hybrid (e.g., "count outgoing only when the outcome is
highly evidenced") introduces a new rule not present in any
frozen spec, adds a second threshold to tune, and still breaks
the one-function compression. Rejected as unprincipled
complexity.

## Recommendation

**Option (a): align ACT `bid()` to directional counting.**

Change act.zag `bid()` to count only incoming edges
(`t==a`), matching CLA-2 `evcount()` semantics. This is a
two-line change (remove the `if(f==a)` branch). No test
changes needed. The spec A3 claim ("reuses the same function")
becomes true.

If a future prereg wants informativeness as a selection
criterion, it should be frozen as a separate, named
mechanism, not folded into the evidence bid.

## Governance

- Analysis only. No code changes made.
- Zero Python invocations. Toolchain guard recorded in
  NAMECHECK.md.
- No sealed FW1-FW9 files accessed.
- Contaminated paper zero-diff.
- Dash-clean.
