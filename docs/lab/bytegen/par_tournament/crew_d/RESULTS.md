# CREW D — tournament RESULTS (numeric record)

Full battery log: `runs/battery.log` (rc=0). Per-leg machine files under
`results/`. Pinned znc `znc_linux_x86_64_abed8aa1`; pure Zag; zero RNG.
All wavs/mixes: 44,100 Hz, 30 s unless noted.

## Determinism (4 rerenders each, `cmp` + SHA-256)

| Scheme | SHA-256 (all 4 identical) |
|---|---|
| D1 | `1823f8fa82af3aca23c598b902c53a0df072315c84e7c5509b26625299427ca4` |
| D2 | `1823f8fa82af3aca23c598b902c53a0df072315c84e7c5509b26625299427ca4` |
| D3 | (see `results/d3_determinism.sha256`) |

D1 and D2 clean renders are the SAME bytes (both bit-identical to NATIVE).
The D1/D2 SHA equals the dive's 2026-09-24 SHA — cross-session reproducibility.
(`results/d1_determinism.sha256`, `results/d2_determinism.sha256`)

## Clean vs NATIVE (D1-C1 / D2-C1 / D3-C1)

All three: mix AND wav `cmp`-identical to rebuilt `render_native`.

## Quality — 9 V10 gates (identical for D1/D2/D3 = NATIVE bytes)

G-PER 0.340 / G-STA 1.826 / G-LURCH 2.362 / G-DRIFT 480.284 /
G-FLUXm 241.824 / G-SIL1 0.000 / G-SIL2 0.000 / G-CLIP 0.849 /
G-CREST 3.863 — 9/9 PASS. (`results/d1_gate.txt`, `d2_gate.txt`, `d3_gate.txt`)

## CHOP (complete 271-event list, `tests/events_full.txt`)

CHOP-1: 0 hard discontinuities. CHOP-2: no silent gaps ≥150 ms.
CHOP-3: 29 flux spikes, 0 unexplained. (Identical ×3.)
(`results/d1_chop.txt`, `d2_chop.txt`, `d3_chop.txt`)

## Coherence decomposition (vs NATIVE)

zero-lag xcorr 1.000000; max-lag xcorr 1.000000 @ 0 samples;
pitch-contour r 1.000000; IOI-contour r 1.000000. (Identical ×3.)
(`results/d1_coherence.txt`, `d2_coherence.txt`, `d3_coherence.txt`)

## RT-LONG honest-cents scoreboard

| | Original (nominal 880, true cue 440) | Near-miss (nominal 460, true cue 440) |
|---|---|---|
| NATIVE (measured, `render_native`) | renders 880 → **1200.00¢** (ZCR 842.5 Hz, −75c bias) | renders 460 → **76.96¢** (ZCR 441.2 Hz, −72c bias) |
| D2 | LATCHED f0q=28835840 → **0¢** (ZCR vs 440: 425.0 Hz, −60c bias) | LATCHED f0q=28835840 → **0¢** |
| D1 / D3 | PAR semantics: render nominal 880 (tie) | PAR semantics: render nominal 460 (tie) |

D2 multi-trap: e=4 ABSTAIN code=1; e=5 latch 440; e=6 latch 523.25
(f0q=34291712 exact). (`results/native_rtlong.txt`,
`results/native_rtlong_near.txt`, `results/d2_rtlong.txt`,
`results/d2_rtlong_near.txt`, `results/d2_rtlong_orig_zcr440.txt`,
`results/d2_rtmulti.txt`)

## RT-CASCADE

| Scheme | Frozen (64 XOR @3 s): pre/in/post | Sustained 1292-block |
|---|---|---|
| D1 | 0 / 64 / 0 | 82,688 diffs, 100% inside fault blocks, 0 outside |
| D2 | 0 / 64 / 0 (latch fires, cue window clean) | ABSTAIN code=3 (cue window corrupted — no hallucination) |
| D3 | **0 / 0 / 0** (repaired 1,024) | **0 diffs vs clean** (repaired 1,323,000) |

D3 extended (§2): burst 4096@10s → 0 diffs (repaired 5,120);
dropout 1024@20s → 0 diffs (repaired 2,048); DC +10000 over 8192@5s →
0 diffs (repaired 9,216). Repair spans exceed fault sizes at 1024-sample
block boundaries — documented, bytes are exactly plan-pure.
(`results/d1_cascade.txt`, `d1_sustained.txt`, `d2_cascade.txt`,
`d2_sustained.txt`, `results/d3_cascade.txt`, `results/d3_cascade_ext.txt`)

## RT-EDGE (frozen)

All three: wav bit-identical to NATIVE. (`runs/battery.log`)

## D1 15 s window-cut extension (outside frozen battery)

hardstop=1 fires. A/B analyzer (`results/d1_edgeAB.txt`): fade ends
0.0000 FS; nofade ends 0.3142 FS; 214 diffs all inside [n−220,n),
0 outside; fade end-slope 0.01480 FS vs nofade 0.02687 FS; frozen CHOP-1
0/0 (does not discriminate sub-0.35 end-steps — documented).

## Order permutation

seq == rev bit-identical for D1, D2, D3. (`runs/battery.log`)

## §5 red team

- D1 between-pass injection: `results/d1_redteam_pass3.txt` — T1
  hardstop=1 under 41,344 faults; T2 41,344/0 diff-set (gains index-pure);
  T3 0/20 analytic-LUT mismatches. Full report: `REDTEAM.md`.
- D2 adversarial ×5: `results/d2_adversarial.txt` — emptywin/badwin
  ABSTAIN code=1; nomlie LATCHED 440 (nominal ignored); chain e=1 latch
  440 + e=2 ABSTAIN code=1; hugeamp completes, latch fires. f0lie:
  latches plan-declared 466.16 (f0q=30550261) → 0¢ vs plan, 99.99¢ vs
  intent — provenance boundary mapped.
- D3 failure modes: F1 blind to plan-pure-coincident faults; F2 lying
  plan passes audit; F3 2.22× cost.

## COST (interleaved, same machine; `/proc` VmHWM)

| Binary | wall s (r1/r2/r3) | median | peak RSS |
|---|---|---|---|
| render_native | 4.35 / 6.91 / 6.06 | 6.06 | 13,032 KB |
| render_d1 | 3.61 / 5.86 / 5.96 | 5.86 | 13,048 KB |
| render_d2 | 5.98 / 5.77 / 8.07 | 5.98 | 13,048 KB |
| render_d3 | 7.52 / 13.45 / 15.31 | 13.45 | 13,052 KB |

D3/native = 2.22×. (`results/cost_interleaved.txt`)

## Excerpts (WITHHELD-NOT-FOR-REVIEW)

`excerpts/README.md`; SHAs in `results/excerpts.sha256`.
d1_boundary_fade.wav `2ea2a5c8…eb814`; d1_boundary_nofade.wav
`0e75a9e5…326b07`; d2_planref.wav `cdd77569…7db3ff9d`.
