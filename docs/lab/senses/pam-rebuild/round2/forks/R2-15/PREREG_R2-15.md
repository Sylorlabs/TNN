# PREREG R2-15 — FS-C "Cross-Modal Booster Marginal-Gain fork"

**Status: FROZEN 2026-09-23. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_D_new_fronts.md` §4 FS-C (front (c) ruling: AGAINST as a
*required* install warrant; FOR as a booster/composite — cross-modal corroboration SURVIVES as one
admissible disjoint-evidence class inside the R2-3 admission law: never required, never sufficient;
correlated fooling must be a frozen battery family).
**Adaptation note (frozen):** the debate's FS-C mechanism sketch names the R2-7 challenge runner as
the base; R2-7 is ALIVE but its evaluation is still pending, so this fork builds on the **R2-3
admission gate** as the base path instead (R2-3 is ALIVE with a frozen, byte-identical instrument).
Kill bars below are the debate's FS-C bars with the overall bar set to the ≤3% B5-style install bar
per the build order (the ≤1% bar belongs to the R2-7-based variant, which is not built here).

## 1. Hypothesis under test (verbatim from DEBATE_D §4 FS-C)

> *Hypothesis:* requiring cross-modal agreement (on multimodal tasks) reduces false installs over the
> R2-7 challenge baseline by a measurable, ablation-proven margin.

Fork-local restatement (same claim, R2-3 base): adding cross-modal confirmation as an **optional
booster inside R2-3's admission law** reduces false installs on multimodal trials without starving
recall. Single-modality percepts remain installable via the base R2-3 path (booster never required).

## 2. What is built

- **Base path (booster OFF — the ablation control):** the R2-3 reference-gate disposition on the
  visual channel: percept formed on visual formation evidence; INSTALL iff the visual gate-span
  judgment agrees (withhold iff they disagree). Reuses `r2p_front.zag`/`r2p_protos.zag` verbatim.
- **Booster (ON):** base path PLUS cross-modal concurrence: the percept (formed in the visual
  modality) installs only if a **second modality's independently-declared disjoint evidence**
  concurs — here the audio channel's gate span (seconds 2–4, uncorrupted token, per the frozen
  R2_FIXTURE_SET.md declarations for pitchdisc/timbredisc) must judge the same symbol. The
  booster's evidence is itself admission-law evidence (disjoint, declared, overlap-audited), never
  the formation span — per sol's concurrence in debate D §9 ("Do not silently substitute
  same-modality evidence and call it cross-modal").
- **Symbol vocabulary (frozen):** S0 = (visual CIRCLE, audio SAME), S1 = (visual TRIANGLE, audio
  HIGHER), S2 = (visual SQUARE, audio LOWER). Visual judged by `front_shapetrans` (0/1/2 =
  CIRCLE/TRIANGLE/SQUARE); audio judged by `front_pitchdisc` (0/1/2 = SAME/HIGHER/LOWER) on a
  two-tone token (440 Hz reference + symbol tone at 440/528/366.67 Hz). Booster concurrence =
  audio-gate code equals installed visual code.
- Pure Zag, zero RNG in any decision path. Hash-chained ledger; battery run twice per mode,
  byte-identical (`cmp`).

## 3. Fixtures (frozen battery FSC-BATT, generator `round2/fixtures/gen_fsc.py`)

Each trial file embeds: magic "FSC1", truth symbol, family id, trial index, then four blobs —
visual-F (48×48 RGB), visual-G (48×48 RGB), audio-F (2.0 s @8 kHz i16 PCM, formation token),
audio-G (2.0 s @8 kHz i16 PCM, clean gate token). Master seed 20260923 (frozen),
stream ids 700+family (new; no overlap with 400/500/600/900 streams). Every trial is
**verified at generation time** against a Python mirror of the exact naive front-ends
(`naive(visual-F)`, `naive(visual-G)`, `naive(audio-F)`, `naive(audio-G)` must equal the designed
values); a trial that cannot be verified is never written. MANIFEST.fsc.sha256 covers all bytes.

Corruption families (deterministic, seeded):
- **FSC-VIS-1** (visual): tonal inversion (photographic negative) — the R2-3-proven deterministic
  fooler of the template matcher (attacks the brightness-threshold feature band). Lie symbol =
  whatever the naive judge returns on the inverted render (computed, asserted ≠ truth).
- **FSC-AUD-1** (audio): pitch-shift of the symbol tone (tone-B regenerated at the lie symbol's
  frequency) — the true token transformed so the naive relative-pitch judge flips to the lie.

| Family | Id | N | Visual-F | Visual-G | Audio-F | Audio-G | Expected disposition |
|---|---|---|---|---|---|---|---|
| M-N normal | 0 | 400 | clean | clean | clean | clean | both modes install truth (recall set) |
| M-U uncorrelated spoof | 1 | 200 | FSC-VIS-1 (lie L) | clean | clean | clean | both withhold |
| M-W within-modality persistent spoof | 2 | 200 | FSC-VIS-1 (lie L) | FSC-VIS-1 (lie L) | clean | clean | OFF installs L (FALSE); ON withholds |
| M-C **CORRELATED-FOOLING** (H1-killer) | 3 | 200 | FSC-VIS-1 (lie L) | clean | FSC-AUD-1 (lie L) | clean | both withhold (base gate check fires) |
| M-WA audio-channel persistent spoof | 4 | 150 | clean | clean | FSC-AUD-1 (lie L≠T) | FSC-AUD-1 (lie L≠T) | DIAGNOSTIC only: OFF installs truth; ON withholds (second-modality DoS cost) |

M-W is the R2-1-shaped attack on the base path: the adversary holds the visual corruption across
the temporal gate span, breaking the base path's declared-clean-gate assumption; the booster's
independent second modality is the only clean witness. M-C is the frozen H1-killer family: joint
audio-visual formation spoofing to the same lie (both modalities agree on the lie at formation;
both gate spans clean). M-WA is reported with no kill bar (honest measurement of the booster's
install-starvation cost under second-modality attack).

## 4. Bars (all preregistered, applied mechanically; mode ON is the fork, mode OFF the ablation)

- **KB-1 booster ablation (LOAD-BEARING):** false-install rate on the multimodal adversarial subset
  (M-U + M-W + M-C, 600 trials) with booster ON must be **≥5 percentage points (absolute) lower**
  than with booster OFF. Removing the booster must cost ≥5 points; else the booster is decorative
  → **DIES**.
- **KB-2 correlated fooling (HARD):** false installs on M-C with booster ON **≤2%** (≤4/200).
  Any exceedance → **DIES**. This is H1's 44.5% death made into a test.
- **KB-3 recall:** correct-install rate on M-N with booster ON ≥ correct-install rate with booster
  OFF **− 5pp**. Drops more → **DIES** (the booster must not starve recall).
- **KB-4 overall (B5-style install bar):** false installs with booster ON over the full adversarial
  battery (M-U + M-W + M-C, 600 trials) **≤3%**. Exceedance → **DIES**.
- **KB-5 determinism (HARD):** the full battery runs **twice per mode**; reports and ledgers must be
  **byte-identical** (`cmp` clean); hash chains verified by an independent script. Any mismatch →
  **DIES**.
- **Diagnostic (no bar):** M-WA install-starvation rate with booster ON is reported as the measured
  cost of the booster under second-modality attack.

Expected under the design (not a bar — measured): KB-1 ≈ 33.3pp (200/600 OFF vs 0/600 ON);
KB-2 0/200; KB-3 100% vs 100%; KB-4 0/600; M-WA starvation ≈ 150/150.

## 5. Kill criteria

1. Dies on any of KB-1..KB-5. KB-2 and KB-5 are hard kills.
2. If KB-1 fails while KB-2/KB-3/KB-4 pass → the booster is decorative: the fork DIES and the
   base-R2-3-only variant is adopted (debate D §4: "the booster must earn its keep or die").
3. If KB-2 fails → correlated fooling defeats the admitted cross-modal booster: the fork DIES;
   report as the experiment working (the H1-killer family did its job).
4. No retroactive bar changes after results. Amendments go to Micah.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-15.md` (committed ALONE — no src, no
  fixtures, no evidence).
- Build output (later, separate commits): `senses/pam-rebuild/round2/forks/R2-15/`: PREREG copy,
  `src/` (R2-3 sources reused verbatim + `fsc.zag` booster/runner), `evidence/` (reports, ledgers,
  VERDICT), `LEDGER.md`.
- Frozen fixtures + generator + manifest: `senses/pam-rebuild/round2/fixtures/fsc/`,
  `senses/pam-rebuild/round2/fixtures/gen_fsc.py`, `MANIFEST.fsc.sha256`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`,
  lab-relative paths `senses/pam-rebuild/round2/...`, TMPDIR=`~/workspace/tmp_commit`. No binaries,
  no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language,
max-risk posture.
