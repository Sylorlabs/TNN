# PREREG: H-INTENT-UNIFIED6 Repair (FROZEN)

## Hypothesis

H-INTENT-UNIFIED6 closes the H-INTENT-UNIFIED5 red-team downgrade at the
mechanism level:

- X-IU5-1: third truncation anchor. Three truncated (true npairs=17)
  candidates with em=0: C1 (bridge, score 30000, answer `xxx`), C2
  (bridge, score 20000, answer `xxx`), C3 (proc, score 10000, answer
  `bax`). The R6 both-truncated guard compares only top (C1) vs second
  (C2); answers agree (`xxx` vs `xxx`) so it falls through. The genuine
  C3/C1 contradiction (`bax` vs `xxx`) is silently resolved via ranking.
  The frozen IU5 claim "conflict detection is verbatim-anchored AND
  both-truncated-anchored (no other anchor)" is overstated: the anchor
  set is top-two-only.

The repair extends the both-truncated guard pairwise over ALL truncated
candidates with em=0, regardless of rank. If any two such candidates
disagree on the query answer, WITHHOLD AMBIGUOUS with an explicit
diagnostic. This is a minimal, faithful extension of the R6 mechanism.
Classification target: bounded L2 integration repair. No L3 claimed.

## Frozen kill bars

### K-IU6-1: X-IU5-1 closed (all-pairs both-truncated guard)

Fixture (exact, from IU5-ADV X-IU5-1):

