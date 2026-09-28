# VERDICT.md — T2-CERT (replacement crew): certifier red-team, 0 flips (Type C)

**Crew:** T2-CERT (REPLACEMENT — predecessor killed mid-run by runtime daemon restart; no inherited state beyond an empty repo dir)
**Date:** 2026-09-22 (PDT)
**Type:** C — committed-evidence re-derivation. No live-web recapture. Pure Zag for verification; zero RNG.

## Frozen pins (recorded before running)

- Frozen prereg: `sylorlabs/TNN` branch `tnn-native-lab`, commit `7b2100d09911c5c10252c5756c7def288e70bd1f`
  — clean clone verified: `git rev-parse HEAD` = `7b2100d09911c5c10252c5756c7def288e70bd1f`, `git fsck` clean, `git status` clean.
- znc: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
  sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
- Evidence pin frozen by this crew (per prereg method "crew freezes the pin"):
  verdict commit `cadacc199684381833dbed4b27bb171b1d6f739f`
  ("certifier-rebuild: rebuilt certifiers + full historical diff + verdict (red-team attack #1)", 2026-09-21 20:39:58 -0700);
  prereg commit `26b86329b53b9aa24589dcf11d5ff09b125c1fe8`.
  Evidence tree: `docs/lab/redteam/certifier-rebuild/` (VERDICT.md, PREREG.md, results.tsv, rerun_all.sh,
  thincert_rb.zag, rngscan_v3_rb.zag, transform.py, tprobe.zag, CAST_AUDIT.md).
- **Pin discrepancy (RESOLVED 2026-09-22 23:31 PDT):** the task brief's "expected pin `e3c2b9cc34e8`"
  was a coordinator-confirmed transcription artifact — GitHub API returns HTTP 422
  "No commit found for SHA: e3c2b9cc34e8" in `sylorlabs/TNN`. Disregarded per coordinator
  instruction; work proceeded on the frozen prereg's authority throughout. The T2-CERT prereg
  section itself names no SHA pins (its method is "crew freezes the pin"); the evidence pins
  below are those named by the committed evidence chain at the frozen commit, all API-verified:
  `7b2100d0…` → 200 OK, `cadacc199684…` → 200 OK, `26b86329…` → 200 OK.

## Authoritative checklist — quoted verbatim from the frozen prereg

Source: `docs/lab/crossref/PREREG_TIER2.md`, lines 125–129, at frozen commit `7b2100d0`
(extracted by this crew from its own clean clone; not taken from any summary):

> ## T2-CERT — certifier red-team: 0 flips (Type C)
>
> **Claims:** 2026-09-22 day verdict: 0 flips — the no-RNG law stands, no historical certification voided. Honest gap: the dirty1_urandom binary is unreproducible.
> **Method:** Type C — re-derive from the committed red-team evidence (crew freezes the pin); verify the 0-flip count and the dirty1_urandom gap as described.
> **Rule:** REPRODUCED if 0 flips re-derives; UNREPLICABLE-AS-IS if the evidence pin can't be located (name it).

## Claim-by-claim results

### Claim 1 — "0 flips — the no-RNG law stands, no historical certification voided"

**Re-derivation:** pure-Zag program `work/flipcount.zag` (zero RNG) parses the committed
`results.tsv` (35 data rows + header) and tallies rows / flips (`stored != new` on scored rows only,
per PREREG KB-FLIP: INCONCLUSIVE = input-missing, never a flip) / CONFIRMED / VOID / ARTIFACT-FAIL /
INCONCLUSIVE / other. Built from source with the pinned znc; no binary copies.

**Measured (3/3 byte-identical runs, sha256 `5ee19c73f6e3ff7297efab70a0fa6e11fbc4577d86415581d478dd6a16db9fc8`):**

| Metric | Committed (VERDICT.md / results.tsv) | Re-derived |
|---|---|---|
| rows | 35 | 35 |
| flips (`stored != new`, scored rows) | 0 | **0** |
| CONFIRMED | 34 | 34 |
| VOID | 0 | **0** |
| ARTIFACT-FAIL | 0 | 0 |
| INCONCLUSIVE | 1 (t1_plant07, no stored attestation) | 1 |
| other | 0 | 0 |

