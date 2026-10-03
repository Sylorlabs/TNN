# LANE SURVEY wave-20260926-1721pdt

Survey window: 2026-09-26 14:21 PDT to 2026-09-26 17:21 PDT.
Worker: lane survey (read-only). Commit nothing.

Verdict up front: no new prereg drafts, no design ideas, no re-aimed preregs, no new candidates. The stand-down holds for this wave. All six lanes keep their prior standing. His six governance rulings remain open and untouched; they were not relitigated.

## 1. Commits in docs/lab/rsi/ during the window

Exactly one commit landed in the window:

- e8b913584 (wave-20260926-1421pdt: evidence batch (spot re-run, fork battery, FIT, interactive survey, lane survey, DP-1 blind pair, debate transcript, judge-ordered P18 brief repair))

A second commit, a222f8f17 (wave-20260926-1421pdt: LOOP_STATE verdicts (6 motions ruled; P18 sealed-blind protocol minted; DP-1 pair repair applied)), sits inside the window and touches only LOOP_STATE.md outside docs/lab/rsi/. Its 6 motions are loop-internal (P18 protocol minting, DP-1 pair repair); they do not touch his six governance rulings.

## 2. prereg/design filename hits in the window

`git log --name-status` over the window, grepped case-insensitively for prereg|design, returned zero hits. No prereg or design file was touched in the window.

## 3. Prereg inventory

All existing preregs, newest first by wave:

- wave-20260925-1721pdt: PREREG_DP1_1721.md (newest prereg overall)
- wave-20260925-1121pdt: PREREG_COMP2_1121.md, PREREG_B1_1121.md
- wave-20260925-0821pdt: PREREG_D2_0821.md
- wave-20260925-0521pdt: PREREG_CVP_0521.md, PREREG_ST1_AUD.md, PREREG_ST1_AUD_ADDENDUM_A1.md
- older waves: PREREG_CV1_FALLBACK_0221, PREREG_DVID1_V3_2321, PREREG_G1_SHAFTS_1721 (plus sign addendum), PREREG_CV1_CITE_1721, PREREG_G1_SHAFTS_1421, PREREG_CV1_CITE_1421, PREREG_SENSE_BIGLEVER_1121, PREREG_KB4_TAIL_1121, PREREG_INTELTRADE_1121, PREREG_M4R2_T2VETO_1121, PREREG_SECONDPATH_PARTE_0521, PREREG_DVID1_V2_0521, PREREG_C_D19_0521, plus legacy preregs outside runs/.

Design docs: autonomous_run_2/design_subject_loop.md, autonomous_run_2/design_teaching.md (both legacy).

No prereg or design file postdates the window. Nothing new was frozen.

## 4. Genuinely new files on disk

Every file newer than 14:21 PDT under docs/lab/rsi/ belongs to the wave-20260926-1421pdt evidence batch, committed in e8b913584:

- debate/ADVOCATE_BRIEF.md, debate/SKEPTIC_REPORT.md, debate/JUDGE_RULINGS.md
- dp1/blind/: JUDGE_BRIEF_DP1.md, LISTENING_DP1.md, SEALED_MAPPING_DP1.md, pair_41tIYv.wav, pair_RGLaA4.wav
- fit/FIT_1421.md
- forks/FORK_RESULTS_1421.md plus forks/evidence/ archives
- interactive/INTERACTIVE_1421.md
- survey/LANE_SURVEY_1421.md

No new prereg drafts and no design notes on disk.

## 5. Uncommitted material

`git status --short docs/lab/rsi/` shows 27 untracked entries, zero of them matching prereg|design. All are build artifacts and frame/binary residue from older waves:

- untracked wave dirs: wave-20260923-2021pdt/, wave-20260924-0221pdt/
- dvid1 frame and binary residue: dvid1v2/frames_base/, dvid1v2/frames_v2/, dvid1_geomchurn_v3/ (band_bin, frames_v3_r1/r2/r3, ocean_base_bin, ocean_v3_bin, dist_bin, v3_sha_bin, v3_verify_bin, foam_dbg/, baseline/frames_base/, substrate/)
- intel_trade impl and tool binaries: intel_trade/impl/cv1c_base, cvp, gate_op_base, comp2; tools/score, tools/stemcheck, tools/pair_enum
- sensory st1 binaries: bin_dry, bin_st1, bin_verify
- freelunch/bin/

There are no uncommitted prereg drafts and no uncommitted design ideas. No .wave_lock. No scratch dirs.

## 6. Merge range 28ec31ab0..45d449a56

His three frontier commits are CLOSED and are not loop candidates:

- 28ec31ab0: Audio de-synth: measured-timbre renderer replaces synth (2026-09-26)
- c094d7770: Upscale concept probe: behavioral C1-C4 gate through TNN intake (2026-09-26)
- 39bf8d5d4: Upscale concept probe -> teach -> re-probe: PASS, concept HELD (C1-C4)

The same origin-side merge (45d449a56) also pulled in more of his own work, all CLOSED: c5d01683c (head placement, no secret crew hardcodes), cf1a42f6b (dialogue round-3 chat), 86132c3a0 (image-issue diagnostician), ce15343fb and dee44ecb6 (generation audits), eb1586771 and 2c01cdea3 (abstention work). None of these are loop preregs or candidates; none are claimed or re-certified here.

Loop-work mechanism-like material inside the range: two commits, both from wave-20260925-1721pdt (Sept 25, before this survey window), both sensory audio lane:

- 18ad30fe3: DP-1 doppler flyby frozen prereg (pre-implementation)
- 02d1dcb31: DP-1 doppler flyby implementation plus evidence (READY-FOR-JUDGE)

DP-1 is tagged [NEW] in its own prereg (constant-velocity flyby rendered through a time-varying propagation delay on the D-AUD-3 bed). It is candidate-adjacent but already known: 1121pdt held it in the judge queue (modified-cert NEW, queue-HELD), and 1421pdt applied a DP-1 pair repair under the minted P18 sealed-blind protocol. Nothing new this window.

All other loop commits in the range are process evidence, not mechanisms: evidence batches, LOOP_STATE verdicts, debate transcripts, fork battery results, FIT evidence. No other mechanism-like loop-work was found.

## 7. Re-aimed preregs

None. Each of the seven lane preregs was checked individually with `git log --since` over the window; all are untouched:

- PREREG_DP1_1721 (wave-20260925-1721pdt)
- PREREG_D2_0821 (wave-20260925-0821pdt)
- PREREG_COMP2_1121 (wave-20260925-1121pdt)
- PREREG_B1_1121 (wave-20260925-1121pdt)
- PREREG_ST1_AUD and PREREG_ST1_AUD_ADDENDUM_A1 (wave-20260925-0521pdt)
- PREREG_CVP_0521 (wave-20260925-0521pdt)

No new sections, addenda, or amendments were added to any of them.

## Per-lane standing (unchanged)

- G1 (sunshafts): STOOD-DOWN. No new material this window.
- D-VID-1: STOOD-DOWN. No new material this window.
- CV-P: barred pending his governance ruling 6. No rotated-author re-test. Unchanged.
- COMP-2: ruling 6 open; P11 stemmer-contingency unresolved. Unchanged.
- B1-class: P9 reformulation not found. Unchanged.
- ST-1: DEAD on pristine evidence. Unchanged.

## Survey result

New prereg drafts: no. Design ideas: no. Re-aimed preregs: no. New candidates: no. Stand-down confirmed for wave-20260926-1721pdt.
