# MINI-PREREG M4 — Determinism-by-construction subset compiler

> **FROZEN — 2026-09-25** under `PREREG_GATE_EXPANSION.md`.
> Method: don't detect RNG in arbitrary code — refuse to compile
> non-deterministic code. The gate is constructive: "this binary was
> produced by the subset compiler from this source," not "no scan found
> anything."

## 1. Hypothesis

Post-hoc scanners (v1–v3, thincert) lose because they accept arbitrary
Zag and then hunt an inexhaustible idiom space. Invert the burden: the
variation path must be written in a restricted dialect whose every
construct is deterministic by construction. The compiler is small (its
own audit is tractable) and REFUSING — non-dialect code is not scanned,
it is rejected. There is no idiom space to exhaust because there is no
detection step.

## 2. The dialect (frozen)

A variation module is subset-clean iff ALL of the following hold
(checked by `m4_subset.zag`, pure Zag, pinned toolchain):

- **D1 — no raw syscalls:** the token `_zag_raw_syscall` appears NOWHERE
  outside the pinned substrate allowlist files
  (`substrate/R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`,
  committed SHAs). Any other file containing it → REFUSE.
- **D2 — no argv/env access:** the token `_zag_arg` with any index
  outside the committed whitelist `{1,2,3,4}` (input/state slots), and
  NO occurrence of `_zag_arg(0)` (program path) → REFUSE. No `getenv`
  or env-token of any spelling → REFUSE.
- **D3 — no uninit allocation:** bare `nio_alloc` is banned in the
  dialect. The only allocation primitive is `z_alloc_init(n, byte)`
  (alloc+fill, provided by the subset prelude). Any `nio_alloc` token
  outside the prelude → REFUSE.
- **D4 — no hash iteration:** tokens `bucket`, `slotmap`, `hashmap`,
  `map_iter`, `bucket_iter`, or any `for`-over-associative-structure
  pattern in the committed pattern list → REFUSE. Indexed arrays only.
- **D5 — pinned file IO:** file-open path arguments must be
  compile-time string literals present in the committed path allowlist
  (data files only). Computed paths, non-literal paths → REFUSE.
- **D6 — no timing/entropy intrinsics:** tokens `rdtsc`, `rdseed`,
  `rdrand`, `clock`, `time` (as identifiers, word-bounded) → REFUSE.
- **D7 — no address exposure:** taint set seeded by `&x`,
  `_zag_arg(...)`, and `z_alloc_init` returns; any `as i64/i32/u64/u32`
  cast applied to a tainted expression → REFUSE (blocks pointer→int
  leaks including ASLR).
- **D8 — transitive closure:** all `@import`ed files (bare directives)
  are checked under D1–D7 except the pinned substrate files.

**Verdict:** all rules hold → `CERTIFY` (emits certificate: source SHA,
dialect version `M4-2026-09-25-v1`, rule-hit counts, all zero).
Any refusal → `REFUSE` with rule + file + line cited.

The gate: the shipped variation binary must be built by the pinned
toolchain from subset-certified sources; the certificate travels with
the build. A rebuild restarts certification.

## 3. Battery mapping (pre-declared scope — frozen)

| Plant | Expected | Rationale |
|---|---|---|
| P01 getrandom | REFUSE (D1) | raw syscall token |
| P02 clock_gettime | REFUSE (D1/D6) | raw syscall / clock token |
| P03 /dev/urandom | REFUSE (D5) | path not in allowlist |
| P04 uninit read | REFUSE (D3) | bare nio_alloc banned |
| P05 env-var | REFUSE (D2) | env token |
| P06 ASLR leak | REFUSE (D7) | tainted cast |
| P07 rdtsc | REFUSE (D6) | intrinsic token |
| P08 hash order | REFUSE (D4) | iteration pattern |
| P09 innocent tables | CERTIFY (clean) | indexed arrays are dialect-legal — correctly not flagged |
| P10 machine-id | REFUSE (D5) | path not in allowlist |
| P11 argv[0] | REFUSE (D2) | `_zag_arg(0)` banned |
| P12 invoke-discard | REFUSE (D1) | invocation contains the banned token regardless of consumption |

**Counting rule (frozen):** REFUSE on dirty = CAUGHT; P09 must CERTIFY.
No out-of-scope declarations: M4 claims full coverage; any miss kills.

**K-CLEAN mapping:** C01,C02,C04,C05,C06 must CERTIFY. The crew must
write the clean modules IN the dialect (this is part of the test — if
the dialect cannot express lawful variation, that's a finding, not a
free pass; a clean module that cannot be written in-dialect is recorded
as a dialect-expressiveness gap and counts as a K-CLEAN failure).
C03 (fenced RNG): declared OUT-OF-SCOPE pre-test — the dialect has no
RNG construct by design.

## 4. Kill-bar instantiation

- K-CATCH: 12/12 decided correctly (11 REFUSE + P09 CERTIFY).
- K-CLEAN: 5/5 CERTIFY (C03 out-of-scope pre-test).
- K-RED: 12 novel plants, blind, per umbrella §5. Expected red focus:
  dialect-edge smuggling (encode a banned token across string
  concatenation, e.g. `"_zag_"+"raw_syscall"`; hide casts behind
  macros/aliases the taint set doesn't track; abuse the pinned
  substrate allowlist by adding a file to it — the red team may NOT
  modify pinned files, but may try to get the CHECKER to trust them).
  The red team receives the D1–D8 rule list (it must, to design novel
  plants) but NOT the implementation.
- K-DET: 3/3 byte-identical full-battery reruns (certificates stable).

## 5. Known hard problems (stated pre-test)

1. **Token-splitting:** `"_zag_raw_"+"syscall"` defeats word-boundary
   token rules. Frozen answer: D1/D6 are evaluated on the source AFTER
   constant-folding string concatenations (the checker implements a
   mini constant-folder for string literals; committed pre-test).
   Residual: runtime-constructed strings are not syscalls by
   themselves — only their USE in call position matters; the checker
   flags any identifier resolving to a banned token through alias
   assignment (`let f = _zag_raw_syscall` tracked in the alias table).
2. **The checker is itself attack surface:** a bug in m4_subset.zag is
   a gate hole. Mitigation (frozen): the checker is <1500 lines, its
   own source is committed, and the red team is explicitly invited to
   attack the CHECKER (not just the dialect). A checker bug that lets a
   dirty plant certify is a K-RED kill.
3. **Expressiveness risk:** if C02 (lawful variation) cannot be written
   in-dialect, M4 is useless as a gate regardless of catch rate. This
   is measured, not assumed (K-CLEAN).

## 6. Evidence layout

`wave12/step1a-v2/gate-expansion/evidence/m4/`:
`m4_subset.zag`, dialect prelude, pinned allowlists, per-plant
verdicts, `M4_VERDICT.md` with the kill table.
