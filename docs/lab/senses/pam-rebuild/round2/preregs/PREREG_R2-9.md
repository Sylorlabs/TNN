# PREREG R2-9 — Witness-Emission PAM (C-EC1)

**Status: FROZEN 2026-09-22. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_C_sensory_output.md` §9 EC1 (commit 891f4dae). Hypothesis text and KB-E1..KB-E5 below are copied verbatim from the debate.
**Verdict carried:** round-2 forks emit sensory output under the WITNESS (replay-only) contract — replay-only, never generate; replay is identity, so no renderer is under test.

## 1. Hypothesis under test (verbatim from DEBATE_C §9 EC1)

> **EC1 — Witness-Emission PAM (replay-only, selection-emitting)**
>
> **The hypothesis.** Every percept carries an emission mapping: the exact source span (audio) or region (visual) the PAM claims to have witnessed. The fork emits bit-faithful replays of those selections — nothing more. No synthesis, no enhancement, no invention. Emission is read-only: the percept pipeline cannot see or be steered by the emission path.
>
> **Kill bars (preregistered, applied mechanically unless marked human):**
> - **KB-E1 — byte-identity (mechanical, all trials):** every emitted artifact is byte-identical to its cited source span/region; emissions byte-identical across 3 full reruns. Any divergence kills.
> - **KB-E2 — no phantom emission (mechanical, all trials):** every emission cites a non-empty selection owned by a percept; no emission without a claiming percept. Phantom output kills.
> - **KB-E3 — human equivalence (human, frozen stratified sample, double-blind):** audio — the judge cannot distinguish PAM replay from direct source playback (≥90% "same" judgments; threshold inherited from H1's frozen bar). Visual — the emitted crop is judged to contain the annotated event and exclude the distractor (≥80% vs. frozen human annotations of the sample).
> - **KB-E4 — spoof-catch (human, adversarial sample):** on fixtures with injected false percepts (decoys, metamers, occlusions, glide-through-threshold), the three-way comparison (claim vs. emission vs. source) must let the judge detect the mismatch on ≥90% of injected false percepts. This operationalizes position (e).
> - **KB-E5 — no-interference (mechanical, ablation):** percepts and install/withhold dispositions byte-identical with emission on vs. off. Any difference kills the fork immediately.

## 2. What is built

- Pure-Zag percept pipeline as in R2-1, PLUS the emission mapping: every percept carries the exact source span (audio byte range) or region (visual pixel rect) it claims to have witnessed. The emission path is read-only on the percept pipeline (one-way data flow; the pipeline cannot see or be steered by the emission path).
- A byte-faithful replay emitter: audio = exact bytes of the cited span; visual = exact pixels of the cited region. No synthesis, no enhancement, no invention.
- A `sense` CLI: fixture bytes in → percept records + emission artifacts + dispositions out, hash-chained ledger.

## 3. Fixtures

- Frozen suite R2A per `R2_FIXTURE_SET.md`: 10,000 trials (5,000 normal + 5,000 adversarial). KB-E1/E2/E5 run mechanically on all 10,000.
- Frozen human sample (for KB-E3/E4): 200 trials — 100 clean, 100 adversarial — stratified across the 18 attack families, frozen and committed BEFORE the fork build begins. The fork cannot see the sample (Goodhart handling). Adversarial 100 drawn from decoy/metamer/occlusion/glide-through-threshold families (R2A-SHP-1, R2A-SHP-2, R2A-COL-1, R2A-PTC-2, R2A-MOT-2, R2A-CCN-2).
- Sample SHA256 committed with this prereg's build design; presentation order randomized double-blind at trial time.

## 4. Bars (all preregistered; mechanical unless marked human)

- **B1 viability:** mean primary accuracy on the frozen 370 harness primary ≥ 60%.
- **B2 vs Approach A:** head-to-head judgment-accuracy delta on identical fixtures; reported.
- **B3 efficiency:** ops and bytes per percept vs Approach A (measured); emission bytes counted.
- **B4 no-interference (LOAD-BEARING HARD KILL — this hypothesis's form):** ablation per KB-E5 — percepts and install/withhold dispositions byte-identical with emission on vs. off. ANY difference kills the fork immediately. (For this hypothesis the contract's load-bearing claim is read-only emission; the ablation tests exactly that.)
- **B5 KB4:** false permanent installs ≤ 3% on the 10,000 trials (RK-1 analog).
- **B6 determinism (HARD KILL):** ≥3 runs byte-identical (KB-E1 subsumes this for artifacts; B6 covers percepts/dispositions/ledger), hash-chained ledger verified.
- **B7 beauty — FINALLY EXERCISED (this hypothesis emits):**
  - (i) mechanism elegance — judged against the hypothesis's own beauty claim: faithful, clean selection — the beauty of testimony, not of painting; replay is identity, one obligation doing the work of audit, defense, and beauty.
  - (ii) human verdict per the shared protocol (§5 below): KB-E3 (≥90% audio "same"; ≥80% visual selection-honest vs frozen annotations) and KB-E4 (≥90% spoof-catch on the adversarial sample). Micah's verdict outranks metrics on the sample. Below-threshold human agreement kills the fork even if every metric passes.

## 5. Kill criteria (KB-E1..KB-E5, hardened) + the shared human-verdict protocol

1. KB-E1: any emitted artifact diverging byte-for-byte from its cited span/region, or any emission differing across 3 reruns → dies.
2. KB-E2: any emission without a claiming percept, or any emission citing an empty selection → dies.
3. KB-E3: human ≥90% "same" on audio replay vs source; ≥80% on visual selection honesty vs frozen annotations → below kills.
4. KB-E4: ≥90% mismatch detection on injected false percepts via the three-way comparison → below kills.
5. KB-E5 (= B4): emission on vs off must be byte-identical in percepts and dispositions → any difference kills immediately.
6. B4 and B6 are HARD KILLS: fails B4 → dies; fails B6 → dies.
7. **No retroactive bar changes after results.** Frozen before the build; amendments go to Micah.

**Shared human-verdict protocol (DEBATE_C §9, frozen):** (1) trial set, presentation order, stratification, thresholds frozen before the build; (2) mechanical bars before human ears — KB-E1/E2 failures never reach the human trial; (3) pre-delivery consistency gate on every audio artifact (envelope stationarity, spectral drift, loop-periodicity, transient regularity, calibrated against real field recordings — standing rule); visual boundary sanity; (4) every trial ships the brief — claim, boundaries, warrant; (5) double-blind randomized presentation, source interleaved, judge blind to fork and metric predictions; (6) stratified 200-trial sample (100 clean / 100 adversarial); mechanical bars run on the full 10,000; (7) his verdict outranks metrics on the sample — below-threshold kills even if metrics pass; above-threshold does not rescue a mechanical-bar failure; (8) batched scheduling, verdicts recorded verbatim with attribution.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-9.md` (committed ALONE — no src, no evidence).
- Build output (later, separate commits): `senses/pam-rebuild/round2/forks/R2-9/`: PREREG copy, src/, evidence/ (incl. emission artifacts + briefs + human-verdict records), LEDGER.md.
- Shared fixtures: `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language, max-risk posture.
