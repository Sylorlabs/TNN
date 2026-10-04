# C510 PREREG — COGOPS-LESION (adversarial re-test of C506 NEGATIVE)
**Lane:** COGOPS-LESION, branch `lane/cogopslesion`, worktree
`/Users/Shared/micah/Documents/TNN/.worktrees/cogopslesion`
**Frozen:** 2026-10-03, BEFORE the lesion-deletion grid or any form-count
instrument is built. Committed alone.
**Target under test:** `arch/cogops-unify` @ `1356c6434` — C502 prereg,
C503 UGEN, C504 ablation, C505 deletion ledger, C506 NEGATIVE verdict.
**Claim ids reserved:** C510 (this prereg), C511 (count verification),
C512 (B13/toolchain reproduction), C513 (lesion-deletion grid),
C514 (form quantification), C515 (competing hypothesis), C516 (verdict).

## 0. STANCE

C506 is a published NEGATIVE result. My job is to try to **break** it, not to
confirm it. I adopt its own preregistered next experiment (its N1) and its
own kill bar verbatim, and I add one hypothesis it did not test. Both
outcomes are reportable. I will not weaken a bar after seeing data.

## 1. FROZEN FIXTURES (copied into this lane; no existing lane is modified)

| fixture | provenance | sha256 (16) |
|---|---|---|
| `ref/base_orig.zag` | `cogops_rescueaware/c15_base.zag`, 174 lines | `fc1f6e73c43a...` |
| `ref/base.zag` | the above, **one line** changed: `o_flush` body `_zag_raw_syscall(...)` -> `_zag_print(b[0..c])` | see `out/` |
| `ref/world.zag` | `cogops_unify_general/ref/world.zag` = `c12_world.zag` | `46c6b0dc101f85ab` |
| `ref/frozen_prefix.zag` | `c8_learn.zag` lines 1..1331, byte-identical | `750cb01d086f0f4e` |
| `ref/main.zag` | `c15_main.zag`, 792 lines, **unmodified** | `739ae60a21df3b99` |
| `ref/main_nolesion.zag` | `ref/main.zag` with **3 lines** replaced by comments: the three `strat_lesion_s1x(L,ctx_of_goal(L,G));` call sites at lines 736/753/768. The three lesion FUNCTIONS are left defined but never called. That is the whole edit. | see `out/` |
| `ref/inc_c1*.zag` | the 9 reference additives of C500 | see `out/` |

**The independent variable in every build is the additive section only.**
`mk.sh <additive> <tag> [main]` is the only build path; it is fixed now.

**Reference point frozen BEFORE the grid:** `mk.sh ref/inc_c15.zag v15` with
`ref/main.zag` MUST reproduce `cogops_rescueaware/c15_run1.txt`
(sha256 `d9feba834bfbc6f1f047c5dedfcea5cad0315169b82fbfdb4df00ceae221480c`,
8986 bytes) byte-for-byte. This is the **C512 / B13 reproduction check** and
it is a kill bar (K0), not a formality.

## 2. KILL BARS (frozen; not to be moved)

**K0 — corpus reproducibility / B13.** `mk.sh ref/inc_c15.zag v15` output ==
`cogops_rescueaware/c15_run1.txt` byte-for-byte, on this host, with the
single-line `_zag_print` shim. *Fail ⇒ the whole lane is void; C501/C506 §4.1
is false and I report that instead.*

**K1 — determinism.** Every artefact this lane builds is
`zbuild.sh --rep 3` clean: 3/3 byte-identical stdout, **and** stdout is
**NON-EMPTY** (asserted explicitly; an empty log is a hard fail, per brief
§4.0 silent-success mode). *Fail ⇒ kill.*

**K2 — pure Zag.** Every number in every report of this lane is computed by a
Zag translation unit. Shell is used only to concatenate fixtures, invoke
`znc`/`zbuild.sh`, move files, and run `git`. *Any computation done in awk,
python, perl, or any other interpreter ⇒ PROCESS-FAIL, results uncitable.*

