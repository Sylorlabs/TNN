# F2 `inventory_splice` — build crew RUNLOG

Crew: F2 build crew (subagent). Date: 2026-09-24 PDT.
Frozen prereg: `~/workspace/audio_round3/ROUND3_PREREG.md` (read in full before work; §4 is the spec, §§0/2/7/8 binding law).
Workdir: `~/workspace/audio_round3/build_f2/`.

## Source SHAs (verified 2026-09-24, sha256sum)

| file | SHA-256 | format |
|---|---|---|
| `~/workspace/v5work/kida.wav` | `b8ad8e1a1f4f70b01a602fd1848db8aacd9f4857311a19b72757f1af570cfd6e` | mono 16-bit 44.1 kHz, 1,323,000 samples, 30.0 s |
| `~/workspace/v5work/kidb.wav` | `13285a0da02de5a830e289924ba4c9e5b831ac86bbd7de0002f033d7046682a3` | same |
| `~/workspace/v5work/kidc.wav` | `5a1b1f7b1f359f4fa6fff40580e72be5c34f33f300dc4b2f9a6140c78eb4ab44` | same |
| `~/workspace/v5work/kidd.wav` | `ab22c5e400c26c1693020317526f6bff69661b5a48fc7e58efdb085549c3e9dd` | same |
| `~/workspace/v5work/kide.wav` | `5d69f49dd6653c4bbd1fe5c0296b4240ff52224ce47e7062b0a12c05ba40c701` | same |

Fossil cores (for inventory under an amended spec; provenance verified non-kid):
- VF-1 source `aporee_kids_play_area_30s.wav` SHA `6adafbf0143df1c1721377cd8eaa7f25aa6305fb4be6d12c6268d28281738960`
- VF-3 source `aporee_kids_play_area.wav` (134 s) SHA `24981f77ff52acb701f3e6957ece9c5b5ab8d53857887d7bc69bc0d717c79b77`
- (SHAs from `~/workspace/audio_forks/vowel_fossils/FOSSIL_LOG.md`; neither fossil has kida.wav or kidc.wav provenance.)

## Step 1 — donor-take verification (prereg §4 precondition)

Prereg §4 requires: "Target: phonetic string + durations + voiced/unvoiced labels
measured from `kida.wav`". Debate requires "a phonetic string that is actually
attested in `kida.wav`".

### 1a. Render-code evidence — kida.wav is the bed-only isolation

`~/workspace/v5work/render_v5.zag`:
- line 774: `if(_zag_strcmp(subj,"kida")==1){which=11;}`
- lines 864–877: `if(which!=12){bed(...);}` then score dispatch only for
  which==1 (`score_kids`) and which==12/13/14/15 (`score_kids_iso`).
  which==11 receives `bed()` and **no score call** → bed only, zero placed atoms.
- Source comment at line ~860: "Battery 1e/V5: component isolation. kida = bed only;
  kidb = events only; kidc = full mix (v4 replica); kidd = mix minus harsh atoms;
  kide = mix with harsh atoms replaced."

### 1b. Waveform measurement of kida.wav (deterministic, numpy)

- Whole file: peak 698 (−33.4 dBFS), RMS 125 (−48.4 dBFS).
- Per-second scan (30 s): peak 367–698 every second, RMS 83–176 — uniform; no foreground events anywhere.
- Frame scan (25 ms window / 10 ms hop, 2998 frames; voiced iff normalized autocorr peak ≥ 0.5 in lag range [sr/1200, sr/80] and frame RMS > −50 dBFS):
  - voiced frames: 497/2998 (16.6%)
  - voiced F0: min 227 Hz, p10 304 Hz, median 639 Hz, p90 689 Hz, max 1225 Hz
  - 37% of voiced frames within 668±20 Hz (a recurring periodic bed texture; the rest is faint background babble)
  - longest contiguous voiced run: 20 frames = 0.20 s at t = 4.40 s
  - max frame RMS over the whole file: **−42.1 dBFS** (p99 −42.9); **zero frames above −40 dBFS in 30 s**
- Loudest 100 ms window (t = 4.54 s): RMS 222.9, peak 547; band energy concentrated 500–2000 Hz; autocorr peak 0.769 in F0 lag range.

### 1c. Debate-record evidence — the silence was known before freezing

`~/workspace/audio_round3/native_position_B.md` (debate input to the frozen prereg):
- line 73: "kida.wav measured as near-silence throughout, RMS ≈ 100 — the mic-noise floor — and is *not* used as content"
- line 123: "kida.wav's near-silent stretches (RMS ≈ 100, the actual mic-noise floor of the session...)"
- line 170 (source table): "near-silence throughout (RMS ≈ 100, mic-noise floor) — candidate recorded-silence source, not content"
- SHA logged there (`b8ad8e1a…`) matches the file on disk — same file, no re-render.

### 1d. Precondition verdict

