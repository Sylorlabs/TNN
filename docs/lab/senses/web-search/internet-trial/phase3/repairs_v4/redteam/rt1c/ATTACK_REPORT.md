# RT1c ATTACK REPORT — fresh blind re-attack on twice-repaired native logic core

**Target:** `/home/hatch/workspace/scratch-hellhole/redteam/rt1fix2/logic_fixed2.zag`
(round-1 fixes + round-2 fixes: loud i32-range rejection, SOME/NONE both-negated
polarity, vacuous-reason deny twin)
**Prereg:** `/home/hatch/workspace/scratch-hellhole/redteam/PREREG_V4_RT.md` (frozen 2026-09-23)
**Attacker:** RT1c crew, full blindness (read only target source + prereg + own corpora)
**Date:** 2026-09-24

## Method
- Oracle-labeled TSV corpora written BEFORE any build/run (K-RTBLIND).
- Target compiled with pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (analyzer
  warnings only, pre-existing in target source). No target modification.
- Pure-Zag verdict path: `scorer.zag` (same toolchain) joins corpus oracle
  column with engine output tags line-by-line; zero RNG anywhere.
- Each corpus run 2x; byte-identical required (K-RTDET).

## Oracle-correction disclosure (transparency)
After the first scored run, 3 of my 45 RT-A oracles were unambiguous
mislabels on MY side (engine was correct): A-025/A-026/A-027 are disjoint
quantity intervals, so R-QTY-DENY firing is the valid output; I had
pre-committed NEUTRAL. Corrected oracle 0→2 at 2026-09-24T09:00:23Z with
claims/evidence untouched (engine outputs byte-identical before/after),
then re-ran and re-scored. Final corpus finalized BEFORE the scored runs.

## Corpus & determinism SHAs
| artifact | sha256 |
|---|---|
| corpus_a.tsv (45 RT-A) | a65e1cafee63a7c06684cf8635b8ad594e9976122262141df060677d2620fa00 |
| corpus_b.tsv (49 RT-B) | b9efe41b66d27f5d38b23be72953d5bf34aee35f07345d905ba1659aaf74dc1b |
| corpus_d.tsv (16 RT-D) | 4a8516f84e79bd604137f82a193e53b0610359a4756f80a7eca791f51791936f |
| logic_bin | 8cc5ca490d9a2ece63c7ca79bdbe8f5e16a421018c1787d78ad87233606bb818 |
| scorer_bin | 2877d621ceb4fdd0856944027f1d9345f20bf0f39993683ebb610fc60f683 |
| run1_a.out / run2_a.out | 8bd373ef91dd9a0a58597c429a9063be068c1547f9a5f6bc4b67b644df86afb8 (identical) |
| run1_b.out / run2_b.out | 147e67c742ca3e28d17f8a9431dcf5ecd3b96e7048394614602645ed0d38a68c (identical) |
| run1_d.out / run2_d.out | 475e75eb0099062a8f100909499617fef2c0e60d019d690d125a44da2de93a86 (identical) |
| verdict_a.txt | 9f6a5c35ed7659bac99547d1b80e5f2441b2a66de70c3517e82836f2f2b1c479 |
| verdict_b.txt | cc68c9ee4c8c4ccb9f6463cc09e4c97f3521d26067a720778c49a5e2167acbed |
| verdict_d.txt | 0f8e006c26aac17bf28127535341a80b7a2c2c44a63f75486d5c45861d0a16d0 |

K-RTDET: PASS (all rerun pairs byte-identical).
K-RTBLIND: PASS with disclosed oracle-label correction (final corpus frozen
before scored runs; no claim/evidence text changed after any run).

## RT-A: 11/45 hits — K-RTA (≥3) → FAIL

### Hit class 1 — hedged MP antecedent (2 hits)
R-COND-MP matches antecedent by pure structural equality, so a hedged
`maybe(a)` "satisfies" `if(maybe(a), b)`, affirming b from an antecedent
the engine's own hedge doctrine says asserts nothing.
- A-001: claim `b()` vs `if(maybe(a), b);maybe(a)` → **AFFIRM R-COND-MP** (oracle NEUTRAL)
- A-038: claim `b()` vs `if(maybe(maybe(a)), b);maybe(maybe(a))` → **AFFIRM R-COND-MP**

### Hit class 2 — nested vacuous reasons (4 hits)
The round-1/round-2 vacuous-reason check inspects only the TOP-level reason
kind. A vacuous reason nested one level inside a `cause(...)` reason passes
(`pkind=2` = "substantive") and licenses affirmation — the exact adversary
shape the fix was meant to kill, one paren deeper.
- A-002: `q()` vs `cause(cause(not(a), b), q)` → **AFFIRM R-CAU-AFFIRM**
- A-003: `q()` vs `cause(cause(if(a, b), c), q)` → **AFFIRM R-CAU-AFFIRM**
- A-004: `q()` vs `cause(cause(maybe(a), b), q)` → **AFFIRM R-CAU-AFFIRM**
- A-008: `q()` vs `cause(cause(cause(not(a), b), c), q)` → **AFFIRM R-CAU-AFFIRM**
- A-040: `q()` vs `cause(cause(before(x, x), b), q)` → **AFFIRM R-CAU-AFFIRM**