**K3 — non-empty output assertion.** Each build must produce ≥ 1 byte and
≥ 1 line of stdout. Asserted in `mk.sh` for every cell.

## 3. WHAT I AM TESTING

### 3.1 C511 — independent verification of the corrected counts

C506 §3.1 claims, correcting its own earlier 35:
**41 files** contain `fn strat_sel`; **15** named lanes; **12** directories;
**10** distinct `strat_sel` bodies; the 10 bodies total **463** LOC; one
additive section is **624** LOC.

*Method (pure Zag):* a Zag tool reads each of the 41 files named in
`FILES.txt`, extracts the `fn strat_sel` body by brace matching from the
`fn strat_sel(` line to its closing `}` at column 0, and writes a 32-bit
FNV-1a hash of the extracted bytes plus its line count. Distinctness is
decided by **byte equality of the extracted bodies**, not by the hash; the
hash is only a label. Both are reported so a hash collision cannot hide a
distinct body.

*Prediction P1:* 41 files, 15 lanes, 12 dirs, **10** distinct bodies, LOC
sum 463, per-body LOC multiset `{46,46,42,42,42,53,53,30,61,78}`.

*Kill bar:* if the distinct-body count is not 10, or the file count is not
41, C500/C506 §3.1 is wrong and I say so with the corrected number. I do not
assume their number.

### 3.2 C512 — B13 / `_zag_raw_syscall` inertness, re-verified myself

Two probes, both pure Zag, both in this lane:
* **B1.** A 3-byte buffer `"OK\n"` written with
  `_zag_raw_syscall(1,1,_zag_slice_ptr(b),3,0,0,0)` between two
  `_zag_println` markers. *Prediction:* no `OK` appears.
* **B2.** The K0 reference-point rebuild above.

I report the return value of the raw syscall as well, since C501 says it
returns negative while brief §4.0 says it returns rc=0. Whichever is true is
true; I measure it.

### 3.3 C513 — THE LESION-DELETION GRID (C506's own N1)

**The one variable:** `ref/main.zag` vs `ref/main_nolesion.zag`. Everything
else frozen. The grid is C500's grid, unchanged:

`P ∈ {0,1,2,3,4,6,8,12,16}` (9) × `Q ∈ {0,1,2}` (3) × `D ∈ {1,2,3}` (3) ×
`{min,max}` (2) × `{hedge on,off}` (2) = **324 cells**, per main. Two mains
= 648 builds.

