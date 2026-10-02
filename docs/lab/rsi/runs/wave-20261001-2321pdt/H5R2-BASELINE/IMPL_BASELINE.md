# H5R2-BASELINE Implementation Record

Lane H5R2-BASELINE, wave-20261001-2321pdt. Implements the frozen prereg
PREREG_BASELINE.md (freeze commit 28cbe5877, 2026-10-02 06:44:42 UTC).
Pure Zag, safebin toolchain, no forbidden executables.

## Ordering and base verification

- Prereg freeze commit: 28cbe5877 (2026-10-02 06:44:42 UTC), containing
  only NAMECHECK.md and PREREG_BASELINE.md. All baseline source files
  were created after.
- Base for all three baselines: the committed H5R2 source extracted via
  git show from commit 9db334bd4a01d21cce52da3bb2a1c45a10c4c172,
  SHA-256 04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a
  (matches the lane's frozen substrate hash).

## Baseline (b): NO-GATE (bl_nogate.zag)

Exact minimal change per prereg section 1: deleted the t2_prov_ok
comment block and helper (14 lines), restored the four t2_trial
promote sites to the ungated `if(v2!=-2){...}` form. Verification:
bl_nogate.zag is byte-identical (cmp clean) to the H5R base blob
extracted via git show from commit 830f95ab7, SHA-256
d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384.
This baseline IS the killed H5R mechanism, bit for bit.

## Baseline (a): REVERT-TO-LATEST (bl_latest.zag)

Changes vs the H5R2 base (verified by diff):
1. Deleted the t2_prov_ok comment block and helper (14 lines); all
   four t2_trial promote sites ungated to `if(v2!=-2){...}`.
2. Chain path: inner p loop reversed (`let p:i32=np-1;
   while(p>=0 && ans==-2){`, `p=p-1;`).
3. Count path: relation loop reversed (`let i:i32=nr-1;
   while(i>=0 && ans==-2){`, `i=i-1;`).
4. Single-hop path: p loop reversed (same as chain).
5. Sum path: enumeration order unchanged (subset-size descending, mask
   descending already tries newer-fact subsets first); only ungated.
6. k order (2..4), path-type order (chain, sum, count, single-hop)
   unchanged. Zero references to t2_prov_ok remain; is_superseded is
   kept (used by supersede/revise machinery) but unused by the trial.
Net effect: the last verifying candidate in the original enumeration
order is accepted, i.e. the candidate licensed by the most recently
created facts. No liveness or supersession checks anywhere.

## Baseline (c): RANDOM-ANCHOR (bl_random.zag)

Changes vs the H5R2 base:
1. Deleted the t2_prov_ok comment block and helper; added two helpers
   in its place: bl_rng (deterministic LCG, state in the unused W
   header field 52, lazily seeded to 12345; state kept below 65536 so
   s*129+7 never overflows i32; full period 65536) and bl_keep
   (returns 1 with probability 1/nv via repeated-subtraction mod; no %
   operator exists in Zag).
2. t2_trial restructured per prereg: same composition-preserving search
   order (k=2..4 chains, then sums, counts, single hops), but each
   promote site runs single-pass reservoir sampling over the forward
   enumeration and promotes the sampled verifying candidate. The chosen
   candidate's value, graph root, and fact array are copied to bv/br/bf
   before promotion. No provenance gating.
3. No clock or time reads; deterministic by construction (fixed seed,
   header field 52 zeroed by tnn2_init on every run).

## Build (pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1)

- bl_nogate.bin, bl_latest.bin, bl_random.bin: all compiled with zero
  errors (only pre-existing A0102 warnings).
- Built-in battery (run_all, unsealed): (b) 46/46 PASS; (c) 46/46
  PASS; (a) 45/46, F2 FAIL. The F2 test pins masked-query
  disambiguation: with two verifying 2-hop chains and a masked query,
  first-match returns the BFS-first chain (201) while recency returns
  the most recently taught chain (202). This is a real behavioral cost
  of the recency heuristic outside the sealed worlds (whose queries
  are all unmasked), disclosed here and in the eval.

## Sealed world assembly (post-implementation, per prereg 5.2)

For each baseline, four world files: byte-copy of the baseline
substrate with the single line
`fn main()i32 { return run_all(); }` changed to
`fn main()i32 { return sealed_main(); }` (diff-verified: exactly one
line differs), plus the frozen DRIVER_TMPL.zag appended (SHA-256
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af,
extracted from commit 9db334bd4), plus one alias line selecting the
world. World file SHA-256s recorded in EVAL_BASELINE.md before any
run. Each world compiled separately with the pinned znc; 3/3 runs;
full-stdout SHA-256 compared (CB-3).

## Deviations from the prereg

None.

## Process

PATH was $HOME/safebin for every command. `which python3` printed
nothing (exit 1) at lane startup and at every check. Shell invoked
only: the pinned znc, built binaries, git read-only ops (show/diff),
and file copies. Zero forbidden-executable invocations. No push. No
files written outside the lane directory and /tmp scratch.
