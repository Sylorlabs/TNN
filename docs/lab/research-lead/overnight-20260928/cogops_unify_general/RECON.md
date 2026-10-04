# C500 RECON — the `strat_sel` family, verified
**Lane:** ARCHITECT-COMPRESSION / `arch/cogops-unify`
**Date:** 2026-10-03
**Status:** recon complete, independently re-derived. Several prior-recon claims
are CORRECTED below.

## 0. Frozen inputs, hashes

| file | lines | sha256 (12) |
|---|---|---|
| `cogops_learnosc2/c8_learn.zag` (frozen prefix) | 1331 | `750cb01d086f` |
| `cogops_rescueaware/c15_base.zag` (base arena) | 174 | `fc1f6e73c43a` |
| `cogops_optimistic/c12_world.zag` (world) | 594 | `46c6b0dc101f` |
| `cogops_rescueaware/c15_main.zag` (main) | 792 | `739ae60a21df` |

## 1. Claim 1 — "26 source files differ only in `strat_sel`" — PARTLY WRONG

`rg -l 'fn strat_sel'` over `overnight-20260928` (excluding this lane) returns
**41 files**, not 26. They decompose as:

* **14** `*_learn.zag` (the lane's assembled learner = 1331-line prefix + additive)
* **13** `*_strat_additive.zag` (the additive section alone)
* **14** `*_full.zag` (base + world + [world_add] + learn + main, the linked TU)

14 + 13 + 14 = **41**, across **12** directories. `c19pos` exists only as a
`_full.zag`; `cogops_transition_predict` holds only `c21h_learn.zag` (no
additive and no `_full` committed).

The `*_full.zag` and `*_strat_additive.zag` files are *not* independent lanes;
they are the same lane's build products. The independent lane count is
**15 named policies** (c10, c11, c12, c13, c14, c15, c16, c17, c18, c18h, c19,
c19h, c19pos, c20h, c21h), in **12 directories**.

### 1a. The frozen-prefix claim IS exact
`diff <(sed -n 1,1331p c8_learn.zag) <(sed -n 1,1331p F)` is **empty for all
14 `*_learn.zag`**. Verified. The 1331-line prefix is byte-identical everywhere.

### 1b. Not all lanes differ only in `strat_sel`
`base.zag` is byte-identical (`fc1f6e73c43a`) across all lanes, but
`world.zag` and `main.zag` are **not**:

| world sha12 | lanes |
|---|---|
| `3491343a8ab7` | c10 |
| `cdb79082cf68` | c11 |
| `46c6b0dc101f` | c12, c13, c14, c15, c16, c17 |
| `99a5f6f11fe6` | c18, c18h, c19, c19h, c19pos, c20h, c21h |

`main.zag` differs in **all 15** lanes (646–795 lines). So only the set
**{c12,c13,c14,c15,c16,c17}** is a clean single-variable family (same world,
same base). The later lanes changed the *apparatus* as well as the policy, so
their cross-lane SUMMARY differences are confounded. Prior recon did not
separate this.

## 2. Claim 2 — the ACTUAL set of distinct `strat_sel` bodies

SHA-256 (12) of the extracted function text, per file. **10 distinct bodies:**

| # | sha12 | lines | appears in | signature |
|---|---|---|---|---|
| B1 | `7e35f01ecf19` | 46 | c10 | global `st_`; argmax `w/u` raw; hedge |
| B2 | `623be2ab9b01` | 46 | c11 | global `st_`; argmax `w/cost` raw; hedge |
| B3 | `074096387722` | 42 | c12 | global `st_`; argmax `(w+1)/(c+1)`; hedge |
| B4 | `97496662e3e3` | 42 | c13 | per-context `cx_`; argmax `(w+1)/(c+1)`; hedge |
| B5 | `7f81c4d21631` | 42 | c14 | per-context; **argmin** `(c+2)/(u+2)`; hedge |
| B6 | `36a16c38d69f` | 53 | c15 | per-context; argmin `[(c+2)rb+(u−w+1)ra]/(u+2)`; hedge |
| B7 | `5d69516f1563` | 53 | c16, c18h | per-context; argmin `[(c+**8**)rb+(u−w+1)ra]/(u+2)`; hedge |
| B8 | `26e13db4f42b` | 30 | c17, c18, c19 | B7 **minus the whole hedge block** |
| B9 | `87ac71009638` | 61 | c19h, c19pos | B7 + 2 log-only `det_ev` calls |
| B10 | `679faae0565b` | 78 | c20h, c21h | B9 + log-only tie-mask `det_ev(12)` |

### 2a. Prior-recon header claims, checked one by one

* `c19 = c17` **CONFIRMED** — byte-identical (`26e13db4f42b`). So is `c18`.
* `c19h = c16 + log-only instrumentation` **HALF WRONG** — c19h is 61 lines vs
  c16's 53, and the 8 extra lines are `det_ev(10)` + `det_ev(11)`. But the
  *base* it instruments is B7, so the behavioural claim (log-only) is right;
  the recon's "c19h = c16 + ..." understated that c19h also inherits c16's
  `8`. Behaviourally c19h ≡ c16 + logging, which is what the lane's own
  `REPORT.md` claims. No contradiction with the frozen outputs.
* `c20h = c19h + tie mask` **CONFIRMED** — the 17 extra lines are the
  `det_ev(12)` tie mask, log-only.
* `c10 efficiency argmax (w+1)/(c+1)` **WRONG.** c10's code is
  `if(ln*rd>rn*ld)` on raw `w`/`u` with a zero-denominator clamp — **no `+1`
  smoothing at all**. c10 is argmax of the *unsmoothed* hit rate `w/u`, with
  `ld==0 → ld=1` (an untried strategy scores 0 and can never win).
* `c11 cost-aware argmax wins/cost` **CONFIRMED** (raw, unsmoothed).
* `c12 optimistic` **CONFIRMED** (`(w+1)/(c+1)`).
* `c14 expected-cost argmin (c+2)/(u+2)` **CONFIRMED**.
* `c15 rescue-aware, ledger 16680/16684**/16684**` **CONFIRMED**.
* `c16 pessimistic untried prior` — the *mechanism* is confirmed (larger cost
  prior `8`), but "pessimistic" is a **misnomer**: a larger `P` in
  `(c+P)rb + (u−w+1)ra` penalises the **untried** more, so c16 is the
  *optimistic-about-tried / pessimistic-about-untried* policy. It is the
  **exploration-hostile** one. The battery confirms this: at S14 c16 picks
  PW (`chosen=1`) where c15 picks WHOLE (`chosen=2`), and c16 never reaches
  ALT in S13.
* `c13 per-context tables` **CONFIRMED** — c13 is B3 with `st_` → `cx_`,
  nothing else.
* `c17 = c16 minus the hedge` **CONFIRMED exactly** (diff = the 22-line
  `if(tried==0){...}` block).

### 2b. The parametric decomposition (this is the real content)

Every one of the 10 bodies is an instantiation of **one** template with a
handful of integer constants and one accessor scope:

```
ra := L[16680] + 2      # global rescue turns   (LEARNED)
rb := L[16684] + 2      # global rescue loops   (LEARNED)
for s in 1..4:
    if ((tried >> s) & 1) == 0:                       # ADMISSION  (identical in all 10)
        (u,w,c) := T[slot,s]                          # SCOPE: global st_ | per-context cx_
        N := (c+P)*rb + (u-w+Q)*ra                    # NUMERATOR
        keep s*  iff  dir*( N*(u_s*+D) - N_s*(u+D) ) > 0   # COMPARE  (identical skeleton)
if tried==0 and exact-tie(s=1,s=3,s*): best := 4       # HEDGE
[optional log-only det_ev instrumentation]
return best
```

| body | scope | statistics | direction | P | Q | D | hedge | instr |
|---|---|---|---|---|---|---|---|---|
| B1 c10 | global | w,u | max | – | – | 1(raw) | yes | – |
| B2 c11 | global | w,c | max | – | – | 1(raw) | yes | – |
| B3 c12 | global | w,c | max | 1 | – | 1 | yes | – |
| B4 c13 | ctx | w,c | max | 1 | – | 1 | yes | – |
| B5 c14 | ctx | u,c | min | 2 | – | 2 | yes | – |
| B6 c15 | ctx | u,w,c | min | 2 | 1 | 2 | yes | – |
| B7 c16/c18h | ctx | u,w,c | min | 8 | 1 | 2 | yes | – |
| B8 c17/c18/c19 | ctx | u,w,c | min | 8 | 1 | 2 | **no** | – |
| B9 c19h/c19pos | ctx | u,w,c | min | 8 | 1 | 2 | yes | det10,11 |
| B10 c20h/c21h | ctx | u,w,c | min | 8 | 1 | 2 | yes | +det12 |

Two of the ten (B5, B6) are *degenerate instances of B7's own algebra*:
B5 = B7 with `ra:=0`; B6 = B7 with `P:=2`. The remaining spread is
`{scope} × {direction} × {which statistics} × P × Q × D × hedge × instr`.

**Key observation:** `ra` and `rb` — the coefficients that set the
cost:turn:rescue exchange rate — are already **learned from the learner's own
trajectory** (cells 16680/16684, filled by `rescue_finalize`). The
researcher-authored part is only `P`, `Q`, `D`, the direction, the statistic
subset, and the hedge. `P`, `Q`, `D` are **prior/offset constants about
unobserved quantities**; they are not read from any cell.

## 3. A NEW FINDING the prior recon missed: 3 of 14 battery stages do not
##    exercise `strat_sel` at all

`ref/main.zag` (c15 main, the one shared by the whole clean family) contains:

```
fn strat_lesion_s12(L,slot)  fn strat_lesion_s13(L,slot)  fn strat_lesion_s14(L,slot)
```

These **hand-write the (uses,wins,cost) table** for the context with 11–12
literal `set32` calls before the query. Stages **S12, S13, S14** therefore
test "does a researcher-chosen table produce the intended argmin?", not
"does the learner choose well?". The main file's own comment for S14 asserts
`"WHOLE untried is the STRICT expected-cost argmin (1.0 < 8/5 < 2.0 < 10/4)"` —
and the numbers it lists are the c14 form `(c+2)/(u+2)` for the S14 table,
while the c15 rescue-aware form on that same table selects WHOLE for a
different reason. The comment does not describe the code it ships with.

## 4. The controlled measurement, and its result

`mk.sh` assembles `base + world + frozen_prefix + <additive> + main`. Only the
additive varies. Rebuilt on this host with `--target macos-arm64`:

| variant | reproduces checked-in lane output |
|---|---|
| v15 (c15 additive) | **byte-identical** to `cogops_rescueaware/c15_run1.txt` |
| v16 (c16 additive) | **byte-identical** to `cogops_pessimistic/c16_run1.txt` |
| v17 (c17 additive) | **byte-identical** to `cogops_hedgeremoval/c17_run1.txt` |
| v13 (c13 additive) | identical except its own main omits the `RESCUE` dump line |
| v14 (c14 additive) | identical except its own main omits the `RESCUE` dump line |

So the family **is** re-verifiable on this macOS/arm64 host. Blocker **B13 is
false for the COGOPS `strat_sel` family** (see `PROBE_RAW_SYSCALL_INERT.md`
for the one toolchain adaptation required).

### 4a. THE RESULT: the capability metric is CONSTANT across the family

Same base, same world (`46c6b0dc101f`), same main (`739ae60a21df`), same
1331-line frozen prefix. **Only `strat_sel` varies.**

```
v13  (ctx argmax (w+1)/(c+1))   agree=1 plans_built=8 plans_loaded=4 trials=6 declines=0 prior=2
v14  (ctx argmin (c+2)/(u+2))   agree=1 plans_built=8 plans_loaded=4 trials=6 declines=0 prior=2
v15  (rescue-aware P=2)         agree=1 plans_built=8 plans_loaded=4 trials=6 declines=0 prior=2
v16  (rescue-aware P=8)         agree=1 plans_built=8 plans_loaded=4 trials=6 declines=0 prior=2
v17  (P=8, no hedge)            agree=1 plans_built=8 plans_loaded=4 trials=6 declines=0 prior=2
v18  (== v17, byte-identical)   agree=1 plans_built=8 plans_loaded=4 trials=6 declines=0 prior=2
```

**Six arithmetically distinct decision policies. One identical capability
score.** The policies differ only in the internal `DET-STRAT`/`DET-SWITCH`
trace and in the accumulated CTXT bookkeeping — and, per §3, the *only*
stages where the choice differs at all are S8 (hedge, learned table) and
S13/S14 (**researcher-lesioned** tables).

Full-trace divergence: v15 vs v16 differ on 11 lines; v15 vs v17 on 20 lines;
v13 vs v15 on 22 lines. **0 of those lines are in `SUMMARY-DET`.**
