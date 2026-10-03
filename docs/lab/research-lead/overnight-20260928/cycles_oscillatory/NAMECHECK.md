# NAMECHECK: CYCLES-OSCILLATORY

Worker: cycles-oscillatory. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cycles_oscillatory/`
Task: test whether GEN-CYCLES/C420's frozen sequences+halting handles
oscillatory cycles: O-Q1 period-2 on-cycle start, O-Q2 tail-entry
lasso (2-step tail + period-2), O-Q3 period-3. Frozen mechanism and
base, zero modifications, zero extensions.

## Step 0: toolchain guard (worker governance)

- Safebin active: `export PATH="$HOME/safebin"` at session start.
- `which python3` returns nothing; `which python` returns nothing
  (verified 2026-10-03 in-lane).
- Pinned znc: /home/hatch/safebin/znc, `znc 2026.07.0-dev`.
- All computational research operations in pure Zag via pinned safebin
  znc. Shell only for znc, binary runs, git ops, file assembly,
  byte-verification (cmp/sha256sum/diff/grep/sed).
- No forbidden interpreter invocation. Any such invocation would make
  this wave PROCESS-FAIL.

## Step 1: frozen source digests (verified before implementation)

From the gen_cycles lane (GEN-CYCLES PASS 2026-10-03), via the
cycles_generalize lane (C420 PASS 2026-10-03):
- gc_uni.zag (frozen sequence-trial mechanism):
  33cbd90db2ce77fb837a6542f70a8758f72e3210d6b9d6d5db4d325b035b03f6
- gc_base.zag (frozen base + STEP class 4):
  0a12cc9a4f9b10fc8c4ce2a2f65294d48d8d402f827ceeb9d3d6126e754cb125
- uni_nomain.zag (frozen U region, main stripped):
  e741ecde990d55345e2fe3aa794c75aa11a8fc5d5c54cf995aa38cb5dfcbb1b3

Lane copies must match these digests (O7 audit in build.sh).

## Step 2: prereg commit order

- This NAMECHECK.md (Steps 0-2) + PREREG.md commit strictly precedes
  all implementation (new .zag files, builds, runs).
- O1 audits this via the lane-local git log order.
