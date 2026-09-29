# PREREG: H-INTENT-UNIFIED5 Red Team (FROZEN)

## Mission

Independently attack H-INTENT-UNIFIED5. Assume the repair claim is false.
H-INTENT-UNIFIED5 SURVIVES per IU5_RESULT.md: R6 both-truncated guard,
R7 16-char extraction cap, all frozen bars PASS, 3/3 deterministic.

## Target

Committed `unified_learn.zag` (and `intent_learn.zag`) on branch
`tnn-native-lab`. Harness = mechanism region copied byte-verbatim
(cmp-verified) plus attack-only `main()`. Pure Zag. No Python.

## Attack X-IU5-1: third truncation anchor

### Hypothesis

The R6 both-truncated guard examines only the top two ranked candidates
(`top`, `second`). A genuine truncated-vs-truncated contradiction between
the winner and a THIRD-ranked truncated record is silently resolved by the
score gap. This is the same hazard class as X-IU4-1a (which R6 claims to
close "at the mechanism level"), reached via a third anchor.

### Fixture (fresh W, learn order: proc, bridge-C1, bridge-C2)

- C3 = proc, 17 reverse pairs (3-char), 17th unrecorded:
  `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
  Direct discovery -> reverse proc. Record: 16 inputs, true npairs=17
  (truncated). tlen=3.
- C1 = bridge, 17 pairs (3-char), 17th unrecorded:
  `xbc>xxx;xde>xxx;xfg>xxx;xhi>xxx;xjk>xxx;xlm>xxx;xno>xxx;xpq>xxx;qab>baq;wab>baw;eab>bae;rab>bar;tab>bat;yab>bay;uab>bau;xab>xxx`
  Bridge learns IF input[0]=='x' THEN emit-input[0]x3 ELSE reverse.
  Record: 16 inputs, true npairs=17 (truncated). tlen=3.
- C2 = bridge, 17 pairs (first 16 are 4-char, 17th is `xab>xxx`):
  `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xopq>xxx;xrst>xxx;xuvw>xxx;qbcd>dcbq;wbcd>dcbw;ebcd>dcbe;rbcd>dcbr;tbcd>dcbt;ybcd>dcby;ubcd>dcbu;ibcd>dcbi;xab>xxx`
  Bridge learns IF input[0]=='x' THEN emit-input[0]x3 ELSE reverse.
  Record: 16 inputs, true npairs=17 (truncated). in_lens mixed (16x4+1x3)
  so tlen=-1.

Query: `xab` (qlen=3).

### Predicted mechanism behavior (pre-execution)

- C3: em=0 (xab not in recorded 16), lm=1 (tlen=3=qlen), score=10000.
  proc_apply(xab)=`bax`.
- C1: em=0, cf=1 (xab[0]=='x'), lm=1, score=30000. bridge_apply=`xxx`.
- C2: em=0, cf=1, lm=0 (tlen=-1), score=20000. bridge_apply=`xxx`.
- Ranking: top=C1 (30000), second=C2 (20000). Guard: em=0 both,
  trunc=1 both -> check=1, both_trunc=1. Answers `xxx` vs `xxx` agree
  -> fall through. gap=10000 -> kind=1 (bridge), answer `xxx`.
  No TRUNCATED-CONFLICT-POSSIBLE diagnostic.
- Genuineness: C3's training line contained `xab>bax` as its 17th pair;
  C1's training line contained `xab>xxx` as its 17th pair. Direct
  application confirms proc_apply(C3,xab)=`bax` vs
  bridge_apply(C1,xab)=`xxx`: disagree. Both records truncated,
  em=0 on the query. This is exactly the X-IU4-1a configuration with
  the conflicting record ranked third.

### Kill criterion

SUCCEEDS iff: the decision is decisive (kind>=0) with NO
TRUNCATED-CONFLICT-POSSIBLE diagnostic, while direct application shows
a third truncated record (em=0) genuinely disagreeing with the winner
(truncated, em=0) on the query. Verdict on success: H-INTENT-UNIFIED5
DOWNGRADED (the R6 coverage generalization is top-two-only; the frozen
claim "X-IU4-1a closed at the mechanism level" is overstated; K-IU5-1's
literal fixture still passes, so not killed).

FAIL iff: kind=-2 with the both-truncated diagnostic (guard somehow
reaches the third anchor), or the fixture does not set up as predicted
(then the attack is redesigned or dropped with disclosure).

## Attack X-IU5-2: 16/17-char extraction boundary

### Hypothesis

R7 excludes pairs with `out_len > 16`. Off-by-one or a missed path could
panic on 17, wrongly exclude 16, or silently accept 17.

### Fixtures (fresh W each)

- B1: `abcdefghijklmnop>ponmlkjihgfedcba` (16-char reverse; each output
  char appears exactly once in input, so pextract succeeds with sl=16).
  Expect: direct discovery -> proc slot (rc 0..15), NO honest-cap
  diagnostic, exit 0. Then query `abcdefghijklmnop` -> `ponmlkjihgfedcba`
  (seqbase slot integrity end-to-end).
- B2: `abcdefghijklmnopq>qponmlkjihgfedcba` (17-char reverse).
  Expect: honest-cap diagnostic `exceeds 16-char extraction capacity`
  exactly once, rc=-1 (ULEARN FAIL), exit 0, no panic.
- B3: `abcdefghijklmnop>ponmlkjihgfedcba;abcdefghijklmnopq>qponmlkjihgfedcba`
  (one 16-char + one 17-char). Expect: exactly one honest-cap
  diagnostic (for pair 1), rc=-1, exit 0, no panic.
- B4 (audit): grep the committed source for all `pextract(` call sites
  and all `sq`-style 64-byte buffers; verify every write path is
  dominated by the R7 `out_len>16` check or a `<=16` bound.

### Kill criterion

SUCCEEDS iff: B1 panics or is wrongly excluded, B2/B3 panic or silently
accept (rc>=0 with no diagnostic), or the audit finds a length-dependent
write not dominated by the cap. Verdict on success: KILLED (R7
insufficient) or DOWNGRADED (diagnostic gap), per severity.
FAIL iff all fixtures behave exactly as specified.

## Attack X-IU5-3: agreement fall-through

### Hypothesis

R6 falls through when the top two truncated candidates agree. Agreement
on the query means no observable conflict between them (proc_apply writes
exactly qlen bytes, so the qlen-byte comparison is complete). A "hidden"
conflict would have to live in the unrecorded tails, which no
observation-only guard can see (same underdetermination class as
X-RV5-1). This attack verifies the guard's agreement logic is sound for
all OBSERVABLE conflicts and documents the unobservable-tail boundary.

### Fixture

P = proc, 16 reverse pairs (3-char, recorded) + 17th `xab>bax`
unrecorded outlier is NOT used here; instead: P's 16 recorded pairs all
`x..>xxx`-style are impossible for direct (conditional). Construction:
P = direct const-`xxx` proc from 17 identical pairs
`xab>xxx` x17? No: identical pairs, direct discovery finds const.
Simpler observable test: two truncated candidates that agree because
both procedures genuinely compute the same answer, plus a tail-outlier
variant to confirm unobservability:
- P: 17 pairs `abc>xxx;def>xxx;...` (16 recorded, all ->xxx) + 17th
  `xab>xxx`. Direct -> const-xxx. Record truncated, em(xab)=0.
- B: 17 pairs x-rule -> `xxx` on xab (same as X-IU5-1 C1 but WITHOUT a
  conflicting third record).
Query `xab`: both give `xxx`, agree -> fall through -> decisive `xxx`.
No observable conflict exists; the decision is correct.

Tail-outlier variant (boundary documentation, not a kill attempt):
P2: 16 recorded reverse pairs + unrecorded 17th `xab>QQQ` (outlier,
inconsistent with reverse). P2 learns reverse, gives `bax` on xab.
B2: x-rule bridge giving `xxx` on xab, unrecorded 17th `xab>QQQ`.
Query xab: `bax` vs `xxx` disagree -> guard withholds (safe direction).
This confirms the mechanism cannot be MADE to agree-hide here; the only
agreement-hides-conflict cases are unobservable-tail cases no guard can
catch.

### Kill criterion

SUCCEEDS iff an OBSERVABLE genuine conflict (both records truncated,
em=0, direct application disagrees) is resolved decisively via the
agreement fall-through. Expected: FAIL (no such case constructible;
agreement implies no observable conflict). A FAIL here is an honest
negative and supports the guard's agreement logic.

## Attack X-IU5-4: regression

### Fixtures (exact, from IU5 prereg)

- K-IU5-1 both orders -> kind=-2 with both-truncated diagnostic.
- K-IU5-2 (two 20-char pairs) -> honest-cap x2, ULEARN FAIL, no panic.
- K-IU4-1 (verbatim-vs-truncated) -> kind=-2 with UNCHANGED diagnostic
  `verbatim candidate meets truncated record with different answer`.
- Rebuild committed `iu5_verify.zag` -> output md5 must equal frozen
  `24817621d9c6a137acebef23c7ab501d`.
- Rebuild committed `unified_learn.zag` main -> 20/20, md5 must equal
  frozen `904de9f83a2873c7a8862b71804a9065`.
- Rebuild committed `intent_learn.zag` main -> 10/10, md5 must equal
  frozen `98315faec8faea24e75533892c0b240d`.
- Grep: R7 honest-cap code present and identical in both .zag files.

### Kill criterion

SUCCEEDS iff any frozen bar breaks or any md5 differs. Verdict:
KILLED (regression). FAIL iff all reproduce exactly.

## Methodology

1. This prereg committed alone before any attack fixture is written,
   built, or run. Commit order verified by `git merge-base
   --is-ancestor`.
2. Harness: `iu5_adv.zag` = lines 1..1415 of committed
   `unified_learn.zag` (mechanism region, cmp-verified byte-identical)
   plus attack-only main(). Builds in /tmp only, never committed.
3. Each attack run 3x, byte-identical (cmp/md5).
4. Pure Zag throughout. No Python at any stage.
5. Only adversary-owned paths staged: `iu5_adversary/PREREG_IU5_ADV.md`
   (this file, already committed), `iu5_adversary/iu5_adv.zag`,
   `iu5_adversary/IU5_ADV_RESULT.md`,
   `iu5_adversary/IU5_ADV_RAW.txt`.

## Verdict rules (frozen)

- X-IU5-1 SUCCEEDS -> H-INTENT-UNIFIED5 DOWNGRADED (not killed;
  K-IU5-1 literal fixture unaffected; claim narrowed to top-two).
- X-IU5-2 SUCCEEDS -> KILLED or DOWNGRADED per severity.
- X-IU5-3 SUCCEEDS -> KILLED (would break the guard's soundness claim).
  Expected FAIL (honest negative).
- X-IU5-4 SUCCEEDS -> KILLED (regression).
- If all four FAIL -> H-INTENT-UNIFIED5 SURVIVES this red team.
