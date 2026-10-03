# IU6-ADV RESULT: H-INTENT-UNIFIED6 Red Team

## Verdict: H-INTENT-UNIFIED6 SURVIVES this red team

Three of four attacks fail (mechanism holds). One attack succeeds but
confirms the explicitly disclosed out-of-scope boundary; per the frozen
prereg and the H-CAUSAL-UNIFIED4 precedent, confirming a disclosed
boundary that does not falsify the headline claim does not change the
verdict.

## Lineage

- Prereg `iu6_adversary/PREREG_IU6_ADV.md` committed alone as
  `055e1982e` before any attack code was written, built, or run.
  `git merge-base --is-ancestor 055e1982e HEAD` verified.
- Harness: `iu6_adversary/iu6_adv.zag` = lines 1-1471 of the COMMITTED
  `unified_learn.zag` (mechanism region, everything before `fn main`),
  cmp-verified byte-identical against `git show HEAD:...`, plus
  test helpers (`t_learn`, `t_decide`, `iu4_init`, `apply_str`,
  `build_big_line`) plus attack-only `main()`. No mechanism edits.
  Builds in /tmp/iu6adv only; the binary was never committed.
- Raw evidence: `iu6_adversary/IU6_ADV_RAW.txt` (md5
  `e027a99fdc1b8d1da2ca797bee1e1bcc`, 3/3 byte-identical, exit 0).
- Toolchain: znc 2026.07.0-dev (edition 2026), pinned. Pure Zag
  throughout: prereg, harness, builds, runs, greps, md5, cmp. No
  Python at any stage.

## X-IU6-1: fourth-anchor both-truncated dissenter -- FAILS (R8 holds)

### Fixture (fresh W; learn order P_dissent, P_agree, B1, B2)

- P_dissent: proc (reverse), 17 pairs, `xab>bax` 17th (unrecorded).
  npairs=17, em=0. Direct apply: `bax`.
- P_agree: proc (emit-input[0]x3), 17 x-prefixed pairs, `xab>xxx`
  17th (unrecorded). npairs=17, em=0. Direct apply: `xxx`.
- B1: bridge (x-rule), 17 pairs (3-char), `xab>xxx` 17th. npairs=17,
  em=0. Score 30000. Direct apply: `xxx`.
- B2: bridge (x-rule), 17 pairs (16x4-char + `xab>xxx`), `xab>xxx`
  17th. npairs=17, em=0. Score 20000. Direct apply: `xxx`.

Query: `xab` (qlen=3).

### Observed (3/3 identical)

```
T GENUINE npairs: PD=17 PA=17 B1=17 B2=17 em(xab): PD=0 PA=0 B1=0 B2=0
T APPLY tag=X1-PD-direct [bax]
T APPLY tag=X1-PA-direct [xxx]
T APPLY tag=X1-B1-direct [xxx]
T APPLY tag=X1-B2-direct [xxx]
INTENT query [xab] qlen=3
  cand kind=proc slot=0 exact_match=0 len_match=1 train_len=3 seq=0 cond_fire=0 score=10000
  cand kind=proc slot=1 exact_match=0 len_match=1 train_len=3 seq=1 cond_fire=0 score=10000
  cand kind=bridge slot=0 exact_match=0 len_match=1 train_len=3 seq=2 cond_fire=1 score=30000
  cand kind=bridge slot=1 exact_match=0 len_match=0 train_len=-1 seq=3 cond_fire=1 score=20000
INTENT TRUNCATED-CONFLICT-POSSIBLE: truncated candidates disagree beyond top two; WITHHOLD AMBIGUOUS
T DECIDE tag=X-IU6-1 kind=-2 slot=-1 gap=10000
X-IU6-1 VERDICT: kind=-2 WITHHOLD -> attack FAILS (R8 holds)
```

### Analysis

Four truncated (em=0) candidates. The top two (B1=30000, B2=20000)
agree on `xxx`; the top-two both-truncated guard falls through. The
dissenter (P_dissent, `bax`, score 10000, tied for third) is not in the
top two. R8's all-pairs comparison finds the disagreeing pair and
withholds with the exact "beyond top two" diagnostic. The genuine
P_dissent/B1 tail contradiction (`xab>bax` vs `xab>xxx`, both pair 17
unrecorded) is caught regardless of rank. R8 is rank-agnostic as
claimed.

