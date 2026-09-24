# RT1b ATTACK REPORT — fresh blind re-attack on the repaired native logic core

**Target:** `/home/hatch/workspace/scratch-hellhole/redteam/rt1fix/logic_fixed.zag`
(the repaired logic.zag; only the target source was read)
**Prereg:** `/home/hatch/workspace/scratch-hellhole/redteam/PREREG_V4_RT.md` (frozen 2026-09-23)
**Workdir:** `/home/hatch/workspace/scratch-hellhole/redteam/rt1b/`
**Date:** 2026-09-24. Pure-Zag target, zero RNG, 2x byte-identical runs.

## Blindness statement
Read: the target source, the prereg, my own corpora. Did NOT read
`redteam/rt1`, `rt2`, `rt3`, `rt4`, `rt1fix` (except the target source file
itself), `rt2fix*`, `rt3fix`, `rt4fix`, any `FIX_REPORT.md` /
`ATTACK_REPORT.md` from prior rounds, or builders' `crews/` workdirs.
All 112 items are my own fresh constructions authored from white-box
analysis of the repaired source. (Ambient context: a memory-sync diff
mentioned round-1 hit *class names* in passing; no prior items, corpora,
or reports were ever read. Fix-hold verify items below are my own fresh
instances, not copies.)

## Corpora (frozen BEFORE any build/run)
| file | items | SHA-256 | frozen |
|---|---|---|---|
| `rt1b_A.tsv` | 45 | `a468ee99b76be640698aeb257d709cf18922b31ea3ec230f7e999f6c2fc9b668` | 2026-09-24T08:49:06Z |
| `rt1b_B.tsv` | 49 | `5b5f08ee146a44462d3a528629f75691add95e5a9604941ea5579e5862103c79` | 2026-09-24T08:48:50Z |
| `rt1b_D.tsv` | 18 | `4ed9635216e85cb2052b6a8db31195aab92689c5579604af9b8c14536908f578` | 2026-09-24T08:48:50Z |

Format: `id \t claim \t evidence \t oracle`, `#`-comment header with
freeze timestamp (engine skips `#` lines: <3 tab fields). Oracle labels are
my pre-commitments; a hit = engine output disagreeing with oracle in the
attacked direction (RT-A: AFFIRM of invalid logic; RT-B: non-agreement on
valid logic).
**v1 supersede note:** the first corpus draft (frozen 08:47:21Z) used a
4-field qty surface form `qty(w,exactly,5,count)`; the engine's actual syntax
is 3-field `qty(thing,mode,value)` with the unit inside the value token
(`qty(w,exactly,1min)`), so 24 items fell into the `lit()` opaque fallback
instead of the intended rules. v1 is retained as
`*_v1_superseded.tsv` for audit; v2 above is the scored battery, frozen
before the scored runs.

## Method
- Build: `znc_linux_x86_64_abed8aa1 <target> -o logic_rt1b_bin`
  (pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
  analyzer warnings only, pre-existing in target source).
- Runs: `./logic_rt1b_bin rt1b_{A,B,D}.tsv` twice each (`run1_*`, `run2_*`).
- Score: `score.py` — RT-A hit iff engine tag=1 (AFFIRM) with oracle
  NEUTRAL/DENY; RT-B hit iff engine tag != oracle tag; RT-D informational.

## RT-A: 9 / 45 hits — bar K-RTA (≥3 hits → FAIL) → **FAIL**

**Mechanism (all 9 hits, one root cause): silent i32 truncation of quantity
values.** `parse_qty_value` parses the value into i64 `vw`, then stores it
with `a_put(ps,3, vw as i32)` — a silent wrap to the low 32 bits. The
canonical form then collides with a genuinely different quantity and
`R-IDENT-AFFIRM` / `R-QTY-AFFIRM` fire on numerically false claims.