**Verdict on claim 1: REPRODUCED.** Zero flips re-derives exactly; zero voided certifications.
(Note, immaterial to the headline: the source VERDICT.md's KB-FLIP bar line reads "35 CONFIRMED"
but its own table and `results.tsv` sum to 34 CONFIRMED + 1 INCONCLUSIVE = 35 rows; likewise the
"35/35 `old==stored`" baseline is 34/34 on scored rows. The headline "Zero flips. Zero voided
certifications." is exact either way.)

### Claim 2 (honest gap) — "the dirty1_urandom binary is unreproducible"

**Re-derivation:**
- Committed plant sources match the manifest source pins byte-exactly:
  `variation.zag` sha256 `de2b4b6d66cd1071d6703415d70a9ae8d3384e934e9811494ae851eceab1f898` ✓;
  `R33_NATIVE_IO_V1.zag` sha256 `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` ✓.
  Sources are intact; the gap is not source corruption.
- Rebuild of `plant.bin` from those committed sources with the pinned znc **fails**:
  `plant_urandom` (variation.zag lines 102–112) calls `nio_open_readonly` — absent from the
  committed substrate — and the `_zag_rand()` intrinsic — rejected by the pinned znc native
  backend ("call to unknown function"). No binary is producible from committed sources +
  pinned toolchain, so the manifest-pinned BIN hash
  `5f70bf18a086007016e948b04aed3b82103a36bea41755b6cddfaf10ace3c6ef` is unreproducible.
- Controls (same setup, same toolchain): `dirty2_clock`, `dirty3_uninit`, `dirty5_ptrleak`
  all rebuild cleanly; `dirty2_clock`'s rebuilt binary hash **equals its manifest pin
  byte-exactly** (`8396d8bf8ee209595da3be250e5d6e21a964c6f1f9cb271dfb900d658041b694`),
  proving the build setup is faithful and the failure is specific to `dirty1_urandom`.
- Corroboration inside the committed evidence: the historical attestation itself records
  `R7=FAIL` (binary hash mismatch) — the binary already failed to match its manifest pin at
  certification time.

**Verdict on claim 2: VERIFIED AS DESCRIBED** — and the mechanism is now identified: the
committed `dirty1_urandom` plant source references two functions the pinned toolchain does not
provide, so the historical binary cannot be rebuilt from the frozen evidence.

## Final verdict

**REPRODUCED.** Per the frozen decision rule: 0 flips re-derives (pure Zag, 3/3 byte-identical),
and the evidence pin was located and verified (not UNREPLICABLE-AS-IS). The honest
`dirty1_urandom` gap verifies as described, with root cause identified (unbuildable plant source:
`nio_open_readonly` + `_zag_rand` unknown to the pinned toolchain).

## Caveats / follow-ups for the parent

1. The brief's expected pin `e3c2b9cc34e8` was a coordinator-confirmed transcription artifact
   (GitHub API: 422 "No commit found"). Resolved; all prereg pins API-verified (see pins section).
2. Two immaterial arithmetic slips in the source VERDICT.md ("35 CONFIRMED" bar line; "35/35
   old==stored") — the underlying table and `results.tsv` are self-consistent at 34+1; the
   0-flip headline is unaffected.
3. `MASTER_ERROR_LEDGER.md` cites the evidence path as `redteam/...`; the actual committed path
   is `docs/lab/redteam/...`.
4. No live-web recapture was performed (Type C). No commits were made; no binaries or `.zagd`
   files were produced or retained (build outputs deleted after hashing). Scratch only; nothing
   written outside `~/workspace/scratch-crossref/T2/CERT/` and `~/workspace/tmp_commit`.

## Files

- `~/workspace/scratch-crossref/T2/CERT/crew/VERDICT.md` (this file)
- `~/workspace/scratch-crossref/T2/CERT/crew/RUNLOG.md`
- `~/workspace/scratch-crossref/T2/CERT/crew/work/flipcount.zag` — pure-Zag re-derivation source
- `~/workspace/scratch-crossref/T2/CERT/crew/work/run1.out`, `run2.out`, `run3.out` — 3 byte-identical runs
- `~/workspace/scratch-crossref/T2/CERT/crew/results_source.tsv`, `VERDICT_source.md`, `PREREG_source.md`,
  `rerun_all_source.sh`, `dirty1_variation.zag` — evidence extracts from pin `cadacc199684`
