# Phase 4 — differentiation: TNN distinguishes who's talking to it

**Status: COMPLETE 2026-09-27. Verdict: claim C UPHELD** (see `VERDICT.md`).

## Question

Does TNN genuinely model *people* — distinguishing interlocutors through
interaction identity — or does it merely partition facts by name tag?

## Answer (preregistered, sealed, red-teamed)

It differentiates **by interlocutor identity**. The name is a mutable
attribute of the person record: renaming never moves facts (S1/R2),
recycling a name never inherits them (S2), two persons can share a name
without merging (S3/R1). A name-keyed lookup fails the battery by
construction; this implementation passes it, so the "just a name-keyed
lookup" hypothesis is dead.

## Layout

| Path | Contents |
|---|---|
| `PREREG.md` | Frozen prereg (committed BEFORE implementation: commit `d97743268a8ff3ccedc637ecfdab07f8293ec965`) |
| `VERDICT.md` | Honest verdict with honest scoping |
| `build/p4.zag` | Pure-Zag person-substrate interpreter (27 KB, zero RNG, zero structs, `[]i64` tables only) |
| `build/R33_NATIVE_IO_V1.zag` | Native I/O substrate (workbuddy round-2, unmodified) |
| `build/BUILD.md` | Build notes, toolchain pin, znc lessons applied |
| `sealed/` | Sealed battery: generator + `bindings.txt` + SHA256SUMS + probes `s1.txt`–`s8.txt` (seed 20260927) |
| `battery/` | Runner (3× byte-identical gate), strict scorer (exact R-lines + FNV-1a chain), structural expectations |
| `redteam/` | Novel attacks `r1`–`r6` (fresh seed 20260928), `REDTEAM.md`, hardcode audit |
| `results/` | Canonical 3×-verified outputs (`*.out`) + all three runs + `SHA256SUMS_RESULTS.txt` |

## Protocol (single line per person-session)

`open pN` → `name pN <name>` → `teach` / `secret` / `assert` / `correct` /
`recall` / `belief` / `judge` / `who` / `profile` / `topics` / `close`.
Every input line gets an `L` ledger line; every result an `R` line; the run
ends with `R chain <FNV-1a-64 hex>` over all preceding R/L lines (chain line
itself excluded). Unknown persons/topics → `WITHHOLD`, never confabulation.

## Reproduce

```
cd build
<toolchain>/znc_linux_x86_64_abed8aa1 p4.zag -o p4_bin
./p4_bin ../sealed/probes/s1.txt
bash ../battery/run_probe.sh s1
python3 ../battery/score.py ../results
```
