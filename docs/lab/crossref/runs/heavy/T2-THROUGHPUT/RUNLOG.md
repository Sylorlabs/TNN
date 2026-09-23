# T2-THROUGHPUT crossref crew — RUNLOG

## Pins (frozen before running)
- PREREG: ~/workspace/tnn-lab/crossref/PREREG_TIER2.md
  sha256: 90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f
- tnn-native-lab branch head: (resolving — no local git; will clone and record)
- Evidence commit: 67bf4c4cf81b9d1d5e1e4e150892843830ff8b2b (from prereg §T2-THROUGHPUT)
- METHOD.md: ops/throughput/METHOD.md (sha256 recorded below)
- znc: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
- Clock discipline: CLOCK_PROCESS_CPUTIME_ID per METHOD.md

## Pins (frozen before running)
- tnn-native-lab branch head (run start, API): 5efe0a10a93a5bffa07f689a58d86417e850425c (2026-09-23T09:04:53Z)
- Evidence commit (API-verified): 67bf4c4cf81b9d1d5e1e4e150892843830ff8b2b (2026-09-22T21:44:41Z, empty message per prereg caveat)
- METHOD.md blob: fe64a1232785aa631aef77bbd003f810e8265a0b (local clean checkout == pinned commit)
- Instrument blobs @67bf4c4c: thru_learner.zag c65b6d4c0f4539227540097772129c37c6978f51; dlg_thru.zag 776ce3c174e3383bf3897ee090b41de2570e7dc2 (both match local)
- Clean checkout: sparse clone sylorlabs/TNN@67bf4c4c (docs/lab/ops/throughput, docs/lab/dialogue, docs/lab/scale)
- Corpus: ~/workspace/scale/corpus/texts (lab-local, not in git); 22-file sha256 bundle: 52dd88c90b9da74f676c83e49921e1b92f2ed7a7466c243692b0a95675214771
- znc: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 --no-analyze; both bins built clean

## Instrument verification
- dlg_thru.zag vs dialogue.zag@67bf4c4c: 55 diff lines, all now_ns/emit-accumulator/turn-accumulator/THRU prints — timing-only ✓
- thru_learner.zag vs scale/fewshot/driver/fewshot_learner.zag@67bf4c4c: 55 diff lines, all fs_cpu_ns/truth-teach-CPU accumulators/adaptive-recall/THRU prints — timing-only ✓

## VM-load sensitivity (required by prereg)
- Learner anchors (09:14–09:21): load avg 18–35. A VM reboot occurred ~09:20–09:22 (daemon restart, uptime reset to 1 min); N=240k rep2 killed mid-run, re-run post-reboot. Rep1 (pre-reboot) kept — valid.
- Dialogue loaded set (09:26): load ~16.8. Dialogue quiet set (09:27+): load 5–17.
- Original crew's load: 8–13 (their own report documents wall degradation under contention).
- Wall-clock anchors (recall, deliberation, emission, end-to-end) are load-sensitive and moved down; CPU-clock install anchors are contention-robust and hold. This is stated explicitly in VERDICT.md.

## Numbers (≥3 reps each)
Install µs/fact (CPU clock): N=240: 5.97, 5.93, 6.29 (med 5.97 → 167.6K/s); N=240k: 6.41, 6.385, 6.266 (med 6.385 → 156.6K/s). Committed: ~6.2 (n=7: 5.74–6.19; ANALYSIS n=3: 6.1–6.2). ±10% band [5.58,6.82] — PASS. Flat O(1) in N — PASS.
Ops/fact (driver's own): N=240: 4.004; N=240k: 4.000 (committed range 4.000–4.004) — PASS exact.
Bytes/fact: SCALE_MEM total_bpf=92 (slot 24 + index 4 + audit 64) both scales — PASS exact.
Determinism: SCALE_DIGEST fnv1a 44a61309cf780de1 ×3 (N=240), 31377bd76faa81c1 ×3 (N=240k) — PASS byte-identical.
Recall µbench (wall): N=240: 2.23, 2.30, 3.25 µs/probe (307–449K/s); N=240k: 468 ns (2.14M/s, in-band), 1956 ns (511K/s), 1367 ns (731K/s). Committed: 1–3.2M band (ANALYSIS N=240k median 942K [803K,1.47M]). O(1) in N holds; band moves with load — PARTIAL item #1.
Evalsweep (realistic, wall): N=240: 962–1027 ns/probe (~1.0M/s, in-band); N=240k: 9.7–18.6 µs/probe (54–103K/s, below — truth-derivation is wall-contended).
Deliberation (wall): loaded reps 955/793/769 eps (1.05/1.26/1.30 ms/turn); quiet reps 738/1475/954 eps (1.36/0.68/1.05 ms/turn). Committed median 3,322.8 [2,662, 4,600]; ±20% bar [2,640,3,960] — NOT met. Ordering holds (deliberation still slowest stage vs 42–307 µs/utterance emission) — PARTIAL item #2.
Emission (wall): 775K ✓ / 106K / 119K / 138K / 460K ✓ / 110K chars/sec vs committed median 507K [342K,1.29M] — mixed, load-contended.
End-to-end (wall): 25.2–31.3K chars/sec vs committed median 109K [87K,151K] — below.
Dialogue correctness: 370/370 PASS ×6 reps; deterministic content byte-identical across all 6 reps (sha256 33743aead2f6457dce48653df1eff28e91cbf165208839ab86fad0e8c4bbb372) — PASS.

## Verdict
PARTIAL — see VERDICT.md. Missing: quiet-VM rerun of the wall-clock anchors at load comparable to the original measurement.