**No phonetic string is attested in kida.wav.** The file is the bed-only isolation:
30 s of playground ambience at −48 dBFS RMS with no foreground content (nothing above
−40 dBFS frame RMS anywhere). The 16.6% "voiced" frames are faint background textures,
not speech. Measuring a "phonetic string + durations + voiced/unvoiced labels" from it
would mean labeling mic-noise-floor bed texture as phones — fabrication, not measurement.
The prereg §4 target specification is unsatisfiable as written. This is a prereg defect,
not a mechanism failure: the debate record documents kida's silence, but the frozen §4
still mandates it as the donor take.

## Step 2 — kill-bar verdicts (per bar, honest status)

No target string exists → no inventory was cut (cutting units for a void target would be
theater) → no Viterbi run → no render → no analyzer run. All mechanism bars are
UNTESTED, not failed. The fork is killed at the precondition.

| bar | verdict | note |
|---|---|---|
| F2.1 donor exclusion (zero kida.wav samples) | UNTESTED | constraint satisfiable; nothing rendered to audit |
| F2.2 unit ≥ 40 ms, ≥ 2 periods if voiced; no unit > 2× | UNTESTED | no inventory cut |
| F2.3 join click (first-diff ≤ 4× interior median; flux ≤ 2×; C = 10 ms frozen) | UNTESTED | no joins exist |
| F2.4 Viterbi 3× identical path + identical SHA | UNTESTED | no Viterbi run |
| F2.5 ablation (join-cost=0 must degrade: join total +≥50% AND ≥2 gates fail) | UNTESTED | no baseline path |
| F2.6 negative control (LF+formant diphones must fail ≥ 3 gates) | UNTESTED | no path to control |
| G1 provenance 100% | UNTESTED | no output samples |
| G2 3× byte-identical | UNTESTED | no render |
| G3 shared analyzer gates | UNTESTED | no render |
| G4 no-static audit | UNTESTED | no render |
| G5 silence test (zeroed sources → bit-exact zeros) | UNTESTED | no pipeline built |
| G6 no output-derived normalization | SATISFIED VACUOUSLY | no gains computed, no normalization performed |
| G7 ear staging | NOT REACHED (correct) | nothing staged; "Do NOT stage for ears" honored |

**Overall: KILL at precondition.** Zero repairs attempted — no failed bar exists that a
repair could address; the defect is in the frozen source specification. Per tasking
("one logged repair per failed bar max, then honest kill"), this is the honest kill.

**Explicitly not claimed:** the F2 *mechanism* (deterministic concatenative unit
selection) is UNTESTED, not falsified. A gate-failure verdict on a degenerate target
would misattribute a spec defect to the mechanism; it was not attempted.

## Step 3 — amendment viability check (for Micah's word, not executed)

The natural amendment: donor take = `kidc.wav` (full mix, v4 replica) instead of
`kida.wav`; `kidc.wav` BANNED from inventory; inventory from `kidb.wav`/`kidd.wav`/
`kide.wav` + fossil vowel cores; F2.1 becomes "zero samples with provenance in kidc.wav".

Viability measurements (same frame scan as §1b):

| file | voiced frac | voiced F0 (min/p10/med/p90/max Hz) | frame RMS p50 / max (dBFS) | longest voiced run |
|---|---|---|---|---|
| kidc.wav (proposed donor) | 1159/2998 = 0.387 | 158 / 329 / 573 / 1225 / 1225 | −22.4 / −11.6 | 0.39 s at t = 13.91 s |
| kidb.wav (inventory) | 1069/2998 = 0.357 | — | −22.4 / −11.6 | — |
| kidd.wav (inventory) | 1189/2998 = 0.397 | — | −23.2 / −11.6 | — |
| kide.wav (inventory) | 1107/2998 = 0.369 | — | −21.6 / −11.5 | — |

kidc.wav is speech-bearing (kid events at healthy levels, 38.7% voiced, F0 158–1225 Hz):
a phonetic string + durations + V/UV labels is measurable from it. All three inventory
files carry comparable voiced content. The amended fork is buildable.

Provenance nuance for the amended crew: kidb/kidc/kidd/kide are all renders from the
same v5 atom catalog with different seeds/scores — an inventory unit from kidb may
contain the same underlying recorded atom as a donor region in kidc. F2.1 (as amended)
bans *kidc.wav file* provenance, not atom identity; novelty is at the sequence level.
Flagged, not blocking.

Fossil "donor take" exclusion (prereg §4: "fossil vowel cores EXCLUDING the donor take"):
under the frozen prereg the donor take is kida.wav; neither fossil core has kida.wav
provenance (both from aporee field recordings, SHAs above), so both VF-1 and VF-3 are
eligible — the exclusion is satisfiable. (The debate text's "other than the anchor slice"
language does not appear in the frozen prereg; prereg wins on conflict. Noted for the
amended crew; does not affect this kill.)

## Files in this workdir

- `RUNLOG.md` (this file)
- `KILL_VERDICT.md` — per-bar verdicts + amendment proposal for Micah's word
- `SHA_LOG.md` — source SHA-256 log

No WAV master, no provenance table, no analyzer report, no rerun SHAs: none produced,
per the kill. Nothing staged for ears.
