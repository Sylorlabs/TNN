# Determinism proof (H5 deliberation harness v2, §12 amendment)

Claim: for fixed inputs (items file + depth config), the v2 `delib_harness`
produces byte-identical `results.jsonl` and `ledger.jsonl` on every run —
no RNG, no timestamps, no PIDs anywhere in the decision or output paths.

## How it was proven

`run_determinism.sh` (re-run it anytime; run in a scratch copy — it builds
`delib_harness_det` and `det_*` workdirs next to itself):

1. Rebuilds from source with the pinned znc
   (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`),
   twice; requires the two binaries byte-identical.
2. Runs the 6-item smoke battery **twice** under each depth config
   (`smoke_shallow.cfg`, `smoke_deep.cfg`, `smoke_adaptive.cfg` —
   the adaptive smoke config now uses the frozen values k=3, ε=20, cap=16).
3. Requires `cmp`-clean equality of both output files between the two runs.
4. Runs a malformed-input battery twice and requires `cmp`-clean equality
   of the error-path outputs too.
5. Records SHA256 of every artifact.

The full transcript is `DETERMINISM_LOG_V2.txt` (generated 2026-09-24).

## Result

**PASS.** All comparisons byte-identical:

| Config | results.jsonl SHA256 | ledger.jsonl SHA256 |
|---|---|---|
| shallow | `df405c45…a2fc9c63` | `d0f20a02…7219f39e` |
| deep | `a8db7816…962cf04835` | `075297bf…11d6c0adfc3` |
| adaptive | `b6496048…19028bd19f` | `ee9ede4a…2711d6c0adfc3` |

Binary SHA256 (both builds): `526bccd0c1fb925fa92fcde451091e636df15a35b7daa7dbfd5e4f1c8a23032e`.

## §6 rule unit tests (hand-computed expectations)

Synthetic 2-hypothesis items under the frozen adaptive config (k=3, ε=20,
cap=16), run with the v2 binary:

| Item | Design | Expected | Observed |
|---|---|---|---|
| U-settle5 | conf 100,200,205,210,215,220 → gains 0,100,5,5,5,5 | stop at round 5 | rounds_used=5, cap=0 ✓ |
| U-drop | conf 100,10,15,20,25,30 → signed drop −90 at r=2 | NO stop at r=3 (drops never settle); stop at r=5 | rounds_used=5 ✓ |
| U-cap | conf oscillates 500↔0 for 20 rounds | run to cap 16, cap=1 | rounds_used=16, cap=1 ✓ |

U-drop is the discriminating test: under the OLD (signed, cumulative)
rule the −90 drop would count as settled and stop at round 3; under §6
the absolute gain 90 ≥ ε prevents stopping. The v2 binary stops at
round 5, as §6 requires.
