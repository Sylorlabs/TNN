# NAMECHECK.md -- Specialize Mask Revision Worker

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` printed. `which python3 python` returned
NOTHING. All subsequent work ran with PATH=$HOME/safebin.

Note: znc was already linked in $HOME/safebin by prior work
(pinned `znc 2026.07.0-dev (edition 2026)`); a hello-world probe
compiled and ran (BUILD-OK) before any experiment code was written.

No forbidden executable invoked at any point. Pure Zag via the pinned
znc. Shell used only for: safebin setup, file concatenation, znc
invocation, binary runs, sha256sum, read-only greps, and git ops.

## Step 1: Task identity

Specialize Mask Revision Worker (subagent, 2026-10-02). Mission: test
revision of SPECIALIZE masks when the world changes. Phase 1 masks
work (MASK_K1=48, MASK_K2=12 from L2-L3-SPEC-COMPLETE); phase 2 world
change moves the informative slots (kind 1 signal pair (d,e) -> (b,c),
kind 2 signal pair (b,c) -> (d,e)); the learner must revise the masks
via x_revise_masks (consolidation pointer REV_PTR, recompute per-kind
variance masks over the not-yet-consolidated window). Four arms:
ARM-BASE (masks work initially, Z-PHASE1 4/4), ARM-STALE-KEEP (stale
masks, M1 reused, Z exactly 2/4), ARM-STALE-REBUILD (stale masks,
construction re-run, n=0, Z 0/4: information-starvation proof),
ARM-REVISE (masks swap 48<->12, M1 reused, Z-REVISE 4/4).

## Step 2: Constraints honored

- Unfrozen only. No frozen source touched. Sibling l2_l3_spec source
  read for method reuse, adapted with disclosed deltas (32-episode X
  store, shifted state offsets, x_learn_masks replaced by the
  consolidation-pointer x_revise_masks).
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified before commit).
- Paper untouched.
- Nothing pushed. Commits local only on tnn-native-lab, with EXPLICIT
  pathspecs (concurrent workers active).
- 0 modes, 0 handlers, 0 semantic cases; op basis {CPY,ADD,SUB,MAX,MIN}
  frozen in prereg and never expanded (F-OP-EXPAND silent).
- ADAPT_ON is a driver-set causal-control flag (the composition_l2
  adapt_on precedent), never written by the learner.
- Commit order: prereg committed alone at cda792126 before any
  implementation file existed. No amendments.

## Step 3: Development notes

1. The prereg hand derivations were done before any implementation
   existed. The first full build reproduced every one with zero
   source changes after the initial pre-run cleanup (one unused
   driver local `mnB` removed; it only triggered a B0103 warning).
2. Build: `cat learner.zag world.zag driver.zag > rv_full.zag`
   (1010 lines), then `znc rv_full.zag -o rv_bin`. Build exit 0.
   Only diagnostics: the benign zagd-unavailable notice plus three
   A0101 off-by-one heuristic warnings in x_revise_masks/x_recall
   (analyzer cannot prove the bounds; indices are provably in
   range: max store index 8+31*7+6=231, max mask offset 405, all
   inside their buffers).
3. Output path follows the AGENTS.md stdout workaround: numbers
   formatted directly into one preallocated 64KB buffer with
   cursor-returning helpers (ob_app/ob_i32), single
   `_zag_raw_syscall(1,1,ptr,len)` write loop. No `_zag_print`
   anywhere. Stdout verified: 190 lines, 0 NUL bytes (tr/cmp
   check), ends with SHIFT-MASK-REVISION-END.
4. State uses u8 buffers with get32/set32 only; no `as *i32` slice
   construction. Register file is an 8-byte scratch (2 registers).
   Mask bit tests use integer division, not bitwise ops.
5. Key result shape: masks SWAP 48<->12 on revision (kind 1 window
   varies slots 2,3 only; kind 2 varies slots 4,5 only); M1
   [ADD R0,R1] reused untouched; stale arms give exactly 2/4
   (always-skip) and n=0/0/4 (information starvation).

## Step 4: Determinism

- No RNG anywhere. Fixed candidate order (op 0..4, d 0..1, s 0..1),
  first-max tie-breaking, ascending threshold sweeps (t=0..40).
- rv_run1/2/3.txt sha256 identical:
  82fab4f577319d2d58858a7556b23448bb47c6296b207e366216b9df2a27a6a4
  (all three). K-RV-7 PASS.
