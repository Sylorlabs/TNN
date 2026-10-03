# NAMECHECK: RANK-OWNER-DUPKEY

Worker: RANK-OWNER-DUPKEY (non-ledger task; claim minting paused).
Lane: docs/lab/research-lead/overnight-20260928/rank_owner_dupkey/
Parent: RANK-DUPKEY-FIX (VERDICT=PASS 8/8), additive on its
rank_dupkey_fix.zag. Substrate functions byte-unchanged.

## Step 0: toolchain guard (worker startup)

- Ran docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  equivalent: `export PATH="$HOME/safebin"` for every build/run.
- `command -v python3` -> empty. `command -v python` -> empty.
- `command -v znc` -> /home/hatch/safebin/znc.
- `cmp /home/hatch/safebin/znc <repo>/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  -> identical (ZNC-CMP-IDENTICAL).
- All research logic in pure Zag. Shell only: znc invocation,
  binary runs, sha256sum, git ops, file moves. No python invoked;
  any forbidden-interpreter invocation would be PROCESS-FAIL
  (none occurred).

## Analyzer/toolchain audit (on implementation)

- No `while.*!(` negated conjunctions in new code.
- No _zag_print; output via the single preallocated buffer +
  one _zag_raw_syscall write (carried over).
- No `as *i32` slice construction; if-nesting at most 2 in new code.
- No new `as *u8` (the one approved z_alloc cast carried over).
- `// znc:allow` lines: none expected in new code (all return
  values used).
