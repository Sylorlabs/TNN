# NAMECHECK: Corruption Detector Specifier

## Step 0: Toolchain guard

- Safebin activated: `$HOME/safebin` prepended to PATH.
- `which python3 python` returned nothing. Zero forbidden executables invoked.
- All work is specification writing (text files) plus read-only source
  inspection via shell text tools (grep, sed). No computation, no binaries
  built, no variant created.
- Any forbidden executable invocation would make this wave PROCESS-FAIL.
  None occurred.

## Scope

SPECIFICATION ONLY. No implementation, no unfrozen variant, no driver code.
This task specifies the CORRUPTION detector for the lifetime protocol;
it does not build it.

## Input provenance

- Eviction-corruption root cause: commit `986c52fdc`
  (`docs/lab/research-lead/overnight-20260928/eviction_corruption/EVICTION_CORRUPTION.md`)
- Zombie census with measured rates: commit `2b81d0692`
  (`docs/lab/research-lead/overnight-20260928/zombie_census/ZOMBIE_CENSUS.md`)
- Lifetime protocol v2, Section 6.1: `docs/lab/research-lead/overnight-20260928/lifetime_protocol/LIFETIME_PROTOCOL_V2.md`
- Genuine-state map (tag corrections): commit `a5b66a376`
- Frozen TNN-2 source read from git object store (read-only); frozen
  source and binary untouched.

## Constraints honored

- Zero em dashes in deliverables (byte-verified before commit).
- Paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- No sealed worlds opened.
- Nothing pushed; commit stays local on `tnn-native-lab`.
- Explicit pathspecs on both `git add` and `git commit`.
