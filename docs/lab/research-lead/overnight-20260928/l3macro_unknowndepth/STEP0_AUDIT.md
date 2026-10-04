# STEP 0 — FROZEN-CORE LOOP AUDIT + TWO CORRECTED PROVENANCE FINDINGS

Worker: L3-MACRO. Lane: `lane/l3macro`. Dir: `l3macro_unknowndepth/`.
Claim IDs: **C600** (Step-0 verdict), **C601** (deleted-evidence correction),
**C602** (CALR recovered + reclassified). C377-C466 untouched; C590/C591 belong to
`redteam/suf-audit`.

This file is committed **before** the prereg and before any implementation. It is
source reading only. No experiment has been run.

---

## 1. GATE C600: MACRO-OF-UNKNOWN-DEPTH IS DEAD ON ARRIVAL

**Verdict: DEAD.** Two independent fatal findings. The second is sufficient alone.

### 1.1 Finding A — the frozen core already contains general iterated-execution constructs

Subject: `docs/lab/research-lead/overnight-20260928/cogops_learnosc2/c8_learn.zag`,
1331 lines, sha256 `750cb01d086f0f4eeb29d0a8481e36941a7551396e5c514429a0dffc7aa4b4e8`
(matches brief §7).

| Construct | file:line | Nature |
|---|---|---|
| `execute_plan_iter` | `c8_learn.zag:994-1041` | change-driven worklist; runs needs in plan order, re-dirties link-successors when an output record changes |
| `topo_g` | `c8_learn.zag:804-861` | partial-order completion with stall repair — source comment `:802`: "Not cycle detection: it completes any partial order" |
| `osc_one_pass` / `osc_handle` | `c8_learn.zag:1218-1237` / `:1239-1331` | multi-pass loop with cycle-lag detection (`osc_review:1149`) and a stored response table (`outc_store:1176`, 3 entries) |
| `compose_iter` | `c8_learn.zag:1045-1071` | generalized entry point wrapping the above |

`execute_plan_iter`'s own header (`:988-993`) states the exit rule in prose:
"Halts on quiescence (a pass with no dirty need) or the pass CAP (16, frozen
totality bound)."

