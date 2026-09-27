# Pre-Repair Negative Control (Untrained Analyzer)

Date: 2026-09-26
Purpose: Documents the pre-repair analyzer's failure modes as a negative
control for the repaired/abstention-capable production version.

## Pre-repair scores (old inputs)
- 23 MATCH
- 8 MISS
- 4 WEAK
- 3 PARTIAL
- 6 HALLUCINATION

## Post-repair scores (same inputs, for comparison)
- B set: 35 MATCH / 0 hallucinations
- C set: 39 MATCH / 3 MISS / 2 WEAK MISS / 3 PARTIAL / 0 hallucinations

## What was fixed
Three false-positive mechanisms were repaired white-box:
1. (mechanism details in repair evidence)
2. (mechanism details in repair evidence)
3. (mechanism details in repair evidence)

The 6 pre-repair hallucinations are the negative control: the production
analyzer must not reintroduce them. The B/C regression (12/12 byte-identical)
proves it has not.
