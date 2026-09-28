# Toolchain characterization: function descriptors and raw code execution
(on the pinned znc, 2026-09-25; needed for P07)

## Finding

`fn as i64` does NOT yield the code address. It yields the address of a
**stack-allocated function descriptor**: `[code_addr, 0, 0, 0]`
(proven by *u64 dump: desc[0]=0x40305A, desc[1..3]=0).

Consequences:
- `i64 as fn()i64` does NOT round-trip a raw integer address. Casting a
  raw mmap address to `fn()i64` and calling it segfaults — even when the
  target is a single `ret` (0xC3) instruction. `(f as i64) != mem`
  (proven: mem=130680558571520, back=140722663002768).
- Indirect calls through a descriptor created from a REAL Zag function
  (`forty_two as i64` → `as fn()i64` → call) DO work (probe3 pattern).

## Working rdtsc mechanism (pure Zag)

1. `let faddr:i64 = tsc_slot as i64;` (descriptor on stack)
2. `let code:i64 = (faddr as *u64)[0];` (real code address)
3. `mprotect(code_page, 4096, PROT_READ|WRITE|EXEC)` via syscall 10
4. `*(code as *u64) = 12792079;` — 0xC3310F, LE bytes `0F 31 C3` = rdtsc; ret
   (the *u64 store pattern is substrate-proven; *u8 stores were not used)
5. `let g:fn()i64 = faddr as fn()i64; let v:i64 = g();`
   — calls through the INTACT descriptor; the CPU executes rdtsc;ret at
   the (now-patched) code address.

Verified: two consecutive calls return strictly increasing values
(e.g. 4156595212 → 4156595242), and values differ across processes —
a genuine hardware timestamp counter, not a constant.

## Constants (shell-verified, not mental arithmetic)

0xC3310F = 12792079. Earlier probe crashes were caused by wrong decimal
constants (0xC3390F, 0xC338DF), not by the mechanism — the readback
bytes matched the (wrong) stored values exactly, proving the store path.

## Implication for the gate

A true rdtsc plant IS buildable in pure Zag on the pinned toolchain via
this mechanism. P07 uses it. No inline assembly or intrinsic exists.
