# DEMO CORPUS MANIFEST — audio_longhorizon wiring hello-world (SEALED)

Sealed 2026-09-25 PDT, BEFORE any wiring trial binary touched these files.
Per PREREG_LH §8: SHA-256 per clip, committed before runs. Any clip added
later = new manifest version + note (never silent).

Base: /home/hatch/workspace/

## Demo session S1 (16 episodes; scored claims: ablation K-W1/K-W2, determinism K-W4)

| ep | file | sha256 | provenance |
|----|------|--------|------------|
| 1 | v5work/kidc.wav | 5a1b1f7b1f359f4fa6fff40580e72be5c34f33f300dc4b2f9a6140c78eb4ab44 | real child speech (G4c case) |
| 2 | goals/tnn-real-ai-architecture/files/imagination_audio/v1_audio_brief3_human.wav | 2738fc2971476886f89da9ea4cd53be664890094167dd682d849f7769731309b | real human utterance, 1.0 s |
| 3 | goals/tnn-real-ai-architecture/files/imagination_audio/f3mood_scary.wav | 8f7466e94576c0f4ca2ef065e7fe980174d3f4b2fb2214a79017eb29b74cde15 | imagination_audio render (= piece_C.wav, same bytes), contrast only |
| 4 | v5work/kida.wav | b8ad8e1a1f4f70b01a602fd1848db8aacd9f4857311a19b72757f1af570cfd6e | real child speech |
| 5 | goals/tnn-real-ai-architecture/files/imagination_audio/f3mood_calm.wav | b582ff7be98ba4be1f6e851ef0c1f10dc5ae78a824667cde7587c924174e6428 | imagination_audio render (= piece_A.wav, same bytes), contrast only |
| 6 | goals/tnn-real-ai-architecture/files/imagination_audio/f3song_hifi.wav | 0af6a284942f7a0eae23321a7c8bbc8c3eba80e14217f3b873c8813cadc48a08 | imagination_audio render, contrast only |
| 7 | v5work/kidb.wav | 13285a0da02de5a830e289924ba4c9e5b831ac86bbd7de0002f033d7046682a3 | real child speech |
| 8 | goals/tnn-real-ai-architecture/files/imagination_audio/f3mood_happy.wav | d774f4a4b6f76def9827e876893f63eaa7e79ceab20e3d5209df74d7e71d8dba | imagination_audio render (= piece_B.wav, same bytes), contrast only |
| 9 | v5work/kidd.wav | ab22c5e400c26c1693020317526f6bff69661b5a48fc7e58efdb085549c3e9dd | real child speech |
| 10 | goals/tnn-real-ai-architecture/files/imagination_audio/v1_audio_brief3_human.wav | 2738fc2971476886f89da9ea4cd53be664890094167dd682d849f7769731309b | repeat of ep 2 (recall probe) |
| 11 | v5work/kide.wav | 5d69f49dd6653c4bbd1fe5c0296b4240ff52224ce47e7062b0a12c05ba40c701 | real child speech |
| 12 | v5work/kidc.wav | 5a1b1f7b1f359f4fa6fff40580e72be5c34f33f300dc4b2f9a6140c78eb4ab44 | repeat of ep 1 (recall probe) |
| 13 | goals/tnn-real-ai-architecture/files/imagination_audio/f3mood_scary.wav | 8f7466e94576c0f4ca2ef065e7fe980174d3f4b2fb2214a79017eb29b74cde15 | repeat of ep 3 (recall probe) |
| 14 | v5work/kida.wav | b8ad8e1a1f4f70b01a602fd1848db8aacd9f4857311a19b72757f1af570cfd6e | repeat of ep 4 (recall probe) |
| 15 | goals/tnn-real-ai-architecture/files/imagination_audio/f3song_hifi.wav | 0af6a284942f7a0eae23321a7c8bbc8c3eba80e14217f3b873c8813cadc48a08 | repeat of ep 6 (recall probe) |
| 16 | goals/tnn-real-ai-architecture/files/imagination_audio/f3mood_calm.wav | b582ff7be98ba4be1f6e851ef0c1f10dc5ae78a824667cde7587c924174e6428 | repeat of ep 5 (recall probe) |

Duplicate-byte notes (discovered at seal time, not hidden):
- v5work/kidc2.wav is byte-identical to v5work/kidc.wav (sha 5a1b1f7b...);
  the session uses the kidc.wav path for both repeat turns.
- f3mood_calm.wav == piece_A.wav; f3mood_happy.wav == piece_B.wav;
  f3mood_scary.wav == piece_C.wav (same bytes, two names each).
- "Real" claims rest ONLY on the kid* clips and v1_audio_brief3_human.wav.
  The f3* imagination_audio files are contrast material of workstream-render
  provenance (2026-09-22); no realness claimed for them.

All demo clips are PCM16 mono 44.1 kHz (organ-compatible). The 8 kHz
_human files are NOT in the demo session (organ rejects non-44.1k).

## F0 estimator probe set (test equipment for §4; not scored demo material)

| file | sha256 | note |
|------|--------|------|
| goals/tnn-real-ai-architecture/files/imagination_audio/n5_human.wav | a9c0dbd3a69e553ca8ea16746ab95e6e2121bdefb02885e69294c5a7a04a8e87 | real human, 8 kHz — low-F0 probe candidate |
| goals/tnn-real-ai-architecture/files/imagination_audio/n6_human.wav | a15c92a06e5dcad183cdc9223ad4941c53a8b3c899db004ba700619e65017bfd | real human, 8 kHz — low-F0 probe candidate |
| goals/tnn-real-ai-architecture/files/imagination_audio/a1_human.wav | 859488bacc523d4b640933318c28122cb4b4348f9de197430d22a5b7be1634d909ba45ad8c1 | real human, 8 kHz |
| goals/tnn-real-ai-architecture/files/imagination_audio/a2_human.wav | a784b20ae24f3ffb9e0f14a42f7226abb6c5316f045b7be1634d909ba45ad8c1 | real human, 8 kHz |

## Synthetic characterization tones (crew_p test_wavs, dev renders — NOT real)

Used only to characterize the F0 estimator failure surface (pitchabs:NNNN.wav
pool, 60 tones). Never headline evidence, never "real" claims.
