# REPRODUCIBILITY MANIFEST — provenance of legacy results

**Date:** 2026-10-05 · **Binaries NOT purged · history NOT rewritten**

## Why

This lane carries **344 extension-less committed binaries** (`*_bin`, `bp_bin`, `c5_bin`, …)
beside their sources. A committed binary cannot be rebuilt on another platform and
silently shadows the source next to it. That is not hypothetical: in `p6struct`, a failed
compile was followed by a run of the old binary, and I read its output as results.

Per standing instruction the binaries are **retained**. Instead every source is classified
by what can actually back it.

## Classes

| class | meaning | canonical? |
|---|---|---|
| **A** | compiles AND runs exit 0 under the build-run gate | yes |
| **B** | compiles, non-zero exit | provisional |
| **F** | fragment/template — not standalone source, build documented | provisional |
| **E** | has `main` but the compiler rejects it — **dead claim** | **NO** |
| **C** | binary with no recoverable source (344 files) | **NO** |

Noncanonical results may be cited as **history**, never as **evidence**.

## Mechanical result

Produced by `tools/gate/zag_rebuild_pass.sh` over all 1048 committed `.zag` sources:

```
committed .zag sources compiled : 1048
  A  compiles AND runs exit 0            : 382
  B  compiles, non-zero exit              :   0
  F  FRAGMENT/TEMPLATE, build documented  : 659
  E  COMPILER REJECTS (dead)              :   7
  unclassified                            :   0

committed non-Zag sources      : 0   (must be 0)
committed extension-less files : 344 (retained as history, NONCANONICAL)
```

**A means COMPILES AND RUNS. It does not mean REPRODUCES the original numbers.** That is
a stronger claim needing the original output for comparison, checked per-result by hand.
"Compiles" is not "reproduces" — conflating them is how a lane convinces itself of a result
it never re-derived.

## The 7 dead claims (class E)

Each has a `main` yet the compiler rejects it, and no sibling or recipe supplies the
missing definitions. **Each was verified independently of the pass that found it.**

| source | error |
|---|---|
| `compose_adversary/eval_templates/eval_main_{a,b,c}.zag` | `unknown function: o_app` |
| `l3_suf_redteam/rt_surv.zag` | `unknown function: get32` |
| `l3_suf_redteam/rt_trace.zag`, `rt_trace07.zag` | `unknown function: z_alloc` |
| `p5meta5g/m5g.zag` | `E0010 unexpected token at top level: _zag_print` |

Consequence: **any conclusion resting solely on `p5meta5g` is noncanonical.** That
includes the P5-meta closing analysis, which must be re-derived from its scorer
(`p5meta3/score53.zag`, class A) rather than from the generator.

## Three classification errors I made, and the corrections

The first three passes reported **406**, then **237**, then **125**, then **50** dead
sources. Each reduction came from investigating an "E" rather than accepting it, and each
was my error, not the corpus's:

1. **406 → 237.** Many "dead" sources are **fragments built by concatenation**.
   `belief_provenance/NAMECHECK.md` states the recipe outright:
   `cat bp_learner.zag bp_world.zag bp_driver.zag > bp_full.zag`. The fragments cannot
   compile alone; the `_full.zag` sibling compiles. Not dead.

2. **237 → 125.** Some directories carry the recipe under a name I had not matched.
   `p6_formal_induce` uses `p6_build_all.sh`, and `cogops_unify_general` uses plain
   `mk.sh` / `gen.sh` / `det.sh`. Matching only `*_build.sh` missed them.

3. **125 → 50.** A large block was **templates and include fragments with no `main` at
   all** — the compiler says `no main function found`, and files like
   `grid/tmpl_head.zag` literally contain `${...}` placeholders. A template is not meant
   to compile standalone. Calling these "the compiler rejects these sources" overstated
   the damage by ~20× and would have wrongly condemned most of the corpus.

The lesson generalises past this script: **"the build failed" and "the claim is dead" are
different statements**, and I collapsed them three times before checking what the failure
actually was.

## Adjudicated by hand

- **A** — `p6struct/precond.zag` (forward lens 3/2/4, 3 of 340 derivable, matching
  hand-derived arithmetic; `bughunt.sh` C1–C3 confirm mutation sensitivity),
  `phase1/audit_struct.zag` (the **0/574 structural bound**).
- **F (stale)** — any pre-gate output attributed to `p6struct/precond.zag`. The readings
  `A0 -> FAILED`, `derivable : 0`, and heap garbage as derived symbols are **not results**.
- **F (scorer clean, generator unproven)** — `phase6/`. The ported scorer is pure Zag and
  reproduces every bar; the **generator** it scores is a separate claim.
- **E (guard bypass)** — results whose generator used `/usr/bin/python3`. All 13 scorers are
  ported and re-run, so the *verdicts* are re-derived, but the **generators** remain
  separate. And same-author re-derivation is not independent confirmation.

## Load-bearing status

Only two claims rest on A-class evidence:

1. the **0/574 structural bound** (Phase 1),
2. the **3-rule grammar serving both directions** (P6 precondition).

Everything else is B, F, C or E until rebuilt.

## Open decision (unchanged)

Purge-and-rebuild-all, or adopt a documented **frozen binary** rule with a `FROZEN.md` per
phase. Default meanwhile: binaries retained but **noncanonical**.