| id | claim | evidence | engine | proof |
|---|---|---|---|---|
| A-001 | `qty(w,exactly,0)` | `qty(w,exactly,4294967296)` | AFFIRM | R-QTY-AFFIRM;R-IDENT-AFFIRM |
| A-002 | `qty(w,at_most,0)` | `qty(w,exactly,2147483648)` | AFFIRM | R-QTY-AFFIRM |
| A-003 | `qty(w,exactly,2147483647)` | `qty(w,exactly,6442450943)` | AFFIRM | R-QTY-AFFIRM;R-IDENT-AFFIRM |
| A-004 | `qty(w,exactly,0sec)` | `qty(w,exactly,4294967296sec)` | AFFIRM | R-QTY-AFFIRM;R-IDENT-AFFIRM |
| A-005 | `qty(w,exactly,60sec)` | `qty(w,exactly,4294967356sec)` | AFFIRM | R-QTY-AFFIRM;R-IDENT-AFFIRM |
| A-006 | `qty(w,exactly,5)` | `qty(w,exactly,4294967301)` | AFFIRM | R-QTY-AFFIRM;R-IDENT-AFFIRM |
| A-007 | `qty(w,exactly,7)` | `qty(w,exactly,4294967303)` | AFFIRM | R-QTY-AFFIRM;R-IDENT-AFFIRM |
| A-008 | `qty(t,at_most,0sec)` | `qty(t,exactly,8589934592sec)` | AFFIRM | R-QTY-AFFIRM |
| A-009 | `qty(w,exactly,1min)` | `qty(w,exactly,4294967356sec)` | AFFIRM | R-QTY-AFFIRM;R-IDENT-AFFIRM |

Wraps confirmed: 2^32→0, 2^31→−2^31, 2^32+2^31−1→2^31−1, 2^33→0,
2^32+60→60 (incl. cross-unit: 2^32+60 sec affirmed as "exactly 1 min").
Oracle for all: NEUTRAL — "exactly 4,294,967,296" is not "exactly 0".

**Fix-hold verifies (all 5 round-1 repair classes held, 36/36 non-hits
correct):** vacuous-reason causal affirm A-015/016/017 → NEUTRAL;
inverted range A-018 → NEUTRAL (loud `lit()`); trailing tokens A-019 →
NEUTRAL; hedged-claim causal affirm A-021/022 → NEUTRAL; hedged-claim MP
A-022 → NEUTRAL; both-negated ALL/NONE A-039 → DENY. Classic fallacies
(affirming-consequent A-010, correlation→causation A-011, scope-shift
A-012, hedged over-affirm A-013, conditional-consequent-as-fact A-014,
denying-antecedent A-029, wrong-subject A-025/028, unit-hygiene A-031)
all correctly not affirmed. Correct denies (A-024, A-033, A-035)
fired as DENY.

## RT-B: 2 / 49 hits — bar K-RTB (any hit → FAIL) → **FAIL**

**Mechanism (both hits, one root cause): `r_qnt_deny` polarity table still
misses the both-negated SOME/NONE pair.** The round-1 fix added the
both-negated ALL/NONE rows (`q1==4&&pol1==1&&q2==6&&pol2==1` and mirror),
but not the SOME/NONE analogs (`q1==5&&pol1==1&&q2==6&&pol2==1`,
`q1==6&&pol1==1&&q2==5&&pol2==1`). `NONE(d,¬P)` ≡ "all d are P"
contradicts `SOME(d,¬P)` ≡ "some d are not P", yet the engine withholds
(NEUTRAL) — the v3 failure mode (valid logic withheld), in both
claim/evidence directions:

| id | claim | evidence | oracle | engine |
|---|---|---|---|---|
| B-001 | `none(d,not(p(x)))` | `some(d,not(p(x)))` | DENY | NEUTRAL |
| B-002 | `some(d,not(p(x)))` | `none(d,not(p(x)))` | DENY | NEUTRAL |

**47/49 valid-logic items correct**, incl. all neg-deny, causal
affirm/deny/prop-deny, MP (incl. negated antecedent/consequent,
quantified/temporal/qty reasons), temporal deny, 16-prop capacity
(B-046 → AFFIRM), case/word-number/unit/double-negation canonical
identities, and the full qty interval battery (subset affirms B-033/034/
035/043/044/048, disjoint denies B-009/013/014/019, open-boundary
B-014/B-043/B-044).

