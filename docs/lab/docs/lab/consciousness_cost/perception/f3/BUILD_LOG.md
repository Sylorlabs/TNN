# F3 DELIBERATIVE-UNTRAINED — build log

Built 2026-09-24 ~06:00 UTC by the perception cost-measurement crew (subagent),
from the frozen prereg
`docs/lab/consciousness_cost/preregs/PERCEPTION_PREREG.md` (§1, frozen
2026-09-24T05:52:53Z — prereg written BEFORE this build).

## Source

`docs/lab/consciousness_cost/perception/f3/`:
- `f3.zag` — copy of `tnn-lab/senses/conscious-perception/forks/deliberative/f2.zag`
  with POLICY-ONLY changes (see below).
- `f1.zag`, `fio.zag`, `substrate/` — byte-identical copies of the F2 fork's
  files (`diff` clean; machinery shared by construction).

## Policy diff vs f2.zag (complete — nothing else changed)

1. `const CONF_BAR:i32=250;` → `const CONF_BAR:i32=900;`
   (naive uncertainty threshold: resense unless near-certain).
2. New `f3_choose_fixed(task,used)`: fixed per-task selector order
   [10,11,12,13] (pitch/colordisc), [10,11,12] (timbre/colorconst), [10,11]
   (motion) — ignores trigger code and background hint. `f2_choose` remains
   in the file but is never called.
3. Main acquisition loop `while(tcode!=TR_NONE && acq<MAX_ACQ)` (trigger-gated,
   hint-guided) replaced by: `if(tcode!=TR_NONE){ exactly F3_FIXED_ROUNDS=2
   acquisitions via f3_choose_fixed }`. CAPTURE ledger trigger name
   "fixed-budget-2".
4. Ledger honesty updates (declarations, not mechanism): P1_PLAN triggers
   string now "NAIVE-uncertain-conf<900;..."; budget "FIXED-2-acq+maxverifydepth2";
   verdict gains `policy=untrained`.
5. Header comment documents the untrained policy.

Triggers, selectors, resamplers, bg scan, adjudication (majority, newest-wins
ties), install-time verification (depth ≤ 2), install/provisional logic,
ledger hash chain — all shared with F2, untouched.

## Build

```
export TMPDIR=~/workspace/tmp_commit
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 f3.zag -o f3_bin --no-analyze
# znc: wrote native binary f3_bin (188429 bytes main, 0 external tools)
```

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).
- Binary SHA-256: `05e5cb791e4db008d95ab9a2908269bc722514f0e194a53be2c4ec94784b554f`
- F2 binary (rebuilt from f2.zag same session, same toolchain) SHA-256:
  `a4ad7c49333e04dfdad17b0827a0063f8b1a5b3f1da0107b49f39e8572931444`
- F1 binary (frozen, pre-existing) SHA-256:
  `68db15216d9dc75a10839212ac5349195248f5ae113a7e37dc336795db8e35a1`

## Smoke tests (post-build, pre-battery)

- `f3_bin <om_p1.pcm>`: 2 fixed rounds (selectors 10,11), final=HIGHER ✓,
  ops_total=10236, policy=untrained.
- `f3_bin <ib_m1.vid>`: 2 fixed rounds (selectors 10,11), final=W ✓,
  ops_total=67584.
- Determinism: the full 14-fixture battery later ran 3× per fixture with
  SHA256-identical contract stdout on all 42 runs (see RAW_RESULTS.md).

## Provenance note

No binaries, `.zagd`, or `.zag-cache` are committed to git. The binary is
re-derivable from `f3.zag` + pinned toolchain with the command above.