- C3 = proc, 17 reverse pairs, `xab>bax` 17th (unrecorded):
  `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
  Direct discovery -> reverse proc, slot 0. Record: 16 inputs, true
  npairs=17 (truncated), tlen=3.
- C1 = bridge, 17 pairs (3-char), `xab>xxx` 17th (unrecorded):
  `xbc>xxx;xde>xxx;xfg>xxx;xhi>xxx;xjk>xxx;xlm>xxx;xno>xxx;xpq>xxx;qab>baq;wab>baw;eab>bae;rab>bar;tab>bat;yab>bay;uab>bau;iab>bai;xab>xxx`
  Bridge learns IF input[0]=='x' THEN emit-input[0]x3 ELSE reverse,
  rule 0. Record: 16 inputs, true npairs=17 (truncated), tlen=3.
- C2 = bridge, 17 pairs (first 16 are 4-char, `xab>xxx` 17th):
  `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xopq>xxx;xrst>xxx;xuvw>xxx;qbcd>dcbq;wbcd>dcbw;ebcd>dcbe;rbcd>dcbr;tbcd>dcbt;ybcd>dcby;ubcd>dcbu;ibcd>dcbi;xab>xxx`
  Bridge learns IF input[0]=='x' THEN emit-input[0]x3 ELSE reverse,
  rule 1. Record: 16 inputs, true npairs=17 (truncated). in_lens mixed
  (16x4+1x3) so tlen=-1.

Learn order (fresh W): proc (C3), then bridge-C1, then bridge-C2.
Query: `xab` (qlen=3).

PASS iff: kind=-2 AND the diagnostic line contains
`TRUNCATED-CONFLICT-POSSIBLE` and indicates the beyond-top-two scope
(exact text frozen in R8 below).

FAIL: kind>=0 (silent resolution), kind=-2 with the top-two-only
diagnostic text (guard did not extend), or no diagnostic.

### K-IU6-2: K-IU5-1a/b still PASS (top-two both-truncated precedence)

Fixture (exact, from PREREG_INTENT_UNIFIED5 K-IU5-1):

- Proc learn: `abc>cba;...;tuv>vut;xab>bax` (17 reverse pairs).
- Bridge learn: `xcd>xxx;...;iab>bai;xab>xxx` (17 pairs).
- Query: `xab`.

Two learn orders (proc-first, bridge-first), each on fresh W.

PASS iff in BOTH orders: kind=-2 AND the diagnostic line reads EXACTLY
`INTENT TRUNCATED-CONFLICT-POSSIBLE: both records truncated with different answers; WITHHOLD AMBIGUOUS`
(the UNCHANGED top-two diagnostic text). The top-two guard must fire
first and keep its exact diagnostic; the all-pairs guard must not
shadow or alter it.

FAIL: any other kind, the new beyond-top-two diagnostic text on this
fixture, or a silent resolution.

### K-IU6-3: no regression (all K-IU5 bars still PASS)

- K-IU5-2: 16-char extraction cap. Two 20-char reverse pairs ->
  process exits 0 (no panic), honest-cap diagnostic appears, rc=-1.
- K-IU4-1 (via K-IU5-3): proc 17-pair + bridge 5-pair; query `xab` ->
  kind=-2 with the UNCHANGED diagnostic
  `INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer; WITHHOLD AMBIGUOUS`.
  The verbatim-vs-truncated branch keeps precedence.
- K-IU4-2 (via K-IU5-3): 129-pair fixture -> rc=-1, WORK honest failure,
  exit 0, no panic.
- K-IU4-3 (via K-IU5-3): unified_learn.zag main() -> 20/20, output
  byte-identical to frozen IU4 evidence (md5
  904de9f83a2873c7a8862b71804a9065). intent_learn.zag main() -> 10/10,
  output byte-identical to frozen IU4 evidence (md5
  98315faec8faea24e75533892c0b240d).

### K-IU6-4: determinism

iu6_verify binary run 3 times -> byte-identical output.
unified_learn.zag main() run 3 times -> byte-identical.
intent_learn.zag main() run 3 times -> byte-identical.

## Frozen repair specification

### R8: all-pairs both-truncated guard (X-IU5-1)

In `intent_winner`, AFTER the existing truncated-conflict guard block
(the `if(second>=0){...}` containing the verbatim-vs-truncated and
top-two both-truncated branches) and BEFORE the `if(second>=0 &&
gap==0)` tie check, insert the all-pairs guard:

For each unordered candidate pair (a,b) with a<b, both ranging over
0..ncand-1:
- If get32(ce,a*4)==0 AND get32(ce,b*4)==0 (both em=0):
  - Determine truncation for a and b via intent_proc_base /
    intent_br_base (kind-dispatched on get32(ck,*4)), checking
    get32(W,rec+8)>16, exactly as the existing guard does.
  - If both truncated:
    - Compute answers via kind-dispatched proc_apply / bridge_apply
      over qlen bytes, exactly as the existing guard does.
    - Byte-compare over qlen; if any byte differs:
      - Emit `INTENT TRUNCATED-CONFLICT-POSSIBLE: truncated candidates disagree beyond top two; WITHHOLD AMBIGUOUS\n`
      - set32(res,0,-2); set32(res,4,-1); return.

Precedence is structural and frozen:
1. The verbatim guard (both em=1) fires first, unchanged.
2. The top-two truncated guard (verbatim-vs-truncated, both-truncated
   top-two) fires second, unchanged, with its exact diagnostic texts.
3. The all-pairs guard fires third, only if the top-two guards did not.
   On the K-IU5-1 fixture the top-two both-truncated guard fires, so the
   all-pairs guard never runs there; K-IU6-2 verifies the exact text.
4. The gap==0 tie check fires last, unchanged.

The all-pairs guard does NOT extend the verbatim-meets-truncated
branches (em=1 on one side); those remain top-two-only, out of scope
for this repair. The guard does not fire on agreement (X-IU5-3 honest
negative preserved: two truncated em=0 candidates agreeing on the
query fall through).

R8 is applied IDENTICALLY in `unified_learn.zag` and
`intent_learn.zag`. Faithfulness invariant (frozen): all 8 intent
functions remain byte-identical between the two files, verified by
per-function extraction and cmp.

## Frozen methodology

1. This prereg committed alone before any implementation edit, build,
   or run. Commit order verified by `git merge-base --is-ancestor`.
2. Implementation: identical R8 edits in both .zag files.
3. Harness: iu6_verify.zag = mechanism region of the NEW
   unified_learn.zag (everything before `fn main`), cmp-verified
   byte-identical; only main() replaced with the K-IU6-1..K-IU6-3
   kill-bar tests above.
4. Raw evidence: IU6_VERIFY_RAW.txt (md5 recorded, 3/3 byte-identical),
   plus fresh 20/20 and 10/10 suite outputs with md5s.
5. Pure Zag throughout: prereg, implementation, harness, builds, runs,
   greps, md5, cmp. No Python at any stage.
6. Toolchain: znc 2026.07.0-dev (edition 2026), pinned.
7. Only researcher-owned paths staged. No em dashes in loop docs.

## Falsification criteria

- K-IU6-1 yields kind != -2, or kind=-2 with the top-two diagnostic
  text -> R8 insufficient -> KILLED.
- K-IU6-2 yields the new diagnostic text instead of the frozen top-two
  text -> precedence broken -> KILLED.
- Any K-IU5 bar breaks -> regression -> KILLED (the bar stands; the
  repair is narrowed, never the bar).
- 20/20 or 10/10 md5 differs from the frozen hashes -> silent behavior
  change -> KILLED.

## Boundaries (frozen, disclosed)

- The all-pairs guard carries the same precision cost as R6: truncated
  records whose procedures merely generalize differently will withhold
  with an honest "POSSIBLE" diagnostic even when the unrecorded
  training pairs do not contradict. The diagnostic says POSSIBLE, not
  CERTAIN. This is disclosed, not a bug.
- The guard is O(ncand^2) in the worst case; ncand is bounded by
  PROC_MAX+BR_MAX (small). No performance claim.
- The verbatim-meets-truncated branches remain top-two-only; a third-
  anchor verbatim-vs-truncated conflict is out of scope.
- Classification: bounded L2 integration repair. Not L3.
