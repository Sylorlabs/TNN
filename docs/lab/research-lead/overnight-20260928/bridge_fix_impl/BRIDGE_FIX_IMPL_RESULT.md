# BRIDGE-FIX-IMPL RESULT: Episode-persistent discovery buffer

Status: FIX-BUILT-PASS. No SURVIVES claim.
Prereg: `PREREG_BRIDGE_FIX_IMPL.md` (commit `75231a87e`). Frozen before
implementation.
Parent design: `bridge_fix/BRIDGE_FIX_DESIGN.md` (commit `791388384`).
Parent mechanism: L3 Bridge BRIDGE-TESTED (commit `ebdc4fd3e`).

## Verdict

FIX-BUILT-PASS. All three kill bars pass.

## Kill bars

- K1: PASS. Prereg frozen at commit `75231a87e` (D1-D3, R1-R7, regression
  contract) strictly before any implementation commit. This result file
  and the implementation are committed after.
- K2: PASS. Modified `bridge.zag` built; the full frozen battery output
  is byte-identical to the authoritative BRIDGE-TESTED raw output; the
  frozen C0-A audit M1-M4 passes on the modified source.
- K3: PASS. Pure Zag: no Python used anywhere (source, build, runs,
  diagnostics, byte checks, verification, analysis). No em dashes or en
  dashes in loop documentation. Deterministic: 3/3 byte-identical runs.

## What was built

`bridge_fix_impl/bridge.zag` is the BRIDGE-TESTED `bridge.zag` (commit
`ebdc4fd3e`, SHA-256
`eaeb266a3a781ffc648b2faae4a5b35319c2bde19ac64e974249650be092bc8e`
verified identical before editing) with exactly four changes, all in
`run_family` evidence management (plus a provenance header comment):

1. D3: DISCOVER appends to bs/bo only while n < 40.
2. D1: VERIFY appends every observed example to bs/bo while n < 40.
3. D2: VERIFY strike resets only vc and wrong; n and the buffer are
   retained; the phase returns to DISCOVER.
4. R7: a VERIFY strike on a live invented form (live == 3) ends the
   episode immediately as HONESTFAIL (adopted=-1, done=1).

The full diff against the BRIDGE-TESTED source contains only these four
changes. No construction, search, gain, novelty, refit, teval, family
spec, or battery code was touched. No new operators, no new branches
keyed on pattern type, family identity, output shape, or signature.

## Regression evidence (frozen contract, section 4 of prereg)

- Toolchain: `/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`
  (`znc 2026.07.0-dev (edition 2026)`), same compiler family as the
  BRIDGE-TESTED build.
- Three runs of the unmodified `main()` battery: all exit 0, all
  byte-identical to each other. SHA-256 of each run:
  `4e20f082fc3682808969fb042ae81773405c4a0e990c80315044db05111491a9`.
- Authoritative BRIDGE-TESTED raw output
  (`l3_bridge_impl/BRIDGE_RAW_FINAL.txt` at commit `ebdc4fd3e`):
  SHA-256
  `4e20f082fc3682808969fb042ae81773405c4a0e990c80315044db05111491a9`.
- `diff` of the fixed output against the authoritative output: empty.
  The battery is byte-identical to BRIDGE-TESTED, including K2=1 and
  `VERDICT BRIDGE-TESTED`.
- Interpretation (verified from the comparison, not assumed): no
  BRIDGE-TESTED battery episode strikes an adopted form in VERIFY, so
  D1-D3 leave every frozen trace unchanged, exactly as the design
  predicted.

## C0-A audit M1-M4 on the modified source

- M1: PASS. `sig==1`, `sig==3`, `sig==4`: zero hits. `node_count` and
  `build_tree`: one hit each, both in the carried-over header comment
  explicitly marking deleted legacy code ("REMOVED: ..."), which the
  frozen audit permits.
- M2: PASS. `construct_search(st:[]u8, bs:[]u8, bo:[]u8, n:i32, cost:[]u8)`
  accepts the failure buffer and budgets; no diagnosis enum.
- M3: PASS. Every `setnode` call site (lines 240, 248-251, 259-262, 266)
  lies textually inside `op_const_leaf`, `op_split_lt`, `op_split_eq`,
  or `op_prune`. Line 200 is the `setnode` definition itself.
- M4: PASS. `teval` is byte-identical to the INVENTOR-TESTED commit
  `1b8e032c4` version; it dispatches only on operator codes 0..3.

## What this does NOT claim

- No L3 claim. C0-C and C0-D remain open promotion-pipeline steps.
- The sealed T-ADV5 re-evaluation is NOT run here. It requires a fresh
  prereg under the design's section 8 rules; the worked prediction in
  design section 5 remains design validation, not a result.
- The fix changes protocol evidence management only. Greedy search
  myopia and first-segment capture are out of scope per design
  sections 7.

## Files

- `PREREG_BRIDGE_FIX_IMPL.md`: frozen prereg (commit `75231a87e`).
- `bridge.zag`: fixed implementation (pure Zag).
- `bridge_fix_bin`: compiled binary (build artifact, not for attribution).
- `FIX_RUN1.txt`, `FIX_RUN2.txt`, `FIX_RUN3.txt`: three deterministic
  runs (byte-identical; identical to BRIDGE-TESTED raw).
- `FIX_RUN1.err`, `FIX_RUN2.err`, `FIX_RUN3.err`: empty stderr logs.
- `BUILD_ERR.txt`: compiler log (clean build; one zagd warning only).
- `BRIDGE_FIX_IMPL_RESULT.md`: this file.
