# COMPOSE-SUSPEND-1 REPORT (2026-10-03)

Worker: COMPOSE-SUSPEND-1. Non-ledger task. Hypothesis B: SUSPEND.
Lane: `docs/lab/research-lead/overnight-20260928/compose_suspend_1/`
Branch: `tnn-native-lab`. Pure Zag, safebin, pinned znc
2026.07.0-dev. Commits local, never pushed.

## Verdict: BUILD-PASS

Every frozen kill bar (PREREG.md Sections 3.1-3.3, as amended by
PREREG_AMEND1/2) passed on 3/3 byte-identical runs of both
binaries. No bar was weakened; no result was adopted from a
broken run.

## What was built

A two-phase lazy composition engine on the PAIR6 substrate:

- **ASSEMBLE** (`sus_asm.zag`): regressive need-solving over
  opaque kind-masks. Needs are kind sets; producers are tried in
  id order; direct-close precedes sub-need alternatives; 2-input
  legs are solved t1-outer/t2-inner. Thunks are hash-consed
  (structural identity) into a persistent DAG. Zero execution
  (phase flag + viol counter instrument every exec site).
  Loop guard: a producer already on the current root-to-leaf
  path fails that choice entirely (PREREG_AMEND1; reproduces
  the 5.4 walkthrough's 20-candidate Q1 sequence exactly and
  keeps CHAIN3's c1(c0(C)) nesting, which uses distinct
  producers).
- **EVALUATE** (`sus_thunk.zag`): recursive demand with identity
  memoization (memo keyed by thunk id, not by value) and a
  loop guard. Per-thunk and per-map execution counters.
- **WIDEN** (`sus_asm.zag`): one-shot, runs at most once per
  process, only when compatible assembly fails. Enumerates all
  MAP applications over thunks whose memos were observed
  non-negative on any prior evaluation, ignoring kind
  compatibility. Needed for Q2's misleading teaching.
- **REBIND** (`sus_rev.zag`): structural copy of a stored
  composite root over a fresh const input; no search, no
  re-assembly; demand re-executes only the fresh thunks.
- **REVISE** (`sus_rev.zag`): inventory-change invalidation
  (changed MAPs + fixpoint ancestor closure only, recorded in
  an explicit invalidation list), fault localization to the
  deepest reachable -2-valued thunk whose inputs are all
  non-(-2), then substitution of the next kind-compatible
  producer over the identical input sub-thunks; memoized
  dead alternatives fail without re-execution.
- **Composite store** (`sus_rev.zag`): keyed by
  (kind-in, kind-out, inventory sketch); solve() stores every
  successful root.

No diamond handler, no shape template, no mode, no domain
branch exists anywhere in the code: map classes are the
PAIR6 substrate's (WALK/COUNT/ADD2), kinds are opaque bit
positions, and every decision is over ids and kind bitmasks.

## Frozen results (run_main_*.txt, 3/3 byte-identical)

| Prob | ANS | Key frozen numbers | Verdict |
|------|-----|--------------------|---------|
| Q1   | 5   | VIOL=0; exec(X)=1; path_exec=4; DSEARCH=1 | PASS |
| Q1b  | 3   | DASM=0; DSEARCH=0; DEXEC=4 | PASS |
| Q1rev| 5   | DEXEC(X)=0; DEXEC(Y)=0; DSEARCH=0; invalidation clean | PASS |
| CHAIN3 | 7 | DSEARCH=1 | PASS |
| FANIN | 9 | DSEARCH=1 | PASS |
| PARTIAL | 3 | ROOT==Q1 Y-leg tid; DEXEC(X)=0 | PASS |
| Q2 | 5 | WIDEN=1 (only widen of the run) | PASS |

Blind battery (run_blind_*.txt, 3/3 byte-identical): 5/5
variants produced byte-identical PASS blocks
(ANS=5, ASMSTEPS=21, WIDEN=0) under relabeling of relation
ids, node ids, and kind polarity. The engine is
domain-blind: it behaves identically under renaming.

## Discriminator analysis (vs GEN / BACKCHAIN)

- **F-B1 is the sharpest architectural discriminator, and it
  held.** A re-running search composer (GEN's ev_query) pays
  assembly steps again on re-query; SUSPEND's rebind pays zero
  assembly steps and exactly 4 executions (one per fresh
  thunk). DASM=0/DSEARCH=0 with DEXEC=4 cannot be produced by
  any architecture that re-derives the composition from
  scratch per query.
- **F-B2 held with zero additional X/Y executions.**
  Inventory-change invalidation touched only the changed MAP's
  thunk and its ancestors (recorded list verified clean);
  the Y-alternative failed on the memoized 6 without
  re-executing Y; the V-alternative succeeded on 2 new
  executions (W-retract re-eval, V, G). A search-based
  reviser would re-execute the whole root path.
- **F-B4 held (VIOL=0 cumulative).** The viol counter was
  verified live (a forced phase-0 execution increments it),
  so zero is evidence of phase separation, not a dead
  instrument.
- **F-B3 held (exec(X)=1).** Identity memoization shares the
  single X(C) thunk across both diamond legs; the path-based
  loop guard is what makes the count exactly 1 (the
  as-specified pair guard allowed X(X(C)) and would have
  given 2; see PREREG_AMEND1).

## Bounds (restated)

SMAX=6 (backup depth cap; path guard is the real termination
rule), MAXT=256 thunks, MAP ids < 16, arities <= 2, one
process, one inventory-change event per run, blind variants
run in fresh arenas. The mechanism was exercised only on the
frozen seven plus five blind variants; wider arities,
multi-change revisions, and larger inventories are untested.

## Architecture accounting (constitution)

Cognition lines added: ~1300 (6 Zag files). New hardcoded
semantic cases: 0. Modes: 0. Bridges: 0. Handlers: 0.
Learner-state structures created: thunk DAG, per-thunk memos,
composite store, invalidation list. The fork from GEN is a
general rule (regressive need-solving + lazy demand), not a
diamond handler.

## Amendments (both committed before the implementation
commit; implementation itself is committed after them)

- PREREG_AMEND1: (need,producer) guard -> path-based
  producer guard. Cause: debug build enumerated 42 Q1
  candidates (X(X(C)) chains) instead of the walkthrough's
  20; F-B3's exec(X)=1 required the path rule.
- PREREG_AMEND2: executable fact encoding. Cause: the
  prereg's "(211,92,3)" shorthand is not executable on the
  PAIR6 substrate (COUNT returns fact counts); realized as
  three distinct facts per the d6 convention. No predicted
  value changed.

## Files

- NAMECHECK.md, PREREG.md, PREREG_AMEND1.md,
  PREREG_AMEND2.md (frozen design)
- sus_base.zag, sus_thunk.zag, sus_asm.zag, sus_rev.zag,
  sus_world.zag, sus_main.zag, sus_blindmain.zag,
  sus_build.sh (implementation)
- sus_full.zag, sus_blind.zag (generated concatenation)
- sus_bin, sus_blind_bin (binaries)
- run_main_1/2/3.txt, run_blind_1/2/3.txt (3/3 logs)
- sus_compile.txt, sus_blind_compile.txt

## Recommended follow-up

SUSPEND is built first, so per COMPOSE-GENERAL-1's step (4)
the blind battery result above already covers it. The
natural next discriminators are A's F-A1 (chain-10 vs
frozen GEN: does regressive assembly stay sublinear where
GEN's search blows up?) and C's F-C1, plus a head-to-head
on an adversary-designed sealed world neither hypothesis
has seen.
