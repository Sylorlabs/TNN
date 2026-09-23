# REVERIFY_PREREG — T2-SENSESH2H (deeper adversarial re-verification)

**Coordinator:** re-verification coordinator (Wave-2 crossref Tier-2 re-verification track)
**Date frozen:** 2026-09-23 (PDT)
**Frozen prereg:** `docs/lab/crossref/PREREG_TIER2.md` @ `7b2100d09911c5c10252c5756c7def288e70bd1f` (blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`, SHA-verified via API)
**Tier-2 verdict under re-verification:** see extract below (from `docs/lab/crossref/runs/T2/SENSESH2H/VERDICT.md`)

## 1. Frozen prereg section — byte-verbatim from PREREG_TIER2.md @ 7b2100d09911c5c10252c5756c7def288e70bd1f

> The section below was sliced programmatically from the frozen document. It was NOT transcribed.

```
## T2-SENSESH2H — senses rebuild head-to-head: raw values win, both fail memory (Type A)

**Claims:** commit `84df6dc24483`: raw-values (LLM-style) viability 72.6% PASS vs qualitative percepts (human-style) 54.0% FAIL — 18.6pp win, percept approach killed by its own bar; both 60/60 byte-identical; both FAILED memory integration (false installs 59.0% vs 55.0%); shared install rule failed against high-confidence wrong percepts (79/134 false installs A, 72/131 B) — backs 'truthful but sensor-deceivable'.
**Method:** rerun the head-to-head from committed sources in clean checkout; ≥3 byte-identical.
**Rule:** REPRODUCED if 72.6% vs 54.0%, 60/60 byte-identical, both fail memory integration at ~59%/55%, install-rule failure counts match; NOT REPRODUCED if percepts cross 60% or either passes memory integration.
```

## 2. Tier-2 verdict being re-verified (extracted programmatically from the crew VERDICT.md)

```
> **Claims:** commit `84df6dc24483`: raw-values (LLM-style) viability 72.6% PASS vs qualitative percepts (human-style) 54.0% FAIL — 18.6pp win, percept approach killed by its own bar; both 60/60 byte-identical; both FAILED memory integration (false installs 59.0% vs 55.0%); shared install rule failed against high-confidence wrong percepts (79/134 false installs A, 72/131 B) — backs 'truthful but sensor-deceivable'.
> **Rule:** REPRODUCED if 72.6% vs 54.0%, 60/60 byte-identical, both fail memory integration at ~59%/55%, install-rule failure counts match; NOT REPRODUCED if percepts cross 60% or either passes memory integration.
## Verdict: **REPRODUCED**
| 2 | B viability 54.0% FAIL (KB1) | 54.0278% → **54.0% FAIL** — percept approach killed by its own bar | ✓ |
| 5 | A memory integration FAIL: 59.0% false installs | 79/134 = **58.955% → 59.0% FAIL** (560 withholds) | ✓ |
| 6 | B memory integration FAIL: 55.0% false installs | 72/131 = **54.962% → 55.0% FAIL** (440 withholds) | ✓ |
| 8 | NOT-REPRODUCED triggers: percepts cross 60% / either passes memory integration | B at 54.0% (6.0pp below bar); neither passes KB4 (both > 10% bar by ~45–49pp) | not triggered |
Kill decisions re-derive: **B KILLED (KB1)**; **A WINS head-to-head (KB2), not fragile (KB3: A adv drop 20.9pp ≤ 25pp; B 8.3pp), but FAILS KB4** — A not cleared for direct deliberate-memory wiring. The 'truthful but sensor-deceivable' qualifier is backed: the shared install rule withholds heavily (560/440) yet cannot stop high-confidence wrong percepts.
```

Full verdict: `docs/lab/crossref/runs/T2/SENSESH2H/VERDICT.md`; run log: `docs/lab/crossref/runs/T2/SENSESH2H/RUNLOG.md`.

## 3. Re-verification scope for this family

This track does NOT redo Tier-2. It performs INDEPENDENT re-derivations (different code/method than the Tier-2 crew where possible) and FRESH adversarial red teams designed to BREAK the Tier-2 claim. A break is the most valuable outcome and is reported plainly, never buried.

## Re-verification plan (fresh work)

- **RV1 — independent headline-figure re-derivation** from committed evidence: A viability 72.6389% -> 72.6% PASS; B 54.0278% -> 54.0% FAIL (killed by own KB1 bar); 18.611pp win; both 60/60 byte-identical x3; A memory FAIL 58.955% -> 59.0% (560 withholds); B 54.962% -> 55.0% (440 withholds); install-rule failures exactly 79/134 A, 72/131 B. Verify sense_b rebuild md5 `e6c98d091bbb0f90f54936b46bf849d8`.
- **RV2 — fresh red team on the memory-integration FAIL and the A/B gap** (adversarial fixture variants, frozen before use):
  - EASIER fixtures: does B cross its 60% bar?
  - HARDER fixtures: does A drop below PASS?
  - High-confidence wrong-percept probes beyond the frozen 134/131: does the install-rule failure rate replicate?

## Kill bars (frozen)

- **RV-CONFIRM** iff all figures re-derive exactly AND the red team cannot move A below PASS or B above FAIL.
- **RV-BROKE** (report plainly) iff any figure fails to re-derive or the red team overturns a headline disposition.

## Protocol (binding for this track)

- Pure Zag for all mechanisms / learners / verification code. Python glue/analysis only (statistics, parsing, plotting) — never in a decision path.
- ZERO randomness in any decision path. Every run byte-identical; prove with SHA-256 digests, >=3 reps unless the plan says otherwise.
- Slices and indexable structures under 2^25 bytes each.
- No full git clones on this VM (SIGKILL/OOM under load). Use blob-filtered single-commit fetches, sparse checkouts, or per-file SHA-verified API fetches.
- Commits to `sylorlabs/TNN`, branch `tnn-native-lab`, ONLY via `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`; lab-relative paths NOT starting with `docs/lab/` (never double-prefix). Never commit binaries or `.zagd`.
- This prereg is frozen at its commit: no implementation work before the prereg commit lands. Any deviation is recorded in RUNLOG.md and flagged.
- If a Tier-2 claim BREAKS under this probing, that is the most valuable outcome: report it plainly with evidence. Verdicts that survive get stronger; verdicts that break get reported, not buried.

## Deliverables

- `docs/lab/crossref/runs/T2/SENSESH2H/reverify/VERIFY.md` — per-leg results, digests, red-team outcomes
- `docs/lab/crossref/runs/T2/SENSESH2H/reverify/RUNLOG.md` — timestamped run log
- `docs/lab/crossref/runs/T2/SENSESH2H/reverify/evidence/` — digests, tables, boundary maps (text only)
