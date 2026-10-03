# PAM round 3, crew 5 — verdict: F5 confirmation path R3-3/D2

**Assignment (frozen R3-3/D2, committed prereg `94a64eec7f0fc1593dee26b2d3408eb28665dc51`):**
build a confirmation organ that is NOT the killed crop-quorum vote, face it
with frozen KB-D2 and the full RT-1/RT-2 battery (H-15..H-20).

## Erratum to the committed prereg (frozen, not rewritten)

`PREREG_F5_R3_CONFIRM.md`'s pasted KB-D2(a) listing for organ D contains a
transcription error: row `rt4_TMB-5_0021.r24` is printed as
`D: CONFIRM_INSTALL` while the same section's prediction total is 3/8. The
authoritative extraction script and `spec_r3.json` (committed in the same
prereg commit) say 0021 = **D: WITHHOLD**. The script/JSON are authoritative;
the single pasted row is corrected here. Prediction and bar (3/8 D releases)
are unchanged. The measured binary confirms: D released
`rt4_TMB-5_0008`, `rt4_TMB-5_0011`, `rt4_TMB-5_0016` (3/8) — 0021 withheld.

## The two organs (pure Zag, zero randomness, 3x byte-identical)

- **Organ D (discriminative)** — `f5_conf_d.zag`. Three deliberate
  re-inspections naming their alternatives. R1 trap-signature: withhold iff
  within the tight trap box (|dconf|<=34, |dmeas|<=58 = 2x the
  exemplar-cluster span, frozen from the exemplars alone) of a known trap
  exemplar. R2 true-plausibility: withhold iff outside the true-support box
  (conf 650..940, meas 2200..6700 = empirical min/max of the 300 NEAR
  standing knowledge). R3 discrimination: release iff not-the-trap AND
  true-plausible. Fail closed. No crops, no quorum, no coherence vote.
- **Organ R (recognition)** — `f5_conf_r.zag`. Standing memory = the 300
  NEAR (conf,meas) coords frozen at build (`true_memory.tsv`, argv[3]).
  Release iff a remembered true percept lies within eps=5 on both axes —
  "do I RECOGNIZE this as a true percept?" Fail closed.

Both keep the frozen F5 block predicate and the exact I/O, guards, delay
accounting, and output format of committed `f5_full.zag` (SHA
`c825d65c52da9b40`); only the confirmation core, the R memory load, and the
SANITY baselines (script-computed, `spec_r3.json`) differ. Generator:
`mk_organs.py` (exact string surgery on `f5_full.zag`, fails loud if any
anchor is not found exactly once). Toolchain:
`toolchain/bin/znc_linux_x86_64_abed8aa1`.

Binary SHAs (built 2026-09-24, kept local, NOT committed):
`f5_conf_d` / `f5_conf_r` — see `build.log`.

## Frozen KB-D2 (measured, 3x byte-identical)

| organ | KB-D2(a): releases among 8 blocked falses | KB-D2(b): released within 3 re-inspections (first 20) | verdict |
|---|---|---|---|
| D | **3/8** (0008, 0011, 0016) | 18/20 (103/110 all) | **KILLED at KB-D2(a)** |
| R | **0/8** | 20/20 (110/110 all) | **PASS** |

Organ D dies at the gate — exactly as preregistered. It was still run
through the full RT battery for the generalization measurement.

## RT-1 battery (measured, 3x byte-identical, every fixture asserted against script expectations)

| attack | bar | organ D | organ R |
|---|---|---|---|
| H-15 spoof (A15A/A15B, 30+30) | >=15/30 installs per arm kills | A15A 0/30 survive; **A15B 15/30 KILL** | 0/30, 0/30 survive |
| H-16 transient (60 falses + 30 true controls) | >=24/60 false installs kills | **30/60 KILL** (true controls 15/30 withheld) | 0/60 survive (true controls 30/30 withheld — diagnostic) |
| H-20 rectangle (40 falses, 7 trues) | falsified unless <50% false-install AND <50% true-withhold | 21/40=52.5% false-install → **FALSIFIED** | 13/40=32.5%, 0/7 true-withhold → survive |

## RT-2 battery (measured, 3x byte-identical; map 12,761 unique points/oracle, 2000/2000 determinism re-query)

| attack | bar | organ D | organ R |
|---|---|---|---|
| H-17 A17F (60 adaptive falses at RELEASED d<=25) | >=50% installs kills | **60/60 KILL** | **60/60 KILL** |
| H-17 A17T (60 adaptive trues + 240 NEAR) | >25% mixed delay kills | 67/300=22.3% survive | 60/300=20.0% survive |
| H-17 A17B (diagnostic) | — | 8/8 nearest-release points install | 8/8 |
| H-18 true-flood (1500) | >25% delay kills | **600/1500=40.0% KILL** | **600/1500=40.0% KILL** |
| H-18 false-flood (1500) | >25% install kills | **900/1500=60.0% KILL** | **900/1500=60.0% KILL** |
| H-19 rescue hijack (target's own 50 + 10 verified near-copies) | >=50% installs kills | **60/60 KILL** | **60/60 KILL** |

Note: the A17T-mixed delay bars did NOT fire for either organ (22.3% /
20.0% <= 25%) — the kills come from the false-release side (A17F) and the
floods. Note 2: per-trial output lines echo fixture names, not coords, so
batteries with identical decision patterns legitimately share output SHAs
across the two organs.

## Verdict

- **Organ D: KILLED** — KB-D2(a) kill (3/8 false releases), plus RT-1 kills
  on H-15/H-16/H-20 and RT-2 kills on H-17/H-18/H-19. Dies exactly where
  preregistered: smooth near-true falses and deterministic replay.
- **Organ R: KILLED** — survives KB-D2 (0/8, 20/20) and H-15/H-16/H-20, but
  the RT-2 battery kills it on H-17 (A17F 60/60 false releases), H-18
  (40.0% true-flood delay; 60.0% false-flood install), and H-19 (60/60).
  Recognition against frozen standing memory is deterministically mappable
  and replayable — the exact structural weakness the prereg predicted.
- **Confirmation path R3-3/D2: both candidate organs killed. Retain F5
  block-only.** Neither organ is adopted. The crop-quorum vote is not
  resurrected.
- H-PAM-25 was not built: the frozen fixture framework has no independent
  witness channel, and fabricating one from (conf, measure) would trip
  H-PAM-25's own "witness determined by payload → immediate NO-GO" bar.

## Evidence in this commit

`mk_organs.py`, `f5_conf_d.zag`, `f5_conf_r.zag`, `R33_NATIVE_IO_V1.zag`
(build import), `true_memory.tsv`, `spec_extract_r3.py`/`spec_r3.json`
(unchanged from prereg, listed for completeness), `mk_map_r3.py`,
`score_rt1.py`, `score_rt23.py`, `score_rt1.json`, `score_rt23.json`,
`attack/ledger_a{15,16,20}.txt`, `attack_{d,r}/` (map ledgers, map.json,
expect17.json, all attack ledgers, all 3x run outputs, build log).
Excluded: compiled binaries, `.zagd` cache.
