# Prereg: H-CAUSAL-UNIFIED (FROZEN)

**Date:** 2026-09-29
**Hypothesis:** H-CAUSAL-UNIFIED
**Status:** FROZEN. Implementation must follow this document. No bar may be
weakened after results. Commit-order: this file's commit must strictly
precede the implementation commit.

## Claim

The full causal contest/split/merge machinery from causal_learn.zag can be
ported into the unified learner process, replacing the simplified causal
store on a new stream format, without breaking the 9 frozen H-UNIFIED bars,
while making SUPERSEDED provenance queryable and converting the U-A2
silent-replacement failure into explicit contest plus withhold.

## Context

1. H-UNIFIED SURVIVES (9/9) on its frozen bars (commit f5dd7cdc7). Its causal
   path is a simplified rule store (clearn/cpredict): 16 rules, single
   condition, single effect, contradiction only marks CONFLICTED.
2. H-CAUSAL SURVIVES (bounded L2): full machinery with episodes, entries,
   SPLIT, AMBIGUOUS candidates, refutation, CONTEST with temporal support
   voting, SUPERSEDED markings, MERGE. 14/14 probes.
3. The H-UNIFIED adversary KILLED the general composition claim via U-A2:
   a format-valid interfering item silently replaced a verified causal
   answer (s1=0 became s1=9) with no withhold and no provenance. The frozen
   9/9 bars still pass; the kill concerns generalization of K-U5. Lineage:
   the frozen SURVIVES stands; the general claim is superseded by the
   adversary report (commit 383c05aeb).
4. Canonical state Section 7 lists as an open question: "Full causal
   contest/split/merge machinery ported into the unified process
   (H-UNIFIED uses the simplified causal store)."
5. Canonical state Section 1.2 records the "decorative provenance"
   downgrade: SUPERSEDED markings are logged but no probe can query them.

## Design

**New file:** `unified_causal.zag`, based on the COMMITTED
`unified_learn.zag` at HEAD (commit e27edbaf3, which includes the H-INTENT
port; 1497 lines; Part A 10 unified tests + Part B 10 intent tests = 20
tests). A separate file avoids any conflict with sibling agents' working
trees. If H-CAUSAL-UNIFIED survives, it becomes the new canonical unified
file; otherwise it is preserved as a negative result and the original
file is untouched.

*Amendment note (2026-09-29, before any implementation): the original
draft of this prereg described the base as the pre-intent 1092-line file
with 9 tests. The H-INTENT work has since been committed (e27edbaf3), so
the base is the 1497-line intent-inclusive file with 20 tests. K-CU1 is
corrected accordingly. No implementation existed at amendment time.*

**Port:** The causal_learn.zag machinery functions (episodes, entries,
effects_over, split_attempt, amb_update, contests, merge_pass,
learn_episode, predict, list_hypos) are copied verbatim except:
- Workspace offsets rebased to FUBASE=3600 (absolute), sized for 128
  episodes / 32 entries / 8 contests (4376 bytes, ends 8076 < PAIRBASE
  8192; clear of the bridge WORK scratch and the H-INTENT IBASE region).
- Capacity guards: new_entry 64->32, new_contest 16->8. The test uses 18
  episodes, under 32 entries, 3 contests; guards never trigger.
- Shared utils (z_alloc, emit, get32, set32) are reused from the unified
  file, not duplicated. An e64 shim is added (defensive newline strip).
- load_obs and main are NOT ported. Added: fu_init (default entries for
  actions 0..3), fu_learn_ep (one episode in, learn it), fu_predict,
  fu_hist_count (emit hypothesis listing, return SUPERSEDED count),
  fu_contests_open (return UNRESOLVED contest count).

**Stream format (router extensions, all additive):**
- CAUS_LEARN: "2+ segs, iiiia>iii" (4 ints left: t,p,l,a; 3 ints right:
  nt,np,nl) routes to code 2 alongside the legacy "iii>ii".
- CAUS_QUERY: "single 4-int tuple" (t,p,l,a) routes to code 4 alongside
  the legacy 3-int tuple.
