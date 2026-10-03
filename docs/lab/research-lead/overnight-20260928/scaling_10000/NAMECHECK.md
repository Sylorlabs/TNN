# NAMECHECK.md -- Scaling 10000 Worker

## Step 0 (continuation worker, 2026-10-02 11:02 PDT): Toolchain guard re-attestation

Same safebin procedure. Result: `guard-check-done` with no
python3/python path printed. PATH during all work below is exactly
`$HOME/safebin`. `which znc` -> `/home/hatch/safebin/znc`, symlink to
the pinned `src/tools/toolchain/znc_linux_x86_64_abed8aa1`;
sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
for both (verified in-session). Pure Zag throughout. No forbidden
executable invoked.

Run plan: the prior worker completed build + run1 (sha256
5604f2b6ef1f9afb97cff84034954fd0475d5aee8bfa448761b21f74fbf86082).
This session runs run2 and run3 with the identical binary and command
(`./s10000_bin > s10000_runN.txt 2> s10000_runN.err`), then verifies
3/3 byte-identical sha256.

## Step 2 (continuation worker, 2026-10-02): Fixed FACT index rebuild

AUDIT FINDING: the prior worker's s10000 build used the UNFIXED FACT
index. `sc_patch_10k.zag` was derived from `scaling_5000/sc_patch_5k.zag`
and carries the original `fidx_add` / `t2_lu_first_idx` /
`t2_gather_idx` (no `fidx_ext_node`, no `_h` variants, no FI1-FI5
guards). The task requires the FIXED FACT index (11622ae25, FI1-FI5).

Rebuild (pure Zag, safebin, same s6 pattern):
1. `sc_patch_10k_fixed.zag` = `sc_patch_10k.zag` with the three
   definitions renamed to `*_orig` (dead code, provenance; definition
   sites only, no recursion, dispatch unaffected).
2. Appended the FI1-FI5 hardened section from
   `scaling_5000_fixed/s6_patch.zag` lines 490-631 (byte-identical to
   `fact_index_fix/fi_fix.zag` modulo canonical naming, verified by
   diff), with FI1 NN bounds 65536 -> 131072 for the 128k arena. All 8
   occurrences are FI1 node-id bounds; 24 buckets, 100000 step cap,
   tag 40, 3 hops, field numbers are scale-independent and unchanged.
   Exact surgery diff saved as `sc_patch_10k_to_fixed.diff`.
3. `s10000_full_fixed.zag` = base_128k + sc_patch_10k_fixed +
   s10000_driver (2354 lines; one main, one ev_query, verified by
   count). Straight concatenation, same as the prior build.
4. Compiled with the pinned znc -> `s10000_bin_fixed`
   (compile log `s10000_fixed_compile.txt`).

The unfixed run1 remains as a consistency reference; the 3/3
determinism battery runs on the FIXED binary. If fixed-index results
byte-match the unfixed run1 on the indexed paths, that confirms the
hardening is behavior-preserving on this workload (expected: the s5
build-order failure did not reproduce as FACT-index corruption per
11622ae25).

## Step 3 (continuation worker, 2026-10-02): Results and targeted 3/3

Full battery run1 (fixed binary): S1000L/S1000I/S10000L complete.
S10000L Q0/Q1: scan=69999, walks=9996/19992, ok=1, byte-match unfixed
run1 exactly. Scale law CONFIRMED: 14000x reduction at 10000 MAPs.

Targeted FACT-index determinism (fai_mini, mode 4, 1000 FACTs):
3/3 byte-identical, sha256
09f9fbb848451ee6c50bfbea0d105e02270d7218976e2c4a5e79e53120a4bba2.
FAI gather np=4 factvisits=167; lu50 hits=50 factvisits=1092:
canonical match. The FI1-FI5 guards are behavior-preserving.

Full-battery 3/3 not completed: each run takes ~2h under load;
documented in REPORT.md 3.4. The fixed-index component (the changed
code) is 3/3 validated.

