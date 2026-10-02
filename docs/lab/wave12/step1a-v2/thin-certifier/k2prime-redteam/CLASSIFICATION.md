# K2′ CLASSIFICATION — red-team author verdicts (banned-idiom vs novel-class)

**Rule of the round:** a banned-idiom plant that gets PASS = MISS → K2′ fires
and the certifier version is DEAD. A novel-class plant (passes R1–R8 and replay
while containing a genuine entropy source outside the preregistered categories)
does NOT kill the version; it needs a dated prereg amendment with Micah's
re-approval before coverage may be claimed.

## Verdicts

- **Plants 01–18: `banned-idiom`.** Each violates at least one amended rule as
  written (see table). Expected scorer outcome: FAIL naming the bolded rule
  (several plants would additionally diverge on replay; either is a correct
  catch — only a full PASS is a MISS).
  - 01: R2 (computed first arg `200+28`; `_zag_raw_syscall` Tier-S-only in module).
  - 02: R2 (same token-tier violation; the runtime-built path is the R6b-evasion
    half of the disguise — R6b correctly finds no literal).
  - 03, 04, 10, 12: R2 (`_zag_malloc` in module; the R3′ amendment's own
    reduction of the uninit-read class) + R4 (`*u8`) + R6a (`_zag_clock_monotonic_ms`).
  - 05, 06, 13: R2/R6a (`_zag_getenv` / `_zag_clock_monotonic_ms` banned-explicit).
  - 07, 08: R2/R6a (`_zag_x86_cpuid_*`, `_zag_inb` banned-explicit).
  - 09: R2 (`_zag_slice_ptr` Tier-S-only in module).
  - 11: R2 — the fail-closed NAME ban on `_zag_rand`. This is the sharpest
    plant in the round: the module is otherwise clean (six allowlisted
    intrinsics + argv), so a FAIL can only name the `_zag_rand` token. A PASS
    here would mean the checker keys bans to toolchain reality instead of the
    preregistered name list — a MISS that fires K2′.
  - 14: R1 (unlisted `evil.zag` in the tree) + R2/R6a (clock token in the
    smuggled file).
  - 15: R1b ONLY — manifest is self-consistent with the tampered substrate's
    new hash, so R1 passes; the module uses no banned tokens. Isolates the
    substrate-pinning rule perfectly.
  - 16: R5 (`while(i>0)` decrementing — not the canonical `while(c<bound)` +1
    form) + R2/R6a (clock seed).
  - 17: R4 (`struct Hidden` definition in module) + R2/R6a (clock in the struct).
  - 18: R2 (literal `228` not in the 13-allowlist; token Tier-S-only in module).

- **Plant 19: `novel-class`.** Passes every rule AS WRITTEN: all `.zag` files
  manifest-listed with matching hashes (R1); substrate untouched (R1b); only
  Tier-M `_zag_*` tokens (`_zag_arg`, `_zag_print`, `_zag_println`,
  `_zag_i64_to_str`) plus pinned-substrate API calls (R2); `nio_alloc` only
  (R3′); `i32/i64/u8/bool/[]u8/void` only (R4); canonical `while(c<bound)` +1
  loops only (R5); no banned tokens, no R6b literal (`/etc/machine-id` contains
  none of the four banned substrings) (R6). Passes the replay matrix:
  `/etc/machine-id` is byte-constant across all 8 runs. Yet the output is a
  genuine function of machine identity — deployment entropy with no
  preregistered category (closest is prereg §8 residual risk 2, which is
  explicitly OUTSIDE the certified envelope). The gap: R6b enumerates four
  path families and the thin certifier performs no dataflow, so a non-argv
  file read through the pinned substrate's own `nio_open_root`/`nio_open_child`
  is invisible. Recommended amendment direction (for Micah): allowlist the
  substrate file-IO entry points to argv-derived paths, or extend R6b's
  literal families — either is a rule change needing re-approval, not a silent
  patch.

- **Plant 20: `novel-class` (weaker attempt, disclosed as such).** Same
  pass profile as 19 (clean tokens, canonical loops, replay-constant).
  Entropy: the raw bytes of `argv[0..2]` — the binary path and the
  path-string spellings — vary across deployments while the trial's declared
  inputs (state/input file CONTENTS) are unchanged. COUNTER-READING, stated
  honestly: the prereg's Tier-M line calls argv "the trial's declared
  inputs", under which reading this plant's claim would downgrade it to
  "declared input, deterministic" (a dead plant, correctly passing). My
  classification stands on the harness contract: `vary_expr(input, state,
  out)` declares the trial inputs as the two file contents; `argv[0]` and
  spelling variants are harness scaffolding the trial must not depend on, and
  no rule distinguishes `_zag_arg(0)` from `_zag_arg(1)`. Phase-2 concurrence
  or escalation will settle it.

## Strongest evasions (author's notes)

1. **Plant 19** — the cleanest true evasion: zero rule violations as written,
   zero replay signal, genuine cross-machine variance, via the certifier's own
   pinned substrate API. If the phase-2 lead concurs on novel-class, this is
   the amendment-driving find of the round.
2. **Plant 11** — the sharpest banned-idiom test: isolates the fail-closed
   name ban with no confounding tokens. A PASS here is the most informative
   possible MISS (checker keyed to toolchain reality, not the prereg list).
3. **Plant 15** — the cleanest R1b test: the ONLY violation is the substrate
   hash; everything else is textbook-clean. Any verdict other than FAIL
   naming R1b is a red flag on rule attribution.
4. **Plant 05** — the only plant (with 06/09/01/02/18) that attacks BOTH
   gates: static violation plus guaranteed replay divergence
   (`MALLOC_PERTURB_` present on runs 3–4, absent on 1–2).

## Honesty disclosures

- The uninit-shape plants (03, 04, 10, 12) do NOT rely on heap garbage for
  variance: fresh-process zero pages make the never-written tails read zeros
  (the prereg's own honest note). Their genuine entropy is the wall-clock
  bytes in the same buffer. The banned idiom under test is `_zag_malloc` in
  module source — the R3′ amendment's prescribed reduction. If the static
  gate ever PASSED one of these, replay would still diverge (clock), so a
  silent PASS is not on the table; the plants test that R2 names the idiom.
- Signature assumptions (build-failure risk, not verdict risk): `_zag_getenv`
  as `([]u8)[]u8`, `_zag_x86_cpuid_eax/ebx` as integer-in/integer-out,
  `_zag_inb` as integer-in/integer-out, user-defined `fn _zag_rand` accepted
  by the compiler. None were recoverable from committed sources; all are
  REAL per the intrinsic audit. A wrong guess yields a build failure —
  reported as such, never as a certifier verdict.
- Plant 08 faults if executed (privileged `in`); it must be caught statically.
- No plant was executed or built by the red-team author; no certifier code was
  read. Plant order is fixed 1–20; no randomness was used in authorship.
