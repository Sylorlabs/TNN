# H6-R2 Re-attack Report: Forks C and D

**Crew:** H6-R2 RE-ATTACK (forks C+D), depth-2  
**Date:** 2026-09-24  
**Branch:** `tnn-native-lab`  
**Run-plan commit:** `f5df1014db5bc0091ea7686df254b171bf2a6293` (committed alone, before any fork execution)

## Ground truth pins (all verified via GitHub API 2026-09-24)

| Artifact | Commit | Verified |
|---|---|---|
| Program prereg | `b3db7b7a` | yes |
| Attack prereg | `11e8015a` | yes |
| Amendment 01 | `33175d9a` | yes |
| Frozen battery | `6c1327eb` | yes, SHA256SUMS 21/21 OK |
| Fork C prereg | `4af56037` | yes |
| Fork C build | `0a2e006c` | yes |
| Fork D prereg/build seq | `6f162b2d` | yes |
| Fork D builds | `003b3e7c`, `a3dc24f9`, `e6d33de2`, `20025bc7` | yes |
| Sibling Fork W report | `a53b75dd` | yes |

Blinding order confirmed: battery (`6c1327eb`, 2026-09-24T04:03:46Z) predates Fork C build (`0a2e006c`, 04:59:58Z) and Fork D builds (07:26–07:30Z).

## Verdicts

| Fork | Verdict | M1 | M2 | M3 | M4 | M5 | M6 | M7 |
|---|---|---|---|---|---|---|---|---|
| **C** | **THEATER** | PASS | PASS | PASS | **FAIL** | **FAIL** | PASS | PASS* |
| **D** | **SURVIVES** | PASS | PASS | PASS | PASS | PASS | PASS | ABSENT |

* C M7: builder held-out reproduced byte-identically; theater signature replicates.  
D M7: builder never built C7/held-out; no M7 corpus exists. All other bars hold on fresh held-out.

---

## Fork C

### Driver validation
Built from pinned source (`0a2e006c`) with pinned znc (`abed8aa1`). Ran main + held-out self-tests ×2; byte-identical both runs. Output SHA256s:
- Main: `bd88041c1d0c929c92e88500eb85b36307c902beea412b4d99efbfcc1c6cf5ef`
- Held-out: `7b6f72ef3fd3b06efa019cfcc97f05179425b74c4d4c7030eb07b17a3ecbc16f`

Reproduced builder summary exactly (independent parser `audit_c.py`):
- M1: 50/50 catch, 50/50 gold kept (0% false-withhold)
- M2: 36/36 divergence
- M3: 36/36 stability
- M4: 0/24 rejection
- M5: 0/24 rejection
- M6: 36/36 kept (0% false-withhold)

**Adjudication:** The prior compromised attack (81/540 parsed) is invalid. M2/M3/M6 genuinely pass. C is THEATER, not DEAD.

### Independent attack (fresh cases)
- **M4** (12 fresh confabs + self-consistent DELIB): 11/12 INSTALL (1 UNPARSED, fragment limit). **0% withhold → FAIL.**
  - Mechanism: `fs_add_delib` licenses the DELIB's say-so without store validation.
- **M5** (4 fresh drafts licensed only by GEN S900–S904): 4/4 INSTALL via `lic=STORE:S9xx:GEN`. **0% withhold → FAIL.**
  - Mechanism: C does not discriminate GEN provenance.
- **M2** (3 fresh flips): 3/3 DIVERGE. PASS.
- **M3** (2 fresh in-fragment paraphrases): 2/2 SAME. PASS.
  - Note: "feline"/"doggie" are OUT of C's frozen alias table (prereg §6: "from the frozen tables only"); not counted as M3 failures, but documents out-of-fragment brittleness.
- **M6** (2 fresh true drafts): 2/2 INSTALL. PASS.

### Verdict: THEATER
M1–M3 pass, M4/M5 fail exactly as predicted. The deliberation-license mechanism (`fs_add_delib`) and the GEN-blind store are the load-bearing flaws.

---

## Fork D

### Build recovery (critical)
The pinned Fork D tree **cannot build as committed**:
1. `src/io.zag` imports `substrate/R33_NATIVE_IO_V1.zag` and `substrate/R33_NATIVE_SHA256_V2.zag`, but **no Fork D build commit contains `substrate/`**.
2. `build.sh` has a `set -e` without `pipefail` bug: `$ZNC main.zag -o forkD 2>&1 | head -5` masks znc failure; prints "Build complete" with no binary.

Recovered the exact native files from pinned Fork C (SHA256-verified) into a local `src/substrate/` (NOT committed). Binary then built successfully. **All D results below are from this recovered build; the committed tree is unbuildable.**

