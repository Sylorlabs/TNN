# H-CAUSAL-UNIFIED7 RESULT

**Hypothesis:** H-CAUSAL-UNIFIED7
**Date:** 2026-09-29
**Mode:** pure Zag, no Python anywhere (implementation, harnesses,
builds, runs, analysis).
**Verdict: SURVIVES (6/6 frozen bars pass).**

## 1. What this hypothesis is

H-CAUSAL-UNIFIED6 left two deferred boundaries: the oldest-first
`find_conflicted` tie-break and shared-winner double voting. Direct
source analysis of the committed CU6 mechanism
(`unified_causal6.zag`, MD5 `3eacd6fe82fae1f7b7ba81c4c7e48387`)
showed the double-voting boundary is not cosmetic. `conflict_adjudicate`
skips only `EP_SUP` when tallying; carve winners are shared by index
into the child entry but remain `EP_ACT` in the parent tombstone. The
same episode can therefore vote in every later adjudication at that
state, which produces cumulative entrenchment: old winner mass persists,
fresh contradictory evidence is repeatedly outvoted and superseded, and
the fresh support needed to flip the outcome ratchets upward across
reversals. H-CAUSAL-UNIFIED7 is the one-episode-one-vote repair.

## 2. Commit lineage

- CU6 source (builder report, 2026-09-29): prereg `2f48dd7e1`,
  result `438c3344a`. Reported SURVIVES, 5/5, bounded L2.
- CU6 red team (2026-09-29): prereg `e74b3f0c8`, result `2cb0b1a6e`.
  Reported SURVIVES, four attacks.
