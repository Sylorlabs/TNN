# C516 REPORT — COGOPS-LESION: adversarial re-test of the C506 NEGATIVE result
**Lane:** COGOPS-LESION · branch `lane/cogopslesion` · worktree
`/Users/Shared/micah/Documents/TNN/.worktrees/cogopslesion` · 2026-10-03
**Target:** `arch/cogops-unify` @ `1356c6434` — C502 prereg, C503 UGEN,
C504 ablation, C506 **NEGATIVE**: the `strat_sel` family is NOT unifiable.

**VERDICT: C506's VERDICT STANDS. One of its supporting CLAIMS is refuted by
its own preregistered experiment, and it rested on a stage-ordering error.
Its central recommendation — that the real violation is the four
researcher-written strategy FORMS, and that unification credit must be
refused until the forms are learner-generated — is CONFIRMED and is now
quantified rather than asserted.**

---

## 1. STATUS

| item | result |
|---|---|
| Prereg (C510) | committed ALONE before any lesion-deletion build |
| Counts (C511) | 41 / 15 / 12 / **10** all CONFIRMED; **one LOC figure refuted** |
| B13 (C512) | reproduced independently via the brief's `_zag_print` shim |
| Lesion grid (C513) | 648 builds, 0 failures, all 3/3 deterministic, non-empty |
| **Kill bar** | **FIRED** — C506 §5's {54,56}-collapse prediction is FALSE |
| C506 §5 verdict | survives, on a narrower and better-supported basis |
| Forms (C514) | 225 LOC of FORM vs 53 LOC of selector; menu is **total** |
| H-alt (C515) | not distinguishable from H0 on this battery |

## 2. COMMITS

1. `8e6e70ea3` — C510 prereg, alone. Frozen fixtures, bars K0–K3, predictions
   P1–P6, C506's kill bar verbatim, H-alt registered without a solution.
2. `887e42d72` — the pure-Zag instruments (`bodycount`, `metrics`, `formcount`).
3. `4db4d2714` — C514 enumeration test (`menum`).
4. `84c8e56e2` — C511/C512/C513 results + all 648 cell outputs under `data/`.
5. this commit — C516 report.

## 3. RESULTS

### 3.1 C511 — counts: confirmed, with one correction

`tools/bodycount.zag` extracts each `fn strat_sel` body by brace matching and
decides distinctness by **byte equality**, never by hash, so a collision cannot
hide a body.

```
files=41  policy names=15  directories=12  distinct bodies=10
```

All of C506's corrected counts confirmed. The four byte-identical duplicate
groups are confirmed by byte equality: `{c17,c18,c19}`, `{c16,c18h}`,
`{c19h,c19pos}`, `{c20h,c21h}`.

**Correction to C506 §3.2: the distinct-body LOC sum is 493, not 463.**
Per-body line counts: `30,53,46,42,61,78,42,42,53,46` → **493**. C502's kill
bar B4 quoted 493 correctly; REPORT §3.2 transposed it. 463 is wrong.

### 3.2 C512 — B13 reproduced independently

Two probes, both pure Zag, in this lane, using the brief §4.0 shim rather than
C501's `_zag_write_file` substitution:

* `_zag_raw_syscall(1,1,ptr,3,0,0,0)` on a 3-byte `"OK\n"` buffer emits **zero
  bytes**. Inert, confirmed. C501 says it returns a negative value; brief §4.0
  says rc=0. **It returns 0 here** — the brief is right about the rc, C501 is
  wrong about it. Both agree it writes nothing, which is the part that matters.
* **K0 satisfied.** `mk.sh ref/inc_c15.zag v15` reproduces
  `cogops_rescueaware/c15_run1.txt` **byte-for-byte**
  (`d9feba834bfbc6f1…`, 8986 bytes). v16 and v17 likewise reproduce their
  checked-in Linux outputs.

Barrier **B16** ("silent miscompilation of indexed reads") is **not
reproduced**: a 648-file pure-Zag reduction with heavy indexed access into flat
byte arenas produced exact counts on every cell once my own offset bug was
fixed. B16 stays doubted, now on a second independent body of evidence.

