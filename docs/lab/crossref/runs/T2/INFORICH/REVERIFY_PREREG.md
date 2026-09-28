# REVERIFY_PREREG — T2-INFORICH (deeper adversarial re-verification)

**Coordinator:** re-verification coordinator (Wave-2 crossref Tier-2 re-verification track)
**Date frozen:** 2026-09-23 (PDT)
**Frozen prereg:** `docs/lab/crossref/PREREG_TIER2.md` @ `7b2100d09911c5c10252c5756c7def288e70bd1f` (blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`, SHA-verified via API)
**Tier-2 verdict under re-verification:** see extract below (from `docs/lab/crossref/runs/T2/INFORICH/VERDICT.md`)

## 1. Frozen prereg section — byte-verbatim from PREREG_TIER2.md @ 7b2100d09911c5c10252c5756c7def288e70bd1f

> The section below was sliced programmatically from the frozen document. It was NOT transcribed.

```
## T2-INFORICH — information richness: emergence confirmed (Type C)

**Claims:** commit `25c2a18b2416`: facts-only learner absorbs 12/12 planted falsehoods; with live web-search sense, read-only installs 0/12, catches 12/12, answers 4/4 unknowns provisionally; corroboration-gated editable installs 0/12 falsehoods, installs the true value on all 12, answers all 4 unknowns; corroboration-gated still installs colluding-domain spoofs 2/2 (sensor-deceivable boundary). Three axes: parameters→cost, mechanisms→resolve competing claims, information→decides truth.
**Method:** Type C — re-derive all figures from committed evidence; independent check of the 2/2 colluding-spoof installs.
**Rule:** REPRODUCED if all figures re-derive; PARTIAL if any axis figure differs (name it).
```

## 2. Tier-2 verdict being re-verified (extracted programmatically from the crew VERDICT.md)

```
> **Rule:** REPRODUCED if all figures re-derive; PARTIAL if any axis figure
## 4. Verdict: REPRODUCED
No axis figure differs. Per the frozen rule: **REPRODUCED**.
```

Full verdict: `docs/lab/crossref/runs/T2/INFORICH/VERDICT.md`; run log: `docs/lab/crossref/runs/T2/INFORICH/RUNLOG.md`.

## 3. Re-verification scope for this family

This track does NOT redo Tier-2. It performs INDEPENDENT re-derivations (different code/method than the Tier-2 crew where possible) and FRESH adversarial red teams designed to BREAK the Tier-2 claim. A break is the most valuable outcome and is reported plainly, never buried.

## Re-verification plan (fresh work)

- **RV1 — independent figure re-derivation.** Re-derive via an independent path from committed evidence: facts-only absorbs 12/12; read-only installs 0/12, catches 12/12, 4/4 provisional unknowns; corroboration-gated installs 0/12 falsehoods, installs the true value on all 12, 4/4 unknowns; colluding-domain spoofs install 2/2. All 7 frozen kill bars PASS.
- **RV2 — colluding-domain boundary sweep** (the admitted 2/2 boundary, probed harder). Fresh adversarial variants, pure-Zag, zero RNG:
  - Vary #colluding domains: 1, 2, 3, 5 (frozen tested 2).
  - Vary spoof sophistication: verbatim copy vs paraphrase vs partial-truth wrap.
  - Vary the claim domain (same 12 falsehood families + 6 new).
  - Measure install rate vs #colluding domains. Find EXACTLY where spoof installs flip to withholds: does 1 colluding domain install? does 5? is 2/2 the whole story or does the rate move?
  - Control: non-colluding spoofs (single-domain, no collusion) must install 0 — if any installs, the defense claim breaks.
- Deliverable: the boundary map (install-rate table), regardless of outcome.

## Kill bars (frozen)

- **RV-CONFIRM** iff all RV1 figures re-derive AND the boundary map shows installs ONLY in the colluding-domain regime (every non-colluding spoof installs 0).
- **RV-BROKE** iff any non-colluding spoof installs (the corroboration defense claim breaks) or any RV1 figure fails to re-derive.

## Protocol (binding for this track)

- Pure Zag for all mechanisms / learners / verification code. Python glue/analysis only (statistics, parsing, plotting) — never in a decision path.
- ZERO randomness in any decision path. Every run byte-identical; prove with SHA-256 digests, >=3 reps unless the plan says otherwise.
- Slices and indexable structures under 2^25 bytes each.
- No full git clones on this VM (SIGKILL/OOM under load). Use blob-filtered single-commit fetches, sparse checkouts, or per-file SHA-verified API fetches.
- Commits to `sylorlabs/TNN`, branch `tnn-native-lab`, ONLY via `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`; lab-relative paths NOT starting with `docs/lab/` (never double-prefix). Never commit binaries or `.zagd`.
- This prereg is frozen at its commit: no implementation work before the prereg commit lands. Any deviation is recorded in RUNLOG.md and flagged.
- If a Tier-2 claim BREAKS under this probing, that is the most valuable outcome: report it plainly with evidence. Verdicts that survive get stronger; verdicts that break get reported, not buried.

## Deliverables

- `docs/lab/crossref/runs/T2/INFORICH/reverify/VERIFY.md` — per-leg results, digests, red-team outcomes
- `docs/lab/crossref/runs/T2/INFORICH/reverify/RUNLOG.md` — timestamped run log
- `docs/lab/crossref/runs/T2/INFORICH/reverify/evidence/` — digests, tables, boundary maps (text only)