- H-CAUSAL-UNIFIED7 prereg: `db6981b27`
  ("PREREG H-CAUSAL-UNIFIED7 FROZEN (alone, before implementation).
  One-episode-one-vote repair; entrenchment kill bars K-CU7-1..6.
  Pure Zag.")
- H-CAUSAL-UNIFIED7 prereg amendment 1: `acfd92697`
  ("PREREG AMEND1 H-CAUSAL-UNIFIED7 FROZEN (before any
  harness/execution). Correct K-CU7-1(b) entry-3 list and K-CU7-1(e)
  withhold path. Pure Zag.")
- This result: committed after this document (see section 12).

## 3. Frozen repair (R1..R5)

R1: new episode state `EP_COUNTED() == 2` (was only
`EP_ACT() == 0`, `EP_SUP() == 1`).

R2: `conflict_adjudicate` tally skips both `EP_SUP` and
`EP_COUNTED`.

R3: the carve loop skips previously counted episodes when
selecting winners and sets `ep_st_set(W,f,EP_COUNTED())` on each
episode it shares into the new entry.

R4: `entry_eps` includes both `EP_ACT` and `EP_COUNTED`, so counted
episodes stay in the evidence set for effects, prediction, merge,
split, and the contradiction guard. The included set is exactly the
pre-repair `EP_ACT` set.

R5: every other episode-state check is unchanged, so counted
episodes remain live for the contradiction guard, conflicted-entry
routing, active contradiction detection, exact-episode prediction,
effects, and usability.

Frozen dispositions: D1, the oldest-first tie-break is unchanged
because no independent unsafe prediction was demonstrated from the
tie-break alone; D2, capacity eviction is deferred to a separate
hypothesis because entry exhaustion (32 entries) is explicit refusal
in `new_entry`, not silent behavior, and bundling eviction with the
vote repair would confound the mechanism change.

## 4. Frozen kill bars (as amended)

K-CU7-1 (double voting closed). Standard 20-episode CU6 flood, then
idx 20 `(0,0,0)` (first carve trigger), idx 21 `(1,1,1)`
(re-conflict), idx 22..26 five further `(1,1,1)`, idx 27..30 four
`(0,0,0)`. Asserts: (a) final `nent == 4` (exactly two carves);
(b) entry 3 episode list is exactly `[21,22,23,24,25,26,28]`
(`en_neps(W,3)==7`, first six `EP_COUNTED`, seventh `EP_ACT`);
(c) among idx 21..30 only idx 27 is `EP_SUP`; (d) final
`EP_COUNTED` count is 8 (idx 16, 20 from the first carve; idx 21..26
from the later carve); (e) final query at `(2,0,0)` action 2 returns
r=0 via the no-entry path and the independent white-box helper
`adv_live_contra(W,2,2,0,0)==1`, proving the contradiction is
genuinely live rather than silently forgotten.

K-CU7-2. Re-derive CU6 fresh-general-shadow closure: contradicted
state withholds, live contradiction remains, control state predicts
`(7,7,7)`.

K-CU7-3. Re-derive CU6 adjudicated-carve behavior: `(2,0,0)` predicts
`(0,0,0)`; `(1,0,0)` predicts `(0,0,0)`; `(0,0,0)` withholds.

K-CU7-4. Regression: CU7 battery stdout byte-identical to CU6
battery (MD5 `3bde55fe381a7c8ff1cef93d8c038da3`); CU7 main stdout
byte-identical to CU6 main (MD5 `87f8edc29825802327029f46f045dbe3`).

K-CU7-5. Three byte-identical runs each for adversary, battery, main.

K-CU7-6. CU6-to-CU7 source diff contains only frozen R1..R5 and no
fixture literals in mechanism functions.

Verdict rule: SURVIVES only if K-CU7-1..K-CU7-6 all pass; any failed
bar kills the hypothesis.

Exploratory (non-verdict) control, preregistered: run the K-CU7-1
entrenchment fixture against the CU6 mechanism and report the
observed ratchet.

## 5. Methodology

1. Extracted the committed CU6 mechanism region
   (`unified_causal6.zag` lines 1..2488) and the CU6 battery driver
   (`cu6_test.zag` lines 2489..2604) and CU6 adversary helpers
   (`cu6_adv.zag` lines 2489..2530) from the committed blobs via
   `git show`.
2. Applied R1..R5 to a copy of the CU6 mechanism, producing
   `unified_causal7.zag` (main begins line 2503; mechanism region
   lines 1..2501). Verified the diff against CU6 contains only R1..R5
   (section 10).
3. Assembled `cu7_adv.zag` = CU7 mechanism lines 1..2501 + CU6
   adversary helpers (byte-verbatim) + new main: `adv_count_epst`
   helper, the K-CU7-1 section (fresh, amended bar text), and the
   K-CU6-1/K-CU6-2 fixture sections copied verbatim with only their
   tags renamed to K-CU7-2/K-CU7-3 and inner emit prefixes renumbered.
   A nonzero exit propagates through a `k1kill` flag: any FAIL emit
   sets it and main returns 1.
4. Assembled `cu7_test.zag` = CU7 mechanism + CU6 battery driver
   byte-verbatim.
5. Built all three executables (`cu7_adv`, `cu7_test`, `cu7_main`
   from `unified_causal7.zag` unchanged) in `/tmp` with the Linux
   toolchain
   `/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`.
   No build output was piped through `head` after the incident in
   section 8.
6. Ran adversary, battery, and main three times each; compared
   MD5s; compared battery/main run 1 byte-for-byte against the
   frozen CU6 raw files; ran the exploratory CU6 control once.

## 6. Raw results

### 6.1 K-CU7-1: double voting closed (PASS, 5/5)

Adversary runs (3x): MD5 `36f835f69f41f100675bc385394cf6c3`,
byte-identical, exit 0, zero FAIL/KILL strings.

```
K1(a) nent=4 (expect 4)
K1(b) entry3-list-ok=1
K1(c) sup-set-ok=1
K1(d) counted=8 (expect 8)
WITHHOLD (no-entry)
K1(e) r=0 live=1
K-CU7-1 PASS: one-episode-one-vote; no immortal re-carve; evidence preserved
```

Mechanism trace of the K-CU7-1 fixture under CU7 (relevant lines):

```
UNCONFLICT action 2 state (2 0 0) at seq 21: winner outcome (0 0 0) support 2 vs loser (1 1 1) support 1; carved new entry 2 [s0=2&s1=0&s2=0] with 2 winner episode(s); 1 loser episode(s) SUPERSEDED in conflicted entry 0 (ST_CONFL kept)
UNCONFLICT action 2 state (2 0 0) at seq 28: winner outcome (1 1 1) support 6 vs loser (0 0 0) support 1; carved new entry 3 [s0=2&s1=0&s2=0] with 6 winner episode(s); 1 loser episode(s) SUPERSEDED in conflicted entry 2 (ST_CONFL kept)
```

Exactly two carves. The phase-A carve (2v1) counts idx 16, 20.
Later absorbs accumulate: at seq 24 the tally sees only uncounted
episodes (idx 16, 20 are counted and skipped), so the 3v2 situation
that carved under CU6 does NOT carve under CU7; the honest 6v1 carve
fires once at seq 28 and counts idx 21..26. Subsequent fresh
`(0,0,0)` evidence (idx 28..30) is absorbed live; no further carve
is possible from counted mass. The final query withholds via the
no-entry path (all covering entries conflicted) while
`adv_live_contra==1` proves the contradiction between the counted
`(1,1,1)` winners and the live `(0,0,0)` evidence is genuinely held,
not forgotten.

### 6.2 K-CU7-2: X-CU4-2 closed (PASS)

`K-CU7-2 PASS: X-CU4-2 closed; withhold holds through live contradiction; general entry intact`

### 6.3 K-CU7-3: adjudicated carves still predict (PASS)

`K-CU7-3 PASS: adjudicated carves predict; never-adjudicated withhold holds`

### 6.4 K-CU7-4: regression (PASS)

- Battery: 3 runs, MD5 `3bde55fe381a7c8ff1cef93d8c038da3`, run 1
  `cmp`-clean against frozen `CU6_TEST_RAW_1.txt`. `=== CU4 TEST
  RESULT: 16/16 ===`.
- Main: 3 runs, MD5 `87f8edc29825802327029f46f045dbe3`, run 1
  `cmp`-clean against frozen `CU6_MAIN_RAW_1.txt`. `=== CAUSAL-UNIFIED
  RESULT: 28/28 ===`.

### 6.5 K-CU7-5: determinism (PASS)

Adversary 3/3 identical (`36f835f69f41f100675bc385394cf6c3`),
battery 3/3 identical (`3bde55fe381a7c8ff1cef93d8c038da3`), main 3/3
identical (`87f8edc29825802327029f46f045dbe3`).

### 6.6 K-CU7-6: diff purity (PASS)

The CU6-to-CU7 source diff contains exactly: the `EP_COUNTED`
constant and its comments (R1); the tally skip condition (R2); the
carve skip condition, the `ep_st_set(W,f,EP_COUNTED())` transition,
and its comments (R3); the `entry_eps` inclusion and its comments
(R4). No other lines differ. No fixture literals appear in any
mechanism function. Full diff is reproduced in section 10.

### 6.7 Exploratory CU6 control (defect demonstration, not a bar)

Running the identical K-CU7-1 fixture against the CU6 mechanism:

```
UNCONFLICT action 2 state (2 0 0) at seq 21: winner outcome (0 0 0) support 2 vs loser (1 1 1) support 1; carved new entry 2 ... with 2 winner episode(s); 1 loser episode(s) SUPERSEDED in conflicted entry 0 (ST_CONFL kept)
UNCONFLICT action 2 state (2 0 0) at seq 24: winner outcome (1 1 1) support 3 vs loser (0 0 0) support 2; carved new entry 3 ... with 3 winner episode(s); 2 loser episode(s) SUPERSEDED in conflicted entry 2 (ST_CONFL kept)
UNCONFLICT action 2 state (2 0 0) at seq 29: winner outcome (1 1 1) support 3 vs loser (0 0 0) support 1; carved new entry 4 ... with 3 winner episode(s); 1 loser episode(s) SUPERSEDED in conflicted entry 2 (ST_CONFL kept)
UNCONFLICT action 2 state (2 0 0) at seq 31: winner outcome (1 1 1) support 3 vs loser (0 0 0) support 1; carved new entry 5 ... with 3 winner episode(s); 1 loser episode(s) SUPERSEDED in conflicted entry 2 (ST_CONFL kept)
exploratory nent=6
```

The block idx 21, 22, 23 voted at seq 24, again at seq 29, and again
at seq 31: three votes each from episodes that each cast one honest
ballot. Fresh `(0,0,0)` evidence idx 28 and idx 30 were each outvoted
3v1 and superseded. The same 3-episode block permanently outvotes any
bounded stream of fresh counter-evidence: the required fresh support
ratchets because the winners never leave the tally. Final query
withholds (r=0, live-contradiction), so the withhold machinery was
never the problem; the adjudication outcome was entrenched.

Causal reading: the oldest-first tie-break routes the re-vote (the
seq 29/31 absorbs tie entry 2 vs entry 3 and pick entry 2), but the
tie-break is not the defect. The defect is the tally including
already-counted winners. Under CU7 the tie-break still routes the
same absorbs to entry 2, and the absorbs simply accumulate live
evidence without carving: the tie-break is behaviorally neutral once
the tally is closed.

## 7. Causal interpretation

The CU6 mechanism had an immortal-vote defect: an episode that won an
adjudication kept its vote in every future adjudication at that
state. This is cumulative entrenchment, not a one-off miscount. Any
block of episodes that wins once can never be displaced by a bounded
amount of fresh evidence, because each reversal attempt re-counts the
old winners. The repair (R1..R5) retires winners from the tally while
keeping them live for every other mechanism use: the contradiction
guard still sees them (the final withhold is honest), absorb routing
still sees them, prediction and effects still see them. One episode,
one vote. The CU7 run shows the healthy counterpart: a 6v1 carve
fires exactly once on honest support, and later evidence accumulates
instead of being crushed by ghosts.

## 8. Failures and corrections during this task

1. Build pipeline incident. The first `znc build` invocation was
   piped through `head`; SIGPIPE killed the compiler before it wrote
   the binary, the observed exit code was `head`'s (not `znc`'s), and
   the subsequent "runs" executed a nonexistent binary (exit 127)
   producing identical empty files that were initially misread as
   successful deterministic runs. Caught on inspection (missing
   binary on disk). Rebuilt all three executables unpiped, verified
   the "wrote native binary" confirmation lines, and reran the full
   3x3 matrix from scratch. No number from the broken invocation
   appears anywhere in this report.
