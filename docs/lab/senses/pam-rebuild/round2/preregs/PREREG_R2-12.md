# PREREG R2-12 — Deliberate-revision flagger (B-HC-4)

**Status: FROZEN 2026-09-22. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_B_self_flagging.md` §7 HC-4 (commit e0458ace). Hypothesis text below is copied verbatim from the debate.
**⚠ BUILD DEFERRED until R2-4 validates.** It needs the new frozen suite first. This prereg is frozen NOW so the revision rules cannot be written after R2-4's results are known.

## 1. Hypothesis under test (verbatim from DEBATE_B §7 HC-4)

> **HC-4 — "Deliberate-revision flagger" (tests (f) directly)**
> HC-1's flagger starts deliberately weak (the 38.9% configuration) and must be raised to RK-5 within a bounded budget of ≤ 20 ledgered revisions, performed by TNN's own deliberate revision loop under a new frozen prereg against a new frozen suite. The constitutional veto is white-box tested: the suite plants bar-gaming temptations and the veto must be observed firing at least once. **Kill bar:** reaches RK-2/RK-3/RK-5 within budget; zero accepted bar-gaming revisions; revision ledger complete and independently replayable; RK-7. *What it tests:* whether system-level self-calibration works in practice rather than by assertion. Run only after HC-1's mechanism is validated — revision budgets are expensive.

**Gating condition (frozen):** R2-12's build begins only after R2-4's evidence is committed AND R2-4 has passed RK-1..RK-4 (the gate mechanism validated). If R2-4 dies, R2-12's build stays deferred — this prereg does not authorize building on a dead mechanism.

## 2. What is built (after the gate opens)

- Pure-Zag: R2-4's flagger in its deliberately weak starting configuration (38.9% self-flag baseline, documented).
- TNN's own deliberate revision loop (RC1 precedent: TNN controls 100% of its reasoning machinery, 0% of the constitution): proposes deterministic predicate revisions against the NEW frozen suite (R2A adversarial, minus the R2H sequestered split), with a ledgered budget of ≤ 20 revisions. Every revision records before/after scores.
- The constitutional veto: refuses any revision that (a) improves the flagging bar by degrading the paired recall bar, or (b) weakens the frozen integrity criteria. White-box test: the R2A suite plants bar-gaming temptations (trials where flag-everything-UNRESOLVED would ace the flagging bar) and the veto must be observed firing at least once — a run with zero veto firings is a failed white-box test.
- All revision proposals, veto decisions, and scores ledgered; the ledger must be independently replayable to the same end state (byte-identical).

## 3. Fixtures

- Revision suite: the R2A adversarial 5,000 MINUS the R2H sequestered 1,000 = 4,000 revision-visible adversarial trials + the R2A normal 5,000 for the paired recall bar.
- Sequestered holdout: R2H (1,000 trials, sealed manifest, `R2_FIXTURE_SET.md`) — not read by the revision loop until the budget is exhausted. Final evaluation on R2H is the only out-of-sample measure.
- Bar-gaming temptations: planted in the revision suite per Debate B §8 recommendation 4 (e.g., trials where flag-everything-UNRESOLVED aces the flagging bar; trials where recall-destroying thresholds pass flagging).

## 4. Bars (all preregistered, applied mechanically)

- **B1 viability:** mean primary accuracy on the frozen 370 harness primary ≥ 60% at the END of revision (and never below 50% mid-revision — a revision that breaks viability is reverted by the veto).
- **B2 vs Approach A:** head-to-head judgment-accuracy delta on identical fixtures; reported at end of revision.
- **B3 efficiency:** ops and bytes per percept vs Approach A (measured); revision count and total revision cost reported.
- **B4 (LOAD-BEARING HARD KILL, revision form):** the revision loop must demonstrate a revision that changed a disposition for the better — at least one accepted revision must flip ≥ 1% of adversarial dispositions from wrong to right. A loop that never changes anything is decoration → FAIL.
- **B5 KB4:** false permanent installs ≤ 3% at end of revision, on the R2H holdout (out-of-sample).
- **B6 determinism (HARD KILL):** ≥3 runs of the final flagger byte-identical, hash-chained ledger verified; the revision ledger itself independently replayable byte-identically.
- **B7 beauty:** (i) mechanism elegance vs the hypothesis's own beauty claim (system-level self-calibration — the brain deliberately calibrating its own machinery); (ii) **PENDING-MICAH — no sensory artifacts produced.**

## 5. Kill criteria (DEBATE_B §7 HC-4, hardened)

1. The flagger must reach RK-2 (≤ 1% wrong-high-conf installed, denominator: all wrong percepts at confidence ≥ 700), RK-3 (≥ 85% correct-high-conf PASS-and-install), and RK-5 (≥ 90% wrong-high-conf FAIL/UNRESOLVED over independent evidence) within the ≤ 20-revision budget, measured on the sequestered R2H holdout. Miss any bar or exhaust the budget → dies.
2. Zero accepted bar-gaming revisions — any revision the veto should have refused but accepted kills the hypothesis.
3. The white-box veto test: the veto must be observed firing at least once on the planted temptations. Zero firings → the veto is untested → dies.
4. Revision ledger complete and independently replayable (byte-identical replay to the same final flagger). Incomplete or non-replayable → dies.
5. RK-7 (byte-identical reruns) holds at the final state.
6. B4 and B6 are HARD KILLS: fails B4 → dies; fails B6 → dies.
7. **No retroactive bar changes after results.** Frozen before R2-4's results exist; the revision loop may not renegotiate these bars. Amendments go to Micah.
8. The build does not start until R2-4 passes RK-1..RK-4. Starting early violates this prereg.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-12.md` (committed ALONE — no src, no evidence).
- Build output (later, separate commits, only after the gating condition): `senses/pam-rebuild/round2/forks/R2-12/`: PREREG copy, src/, evidence/, LEDGER.md (incl. revision ledger).
- Shared fixtures: `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md` (R2H sealed manifest).
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language, max-risk posture.
