# PREREG: H-INTENT-UNIFIED7 Repair (FROZEN)

## Hypothesis

H-INTENT-UNIFIED7 closes the H-INTENT-UNIFIED6 red-team boundary
X-IU6-2 at the mechanism level:

- X-IU6-2: verbatim third-anchor. Two verbatim (em=1) candidates
  V1 (score 50000, answer `xxx`) and V2 (score 40000, answer `xxx`)
  ranked first and second; one truncated (em=0, true npairs=17)
  candidate T3 (score 10000, answer `bax`) ranked third. The
  verbatim guard sees top-two agreement (em=1 on both, answers agree)
  and falls through. The top-two truncated guard needs em=1 on
  exactly one side of the top two for the verbatim-vs-truncated
  branch, or em=0 on both sides for the both-truncated branch; the
  top two are em=1 on both sides, so neither branch fires. The R8
  all-pairs both-truncated guard skips every pair involving an em=1
  candidate, so no pair is compared. The genuine T3/V1 contradiction
  (`xab>bax` in T3's unrecorded tail vs `xab>xxx` in V1's recorded
  data) is silently resolved via ranking: kind=0, answer `xxx`.

The repair extends the verbatim-vs-truncated check pairwise over ALL
candidates, regardless of rank: for any unordered pair (a,b) where one
side carries em=1 and the other side has em=0 with a truncated record
(true npairs > 16), compare kind-dispatched answers over qlen bytes;
on any disagreement, WITHHOLD AMBIGUOUS with an explicit diagnostic.
This is a minimal, faithful extension of the R4/R5/R8 guard family.
Classification target: bounded L2 integration repair. No L3 claimed.

## Frozen kill bars

### K-IU7-1: X-IU6-2 closed (all-pairs verbatim-vs-truncated guard)

Fixture (exact, from IU6-ADV X-IU6-2):

- T3 = proc, 17 reverse pairs, `xab>bax` 17th (unrecorded):
  `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
  Record: 16 inputs, true npairs=17 (truncated), em=0 on `xab`.
- V1 = proc, 3 pairs, `xab>xxx` RECORDED:
  `xab>xxx;xbc>xxx;xde>xxx`
  Record: not truncated, em=1 on `xab`. Score 50000 (em=1, lm=1).
- V2 = proc, 6 pairs, `xab>xxx` RECORDED:
  `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`
  Record: not truncated, em=1 on `xab`. Score 40000 (em=1, lm=0,
  tlen=-1 mixed).

Learn order (fresh W): T3, then V1, then V2.
Query: `xab` (qlen=3).

PASS iff: kind=-2 AND the diagnostic line contains
`TRUNCATED-CONFLICT-POSSIBLE` and indicates the verbatim-vs-truncated
beyond-top-two scope (exact text frozen in R9 below).

FAIL: kind>=0 (silent resolution), kind=-2 with a top-two-only
diagnostic text (guard did not extend), or no diagnostic.

### K-IU7-2: precedence preserved (no shadowing, exact texts)

Three fixtures, each on fresh W, each asserting kind=-2 AND the exact
diagnostic text in the raw output:

(a) K-IU5-1a top-two both-truncated (proc-first):
    Proc learn: `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
    Bridge learn: `xcd>xxx;xef>xxx;xgh>xxx;xij>xxx;xkl>xxx;xmn>xxx;xop>xxx;xqr>xxx;qab>baq;wab>baw;eab>bae;rab>bar;tab>bat;yab>bay;uab>bau;iab>bai;xab>xxx`
    Query: `xab`. Exact text required:
    `INTENT TRUNCATED-CONFLICT-POSSIBLE: both records truncated with different answers; WITHHOLD AMBIGUOUS`
    (the UNCHANGED top-two diagnostic).

(b) K-IU4-1 top-two verbatim-vs-truncated:
    Proc learn: `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
    Bridge learn: `xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee`
    Query: `xab`. Exact text required:
    `INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer; WITHHOLD AMBIGUOUS`
    (the UNCHANGED top-two diagnostic).

(c) X-IU5-1 R8-only fixture (four truncated candidates):
    C3 proc: `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
    C1 bridge: `xbc>xxx;xde>xxx;xfg>xxx;xhi>xxx;xjk>xxx;xlm>xxx;xno>xxx;xpq>xxx;qab>baq;wab>baw;eab>bae;rab>bar;tab>bat;yab>bay;uab>bau;iab>bai;xab>xxx`
    C2 bridge: `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xopq>xxx;xrst>xxx;xuvw>xxx;qbcd>dcbq;wbcd>dcbw;ebcd>dcbe;rbcd>dcbr;tbcd>dcbt;ybcd>dcby;ubcd>dcbu;ibcd>dcbi;xab>xxx`
    Query: `xab`. Exact text required:
    `INTENT TRUNCATED-CONFLICT-POSSIBLE: truncated candidates disagree beyond top two; WITHHOLD AMBIGUOUS`
    (the UNCHANGED R8 diagnostic).

FAIL: any other kind, any of the three new-or-wrong diagnostic texts
on these fixtures, or a silent resolution.

### K-IU7-3: no regression (all K-IU6 bars still PASS)

- K-IU6-1: X-IU5-1 third-anchor (3 truncated) -> kind=-2, NEW R8
  diagnostic. (Same shape as K-IU7-2c minus one candidate.)
- K-IU6-2a/2b: covered by K-IU7-2a.
- K-IU6-3a: 16-char extraction cap. Two 20-char reverse pairs ->
  process exits 0 (no panic), honest-cap diagnostic appears, rc=-1.
