# STUDY_LOG.md — what was studied, how, and what was learned

**Method lineage:** position (b) study-then-invent. Study is the source of
the *vocabulary* (event grains), never of the *composition*. No sample from
any study recording appears unaltered in a deliverable as a "scene" — every
deliverable is a new arrangement under a deliberate grammar, audited by the
no-copy gate (audit.py).

**Study materials are LOCAL ONLY** (`study_src/`, `study_out/`), never
committed. This log + `study.py` make the study reproducible.

## Sources

| # | File (local) | What it is | License | Source URL |
|---|---|---|---|---|
| 1 | `play_berlin.wav` | City playground, Berlin (92 s) | CC0 | https://commons.wikimedia.org/wiki/File:209901_foongaz_city-playground-boxhagenerplatz-berlin.wav |
| 2 | `play_park.oga` | Children playing in a park (30 s) | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:Ambient_sound_children_playing_in_a_park_2026-05-19.oga |
| 3 | `play_douzen.ogg` | Dozen kids on playground (49 s) | Public domain | https://commons.wikimedia.org/wiki/File:Douzen_kids_on_playground.ogg |
| 4 | `feet_gravel.mp3` | Footstep on gravel (0.6 s) | CC BY 4.0 (Gravity Sound) | https://commons.wikimedia.org/wiki/File:Footstep_on_Gravel_(Gravity_Sound).mp3 |
| 5 | `surf_lake.ogg` | Lake Okeechobee surf (332 s) | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:Lake_Okeechobee_Surf_in_April_2016.ogg |
| 6 | `wood_casket.ogg` | Creaky wooden casket (1.4 s) | Public domain | https://commons.wikimedia.org/wiki/File:Creaky_wooden_casket.ogg |
| 7 | `wood_chair.ogg` | Creaky wooden swivel chair (6.6 s) | Public domain | https://commons.wikimedia.org/wiki/File:Creaky_wooden_swivel_chair.ogg |
| 8 | `swings.wav` | Playground swings (19 s) | CC BY 4.0 (Gravity Sound) | https://commons.wikimedia.org/wiki/File:Playground_swings_(Gravity_Sound).wav |
| 9 | `an_ice_crackling.wav` | Ice crackling field (74 s) | Public domain | (aud/inspiration, SOURCES.md) |
| 10 | `an_storm_thunderbolts.wav` | Storm thunder field (303 s) | Public domain | (aud/inspiration, SOURCES.md) |
| 11 | `an_mars_wind_supercam.wav` | Mars wind, SuperCam (40 s) | Public domain (NASA) | (aud/inspiration, SOURCES.md) |
| 12 | `an_mars_dustdevil.wav` | Mars dust devil, SuperCam (27 s) | Public domain (NASA) | (aud/inspiration, SOURCES.md) |

Attribution: CC BY / CC BY-SA sources are credited here; they are used for
study only — no studied sample is redistributed in any deliverable.

## Segmentation (study.py, all deterministic, thresholds below)

- **vocal** (play_*): spectral-flux onsets in 300–6000 Hz, threshold
  median+3·MAD, min gap 90 ms; grain = onset−20 ms … next onset−10 ms
  (cap 700 ms). Then sub-classified by measured features:
  - `laugh`: dur < 320 ms and centroid > 900 Hz
  - `squeal`: centroid > 2000 Hz and dur < 500 ms
  - `shout`: everything else
- **voice ids**: deterministic k-means (k=3, fixed init, empty-cluster
  repair by splitting the largest) on [log centroid, log dur, log rms],
  ordered by median centroid → voice 0 (lowest) … 2 (highest).
- **thump** (play_*, feet_gravel): flux onsets in 60–400 Hz, median+4·MAD,
  min gap 150 ms, ≤450 ms grains. (feet_gravel is one grain whole.)
- **swell** (surf_lake): 1 s moving-average envelope peaks
  (median+1.2·MAD, ≥3 s apart); grain = peak−1.5 s … peak+3 s.
- **wash** (surf_lake, thunder): fixed 3 s texture windows.
- **creak** (wood_*, swings): flux onsets in 800–12000 Hz, median+3·MAD.
- **crack** (ice_crack): flux onsets in 800–12000 Hz, median+5·MAD, ≤350 ms.
- **boom** (thunder): flux onsets in 40–900 Hz, median+4·MAD; grain =
  onset−30 ms … +600 ms; **rumble** = +500 ms … +3 s tail.
- **wind** (mars_wind, dustdevil): fixed 3 s texture windows.

All grains get 2 ms raised-cosine edge fades at cut time; the assembler
applies its own ≤2 ms glue fades (T7) at placement.

## Grain inventory (from study_summary.json)

<!-- filled after the study run -->

## What the study taught (the vocabulary)

- A laugh is not a tone: laugh grains show ragged 4.5–6 Hz-class pulsing
  *inside* the grain, formants that move, and no two alike — the reason
  T5-free assembly (no pitch tools) can still read as laughter: the
  variation is in the grains, not imposed.
- Thunder tails are the longest honest low-frequency textures available
  (up to 3 s); they carry the planet-hum and sky-hum beds without any
  oscillator.
- Ice cracks are the brightest, shortest events in the pool (centroids to
  ~8 kHz); sorted by centroid they become the planet chorus's "rising."
- Swell grains from a lake are small and quick — the alien ocean's
  slowness is composed (T6), not found.
- Wood creaks are sparse (57 grains); they are spent carefully (seismic
  groans, the Raxith's settling plates).

## What the study did NOT supply (declared gaps)

- No rising-pitch grains anywhere → the planet chorus's "rising" is
  brightness+quickness (T8), declared as interpolation in the audit.
- No voice with a larynx for the monster → the Raxith has none either;
  its voice is fracture-grammar, not a voice at all.
- No surf-crash grains big enough for the alien ocean → crests are
  crack-grains by deliberate physics (viscous-crystalline sea), not by
  resemblance.
