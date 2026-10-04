# H-INTENT-UNIFIED9: INDEPENDENT RED-TEAM REPORT (IU9-ADV)

**Date:** 2026-09-30 UTC
**Adversary:** H-INTENT-UNIFIED9 red team (independent of the IU9 builder)
**Target:** H-INTENT-UNIFIED9 SURVIVES (4/4), `IU9_RESULT.md`
**Red-team verdict: H-INTENT-UNIFIED9 SURVIVES the red team.**
No kill trigger fired. No downgrade trigger fired. No bar
SETUP-FAILed. Both disclosed boundaries (B2, B3) were
characterized empirically: B2 is confirmed real (the pair class
is genuinely unguarded, exactly as disclosed), and R9's
POSSIBLE-diagnostic guard was verified working as specified,
which frames B3's precision cost as structural rather than
defective.

## Target claim under test

H-INTENT-UNIFIED9: R10's kind dispatch (proc_apply vs
bridge_apply) on a mixed bridge/proc pair beyond the top two is
correct, and R10 does not over-withhold on agreeing answers with
different internal slots. The IU9 builder closed the IU8 red
team's named gap (a (proc,bridge) pair with the bridge second)
and audited precision on proc/proc agreement.

## Lineage and methodology

- Adversary prereg `PREREG_INTENT_UNIFIED9_ADV.md` committed
  ALONE as `1ad5d1d1f` before any adversary harness build,
  compile, or run. `git merge-base --is-ancestor 1ad5d1d1f
  HEAD` verified.
- Adversary harness `iu9_adv.zag` = mechanism region of the
  COMMITTED `unified_learn.zag` at HEAD (lines 1-1579,
  everything before `fn main`), extracted via `git show`,
  cmp-verified byte-identical against the working-tree region
  (MECH-REGION-COMMITTED-CLEAN); plus t_learn, t_decide,
  iu4_init, iu8_show carried verbatim from the committed
  `iu8_verify.zag` (lines 1580-1698)
  (HELPERS-COMMITTED-CLEAN); plus a new X-IU9-1/2a/2b/4a/4b
  attack main. No mechanism byte was altered.
- Fixture induction was validated in /tmp scratch runs BEFORE
  the prereg was frozen (empirical fixture design, not
  post-hoc tuning: the frozen prereg pins the validated
  fixtures, and all frozen evidence runs happened after the
  prereg commit).
- Evidence method: compiled once to /tmp with the pinned
  toolchain (znc 2026.07.0-dev, edition 2026); the binary was
  executed directly 3 times (exit 0 each, zero stderr bytes).
  Raw evidence: `IU9_ADV_RAW.txt`, md5
  `8907835e86e784d8c5f9a1ea34414bfe`, 3/3 byte-identical via
  cmp.
- X-IU9-3 regression: committed `unified_learn.zag` and
  `intent_learn.zag` at HEAD extracted via `git show`,
  cmp-verified against the worktree, compiled to /tmp, each
  main run 3 times directly. Mechanism region (lines 1-1579)
  verified byte-identical between the IU8 result commit
  `e948219c6` and HEAD (MECH-REGION-FROZEN).
- Pure Zag throughout: prereg, harness, builds, runs, greps,
  md5, cmp. No Python at any stage.
- Diagnostic counting is scoped to lines between the
  `>>> SEC <id> BEGIN` and `>>> SEC <id> END` markers (the
  decide section of each attack). Learn-phase emissions are
  out of scope.

## Attack results

### X-IU9-1: bridge/bridge kind dispatch: PASS

Fixture (fresh W, query `xab`): three bridges, no procs. The
candidate list is built procs-first, bridges-second, so R10's
pair loop can produce (proc,proc), (proc,bridge), and
(bridge,bridge) pairs, but never (bridge,proc). (proc,proc)
was tested by the IU8 builder and (proc,bridge) by IU9 K-IU9-1;
(bridge,bridge) is the only dispatch combination no frozen run
had ever exercised.

- B_a (`aab>aab;abb>abb;acb>acb;abcde>abcde;xab>xxx;xcb>xxx;xdb>xxx`):
  kind=1, em=1, cf=0, score 40000, answer `xxx`.
- B_b (`aad>aad;aae>aae;aaf>aaf;aabcd>aabcd;xab>xxx;xeb>xxx;xfb>xxx`):
  kind=1, em=1, cf=1, score 60000, answer `xxx` (the induced
  split matched the query; pinned in the frozen setup rather
  than the predicted cf=0).
- B_c (`aab>baa;abb>bba;acb>bca;abcde>edcba;xab>bax;xcb>bcx;xdb>bdx`):
  kind=1, em=1, cf=0, score 40000, answer `bax`.

