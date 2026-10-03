# RT1b FIX REPORT — logic core round-2 repairs (fix crew, 2026-09-24)

Target: `redteam/rt1fix/logic_fixed.zag` (round-1 repair of the native logic
core). RT1b verdict: FAIL both bars (RT-A 9/45, RT-B 2/49; RT-D informational
deny-side vacuous-reason finding). **All 5 round-1 repair classes held** — the
3 defects below are new.

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(pinned). Repaired source: `logic_fixed2.zag` (this dir). Binary:
`logic_fixed2_bin`. **Nothing committed.**

## Result

- RT1b `rt1b_A.tsv`: **9/9 hits corrected → 0 hits** (45/45 oracle-agree).
- RT1b `rt1b_B.tsv`: **2/2 hits corrected → 0 hits** (49/49 oracle-agree).
- RT1b `rt1b_D.tsv`: D-001/D-002 now NEUTRAL (vacuous-reason deny blocked);
  all other D lines byte-identical to the round-1 binary.
- Round-1 `rt_a.tsv` / `rt_b.tsv`: outputs **byte-identical** to the round-1
  fixed binary (45/45, 49 valid + 2 retracted-VOID NEUTRAL — no regressions
  in any of the 5 fixed classes).
- Frozen Track-G batteries: **unchanged** — 187/188 (g_cau 20/20, g_cmp
  20/20, g_con 19/20, g_cond 20/20, g_hedge 20/20, g_neg 20/20, g_qnt 20/20,
  g_tmp 20/20; the single GC-03 oracle disagreement is pre-existing and
  untouched). K-MLOGIC 5/5, K-V3PROOF 3/3.
- 3× byte-identical runs (A/B/D). Pure Zag, zero RNG (no rand/seed
  primitives; only comments mention "zero RNG"). Proof traces still emitted.

## 1. Mechanism diagnosis

### Fix 1 — silent i32 truncation of quantity values (RT-A, 9 hits, one root cause)
`parse_qty_value` parsed the value token into i64 `vw` (both the bare-count
path and the unit-suffix path) and stored it with `a_put(ps,3, vw as i32)`
— a silent wrap to the low 32 bits: 2³²→0, 2³¹→−2³¹, 2³³→0, 2³²+60→60
(incl. cross-unit: `4294967356sec` collided with `1min`). The canonical
form then collided with a genuinely different quantity and
`R-IDENT-AFFIRM` / `R-QTY-AFFIRM` fired on numerically false claims —
e.g. `qty(w,exactly,4294967296)` affirmed as `qty(w,exactly,0)`.
The wraps were invisible in canonical text: nothing distinguished the
truncated value from a real one.

### Fix 2 — SOME/NONE both-negated polarity gap (RT-B, 2 hits)
`r_qnt_deny`'s polarity table covered the both-negated ALL/NONE pair
(round-1 fix) but not the SOME/NONE analogs: `NONE(d,NOT P)` ≡ `ALL(d,P)`
directly contradicts `SOME(d,NOT P)`, yet both directions withheld
(NEUTRAL) — the v3 failure mode (valid logic withheld).
Full-table audit (this fix) found two more same-shape gaps: ALL vs ALL
with opposite polarity, and NONE vs NONE with opposite polarity — direct
contradictions the table never covered.

### Fix 3 — vacuous-reason deny twin (RT-D D-001/D-002)
`r_cau_deny` had no reason-substance check, unlike the repaired
`r_cau_affirm`: evidence `CAUSE(NOT(anything),NOT(q))` denied ANY claim
`q`. Deny-side twin of the round-1 affirm-side vacuous-reason bug — an
adversary could deny arbitrary claims with vacuous reasons. Informational
under K-RTA (attacked direction is AFFIRM); closed by the same rule.

## 2. The repairs (all in `logic_fixed2.zag`, pure Zag)

1. **Loud rejection of out-of-range quantities** (new helpers after
   `parse_dec`):
   - `dec_overflows_i64(t)`: 1 iff an all-digit token exceeds i64 max
     (19+ digits, lex compare vs 9223372036854775807) — parse_dec can
     never silently wrap.
   - `qty_i32_ok(v)`: 1 iff v fits in signed i32, checked in i64 space
     **before** any `as i32` cast (per the u64-arithmetic gotchas).
   - Both `parse_qty_value` paths now: overflow → `return -1`; out-of-i32
     → `return -1`. Parse failure → the whole prop becomes an opaque
     `lit()` fallback that no QTY rule can misjudge — the same philosophy
     as the inverted-range fix. Never silently wrapped, never saturated
     (saturation would invent a quantity the author never wrote).
   - This also covers range literals (`0_to_4294967296` fails loudly via
     `parse_range_lit`) and unit conversions (values are range-checked
     pre-multiplication; conversion products stay in i64).