2. Two hand-trace errors, both caught before any verdict-affecting
   execution and corrected by frozen amendment `acfd92697`
   (committed before any harness was built): (a) predicted entry-3
   episode list length 6, actual 7 (idx 28 is appended to entry 3's
   list by `entry_add_ep` before the contest-capacity check
   conflict-marks entry 3); (b) predicted the final query would print
   "WITHHOLD (live-contradiction)", actual is "WITHHOLD (no-entry)"
   because every covering entry is conflicted and `predict` returns
   before the guard. The r=0 criterion was unchanged; only the
   mechanism path was corrected.
3. A third hand-trace error (predicting a CU7 carve at seq 24 by
   forgetting the phase-A winners were already counted) was caught
   when reading the actual CU7 raw; the frozen bars specified only
   final state, so no amendment was required.

## 9. Boundaries and deferred items

- D1 tie-break: unchanged. The CU7 run shows the tie-break still
  routes absorbs to the oldest equally specific tombstone, but the
  route no longer confers repeat votes.
- D2 capacity eviction: unchanged and untouched. Entry capacity is 32
  (not 16); exhaustion is explicit refusal. Contest capacity is 8;
  the flood in this fixture exhausts it, so phase-B/C re-conflicts go
  untracked with an explicit ERROR emit and ST_CONFL marking. This
  behavior is identical under CU6 and CU7 and is orthogonal to the
  vote defect; it remains a separate hypothesis.