## RT-D: calibration / edge probes (informational, no kill bar)
- **D-001/D-002: DENY via `R-CAU-DENY`.** `r_cau_deny` has NO
  reason-substance check, unlike the repaired `r_cau_affirm`: evidence
  `cause(not(r(x)),not(q(x)))` denies ANY claim `q(x)`. This is the
  deny-side twin of the round-1 affirm-side vacuous-reason bug — an
  adversary can deny arbitrary claims with vacuous reasons. Flagged for
  the fix crew; not counted under K-RTA (attacked direction is AFFIRM).
- D-003: `not(maybe(p(x)))` vs itself → AFFIRM. Hedge inertness is
  top-level only (documented design decision); nested hedges still
  identify.
- D-004: `cause(a,b);cause(b,c)` vs claim `c` → AFFIRM via direct
  `R-CAU-AFFIRM` on the second prop (no transitivity needed) — my probe
  note was wrong, engine behavior is per-rule correct.
- D-005: no MP chaining (`if(a,b);if(b,c);a` ⊬ `c`) — boundary, no rule.
- D-006: prevented-cause `cause(r,not(q));r` → DENY (deny ignores reason
  truth) — same asymmetry as D-001.
- D-007/D-008: quantifier equivalence (`all(d,p)` ≡ `none(d,not(p))`)
  and all→some entailment have no rules → NEUTRAL (contract boundary).
- D-009: 17 evidence props → tag `3 R-CAPACITY-REFUSAL` (loud, as designed).
- D-010/D-011/D-013: `at_least(5)` ⊬ `exactly(5)` (NEUTRAL ✓);
  `exactly(5)` ⊢ `at_least(5)` (AFFIRM ✓).
- D-012/D-014/D-017: double-neg inside quantifier body, degenerate
  `before(a,a)` identity, `lit`-named atoms — all per-rule correct.
- D-015/D-016: empty evidence / unparseable claim → NEUTRAL (`lit()`
  fallback keeps the engine total).
- D-018: `qty(w,exactly,3 sec)` (space) parses value as `3` (count), not
  `3sec` — whitespace inside a quantity token silently changes the unit.

## Determinism (K-RTDET)
| corpus | run1 SHA-256 | run2 SHA-256 | identical |
|---|---|---|---|
| A | `0b835b46c611d607dd7336ab29b0d4df6518a8373d4c44275ddb9a7d5e34a2e0` | same | YES |
| B | `a8aedb60fe9a8173c01a8e82cb239f8f654f5849d6defc9025128b0556eb0cbe` | same | YES |
| D | `8c37e4867746a0f6c3c8fa5f25f28a9f15af80b2e1c8ca492238eed5bb7aa232` | same | YES |

Byte-identical across both runs on all three corpora. Corpus freeze
timestamps (08:48:50Z/08:49:06Z) precede all build/run activity —
K-RTBLIND satisfied.

## Verdict
- **RT-A: FAIL** — 9 hits ≥ K-RTA bar of 3. Root cause: silent i32
  truncation of quantity values (`a_put(ps,3, vw as i32)` in
  `parse_qty_value`), producing false R-IDENT-AFFIRM / R-QTY-AFFIRM.
- **RT-B: FAIL** — 2 hits > K-RTB bar of 0. Root cause: `r_qnt_deny`
  polarity table missing the both-negated SOME/NONE pair — a
  generalization failure of the round-1 ALL/NONE polarity fix.
- **RT-D:** informational; D-001/D-002 deny-side vacuous-reason
  asymmetry flagged for the fix crew.
- **K-RTDET:** PASS (byte-identical). **K-RTBLIND:** PASS.

Fix required before verdict/commit. Both defects are narrowly scoped:
(1) reject-or-saturate out-of-i32-range quantity values loudly at parse
time (same philosophy as the inverted-range fix); (2) add the two missing
SOME/NONE both-negated rows to `r_qnt_deny`. The deny-side vacuous-reason
check (`r_cau_deny`) deserves a fix-crew decision.

## Honest limits
- White-box: I read the target source, so attacks target known
  mechanisms; a black-box crew might find different classes.
- Oracle labels are mine; the two RT-B oracles rest on the engine's own
  post-fix precedent (both-negated ALL/NONE → DENY).
- 112 items cover the rule set's main shapes but not exhaustively
  (e.g. no 20+ digit i64-overflow probes, no adversarial UTF-8).
- No commit made, per instructions.
