# Atom provenance and regeneration — 2026-09-27

Both v2 atoms are extracted from real corpus WAVs by `src/extract_atom.py`.
Extraction is deterministic: re-running on the same source reproduces the
atom byte-identically (verified for both atoms).

## Sources

| Atom | Source WAV | SHA-256 (source) | SHA-256 (atom v2) |
|---|---|---|---|
| `atom0_child.bin` | `audio_longhorizon/corpus/child/child-fsd50k-171101.wav` | `ea533ce6218dc1a65d8171ba21b2b5591a68598ffd2becdb293e45ca834720f7` | `05f95cf1e225d55073520681452bc6a849e33d55e95214c96f0004aa92d8aeea` |
| `atom1_speech.bin` | `audio_longhorizon/corpus/speech/speech-e22-000.wav` | `767c8da3af7351ec423ba101c43f3e07e0a1b5af345678dc3482c181e04d5b5e` | `8ea7e03d8e497c0a517da94f9938241fb4e03b3843b56ec63381a2174af3783f` |

## How the child source was identified

The v2 child atom was initially converted from v1 with the source unrecorded.
On 2026-09-27 `src/find_child_source.py` scanned all 52 WAVs in
`audio_longhorizon/corpus/child/` deterministically:

- `child-fsd50k-171101.wav` matched with harmonic-shape correlation **1.000000**.
- Fresh extraction from that WAV reproduced the legacy atom exactly:
  T0 = 112.163570, harmonic waveform correlation 1.0 (max abs diff 0.0),
  amplitude trajectory correlation 1.0 (max abs diff 0.0).
- Fresh v2 extraction is **byte-identical** to the installed v2 atom
  (SHA-256 `05f95cf1…`).

The earlier "source unrecoverable" note is superseded.

## Regeneration

```bash
python3 src/extract_atom.py <corpus-wav> <out.atom>
```

The planner loads atoms at runtime from its configured atoms directory
(currently `/home/hatch/workspace/desynth/atoms/` — a deployment path, not a
source of truth; the source of truth is the extraction above).

## Sealed-fixture decision

The atoms are committed as sealed runtime fixtures under
`fixtures/atoms/` (20 KB each). Rationale: the corpus WAVs are not in the
repo, so without the atoms the committed planner cannot run; the atoms are
the actual test/runtime fixture, byte-pinned by the hashes above, and
regenerable from the documented sources by anyone with corpus access.
