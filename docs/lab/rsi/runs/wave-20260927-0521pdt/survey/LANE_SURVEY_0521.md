# LANE SURVEY wave-20260927-0521pdt

Survey window: 2026-09-27 02:21 PDT to 2026-09-27 05:21 PDT.
Worker: lane survey (read-only git operations only; nothing committed, nothing pushed, .wave_lock untouched).
Run-start HEAD: ecbe9b5b7.

Verdict up front: no new prereg drafts, no design ideas, no re-aimed preregs, no new loop mechanism commits. 23 commits landed in the window: 9 authored by micahcooley (his own frontier work, CLOSED to the loop) and 14 authored by tnn-rsi-loop, of which 13 are the prior wave's (wave-20260927-0221pdt) closed workstreams plus the merge, and 1 is the prior wave's wave record with LOOP_STATE verdicts. The four prereg filename hits in the window all belong to the 0221pdt wave's frozen-and-executed workstreams (EXP1b, EXP2 follow-up, LIGHT-FIELD sensory); every one of them closed with a terminal verdict (EXP1b invention claim DEAD, LIGHT-FIELD KILLED clean, EXP2 narrowed to fidelity self-check with wire-in off the table). None of them is genuinely new candidate material for this wave. The stand-down holds for every lane.

## Verdict line

STAND-DOWN: no new mechanism. 23 commits in the window (9 his-frontier CLOSED, 14 loop: 13 prior-wave workstream plus merge, 1 prior-wave wave record). 4 prereg filename hits, all prior-wave preregs already closed with terminal verdicts. 0 preregs re-aimed, 0 new design documents, 0 lane-directory touches. 37 untracked entries (all residue, fixture material, lock, or empty; 0 drafts or design notes). Six lanes keep prior standing. Six governance rulings remain open and untouched.

## 1. New prereg drafts (name-status scan, window)

Four filename hits, each attributed to its commit and author. All are the wave-20260927-0221pdt loop workstreams, frozen and executed inside this window, now merged and judged:

- A docs/lab/invention/survival/PREREG_EXP1b.md, commit 7e0326d2c (tnn-rsi-loop, 02:34 PDT): EXP1b retune prereg (ceiling removal, literal primitive-action I arm, pure Zag; K1-K6 and C1-C3 carried from EXP1). LOOP_STATE verdict: invention claim DEAD, full certification WITHHELD. CLOSED.
- A docs/lab/onebrain/PREREG_WAVE0221.md, commit 06e28f088 (tnn-rsi-loop, 02:38 PDT): EXP2 follow-up prereg (broader holdouts, K4 hardening, regression sweep). LOOP_STATE verdict: adopted as FIDELITY SELF-CHECK record, NARROWED; wire-in stays off the table. CLOSED.
- A docs/lab/image_upscale/light_field/PREREG_LIGHT.md, commit 4a937d994 (tnn-rsi-loop, 02:41 PDT): LIGHT-FIELD sensory prereg (scene-illumination construction operator). M docs/lab/image_upscale/light_field/PREREG_LIGHT.md, commit c368b8e1f (tnn-rsi-loop, 02:47 PDT): the same commit that records the KILL verdict. LOOP_STATE verdict: KILLED clean by frozen bars (BAR1 FAIL sealed minus 1.853 dB, BAR2 FAIL checkerboard about 3x worse). CLOSED.
- A docs/lab/image_upscale/light_field/PREREG_AMENDMENT_1.md, commit c6b8190f3 (tnn-rsi-loop, 02:45 PDT): pre-run amendment (skycrop resized to 512x184 to match the frozen input protocol; no scores seen). Closed with the kill. CLOSED.

Prereg commit-order self-check, independently confirmed this wave: 7e0326d2c (09:34 UTC) precedes 938d188cb (09:49 UTC); 06e28f088 (09:38 UTC) precedes 32eadf722 (09:43 UTC); 4a937d994 (09:41 UTC) precedes aa76f9b8d (09:45 UTC); amendment c6b8190f3 is pre-run. PASS on all three, matching the 0221pdt LOOP_STATE claim.

