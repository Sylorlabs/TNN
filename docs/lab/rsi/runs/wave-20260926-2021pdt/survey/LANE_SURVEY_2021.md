# LANE SURVEY wave-20260926-2021pdt

Survey window: 2026-09-26 17:21 PDT to 2026-09-26 20:21 PDT.
Worker: lane survey (read-only git operations only; nothing committed, nothing pushed, .wave_lock untouched).
Run-start HEAD: fe1b5e2c0.

Verdict up front: no new prereg drafts, no design ideas, no re-aimed preregs, no loop-authored mechanism commits. The stand-down holds for this wave. All six lanes keep their prior standing. His six governance rulings remain open and untouched; they were not relitigated.

## Verdict line

STAND-DOWN: no new mechanism. One commit touched docs/lab/rsi in the window (ba0487c2384bcf0b9b7ab930633b5336947d2145, the prior 1721pdt wave evidence batch), with zero prereg or design filename hits and nothing tagged [NEW]. The full merge range 45d449a56..fe1b5e2c0 is owner frontier work (16 micahcooley commits, CLOSED) plus the merge itself and the prior wave's own evidence and LOOP_STATE commits. Untracked residue (37 entries) is old binary/frame/bin residue and his-frontier fixture material, with no drafts, preregs, or design notes.

## 1. New prereg drafts (docs/lab/rsi, git log --since/--until over the window)

Exactly one commit landed in the window that touches docs/lab/rsi/:

- ba0487c2384bcf0b9b7ab930633b5336947d2145 (tnn-rsi-loop, 2026-09-27 00:35:06 +0000 = 2026-09-26 17:35 PDT): wave-20260926-1721pdt evidence batch (lane survey, fork battery with evidence archive, interactive survey, debate transcript). 870 files.

`git log --name-status` over the window, grepped case-insensitively for prereg|design, returned zero hits inside docs/lab/rsi/. No new prereg draft was frozen this wave.

Across the whole repo, prereg|design filename hits in the window are all owner-frontier work, authored by micahcooley and therefore CLOSED:

- Added: docs/lab/dialogue/trace-trial/trial/PREREG.md (his trace trial: English vs native reasoning traces, tied to commits 9cc616724, b5ec75e9d). It is his own frontier prereg, not a loop prereg.
- Deleted (8 files): docs/lab/docs/lab/consciousness_cost/preregs/ (DELIBERATION, KBCONTROL, PERCEPTION, REFUSAL) and docs/lab/senses/pam-rebuild preregs (PREREG_RT_X, PREREG_RT_OBJ4, PREREG_D1_STACK, PREREG_O3_REBRIEFED), removed by his de-synth cleanup commit 4f782c40d ("move files to correct location", fixing a doubled-path commit). A cleanup of his own work, not a loop signal.

## 2. Design ideas (new design documents or proposals committed in the window, commit dates in PDT)

No new design documents or proposals were committed in the window. The markdown files added in the window are all the prior wave's process evidence:

- debate/ADVOCATE_BRIEF.md, debate/SKEPTIC_REPORT.md, debate/JUDGE_RULINGS.md
- forks/FORK_RESULTS_1721.md plus forks/evidence/ archives
- interactive/INTERACTIVE_1721.md
- survey/LANE_SURVEY_1721.md

The judge rulings state explicitly that everything under judgment this wave is inherited and re-certified ([RE-CERT]), nothing is [NEW], and the DP-1 sealed pair remains queue-HELD [RE-CERT] after its 1421pdt repair. The LOOP_STATE verdicts commit (a4d4ff7cd) minted P19 coverage-delta accounting, which is loop-internal process bookkeeping, not a mechanism or design idea.

## 3. Re-aimed preregs

None. A per-file scan of every prereg under docs/lab/rsi/runs/ with git log over the window returned zero modifications, and `git log --diff-filter=M` over the window shows no prereg filename modified anywhere in the repo. No existing prereg gained a new mechanism, addendum, or amendment. In particular, no D-VID re-aim with a different mechanism exists.

## 4. New mechanism commits outside his frontier (merge range 45d449a56..fe1b5e2c0)

The range contains 19 commits:

- 16 authored by micahcooley: his own frontier work and CLOSED (noted, never claimed, never re-certified). Includes MP3 Fable work (f6e630ef5, bc8c5586c, c8599659e, 88980f802, a01f5aa11), the audio de-synth planner rebuild (8c73c34ea, c136004b2, 4f782c40d), dialogue round-4 repairs (5a76d07f8, 75267f9df), the reasoning-traces trial (9cc616724, b5ec75e9d), TNN-on-placement scaffold-and-release (1f74010ce), the upscale honest-loss commit (380e1ff2d), and diagnostician v2 (9d70369ac).
- 3 authored by tnn-rsi-loop: the merge itself (fe1b5e2c0), the prior wave evidence batch (ba0487c23, evidence only), and the prior wave LOOP_STATE verdicts (a4d4ff7cd, 4 motions ruled on process items).

Zero loop-authored mechanism commits. Workers do not commit; confirmed again this window.

## 5. Untracked residue (git status --porcelain: 37 untracked entries, 0 modified, 0 staged)

Classification of every untracked entry:

- Old binary/frame/bin residue from older waves: wave-20260923-2021pdt/ and wave-20260924-0221pdt/ untracked dirs; wave-20260924-0521pdt/dvid1v2/frames_base/ and frames_v2/; wave-20260924-0521pdt/freelunch/bin/; wave-20260925-0221pdt/dvid1_geomchurn_v3/ (band_bin, ocean_base_bin, dist_bin, ocean_v3_bin, v3_sha_bin, v3_verify_bin, frames_v3_r1/r2/r3, foam_dbg/, baseline/frames_base/, substrate/); wave-20260925-0521pdt/intel_trade/impl/ (cv1c_base, cvp, gate_op_base) and intel_trade/tools/ (score, stemcheck); wave-20260925-0521pdt/sensory/st1/ (bin_dry, bin_st1, bin_verify); wave-20260925-1121pdt/intel_trade/impl/comp2 and tools/pair_enum.
- Owner-frontier harness fixture material (his sensory rebuild work, not loop): docs/lab/senses/rebuild/corroboration/ and docs/lab/senses/rebuild/harness/fixtures/{_photos, t1_colordisc, t2_colorconst, t3_shapetrans, t4_pitchdisc, t5_timbredisc, t6_motiondir}/. These belong to his research frontier, not the loop.
- err.txt at repo root: empty file, no content.
- .wave_lock at repo root: timestamp lock file (2026-09-27T03:22:04Z). Present and untouched by this worker.

Zero entries look like a draft, prereg, or design note.

## Per-lane standing (all unchanged)

- G1 (sunshafts): STOOD-DOWN. No new design idea.
- D-VID-1: STOOD-DOWN. No re-aimed prereg with a different mechanism.
- CV-P: barred pending his governance ruling 6. Unchanged.
- COMP-2: ruling 6 open; P11 stemmer-contingency unresolved. Unchanged.
- B1-class: P9 bar reformulation not found. Unchanged.
- ST-1: DEAD on pristine evidence. Unchanged.

## Survey result

STAND-DOWN: no new mechanism. Counts: 1 commit in docs/lab/rsi during the window (0 prereg|design filename hits); 19 commits repo-wide in the window (16 his-frontier CLOSED, 3 loop process/merge); 0 preregs frozen, 0 preregs re-aimed; 37 untracked entries (all residue, fixture material, lock, or empty; 0 drafts/design notes); 6 lanes stood down unchanged; 6 governance rulings still open.