- The `predict` comment near line 2205 ("after a successful carve
  the parent tombstone holds exactly 1 distinct live outcome (the
  shared winners; losers are superseded)") remains true under CU7:
  counted winners are still live, just retired from the tally.
- Inherited bytes: `unified_causal7.zag` contains 2 em-dash bytes at
  lines 1 and 1616. Both are verbatim inheritance from the CU2/CU6
  lineage comments, untouched by R1..R5; removing them would have
  added diff lines outside the frozen repair and violated K-CU7-6.
  They are reported here, not silently kept.

## 10. Exact CU6-to-CU7 source diff (K-CU7-6 evidence)

```
1175a1176,1180
> // H-CAUSAL-UNIFIED7 R1: an episode that already voted as a winner in a
> // carve. Retired from future adjudication tallies (one-episode-one-vote)
> // but still live evidence for the query guard, absorb routing, entry
> // beliefs, and effects.
> fn EP_COUNTED()i32 { return 2; }
1379c1384,1386
<     if(ep_st(W,f)==EP_SUP()){k=k+1;continue;}
---
>     // H-CAUSAL-UNIFIED7 R2: one-episode-one-vote. Episodes that already
>     // voted as winners in a carve (EP_COUNTED) do not vote again.
>     if(ep_st(W,f)==EP_SUP() || ep_st(W,f)==EP_COUNTED()){k=k+1;continue;}
1411,1412c1418,1421
<   // move winners (shared indices, stay live); supersede losers in cf
<   // (explicit retirement; losers are not shared with ni).
---
>   // H-CAUSAL-UNIFIED7 R3: move winners (shared indices) and mark them
>   // EP_COUNTED so they never vote in a later adjudication; supersede
>   // losers in cf (explicit retirement; losers are not shared with ni).
>   // Only uncounted live episodes can be winners: one-episode-one-vote.
1417c1426
<     if(ep_st(W,f)==EP_SUP()){k=k+1;continue;}
---
>     if(ep_st(W,f)==EP_SUP() || ep_st(W,f)==EP_COUNTED()){k=k+1;continue;}
1420a1430
>         ep_st_set(W,f,EP_COUNTED());
1566c1576,1579
<     if(ep_st(W,e)==EP_ACT()){tmp[n]=e as u8;n=n+1;}
---
>     // H-CAUSAL-UNIFIED7 R4: counted episodes stay in the evidence set for
>     // effects/prediction/merge/split; only the adjudication tally retires
>     // them. The included set is exactly the pre-repair EP_ACT set.
>     if(ep_st(W,e)==EP_ACT() || ep_st(W,e)==EP_COUNTED()){tmp[n]=e as u8;n=n+1;}
```

Nothing else differs. No fixture literals in mechanism functions.

## 11. Governance disclosures

- Pure Zag throughout: no Python in implementation, harnesses,
  builds, runs, or analysis.
- Prereg `db6981b27` strictly preceded implementation; amendment
  `acfd92697` strictly preceded all harness builds and executions.
  No bar was weakened; the two amended predictions were tightened to
  the exact mechanism behavior.
- Commits stay local on branch `tnn-native-lab`. No push was made or
  authorized.
- Only the owned path
  `docs/lab/research-lead/overnight-20260928/causal_unified7/` was
  staged.
- Classification: bounded L2. The repair is a structural mechanism
  fix to an adjudication defect; no representational invention is
  claimed. This result is this subagent's committed finding and is
  not presented as independently verified canonical work.
- No binaries, caches, or build artifacts are committed. Evidence is
  raw stdout text and assembled Zag sources only.

## 12. Files and evidence

Owned directory:
`docs/lab/research-lead/overnight-20260928/causal_unified7/`

- `PREREG_CAUSAL_UNIFIED7.md` (frozen, `db6981b27`)
- `PREREG_CAUSAL_UNIFIED7_AMEND1.md` (frozen, `acfd92697`)
- `unified_causal7.zag` (CU7 mechanism + main driver)
- `CU7_RESULT.md` (this document)
- `CU7_ADV_RAW_1.txt` (adversary run 1; 3/3 MD5
  `36f835f69f41f100675bc385394cf6c3`)
- `CU7_TEST_RAW_1.txt` (battery run 1; 3/3 MD5
  `3bde55fe381a7c8ff1cef93d8c038da3`)
- `CU7_MAIN_RAW_1.txt` (main run 1; 3/3 MD5
  `87f8edc29825802327029f46f045dbe3`)
- `CU6_ENTR_RAW_1.txt` (exploratory CU6 control, defect
  demonstration)
- `cu7_adv.zag` (assembled adversary source: CU7 mechanism +
  helpers + main)
- `cu7_test.zag` (assembled battery source: CU7 mechanism +
  battery driver)

Toolchain:
`/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`
(znc analyzer warnings only; all builds exit 0).
