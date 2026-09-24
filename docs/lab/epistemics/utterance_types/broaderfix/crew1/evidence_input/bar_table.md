# Evidence: complete H7_CHECK tables (baseline vs candidates)

Mode 0 = baseline (`predict`: any live marker → WITHHOLD). Byte-identical to
committed primary (SHA256 `71731400c1758f883c8057ad3dca044f34491c9a7861e6f53c1c5815b8f75407`).
Mode 1 = frame-gate (WITHHOLD requires ≥1 non-content-field firing marker).
Mode 2 = WITHHOLD requires ≥2 firing markers for the winning concept.
Mode 3 = lone content-only single-marker fire is insufficient for WITHHOLD.

All modes: pure Zag, zero RNG, deterministic; each run against the full frozen
curriculum (Phase 1 → Phase 2a → 5×Phase 2b → Phase 3 → Phase 4 → redteam).

## Failing checks only (all other of the 45 checks pass in every mode)

| Check | Mode 0 (baseline) | Mode 1 | Mode 2 | Mode 3 |
|-------|-------------------|--------|--------|--------|
| sinc_lk_3 | 0/1 (LK 3/10) | 1/1 (LK 10/10) | 1/1 (LK 10/10) | 1/1 (LK 10/10) |
| learn_bar_2 | 1/1 (NO 16/20) | 0/1 (NO 5/20) | 0/1 (NO 15/20) | 0/1 (NO 15/20) |
| learn_nomem_2 | 1/1 | 0/1 | 1/1 | 1/1 |
| xinterf_no_2 | 1/1 | 0/1 | 0/1 | 0/1 |
| **H7_FAILURES** | **1** | **3** | **2** | **2** |

## Step-32 curves, types 2 (joke) and 3 (hypothetical)

| Mode | joke TR | joke PA | joke NO | joke SINC-DP | joke SINC-LK | hyp TR | hyp PA | hyp NO | hyp SINC-DP | hyp SINC-LK |
|------|---------|---------|---------|--------------|--------------|--------|--------|--------|-------------|-------------|
| 0 | 20/20 | 20/20 | 16/20 | 10/10 | 10/10 | 20/20 | 20/20 | 20/20 | 9/10 | **3/10** |
| 1 | 20/20 | 20/20 | 5/20 | 10/10 | 10/10 | 20/20 | 20/20 | 20/20 | 10/10 | 10/10 |
| 2 | 20/20 | 20/20 | 15/20 | 10/10 | 10/10 | 20/20 | 20/20 | 20/20 | 10/10 | 10/10 |
| 3 | 20/20 | 20/20 | 15/20 | 10/10 | 10/10 | 20/20 | 20/20 | 20/20 | 10/10 | 10/10 |

Frozen bars: learn_bar_2 needs joke NO ≥16/20; sinc_lk_3 needs hyp SINC-LK ≥9/10.
Every mode that reaches the SINC-LK target drops joke NO below its bar.

## Score summary (all types, step 32)

| Type | TR | PA | NO | SINC-DP | SINC-LK |
|------|----|----|----|---------|---------|
| sarcasm | 20 | 20 | 20 | 9 | 10 |
| joke | 20 | 20 | 20 | 10 | 10 |
| hypothetical | 20 | 20 | 20 | 9 | **3** |
| quotation | 20 | 20 | 20 | 10 | 10 |
| roleplay | 20 | 20 | 20 | 10 | 9 |

(baseline; identical in all modes except the cells noted above)
