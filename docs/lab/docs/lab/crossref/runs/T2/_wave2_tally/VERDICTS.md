# Wave-2 verdict tally (2026-09-23)

## T2-WEBV2 — REPRODUCED
- Every leg figure re-derived exactly with independent Zag code; R-CORR vs R-CONTRA distinction holds; unanimous-spoof residual exactly as described.
- Caveat: lumy.live 10/10 probe bar has no committed machine JSON (prose table only); corroborated 22/22 recorded queries pass KB-LIVE's bar. No leg figure affected.
- Pins: prereg 7b2100d09911c5c10252c5756c7def288e70bd1f; evidence ff97c7a08fcbac3f832498456c51d28e82146d5d.
- Deliverables: ~/workspace/scratch-crossref/T2/WEBV2/crew/VERDICT.md, RUNLOG.md

## T2-RAWVSHUMAN — REPRODUCED
- In-bin attribution: colordisc 505/506 = 99.80%, pitchdisc 131/132 = 99.24% (both ≥99% bars hold); independent Zag re-derivation, 3 byte-identical runs.
- Rescue forks both <1pp and DEAD at both budgets: B2 vocab growth +0.278pp / 0, B3 fuzzy edges +0.833pp.
- Context: ops ratio 2.42 ✓, B−A gap −27pp ✓, KB4 false-installs A 48.2% / B 54.5% (both fail ≤10% bar) ✓.
- Pins: prereg a87ddfd4..., diagnostics 8954577204f5..., forks 31c68a56fe7c... (all 2026-09-22).
- Deliverables: ~/workspace/scratch-crossref/T2/RAWVSHUMAN/crew/VERDICT.md, RUNLOG.md

## T2-RSI1 — REPRODUCED
- Replication completed via hash-verified committed blobs (a mid-run git fetch died; recorded in RUNLOG, no impact on verdict).
- Deliverables: ~/workspace/scratch-crossref/T2/RSI1/crew/VERDICT.md, RUNLOG.md

## T2-BUGREAD — REPRODUCED
- KB-D1C compiler parity 24/24; KB-D1 30/30 with 0/8 false alarms; KB-D2 30/30; beyond-compiler 6/6; 5-rep byte-identical (digest 2bccc18e… matches committed).
- Curriculum-gap premises verified line-by-line in committed code (zero bug knowledge taught, learner never saw compiler output, no memory, 8 authored repair rules); rearchitect trigger correctly did NOT fire.
- Tripwire (pre-labeled repairs) does NOT fire — battery genuinely tests reading-by-inference.
- Pins: evidence a978fdc90638...; prereg 7b2100d09911c5c10252c5756c7def288e70bd1f (local copy byte-identical, API-verified).
- Deliverables: ~/workspace/scratch-crossref/T2/BUGREAD/crew/VERDICT.md, RUNLOG.md

## T2-JOKE — REPRODUCED (frozen PARTIAL stands)
- Every bar matches: joke catch solo 1/6 (K1 kill-bar tripped, arm-specific) / helper 4/6; satire 6/6 both; hoax 5/6 / 3/6; controls 0/6 all; non-sincere installed solo 1/30 (c3) / helper 3/30 (b1,c1,c5, at pass boundary); glue-on-pizza solo JOKING/withheld vs helper SINCERE/installed; reason honesty 30/30; ledger 32/62 chain OK; 5/arm byte-identical; all 10 outputs byte-identical to d7e59016 run files.
- Pins: prereg 7b2100d09911c5c10252c5756c7def288e70bd1f; freeze 8f33adac...; evidence d7e59016... (all API-verified).
- ANOMALY (flagged by crew): mid-run the entire clean/ tree (.git + worktree) vanished for unknown reasons; crew/ untouched; recovered via re-fetch + re-verification. Cause unknown.
- Deliverables: ~/workspace/scratch-crossref/T2/JOKE/crew/VERDICT.md, RUNLOG.md

## T2-PROSE — REPRODUCED
- All 25 run logs BYTE-IDENTICAL to committed (5 sources × 5 reps); DIGEST/DIGEST2/LEDGER hashes match.
- Viability: sol 220/228 (0.9649), step 204/228 (0.8947), muse 200/228 (0.8772), grok-4.6 189/228 (0.8289); extraction 240/240 all five; tie table matches exactly.
- Q(4.6)=1/456=+0.00219 → NO-DIFFERENTIATION; Q(4.7)=25/456=+0.0548 → QUALITY-MATTERS (boundary, holds under ±0.02 too); 4.7 viability 213/228=0.9342 still fails 0.98; both absorb 12/12 falsehoods; head-to-head +10.52pp.
- Pins: d4c151c7e39c..., fbecf64f08b6f5f41efbf33ef07384154cd48140 (both API-verified).
- Infra note: full git fetch OOM-killed under concurrent crew load (VM load ~26); crew used tree:0 commit fetch + sparse checkout with SHA-verified blobs. No source substitution.
- Deliverables: ~/workspace/scratch-crossref/T2/PROSE/crew/VERDICT.md, RUNLOG.md

