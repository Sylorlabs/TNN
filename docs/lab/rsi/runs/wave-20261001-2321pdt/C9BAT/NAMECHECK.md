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
- 2026-10-01 ~23:55 PDT: Prereg PREREG_C9GEN.md frozen and
  committed alone (9e2ea47fc), before any implementation.
- 2026-10-01 ~00:05 PDT: Implemented c9gen/c9gamer/c9exp/c9score
  (pure Zag), committed (4dc4a6d02). Trial in /tmp (seed 12345,
  not the frozen seed) found two bugs, both fixed without
  moving any kill bar: (1) LCG bit-0 parity made the
  candidate-order coin degenerate 24/24 true-first; binary
  draws now use bit 33, edge flips use mod-2000 at p=0.05;
  (2) the Fisher-Yates shuffle via %3/%2 draws reached only
  3/6 chains; replaced by uniform permutation index via
  mod-6000 (prereg amendment A1, committed c2448aa0b before
  validation).
- 2026-10-01 ~00:15 PDT: Frozen validation run (run_dev.sh,
  SEED_DEV=777001337): gamer old 0/24, gamer first 11/24,
  gamer second 13/24, experimenter 24/24, all-UNKNOWN 0/24,
  3/3 byte-identical generation, 0 chain literals, python3
  absent at end. All 8 kill bars PASS. Verdict: GEN-PASS.
  Reports: DEV_VALIDATION.md, JUDGE_BRIEF.md.
