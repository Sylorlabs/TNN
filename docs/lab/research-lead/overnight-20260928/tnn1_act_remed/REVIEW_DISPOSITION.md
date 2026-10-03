# ACT Remediation Prereg Review Disposition

Date: 2026-09-30. Reviewer: Muse (research coordinator).
Prereg: `docs/lab/research-lead/overnight-20260928/tnn1_act_remed/ACT_REMED_PREREG.md` @ `669aeb56b`.
Integration prereg: `7fc7148ac` (P-INT2, K4).
Coverage assessment: `4b36f0c1e` (3/16 covered, 11 not covered).

## Review

I have read the remediation prereg. It is complete and well-specified:

- Scope is clear: ports all 23 ptests + ALL-PASS banner from the standalone ACT suite into TNN-1, with identical names and expected values.
- The "no test changes" interpretation is precise: no changes to assertions, but P-ACT6A/B invoke TNN-1's real 3-step directional eviction (not the standalone's documented stand-in). This is strictly more informative for the retention claim.
- Predictions R-ACT1..4 cover the 24/24 pass, real eviction, no new architecture, and line count vs the 1200 ceiling.
- Kill bars K1..K5 are solid. K5 correctly handles the ceiling: overage is reported as a finding against F-INT1, not waived.
- Falsifiers F-RACT1..3 are sharp, particularly F-RACT2 (new-mode requirement stops the remediation).
- Controls C1 (standalone agreement) and C2 (compact battery no-regression) are appropriate.

The prereg fulfills the existing frozen P-INT2 requirement without modifying the integration prereg. This is the correct governance: remediation, not amendment.

## Disposition: ACCEPT

The prereg is accepted as frozen. The document's FROZEN status is confirmed.

## K1 anchor

This disposition is recorded. The prereg commit `669aeb56b` (containing the ACT remediation files) is the K1 anchor. The implementation's first commit must strictly follow it.