## X-IU6-2: verbatim third-anchor -- SUCCEEDS (boundary CONFIRMED)

### Fixture (fresh W; learn order T3, V1, V2)

- T3: proc (reverse), 17 pairs, `xab>bax` 17th (unrecorded).
  npairs=17 (truncated), em=0. Direct apply: `bax`.
- V1: proc (direct discovery), 3 pairs (`xab>xxx;xbc>xxx;xde>xxx`),
  `xab>xxx` RECORDED. npairs=3 (verbatim, not truncated), em=1.
  Direct apply: `xxx`. Score 50000 (em=1, lm=1).
- V2: proc (direct discovery), 6 pairs
  (`xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`),
  `xab>xxx` RECORDED. npairs=6 (verbatim), em=1. Direct apply: `xxx`.
  Score 40000 (em=1, lm=0, tlen=-1 mixed).

Note: V1/V2 learned as procs via direct discovery, not bridges. This
does not matter; the attack needs em=1 (verbatim), not a specific
kind.

Query: `xab` (qlen=3).

### Observed (3/3 identical)

```
T GENUINE npairs: T3=17 V1=3 V2=6 em(xab): T3=0 V1=1 V2=1
T APPLY tag=X2-T3-direct [bax]
T APPLY tag=X2-V1-direct [xxx]
T APPLY tag=X2-V2-direct [xxx]
INTENT query [xab] qlen=3
  cand kind=proc slot=0 exact_match=0 len_match=1 train_len=3 seq=0 cond_fire=0 score=10000
  cand kind=proc slot=1 exact_match=1 len_match=1 train_len=3 seq=1 cond_fire=0 score=50000
  cand kind=proc slot=2 exact_match=1 len_match=0 train_len=-1 seq=2 cond_fire=0 score=40000
T DECIDE tag=X-IU6-2 kind=0 slot=1 gap=10000 answer=[xxx]
X-IU6-2 VERDICT: kind=0 DECISIVE -> boundary CONFIRMED (disclosed out-of-scope)
```

No `TRUNCATED-CONFLICT` diagnostic. The genuine T3/V1 contradiction
(`xab>bax` in T3's unrecorded tail vs `xab>xxx` in V1's recorded data)
is silently resolved via the top-ranked verbatim candidate.

### Why this does not downgrade H-INTENT-UNIFIED6

1. The frozen IU6 prereg explicitly discloses: "The
   verbatim-meets-truncated branches remain top-two-only; a
   third-anchor verbatim-vs-truncated conflict is out of scope."
   (PREREG_INTENT_UNIFIED6.md, Boundaries; IU6_RESULT.md, Boundaries.)
2. The IU6 headline claim covers "genuine contradictions among ALL
   truncated candidates with em=0, regardless of rank." This attack
   uses verbatim (em=1) anchors; it does not falsify the
   both-truncated claim.
3. Per the H-CAUSAL-UNIFIED4 red-team precedent (X-CV4-1), a
   disclosure does not convert a successful falsification of the
   headline claim into a non-finding; conversely, confirming a
   disclosed boundary that leaves the headline claim intact does not
   change the verdict.

The boundary is real and exploitable (demonstrated above), but it was
disclosed before this red team ran. Verdict: BOUNDARY CONFIRMED, no
downgrade. The parent may choose to open a follow-up repair lane
(H-INTENT-UNIFIED7) for the verbatim anchor set; that is not this red
team's call.

## X-IU6-3: guard shadowing / precedence -- FAILS (no bug)

X-IU6-3a: On the X-IU6-1 fixture (top-two agree, only R8 can fire),
the diagnostic reads EXACTLY:
`INTENT TRUNCATED-CONFLICT-POSSIBLE: truncated candidates disagree beyond top two; WITHHOLD AMBIGUOUS`

