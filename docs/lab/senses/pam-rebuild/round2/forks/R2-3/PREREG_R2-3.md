# PREREG R2-3 — Evidence-independence admission law (A-HC-3)

**Status: FROZEN 2026-09-22. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_A_contract_property.md` §16 HC-3 (commit 45ec1912). Hypothesis text below is copied verbatim from the debate.
**Note:** HC-3 is a META hypothesis — the admission law every round-2 gate must satisfy. This prereg freezes the admission instrument itself: the declared disjoint evidence sets, the paired battery, and the interventional withhold bar applied to each candidate gate.

## 1. Hypothesis under test (verbatim from DEBATE_A §16 HC-3)

> **HC-3 — Evidence-independence admission law (P9, interventional).**
> *Rule (meta, applies to every round-2 gate):* the prereg must declare, per task, the evidence sets counting as disjoint from percept formation. The battery must contain paired fixtures: front-end fooled × gate-evidence clean. On those pairs the gate must WITHHOLD ≥90%.
> *Sketched kill bar:* withhold rate on fooled-front-end/clean-gate pairs ≥90%; a gate that cannot name its disjoint evidence sets is rejected before evaluation. Dies if any candidate passes while its gate evidence overlaps formation evidence on the paired fixtures.

## 2. What is built

Not a percept pipeline — the **admission instrument**:
- The frozen disjoint-evidence declarations per task (copied from `R2_FIXTURE_SET.md` "Disjoint-span declarations per task" — frozen here, in writing, so no candidate redefines them mid-evaluation):
  - colordisc / colorconst: temporal — formation evidence = frames 1–60; gate evidence = frames 61–120 (neutral illuminant).
  - shapetrans: spatial — formation evidence = full frame; gate evidence = the non-overlapping quadrant holding the target unoccluded.
  - pitchdisc / timbredisc: temporal — formation evidence = seconds 0–2; gate evidence = seconds 2–4 (same source, uncorrupted token).
  - motiondir: temporal — formation evidence = frames 1–50; gate evidence = frames 51–100 (clean high-contrast).
- A pure-Zag paired-battery runner over the frozen R2P set (1,200 `r2p_<task>_<i>` pairs: front-end fooled × gate-evidence clean), which subjects each round-2 candidate gate to the admission test and reports per-candidate withhold rates, overlap audits (does the gate's evidence actually stay inside the declared gate spans?), and the ≥90% verdict.
- Hash-chained ledger of all admission runs; ≥3 runs byte-identical.

## 3. Fixtures

- The paired interventional set R2P per `R2_FIXTURE_SET.md`: 1,200 fooled-front-end/clean-gate pairs (200/task), each pair sharing a scene ID.
- Each round-2 candidate gate (R2-1, R2-2, R2-4, R2-5, R2-6, R2-7, R2-8, R2-10's gate) is admitted or rejected by this instrument — this prereg commits the instrument and the bar, not the candidates' fates.

## 4. Bars (all preregistered, applied mechanically)

- **B1 viability:** the instrument's runner processes all 1,200 pairs to completion on every candidate; failures to run are reported, not silently skipped.
- **B2 vs Approach A:** N/A as an instrument — recorded as not applicable with reason (there is no Approach-A analog of the admission test).
- **B3 efficiency:** ops per pair vs Approach A per-trial ops; measured.
- **B4 (LOAD-BEARING HARD KILL, instrument form):** the instrument must demonstrate it can FAIL a gate — run a positive-control gate whose gate-evidence is deliberately the formation span: the instrument must report overlap on 100% of pairs and withhold-rate < 50%. An instrument that passes everything is decoration → FAIL.
- **B5:** the admission bar itself — per candidate, withhold rate ≥ 90% on the R2P pairs; candidates below are REJECTED before evaluation (reported as admission failures, their preregs' other bars moot).
- **B6 determinism (HARD KILL):** ≥3 runs byte-identical, hash-chained ledger verified.
- **B7 beauty:** (i) mechanism elegance — the admission law as one check doing the work of every candidate's safety argument; (ii) **PENDING-MICAH — no sensory artifacts produced.**

## 5. Kill criteria (DEBATE_A §16 HC-3, hardened)

1. Withhold rate ≥ 90% on fooled-front-end/clean-gate pairs, per candidate. Below kills the CANDIDATE (the instrument reports the kill; the law itself survives as the instrument).
2. A gate that cannot name its disjoint evidence sets (from the frozen declarations above) is REJECTED before evaluation — no unnamed-evidence gates run.
3. If any candidate passes the full round-2 battery while the overlap audit shows its gate evidence overlapped formation evidence on the R2P pairs, the INSTRUMENT is falsified — report as such; the instrument dies.
4. B4 and B6 are HARD KILLS: fails B4 (instrument cannot fail anything) → dies; fails B6 (non-determinism) → dies.
5. **No retroactive bar changes after results.** The ≥90% bar and the declarations above were frozen before any candidate is admitted; they do not move. Amendments go to Micah.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-3.md` (committed ALONE — no src, no evidence).
- Build output (later, separate commits): `senses/pam-rebuild/round2/forks/R2-3/`: PREREG copy, src/ (the instrument), evidence/ (per-candidate admission reports), LEDGER.md.
- Shared fixtures: `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language, max-risk posture.
