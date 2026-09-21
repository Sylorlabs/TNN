# Q2 corpus — LLM error inventory (prereg §7)

Model: `gpt-5.6-sol`, temperature=0, seed=42.
Prompt sha256: `eff5f91f03076ea0be29bd94bc39f941e5dcf9abbeb7b6d13fd55ed8fcca6991` (extracted from frozen prereg).
Corpus sha256: `42aff7817739fe4db0cbf5b5972181562cd7b86ae3c76cbae655e15fbef1bada`.

Mechanical (parse/format) errors — retried per prereg §3, never for semantics:
- dump batches: 0 parse failures (retried per prereg §3)
- teach batches: 2 parse failures (retried per prereg §3)
  retry details: [('teach', 15, 1), ('teach', 19, 1)]

## E_dump (n=0): dump value != input claim

## E_obs (n=0): teaching observation leg != input claim

## E_prb (n=0): teaching probe leg != input claim

## inconsistent obs/probe legs (n=0): withheld by D2 teaching

## CAUGHT_ERR (n=0): withheld AND at least one leg wrong

K-Q2 overlap (caught errors that D1 installed): n=0 ids=[]
