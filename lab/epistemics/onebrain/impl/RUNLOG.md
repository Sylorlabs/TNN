# RUNLOG — Experiment 2 implementer (onebrain)

Workdir: `~/workspace/onebrain/impl/` (all scratch here; nothing in /tmp).
Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (znc 2026.07.0-dev).

## 1. Spec fetch (frozen prereg + reference, from origin via local clone)

```
cd ~/workspace/selfpam_run/tnn-lab
git show 1ab40adceff78d71460b992b078508acea7e8abc:docs/lab/onebrain/PREREG.md \
  > ~/workspace/onebrain/impl/PREREG_FROZEN.md                      # 127 lines
git show 1ab40adceff78d71460b992b078508acea7e8abc:docs/lab/dialogue/deliberation/ARCHITECTURE.md \
  > ~/workspace/onebrain/impl/ARCHITECTURE_REF.md                    # 126 lines
git show 1ab40adceff78d71460b992b078508acea7e8abc:docs/lab/dialogue/deliberation/build/deliberate_frozen_r4.zag \
  > ~/workspace/onebrain/impl/deliberate_v1_ref.zag                 # 4705 lines
```
All three extracted byte-identical from the frozen commit. Prereg kill bars
K1–K6 and the four causal proof protocols are binding; no deviations taken.

Reference files kept in workdir for provenance (NOT shipped as deliverables):
`PREREG_FROZEN.md`, `ARCHITECTURE_REF.md`, `deliberate_v1_ref.zag`,
`R33_NATIVE_IO_V1.zag` (copied from `~/workspace/tnn-lab/toolchain/`;
provides `nio_alloc`/`nio_free` via `@import`).

## 2. Toolchain probe

Wrote `probe.zag` (argv echo + raw-syscall file read). First build failed:
`nio_alloc` unknown — v1 gets it from `R33_NATIVE_IO_V1.zag` via `@import`.
Fix: copied that file into the workdir and added a bare
`@import("R33_NATIVE_IO_V1.zag")`. Rebuilt OK; `_zag_arg(1/2)` and file
read verified working. (`probe.zag`/`probe_bin` retained as scratch.)

## 3. Implementation

Wrote `onebrain.zag` (1358 lines) in 4 chunks: byte helpers/tokenizer/
triggers/KB → ledger + GEN → actions/ELIM/fork/audit/poison → ARGMAX/
driver. New module reusing the v1 ledger geometry (25×552B, turn fields
13804–13820; v1 spare @13816 designated the FORK flag). Zero `as []T`
casts (all tables are []u8 arenas + p32/g32 LE accessors, per the
ZNC-2026-09-21-007 lesson); no structs; no `.*`; no RNG.

`build.sh`:
```
./build.sh
# znc: warning: zagd unavailable; foreground compilation continues without background planning
# znc: wrote native binary /home/hatch/workspace/onebrain/impl/onebrain (133475 bytes main, 0 external tools)
# BUILD OK
```
First attempt failed with one error (`prlen` called with 3 args in
`emit_verdict`); fixed by slicing. Second attempt built clean.
After the poison-hook refinement (see §5) rebuilt clean again
(134881 bytes).

## 4. Smoke problems (invented by the implementer, blind to the frozen set)

`smoke.tsv` (tab-separated, with header row which the parser skips):
- smoke1 `what is the capital of france?` — single reading (plain only)
- smoke2 `forget the joke and compare moby dick and pride and prejudice` — 4 readings
- smoke3 `tell me a joke and remember the louvre` — 3 readings

## 5. Runs

```
./onebrain single  smoke.tsv   # GEN->ELIM->ARGMAX, no fork machinery
./onebrain onebrain smoke.tsv  # full machinery, shared ledger
./onebrain ablate  smoke.tsv   # shared writes OFF (scratch copies)
./onebrain poison  smoke.tsv   # + poison hook between sub-pass rounds
./onebrain min     smoke.tsv   # minimal driver, full machinery
```

