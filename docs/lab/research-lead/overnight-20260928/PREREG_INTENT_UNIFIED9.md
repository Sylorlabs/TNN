# PREREG: H-INTENT-UNIFIED9 (FROZEN)

## Hypothesis

H-INTENT-UNIFIED9: R10's kind dispatch (proc_apply vs bridge_apply)
on a mixed bridge/proc pair beyond the top two is correct, and R10
does not over-withhold on agreeing answers with different internal
slots.

## Background

H-INTENT-UNIFIED8 SURVIVES (9/9, bounded L2 integration repair).
Independent red team SURVIVES (X-IU8-1/3/4/5 PASS, X-IU8-2
INCONCLUSIVE due to a disclosed adversary fixture limitation).

The red team's sharpest named remaining attack surface: R10's kind
dispatch on a mixed bridge/proc pair BEYOND the top two is UNTESTED.
X-IU8-2 could not engage it because the induced bridge outranked the
procs via cf=1 (score 60000), so the IU3 top-two guard fired instead.

The IU8 builder also recommended a precision audit of whether R10
over-withholds on agreeing answers with different internal slots.

## Mechanism delta

None. H-INTENT-UNIFIED9 is a test wave on H-INTENT-UNIFIED8's R10.
It closes the last untested dispatch path named by the red team and
audits precision. If a defect is found, repair follows in a later
wave; this wave does not change the mechanism.

## Frozen bars

### K-IU9-1: Mixed-kind dispatch beyond top two

Fixture (fresh W, learn order V1, V2, B; query `xab`, qlen=3):

- V1 = t_learn(`xab>xxx;xbc>xxx;xde>xxx`): proc. Known from K-IU8-1a:
  em=1, answer `xxx`, score 50000.
- V2 = t_learn(`xab>xxx;xfg>xxx;xhi>xxx`): proc. Structurally
  identical to V1 (uniform 3-char inputs, constant `xxx` output).
  Expected: em=1, answer `xxx`, score 50000.
- B = t_learn(`aab>baa;abb>bba;acb>bca;xab>xab;xcb>xcb;xdb>xdb`):
  bridge. Expected induction from source analysis: the learner tries
  p=0 first, then distinct values in order of appearance ('a' before
  'x'). For v='a', s1={aab>baa, abb>bba, acb>bca} (reverse) and
  s2={xab>xab, xcb>xcb, xdb>xdb} (identity) should both be
  discoverable, yielding IF input[0]==97 THEN reverse ELSE identity.
  For query `xab`, input[0]=120, so the ELSE branch applies: cf=0,
  em=1 (`xab` is the 4th recorded input, within the 16-cap), applied
  answer `xab` (identity), train_len=3 uniform so lm=1, score 50000.

Setup validity (all must hold, else SETUP-FAIL, not a kill):

- v1 >= 0, v2 >= 0, b >= 1000.
- e1 == 1, e2 == 1, eb == 1 via iu8_show.
- iu8_show answers: V1 `xxx`, V2 `xxx`, B `xab` (B dissents).

Frozen expectation:

- kind == -2.
- The decide section contains the R10 diagnostic
  (`verbatim candidates disagree beyond top two`) exactly once.
- Zero occurrences of older-guard diagnostics (IU3-OLD, IU4A, IU4B,
  R8, R9) in the decide section.

Rationale: with all three at 50000 and learn order V1, V2, B, the
top two are V1 and V2 (tie-break keeps earlier), both agreeing on
`xxx`, so IU3, R8, and R9 do not fire. R10 must catch the (V1,B) and
(V2,B) mixed-kind disagreements via correct bridge_apply dispatch.
If B instead outranks to the top two (cf=1, score 60000), IU3 will
fire on the (B,V1) top-two disagreement; that is a setup failure
(the bridge condition matched the query), not an R10 defect.

Verdict: PASS if the frozen expectation is met. SETUP-FAIL if setup
is invalid or IU3 fires (B outranked). KILL if kind != -2 with valid
setup and no R10 diagnostic (dispatch defect), or if a wrong guard's
diagnostic fires, or if R10 fires with incorrect text.

### K-IU9-2: Precision audit (agreeing answers, different slots)

Fixture (fresh W, learn order V1, V2, V3; query `xab`):

- V1 = t_learn(`xab>xxx;xbc>xxx;xde>xxx`): proc, 50000, `xxx`.
- V2 = t_learn(`xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`):
  proc. Known from K-IU8-1a: 40000 (varied input lengths 4,4,4,4,4,3,
  tlen=-1, lm=0), `xxx`.
- V3 = t_learn(`xabcd>xxx;xefgh>xxx;xab>xxx`): proc. Varied input
  lengths (5,5,3), tlen=-1, lm=0. Expected: 40000, `xxx`.

All three agree on `xxx` with different internal candidate slots.

Setup validity: all rc >= 0, all em == 1, all iu8_show answers `xxx`.

Frozen expectation: kind == 0 (proc winner V1), NOT -2. Zero
withhold diagnostics in the decide section. R10 must not fire when
all answers agree.

Verdict: PASS if kind==0 and no withhold diagnostic appears.
KILL if kind==-2 (R10 over-withholds on agreement: precision
defect). SETUP-FAIL if setup is invalid.

### K-IU9-3: Regression (production mains byte-identical)

Rebuild the committed `unified_learn.zag` and `intent_learn.zag`
mains at HEAD via git show (cmp-verified against the worktree),
compile to /tmp with the pinned toolchain, run each main 3 times
directly.

Frozen expectation: unified_learn output md5
`904de9f83a2873c7a8862b71804a9065`; intent_learn output md5
`98315faec8faea24e75533892c0b240d`; 3/3 byte-identical each;
exit 0; zero stderr bytes.

Verdict: PASS if met. KILL on any hash mismatch or
non-determinism.

### K-IU9-4: Determinism

The IU9 harness binary is run 3 times directly.

Frozen expectation: 3/3 byte-identical via cmp, exit 0, zero
stderr bytes.

Verdict: PASS if met. KILL on non-determinism.

## Overall verdict rule

- SURVIVES if all 4 bars PASS.
- KILLED if any bar KILLs.
- INCONCLUSIVE on a dimension if that bar SETUP-FAILs. A
  SETUP-FAIL is disclosed honestly and is not a kill.

## Governance

- This prereg is committed ALONE before any harness build, compile,
  or run. No implementation exists at prereg time.
- Pure Zag throughout: prereg, harness, builds, runs, greps, md5,
  cmp. No Python at any stage.
- Zero em dashes in all authored content (byte-verified before
  commit).
- Harness construction: mechanism region (lines 1-1579) extracted
  from the COMMITTED `unified_learn.zag` at HEAD via git show and
  cmp-verified byte-identical against the worktree region; helpers
  (t_learn, t_decide, iu4_init, iu8_show) carried verbatim from the
  committed `iu8_verify.zag`; new frozen-bar main. No mechanism
  byte is altered.
- Binaries are built only in /tmp and never staged.
- Only owned paths are staged. No broad git add.
