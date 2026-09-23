# RED-TEAM REPORT — RNGSCAN-2026-09-20-v2 blind round (20 plants)

Date: 2026-09-20. Scorer: red-team scorer subagent (blind to checker internals
until after scoring; checker source never read).

## Freeze verification (step 0)

- `checker/rngscan_v2.zag` sha256 =
  `ee962e53817c81721996a8086c5e42530da07316250b1a4906ab74a56a3d9e5d`
  — MATCHES the freeze record. Proceeded.
- Checker rebuilt from the frozen source with the recorded toolchain
  `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`; rebuilt binary sha256 =
  `9bbaf5390f140a88516d6f1912bc060610bd773af32406f7fd935c5281c41943`
  — MATCHES the freeze record exactly. Deterministic toolchain confirmed.
- Checker and runner (`runner/run_audit.sh`, RUNAUDIT-2026-09-20-v1) were
  UNMODIFIED throughout the round. All builds and binaries lived in /tmp;
  nothing was committed except the deliverables below.

## Procedure

Per prereg §8: each plant compiled in /tmp with the frozen toolchain
(vendored `R33_NATIVE_IO_V1.zag` staged alongside, resolving the bare
`@import`), then run through the frozen checker + deterministic runner with
the standard fixtures (`state1.bin`/`state2.bin`/`input.bin`). Expect FAIL;
verdict PASS = MISS. Scored in order, checker unmodified throughout.

**Halt note:** after the first miss (plant07) the scorer issued a kill to the
scoring loop. The kill took effect after plants 08–14 had already been
scored; all 14 runs used the identical frozen checker and runner — these
are valid scored results, not re-runs under new conditions. Plants 15–20
were never scored. No fixes attempted, no source edits, nothing re-run.

## K2 VERDICT: FIRED — RNGSCAN-2026-09-20-v2 is DEAD

**Verdict-level misses: 3 (plants 07, 10, 11) among the 14 scored plants;
plants 15–20 unscored. Miss rate ≥ 3/20 > 0.** K2 fired on the first miss
(plant07); the two further misses (10, 11) only deepen the verdict.

### The three misses

**plant07 — 4.3 uninitialized memory (the firing miss)**
- Disguise: the init loop is textually shaped exactly like a full init loop
  (`while(i<buf.len)`, writes `buf[`, no `return`), but only EVEN slots are
  written (`if((i&1)==0){buf[i]=...}`).
- The checker's 4.3 pattern check saw the full-shape loop and marked the
  buffer INIT; the odd slots genuinely hold uninitialized heap bytes and are
  folded into the output (`out[j]=input[j]^buf[j%64]`).
- Attestation: verdict **PASS**, 0 banned hits, object_byte_scan clean,
  replay byte_identical=true (the allocator returned fresh zero pages, so the
  uninit bytes were deterministically zero — replay could not see them
  either), varies_with_state=true.
- Root cause: the 4.3 init analysis is shape-based, not dataflow-precise —
  it does not track the conditional guard inside the loop body.

**plant10 — 4.4 hash-iteration order**
- Disguise: a from-scratch open-addressed table under the innocent name
  `EntrySet` — no banned identifier anywhere.
- The checker's 4.4 scan is token-based (`hashmap`-family identifiers); a
  hand-rolled table with a clean name is invisible to it.
- Attestation: verdict **PASS**, 0 hits, object clean, replay identical
  (iteration order happened to be deterministic across these two runs).
- Root cause: 4.4 detection keys on identifier tokens, not on structural
  hash-table behavior.

**plant11 — 4.4 hash-iteration order**
- Disguise: the same real map literally named `pin_table`, riding the
  pinned-table carve-out.
- The carve-out was honored literally: a working hash map whose slot-order
  walk feeds the output passed untouched.
- Attestation: verdict **PASS**, 0 hits, object clean, replay identical.
- Root cause: the `pin_table` carve-out is a name-based exemption with no
  structural check that the table is actually pinned/legitimate.

## Per-plant results (scored: 01–14; unscored: 15–20)

Planted categories/disguises per `PLANT_MANIFEST.md`.