No prereg was drafted for wave 0521pdt. No prereg anywhere in the window is a fresh design idea for this wave.

## 2. Design ideas (new design documents or proposals committed in the window)

None. The markdown files added in the window are either his frontier work (REDTEAM_R3.md, SWEEP.md, R4_PER_PROBE.md, upscale round-3 REDTEAM_REPORT.md, audio round-3 EVIDENCE/WHITEBOX/VERDICT, MP3 round-3 evidence) or the 0221pdt wave's red-team-mandated corrections (WAVE_NOTES_EXP1B.md, WAVE0221_JUDGE_NOTE.md, evidence_exp1b audit files). No design proposal, no candidate concept note.

## 3. Re-aimed preregs

None. `git log --diff-filter=M` over the window shows 9 commits with Modified files; none re-aims a loop prereg. The single prereg modification (PREREG_LIGHT.md in c368b8e1f) rides the kill verdict commit of the prior wave's sensory workstream. No existing prereg gained a new mechanism, addendum, or amendment. In particular, no D-VID re-aim with a different mechanism exists.

## 4. Merge-range characterization (23 commits, 02:21 to 05:21 PDT)

Nine authored by micahcooley, all his own frontier work, CLOSED (noted, never claimed, never re-certified):

- b257c02cc 02:27 PDT: WO-SR-1: repair production chunker 64-word cliff (pure Zag, zero RNG). Touches docs/lab/mg_chunking*/intake.zag plus WO_SR1_REDTEAM.md.
- 828bc6ee8 02:36 PDT: Native epistemics Phase 1: pure-Zag deliberation engine plus frozen learned readings plus Train-LOO (attempt 6). New docs/lab/epistemic_native/phase1/ tree.
- 4a7b8d6ce 02:38 PDT: Native epistemics: Train-LOO broker score plus NO-GO report.
- d1b943161 02:47 PDT: Audio round 3 (2026-09-27): MP3 32kHz honest kill plus planner walls verdict. Target of the independent red-team report below.
- 7aa40ac0d 02:59 PDT: Upscale round 3: FINAL, honest all-arm kill (VERDICT_R3.md amended, red-team report).
- 945b061b4 03:15 PDT: Deliberation fork-divergence repair, round 2 (38/38 R4). New deliberate_frozen_r4repair2.zag plus DIVERGENCE_REPAIR.md rewrite.
- ae965e697 03:16 PDT: Deliberation repair round 2: measurement-integrity amendment. DIVERGENCE_REPAIR.md and R4_PER_PROBE.md additions.
- 73411bdef 03:46 PDT: Determinism sweep: byte-identical reruns verified across all adopted batteries (docs/lab/determinism/SWEEP.md). Zero nondeterminism found; 4 battery/document hygiene work orders (see below).
- 7aad68fad 03:54 PDT: Audio round 3: independent red-team report plus SHA256SUMS manifest correction (REDTEAM_R3.md; manifest gap fixed).

Fourteen authored by tnn-rsi-loop, all prior-wave (0221pdt) process and workstream material, CLOSED:

