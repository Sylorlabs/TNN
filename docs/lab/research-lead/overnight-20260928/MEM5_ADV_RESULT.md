# ADV_MEM5_RESULT: H-MEM5 Red Team Report

**Date:** 2026-09-29
**Adversary verdict: H-MEM5 DOWNGRADED (not killed).**
**Frozen prereg:** `PREREG_MEM5_ADV.md` (commit `0e457c276`), strictly before
any adversary implementation or execution (verified below: prereg commit is
an ancestor of the harness and result commits; no amendments).
**Target:** `mem5_learn.zag` at the H-MEM5 result commit (H-MEM5 SURVIVES 4/4).
**Raw evidence:** `MEM5_ADV_RAW_OUTPUT.txt` (md5
`3260cdb805d1a55047ca3dc9df8e7bfc`, 3 runs byte-identical via cmp, exit 0)
**Adversary harness:** `mem5_adv.zag` (mechanism region = lines 1..499 of the
frozen `mem5_learn.zag`, cmp-verified byte-identical against
`git show HEAD:...`; only `main` and fixture builders are new; no mechanism
edits)
**Pure Zag. No Python in fixtures, harness, build, execution, or analysis.**

## Stance and scope

The repair claim was assumed false. Four attacks were preregistered with
explicit frozen verdict rules before any implementation. One succeeds
(downgrade), one succeeds as supporting evidence, one fails as a
preregistered honest negative, one fails (no finding). The downgrade
narrows the interpretive claim; it does not touch the frozen K-M5 bars,
R1, or R3.

## Attack results

### X-M5-1 (stale-merit harm): SUCCEED -> DOWNGRADE

The X-M4-2a harm pattern recurs behind uses=2 stale merit. Fixture:
slot7 holds proc7 with uses=2, both queries ancient (lastq=101, outside
the 20-query operating window), prot window open (seq=105 < prot=109);
slots 0..6 hold procs 0..6 (uses 10..70); operating window Q[6..25] has
proc7 absent. Frozen run (3/3 byte-identical):

```
X-M5-1: wprot=LIFO vprot=slot6 cprot=2 wun=LFU vun=slot7
  [full counterfactual] protected: LIFO victim=slot6(proc6) | unprotected: LFU victim=slot7(proc7)
  [selected-policy] protected-victim=slot6 unprotected-victim=slot7
  CHURN-FULL:1 (winner flips LIFO->LFU; eviction slot6(proc6)->slot7(proc7))
```

Every frozen value matches the hand-derived expectation on first
execution (wprot=3, vprot=slot6, cprot=2, wun=0, vun=slot7, verdict 1;
no fixture tuning). The protected mechanism sacrifices proc6 (70 uses,
replay cost 2) to shield proc7 (2 ancient queries, window cost 0).
Cost 0 -> 2. This is the X-M4-2a harm verbatim, recurring through the
disclosed stale-merit residual instead of grace or fig-leaf merit.

