# Cross-reference replication — VERDICT TABLE

**Wave 1 (Tier 1 families) — closed 2026-09-23.** Preregs frozen at
`7b2100d09911c5c10252c5756c7def288e70bd1f` (see `SCOPE.md`, `PREREG_TIER1.md`).
Every crew ran in a clean environment with the pinned toolchain
`znc_linux_x86_64_abed8aa1`, zero RNG, ≥3 byte-identical runs, pure Zag as
verification authority. Crew evidence: `runs/<family>-<crew>/VERDICT.md` +
`RUNLOG.md` under this directory.

## Family verdicts

| Family | Primary | Cross | Family verdict | One-line |
|---|---|---|---|---|
| R1 D-family distillation (Track 5) | REPRODUCED | REPRODUCED | **REPRODUCED** | B 0.9911 > A 0.6552, C 0.9893; end-state digests byte-identical; noise absorbed 10/25/50%; K-T3/K-Q1 fired, K-Q2 never fired. |
| R2 deliberation ceiling | REPRODUCED | REPRODUCED | **REPRODUCED** | Table cell-for-cell (critique 12/94 destructive); contradiction battery baseline 12/156 → 156/156 both mechanisms; conflict-driven at exactly baseline cost 2.000 ops, identical state digest. |
| R3 teacher showdown legs A/B | REPRODUCED | REPRODUCED | **REPRODUCED** | Leg A tie 0/240 × 2; Leg B E_dump 0 vs 7, 12/12 falsehoods faithful; frozen rule → grok-4.7 champion. Both prereg defects audited verdict-neutral. |
| R4 TP1 + SOURCE_AUTHORITY_LICENSE | PARTIAL | PARTIAL | **PARTIAL** | All 2,640 decisions recomputed byte-identical (T1 +78/180, tie guard 100%→0%, T3 880/880 null, r*=0.50); but 9–10 signed license term-groups lack direct measured basis (license's own Annex A.4 marks them derived/provisional/governance). |
| R5 KB4 autopsy | REPRODUCED | NOT REPRODUCED (mechanical) | **PARTIAL** (adjudicated) | All probe data byte-identical both crews; headline attribution (architecture primary, learning secondary) survives. Three narrative sub-claims fail: binding trade 1.36:1/1.77:1 not 1:1; 50 of 184 fixtures not 185; B gate deviates from match-optimality 6×. |

## What does not survive (record corrections required)

1. **R4 — SOURCE_AUTHORITY_LICENSE as signed law overreaches its measured basis.**
   The experimental results (TP1, round-3 sweep) all survive. But these signed
   operative terms have no direct measured basis: k>1 thresholds, the lower-95%-CI
   gate, n≥20, no cross-type transfer, 24-month recency (provisional), the broad
   tie class (only 2v2 measured; the license itself says not deployable until
   adversarial coverage is met), k-table governance, the (ρ,q,δ) frontier, and
   the skepticism/non-factual/untested-shape exclusions. Both crews independently
   converged on this gap.
2. **R5 — three narrative sub-claims are numerically wrong.**
   (a) Variant-specific stimulus binding does not trade errors 1:1: A 60/44 =
   1.36:1, B 55/31 = 1.77:1; total errors grow +16/+24.
   (b) 50 both-fooled-and-agreeing fixtures of **184** common adversarial
   fixtures, not 185 (B alone has 185; A∩B = 184). The 43.5% figure is
   unaffected.
   (c) "The original gate is already Bayes-optimal" holds for A's gate (exact
   match policy, 0/184 deviations) but not as a blanket claim: the implemented B
   gate deviates 6× (108/185 = 58.38% vs the 60.54% ceiling), corrections the
   WHY_REPORT itself documents.
3. **R1 supporting statement — "75/75 determinism" overstates the committed
   record.** Committed evidence holds 63/75 Track 5 run-pairs (12
   `btrap_Y_*.run1.log` absent). Every headline number still re-derives; the
   determinism claim should be restated as 63/75.
4. **R2 record defects (verdict-neutral):** prereg battery table lists kind 5 as
   n=24 (frozen code, VERDICT.md, and KB-M-TEMPORAL all use 12; totals reconcile
   at 264 only with 12); committed prose rounds baseline contested cost
   3.2857→3.286 (log field `3285`, integer truncation).

## Coordination notes

- R2-PRIMARY v1 errored on a runtime restart drain; the replacement v2 was
  interrupted mid-run; v2 (second replacement) discovered v1's session had kept
  running in the same `primary/` directory. v2 independently rebuilt and
  re-verified everything from the frozen pins and endorses v1's VERDICT.md;
  v2's own `rm -f` deleted v1's in-flight binary mid-run, rebuilt identically
  (same 279,931 bytes), no evidence values affected. Two independent
  verifications agree on every bar — family verdict REPRODUCED stands.
- R4-CROSS and R5-CROSS both noted evidence-tree gaps (TP1 run1–run4.log
  absent, attested by SHA256SUMS; R1 12 missing run1 logs) — recorded as
  caveats, not verdict-changers.
- R3 and R5 crews disclosed method deviations (sparse API fetch instead of full
  clone with per-blob SHA verification; one temp file written to /tmp during
  development, deleted) — disclosed in their RUNLOGs, integrity preserved.

## Waves 2–3 (pending)

Tier 2 (~29 families) and Tier 3 (MA1–MA4, clean LH/R34, RC1, wave-5,
felt-V3-retire) preregs are frozen in `PREREG_TIER2.md` / `PREREG_TIER3.md`.
Their verdicts will be appended here as each wave closes.
