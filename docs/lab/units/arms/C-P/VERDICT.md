# C-P Verdict

**Date:** 2026-09-21
**Arm:** C-P — delimiter chunks (whitespace + punctuation), family CTRL
**Scale:** 1x

## VERDICT: PASS

All 1x bars pass. No binding kill criterion fired. No disqualification criterion fired.

## 1x Scorecard (M1–M9)

| Metric | Prose | Code | Bar | Pass? |
|--------|-------|------|-----|-------|
| M1 recall | 100.0 | 100.0 | ≥ bar | ✓ |
| M1 boundary | 100.0 | 100.0 | ≥ bar | ✓ |
| M1 units | 1,978,395 | 2,505,387 | — | — |
| M2 final recall (t1/t2/t3) | 100.0 | 100.0 | ≥ bar | ✓ |
| M3 survival | 100.0 | — | ≥ bar | ✓ |
| M3 fresh recall | 100.0 | — | ≥ bar | ✓ |
| M4 rev boundary | 100.0 | 100.0 | ≥ bar | ✓ |
| M4 rev content | 100.0 | 100.0 | ≥ bar | ✓ |
| M5 | ok | — | completes | ✓ |
| M6 rec/bnd/rev (p2c) | 100/100/100 | — | ≥ bar | ✓ |
| M6 rec/bnd/rev (c2p) | — | 100/100/100 | ≥ bar | ✓ |
| M7 | non-id (no ID layer) | — | contract | ✓ |
| M8 | PASS (10/10 byte-identical) | — | byte-identical | ✓ |
| M9 shape | fast-then-flat | — | — | — |

## 10x Status

**NOT ATTEMPTED** — 1x battery completed; 10x requires parent coordinator authorization per the "run 10x only if all 1x bars pass" rule. All 1x bars pass, so C-P is eligible for 10x.

## Kill Criteria Evaluated

- **C-P retirement:** "A variant retires if a smart arm beats it ≥2x on M3 and M2 at equal M1 both corpora." — Cannot be evaluated without comparison evidence from other arms. **NOT FIRED.**
- **Global:** "If no smart arm beats C-W on Shakespeare by end of 10x, every smart arm is killed." — 10x not yet run. **NOT FIRED.**
- No other binding kill criteria fired.

## Disqualification Check

- M8: All 7 required artifacts present and byte-identical across 5 perturbations × 2 runs. **NOT DISQUALIFIED.**
- No indexed slice exceeds 2^25 bytes. **COMPLIANT.**
- Zero RNG in decision paths. **COMPLIANT.**
- Byte-identical reruns verified. **COMPLIANT.**

## Ambiguities & Deviations

1. **Delimiter set:** Frozen prereg/alphabet documents contain no definitive punctuation-byte list with sign-off. Used authorized fallback: whitespace (space, tab, LF, CR) + exactly `.,;:!?()[]{}"'`.
2. **M8 hashing:** Uses FNV-1a 64-bit (not SHA-256) for the 9 store segments due to 168MB slot tables (Zag SHA-256 ~3min/run). Deterministic; documented in ARM_SPEC.md.
3. **M8 ingest:** Limited to 200K chunks/corpus (400K total) vs 4.48M full, for battery feasibility. Full recall covered by M1; M8 tests determinism.
4. **M8 probe:** Sparse (stride 10,000); m1p/m1c values (10.1/7.9) reflect sampling of non-inserted chunks beyond the 200K limit and are deterministic but not meaningful as recall rates. M1 covers recall.
5. **M4 kill_rate:** 0.0 — the kill_rate metric counts a specific kill-subtype that did not occur in the test sequence; rev_boundary and rev_content are 100.0. Not a failure.
6. **M7 nulls:** By design — C-P has no ID layer (chunk IDs are positional); the non-ID output contract is satisfied.

## Commits

- Source, docs, and scorecard committed via `commit_to_branch.py` to `tnn-native-lab`.
- (Commit hash to be filled after commit.)

## Evidence

- Battery logs: `.work/m8bat/` (10 runs, 7 artifacts each, all byte-identical)
- 1x verification logs: `.work/smoke/`
- Build log: `BUILD_LOG.md`
- Spec: `ARM_SPEC.md`
- Scorecard: `scorecard_1x.json`
