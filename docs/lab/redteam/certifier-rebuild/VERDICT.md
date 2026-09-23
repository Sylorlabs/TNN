# VERDICT — Certifier rebuild vs every historical certification (red-team attack #1)

**Date:** 2026-09-21 (PDT) · **Crew:** CERTIFIER-REBUILD · **Prereg:** `PREREG.md` (committed `26b86329`, frozen before code)
**Question:** did the proven ZNC-2026-09-21-007 miscompile (consecutive same-size `as []i32` casts cross-reading slots 9–11 into indices 0–2) flip any historical no-RNG certification?

## Method

1. Rebuilt `thincert.zag` (9 casts) and `rngscan_v3.zag` (30 casts) with the **only** permitted change: every indexed `[]i32` table → `[]u8` arena + little-endian `t_put32`/`t_get32` (sign-correct through `i64`; verified by diff review + fidelity scan: zero remaining trigger casts, zero leftover indexed table uses, no `.len` reliance on table views).
2. Rebuilt all four binaries with the pinned toolchain (`znc_linux_x86_64_abed8aa1`).
3. **Baseline:** the OLD binaries reproduce every stored historical attestation (35/35 `old==stored`), proving the re-run harness is faithful to history.
4. Ran OLD and NEW certifiers over identical reconstructed inputs for every historical certification; diffed verdicts AND full attestation bytes.

## Kill-bar outcomes

| Bar | Result |
|---|---|
| KB-DET (5/5 byte-identical reruns, new binaries) | **PASS** — 1 unique hash across 5 runs for each binary |
| KB-FIDELITY (mechanical-only diff + accessor unit test) | **PASS** — `t_put32`/`t_get32` round-trip `0, 1, -1, INT_MIN, INT_MAX, ±123456789`, boundary slots, and 3 adjacent equal-sized arenas with zero cross-contamination (probe exit 0). One fidelity escape was caught by the diff itself (see §3) and fixed before scoring. |
| KB-FLIP (every historical artifact classified) | **35 CONFIRMED, 0 VOID, 0 ARTIFACT-FAIL, 1 INCONCLUSIVE** (table below) |
| KB-AUDIT (lab-wide cast grep) | **PASS** — see `CAST_AUDIT.md`; every live trigger-pattern instance assessed |

## Results — all 35 rerunnable historical certifications

| Case | Historical artifact | stored | old | new | Full-text diff | Class |
|---|---|---|---|---|---|---|
| t1_plant01–06, 08–20 | k2prime red-team scoring attestations (18) | FAIL | FAIL | FAIL | byte-identical | CONFIRMED |
| t1_plant19, t1_plant20 | k2prime clean plants | **PASS** | PASS | PASS | byte-identical | CONFIRMED |
| t1_plant07 | k2prime plant07 | MISSING | — | — | — | **INCONCLUSIVE** (no stored attestation; not scored) |
| t2_dirty1_urandom | armc plant (urandom) | FAIL | FAIL | FAIL | byte-identical | CONFIRMED |
| t2_dirty2_clock | armc plant (clock) | FAIL | FAIL | FAIL | byte-identical | CONFIRMED |
| t2_dirty3_uninit | armc plant (uninit) | **PASS** | PASS | PASS | byte-identical | CONFIRMED |
| t2_dirty5_ptrleak | armc plant (ptrleak) | FAIL | FAIL | FAIL | byte-identical | CONFIRMED |
| t3_rerun | armc clean representative | **PASS** | PASS | PASS | byte-identical | CONFIRMED |
| t3_k3 | armc K3′ bridge | **PASS** | PASS | PASS | byte-identical | CONFIRMED |
| r1_clean2 | rngscan v3 clean module | **PASS** | PASS | PASS | byte-identical | CONFIRMED |
| r1_dirty1–4, 6, 7, 8 | rngscan v3 dirty modules (7) | FAIL | FAIL | FAIL | byte-identical | CONFIRMED |
| r1_dirty5_entryset | rngscan v3 entryset module | FAIL | FAIL | FAIL | byte-identical | CONFIRMED |

**Zero flips. Zero voided certifications.** Every load-bearing PASS (plant19/20, dirty3_uninit, rerun, k3, clean2) re-verifies PASS under the rebuilt certifier, byte-for-byte including rule hits, offsets, counts, and hashes.

## §3 — The dirty5 incident (methodology validation)

Mid-run, the first (buggy) rebuild showed `r1_dirty5_entryset: FAIL → PASS` (ARTIFACT-FAIL). Root cause was **my transformation's miss, not the miscompile**: three indexed uses on `[]i32`-typed *function parameters* (`fnoff`/`fnlen` in `check_44_structural`, `mcount` in `parse_manifest`) were not converted — they silently became single-byte `[]u8` accesses and blinded rule 4.4. The diff methodology caught it immediately (a verdict moved), the script was fixed to cover all `[]i32`-typed names, and the re-run shows byte-identity everywhere. This incident is evidence the diff is **sensitive** to table-access corruption: had the miscompile flipped any historical verdict, this pipeline would have caught it.

## Verdict

**The no-RNG law still stands on clean evidence.** The proven miscompile was present as a source pattern in both certifiers, but across the entire historical certification corpus (35/35 rerunnable artifacts, including all 6 load-bearing PASS certifications) the rebuilt certifiers agree with the old ones **byte-for-byte**. The miscompile was therefore *latent in verdict outcomes* on the historical corpus — it changed nothing that was ever certified. No historical certification is voided by red-team attack #1.

### Qualifiers (stated plainly)

1. **The rebuilt certifiers are measurement instruments, not the adopted gate.** Per the standing rule, adopting them as the pinned per-build certifier requires Micah's dated amendment signature. Until then the pinned binaries remain the historical (pattern-carrying) builds.
2. **plant07** has no stored attestation and could not be scored (INCONCLUSIVE — missing input, not a pass).
3. **The v2 tripwire is still pattern-carrying** (`rngscan_v2.zag`, 23 casts, full trigger shape). It is informational only, not a gate; its `tripwire_v2` readings in the attestations above are untrusted until it is rebuilt or retired (see `CAST_AUDIT.md`).
4. Zero flips on the historical corpus does **not** prove the old binaries never misread a table — only that no certified verdict depended on it. Future certifications should run on the rebuilt binaries once adopted.

## Artifacts committed under `docs/lab/redteam/certifier-rebuild/`

`PREREG.md` · `thincert_rb.zag` · `rngscan_v3_rb.zag` · `transform.py` (mechanical transformer + fidelity scan) · `tprobe.zag` + result (accessor unit test) · `results.tsv` (35-case old/new/stored table) · `rerun_all.sh` · `CAST_AUDIT.md` · `VERDICT.md`
