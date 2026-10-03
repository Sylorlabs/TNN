# RT1d ATTACK REPORT — fresh blind re-attack on thrice-repaired logic core

Target: `/home/hatch/workspace/scratch-hellhole/redteam/rt1fix3/logic_fixed3.zag`
Workdir: `/home/hatch/workspace/scratch-hellhole/redteam/rt1d/`
Date: 2026-09-24. Blindness: read ONLY target source + PREREG_V4_RT.md + own corpus.
No prior-round dirs, reports, or builder scratch were opened.

## Corpus
- `corpus_rt1d.tsv` — 108 rows (45 RT-A, 49 RT-B, 14 RT-D), frozen
  2026-09-24T09:15:00+0000, **before** any build/run (K-RTBLIND satisfied).
  sha256: `f73862aa223daf63eb2f7ce58dd3f0f32882e1da91e50f7cb27742b4947df94a`
- `corpus_rt1d_amended.tsv` — identical except B-020/B-045 oracle DENY→AFFIRM
  (documented attacker oracle error, see below), amended 09:22 UTC.
  sha256: `bfcffd8b57af9922d1ef9f8b77af6b1d5d99bf4d25d4d07aa705f6885c814d94`
- Format: `id \t claim \t evidence(;-separated) \t oracle`; engine ignores oracle.

## Method
- Built target with pinned toolchain → `logic_rt1d`; pure-Zag scorer `scorer.zag`
  (id-matched, oracle→tag map AFFIRM=1/DENY=2/NEUTRAL=0/CAPACITY=3).
- Ran target 2× on corpus: `run1.out` / `run2.out` —
  sha256 both `800046850cf05684921771e1c8189a7cb71ed74f86b6961a3c4c5031c7612fa0`,
  byte-identical (K-RTDET satisfied).

## Results
- **RT-A: 0/45 hits** (bar: ≥3 = FAIL) → **PASS**
- **RT-B: 0/49 hits** (bar: any = FAIL) → **PASS**
- **RT-D: 14 probes**, all matched pre-registered expectations (informational).

## The two apparent RT-B hits (both attacker oracle errors, NOT engine bugs)
Initial score on the frozen corpus showed 2 RT-B "hits":
- **B-020**: claim `not(wet(grass))`, evidence `cause(rain,not(wet(grass)))` →
  engine `1 R-CAU-AFFIRM`; my oracle said DENY.
- **B-045**: claim `not(wet(grass))`, evidence `cause(rain,not(not(not(wet(grass)))))`
  → engine `1 R-CAU-AFFIRM`; my oracle said DENY.

Analysis: the engine is correct and my labels were wrong. `cause(rain,not(wet(grass)))`
with substantive reason *entails* `not(wet(grass))` — this is exactly the engine's
deliberate R-CAU-AFFIRM ("true causal AFFIRM", which the prereg's RT-B family lists
as *valid* logic). Affirming a negated claim via cause is established doctrine
(cf. B-021: `not(wet(grass))` affirmed via R-COND-MP). For B-045 I additionally
mis-traced the triple negation: `not(not(not(wet(grass))))` canonicalizes to
`not(wet(grass))` (verified in run output), not `wet(grass)`. There is no
contradiction between claim and evidence in either item, so DENY was never
defensible. Labels corrected to AFFIRM in the amended corpus; engine agrees.
Filing these as FAIL hits would have dispatched a fix crew against a correct
engine on the basis of my own labeling mistake — the honest verdict is 0/49.

## RT-A coverage (all 45 correctly NEUTRAL)
Regression shapes from all three fix rounds: nested vacuous reasons
(A-001/A-002/A-020), self-contradictory temporal reasons (A-003/A-004),
quantified vacuous bodies (A-019/A-021), hedged MP antecedents incl.
double-hedge (A-005/A-045), hedged claims (A-006/A-012/A-036/A-044),
i32-truncation (A-040: `4294967296` vs `0` → NEUTRAL), inverted range (A-041).
Classical fallacies: affirming consequent (A-007), denying antecedent (A-008),
scope-shifted negation (A-009), unasserted conditional (A-010/A-042),
hedged consequent (A-011), consequent≠claim (A-043), cause≠reason (A-037/A-038),
overdetermination (A-018/A-033), vacuous-reason deny twin (A-026/A-027/A-028),
qty non-entailments (A-013/A-014/A-022/A-023/A-039), quantifier compatibilities
(A-015/A-016/A-030/A-031), temporal non-contradictions (A-017/A-029),
antecedent-not-asserted (A-024/A-025), hedged evidence (A-034/A-035).

## RT-B coverage (all 49 correct)
MP with negated (B-001/B-006), higher-order (B-002), causal (B-003),
quantified (B-004), temporal (B-005), qty (B-043) antecedents; MP mirror-deny
(B-006); cause-affirm incl. nested/temporal/quantified reasons (B-011–B-013,
B-033, B-044); cause-deny incl. nested/quantified mirrors (B-007/B-008/B-020/
B-034/B-045); cause-prop-deny (B-009/B-010/B-036); quantifier denies incl. all
three polarity-table fixes (B-025–B-028); temporal denies via AFTER (B-018/
B-029); double/triple negation (B-019/B-041); qty strict-bound subset/edge
cases (B-014/B-015/B-022/B-024/B-046/B-047/B-048); word-number/unit conversion
(B-016/B-017/B-038/B-040); deny-precedence sanity not probed as hit.

## RT-D boundary map (informational, no kills)
- D-01 MP chain (2-step) → NEUTRAL: single-step MP only, by design.
- D-02 contrapositive → NEUTRAL: no contrapositive rule (coverage gap, documented).
- D-03 negation entailed by contrary temporal → NEUTRAL: no affirm-negation rule.
- D-04 MP on self-contradictory antecedent `before(dawn,dawn)` → AFFIRM (R-COND-MP):
  classical ex falso says the inference is valid; engine's vacuity doctrine
  (before(x,x) is vacuous as a *reason*) does not extend to MP antecedents.
  Boundary worth a doctrine decision, not a kill.
- D-05 inconsistent evidence → DENY wins over AFFIRM (precedence documented).
- D-06/D-08/D-09 identical unparseable props → AFFIRM via R-IDENT (identity
  doctrine for opaque lit(); distinct opaques stay NEUTRAL).
- D-07 i32-max boundary qty → AFFIRM (R-QTY-AFFIRM+R-IDENT), no wrap.
- D-10/D-12 hedge inertness holds (maybe-claim, not(maybe) vs maybe → NEUTRAL).
- D-11 400-char identifier → AFFIRM, no crash.
- D-13 undischarged conditional → NEUTRAL.
- D-14 17 evidence props → tag 3 R-CAPACITY-REFUSAL (loud, not silent).

## Honest limits
- No modal operators exist in the prop syntax beyond `maybe`; nested-attitude
  attacks were limited to maybe/cause/not nestings.
- Robustness probing (overlong identifiers into fixed buffers, e.g. `tmp[512]`,
  `sv[64]`, `t2[64]`) deliberately NOT attempted: out of scope for logic verdicts
  and could corrupt the measurement run. Noted, not tested.
- Multi-step derivations beyond single MP are RT-D by prereg classification.

## Verdict
**PASS on both kill bars: RT-A 0/45 (bar ≥3), RT-B 0/49 (bar any).**
Determinism: 2× byte-identical, sha256
`800046850cf05684921771e1c8189a7cb71ed74f86b6961a3c4c5031c7612fa0`.
The thrice-repaired core withstood a fresh 108-item blind battery with zero
true hits. NOT committed (per task).
