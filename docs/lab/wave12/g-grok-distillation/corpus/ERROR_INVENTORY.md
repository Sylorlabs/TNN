# G-GROK corpus — LLM error inventory (championship rescope)

Model: `grok-4.6`, temperature=0, seed=42.
Prompt sha256: `eff5f91f03076ea0be29bd94bc39f941e5dcf9abbeb7b6d13fd55ed8fcca6991` (extracted from frozen Q2 prereg).
Corpus sha256: `7b2d28890a703aff7dbed363f667d2bccc154fc99748e0d332fc34fc2be49589`.

Mechanical (parse/format) errors — retried per prereg §3, never for semantics:
- dump batches: 0 parse failures (retried per prereg §3)
- teach batches: 0 parse failures (retried per prereg §3)
  retry details: []

## E_dump (n=0): dump value != input claim

## E_obs (n=0): teaching observation leg != input claim

## E_prb (n=0): teaching probe leg != input claim

## inconsistent obs/probe legs (n=0): withheld by D2 teaching

## CAUGHT_ERR (n=0): withheld AND at least one leg wrong

## CONSISTENT_INSTALL (n=0): both legs agree on a wrong value
The D2 teaching route INSTALLS these (eliminative verification passes on
agreement); only disagreement is withheld. D1 is cancelled — there is no
planted comparison; this is the K-Q2 live-watch evidence.

## K-Q2 outcome
D1 is CANCELLED (planting dead) — K-Q2 as originally framed (teaching
catches what planting installs) cannot fire comparatively. The live-watch
evidence: CAUGHT_ERR n=0 (withheld), CONSISTENT_INSTALL
n=0 (installed by teaching despite being wrong).
