# PREREG R2-11 — Test-both head-to-head: replay vs generative emission (C-EC3)

**Status: FROZEN 2026-09-22. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_C_sensory_output.md` §9 EC3 (commit 891f4dae). Hypothesis text, KB-E7, KB-E8 below are copied verbatim from the debate.
**Standing rule applied:** test-both when in doubt (Micah). The (a)-maximalist position gets its empirical trial as the explicit challenger to R2-9.

## 1. Hypothesis under test (verbatim from DEBATE_C §9 EC3)

> **EC3 — Test-both: replay vs. generative emission, head-to-head**
>
> **The hypothesis.** Per the standing test-both rule, the (a)-maximalist position gets its empirical trial: build the generative-emission fork as the explicit challenger to EC1 — a PAM+renderer hybrid that reconstructs the scene from the compressed percept (renders the percept, not the span). The no-interference bar applies (percepts identical with renderer on/off), so the experiment is clean and the purity camp's corruption worry is contained by construction.
>
> **Kill bars:** both forks face EC1's KB-E1–E5 (the generative fork will fail KB-E1 by design — that failure is *scored*, not excused); additionally **KB-E7 — no-laundering (mechanical + human):** any emitted byte diverging from the cited source span must be declared in the brief *before* the human trial; undeclared divergence kills. **KB-E8 — head-to-head (human, frozen sample):** Micah's verdict on which fork's emissions he trusts as witness testimony. If the generative fork's renders systematically mislead him (human-certified false percepts — the spoof-amplification failure), it dies and the outcome is recorded as evidence for the witness contract.
>
> **Rationale:** settles replay-only vs. generative emission empirically rather than by argument. If EC3's generative fork survives KB-E7/E8, the witness contract was too narrow and the program learns something. If it dies the predicted death, the exclusion of generation from PAMs graduates from debate verdict to tested result.

**Pre-committed no-laundering rule (frozen):** the generative fork's brief must declare, per emitted artifact, every byte-range that diverges from the cited source span and what the renderer put there instead — BEFORE the human trial runs. Undeclared divergence found by mechanical diff or by the human → immediate death, no second run.

## 2. What is built

- Two forks, pure-Zag:
  - **Fork A (replay):** R2-9's witness-emission PAM, unchanged.
  - **Fork B (generative challenger):** R2-9's percept pipeline + a generative renderer that reconstructs the scene FROM THE COMPRESSED PERCEPT (renders the percept, not the span). The renderer is contained: percepts must be byte-identical with the renderer on vs. off (no-interference, same as KB-E5).
- Both forks emit artifacts; both face KB-E1–E5 (Fork B's KB-E1 failure is scored as predicted, not excused — it counts against KB-E7/E8 evaluation); both ship the brief; both face the human sample double-blind.

## 3. Fixtures

- Frozen suite R2A per `R2_FIXTURE_SET.md`: 10,000 trials for mechanical bars on both forks.
- Frozen human sample: 200 trials (100 clean / 100 adversarial), stratified across the 18 families, frozen before either fork builds. Both forks' artifacts presented double-blind, interleaved, with the brief; judge does not know which fork produced which artifact.
- Spoof-amplification probe: the adversarial 100 include the families most likely to produce human-certified false percepts under generation (R2A-SHP-1 occlusion-bar, R2A-COL-1 metamer-pairs, R2A-MOT-1 reversed-video, R2A-TMB-2 harmonic-boost).

## 4. Bars (all preregistered; mechanical unless marked human; applied to BOTH forks)

- **B1 viability:** each fork: mean primary accuracy on the frozen 370 harness primary ≥ 60%.
- **B2 vs Approach A:** head-to-head delta per fork on identical fixtures; reported.
- **B3 efficiency:** ops and bytes per percept per fork vs Approach A (measured); the renderer's cost counted against Fork B.
- **B4 no-interference (LOAD-BEARING HARD KILL, per fork):** percepts and dispositions byte-identical with emission/renderer on vs. off. Any difference kills that fork immediately.
- **B5 KB4:** per fork, false permanent installs ≤ 3% on the 10,000 trials.
- **B6 determinism (HARD KILL, per fork):** ≥3 runs byte-identical, hash-chained ledger verified.
- **B7 beauty — EXERCISED, head-to-head:**
  - (i) mechanism elegance per fork vs its own beauty claim;
  - (ii) human verdict: KB-E3, KB-E4 per fork (replay fork faces them as in R2-9; the generative fork's KB-E1 divergence is scored), plus KB-E8: Micah's verdict on which fork's emissions he trusts as witness testimony. Systematic misleading (human-certified false percepts from the generative fork — the spoof-amplification failure) kills the generative fork and is recorded as evidence for the witness contract. If the generative fork survives KB-E7/E8, the witness contract was too narrow — recorded as evidence against it.

## 5. Kill criteria (KB-E1–E5 + KB-E7 + KB-E8, hardened)

1. Each fork faces KB-E1–E5; failures kill that fork (the generative fork's predicted KB-E1 failure is scored into the head-to-head, not excused).
2. KB-E7: any emitted byte diverging from the cited source span not declared in the brief BEFORE the human trial → that fork dies immediately.
3. KB-E8: Micah's head-to-head verdict on which fork's emissions he trusts as witness testimony — recorded; a fork he systematically distrusts as testimony is dead as a witness.
4. Shared human-verdict protocol applies (see R2-9 §5 — same 8 rules).
5. B4 and B6 are HARD KILLS per fork: fails B4 → dies; fails B6 → dies.
6. **No retroactive bar changes after results.** Frozen before the builds; amendments go to Micah.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-11.md` (committed ALONE — no src, no evidence).
- Build output (later, separate commits): `senses/pam-rebuild/round2/forks/R2-11/`: PREREG copy, src/ (both forks), evidence/ (incl. artifacts, briefs, divergence declarations, human-verdict records), LEDGER.md.
- Shared fixtures: `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language, max-risk posture.