### 3.3 C513 — the lesion-deletion grid: the kill bar FIRES

One variable: `main.zag` vs `main_nolesion.zag`, which differs by exactly
**3 lines** — the three `strat_lesion_s1x(L,ctx_of_goal(L,G));` call sites
replaced by comments. Grid cell `(8,1,2,min,on)` asserted byte-identical to
`ref/inc_c16.zag` before the sweep.

| metric | L (lesioned, C506's grid) | NL (lesions deleted) |
|---|---|---|
| **capability score** | **1** value | **1** value |
| | `agree=1 plans=8 loaded=4 trials=6 declines=0 prior=2` | identical |
| **LEARNED_CMP (S1–S11)** | **2** values `{54,56}` | **2** values `{54,56}` |
| — hedge=on (162 cells) | 1 value `{54}` | 1 value `{54}` |
| — hedge=off (162 cells) | 2 values; 73@54, 89@56 | 2 values; **73@54, 89@56** |
| TOTAL_CMP | 8 values, 63…73 | 8 values, 63…74 |
| S12–S14 comparisons | 7 values, 9…18 (2×) | 6 values, 9,11,13,15,16,18 |

**C506's kill bar, verbatim: "if learner-stage cost still varies over the grid
once the lesions are gone, my §5 conclusion is wrong and I will say so."**

`LEARNED_CMP` still takes 2 values. **The bar fires. C506 §5's claim that
lesion deletion collapses `{54,56}` to a single value is FALSE.** I am
reporting that as its author required.

**The refutation is narrower than the bar's wording, and the reason is
measurable.** The `{54,56}` split is *bit-identical* between the two mains —
same 162 hedge=on cells all at 54, same 73/89 split at hedge=off — and it
lives **entirely inside the hedge=off half**. Under hedge=on, all 162 NL cells
sit at 54 with zero variation.

Root cause, and it is a defect in C506's N1 rather than in its verdict:
**S1–S11 execute before S12–S14 in `main.zag`.** Deleting a S12–S14 fixture
cannot change a S1–S11 measurement, because the learner-stage cost had
already been spent by the time the lesions are written. The `{54,56}` range was
never downstream of the lesions. No edit to the lesions could have collapsed it,
so N1's registered prediction was not achievable.

What lesion deletion *does* do, now measured: it makes S12–S14 run against
learner-generated tables instead of rigged ones, and those three stages get
**more** expensive (NL dominated by 13/15/16 where L was dominated by 11/13) —
the expected sign when the learner must work from its own evidence. And **P3
is confirmed**: capability score is single-valued across all 648 builds, so the
lesions were never load-bearing for capability.

**C506's secondary prediction is confirmed and is now a measurement:**
with the lesions gone, the entire learner-owned dynamic range over all 324
cells is **2 comparisons in 54 (3.7%), produced solely by the
researcher-authored tie-to-ALT hedge.**

### 3.4 C514 — where the researcher cognition actually lives

Brace-matched LOC, verified against the file (`strat_sel` = lines 193…245 = 53
lines, matching C506's independent count):

| unit | LOC |
|---|---|
| `strat_sel` — the selector | **53** |
| `pw_try` 32 · `pw_propose` 26 · `who_try` 32 · `who_turn` 24 · `need_try` 61 · `need_turn` 24 | **199** |
| the hand-written `s==1..s==4` dispatch inside `det_handle` | **26** |
| **FORM total vs selector** | **225 / 53 = 4.25×** |

**P5 falsified as I wrote it.** I predicted FORM/SEL > 5; measured 3.75 on
form bodies alone, 4.25 including the dispatch. "The menu dwarfs the selector"
survives; my threshold did not. The real number is above.

**The menu is TOTAL — this is the load-bearing result.** In `ref/inc_c15.zag`:
`if(s==1){` … `if(s==4){` each occur **exactly once**; `if(s==5){` and
`if(s==6){` occur **zero times**; `strat_sel`'s admission loop is `while(s<5)`
and it `return best`. So the id set the learner can ever name is `{1,2,3,4}` and
each has exactly one hand-written body. No unreachable arm, and no syntax by
which a fifth form could enter.

**The form space is enumerable and largely already enumerated.** Over the axes
the four incumbents actually vary, all visible as source literals:

```
A compare predicate   whole-state eq | per-need eq      (2)
B hypothesis rule     non-empty mask | need must change  (2)
C lag schedule        ordered subset of {1,2,3}          (7)
D quiescence rule     lag==1 is fixpoint | no rule        (2)
E pass advance        1 pass | 2 passes                   (2)
|A x B x C x D x E| = 112 forms;  incumbents occupy 4;  108 unoccupied
```

The 108 are reachable by recombining researcher-written primitives, so under
brief §9 none of them clears L3 either.

**Shape is literal, not learned — the answer to "what would it take".** The
decisions determining what a form *does* (not how it scores) are
`while(bi<4)`×1, `while(d<4)`×2, `if(lagp==1)`×1, `return 3`×1, `nadv=2`×1.
Every one is an integer **literal**. **Zero** of them read a learner cell. The
cells the forms do read are bookkeeping only (15900, 15904, 16650, 16680/16684,
16688/16692, 17000+slot). Not one selects a form.

**Honest reachability verdict.** With zero learner-owned shape parameters and a
total 4-arm dispatch, there is no quantity a learner could estimate that would
move the choice of form. The form choice is not *under*-learned; it is **not
parameterised at all**. Bridging it needs a substrate where a procedure is
representable as data the learner constructs and mutates. Per brief §2 this
language has no arrays, structs, closures, generics, or dynamic code; records
are byte-offset conventions over a flat arena, so a form is expressible only as
source text only the researcher writes. **That is a substrate limit, not an
experiment result**, and I state it as such rather than proposing a workaround.

### 3.5 C515 — competing hypothesis H-alt

C506's H0-a is a correct theorem about the **SS projection** (the cells
`strat_sel` reads). But the disagreement it certifies is specifically about the
**cost prior of an untried strategy**: c15 assumes `P+2` turns, c16 assumes
`P+8`. So the one extra learner-owned quantity a unifying mechanism would need
is an estimate, derived from the learner's own trajectory, of the turn-cost an
untried strategy is expected to incur — the analogue of cells 16680/16684 for
the *first* turn rather than the rescue turn. **No such ledger exists.** That is
the named gap. I am not filling it.

**Fairness clause, applied:** H-alt is a rescue only if testable on this
battery. It is not. Both discriminators came back negative for it — capability
score single-valued across all 648 builds, and the only learner-owned dynamic
range is 2 comparisons in 54 with the lesions deleted. **With no gradient there
is nothing to fit an untried-cost prior to.** H-alt is therefore
**indistinguishable from H0 on this apparatus**, and I say so rather than
treating it as a live alternative.

## 4. WHAT C506 GOT RIGHT AND WRONG

| C506 claim | this lane |
|---|---|
| Family not identifiable from this battery (H0-b) | **CONFIRMED** — 648 builds, 1 capability value |
| Pointwise contradiction over SS (H0-a) | **CONFIRMED as a theorem**, but it is a statement about a chosen projection, not about unifiability in principle |
| 41 files / 15 lanes / 12 dirs / 10 bodies | **CONFIRMED** |
| distinct bodies sum to 463 LOC | **REFUTED — 493** |
| The 4 forms are the real violation, not the scoring function | **CONFIRMED and quantified**: 225 vs 53 LOC; menu is total |
| N1: lesion deletion collapses {54,56} | **REFUTED** — impossible by stage ordering |
| N1 secondary: hedge is the entire remaining range | **CONFIRMED** |
| Recommendation: refuse unification credit until forms are learner-generated | **CONFIRMED**, and shown to require a substrate change |

## 5. BOUNDARIES

1. **Single battery, single world, single seed.** No cross-validation. The
   negative result is *for this apparatus*, which is the boundary C506 drew and
   the only one I can support.
2. **The 41-file count is over one corpus subtree** (`overnight-20260928`,
   excluding this lane). A repo-wide `rg` was not run.
3. **The kill bar fired on a claim, not on the verdict.** C506 §5's *mechanism*
   claim ("the 2× range lives in the lesions") is confirmed; its *N1
   prediction* about collapsing `{54,56}` is refuted. I have not shown the
   verdict is wrong, and I am not claiming it is.
4. **The form-space count 112 is an enumeration I chose**, over the five axes
   the incumbents demonstrably vary. A different axis set gives a different
   number. The *totality* result (4 arms, `while(s<5)`) does not depend on it.
5. **P5's threshold failed.** I report 4.25×, not the >5 I predicted.
6. **`_zag_print` shim**, per brief §4.0. If a future toolchain restores
   `_zag_raw_syscall`, revert and re-run.
7. **H-alt is untested, not refuted.** It is untestable on a battery with no
   gradient; that is a statement about the battery.
8. **Toolchain, for the next worker.** B16 not reproduced. But I hit four real
   traps, all mine, none compiler faults: `get32/set32` take **byte** offsets
   (I passed element indices, producing plausible garbage); a `z_alloc`'d
   needle carries **trailing NUL** padding so `find` cannot match it unless
   sliced exactly; building a search needle by byte assignment **silently
   corrupts** it (`t[7]=48+1` did not land), so use string literals; and a
   string-slicing parser that is correct in a small test can drift in a large
   one — prefer index arithmetic over parsing when the enumeration order is
   known.

## 6. NEXT EXPERIMENT

> **N1' — make the hedge's cost visible, or stop.** The entire learner-owned
> dynamic range in the whole family is 2 comparisons in 54, and it is produced
> by one researcher-authored tie-break. Either delete the hedge permanently and
> record that the apparatus then has **zero** learner-owned policy range — at
> which point the strategy-selection machinery is provably inert and should be
> removed rather than unified — or build the battery N2 asks for, where
> strategy choice changes `plans_built` / `trials` / `declines`. Do not spend
> more effort on scoring functions; there is nothing there.

> **N2' — attack the menu, but first settle reachability.** Before proposing
> any form-generation experiment, answer on paper: *what in this substrate
> could a learner mutate that would change which form runs?* My measurement
> says the answer is "nothing that exists today." If the honest answer is
> "a code-writing substrate must be built first," that is a substrate project,
> not a cognition experiment, and should be scoped as one.

> **N3' — cheap, do it now.** Delete the four byte-identical duplicate lanes
> (c18, c19, c19pos, c21h). 15 → 11 lanes, provably zero capability cost, and
> it stops the next worker re-counting them as modes. Confirm with
> `tools/bodycount.zag`, which already identifies them by byte equality.

> **N4' — correct the ledger.** C506 §3.2's `463` must become `493` in
> `cogops_unify_general/REPORT.md`, and N1's prediction there should be
> annotated as stage-ordering-infeasible rather than left standing as a live
> prediction.

## 7. FILE INVENTORY (`cogopslesion/`)

| file | what |
|---|---|
| `PREREG.md` | C510: frozen fixtures, bars K0–K3, predictions P1–P6 |
| `mk.sh` | the one build path; asserts non-empty output (K3) |
| `gen.sh` | the 648-build grid; asserts the c16 roundtrip |
| `FILES.txt` | the 41 `strat_sel` paths |
| `ref/base_orig.zag` | `c15_base.zag`, untouched |
| `ref/base.zag` | the above, **one line** changed to the `_zag_print` shim |
| `ref/main.zag` | `c15_main.zag`, **unmodified** |
| `ref/main_nolesion.zag` | **3 lines** changed — the lesion call sites |
| `ref/inc_c1*.zag`, `ref/tmpl.zag` | reference additives; the grid template |
| `tools/bodycount.zag` | C511 — distinctness by byte equality |
| `tools/metrics.zag` | C513 — per-stage and capability counts |
| `tools/aggregate.zag` | C513 — grid reduction + the kill-bar verdict line |
| `tools/attribute.zag`, `tools/attrib2.zag` | C513 — axis attribution |
| `tools/dump.zag` | C513 — per-cell table (the citable one) |
| `tools/formcount.zag` | C514 — brace-matched LOC accounting |
| `tools/menum.zag` | C514 — dispatch totality + form-space size |
| `data/` | all 648 cell outputs |
| `out/dump.txt`, `out/formcount.txt`, `out/gen.log` | measurements |