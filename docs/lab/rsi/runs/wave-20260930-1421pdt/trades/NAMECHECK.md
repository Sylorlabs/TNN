# NAMECHECK.md wave-20260930-1421pdt trades

## Step 0 (WORKER TOOLCHAIN GUARD, mandatory)
- `which python3` returned: `/usr/bin/python3` (system runtime binary; cannot be removed from PATH without breaking runtime tools; coordinator-documented).
- Python/python3 will NEVER be invoked in this lane. Shell is used only to invoke znc, run compiled binaries, do read-only git ops, and move/copy files. All computational research logic is pure Zag.
- No forbidden-executable invocation has occurred. Wave is not PROCESS-FAIL.

## Compiler lesson applied
- No `as *i32` + `q[0..n]` slice construction inside functions. All numeric state in Zag uses u8-backed cells with little-endian pack/unpack helpers (ig/is).

## File creation order (coordinator commits centrally)
1. NAMECHECK.md (this file)
2. PREREG_TRADES.md (frozen kill bars, before implementation)
3. ORDER.txt (creation order record)
4. implementation .zg file(s)
5. test driver .zg, results logs
