# PREREG R2-13 Amendment A1 (pre-results): trial count N=10,425

**Date:** 2026-09-23  
**Status:** PRE-RESULTS amendment. No evaluation battery has been run. No holdout
data has been viewed. This supersedes the N=9,925 figure in PREREG_R2-13.md §6.

## What changed

PREREG_R2-13.md §6 froze "9,925 adversarial trials". That number was a partial
filesystem observation made while the R2-7 fixture generator was still writing.
The authoritative fixture manifest is the R2-7 generator's own deterministic
record:

`senses/pam-rebuild/round2/forks/R2-7/fixtures_R2A/gen_ledger.jsonl`

which lists, for splits `r2a`/`r2a2`:
- r2a: 5,276 fixtures
- r2a2: 5,149 fixtures
- **Total adversarial: 10,425**

All 10,425 files exist on disk and their SHA-256 hashes match the ledger
(verified 2026-09-23: 10,425 ok, 0 missing, 0 bad SHA).

## Excluded

50 `.r2fx` files present on disk (17 in r2a/, 33 in r2a2/, all motiondir) are
NOT listed in gen_ledger.jsonl and have unknown provenance (likely partial
writes from a concurrent generation run). They are excluded from the eval.
All excluded files have `.truth` sidecars; exclusion is by ledger-membership,
not by content.

## Amended bar wordings

- **Bar 1:** ≤1% false installs on **10,425** adversarial trials
  (≤104 false installs; 104/10425 = 0.998%).
- **Bar 2:** unchanged (six novel holdout families; ≤2% each and ≤1% pooled).
- **Bar 3:** unchanged (≥50% reduction on design-family false installs).

## Rationale

The prereg §6 states "the fixture set is authoritative". The gen_ledger.jsonl
is the fixture set's authoritative manifest. Using it (rather than a
point-in-time directory listing) is the faithful implementation of the frozen
intent. The 10,425-trial battery is a strictly stronger falsifier than the
9,925-trial version.

## What did NOT change

Mechanism, features, contract rule, clauses, thresholds, bank construction,
holdout family list, scoring definitions, and determinism requirements are
unchanged. Only the trial-count N is corrected to the authoritative manifest.
