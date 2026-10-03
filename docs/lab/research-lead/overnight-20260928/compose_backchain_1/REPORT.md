# COMPOSE-BACKCHAIN-1 REPORT (2026-10-03)

Worker: COMPOSE-BACKCHAIN-1 (retry; prior worker errored with no
result). Non-ledger task. Hypothesis A: BACKCHAIN.
Lane: `docs/lab/research-lead/overnight-20260928/compose_backchain_1/`
Branch: `tnn-native-lab`. Pure Zag, safebin, pinned znc.
Commits local, never pushed.

## Verdict: BUILD-PASS

Every frozen kill bar (PREREG.md Section 3) passed on 3/3
byte-identical runs of both binaries. No bar was weakened; no
result was adopted from a broken run. One implementation-side
sizing fix was needed (occ arena 8192 -> 1.2M frames; see below);
it changes no frozen bar and no mechanism rule.

## What was built

BACKCHAIN-A: lazy chronological backtracking over derivation
trees with INTERLEAVED execution. Occurrence frames solve one
need occurrence each; every completed candidate derivation is
executed immediately via demand() (identity memoization, so a
thunk never re-executes); -2 outcomes are skipped, never
yielded; end-to-end failure resumes the search. Loop guard:
(need-kind, producer-id) pair on the open stack fails the
producer choice entirely (PREREG 1.3 amendment: the design's
need-identity guard provably breaks chain nesting, so F-A2 was
restated as DIST1). Backup depth bound DMAX=16 (frozen). WIDEN:
one-shot relaxed pass on observed exhaustive failure. Fresh
learner state per problem: memoryless by construction. No
phases, no composite store, no rebind, no revise.

No diamond handler, no shape template, no mode, no domain
branch: all decisions are over opaque map ids, arities, and
kind bitmasks.

## Frozen results (run_main_*.txt, 3/3 byte-identical)

| Prob | ANS | Key frozen numbers | Verdict |
|------|-----|--------------------|---------|
| Q1 | 5 | TRIES=7; EXEC=1 2 2 2; e1=1; WIDEN=0 | PASS |
| Q1b | 3 | TRIES=7 (=Q1: full re-search) | PASS |
| Q1rev | 5 | TRIES=9; EXEC(m0)=1, EXEC(m1)=2 | PASS |
| CHAIN3 | 7 | TRIES=6 | PASS |
| FANIN | 9 | TRIES=4 | PASS |
| PARTIAL | 3 | TRIES=3 | PASS |
| Q2 | 5 | WIDEN=1 | PASS |
| Q1K | 5 | WIDEN=1 (F-A4: kind gate held) | PASS |
| CHAIN10 | 4 | TRIES=55 (<=120); WIDEN=0; DMAX=16 only | PASS |
| DIST1 | 5 | WIDEN=0; TRIES=12 | PASS |

Blind battery (run_blind_*.txt, 3/3 byte-identical): 5/5
variants byte-identical (ANS=5, TRIES=7, WIDEN=0) under
relation/node/kind relabeling. Domain-blind.

## A vs B (the comparison)

Structural difference, confirmed by measurement:
- A interleaves search and execution (e1=1: a MAP executes
  before the second candidate is constructed). B separates
  them (VIOL=0). This is the sharpest confirmed difference.
- A is memoryless: Q1b re-derives fully (TRIES 7, same as Q1);
  B rebinds with 0 assembly steps. Q1rev: A re-searches from
  scratch (X/Y re-execute); B revises surgically (0 additional
  X/Y execs). B wins re-query and revision; those are the ONLY
  axes where B's extra machinery (composite store, rebind,
  invalidation, revise) pays.
- First-encounter exec efficiency: B 4 execs vs A 7 on Q1
  (B never executes dead candidates during assembly).
- Simplicity: A has no store/rebind/revise/invalidation.
  B's machinery is justified only by F-B1/F-B2.
- Generality on tested worlds: tie (chains, fan-in, diamond,
  partial, widen all pass under both).
- F-A1: A solves chain-10 with only the frozen depth bound
  (no round/pool caps), discriminating vs frozen GEN's round
  cap 6. Cost: ~986k occ frames (permutation exploration;
  design 4.8's exponential worst case is real). B was not run
  on chain-10; its candidate buffer cap (256) and MAXT=256
  suggest it would not scale as built (untested, not claimed).

Net: A is the simpler baseline that solves everything B
solves on first encounter; B's persistence/revision is its
sole architectural premium. For a continuing learner, B's
premium matters; for one-shot composition, A suffices.

## Bounds (restated)

Cycles BOUND (pair guard + onstack demand guard; no
iterate-with-halt). Purity assumed (identity memoization
unsound for effectful MAPs). BACKCHAIN is memoryless by
construction; learning curves belong to hypothesis C.

## Implementation note (sizing, not a mechanism change)

The 8192-frame occ arena overflowed on CHAIN10 (the pair
guard permits permutation exploration: 986,410 frames =
sum P(9,k)); occ_new returning -1 was misread as "producer
exhausted", killing the search at 12 tries. Fixed by sizing
the arena to 1.2M frames. No rule, bar, or prediction
changed; all frozen TRIES bars still hold exactly.

## Files

- NAMECHECK.md, PREREG.md (frozen design)
- bc_base.zag, bc_thunk.zag, bc_search.zag, bc_world.zag,
  bc_main.zag, bc_blindmain.zag, bc_build.sh
- bc_full.zag, bc_blind.zag (generated); bc_bin,
  bc_blind_bin (binaries)
- run_main_1/2/3.txt, run_blind_1/2/3.txt (3/3 logs)
- bc_compile.txt, bc_blind_compile.txt
