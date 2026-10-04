# H-INTENT-UNIFIED7: INDEPENDENT RED-TEAM REPORT (IU7-ADV)

**Date:** 2026-09-29
**Adversary:** H-INTENT-UNIFIED7 red team (independent of the IU7 builder)
**Target:** H-INTENT-UNIFIED7 SURVIVES (8/8), `IU7_RESULT.md`
**Red-team verdict: H-INTENT-UNIFIED7 SURVIVES the red team.**
No kill trigger fired. No downgrade trigger fired. One attack
(X-IU7-1) yielded no conclusion due to a fixture setup failure, and
is reported as such rather than as a pass or a fail.

## Target claim under test

H-INTENT-UNIFIED7 repaired the X-IU6-2 verbatim third-anchor boundary
with R9: an all-pairs verbatim-vs-truncated guard in `intent_winner`,
inserted after the R8 all-pairs both-truncated block and before the
gap==0 tie check. For each unordered candidate pair (a,b) with a<b,
if em==1 on exactly one side and the em==0 side has a truncated
record (true npairs > 16), the guard computes kind-dispatched
answers over qlen bytes; on any disagreement it emits
`INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets
truncated record with different answer beyond top two; WITHHOLD
AMBIGUOUS` and returns kind=-2.

The surviving claim's stated scope (from `IU7_RESULT.md`): the
verbatim-vs-truncated branches now cover genuine contradictions
among ALL candidates regardless of rank, for pairs with em=1 on
exactly one side and a truncated em=0 record on the other.

Disclosed boundaries carried into this red team:
- B1: a both-verbatim (em=1 on both sides) disagreement beyond the
  top two remains out of scope; the IU3 verbatim guard is
  top-two-only.
- B2: an em=1 vs em=0 non-truncated pair remains out of scope (same
  as R4/R5).
- B3: the precision cost of the POSSIBLE diagnostic (disclosed, not
  a bug).

Score model (frozen, read from the committed source):
qscore = em*40000 + cf*20000 + lm*10000. Proc candidates always
have cf=0.

## Lineage and methodology

- Adversary prereg `PREREG_INTENT_UNIFIED7_ADV.md` committed ALONE
  as `069bb3bcf` before any adversary harness build, compile, or
  run. No amendments. `git merge-base --is-ancestor 069bb3bcf HEAD`
  to be verified at commit time.
- Adversary harness `iu7_adv.zag` = mechanism region of the
  COMMITTED `unified_learn.zag` (lines 1-1529, everything before
  `fn main`), extracted via `git show HEAD:...`, cmp-verified
  byte-identical against the working-tree region
  (MECH-REGION-COMMITTED-CLEAN); plus t_learn, t_decide, iu4_init
  carried verbatim from `iu7_verify.zag` (lines 1530-1579); plus a
  new `adv_show` helper (prints kind/slot/em/npairs/applied answer
  for a learned candidate) and a new X-IU7-1..3 attack main. No
  mechanism byte was altered.
- Evidence method: compiled once to /tmp with the pinned toolchain
  (znc 2026.07.0-dev, edition 2026); the binary was executed
  directly 3 times (exit 0 each) to avoid `--run` compile-time
  analyzer warnings on stderr. This is the same method the IU6 and
  IU7 builders used. Binaries were built in /tmp only and never
  committed.
- Raw evidence: `IU7_ADV_RAW.txt`, md5
  `2b12914e5424a06b6975c859b1e032cc`, 3/3 runs byte-identical
  (cmp). Exit 0 on all runs.
- Pure Zag throughout: prereg, harness, builds, runs, greps, md5,
  cmp. No Python at any stage, including scratch analysis.
- X-IU7-4 rebuilt `unified_learn.zag`, `intent_learn.zag`, and
  `iu7_verify.zag` from `git show HEAD:...` blobs (worktree
  cmp-verified identical to the committed blobs first), compiled
  each once to /tmp, ran each main 3 times.

## Attack X-IU7-1: both-verbatim disagreement beyond the top two

**Purpose (frozen):** verify disclosed boundary B1 is real and
genuinely exploitable, not merely asserted.

**Frozen fixture:** fresh W; learn V1 =
`xab>xxx;xbc>xxx;xde>xxx`, V2 =
`xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`, V3 =
`xbcd>yyy;xdef>yyy;xfgh>yyy;xijk>yyy;xlmn>yyy;xab>yyy`; query `xab`.

**Result: SETUP-FAIL. No conclusion.** The V3 teaching line failed
to learn. Raw evidence, quoted verbatim from `IU7_ADV_RAW.txt`:

