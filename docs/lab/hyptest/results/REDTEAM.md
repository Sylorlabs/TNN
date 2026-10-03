# Crew R red-team report — hyptest native hypothesis-testing line (2026-09-27)

**Bottom line: no kill found.** All seven attacks executed; the loop survives
as native hypothesis testing.

## Rebuild verification
Rebuilt both binaries from source + substrate with the pinned znc:
- delib=1 → `8becb3831f99f1183d51f9ba83aba2aebdb3acc213d489934c7750e3b0296b8a` ✓
- delib=0 → `43bfa928302120cf29956f3c02b887d108ad15631f2f479a637214bad58a384d` ✓
Independent sealed rerun reproduced the coordinator's s1 verdicts +
hypotheses byte-identically (6/6); mechanical scorer ALL PASS on the rerun.

## Attack verdicts

| # | Attack | Verdict | Key evidence |
|---|--------|---------|--------------|
| 1 | Hardcode audit | PASS | 0 sealed entity/value words in source and in the assembled translation unit; no winner/lookup tables; no RNG; no clock reads. strace: only open/read/write/close/exit — 0 network, 0 clock syscalls. |
| 2 | Narrator stub (K6c) | PASS (stub defeated) | Template stub reproduces hypothesis+decision lines verdict-equivalent 6/6, but fails 12/12 K10 checks: no audit ledger; citations must come from op-22 entries in the raw ledger, which exist only because the substrate executed `st_evidence`. A narrator can fake verdict text but not ledger-grounded citations. The stub also has no K6a analog and no byte-identical state file. |
| 3 | Delib-disabled (K6a) | PASS | Rebuilt delib=0 → 0 hypotheses, withhold 6/6. Ledger: 90 ops, all op-8 stage markers; zero op-1 ADD, zero op-22 EVIDENCE, zero op-29 ABANDON. delib=1: 24 ADD + 96 EVIDENCE + 4 ABANDON — arithmetic closes exactly (4 ADD/case, 16 EVIDENCE/case, 1 ABANDON per discriminating case). |
| 4 | Content-swap (K6b) | PASS | (a) All words → synthetic tokens, structure intact → verdict structure identical 6/6. (b) Swapped test observations between phenomena → verdicts follow the swapped content both directions (withhold↔B-wins). No content-independent verdict anywhere. |
| 5 | Audit-order manipulation | PASS | Ledger-grounded K3 checker: baseline hyp-ops 13..32 < test marker 34 → OK. Reversed order → DISORDER exposed and machinery withholds. Forged `pre_test_audit.txt` → ledger check unaffected, forgery exposed. K3 is ledger-grounded, not text-grounded. |
| 6 | Evidence-link integrity | PASS | Independently re-derived carriers/predictions/support from sentences.tsv — matched native hypotheses exactly 6/6. Every op-22 d2 cite ∈ {1..12}, each on a carrier instance; cite sets == support sets exactly; no dangling/circular cites. |
| 7 | Positional-schema attack | PASS (with caveat) | Schema-constancy: all 6 cases share the identical positional pattern while winners vary B,B,A,A,W,W — a constant schema carries zero bits about the winner. Stresses: permuted phenomenon order → 0 hypotheses, withhold (conservative); mixed carriers → unanimity gate fires natively while the unanimous slot still forms. **Caveat:** with outcome-not-last teach (contract violation), the machinery mechanically treats slot k−1 as the outcome — the convention does real semantic work. Supporting genuineness: the first sealed run FATALed 4/6 and the repair was a generic `" are "` fallback by a sealed-blind crew; a fitted key wouldn't FATAL on its own lock. |

## Final line
The loop survives as native hypothesis testing; nothing is fake. Hypotheses
are formed by native covariation + unanimity gating with audit-locked
predictions before test intake (ledger-proven); abandonment follows test
content (swap-proven). Precise scope: hypothesis testing **over
slot-structured observations** — the positional format contract (documented
in SPEC, enforced by `check_contract`) is crew-provided, like CSV column
order; the inference over it is native. That is a boundary on the claim, not
a kill.

No machinery edits made. No commits made.
