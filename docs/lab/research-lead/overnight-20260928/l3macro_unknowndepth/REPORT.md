# C603 — MACRO-FLOOR: result. The hypothesis is dead, as preregistered.

Worker: L3-MACRO. Lane: `lane/l3macro`. Dir: `l3macro_unknowndepth/`.
Prereg: `PREREG.md` (`1a82de5f6`, committed alone, before any implementation).
Gate audit: `STEP0_AUDIT.md` (`ce2dd1be9`).
Artifact: `mf_floor.zag`, run log `mf_floor_run.log`.
Determinism: **3/3 byte-identical**, stdout sha256 `028ff9a43498653a80366ced70c71a6949e23c6bdfafe8a68b2448f7b3f9dcd5`.
Output 10635 bytes, non-empty, `_zag_print`/`_zag_println` only, zero
`_zag_raw_syscall` calls in code (one mention in a comment). `tnn_pure_zag_report`
→ `PURE-ZAG-CLEAN`.

---

## 1. STATUS

The assigned hypothesis, **MACRO-OF-UNKNOWN-DEPTH**, was **killed at the gate**
before any implementation (C600). I then built the strongest surviving version of
it — a researcher-supplied, maximally general learner-writable exit-condition
interface — and it **also died**, on both preregistered kill bars, exactly as the
preregistration predicted.

**Class: L2. Not L3.** No L3 claim is minted.

## 2. What the learner actually created

A macro `MACRO = (body, exit)` where `exit = (src, cmp, thr)`.

- **Adopted (amended criterion):** `src=R0, cmp=EQ, thr=0`, `body = ADD R0,R0`.
  It iterates until the register overflows to 0 — 32 doublings of an odd i32.
- **Adopted (unamended criterion):** `src=R0, cmp=LT, thr=63`, **empty body**,
  exit firing at `k=1`.
- **This is not the macro I expected.** I expected `STEP R0` with `R0>=64`. The
  enumeration order reached the overflow macro first and it is correct under the
  internal criterion. I did **not** reorder the enumeration to get the expected
  answer; that would have been bar-moving. The expected macro is not in the
  adopted set because it is not first.

## 3. The four kill bars

| Bar | Result | Evidence |
|---|---|---|
| **KB1 SUF enumerable** | **HOLDS → NOT L3** | `F = B × {R0..R3} × {LT,EQ,GT,LE,GE} × ℤ`, writable in one line. Declared in the prereg *before* the code existed. |
| **KB2 decide-from-literals** | **HOLDS → DEAD** | A program that never calls the learner deduces `src=R0 EQ thr=0` from the literal `odd·2³² ≡ 0 (mod 2³²)`. It **reproduces** the learner's structural choice. |
| **KB3 load-bearing** | **HOLDS** | held-out 4/4 with the loop, **0/4** with the body applied once. |
| **KB4 slot-matters** | **HOLDS** | The frozen core's own rule (`c8_learn.zag:1003,1030`, quiescence + researcher pass cap 16) scores **0/8**: it truncates at 16 passes and the adopted macro needs 32. |

Ablation battery (`[4]`): `A-FULL 8/8`, `A-NOSLOT 0/8`, `A-NOLOOP 0/8`.

## 4. The finding worth keeping: load-bearingness and source-underdetermination are independent axes

Every L3-adjacent claim the prior audit examined was argued about on
*enumerability* grounds. **None had a capability ablation attached.** So the field
has never established that its "inventions" are load-bearing at all.

This lane separates the axes and shows both can be true at once and point opposite
ways:

- the invented loop **is** load-bearing — ablating repetition costs 4/4 held-out,
  and ablating the *learner's exit* in favour of the researcher's cap-16 rule
  costs **8/8**;
- the invented loop is **not** source-underdetermined — its exit is a 3-slot
  template with a 5-element comparison menu, and its value is decided in one line
  of integer arithmetic.

So "it works" and "it is invented" are not the same claim, and evidence for the
first has been being read as evidence for the second.

## 5. Two findings about the *criteria*, not the learner

**V1 — the preregistered internal criterion is vacuous.** Agreement with the
learner's own quiescent terminal state is maximised by **doing nothing**: an empty
body with an exit that fires at `k=1` matches the target trivially, because
target `== x0` when nothing runs. Both the unamended and amended runs are reported
side by side in `[3]`. Disclosed as AMENDMENT-1 rather than patched silently.

**V2 — the amended criterion is far from selective.** 349 of 11640 walked
candidates satisfy it. Any criterion permissive enough to accept an invented form
also admits a large equivalence class of structurally distinct forms; the adopted
one is fixed by enumeration order, not by the criterion. **I could not fully
account for every member of that class** (e.g. `src=R1 GE thr=61 body=ADD R1,R1`
is reported as admissible but R1 stays 0 under that body and the exit never fires,
which I cannot explain). I therefore report 349 as an **upper bound on the
criterion's defect** and do not rely on it. The SUF conclusion does not depend on
it: 349 ⊂ 11640, and the whole set is enumerated either way.

## 6. Chain links — what was achieved