## T2-TRACKR0 — REPRODUCED
- B-T1 FAIL stands; ordering holds; raw_micro 7/10 overall, 6/9 binding; repaired mean 0.8319, rank 7/11, still FAIL; heap-buffer overflow verified in pre-repair source; repair root cause = index overflow; 20/20 golden-hash agreement non-grounded arms.
- DISPATCH ARTIFACT (mine): the pins I gave (ce1e3b0b / bcd39f4b) do not exist in sylorlabs/TNN — crew correctly used the prereg's own pins (0489675d..., 18284131..., repair 53d5612c...). Not an evidence problem.
- Errata (verdict-neutral): REPAIR.md prose "raw_micro=8 of 10 binding" is wrong — committed rank_table_repaired.json and re-derivation give 7/10 binding (8 is the overall rank of 11). Plus 2.5e-7 rounding residuals and a 4-decimal truncation note.
- Open: B-T5 split-to-merge FAIL has no evidence supplied (outside prereg method/rule); artifact-driven suspicion recorded as open amendment case.
- Deliverables: ~/workspace/scratch-crossref/T2/TRACKR0/crew/VERDICT.md, RUNLOG.md

## T2-DUEL — REPRODUCED (SCENARIO-FIT, no champion)
- All figures exact: SG-PARA sol 96/192 vs grok 188/192; SG-WRONG grok 104/432 (0.2407, fails eligibility) vs sol 0; SG-SAFE 72/72 vs 66/72; SG-PREC 48/48 vs 16/48; grok's 104 decomposition identical; hybrid = grok cell-for-cell, no win; multi sol 0/24, grok 4/24.
- 5/5 byte-identical per contender; rebuilt binaries exactly the frozen sizes; my run-1 outputs cmp-clean vs committed evidence.
- Method note: full git clone infeasible (runtime killed long fetches); inputs fetched file-by-file at pinned SHAs via GitHub API — same bytes, independence held.
- Pins: prereg 7b2100d09911c5c10252c5756c7def288e70bd1f; claim e18a2ca13589...; build-freeze 6c520a990a01...; sealed battery 6978db0af55f...
- Deliverables: ~/workspace/scratch-crossref/T2/DUEL/crew/VERDICT.md, RUNLOG.md

## T2-HELLHOLE — REPRODUCED
- Ledger integrity: solo 409/409, helper 473/473 chain-clean; live == replay_n5 byte-identical both arms.
- Bars all match: solo M1 5/9 FAIL (K1 trips on C8,C11,C15,C16), M3 0/3 FAIL (K2 trips C5,C12,C13); helper M1 7/9 FAIL (K1 trips C8,C15), M3 0/3 FAIL (K2 trips); K3/K4/K5 clear both. Binding FAIL confirmed.
- Attribution: 19 NEC total, ranking M1>M3>M2>M4. Counterfactuals all identical to committed. Negation: inversion NECESSARY for 0/6 K1 installs; C3 false REJECT kill confirmed.
- Erratum (verdict-neutral): CONTRACT.md prose on hash canonicalization (sorted newline-joined k=v) is wrong; committed ht_supervise.py hashes prev+"\n"+etype+"\n"+tab-joined escaped k=v in field order. Verifiers follow the code.
- SECOND VANISHING-TREE ANOMALY: clone tree disappeared mid-run (recreated, HEAD re-verified). Same pattern as T2-JOKE. Flagged for investigation.
- Pins: prereg 7b2100d09911c5c10252c5756c7def288e70bd1f; phase-2 83d62d8f...; whys 1d6d5faa...
- Deliverables: ~/workspace/scratch-crossref/T2/HELLHOLE/crew/VERDICT.md, RUNLOG.md

