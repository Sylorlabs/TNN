# Contender A — Audio Path Verdict (§2 battery + §6 bars)

**Date:** 2026-09-24 | **Pinned compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Sources:** `src/form_par.zag` (plan formation), `src/render_a.zag` (renderer). Pure Zag, zero RNG.

## §2 Frozen battery (fixture `bytegen/fixture/plan_v1.txt`, 30 s / 44.1 kHz / mono)

| Bar | Contender A | Native (AR) | Verdict |
|---|---|---|---|
| **DET** (2 renders, cmp @ mix) | byte-identical (`a_seq1==a_seq2`) | byte-identical | TIE (both pass) |
| **QUALITY** (9 V10 bars) | 9/9 PASS (G-PER 0.340≤0.350, G-STA 1.826≤3.000, G-LURCH 2.362≤5.000, G-DRIFT 480.284≤800, G-FLUXm 241.824≤350, G-SIL1 0, G-SIL2 0, G-CLIP 0.849≤0.950, G-CREST 3.863≤14) | 9/9 PASS | TIE (both pass) |
| **CHOP-1/2/3** (complete 314-ts list) | 0 hard disc / no ≥150ms gaps / 29 spikes, 0 unexplained | — | PASS |
| **COHERENCE** xcorr zero-lag | **1.000000** | 0.736557 | **A WINS** |
| **COHERENCE** max-lag ±50ms | **1.000000** | 0.736557 | **A WINS** |
| **COHERENCE** pitch contour | **1.000000** | 0.999630 | **A WINS** |
| **COHERENCE** IOI contour | 1.0 | 1.0 | TIE |
| **COST** wall (6 interleaved, s32 mix) | median **6.40 s** | median **4.38 s** | **NATIVE WINS** (~46%) |
| **RT-LONG** (cue 440, nominal 880) | **440.00 Hz, +0.00 cents** | 453.75 Hz, +53.27 cents | **A WINS** |
| **RT-LONG** near-miss (nominal 460) | **440.00 Hz, +0.00 cents** | — | A ignores nominal |
| **RT-LONG** glide cue (+1200c glide) | plan resolves **440 Hz**; sine renders 439.50 Hz (-1.97c) | — | glide can't confuse formation |
| **RT-LONG** vibrato cue (5.5 Hz) | plan resolves **440 Hz** | — | vibrato can't confuse formation |
| **RT-CASCADE** single-bit @3s, post-cut diffs | **0 / 1,190,699** | 5,791 | **A WINS** |
| **RT-CASCADE** burst @10s | pre 0, win 44,100/44,100, post **0** | — | A: zero cascade |
| **RT-CASCADE** dropout @10s | pre 0, win 44,098/44,100, post **0** | — | A: zero cascade (2 clean-zeros) |
| **RT-CASCADE** DC-shift @10s | pre 0, win 44,100/44,100, post **0** | — | A: zero cascade |
| **RT-EDGE** (truncate @15s) | 4,397/661,500 diffs, ALL in [14.9,15.0) legitimate envelope region; 0 elsewhere | — | PASS (legitimate only) |
| **FAILURE MODES** | see FAILURE_MODES.md | — | documented |

## §4 Plan-formation parallelism

`form_par`: two-pass formation. Pass 1 enumerates all non-RESPOND specs into an
immutable table; pass 2 resolves every RESPOND against the complete table —
theme text order cannot affect resolution. Verified 2026-09-24 (after hang fix):

- `seq`/`rev`/`stride` formation orders → byte-identical plans (order-invariance)
- Output byte-identical to frozen `bytegen/fixture/plan_v1.txt`
- Cue-before-RESPOND vs cue-after-RESPOND: both resolve to 440 Hz (nominal 880
  ignored); renders bit-identical (`cmp` PASS)
- Slot coverage: every slot computed exactly once (all orders)

## §5 Red team (A)

- **Sustained 1292-block corruption:** 0 deviating blocks/samples vs exact
  expected `clean XOR per-sample pattern`; 1,322,969 samples corrupted → landed.
- **Event-order permutation:** `evperm+mix` bit-identical to `seq+mix` (`cmp` PASS).
- **Blocked tiling:** `blocked+mix` bit-identical (`cmp` PASS).
- **Streaming:** `seq+streammix` bit-identical to `seq+mix` (`cmp` PASS).
- **Plan-text adversarial:** 9 cases (empty, negative dur, 20 kHz, amp 0,
  amp 999999, late event, nonnumeric, short event, triple overlap) — no
  crash/hang. Malformed inputs degrade to silence/bed (documented, not rejected).
- **Polyphonic RESPOND:** louder-440 cue wins; exact tie → earliest event.
- **Sub-octave nominal lie (220):** resolved to cue 440, nominal ignored.
- **Vibrato cue:** resolved correctly (ZCR sensor not used for formation).
- **5-minute drift:** motif @2s vs @290s byte-identical, xcorr 1.000000000.

## §6 Overthrow assessment (audio)

A is **strictly better** than native on **RT-LONG** (0.00 vs +53.27 cents),
**RT-CASCADE** (0 vs 5,791 post-cut diffs), and **coherence** (1.000000 vs
0.736557). It matches on quality (9/9), DET, and RT-EDGE (legitimate-only).

**COST is a genuine regression:** 6.40 s vs 4.38 s median (~46% slower,
6 interleaved runs, equivalent s32-mix output). Root cause is architectural,
not a bug: pure `f(plan,t)` recomputes oscillator phase per sample per voice
via integer division, while native's carried phase uses one addition per
sample. This is the fundamental price of statelessness in a single-threaded
implementation. PAR's parallel dividend (multi-core) is not demonstrated here.

**Verdict: PARTIAL WIN — not a clean §6 overthrow.** A dominates the
correctness/robustness axes (RT-LONG, RT-CASCADE, coherence, zero drift, zero
cascade by construction) but loses COST single-threaded. Under §6's "no
regression elsewhere" clause and the "tie keeps native" rule, the COST deficit
blocks a clean overthrow claim. The result strongly favors PAR for
robustness-critical audio; the cost is real and must be weighed.

No victory claimed prematurely. Matrix reported, not a single crown.