Top two: B_b (60000) and B_a (40000), both `xxx`, both em=1:
they agree, so IU3 does not fire. R10's pair loop in
candidate-index order checks (B_a,B_b) first (agree on `xxx`),
then (B_a,B_c): `xxx` vs `bax`. Observed: kind=-2, gap=20000.
Decide section: R10-NEW exactly once; IU3-OLD, IU4A, IU4B, R8,
R9 zero times. The withhold was necessarily triggered by the
(B_a,B_c) pair: bridge_apply vs bridge_apply, the last
untested dispatch combination. It works exactly as specified.

### X-IU9-2a: precision, bridge winner agreeing with procs: PASS

Fixture (fresh W, query `xab`): Bw (bridge, em=1, cf=0, 50000,
`xxx`) wins outright over two procs (40000 each, `xxx`). All
agree. Observed: kind=1, slot=0, gap=10000, answer `xxx`.
Decide section: zero `WITHHOLD AMBIGUOUS` occurrences. The
kind=1 winner return path is intact and R10 does not fire on
bridge/proc agreement.

### X-IU9-2b: precision, truncated bridge agreeing with procs: PASS

Fixture (fresh W, query `xab`): a 17-pair const-`xxx` learn
induced a truncated bridge (kind=1, em=1, true npairs=17,
cf=1, score 70000, answer `xxx`), winning over two procs
(50000 each, `xxx`). All agree. Observed: kind=1, gap=20000,
answer `xxx`. Decide section: zero `WITHHOLD AMBIGUOUS`
occurrences. Neither R10 nor any truncated guard over-withholds
on a truncated kind=1 agreeing member. (X-IU8-4 showed a
truncated em=1 DISSENTER is claimed by R10; this is the
agreeing mirror.)

### X-IU9-3: regression: PASS

- `unified_learn.zag` main at HEAD: 3/3 runs exit 0, zero
  stderr, output md5 `904de9f83a2873c7a8862b71804a9065`
  (frozen IU7/IU8/IU9 hash reproduced).
- `intent_learn.zag` main at HEAD: 3/3 runs exit 0, zero
  stderr, output md5 `98315faec8faea24e75533892c0b240d`
  (frozen IU7/IU8/IU9 hash reproduced).
- Mechanism region lines 1-1579 byte-identical between
  `e948219c6` and HEAD: no mechanism change since IU8, as
  claimed.

### X-IU9-4a: boundary B2 characterization: PASS (boundary CONFIRMED)

Fixture (fresh W, query `xab`): V1 (50000, `xxx`, em=1), V2
(40000, `xxx`, em=1), R3 (5-pair reverse, em=0, true npairs=5,
not truncated, applied answer `bax`, score 10000). The (V1,R3)
and (V2,R3) pairs are exactly the disclosed B2 class: em=1 vs
em=0 non-truncated. No guard claims them (R8 needs em=0 on
both sides, R9 needs the em=0 side truncated, R10 needs em=1
on both sides). Observed: kind=0, gap=10000, answer `xxx`,
zero `WITHHOLD AMBIGUOUS` in the decide section. The genuine
disagreement (verbatim `xxx` vs 5-pair generalization `bax`)
resolves silently by score. B2 is real, exactly as disclosed.
This bar cannot kill (B2 is outside the IU9 claim scope); it
confirms the disclosure is accurate.

Adversary fixture note: the first attempt used two 50000
procs (gap=0) and hit the silent gap==0 tie withhold instead
of the intended B2 arrangement. The fixture was corrected to
V1/V2 at 50000/40000 during pre-prereg validation; the frozen
prereg pins the corrected fixture. The silent gap==0 tie
check remains last and silent, as previously documented.

### X-IU9-4b: boundary B3 context, R9 positive control: PASS

Fixture (fresh W, query `xab`): V0 (50000, `xxx`, em=1), V1
(50000, `xxx`, em=1), T2 (18-pair reverse record, query
unrecorded: em=0, true npairs=17, truncated, applied answer
`bax`, score 10000). The top two agree, so the top-two guards
do not fire. Observed: kind=-2. Decide section: the R9 text
(`verbatim candidate meets truncated record with different
answer beyond top two`) exactly once; IU3-OLD, IU4A, IU4B,
R8, R10-NEW zero times. R9 works as specified on a kind=0
truncated dissenter beyond the top two. (R9 also fires before
the gap==0 tie check here: gap=0 with an explicit diagnostic,
confirming the precedence order.)

## Exact-text inventory across the raw (decide sections only)

- R10-NEW (`verbatim candidates disagree beyond top two`): 1
  (X-IU9-1).