So the hypothesis "the learner emits its own LOOP / ITERATIVE MACRO" is, on this
core, **already implemented by the researcher**. This is `L3_CANDIDATE.md` §3.1's
own named killer ("the frozen COGOPS core already has `cycles_learned` and
`compose`; a repeat construct may already exist"), confirmed. One correction:
**`cycles_learned` does not exist** in the frozen prefix (`rg -n cycles
c8_learn.zag` → 0 hits). `L3_CANDIDATE.md` §3.1 names it in error. The
construct is real; the symbol name in the candidate doc is wrong.

### 1.2 Finding B — the emittable exit-condition set is four literals, all hardcoded, none learner-writable

This is the decisive one, and it is stronger than Finding A. Every iteration
construct above has its **exit condition written as a literal in the researcher's
source**. The complete set:

| # | Exit condition | file:line | Learner-writable? |
|---|---|---|---|
| 1 | `progressed==0` (quiescence) | `c8_learn.zag:1030` | **no** |
| 2 | `pass>=cap` where `cap:i32=16` | `c8_learn.zag:1003,1006` | **no** |
| 3 | `stall==0` (stall-repair fixpoint) | `c8_learn.zag:820` | **no** |
| 4 | cycle-lag recurrence (`traj_state_eq`) | `c8_learn.zag:1149-1155` | **no** |

Therefore **`F_exit = {quiescence, cap16, stall-repair, cycle-lag}` is enumerable
from source in four lines**, and — critically — `execute_plan_iter`'s signature
(`c8_learn.zag:994`, 16 parameters) contains **no argument, field, or slot through
which a learner could supply an exit condition**. There is no interface to fill.

This kills the hypothesis in the strongest available way, which is *not* the way
`L3_CANDIDATE.md` predicted. The candidate's `E1` falsifier said: "if the loop is
assembled by a generic re-execute-body-until-predicate call where the predicate is
a learned i32 comparison … the loop **is** a template with five slots and the
claim is **L2, dead**." That is right. But the actual situation is one notch
worse: **the frozen core does not merely supply the template, it supplies the
whole loop with the exit sealed shut.** The learner has *less* structural freedom
here than in C287, where at least a count `K` was a slot the learner filled.

Any design I build which has "the learner construct its own exit condition" is
therefore necessarily a **new interface I add myself** — which is exactly the act
that makes the result L2 (researcher-authored machinery). The hypothesis cannot be
reached by working within the frozen core, and cannot be reached by leaving it.

### 1.3 Finding B′ — the macro-form cells the frozen core already occupies

Generalising Finding A, the frozen COGOPS core already supplies every macro form
the assignment's hypothesis space names. Occupancy map, with `file:line`:

| Macro form | Occupied? | Evidence |
|---|---|---|
| iterate to quiescence (worklist fixpoint) | **YES** | `execute_plan_iter` `:994` |
| partial-order completion / stall repair | **YES** | `topo_g` `:804` |
| named, persisted, reusable procedure | **YES** | `plan_find/plan_new/plan_drop` `:570,:578,:1073`; `compose_iter` returns `1=loaded, 2=built` `:1066,:1070` |
| multi-pass with cycle detection + memoised response | **YES** | `osc_handle` `:1239`, `outc_store` `:1176` |
| list aggregation / fan-in | **YES** | `apply_kind3` `:429` |
| scalar propagation over a DAG | **YES** | `apply_kind1` `:399` |
| version-indexed relation selection | **YES** | `ret_version/vfy_version/cnt_version` `:286,:290,:302` |
| **learner-writable exit/termination predicate** | **NO — and no interface exists** | §1.2 |
| **learner-emitted new node kind / semantic rule** | **NO — vocabulary closed** | `l3_suf_intermediate/src/learner2.zag:387-395` hardcodes `kind∈{0,1,2}`; GPI-3 rejects anything else (`gpi3_learner.zag:597`) |
| **quantifier over a learned binding set** | partial, menu of 3 | `learn_bindings` `:527`, `fam<3` at `:536` |

**The two empty cells are both empty for an architectural reason, not an
empirical one.** The exit cell is sealed (§1.2); the new-node-kind cell is closed
by explicit kind guards. Neither can be entered by a learner acting alone. So the
"learner emits its own macro" hypothesis space is **exhausted at L2**.

## 2. C601 — CORRECTION TO THE PRIOR AUDIT'S DELETED-EVIDENCE FINDING (P1)

I independently re-derived the prior audit's P1. **The finding is TRUE. The
diagnosis is wrong, and the error runs in the direction that matters: the prior
audit declared evidence "never committed as source" that in fact existed and was
destroyed.**

`b3b3ee00a47e6be1c80e54bb00500e5450d75317`, subject:

> `lm3_lifetime: prereg (PREREG.md + NAMECHECK.md); frozen kill bars B1-B7 before
> implementation. Non-ledger.`

`git show --numstat b3b3ee00a`:

```
files=160517  added=234  deleted=44104446
```

**160,517 files and 44.1 million lines.** This is not a targeted deletion of two
directories; it is a whole-tree wipe carried by a commit whose subject claims to
be a preregistration of frozen kill bars. It deleted, among 160k others:

- `l3_repro_transfer/` — 44 files, incl. `orig_glm_learner.zag` (243),
  `orig_gl2m_h1.zag` (690), `orig_gl2m_h2.zag` (577), 9 run logs
- `l3_redteam/` — 7 versions v0..v6, each with `learner.zag`/`full.zag`/3 run logs
- `l3_novel_intermediate_v2/` — the **entire CALR implementation**, see §3
- plus `l3_delayed_stochastic` (656-line learner, 3× 220,714-line run logs),
  `l3_bridge_impl`, `l3_transfer_adapt`, `l2_l3_spec`, `l2_l3_trunc`,
  `l2_l3_adv`, `l2_l3_combo`, `composition_l3*`, `f2_ablation`, and the whole
  `.github/scripts/e51a*` workflow fleet

The commit is an ancestor of HEAD. **It has never been repaired.** Two sibling
events in the same 17 hours *were* noticed and repaired, which is why the pattern
is visible:

| Time (UTC) | Event | Repaired by |
|---|---|---|
| 2026-10-03 04:21 | `c721bcc61` — "WATCHDOG mass deletion", 160,348 files | `b688fa031` "GIT-REPAIR2" |
| 2026-10-03 19:38 | `169894404` — empty-tree commit | `cef8c4095` "REPAIR: restore full tree nuked by" |
| 2026-10-03 20:43 | **`b3b3ee00a` — 160,517 files, subject says "prereg"** | **none** |

**Correction to `SUF_AUDIT.md` §7 P1.** It attributes the loss of
`l3_repro_transfer/` and `l3_redteam/` to `b3b3ee00a` as though it were a
targeted deletion ("whose subject has nothing to do with them"). Corrected: it was
collateral damage of an unrepaired repo-wide wipe. The governance conclusion is
*stronger* than the prior audit's, not weaker — a single commit destroyed
44.1M lines including every L3 artifact and every published experiment, and the
recovery pattern that caught two sibling events missed this one because the
subject line reads as a routine preregistration.

## 3. C602 — THE CALR FAMILY: RECOVERED FROM SOURCE, AND WORSE THAN "NOT VERIFIABLE"

`SUF_AUDIT.md` §1 and boundary B-A1 state the `l3_niv2_*`/CALR family
(C350/358/364/367/391) has **no source in the repository**, on the basis of
`git ls-tree` at HEAD and at `cef8c4095`. **That is a false negative.** The
parent of `b3b3ee00a`, `4e7eb30b107b9a04ccf5f0f4bacc37f821718df0`, contains the
full implementation. I recovered and read it.

`SUF_AUDIT.md`'s *classification* of CALR as "beam/argmax search over an
enumerated candidate pool" is **CONFIRMED, and stronger than stated**. From
`l3_novel_intermediate_v2/impl/`:

**`isa.zag:1-13` — the emittable alphabet is C281's alphabet, verbatim:**

```
// Basis (frozen, recorded at code freeze): the C281-line 5-op register
// ISA already present in the learner lineage:
//   0=CPY, 1=ADD, 2=MUL, 3=SET1, 4=INC.
// Registers R0..R3. Instruction = 3 bytes (op,d,s). Program = flat
// instruction sequence, max 64 instructions.
// ZERO new opcodes, ZERO new semantic cases.
```

So **CALR's `F` is exactly the same 80-instruction alphabet that
`SUF_AUDIT.md` §3.1 used to kill C281/C284 to L1** (5 ops × 4 dst × 4 src), with
a length cap of 64 and **zero added semantics**. The search over it:

- `lm_cons.zag:79` — pool cap `if(pn>=32768){ return -1; }` → 32768. Matches ledger.
- `lm_cons.zag:243` — `// gen_appends: generate all 80 append children`
- `lm_cons.zag:269` — `// gen_substs: 80 substitute-last children`
- `lm_cons2.zag:185` — `select_beam`, `:129` `beam_level`, `:42` `sel_better`,
  `:92` `cand_cmp`: score-stratified, then length, then lexicographic tie-break
  (`:101-110`), then id (`:111`). Textbook argmax over an enumerated pool.

**Classification: L1, not "NOT VERIFIABLE."** The prior audit recorded CALR as
"cannot be audited further to know that [it is not L3]" — correct as far as it
went, but it reached that conclusion from ledger prose when the source was
recoverable and would have settled it in three lines. C350/358/364/367/391 are
**L1**: enumeration of 80 instructions plus an argmax with a lexicographic
tie-break, on an alphabet the same audit had already condemned. The audit's
"absent ⇒ not adjudicable ⇒ no accusation" discipline was sound as a rule and
cost it the one family where the answer was available.

I take no position on whether C350's *authors* misdescribed it; that needs the
lane's own reports, which exist in the same recovered tree
(`REPORT.md`, `REPORT_WAVE3.md`, `REPORT_WAVE4.md`) and were not read here.

## 4. Method, and what this audit is NOT

- Source reading of `c8_learn.zag`, `l3_suf_intermediate/src/`,
  `l3_novel_intermediate_v2/impl/` (recovered at `4e7eb30b1`), plus `git log`
  forensics. No experiment was run; no audited mechanism was re-executed.
- I did **not** verify any digest, determinism claim, or PASS/FAIL verdict.
- **B-0a** the Step-0 verdict is about `cogops_learnosc2/c8_learn.zag` as frozen
  at `750cb01d086f`. A core that added a learner-writable exit slot would reopen
  the hypothesis; no such core exists in this checkout.
- **B-0b** §1.3's occupancy map covers the macro-form cells this assignment
  named. It is not a proof that no L3 construct exists in any language.
- **B-0c** §3 reads `isa.zag` and the search structure only. I did not run CALR
  or check its results.