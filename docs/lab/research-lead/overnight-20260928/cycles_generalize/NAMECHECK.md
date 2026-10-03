# NAMECHECK: CYCLES-GENERALIZE

Worker: cycles-generalize. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cycles_generalize/`
Task: test whether GEN-CYCLES's sequences+halting generalizes:
T1 alternating two-structure fixpoint family (frozen mechanism),
T2 data-dependent halting as the operative stop of a winning trial
(frozen mechanism), T3 HALT-kind contract signal (preregistered
additive extension + frozen control + reduction test).

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

From the gen_cycles lane (GEN-CYCLES PASS 2026-10-03):
- gc_uni.zag (frozen sequence-trial mechanism):
  33cbd90db2ce77fb837a6542f70a8758f72e3210d6b9d6d5db4d325b035b03f6
- gc_base.zag (frozen base + STEP class 4):
  0a12cc9a4f9b10fc8c4ce2a2f65294d48d8d402f827ceeb9d3d6126e754cb125
- uni_nomain.zag (frozen U region, main stripped):
  e741ecde990d55345e2fe3aa794c75aa11a8fc5d5c54cf995aa38cb5dfcbb1b3
- cyc_nomain.zag (C403 workload setup region):
  aa28dac4506bfa8dc2a7f821bbb15fff2bdf89dc157c16def1472d97965baea6

Lane copies must match these digests (G8 audit in build.sh).

## Step 2: prereg commit order

- This NAMECHECK.md (Steps 0-2) + PREREG.md commit strictly precedes
  all implementation (new .zag files, builds, runs).
- G1 audits this via git log order.