- af657c8e5 02:24 PDT: merge origin/tnn-native-lab (52 commits ahead); 18 add/add conflicts in docs/lab/invention/survival/ resolved keeping both sides (canonical path keeps the tested version; origin lineage preserved as *.origin-wave.* with provenance headers); no Micah frontier files involved.
- 7e0326d2c 02:34 PDT: EXP1b prereg (frozen 2026-09-27).
- 06e28f088 02:38 PDT: prereg: Experiment 2 follow-up (broader holdouts, K4 hardening, regression sweep).
- 4a937d994 02:41 PDT: PREREG (frozen): LIGHT-FIELD scene-illumination construction operator, wave-20260927-0221pdt sensory.
- 32eadf722 02:43 PDT: wave0221: freeze new holdouts (S2 synergy, S3 slow-burn) and regression batteries.
- a2a36e657 02:45 PDT: wave0221: evidence and bar results (broader holdouts, K4-hardened, regression sweep).
- aa76f9b8d 02:45 PDT: LIGHT-FIELD implementation: azupscale_light.zag, azcrop.zag, azdb.zag (pure-Zag scorer with log10 self-test); support sources copied unchanged.
- c6b8190f3 02:45 PDT: PREREG amendment 1 (pre-run).
- c368b8e1f 02:47 PDT: LIGHT-FIELD verdict: KILL. Variant degrades sealed minus 1.85 dB and skycrop minus 0.68 dB (BAR 1 fail); checkerboard 3x worse (BAR 2 fail). Mechanism double-counts local illumination. No judge brief.
- 938d188cb 02:49 PDT: EXP1b implementation: 12 variants, literal-primitive I agent, runner, world bounce fix.
- 1010a63c3 02:50 PDT: EXP1b evidence: K1 PASS (380>376), K4/K6 KILL invention claim, K5 incomplete.
- 1bb09fd67 03:00 PDT: merge EXP2 follow-up branch (prereg 06e28f088, freeze plus impl 32eadf722, evidence a2a36e657).
- 771def6c3 03:00 PDT: merge sensory light-field branch (prereg 4a937d994, amendment c6b8190f3, impl aa76f9b8d, evidence c368b8e1f).
- 463b115b6 03:07 PDT: tnn-rsi loop wave-20260927-0221pdt: wave record, debate transcript, EXP1b corrections, EXP2 judge note, LOOP_STATE verdicts.

Zero loop-authored mechanism commits for this wave. The current wave's own dirs (forks/, interactive/, survey/) hold process evidence only. Branch check: no new workstream branches for wave 0521pdt; the three new branches (wave-20260927-0221pdt-exp1, exp2, sensory) are the prior wave's and are already merged.

Note: run-start HEAD ecbe9b5b7 is a tnn-rsi-loop merge of origin/tnn-native-lab stamped 05:22 PDT, one minute outside this survey window; it belongs to the next interval and was not surveyed here.

## SWEEP.md work orders (commit 73411bdef): zero nondeterminism, 4 hygiene items

The sweep verified byte-identical reruns across all adopted mechanisms (dialogue round-4, deliberation repair R4, one-brain round 3, epistemic native Train-LOO, promoted chunker, MP3 decoder, de-synth closure; upscale round-1 Phase-1 only). Verdict: no nondeterminism found anywhere. The 4 follow-up work orders are battery/document hygiene for the owning lines, explicitly NOT determinism failures, and no fixes were made by the sweep:

1. Text: 3 stale E-lines in docs/lab/dialogue/round4/battery_round4.txt (R4-01 t2 expects the pre-G6 confabulation; R4-01 t5 and R4-03 t4 predate adopted rendering). Byte-exact E-match is 26/29; the "23/23 good" adoption claim is qualitative. Also: the generality battery's E-lines are all literal `?` (runner FAIL marks there are meaningless), and the B20 battery at trace-trial/trial/battery20.txt is cited by path in no deliberation doc.
2. Intel: naming drift, round 3 is committed as docs/lab/onebrain3/ not docs/lab/onebrain/. Also: committed R33_NATIVE_IO_V1.zag under docs/generations/R33/ is darwin-flavored and fails linux builds; the working linux copy at docs/lab/onebrain3/impl/ should be the canonical one.
3. Image: Phase-2 outpaint deterministically broken, not nondeterministic (rc=1 with identical stdout every run: shapes regions 18, no border region at row 160). Root cause: rectangle-fix commit f67e98933 changed region tiling (36 to 18 regions); azoutpaint.zag:127-158 requires every output row to have a SHAPES region with rx+rw==256, which now fails at row 160. Committed evidence/SHASUMS.txt and OUTPAINT_TRACE.txt are stale (pre-fix). Regenerate or retire Phase 2 and refresh the evidence files.
4. Audio: frozen 34-driver Huffman / 33-frame stress rerun BLOCKED: the generators were never committed (STRESS_REPORT documents them as "in workdir, uncommitted"). Not a determinism fail, but the stress battery is unrepeatable until they are committed. Also: the extraction-window SHA in STRESS_REPORT did not reproduce under 10 plausible byte windows (documentation gap only).