- New code 5 CAUS_HIST for the literal "caus_hist": emits the hypothesis
  and contest listing, returns counts.
- Mixed 3>2 and 4>3 segments in one line: WITHHOLD (malformed).

**Handlers:** handle_caus_learn dispatches per segment on left-int count
(3 = legacy clearn, 4 = fu_learn_ep). handle_caus_query dispatches on
tuple length (3 = legacy cpredict, 4 = fu_predict). handle_caus_hist
calls fu_hist_count and fu_contests_open.

**Test in main():** After the 9 original tests (unchanged), the 17
H-CAUSAL episodes are fed incrementally as five 4>3 stream lines (phase
deltas, same order as cum_C2.txt), with the 14 probes as 4-int queries
after each phase, then the history query, then the U-A2 interference
probe on the full path.

## Frozen kill bars

**K-CU1:** All 20 tests in unified_learn.zag at HEAD pass unchanged in
unified_causal.zag: Part A (K-U1, K-U2a, K-U2b, K-U2c, K-U3, K-U4a
intent-adapted, K-U4a2, K-U4b, K-U5, K-A) and Part B (B-T1, B-T1a, B-T1b,
B-T2, B-T2a, B-T2b, B-T3, B-T3b, B-T3c, plus the B-T3 intent_winner check:
10 intent battery tests). The original 9 frozen H-UNIFIED bars are
preserved inside this set (K-U4a is intent-adapted per e27edbaf3).

**K-CU2:** All 14 H-CAUSAL probes PASS within the unified process, fed
incrementally, with these exact expected outputs (from RESULTS_CAUSAL.md):
- Phase A: Q(2,0,0)|2 -> (2,1,0); Q(1,1,0)|2 -> (1,1,0); Q(0,0,0)|0 ->
  (1,0,0).
- Phase B: Q(2,0,0)|2 -> WITHHOLD; Q(2,0,1)|2 -> (2,0,1); Q(0,0,0)|2 ->
  (0,1,0).
- Phase B2: Q(2,0,0)|2 -> (2,0,0); Q(0,0,0)|2 -> (0,1,0); Q(1,1,1)|2 ->
  (1,1,1).
- Phase C1: Q(2,0,0)|2 -> (2,1,0); Q(2,0,1)|2 -> (2,0,1).
- Phase C2: Q(2,0,0)|2 -> (2,1,0); Q(2,0,1)|2 -> (2,1,1); Q(0,0,0)|2 ->
  (0,1,0).

**K-CU3:** After phase C2, the `caus_hist` query routes to CAUS_HIST,
emits the hypothesis listing, and returns SUPERSEDED count >= 1
(provenance is queryable, not decorative).

**K-CU4:** Two full runs of the binary are byte-identical (determinism).

**K-CU5 (U-A2 regression on the full path):** After phase C2 verifies
Q(2,0,0,2) -> (2,1,0), feeding the interfering item "2,0,0,2>2,0,0"
(a) opens a contest (emitted), (b) makes Q(2,0,0,2) WITHHOLD while the
contest is unresolved (no silent replacement), and (c) the history query
shows >= 1 UNRESOLVED contest. This is the behavior the simplified store
failed (U-A2 kill).

## What success looks like

unified_causal.zag compiles under the pinned znc, the binary prints
37/37 (20 preserved Part A + Part B tests, 14 H-CAUSAL probes, K-CU3
history check, 2 K-CU5 interference checks), K-CU4 holds by byte
comparison, and the trace shows SPLIT/CONTEST/RESOLVE/MERGE/SUPERSEDE
lines from the ported machinery operating inside the unified process.

## What failure looks like

Any frozen bar fails: the port is KILLED, the file is kept as negative
evidence, and unified_learn.zag remains the canonical file. In
particular, if the 14 probes do not reproduce exactly (porting error), or
if K-CU5 shows silent replacement on the full path (the machinery does
not transfer), the hypothesis dies.

## Purity

Pure Zag. No Python. Fixture conversion (none needed; episodes are inline
literals transcribed from the committed obs files) uses no tooling.
Determinism check uses cmp and sha256sum (shell, not Python).
