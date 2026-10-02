# NAMECHECK: C9BAT lane, wave-20261001-2321pdt

Replacement worker for the C9 causal battery. The ARENA2 lane proved
the frozen arena C9 battery is broken by design (all 12 causal
observations satisfy x==y==z by CHECK 1; zero intervention turns; the
true chain is always listed first in discrim items and the key is
chain[0], so the only 3/3 mechanism is format parsing). This lane
builds a CORRECTED causal battery generator as a NEW candidate
instrument. The frozen arena battery stays frozen and untouched.

## Step 0: toolchain guard (2026-10-01 ~23:50 PDT)

Ran from ~/workspace/tnn-rsi:
  sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  export PATH="$HOME/safebin"

Setup output:
  safebin: /home/hatch/safebin
  linked: 36 tools
  znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
  verify: python3 absent from safebin PATH (OK)
  verify: python absent from safebin PATH (OK)
  SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)

Verification:
  $ which python3
  (no output; exit code 1)
  $ which python
  (no output; exit code 1)

`which python3` prints nothing. Pure Zag only for this lane. Any
forbidden-interpreter invocation is PROCESS-FAIL and voids the verdict.

## Task lineage

Read-only sources consulted (never modified):
- docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA2/NAMECHECK.md (C9
  negative finding)
- docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA2/PREREG_ARENA_TRANSFER.md
- docs/lab/research-lead/overnight-20260928/competitive_arena/world_gen.zag
  (C9 emission lines 365-395, 480-525, 910-925; expo format)
- docs/lab/research-lead/overnight-20260928/competitive_arena/ARENA_PREREG.md
  (section 4.3 causal subsystem spec)

## Lane log

- 2026-10-01 ~23:50 PDT: Step 0 toolchain guard recorded. Safebin
  active, python3 absent. Lane directory created.
