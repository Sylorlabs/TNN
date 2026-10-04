# PREREG: H-INTENT-UNIFIED8 Repair (FROZEN)

## Hypothesis

H-INTENT-UNIFIED8 closes the H-INTENT-UNIFIED7 red-team boundary B1
(both-verbatim disagreement beyond the top two) at the mechanism
level.

B1, stated exactly as disclosed in IU7_RESULT.md and confirmed
untested by the IU7 red team (X-IU7-1 SETUP-FAIL, no conclusion):
a both-verbatim (em=1 on both sides) disagreement beyond the top
two is out of scope; the IU3 verbatim guard is top-two-only. The
IU7 red team proposed a valid retry fixture (input-character-
composable: `xab>bax;abcd>dcba`, reverse program, `xab` recorded
so em=1, mixed lengths so lm=0, expected score 40000); this prereg
adopts that fixture as K-IU8-1a and extends it to rank 4 as
K-IU8-1b.

The B1 hazard, stated concretely: V1 (proc, em=1, answer `xxx`,
score 50000) ranked first, V2 (proc, em=1, answer `xxx`, score
40000) ranked second, V3 (proc, em=1, answer `bax`, score 40000)
ranked third. The verbatim guard sees top-two agreement and falls
through. The top-two truncated guards need em=1 on exactly one
side or em=0 on both sides; the top two are em=1 on both sides,
so neither fires. R8 skips every pair with an em=1 side. R9 needs
em=1 on exactly one side of the pair; every pair here is em=1 on
both sides, so no pair is compared. The genuine recorded-data
contradiction (`xab>bax` in V3's recorded evidence vs `xab>xxx`
in V1's recorded evidence) is silently resolved via ranking:
kind=0, answer `xxx`. The training data genuinely contradicts
itself and no guard sees it.

The repair extends the verbatim check pairwise over ALL
candidates, regardless of rank: for any unordered pair (a,b)
where em=1 on both sides, compare kind-dispatched answers over
qlen bytes; on any disagreement, WITHHOLD AMBIGUOUS with a NEW
explicit diagnostic. This is a minimal, faithful extension of the
R4/R5/R8/R9 guard family, symmetric with R8 (all-pairs
both-truncated) and R9 (all-pairs verbatim-vs-truncated).
Classification target: bounded L2 integration repair. No L3
claimed.

## Frozen kill bars

Setup-validity rule (frozen): every K-IU8 bar first checks its
learn preconditions via the `iu8_show` helper (prints kind, slot,
em, true npairs, and the applied answer per learned candidate).
If any learn fails (rc<0) or any candidate is not a proc (kind=0)
with em=1 where the bar requires it, the bar reports SETUP-FAIL:
no conclusion, NOT counted as a pass. Post-hoc fixture tuning is
forbidden.

### K-IU8-1a: B1 closed at rank 3 (red-team-proposed fixture)

Fixture (exact):

- V1 = proc: `xab>xxx;xbc>xxx;xde>xxx`
  (constant-0 program; `xab` recorded; uniform len 3; em=1, lm=1;
  expected score 50000, answer `xxx`)
- V2 = proc: `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`
  (constant-0 program; `xab` recorded; mixed lengths, tlen=-1;
  em=1, lm=0; expected score 40000, answer `xxx`)
- V3 = proc: `xab>bax;abcd>dcba`
  (reverse program n-1-k, N-referencing; `xab` recorded; mixed
  lengths, tlen=-1; em=1, lm=0; expected score 40000, answer
  `bax`)

Learn order (fresh W): V1, then V2, then V3.
Query: `xab` (qlen=3).

Expected arrangement: top=V1 (50000), second=V2 (40000, learned
before V3 so strict selection keeps it second on the tie), V3
(40000) ranked third. All three em=1.

PASS iff: kind=-2 AND the K-IU8-1a raw section contains the NEW
R10 diagnostic
`INTENT VERBATIM-CONFLICT: verbatim candidates disagree beyond top two; WITHHOLD AMBIGUOUS`
exactly once, AND no other guard diagnostic text
(`top two candidates both have exact_match=1 but disagree`,
`TRUNCATED-CONFLICT-POSSIBLE`) appears in the section.

FAIL: kind>=0 (the B1 silent resolution), kind=-2 with a
top-two-only or truncated diagnostic (wrong guard fired), or a
silent resolution.

### K-IU8-1b: B1 closed at rank 4 (all-pairs, not rank-limited)

Fixture (exact):

- V1, V2 as in K-IU8-1a.
- V3 = proc: `xab>xxx;xbcd>xxx;xdef>xxx;xfgh>xxx`
  (constant-0 program; `xab` recorded; mixed lengths, tlen=-1;
  em=1, lm=0; expected score 40000, answer `xxx`)
- V4 = proc: `xab>bax;abcd>dcba` (as K-IU8-1a V3; expected score
  40000, answer `bax`)

Learn order (fresh W): V1, V2, V3, then V4.
Query: `xab`.

Expected arrangement: top=V1 (50000), second=V2 (40000),
V3 (40000) third, V4 (40000) fourth. All four em=1. Answers
xxx, xxx, xxx, bax.

PASS iff: kind=-2 AND the NEW R10 diagnostic appears exactly
once in the K-IU8-1b section, AND no other guard diagnostic
appears in the section.

FAIL: kind>=0, or kind=-2 with a wrong diagnostic.

### K-IU8-2: precedence preserved (no shadowing, exact texts)

Four fixtures, each on fresh W, each asserting kind=-2 AND the
exact frozen diagnostic text (the UNCHANGED text from earlier
lanes), AND that the NEW R10 diagnostic appears zero times in
the section:

(a) K-IU7-2a top-two both-truncated (proc-first):
    Proc learn: `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
    Bridge learn: `xcd>xxx;xef>xxx;xgh>xxx;xij>xxx;xkl>xxx;xmn>xxx;xop>xxx;xqr>xxx;qab>baq;wab>baw;eab>bae;rab>bar;tab>bat;yab>bay;uab>bau;iab>bai;xab>xxx`
    Query: `xab`. Exact text required:
    `INTENT TRUNCATED-CONFLICT-POSSIBLE: both records truncated with different answers; WITHHOLD AMBIGUOUS`

(b) K-IU7-2b top-two verbatim-vs-truncated:
    Proc learn: `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
    Bridge learn: `xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee`
    Query: `xab`. Exact text required:
    `INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer; WITHHOLD AMBIGUOUS`

(c) K-IU7-2c R8-only four-truncated:
    C3 proc: `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
    C1 bridge: `xbc>xxx;xde>xxx;xfg>xxx;xhi>xxx;xjk>xxx;xlm>xxx;xno>xxx;xpq>xxx;qab>baq;wab>baw;eab>bae;rab>bar;tab>bat;yab>bay;uab>bau;iab>bai;xab>xxx`
    C2 bridge: `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xopq>xxx;xrst>xxx;xuvw>xxx;qbcd>dcbq;wbcd>dcbw;ebcd>dcbe;rbcd>dcbr;tbcd>dcbt;ybcd>dcby;ubcd>dcbu;ibcd>dcbi;xab>xxx`
    Query: `xab`. Exact text required:
    `INTENT TRUNCATED-CONFLICT-POSSIBLE: truncated candidates disagree beyond top two; WITHHOLD AMBIGUOUS`

(d) K-IU6-3d in-cap verbatim conflict (top-two verbatim guard
    must still fire first; R10 must not shadow it):
    Proc learn: `xab>bax;abc>cba`
    Proc learn: `xab>xxx;xcd>xxx`
    Query: `xab`. Exact text required:
    `INTENT VERBATIM-CONFLICT: top two candidates both have exact_match=1 but disagree; WITHHOLD AMBIGUOUS`

FAIL: any other kind, the NEW R10 diagnostic on any of these
fixtures (precedence broken), a wrong frozen text, or a silent
resolution.

### K-IU8-3: no regression (all K-IU7 bars still PASS)

- K-IU7-1 (R9's own fixture: T3 truncated + V1/V2 verbatim
  agreers, query `xab`) -> kind=-2 with the R9 diagnostic
  `verbatim candidate meets truncated record with different answer beyond top two`
  exactly once, and the NEW R10 diagnostic zero times
  (R10 must not fire before R9 on R9's fixture: the only
  both-em=1 pair is (V1,V2), which agrees).
- K-IU7-2a/2b/2c: covered by K-IU8-2a/2b/2c.
- K-IU7-3a: X-IU5-1 third-anchor (3 truncated) -> kind=-2, R8
  diagnostic.
- K-IU7-3b: 16-char extraction cap. Two 20-char reverse pairs ->
  process exits 0 (no panic), rc=-1.
- K-IU7-3c: 129-pair fixture -> rc=-1, WORK honest failure,
  exit 0, no panic.
- K-IU7-3d: in-cap verbatim conflict (`xab>bax;abc>cba` vs
  `xab>xxx;xcd>xxx`) -> kind=-2. (Covered by K-IU8-2d.)
- unified_learn.zag main() -> 20/20, output byte-identical to
  frozen IU4 evidence (md5 904de9f83a2873c7a8862b71804a9065).
- intent_learn.zag main() -> 10/10, output byte-identical to
  frozen IU4 evidence (md5 98315faec8faea24e75533892c0b240d).
- The R10 diagnostic fires zero times across both suites: no
  existing fixture behavior changed.

### K-IU8-4: determinism

iu8_verify binary run 3 times -> byte-identical output.
unified_learn.zag main() run 3 times -> byte-identical.
intent_learn.zag main() run 3 times -> byte-identical.

## Frozen repair specification

### R10: all-pairs both-verbatim guard (B1)

In `intent_winner`, AFTER the R9 all-pairs verbatim-vs-truncated
guard block (the `if(second>=0){...}` containing the iu7_a/iu7_b
loops) and BEFORE the `if(second>=0 && gap==0)` tie check, insert
the all-pairs both-verbatim guard:

For each unordered candidate pair (a,b) with a<b, both ranging
over 0..ncand-1:
- Let em_a = get32(ce,a*4), em_b = get32(ce,b*4).
- If em_a==1 AND em_b==1:
  - Compute answers for a and b via kind-dispatched proc_apply /
    bridge_apply over qlen bytes, exactly as the existing guards
    do (kind from get32(ck,*), index from get32(ci,*)).
  - Byte-compare over qlen; if any byte differs:
    - Emit `INTENT VERBATIM-CONFLICT: verbatim candidates disagree beyond top two; WITHHOLD AMBIGUOUS\n`
    - set32(res,0,-2); set32(res,4,-1); return.

Precedence is structural and frozen:
1. The verbatim guard (both em=1, top-two) fires first, unchanged.
2. The top-two truncated guards (verbatim-vs-truncated,
   both-truncated top-two) fire second, unchanged, with their
   exact diagnostic texts.
3. The R8 all-pairs both-truncated guard fires third, unchanged,
   with its exact diagnostic text.
4. The R9 all-pairs verbatim-vs-truncated guard fires fourth,
   unchanged, with its exact diagnostic text.
5. The R10 all-pairs both-verbatim guard fires fifth, only if the
   earlier guards did not, with its NEW diagnostic text.
6. The gap==0 tie check fires last, unchanged.

Pair-class exclusivity (by construction): a pair is checked by R8
iff em=0 on both sides; by R9 iff em=1 on exactly one side with
the em=0 side truncated; by R10 iff em=1 on both sides. No pair
is checked by two guards. A pair with em=1 on one side and a
non-truncated em=0 record on the other is checked by none
(disclosed boundary B2, unchanged).

R10 is applied IDENTICALLY in `unified_learn.zag` and
`intent_learn.zag`. Faithfulness invariant (frozen): every
`fn intent_*` function remains byte-identical between the two
files, verified by per-function extraction and cmp.

## Frozen methodology

1. This prereg committed alone before any implementation edit,
   build, or run. Commit order verified by
   `git merge-base --is-ancestor`.
2. Implementation: identical R10 edits in both .zag files; no
   other mechanism byte changed (verified by diff: only the R10
   insertion hunks).
3. Harness: iu8_verify.zag = mechanism region of the NEW
   unified_learn.zag (everything before `fn main`),
   cmp-verified byte-identical; helpers t_learn, t_decide,
   iu4_init, build_big_line carried verbatim from iu7_verify.zag;
   new iu8_show helper (prints kind/slot/em/true-npairs/applied
   answer per learned candidate); new K-IU8 test main. No
   mechanism byte altered.
4. Evidence method: compile once to /tmp with the pinned
   toolchain (binaries never committed); execute the binary
   directly 3 times for clean raws (avoids --run analyzer
   warnings on stderr). Raw evidence: IU8_VERIFY_RAW.txt (md5
   recorded, 3/3 byte-identical via cmp), plus fresh 20/20 and
   10/10 suite outputs with md5s.
5. Pure Zag throughout: prereg, implementation, harness, builds,
   runs, greps, md5, cmp. No Python at any stage.
6. Toolchain: znc 2026.07.0-dev (edition 2026), pinned.
7. Only researcher-owned paths staged (pathspec-restricted).
   Concurrent workers' files untouched.
8. No em dashes in loop documentation (byte-verified).

## Falsification criteria

- K-IU8-1a or K-IU8-1b yields kind != -2, or kind=-2 with a
  top-two-only or truncated diagnostic text -> R10 insufficient
  or misfiring -> KILLED.
- Any K-IU8-2 fixture yields the NEW R10 diagnostic instead of
  its frozen text -> precedence broken -> KILLED.
- Any K-IU7 bar breaks -> regression -> KILLED (the bar stands;
  the repair is narrowed, never the bar).
- 20/20 or 10/10 md5 differs from the frozen hashes -> silent
  behavior change -> KILLED.
- Any `fn intent_*` function differs between the two .zag files
  -> faithfulness broken -> KILLED.

## Boundaries (frozen, disclosed)

- The R10 guard carries no POSSIBLE-style precision cost: both
  sides carry verbatim recorded evidence for the exact query, so
  a disagreement is a genuine recorded-data contradiction, not a
  generalization artifact. The diagnostic says VERBATIM-CONFLICT,
  not POSSIBLE.
- The guard is O(ncand^2) in the worst case; ncand is bounded by
  PROC_MAX+BR_MAX (small). No performance claim.
- B2 (em=1 vs em=0 non-truncated pair beyond the top two)
  remains out of scope, red-team-confirmed as real behavior. The
  recorded evidence does not contradict itself there: the em=0
  non-truncated record says "no exact match for this query", so
  the disagreement is a generalization difference, not a
  recorded-data contradiction. Withholding there would trade a
  real precision cost for no recorded-data hazard. This is a
  disclosed design position, not an untested claim.
- B3 (POSSIBLE-diagnostic precision cost of the truncated
  guards) is untouched by R10 and stands as disclosed.
- The procedure store's programs copy input characters by index
  (`out[k]=inp[peval(prog,k,n)]`); a constant output is
  unlearnable unless some input character matches at a
  program-expressible index. This bounded the fixture design
  (the IU7 red team's X-IU7-1 SETUP-FAIL) and is documented as a
  mechanism property, not repaired here.
- Classification: bounded L2 integration repair. Not L3.
