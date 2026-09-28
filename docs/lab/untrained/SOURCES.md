# SOURCES — novel inputs for Workstream B (untrained structural analysis)

All downloaded fresh 2026-09-26. The analyzer never saw these bytes before the
sealed runs. Only the transport-normalized forms (WAV/PPM/frames) were analyzed;
originals are documented here for provenance and NOT committed (blobs).

## Audio originals (MP3, archive.org)

1. A1_thunderstorm_full.mp3 — 32,727,168 bytes
   SHA-256: 2e6ab22cc22d9ebec9760c0b6b4105789bb18b15c0218ab0ce4162fd74232ef6
   URL: https://archive.org/download/ThunderStorm_943/NaturalSounds-Thunderstorm.mp3
   Analyzed: 30.0 s excerpt starting at 422.0 s (loudest 1 s interval ~437 s),
   normalized to 16 kHz mono 16-bit PCM -> inputs/wav/A1_thunderstorm.wav
   (960,092 bytes).

2. A2_bellbuoy.mp3 — 1,550,055 bytes, 55.8 s
   SHA-256: 16befb6bbb57a34d6c0aafbcc6f83d727f9a70ef077d8d8c90bbb68e5d0ea3fc
   Source: archive.org "133 Authentic Sound Effects" collection, bell buoy track.
   Normalized -> inputs/wav/A2_bellbuoy.wav (1,785,842 bytes).

3. A3_crickets.mp3 — 1,276,960 bytes, 43.2 s
   SHA-256: 068cba5f48f892390b25de47177b60bd47a587e6d7c3e4e3768bc0b9318451d8
   Source: archive.org "133 Authentic Sound Effects" collection, crickets track.
   Normalized -> inputs/wav/A3_crickets.wav (1,382,654 bytes).

## Image originals (JPEG, Wikimedia Commons)

4. I1_frost.jpg — 6,875,270 bytes, 5472x3648
   SHA-256: cd8c433ccf60f6cf67812c8db9be5ad60fed75c4ced94feb45ff3be44ec977ac
   Title: "Ice Crystals on Window Pane".
   Transport-normalized (ffmpeg scale 480:-1) -> inputs/ppm/I1_frost.ppm
   (480x320, 460,815 bytes).

5. I2_terraces.jpg — 15,932,402 bytes, 5600x4000
   SHA-256: e1989707a7e52f78aa25a5391967004785cfda9f18731636aab3f75720efa73a
   Title: "Longsheng Rice Terraces November 2017 021".
   Transport-normalized -> inputs/ppm/I2_terraces.ppm (480x343, 493,935 bytes).

## Video original (OGV, Wikimedia Commons)

6. V1_waves.ogv — 15,442,896 bytes, 1920x1080, 11.04 s
   SHA-256: cd9545398523ef089578f49e2e7ad9982f2b4e60814c25531e08eed41a9c47d9
   Title: "Ocean surface waves 09.ogv".
   Extracted at 2 fps, scaled 320x180 -> inputs/frames/f_001.ppm .. f_022.ppm.

## Normalization (transport only; no content selection except A1 excerpt window)

- Audio: `ffmpeg -ar 16000 -ac 1 -sample_fmt s16` (A1 additionally `-ss 422 -t 30`).
- Images: `ffmpeg -vf scale=480:-1` to binary PPM (P6).
- Video: `ffmpeg -vf fps=2,scale=320:180` to PPM frames.
- The analyzer opens the given byte path only and never parses filenames.