- R9 (`different answer beyond top two`): 1 (X-IU9-4b).
- IU3-OLD, IU4A, IU4B, R8: 0 everywhere.
- KIND-BAD: 0. SETUP-FAIL: 0. Panics: 0.
- `WITHHOLD AMBIGUOUS` total across all decide sections: 2
  (one R10, one R9).

## Failures, boundaries, interpretation

- No kill trigger fired: no silent resolution of a genuine
  recorded-data contradiction in any attacked dimension; no
  panic; no regression hash mismatch; 3/3 determinism.
- No downgrade trigger fired: no precedence violation and no
  diagnostic-precision failure attributable to the mechanism.
- R10's kind dispatch is now empirically confirmed on every
  reachable pair-kind combination: (proc,proc) by the IU8
  builder, (proc,bridge) by IU9 K-IU9-1, and (bridge,bridge)
  by this red team (X-IU9-1). The (bridge,proc) order is
  unreachable by construction (candidates are built
  procs-first, bridges-second) and the dispatch reads ka/kb
  symmetrically per candidate, so no untested combination
  remains.
- Precision holds beyond the builder's audit: a bridge winner
  (kind=1) and a truncated bridge member agreeing with procs
  produce no withhold and the correct winner (X-IU9-2a/2b).
- B2 is empirically real: the em=1 vs em=0 non-truncated pair
  class beyond the top two resolves silently by score, with
  no guard claiming it (X-IU9-4a). The disclosure was
  accurate. This remains the sharpest known unguarded pair
  class and the natural next frontier if a principled
  evidence rule for it is formulated.
- B3 (POSSIBLE-diagnostic precision cost): R9 fires exactly as
  specified on truncated disagreement (X-IU9-4b). On the cost
  question itself, white-box analysis shows the cost is
  structural, not defective: the POSSIBLE guards compare
  applied answers from learned mappings, and a kind=0 learned
  mapping necessarily fits all of its recorded pairs, so its
  applied answer always matches the full record on recorded
  inputs. The cases where the guard withholds are exactly the
  cases where the full information is unknowable at decide
  time (the query is absent from the em-checked inputs and
  the record is truncated). No false-positive instance was
  constructed; the "cost" is the disclosed safety trade,
  working as designed.

## Adversary observations (not defects)

1. Bridge induction keeps its X-IU8-2 unpredictability: two
   fixtures induced splits whose condition matched the query
   (cf=1) instead of the predicted cf=0 split (X-IU9-1 B_b,
   X-IU9-2b Tt). Both still engaged their targets because
   top-two agreement was structurally guaranteed, and both
   were pinned in the frozen setup rather than retuned. This
   is an adversary-fixture-design note, not a mechanism
   defect: induction searches (pos,val) splits over the
   training data and the winning split is data-dependent.
2. A 17/18-pair const-`xxx` learn induces a bridge (cf=1),
   not a constant proc. Discovery behavior note only.
3. `bridge_apply` delegates to `proc_apply`, so applied
   answers are always exactly qlen bytes; the R10 comparison
   loop cannot read uninitialized tail bytes. The precision
   attack surface this would have opened does not exist.

## Governance disclosures

- The em dash in `// unified_learn.zag ... End-to-end ...` on
  line 1 of the adversary harness is pre-existing in the
  production source and predates this wave (same disclosure
  the IU7, IU8, and IU9 waves made); it is carried
  byte-verbatim to keep the mechanism-region comparison
  exact. All content authored in this wave (prereg, attack
  main, report) contains zero em dashes (byte-verified).
- Prereg `1ad5d1d1f` was committed alone before any adversary
  build, compile, or run. Fixture induction was validated in
  /tmp scratch runs before the prereg froze; the frozen
  prereg pins those fixtures and every frozen evidence run
  postdates the prereg commit. No bar was weakened or
  redefined after any observation. No Python was used
  anywhere.
- Commit set for this wave: the prereg (alone, beforehand),
  the harness `iu9_adv.zag`, the raw evidence
  `IU9_ADV_RAW.txt`, and this report. Binaries were built
  only in /tmp and never staged. Only owned paths staged
  (pathspec-restricted); concurrent workers' files untouched.

## Causal reading

R10's dispatch is now covered on all reachable kind
combinations with correct precedence and exact diagnostics,
and its precision holds for bridge winners and truncated
agreeing members, not just the proc/proc cases the builder
tested. The guard family's remaining open dimensions are
exactly the disclosed ones: B2 (an unguarded pair class,
now empirically confirmed rather than merely disclosed)
and B3 (a structural safety trade in the truncated guards,
now with its guard verified working as specified).

## Classification

Bounded L2 integration test, unchanged. This red team finds
no evidence against the IU9 claim within the attacked
dimensions. H-INTENT-UNIFIED9 SURVIVES the red team, with B2
confirmed as the sharpest remaining attack surface.
