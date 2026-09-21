# R2 Build Log

## 2026-09-21 — arm.zag construction

Built `cl/arm.zag` (~1800 lines, pure Zag, zero RNG) in six appended chunks:
1. Store core: R2 struct, ID/slot/span hash maps, ingest/dedup/supersede,
   recall, kill/pin/weaken/defect/revise, FIFO eviction, allocator trace.
2. Compounding-elimination segmentation engine (FNV-1a 64B blocks, cheap
   candidate proposal on recurrent adjacent fingerprints, pair-recurrence
   acceptance, 3-block prune on elimination), file I/O, JSON helpers,
   generic segmentation probe, M1 (with A15 swap probe), M2+M9.
3. M3 strength trial, M4 defect revision, M5 resource accounting.
4. M6 transfer, M7 ID-arm rig, M8 determinism gate, main dispatch.

## Bugs found during smoke testing (all fixed, all in source)

1. **m4 infinite loop (hang):** the final "killed" counting loop was missing
   `j=j+1`. Found by timeout; fixed.
2. **m3 slice-OOB panic:** valuable selection `cidx=v*total/1000` assumed
   ≥1000 chunks; panicked on small corpora. Replaced with `nv=min(total,
   1000)` spread (`cidx=v*total/nv`) and weaken spread `vj=w*nv/50`.
   Same fix applied to the t_m8 M3 sequence.
3. **m7 round-3 comparison bug:** re-ingesting C after C′ compared the new
   bytes against themselves (cmp=prose), so reverted edits were wrongly
   "reused". Now compares against cprime (the bytes the live spans reflect).
4. **m8 alloc_trace written before cleanup frees:** moved the trace write
   after all `hfree` calls so the artifact records the full lifecycle.
5. **Battery launch error (harness usage, not arm):** first launch used
   relative binary paths; `run_metric.sh` cds into per-leg dirs → rc=127.
   Relaunched with absolute paths.

## 2026-09-21 — segmentation operationalization revised (hybrid)

**Problem found:** The original 64B-block-recurrence segmentation was degenerate
on real corpora. Full M1 run on 5.4MB prose: `TAG,R2_SEG,0,0,0,0,662,prose`
(0 proposals, 0 accepts; all 662 chunks from the 8KB force-split).
Measured: 1 recurrent 64B block in 84,730; 0 recurrent adjacent pairs.
Natural text does not contain recurrent 64B blocks.

**Root cause:** The alphabet spec (ALPHABET_M-R.md §R2) does not fix a span
size. My 64B choice was arbitrary and wrong for text.

**Fix:** Hybrid operationalization — cut candidates at every 64B boundary
(cheap: zero lookup); verification context = 8B pair (4B left + 4B right),
31-bit FNV-1a, online left-to-right running counts. Pair seen before
(count≥1) → ACCEPT; else ELIMINATE. The single-pair check satisfies all
three alphabet conditions (pair co-occurs ≥2 ⇒ left/right spans recur ≥2).

**Validation (Python prototype, then Zag smoke test on 500KB prose):**
- Proposals: 7812 (constant per decile, as designed).
- Accepts: 376 (rising per decile: 24,28,17,39,32,40,49,45,39,63).
- Ratios: 32.5,27.9,45.9,20.0,24.4,19.5,15.9,17.4,20.1,12.4.
- Early-3: 33.96; Late-3: 15.95 → FALLS. Core claim holds.
- M1: recall 100.0, boundary 100.0, 378 chunks, swap 62/62.
- Deterministic (byte-identical reruns), 0 FATALs.

**Audit note:** Per-decile aggregates audited (op=41). Per-proposal/
per-elimination entries NOT written (would be ~30/KB, breaking M5's
≤10/KB bar). Documented deviation from alphabet §4 build note.

**Battery:** The 64B-degenerate battery (proc_9f609de9b6ce) was killed;
its output deleted as invalid. Full 1× battery with the hybrid binary
relaunched 2026-09-21 ~04:50 UTC (PID 388726). That run completed 17/18
legs but M8 gate FAILED on `aslr` (rc=1, "invalid or double free").

