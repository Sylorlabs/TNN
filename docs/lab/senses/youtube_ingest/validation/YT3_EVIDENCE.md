# validation/YT3_EVIDENCE.md — determinism rerun (2026-09-22)

Video: Eoo4HzILB-M (sunset beach waves, 21s, 505 frames @ 25fps, 17 windows).
Script: rerun_yt3.py — re-runs convert (ffmpeg) + perceive (sense_t1 ×5,
method2, gate.zag) from the downloaded bytes into rerun_yt3/, then compares.

1. Converter byte-compare: all 17 .vid files sha256-identical to the
   first-run windows/ files → PASS.
2. Sense record compare: 17 rerun percept records field-identical to the
   matching records in percepts.jsonl → PASS.

YT3: PASS — same video bytes → same .vid → same percepts.

Also: perceive.py on probe_heldout ×2 (13 fixtures incl. method2+gate) →
byte-identical percepts (sha ff6dd2d8ac06a2240eb8489885134ab3608013a5914bf9a24d71b3fdab7f4bb2).