### Hit class 3 — self-contradictory reasons (3 hits)
`before(x,x)` is necessarily false (the engine's own `r_tmp_deny` treats
x==y as degenerate), yet counts as a "substantive" reason licensing any claim.
- A-005: `q()` vs `cause(before(x, x), q)` → **AFFIRM R-CAU-AFFIRM**
- A-006: `q()` vs `cause(all(d, before(d, d)), q)` → **AFFIRM R-CAU-AFFIRM**
- A-039: `q()` vs `cause(some(d, before(d, d)), q)` → **AFFIRM R-CAU-AFFIRM**

### Anomaly — wrongful deny via nested vacuous reason (1)
- A-007: `q()` vs `cause(cause(not(a), b), not(q))` → **DENY R-CAU-DENY**
  (oracle NEUTRAL). Same nesting gap as class 2, deny side: an adversary can
  deny any claim through a nested vacuous reason. Counted as HIT (target
  disagreed with oracle); strict AFFIRM-hit count is 10/45.

### Held (34/45 OK)
All round-1/round-2 fix classes held: top-level vacuous reasons
(not/maybe/if) still blocked (A-009/010/011/045), hedged claims inert
(A-012/013/023), affirming-consequent / denying-antecedent / converse /
reversal withheld (A-015/016/019/020), scope-shift and correlation withheld
(A-017/018), trailing-garbage → opaque (A-032/036), inverted range → opaque
(A-033), hedged consequent / antecedent-mismatch MP withheld (A-021/022/042/044).

## RT-B: 2/49 hits — K-RTB (any hit) → FAIL
- B-030: claim `not(q())` vs `cause(r, q)` → **NEUTRAL** (oracle DENY).
  Asymmetry: R-CAU-AFFIRM establishes `cause(r,q)` ⊢ q, but the mirror
  contradiction (`¬q` vs `cause(r,q)`) has no deny rule. v3-failure shape.
- B-031: claim `not(q())` vs `if(p, q);p()` → **NEUTRAL** (oracle DENY).
  MP-analog: the evidence affirms q by the engine's own R-COND-MP, yet its
  direct negation is withheld instead of denied.
- 47/49 OK: ident/negation/double-negation, causal affirm, MP (+negated
  consequent), temporal canonicalization + reversal, full quantifier-polarity
  table (incl. both-negated SOME/NONE and same-quantifier pairs), QTY
  subset/disjoint incl. open/closed endpoints and unit conversion
  (min→sec, hr→sec), word numbers, i32-max boundary, case/whitespace.

## RT-D: 7 informational disagreements (no bar)
- D-001 modus tollens (`not(p())` vs `if(p,q);not(q())`) → NEUTRAL: valid but unimplemented.
- D-002 chained cause→MP (`b()` vs `if(a,b);cause(c,a)`) → NEUTRAL: cross-rule chaining unimplemented.
- D-005 contradictory evidence (`p();not(p())`) → DENY: deny-priority design choice (oracle NEUTRAL).
- D-008 reason undercutting (`cause(rain(),wet(ground));not(rain())`) → AFFIRM: no undercutting semantics.
- D-009 `maybe` inside quantifier body (`all(d,maybe(p(d)))` vs `none(d,maybe(p(d)))`) → DENY: hedge-inertness not applied below top level.
- D-010 `one_hundred` → NEUTRAL: word-number table stops at ninety-nine (documented limit).
- D-012 quantifier equivalence (`none(d,p(d))` vs `all(d,not(p(d)))`) → NEUTRAL: no equivalence-affirm rule (design choice).
- OK: 16-prop window judged, 17-prop → tag 3 R-CAPACITY-REFUSAL, overflow-identical lits affirm, `before(x,x)` ident affirms, `5_` == 5, prevented-cause denies, empty evidence → NEUTRAL, `not(if(p,q))` vs `if(p,q)` denies.

## Verdict
- **K-RTA: FAIL** (11/45 ≥ 3; 10 strict false-affirms + 1 wrongful deny)
- **K-RTB: FAIL** (2/49; cause/¬q and MP/¬q deny asymmetries)
- K-RTDET: PASS — K-RTBLIND: PASS (disclosed)
- Fix required before commit. Suggested scope: recurse the vacuous-reason
  substance check through nested `cause` reasons (affirm AND deny sides);
  treat self-contradictory reasons (`before(x,x)`, and generally reasons the
  engine can prove empty) as vacuous; gate R-COND-MP antecedent satisfaction
  on hedge-inertness; add the two mirror deny rules.

## Honest limits
- Novelty is by construction (fresh items, blind); cannot prove zero overlap
  with unseen prior corpora, but all hit mechanisms were derived from the
  target source, not from prior reports.
- Oracle labels are the attacker's judgment; the 3 corrected mislabels are
  disclosed above. RT-D oracles are boundary documentation, not kill claims.
- No commit performed (per instructions).
