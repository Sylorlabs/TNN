# VOICE_SIG_FROZEN — frozen instrument for AUDIO V11 objective judging

Status: **FROZEN** — byte-identical copy of the validated `voice_sig.zag`
source (Crew C, 2026-09-24). This file must NEVER be modified after commit.
Any instrument change is a NEW file plus a protocol amendment (Micah's
sign-off, new protocol version); the frozen copy stays in git history.

- Frozen source: `docs/lab/imagination_discovery/aud/b_alpha/voice_sig_frozen.zag`
- Source SHA-256:
  `7117ac57b2ad98a2849e4c86ef659164911835f03b50a63c5f6b7b64996e9a65`
- Live source verified at commit time at
  `imagination_discovery/aud/b_alpha/consistency_gate/src/voice_sig.zag`
  (identical SHA; not committed separately).
- Dependency: `src/common_v5.zag`
  (SHA-256
  `f98c04dc0e68536035faccaac32a1fb0e700f26ffec6d6be54224100deac4dc5`,
  already committed at
  `docs/lab/imagination_discovery/aud/b_alpha/src/common_v5.zag`).
- Compiler: pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Reference binary built at freeze time, SHA-256:
  `56d28c74a51eaa6a0b9ccf51b250088856f7edf28e9eb5fbd26a3bfb94198b29`
  (build artifact; NEVER committed).

## Build command (exact)

IMPORTANT: znc `@import` paths resolve relative to the current working
directory, not the source file. Build ONLY from the source's own directory:

```
cd ~/workspace/tnn-lab/imagination_discovery/aud/b_alpha/consistency_gate/src
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 voice_sig.zag -o voice_sig
```

(The frozen copy `voice_sig_frozen.zag` has the identical `@import`
line; if you build from that copy, place a sibling tree with
`../../src/common_v5.zag` relative to your build cwd.)

Build warnings seen at freeze (analyzer notes, non-fatal): two
"loop variable decreases but the condition requires it to be lesser"
hints (in `vs_cosg`/`vs_log2fp`); build completes, output verified.

## Run command

```
./voice_sig <clip.wav>
```

44.1 kHz mono 16-bit WAV in, `VS_*` lines on stdout, exit 0. Zero RNG,
deterministic. Usage: `voice_sig <clip.wav>` → `VS_OK`, `VS_NVOICED`,
`VS_MOD4`, `VS_F0_MED`, `VS_F0_P10`, `VS_F0_P90`, `VS_F1B`, `VS_F2B`,
`VS_F2B_IQR`, `VS_F3B`, `VS_HNR_MED`, `VS_TILT_MED`, `VS_CENT_MED`.

## Verification record (freeze-time, 2026-09-24)

Rebuilt from source with the pinned compiler and run against the anchor
`consistency_gate/calibration/aporee_kids_play_area_30s.wav`
(SHA-256
`6adafbf0143df1c1721377cd8eaa7f25aa6305fb4be6d12c6268d28281738960`;
CC BY-NC-ND — measurement only, NEVER committed). Output reproduced the
frozen anchor signature in JUDGE_PROTOCOL_V11.md §8 EXACTLY, byte-identical
across two runs, and byte-identical to Crew C's `anchor_v5.txt`:

```
VS_OK 1 | VS_NFRAMES 2000 | VS_NVOICED 36 | MOD4 0.412 | VFRAC 0.018
F0_MED 651.3 | F0_P10 598.0 | F0_P90 772.3 (F0DYN = 174.3)
F1B 794 | F2B 2104 | F2B_IQR 715 | F3B 2814 | HNR_MED 3.7 | TILT_MED 0.9
```

Kill-rule baselines (§8) reproduced exactly with the rebuilt binary
(clips in `clips/b_alpha_kids_1e_j_v10_*.wav`):

- ARTIC → `VS_OK 0`, 0 clean voice frames ✓ (no measurable voice signature)
- SPECSTAT → `VS_OK 0`, 0 clean voice frames ✓
- PARADD → `VS_OK 1`, 52 clean voice frames; signature
  `F0 766.6 | F0DYN 384.3 | F1B 740 | F2B 2329 | F2B_IQR 1247 |
  F3B 2968 | HNR 4.0 | TILT 0.0 | MOD4 0.551` — matches frozen §8 and is
  byte-identical to Crew C's `v10_paradd_v5.txt` ✓

Conclusion: the workdir source matches the validated instrument; no drift.
Frozen for all V11 fork builders — every fork builder MUST self-measure
with a binary built from this exact file (or bit-compare their binary's
output against the frozen values above).