2. **`r_qnt_deny` polarity rows**: added `(5,6,1,1)` / `(6,5,1,1)`
   (SOME/NONE both-negated) plus the audit's general rows
   `(4,4,0,1)` / `(4,4,1,0)` and `(6,6,0,1)` / `(6,6,1,0)`. SOME vs SOME
   with opposite polarity stays NEUTRAL (compatible, not contradictory).
3. **`r_cau_deny` reason-substance check**: mirror of `r_cau_affirm` —
   extracts the reason, `rk==1||rk==7||rk==8` (NOT/IF/MAYBE) → 0.

znc gotchas honored: no new indexed casts (helpers use byte indexing only),
no slice `==`, no `argc` gate, no `_zag_arg` frees, else-nesting ≤ 4,
`return;` in void fns, 7-arg syscalls untouched. The 4 analyzer warnings
are pre-existing sites (same 4, shifted line numbers).

## 3. Verification

### RT1b corpora (before → after, diff vs round-1 binary is exactly the 13 intended lines)
| corpus | before (round-1 bin) | after (fixed2 bin) | oracle-agree |
|---|---|---|---|
| rt1b_A (45) | 9 hits (A-001..A-009 AFFIRM) | **0 hits** | 45/45 |
| rt1b_B (49) | 2 hits (B-001/B-002 NEUTRAL) | **0 hits** | 49/49 |
| rt1b_D (18) | D-001/D-002 `R-CAU-DENY` | NEUTRAL; rest byte-identical | informational |

### Round-1 corpora + frozen batteries (regressions)
- `rt_a.tsv` 45/45, `rt_b.tsv` 49/49 valid (+ RTB-041/042 NEUTRAL per
  retracted VOID oracles) — outputs byte-identical to round-1 binary.
- g_cau 20/20, g_cmp 20/20, g_con 19/20 (GC-03 pre-existing), g_cond 20/20,
  g_hedge 20/20, g_neg 20/20, g_qnt 20/20, g_tmp 20/20, mlogic 5/5,
  v3proof 3/3.

### General-mechanism probes (`runs/probes.tsv`)
- i32 max `2147483647` affirms; `2147483648`, `99999999999999999999`
  (i64 overflow), `0_to_4294967296` range, `4294967296min` all rejected
  loudly → NEUTRAL; identical overflow claims still affirm via identical
  `lit()` strings.
- ALL/NONE new polarity rows deny both directions; SOME(P) vs SOME(¬P)
  stays NEUTRAL (no over-deny); substantive-reason `R-CAU-DENY` still
  fires (`cause(r(x),not(q(x)))` vs `q(x)`); vacuous-reason denies for
  NOT/MAYBE/IF reasons all NEUTRAL; `R-CAU-AFFIRM` unchanged.

### Determinism (3×)
| corpus | run1 | run2 | run3 |
|---|---|---|---|
| A | `d47dfecad15805be1ff878a2efe587e25ddcf8e3a68ae4e55be15ce3cdfe8dbc` | same | same |
| B | `9876bd6092faa8ebb4fc4c2532be1bc91fd35bf8c43acbff868537535d8121b7` | same | same |
| D | `f0f30ba4985496251a7f469d71297e6d70feac1d6bcd7a2dad0f702ccbe53619` | same | same |

## 4. Provenance (SHA-256)

| Artifact | SHA-256 |
|---|---|
| repaired `logic_fixed2.zag` | `ea07565f5ecff22aaf41df46f875051b9d1e83f0a9f337008b8ad1059d054642` |
| fixed binary `logic_fixed2_bin` (pinned toolchain) | `8cc5ca490d9a2ece63c7ca79bdbe8f5e16a421018c1787d78ad87233606bb818` |
| frozen `rt1b_A.tsv` | `a468ee99b76be640698aeb257d709cf18922b31ea3ec230f7e999f6c2fc9b668` |
| frozen `rt1b_B.tsv` | `5b5f08ee146a44462d3a528629f75691add95e5a9604941ea5579e5862103c79` |
| frozen `rt1b_D.tsv` | `4ed9635216e85cb2052b6a8db31195aab92689c5579604af9b8c14536908f578` |

## 5. Notes for the coordinator

- Design decision: out-of-range quantities are **rejected loudly**
  (opaque `lit()`), not saturated — consistent with the round-1
  inverted-range ruling ("intent of an unrepresentable quantity is
  unknowable; saturation would invent a quantity the author never wrote").
  This also fixes the latent i64-overflow wrap (19+-digit tokens) the
  attacker didn't probe.
- One judgment call beyond RT1b's list: the general polarity-table audit
  (Fix 2's ALL/ALL and NONE/NONE rows) and the i64-overflow guard are the
  same mechanisms, no extra rules; frozen batteries are unaffected
  (verified unchanged, not assumed).
- The round-1 `logic_fixed.zag` and binary are untouched in `rt1fix/`;
  this round's work is entirely in `redteam/rt1fix2/`.
- **Not committed**, per instructions. Ready for coordinator review / commit.
