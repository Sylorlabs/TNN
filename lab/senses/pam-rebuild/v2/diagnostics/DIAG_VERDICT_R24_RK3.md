# DIAG_VERDICT — self-application: R2-4 / RK-3 (9.4% correct installs)

**Harness:** `diagnose.zag` (frozen by PREREG_DIAG.md 2026-09-23)
**Case:** R2-4/RK-3 — correct high-confidence percepts reaching PASS-and-install
**Report:** `DIAG_REPORT_R24_RK3.txt` (sha256
`9ee3bdecdd103181e11e25201f425e1e1d6faba346a04c62f80f33ee142e7b0f`;
3 byte-identical runs)
**Date:** 2026-09-23

## Harness verdict (machine-produced, from instrumented evidence)

**KNOWLEDGE (primary) + SPEC-TENSION.**

| Probe | Result | Reading |
|-------|--------|---------|
| REPRODUCE | 104/1,102 (943 bps) vs bar 85% | failure frozen exactly |
| REPLAY | 0/11,840 disposition mismatches, 0 detail mismatches | machinery executes its design exactly — no implementation bug |
| K1 program knowledge | 1,062/1,102 progF==PASS (96.4%) | the system HAD the knowledge |
| K2 delivered to gate | 824/1,102 prog==PASS (74.8%) | 25.2% of the knowledge never reached the decision point |
| K3 buckets (of 998 non-installs) | never-PASS 278, conflict-withheld 621, suppressed 99, pred0 0, other 0 | complete partition, zero residue |
| K4 rule-blind knowledge | 605/621 conflict trials had progF==PASS (97.4%) | knowledge present in the record, unread by the rule |
| M1 synthetic control | 1,200/1,200 install | mechanism executes correctly, knowledge fixed |
| M2 synthetic conflict | 1,200/1,200 CONFLICT_WITHHELD | designed rule executes deterministically |
| CEILING | 824/1,102 = 74.8% < 85% bar | no gate change can pass RK-3 |

**Repair class:** RULE-ADDITION (corroborated-revision adjudication) |
PROGRAM-TEACHING (the (g) check's 278 false negatives) | SPEC-CHANGE (the
85% bar is arithmetically unreachable — 74.8% ceiling proven from the frozen
record).

**Surface patch: BLOCKED.** Installing more without the missing adjudication
rule installs false permanents — proven by the cf2 counterexample
(AUTOPSY_R2-4 §2.3: naive single-shot revision installs wrong trial seq 1145,
RK-1 0→1).

## Kill-bar scorecard (PREREG_DIAG.md §6)

- KB-D1 builds clean: PASS (3 non-blocking analyzer warnings, reference class)
- KB-D2 reproduces 104/1,102, replay 0/11,840: PASS
- KB-D3 3 byte-identical runs: PASS
- KB-D4 M1/M2 100%: PASS
- KB-D5 structured verdict, all numbers with evidence pointers: PASS
- KB-D6 zero RNG (static scan): PASS

## Red-team review of the harness conclusion (method §5 rule)

Reviewer: the building analyst, adversarial pass 2026-09-23.

1. **"KNOWLEDGE is doing too much work — the 621 and the 278 are different
   diseases."** Sustained in part. The harness's K3 already separates them
   (never-PASS vs conflict buckets) and the repair class names both paths
   (PROGRAM-TEACHING vs RULE-ADDITION). The single KNOWLEDGE label is the
   taxonomy's coarseness, not an error — but the verdict doc must always be
   read with the bucket table, never the label alone. **Action:** the method
   doc (§3d) now requires bucket-level repair mapping, not label-level.
2. **"K1's 96.4% could be (g)-check luck, not knowledge."** Answered in RT1:
   correctness is anchored to ground truth via jcorrect; the conjunction is
   the claim. The 278 false negatives are the honest counterweight — the
   harness reports both.
3. **"The SPEC-TENSION flag lets the bar off the hook — maybe the ceiling
   computation is wrong."** Checked: ceiling = correct-highconf with
   prog==PASS (the gate's actual input) and pred==1 = 824. The gate installs
   only PASS percepts (frozen H2 contract); deliberation downgrades are in
   the record. 824/1,102 = 74.77% < 85% is arithmetic, not modeling.
   The flag stands.
4. **"Replay fidelity is circular — same author, same misreading."**
   Partially sustained: the replay was written from memgate.zag by the same
   analyst. Mitigations in place: (a) byte-verified against the independent
   artifact `gate_dispositions.txt` (0/11,840 — a misreading that still
   matched 11,840 dispositions would have to be behaviorally identical, i.e.
   not a misreading that matters); (b) the sibling Python replay agreed
   independently. Residual risk recorded as gap G2/R T2, not hidden.
5. **"Does the harness add anything over the autopsy?"** Yes, two things:
   (a) the deliberation-downgrade catch (trials 2366/2372 — the hand analysis
   mis-bucketed them; the instrument didn't); (b) machine-checkable,
   re-runnable verdicts — the autopsy is a document, the harness is
   machinery any future case can invoke.

**Red-team sign-off:** conclusion stands with the bucket-table caveat (1).
No surface patch permitted.

## Honest gap list (what the harness cannot do — PREREG_DIAG.md §3.9 + §9)
G1–G4 as emitted in the report. Load-bearing: G1 (no program-text parsing —
mrgF/agree/strong opaque) means the harness cannot adjudicate the
corroborated-revision design itself, only diagnose the failure that motivates
it.
