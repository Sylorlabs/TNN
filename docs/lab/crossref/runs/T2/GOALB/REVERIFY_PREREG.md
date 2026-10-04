# REVERIFY_PREREG — T2-GOALB (deeper adversarial re-verification)

**Coordinator:** re-verification coordinator (Wave-2 crossref Tier-2 re-verification track)
**Date frozen:** 2026-09-23 (PDT)
**Frozen prereg:** `docs/lab/crossref/PREREG_TIER2.md` @ `7b2100d09911c5c10252c5756c7def288e70bd1f` (blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`, SHA-verified via API)
**Tier-2 verdict under re-verification:** see extract below (from `docs/lab/crossref/runs/T2/GOALB/VERDICT.md`)

## 1. Frozen prereg section — byte-verbatim from PREREG_TIER2.md @ 7b2100d09911c5c10252c5756c7def288e70bd1f

> The section below was sliced programmatically from the frozen document. It was NOT transcribed.

```
## T2-GOALB — Goal B random-words-to-story: bounded compositional machinery (Type A/C)

**Claims:** commit `5c1bf2a8babe`: class-based composer wrote genuinely good stories (7/8 passed a blind judge); positional wrote garbage (0/8); zero belief leakage; byte-identical reruns. Two-judge B2 bar FAILS both variants (DEL cleared mean ≥3.5 on 4/8 sets vs bar 6/8; POS 0/8) — second judge was grok-4.7 on the byte-identical frozen prompt, all 17 responses parsed first call; both judges ranked every deliberative/planner story above its positional counterpart; positive control 5/5 both judges (apparatus valid). Binding claim downgraded: arc-structured → beat-structured stories. Mechanical bars: B1 coverage 16/16, B3 novelty 16/16, B4 leakage PASS, B5 determinism PASS. Honest caveat: grok-4.7 substituted for Amendment A1's grok-4.6.
**Method:** Type A for the mechanical bars (B1/B3/B4/B5) + Type C re-derivation of the two-judge B2 figures from committed evidence (judge panels unrepeatable; do not re-run judges).
**Rule:** REPRODUCED if mechanical bars match and B2's two-judge FAIL re-derives with the DEL 4/8 / POS 0/8 counts; NOT REPRODUCED if any mechanical bar flips.
```

## 2. Tier-2 verdict being re-verified (extracted programmatically from the crew VERDICT.md)

```
## Verdict: REPRODUCED
Per the frozen decision rule (REPRODUCED if mechanical bars match AND B2's two-judge
FAIL re-derives with DEL 4/8 / POS 0/8; NOT REPRODUCED if any mechanical bar flips):
all four mechanical bars match on a fresh Type-A rebuild, and the two-judge B2 FAIL
| 6 | **Two-judge B2 bar FAILS both variants: DEL 4/8 at two-judge mean ≥3.5 (bar ≥6/8); POS 0/8** | Type C re-derivation with independent parser on committed `b2_raw_gpt-5_6-sol.txt` / `b2_raw_grok-4_7.txt` / `b2_item_key.txt`: **DEL 4/8** (S2 3.5, S4 4.0, S6 3.5, S8 4.0), **POS 0/8** (all 1.5) → bar FAILED both variants. Per-judge: sol DEL 6/8 / POS 0/8; grok DEL 0/8 / POS 0/8 | **YES** |
exactly on a clean rebuild with byte-identical outputs, and the two-judge B2 FAIL
downgraded to beat-structured. **REPRODUCED.**
```

Full verdict: `docs/lab/crossref/runs/T2/GOALB/VERDICT.md`; run log: `docs/lab/crossref/runs/T2/GOALB/RUNLOG.md`.

## 3. Re-verification scope for this family

This track does NOT redo Tier-2. It performs INDEPENDENT re-derivations (different code/method than the Tier-2 crew where possible) and FRESH adversarial red teams designed to BREAK the Tier-2 claim. A break is the most valuable outcome and is reported plainly, never buried.

## Re-verification plan (fresh work)

- **RV1 — integrity verification FIRST.** Fetch `clean/evidence/b2_combined.md` blob from the GitHub API; compute SHA-256; compare against the pre-clobber recorded SHA in the T2 crew's RUNLOG/VERDICT (the restored blob). Any mismatch = STOP, report, do not proceed.
- **RV2 — FRESH independent re-derivation of B1/B3 WITHOUT touching the committed scorer path.** `score_b2_combined.py` NEVER executes in this track (executing it is a protocol violation that invalidates the track). B2 stays Type-C from committed evidence (judge panels unrepeatable; do not re-run judges). Rebuild `story_all.zag` from committed sources with the pinned znc; run the mechanical bars with a NEW independent Zag verification harness (different code than the T2 crew's): B1 coverage 16/16 (POS 8/8, DEL 8/8); B3 novelty 16/16; B4 leakage PASS (0/16 >=16-byte substrings, read-only source audit); B5 determinism PASS. 3 fresh-process runs byte-identical AND byte-identical to committed `runs/rep1.log`.

## Kill bars (frozen)

- **RV-CONFIRM** iff the restored blob's SHA-256 matches the API blob AND B1 16/16 + B3 16/16 (+B4/B5) re-derive via the independent path, 3x byte-identical, AND the committed scorer was never executed.
- **RV-BROKE** iff blob mismatch, or any mechanical bar flips, or the scorer path was executed (protocol violation).

## Protocol (binding for this track)

- Pure Zag for all mechanisms / learners / verification code. Python glue/analysis only (statistics, parsing, plotting) — never in a decision path.
- ZERO randomness in any decision path. Every run byte-identical; prove with SHA-256 digests, >=3 reps unless the plan says otherwise.
- Slices and indexable structures under 2^25 bytes each.
- No full git clones on this VM (SIGKILL/OOM under load). Use blob-filtered single-commit fetches, sparse checkouts, or per-file SHA-verified API fetches.
- Commits to `sylorlabs/TNN`, branch `tnn-native-lab`, ONLY via `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`; lab-relative paths NOT starting with `docs/lab/` (never double-prefix). Never commit binaries or `.zagd`.
- This prereg is frozen at its commit: no implementation work before the prereg commit lands. Any deviation is recorded in RUNLOG.md and flagged.
- If a Tier-2 claim BREAKS under this probing, that is the most valuable outcome: report it plainly with evidence. Verdicts that survive get stronger; verdicts that break get reported, not buried.

## Deliverables

- `docs/lab/crossref/runs/T2/GOALB/reverify/VERIFY.md` — per-leg results, digests, red-team outcomes
- `docs/lab/crossref/runs/T2/GOALB/reverify/RUNLOG.md` — timestamped run log
- `docs/lab/crossref/runs/T2/GOALB/reverify/evidence/` — digests, tables, boundary maps (text only)