**Prediction P2 (C506's, verbatim):** with the lesions deleted, the
learner-stage comparison count collapses from `{54,56}` to a **single value**,
leaving the hedge as the entire remaining dynamic range.

**KILL BAR (C506's, verbatim):** *"if learner-stage cost still varies over the
grid once the lesions are gone, my §5 conclusion is wrong and I will say so."*
Mapped to a number: if, under `ref/main_nolesion.zag`, the per-cell
comparisons-charged-to-cell-16650 total over the 8 learner-driven stages
S1–S11 takes **more than one distinct value** across the 324 cells, then
**C506 §5 is WRONG and I report H0-b as refuted.** Note this bar is stated on
the *learner-stage* metric specifically; a surviving range confined to the
lesioned split would not trip it, but under the no-lesion main the lesioned
split no longer exists as a separate construct, so all 14 stages are learner
stages and the whole-run comparison total is the operative number.

**Secondary prediction P3 (C506's):** with lesions gone, the capability score
`agree/plans_built/plans_loaded/trials/declines/prior` is still single-valued
across all 324 cells. *If it is NOT single-valued, the lesions were
load-bearing for capability, C506 §5's "the scoring function is not where the
cognition lives" is WRONG, and I report that.*

**Prediction P4 (mine, not C506's):** the no-lesion main makes S12/S13/S14 run
against whatever tables the learner has actually built, so I predict those
three stages will produce **more** strategy switches, not fewer, and that the
whole-run comparison total will be **higher** than the lesioned main's. If the
lesion-deletion main produces *lower* whole-run cost than the lesioned main,
that is a surprise and I report it.

### 3.4 C514 — WHERE THE RESEARCHER COGNITION ACTUALLY LIVES

C506's sharpest claim is not about scoring functions. It is: *"the one-system
violation is the four researcher-written strategies (PW/WHOLE/NEED/ALT)
selected by index — i.e. MENU SELECTION."* That claim is currently
**asserted, not measured.** I measure it. Pure-Zag LOC accounting over
`ref/inc_c15.zag` and `ref/main.zag`, with the line ranges identified by
brace matching from each `fn` header, not by hand:

* **M-A.** LOC of each of the four strategy FORMS' implementations
  (`pw_try`+`pw_propose`, `who_try`+`who_turn`, `need_try`+`need_turn`, and
  the `s==4` alternation block inside `det_handle`). Sum = FORM_LOC.
* **M-B.** LOC of `strat_sel` itself = SEL_LOC.
* **M-C.** **Ratio FORM_LOC / SEL_LOC.** This is the number that decides
  where the researcher cognition is. *Prediction P5:* FORM_LOC/SEL_LOC > 5,
  i.e. the menu is more than five times the size of the selector that picks
  from it. C506 argues the scoring function is the wrong place to look; this
  quantifies by how much.
* **M-D.** The **enumeration test** for "is a form enumerable from source":
  count how many of the four forms are *reachable by a finite syntactic
  enumeration* over the strategy-slot alphabet `{1,2,3,4}`. Answer, stated in
  advance: **all four**, because the dispatch in `det_handle` is literally
  `if(s==1){...} if(s==2){...} if(s==3){...} if(s==4){...}` — a total,
  exhaustive, hand-written enumeration of the entire menu. A form that can be
  enumerated from source in 4 cases cannot be a learner-generated form; it is
  a lookup. I will quote the dispatch line numbers as the evidence.
* **M-E.** What would it take for the learner to generate a form rather than
  select one? Stated as a measurement of the substrate, not as a proposal:
  count the **free parameters** a form would need (which cells are read to
  decide the *shape* of a proposal, as opposed to its score). Answer in
  advance: **zero.** Every shape decision in `pw_propose`/`who_turn`/
  `need_turn` — which lags to sweep (`d=2..3`), whether to suppress the prior
  duplicate, whether `lagp==1` returns quiescence `3` — is a **literal in the
  source**, not a cell read. I will count the literals. If that count is > 0,
  the menu is not learner-parameterised at all and the L3 bar cannot be met
  by tuning this apparatus.
* **M-F.** Honest reachability verdict: state whether learner-generated form
  generation is reachable in THIS substrate at all, given §2 of the worker
  brief (no arrays, no structs, no closures, no dynamic code, no
  self-modifying memory; "records" are byte-offset conventions over a flat
  arena). I expect the answer to be *not without a code-writing substrate*,
  and I will say so plainly rather than proposing a workaround.

### 3.5 C515 — COMPETING HYPOTHESIS: richer learner state

C506's H0-a is a pointwise contradiction **over SS-state**, where SS-state is
the vector of cells `strat_sel` reads. That is a real theorem. But it is a
theorem about a *chosen* projection, and a projection can always be enlarged.

*Competing hypothesis H-alt:* the family IS unifiable by a single-valued
function of a **richer, still learner-owned** state — specifically a state
that includes the *per-slot training history* that distinguishes the S13
contradicting cell from its neighbours. The contradiction witness is at
`tried=0 slot=3 rt=35 rc=8` with a table `1:3,2,6 2:0,0,0 3:2,0,8 4:0,0,0`.
Under SS those cells are identical for c15 and c16; the only thing that
differs is the **prior constant** `P` (2 vs 8) baked into the source.

*What H-alt requires, stated WITHOUT writing the solution:* the contradiction
is a disagreement about **the cost of an UNTRIED strategy**. c15 assumes an
untried strategy costs `P+2` turns; c16 assumes `P+8`. So a unifying
mechanism needs one more learner-owned quantity: **an estimate, derived from
the learner's own trajectory, of the turn-cost an untried strategy is
expected to incur** — i.e. a prior over first-turn cost learned the way
`ra`/`rb` already are (cells 16680/16684 are the learner's own rescue
ledger; the analogous untried-cost ledger does not exist). I am naming the
MISSING STATE, not supplying it. Whether it can be *identified* from this
battery is a separate question, and P2/P3 bear on it directly.

*Fairness clause:* H-alt is a rescue only if it is testable on this battery.
If P2 holds (capability single-valued, learner-stage cost single-valued), then
H-alt is **not distinguishable from H0 on this apparatus**, and I will say
exactly that: the negative result stands *for this battery*, not in principle.
If P2 FAILS, then there IS a gradient, H-alt becomes worth building, and I
say so. Either way I do not build it — this lane measures, it does not rescue.

## 4. FROZEN PREDICTION TABLE

| id | prediction | if false |
|---|---|---|
| P1 | 41 files / 15 lanes / 12 dirs / 10 distinct bodies / 463 LOC / per-body `{46,46,42,42,42,53,53,30,61,78}` | report corrected counts |
| P2 | no-lesion learner-stage comparison count is SINGLE-VALUED over 324 cells | **KILL C506 §5 / H0-b. Report refuted.** |
| P3 | no-lesion capability score single-valued over 324 cells | report lesions were load-bearing; §5 wrong |
| P4 | no-lesion whole-run comparison total > lesioned whole-run total | report the surprise |
| P5 | FORM_LOC / SEL_LOC > 5 | report the real ratio |
| P6 | `_zag_raw_syscall` write emits 0 bytes; c15 rebuild byte-identical to checked-in Linux output | K0 void |

## 5. WHAT I WILL NOT DO

* I will not modify any existing `cogops_*` lane, any file outside
  `cogopslesion/`, or `arch/cogops-unify`. My worktree is private.
* I will not `git checkout` in the main repo. Never `git commit -a`.
* I will not weaken, re-scope, or reinterpret K0/K1/K2/K3 or the C506 kill
  bar after seeing data. If P2 fails I report C506 §5 as refuted.
* I will not build H-alt. I name the missing state and stop.
* I will not claim any L3 credit for anything measured here. Per brief §9,
  selecting among researcher-written forms is C285's "MENU SELECTION" and is
  explicitly not L3.
* I will not treat a tie against a constant baseline as evidence. C506's §4
  reasoning about vacuous retention applies to my own results too.
## 6. FROZEN FIXTURE HASHES (recorded at prereg time)

| file | sha256 |
|---|---|
| `FILES.txt` (41 paths) | `30bd9d67bc579ac28d2ac0b1b1fb63c4be0fc1c2545d55a98d894646b4c83f72` |
| `ref/base_orig.zag` | `fc1f6e73c43ae8e4ea2b7af50f1606cc4b6c5353992bd5d4411cb4c9a3b73e61` |
| `ref/base.zag` (1-line shim) | `37087f4376d2e0a4ca156c7263eb0710eb7d0a11fa13b5d4db251526ff1bf1bf` |
| `ref/main.zag` (unmodified) | `739ae60a21df3b994c6bd3c0f82e11d615740fc57a301132929b5eba381b7460` |
| `ref/main_nolesion.zag` (3 lines) | `ffadbe9262f06f6ed67211b4bc4871fc27de59ced37c217803571fd87d87338f` |
| `ref/world.zag` | `46c6b0dc101f85ab...` |
| `ref/frozen_prefix.zag` | `750cb01d086f0f4e...` |
| `out/v15.txt` (K0 artefact) | `d9feba834bfbc6f1f047c5dedfcea5cad0315169b82fbfdb4df00ceae221480c` = `cogops_rescueaware/c15_run1.txt` |

K0 is satisfied **at prereg time** on the lesioned main. The no-lesion main is
built only after this file is committed.
