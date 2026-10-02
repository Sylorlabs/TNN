# PREREG: C8/C12 surface-transfer test (wave-20261002-0521pdt, ARENA lane)

Status: FROZEN PREREG. Committed alone before any transfer
contestant build, run, or score in this lane. Any change to the
design below requires a dated amendment committed alone before
the changed code runs. Commit-order rule: this file's commit must
strictly precede every implementation commit for the transfer
test in this lane. Kill bars never move after this commit.

## 1. Objective: the single highest-information next experiment
for C8 and C12

State of the board (prior sealed verdicts):
- INQ (C8 inquiry candidate): C8 4/4 = 1.000, total 58/68 = 0.853,
  K1-K9 PASS (wave-20261001-2321pdt ARENA SEALED_EVAL.md).
- REMAP (C12 procedure candidate): C12 6/6 = 1.000, total
  60/68 = 0.882, K1-K4 PASS (wave-20261001-2321pdt ARENA2
  SEALED_EVAL.md).

Both mechanisms are at 1.000 on their capability in the frozen
world. Further frozen-world tuning would be benchmark polishing,
not information. The open question for each is surface
generality: does the mechanism survive changed surface
representations (different entity names, words, attribute values,
remap tables, segment values) with zero code changes, or is it
coupled to the frozen world's surface?

The D5-fixed world (fixrun2, GEN-PASS this wave, C9D5FIX_EVAL.md)
is the transfer substrate: its non-causal subsystems are
logic-identical to the frozen world (C9FIX F6), but the RNG stream
position differs downstream of the causal draws, so entity names,
Zem words, attribute values, and the remap table all differ. The
C8 items keep the scripted double-test-turn plus observe_result
structure; the C12 items keep the remap_prod/remap_class forms.
No contestant source changes are made for this test: this is a
measurement of the committed mechanisms' generality, not an
intervention. Per the ONE-SYSTEM rule, a pass here is evidence
the mechanisms are not surface-coupled handlers; a fail is an
honest negative about surface generality (not a process
failure).

## 2. Frozen design

Contestants (rebuilt, never modified):
- INQ: source extracted via `git show` from implementation
  commit 0ddb5e9ce
  (docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA/inq_contestant.zag);
  built with the pinned znc; binary must be byte-identical to the
  sealed binary sha256
  09f59dcbee0fcd443a911f2bf24bff883960f457d0ce9acd59506d3c38339b1d.
- REMAP: source extracted via `git show` from implementation
  commit 18309290c
  (docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA2/remap_contestant.zag);
  built with the pinned znc; binary must be byte-identical to the
  sealed binary sha256
  4a80837a2ad90779c156584ec0be80aabc548ac6c29e5ec91d940ce010ec9a21.

Substrate: fixrun2/ (this lane; GEN-PASS). Scorer: arena_512
(this lane; cross-validated byte-identical results.json vs the
frozen scorer on the 131-turn world; see SEALED_EVAL_C9.md).

Protocol per contestant:
1. Rebuild from the committed source; verify byte-identical to
   the sealed binary (T5 gate: any mismatch aborts the test).
2. 3 runs on fixrun2 with fresh state each (same driver pattern
   as run_sealed.sh, arena_512 scoring).
3. Strip volatile fields (ms, rss_kb); verify 3/3 byte-identical
   stripped reply streams.
4. Record per-capability scores; compare against the v6 baseline
   on fixrun2 (54/68 = 0.794, measured this wave in
   SEALED_EVAL_C9.md).

## 3. Kill bars (frozen; never move after this commit)

T1 (C8 transfer): INQ scores 4/4 on the C8 items in fixrun2.
T2 (C12 transfer): REMAP scores 6/6 on the C12 items in fixrun2.
T3 (no regression): INQ total >= 54/68 on fixrun2 AND REMAP
total >= 54/68 on fixrun2 (the v6 baseline total on the same
world; the v6 baseline is not re-run, its fixrun2 score from
SEALED_EVAL_C9.md is reused with citation).
T4 (determinism): 3/3 stripped reply streams byte-identical per
contestant.
T5 (purity): both rebuilt binaries byte-identical to their
sealed binaries; zero contestant source changes; pure Zag
(`which python3` returns nothing).

TRANSFER-PASS requires T1 through T5 all PASS. Any bar failing
yields TRANSFER-FAIL with the killing evidence named. A T1 or T2
failure is recorded as an honest negative about surface
generality and queues a mechanism-coupling investigation; it is
not a process failure and does not authorize a patch.

## 4. Scope honesty

fixrun2 comes from the same generator family as the frozen world
(same code, different RNG stream positions). This test measures
surface transfer, not broad generality: a pass does not
establish that INQ or REMAP survive new world families, new
inquiry forms, or new procedure families. No L3 claim, no
TNN-beats-LLM claim, no canonical-score claim. FW1-FW9 remains a
regression battery only.
