# IU5-ADV RESULT: H-INTENT-UNIFIED5 Red Team

## Verdict: H-INTENT-UNIFIED5 DOWNGRADED (not killed)

One of four attacks succeeds. X-IU5-1 demonstrates a genuine
truncated-vs-truncated training-data contradiction silently resolved via
a third-ranked anchor, the same hazard class R6 claims to close "at the
mechanism level". All frozen K-IU5 bars still pass; the repair is
narrowed, not broken.

## Lineage

- Prereg `iu5_adversary/PREREG_IU5_ADV.md` frozen before any attack
  fixture was written, built, or run. Governance note: the prereg file
  was staged by this researcher and swept into a concurrent worker's
  broad-pathspec commit `0b23cd3d8`
  (`0b23cd3d8a1e68524259a5845bb69399c2b19f70`, "Paper:
  H-CAUSAL-UNIFIED4 DOWNGRADED (merge-broadening)"); the committed blob
  is byte-identical to the authored prereg (md5-verified by cmp against
  `git show`). Content frozen; commit message is the other worker's.
  This is recorded, not hidden. `git merge-base --is-ancestor`
  confirms the prereg commit strictly precedes any attack code.
- Harness: `iu5_adversary/iu5_adv.zag` = lines 1..1415 of the committed
  `unified_learn.zag` (mechanism region), cmp-verified byte-identical
  against `git show HEAD:...`, plus attack-only `main()`. Builds in
  /tmp only; the binary was never committed.
- Raw evidence: `iu5_adversary/IU5_ADV_RAW.txt` (md5
  `925fb63b0c9f987116983318c379c97a`, 3/3 byte-identical, exit 0).
- Toolchain: znc 2026.07.0-dev (edition 2026), pinned. Pure Zag
  throughout: prereg, harness, builds, runs, greps, md5, cmp. No
  Python at any stage.

## X-IU5-1: third truncation anchor -- SUCCEEDS (downgrade)

### Fixture (fresh W; learn order proc, bridge-C1, bridge-C2)

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

Query: `xab` (qlen=3).

### Observed (3/3 identical)

```
T GENUINE npairs: C3=17 C1=17 C2=17 em(xab): C3=0 C1=0 C2=0
T APPLY tag=X1-C3-direct [bax]
T APPLY tag=X1-C1-direct [xxx]
T APPLY tag=X1-C2-direct [xxx]
INTENT query [xab] qlen=3
  cand kind=proc slot=0 exact_match=0 len_match=1 train_len=3 seq=0 cond_fire=0 score=10000
  cand kind=bridge slot=0 exact_match=0 len_match=1 train_len=3 seq=1 cond_fire=1 score=30000
  cand kind=bridge slot=1 exact_match=0 len_match=0 train_len=-1 seq=2 cond_fire=1 score=20000
T DECIDE tag=X-IU5-1 kind=1 slot=0 gap=10000 answer=[xxx]
```

No `INTENT TRUNCATED-CONFLICT-POSSIBLE` diagnostic anywhere in the raw
(the single grep hit is the harness's own informational text
"check raw for TRUNCATED-CONFLICT diagnostic").

### Why this is genuine

- C3's training line contained `xab>bax` as its 17th pair; C1's
  training line contained `xab>xxx` as its 17th pair. Both pairs were
  fed to the learner; both fell outside the 16-input record cap.
- Both records carry true npairs=17 (>16, truncated); em(xab)=0 on all
  three records.
- Direct application confirms the contradiction: proc_apply(C3,
  `xab`)=`bax` vs bridge_apply(C1, `xab`)=`xxx`.
- This is exactly the X-IU4-1a configuration (both-truncated, em=0,
  genuine tail contradiction), except the conflicting record is ranked
  third (score 10000) behind an agreeing second (score 20000).
- The R6 guard examines only top (C1) vs second (C2): both truncated,
  em=0, answers `xxx` vs `xxx` agree -> falls through. gap=10000 ->
  decisive kind=1, answer `xxx`. The C3/C1 contradiction is silently
  resolved.

### Causal interpretation

R6 generalized the guard's coverage condition from verbatim-anchored to
both-truncated-anchored, but the guard still only compares the top two
ranked candidates. Any genuine truncated-vs-truncated contradiction in
which an agreeing candidate outranks the conflicting one escapes
detection entirely. The frozen IU5 claim "X-IU4-1a closed at the
mechanism level" and "conflict detection is verbatim-anchored AND
both-truncated-anchored (no other anchor)" overstate the coverage: the
anchor set is top-two-only. This is the same hazard class as X-IU4-1a,
reached through ranking rather than through the both-truncated shape.

### Scope of the downgrade

- K-IU5-1's literal fixture (two candidates) still passes; the R6
  mechanism is intact for the top-two case. Hence DOWNGRADED, not
  killed.
- The narrowed claim: the both-truncated guard covers genuine
  contradictions between the top two ranked candidates only.
- Suggested repair direction (not implemented here): extend the guard
  to pairwise-compare all truncated candidates, or withhold whenever
  any two truncated candidates with em=0 disagree, regardless of rank.

## X-IU5-2: 16/17-char boundary -- FAILS (attack fails; boundary holds)

- B1 (two 16-char reverse pairs): direct discovery -> proc slot 0, NO
  honest-cap diagnostic, both queries return exact reverses. The 16-char
  case flows through cleanly; seqbase slot integrity confirmed
  end-to-end.
- B2 (two 17-char reverse pairs): honest-cap diagnostic exactly twice
  (pair 0 and pair 1), rc=-1 (ULEARN FAIL), exit 0, no panic.
- B3 (one 16-char + one 17-char pair): exactly one honest-cap
  diagnostic (pair 1), rc=-1, exit 0, no panic.
- B4 (audit): exactly one `pextract(` call site per file
  (unified:489, intent:460), each dominated by the R7 `out_len>16`
  guard (unified:479, intent:450). `pextract` writes at most out_len
  i32s; with out_len<=16 the 64-byte `sq` and the 64-byte seqbase slot
  cannot overflow (16*4=64 exactly). No other length-dependent fixed
  buffer exists on the learn path (Step 3 buffers are npairs-sized or
  256-byte dvals). No off-by-one: 16 passes, 17 excluded, both loud.

## X-IU5-3: agreement fall-through -- FAILS (honest negative)

- Fixture: P = direct emit-input[0]x3 proc, 17 x-prefixed pairs,
  `xab>xxx` 17th (record truncated, em=0); B = x-rule bridge, 17 pairs,
  `xab>xxx` 17th (record truncated, em=0). Both procedures genuinely
  compute `xxx` on `xab`.
- Observed: top=B (30000), second=P (10000); guard check=1
  (both-truncated, em=0), answers `xxx` vs `xxx` agree -> fall through;
  kind=1, answer `xxx`, no diagnostic. Correct: no observable conflict
  exists between the candidates.
- proc_apply writes exactly qlen bytes, so the guard's qlen-byte answer
  comparison is complete; agreement on the query means no observable
  contradiction. A "hidden" conflict would have to live in the
  unrecorded tails, which no observation-only guard can see (same
  underdetermination class as X-RV5-1). Documented as a theoretical
  boundary, not a flaw. The guard's agreement logic is sound.

## X-IU5-4: regression -- FAILS (no regression)

- Rebuilt committed `iu5_verify.zag`: output md5
  `24817621d9c6a137acebef23c7ab501d` = frozen IU5 hash. All K-IU5-1a/b,
  K-IU5-2, K-IU5-3a/b/c reproduce.
- Rebuilt committed `unified_learn.zag` main: `20/20`, md5
  `904de9f83a2873c7a8862b71804a9065` = frozen IU4 hash.
- Rebuilt committed `intent_learn.zag` main: `10/10`, md5
  `98315faec8faea24e75533892c0b240d` = frozen IU4 hash.
- R7 honest-cap code present and identical in both .zag files
  (single guard + single diagnostic each).

## Final tally

- X-IU5-1 SUCCEEDS -> DOWNGRADE.
- X-IU5-2 FAILS, X-IU5-3 FAILS, X-IU5-4 FAILS (all honest negatives).
- **H-INTENT-UNIFIED5 DOWNGRADED (not killed).** All frozen K-IU5 bars
  hold; the both-truncated conflict-detection claim is narrowed to
  top-two candidates.

## Governance disclosures

1. Prereg committed before any attack code; ordering verified by
   merge-base --is-ancestor. The prereg file was swept into concurrent
   worker commit `0b23cd3d8`; content verified byte-identical, lineage
   recorded here.
2. Fixture correction disclosed: the prereg's X-IU5-1 C1 fixture text
   listed 16 pairs (missing `iab>bai`) while describing 17; the first
   run exposed C1 as verbatim (em=1, npairs=16) instead of truncated.
   The fixture was corrected to the described 17 pairs before the
   recorded runs; the kill criterion (decisive + no diagnostic +
   genuine third-anchor disagreement) is unchanged. The X-IU5-2 B1/B2
   fixtures were likewise corrected (single-pair lines route-WITHHOLD;
   replaced with two-pair lines; B2's second pair corrected to a true
   17-char pair). All corrections are disclosed here, not hidden.
3. Pure Zag throughout; zero Python at any stage.
4. One `znc build` syntax error during harness setup (used `znc build
   <src> -o <out>`; correct form is `znc <src> -o <out>`). The bad
   invocation produced no binary; no stale-binary execution occurred.
   All committed evidence comes from correctly built binaries.
5. No binaries committed (builds in /tmp/iu5adv only).
6. Only adversary-owned paths staged:
   `iu5_adversary/PREREG_IU5_ADV.md` (already committed via sweep),
   `iu5_adversary/iu5_adv.zag`, `iu5_adversary/IU5_ADV_RESULT.md`,
   `iu5_adversary/IU5_ADV_RAW.txt`. Concurrent workers' files
   untouched (pathspec-restricted staging).
7. Two `.git/index.lock` contentions encountered; waited for live locks
   to clear per standing rules, never removed.
8. No em dashes in loop documentation.
9. No test-answer literals in mechanism regions: the harness's
   mechanism section is byte-identical to the committed
   `unified_learn.zag` lines 1..1415; all fixture strings live in the
   attack-only `main()`.

## Suggested follow-ups for parent

1. Repair lane (H-INTENT-UNIFIED6): extend the both-truncated guard
   beyond the top two (e.g., pairwise over all truncated candidates,
   or withhold on any truncated-candidate disagreement). Suggested
   kill bars: the X-IU5-1 fixture -> kind=-2 with the both-truncated
   diagnostic; K-IU5-1a/b still kind=-2; 20/20 and 10/10 md5s unchanged.
2. The research paper's H-INTENT-UNIFIED5 section needs this downgrade
   entry (paper lane, not mine).