Verdict lines (final binary):
- single : smoke1 default/209 fork=0; smoke2 joke/242 fork=0; smoke3 joke/241 fork=0
- onebrain: smoke1 default/209 fork=0; smoke2 compose/227 fork=1; smoke3 joke/241 fork=1
- ablate : smoke1 default/209 fork=0; smoke2 joke/242 fork=1; smoke3 joke/241 fork=1
- poison : smoke1 default/209 fork=0; smoke2 NO_VERDICT fork=1; smoke3 memory/238 fork=1
- min    : identical verdict lines to onebrain (diff clean)

Key trace excerpts (onebrain, smoke2):
```
FORK_ASSESS nread=4 margin=7 fork=1
SUBPASS branch=0 round=0
AUDIT_DENY fact=12 by=6          # forget reading denies the joke fact
AUDIT_CLEAN bid=13 dep=12       # joke bid dies (shared write)
AUDIT_CLEAN bid=15 dep=12       # forget bid dies
AUDIT_CLEAN bid=22 dep=12       # clarify bid dies
SUBPASS branch=1 round=0
AUDIT_DUEL kill=6 by=7 corr=2 vs=0
SUBPASS branch=0 round=1
SUBPASS branch=1 round=1
ARGMAX winner=18 score=227      # compose wins on the shared ledger
```

Poison refinement: first version poisoned the max-q fact; refined to
poison the supporting fact of the current leading bid (most adversarial).
smoke3 then shows the K2 flip:
```
POISON fact=11
AUDIT_CLEAN bid=13 dep=11   # round 2: joke bid eliminated
AUDIT_CLEAN bid=22 dep=11   # round 2: clarify eliminated
ARGMAX winner=14 score=238  # memory wins — branches reacted mid-deliberation
```

## 6. Determinism (K5): 3× reruns, SHA-256 of full stdout

| mode     | run1 | run2 | run3 |
|----------|------|------|------|
| single   | 2f6db326…02825a6b | 2f6db326…02825a6b | 2f6db326…02825a6b |
| onebrain | 6b2c6c5c…852d5f23 | 6b2c6c5c…852d5f23 | 6b2c6c5c…852d5f23 |
| ablate   | 692fa483…06f0dedfa | 692fa483…06f0dedfa | 692fa483…06f0dedfa |
| poison   | 31b32a41…5ff579cf2 | 31b32a41…5ff579cf2 | 31b32a41…5ff579cf2 |
| min      | 2d6e922c…1af5b3b1 | 2d6e922c…1af5b3b1 | 2d6e922c…1af5b3b1 |

Full SHAs:
- single:   2f6db326664525b577631f6134b5bffee77e22ec666d33fe8807c78d02825a6b
- onebrain: 6b2c6c5cc1f4110717b3a85828b46de1729b5a21ee7260fe467ec9fe852d5f23
- ablate:   692fa4833372b3b156b6d8b4c345c97453f0ab612a544084f77406f0dedfa16e
- poison:   31b32a41b24e0bce198f74cd13ea67d3c5ddc400c04c94be0cb25aff579cf288
- min:      2d6e922c012177291a686cd6c09370b26c5c84fd983dcc44789ad2861af5b3b1

All 15 runs byte-identical within mode.

## 7. Neuter test (K5-lesson channel check)

smoke2 — onebrain vs ablate:
- onebrain: winner=18 compose score=227 (shared denial+cleanup applied)
- ablate:   winner=13 joke    score=242 (writes discarded)
Outcome CHANGES → shared-state channel is causal, not decorative. PASS.

## 8. K3 structural check

Grepped driver functions (`main`, `run_full`, `run_minimal`, `solve_one`)
for `fork|fan_out|subpass`: only hit is the `fork_en` MODE-CONFIG parameter
of `run_full` (experiment-arm selection, not a per-problem decision).
`run_minimal` is a bare loop; its verdict lines are byte-identical to
`onebrain` mode and fork=1 fires on smoke2/smoke3 → the machinery fans out
via its own ledger flag. PASS.

## 9. Edge cases

- empty query → assertion "Noted.", no crash
- `???` → withhold "I don't know that one."
- `forget` → forget "Forgotten.", fork=0 (margin 21 > 12)
- unknown mode → usage line, exit 0

## 10. K6 audit

`grep -i "rand\|random\|rng\|srand\|seed"` on onebrain.zag: only two
comments asserting zero-RNG. No RNG in any decision path. PASS.