- K-IU6-3b: covered by K-IU7-2b.
- K-IU6-3c: 129-pair fixture -> rc=-1, WORK honest failure, exit 0,
  no panic.
- K-IU6-3d: in-cap verbatim conflict (`xab>bax;abc>cba` vs
  `xab>xxx;xcd>xxx`) -> kind=-2. Verbatim guard intact.
- unified_learn.zag main() -> 20/20, output byte-identical to frozen
  IU4 evidence (md5 904de9f83a2873c7a8862b71804a9065).
- intent_learn.zag main() -> 10/10, output byte-identical to frozen
  IU4 evidence (md5 98315faec8faea24e75533892c0b240d).

### K-IU7-4: determinism

iu7_verify binary run 3 times -> byte-identical output.
unified_learn.zag main() run 3 times -> byte-identical.
intent_learn.zag main() run 3 times -> byte-identical.

## Frozen repair specification

### R9: all-pairs verbatim-vs-truncated guard (X-IU6-2)

In `intent_winner`, AFTER the R8 all-pairs both-truncated guard block
(the `if(second>=0){...}` containing the iu6_a/iu6_b loops) and BEFORE
the `if(second>=0 && gap==0)` tie check, insert the all-pairs
verbatim-vs-truncated guard:

For each unordered candidate pair (a,b) with a<b, both ranging over
0..ncand-1:
- Let em_a = get32(ce,a*4), em_b = get32(ce,b*4).
- If (em_a==1 && em_b==0) or (em_a==0 && em_b==1):
  - Let the em=0 side be m. Determine its truncation via
    intent_proc_base / intent_br_base (kind-dispatched on
    get32(ck,m*4)), checking get32(W,rec+8)>16, exactly as the
    existing guards do.
  - If the em=0 side is truncated:
    - Compute answers for a and b via kind-dispatched proc_apply /
      bridge_apply over qlen bytes, exactly as the existing guards
      do.
    - Byte-compare over qlen; if any byte differs:
      - Emit `INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer beyond top two; WITHHOLD AMBIGUOUS\n`
      - set32(res,0,-2); set32(res,4,-1); return.

Precedence is structural and frozen:
1. The verbatim guard (both em=1, top-two) fires first, unchanged.
2. The top-two truncated guards (verbatim-vs-truncated, both-truncated
   top-two) fire second, unchanged, with their exact diagnostic texts.
3. The R8 all-pairs both-truncated guard fires third, unchanged, with
   its exact diagnostic text.
4. The R9 all-pairs verbatim-vs-truncated guard fires fourth, only if
   the earlier guards did not, with its NEW diagnostic text.
5. The gap==0 tie check fires last, unchanged.

Pair-class exclusivity (by construction): a pair is checked by R8 iff
em=0 on both sides; by R9 iff em=1 on exactly one side and the em=0
side is truncated. No pair is checked by both. A pair with em=1 on
both sides beyond the top two is checked by neither (disclosed
boundary, see below).

R9 is applied IDENTICALLY in `unified_learn.zag` and
`intent_learn.zag`. Faithfulness invariant (frozen): all 8 intent
functions remain byte-identical between the two files, verified by
per-function extraction and cmp.

## Frozen methodology

1. This prereg committed alone before any implementation edit, build,
   or run. Commit order verified by `git merge-base --is-ancestor`.
2. Implementation: identical R9 edits in both .zag files.
3. Harness: iu7_verify.zag = mechanism region of the NEW
   unified_learn.zag (everything before `fn main`), cmp-verified
   byte-identical; only main() replaced with the K-IU7-1..K-IU7-4
   kill-bar tests above.
4. Raw evidence: IU7_VERIFY_RAW.txt (md5 recorded, 3/3 byte-identical),
   plus fresh 20/20 and 10/10 suite outputs with md5s.
5. Pure Zag throughout: prereg, implementation, harness, builds, runs,
   greps, md5, cmp. No Python at any stage.
6. Toolchain: znc 2026.07.0-dev (edition 2026), pinned.
7. Only researcher-owned paths staged. No em dashes in loop docs.

## Falsification criteria

- K-IU7-1 yields kind != -2, or kind=-2 with a top-two-only diagnostic
  text -> R9 insufficient -> KILLED.
- Any K-IU7-2 fixture yields the NEW diagnostic text instead of its
  frozen top-two/R8 text -> precedence broken -> KILLED.
- Any K-IU6 bar breaks -> regression -> KILLED (the bar stands; the
  repair is narrowed, never the bar).
- 20/20 or 10/10 md5 differs from the frozen hashes -> silent behavior
  change -> KILLED.

## Boundaries (frozen, disclosed)

- The R9 guard carries the same precision cost as R6/R8: truncated
  records whose procedures merely generalize differently will withhold
  with an honest "POSSIBLE" diagnostic even when the unrecorded
  training pairs do not contradict. The diagnostic says POSSIBLE, not
  CERTAIN. This is disclosed, not a bug.
- The guard is O(ncand^2) in the worst case; ncand is bounded by
  PROC_MAX+BR_MAX (small). No performance claim.
- A both-verbatim (em=1 on both sides) disagreement beyond the top two
  remains out of scope: the IU3 verbatim guard is still top-two-only.
  This is the next disclosed boundary for a future lane.
- The R9 pair check fires only when the em=0 side is truncated; an
  em=1 vs em=0 non-truncated pair is out of scope (same as R4/R5).
- Classification: bounded L2 integration repair. Not L3.