Why this is a downgrade and not a boundary confirmation: the builder
disclosed the mechanism fact ("uses>=2 from ancient queries remains
protected") but did not disclose or demonstrate that the cost-0→2 harm
recurs through it. The H-MEM5 headline hypothesis claims the harm is
"closed at the mechanism level"; the natural reading is that the harm
pattern (protection-induced sacrifice of a queried proc for a
window-absent newcomer) is closed, not merely two fixtures. Per the
X-CV4-1 precedent, a disclosure of a mechanism fact does not convert a
successful demonstration of the harm into a non-finding.

Why not killed: frozen K-M5-1 (uses=0), K-M5-2 (uses=1), K-M5-3, K-M5-4
all still pass; the failure is the scope of the "substantive merit"
guarantee, not the implementation. The mechanism implements exactly what
was preregistered.

Narrowed claim (replaces the headline): "H-MEM5 closes the
protection-induced cost-0→2 harm for newcomers with uses in {0,1} and
for fresh uses>=2. The harm recurs for stale uses>=2: the merit gate
counts all-time uses with no recency weighting, so two ancient
window-absent queries suffice to shield a cost-0 newcomer and sacrifice
a queried procedure. The threshold raise narrows the harm class; it does
not close it. Recency-weighted merit (H-MEM6) is the follow-up."

### X-M5-2 (one-query cliff): SUCCEED (supporting evidence)

Two fixtures identical in every respect except slot7's uses (1 vs 2).
Frozen runs (3/3 byte-identical):

```
X-M5-2a: wprot=LFU vprot=slot7 cprot=0 wun=LFU vun=slot7
  CHURN-FULL:0 (winner stable at LFU; eviction unchanged)
X-M5-2b: wprot=LIFO vprot=slot6 cprot=2 wun=LFU vun=slot7
  CHURN-FULL:1 (winner flips LIFO->LFU; eviction slot6(proc6)->slot7(proc7))
```

Both match the hand-derived expectations on first execution. A single
marginal query flips the outcome from "evict newcomer at cost 0" to
"sacrifice proc6 at cost 2". By the builder's own rationale a single
query "is not evidence of merit (probe, misroute, noise)" — yet a single
query is exactly what moves a slot across the cliff. The repair's
efficacy rests on a knife-edge, not a substantive distinction. This
supports the X-M5-1 downgrade; it is not an independent verdict driver.

### X-M5-3 (newcomer churn): FAIL (honest negative, as preregistered)

Fixture: slot7 newcomer (proc7, uses=1, recent lastq=104, evictable)
alongside a protected stale slot (slot5, proc5, uses=2, ancient
lastq=90, protected). Frozen run (3/3 byte-identical):

```
X-M5-3: wprot=LFU vprot=slot7 cprot=1 wun=LFU vun=slot7
  CHURN-FULL:0 (winner stable at LFU; eviction unchanged)
```

Matches the hand-derived expectation. No divergence: the newcomer
(uses=1) is the global LFU minimum and is never protected, so both
modes agree on evicting it. A protection-induced cost harm against the
newcomer cannot arise by construction (protection only excludes slots
from eviction; the newcomer is never excluded). The residual is bounded
to unrepresentable opportunity cost, not protection-induced cost harm.

Observation (not a finding): the mechanism evicts the fresher uses=1
newcomer (lastq=104) while shielding the staler uses=2 slot
(lastq=90). The merit order (count) contradicts the recency order, and
the mechanism has no way to express the difference. This is the same
missing recency weighting as X-M5-1, seen from the other side.

### X-M5-4 (regression): FAIL (no finding)

`mem5_learn.zag` rebuilt unmodified from the committed blob
(`git show HEAD:...`, cmp-verified identical to the worktree file):
stdout md5 `2888f9331dae55f802055ec65e9101fb` matches the frozen value
exactly; 3 consecutive runs byte-identical; `ALL BARS PASS` printed;
0 FAIL lines. The builder's 4/4 stands as executed.

## Causal interpretation

The downgrade is a design-scope finding, not an implementation bug.
`elig()` implements exactly what the builder preregistered. The merit
signal and the cost signal live in different scopes: merit is all-time
(`st_uses` cumulative, never reset, never decayed); harm is
window-scoped (`replay_cost` over 20 queries). The protection decision
uses all-time merit to shield a slot from a window-scoped eviction. A
slot with 2 all-time queries and 0 window queries is "meritorious" by
the gate but free to evict by the cost function; protecting it cannot
reduce cost, only increase it. The X-M4-2a/2b repair raised the gate
from uses>0 to uses>=2, but the scope mismatch is untouched: 2 ancient
queries are no more probative of current demand than 1, and the
one-query cliff (X-M5-2) shows the threshold's marginal decision is
driven by exactly the unit the builder calls non-evidence. A principled
fix needs recency in the merit signal (the builder's own H-MEM6
direction), not a higher all-time count.

## Verdict aggregation (per frozen rules)

- X-M5-1 SUCCEED: H-MEM5 DOWNGRADED (not killed).
- X-M5-2 SUCCEED: supporting evidence (knife-edge).
- X-M5-3 FAIL: honest negative as preregistered; residual bounded.
- X-M5-4 FAIL: no finding; 4/4 regression stands.

Surviving claims: all four frozen K-M5 bars as executed; R1 full
counterfactual; R3 adversarial-target screen within its disclosed
scope. Narrowed claims: R4 substantive-merit probation (the
protection-induced cost harm is closed for uses in {0,1} and fresh
uses>=2; it recurs for stale uses>=2). H-MEM5 remains bounded L2; no L3
implication was claimed or affected.

## Governance disclosures

- Adversary harness reuses the frozen mechanism source verbatim
  (lines 1..499, through the close of `learn_stream`); only the driver
  `main` and fixture builders are new. No mechanism file was modified
  by the adversary. Correction to the prereg text: the prereg says
  "lines 1..498"; the actual region boundary is line 499 (the closing
  brace of `learn_stream`; line 498 is its final `return;`). The region
  was cmp-verified byte-identical against `git show HEAD:...`; the
  one-line correction changes nothing about the attack.
- The mechanism region contains no fixture literals (grep for the
  fixture constants finds only a header comment mentioning slot7;
  all mechanism logic uses accessors).
- Prereg commit `0e457c276` strictly precedes all adversary
  implementation and execution; no amendments were made. Ordering to be
  verified with `git merge-base --is-ancestor` at result commit.
- All fixture arithmetic was hand-derived in the prereg and reproduced
  on first execution; the first build failed only on a harness-side
  line-range cut (missing closing brace), fixed before any run; no
  fixture was tuned after seeing output.
- No Python was used at any stage (fixtures, harness, build,
  execution, analysis, or editing; edits via the file-editing tool).
- Determinism: 3/3 byte-identical adversary runs; 3/3 byte-identical
  regression rebuilds.
- Binaries built in /tmp/mem5adv only, never committed. Only
  adversary-owned paths staged. No em dashes in loop documentation.

## Files (all committed to `tnn-native-lab`)

- `PREREG_MEM5_ADV.md` (frozen prereg, commit `0e457c276`)
- `mem5_adv.zag` (adversary harness)
- `MEM5_ADV_RAW_OUTPUT.txt` (raw evidence, md5
  `3260cdb805d1a55047ca3dc9df8e7bfc`, 3/3 identical)
- `MEM5_ADV_RESULT.md` (this report)

## Suggested follow-ups for the parent

1. H-MEM6 repair hypothesis: recency-weighted merit (the builder's own
   stated direction). Suggested kill bars: the X-M5-1 fixture ->
   protected evicts slot7 at cost 0 (stale merit expires); the X-M5-2
   cliff -> no discontinous harm at the margin; K-M5-1..K-M5-4 still
   pass.
2. The paper's H-MEM5 line must read DOWNGRADED with the narrowed
   claim, superseding the SURVIVES headline.
3. Classification remains bounded L2, narrowed. Not L3.
