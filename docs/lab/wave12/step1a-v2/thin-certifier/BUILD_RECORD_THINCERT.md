# THINCERT Build & Freeze Record — 2026-09-20

Implementation of PREREG_THIN_CERTIFIER.md (commit d433fc8ba3cda35e141876e15f98a6b1ad8eddb3).
Status: AMENDMENT-PENDING (AMENDMENT_2026-09-20_THINCERT_R3.md is DRAFT, awaiting Micah's re-approval).
No K gate is final until the amendment is approved.

## Frozen implementation hashes

| Artifact | SHA-256 |
|---|---|
| `certifier/thincert.zag` (952 lines) | `9b55fa2f158d98c31b4011c09f2f2a4394e740d9fa95450cad2ad5bdea9bbbd3` |
| `runner/run_thincert.sh` (99 lines) | `b5bfff3d2d3f4fd94b99ec844f269d5161a3596ac7fa898665f1af5fe0eee343` |
| `certifier/substrate/R33_NATIVE_IO_V1.zag` (vendored) | `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` |
| `certifier/substrate/R33_NATIVE_SHA256_V2.zag` (vendored) | `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` |
| Built `thincert` binary (this source, znc_linux_x86_64_abed8aa1) | `d5e4de746a790b234726a3bcd5043bbfb7487fea203f7005e88b8c8012f2d3ca` |

Binary is byte-reproducible: rebuilding `thincert.zag` with the pinned toolchain
reproduces `d5e4de74…` exactly (runner aborts exit 3 on mismatch).

## What the certifier does (pure Zag, no RNG)

- Whole-file deterministic IO + SHA-256 (vendored substrates).
- Comment/string stripping; string literals extracted separately for R6b.
- R1: manifest parse → per-file source SHA-256 verify → recursive `getdents64`
  tree-walk correspondence (no unlisted `.zag` files) → import correspondence
  (`@import` targets resolve to manifest-pinned substrate files, normalized
  relative-import check).
- R1b: Tier-S substrate bytes must equal the prereg-pinned known-good hash.
- R2: Tier-M = exactly the 6 prereg intrinsics; any other `_zag_*` in module → FAIL.
  Tier-S = Tier-M + `_zag_malloc/_zag_free/_zag_slice_ptr/_zag_raw_syscall`.
  `_zag_raw_syscall` first arg must be an integer literal in the prereg allowlist.
- R4: no `struct`, no slice types, no pointer types, no `as *` casts in module.
- R4b: module code may not define/shadow `nio_*`.
- R5: only `while` loops; canonical skeleton enforced.
- R6a: explicit banned tokens (`_zag_rand`, `_zag_clock_monotonic_ms`, …).
- R6b: banned literal substrings (`urandom`, `/dev/`, `/proc/`, `/sys/`, …).
- R7: trial binary SHA-256 must equal manifest `BIN` entry.
- REPLAY: evidence must assert byte_identical=1, varies_with_state=1,
  exit_ok=1, rebuild_ok=1.
- Writes a deterministic text attestation; exit 0 PASS / 1 FAIL / 2 IO.

## Validation 2026-09-20 (this build)

Clean representative build (repbuild, frozen manifest):
- Full runner pipeline: rc=0, verdict=PASS. All R1–R7 PASS, REPLAY=PASS
  (8-condition interim matrix: byte_identical=1, varies_with_state=1).
- v2 tripwire (informational): PASS.

Dirty plants (static source plants; exact failure attribution verified):
| Plant | Result | Rule hit |
|---|---|---|
| dirty1_urandom (`_zag_rand` + `/dev/urandom`) | FAIL | R6a:`_zag_rand`, R6b:`urandom` |
| dirty2_clock (`_zag_raw_syscall(228,…)`) | FAIL | R2:`_zag_raw_syscall` |
| dirty3_uninit (uninit `nio_alloc` read) | PASS (static) | — documented R3′ residual: reads deterministic zeros |
| dirty5_ptrleak (`_zag_slice_ptr` in module) | FAIL | R2:`_zag_slice_ptr` |

## Bugs found and fixed during bring-up

1. `nio_read_exact` max-bytes guard rejected the 33,554,432 size class → R7
   "binary unreadable". Fixed to 33,554,431.
2. `walk_fd` path prefix was `nio_alloc(1)` (len 1, a NUL byte) instead of a
   true empty slice → every walked path had a leading `\0` → R1 B-UNLISTED.
   Fixed with `nio_alloc(0)`.
3. `att_kv` emitted a redundant `=` separator; fixed to clean `key=value`.
4. R6a/R6b (and R4/R4b) shared one detail buffer → failure attribution
   clobbered. Now separate buffers per rule.
5. Runner wrote no evidence file before invoking the v2 tripwire → ERROR.
   Now writes v2-schema evidence (`state_words` included).

## K-gate status (honest)

- K1′ (allowlist + replay matrix): implementation complete, clean PASS on the
  representative build; dirty-plant matrix behaves as specified. FINAL only
  after amendment approval + blind K2′.
- K2′ (blind red team): NOT RUN — requires a separate blinded agent (this
  session is depth 2/2 and cannot spawn one). Parent/coordinator must delegate.
  No certifier edits once K2′ starts.
- K3′ (hardened replay vs exact frozen binary): INTERIM PASS (8-condition
  matrix, byte-identical 1–7, varies on 8). FINAL requires the phase-1
  hardened replay harness; interim evidence is real but not the hardened bar.
- Amendment: DRAFT, pending Micah. Until approved, verdicts are provisional.