X-IU6-3b: On the two-candidate top-two both-truncated fixture
(K-IU6-2a shape: proc 17-pair `xab>bax` + bridge 17-pair `xab>xxx`),
the diagnostic reads EXACTLY:
`INTENT TRUNCATED-CONFLICT-POSSIBLE: both records truncated with different answers; WITHHOLD AMBIGUOUS`

Observed (3/3 identical):
```
T DECIDE tag=X-IU6-3b kind=-2 slot=-1 gap=20000
```

The top-two guard fires first with its unchanged text; R8 does not
shadow it. R8 fires only when the top-two guards fall through, with
its distinct text. Precedence is structural and correct. No
shadowing in either direction.

## X-IU6-4: regression -- FAILS (no silent changes)

Rebuilt from committed sources (`git show HEAD:...`):

- `iu6_verify.zag`: output md5 `a4dad5090897bf0a82c5fddad3e45b57` =
  frozen IU6 hash. 7/7, SURVIVES.
- `unified_learn.zag` main(): 20/20 PASS, md5
  `904de9f83a2873c7a8862b71804a9065` = frozen IU4 hash.
- `intent_learn.zag` main(): 10/10 PASS, md5
  `98315faec8faea24e75533892c0b240d` = frozen IU4 hash.

No md5 differs. No non-determinism (adversary harness 3/3
byte-identical). No silent behavior change.

## Final tally

- X-IU6-1 FAILS (R8 holds at rank 3-4; honest negative).
- X-IU6-2 SUCCEEDS (boundary CONFIRMED; disclosed out-of-scope, no
  verdict change).
- X-IU6-3 FAILS (precedence correct; honest negative).
- X-IU6-4 FAILS (no regression; honest negative).
- **H-INTENT-UNIFIED6 SURVIVES this red team.**

Classification remains: bounded L2 integration repair. Not L3.

## Governance disclosures

1. Prereg `055e1982e` strictly precedes all attack code; verified via
   `git merge-base --is-ancestor`. No amendments.
2. Pure Zag throughout; zero Python at any stage. (The only
   "python" strings in the repo files are in comments stating
   "No Python".)
3. Binaries built in /tmp/iu6adv only, never committed.
4. Only adversary-owned paths staged: `iu6_adversary/PREREG_IU6_ADV.md`
   (already committed), `iu6_adversary/iu6_adv.zag`,
   `iu6_adversary/IU6_ADV_RAW.txt`, `iu6_adversary/IU6_ADV_RESULT.md`.
   Concurrent workers' files untouched (pathspec-restricted staging).
5. No em dashes in loop documentation.
6. No test-answer literals in mechanism regions; the harness's
   mechanism section (lines 1-1471) is byte-identical to the committed
   `unified_learn.zag`; all fixture strings live in the attack-only
   `main()`.
7. X-IU6-2 fixture note: V1/V2 learned as procs (direct discovery),
   not bridges as the prereg anticipated. The kill criterion depends
   only on em=1 (verbatim) vs em=0, not on kind; the observed
   configuration (two verbatim em=1 procs agreeing, one truncated
   em=0 proc dissenting at rank 3) satisfies the prereg's structural
   requirements exactly. The boundary confirmation stands.

## Files (branch `tnn-native-lab`)

- `docs/lab/research-lead/overnight-20260928/iu6_adversary/PREREG_IU6_ADV.md`
  (commit `055e1982e`, prereg alone)
- `docs/lab/research-lead/overnight-20260928/iu6_adversary/iu6_adv.zag`
  (adversary harness)
- `docs/lab/research-lead/overnight-20260928/iu6_adversary/IU6_ADV_RAW.txt`
  (raw evidence, md5 `e027a99fdc1b8d1da2ca797bee1e1bcc`, 3/3 identical)
- `docs/lab/research-lead/overnight-20260928/iu6_adversary/IU6_ADV_RESULT.md`
  (this report)

## Suggested follow-ups for parent

1. Optional H-INTENT-UNIFIED7 repair lane: extend the
   verbatim-vs-truncated guard beyond the top two (the X-IU6-2
   boundary). Suggested kill bar: the X-IU6-2 fixture -> kind=-2.
2. The research paper's H-INTENT-UNIFIED6 section should note the
   X-IU6-2 boundary confirmation (paper lane, not mine).
