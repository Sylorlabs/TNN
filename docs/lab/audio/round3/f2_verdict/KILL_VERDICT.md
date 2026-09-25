# F2 `inventory_splice` — KILL VERDICT

Date: 2026-09-24 PDT. Crew: F2 build crew.
Prereg: `~/workspace/audio_round3/ROUND3_PREREG.md` §4 (frozen).

## Verdict: KILL — precondition failure (prereg §4 target specification unsatisfiable)

The fork was killed **before any mechanism was built**, because the frozen prereg's
source specification cannot be satisfied: §4 mandates the target
("phonetic string + durations + voiced/unvoiced labels") be MEASURED from
`kida.wav`, and no phonetic string is attested in `kida.wav`.

### Evidence

1. **kida.wav is the bed-only isolation.** `~/workspace/v5work/render_v5.zag` line 774
   maps `kida` → `which=11`; the render dispatch (lines 864–877) gives which=11 the
   `bed()` call and **no score call** (`score_kids`/`score_kids_iso` are only invoked
   for which==1/12/13/14/15). Source comment: "kida = bed only".
   SHA-256 `b8ad8e1a1f4f70b01a602fd1848db8aacd9f4857311a19b72757f1af570cfd6e`.
2. **Waveform measurement:** 30 s, peak 698 (−33.4 dBFS), RMS 125 (−48.4 dBFS), uniform
   across all 30 one-second slices. Frame scan (25 ms/10 ms): max frame RMS **−42.1 dBFS**;
   zero frames above −40 dBFS in the whole file. 497/2998 frames "voiced" (16.6%) are
   faint background textures (F0 227–1225 Hz, 37% at the recurring 668 Hz bed texture),
   longest run 0.20 s — not speech.
3. **The debate record knew.** `native_position_B.md` (debate input to the frozen prereg)
   documents kida.wav as "near-silence throughout, RMS ≈ 100 — the mic-noise floor — and
   is *not* used as content" (lines 73, 123, 170), with the matching SHA. The frozen §4
   kept kida.wav as the donor take regardless — a prereg defect.

Labeling mic-noise-floor bed texture as phones would be fabrication, not measurement.
A build on a degenerate target would die at the gates for the wrong reason (void target,
not mechanism failure) and misattribute the failure. The honest kill is at the
precondition.

### Per-bar verdicts

| bar | verdict |
|---|---|
| F2.1 donor exclusion | UNTESTED — no render; constraint itself satisfiable |
| F2.2 unit length / no-reuse | UNTESTED — no inventory cut |
| F2.3 join click | UNTESTED — no joins |
| F2.4 Viterbi determinism | UNTESTED — no Viterbi run |
| F2.5 ablation | UNTESTED — no baseline |
| F2.6 negative control | UNTESTED — no path |
| G1–G5, G7 | UNTESTED / NOT REACHED |
| G6 | satisfied vacuously (no gains, no normalization) |

Repairs attempted: **zero** — no failed bar exists that a repair could address.
**The F2 mechanism is UNTESTED, not falsified.**

## Amendment proposal (needs Micah's word)

Replace the donor take in §4:

- **Donor take: `kidc.wav`** (full mix, v4 replica; SHA
  `5d69f49dd6653c4bbd1fe5c0296b4240ff52224ce47e7062b0a12c05ba40c701`) **instead of
  `kida.wav`. `kidc.wav` BANNED from the inventory.**
- **Inventory:** `kidb.wav` + `kidd.wav` + `kide.wav` + fossil vowel cores (VF-1, VF-3;
  neither has kid provenance).
- **Target:** phonetic string + durations + voiced/unvoiced labels measured from `kidc.wav`.
- **F2.1 becomes:** zero samples with provenance in `kidc.wav`.
- All other §4 text (chain, costs, C = 10 ms frozen, kill bars F2.2–F2.6, G1–G7) unchanged.

Viability (measured, same scan): kidc.wav 38.7% voiced, F0 158–1225 Hz (med 573),
frame RMS p50 −22.4 / max −11.6 dBFS, longest voiced run 0.39 s — a measurable
phonetic target. kidb/kidd/kide: 35.7–39.7% voiced, peaks −11.5 dBFS — viable inventory.

Caveat for the amended crew: kidb/kidc/kidd/kide share the v5 atom catalog (different
seeds/scores); an inventory unit may contain the same recorded atom as a donor region.
F2.1-as-amended bans kidc.wav *file* provenance; sequence-level novelty stands. Flagged.

## What died and why (one line)

F2-as-preregistered died at the source-specification precondition: the designated donor
take kida.wav is the bed-only isolation (near-silence, nothing above −40 dBFS frame RMS
in 30 s), so no phonetic string can be honestly measured from it; the mechanism itself
was never tested.
