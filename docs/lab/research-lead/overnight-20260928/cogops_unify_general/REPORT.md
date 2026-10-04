# C506 REPORT — COGOPS-UNIFY-GENERAL
**Lane:** ARCHITECT-COMPRESSION · branch `arch/cogops-unify` · 2026-10-03
**VERDICT: NEGATIVE (H0). The `strat_sel` family is NOT unifiable, and the
reason is provable rather than a matter of taste. `26 → 1` is nevertheless
reachable — but only by DELETION, not by unification, and the deletion is
justified only for byte-identical duplicates.**

---

## 1. STATUS

| item | result |
|---|---|
| Prereg (C502) | committed alone before any UGEN code |
| Recon (C500) | 35 files / 15 lanes / **10** distinct bodies, not 26 / 26 |
| Toolchain (C501) | `_zag_raw_syscall` inert; B13 **false** for this family |
| UGEN built (C503) | yes, pure Zag, **0 modes**, determinism 3/3 |
| Ablation (C504) | yes — **fails to move any learner-owned metric** |
| M1 dead-mode ledger | 10 bodies, 4 provable duplicate groups |
| M2 parameter grid | **324/324 cells, 1 capability score** |
| M3 contradiction witness | **found, machine-logged** |
| M4 ablation | **FAILS on every clean split** |
| H1 (unification) | **REFUTED** |
| H0-a (pointwise contradiction) | **PROVEN** |
| H0-b (no gradient) | **PROVEN** |

---

## 2. COMMITS

1. `05826b235` — C501 toolchain finding + C502 frozen prereg + C500 recon.
   (Committed alone, before implementation.)
2. this commit — C503 UGEN, C504 ablation, C505 deletion ledger, C506 report,
   plus the 324-cell grid and the SS-state probe logs.

---

## 3. RESULTS

### 3.1 Mode count

| unit | count |
|---|---|
| files in the repo containing `fn strat_sel` | **35** (recon said 26) |
| named lanes | **15** (c10,11,12,13,14,15,16,17,18,18h,19,19h,19pos,20h,21h) |
| directories | 12 |
| **distinct `strat_sel` bodies** | **10** |
| **distinct additive sections** | **10** (c16 ≡ c18h, byte-identical) |
| distinct templates | **1** (one scoring loop, 5 dimensions) |
| **after UGEN** | **1** |

Four lane groups are byte-identical duplicates, so 15 → 10 lanes is a
provable, zero-risk deletion:

| sha12 | lanes |
|---|---|
| `26e13db4f42b` | c17, c18, c19 |
| `5d69516f1563` | c16, c18h |
| `87ac71009638` | c19h, c19pos |
| `679faae0565b` | c20h, c21h |

### 3.2 LOC

| | lines |
|---|---|
| 10 distinct `strat_sel` bodies, summed | **463** |
| 10 distinct additive sections, summed | **5777** |
| one representative additive (c15) | 624 |
| **UGEN additive (whole section)** | **646** |
| — of which the UGEN mechanism (`ugen_*` + `strat_sel`) | **107** |
| — of which shared with c15 (unchanged driver machinery) | 539 |

Kill bar **B4** as written ("fewer lines than the *sum* of the incumbents")
passes trivially (646 < 5777). Against the honest single-incumbent
baseline it **fails**: UGEN's section is 22 lines *longer* than c15's. The
mechanism itself (107 lines) is shorter than the 463 lines of bodies it
replaces, but it is not shorter than any one of them plus its ctors.

### 3.3 Capability retention — and why it is vacuous

```
                 capability score                                turns  wins  cost  rescueT  lesionedCost  learnedCost
v13 (w+1)/(c+1)  agree=1 plans=8 loaded=4 trials=6 dec=0 prior=2    29    15    86     38/9         --           --
v14 (c+2)/(u+2)  agree=1 plans=8 loaded=4 trials=6 dec=0 prior=2    30    15    86      0/0         --           --
v15 rescue P=2   agree=1 plans=8 loaded=4 trials=6 dec=0 prior=2    29    15    84     38/9          9           54
v16 rescue P=8   agree=1 plans=8 loaded=4 trials=6 dec=0 prior=2    29    15    86     37/9         11           54
v17 P=8 no hedge agree=1 plans=8 loaded=4 trials=6 dec=0 prior=2    29    15    86     43/11        11           56
UGEN    (C503)   agree=1 plans=8 loaded=4 trials=6 dec=0 prior=2    29    15    90     47/11        15           56
ABLATE  (C504)   agree=1 plans=8 loaded=4 trials=6 dec=0 prior=2    30    15    92     51/12        17           56
```