```
ROUTE [xbcd>yyy;xdef>yyy;xfgh>yyy;xijk>yyy;xlmn>yyy;xab>yyy] -> PROC_LEARN (2+ segs, str>str)
bridge: direct failed, inducing condition...
ULEARN FAIL: no program and no bridge
T LEARN tag=X71-V3 rc=-1
X-IU7-1 SETUP-FAIL v1=0 v2=1 v3=-1
```

V1 learned as proc slot 0 (rc=0) and V2 as proc slot 1 (rc=1), both
as in the proven shapes. V3 returned rc=-1: program discovery found
no fitting program and bridge induction also failed, so no
candidate existed for V3 and the attack arrangement could not be
constructed.

**Causal interpretation of the setup failure (read from the
committed source, no new experiments):** the procedure store's
programs compute output as copies of input characters by index:
`proc_apply` does `out[k]=inp[idx]` where `idx=peval(...)` must be
a valid input index (`if(idx<0 || idx>=n){return 0;}`). V3's
teaching pairs demand output character `y`, but every V3 input
(`xbcd`, `xdef`, `xfgh`, `xijk`, `xlmn`, `xab`) contains only the
characters {x,a,b,c,d,e,f,g,h,i,j,k,l,m,n}. No index program can
emit a character absent from the input, so direct discovery
correctly fails, and the bridge path also fails on this line. The
V1/V2 shapes work because their outputs (`x`) are the first input
character (index-0 program). The failure is a property of the
fixture string I chose (constant `yyy` with x-leading inputs), not
of the R9 guard under test.

**Consequence per the frozen prereg:** SETUP-FAIL yields no
conclusion. Boundary B1 is NOT confirmed and NOT refuted by this
red team. It remains a disclosed but empirically untested boundary.
I did not redesign or rerun the fixture: the prereg froze the
fixture, and post-hoc fixture tuning would violate prereg
discipline. A concrete follow-up fixture is proposed below, not
executed.

## Attack X-IU7-2: em=1 vs em=0 non-truncated pair beyond the top two

**Purpose (frozen):** verify disclosed boundary B2 is real.

**Frozen fixture:** fresh W; learn V1 =
`xab>xxx;xbc>xxx;xde>xxx`, V2 =
`xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`, T4 =
`abc>cba;def>fed;ghi>ihg`; query `xab`.

**Result: SUCCESS. Boundary B2 CONFIRMED.** All four frozen
success conditions hold, quoted verbatim from `IU7_ADV_RAW.txt`:

1. Candidate records (via `adv_show`):
```
ADV SHOW tag=X72-V1 kind=0 slot=0 em=1 npairs=3 ok=1 answer=[xxx]
ADV SHOW tag=X72-V2 kind=0 slot=1 em=1 npairs=6 ok=1 answer=[xxx]
ADV SHOW tag=X72-T4 kind=0 slot=2 em=0 npairs=3 ok=1 answer=[bax]
```
V1 and V2 are verbatim procs answering `xxx`; T4 is a proc with
em=0, npairs=3 (not truncated, 3 <= 16), whose reverse program
applied to `xab` gives `bax`, differing from `xxx`. Condition 1
holds.

2. Decision:
```
  cand kind=proc slot=0 exact_match=1 len_match=1 train_len=3 seq=0 cond_fire=0 score=50000
  cand kind=proc slot=1 exact_match=1 len_match=0 train_len=-1 seq=1 cond_fire=0 score=40000
  cand kind=proc slot=2 exact_match=0 len_match=1 train_len=3 seq=2 cond_fire=0 score=10000
T DECIDE tag=X72-xab kind=0 slot=0 gap=10000 answer=[xxx]
```
kind=0 (decisive proc), answer `xxx`. Condition 2 holds.

3. The X-IU7-2 section contains zero lines with `CONFLICT`
(byte-counted: 0). Condition 3 holds.

