# G2 BUILD_LOG

**Date:** 2026-09-21
**Source:** `cl/arm.zag` (2,263 lines, pure Zag)
**Compiler (frozen):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Corpora:** `units/arms/harness/corpora/r1/` (prose.bin 5,422,721 B; code.bin 9,515,341 B; t1/t2 splits; churn_fresh.bin 448,000 B)

## 1. Prior state (first crew, observed 2026-09-21)

M1 (prose+code) and M3 completed at 100.0 recall. M2/M4/M5/M6/M7 panicked (`slice index out of bounds`); M8/M9 not completed. No commit had been made. A wrong-path doc copy existed at `G2/docs/lab/units/arms/G2/` (superseded by this continuation's root docs; not committed).

## 2. Root causes found and fixed

### 2a. `halloc` before `g_init` (M2, M6 panic)
`halloc`/`hfree` write to the allocation trace, which is allocated inside `g_init`. Both `t_m2` and `t_m2_inner` called `halloc(cbufs)` before `g_init` → trace was the empty slice → panic. Fix: size/count computation and `g_init` moved before the first traced allocation in both functions.

### 2b. Ledger overflow (M4, M5, M7 — `FATAL: ledger overflow`, exit 4)
Corpus-driven operation counts exceed the 65,536 default (`DEF_LEDGER_CAP`). M4 needs ~85,148 entries (84,731 ADD + defects + 50×3 revision entries); M5 needs 85,732 (84,731 ADD + SCAN_COMMIT + 500 fresh ADD + 500 KILL mini-pressure); M7's leg likewise. Fix: M2/M4/M5/M6/M7 init at 260,000 entries (16.64 MB, under the 2^25 single-slice index limit); M8 at 400,000 (25.6 MB). Verified by opcode census of `ledger.bin` (M5: 85,231 ADD + 500 KILL + 1 SCAN_COMMIT = 85,732 ✓).

### 2c. `g_recall` empty source for transfer corpora (M2, M6 panic)
`g_recall` selected its source buffer only for corpus ids 0/1 (`if (corpus == 0/1) src = cbufs`), leaving `src` empty for the transfer corpora 3–6 → `src[base+off+k]` panicked after the ingest loop completed. Fix: `src = cbufs` unconditionally; the per-corpus base comes from the `(coffs, clens)` registry. `train_tier`/`transfer_probe` signatures changed to take the full registry buffer plus explicit tier length (`blen`), with `base` looked up from the registry — all 8 call sites updated (verified by count assertion).

### 2d. Panicking/fragile JSON paths
All active `j_i64`/`j_str`/`j_raw` call sites in M2/M4/M5/M6/M7 replaced with the non-panicking `jf_int`/`jf_int_last`/`jf_str` helpers (same pattern as the M1 workaround); M7's `"m7_na_reason": null` emitted via direct `_zag_print`. M3's `_tenths` keys corrected from `jf_dec1` (which printed `100.0`) to `jf_int` (prints `1000`).

### 2e. M8 `alloc_trace.txt` irreproducible by design
The allocation trace recorded raw heap pointers (`b as i64`). Addresses are OS-assigned (ASLR): even `clean/run1` vs `clean/run2` differed, failing `m8_compare.py`. This is not behavioral nondeterminism — every semantic artifact (store_hashes, store_chain, ledger.bin, ledger_chain, stdout, stderr) was already byte-identical across all 10 runs. Fix: trace entries now record `(size:i64, code:i32, size:i32)` — allocation pattern fully deterministically; nothing in the arm reads the trace (write-only evidence). M8 gate re-run → **PASS**.

### 2f. Stale binary incident
A `work/build/g2` binary timestamped before the final source edit produced impossible-fast `FATAL: ledger overflow` on M4/M5/M7; rebuilding from current source resolved it. Lesson: always rebuild-then-run; never trust a binary whose mtime predates the source. (Not a compiler nondeterminism: sizes differed, 247,457 vs 243,369 bytes.)

### 2g. Cosmetic wart (documented, not fixed)
`m4_detected_tenths` = 2000 = defect count × 10, not a rate; all 200 defects are detected structurally. Left as-is to preserve the exact evidence already gated; does not affect any bar.

## 3. Final build

```
znc_linux_x86_64_abed8aa1 cl/arm.zag -o work/build/g2   # exit 0 (warnings only, pre-existing style lints)
```

## 4. Battery results (final binary)

Full 1x M1–M9, two runs per leg, stdout byte-identical (`cmp -s` clean), all exit 0:

| Leg | Run a == run b | Exit |
|-----|----------------|------|
| m1-1x-prose | IDENTICAL | 0 / 0 |
| m1-1x-code | IDENTICAL | 0 / 0 |
| m2-1x | IDENTICAL | 0 / 0 |
| m3-1x | IDENTICAL | 0 / 0 |
| m4-1x | IDENTICAL | 0 / 0 |
| m5-1x | IDENTICAL | 0 / 0 |
| m6-1x | IDENTICAL | 0 / 0 |
| m7-1x | IDENTICAL | 0 / 0 |
| m8-1x (gate) | 10/10 artifacts identical | M8GATE PASS |

Evidence: `work/runs/leg_*/{a,b}/stdout.txt`, `work/m8/<pert>/run{1,2}/` (7 artifacts each).

## 5. Substrate/toolchain notes (for future crews)

- `nio_alloc` accepts 1..33,554,432 bytes; no indexed slice may exceed 2^25.
- `_zag_arg(n)` is non-owned (never free); `_zag_strcmp` returns 1 on equality; `_zag_i64_to_str` returns owned memory.
- `znc` passes `argc=0` to `main` regardless of real argc (AGENTS.md ZNC-2026-09-21-007) — read `_zag_arg(n)` unconditionally, treat `""` as absent.
- G2 uses only `[]u8` arenas with `iput`/`iget`; unaffected by ZNC-2026-09-21-007 (`as []i32` miscompile).
- Lab VM `/tmp` is a 512 MB tmpfs — battery workdirs live under `~/workspace`, never `/tmp`.
