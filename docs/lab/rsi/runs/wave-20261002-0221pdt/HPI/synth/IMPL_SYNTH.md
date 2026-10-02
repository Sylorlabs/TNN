# IMPL_SYNTH: newest-live-among-all-live gate implementation

Lane: HPI, wave-20261002-0221pdt. Built after the freeze commit of
PREREG_H5R2_SYNTH.md (5b2f8e0f0, 2026-10-02 09:40:58 UTC); earliest
synth artifact mtime 09:41:06 UTC. SYN-ORDER holds.

## Sources (extracted read-only, hash-verified before use)

- H5R2 base: git show
  9db334bd4a01d21cce52da3bb2a1c45a10c4c172:docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/tnn3_h5r2.zag
  -> synth/h5r2_base.zag, SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a
  (matches the prereg).
- NEWEST-LIVE-ON-KEY: git show
  f461e812d:docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-SKEPTIC2/bl_newest.zag
  -> synth/bl_newest.zag, SHA-256
  e5df3ddb28858b60efb01f3d8df524a98ce79686e199532e53713c24f367b649
  (matches the prereg).

## The gate (synth/synth.zag)

Per the frozen appendix: t2_prov_ok replaced by synth_elig (the
unchanged all-live tag-1 non-superseded filter) plus synth_score
(maximum licensing node id). The four t2_trial promote sites
(chains k=2..4, sums, counts, single hops) are restructured from
first-verifying early-exit to best-selection within the site:
every candidate is tried, each verifying eligible candidate is
scored, the highest score wins, enumeration order breaks ties
(strict > keeps the first candidate at a given score). Site order
is unchanged: a later site runs only if ans==-2 after the earlier
sites. Deferred promotion is safe: t2_try_verify is pure with
respect to W (it only reads and bumps the st counters), and
promote_graph only needs the saved root id, answer, and licensing
fact ids, which are copied to best buffers (16/48/60/16 bytes for
the four sites, sized to the sites' maxima).

Diff verification: diff of synth.zag vs h5r2_base.zag shows 99
changed lines, all inside the gate function and the four promote
sites; the only remaining mention of t2_prov_ok is in the
replacement comment. No other region differs.

Cognition source delta: +99/-0 lines changed vs the H5R2 base, all
in the trial/miss-policy function t2_trial. new_semantic_cases=0;
modes/bridges/handlers added=0; no protected-core change (the
change is confined to candidate selection in the trial loop, not to
ALLOC/READ/WRITE/LINK/COMPARE/branch machinery). SYN-ARCH holds.

## Build

Pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1, pure Zag,
PATH=$HOME/safebin (no python3; NAMECHECK.md Step 0). synth.zag
compiles clean (exit 0; analyzer warnings only, same class as the
base build). Binary: synth/synth_bin.

## Sealed battery (S arm, main=run_all)

3/3 runs, byte-identical full stdout (SHA-256
e6ac118dd318b54e22bb9bab8b87b6456cb8bfc16355cabac6a552e9b43bf82c),
zero stderr bytes, exit 1 (one failing test). TOTAL 45/46; the
single failure is t_f2 (line 23: "F2 FAIL"), the masked query that
promotes the later-taught 2-hop reading [F2,F4] -> 202 instead of
201. This is the pre-registered Attack 3 regression: the gate breaks
the frozen composition-preserving order.

## DT fragment

synth/DT_FRAG.zag written post-freeze to the frozen section-5 spec
(two competing 2-hop readings, masked query, arm-neutral DT-check,
DT-FIRST/DT-LATER markers, MAPCON-ALL negative control, canonical
state dump). SHA-256
3f3990d727428c360300841230fc483b8522a040793ce7879eb5593dae4d679b,
recorded in DT_FRAG.sha256 before any DT world was assembled or run.

## World assembly

Per the frozen 11.1 rule: byte-copy of the arm substrate with the
single main line changed (diff-verified: exactly one line differs
per world), plus DRIVER_TMPL.zag (SHA-256 verified
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af),
plus the family FRAG, plus one alias line. 12 worlds (S x
s1/s2/d1/d2/e1/e2/t1/t2; H x t1/t2; N x t1/t2); world file SHA-256s
in synth/sealed/worlds.sha256, recorded before any run.

## Runs

Each world compiled separately with the pinned znc; 3/3 runs;
full-stdout SHA-256 compared per world: 12/12 DET-OK, zero stderr
bytes on all 36 runs. Per-world stdout hashes are in the batch log
and SEALED_EVAL.md.