4. Setup validity (condition 1's proc/em/npair checks) holds as
shown above.

**Causal reading:** top=V1 (50000), second=V2 (40000); the IU3
verbatim guard sees top-two agreement and falls through; the
top-two truncated guard needs em=1 on exactly one side of the top
two (both are em=1) or em=0 on both sides, so neither branch fires;
R8 skips every pair involving an em=1 candidate, and T4 is the
only em=0 candidate, so no R8 pair exists; R9 examines pairs
(V1,T4) and (V2,T4) but T4 is not truncated (npairs=3), so both are
skipped; gap=10000, no tie. The mechanism returns the top
candidate's answer with no diagnostic. T4's generalized `bax` is
silently resolved.

**Consequence per the frozen prereg:** boundary B2 CONFIRMED as
stated. The surviving claim never covered em=1 vs em=0
non-truncated pairs, so per loop precedent the verdict is
UNCHANGED. Disclosed caveat: T4's contradiction is a
generalization (its program applied to an untaught input), not
recorded evidence; the top-two verbatim-vs-truncated guard would
have caught this pair had T4 ranked in the top two. The boundary
is specifically about rank-hiding of non-truncated em=0 pairs.

## Attack X-IU7-3: rank-4 verbatim-vs-truncated dissenter

**Purpose (frozen):** test the headline R9 claim ("covers genuine
contradictions among ALL candidates regardless of rank") at rank 4.
R9 is all-pairs, so this attack was expected to fail against the
mechanism; a mechanism miss would have triggered DOWNGRADE.

**Frozen fixture:** fresh W; learn V1 =
`xab>xxx;xbc>xxx;xde>xxx`, V2 =
`xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`, V3 =
`xab>xxx;xbcd>xxx;xdef>xxx;xfgh>xxx`, T4 =
`abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
(the exact K-IU7-1 T3 string); query `xab`.

**Result: MECHANISM-HOLDS. The R9 claim survives at rank 4.** All
three frozen hold conditions are met, quoted verbatim:

1. Candidate records:
```
ADV SHOW tag=X73-V1 kind=0 slot=0 em=1 npairs=3 ok=1 answer=[xxx]
ADV SHOW tag=X73-V2 kind=0 slot=1 em=1 npairs=6 ok=1 answer=[xxx]
ADV SHOW tag=X73-V3 kind=0 slot=2 em=1 npairs=4 ok=1 answer=[xxx]
ADV SHOW tag=X73-T4 kind=0 slot=3 em=0 npairs=17 ok=1 answer=[bax]
```
Three verbatim agreers (`xxx`) and one truncated dissenter
(npairs=17 > 16, em=0, answer `bax`). Condition 1 holds. (The raw
also shows the honest record-cap warning for T4:
`INTENT WARN: record cap 16 reached; 17 training inputs, only first
16 recorded; em coverage incomplete`.)

2. Decision:
```
  cand kind=proc slot=0 exact_match=1 len_match=1 train_len=3 seq=0 cond_fire=0 score=50000
  cand kind=proc slot=1 exact_match=1 len_match=0 train_len=-1 seq=1 cond_fire=0 score=40000
  cand kind=proc slot=2 exact_match=1 len_match=0 train_len=-1 seq=2 cond_fire=0 score=40000
  cand kind=proc slot=3 exact_match=0 len_match=1 train_len=3 seq=3 cond_fire=0 score=10000
INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer beyond top two; WITHHOLD AMBIGUOUS
T DECIDE tag=X73-xab kind=-2 slot=-1 gap=10000
```
kind=-2. Condition 2 holds.

3. The NEW R9 diagnostic text
(`verbatim candidate meets truncated record with different answer
beyond top two`) appears exactly once in the X-IU7-3 section
(byte-counted: 1); no other guard's diagnostic appears. Condition
3 holds.

**Causal reading:** the top-two guards fall through (verbatim
agreement on `xxx`; em=1 on both sides of the top two); R8 finds
only one em=0 candidate and no pair; R9's all-pairs loop reaches
pair (V1,T4) and withholds with its own diagnostic before any
later pair matters. The rank-4 dissenter is caught exactly as the
headline claim promises. The DOWNGRADE trigger did not fire.

## Attack X-IU7-4: regression (no silent behavior change)

**Result: no regression. The KILL trigger did not fire.**

- `unified_learn.zag` rebuilt from the committed blob: main run 3
  times, 3/3 byte-identical, exit 0. Output md5
  `904de9f83a2873c7a8862b71804a9065`, exactly the frozen IU4
  hash. Suite line: `=== INTENT-UNIFIED RESULT: 20/20 ===`.
- `intent_learn.zag` rebuilt from the committed blob: main run 3
  times, 3/3 byte-identical, exit 0. Output md5
  `98315faec8faea24e75533892c0b240d`, exactly the frozen IU4
  hash. Suite line: `=== INTENT RESULT: 10/10 ===`.
- `iu7_verify.zag` rebuilt from the committed blob: run 3 times,
  3/3 byte-identical, exit 0, and cmp-verified byte-identical
  against the committed `IU7_VERIFY_RAW.txt`. All 8 `K-IU7-* PASS`
  lines reproduce.

No silent behavior change. The 8/8 builder claim reproduces
independently from committed sources.

## Determinism

Adversary binary: 3/3 runs byte-identical (cmp), md5
`2b12914e5424a06b6975c859b1e032cc`, exit 0 each. Suite rebuilds:
each 3/3 byte-identical as listed above.

## Boundaries after this red team

- B1 (both-verbatim beyond top two): REMAINS DISCLOSED BUT
  EMPIRICALLY UNTESTED. X-IU7-1 could not be constructed with the
  frozen fixture. This red team neither confirms nor refutes it.
- B2 (em=1 vs em=0 non-truncated beyond top two): CONFIRMED by
  X-IU7-2 with the full candidate-record evidence above.
- B3 (POSSIBLE-diagnostic precision cost): untouched by these
  attacks; stands as disclosed.
- R9's rank coverage: verified at rank 4 by X-IU7-3. Ranks 5+
  remain untested but the guard is all-pairs by construction
  (nested a<b loops over all ncand).

## What the verdict means and does not mean

H-INTENT-UNIFIED7 SURVIVES this red team: the R9 repair does what
its claim says (all-pairs verbatim-vs-truncated coverage,
verified at ranks 3 and 4), its precedence is intact (X-IU7-4
reproduces all 8/8 builder bars and both suite hashes), and the
one in-scope boundary probed (B2) behaves exactly as disclosed.
The red team did not test B1; the surviving claim never covered
B1, so the verdict is unchanged, but B1 should not be cited as
red-team-confirmed. Classification remains bounded L2 integration
repair. Not L3. Nothing in this red team changes that.

## Proposed follow-up (not executed, needs its own prereg)

A valid X-IU7-1 retry must use a disagreeing verbatim answer
composable from the dissenter's own input characters (the
procedure store only copies input characters by index). Concrete
candidate, NOT run: V1 = `xab>xxx;xbc>xxx;xde>xxx` (50000, em=1,
`xxx`); V2 = `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`
(40000, em=1, `xxx`); V3 = `xab>bax;abcd>dcba` (reverse program,
`xab` recorded so em=1, mixed lengths so lm=0, expected score
40000, recorded answer `bax`); query `xab`. Expected arrangement:
top=V1 (50000), second=V2 (40000, learned before V3 so strict
selection keeps it second on the tie), V3 (40000) outside the top
two, genuine recorded `xab>bax` vs `xab>xxx` contradiction
silently resolved to kind=0/`xxx` if B1 holds. This fixture must
be preregistered fresh before anyone runs it.

## Governance disclosures

1. Adversary prereg `069bb3bcf` strictly precedes all adversary
   harness builds and runs. No amendments. Commit-ancestor check
   to be recorded at commit time.
2. Pure Zag throughout, including all scratch analysis (greps,
   md5, cmp, byte counts). Zero Python at any stage.
3. The mechanism region was extracted from the committed blob and
   cmp-verified byte-identical; no mechanism byte was altered for
   the adversary harness.
4. Binaries built in /tmp only, never committed.
5. Only adversary-owned paths staged:
   `PREREG_INTENT_UNIFIED7_ADV.md` (already committed),
   `iu7_adv.zag`, `IU7_ADV_RAW.txt`, `IU7_ADV_RESULT.md`
   (this report). Concurrent workers' files untouched
   (pathspec-restricted staging).
6. No em dashes in adversary-authored loop documentation
   (byte-verified: 0 in the prereg, 0 in this report, 0 in the
   raw). Note: the committed `unified_learn.zag` line 1 contains
   one pre-existing em dash in a code comment
   (`// unified_learn.zag ... End-to-end ...`); it was carried
   byte-verbatim into `iu7_adv.zag` to preserve the
   cmp-verification, and is disclosed here rather than altered.
7. No test-answer literals were added to any mechanism region;
   all fixture strings live in the harness main().
8. The X-IU7-1 SETUP-FAIL is reported as no-conclusion per the
   frozen prereg, not reworked into a pass or a fail.

## Files (branch `tnn-native-lab`)

- `docs/lab/research-lead/overnight-20260928/PREREG_INTENT_UNIFIED7_ADV.md`
  (adversary prereg, committed alone as `069bb3bcf`)
- `docs/lab/research-lead/overnight-20260928/iu7_adv.zag`
  (adversary harness: committed mechanism region + helpers +
  attack main)
- `docs/lab/research-lead/overnight-20260928/IU7_ADV_RAW.txt`
  (raw evidence, md5 `2b12914e5424a06b6975c859b1e032cc`, 3/3
  byte-identical, exit 0)
- `docs/lab/research-lead/overnight-20260928/IU7_ADV_RESULT.md`
  (this report)

## Suggested follow-ups for parent

1. Fresh-prereg X-IU7-1 retry with the input-character-composable
   fixture proposed above, to empirically settle boundary B1.
2. Paper lane: the H-INTENT-UNIFIED7 section should record that
   B2 is red-team-confirmed while B1 remains disclosed but
   empirically untested (it must not be cited as confirmed).
3. Consider whether the procedure store's input-copy-only program
   space (which made constant-`yyy` unlearnable) deserves its own
   characterization lane; it bounded this red team's fixture
   design.
