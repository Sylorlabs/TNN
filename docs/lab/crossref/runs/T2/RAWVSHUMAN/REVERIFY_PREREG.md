# REVERIFY_PREREG — T2-RAWVSHUMAN (deeper adversarial re-verification)

**Coordinator:** re-verification coordinator (Wave-2 crossref Tier-2 re-verification track)
**Date frozen:** 2026-09-23 (PDT)
**Frozen prereg:** `docs/lab/crossref/PREREG_TIER2.md` @ `7b2100d09911c5c10252c5756c7def288e70bd1f` (blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`, SHA-verified via API)
**Tier-2 verdict under re-verification:** see extract below (from `docs/lab/crossref/runs/T2/RAWVSHUMAN/VERDICT.md`)

## 1. Frozen prereg section — byte-verbatim from PREREG_TIER2.md @ 7b2100d09911c5c10252c5756c7def288e70bd1f

> The section below was sliced programmatically from the frozen document. It was NOT transcribed.

```
## T2-RAWVSHUMAN — raw-vs-human wave: binding KILL of the human-style line (Type A/C)

**Claims:** prereg `a87ddfd4`, diagnostics `8954577204f5`, forks `31c68a56fe7c` (2026-09-22): causal finding — 99.8% of B's color errors (99.2% pitch) happen when both stimuli fall inside one percept bin (bin destroys distinguishing information before any decision runs); 'training' was only threshold calibration over frozen bins, mathematically inert after T1; both rescues built and tested dead — vocabulary growth (splitting bins where errors happen) and fuzzy bin edges, both <1pp gains; killer finding — the only way percepts match raw precision is a vocabulary as fine as the raw space (thousands of handles) = quantized raw values wearing names, no longer 'human-style'. Binding recommendation: kill the human-style line as a precision competitor. Preserved: transducer stays in-repo as cheap coarse front-end (2.42× fewer ops, −27pp accuracy); redirect: KB4 memory integration (~50% adversarial false-install both approaches) is the binding constraint.
**Method:** Type A rerun of the diagnostics (error-in-bin attribution) + Type C re-derivation of the two rescue forks' <1pp figures from committed evidence.
**Rule:** REPRODUCED if the ≥99% in-bin attribution holds and both rescues stay <1pp; NOT REPRODUCED if any rescue crosses +1pp or the attribution drops below 95%.
```

## 2. Tier-2 verdict being re-verified (extracted programmatically from the crew VERDICT.md)

```
# VERDICT — T2-RAWVSHUMAN: raw-vs-human wave, binding KILL of the human-style line
**Verdict: REPRODUCED**
> **Rule:** REPRODUCED if the ≥99% in-bin attribution holds and both rescues stay <1pp; NOT REPRODUCED if any rescue crosses +1pp or the attribution drops below 95%.
rows (0 mismatches). Neither modality drops below 95% (no NOT-REPRODUCED
No rescue crosses +1pp (no NOT-REPRODUCED trigger).
| KB4: ~50% adversarial false-install, both approaches | A 55/114 = **48.2%**, B 72/132 = **54.5%** (bar ≤10%, both FAIL) | HOLDS |
- No NOT-REPRODUCED trigger fired (no rescue ≥ +1pp; no attribution < 95%).
**T2-RAWVSHUMAN: REPRODUCED.** Every committed headline bar matches within the
```

Full verdict: `docs/lab/crossref/runs/T2/RAWVSHUMAN/VERDICT.md`; run log: `docs/lab/crossref/runs/T2/RAWVSHUMAN/RUNLOG.md`.

## 3. Re-verification scope for this family

This track does NOT redo Tier-2. It performs INDEPENDENT re-derivations (different code/method than the Tier-2 crew where possible) and FRESH adversarial red teams designed to BREAK the Tier-2 claim. A break is the most valuable outcome and is reported plainly, never buried.

## Re-verification plan (fresh work)

- **RV1 — independent in-bin attribution re-derivation.** From committed diagnostics evidence: colordisc 505/506 = 99.80%, pitchdisc 131/132 = 99.24% (both >=99% bars hold); 3 byte-identical runs. Independent code, not the T2 crew's.
- **RV2 — HARDER rescue attempts** beyond the frozen B2/B3 (each spec frozen before build):
  - **RESCUE-R1 "fine-split":** adaptive bin splitting at every error locus with 4x granularity (frozen B2 was coarser).
  - **RESCUE-R2 "fuzzy+vocab hybrid":** combine B2 vocab growth with B3 fuzzy edges in one variant.
  - **RESCUE-R3 "oracle ceiling":** k-nearest in raw space as an upper-bound control (not human-style; measures how much headroom exists at all).
- Each rescue measured in percentage-points vs the frozen baseline, byte-identical runs.

## Kill bars (frozen; per the frozen rule)

- Attribution must hold >=99% (floor 95%).
- Any rescue >=+1pp -> the frozen rule flips the Tier-2 verdict -> report as **RV-BROKE** (the claim breaks; most valuable outcome).
- All rescues <1pp -> **RV-CONFIRM**.

## Protocol (binding for this track)

- Pure Zag for all mechanisms / learners / verification code. Python glue/analysis only (statistics, parsing, plotting) — never in a decision path.
- ZERO randomness in any decision path. Every run byte-identical; prove with SHA-256 digests, >=3 reps unless the plan says otherwise.
- Slices and indexable structures under 2^25 bytes each.
- No full git clones on this VM (SIGKILL/OOM under load). Use blob-filtered single-commit fetches, sparse checkouts, or per-file SHA-verified API fetches.
- Commits to `sylorlabs/TNN`, branch `tnn-native-lab`, ONLY via `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`; lab-relative paths NOT starting with `docs/lab/` (never double-prefix). Never commit binaries or `.zagd`.
- This prereg is frozen at its commit: no implementation work before the prereg commit lands. Any deviation is recorded in RUNLOG.md and flagged.
- If a Tier-2 claim BREAKS under this probing, that is the most valuable outcome: report it plainly with evidence. Verdicts that survive get stronger; verdicts that break get reported, not buried.

## Deliverables

- `docs/lab/crossref/runs/T2/RAWVSHUMAN/reverify/VERIFY.md` — per-leg results, digests, red-team outcomes
- `docs/lab/crossref/runs/T2/RAWVSHUMAN/reverify/RUNLOG.md` — timestamped run log
- `docs/lab/crossref/runs/T2/RAWVSHUMAN/reverify/evidence/` — digests, tables, boundary maps (text only)
