# PREREG — Certifier rebuild (red-team attack #1)

**Date:** 2026-09-21 (PDT) · **Crew:** CERTIFIER-REBUILD · **Parent:** red-team "too good to be true" verdict, attack #1 (commit `bc61ef55`, `docs/lab/redteam/REDTEAM.md`)
**Status:** FROZEN before any rebuild code. This document governs the rebuild; amendments need a dated note.

## The question

The no-RNG law-gate certifier (`thincert.zag`, 9 casts) and the RNGSCAN v3 checker (`rngscan_v3.zag`, 30 casts) read indexed `[]i32` tables through proven-live miscompile ZNC-2026-09-21-007: the 2nd and later of consecutive same-size `as []i32` casts return the *previous* table's slots 9–11 on reads of indices 0–2. Reruns are blind to it by construction (identically wrong 5/5). Blast radius on historical verdicts is untested. This experiment rebuilds both with the documented `[]u8`+accessor workaround and diffs every historical certification.

## Rebuild rule (fidelity)

The ONLY permitted source change is the mechanical transformation:

- Every `let xr:[]u8=nio_alloc(N); let x:[]i32=xr as []i32;` becomes `let xr:[]u8=nio_alloc(N);` (arena kept under its `*r` name).
- Every indexed read `x[i]` becomes `t_get32(xr,i)`; every indexed write `x[i]=v` becomes `t_put32(xr,i,v)`.
- Function signatures change `[]i32` → `[]u8` for table params; call sites pass the arena.
- New helpers `t_put32`/`t_get32` (little-endian, sign-correct via i64) added once per binary.
- No logic changes, no renames of behavior, no new checks, no removed checks.

## Kill bars (applied mechanically)

| ID | Bar | Verdict if tripped |
|---|---|---|
| KB-DET | Rebuilt binaries: 5/5 byte-identical reruns on fixed inputs | FAIL — rebuild nondeterministic, stop |
| KB-FIDELITY | Source diff old→new contains ONLY the mechanical transformation (verified by diff review + a hunk-class check script) AND `t_put32`/`t_get32` round-trip unit test passes (incl. negative values, boundary indices) | FAIL — rebuild unfaithful, stop |
| KB-FLIP | For EVERY historical certification artifact with a stored attestation, run the rebuilt certifier on the same inputs and report old→new verdict. Any historical `verdict=PASS` that becomes `verdict=FAIL` = that certification is **VOID** (named explicitly). Any historical `verdict=FAIL` that becomes `verdict=PASS` = the old catch was a **miscompile artifact** (named explicitly) | Informational — this bar never "passes"; it classifies |
| KB-AUDIT | Lab-wide grep for `as []i32` / `as []u32` / `as []u16` across `~/workspace/tnn-lab`; every hit reported with file:line and blast-radius assessment (indexed reads? consecutive same-size group?) | FAIL if any hit is left unassessed |

## Historical artifact inventory (inputs must exist for a rerun)

**thincert** (`thincert <manifest> <builddir> <binary> <replay-evidence> <attestation>`):
- k2prime-redteam/scoring/plant01–20 (plant07 has no attestation — reported as MISSING): MANIFEST.work + tree buildir must be reconstructed per k2_score_batch.sh (plants/*.zag + MANIFEST.txt), binary rebuilt with pinned toolchain, replay evidence on file.
- armc-rerun-2026-09-21/thincert/evidence/{rerun,k3_rerun}_attestation.txt + evidence files; plants/dirty{1,2,3,5}_* with variation.zag + MANIFEST.txt + attestation.txt.

**rngscan_v3** (`rngscan_v3 <module.zag> <module-binary> <replay-evidence> <attestation.json>`):
- attestations/clean2 + dirty1–8; modules/*.zag sources; blind/run_audit.sh to regenerate replay evidence deterministically; module binaries rebuilt with pinned toolchain.

If any input is unrecoverable, the artifact is reported INCONCLUSIVE (input-missing), never silently dropped.

## Baseline sanity

Before trusting the diff, build the ORIGINAL sources with the pinned toolchain and confirm the old binary reproduces a sample of stored historical attestations. If it does not reproduce, the re-run harness differs from history — stop and diagnose before diffing.

## Scope boundary

- The rebuilt certifier is a measurement instrument, NOT an adopted gate. Adoption as the pinned per-build certifier needs Micah's dated amendment signature (standing rule).
- Verdict classes per artifact: CONFIRMED (verdict unchanged), VOID (old PASS → new FAIL), ARTIFACT-FAIL (old FAIL → new PASS), INCONCLUSIVE (inputs missing).
- Headline question answered in the verdict: does the no-RNG law still stand on clean evidence after the rebuild?
