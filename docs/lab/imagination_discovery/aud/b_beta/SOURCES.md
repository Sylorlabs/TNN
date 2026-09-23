# B-β source registry

All sources are **local originals** under `b_beta/sources/` (and uniform
44.1 kHz mono s16 staging conversions under `b_beta/work/wav/`).
**They are never committed.** Every audible moment of every B-β output is
cut from these files; the placement log (`work/place_kids.log` format)
gives the per-event lineage.

Provenance observed 2026-09-22. Four URLs independently verified via the
B-γ fork's study records plus duration cross-check; the remaining seven
page URLs were not recovered in this session — they are marked
UNVERIFIED rather than guessed. (All are Wikimedia Commons uploads;
the pre-compaction download transcript held the exact URLs.)

## Kids benchmark sources (src IDs as used in catalog/mechanisms)

| src | Local file | Duration | License | Author | Commons page |
|---|---|---|---|---|---|
| 0 | `kids_park.oga` | 30.0135 s | CC BY-SA 4.0 | — | https://commons.wikimedia.org/wiki/File:Ambient_sound_children_playing_in_a_park_2026-05-19.oga ✓ |
| 1 | `kids_playground.ogg` | 48.849 s | Public domain | stephan | https://commons.wikimedia.org/wiki/File:Douzen_kids_on_playground.ogg ✓ |
| 2 | `kid_laugh.ogg` | 11.260 s | CC BY 3.0 | — | UNVERIFIED (known 4yo boy laugh) |
| 3 | `kids_berlin.wav` | 92.389 s | CC0 | foongaz | https://commons.wikimedia.org/wiki/File:209901_foongaz_city-playground-boxhagenerplatz-berlin.wav ✓ |
| 4 | `footstep_gravel.mp3` | 0.575 s | CC BY 4.0 | Gravity Sound | https://commons.wikimedia.org/wiki/File:Footstep_on_Gravel_(Gravity_Sound).mp3 ✓ |
| 5 | `forest_track4.ogg` | 10.684 s | Public domain | tball74 | UNVERIFIED |

## Test 2 / Test 3 sources (not yet catalogued)

| Local file | Duration | License | Author | Commons page |
|---|---|---|---|---|
| `ocean_tropical.ogg` | 384.268 s | CC0 | — | UNVERIFIED |
| `sea_waves.wav` | 20.88 s | CC BY-SA 4.0 | — | UNVERIFIED |
| `loon_yodels.ogg` | 12.939 s | CC BY-SA 2.5 | — | UNVERIFIED |
| `throat_singing.ogg` | 18.792 s | CC BY-SA 4.0 | — | UNVERIFIED |
| `whale_song.oga` | 52.699 s | CC BY 2.5 | — | UNVERIFIED |

## Compliance notes

- No source is modified except: format conversion to s16 mono 44.1 kHz
  (staging only), and cutting events at measured zero-crossings.
- No pitch shift, time stretch, EQ, reverb, or any processing is applied
  to source audio at any stage. Gain is constant per placement (Q16).
- 3 ms linear edge fades are applied at placement time for seam removal
  only (documented in `assemble.zag` `place()`); they are not envelopes.
- CC BY-SA 4.0 sources (0, throat_singing): the output is an adaptation;
  attribution is recorded here and in the commit message.