* **B2 (match or beat the best incumbent)**: on the *declared* capability
  score, UGEN **ties** (everything ties). On the only metric with variance —
  comparisons spent — UGEN **loses**: 90 vs the grid optimum 84. **B2 FAILS.**
* **B3 (no regression of the worst)**: UGEN 90 > every incumbent (84–86).
  **B3 FAILS.**
* **B1 determinism**: `ugen`, `abl`, `v15`, `v16`, `v17` all **3/3
  byte-identical**. PASS.
* **B5 zero new modes**: UGEN has no mode selector, no config table, no
  per-regime constant, no `if` that selects a scoring form, and no literal in
  `{1,2,8}` used as a prior or offset. Every coefficient is a cell. PASS on
  the letter — see §4 for why this does not rescue H1.

### 3.4 M2 — the grid (H0-b, PROVEN)

`P∈{0,1,2,3,4,6,8,12,16} × Q∈{0,1,2} × D∈{1,2,3} × {min,max} ×
{hedge on,off}` = **324 cells**, all built, 0 failures, against the frozen
base / world / main / 1331-line prefix.

| metric | distinct values over 324 cells |
|---|---|
| **capability score** (`agree`,`plans_built`,`plans_loaded`,`trials`,`declines`,`prior`) | **1** |
| **wins** | **1** (15) |
| turns | 2 (29, 30) |
| comparisons spent, total | 7 (84,86,88,90,91,92,93) |
| **comparisons spent on LEARNED stages S1–S11** | **1 (54)** |
| comparisons spent on LESIONED stages S12–S14 | 9 values (9…17) |

**The capability score is a constant of the apparatus.** Every arithmetically
distinct decision policy scores identically. There is no gradient, therefore
no estimation procedure over learner state can identify `P`, `Q` or `D` —
they are not *parameters of a learnable family*, they are free choices.

The 34 grid cells that reach the optimum (cost 84) span `P ∈ {0,…,8}` with
`Q`, `D` arbitrary, and **every optimum cell appears in a hedge-on/hedge-off
pair with identical cost**. The hedge — the sole feature the c17/c19 lane
was created to ablate — has **zero** effect on any metric.

### 3.5 M3 — the contradiction witness (H0-a, PROVEN)

An SS-state probe (`probe/ss_probe.zag`) logs, at **every** `strat_sel`
call, the complete vector of learner-state cells `strat_sel` reads plus the
value it returns. `strat_sel` reads no other cell.

29 calls per run. Comparing c15's log with c16's log call by call:

* 26/29 calls: **identical input vector**, identical output.
* **1 call: identical input vector, DIFFERENT output.**

```
SS tried=0 slot=3 rt=35 rc=8 1:3,2,6 2:0,0,0 3:2,0,8 4:0,0,0 -> best=2   (c15)
SS tried=0 slot=3 rt=35 rc=8 1:3,2,6 2:0,0,0 3:2,0,8 4:0,0,0 -> best=1   (c16)
```

Same 11 integers in, different integer out. **No single-valued function of
learner state can be both c15 and c16.** This is a machine-checked proof,
not an argument. `probe/ss_probe.zag` is re-runnable; the logs are
`out/ss15.ss`, `out/ss16.ss`.

Worse (for the family): that single disagreement occurs at stage **S13**,
whose table is not learned. It is written cell-by-cell by
`strat_lesion_s13` in `main.zag`. Kill bar **B7** applies: the only point at
which the family's policies are not extensionally equal is inside a
researcher-authored fixture.

### 3.6 M4 — the ablation (FAILS)

`ablate/inc_abl.zag` keeps every learner-owned structure and every update
(CTXT tables, rescue ledger 16680/16684, UGEN ledger 17600–17608, DET ring,
lag prior) and destroys only the credit assignment: selection degenerates to
the lowest admissible strategy id.

| split | UGEN | ablated | drop? |
|---|---|---|---|
| capability score | 1/8/4/6/0/2 | 1/8/4/6/0/2 | **NO** |
| comparisons, learned stages S1–S11 | 56 | **56** | **NO** |
| comparisons, S8 (the only learned stage that moves at all) | 8 | **8** | **NO** |
| comparisons, lesioned stages S12–S14 | 15 | 17 | yes, but researcher-authored |
| total comparisons | 71 | 73 | +2.8% |

