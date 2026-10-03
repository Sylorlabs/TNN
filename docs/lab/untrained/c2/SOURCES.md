# SOURCES — confirmatory inputs for Workstream B (c2 run, 2026-09-26)

All downloaded fresh 2026-09-26, AFTER the c2 analyzer was frozen
(source SHA 826ff00344c8d83df1d327c6474190df62eb50a4c6d8986adcf8914b371310b5,
binary SHA d4ed41c4fba7336f8474a8ee4f31d9bf4e11e9e52e145177b47437baeeba8420).
The analyzer never saw these bytes before the sealed confirmatory runs.
Only the transport-normalized forms (WAV/PPM/frames) were analyzed;
originals are documented here for provenance and NOT committed (blobs).

## Audio originals (MP3, archive.org — "133 Authentic Sound Effects" collection)

1. B1_surf.mp3 — 2,199,849 bytes, 91.0 s
   SHA-256: 8983c84e2b043fc2456a847005be18b783bd7793e56d5899e57853bc195b686b
   Git blob: 4cc8bf5d1a0fc73929cf8b2c672ba74c1eac1e8f (not in repo — novel)
   Track: "Surf" (disc1/02.07). Normalized -> inputs/wav/B1_surf.wav (2,912,238 bytes).

2. B2_hootowl.mp3 — 997,022 bytes, 34.9 s
   SHA-256: fddb2ecde4d2947af264e584f6e35145f17eff7681eaef84b5e6e736a9ec4c9d
   Git blob: 6e1d10545d6b69ba78df92b865d3f9bc71297ac6 (not in repo — novel)
   Track: "Hoot Owl" (disc1/01.21). Normalized -> inputs/wav/B2_hootowl.wav (1,117,044 bytes).

3. B3_helicopter.mp3 — 1,823,177 bytes, 72.4 s
   SHA-256: 9151fe3efc01390e23f39bda787ce1f8a685a8871ed82bf9675e2039f6a3c9a6
   Git blob: a3cd91bb2385211fb20ce8ccbf3afed886b69622 (not in repo — novel)
   Track: "Helicopter Passes Overhead" (disc1/01.04). Normalized -> inputs/wav/B3_helicopter.wav (2,317,060 bytes).

## Image originals (JPEG, Wikimedia Commons)

4. B4_forest.jpg — 9,172,434 bytes, 6000x4000
   SHA-256: 06608dececedc6a39e051c83daf23202f5e2d8fbd03f202a6b67d7b67107f604
   Git blob: 3d507f962057c7549c4466973062e6230a9cd5fb (not in repo — novel)
   Title: "Forest in the mist 03.jpg".
   Transport-normalized (ffmpeg scale 480:-1) -> inputs/ppm/B4_forest.ppm
   (480x320, 460,815 bytes).

5. B5_dunes.jpg — 7,305,330 bytes, 5385x3590
   SHA-256: a29676904ca8d54a9e2f3985b86ee9e9f5bfb18bb545ada8b740b1c1efdf520a
   Git blob: 1bef0a19a5814dac292ec43e32e1ed435993c204 (not in repo — novel)
   Title: "006 Dune 45 in Sossusvlei at sunrise Photo by Giles Laurent.jpg".
   Transport-normalized -> inputs/ppm/B5_dunes.ppm (480x320, 460,815 bytes).

## Video original (OGV, Wikimedia Commons)

6. B6_waterfall.ogv — 14,913,739 bytes, 1920x1080, 6.8 s
   SHA-256: 7d16529b2a9458b143a15e76f156ff34451fbbe5fbfe45675d8fa48de4c6cb0f
   Git blob: 4b6475b641463e81553fcb9d283444ec13a0b949 (not in repo — novel)
   Title: "Tresaith Waterfall.ogv".
   Extracted at 2 fps, scaled 320x180 -> inputs/frames/b6_f_001.ppm .. b6_f_014.ppm.

## Normalization (transport only; no content selection)

- Audio: `ffmpeg -ar 16000 -ac 1 -sample_fmt s16` (full files, no excerpts).
- Images: `ffmpeg -vf scale=480:-1` to binary PPM (P6).
- Video: `ffmpeg -vf fps=2,scale=320:180` to PPM frames.
- The analyzer opens the given byte path only and never parses filenames.

## Novelty audit (correct method)

Each original's Git blob object ID (via `git hash-object`) was checked
against the repository's object store via the GitHub API. All six blobs
return 404 (not found): these exact bytes were never committed to the repo.
This replaces the exploratory run's inadequate audit (which passed raw
SHA-256 to `git cat-file`, a category error — the repo uses Git object IDs).
