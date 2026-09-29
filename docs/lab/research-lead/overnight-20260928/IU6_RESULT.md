# H-INTENT-UNIFIED6: RESULT (IU6)

**Date:** 2026-09-29
**Verdict: H-INTENT-UNIFIED6 SURVIVES (7/7).** The X-IU5-1 third-anchor
downgrade is closed at the mechanism level. Classification: bounded L2
integration repair. Not L3.

## Lineage

- Prereg `PREREG_INTENT_UNIFIED6.md` committed alone as `f3c068fd4`
  before any implementation edit, build, or run. No amendments.
  `git merge-base --is-ancestor f3c068fd4 HEAD` verified.
- Implementation: identical R8 edits in `unified_learn.zag` and
  `intent_learn.zag`. All 8 intent functions verified byte-identical
  between the two files via per-function extraction and cmp.
- Harness: `iu6_verify.zag` = mechanism region of NEW
  `unified_learn.zag` (lines 1-1471, everything before `fn main`) plus
  test helpers (t_learn, t_decide, iu4_init, build_big_line) plus
  K-IU6 test main. Built in /tmp only; binary never committed.
- Toolchain: znc 2026.07.0-dev (edition 2026), pinned. Pure Zag
  throughout. No Python at any stage.

## The repair (R8: all-pairs both-truncated guard)

The R5/R6 guards compare only the top two ranked candidates. X-IU5-1
demonstrates a genuine truncated-vs-truncated contradiction hiding
behind an agreeing second: C3 (proc, score 10000, answer `bax`) ranked
third behind C2 (bridge, score 20000, answer `xxx`), while top C1
(bridge, score 30000, answer `xxx`) agrees with C2. The top-two guard
falls through; the C3/C1 contradiction is silently resolved.

R8 inserts, after the existing truncated-conflict guard block and before
the gap==0 tie check, an all-pairs guard: for each unordered candidate
pair (a,b) with a<b, if both have em=0 and both records are truncated
(true npairs > 16), compute kind-dispatched answers over qlen bytes;
if any pair disagrees, emit
`INTENT TRUNCATED-CONFLICT-POSSIBLE: truncated candidates disagree
beyond top two; WITHHOLD AMBIGUOUS` and return kind=-2.

Precedence is structural and frozen:
1. Verbatim guard (both em=1) fires first, unchanged.
2. Top-two truncated guards (verbatim-vs-truncated, both-truncated)
   fire second, unchanged, with exact diagnostic texts.
3. All-pairs guard fires third, only if the top-two guards did not.
4. Gap==0 tie check fires last, unchanged.

The all-pairs guard does not extend the verbatim-meets-truncated
branches (em=1 on one side); those remain top-two-only. It does not
fire on agreement (X-IU5-3 honest negative preserved).

## Frozen kill-bar evidence

Raw: `IU6_VERIFY_RAW.txt` (md5 `a4dad5090897bf0a82c5fddad3e45b57`),
3/3 runs byte-identical (cmp), exit 0.

- **K-IU6-1 PASS:** X-IU5-1 fixture (C3 proc + C1 bridge + C2 bridge,
  all 17-pair truncated, query `xab`) -> kind=-2 with the NEW
  diagnostic `truncated candidates disagree beyond top two`. The
  third-anchor contradiction is now caught.
- **K-IU6-2a PASS:** K-IU5-1a (proc-first, top-two both-truncated) ->
  kind=-2 with the UNCHANGED diagnostic `both records truncated with
  different answers`. Precedence preserved; all-pairs guard did not
  shadow.
- **K-IU6-2b PASS:** K-IU5-1b (bridge-first) -> kind=-2 with the
  UNCHANGED top-two diagnostic. Precedence preserved.
- **K-IU6-3a PASS:** K-IU5-2 (20-char outputs) -> rc=-1, honest-cap
  diagnostic, exit 0, no panic. R7 intact.
- **K-IU6-3b PASS:** K-IU4-1 (verbatim-vs-truncated) -> kind=-2 with
  the UNCHANGED verbatim-vs-truncated diagnostic. Branch precedence
  intact.
- **K-IU6-3c PASS:** K-IU4-2 (129-pair) -> rc=-1, WORK honest failure,
  exit 0, no panic.
- **K-IU6-3d PASS:** In-cap verbatim conflict -> kind=-2. Verbatim
  guard intact.
- **K-IU6-4 PASS:** 3/3 byte-identical.

**Regression suites:**
- `unified_learn.zag` main(): 20/20, md5
  `904de9f83a2873c7a8862b71804a9065` = frozen IU4 hash. Byte-identical.
- `intent_learn.zag` main(): 10/10, md5
  `98315faec8faea24e75533892c0b240d` = frozen IU4 hash. Byte-identical.

## What the verdict means

The frozen IU5 claim "conflict detection is verbatim-anchored AND
both-truncated-anchored (no other anchor)" is superseded. The
both-truncated guard now covers genuine contradictions among ALL
truncated candidates with em=0, regardless of rank. The X-IU5-1 hazard
class (silent resolution via ranking) is closed at the mechanism level.

## Boundaries (disclosed)

- Same precision cost as R6: truncated records whose procedures merely
  generalize differently will withhold with an honest "POSSIBLE"
  diagnostic even when unrecorded pairs do not contradict.
- The verbatim-meets-truncated branches remain top-two-only; a
  third-anchor verbatim-vs-truncated conflict is out of scope.
- O(ncand^2) worst case; ncand bounded by PROC_MAX+BR_MAX (small).
- Bounded L2, not L3.

## Governance disclosures

1. Prereg `f3c068fd4` strictly precedes all implementation; verified
   via `git merge-base --is-ancestor`. No amendments.
2. Pure Zag throughout; zero Python at any stage.
3. Binaries built in /tmp/iu6 only, never committed.
4. Only researcher-owned paths staged: `PREREG_INTENT_UNIFIED6.md`
   (already committed), `unified_learn.zag`, `intent_learn.zag`,
   `iu6_verify.zag`, `IU6_VERIFY_RAW.txt`, `IU6_RESULT.md`.
   Concurrent workers' files untouched (pathspec-restricted staging).
5. No em dashes in loop documentation.
6. No test-answer literals in mechanism regions; all fixture strings
   live in the harness main().

## Files (branch `tnn-native-lab`)

- `docs/lab/research-lead/overnight-20260928/PREREG_INTENT_UNIFIED6.md`
  (commit `f3c068fd4`, prereg alone)
- `docs/lab/research-lead/overnight-20260928/unified_learn.zag`
  (R8 applied)
- `docs/lab/research-lead/overnight-20260928/intent_learn.zag`
  (R8 applied identically)
- `docs/lab/research-lead/overnight-20260928/iu6_verify.zag`
  (harness)
- `docs/lab/research-lead/overnight-20260928/IU6_VERIFY_RAW.txt`
  (raw evidence, md5 `a4dad5090897bf0a82c5fddad3e45b57`)
- `docs/lab/research-lead/overnight-20260928/IU6_RESULT.md` (this report)

## Suggested follow-ups for parent

1. Independent red team on H-INTENT-UNIFIED6 (natural attacks:
   fourth-anchor conflicts, verbatim-meets-truncated third-anchor,
   agreement among 3+ with one dissenter at rank 4+).
2. The research paper's H-INTENT-UNIFIED5 section needs this downgrade
   plus the H-INTENT-UNIFIED6 result (paper lane).
