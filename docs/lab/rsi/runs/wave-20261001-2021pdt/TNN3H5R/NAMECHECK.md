# NAMECHECK TNN3H5R (H5 re-prereg, writing only)

Lane: TNN3H5R. Wave: wave-20261001-2021pdt. Worker role: drafting fresh prereg for H5
(return via VOID discipline: fresh prereg + fresh sealed worlds only).

## Step 0. Toolchain verification (Worker Toolchain Guard)

1. Ran `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`.
   Output: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python). znc OK.
2. `export PATH="$HOME/safebin"`.
3. `which python3` prints NOTHING (exit 1). Confirmed absent from safebin PATH.
4. This task is WRITING ONLY: no implementation files, no binaries, no compilation,
   no forbidden executables invoked. Only two new files in the lane directory:
   NAMECHECK.md and PREREG_H5R.md.

## Scope of this lane

- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
- Write ONLY inside docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5R/.
- No git operations (coordinator commits). No push. No writes to TNN3H5/.
- Documentation rule: no em-dashes anywhere.

## Step 1. Context read (before drafting)

Read, in full, before writing the prereg:
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/PREREG_H5.md (killed prereg)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/SEALED_EVAL.md
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/REDTEAM_REVIEW.md (kill verdict dbf25e447)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/SHADOW_DIAGNOSIS.md (committed at 71b09b624)

## Step 2. Draft PREREG_H5R.md incorporating ALL diagnosis requirements

1. MAP-key pinned for all behavioral bars; exact (s,r) key convention stated.
2. Frozen white-box bar: zero live tag-1 facts on (s,r) at MAP-key probe time.
3. Behavioral bar: twice-corrected value on MAP-key query after double contradiction,
   with re-derivation demonstrated (white-box: mp_run reached, or MAP miss then fresh promotion).
4. Exact CON counts, control-live, wrong-key checks (red-team calibration gap).
5. Fact-key KB-B2/KB-B3 bars dropped or re-anchored as fact-key-specific with correct baseline.
6. Substrate option pinned: Option A (MAP node as retrieval structure) or Option B
   (provenance-linked shadow fact superseded with MAP). NEVER freeze
   activate/promote_graph/ev_teach_in unchanged while claiming MAP-key re-derivation.
7. Mandatory substrate verification section quoting exact lines to change.
8. Sealed family requirements for post-freeze independent adversary.
9. Falsifiable prediction and kill conditions.
10. Process bars, architecture bars, three-valued verdict, commit-order self-check.

## Step 3. Draft complete (2026-10-01)

PREREG_H5R.md written. All 10 diagnosis requirements incorporated.
No em-dashes in either lane file (verified by grep).

Substrate option pinned: Option A. promote_graph no longer teaches the
shadow fact (delete line 551 ev_teach_in call); activate admits
non-superseded tag-20 MAPs on the key via (f8,f4)==(s,r); the MAP node
itself is the retrieval structure answering from f28. Option B not
authorized in this prereg (needs a fresh prereg); Option C stays
rejected per the H5 Q1 ruling.

Frozen bar list: KB-W0 (white-box primary: zero live tag-1 facts on the
MAP key across 36 probe snapshots, answer sourced from the live tag-20
MAP), KB-S1 (substrate gate, pre-run diff check), KB-W1R (exact 8
guide-CON, 4+4), KB-S1R (control-live), KB-S2R (wrong-key), KB-B1R
(8/8 ev_act zero), KB-W2R (per-probe exact 2 superseded + 1 live MAP,
12/12), KB-B2R (16/16 twice-corrected on MAP key), KB-B3R (4/4 MAP-key
revert), KB-R1R (12/12 retention), KB-G1R (architecture accounting),
KB-D1 (determinism), KB-P1 (process). Fact-key KB-B2/KB-B3 dropped as
non-discriminating. Verdict three-valued: ADVANCE / KILL / VOID.