## REDTEAM_R3.md headlines (commit 7aad68fad)

Independent red team against his commit d1b943161 (Audio round 3). Overall judgment: the round-3 evidence HOLDS on every technical claim, but the "trap still holds" conclusion is REFUTED by a red-team variant.

- Attack 1 (MP3 32 kHz mixed-block re-derivation): CONFIRMED strongly on two fixtures. Zag vs oracle: 99,072 samples, max 1 LSB, mean about 0.0002 to 0.0003 LSB; oracle mixed vs unflipped path non-vacuous (max 35,802 to 51,444 LSB). Byte-identical reruns. Oracle-shift formal analysis correct: my_sr is 6/7/8 for MPEG-1; the 12 kHz mixed row crashes even the oracle (IndexError), so the path is untestable in the reference. Qualification: the Zag decoder does not explicitly reject non-MPEG-1 version bits.
- Attack 2 (MP3 fixture regression, comment-only change): CONFIRMED. 7 fixtures byte-identical; diff parent to target shows exactly eight added comment lines, no executable change.
- Attack 3 (manifest checks): CONFIRMED (hashes valid) plus NEW FINDING (process): SHA256SUMS called itself a "manifest of every delivered file" but omitted zai_q1_answer.txt and zai_q1_question.txt. Corrected in this commit.
- Attack 4 (atom identities): CONFIRMED. All six current atoms match the committed claims.
- Attack 5 (planner battery re-derivation): CONFIRMED. Full 20-target batteries re-run; all scores exact; 13/13 WAVs byte-identical; analyzer spot-checks pass.
- Attack 6 (adversarial variants, spike-conditional median): V-A (preregistered 5 percent magnitude threshold) REFUTED: no magnitude threshold separates wins from regressions (t9/t10 disagree more than t12/t14 yet regress). V-D (post-hoc directional rule: use interp_median only if median > mean) NEW FINDING: the trap is broken. Full 20-target battery: t12 172 to 0, t14 146 to 0, total 8502 to 8184 (minus 318), ZERO regressions. Byte-identity proof: V-D t12/t14 WAVs equal candidate WAVs; V-D t5/t9/t10/t13 WAVs equal baseline. Interpretation: the candidate's error was unconditional median application, not the median itself. V-D is an existence proof, not a validated fix (post-hoc, no held-out test).
- Attack 7 (telemetry decomposition): CONFIRMED. Independent YIN and contour set confirm the tracker is about 250x too accurate to explain planner errors; the problem is narrowly the spike-corrupted mean statistic.
- Attack 8 (waveform audit): CONFIRMED. No anomalous artifacts.
- Attack 9 (Huffman / pow_43): CONFIRMED (linbits claim), with a precision footnote (pow_43_z 1.325e-6).
- Attack 10 (close-call hunt, mixed-block n_long_bands): REFUTED (no counterexample; the hardcoded 2 is exactly right for all MPEG-1 rows).

All of this is his frontier work. Noted as CLOSED; the V-D directional rule is his own existence proof, not a loop candidate.

## 5. Untracked residue (git status --porcelain: 37 entries, 0 modified, 0 staged)

Classification of every untracked entry:

- Old binary/frame/bin residue from older waves: wave-20260923-2021pdt/ and wave-20260924-0221pdt/ untracked dirs; wave-20260924-0521pdt/dvid1v2/frames_base/ and frames_v2/; wave-20260924-0521pdt/freelunch/bin/; wave-20260925-0221pdt/dvid1_geomchurn_v3/ (band_bin, ocean_base_bin, dist_bin, ocean_v3_bin, v3_sha_bin, v3_verify_bin, frames_v3_r1/r2/r3, foam_dbg/, baseline/frames_base/, substrate/); wave-20260925-0521pdt/intel_trade/impl/ (cv1c_base, cvp, gate_op_base) and intel_trade/tools/ (score, stemcheck); wave-20260925-0521pdt/sensory/st1/ (bin_dry, bin_st1, bin_verify); wave-20260925-1121pdt/intel_trade/impl/comp2 and tools/pair_enum.
- His-frontier fixture material (his sensory rebuild work, not loop): docs/lab/senses/rebuild/corroboration/ and docs/lab/senses/rebuild/harness/fixtures/{_photos, t1_colordisc, t2_colorconst, t3_shapetrans, t4_pitchdisc, t5_timbredisc, t6_motiondir}/.
- err.txt at repo root: empty file, no content.
- .wave_lock at repo root: timestamp lock file. Present and untouched by this worker.

Zero entries look like a draft, prereg, or design note.

## Per-lane standing (all unchanged)

- G1 (sunshafts): STOOD-DOWN. No new design idea. Zero lane-directory touches in the window.
- D-VID-1: STOOD-DOWN. No re-aimed prereg with a different mechanism.
- CV-P: barred pending his governance ruling 6. Unchanged.
- COMP-2: ruling 6 open; P11 stemmer-contingency unresolved. Unchanged.
- B1-class: P9 bar reformulation not found. Unchanged.
- ST-1: DEAD on pristine evidence. Unchanged.

## Queued-item blocker check (carried from wave-20260927-0221pdt)

- EXP1c (needs a real compositional-choice design: shrunk plan space, longer horizon, or decaying B0): zero EXP1c material anywhere in the repo. Blocker NOT cleared.
- EXP2 (grounding in real deliberation failures plus K4 hardening against the rescuer lens): nothing new this wave. The K4-hardening in a2a36e657 is the closed 0221pdt wave record itself; no new grounding work committed. Blocker NOT cleared.
- Frozen enumeration manifest for the fork battery (process item, fork worker's): no manifest committed in this window (the only new manifests are his MP3/SHA manifests). NOT cleared.

## Governance and sealed pairs (untouched)

The six governance rulings (S7 strike, MD-SSD-1, S11 pull, S11-AUD pull, C12 queue, Python-mirror logic) remain OPEN. Nothing was decided, relitigated, or re-presented. The sealed blind pairs (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform) were not touched. DP-1's repaired sealed blind pair is ready; its presentation to his ears is a parent-agent queue decision, not this wave's.

## Survey result

STAND-DOWN: no new mechanism [RE-CERT]. Counts: 23 commits in the window (9 his-frontier CLOSED, 14 loop: 13 prior-wave workstream plus merge, 1 prior-wave wave record); 4 prereg filename hits, all prior-wave preregs closed with terminal verdicts (EXP1b invention claim DEAD with certification withheld, LIGHT-FIELD KILLED clean, EXP2 narrowed to fidelity self-check); 0 preregs re-aimed; 0 new design documents; 0 lane-directory touches; 37 untracked entries (0 drafts or design notes); 6 lanes stood down unchanged; 6 governance rulings still open.

Proposed verdict line for the wave debate:

STAND-DOWN [RE-CERT]: no new mechanism this wave. 23 commits in the 02:21 to 05:21 PDT window are 9 Micah-frontier (CLOSED) plus 14 loop, of which 13 are the closed 0221pdt workstreams (EXP1b DEAD, LIGHT-FIELD KILLED, EXP2 narrowed, wire-in off the table) and 1 is the wave record with LOOP_STATE verdicts. Zero new prereg drafts, zero re-aimed preregs, zero new design documents, zero lane-directory touches, 37 untracked residue entries with no drafts. All six lanes hold prior standing; all six governance rulings stay open and untouched; no queued-item blocker cleared.
