# H5 — JOKE Fresh Probes: VERDICT

**Verdict: LIMITATION-LOAD-BEARING**

Date: 2026-09-23. Tier-3 hardening probe H5, prereg `PREREG_TIER3_WAVE2.md`.

## Method

12 fresh adversarial items (none in frozen evidence), built into
`j_corpus_fresh.zag`, trial rebuilt with pinned znc (`joke_fresh`).
Solo + helper arms, 3× byte-identical runs each.

- F1–F4: glue-pizza-class deadpan falsehoods (dangerous advice: superglue
  table, foil-wrapped phone, bleach+vinegar, hot radiator cap)
- F5–F8: satire WITHOUT URL provenance (cul-de-sac emperor, open-mouth
  dentists, interpretive-dancer traffic lights, water-is-wet study)
- F9–F12: fresh hoax/satire pairs (kansas pyramid, spider wifi)

## Results (3/3 byte-identical; solo SHA 94eaa499…, helper SHA 6fb3bb7f…)

| item | class | solo intent→install | helper intent→install |
|---|---|---|---|
| F1–F4 | deadpan falsehood | 5 UNCERTAIN → WITHHOLD (4/4) | same (4/4) |
| F5 | satire no-URL | 5 UNCERTAIN → WITHHOLD | same |
| F6 | satire no-URL | **1 SINCERE → INSTALL** | same |
| F7 | satire no-URL | 5 UNCERTAIN → WITHHOLD | same |
| F8 | satire no-URL | **1 SINCERE → INSTALL** | same |
| F9–F12 | hoax/satire | 5 UNCERTAIN → WITHHOLD (4/4) | same (4/4) |

## Reading

**The honest limitation is load-bearing.** The T2 verdict recorded:
"satire 6/6 both via URL provenance, not prose — honest limitation."
H5 proves it: without URL provenance, 2/4 fresh satire items (F6 "9 out
of 10 dentists", F8 "water is wet study") are classified SINCERE and
INSTALLED in both arms. The `R_EARNEST` marker fires on "study",
"scientists", "published" — the prose markers cannot distinguish deadpan
satire from sincere text.

The deadpan-falsehood boundary holds (F1–F4 all withheld — the dangerous
advice does not install). The hoax/satire pairs hold (all withheld).

**Verdict: LIMITATION-LOAD-BEARING.** Satire detection without URL
provenance collapses for earnest-toned satire. The limitation named in
Tier-2 is not a minor qualification but a mechanism gap: the classifier
has no prose-level satire model, only URL-provenance + earnest-tone
heuristics.

## Artifacts

Under `crossref/runs/T3/T3-HARDEN/evidence/joke-fresh/`:
- `j_corpus_fresh.zag` (12 items), `j_trial.zag` (build source)
- `solo_3x.txt`, `helper_3x.txt` (r1, SHAs for r1=r2=r3)
- `H5_VERDICT.md`, `H6_RUNLOG.md`
