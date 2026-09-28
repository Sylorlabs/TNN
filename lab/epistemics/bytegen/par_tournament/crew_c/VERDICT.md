# CREW C — Tournament Verdict: Contender C and forks

Date: 2026-09-24. Frozen battery: `~/workspace/tnn-lab/bytegen/par_dive/PREREG_PAR_DIVE.md`.
Pure Zag, zero RNG, pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
All comparisons at mix level; reruns proven by `cmp` + SHA-256.

## Source SHAs (all rebuilt 2026-09-24)

| Binary | Source SHA-256 |
|---|---|
| stock C (`render_c.zag`) | `0640f28fe1496d614d45c7480ea0dd211bb76fc24d4549a2433fc07a26c6d3db` (matches frozen dive) |
| C-gate/rg | `82a0911125ab1274ffdeb8632828329816c2e77b11f985ff3e573c667d506c71` |
| C-gate/cons | `01ae76ab1431cf2d137a8ced10e04e3feff8dff4493d4d263698d45f87f487a2` |
| C-gate/plan | `3560d538a6bc1feaff947dfda5686a0a7ee6f1c81bc14d814e8796f683710033` |
| C-deadband | `b1294126bd7c82e878157516a201a90c58d40afa8099d9188606f98e1555d431` |
| C-fx (cascade ext; clean mode bit-identical to stock) | `b8d95c6523b4cf5d95124d928096675f9b5a8fa04cbb40413383d072a05843a8` |
| C-poly | stock binary + 7 new test plans (no code change) |

## Battery table — stock C (rebuilt)

| Check | Result |
|---|---|
| DET (2× seqmix) | `cmp` clean; SHA `7472ad89f8102b03c72111c3be2511279b77ddc65e07e55a07579181c84a838c` |
| Quality (9 gates) | 9/9 PASS (G-PER 0.333, G-STA 2.020, G-LURCH 2.518, G-DRIFT 477.143, G-FLUXm 242.649, G-SIL1/2 0.000, G-CLIP 0.849, G-CREST 4.324) |
| CHOP-1/2/3 | 0 / none / 41 total, 0 unexplained (known C-CAVEAT item reproduced) |
| Coherence | 1.000000 / 0.999999 lag 0; pitch/centroid/IOI 1.000000; 10/10 onsets |
| RT-LONG | base 440→440 ✓; lies corrected ✓; vibrato ✓; glide abstains→880 ✓; poly abstains ✓ |
| RT-LONG cue30 | **FAIL** — fm=79 Hz, k=-3, latches 110; measured 110.00 Hz |
| RT-CASCADE | fault/dropout/burst/dcshift: 0 post-fault diffs each (vetoes 1/1/8/1) |
| RT-EDGE | first diff 14.975 s (bed edge fade, legitimate); 0 diffs before 14.9 s |
| Cross-region leakage (5 boundaries) | 0 gain diffs in all post-smuggle regions (1208+1035+884+604+259 blocks) |
| sus1292 | 1295/1295 gains bit-identical; 1295 vetoes |
| COST | 11.63 s median; 15832 KB peak RSS |
| Gain range | [0.8763, 1.1574]; inside clamp [0.25, 4.0]; 0 vetoes on fixture |

## Battery table — forks (delta vs stock)

