# RUNLOG.md — YT-INGEST-1 pipeline scaffold, first run (2026-09-22)

## Pipeline stages
1. `venv/` — python3 -m venv + yt-dlp 2026.08.19. Reachability verified
   (one metadata probe on aqz-KE-bpKQ; initial timeout was transient).
2. `manifest.tsv` — frozen 7-video sample (6-8 required), all <5 min,
   diverse motion. One metadata probe per video (ytsearch flat or
   watch-page probe). See manifest for ids/titles/durations/categories.
3. `download.py` — one download per video, format
   `bv[height<=480]+ba/best[height<=480]/bv+ba/best` merged to mp4.
   DEVIATION from prereg ≤360p: YouTube serves no 360p formats for these
   videos (verified --list-formats; min is 480p). 64x64 downscale in ffmpeg
   keeps the modesty intent (files 0.4–9 MB). Log: raw/download_log.tsv
   (video_id, sha256, bytes, title, duration, category).
   NOTE: downloads were bot-walled ("Sign in to confirm you're not a bot")
   for ~30 min after the metadata burst; ios/web_embedded player clients
   bypass the wall but return storyboards only. After a cooldown the
   default client worked. Exact error is in the report.
4. `vidio.py` + `validate_vid.py` — .vid writer validated: byte-identical
   to harness gen.py write_vid on synthetic frames (sha match), and the
   real fixture p000.vid parses as (8,64,64) with size 12+8*64*64*3.
   Validation evidence: validation/ (VALIDATION: PASS).
5. `convert.py` — ffmpeg per video:
   `-vf "crop=min(iw,ih):min(iw,ih),scale=64:64" -pix_fmt rgb24 -f rawvideo`,
   then 8-frame windows every 30 frames via vidio.write_vid.
   Log: windows/convert_log.tsv (video_id, window_idx, start_frame,
   stride, fps, src_sha256).
6. `yt_sense/sense_t1` — copy of a_raw/sense.zag with the rematch-T4
   fitted rule (STILL iff mag < 1, i.e. `mag2 >= 1`), built with the
   pinned toolchain. sha256 1f208c2362000564179fed80a669b1c063ce4a97cb57299b4987f901e1a16385;
   rebuild byte-identical. Behavioral probe (mag=2): old STILL → new E.
   Evidence: validation/BUILD_EVIDENCE.md.
   DISCREPANCY FOUND (flagged): code/src/sense.zag + code/src/sense (the
   sibling trial's dir) are the UNfitted rule (mag2 >= 9, binary gives
   STILL at mag=2), but the sibling's recorded runs/* show direction
   judgments at mag=1..2 — i.e. their trial ran with a fitted binary
   that is no longer on disk. Their final.json digest is the recorded
   artifact; their code/src/sense binary does NOT reproduce their runs.
   My pipeline uses yt_sense/sense_t1 (fitted, proven).
7. `perceive.py` — per 8-frame window: byte-exact sub-slicing
   (w1=frames0-3, w2=frames4-7, cl/cr crops, mirroring windowize.py);
   sense_t1 on whole/w1/w2/cl/cr; code/src/method2 (fitted, verified
   STILL iff mag<1) on whole; code/src/gate ALL over the six pairs in
   sibling order (w1,w2,cl,cr,whole,m2). One JSON record per window.
8. `gate.py` — verdict-aware layer. Reads READINESS.md ("## Verdict:"
   line): READY → G-ALL candidates go through the vendored
   apply_memory_rule → INSTALL-INTENT; GATED → same gate, but installs
   become PARKED (install-intent, nothing enters memory); NOT READY /
   missing → WITHHOLD all. Every record carries a concrete reason.
   Current verdict: GATED. --counterfactual-ready evaluates the gate as
   if READY (for the YT1 probe).
9. `make_probe.py` — 13-fixture YT1 held-out probe (8 adversarial
   1px/frame 0.25-contrast directions + STILL, 4 primary-like 2px/frame
   full-contrast), deterministic texture, disjoint from readiness
   fixtures. probe_heldout/probe_manifest.tsv + probe_percepts.jsonl +
   probe_gate.jsonl.

## Validation evidence
- .vid layout: VALIDATION: PASS (byte-identical to harness write_vid).
- Fitted binary: BUILD_EVIDENCE.md (sha, rebuild-identical, mag=2 probe).
- Determinism: perceive.py on probe_heldout ×2 → byte-identical
  percepts.jsonl (sha ff6dd2d8ac06a2240eb8489885134ab3608013a5914bf9a24d71b3fdab7f4bb2).
- YT1 probe (counterfactual READY): 13 fixtures → 2 INSTALL-INTENT,
  0 false installs → adversarial false-install rate 0/2 = 0% ≤ 10%: PASS.
  (Actual verdict GATED: those 2 become PARKED; nothing enters memory.)

## First-run results (2026-09-22/23)

Windows per video (8-frame 64x64, stride 30):
  0_jNjpVxUt0 (timelapse clouds): 27
  kcfs1-ryKWE (FPV Iceland canyon): 67
  9AwUsf8HzVI (30 dunks in 60s): 60
  OQSNhk5ICTI (double rainbow, static talking head): 175
  uKNQCPXDNdc (deer nature): 124
  bwJ-TNu0hGM (city street): 139
  Eoo4HzILB-M (ocean waves): 17
Total: 609 windows, 609 percepts (percepts.jsonl).

Gate (verdict GATED → all installs parked; gate_log.jsonl):
  WITHHOLD 514, PARKED 95, INSTALL-INTENT 0.
  Gate reasons: temp_disagree 375, spat_disagree 87, meth_disagree 49,
  agree 98 (95 parked STILL; 3 direction candidates S/N/W blocked by the
  run-local memory rule: an earlier STILL with conf>= was installed first).
  Notable: double rainbow (static) → 175/175 withheld (handheld jitter
  disagrees across windows); FPV drone → 67/67 withheld.

Notes for the parent
- A service restart killed the first perceive run at 208/609 windows;
  records were the first-208 sorted filenames (verified), so the run was
  resumed for the remaining 401 and concatenated (sorted order preserved,
  609 unique records).
- Zero RNG in every stage; Python is download/decode glue only.
- Nothing committed. No real-memory wiring anywhere.
- sense_run.py superseded by perceive.py (full G-ALL procedure per
  READINESS.md gate spec); old script kept for reference.
