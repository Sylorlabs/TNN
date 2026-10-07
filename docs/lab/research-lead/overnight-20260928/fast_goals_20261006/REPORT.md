# Fast TNN goals wave - results and handoff

Date: 2026-10-06. Status: THREE SMALL AUDITS EXECUTED; larger goal tests PLANNED.
Base: ownership 91b2acc29731135a143adf27c00400174550eaf1.
Branch/worktree: fast/method-identifiability / .worktrees/fast-method-identifiability.
Prereg-only commit: 680b65235 (before drivers). No original learner source edited.
Science: pure Zag; portable output; compile-gated executions. No claim minted.

## Answer

Current small contract mechanisms do not establish reliable general control or
representation necessity. They have real bounded adaptation, but the next research
investment should be qualified evaluators, authority semantics, state isolation,
and a same-information facts-only method-ownership baseline.

## Q1 / T01 - historical reject after growth

QUESTION: does growth preserve a known rejection?
HYPOTHESES: reject preservation vs interval-hull widening.
MINIMUM WORLD: accepts 2,4; reject 6; later success 8.
CONTROLS: frozen interval, fresh reinduction with all observations, hand predicate
on x=1..10; unmodified original u_* functions.
EXPECTED DISCRIMINATOR: 6 rejected initially; growth admits it; reinduction can
include 8 without admitting 6.
RUN: contract_probe, three fresh builds/runs.
RESULT:
- Initial contract rejects 6 and 8.
- u_grow(8) admits both 6 and 8. Frozen contract still rejects 6.
- Reinduction accepts 2,4,8 and rejects 6; induced mod8 interval [0,4].
- On independent predicate even in [2,8] except 6: grown errors 4/10,
  frozen errors 2/10, reinduced errors 4/10 (mixed observed/unseen grid).
- Reinduction errors are x=1,3,9,10. It fits observed labels, not the intended law.
- The ten-point evaluation grid includes observed 2,4,6,8, so it is not wholly
  heldout. On the six never-observed points {1,3,5,7,9,10}, errors are grown 3/6,
  frozen 1/6, reinduced 4/6. Historical-reject regression at 6 is separate.
WHAT IT KILLS: reject-preserving-control interpretation of unguarded u_grow.
WHAT IT DOES NOT KILL: legitimate predictive widening; immutable authority guard
implemented elsewhere; broad contract-learning methods. No safety rule was supplied
by a human in this fixture, so call this a control-semantics gap, not an actual safety
incident. No claim reinduction repairs generalization.
NEXT QUESTION: keep immutable authorization limits distinct from learned predictive
contracts; test stored-counterexample checks, then noise and replay paths. Also run
join-underdet-style disambiguation: an alternative fitting the data is not wrong merely
because the researcher secretly intended another law.

## Q2 / T02 - revision locality

QUESTION: can A's failures trigger B's revision in one arena?
HYPOTHESES: per-contract history vs arena-global failure/request state.
MINIMUM WORLD: A and B at bases 100/200; B never fails; three A disagreements.
CONTROLS: B alone in an isolated arena, same B judgment table.
EXPECTED DISCRIMINATOR: shared B revision count=1; isolated B revision count=0.
RUN: contract_probe, same three runs as Q1.
RESULT: shared failure run=3, request=1. A clause retired; B remained active with
local disconfirmation count=0. Calling u_revise(B) consumed the shared request and
incremented revision count to 1. Isolated B revision count remained 0. B's prediction
at 25 stayed correct before/after (no behavioral damage demonstrated here).
WHAT IT KILLS: interpreting this API's shared-arena failure history as per-contract.
WHAT IT DOES NOT KILL: per-instance use, intentional global coordination, or actual
TNN integration which may allocate independent arenas. This probe deliberately tests
multiple bases; original scenarios only exercise a single contract per arena.
NEXT QUESTION: declare whether global coordination is intended; if not, make history,
judgment window and revision ownership local and test multiple persisted contracts.

## Q3 / T03 - kinds versus flat observed-output membership