Per-stage, UGEN and the ablation are **identical on every learned stage**.
The unified mechanism has **zero** effect on any learner-owned measurement.
Preregistered prediction **P5 confirmed**: removing the mechanism drops the
trace but not the capability — and it turns out not to drop the trace either,
on the part of the trace the learner owns.

UGEN's entire deficit against c15 is one learned stage, **S8** (8 vs 6
comparisons): S8 is the stage whose whole purpose is to test the
tie-to-ALT hedge. UGEN has no hedge — by design, one fewer mode — and pays
2 comparisons for it. Every other learned stage is identical.

---

## 4. WHY B5 PASSING DOES NOT RESCUE H1

UGEN satisfies every syntactic requirement the mission set: one mechanism,
zero modes, zero per-regime constants, every coefficient read from a cell,
the alternation strategy competing on the same terms as the rest with no
special case, and the hedge block deleted outright. It is a *real*
generalisation of the incumbents — c15 is literally the specialisation in
which the learned price vector happens to equal `(rb, ra)` on the
cost/failure coordinates. c15's `ra = rt+2`, `rb = rc+2` were already
learned from the learner's own rescue ledger; UGEN just learns the other two
coordinates the same way and stops special-casing the first two.

And it still cannot be identified, for two independent reasons:

1. **It is not the only mechanism that ties.** So is a constant `(P,Q,D)`
   picked from the 34 optimum cells. So is the ablation, which contains no
   mechanism at all. A tie against a constant baseline is not evidence, and
   the grid proves the baseline is constant.
2. **The family's members contradict each other on a pinned state.** Even a
   perfect mechanism could not be consistent with all 10, because two of them
   demand different answers from the same 11 integers.

The honest statement is therefore: **UGEN demonstrates that one general
mechanism is *sufficient* for the family's declared capability. It does not
demonstrate that the family is *one policy*, because the family has never
been shown to be a family — the apparatus cannot tell its members apart.**

---

## 5. THE COMPRESSION THAT IS ACTUALLY AVAILABLE

`26 → 1` in the recon's framing is not a real number. The real numbers are
**35 files → 10 bodies → 1 template**, and the reductions split cleanly:

**UNCONDITIONAL (provable, zero capability cost):**
* 35 files → 15 lanes → **10 distinct bodies**. Four duplicate groups
  (`26e13db4f42b`, `5d69516f1563`, `87ac71009638`, `679faae0565b`) can be
  deleted outright; they are the same bytes in a different directory.
* The 10 additive sections share a ~460-line driver tail. What differs
  between c13/c14/c15/c16/c17 is **32 to 145 lines** each (mostly the
  header comment). c10/c11/c12 differ by ~230 because they use global `st_`
  tables instead of per-context `cx_` ones — a scope choice, not a policy.

**CONDITIONAL, and I do not recommend it:**
* Collapsing 10 → 1 requires accepting that "capability" means the declared
  score, which §3.4 proves is constant. Under that reading the collapse is
  free — and equally meaningless. Under the only metric with variance
  (comparisons spent) the 10 bodies span 84…93, **11%**, and the ordering is
  set by constants no amount of learning can recover from this apparatus.
* Killing the hedge costs 2 comparisons on S8 and nothing else. That is the
  one real, small, defensible win in the whole exercise, and it comes from
  **deleting a mode**, not from unifying ten.

**THE REAL DEBT, WHICH IS NOT IN `strat_sel` AT ALL:**
* Stages **S12, S13, S14** do not exercise `strat_sel`. `main.zag` calls
  `strat_lesion_s12/s13/s14`, which hand-write the (uses,wins,cost) table
  with 11–12 literal `set32` calls before the query. Those three stages
  produce **100% of the measurable difference between all 10 policies** and
  **100% of UGEN's deficit against c15 on the lesioned split**. Every policy
  scores identically on the 8 stages the learner actually drives.
* `main.zag`'s comment on S14 asserts `"WHOLE untried is the STRICT
  expected-cost argmin (1.0 < 8/5 < 2.0 < 10/4)"` — the numbers it lists are
  the **c14** form `(c+2)/(u+2)` evaluated on the S14 table, and they do not
  support the conclusion drawn from them. The comment does not describe the
  code it ships with.
* The four "strategies" themselves (1=PW, 2=WHOLE, 3=NEED, 4=ALT) are four
  researcher-written procedures. **That** is the cognitive-mode menu. The
  scoring function was never where the menu was.

---

## 6. BOUNDARIES — what this does NOT show

1. **Does not show the family is irreducibly distinct in principle.** It shows
   the family is *not identifiable from this battery*. A battery in which
   strategy choice changes outcomes could identify it. This battery does not.