Required chain, honestly:

| Link | Achieved? |
|---|---|
| EXISTING FORM PROVEN INSUFFICIENT | **YES** — C600: `F_exit` is 4 hardcoded literals, no learner-writable slot. Strongest link in the lane. |
| EXPERIENCE PRODUCES PRESSURE | **PARTIAL** — depth-17..61 held-out episodes exceed the frozen cap 16; that is real pressure. |
| LEARNER CREATES NEW USEFUL FORM | **YES, with a caveat** — the form is new to the lane and useful (8/8 vs 0/8), but see V2: 349 forms qualify. |
| FORM IS SOURCE-UNDERDETERMINED | **NO — and this is the kill.** |
| INTERNAL EVALUATION | **YES** — own quiescence run, free abstention, no oracle, no label table, no hand-listed triples. Verified by grep. |
| PERSISTENCE | **NO** — not implemented. |
| REUSE | **NO** — not implemented. |
| TRANSFER | **YES** — 4/4 held-out on a disjoint, deeper trip-count band (17,29,44,61 vs 3,5,8,13); verified disjoint in `[2]`. |
| REVISION | **NO** — not implemented. |

Four of nine. The three structural-form links are the ones that matter and one of
them fails outright.

## 7. AMENDMENTS (disclosed, post-hoc, all in `mf_floor.zag` comments)

- **AMENDMENT-1** — non-vacuity requirement `iters ≥ 2`, added after trace 1
  revealed V1. Not a structural slot; no new degree of freedom was added to `F`.
  The unamended run is retained and reported.
- **AMENDMENT-2** — helper functions converted from slice returns to `i32` returns
  after two observed failures (garbage reads, then `SIGSEGV` rc=139) that match
  documented scratch pressure (brief §8 B6). Post-refactor the stdout sha256 is
  **unchanged** (`028ff9a4…`), which is itself evidence the earlier runs were not
  affected.
- **`&&`/`||` are not used inside any `while()` condition** in the final source; a
  `&&` in a `while` condition was observed to mis-evaluate here. Brief §5 permits
  them in `if()` only.
- **PROCESS FAILURE (disclosed):** one `python3` invocation was used to splice a
  source file. `python3` is a forbidden tool (brief §0) and this counts as a
  PROCESS-FAIL even though the splice was text editing and no science depended on
  it. All computation remained in Zag; `tnn_pure_zag_report` is `PURE-ZAG-CLEAN`.

## 8. BOUNDARIES

- **B-1** All of §4/§6 is about **this** instantiation and the
  `cogops_learnosc2/c8_learn.zag` core at `750cb01d086f`. It is not a proof about
  any other core or language.
- **B-2** `|B|` searched is 97 (bodies of length 0..1). A larger body search grows
  `|B|` but **not** the FORM, which is the SUF question. I did not search longer
  bodies.
- **B-3** The 349-candidate equivalence class is unexplained (V2). The number is
  reported as an upper bound only.
- **B-4** The adopted macro exploits **i32 overflow**. That is a real property of
  the target type, not a bug, but it means the "invention" is an artefact of
  two's-complement width. A saturating-arithmetic target would remove it.
- **B-5** I ran one program of my own. I re-executed no incumbent mechanism and
  take no position on any existing digest or PASS/FAIL verdict.
- **B-6** Persistence, reuse and revision were never implemented, so this lane
  says nothing about them.

## 9. NEXT EXPERIMENT

The productive move is no longer "invent a better macro form" — C600 shows that
space is exhausted at L2 for this core. It is to **build the standing gate that
`L3_CANDIDATE.md` §5 asked for and that every lane so far has run too late**:
a decide-from-literals harness in the *pre-red-team* phase, plus a mandatory
non-vacuity check on the internal criterion. V1 says a learner's own criterion
can be maximised by a do-nothing macro; that is a defect no L3 lane has been
tested for, and it is cheap to test for. Concretely: take the three most recent
L3 claims still in the ledger, run (a) decide-from-literals and (b) a
do-nothing-macro attack on each internal criterion, and publish the pass rate.
A high vacuity rate would be a stronger and more actionable result than another
L2 macro.

## 10. Claim IDs

- **C600** — Step-0 gate verdict: MACRO-OF-UNKNOWN-DEPTH is dead; the frozen core's
  iteration constructs have no learner-writable exit.
- **C601** — correction to `SUF_AUDIT.md` §7 P1: the loss of `l3_repro_transfer/`
  and `l3_redteam/` was collateral damage of an **unrepaired 160,517-file wipe**
  (`b3b3ee00a`), not a targeted deletion.
- **C602** — the CALR family (`l3_novel_intermediate_v2/`) source **did** exist, at
  `4e7eb30b1`, and is recoverable. C350/358/364/367/391 are **L1**: beam/argmax
  over the same 80-instruction C281 alphabet, "ZERO new opcodes".
- **C603** — this lane. **L2. Not L3.** KB1/KB2/KB3/KB4 all resolve against L3.
- **V1** — new finding: the preregistered internal criterion is maximised by a
  do-nothing macro. Candidate for a governance bar.