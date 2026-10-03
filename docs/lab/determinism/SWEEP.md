# Determinism Sweep — TNN program (2026-09-27)

**Law under test:** zero randomness anywhere in TNN's decision paths — every mechanism deterministic given state, byte-identical reruns. A single hidden nondeterminism source poisons all evidence, so this sweep verifies the law across every adopted mechanism with a frozen battery.

**Method (uniform across 4 sector probes):**
1. Sources extracted from COMMITTED tree only — `git archive origin/tnn-native-lab @ 5b661730da28fe61e5c9e4477786bfd606639910` — the working tree was never read or built (other crews were actively editing it).
2. Built with the pinned toolchain `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (verified `znc 2026.07.0-dev`, SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`), following each battery's committed build recipe.
3. Each frozen battery run **twice** from the same build; every output `sha256sum`'d and byte-diffed run1 vs run2.
4. **Allocator-luck probes:** 3 extra runs per flagship battery under perturbed layouts — (a) `env -i` minimal env, (b) env padded with large dummy vars, (c) different cwd. Shifts heap/stack layout; catches uninitialized-memory or address-dependent behavior that looks stable in only one layout (the program has precedent: arms that "worked" on allocator luck).
5. White-box scan of each source for RNG/clock/env/pid/address-ordered iteration.

Sector reports with full commands, SHAs, and build recipes: `~/workspace/det_sweep/{text,intel,image,audio}.md` (probe scratch; not committed).

## Verdict

| Sector | Mechanism (committed source) | Determinism | Battery integrity | Detail |
|---|---|---|---|---|
| text | Dialogue round-4 `docs/lab/dialogue/round4/dialogue.zag` | **PASS** | PASS (caveats) | Byte-identical ×2 on all 3 batteries + 3/3 perturbed runs; 38/38 reproduces exactly; zero RNG/clock/env syscalls |
| text | Deliberation repair #4 `docs/lab/dialogue/deliberation/build/deliberate_frozen_r4.zag` (SHA matches BAR_RESULTS.md pin `7dec26d8…a61b787`) | **PASS** | PASS | Byte-identical ×2 on R4/B20/heldout + 3/3 perturbed runs; R4 27/29, B20 28/28, heldout 20/20 — every adoption number reproduced |
| intel | One-brain round 3 `docs/lab/onebrain3/` (44-item v6 set) | **PASS** | PASS | 9/9 modes byte-identical ×2 + 3/3 perturbed runs; 27/27 committed traces match; single 20/44, onebrain 23/44, ablate 21/44, poison 4/44, min 23/44 all reproduce |
| intel | Epistemic native train-LOO `docs/lab/epistemic_native/implementation/epistemic.zag` | **PASS** | PASS | 5 LOO runs (448 claims each) byte-identical, SHA `f5666e76…a518efc5` == committed `evidence/verdicts_train_loo.tsv`; label-blindness preserved (opaque V1–V4 IDs only) |
| image | Promoted chunker `docs/lab/mg_chunking_promote/` | **PASS** | PASS | battery1 RUN1==RUN2==env−i==padded==cwd → `0a341163…a41d268` == committed `evidence/RUN_LIVE*.out` (57/57/57/0); degen → `8880c82e…955` == committed (6/6/6/0); zero RNG/time/seed references in any .zag |
| image | Upscale round-1 `docs/lab/image_upscale/` | **PASS** | **PARTIAL** | Prep + Phase-1 upscale byte-identical across all runs and == committed evidence; Phase-2 outpaint **deterministically broken** (see work orders) |
| audio | MP3 decoder `docs/lab/universal_intake/mp3/zag_full/` | **PASS** | PASS (1 blocked) | 3 fixtures byte-identical ×2 and == committed BUILD.md SHAs; pow_43_z full-domain sweep (x=0…8206) == committed frozen sweep SHA; 6/6 env probes identical; white-box clean (heap zeroed-or-assigned-before-use) |
| audio | De-synth closure `docs/lab/audio_longhorizon/desynth/closure/` | **PASS** | PASS | 134 WAVs byte-identical ×2 + 3/3 perturbed runs; run1 log byte-identical to committed `battery_final_run1.log`; regenerated TSV byte-identical to committed (41 lines); white-box clean |

**FAILs on determinism: NONE. No nondeterminism was found in any adopted mechanism.**

## Follow-up work orders (battery/document hygiene — NOT determinism failures)

For the B1 fix-or-kill executor / owning lines:

1. **Text — 3 stale E-lines in `docs/lab/dialogue/round4/battery_round4.txt`** (R4-01 t2 expects the pre-G6 confabulation "Herman Melville died in 1891."; R4-01 t5 and R4-03 t4 predate adopted rendering). Byte-exact E-match is 26/29; the "23/23 good" adoption claim is qualitative. Update the E-lines. Also: the generality battery's E-lines are all literal `?` (don't-care — the runner's FAIL marks there are meaningless), and the B20 battery lives at `trace-trial/trial/battery20.txt` but is cited by path in no deliberation doc — record it.
2. **Intel — naming drift:** round 3 is committed as `docs/lab/onebrain3/`, not `docs/lab/onebrain/` (rounds 1–2). Also: the committed `R33_NATIVE_IO_V1.zag` under `docs/generations/R33/…` is darwin-flavored and fails linux builds; the working linux copy at `docs/lab/onebrain3/impl/` should be the canonical one.
3. **Image — Phase-2 outpaint deterministically broken, not nondeterministic:** rc=1 with identical stdout every run (`shapes regions 18 / no border region at row 160`). Root cause: the rectangle-fix commit `f67e98933` changed region tiling (36→18 regions via genuine reject); `azoutpaint.zag:127-158` requires every output row to have a SHAPES region with `rx+rw==256`, which now fails at row 160. Committed `evidence/SHASUMS.txt` and `OUTPAINT_TRACE.txt` are stale (pre-fix). Regenerate or retire Phase 2 and refresh the evidence files.
4. **Audio — frozen 34-driver Huffman / 33-frame stress rerun BLOCKED:** the generators were never committed (STRESS_REPORT documents them as "in workdir, uncommitted"). Not a determinism fail, but the stress battery is unrepeatable until they're committed. Also: the extraction-window SHA in STRESS_REPORT (`c47f8ce8…`) didn't reproduce under 10 plausible byte windows — documentation gap only (output arithmetic proven identical by the sweep check).

## Notes
- Disk was at 99–100% during the sweep; the audio probe's full run set completed before the 100% event and all artifacts were verified intact afterward. Probe scratch cleaned.
- This is a sweep: no fixes were made. Work orders above go to the owning lines.
