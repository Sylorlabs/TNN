# RT1c FIX REPORT — logic core round-3 repairs (fix crew, 2026-09-24)

Target: `redteam/rt1fix2/logic_fixed2.zag` (rounds 1+2 repaired native logic
core). RT1c verdict: FAIL both bars (RT-A 11/45, RT-B 2/49; RT-D
informational). **All round-1 and round-2 fix classes held** — the 4 defects
below are new, all mechanism-level.

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(pinned; same 4 pre-existing analyzer warnings, shifted line numbers).
Repaired source: `logic_fixed3.zag` (this dir, 1230 lines). Binary:
`logic_fixed3_bin`. **Nothing committed.**

## Result

- RT1c `corpus_a.tsv`: **11/11 hits corrected → 0 hits** (45/45 oracle-agree).
- RT1c `corpus_b.tsv`: **2/2 hits corrected → 0 hits** (49/49 oracle-agree).
- RT1c `corpus_d.tsv`: byte-identical to fixed2 binary (same 7
  informational disagreements D-001/D-002/D-005/D-008/D-009/D-010/D-012,
  no bar).
- Round-1 `rt_a.tsv`: 45/45. `rt_b.tsv`: 49 valid + RTB-041/042 NEUTRAL
  per retracted-VOID oracles (engine output byte-identical to fixed2).
- Round-2 `rt1b_A.tsv`: 44/45 — the single disagreement is A-044, a
  disclosed oracle conflict (see §4), not a mechanism regression.
  `rt1b_B.tsv`: 49/49.
- Frozen Track-G batteries: g_cau 20/20, g_cmp 20/20, g_con 19/20 (GC-03
  pre-existing, fixed2-identical), g_cond 19/20 + GD-19 disclosed oracle
  conflict (see §4), g_hedge 20/20, g_neg 20/20, g_qnt 20/20, g_tmp 20/20.
  K-MLOGIC 5/5, K-V3PROOF 3/3.
- 3× byte-identical runs (all corpora). Pure Zag, zero RNG (no rand/seed
  primitives; only comments mention "zero RNG"). Proof traces still
  emitted (new rule id `R-COND-MP-DENY`).

## 1. Mechanism diagnosis

### Fix 1 — hedged MP antecedent (RT-A, 2 hits)
`R-COND-MP` matched the antecedent by pure structural equality, so a
hedged `maybe(a)` "satisfied" `if(maybe(a), b)`, affirming `b` from an
antecedent the engine's own hedge doctrine says asserts nothing
(A-001; A-038 the double-hedged twin). The round-1 hedge guards covered
hedged *claims*; the *antecedent* side was unguarded.

### Fix 2 — nested vacuous reasons (RT-A 4 hits + 1 wrongful deny)
The vacuous-reason substance check inspected only the top-level reason
kind. A vacuous reason nested one level inside a `cause(...)` reason
(`cause(cause(not(a),b),q)`, A-002; `if`-reason A-003; `maybe`-reason
A-004; 3-deep A-008) passed as "substantive" and licensed affirmation —
the exact adversary shape the fix was meant to kill, one paren deeper.
Deny-side twin: `cause(cause(not(a),b),not(q))` wrongfully denied q
(A-007 anomaly).

### Fix 3 — self-contradictory temporal reasons (RT-A, 3 hits)
`before(x,x)` is necessarily false (the engine's own `r_tmp_deny` treats
x==y as degenerate), yet counted as a "substantive" reason licensing any
claim: `cause(before(x,x),q)` (A-005), `cause(all(d,before(d,d)),q)`
(A-006), `cause(some(d,before(d,d)),q)` (A-039), nested
`cause(cause(before(x,x),b),q)` (A-040). `after(x,x)` canonicalizes to
`before(x,x)`, so one check covers both surface forms.

### Fix 4 — deny asymmetries (RT-B, 2 hits)
`R-CAU-AFFIRM` establishes `cause(r,q) ⊢ q` and `R-COND-MP` establishes
`if(p,q);p ⊢ q`, but neither had a mirror deny: `not(q)` vs `cause(r,q)`
(B-030) and `not(q)` vs `if(p,q);p()` (B-031) withheld instead of denied —
the v3-failure shape (valid logic withheld).

## 2. The repairs (all in `logic_fixed3.zag`, pure Zag, general mechanisms)

