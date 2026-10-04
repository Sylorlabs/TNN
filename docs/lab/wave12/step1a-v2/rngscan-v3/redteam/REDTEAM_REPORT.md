# RNGSCAN v3 blind red-team report

**Date:** 2026-09-20
**Checker:** RNGSCAN-2026-09-20-v3 (`af0ebba954280b3af50aa79b9bc51b1c7331ecadc9369a3ba81e22776f08e055`)
**Auditor:** blind red-team subagent (this report)

## K2 VERDICT: FIRED — RNGSCAN-2026-09-20-v3 is DEAD

**Verdict-level misses: 1 (plant17) among the 17 scored plants; plants 18–20
not scored. Miss rate ≥ 1/20 > 0.** K2 fired on the first miss (plant17);
per protocol the round halted immediately — plants 18–20 were authored but
never audited, no plant21 was authored, and no v4 work was started.

### The firing miss

**plant17 — 4.4 hash-iteration order (the firing miss)**
- Disguise: a from-scratch open-addressed hash table (64 slots) with
  identifier-clean names — insert fn `stash`, iterate fn `drain`. No
  insert-family token (`insert`/`put`/`add`/`push`/`emplace`), no
  iter-family token (`iter`/`enumerate`/`foreach`), no `struct` declaration
  at all, no tripwire identifier (`hashmap`/`dict`/`bucket`/…).
- The checker's 4.4 scan is token-based; a hand-rolled table with clean
  names is invisible to it. This is the same class as the v2 killer
  (v2 plant10, `EntrySet`) — v3 did not close it.
- Attestation: verdict **PASS**, 0 banned hits, `object_byte_scan: clean`,
  `vendored_ok: true`, replay `byte_identical: true` over 8 runs × 4 layout
  variants, `varies_with_state: true`.
- Genuineness (independently verified): all 64 slots occupied; the printed
  output is byte-exact slot-order iteration of the table, reproduced by an
  independent Python simulation of the same hash function
  (`h=(k*7+3)%64`, linear probing). The slot order shapes the output — it
  is not input order.
- Root cause: 4.4 detection keys on identifier tokens and `struct`
  declarations, not on structural hash-table behavior (insert + probe +
  order-dependent iteration). A token-free table passes untouched.

## Method and blinding compliance

- Read only: `rngscan-v3/blind/` (brief, prereg, runner, harness, clean
  template, fixtures, checker binary) and the old v2 red-team report
  (authorized path `step1a-v2/redteam/`, fetched from the committed branch —
  the local directory held only a placeholder scorecard).
- Never listed, opened, or read: checker source, `BUILD_LOG.md`, dirty
  fixtures, or any other file under `rngscan-v3/` outside `blind/`.
- Frozen checker hash verified before any plant work:
  `af0ebba954280b3af50aa79b9bc51b1c7331ecadc9369a3ba81e22776f08e055` —
  matches the brief.
- Frozen toolchain: `znc_linux_x86_64_abed8aa1`. Clean template compiled
  and audited first: PASS, zero hits, 8/8 replay runs byte-identical,
  alternate state varied — rig proven end-to-end before plants.
- 20 fixed-order pure-Zag plants authored. Plants 1–6 reconstruct old v2
  plants 15–20 (raw-syscall `/proc/self/exe` read; reassigned `fn*`;
  struct of `fn*`; commented import; literal `318` as helper arg;
  sentinel-break init). Plants 7–20 are new and do not repeat the
  dirty-round shapes listed in the brief.
- Every plant was compiled and executed; genuineness verified per plant
  (3-run variation for live-entropy plants; byte-flow diffs and an
  independent table simulation for deterministic plants). Details §5.
- Audits run sequentially in fixed order with the frozen `run_audit.sh`;
  loop broke at the first rc=0 per protocol.

### Caveats (honest)

1. **Substrate copy.** `harness.zag` imports `../substrate/R33_NATIVE_IO_V1.zag`;
   the blind directory has no compilable sibling substrate layout, so
   `R33_NATIVE_IO_V1.zag` and `R33_NATIVE_SHA256_V2.zag` were mechanically
   copied from `rngscan-v3/substrate/` (a path outside the stated blind
   boundary) purely as build support. Contents never opened or inspected.
   Vendored hashes verify OK in every attestation.
2. **Plant17/18 init-loop fix.** The first draft initialized the table
   buffers with `while(zi<64)` (literal bound), which is not the strict
   canonical form (`I<B.len`), producing unintended 4.3 hits. Fixed to
   three canonical `while(zi<keys.len)`-style loops before any valid audit,
   matching the plants' documented intent (pure 4.4 test). Output
   byte-identical before/after; genuineness re-verified.
3. **First audit pass was invalid and discarded.** The initial 20 audits
   were invoked with slash-free relative fixture paths (`state1.bin`);
   the harness `load_file` requires a `/` in the path, so all replay runs
   errored (`exit_ok=0`) and every plant FAILed via REPLAY. Those results
   were thrown away; all 20 plants were re-audited with valid absolute
   paths. Only the second (valid) pass is reported.

## Per-plant results (scored: 01–17; 18–20 authored, not audited)

