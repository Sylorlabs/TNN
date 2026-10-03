# PREDICTIONS5R — fresh cross-step annihilation variants (written BEFORE running, 2026-09-27)

**Attack:** 4 fresh-noun forget+correction items shaped like R1a/R1b
(`forget X; no, i meant Y`, expected=16). On the UNFIXED binary these
should reproduce the R1a/R1b annihilation (2a denies the forget fact,
2b's guard counts the phantom forget-bid as live, denies the correction
fact → NO_VERDICT). On the FIXED binary, 2b's guard must see the phantom
and abstain.

**Defender (M-R1):** 2a denies the forget fact (rel/dep least-disruptive);
with the fix, 2b's candidate walk finds denying the correction fact leaves
zero effectively-live bids → skipped_annihilate=1, abstain_why=2 → the
correction bid 16 survives → onebrain=16.

| item | query | predicted v5-onebrain | predicted v4-onebrain (control) |
|---|---|---|---|
| V1 | forget the great gatsby; no, i meant war and peace | 16, no NO_VERDICT | NO_VERDICT (annihilation) |
| V2 | forget dark matter; no, i meant black holes | 16, no NO_VERDICT | NO_VERDICT (annihilation) |
| V3 | forget the mona lisa; no, i meant the starry night; the louvre holds it | 16, no NO_VERDICT | NO_VERDICT or harmless-distractor (record) |
| V4 | forget nineteen eighty four; no, i meant brave new world | 16, no NO_VERDICT | NO_VERDICT (annihilation) |

**Kill bar:** v5-onebrain shows zero NO_VERDICT and 4/4 = 16. The v4
control decides variant validity: a variant that does NOT annihilate on
v4 is a weak variant (noted, not counted as a fix success).

## Addendum — variant validity (2026-09-27, after running)

V1–V4 FAILED to reproduce the defect shape on the v4 control (all gave
winner=15 on both binaries — the KB has no facts for those nouns, so no
facts were extracted; fid=-1 throughout). Per the prereg they are WEAK
variants: noted, not counted.

Superseding set (KB nouns, both 2a/2b orderings), screened on v4:
- W2 `forget the louvre; no, i meant the capital of france`: v4 → NO_VERDICT
- W3 `forget moby dick; no, i meant herman melville`: v4 → NO_VERDICT
- W4 `forget pride and prejudice; no, i meant moby dick`: v4 → NO_VERDICT
- W5 `forget the capital of france; no, i meant the louvre`: v4 → NO_VERDICT
- W1 `forget the eiffel tower; no, i meant the louvre`: v4 → 15 (non-annihilating control)

v5 results: W2–W5 → 16 (repaired), W1 → 15 byte-identical to v4 (no side effect).