1. **`reason_substantive(r, parts)`** (new, before `r_neg_deny`): recursive
   reason-substance predicate. `NOT`/`MAYBE`/`IF` → vacuous (asserts
   nothing positive); `BEFORE(x,x)` → vacuous (self-contradictory;
   covers `after(x,x)` via canonicalization); `CAUSE(r2,q2)` → recurse
   into the inner reason `r2`; `ALL/SOME/NONE(d, body)` → recurse into
   the body; atom/qty/temporal(x≠y) → substantive. `r_cau_affirm` and
   `r_cau_deny` both gate on it (replacing the top-level-only kind test).
   Slices are (ptr,len), so the shared `parts` scratch is safe to reuse
   across recursion.
2. **Hedged-antecedent gate in `mp_cond`** (new helper; driver MP block
   flattened into it, keeping else-nesting ≤ 4): the conditional's
   antecedent `aa` must satisfy `pkind(aa) != 8` — a hedged antecedent
   can never discharge the conditional (`maybe(maybe(a))` covered: pkind
   reads the outer constructor). Structural-equality matching otherwise
   unchanged.
3. **Mirror deny rules**:
   - `r_cau_deny` direction 2: claim `NOT(q)` vs `CAUSE(r, q)` (same
     substantive-reason gate) → DENY, reusing rule id `R-CAU-DENY`.
   - `mp_cond` returns 2 for claim `NOT(q)` where the evidence set
     derives `q` by MP (`IF(a,q)` + unhedged `a` present) → DENY, new
     rule id 11 `R-COND-MP-DENY`.
   Hedged claims stay inert (`pkind(ccan) != 8` loop guard; `is_not`
   never matches a `maybe` claim), and hedged antecedents cannot
   trigger the MP mirror either.

znc gotchas honored: no new indexed casts (byte indexing only), no slice
`==`, no `argc` gate, no `_zag_arg` frees, else-nesting ≤ 4 (MP logic
factored into `mp_cond`/`mp_find_ant` helpers), `return;` in void fns,
7-arg syscalls untouched, all slices far below 2^25.

## 3. Verification

### RT1c corpora (before → after; before = fixed2 binary)
| corpus | before | after | oracle-agree |
|---|---|---|---|
| corpus_a (45) | 11 hits (A-001..A-008, A-038, A-039, A-040) | **0 hits** | 45/45 |
| corpus_b (49) | 2 hits (B-030, B-031 NEUTRAL) | **0 hits** | 49/49 |
| corpus_d (16) | 7 informational | byte-identical | same 7, no bar |

Diff fixed2→fixed3 on RT1c-A is exactly the 11 intended lines (10
AFFIRM→NEUTRAL, A-007 DENY→NEUTRAL); on RT1c-B exactly the 2 intended
lines (NEUTRAL→DENY with `R-CAU-DENY` / `R-COND-MP-DENY` traces).

### Prior corpora + frozen batteries (regressions)
- `rt_a.tsv` 45/45; `rt_b.tsv` 49/49 valid (+ RTB-041/042 NEUTRAL per
  retracted-VOID oracles — fixed2-identical output).
- `rt1b_A.tsv` 44/45: A-044 explained below. `rt1b_B.tsv` 49/49.
  `rt1b_D.tsv` byte-identical to fixed2.
- Batteries: g_cau 20/20, g_cmp 20/20, g_con 19/20 (GC-03 pre-existing,
  fixed2-identical), g_cond 19/20 (GD-19 explained below), g_hedge 20/20,
  g_neg 20/20, g_qnt 20/20, g_tmp 20/20, mlogic 5/5, v3proof 3/3.

### General-mechanism probes (`runs/probes.tsv`)
- Hedged antecedents `if(maybe(a),b);maybe(a)`,
  `if(maybe(maybe(a)),b);maybe(maybe(a))`, `if(maybe(a),b);a()` → all
  NEUTRAL; clean `if(a,b);a()` → AFFIRM `R-COND-MP`.
- Nested vacuous (2-deep, 3-deep, `if`-reason) → NEUTRAL; substantive
  nested `cause(cause(rain(),wet(ground)),flood())` → AFFIRM;
  `cause(all(d,p(d)),q)` → AFFIRM (B-027/B-045 classes preserved).
- `cause(before(x,x),q)`, `cause(some(d,before(d,d)),q)` → NEUTRAL;
  `before(x,x)` ident → AFFIRM (RT1c-D-007 preserved);
  `cause(before(x,y),q)` → AFFIRM.