## T2-DIALOGUE — REPRODUCED
- 370/370 all sections PASS; response digest 35aaae8ac1bbf764... exact; 5/5 byte-identical; my logs byte-identical to committed full_1..5.log; committed oracle 8/8 sections 100%, 0 errors.
- Pin-clarity note (record, not re-litigate): src/experiments/R33_NATIVE_IO_V1.zag at the frozen commit is the macOS/Darwin build — unusable on Linux. Build used the committed Linux x86-64 port from docs/lab/prose-learning/src/ (byte-identical to the original crew's build dir). Future pins must name the Linux-port path.
- Infra: full clone repeatedly died (remote SIGKILL on pressured VM); blob-filtered single-commit fetch succeeded.
- Deliverables: ~/workspace/scratch-crossref/T2/DIALOGUE/crew/VERDICT.md, RUNLOG.md

## T2-SELFTEST — REPRODUCED
- 40/40 and 400/400 oracle fidelity; 5/5 byte-identical at both scales (md5-identical to committed logs); overhead exactly 0.0127×; silent-skip fault blocked by both binary and oracle; per-battery verdicts exact (B1 240 PASS, B2 12 PASS, B3 96 PASS, B4 48 PASS, B5 UNRUNNABLE, B6 PASS, T1 239 TRIP, T4 47 TRIP).
- Honest caveats (from frozen doc's own doc-sweep): B6 oracle ASSERTS digest equality rather than recomputing (real coverage 35/40, 350/400); T1 ≤2.0 overhead bar is non-informative (0.0127 is 157× under it).
- THIRD VANISHING-TREE ANOMALY: 463MB clean clone vanished ~05:21, not in trash, 68GB free, cause unknown. Recovered via depth-110 blob:none re-fetch + read-only inspection of TQ crew's clone. Pattern now: JOKE, HELLHOLE, SELFTEST.
- Pins: prereg 7b2100d09911c5c10252c5756c7def288e70bd1f; claim 334444eb94d8... (API-verified).
- Deliverables: ~/workspace/scratch-crossref/T2/SELFTEST/crew/VERDICT.md, RUNLOG.md

## T2-INFORICH — REPRODUCED
- All figures re-derive: facts-only absorbs 12/12; read-only installs 0/12, catches 12/12, 4/4 provisional unknowns; corroboration-gated installs 0/12 falsehoods, 12/12 true values, 4/4 unknowns; colluding-domain spoofs still install 2/2 (sensor-deceivable boundary). Three verification legs (rebuild byte-identical, 140/140 extraction cross-check, independent Zag verifier 20/20). All 7 frozen kill bars PASS.
- SECOND DISPATCH PIN ARTIFACT: my template pin 23c4fc6ea5a9 does not exist (API 422, zero workspace occurrences). Crew correctly used the prereg's own pin 25c2a18b2416... per its authority. Audit of my dispatch pins needed.
- Observation (not a claim difference): manifest shows 7 pre-cap V-domains for F08/U02 but mechanism's view has 6 (documented if(n<6) cap drops two); prereg premise (≥2) holds either way.
- Pins: prereg 7b2100d09911c5c10252c5756c7def288e70bd1f; evidence 25c2a18b2416...
- Deliverables: ~/workspace/scratch-crossref/T2/INFORICH/crew/VERDICT.md, RUNLOG.md

## T2-SCALEDOWN — REPRODUCED
- All three preregistered gates hold: clean mastery 1.0000 at N=1/2/8/192 (1/1, 2/2, 7/7, 179/179); one-shot planted lie absorbed 1/1; recall latency constant in N (173–377 ns/probe, 11–24× faster than install).
- 30/30 run logs byte-identical to committed (timing line excluded); 5/5 reps identical per leg; all six SCALE_DIGEST fnv1a match; deciles identical.
- Cross-checks: N=240 P=3 validation matches scale-up VERDICT row; N=24,000 leg matches committed s2_r0.log byte-identical except expected `,off=0` CFG field. 6,585,360-fact endpoint NOT re-run (non-interference: ~8h CPU on shared 2-vCPU VM).
- Pin 2d367807d806 API-verified EXISTS.
- Deliverables: ~/workspace/scratch-crossref/T2/SCALEDOWN/crew/VERDICT.md, RUNLOG.md

## T2-TQ — REPRODUCED
- All 10 checks match: 17/17 self-contradictions REJECTed at R1; end-state digest identical to Q1B (6317c2dc... both); no knee — 49/49 at 25%, 99/99 at 50%, filtered=0 at every level; §B.7 blind to value noise (96/96 flaw battery at 0/25/50% while mastery falls 192→143→93).
- N=5 byte-identical on all 4 legs; stdout SHA-256 matches committed n5_sha256.txt; run1 cmp-clean vs committed.
- Pin 107f6ca108fbe9a6bf30a8c22dd168b798a8f791 API-verified EXISTS.
- Deliverables: ~/workspace/scratch-crossref/T2/TQ/crew/VERDICT.md, RUNLOG.md

## T2-IMAG — REPRODUCED
- All 7 checks match: 36/36 both modes, 2/36 control, 6/8 vs 4/8 MARGINAL no-winner, 12/12 both video modes; Q4 blind ratings excluded per prereg.
- Byte-identity vs committed SHA256SUMS verified.
- Pin a39aadf API-verified EXISTS.
- Deliverables: ~/workspace/scratch-crossref/T2/IMAG/crew/VERDICT.md, RUNLOG.md

## PIN AUDIT (2026-09-23 ~06:10 UTC)
Brief pins verified via GitHub API commits endpoint:
- EXIST: 2d367807d806 (SCALEDOWN), a39aadf (IMAG), 4be6b0cf128d (PROSEV3), 107f6ca1 (TQ), 84df6dc24483 (SENSESH2H), ccbb3d3c39d7 (PARAMS)
- MISSING (422 No commit found) — all from replacement batch briefs, transcription artifacts: e7c5bcd6 (HTD1), 02ffbc1be27a (TRACKA), 8d0d6b9e9c9c (TRACKB), b9d7a6 (CHAMP), d50bf92cd9e8 (CLASS3DEC), e3c2b9cc34e8 (CERT), ddc9a1b04f1a (SENSESINT), 5d1a3d0cfd (GOALB), e15eebc5c4ec (AUDIOCONT), 1b27f5+e6d1b7b (HELLHOLE), ce1e3b0b+bcd39f4b (TRACKR0), 23c4fc6ea5a9 (INFORICH)
- Completed crews (TRACKR0, INFORICH, HELLHOLE) correctly fell back to prereg's own pins per §1. Corrections sent to all still-running affected crews; GOALB re-dispatched with prereg-pin instruction.

## VANISHING-TREE ANOMALIES (4 crews)
JOKE, HELLHOLE, SELFTEST, SENSESINT — clean/ or clone trees vanished mid-run, not in trash, disk free. All recovered; verdicts sound. Cause unknown; monitoring.

## VANISHING-TREE INVESTIGATION (2026-09-23 ~06:19 UTC)
- VM uptime only 32 min → reboot at ~05:47 UTC (matches daemon-restart wave).
- Disk healthy: /home/hatch 37G/100G used (63G free); /tmp 52M/512M.
- Symptoms differ: SENSESINT's clean/tnn/ was EMPTY (dir present, contents gone); JOKE/SELFTEST lost entire trees incl .git. SELFTEST's loss ~05:21 (pre-reboot); others' timing unclear.
- No conclusion yet. All crews recovered; no verdict affected. Grep for rogue rm -rf across scratch tree running in background.

## T2-TRACKB — PARTIAL (16th verdict; first non-REPRODUCED in Wave 2)
- All 11 frozen claims re-derived: 25/25 independent Zag checks PASS, 3/3 byte-identical; pcodec FROZEN_DECODE_PASS re-derived from rebuilt W5 verifier, 3/3 byte-identical.
- PARTIAL comes SOLELY from the frozen rule's named condition: the arm-3 rebuild's three PASS variants (varA 7d056be, varB d7929bb, varC f0031d9) create genuine ambiguity about which is "the" arm — parked as GOVERNANCE CALL #1 for Micah. Nothing failed; no bar misapplied.
- Crew had already independently disregarded my bad brief pin before my correction arrived; all prereg pins API-verified (47c48d3e7cf9f, 89745ce1117c, d921459a, 4a6d898c1e66 + 6adb2fa5930c).
- Per Micah's rule a PARTIAL never ends a track.
- Deliverables: ~/workspace/scratch-crossref/T2/TRACKB/crew/VERDICT.md, RUNLOG.md

## T2-IMAG — REPRODUCED (formal handoff; matches file-read log)
- Caveat: frozen section attributes the video battery to a39aadf, but Q1V exists there only as a PROPOSED amendment — built/run/committed at 4d1a40ecaa (~19 min later). Diff proves purely additive (207 insertions, Q1/Q3 untouched). Recommend amending frozen pin to a39aadf + 4d1a40ecaa.
- Caveat: Q2 (12/12, 12/12, 24/24) is committed evidence but not in frozen claims — not rerun.
- VANISHING-TREE MECHANISM HYPOTHESIS: IMAG crew reports "a stale git clone from a timed-out attempt wiped the recreated clean/ mid-task" — zombie clone processes racing recreated checkouts may explain several vanishings.

## T2-TQ — REPRODUCED (formal handoff; matches file-read log)
- Ops note: ~34 orphan git clones from the daemon restart wedged disk I/O ~40 min. Cleanup survey pending.
- TQ crew made no box commit (left to parent; commit races live tonight).

## VANISHING-TREE INVESTIGATION — CONCLUSION (2026-09-23 ~06:25 UTC)
- Grep for rogue "rm -rf" across scratch tree: nothing suspicious — only old committed lab harness scripts (R5 doc-stage, m8_gate.sh, run_smoke.sh etc.). No cleanup culprit.
- Best hypothesis remains IMAG crew's: zombie `git clone` processes from timed-out attempts racing recreated checkouts (a stale clone "wiped the recreated clean/ mid-task"). All 4 vanishings involved crews doing clone retries under VM pressure.
- Disk healthy (61G free). No orphan-clone crisis found (HTD1 4.2G + PROSEV3 3.2G checkouts belong to RUNNING crews — do not touch). Monitoring continues.

## T2-PARAMS — REPRODUCED (17th verdict)
- Type A full rerun: 19 configs (59 runs) at 24,000 facts, pure Zag, zero RNG. All 59 run logs BYTE-IDENTICAL to committed.
- 16/19 configs byte-identical learner digest 8e6238911bb7cef0; the 3 differing (slot025, slot05, jsmall) are sub-1× slot-capacity configs differing by stored-set size, not behavior — 16/19 ≥ 16 bar met.
- Cost multipliers all match: slots ×0.25/×0.5 exactly proportional (clean prefix cut at cap, zero corruption); depth2/depth4 5.000/7.000 ops; red2/red4 6.000/10.000 ops, 3.3× memory; evidence/audit/jbig change cost only. Falsehoods absorbed 1.0 at every config; flaw battery 96/96 all 19; det=OK 19/19.
- Procedural note: full clone impossible (network); clean checkout assembled per-file at pinned SHA via raw.githubusercontent — driver blob SHA matches pinned blob; fidelity gate reproduced committed bytes before sweep.
- Pin ccbb3d3c39d70924c8e2e2463cb5fb7057f19616 API-verified EXISTS.
- Deliverables: ~/workspace/scratch-crossref/T2/PARAMS/crew/VERDICT.md, RUNLOG.md, runs/ (59 logs)
## T2-PARAMS — REPRODUCED (17th verdict)
- Type A full rerun: 19 configs (59 runs) at 24,000 facts, pure Zag, zero RNG. All 59 run logs BYTE-IDENTICAL to committed.
- 16/19 configs byte-identical learner digest 8e6238911bb7cef0; the 3 differing (slot025, slot05, jsmall) are sub-1x slot-capacity configs differing by stored-set size, not behavior — 16/19 >= 16 bar met.
- Cost multipliers all match: slots x0.25/x0.5 exactly proportional (clean prefix cut at cap, zero corruption); depth2/depth4 5.000/7.000 ops; red2/red4 6.000/10.000 ops, 3.3x memory; evidence/audit/jbig change cost only. Falsehoods absorbed 1.0 at every config; flaw battery 96/96 all 19; det=OK 19/19.
- Procedural note: full clone impossible (network); clean checkout assembled per-file at pinned SHA via raw.githubusercontent — driver blob SHA matches pinned blob; fidelity gate reproduced committed bytes before sweep.
- Pin ccbb3d3c39d70924c8e2e2463cb5fb7057f19616 API-verified EXISTS.
- Deliverables: ~/workspace/scratch-crossref/T2/PARAMS/crew/VERDICT.md, RUNLOG.md, runs/ (59 logs)

## T2-AUDIOCONT — REPRODUCED (18th verdict)
- All six dispositions match: sol-H2 seams KILLED (299/300 edges; 3/4 measures oppose, p~0.98-1.00 against); grok46-G3 KILLED (Wilcoxon one-sided p=0.1875->0.19 exact); sol-H3 VOID/INDETERMINATE; sol-H1 REFINED (sign-test p 0.942340/0.868412 exact); grok46-G1 REFINED (ratios 0.71-2.16 <2.4); grok46-G2 REFINED (min ratio 1.19 <2.7, no monotonic decline). No hypothesis warranted v4 recomposition.
- Flagship scans independently re-measured: B-beta 590ms @28.71s, B-gamma 1300ms @28.70s — byte-identical to committed scan records; instrument cross-checked vs numpy.
- EVIDENCE GAP (bounds this replication): the raw Type-A render battery is NOT re-executable from committed sources — r2g.zag/r2b harness, patch/analysis scripts, renders, scan records never committed (only redscan.zag was), despite frozen prereg promising "fixed sources committed after." Replication = independent re-measurement + exact statistical re-derivation.
- Pins: test head 070c94cb4608..., red-team f2c7b85e8f4..., round-2 prereg 9d1dbf865e36..., flagships 42cb573023d3...
- Deliverables: ~/workspace/scratch-crossref/T2/AUDIOCONT/crew/VERDICT.md, RUNLOG.md, crew/evidence/

## T2-CERT — REPRODUCED (19th verdict)
- 0 flips re-derived in pure Zag (rows=35, flips=0, confirmed=34, void=0, artifact_fail=0, inconclusive=1); 3/3 byte-identical.
- dirty1_urandom gap root-caused: committed plant source calls nio_open_readonly + _zag_rand, both unknown to the pinned toolchain — that binary is unreproducible from frozen evidence (artifact limitation, not a verdict flip).
- Pin method note: frozen T2-CERT section names no SHA pins ("crew freezes the pin"); pins used came from the committed evidence chain (MASTER_ERROR_LEDGER.md, VERDICT.md header) — cadacc199684..., 26b86329b53b..., all API-verified. My bad brief pin e3c2b9cc34e8 confirmed 422.
- Deliverables: ~/workspace/scratch-crossref/T2/CERT/crew/VERDICT.md, RUNLOG.md

## T2-SENSESINT — PROVISIONAL PARTIAL (stood-down crew's finding; crew of record 247aa7b5 still adjudicating)
- Stood-down crew (f3e9de78) completed VERDICT.md/RUNLOG.md before stand-down: verdict PARTIAL.
- Finding: 10/140 manifest items have evidence paths absent from the frozen commit — including the 3 P0 GK trial sources (gk1/gk2/gk3_trial.zag), the load-bearing HTRF batteries behind "H1,H2,H3 all SUSTAINED" and the headline digests 488af9ab.../7f351a53.../94575a9a.... 7 P2 internet-trial phase1 jsonl files also absent. 2 manifest size mismatches (kb5.py manifest 2189 vs committed 2731; +1 more).
- COORDINATOR INDEPENDENT CHECK (2026-09-23 ~06:45 UTC): GitHub contents API at frozen commit 7b2100d0... — gk1_trial.zag returns genuine HTTP 404; directory listing of docs/lab/senses/web-search/v2/src/ shows ws2_* files but NO gk*_trial.zag. Core finding CORROBORATED.
- Frozen rule: "PARTIAL if any item's evidence is missing (name it)." This looks like a REAL evidence gap, not a pin artifact. Final verdict awaits crew of record 247aa7b5.

## T2-HTD1 — REPRODUCED (20th verdict)
- Every kill/survive entry re-derives from frozen preregs with bars applied exactly as written (independent pure-Zag re-derivation, zero RNG, 3x byte-identical, SHA 68f6ae67...).
- E-DE1/DE2/DE3 KILLED; E-DE4-narrow SURVIVES/broad KILLED; E-DE5a PASSES/DE5b KILLED/DE5d PASSES; E-LG1 PASS; E-LG2 PASS K=64/256 FAIL K=16; E-LG4 PASS; G-CO2 PASS; G-CO3 PASS (contract-dependent); G-CM1c over G-CM1d; G-CM1b eviction PASS; E-DE2+E-DE4 composition; E-SP research plan not executed (explicit gap as stated).
- ANOMALY (verdict-neutral): prereg pin-swap — frozen section labels G-CM1b 16a2574f3d and E-LG1 1005582b5c, but branch history proves the REVERSE. Labels transposed only; both verdicts PASS; evidence correct.
- GOVERNANCE NOTE: G-CO3 PASS rests on the weighted reading (0.686 >= 0.60); raw 0.499 < 0.60 would KILL. Micah has not ruled raw ops.
- Pins: prereg 7b2100d0..., sheet 8d74c47b5737 (prereg's own pin; my bad e7c5bcd6 retired).
- Deliverables: ~/workspace/scratch-crossref/T2/HTD1/crew/VERDICT.md, RUNLOG.md

## T2-SENSESINT — PARTIAL (CONFIRMED by crew of record 247aa7b5; 21st verdict)
- Crew of record independently confirmed the stood-down crew's finding and adopted PARTIAL.
- 10/140 manifest evidence paths absent from frozen commit (3 P0 GK trial sources gk1/gk2/gk3_trial.zag — load-bearing HTRF batteries; 7 P2 internet-trial phase1 jsonl). Coordinator independently corroborated via GitHub API (genuine 404s; dir listing has ws2_* but no gk*).
- 2 manifest size mismatches: kb5.py 2189->2731, run_all.py 4302->5801.
- All other claims hold (140-row TSV re-derives, VERDICT_SHEET present, 5/5 spot-verification substrings, §9/§12 verbatim).
- SENSESINT alone suffered THREE vanishing-directory incidents (crew/ev/ scratch dir vanished mid-session). Anomaly class confirmed recurring.
- Frozen rule: "PARTIAL if any item's evidence is missing (name it)." Real evidence gap.
- Deliverables: ~/workspace/scratch-crossref/T2/SENSESINT/crew/VERDICT.md (+ §9 addendum), RUNLOG.md

## T2-CLASS3DEC — REPRODUCED (22nd verdict)
- Verdict remains REPRODUCED on API-verified pins. The frozen T2-CLASS3DEC section contains ZERO pins (claims/method/rule only) — the sole authority is the frozen prereg commit 7b2100d0... (API-verified). My bad brief pin d50bf92cd9e8 confirmed 422, was never used for anything.
- Deliverables: ~/workspace/scratch-crossref/T2/CLASS3DEC/crew/VERDICT.md, RUNLOG.md

## T2-GOALB — REPRODUCED (23rd verdict)
- Type A (rebuilt story_all.zag with pinned znc): B1 coverage 16/16 (POS 8/8, DEL 8/8); B3 novelty 16/16; B4 leakage PASS (0/16 >=16-byte substrings, read-only source audit); B5 determinism PASS; 3 fresh-process runs byte-identical (sha256 9dd1c20c...) AND byte-identical to committed runs/rep1.log. Negative control re-run live (deleted-word story correctly flagged).
- Type C (B2 independent re-derivation, judges not re-run): DEL 4/8 at two-judge mean >=3.5; POS 0/8; bar >=6/8 -> FAIL both variants. sol DEL 6/8/POS 0/8; grok DEL 0/8/POS 0/8; control 5/5 both. All figures exact; prompt md5 matches 7e79199c...
- DESTRUCTIVE ARTIFACT (final-report item): the committed score_b2_combined.py CLOBBERS clean/evidence/b2_combined.md when re-run. Crew detected, restored blob from API, re-swept 32 files clean. The scorer is destructive on re-execution.
- Caveats: B3 corpus = kb.txt + battery.txt only (prose-learning/v3/inputs3* absent at evidence commit); grok-4.7-for-4.6 substitution accepted from committed record (panels unrepeatable by prereg design).
- Pins: prereg 7b2100d0..., evidence commit 5c1bf2a8babe2197160d5c092298bdb946d8bc67 (API-verified).
- Deliverables: ~/workspace/scratch-crossref/T2/GOALB/crew/VERDICT.md, RUNLOG.md

## T2-TRACKA — REPRODUCED (24th verdict)
- Body count 16/20/13/3 re-derives textually from pinned verdict 1706708005a9; Y5 7/8 via independent Zag check (3x byte-identical, SHA 170d6cee..., VERIFY=PASS). All sampled kill applications correct; 52-arm correction verified; D-family provisional unambiguous. No binding kill misapplied.
- I1 ADJUDICATION (RESOLVED, not punted): I1 = KILLED. Chronology: 8feb65b "survives" -> 3af67c0 kill-ii SURVIVE (synthetic corpus) -> 1706708 PROVISIONAL -> 0741530 (14:05, KILLED, binding kill (ii)), ancestor of frozen head. Deciding evidence: prose maintenance-churn 24,164/109,295 = 22.1% > frozen 20% bar -> kill (ii) fires. The prereg's "I1 SURVIVES" is stale (matches superseded 8feb65b); its own "F-B, R2, I1 killed" phrase is correct.
- CORRECTIONS (verdict-neutral): "F-S SURVIVES" -> actually PROVISIONAL; "10x legs blocked" -> Y5's 10x complete at f225a71f; Y5 provisional (pinned) -> CONFIRMED at frozen head (sheet counts 17/21/11/3 there); footer "48->53" arithmetically wrong (49 rows, B->3, C->2).
- Pins: prereg 7b2100d0..., closeout 1706708005a9 (API-verified), R-kill 76849610b8 (API-verified). My bad brief pin 02ffbc1be27a confirmed nonexistent.
- Deliverables: ~/workspace/scratch-crossref/T2/TRACKA/crew/VERDICT.md, RUNLOG.md

## T2-SPEEDINTEL — REPRODUCED (25th verdict)
- Coding (budgets 2/4/8/16 x 3): 6/18 -> 18/18 -> 18/18 -> 18/18; canonical digests match frozen prefixes; iters 32/46/46/46; identical x3.
- Epistemic (frozen 94, budgets 1/2/4/8 x 3): 29/94 -> 59/94 -> 59/94 -> 59/94; mean preds 3.000/9.000/9.319/10.319; recon 0, vflips 0; identical x3; all 12 committed out_b*.txt byte-identical with a fresh build.
- Fresh battery (SI-A1): sweep 29/94 -> 59/94 -> 59/94 -> 59/94 — PLATEAU-CONFIRMED.
- Exchange rate (Arm 4): knee+all winners 18/18, 46 iters, 28 znc (-37.8%), 45 evals (-65.1%) — identical x3; precheck FP 0/51; gates 6/6 on all three rebuilt binaries. 4x/8x buy nothing; 2x holds the knee; exchange-rate claim holds at byte-identical quality.
- EVIDENCE GAP: delib_si.zag's R33 imports were NEVER committed (absent at SI results commit and frozen pin). Substituted canonical in-lab copies (41 IO copies all identical variant; 37 SHA256 copies all identical variant). Behaviorally proven: all 12 committed outputs byte-identical with fresh build.
- Procedural: per-file API fetch with 27/27 blob SHAs verified (full clone stalls on this VM); predecessor left only a corrupt empty clone (removed).
- Deliverables: ~/workspace/scratch-crossref/T2/SPEEDINTEL/crew/VERDICT.md, RUNLOG.md

## T2-CHAMP — REPRODUCED (26th verdict)
- All class figures re-derived in pure Zag: class-4 0.9911 (six boxes x 12 reps), class-3 SWE 0.9921, class-2 0.9911 (x 5 reps), class-1 0.9253, curated flags 12/12 FP 0, bestof faithfulness/legB/legC; 1,140-row zero-split matrix. Three byte-identical runs (e4b45499...).
- Pin correction recorded: b9d7a6 confirmed transcription artifact (422, 0 hits everywhere); all work ran on prereg authority from the start.
- Deliverables: ~/workspace/scratch-crossref/T2/CHAMP/crew/VERDICT.md, RUNLOG.md

## T2-PROSEV3 — REPRODUCED (27th verdict)
- KB3-VIABLE FAIL (2/4) fully reproduced from clean rebuild. Battery: 220/220 logs byte-identical; 5 reps per run, all identical, zero RNG.
- Rebuild fidelity (strongest form): prose_learn3 a5cff7cde60074176b5a1c480ea58ed263fb22514c0a29992301e8b4ae82dc72 and prose_learn2 8dbb02fda28f32f88f10e2aa23668c308efd4b59d5369697e210b71cf8e1a901 both byte-identical to SHAs in committed src/PROOF.md. 303/303 packaged files verify against committed checksums.sha256.
- Headline (independent pure-Zag verifier, 17/17 assertions): A3 grok 183/228, sol 204/228, step 208/228, muse-native 227/228 vs frozen v1 189/204... A3 beats v1 on step + muse-native only -> 2/4 -> KB3-VIABLE FAILS.
- Deviation footprint all match: CORE 11/24->22/24 with 5+6 causal attribution (fixed set {2,3,5,7,9,10,13,16,17,18,23}; narrow-trigger diagnostic proves 6 come from unregistered its/these/those + "the word"/"the letter" expansion); wrong-value 8->30/912; unknown/other misses 523->60 (463 converted); SUB-DISTR 65/240->199/240; PARA 48/48; CONTR 24/24; MULTI 24/24; ABS-3 9/12,11/12,11/12,11/12; NOSILENT leaks=2.
- Procedural: SHA-verified codeload extract (no git clone feasible); ran 5 reps (stronger than committed 3+2); committed run_legs.sh symlink dependency handled via committed frozen v1 false_ids.
- Pins: prereg 7b2100d0..., evidence 4be6b0cf128d5a443c9e67486f63520816535cca (API-verified).
- Deliverables: ~/workspace/scratch-crossref/T2/PROSEV3/crew/VERDICT.md, RUNLOG.md

## T2-SENSESH2H — REPRODUCED (28th verdict — WAVE 2 COMPLETE)
- A viability 72.6389% -> 72.6% PASS; B 54.0278% -> 54.0% FAIL (killed by own KB1 bar); 18.611pp win, no tie; both 60/60 byte-identical x3 full pipeline runs; A memory FAIL 58.955% -> 59.0% (560 withholds); B 54.962% -> 55.0% (440 withholds); install-rule failure counts exactly 79/134 A, 72/131 B. NOT-REPRODUCED triggers not fired.
- Replication strength beyond claims: rebuilt sense_b md5 e6c98d091bbb0f90f54936b46bf849d8 BYTE-IDENTICAL to original crew's recorded binary; metrics.json field-by-field float-exact identical to committed harness/results/metrics.json (zero mismatches); fixture regeneration verified end-to-end 2020/2020 MANIFEST.sha256 OK (the regeneration the original VERDICT left unverified is now verified byte-identical).
- Incidents: predecessor's full-tree checkout died (git-remote-https SIGKILLed/OOM); clean/repo found deleted at 05:21 (cause undetermined); recovered via blob:none clone + sparse checkout. gen.py photo-fetch >2000-byte guard rejects 6 picsum seeds' small-but-valid JPEGs — downloaded directly, exact-match vs committed manifest.
- Pins: prereg 7b2100d0..., trial 84df6dc24483 (matches expected), znc pinned.
- Deliverables: ~/workspace/scratch-crossref/T2/SENSESH2H/crew/VERDICT.md, RUNLOG.md

---

# WAVE-2 FINAL: 28/28 resolved — 26 REPRODUCED, 2 PARTIAL
- PARTIALs: T2-TRACKB (arm-3 identity ambiguity; governance call #1 for Micah — nothing failed) and T2-SENSESINT (10/140 evidence paths missing incl. 3 P0 GK trial sources; 2 size mismatches).
- Wave-2 results NOT yet copied to docs/lab/crossref/runs/, added to VERDICT_TABLE.md, committed, or API-verified.
