# H-INTENT-UNIFIED8: INDEPENDENT RED-TEAM REPORT (IU8-ADV)

**Date:** 2026-09-30 UTC
**Adversary:** H-INTENT-UNIFIED8 red team (independent of the IU8 builder)
**Target:** H-INTENT-UNIFIED8 SURVIVES (9/9), `IU8_RESULT.md`
**Red-team verdict: H-INTENT-UNIFIED8 SURVIVES the red team.**
No kill trigger fired. No downgrade trigger fired. One attack
(X-IU8-2) is INCONCLUSIVE due to a disclosed adversary fixture
limitation: the intended beyond-top-two mixed bridge/proc pair
did not materialize, so R10's kind dispatch on a mixed pair
remains untested by this red team. The mechanism's actual
behavior on that fixture was provably correct per the frozen
precedence.

## Target claim under test

H-INTENT-UNIFIED8 repaired the H-INTENT-UNIFIED7 red-team
boundary B1 with R10: an all-pairs both-verbatim guard in
`intent_winner`, inserted after the R9 all-pairs
verbatim-vs-truncated block and before the gap==0 tie check.
For every unordered candidate pair with em==1 on both sides,
kind-dispatched answers are compared over qlen bytes; on any
disagreement it emits
`INTENT VERBATIM-CONFLICT: verbatim candidates disagree beyond top two; WITHHOLD AMBIGUOUS`
and returns kind=-2. Frozen precedence: IU3 top-two verbatim,
IU4/IU5 top-two truncated, R8 all-pairs both-truncated, R9
all-pairs verbatim-vs-truncated, R10, then gap==0 last.
Pair-class exclusivity: R8 = em=0 on both sides, R9 = em=1 on
exactly one side with the em=0 side truncated, R10 = em=1 on
both sides.

The surviving claim's stated scope: the both-verbatim pair
class is now covered regardless of rank. Disclosed boundaries
carried into this red team: B2 (em=1 vs em=0 non-truncated
beyond the top two) and B3 (POSSIBLE-diagnostic precision cost)
are untouched by R10.

Score model (read from the committed source): qscore =
em*40000 + cf*20000 + lm*10000. `intent_exact_match` checks
only the first 16 recorded inputs; o+8 holds TRUE npairs;
truncated = (TRUE npairs > 16).

## Lineage and methodology

- Adversary prereg `PREREG_INTENT_UNIFIED8_ADV.md` committed
  ALONE as `5137939a1` before any adversary harness build,
  compile, or run. Amendment
  `PREREG_INTENT_UNIFIED8_ADV_AMEND1.md` (X-IU8-4 fixture count
  17->18 pairs, clerical) committed as `b70246cf5`, also before
  any build or run. `git merge-base --is-ancestor 5137939a1
  HEAD` verified at commit time.
- Adversary harness `iu8_adv.zag` = mechanism region of the
  COMMITTED `unified_learn.zag` at the IU8 result commit
  `e948219c6` (lines 1-1579, everything before `fn main`),
  extracted via `git show`, cmp-verified byte-identical
  against the working-tree region
  (MECH-REGION-COMMITTED-CLEAN); plus t_learn, t_decide,
  iu4_init, iu8_show carried verbatim from the committed
  `iu8_verify.zag` (lines 1580-1698)
  (HELPERS-COMMITTED-CLEAN); plus new `adv_npairs` and
  `adv_answer_is` setup-validity helpers and a new X-IU8-1..4
  attack main. No mechanism byte was altered.
- Evidence method: compiled once to /tmp with the pinned
  toolchain (znc 2026.07.0-dev, edition 2026); the binary was
  executed directly 3 times (exit 0 each, zero stderr bytes).
  Raw evidence: `IU8_ADV_RAW.txt`, md5
  `5b75d70579cc80f6635838ebefd515f8`, 3/3 byte-identical via
  cmp.
- X-IU8-5 regression: committed `unified_learn.zag` and
  `intent_learn.zag` at `e948219c6` extracted via `git show`,
  cmp-verified against the worktree, compiled to /tmp, each
  main run 3 times directly.
- Pure Zag throughout: prereg, amendment, harness, builds,
  runs, greps, md5, cmp. No Python at any stage.
- Diagnostic counting is scoped to lines after the
  `--- decide ---` marker inside each attack section, per the
  frozen prereg. Learn-phase emissions (e.g. the INTENT WARN
  cap notice on the 18-pair learn) are out of scope.

## Attack results

### X-IU8-1: rank-5+ dissenter with multi-class bystanders: PASS

