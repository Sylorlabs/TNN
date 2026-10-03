# DEVINT-CLA2 Red Team Report

**Verdict: DEVINT-CLA2-REDTEAM-COMPLETE.**
**Target:** `devint_cla2_build/devint_cla2.zag` (commit `35f9500b2`, BUILD-PASS, 11 stages).
**Prereg:** `devint_cla2_prereg/PREREG_DEVINT_CLA2.md` (commit `f24063bcb`).
**Method:** read-only source audit (full 1251-line read), binary reproduction,
pure-Zag empirical pressure probes with verbatim-extracted retention functions
(`/tmp/devint_redteam/pressure_test.zag`, pinned znc `abed8aa1`).
Implementation untouched. No sealed FW files accessed. Zero Python invoked.

## Summary of verdicts

| Vector | Verdict |
|---|---|
| 1. Unseen domain transfer | ATTACK-SUCCESS |
| 2. Long interference (10x) | ATTACK-SUCCESS |
| 3. Stage-label leakage (B3) | ATTACK-PASS (with caveat) |
| 4. GROUP protection under pressure | ATTACK-SUCCESS (conditional) |
| 5. Contradiction handling | ATTACK-SUCCESS (partial) |
| 6. K1/K2/K3 | K1 PASS, K2 qualified, K3 PASS |

**Bottom line:** The frozen B1-B5 bars literally hold, so BUILD-PASS stands.
But six prereg-specified elements were not implemented as specified, and the
retention mechanism has three genuine fragilities under sustained pressure.
The BUILD_REPORT overclaims on M2. Details below.

## What genuinely works (adversarial honesty)

- All 11 stages run in one process on one persistent workspace (B1 holds).
- Binary reproduction: re-ran `devint_cla2_bin`, got BUILD-PASS with identical
  numbers (S5 5 ACTIVE, S11 17/17, procedure 3/3).
- `feed_episode` takes only episode bytes; no stage/task/mode parameter on any
  learner entry point.
- CONTRADICTS edges are authored, rules demote, superseded history is
  retrievable (S7/S9 core genuinely passes).
- UNCERTAINTY raise/resolve works as workspace structure with an ACT-visible
  selection trace (S8 genuinely passes).
- GROUP/MEMBER formation works on the S1/S2 corpus (4 GROUPs, 0 spurious).

## Vector 1: Unseen domain transfer -- ATTACK-SUCCESS

`form_groups` (lines 299-340), presented as the concept-formation mechanism,
calls `s1_episode(i)` and `s2_episode(i)` internally (lines 302, 317). It does
not operate on the learner's accumulated experience; it replays the frozen
harness corpus. Fed a novel domain, `form_groups` would still count the
original bik/gup/zol/tav segments. The mechanism is not reusable.

Additional hard domain couplings in mechanism functions:

- `feed_episode` updates substring statistics for length-3 substrings only.
- `segment_episode` tries length 3 exclusively ("morphemes are length 3");
  no lexicon match at length 3 returns -1. A length-4 morpheme domain fails.
- `build_lexicon` threshold (>= 2) is generic; the length is not.

The byte-literal morpheme checks (lines 863-866, 956-959, 1004-1005,
1050-1052, 1194-1197) live in `stage_*` functions, which the prereg allows as
harness infrastructure. But the `form_groups` coupling is inside a mechanism
function, and the S6 pairing derivation (vector 6) crosses from "feed
schedule" into "performing the induction."

## Vector 2: Long interference -- ATTACK-SUCCESS

Empirical probes in pure Zag with verbatim-extracted `evict_one`/`bid`
(identical code to the implementation):

**T1 (200 distractor episodes, 60 evictions): evidence-cascade failure.**
All 3 rules (bid 5 each) were evicted. Mechanism: unprotected bid-0 evidence
nodes are evicted first; rule SUPPORTS edges vanish with them; rule bids
collapse to 0; the positional tie-break (lowest node id, via strict `<` in
`evict_one`) then kills the low-id rules before the remaining distractors.
High-bid structures are only as safe as their unprotected evidence. In the
real implementation this is worse: `stage_s5` calls `rule_support` cnt times
with the SAME bigram node, so all of a rule's SUPPORTS edges share one
evictable node.

**M2 was never computed.** `m2_check` (line 663) is defined but never called.
The BUILD_REPORT claims "M2 holds" and "Bid-vs-survival correlation holds,"
but the frozen M2 metric (bid>=2 vs bid<=0 survival rates, >= 40 point gap)
was never measured. GROUPs survived S10 via harness-authored PROTECT edges,
not via bid. F4's guard ("eviction without bid correlation") is therefore
vacuous: the correlation it guards was never computed.

**F1 "no positional attractor" is shaky.** `evict_one` breaks bid ties by
lowest node id. Under bid-collapse (T1) the tie-break becomes the decider,
and it is positional.

**Prereg S10 required "post-eviction next-concept prediction accuracy on 10
held-out episodes measured."** Not implemented; `stage_s10` checks only
eviction count and GROUP survival.

## Vector 3: Stage-label leakage (B3) -- ATTACK-PASS with caveat

`feed_episode(W, ep)` carries only episode bytes. No stage label, task ID, or
mode flag reaches any learner entry point. B3 as literally specified holds.

