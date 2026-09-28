# CERT RE-DERIVATION — arena certifier vs the 2026-09-20 gate evidence

**Track:** WI-3 (Arm C gate-expansion), PREREG_GATE_EXPANSION.md — frozen spec
`CERT_REDERIVATION.md` (committed `293f0cb4`). **Date:** 2026-09-25 (PDT).
**Independent check** of the CERT crew's 35/35 CONFIRMED result
(`redteam/certifier-rebuild/VERDICT.md`), thincert track only.
NOTHING HERE ADOPTS ANYTHING — adoption needs Micah's dated signature.

## 1. Independent arena build (K-BUILD)

| Item | Value |
|---|---|
| Source | `redteam/certifier-rebuild/thincert_rb.zag`, sha256 `d1c50c1b3b14a84473c270b72fa1a5c80a1d9cf3d6753d8b919839df75d03371` (byte-identical to the CERT crew's build source in `~/workspace/certrebuild/work/thincert/thincert_rb.zag`) |
| Substrate inputs | `R33_NATIVE_IO_V1.zag` `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` · `R33_NATIVE_SHA256_V2.zag` `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` (copied from `wave12/step1a-v2/thin-certifier/certifier/substrate/`, placed next to the source per the CERT crew's layout; imports resolve relative to build cwd) |
| Toolchain (pinned) | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` |
| Build command | `cd <builddir> && znc build thincert_rb.zag -o thincert_arena` (fresh dirs `work/build1`, `work/build2`; no shared `.zag-cache`) |
| Build 1 sha256 | `362089d5a4405b69fe072e1aa8e91481b1237a1852bac9a29d65335c125ebe37` |
| Build 2 sha256 | `362089d5a4405b69fe072e1aa8e91481b1237a1852bac9a29d65335c125ebe37` |
| K-BUILD | **PASS** — 2/2 byte-identical |
| CERT crew cross-check | `~/workspace/certrebuild/work/thincert/thincert_new` sha256 `362089d5a4405b69fe072e1aa8e91481b1237a1852bac9a29d65335c125ebe37` — **identical to the fresh builds** (same source + same toolchain, deterministic). The CERT crew's arena binary is independently reproduced, not taken on faith. |

## 2. Re-run of the 2026-09-20 thin-certifier gate evidence

Harness `work/rederive_tc.sh` (modeled on the CERT crew's `rerun_all.sh` `run_tc`, thincert cases only; no rngscan — out of scope per spec §4).
Each case: run fresh arena binary as
`thincert <manifest> <builddir> <binary> <replay-evidence> <attestation-out>`,
extract `verdict=`, compare vs stored verdict, and byte-compare the full
attestation vs the stored record. Inputs reconstructed exactly per
`rerun_all.sh` (T1: k2prime plant source rebuilt with pinned toolchain;
T2: armc plant source rebuilt; T3: repbuild_run source rebuilt).

Columns: `stored` (2026-09-20 committed attestation verdict) · `old`
(CERT crew's old-binary verdict from `results.tsv`) · `new` (fresh arena
verdict, this run) · `new==stored` · `full_bytes` (fresh attestation vs
stored attestation) · class.

| case | stored | old | new | new==stored | full_bytes | class |
|---|---|---|---|---|---|---|
| t1_plant01 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant02 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant03 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant04 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant05 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant06 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant08 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant09 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant10 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant11 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant12 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant13 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant14 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant15 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant16 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant17 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant18 | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t1_plant19 | **PASS** | PASS | PASS | YES | IDENTICAL | CONFIRMED |
| t1_plant20 | **PASS** | PASS | PASS | YES | IDENTICAL | CONFIRMED |
| t2_dirty1_urandom | FAIL | FAIL | FAIL | YES | DIFF (R7 reason only, §3) | CONFIRMED |
| t2_dirty2_clock | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t2_dirty3_uninit | **PASS** | PASS | PASS | YES | IDENTICAL | CONFIRMED |
| t2_dirty5_ptrleak | FAIL | FAIL | FAIL | YES | IDENTICAL | CONFIRMED |
| t3_rerun | **PASS** | PASS | PASS | YES | IDENTICAL | CONFIRMED |
| t3_k3 | **PASS** | PASS | PASS | YES | IDENTICAL | CONFIRMED |
| t1_plant07 | MISSING | — | — | — | — | **INCONCLUSIVE** (§4) |

**25/25 scored cases CONFIRMED; 0 flips; 0 voided certifications.**
K-FLIP not triggered (no new ≠ stored verdict anywhere). All six
load-bearing PASS certifications (t1_plant19/20, t2_dirty3_uninit,
t3_rerun, t3_k3) re-verify PASS under the fresh arena binary,
byte-for-byte including rule hits, offsets, counts, and hashes.

## 3. The one full-text DIFF: t2_dirty1_urandom

Stored line 12: `R7=FAIL:R7:binary hash mismatch`.
Fresh (and CERT crew's) rerun line 12: `R7=FAIL:R7:binary unreadable`.
Verdict identical (FAIL). This is NOT a flip: the dirty1 plant's
`variation.zag` **cannot be built with the pinned toolchain**
(`nio_open_readonly` / `_zag_rand` are unknown functions — build aborts),
a documented property of the evidence
(`armc-rerun-2026-09-21/thincert/builds/HASHES.md`: "NOT BUILDABLE with
pinned toolchain — recorded BIN 5f70bf18… is not reproducible from frozen
sources"). The historical certification ran against a binary that is not
reproducible; the CERT crew's own rerun artifacts hit the identical
`binary unreadable` line (their `old.txt` and `new.txt` are byte-identical
to each other), and my fresh attestation is **byte-identical to the CERT
crew's rerun `new.txt`** — not just verdict-equal. So the R7 line is
explained by a pre-existing evidence property, not by the arena rebuild,
and the certifier's decision (FAIL) is unchanged.

## 4. plant07 disposition: INCONCLUSIVE (recorded with reason)

plant07's source (`k2prime-redteam/plants/plant07/`) is intact, but the
K2′ scorer recorded BUILDFAIL on 2026-09-20: `variation.zag` fails with
the pinned toolchain (`x86 cpuid expects leaf and subleaf` — build
aborted). Re-running the exact plant build with the pinned toolchain in
this track reproduced the failure (rc=1, same error class). With no
binary there is no replay evidence and no attestation to certify — the
certifier has no valid inputs, so plant07 cannot be scored. Disposition:
**INCONCLUSIVE — missing input (unbuildable plant), not a pass**, matching
the CERT crew. No verdict is asserted for plant07.

## 5. K-bar events

- **K-BUILD:** PASS — 2/2 independent arena builds byte-identical; CERT
  crew's arena binary SHA-matches both.
- **K-FLIP:** not triggered — zero cases where new ≠ stored verdict.
- **K-HONEST (what was and was not re-run):**
  - Re-run: all 25 thincert cases in the CERT crew's corpus (19 k2prime
    plants, 4 armc plants, t3_rerun, t3_k3), through the fresh arena
    binary built above; per-case attestations preserved in
    `work/reruns/<case>/new.txt`; full run log in `work/rederive_run.log`
    and `work/reruns/results.tsv`.
  - NOT re-run: the r1_* rngscan_v3 cases (out of scope per frozen spec
    §4 — rngscan_v2/v3 are not the thincert gate; no claim is made about
    them in this track), and plant07 (INCONCLUSIVE, §4).
  - The "old" column is the CERT crew's recorded old-binary verdict from
    their frozen `results.tsv` (not an independent old-binary re-run by
    this track); this track's independent contribution is the fresh
    arena build + new-vs-stored comparison.
  - No extrapolation beyond the evidence set: this re-derivation covers
    only the historical certifications listed above; zero flips on the
    historical corpus does not prove the old binaries never misread a
    table on other inputs.

## 6. Citable re-derivation statement

**The 2026-09-20 thin-certifier gate evidence re-derives cleanly under
the arena-rebuilt certifier (zero verdict flips, zero voided
certifications).** The arena binary was independently rebuilt twice with
the pinned toolchain (2/2 byte-identical, SHA-matching the CERT crew's
build); 25/25 rerunnable thincert certifications CONFIRM (old == stored ==
new verdicts); 24/25 attestations are byte-identical to the stored
records, with the single difference (t2_dirty1_urandom's R7 reason string)
explained by the documented non-reproducibility of that plant's binary and
verdict-unchanged; t1_plant07 remains INCONCLUSIVE (unbuildable plant,
no stored attestation).