| Check | gate/rg | gate/cons | gate/plan | deadband |
|---|---|---|---|---|
| Fixture mix bytes | identical (7472ad89…) | identical | identical | differs (936566e3…; max 1.4e-6 FS) |
| DET rerun | cmp clean | cmp clean | cmp clean | cmp clean |
| 9 gates | (identical bytes → pass) | (identical → pass) | (identical → pass) | 9/9 PASS (G-DRIFT 404.9 < stock 477.1) |
| CHOP | identical | identical | identical | 0/none/41, 0 unexpl. (identical) |
| Coherence | identical | identical | identical | identical (1.0/0.999999) |
| RT-LONG cue30 | 110 Hz (FAIL, same as stock) | **880 Hz** (abstain, rsn=5) | **880 Hz** (range-reject on true 30 Hz) | 110 Hz (FAIL, latch untouched) |
| RT-LONG base 440 | 440 ✓ | 440 ✓ | 440 ✓ | 440 ✓ |
| Deep vibrato 200¢ | 440 ✓ | **880 ✗ (regression)** | 440 ✓ | 440 ✓ |
| Deep vibrato 300¢+ | 880 (=stock) | 880 (=stock) | **440 ✓ (improvement)** | 880 (=stock) |
| Glide | 880 (=stock) | 880 (=stock) | **440 (changed; arguably fix)** | 880 (=stock) |
| RT-CASCADE/EDGE/COST | identical | identical | identical | identical (11.62 s; edge 14.975 s) |
| Adapts (fixture) | 137 | 137 | 137 | **513** |
| Gain range | [0.8763,1.1574] | same | same | [0.8801,1.1896], no rail-pin |
| Rail probes | — | — | — | 0 vetoes; adapts 2–3× stock; no pin |

## C-poly (test battery, stock binary)

All true overlaps (dyad, detuned unison, triad, loud+quiet, partial, edge) → `nvoice=2/3` → abstain → nominal. Count-based, not audibility-based (even a quiet second voice abstains). Voice ending before the cue window → `nvoice=1` → correct latch. Failure mode = conservative blindness, never hallucinated pitch.

## §6 verdict matrix

Frame: ≥9/9 bars, coherence ≥ NATIVE, strict win in ≥1 of {RT-LONG honest-cents, RT-CASCADE, RT-EDGE, COST} with no regression elsewhere, byte-identical reruns, §5 survival. Tie keeps NATIVE.

| Fork | §6 verdict | Rationale |
|---|---|---|
| stock C | **Does not survive §5** (cue30) | 9/9, coherence max, cascade/edge/cost strong — but the cue30 red-team attack lands: confident wrong latch to 110 Hz. |
| C-gate/rg | **REJECT** | Preregistered no-op confirmed: explicit measured-path range gate changes nothing; cue30 survives. Falsified as a fix. |
| C-gate/cons | **REJECT** | Kills cue30 (abstain→880) but regresses a legitimate case stock handles: 200¢-deep vibrato latching → abstains to wrong nominal. Regression elsewhere. |
| C-gate/plan | **RECOMMENDED §5 fix** | Kills cue30 (880 via range-reject on true plan pitch 30 Hz); no regressions — base RT-LONG, lies, poly identical; glide and deep-vibrato strictly improve. Cost/edge/cascade identical. Caveats: (1) mechanism changes from output sensing to plan-reference sensing — this is B's actual immunity mechanism, confirmed as the load-bearing difference; (2) safety gate, not recovery — renders nominal 880, not the true 30 Hz. |
| C-deadband | **Viable refinement; tie keeps NATIVE** | 9/9 (G-DRIFT/G-PER slightly better), coherence identical, no regressions, rail-pin concern falsified (clamp+contraction are load-bearing, not the deadband). But: no strict win in any §6 category (RT-LONG/CASCADE/EDGE/COST all identical to stock) and cue30 still fails. Per the frozen tie rule, NATIVE keeps the letter. |
| C-poly | **Documents a boundary** | No code change. Proves polyphonic latch failure is conservative abstention, not hallucination. No §6 standing. |

## Notes for C-CAVEAT (shared, not duplicated)

- Rebuilt-C source/binary SHAs are in the table above; stock source SHA matches the frozen dive exactly.
- Footgun encountered: new `*mix` mode strings must be added to the `mix_write` dispatch list or the binary silently writes WAV — the exact redteam-documented trap. Caught by file-size check (2646044 = 44 + 1323000×2), fixed, rebuilt.
- Region-aware cascade analysis: region-1 blocks are 1024-aligned from 88200, so the t=3 s block is [132232, 133256), not [132096, 133120). Naive cut-point scripts misattribute in-block diffs as post-cut leakage.
- Pitch measurement: full-window ZCR/autocorrelation are contaminated by the continuous 110 Hz bed; FFT peak (50–2000 Hz) is the honest output-pitch meter. Latch-log ZCR is the detector's report, not the output pitch — keep the two separate in every table.