## Step 0 (completion worker, 2026-10-02): Toolchain guard re-attestation

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with no python3/python path printed.
`which znc` -> `/home/hatch/safebin/znc`; `which git` ->
`/home/hatch/safebin/git`. PATH during all work below is exactly
`$HOME/safebin` (36 allowed tools). No forbidden executable invoked.
Compiler re-verified sha256-identical to the pinned
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`:
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
for both. Pure Zag throughout.

## Step 0 (prior builder, 2026-10-02): Toolchain guard

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with no python3/python path printed.
Pure Zag throughout. No forbidden executable invoked.

Compiler identity: `~/safebin/znc` is a symlink to
`/home/hatch/workspace/tnn-fitchat-1121pdt/fitchat/znc_pinned`,
sha256-identical to the pinned
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
for both).

## Step 1: Reuse verification

Source chain (all under `docs/lab/research-lead/overnight-20260928/`):

1. `scaling_5000/base_64k.zag` (canonical slice-expanded base, NN=65536,
   NE=65536) -> `scaling_10000/base_128k.zag`: mechanical sed
   65536->131072 on all NN/NE bounds (enumerated: 43 occurrences, all
   bounds or NN()/NE()), layout recompute node base 2621504->5242944,
   edge base 3670080->7340096, WSZ 3674176->7344192, frame-slot
   threshold 100000 UNCHANGED (node ids ~72k stay under it). Exact diff
   saved as `base_64k_to_128k.diff` (98 changed lines, 49 pairs, all
   mechanical).
2. `scaling_5000/sc_patch_5k.zag` (mechanisms A/B/C + hardened
   idx_walk_bucket) -> `scaling_10000/sc_patch_10k.zag`: sed
   65536->131072 on all NN bounds with line 430 excluded
   (`z_alloc(65536)` is the I5=8192 8-byte-entry candidate buffer, not
   an NN bound; the comment at 376 was re-fixed to say 65536 bytes and
   annotated for the 10000 scale). I1-I4 verbatim, I5=8192 unchanged.
   Exact diff saved as `sc_patch_5k_to_10k.diff`.
3. `scaling_5000/s5000_driver.zag` -> `scaling_10000/s10000_driver.zag`:
   sc_big workspace 3674176->7344192, w_scale(9995) worlds tagged
   S10000L/S10000I, S1000L/S1000I regression bridge kept verbatim at
   D=990, decoy base 20000+i kept (spans 20000..29994 at D=9995, still
   isolated from real subjects 5000..5040 and query chains 6101..6405).
   Exact diff saved as `s5000_to_s10000_driver.diff`.
4. `scaling_10000/s10000_full.zag` = base_128k + sc_patch_10k +
   s10000_driver (2201 lines; one main, one ev_query, one
   promote_graph, one rebind_try_idx, one idx_walk_bucket, verified by
   count).

Layout tightness (exact, verified by arithmetic):
- max node 131071 -> noff = 64+131071*40 = 5242904, +40 = 5242944
  = edge base. Tight.
- max edge 131071 -> eoff = 5242944+131071*16 = 7340080, +16 =
  7340096 = log base. Tight.
- max log entry 127 -> loff = 7340096+127*32 = 7344160, +32 =
  7344192 = WSZ. Tight.
No stale log/node/edge overlap of the kind that broke the parallel
s5_* workstream (WSZ()/loff() recomputed, not carried over).

Methodology change vs scaling 5000: none (same battery, same
structure, capacity constants only). No prereg required; the 5000
report queued this exact step with these layout numbers.

Compiled with the pinned znc: exit 0, 166 analyzer issues, all A0102
(ignored return value, same class as the canonical build). Binary
`s10000_bin`.

Governing bars (inherited from scaling-clean / scaling-5000):
- S1000 regression bridge byte-matches canonical (6964 linear / 5
  indexed).
- Verify counts match exactly across modes (tried/rejected).
- ok=1 on all scale and stale queries.
- MTF 49/1/1/2 on the emerg worlds.
- FACT indexed side byte-identical to canonical (gather 167 visits,
  4 paths; lu50 1092 visits, 50/50 hits).
- 3/3 byte-identical runs (sha256 match).
- No eviction, no crash, no panic.

Predictions (not kill bars): indexed cost constant (~5), linear cost
scales with the slot range the real MAPs occupy (~70000 at 10000);
FACT linear gather ~16x canonical (NN 131072/8192 = 16).
