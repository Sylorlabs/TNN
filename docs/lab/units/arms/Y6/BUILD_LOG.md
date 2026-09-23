# Arm Y6 — Build Log

Date: 2026-09-21. Author: ARM CREW Y6.

## Sources

- `units/arms/Y6/cl/arm.zag` — the arm (adapted from the B-64 reference
  `units/arms/harness/b64/cl/arm.zag`; Y6 ID/refcount/tombstone/checker
  machinery added).
- `units/arms/Y6/substrate/R33_NATIVE_SHA256_V2.zag`,
  `units/arms/Y6/substrate/R33_NATIVE_IO_V1.zag` — copied from the harness
  substrate (bare relative imports).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Build

```
znc_linux_x86_64_abed8aa1 ../cl/arm.zag -o y6_bin
```

Zero compile errors (analyzer warnings inherited from B-64 I/O patterns
only). Final binary: `units/arms/Y6/work/y6_bin`.

## Implementation notes (decisions with consequences)

1. **Ledger bound drops, not flushes.** Inherited from B-64: `b_led` silently
   drops entries past `led_cap` ("LEDGER-BOUND: scored on what completed").
   M3 sizes its ledger at 24,000 entries and fits (14,050 written); M5 sizes
   generously. Consequence: `m3_ledger_entries` is a true count only because
   the curriculum fits the cap — documented, not changed (changing it would
   break byte-parity with the reference design).
2. **M3 is the small curriculum.** Like B-64, Y6's M3 ingests 1,000 valuables
   + 3,000/4,000 fresh-churn (14,050 ledger entries), not the full corpora.
   Arm D's M3 ingests both full corpora (~244k entries). The kill-criterion
   comparison is reported per-curriculum with this structural difference
   explicit (see VERDICT.md).
3. **Checker count outputs** use a 12-byte caller buffer (`y6_checker_core`)
   because this znc build rejects direct `*i32` out-pointer dereferencing.
4. **M7 reuse/dedup are measured, not closed-form.** An earlier revision used
   a 3n formula (wrong: rounds are 2n ingests) and a hardcoded dedup 0.5;
   both were replaced with measured values (distinct live IDs from
   `s.n_live`; references counted per the documented definition) before the
   final battery. The printed M7 TAG line changed accordingly
   (`...,100.0,2.06,0.50`).
5. **`y6-selftest` mode added** (diagnostic): tombstone lifecycle +
   checker negative control. Does not affect harness modes (verified:
   harness-mode outputs unchanged — the final 1x battery re-ran everything).

## znc issues encountered

- None new beyond the documented ZNC-2026-09-21-00X series (workarounds in
  AGENTS.md). One silent `muse.edit` non-application was caught by
  grep-verification before compile; all edits are grep-verified in this
  workflow now.

## Artifact hygiene

`y6_bin`, `build*.log`, `.zagd`, `.zag-cache`, raw corpora, and incidental
`ledger.bin` files are NOT committed. Battery workdirs live under
`~/workspace/y6_battery/` (never `/tmp` — 512MB tmpfs).