2. **Does not evaluate c10, c11, c12, c18, c18h, c19, c19h, c19pos, c20h,
   c21h** on the controlled apparatus: they ship different worlds
   (`3491343a`, `cdb79082`, `99a5f6f1`) and different mains, so their SUMMARY
   differences are confounded with the apparatus. Only their `strat_sel`
   bytes were analysed.
3. **The single-variant axis held fixed is the score template.** The scope
   axis (global `st_` vs per-context `cx_`) and the direction axis
   (`argmax` success-per-cost vs `argmin` cost-per-use) were swept only
   inside the per-context family; c10–c12's global-scope variants were not
   re-run under the frozen world because their mains do not link.
4. **S13's contradictory state is a lesion.** H0-a would be a much stronger
   result if the witness lay on a learner-generated table. It does not.
   Where the learner generates the table (S1–S11), **all 10 bodies are
   extensionally equal** — 54 comparisons each, identical `wins`.
5. **`o_flush` was substituted** (§C501). Provenance of that substitution is
   the byte-identity of the c15 rebuild against the checked-in Linux output.
   If a future toolchain restores `_zag_raw_syscall`, the substitution should
   be reverted and the results re-run.
6. **Single seed, single world.** `mk.sh` uses one world and one main. No
   cross-validation.

---

## 7. NEXT EXPERIMENT

The productive question is **not** "can 10 scoring functions be unified?" —
that question is closed, and it was never the interesting one. It is:

> **N1. Does strategy choice change anything at all, on a battery where the
> strategy tables are never written by hand?**
> Delete `strat_lesion_s12/s13/s14` from a copy of `main.zag` and rerun the
> 324-cell grid. Registered prediction: the capability score stays at 1 value
> (it already does) **and the learned-stage comparison count stays at 54 for
> all 324 cells** — because it already does for all 10 bodies. If it does,
> the entire COGOPS strategy-selection apparatus is *inert* on this battery,
> and the correct next claim is not about scoring functions at all.
> Kill bar: if learned-stage cost varies over the grid once the lesions are
> gone, my §5 conclusion is wrong and I will say so.

> **N2. Give the choice a consequence.** Until the cost of a strategy choice
> is visible in a metric the researcher did not enumerate, no policy — unified
> or not — can be selected for. Concretely: make `plans_built`, `trials` or
> `declines` sensitive to strategy choice (e.g. by removing the
> `SPECCHK`/`AGREE` shortcuts that currently make every strategy succeed), and
> re-run the grid. Only then does H0-b become falsifiable and H1 becomes worth
> building.

> **N3. Attack the real menu.** The four detection strategies are
> researcher-written procedures selected by index. Per the central negative
> result in the worker brief (§9: *"an L3 claim is only credible if the NOVEL
> FORM ITSELF is not enumerable from source"*), selecting among four
> researcher-written strategies is C285's "MENU SELECTION over 5 ops". Any
> unification credit for collapsing the scoring functions should be **refused**
> until the strategy *forms* are learner-generated.

> **N4. Cheap.** Delete the four byte-identical duplicate lanes
> (c18, c19, c19pos, c21h) from the tree. 15 → 11 lanes, zero risk, and it
> stops the next worker from re-counting them as separate modes.

---

## 8. FILE INVENTORY (all inside `cogops_unify_general/`)

| file | what |
|---|---|
| `RECON.md` | C500 recon + corrections to the prior recon |
| `PREREG.md` | C502 frozen prereg, bars B1–B7, predictions P1–P5 |
| `PROBE_RAW_SYSCALL_INERT.md` | C501 toolchain finding |
| `REPORT.md` | this file (C506) |
| `mk.sh` / `mk2.sh` | build+run harness (single-variable assembly) |
| `gen.sh` | M2 grid generator |
| `det.sh` | B1 determinism (file-sink form) |
| `sum.sh` / `stagecost.sh` | metric extraction, learned/lesioned split |
| `ref/` | frozen fixtures + the 9 reference additives |
| `ugen/inc_ugen.zag` | C503 the unified mechanism |
| `ablate/inc_abl.zag` | C504 the ablation |
| `probe/ss_probe.zag` | M3 SS-state probe |
| `out/M2_grid.txt` | 324-cell grid, capability score per cell |
| `out/M2_efficiency.txt` | 324-cell grid, all metrics per cell |
| `out/ss15.ss`, `out/ss16.ss` | M3 witness logs |
| `out/*.txt` | per-variant full outputs |