- Mirrors: `not(q())` vs `cause(r,q)` → DENY `R-CAU-DENY`; vs
  `if(p,q);p()` → DENY `R-COND-MP-DENY`; `maybe(q())` claim → NEUTRAL;
  `not(q())` vs `cause(not(r),q)` (vacuous reason) → NEUTRAL;
  `not(q())` vs `if(maybe(p),q);maybe(p)` (hedged antecedent) → NEUTRAL.

### Determinism (3× byte-identical)
| corpus | sha256 (all 3 runs) |
|---|---|
| rt_a | `d77dfe1d8a0c17b89e1bcfe6ff20f474e7a11ecb5f66ef95c25e343e704082d5` |
| rt_b | `a91571d76943f4d9fa11160e2e605f1e178b4acabdbb83eba39f6a5aeefda7d9` |
| rt1b_A | `38a9e5e3abd483a432bc18e32709e166977a854241a78996c155f105e42fda77` |
| rt1b_B | `9876bd6092faa8ebb4fc4c2532be1bc91fd35bf8c43acbff868537535d8121b7` |
| rt1c_a | `28fbe10a97f41bfc708b9cd6dea761269aa6cf98949aa67cdbb0424ba4efbb22` |
| rt1c_b | `353020e3431137296188673fc6fd9cab4821ab73b1e63a1150047debec97711f` |
| g_cau | `a58dd89b2820c1e08429861ab472663d03b5d1611d8a35ea62301cb9dae43b43` |

## 4. Oracle conflicts (disclosed, 2 items)

The general mirror-deny rules surface two stale oracles that contradict
the fresh RT1c oracles, the task's explicit general-fix order, and their
own corpora's affirm oracles:

- **rt1b A-044** (`not(q(x))` vs `cause(r(x),q(x))`, oracle NEUTRAL):
  engine now DENYs. rt1b's own B-026 (`q(x)` vs `cause(r(x),q(x))` →
  AFFIRM) establishes that this evidence proves `q(x)`; its direct
  negation cannot coherently withhold. Same shape as RT1c B-030 (DENY).
  The NEUTRAL label was the asymmetry the fresh attack caught.
- **battery GD-19** (`NOT(B())` vs `IF(A(),B());A()`, oracle NEUTRAL):
  engine now DENYs (`R-COND-MP-DENY`). The battery's own
  GD-03/GD-08/GD-10/GD-14 (`B()` vs `IF(A(),B());A()` → AFFIRM) establish
  that this evidence proves `B()`; GD-19's NEUTRAL encoded the old
  withhold behavior. Same shape as RT1c B-031 (DENY). Companion GD-20
  (`MAYBE(B())` claim) stays NEUTRAL — hedge inertness intact.

Both are oracle-label corrections of the same kind the RT1c attacker
disclosed for A-025/A-026/A-027. Frozen corpus files were NOT modified.

## 5. Provenance (SHA-256)

| Artifact | SHA-256 |
|---|---|
| repaired `logic_fixed3.zag` | `0a8b6c4c6694232fa48e4ed30cdcf63a8996e40eff2034c2717cca7555373ced` |
| fixed binary `logic_fixed3_bin` (pinned toolchain) | `6f59470c03129f4a4d20b72b7da3d232c5e26295476dfa021ca20c94082cec5c` |
| RT1c `corpus_a.tsv` | `a65e1cafee63a7c06684cf8635b8ad594e9976122262141df060677d2620fa00` |
| RT1c `corpus_b.tsv` | `b9efe41b66d27f5d38b23be72953d5bf34aee35f07345d905ba1659aaf74dc1b` |
| RT1c `corpus_d.tsv` | `4a8516f84e79bd604137f82a193e53b0610359a4756f80a7eca791f51791936f` |

## 6. Notes for the coordinator

- The round-2 `logic_fixed2.zag` and binary are untouched in `rt1fix2/`;
  this round's work is entirely in `redteam/rt1fix3/`.
- Judgment call: quantified-body recursion in `reason_substantive` treats
  `all(d,maybe(p(d)))` as a vacuous reason (no corpus/battery item covers
  it; principled extension of hedge inertness below the top level).
- `r_cau_prop_deny` deliberately untouched: it denies structural
  negations of a causal claim's components, not affirmations via
  vacuous reasons — no attack item implicated it.
- **Not committed**, per instructions. Ready for coordinator review /
  commit.
