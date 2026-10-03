# H-INTENT-UNIFIED7: RESULT (IU7)

**Date:** 2026-09-29
**Verdict: H-INTENT-UNIFIED7 SURVIVES (8/8).** The X-IU6-2 verbatim
third-anchor boundary is closed at the mechanism level.
Classification: bounded L2 integration repair. Not L3.

## Lineage

- Prereg `PREREG_INTENT_UNIFIED7.md` committed alone as `7bc85499d`
  before any implementation edit, build, or run. No amendments.
  `git merge-base --is-ancestor 7bc85499d HEAD` verified.
- Implementation: identical R9 edits in `unified_learn.zag` and
  `intent_learn.zag`. All 8 intent functions verified byte-identical
  between the two files via per-function extraction and cmp.
- Harness: `iu7_verify.zag` = mechanism region of NEW
  `unified_learn.zag` (lines 1-1529, everything before `fn main`),
  cmp-verified against the committed source; helpers
  (t_learn, t_decide, iu4_init, build_big_line) carried over from
  `iu6_verify.zag`; new K-IU7 test main. Built in /tmp only; binary
  never committed.
- Evidence method: `znc --run` emits compile-time analyzer warnings
  to stderr, so each source was compiled once to /tmp (binaries never
  committed) and the binary was executed directly three times for
  clean raws. The IU6 worker used the same method.
- Toolchain: znc 2026.07.0-dev (edition 2026), pinned. Pure Zag
  throughout. No Python at any stage.

## The repair (R9: all-pairs verbatim-vs-truncated guard)

