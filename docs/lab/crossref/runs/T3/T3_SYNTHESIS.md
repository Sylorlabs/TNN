# Wave-2 Tier-3 Cross-Reference: SYNTHESIS

**Date:** 2026-09-23  
**Coordinator:** Tier-3 coordinator (direct execution, depth 2/2 — no subcrews)  
**Frozen prereg:** `docs/lab/crossref/PREREG_TIER3_WAVE2.md` @  
`ac4a96c0b1f149d2f7338888de52b0607c4e7bbf` (blob `c391bbbf2818a9f74e8dd726cec1601bb3c338f8`)

**Filename deviation (justified):** The prereg specified `PREREG_TIER3.md`;
the Wave-2 Tier-3 prereg was frozen as `PREREG_TIER3_WAVE2.md` to avoid
confusion with the older (different) `PREREG_TIER3.md`. The synthesis
discloses this per the task requirement.

## Tier-2 closeout verified

- Closeout: `docs/lab/crossref/runs/T2/_closeout/CLOSEOUT_WAVE2.md`
  (blob `d4ab79881f8f741533558046a4bf5142703b80b8`)
- **28/28 resolved: 26 REPRODUCED, 2 PARTIAL**
- Tally blob: `f10ff197f36a1525c9b7858f09f96303b9e4b484`
- Tier-2 prereg: commit `7b2100d09911c5c10252c5756c7def288e70bd1f`,
  blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`

## Track verdicts

### T3-CONSIST — CONSISTENT (commit `6037f74d`)

4 CONSISTENT (R2, R5, R6, R8), 4 DISTINGUISHED (R1, R3, R4, R7),
0 INCONSISTENT. No Tier-2 claim broke.

**Key finding:** SENSESINT's `VERDICT_SHEET.md` notes INFORICH's R0→R2
causal framing confounds information access with policy changes; proposes
unbuilt control IS-R3. Zero GitHub hits for IS-R3 (2026-09-23). The claim
that "information richness caused truth discrimination" remains bounded.

### T3-ANOMALY — MECHANISM-REPRODUCED (commits `6037f74d`, `483ec095`)

**Correction applied 2026-09-23:** Original verdict HYPOTHESIS-CONFIRMED
overstated confidence. Revised to **mechanism reproduced; historical root
cause unresolved/best-supported**.

- 151 MB fixture recreated deterministically (SHA-256 counter mode, zero
  RNG — original used `os.urandom` despite "zero RNG" docs).
- Test 2 (late `rm -rf`) rerun 3/3: all WIPED. HTTP server stopped.
- The 3/3 control proves the mechanism *can* wipe a repopulated tree, not
  that it *did* in every historical incident. No per-incident evidence found.
- Retains direct exclusion of orphan `git-remote-http` writes and reboot wipes.

### T3-HARDEN

#### H1 — ARTIFACT-BOUND (commit `de09f984`)

- `nio_open_readonly` + `_zag_rand` unknown to pinned znc; boundary documented.
- 0-flip verdict independent: 35→33 rows, 0 flips both ways (pure-Zag).
- Clean-room plant with known syscalls builds and is caught (hits=11, FAIL).
- No Tier-2 claim breaks.

#### H2 — PARTIAL (commits `c9863daa`, `e3413ed8`)

- Full 1.4 GB battery recovered; sources committed (248K, no WAVs/binaries).
- All 4 analyses 3× byte-identical.
- **Sol-H1/H2/H3: GAP-CLOSED** (all dispositions match T2 exactly).
- **Grok-G1/G3: NOT reproduced** from recovered `analyze_gx.py` (different
  test/numbers; T2's came from crew re-derivation).
- **Grok-G2: PARTIAL** (ratios match exactly; mechanism-contradiction was
  T2's analysis).
- Tier-2 bound stands for Grok hypotheses.

#### H3 — BOUNDARY-MAPPED (commit `f988e4da`)

- Real WITHHOLD-before-corroboration gate in `ws2_sense.zag` copy.
- Ungated baseline: 38/38 match to committed trial (faithful harness).
- Gated 3× byte-identical: helper FULL PASS (K1 1/9, M1 8/9, K2 0/3);
  solo K1 trips on C15/C16 spam pair (2/9); K2 clear both arms.
- Fresh 12: 8/12 withheld; 4/4 spam-class install (boundary).
- **Exactly** the Tier-2 counterfactual, confirmed with real mechanism.

#### H4 — NOT EXECUTED

Code analysis only. The gate requires ≥2 domains with byte-identical
answers; N=2,3,4 colluding domains all install (T2 confirmed 2/2).
Distinct surface forms evade (exact match required). No distinct-origin
defense implemented. Full probe not built.

#### H5 — LIMITATION-LOAD-BEARING (commit `c8d13c47`)

- 12 fresh items, solo+helper 3× byte-identical.
- Deadpan falsehoods 4/4 withheld; hoax/satire pairs 4/4 withheld.
- **2/4 satire-without-URL INSTALL as SINCERE** (F6, F8, both arms).
- The T2 honest limitation (satire via URL, not prose) is a mechanism gap.

#### H6 — GUARDED (commit `584a0b78`)

- SHA-256 pre-run gate + readonly mode in scorer.
- 3× runs: gate PASS, outputs byte-identical, 8/8 blobs unchanged.
- B5: 3× story reruns byte-identical (matches T2 `9dd1c20c…`).
- B1/B3/B4 via T2 verification (guard is scorer-only).

### T3-REMATCH — PENDING (T4 running)

- T1 (740), T2 (7,400) caches byte-identical.
- T3 (37,000) complete 2026-09-23 19:40 UTC, all chunks byte-identical.
- T4 (74,000) in progress (6.6 MB so far).
- VERDICT.md has `[TO BE FILLED]`; crew RUNLOG documents progress.
- **Do not interrupt.** Integration pending T4 completion.

### T3-PARTIALS — PARTIAL (commit `09589542`)

- **TRACKB:** varA/varB/varC all PASS; arm-3 choice is governance call #1
  for Micah (parked in closeout `47c48d3e7cf9f`). No selection made.
- **SENSESINT:** 140/140 verified; commit `79fb9a7b` amends 3rd stale
  manifest size. IS-R3 proposal remains open.
- Integrated by reference; no adjudication.

## Claims hardened

1. **HELLHOLE K2 (contradiction):** RESCUED in both arms via real gate.
2. **HELLHOLE K1 (helper):** RESCUED (2/9 → 1/9).
3. **CERT 0-flip:** Hardened via independence proof + clean-room plant.
4. **GOALB scorer:** GUARDED (destructive write eliminated).
5. **AUDIOCONT Sol battery:** GAP-CLOSED (3× byte-identical re-execution).

## Claims broken / bounded

1. **HELLHOLE K1 (solo):** FAIL STANDS on spam pair (2/9). Boundary mapped.
2. **JOKE satire:** LIMITATION-LOAD-BEARING — 2/4 satire-without-URL install
   as sincere. The URL-provenance limitation is a mechanism gap.
3. **INFORICH collusion:** Boundary confirmed (N≥2 installs); H4 probe not
   executed.
4. **ANOMALY historical root cause:** Revised from CONFIRMED to
   best-supported/unresolved. Mechanism reproduced, not historically proven.
5. **AUDIOCONT Grok battery:** Not reproduced from recovered sources;
   Tier-2 bound stands.

## Consistency

T3-CONSIST: 4 CONSISTENT, 4 DISTINGUISHED, 0 INCONSISTENT. The
distinguished results (R1, R3, R4, R7) differ in scope/method, not in
contradiction. The IS-R3 unbuilt control bounds INFORICH's causal claim.

## Anomalies resolved

- **Vanishing trees:** Mechanism (late `rm -rf`) reproduced 3/3 with
  deterministic fixture. Historical attribution revised to best-supported.
  Orphan writes and reboot wipes directly excluded.
- **H2 Grok mismatch:** Resolved as version difference — recovered
  `analyze_gx.py` is not the analysis that produced T2's Grok numbers.

## Heavy/partial integration

- **T3-REMATCH:** T1/T2/T3 byte-identical; T4 running. Pending completion.
- **T3-PARTIALS:** TRACKB (governance) and SENSESINT (140/140) integrated
  by reference.

## Limitations (honest)

1. **Direct execution, no subcrews:** Depth 2/2; all work done directly,
   no parallel crews. This limits throughput but ensures fidelity.
2. **H4 not executed:** INFORICH collusion probe requires a harness not built.
   Code analysis only.
3. **T3-REMATCH incomplete:** T4 still running; verdict pending.
4. **H2 Grok:** Recovered battery does not reproduce T2's Grok dispositions.
5. **T3-ANOMALY:** Historical root cause not proven, only best-supported.
6. **No independent numeric Zag verifier** for CONSIST (Type-C manual arithmetic).

## Commits

| track | commit | verdict |
|---|---|---|
| T3-CONSIST | `6037f74d` | CONSISTENT |
| T3-ANOMALY | `6037f74d` + `483ec095` | MECHANISM-REPRODUCED |
| H1 | `de09f984` | ARTIFACT-BOUND |
| H2 | `c9863daa` + `e3413ed8` | PARTIAL |
| H3 | `f988e4da` | BOUNDARY-MAPPED |
| H5 | `c8d13c47` | LIMITATION-LOAD-BEARING |
| H6 | `584a0b78` | GUARDED |
| T3-PARTIALS | `09589542` | PARTIAL |

All on branch `tnn-native-lab`. No binaries, `.zag-cache`, `.zagd`, or
`__pycache__` committed. All reruns byte-identical (3×). Zero RNG in all
Tier-3 mechanisms.