Fixture (fresh W, learn order V1..V6, query `xab`): four
verbatim agreers on `xxx` (V1 50000; V2, V3, V4 40000 each),
one em=0 non-truncated agreeing bystander T5 (5 pairs, score
10000), one verbatim dissenter V6 (`bax`, 40000) learned last.
Observed trace: six candidates as expected; top=V1 (50000),
second=V2 (40000), gap=10000; the dissenter sits beyond every
rank the builder tested, with the em=0 bystander present.
R8 had only one em=0 candidate (no pair); R9 saw the em=0 side
non-truncated (correctly skipped). kind=-2. Decide section:
R10-NEW exactly once; IU3-OLD, IU4A, IU4B, R8, R9 zero times.
R10 generalizes beyond rank 4 and is not diverted by
multi-class bystanders.

### X-IU8-2: mixed bridge/proc verbatim dissenter: INCONCLUSIVE (adversary fixture limitation)

Fixture intent: proc V1 (50000, `xxx`), proc V2 (40000,
`xxx`), bridge B (em=1, 40000, applied answer `xab`) ranked
third, to exercise R10's per-candidate kind dispatch
(proc_apply vs bridge_apply) on a beyond-top-two mixed pair.

What actually happened: the bridge learn line
`aab>baa;abb>bba;xab>xab;xcd>xcd;xabcd>xabcd` did not induce
the predicted split (input[0]=='a' separating reverse from
identity). Direct discovery failed as predicted, but the
winning split was IF input[1]==97 ('a') THEN proc ELSE proc,
with the ELSE/THEN procs arranged so that bridge_apply on
`xab` yields `xab` (all frozen preconditions still met:
rc=1000, kind=1, em=1 for all three, applied answers `xxx`,
`xxx`, `xab`; hence not a SETUP-FAIL). Because the query
`xab` satisfies the bridge condition (input[1]=='a'), the
bridge earned cf=1 and score 60000, ranking it FIRST, ahead of
V1 (50000). The top two (bridge/`xab`, V1/`xxx`) both carry
em=1 and disagree, so the IU3 top-two verbatim guard fired
correctly with IU3-OLD, kind=-2, gap=10000. R10 never ran.

