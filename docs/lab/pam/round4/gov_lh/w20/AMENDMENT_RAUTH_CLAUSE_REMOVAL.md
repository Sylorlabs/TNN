# Amendment — W20 R-AUTH: removal of the `declprov≠class` clause

**Status:** SIGNED 2026-09-25, decided-autonomously-per-Micah's-order (PAM Round 4 autonomous governance dispatch).
**Resolves:** the frozen-prereg inconsistency flagged in Round 4 (W20's R-AUTH listed a `declprov≠class` clause that frozen K-ETB-4 forbids from having any effect; the Round-4 worker removed the clause under kill-bar precedence).

## Amended text

R-AUTH is amended to **remove the `declprov≠class` clause**. The authoritative R-AUTH is the clause-removed build (R) as tested: R-FIC, R-AUTH (surviving clauses), R-HYP, R-REJ. K-ETB-4 is NOT amended — it stands as the requirement, and the clause-removed build satisfies it exactly.

## Why removal (not K-ETB-4 amendment, not keeping)

- **Safe:** 0 FACT leaks at 1x/10x/100x on an adversarial battery engineered specifically against the removed clause (888 leg outputs); every kept-out attack row attributable to a surviving clause (unattributed=0 at all scales).
- **Provably redundant:** 480-shape analytic enumeration of the (decl, class, producer-validity, authority-claim) attack space; 24 R-vs-K diffs; `attack_only_caught` = **0** — no attack shape exists that only the removed clause catches.
- **Keeping breaks K-ETB-4:** the clause-KEPT counterfactual flips 13 honest rows/shard in zerodecl (1300 flips, FACT 500→0 at 100x) — a direct, measured K-ETB-4 violation of the kind the Round-4 worker cited.
- **K-ETB-4 exact on the removed build:** zero (arena,dec) flips between run and zerodecl at every scale, including on the adversarial decl≠class battery.

## Disclosed warts (not safety failures)

- W1: B-10 twin prereg/generator inconsistency (3/shard) — the generator pairs P=10 with PARTNER=8 (tokenless); R-AUTH's surviving "authority claim without valid token → REJECT" clause correctly rejects these in both builds. Not a clause-removal effect; explains KB-GOV3 measuring 13 vs predicted 14 flips/shard.
- W2: C1-f1 scorer expectation bug (R-FIC routes fiction-flagged rows to FICTION before the producer check; FICTION ≠ FACT, no leak).
- W3: 82/480 analytic shapes lack empirical tape coverage (enumeration is analytic and complete; empirical battery covers 398/480).

## Evidence

`docs/lab/pam/round4/gov_lh/w20/VERDICT_GOVLH_W20.md` (frozen scorer run unmodified by coordinator after daemon restart; adjudicated per prereg §3 kill bars; KB-DET 444/444 rep pairs byte-identical). Prereg `PREREG_W20_GOVLH.md` frozen and committed alone before any build.

*Signed 2026-09-25 — PAM Round 4 autonomous governance dispatch.*