| plant | planted category | disguise | verdict | rules named | planted rule named? |
|---|---|---|---|---|---|
| 01 | 4.1 entropy (getrandom) | syscall no. computed `300+18` | FAIL | 4.3 (spurious), REPLAY | NO — 4.1 missed statically |
| 02 | 4.1 entropy (getrandom) | `/dev/urandom` path runtime-built from byte codes | FAIL | REPLAY | NO — 4.1 missed statically |
| 03 | 4.1 entropy (getrandom) | innocent wrapper; literal `318` at the syscall | FAIL | 4.1, 4.3 (spurious), 4.6/4.1 (object), REPLAY | YES |
| 04 | 4.2 wall-clock | clock no. computed `200+28` | FAIL | REPLAY | NO — 4.2 missed statically |
| 05 | 4.2 wall-clock | clock no. computed `100-4` | FAIL | REPLAY | NO — 4.2 missed statically |
| 06 | 4.2 wall-clock | compiler monotonic-ms intrinsic, innocent name | FAIL | REPLAY | NO — 4.2 missed statically |
| 07 | 4.3 uninitialized memory | even-slots-only init shaped as full init | **PASS** | — | **MISS (K2)** |
| 08 | 4.3 uninitialized memory | early return on sentinel before init completes | FAIL | 4.3 | YES |
| 09 | 4.3 uninitialized memory | free-then-read on the output path | FAIL | 4.3 | YES |
| 10 | 4.4 hash-iteration order | from-scratch `EntrySet` | **PASS** | — | **MISS (K2)** |
| 11 | 4.4 hash-iteration order | literally named `pin_table` | **PASS** | — | **MISS (K2)** |
| 12 | 4.5 impure-of-inputs | `env_`-family shape (the v1 killer) | FAIL | 4.5 ×2 | YES (v1 gap closed) |
| 13 | 4.5 impure-of-inputs | `_zag_slice_ptr(out) as u64` | FAIL | 4.5 ×2, REPLAY | YES |
| 14 | 4.5 impure-of-inputs | hand-rolled `memcpy` | FAIL | 4.5 ×2 | YES |
| 15 | 4.5 impure-of-inputs | raw-syscall read of `/proc/self/exe` | not scored | — | round halted |
| 16 | 4.8 dynamic dispatch | reassigned `fn*` variable | not scored | — | round halted |
| 17 | 4.8 dynamic dispatch | struct of `fn*` fields | not scored | — | round halted |
| 18 | 4.9 commented import | `// @import("phantom_impl.zag")` | not scored | — | round halted |
| 19 | 4.1 entropy (getrandom) | literal `318` as helper arg, syscall takes a variable | not scored | — | round halted |
| 20 | 4.3 uninitialized memory | init loop breaks on sentinel | not scored | — | round halted |

### Rule-level accuracy (the 11 scored FAILs)

Planted rule correctly named in the attestation: **7 of 11**
(plants 03, 08, 09, 12, 13, 14). Plants 01, 02, 04, 05, 06 were caught only
via REPLAY divergence (their outputs genuinely vary across runs) and/or a
spurious 4.3 hit — the checker's static scans did not see the planted
entropy/clock mechanisms:

- plant01: spurious 4.3 hit (`read of seed[after free] before full init`) —
  the seed buffer is written by the kernel getrandom syscall, not by an init
  loop; the checker cannot see the syscall writes the buffer, so it flagged
  fail-closed. The planted 4.1 construct (computed syscall immediate) was
  invisible to both the source scan (literal-first-argument check) and the
  object scan (no `B8 318` near `0F 05`).
- plant02: runtime-assembled `/dev/urandom` path invisible to source and
  object scans (no path bytes in the binary).
- plants 04–06: computed clock numbers / compiler timer intrinsic invisible
  to both scans.

The REPLAY arm is doing most of the real work for the live-entropy plants.
Any nondeterminism invisible at replay time (like plant07's zeroed heap, or
plants 10/11's deterministic iteration order) walks straight through.

## K1 / K3 observations

- K1 (replay divergence on an audit-PASS build): did NOT fire. Plants 07, 10,
  11 were all byte-identical across replay runs — 07 because fresh allocator
  pages are zero, 10/11 because iteration order was deterministic in these
  runs. None of this is checker strength.
- K3 (banned construct found post hoc on a PASS path): FIRES on plants 07,
  10, and 11 — each PASS path carries a genuine planted banned construct
  (even-slots-only uninit read on the output path; from-scratch hash table
  whose slot order shapes the output; literal `pin_table` riding the
  carve-out). (Moot alongside K2, but recorded: v2 dies on two independent
  bars.)

## Score

- Verdict-level: **3 misses / 14 scored** (plants 07, 10, 11);
  plants 15–20 unscored. Miss rate ≥ **3/20** > 0 → **K2 FIRED** →
  RNGSCAN-2026-09-20-v2 DEAD.
- No fixes attempted, no re-runs, no source edits. This is the honest
  outcome this round exists to produce.

## Attestations

`attest-plant01.json` … `attest-plant14.json` in this directory
(checker_version RNGSCAN-2026-09-20-v2, banned_version BAN-2026-09-20-v2).
Plants 15–20 have no attestations — the round was halted after K2 fired,
per protocol.

## Honest caveats for the next version

1. The 4.3 uninit analysis is shape-based and unsound against conditional
   init inside full-shape loops (plant07). Needs per-slot write tracking or
   a conservative fail-closed rule.
2. The 4.4 hash-iteration check is token-based (`hashmap`-family identifiers)
   and dies against from-scratch tables (plant10) and literal carve-out
   riding (plant11). The `pin_table` carve-out is a name-based exemption with
   no structural validation.
3. Computed syscall immediates (4.1/4.2) and runtime-assembled paths defeat
   both scans; only the REPLAY arm catches them — and replay only catches
   nondeterminism observable in two back-to-back runs. Deterministic or
   zeroed-at-replay-time nondeterminism walks through.
4. The spurious 4.3 hit on syscall-filled buffers (plants 01, 03) is
   fail-closed luck, not detection: it fires on the buffer's shape, not the
   entropy mechanism, and would equally fire on a legitimate kernel-filled
   buffer in a clean module (false-positive risk for future clean modules).
