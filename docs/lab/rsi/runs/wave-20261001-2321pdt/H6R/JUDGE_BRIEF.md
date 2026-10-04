# H6R JUDGE BRIEF (wave-20261001-2321pdt)

## Provenance

- RENDER_SHA: c7f6774809d9688f14d158ffacee4b90760e06dd
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: TNN3H6 SUBSTRATE-ABSENT, TNN3-SUBSTRATE DESIGN-COMPLETE with KB-H6R
- NEW_KNOWLEDGE_CLAIM: The standing package unblocks H6's accumulation and integration bars (B1, B2 pass) but cannot beat the no-standing baseline on probe prediction (B3 margin exactly 0, kill fires) and cannot express preferential retention (B4 substrate-insufficient: standing records are unprotected zero-lbid nodes evicted before any fact).

## Verdict

BUILD-FAIL. The B3 kill bar fired (margin 0 < 15 points, exactly as the frozen H6R-B3-nil theorem predicted). B4 is additionally SUBSTRATE-INSUFFICIENT with the exact gap below. Kill bars KB-H6R were not weakened.

## Numbers versus frozen KB-H6R bars

- B1 (trajectory discrimination): PASS. Singleton contradict dips 4 to 3 then recovers to 3 under confirms; systematic shift declines 1 to 0 to -1 to -1 monotonically. White-box asserted.
- B2 (integration): PASS. lbid is live at the activate path: one confirm plus five query hits gives standing 1 versus bid 6, and lbid selects through the standing record. Source-level adoption verified by byte-compare against the committed prototype.
- B3 (sealed probe prediction, 4 worlds x 20 probes = 80): accT = 50/80, accC = 50/80, margin = 0 points. Frozen bar: margin >= 15 points. KILL fires. Per-world: W1 0/20 vs 0/20, W2 20/20 vs 20/20, W3 20/20 vs 20/20, W4 10/20 vs 10/20. Post-ablation agreement 20/20 on all worlds with the tombstone white-box (records -44, lbid == bid) satisfied, so the ablation destroyed the (zero) advantage as required. The frozen H6R-B3-nil theorem predicted exactly this margin.
- B4 (retention): SUBSTRATE-INSUFFICIENT, not a mechanism fail. Exact gap: standing values live on kind-904 record nodes that are never protection-pinned (no ref_prot call in ls_touch; only facts and roots are pinned) and carry lbid 0 (their value sits in field 24, invisible to the lbid selector; their only in-edge is the type-10 root link, which bid does not count). The adopted evict_node selects argmin lbid over unprotected live nodes, so it always evicts standing records before any fact node. Sealed run evidence: B4-W1 first real eviction = node 6 (nH's standing record; nodes 2 = nH, 3 = nF, 4 = pacemaker, 5 = STAND_ROOT), not nF. Evicting a record destroys that node's standing (ls_find requires a live record), collapsing lbid to bid, so no world can express "high-standing nodes survive preferentially." The package pins roots but not records.
- P3 (determinism): 3/3 byte-identical reruns. sha256 01128d9af991d824595d127d963a35e9e283fa8b5bf47725197fd37497021bd7 on all three logs.
- P4 (K-C0A audit): zero new semantic cases in lane-added code. h6r_checks.zag is harness only (world drivers, asserts, the bid-argmax control replica, the tombstone ablation writer); no switch/match/case, no new kind-based branches, no new opcodes, no domain constants. The -44 tombstone is a measurement instrument required by the frozen kill rule, not cognition.

## Why B3 is nil (frozen theorem, confirmed)

Standing changes only on the activated fact; contradicts supersede; trailing nodes cannot accumulate standing; both the lbid-argmax and the bid-argmax therefore select the earliest-taught live node on every probe. The sealed worlds confirmed the mechanism works (B1/B2) while the prediction task cannot use it (B3 margin exactly 0). This tests whether the standing mechanism unblocks H6's hypothesis, per the carried governance questions; it does not decide them.

## Commits (local only, never pushed)

- 784b329eb8425a7d9d781c73530324801d21a299: PREREG freeze (KB-H6R unweakened; H6R-B3-nil prediction recorded)
- d8d73d3ecd0b8bf5c8d506eda75ebda88288cfa3: PREREG Amendment 1 (B4 pacemaker; pilot found the frozen filler re-pin was a no-op because decay removes the root's type-9 edge after 12 standing-free events and ref_prot cannot restore a removed edge)
- 5b46e84e212c05d4693dc37cc3e36e50263eaad4: PREREG Amendment 1 wording fix (R2/R3 even query counts)

Implementation and sealed-evaluation commits follow in the lane directory.

## Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/H6R/PREREG_H6R.md (frozen prereg + Amendment 1)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H6R/NAMECHECK.md (toolchain guard, pilot finding)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H6R/build_h6r.sh (mechanical extraction, byte-compare, pinned znc build)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H6R/pkg_block.zag (197-line PKG block, extracted from a11dde4b9)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H6R/h6r_checks.zag (sealed worlds, frozen before the run)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H6R/h6r_proto.zag (built source: substrate byte-identical to a11dde4b9 modulo dev harness)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H6R/h6r_run1.log, h6r_run2.log, h6r_run3.log (3 byte-identical sealed runs)

## Carried governance questions (not decided)

(i) Whether lbid's record-wins-else-bid default needs H6R override. (ii) Whether +1/-1 polarities must become learner-owned before H6R freezes. The experiment proceeded with the package as frozen researcher constants.