The R4/R5 truncated guard compares only the top two ranked candidates
for pairs with em=1 on one side. X-IU6-2 demonstrates a genuine
verbatim-vs-truncated contradiction hiding behind agreeing verbatim
anchors: T3 (proc, 17-pair truncated, em=0, answer `bax`, score 10000)
ranked third behind V1 (proc, em=1, answer `xxx`, score 50000) and V2
(proc, em=1, answer `xxx`, score 40000). The verbatim guard sees
top-two agreement and falls through; the top-two truncated guard needs
em=1 on exactly one side of the top two (both are em=1) or em=0 on
both sides; R8 skips every pair involving an em=1 candidate. The
genuine T3/V1 contradiction (`xab>bax` in T3's unrecorded tail vs
`xab>xxx` in V1's recorded data) was silently resolved: kind=0.

R9 inserts, after the R8 all-pairs both-truncated block and before the
gap==0 tie check, an all-pairs guard: for each unordered candidate
pair (a,b) with a<b, if em==1 on exactly one side and the em==0 side
has a truncated record (true npairs > 16), compute kind-dispatched
answers over qlen bytes; if any pair disagrees, emit
`INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets
truncated record with different answer beyond top two; WITHHOLD
AMBIGUOUS` and return kind=-2.

Precedence is structural and frozen:
1. Verbatim guard (both em=1, top-two) fires first, unchanged.
2. Top-two truncated guards (verbatim-vs-truncated, both-truncated)
   fire second, unchanged, with exact diagnostic texts.
3. R8 all-pairs both-truncated guard fires third, unchanged, with its
   exact diagnostic text.
4. R9 all-pairs verbatim-vs-truncated guard fires fourth, only if the
   earlier guards did not, with its NEW diagnostic text.
5. Gap==0 tie check fires last, unchanged.

Pair-class exclusivity holds by construction: a pair is checked by R8
iff em=0 on both sides; by R9 iff em=1 on exactly one side with the
em=0 side truncated. No pair is checked by both.

## Frozen kill-bar evidence

Raw: `IU7_VERIFY_RAW.txt` (md5 `502c02b402da0079f6775b31dd696273`),
3/3 runs byte-identical (cmp), exit 0.

- **K-IU7-1 PASS:** X-IU6-2 fixture (T3 truncated + V1/V2 verbatim
  agreers, query `xab`) -> kind=-2 with the NEW diagnostic
  `verbatim candidate meets truncated record with different answer
  beyond top two`. The verbatim third-anchor contradiction is now
  caught. The NEW diagnostic text appears exactly once in the raw
  (K71 section), nowhere else.
- **K-IU7-2a PASS:** K-IU5-1a (proc-first, top-two both-truncated) ->
  kind=-2 with the UNCHANGED diagnostic `both records truncated with
  different answers`. Exact text count in raw: 1. R9 did not shadow.
- **K-IU7-2b PASS:** K-IU4-1 (top-two verbatim-vs-truncated) ->
  kind=-2 with the UNCHANGED diagnostic `verbatim candidate meets
  truncated record with different answer`. Exact text count in raw: 1.
  R9 did not shadow.
- **K-IU7-2c PASS:** X-IU5-1 four-truncated fixture -> kind=-2 with
  the UNCHANGED R8 diagnostic `truncated candidates disagree beyond
  top two`. Exact text count in raw: 2 (2c and 3a sections). R8
  intact.
- **K-IU7-3a PASS:** K-IU6-1 X-IU5-1 three-truncated -> kind=-2, R8
  diagnostic.
- **K-IU7-3b PASS:** 20-char honest cap -> rc=-1, no panic.
- **K-IU7-3c PASS:** 129-pair WORK guard -> rc=-1, no panic.
- **K-IU7-3d PASS:** In-cap verbatim conflict -> kind=-2. Verbatim
  guard intact.

**Regression suites (binary-run, clean raws):**
- `unified_learn.zag` main(): 20/20, md5
  `904de9f83a2873c7a8862b71804a9065` = frozen IU4 hash.
  Byte-identical. 3/3 deterministic.
- `intent_learn.zag` main(): 10/10, md5
  `98315faec8faea24e75533892c0b240d` = frozen IU4 hash.
  Byte-identical. 3/3 deterministic.
- The R9 diagnostic fires zero times across both suites: no existing
  fixture behavior changed.

**Methodology note (disclosed):** an initial `--run` capture showed
suite md5s differing from the frozen hashes; the difference was
compile-time analyzer warnings (A0102) on stderr, not behavior. The
IU6-era sources produce the same warnings under `--run`. Re-running
via compile-once + direct binary execution (the IU6 evidence method)
reproduces the frozen hashes exactly. No behavior changed.

## What the verdict means

The frozen IU6 claim "the verbatim-meets-truncated branches remain
top-two-only" is superseded. Verbatim-vs-truncated conflict detection
now covers genuine contradictions among ALL candidates regardless of
rank, for pairs with em=1 on exactly one side and a truncated em=0
record on the other. The X-IU6-2 hazard class (silent resolution via
ranking behind verbatim agreers) is closed at the mechanism level.

## Boundaries (disclosed)

- Same precision cost as R6/R8: truncated records whose procedures
  merely generalize differently will withhold with an honest
  "POSSIBLE" diagnostic even when the unrecorded training pairs do
  not contradict.
- O(ncand^2) worst case; ncand bounded by PROC_MAX+BR_MAX (small).
- A both-verbatim (em=1 on both sides) disagreement beyond the top
  two remains out of scope: the IU3 verbatim guard is still
  top-two-only. Next disclosed boundary for a future lane.
- An em=1 vs em=0 non-truncated pair is out of scope (same as R4/R5).
- Bounded L2, not L3.

## Governance disclosures

1. Prereg `7bc85499d` strictly precedes all implementation; verified
   via `git merge-base --is-ancestor`. No amendments.
2. Pure Zag throughout; zero Python at any stage.
3. Binaries built in /tmp only, never committed.
4. Only researcher-owned paths staged: `PREREG_INTENT_UNIFIED7.md`
   (already committed), `unified_learn.zag`, `intent_learn.zag`,
   `iu7_verify.zag`, `IU7_VERIFY_RAW.txt`, `IU7_RESULT.md`.
   Concurrent workers' files untouched (pathspec-restricted staging).
5. No em dashes in loop documentation (byte-verified: 0 in raw).
6. No test-answer literals in mechanism regions; all fixture strings
   live in the harness main().
7. All kill-bar fixtures executed with zero tuning on first run; 8/8
   PASS on first execution.

## Files (branch `tnn-native-lab`)

- `docs/lab/research-lead/overnight-20260928/PREREG_INTENT_UNIFIED7.md`
  (commit `7bc85499d`, prereg alone)
- `docs/lab/research-lead/overnight-20260928/unified_learn.zag`
  (R9 applied)
- `docs/lab/research-lead/overnight-20260928/intent_learn.zag`
  (R9 applied identically)
- `docs/lab/research-lead/overnight-20260928/iu7_verify.zag`
  (harness)
- `docs/lab/research-lead/overnight-20260928/IU7_VERIFY_RAW.txt`
  (raw evidence, md5 `502c02b402da0079f6775b31dd696273`)
- `docs/lab/research-lead/overnight-20260928/IU7_RESULT.md` (this report)

## Suggested follow-ups for parent

1. Independent red team on H-INTENT-UNIFIED7 (natural attacks:
   both-verbatim beyond-top-two disagreement; em=1 vs em=0
   non-truncated pairs; rank-4+ verbatim-vs-truncated dissenters;
   three-way mixed anchor sets).
2. The research paper's H-INTENT-UNIFIED6 section should note the
   X-IU6-2 boundary closure plus the H-INTENT-UNIFIED7 result (paper
   lane).