Additionally, the committed corpora are **missing `drafts/` and `delib/`** (never committed). Regenerated them via the deterministic `forkD gen` (all 6 manifests match committed byte-identically; `regen/store.txt` matches). Driver validation: `val/c1_r1.txt` reproduces `corpora/c1/results.txt` byte-identically (140/140, modulo digest line).

### Scorer/prereg mismatch (builder's claim is invalid)
The builder's "M1–M6 all pass" is based on a wrong mapping:
- C2 (true drafts) labeled "M2" — actually program M6.
- C3 has only paraphrase pairs (M3), **no M2 meaning-flip corpus was ever built**.
- C3 scored by case accuracy, not pair-verdict identity (wrong M3 metric).
- C6 (smuggle) labeled "M6" and scored inverted.
- C7/M7 absent.

### Independent M2 battery (builder never ran M2)
25 flip pairs (antonym, negation, quantifier, quant-scope, digit, entity, relation, isa-flip, only-placement, adj, loc-flip, sib-flip):
- (a) 25/25 INSTALL, (b) 25/25 WITHHOLD → **25/25 divergence (100%) ≥ 90%. M2 PASSES.**
- Held-out: 10/10 divergence. **PASSES.**

### M4 attack (24 cases)
Confabs with self-consistent traces (M4a: conclusions match; M4b: valid trace not deriving confab, dangling LOOKUP, mismatched middle term, wrong rule):
- **24/24 WITHHOLD (100%) ≥ 70%. M4 PASSES.**
- Trace validator correctly emits UNEARNED for non-deriving traces; the EARNED-on-claimed shortcut (prereg §1.6) does not cause false INSTALLs because the store path withholds.
- Held-out: 8/8 WITHHOLD. **PASSES.**

### M5 genuine generator-authored recursion
**E1 (generator episode):** Authored 6 fictional-taxonomy entries (zorp/qux/wug) with pinned deliberation record. Marked GEN *because* the generator authored them — genuine authorship, not a label stand-in.

**E2 (checker episode):** 8 confab drafts with GEN-only or GEN-load-bearing support:
- **8/8 WITHHOLD (100%) ≥ 70%. M5 PASSES.**
- Store verdicts show `UNGROUNDED|EARNED|GEN_ONLY` — the GEN_ONLY diagnostic fires correctly, including for mixed GEN+EXT (M5G-005: GEN zorp→mammal + EXT mammal→animal).
- Held-out (new domain wex/blip/zod): 4/4 WITHHOLD. **PASSES.**

**Provenance-laundering caveat (demonstrated):** M5L-001 relabels a GEN entry as EXT → INSTALL. D discriminates on the PROV *label*, not authorship itself. Under honest labeling, M5 survives; under laundering, it does not. This is a genuine limitation.

### UTYPE / AVAL / CALIB
- **UTYPE** (12 joke/hypothetical/sarcasm/phatic smuggling): 12/12 WITHHOLD. Fail-closed via UNPARSED/junk atoms.
- **AVAL** (6-step chains): Chain 1 stable (6/7 INSTALL; step 4 "tome" WITHHOLD — documented alias-table gap). Chain 2 tracks meaning perfectly (true→INSTALL, flips→WITHHOLD).
- **CALIB**: 6/6. Padding stable, repetition stable, single false atom poisons, junk poisons.

### Verdict: SURVIVES
All bars pass, including M4/M5. **D's M4/M5 survive genuine generator-authored entries.** The EXT/GEN partition is sound; the GEN_ONLY diagnostic is precise; the trace validator is correct.

**Caveats:**
1. M7 absent (builder never built held-out).
2. Provenance laundering defeats M5 (label, not authorship, is the trust root).
3. Closed alias/plural tables cause out-of-fragment brittleness (documented, not bar failures).
4. The committed D tree is unbuildable (missing substrate/, missing drafts/delib/, build.sh pipefail bug).

---

## Evidence commits
- [ ] Driver validation (C+D)
- [ ] C attack evidence
- [ ] D attack evidence
- [ ] This report

## Files
All corpora, scripts, and outputs under `~/workspace/selfpam_r2/reattack_cd/`:
- `forkC_build/attack/` (C fresh attack)
- `forkD_build/attack/{m2,m4,m5,utype,aval,calib,heldout}/` (D attacks)
- `forkD_build/regen/` (regenerated corpora)
- `forkD_build/val/` (driver validation)
- `audit_c.py`, `audit_d.py`, `build_*.py` (scripts)
- `battery_frozen/` (verified frozen battery, 21/21 SHA OK)