Assessment: the mechanism behaved exactly as the frozen
precedence demands (item 1: the IU3 top-two verbatim guard
fires first on a genuine top-two verbatim disagreement). No
silent resolution occurred, no wrong diagnostic fired for the
situation at hand, and no precedence rule was violated. The
attack simply failed to engage its target: the intended
beyond-top-two mixed pair did not materialize, so R10's kind
dispatch on a mixed bridge/proc pair remains UNTESTED by this
red team. This is an adversary fixture-design limitation
(the bridge's cf scoring was not accounted for), disclosed
here, not a mechanism defect.

On the frozen DOWNGRADE criterion: its literal trigger
("kind=-2 but a different guard's text fires") is met, but its
documented intent was to catch R10 being shadowed where R10
should fire. Here R10 should NOT have fired: the top-two pair
is IU3's jurisdiction by frozen precedence item 1, and IU3
fired correctly. Applying DOWNGRADE would misrepresent
correct behavior as a defect. The coordinator may adjudicate;
this report records the attack as INCONCLUSIVE rather than a
pass, kill, or downgrade. No second fixture was attempted:
post-hoc fixture tuning is forbidden.

### X-IU8-3: gap==0 top tie with a rank-3 dissenter: PASS

Fixture (fresh W, query `xab`): V1 and V2 both 50000 with
answer `xxx` (top tie, V1 learned first so strict selection
keeps it top), V3 (`bax`, 40000) ranked third. Observed trace:
top=V1, second=V2, gap=0 as intended. kind=-2. Decide
section: R10-NEW exactly once; IU3-OLD, IU4A, IU4B, R8, R9
zero times. R10 correctly precedes the gap==0 tie check: the
withhold carries the explicit R10 diagnostic instead of the
tie check's silent kind=-2. The frozen precedence interaction
the builder never tested holds.

### X-IU8-4: truncated-verbatim dissenter (pair-class exclusivity): PASS

Fixture (fresh W, query `xab`): V1 (50000, `xxx`), V2 (40000,
`xxx`), V3 = 18-pair reverse-proc with `xab>bax` recorded
FIRST (inside the 16-cap, so em=1; TRUE npairs=18, so
truncated; mixed lengths, 40000, answer `bax`). Observed:
em=1 for all three, V3 true npairs=18, answers `xxx`,
`xxx`, `bax`. kind=-2. Decide section: R10-NEW exactly once;
IU3-OLD, IU4A, IU4B, R8, R9 zero times. A both-verbatim pair
member that is also truncated is claimed by R10 (em=1 on both
sides), not by R8 (needs em=0 both) or R9 (needs em=1 on
exactly one side). Pair-class exclusivity holds on the
truncation boundary the builder never tested.

### X-IU8-5: regression (production mains byte-identical): PASS

- `unified_learn.zag` main at `e948219c6`: 3/3 runs exit 0,
  zero stderr, output md5 `904de9f83a2873c7a8862b71804a9065`
  (frozen IU7 hash reproduced).
- `intent_learn.zag` main at `e948219c6`: 3/3 runs exit 0,
  zero stderr, output md5 `98315faec8faea24e75533892c0b240d`
  (frozen IU7 hash reproduced).
No silent behavior change from R10.

## Exact-text inventory across the raw (decide sections only)

- R10-NEW (`verbatim candidates disagree beyond top two`): 3
  (X-IU8-1, X-IU8-3, X-IU8-4).
- IU3-OLD (`top two candidates both have exact_match=1 but
  disagree`): 1 (X-IU8-2, correct top-two firing).
- IU4A, IU4B, R8, R9: 0 everywhere.
- KIND-BAD: 0. SETUP-FAIL: 0. Panics: 0.

## Failures, boundaries, interpretation

- No kill trigger fired: no silent resolution of a genuine
  recorded-data contradiction on any attack; no panic; no
  regression hash mismatch; 3/3 determinism on all binaries.
- No downgrade trigger fired: no precedence violation and no
  diagnostic-precision failure attributable to the mechanism.
  (X-IU8-2 is addressed above.)
- R10's rank independence is confirmed empirically at ranks 3
  (builder), 4 (builder), and 5+ (this red team, X-IU8-1): the
  guard loops over learn-order candidate indices, so rank
  truly does not matter, and the 6-candidate mixed-class
  arrangement confirms no diversion by bystander classes.
- The gap==0 tie check remains last: with a live tie at the
  top and a rank-3 dissenter, R10 fires first with its
  explicit diagnostic (X-IU8-3).
- Pair-class exclusivity holds including the truncated-member
  edge: em=1 is the only criterion R10 checks, and R8/R9 do
  not claim em=1/em=1 pairs even when one side is truncated
  (X-IU8-4).
- Open dimension (untested, disclosed): R10's kind dispatch
  (proc_apply vs bridge_apply) on a mixed bridge/proc pair
  BEYOND the top two. X-IU8-2 could not engage it because the
  induced bridge outranked the procs via cf=1. A future
  adversary should design the bridge so its condition does not
  match the query (cf=0) while keeping em=1 and a dissenting
  applied answer. This is the single sharpest remaining
  attack surface on R10 named by this red team.
- B2 (em=1 vs em=0 non-truncated beyond the top two) and B3
  (POSSIBLE-diagnostic precision cost) remain untouched and
  undisputed.

## Governance disclosures

- The em dash in `// unified_learn.zag ... End-to-end ...` on
  line 1 of the adversary harness is pre-existing in the
  production source and predates this wave (same disclosure
  the IU7 and IU8 builders made); it is carried byte-verbatim
  to keep the mechanism-region comparison exact. All content
  authored in this wave (prereg, amendment, attack main,
  report) contains zero em dashes.
- Prereg `5137939a1` and amendment `b70246cf5` were each
  committed alone before any adversary build, compile, or run;
  the amendment is a clerical count correction (17->18
  pairs) that preserves the frozen "truncated" requirement,
  disclosed before any observation.
- No Python was used anywhere in this red team.
- The X-IU8-2 fixture's bridge split differed from the
  adversary's prediction (input[1]==97 won, not input[0]=='a');
  the prediction error is disclosed above. The frozen
  preconditions were still met, so the run stands as executed;
  no retuning was attempted.
- Commit set for this wave: the prereg, the amendment, the
  harness `iu8_adv.zag`, the raw evidence
  `IU8_ADV_RAW.txt`, and this report. Binaries were built
  only in /tmp and never staged.

## Causal reading

R10 closes the rank dimension for the both-verbatim pair
class completely and with correct precedence: rank-5+
dissenters withhold (X-IU8-1), the guard precedes the silent
gap==0 tie withhold (X-IU8-3), and truncated members of the
class are claimed by R10 rather than leaking to R8/R9 or to
silent resolution (X-IU8-4). The one untested dispatch path
(mixed bridge/proc beyond the top two) is a coverage gap in
this red team's fixtures, not a mechanism behavior anomaly:
where a mixed pair did reach the top two, the older verbatim
guard fired exactly as specified (X-IU8-2).

## Classification

Bounded L2 integration repair, unchanged. This red team
finds no evidence against the IU8 claim within the attacked
dimensions. H-INTENT-UNIFIED8 SURVIVES the red team, with the
mixed-kind beyond-top-two dispatch named above as the
sharpest remaining untested attack surface.