QUESTION: do refined kinds add a selection distinction beyond facts in this fixture?
HYPOTHESES: kind structure necessary vs singleton tags equivalent to probe membership.
MINIMUM WORLD: original LCONT two worlds; 41 targets 0..40; six operation candidates.
CONTROLS: flat probe_has rival with same maximal-evidence selection and tie order;
coarse-kind control; IDs are behavior-permuted between original worlds.
EXPECTED DISCRIMINATOR: refined-flat flags and outer-choice mismatches=0.
RUN: flat_probe, three fresh builds/runs.
RESULT per world:
- duplicate kind pairs=0 (all singleton kinds).
- candidate flags: 246 comparisons, 0 mismatches.
- outer choices: 41 comparisons, 0 mismatches.
- coarse-flat candidate mismatches=210; choice mismatches=33.
Total refined-flat: 492 flag comparisons and 82 outer choices, zero mismatches.
WHAT IT KILLS: necessity of refined kinds for these candidate/selection decisions.
WHAT IT DOES NOT KILL: benefit of refinement relative to a coarse indiscriminate
selector, learned behavior grouping, non-singleton abstractions, or full task success
on novel inputs. The rival retains original probe facts and evidence; it does not
consult kind assignments or hidden world law. No timing/speed claim made.
NEXT QUESTION: shared behavioral classes and uncacheable transfer where a learned
contract demonstrably compresses/generalizes better than an equally informed table.

## Original positive scenarios reproduced

Explicit post-prereg sanity checks, not newly preregistered capability claims:
- Original contract-unification scenario freshly built/run three times.
- Original learned-contracts scenario freshly built/run three times.
- Only final output transport patched from inert Linux raw syscall to _zag_print;
  LCONT return now also fails if its original measured aggregate fails.
- Each full output matches its archived run1.txt BYTE-FOR-BYTE, via cmp.
- Archived contract output SHA: 628b78121ddf7a67a2543b152b705cab8fd95a556b8ffcee6a3cf5edf55f45e1.
- Archived LCONT output SHA: 45bfba7a30a0c3d9f9a64cefd4c52267d402e186e8179ee20c10b656f7c6220f.

These positives and our narrow negatives coexist: reported adaptation happens, yet
stronger control and representational-necessity interpretations do not follow.

## Verification and interfaces

From this isolated worktree run:

```sh
bash docs/lab/research-lead/overnight-20260928/fast_goals_20261006/run.sh
bash docs/lab/research-lead/overnight-20260928/fast_goals_20261006/reproduce_originals.sh
```

run.sh assembles unchanged prefixes, cmp-checks them, checks PURE-ZAG-CLEAN,
compiles for macos-arm64, requires runtime success/nonempty output, and compares
three repeats. See environment.txt/provenance.txt, compile/run logs, driver and
assembled source. Binary hashes agree for each adversarial probe's three builds.
Driver exit 0 means predicted audit measurements confirmed, not the architecture
passed autonomy/control. Separate Zag compiler type/build checks succeeded.

Original source and historical report/prereg files untouched. New-driver loop and
bar lints CLEAN. Remaining performance/scaling questions unmeasured; no speedup
claim. Determinism is not independent replication. No canonical TNN learner or
transformer benchmark was run. Current docs are a broad hypothesis map, not an
exhaustive audit of all repository lanes.

## Documentation delivery

- ../../RESEARCH_GOALS_AND_TESTS.md: eight operational goals, 22 hypothesis/test
  specifications, common controls, stop rules and priority order.
- ../../CURRENT_EVIDENCE_NOTES.md: dated correction layer for misleading scope,
  recursive-grammar, statistical-impossibility, contract-unification and hypothesis
  language. Historical records remain unchanged.
- ../../FRONTIER_QUEUE.md: links to plan/corrections, scorer qualification item,
  stale tool paths corrected, P5-meta5f no longer labeled an unrun experiment.
- ../fast_membership_order/: earlier order/permutation audit source/logs preserved.

## Main-researcher handoff (do not build everything)

1. P0: qualify grammar scorer with the existing adversarial fixture and a genuine
   bounded recursive oracle. Explicit designated-root semantics required.
2. P0: declare hard-authority versus learned-applicability semantics; guard actual
   effects and test update/replay/revocation paths. Decide multi-contract state scope.
3. P1: run uncacheable method-ownership with facts retained/method erased, flat table,
   and equal-search-budget controls. Freeze source across new task laws.
4. Only a surviving result proceeds to unseen depth, revision+interference, and actual
   canonical learner interface replication. Graph expansion waits for causal evidence.
