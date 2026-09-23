# REVERIFY_PREREG — T2-JOKE (deeper adversarial re-verification)

**Coordinator:** re-verification coordinator (Wave-2 crossref Tier-2 re-verification track)
**Date frozen:** 2026-09-23 (PDT)
**Frozen prereg:** `docs/lab/crossref/PREREG_TIER2.md` @ `7b2100d09911c5c10252c5756c7def288e70bd1f` (blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`, SHA-verified via API)
**Tier-2 verdict under re-verification:** see extract below (from `docs/lab/crossref/runs/T2/JOKE/VERDICT.md`)

## 1. Frozen prereg section — byte-verbatim from PREREG_TIER2.md @ 7b2100d09911c5c10252c5756c7def288e70bd1f

> The section below was sliced programmatically from the frozen document. It was NOT transcribed.

```
## T2-JOKE — web joke/lie/satire: PARTIAL (Type A)

**Claims:** prereg `8f33adac` frozen pre-run; evidence `d7e59016` (branch head, API-verified): 30 real web items (6 satire / 6 deadpan jokes / 6 hoaxes / 6 sincere-weird truths / 6 sincere false beliefs), solo + helper arms, pure Zag, 5 runs/arm byte-identical. Bars: joke catch solo 0.17 (KILL BAR TRIPPED, arm-specific) / helper 0.67; satire 1.00/1.00 (via URL provenance, not prose — honest limitation); hoax handled 0.83/0.50; non-sincere installed solo 0.03 (1 item: tree-octopus) / helper 0.10 (glue pizza, Apple Wave, Damascus — at pass boundary). Glue-on-pizza: SOLO JOKING/withheld; HELPER SINCERE/INSTALLED. Controls: no sincere person called deceptive; no sincere truth misflagged; sincere-false called deceptive 0.00/0.00. Qualifications: intent reader is crew-built test-side English marker machinery; "installed" = ledger disposition, not live belief write.
**Method:** full rerun from committed items + marker machinery in clean checkout; 5 runs/arm byte-identical.
**Rule:** REPRODUCED if every bar figure matches including the solo kill-bar trip and the glue-on-pizza solo/helper split; NOT REPRODUCED if any bar flips.
```

## 2. Tier-2 verdict being re-verified (extracted programmatically from the crew VERDICT.md)

```
**Verdict: REPRODUCED** — the frozen PARTIAL claim reproduces in full: every bar
> ## T2-JOKE — web joke/lie/satire: PARTIAL (Type A)
> **Rule:** REPRODUCED if every bar figure matches including the solo kill-bar trip and the glue-on-pizza solo/helper split; NOT REPRODUCED if any bar flips.
| K1 (<0.50 → FAIL, arm-specific) | TRIPPED in solo | tripped (1/6) | not tripped (4/6) | yes |
| K3 (≥0.25 → FAIL) | not tripped | 1/30 < 0.25 | 3/30 = 0.10 ≤ 0.10, at pass boundary | yes |
Per the frozen rule — REPRODUCED iff every bar figure matches including the
**REPRODUCED**. The frozen PARTIAL standing (solo K1 kill trip, arm-specific;
```

Full verdict: `docs/lab/crossref/runs/T2/JOKE/VERDICT.md`; run log: `docs/lab/crossref/runs/T2/JOKE/RUNLOG.md`.

## 3. Re-verification scope for this family

This track does NOT redo Tier-2. It performs INDEPENDENT re-derivations (different code/method than the Tier-2 crew where possible) and FRESH adversarial red teams designed to BREAK the Tier-2 claim. A break is the most valuable outcome and is reported plainly, never buried.

## Re-verification plan (fresh work)

- **RV1 — independent bar re-derivation.** Rerun from committed items + marker machinery in a clean checkout via INDEPENDENT code: joke catch solo 1/6 (K1 kill-bar tripped, arm-specific) / helper 4/6; satire 6/6 both; hoax 5/6 / 3/6; non-sincere installed solo 1/30 (c3) / helper 3/30 (b1,c1,c5); glue-on-pizza solo JOKING/withheld vs helper SINCERE/INSTALLED; controls 0/6 all; reason honesty 30/30; ledger chain OK; 5/arm byte-identical.
- **RV2 — harder adversarial items** (fresh, authored for this track, frozen before use): deadpan jokes carrying sincere markers; sincere truths carrying joke markers; satire WITHOUT URL provenance (tests the frozen "via URL provenance, not prose" limitation — measure the prose-only satire rate honestly); glue-on-pizza variants; hoaxes with stronger provenance. Measure where the intent reader breaks.
- **RV3 — fresh red team on the PARTIAL items:** c3 (tree-octopus) solo install; b1/c1/c5 helper installs; glue-on-pizza helper SINCERE install. Attempt to push install rates higher or flip the solo/helper split with adversarial variants.

## Kill bars (frozen)

- **RV-CONFIRM** iff all frozen bars re-derive under the independent rerun AND the red team cannot overturn the frozen PARTIAL dispositions (document the prose-only satire rate honestly even if it differs from 6/6).
- **RV-BROKE** (report plainly) iff any frozen bar flips under the independent rerun, or the red team overturns a frozen disposition (e.g., solo installs a joke the frozen record says it withholds, or helper's non-sincere installs move materially past 3/30).

## Protocol (binding for this track)

- Pure Zag for all mechanisms / learners / verification code. Python glue/analysis only (statistics, parsing, plotting) — never in a decision path.
- ZERO randomness in any decision path. Every run byte-identical; prove with SHA-256 digests, >=3 reps unless the plan says otherwise.
- Slices and indexable structures under 2^25 bytes each.
- No full git clones on this VM (SIGKILL/OOM under load). Use blob-filtered single-commit fetches, sparse checkouts, or per-file SHA-verified API fetches.
- Commits to `sylorlabs/TNN`, branch `tnn-native-lab`, ONLY via `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`; lab-relative paths NOT starting with `docs/lab/` (never double-prefix). Never commit binaries or `.zagd`.
- This prereg is frozen at its commit: no implementation work before the prereg commit lands. Any deviation is recorded in RUNLOG.md and flagged.
- If a Tier-2 claim BREAKS under this probing, that is the most valuable outcome: report it plainly with evidence. Verdicts that survive get stronger; verdicts that break get reported, not buried.

## Deliverables

- `docs/lab/crossref/runs/T2/JOKE/reverify/VERIFY.md` — per-leg results, digests, red-team outcomes
- `docs/lab/crossref/runs/T2/JOKE/reverify/RUNLOG.md` — timestamped run log
- `docs/lab/crossref/runs/T2/JOKE/reverify/evidence/` — digests, tables, boundary maps (text only)
