# SEALED_EVAL.md - INDEX-EVICT lane, wave-20261002-0521pdt

Governing frozen bar: PREREG_EVICT.md (commit `0f2a862f2`, alone, before
any implementation file). Verdict: **EVICT-PASS**. All eight frozen
conditions hold; no bar was weakened.

## Build (frozen inputs, pure Zag, pinned znc)

Sealed inputs in `work/sealed/` (shas in BUILD.txt). Driver sha256
`b421402707b429bad88b89640b11956720ce6fcd53c4e5e4364732052ad6b450`,
byte-identical in both binaries. The ONLY source delta NEW vs OLD is
the eviction hook (1 line in `evict_node` + `idx_on_evict` hook
functions, ~90 lines, 0 new modes/bridges/handlers).

A red-team self-catch during the sealed runs: the per-eviction seq
table initially kept the LAST type-12 edge per source while `seq_nx`
(used by `rb_chain_plen`) returns the FIRST. Fixed to first-wins
(matching `seq_nx` exactly, per the prereg's "mirroring rb_chain_plen
exactly"); the governing run set below uses the fixed build. The two
builds are byte-identical in output on all sealed runs (each 101 node
has exactly one type-12 out-edge in these worlds), so the fix is a
soundness hardening, not a behavior change. An initial last-wins run
set was superseded and is not the verdict basis.

## Runs

- sealed_new_r1/r2/r3.txt: sha256
  `54df62307f28fcd05fcbe455cbc6e062ed90c2287860f4c8011a3d6d86293414`
  (3/3 byte-identical).
- sealed_old_r1/r2/r3.txt: sha256
  `63f9f7e0669312ddca56683733c8437296c530cbeb28da60be670c7c26ceb38a`
  (3/3 byte-identical).
- parta_new_r1/r2/r3.txt: sha256
  `eee373a21053b2a3a0005be8c1c83ed923f51b22c528b36cd9425d3052146d9d`
  (3/3 byte-identical; canonical Part A hash).

## Kill-bar evaluation

(i) Vacuity (OLD demonstrates the bug). PASS. W1 Phase A: victim 22
(tag 101) flips `idx` 1 to 0, FIRSTFLIP cause=3 (chain invalidation,
V2). W1 Phase B: victim 35 (tag 20) flips, FIRSTFLIP cause=1 (dead
member, V1). W2 Phase A: victim 7 (tag 1) flips `fidx` 1 to 0,
FIRSTFLIP cause=4. W2 Phase B: same, cause=4. CHURN gates: W1 idx=0,
W2 fidx=0. The storm exercises both stale paths; not vacuous.

(ii) Coherence invariant (NEW). PASS. `idx_validate==1` and
`fidx_validate==1` after EVERY eviction in W1 and W2, all 3 runs.
Zero gate-0 lines in 3/3 NEW logs (grep for `idx=0|fidx=0` returns
none). Covers V1 (stale membership) and V2 (chain invalidation).

(iii) No performance collapse. PASS.
- W1: NEW QPOST2 q0 scan=39 < OLD QPOST2 q0 scan=56 (strict), and
  39 <= 4 x NEW QPRE q0 scan=38 (152). The index serves post-storm;
  OLD degrades to linear.
- W2: NEW GPOST gather factvisits=59 < OLD GPOST gather
  factvisits=32760 (strict; 555x), and 59 <= 4 x NEW GPRE gather=51
  (204). OLD collapses to full linear scan; NEW stays indexed.

(iv) Answers preserved. PASS. Every emitted ans/ok/np/hits value in
NEW equals the corresponding OLD value run-for-run (diff of the
answer projection is empty). Eviction changes nothing the system
knows.

(v) Determinism. PASS. 3/3 byte-identical per binary (hashes above).

(vi) Healthy-state no-op. PASS. NEW on the Part A driver: 3/3 runs
byte-identical to the canonical hash
`eee373a21053b2a3a0005be8c1c83ed923f51b22c528b36cd9425d3052146d9d`.
The hook is output-silent on healthy worlds.

(vii) Mechanism accounting. PASS. NEW W1: node-0 field 4 (unmap) = 6
= number of tag-20 victims; all 6 died (k20=6, calls=6). NEW W2:
field 8 (unfact) = 18 = 10 Phase-A + 8 Phase-B tag-1 victims; all 8
targeted died (k10=8, calls=8). Field 12 (unchain) = 1 >= 1
(chain-break unlinks happened). OLD: all three counters 0.

(viii) MTF coherence. PASS. W1 Phase B: the MTF winner (673) is a
targeted victim; the eviction line that killed it (c=3) shows
`cache=-1` immediately after. Query answers still equal OLD (iv).

## Cost

Wall time on the identical storm driver: NEW 1m27s, OLD 1m46s. The
hook (one 16384-edge scan plus short chain walks per chain-victim
eviction) costs less than the linear fallback it prevents; NEW is
faster because it stays on the index while OLD degrades. New
cognition lines: ~90 (4 functions). New modes: 0. New bridges: 0.
New handlers: 0. New semantic cases: 0.

## Verdict

**EVICT-PASS** under PREREG_EVICT.md (commit `0f2a862f2`). The
eviction path that created stale bucket entries now maintains index
coherence: both stale membership (V1) and chain invalidation (V2)
are unlinked at eviction time, the validation gate accepts after
every eviction, post-storm queries stay indexed, answers are
unchanged, and healthy-state output is byte-identical to the Part A
canonical hash.

## Red-team self-review (summary)

Full text in REDTEAM_SELF.md. The mechanism holds for the
`evict_node` path. Known bounded gaps, none firing in the sealed
eval: (a) infrastructure nodes (tag 40/900) as victims are not
handled; (b) `t2_revise_graph` tombstones chain nodes outside
`evict_node` (queued adjacent work); (c) plen-2/plen-4 bucket victim
positions untested. The claim is "index-coherent eviction for the
evict_node path", not "all memory mutation is index-safe".
