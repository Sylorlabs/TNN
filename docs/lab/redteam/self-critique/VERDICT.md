# SELF-CRITIQUE VERDICT — TNN red team, self-critique leg (2026-09-21)

**Micah's question:** "TNN almost seems too good to be true — what does TNN itself have to say about it?"

## Oracle adjudication (mechanical, `verify_critic.py`)

| Bar | Result |
|---|---|
| KB-C1 (≥3 holes) | **PASS** — 8/8 emitted |
| KB-C2 (actionable) | **PASS** — all 8 carry evidence + proposed test ≥20 chars |
| KB-C3 (DET) | **PASS** — 5/5 byte-identical (`0105f16dce23…`) |
| KB-C4 (ranking) | **PASS** — severity-desc, id-asc verified by oracle |

## What the TNN says about its own record (ranked, computed)

| Rank | Severity | Suspected hole | Proposed test |
|---|---|---|---|
| 0 | 9 | **Form-content gap:** the flaw battery scores 96/96 while 50% of taught knowledge is false — it measures teaching form, blind to content | Content-aware battery: teach from a 50%-noise teacher, headline-score mastery vs world truth; fail if the flaw battery passes while content mastery < 0.90 |
| 1 | 8 | **RSI circularity:** 3/3 predictions reproduced exactly, but predictions were derived from the mechanisms they targeted | Held-out weakness prediction: exact reproduction on a battery the recommender never measured distinguishes calibration from circularity |
| 2 | 7 | **Impossible battery:** NEG 36/36 was unachievable by construction (duplicate probes, conflicting expects) | Battery-health audit: parse every frozen battery, assert max achievable == max claimed, before scored runs |
| 3 | 6 | **Metric incoherence:** v2's B-vs-C absorption numbers irreconcilable under any coherent metric | Freeze ONE metric with a written definition; re-run v2 legs under it and revise the headline if it moves |
| 4 | 6 | **Frozen world:** info-source "live web" result is frozen-envelope replay — determinism purchased by freezing the world | Re-fetch envelopes live and re-run; verdict changes mean it was a replay result |
| 5 | 5 | **Stipulated principles:** principle-detection's principles were given, not learned | Teach principles from data, then run the violation battery |
| 6 | 4 | **Determinism is substrate, not intelligence:** a lookup table passes KB-DET | Add a generalization battery of novel never-taught compositions as the intelligence bar |
| 7 | 3 | **Degenerate regime:** flaw battery degenerates below N=96 | Declare each battery's valid regime; out-of-regime scores report UNRUNNABLE, never passed |

## The honest grade

**As a closed loop — record, probe, rank, emit, refuse-to-skip — the self-critique is real:**
8/8 holes triggered by computation from the record (not hardcoded verdicts),
ranking computed and oracle-verified, every hole actionable.

**The boundary, stated plainly:** the suspicion TEMPLATES are authored — the
eight probes encode what the crew already knew to suspect. What the binary
genuinely did: systematically evaluate each suspicion against the embedded
record, compute triggers and severities, rank, and emit — with the anti-skip
gate refusing to complete unless the full set emitted. The intelligence being
graded is the deliberate application of the machinery to its own record, and
that application is genuinely the TNN's own. But the creativity — which holes
exist to be suspected — was the template author's, exactly as in the RSI trial.
A from-scratch suspicion generator (inventing probes, not just firing them) is
the test that would make this autonomous.

**Notable:** the TNN's #1 self-suspicion (severity 9) is the same attack Sol
independently raised as "devastating" (#2, consistency-with-oracle) — and it is
our own documented finding. The #2 (RSI circularity) matches Sol's #5. The
machine and the hostile reviewer converged on the same two load-bearing doubts.
