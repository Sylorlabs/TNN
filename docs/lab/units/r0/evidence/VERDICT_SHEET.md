# R0 HARNESS — Verdict Sheet (2026-09-21)

Track R0 measurement infrastructure under `docs/lab/units/r0/impl/harness/`.
Prereg treated as FROZEN per parent/coordinator instruction (Micah signed 2026-09-21).

## Verdict: HARNESS COMPLETE — all corrections applied and verified

| Check | Result |
|---|---|
| Build (znc `abed8aa1`, sha256 `498abcb5…`) | BUILD_OK, binary `da58854f…`, byte-identical across rebuilds |
| `selftest` ×2 | `fails=0`, exit 0, stdout byte-identical (`c0193843…`), stderr empty+identical |
| `r1test` ×2 | `fails=0`, exit 0, stdout byte-identical (`33dab7e9…`) |
| M8 gate `selftest` | PASS 5/5 (stdout, **stderr**, captures identical) |
| M8 gate `r1test` | PASS 5/5 |
| Scorecard JSON | exact normative key list, flags as strings, no additions |
| Batteries run | **NONE — harness selftests only, per instructions** |

## What was built

Pure-Zag measurement infrastructure: packed 64-byte audit ledger with episode
mapping and rolling hash; probe/episode framework (kinds, routes, dose schedule
250→8000, support-gap 1..16, near-twin, split/merge scenario); R-1 aggregation
API; fixed-order corpus ingest with 2²⁴ striping; metrics-v1 evidence emitter;
M8 armor (perturbations 0–4) + 5-run gate runner; deterministic env stream with
logged fixed seed `20260921` (environment-input-only, printed at startup).

## R-1 operationalization (exact)

R-1 is implemented as an **aggregation API over battery-supplied, preregistered
probe observations** — nothing more than the frozen text defines:
- Deterministic byte-span grouping (FNV-1a-64 open-addressing table, ascending
  scans, exact occurrence accounting, truncation flags).
- Per occurrence the battery supplies `recall_success` (0/1) and downstream
  `probe_outcome` (0/1), per its manifest-defined probe recorded **before execution**.
- `b = 1` iff probe outcomes agree across **all** occurrences of the span.
- `label(o_j) = 2·a_j + b ∈ {0,1,2,3}`; `purity = max(c_0..c_3)/k` (millipoints).
- Singleton spans (k<2) are not labeled. R-7 test-both: purity mode 1 =
  recall-only variant (input flag, not a redefinition).

## Corrections applied (parent's six + coordinator hardening)

1. **Audit layout**: was 512-byte entries (offsets misread as `[]i64` indices);
   now packed 64-byte entries (`op@0, slot@4, rc@8, b1..b5@12..28,
   a1..a5@32..48, stage@52, d1@56, d2@60`), `[]u8` chunks, logical 16-value
   readback at indices 0..15, byte-level spot check in selftest.
2. **R-1 over-interpretation removed**: the invented longest-suffix reference
   predictor and ASCII-alphabetic downstream predicate are gone. Replaced by the
   aggregation API above; `R1.md` rewritten.
3. **metrics-v1**: removed top-level `"schema"` and nested m2 `"note"`;
   `m4_kill_substitution_flag` and `disqualified` are now strings
   (`"true"`/`"false"`); emitted JSON validated key-for-key against the normative
   list (exact match, no extras, no missing).
4. **M8 runner**: now hashes raw stderr per run and requires byte-identity across
   all 5 (fail-closed); negative control proved the check is live.
5. **Fetch script**: sqlite ZIP extraction via `unzip -p` (no Python).
6. **Compiler-bug audit** (coordinator): full `[]i32`/`[]i64` sequential-store
   audit — 3+ sequential store sites rewritten to `[]u8` LE cells; one live
   catch (`audit_get` 16-store loop corrupted word 12: read `65536`, expected
   `204`); remaining 2-store/single-store patterns proven by the readback-based
   `STORESEQ` probe (`fails=0`). Details: `znc_bugs.md`.

## Flagged ambiguities (not silently resolved)

1. **Stale prereg text**: local `PREREG_FREEZE.md` still says "PROPOSED — NOT
   FROZEN" / "Micah must approve/amend" on R-1, contradicting the signed-freeze
   instruction. Prereg not edited; discrepancy recorded here.
2. **R-1 concrete probe**: frozen text does not specify the probe task or outcome
   encoding. The harness takes observations as input; each battery's manifest
   must define its probe before execution.
3. **Scorecard schema divergence**: `METRICS.md` ("flags as strings", listed keys)
   vs `ARM_INTERFACE.md` (JSON booleans, wider `m2_etc`, extra m3/m5 fields).
   The emitter follows `METRICS.md` exactly per the harness's normative
   declaration; the divergence needs Micah's ruling before batteries score.
4. **m2_etc inner keys**: `{t1_prose,t1_code,t2,t3}` per the METRICS.md column
   spec ("T2/T3 single numbers"); ARM_INTERFACE lists more. Same ruling needed.

## Commits (branch `tnn-native-lab`)

- Corpus hash commitment: `53367a730ef73f1e30ed6b7ea2b43d5f5ebae019`
- Harness implementation + evidence: `337b629bf33f2f10bd830314a25385af9a3757df`

## Files

- Implementation: `docs/lab/units/r0/impl/harness/` (`README.md`, `build.sh`,
  9 `.zag` modules, `m8_gate.sh`, `fetch_corpora.sh`, `R1.md`, `M8.md`)
- Evidence: `docs/lab/units/r0/evidence/` (`corpora.json`, `build.json`,
  `selftest.json`, `r1test.json`, `m8_gates.json`, `scorecard_sample.json`,
  `znc_bugs.md`, this sheet)
- Never committed: binaries, `.zagd`, `.zag-cache/`, corpora, `/tmp` outputs
