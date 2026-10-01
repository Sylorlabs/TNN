# NAMECHECK: wave-20261001-1421pdt, lane pi-rev2-step5-baseline (H-PI-REV2 step 5 baseline comparison execution)

Worker: step-5 baseline executor (implements B0/B1/B2 and runs the frozen
revision binary under the frozen step-5 prereg; no commits).

## Step 0: toolchain guard activation (mandatory first act)

Commands executed (safebin PATH exported):

```
bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"
```

Output:

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```

Forbidden-executable verification in the safebin PATH:

```
which python3   -> exit 1 (resolves to nothing)
command -v python -> exit 1 (resolves to nothing)
```

Step 0: PASS. Pure Zag rule acknowledged: no Python anywhere in this
lane (not glue, not analysis, not verifiers, not harnesses). Shell only
for orchestration. Zag idiom noted: no `as *i32` plus `q[0..n]` slice
construction inside functions; u8-backed cells with little-endian
get32/set32 helpers.

## Step 1: prereg tracking and contamination check

- Frozen prereg docs/lab/rsi/runs/wave-20261001-1121pdt/pi_rev2/PREREG_PI_REV2_STEP5_BASELINE.md
  confirmed tracked via `git ls-files`.
- Work dir docs/lab/rsi/runs/wave-20261001-1421pdt/pi_rev2_exec/ was empty
  at lane start: no implementation existed. NOT CONTAMINATED.
- Frozen mechanism source verified before build (see RESULT doc).

## Step 2: forbidden-executable audit (at lane end)

COMPLETE. Executables invoked during this lane, all from the safebin
PATH (python3/python absent by construction): bash, awk, cat, cmp, date,
git, grep, mkdir, mv, sed, sha256sum, stat, tee, wc, znc. No python3,
python, perl, ruby, node, or other interpreter was invoked at any stage
(implementation, build, run, analysis). Build logs containing a
compiler-emitted em-dash (znc A0102 lint text) were moved to /tmp with
hashes recorded in the RESULT doc; the lane is byte-clean for em-dash
and en-dash. No git commit, push, checkout, or branch change was made;
all lane files remain uncommitted on branch tnn-native-lab.

No em-dashes in this documentation.