| plant | planted category | disguise | verdict | rules named in attestation | planted rule named? |
|---|---|---|---|---|---|
| 01 | 4.5 impure-of-inputs | raw-syscall read of `/proc/self/exe`, byte-built path | FAIL | 4.5, 4.1/4.2 | YES |
| 02 | 4.8 dynamic dispatch | reassigned `fn*`; callee reads clock_gettime | FAIL | 4.8, 4.6/4.2 (obj: imm 228), REPLAY | YES |
| 03 | 4.8 dynamic dispatch | struct of `fn*` fields (declared; literals unsupported by znc) + live `fn*` dispatch to getrandom | FAIL | 4.8 ×3, 4.6/4.1 (obj: imm 318), REPLAY | YES |
| 04 | 4.9 commented import | `// @import("phantom_impl.zag")` (real file, correctly absent); module's own raw getrandom | FAIL | 4.1/4.2, 4.6/4.1 (obj: imm 318), REPLAY | YES (4.9 correctly not fired) |
| 05 | 4.1 entropy | literal `318` as helper arg; syscall takes variable | FAIL | 4.1/4.2 (source), REPLAY | YES (source; object clean) |
| 06 | 4.3 uninit memory | init loop breaks on sentinel; tail uninit | FAIL | 4.3 | YES |
| 07 | 4.3 uninit memory | init loop with `i64` counter (not the canonical `i32` form) | FAIL | 4.3 | YES |
| 08 | 4.3 uninit memory | cross-procedure init (callee inits its param; caller buffer unproven) | FAIL | 4.3 | YES |
| 09 | 4.3 uninit memory | subrange alias `s=b[8..56]` of uninit buffer | FAIL | 4.3 (on alias `s`) | YES |
| 10 | 4.2 wall-clock | syscall number via `const CLK:i64=228` | FAIL | 4.1/4.2 (source), REPLAY | YES (source; object clean) |
| 11 | 4.1 entropy | number computed inline `(100*3)+18` | FAIL | 4.1/4.2, 4.6/4.1 (obj: imm 318 — znc folded it), REPLAY | YES |
| 12 | 4.8 dynamic dispatch | `fn*` dispatch in helper file `helper12.zag` | FAIL | 4.8 (import-graph violation), 4.6/4.1 (obj: imm 318), REPLAY | YES (FAIL; via import violation + object) |
| 13 | 4.9 commented import | commented import of real `phantom_impl.zag`; module's own raw getrandom | FAIL | 4.1/4.2, 4.6/4.1 (obj: imm 318), REPLAY | YES (4.9 correctly not fired) |
| 14 | 4.3 uninit memory | free-then-read | FAIL | 4.3 | YES |
| 15 | 4.1 entropy | `/dev/urandom` via raw openat/read, byte-built path, fd through helper | FAIL | 4.1/4.2 (source), REPLAY | YES (source; object clean — path never appears as bytes) |
| 16 | 4.2 wall-clock | syscall number via memory mailbox (228 stored as bytes, reloaded) | FAIL | 4.1/4.2 (source), REPLAY | YES (source; object clean — no 228 immediate) |
| 17 | 4.4 hash-iteration order | open-addressed table, clean names (`stash`/`drain`), no struct | **PASS** | — | **MISS (K2)** |
| 18 | 4.4 hash-iteration order | threshold probe: `_add`/`_iter` (prefix `_`, len 1 < 2), no struct | not audited | — | round halted |
| 19 | 4.3 uninit memory | return-allocated buffer read by caller (untracked name) | not audited | — | round halted |
| 20 | 4.3 uninit memory | canonical init of `b` whose expression reads uninit `c` | not audited | — | round halted |

### Rule-level accuracy (the 16 scored FAILs)

Planted rule correctly named in the attestation: **16 of 16.**
Plants 01–16 were all caught; for the live-entropy plants (02–05, 10–13,
15, 16) the FAIL also rests on REPLAY divergence (outputs genuinely vary
across runs — the replay gate doing its job, per the v2 precedent).

Object-scan notes (intel, not misses — all these plants FAILed):
- Found as immediates near `0F 05`: 228 in plant02, 318 in plants 03, 04,
  11, 12, 13.
- NOT found: 318 in plant05 (immediate at call site, >160 B from the
  syscall — extended recovery window missed it), 228 in plant10 (const),
  228 in plant16 (memory mailbox), `/dev/urandom` path in plant15
  (byte-built, never present as bytes). Source scan caught all four.

## Genuineness verification

- **Live-entropy plants** (02, 03, 04, 05, 10, 11, 12, 13, 15, 16): three
  executions each produced three pairwise-distinct outputs
  (getrandom/clock/urandom bytes flow into the printed hex).
- **Plant01** (`/proc/self/exe`): deterministic per binary, as designed;
  output bytes 0–3 are `65 5f 56 5c` = `7f 45 4c 46` (ELF magic) XOR the
  fixtures — the real file bytes flow into the output.
- **Deterministic 4.3 plants** (06–09, 14): uninit/freed bytes observably
  flow into the output (e.g. plant06's uninit tail prints as `53…`,
  plant14's freed prefix reads back changed vs the live buffer).
- **Plants 17/18**: independent Python simulation of the documented hash
  functions reproduces the binary output byte-exactly; all 64 slots
  occupied; output is slot order, not input order.
- Raw proof outputs are preserved under `genuineness/` in this directory.

## Verdict

**K2 FIRED on plant17. RNGSCAN-2026-09-20-v3 is DEAD.**
Miss rate ≥ 1/20 > 0. The 4.4 token-based detection is blind to a
hand-rolled open-addressed table with clean identifiers — the same class
that killed v2 (plant10 `EntrySet`) is still open in v3. No plant21 was
authored; no v4 work was started.