**Bug found:** `t_m8` freed `aslr_pad` TWICE (duplicate
`if(aslr_pad.len>0){nio_free(aslr_pad);}` lines). Only manifested under
the aslr perturbation (pad only allocated there). Fixed by removing the
duplicate. Binary rebuilt 2026-09-21 05:29 UTC. aslr now exits rc=0.

Full 1× battery relaunched 2026-09-21 ~05:30 UTC with the fixed binary
(session proc_8ba7c1b3dfd2). (An exec infrastructure outage delayed the
first relaunch by ~10 minutes; resolved.)

## Verification so far

- Compiles clean (warnings only; L0010 string-leak notes are the same
  `_zag_i64_to_str`+`nio_free` pattern the reference arm uses).
- Smoke corpus: all modes exit 0; m8 artifacts byte-identical across
  `none` vs `frag` perturbations.
- Full 1× battery on `harness/corpora/r1` launched 2026-09-21 ~03:15 UTC
  (background session); m1-1x-prose leg passed (rc=0, stdout IDENTICAL).

## Toolchain notes

- `znc` refused to rewrite the binary on one invocation (stale binary kept);
  `rm -f r2_bin` before recompiling to be safe.
- `nio_open_child(...,create=1)` uses O_EXCL: re-running a mode in a dirty
  workdir fails the artifact write (returns -1) rather than overwriting.
  The harness uses fresh per-leg dirs, so this is correct behavior.
- Compliant with AGENTS.md znc notes: no `zalloc`, no slice `==`, slice
  field aliases routed through pointers, audit layout stage@52/d1@56/d2@60,
  `@import` bare, no slice larger than 2^25 indexed.

## 2026-09-21 — restart replacement crew (R2 session 2)

**Cause:** previous crew killed by a runtime restart drain mid-M8 gate
(infrastructure failure, not an arm result). The drain hit during
`m8/freelist/run2` (freelist run1 complete, run2 empty). All other artifacts
intact.

**Inventory on takeover:** `cl/arm.zag` (1807 lines, includes the hybrid
segmentation + the aslr double-free fix), ARM_SPEC.md, BUILD_LOG.md,
`substrate/` (R33_NATIVE_IO_V1.zag + R33_NATIVE_SHA256_V2.zag), workdir with
`battery_r1` (17/18 legs + m8 clean/frag/aslr/starve rc=0) — all inherited
outputs treated as NON-evidence per protocol.

**Verification performed:** rebuilt binary from source with the frozen
toolchain (`rm -f r2_bin` first; compiled clean, warnings only, byte-size
matches prior build). Source-audited: zero RNG in decision paths (no
rand/getrandom/clock_gettime in `cl/arm.zag`); mechanism matches the brief
(64B-boundary cheap proposals, 8B-pair FNV-1a running-count verification,
accept iff count≥1, evidence compounds online); aslr double-free fix
confirmed in source (single `nio_free(aslr_pad)` at end of `t_m8`).

**Fresh battery:** relaunched full 1× battery 2026-09-21 ~05:52 UTC into
`work/battery_r2/` with own-built binary + `work/memorizer_bin`:
**18/18 legs passed** (all `rc1=0 rc2=0`, stdout byte-IDENTICAL, fatal=0),
**M8 gate PASS** (clean/frag/aslr/starve/freelist × 2, all rc=0,
byte-identical artifacts). Scorecard assembled via
`work/scorecard_assemble_r2.py` → `work/battery_r2/scorecard_r2_1x.json`.

**Head-to-head note:** arm R has no committed scorecard or VERDICT (checked
`units/arms/R/` locally and branch `tnn-native-lab` head `aa992bb5` — zero
`arms/R/` paths). Kill disjunct (a) adjudicated PROVISIONAL-PENDING-R in
VERDICT.md; no R numbers invented.

**Committing:** source + evidence only (no binaries, no .zagd/.zag-cache, no
corpora) to `sylorlabs/TNN` branch `tnn-native-lab` under
`docs/lab/units/arms/R2/`.
