# NAMECHECK: H2-v2 (generation 2) prereg writer, wave-20261001-1721pdt

Lane: docs/lab/rsi/runs/wave-20261001-1721pdt/H2v2/
Role: Phase 1 prereg writing only. No implementation, no code, no world files.

## Step 0: Toolchain guard (mandatory, executed before any other work)

1. Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   Output (tail):
   ```
   linked: 36 tools
   znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
   verify: python3 absent from safebin PATH (OK)
   verify: python absent from safebin PATH (OK)
   SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
   ```
2. Exported PATH="$HOME/safebin". Resulting PATH: `/home/hatch/safebin`
3. `which python3` returned nothing (exit code 1). Confirmed absent.

Guard status: ACTIVE. No forbidden executable (python3/python/C/node/rust)
was invoked at any point in this lane's work. All subsequent work in this
lane used only safebin tools (coreutils, grep, ls, mkdir).

## Step 1: Context recovered before writing

Prior H2 records and weak K-LT-5 records were read from the repo before
writing the prereg (see lineage section of the prereg):

- H2 prereg frozen `c15a47d63`; H2 evaluation `72173fe11`: H2-EVAL-VOID
  (t2_sig calibration property (ii) failed; trial never ran because
  direct-query facts let activate() short-circuit). VOID preserved.
- H2-v2 generation 1: prereg frozen `84a2a4ddf`; run `8778f1d0b`:
  VALID evaluation, K-H2-1..4 all FAIL on frozen TNN-2 (valid negative
  result; TRIAL_ENTERED=1 on all 8 probes; t2_sig_v2 calibration passed;
  3/3 byte-identical). Recorded honest limitation: worlds normatively
  specified in the prereg from a single design source; the two-family
  post-freeze adversary diversity requirement was NOT met.
- Weak K-LT-5: prereg frozen
  (docs/lab/research-lead/overnight-20260928/weak_klt5/WEAK_KLT5_PREREG.md);
  evaluation `c040e5fde`: WEAK-KLT5-VOID (budget wall invalidates
  protocol; frozen control showed R_frozen = 7.50, killing
  discrimination). VOID terminal.
- H3-lite Node 2: NODE2-REACHABILITY-COMPLETE with verdict UNREACHABLE
  (default never changed from 30). Preserved as a negative finding.

No world files, sealed assets, or prior run outputs were opened or
reused in this lane.

## Step 2: Files written in this lane (Phase 1 only)

- `H2V2_PREREG.md`: fresh H2-v2 generation 2 preregistration (DRAFT).
- `NAMECHECK.md`: this file.

No implementation files were created. No .zag files, no binaries, no
world files, no run outputs, no shell scripts. No git commit, no git
push, no changes to .wave_lock.

## Work plan completed

Phase 1 (prereg writing) is complete. Phase 2 (freeze), Phase 3 (world
building by independent post-freeze adversaries), Phase 4 (evaluation),
and Phase 5 (verdict) are out of scope for this lane.
