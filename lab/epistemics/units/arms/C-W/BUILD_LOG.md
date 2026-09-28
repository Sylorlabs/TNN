# C-W — Build log

## Implementation

- `cl/arm.zag`: full M1–M8 arm, written from the frozen `ARM_INTERFACE.md`,
  `HARNESS_SPEC.md`, `ALPHABET_A-F.md` (Arm C), `briefs/C-W.json`, using the
  frozen B-64 validator (`harness/b64/cl/arm.zag`) as the structural template.
  Pure Zag; no RNG substrate linked.
- `substrate/R33_NATIVE_IO_V1.zag`, `substrate/R33_NATIVE_SHA256_V2.zag`:
  Linux x86-64 ports, byte-identical in behaviour to the harness copies.

## Corpus verification (2026-09-21)

SHA-256 of all r1 corpora verified against `CORPORA.md`/manifest before any
run. Independent whitespace rescan (python) reproduced the arm's chunk counts
and max lengths exactly (table in ARM_SPEC §2).

## The 2^25 bug (found and fixed 2026-09-21)

First battery attempt: `m1-1x-prose`, `m2-t1-prose`, `m7-1x` panicked with
`slice index out of bounds`. Root cause: `nio_alloc` refuses any single slice
over 2^25 bytes (33,554,432) by returning an empty slice; the monolithic audit
ledger (123 MB for M1-prose), the M8 store image (171 MB), and M7's patch area
(79 MB, from a wasteful `pmax=4096`) all exceeded it, and the first indexed
write panicked. Temporary debug prints shifted one small-leg panic between
builds (codegen sensitivity, consistent with the documented ZNC-2026-09-19-001
hot-path miscompile note), but the architectural violation was deterministic
and is fixed properly:

1. Ledger sharded: 16 × 500,000 entries (32.0 MB each), logical order kept.
2. M8 store region hashed directly from the 8 slot arrays in 1 MB logical
   chunks (1 MB staging buffer); no image materialised.
3. M8 ledger hashed the same way (`ns_sha256` caps input at ~33.5 MB).
4. M7 `pmax` = measured max chunk length (63), not 4096.
5. All debug prints removed; per-mode capacities re-audited against 2^25.

After the fix: `m1-1x-prose` → `M1,prose.bin,100.0,100.0,1926956`;
`m7-1x` → `M7,non-id,14070` (independently recomputed from the corpus:
exact match).

## i32 overflow in probe scoring (found and fixed 2026-09-21)

`m1-1x-code` reported `m1_recall_tenths: -75.5`: `probe_chunks` computed
`cok = ok*1000/n` in i32, and `ok = 2,446,768` overflows 2^31 when multiplied
by 1000. Prose (1,926,956) squeaked under the limit, which is why only the
code leg was wrong. Fix: widen to i64 before multiplying. All other `*1000`
sites already widened first; audited and confirmed.

## Uninitialized slot-table flags (found and fixed 2026-09-21)

`cw_init` zeroed neither `flags` nor `ids`. Slot placement (`slot_insert`
skips slots whose garbage `F_OCC` bit happens to be set) would then depend on
heap garbage, which the M8 `frag` perturbation deliberately reshuffles —
exactly the failure another crew (L2) hit. Fix: explicitly zero `flags` and
`ids` over all `cap` slots at init (merged into the existing `pidx` init
loop). Determinism is now structural, not allocator luck. Post-fix smoke:
`m1-1x-prose` byte-identical to pre-fix output.

## Toolchain

`znc_linux_x86_64_abed8aa1 --backend=native`. Build emits analyser warnings
only (66, all A0102-style discarded-value notes); binary runs clean.

## Battery (2026-09-21, r1 1x)

Runner: `harness/run_battery.sh` with `cw_bin` + harness memorizer
(`mem_bin`, built from `harness/memorizer/cl/memorizer.zag`). Every leg runs
twice, stdout diffed (byte-identical rule). Workdir:
`~/workspace/cw-work/battery_r1` (kept out of the repo; binaries, caches,
corpus copies, and raw M8 `ledger.bin` files are never committed).

<!-- battery results appended below when the run completes -->

## Commits

- Implementation: <hash to be recorded>
- Evidence + verdict: <hash to be recorded>

Only `cl/arm.zag`, `substrate/*`, and `docs/lab/units/arms/C-W/` (spec, build
log, ambiguities, scorecard, compact logs, verdict) are committed. Build
binaries (`.zagd.semantic-ready`, `.zag-cache/`, `cw_bin`, `mem_bin`), corpus
files, and M8 `ledger.bin` artifacts are filtered out.

## Final 1x battery (2026-09-21, `carrier` binary)

- Binary: `~/workspace/cw-work/carrier`, SHA-256
  `4482e6d07421c9a10e2e6d3ace6718fb1a7f9b382c0c5a3d4ab088205b1e7e05`
  (byte-identical to `cw_bin`).
- Workdir: `~/workspace/cw-work/battery_r1/`.
- M1–M7 completed with rc=0 on both legs and byte-identical stdout; M1 code
  leg confirms the i64 tenths-arithmetic fix (`M1,code.bin,100.0,100.0,2446768`).
- M8 gate interruptions (all infrastructure, none an arm failure):
  - 07:04 UTC(?) machine reboot (`last reboot`) killed the first gate run.
  - Two subsequent gate launches were killed when the tool-dispatch service
    restarted under VM load (2 CPUs, load >20 from ~53 concurrent arm crews;
    no OOM — 4.4 GB available; dmesg clean).
  - Root cause of process fragility: background exec sessions do not survive
    the dispatch-service restarts; fire-and-forget `setsid nohup ... & disown`
    (no persistent session) plus a resumable gate script
    (`cw-work/cw_m8_resume.sh`, skips perturbation dirs whose artifacts are
    complete) survives.
- M8 evidence: clean/run1 == clean/run2 byte-identical on stdout, stderr,
  `store_hashes.txt`, `store_chain.txt`, `ledger_chain.txt`,
  `alloc_trace.txt`, and raw `ledger.bin` (280,689,536 bytes each).
  frag/run1 and frag/run2 text artifacts match clean; both frag runs rc=0.
- Gate in progress at time of writing: aslr, starve, freelist legs remaining.
