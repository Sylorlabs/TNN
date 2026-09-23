# PAMs v2 — FORK × HYPOTHESIS COVERAGE MATRIX

**Date:** 2026-09-23
**Auditor:** coverage gap-audit (parent: PAMs v2 "test all forks and all hypotheses" directive from Micah)
**Scope:** `docs/lab/senses/pam-rebuild/v2/` on branch `tnn-native-lab` + stated hypotheses from the
committed autopsy/debate/diagnostic documents. A parallel PAMs v2 deep-dive coordinator is running
(Sol + Muse subagents); this matrix marks what it owns vs what gap crews were dispatched to cover.
Gap crews are additive-only: they never modify existing committed files and never touch
`~/workspace/v2work` (live V2-B build).

**Legend:** COVERED = preregistered battery executed, verdict committed. IN-FLIGHT = live work, do not
duplicate. GAP-CREW = dispatched by this audit to fill the gap.

## Fork × hypothesis matrix

| # | Fork / hypothesis | Stated claim | Prereg | Built | Executed | Result | Red-team | Status | Commit(s) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | V2-A "adjudicator" | 9.4%→85% gap is adjudication machinery, not gate strictness | ✅ frozen (`673cd3d1`) | ⚠️ PARTIAL — `vgate_a.zag` only; `vsense.zag`/`deliberate.zag`/substrates absent; red-team interim: does not build as committed | Battery run claimed | **DEAD on RK-3** — 65.88% (matches preregistered ~66% prediction); RK-1 0.01%, RK-2 0.09%, B5 0.00% | Coordinator Team 8b IN-FLIGHT (incl. build repair) | COORDINATOR-OWNED — do not duplicate | `VERDICT_V2-A.md` (LEDGER_VERIFICATION.md + RUNLOG.md still "to be added") |
| 2 | V2-B "interventional-port" | Intervention discriminates truth from spoof where passive gates can't; deciding ablation: full gate must cut false installs ≥0.2pp vs admission-only | ✅ frozen | 🔄 IN-FLIGHT — sibling crew building live in `~/workspace/v2work` (8 parallel `prun.py` perturbation runs, outputs writing every few sec as of 20:51 UTC) | — | — | — | GAP CREW C DISPATCHED — watch/poll for commit, verify prereg adherence + B6 + ledger, run ablation if skipped, red-team the interventional leg; adopt-and-resume ONLY if workdir dead >2h | — (none yet) |
| 3 | V2-C "knowledge-first" (Micah's hypothesis) | Fooled front end = knowledge gap; trap-signature teaching cuts adversarial wrong-HC | ✅ frozen (`61a6b877`) | ⚠️ PARTIAL — `vknow.zag` + byte-identical `memgate.zag`; **`vsense_c.zag` NEVER BUILT** | Python simulation only | KD-1 FAIL by sim (740 vs ≤537); RK-3 death expected | none | GAP CREW A DISPATCHED — prereg amendment, build `vsense_c.zag` + death-board structural detectors (PTC-2 gl_b, spectral AMDF, texcorr, texture-corr, MOT-2/3), calibrate on noise split, run full battery in pure Zag, red-team detectors | `VERDICT_V2-C.md` (sim-based) |
| 4 | V2-D "confidence-separation" | R2-4 conflated detection with adjudication; separated acceptance path clears RK-3 | ✅ frozen (`84329e15`) | ⚠️ PARTIAL — `vgate_d.zag` only | Battery run claimed | **ALIVE** — RK-3 88.48% (vs R2-4's 9.4%); RK-1 0.06%, RK-2 0.63%, B5 0.10%; 934 ACCEPT_INSTALL | Coordinator Team 8b IN-FLIGHT | GAP CREW B DISPATCHED — compute preregistered DD-1/DD-2 from committed evidence (read-only, additive) | `VERDICT_V2-D.md` (DD-1/DD-2 "to be added") |
| 5 | R2-4 death: knowledge vs machinery (Team 1) | CONFLICT_WITHHELD deaths = knowledge gap, qualified: pointwise adjudication is machinery-impossible | n/a (autopsy) | n/a | White-box replay cf1/cf2 | **KNOWLEDGE with qualification** — cf1 (corroborated revision) recovers all 621, 0 false installs; cf2 (naive revision) installs false permanent (seq 1145) | n/a | COVERED | `autopsy/AUTOPSY_R2-4.md` |
| 6 | Death-board: 12 PAM kills (Team 2) | 9 KNOWLEDGE / 1 MACHINERY / 1 UNRECOVERABLE / 1 BENCHMARK-BUG; zero "no detectable signal" | n/a (autopsy) | n/a | Autopsy measurements | Committed verdict table (H1,H2,H3,G1,G2,G3,R2-1,R2-2,R2-5,R2-10,R2-11,R2-11-R29) | n/a | COVERED (autopsy); rescue/detector claims → Crews A/D | `autopsy/AUTOPSY_DEATHBOARD.md` |
| 7 | KB4 channels C1 vs C2/C3 (Team 4) | Why C1 survived while C2/C3 retired | n/a (autopsy) | n/a | Channel autopsy | Committed | n/a | COVERED | `autopsy/AUTOPSY_KB4_CHANNELS.md` |
| 8 | Survivor mechanisms R2-3 + R2-8 (Team 3) | Load-bearing mechanisms for PAMs v2 (admission law, interventional program) | n/a | n/a | Mechanism extraction | Committed (v2 mechanism list) | n/a | COVERED | `autopsy/SURVIVOR_MECHANISMS.md` |
| 9 | Deep-dive diagnostic methodology | Self-application: diagnose R2-4/RK-3 (9.4%) with the instrumented harness | ✅ `PREREG_DIAG.md` | ✅ `diagnose.zag` | ✅ | `DIAG_VERDICT_R24_RK3.md` committed | n/a | COVERED | `diagnostics/` |
| 10 | Sol structured debates (Team 5) | Ranked v2 directions post steelman-reversal | n/a | n/a | 4 debate rounds + briefs | Committed (ranked directions, preserved disagreements) | n/a | COVERED | `debates/DEBATES_V2.md`, `DEBATES_V2_R2.md` |
| 11 | R2-5 threshold claim (death-board) | colordisc thr 15 vs optimal 5.0; 268/720 DIFFERENT missed avoidably (calibration failure) | none | — | — | — | — | GAP CREW D DISPATCHED — new fork `round2/forks/R2-5-thr50/`, pure-Zag battery, additive verdict | — |
| 12 | CCN-2 mislabel claim (death-board) | 338/340 CCN-2 fixtures mislabeled (truth SAME_SURFACE, pixels different photos) | none | — | — | — | — | GAP CREW D DISPATCHED — verify by measurement; quarantine PROPOSAL doc only (no frozen-fixture changes; those need Micah's amendment) | — |
| 13 | MOT-1 unrecoverable claim (death-board) | Benchmark premise flaw: frames reversed, label pre-reversal — truth unobservable from stimulus | none | — | — | — | — | GAP CREW D DISPATCHED — confirm generator/label relationship, document | — |

## Known evidence gaps (owned by the parallel coordinator — not duplicated here)

- V2-A: `LEDGER_VERIFICATION.md`, `RUNLOG.md` missing; committed src does not build (interim fix crew assigned).
- V2-D: `LEDGER_VERIFICATION.md`, `RUNLOG.md` missing; DD-1/DD-2 → Crew B (this audit).
- V2-A vs V2-D head-to-head: decided by Crew B's DD-1/DD-2 + bar table above (V2-D ALIVE 88.48% vs V2-A DEAD 65.88%).

## Laws applied to all gap crews

Pure Zag for mechanisms/learners/verification (Python: glue/analysis/calibration only); zero RNG in
any decision path; byte-identical reruns (B6); frozen prereg/amendment committed alone before any
build; commits to `tnn-native-lab` via `~/workspace/commit_racefree.py` (`TMPDIR=~/workspace/tmp_commit`,
lab-relative paths); no binaries, no `.zagd`; additive-only commits (never rewrite another crew's files).
