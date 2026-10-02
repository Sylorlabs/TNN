# H-INTENT-UNIFIED9 RESULT: R10 mixed-kind dispatch + precision audit

Status: **SURVIVES 4/4** (bounded L2 integration test, not L3).
Date: 2026-09-30 UTC.
Toolchain: `znc 2026.07.0-dev (edition 2026)`, binary at
`/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`.

## Lineage

- Prereg: `PREREG_INTENT_UNIFIED9.md`, committed alone as
  `778079959` BEFORE any harness build, compile, or run. Strict
  ancestry verified via `git merge-base --is-ancestor`.
- Harness: `iu9_verify.zag` (mechanism region lines 1-1579
  byte-identical to the committed `unified_learn.zag` at HEAD,
  cmp-verified; helpers t_learn, t_decide, iu4_init, iu8_show carried
  verbatim from the committed `iu8_verify.zag` lines 1580-1698; new
  frozen-bar main). No mechanism byte altered.
- Raw evidence: `IU9_VERIFY_RAW.txt`, md5
  `933077edbb441bdd0d0df163d1f843db`, 3/3 direct binary runs
  byte-identical via cmp, exit 0, zero stderr bytes.
- Mechanism delta: none. This wave tests H-INTENT-UNIFIED8's R10 on
  its last untested dispatch path (named by the IU8 red team) and
  audits precision. The production sources are unchanged.

## What was tested and why

The IU8 red team left one dispatch path untested: R10's kind
dispatch (proc_apply vs bridge_apply) on a mixed bridge/proc pair
BEYOND the top two. X-IU8-2 could not engage it because the induced
bridge earned cf=1 (score 60000) and outranked the procs, so the IU3
top-two guard fired instead. The IU8 builder also recommended a
precision audit of whether R10 over-withholds on agreeing answers
with different internal slots.

## Frozen bars and outcomes

### K-IU9-1: Mixed-kind dispatch beyond top two: PASS

Fixture (fresh W, learn order V1, V2, B; query `xab`):

- V1 (`xab>xxx;xbc>xxx;xde>xxx`): proc, em=1, answer `xxx`, score
  50000.
- V2 (`xab>xxx;xfg>xxx;xhi>xxx`): proc, em=1, answer `xxx`, score
  50000.
- B (`aab>baa;abb>bba;acb>bca;xab>xab;xcb>xcb;xdb>xdb`): bridge.
  Induced IF input[0]==97 THEN reverse ELSE identity, as predicted
  from source analysis. For query `xab`, input[0]=120, ELSE branch:
  cond_fire=0 (cf=0 confirmed in trace), em=1, applied answer `xab`
  (identity), score 50000.

All three scored 50000; tie-break by learn order ranked V1, V2, B.
The top two (V1, V2) agreed on `xxx`, so IU3, R8, and R9 did not
fire. R10 caught the (V1,B) and (V2,B) mixed-kind disagreements.

Observed: kind=-2. Decide section: R10 diagnostic
(`verbatim candidates disagree beyond top two`) exactly once.
IU3-OLD, IU4A, IU4B, R8, R9: zero occurrences. The bridge_apply
dispatch in R10 computed the correct dissenting answer (`xab`) for
the kind=1 candidate.

### K-IU9-2: Precision audit: PASS

Fixture (fresh W, learn order V1, V2, V3; query `xab`):

- V1 (`xab>xxx;xbc>xxx;xde>xxx`): proc, 50000, `xxx`.
- V2 (`xbcd>xxx;...;xab>xxx`, 6 pairs): proc, 40000, `xxx`.
- V3 (`xabcd>xxx;xefgh>xxx;xab>xxx`): proc, 40000, `xxx`.

All three agreed on `xxx` with different internal candidate slots.
Observed: kind=0 (proc winner V1), gap=10000 (not a tie), zero
WITHHOLD diagnostics in the decide section. R10 did not fire on
agreeing answers. No over-withholding.

### K-IU9-3: Regression: PASS

- `unified_learn.zag` main at HEAD: 3/3 runs exit 0, zero stderr,
  output md5 `904de9f83a2873c7a8862b71804a9065` (frozen IU7/IU8
  hash reproduced).
- `intent_learn.zag` main at HEAD: 3/3 runs exit 0, zero stderr,
  output md5 `98315faec8faea24e75533892c0b240d` (frozen IU7/IU8
  hash reproduced).

### K-IU9-4: Determinism: PASS

IU9 harness binary: 3/3 runs byte-identical via cmp, exit 0, zero
stderr bytes.

## Exact-text inventory (decide sections)

K-IU9-1 decide:

- R10-NEW (`verbatim candidates disagree beyond top two`): 1.
- IU3-OLD, IU4A, IU4B, R8, R9: 0.
- KIND-BAD: 0. SETUP-FAIL: 0.

K-IU9-2 decide:

- WITHHOLD diagnostics: 0.
- Winner: kind=0, slot=0, answer `xxx`.

## Failures, boundaries, interpretation

- No bar failed. No setup failure. No panic, no stderr output.
- R10's kind dispatch is now empirically confirmed on all pair
  kinds: proc/proc (IU8 builder), proc/proc beyond top two (IU8
  builder, IU8 red team X-IU8-1/3/4), and mixed bridge/proc beyond
  the top two (this wave, K-IU9-1). The red team's named coverage
  gap is closed.
- Precision holds: R10 withholds only on genuine answer
  disagreement over qlen bytes. Agreeing answers with different
  internal slots do not trigger a withhold (K-IU9-2).
- B2 (em=1 vs em=0 non-truncated beyond the top two) and B3
  (POSSIBLE-diagnostic precision cost) remain untouched and
  undisputed, as in IU8.
- The `gap==0` tie rule is untouched and still last.
- Causal reading: the X-IU8-2 fixture limitation was a property of
  that fixture's bridge induction (condition matched the query),
  not a mechanism defect. With a bridge whose condition does not
  match the query (cf=0, confirmed via cond_fire=0 in the trace),
  R10's dispatch works exactly as specified.
- Classification: bounded L2 integration test. No new mechanism,
  no new representation, no learned structure. Not L3.

## Governance disclosures

- The em dash in `// unified_learn.zag ... End-to-end ...` on line 1
  of the harness is pre-existing in the production source and
  predates this wave; it is carried byte-verbatim to keep the
  mechanism-region comparison exact. All content authored in this
  wave (prereg, main, report) contains zero em dashes.
- Prereg `778079959` was committed alone before any harness build,
  compile, or run. No bar was weakened or redefined after any
  observation. No Python was used anywhere.
- The bridge induction matched the source-analysis prediction
  (input[0]==97, ELSE branch for `xab`). If it had not, the bar
  would have been reported as SETUP-FAIL per the frozen prereg, not
  retuned.
- Commit set for this wave: the prereg (alone, beforehand), the
  harness `iu9_verify.zag`, the raw evidence `IU9_VERIFY_RAW.txt`,
  and this report. Binaries were built only in /tmp and never
  staged. Only owned paths staged.

## Recommended follow-up

The INTENT-UNIFIED guard family (IU3, IU4/IU5, R8, R9, R10) now has
complete rank and pair-class coverage with no known untested
dispatch paths. The remaining open dimensions are the disclosed
design boundaries B2 and B3. A future wave could address B2 (the
em=0 non-truncated pair class) if a principled evidence rule for it
is formulated, or the frontier can move to a new capability.
