# PROPOSED AMENDMENT to ROUND3_PREREG §4 (F2 donor take) — NEEDS MICAH'S WORD

Status: PROPOSED 2026-09-24 PDT. NOT in force. Frozen prereg stands until signed.

## Defect (verified independently 2026-09-24)

Frozen §4 mandates the F2 target ("phonetic string + durations +
voiced/unvoiced labels") be measured from `kida.wav`. Independent
verification (frame scan, 25 ms/10 ms):

- kida.wav: peak 698 (−33.4 dBFS), RMS 124.8 (−48.4 dBFS),
  max 25 ms-frame RMS −42.1 dBFS — ZERO frames above −40 dBFS.
- Render code (`~/workspace/v5work/render_v5.zag`): kida → `which=11`,
  which gets `bed()` but no score call — source comment "kida = bed only."
- Debate record (native_position_B) independently documented kida as
  near-silence / mic-noise floor, same SHA as the file on disk.

No phonetic string is attested in kida.wav. The F2 build crew killed
the fork at precondition (honest kill; mechanism UNTESTED, not
falsified). Full verdict: `~/workspace/audio_round3/build_f2/KILL_VERDICT.md`.

## Proposed amendment (minimal, from the F2 crew, viability measured)

- Donor take = **`kidc.wav`** (full mix, v4 replica) instead of kida.wav.
- kidc.wav **banned** from the inventory; inventory from
  kidb.wav / kidd.wav / kide.wav + fossil cores.
- F2.1 becomes: "zero samples with provenance in `kidc.wav`."
- All other §4 text unchanged.
- Viability measured: kidc 38.7% voiced, F0 158–1225 Hz (median 573),
  longest voiced run 0.39 s — a measurable phonetic target;
  kidb/kidd/kide 35.7–39.7% voiced, peaks −11.5 dBFS — viable inventory.
- Caveat: all kid takes share the v5 atom catalog (different seeds), so
  inventory units may contain the same recorded atom as donor regions;
  F2.1-as-amended bans kidc.wav *file* provenance; novelty is
  sequence-level, stated openly.

## Alternatives considered

- kidb/kidd/kide as donor: equally viable, but kidc (v4 replica, full
  mix) is the most representative take; any of the four works.
- Labeling kida's noise-floor textures as phones: REJECTED — fabrication.

## Decision needed from Micah

Sign this amendment (donor = kidc.wav, kidc banned from inventory), pick
a different donor take, or kill F2 outright.