Caveat: the leakage present is domain-answer leakage, not stage-label
leakage (vectors 1 and 6). `form_groups` reads frozen harness tables; the S6
harness derives the procedure pairing by byte inspection.

## Vector 4: GROUP protection under pressure -- ATTACK-SUCCESS (conditional)

**T2 probe: learner-authored protection is self-defeating.** With PROTECT
edges authored from a learner node (bid 0, unprotected) instead of node 2,
the anchor was evicted on the very first eviction; 1 of 2 GROUPs fell within
120 further evictions. Protection works ONLY because the anchor is hardcoded
node 2 and `evict_one` hard-skips nodes 0-2 (`let n:i32=3; // skip 0,1,2`).
The scheme cannot survive being learner-owned, which is what the
architecture intends.

**Payload/edge desync (T1):** after evidence eviction, rule0 showed
payload support = 5 with 0 live SUPPORTS edges. Rule payload counters are
never decremented when evidence edges are evicted. The "count edges, don't
store" philosophy is violated by rule payload counters; counted bid and
stored support permanently disagree after eviction.

## Vector 5: Contradiction handling -- ATTACK-SUCCESS (partial)

- **Boundary violations are not represented.** S7's 2 "boundary violation"
  events are a harness-local counter (`nviol=nviol+1`); no SURPRISE edge, no
  UNCERTAINTY node, no workspace structure of any kind. The prereg's ">= 1
  boundary-violation event logged" is satisfied only in the weakest sense.
- **SPLIT never attempted.** `split_group` (line 587) is defined but never
  called. Prereg S9: "SPLIT attempted on the boundary-violated concept."
  Combined with the unrepresented violations, there is no boundary-violated
  concept in the workspace to split. (Frozen B2 requires only demotion, so
  BUILD-PASS stands; the SPLIT half of S9 is unimplemented.)
- **T3 probe: retention is blind to demotion.** A demoted rule (state 0) with
  5 SUPPORTS and 1 CONTRADICTS (bid 4) survived 55 evictions. Each
  CONTRADICTS is -1 against +1 per SUPPORT, so revision barely dents
  retention priority. Contradicted knowledge is retained as strongly as
  confirmed knowledge; S9 changes state but not retention.
- What holds: CONTRADICTS edges authored, demotion occurs, history
  retrievable. The F2 falsification guard is genuinely not triggered.

## Vector 6: K1/K2/K3

- **K1 PASS.** Prereg `f24063bcb` verified as ancestor of `35f9500b2`
  via `git merge-base --is-ancestor`.
- **K2 qualified PASS.** Zero modes, bridges, handlers; no stage params.
  Qualifications: (a) `form_groups` calls frozen episode tables; (b) S6
  pairing supplied by harness, not induced (see below); (c) positional
  tie-break in `evict_one`.
- **K3 PASS.** Pure Zag. Sole "python" match is the "No Python" comment.

**S6 procedure "learning" does not learn from examples.** `s6_train_out`
(line 717) is defined but never called; `s6_train_in` (line 967) is fed only
for substring stats. `learn_procedure(W,g0,g2,g1,g3,ev)` takes the pairing as
explicit harness arguments (derived by byte-matching in `stage_s6`). No code
reads the training pairs to derive bik<->zol / gup<->tav. The 5/5 held-out
check verifies storage and retrieval of a harness-supplied pairing.
Prereg S6 required "Record examples-to-criterion": never recorded.
This is procedure storage, not procedure induction.

## Prereg elements not implemented as specified

1. M2 bid-vs-survival metric: `m2_check` never called; "M2 holds" unmeasured.
2. S10 post-eviction accuracy on 10 held-out episodes: not measured.
3. S6 examples-to-criterion: not recorded; pairing not induced from examples.
4. S9 SPLIT: `split_group` never called.
5. S7 boundary violations: harness counter only, no workspace representation.

## Recommendations for parent

1. BUILD-PASS stands (B1-B5 literally hold), but the BUILD_REPORT's M2/F4
   claims should be corrected: M2 was not measured.
2. The retention mechanism needs hardening before it can carry the
   "evidence-driven" claim: protect evidence nodes or make rule bids robust
   to evidence loss; remove the positional tie-break or justify it; make
   demotion propagate to retention priority.
3. S6 should either induce the pairing from the training examples (real
   procedure learning) or be relabeled as procedure storage/retrieval.
4. `form_groups` should take a corpus argument instead of calling frozen
   episode tables; the length-3 assumption should be a parameter or derived.
5. Either implement SPLIT + violation representation or narrow S7/S9 claims.
6. The next red-team target should be a genuine 10x-interference run of the
   full 11-stage binary (needs a parameterized harness), not just the
   extracted retention functions.

## Governance

- Step 0 guard recorded in NAMECHECK.md (`/usr/bin/python3` present as
  unremovable system binary, documented non-use, zero invocations).
- Read-only audit: implementation, binary, and prereg untouched.
- Probes ran in /tmp (ephemeral); verbatim function extracts noted as such.
- No sealed FW1-FW9 files accessed. Contaminated paper zero-diff verified.
- No em dashes in this report (byte-verified before commit).
- Commit: owned path only, explicit pathspecs.
