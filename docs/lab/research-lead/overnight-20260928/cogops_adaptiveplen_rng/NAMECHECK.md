# NAMECHECK: cogops_adaptiveplen_rng

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, 2026-10-03:

```
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (empty output before
"guard-check-done"). Safebin active for all subsequent commands.
PATH restricted to $HOME/safebin for the whole session.

Pinned znc: `$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the same pinned binary used by COGOPS-ADAPTIVEPLEN; verified present
before use).

Worktree: `$HOME/workspace/tnn-rsi-gpi3` on branch `tnn-native-lab`.

## Step 1: Scope

- Follow-up to COGOPS-ADAPTIVEPLEN (commits c06ee6d01 prereg,
  0086f982d implementation, 702e15b97 report: verdict INCOMPLETE,
  K4 FAIL informative). This lane does NOT modify that lane; it
  discriminates the K4 FAIL's cause (treatment vs RNG-path artifact)
  with a new matched-RNG experiment.
- Base machinery (interpreter, worlds, graded replay, constructor,
  P1 composite fitness, plen_of) adapted from
  docs/lab/research-lead/overnight-20260928/cogops_adaptiveplen/ap.zag
  (cited in PREREG.md); the ONLY behavioral code added is the
  matched-RNG driver (setup + revise-search + reporting-only
  instrumentation). No change to selection, fitness, operators,
  replay, or worlds.
- Research paper untouched.
- Lane: docs/lab/research-lead/overnight-20260928/cogops_adaptiveplen_rng/
  on branch tnn-native-lab. Non-ledger task (claim minting paused).
  Nothing pushed (local commits only, explicit pathspecs).

## Step 2: Computation

- All research logic in pure Zag, compiled with the pinned znc.
- Shell used only for: invoking znc, running binaries, git
  operations, moving/copying files, and build.sh guard greps.
- No Python, no other interpreter, no calculator, no
  text-processing shortcut for research logic. (Shell text tools
  used only for file assembly/inspection and guard assertions,
  never for scoring or experiment decisions.)

## Step 3: Commit order

- PREREG.md + NAMECHECK.md committed FIRST (this commit), strictly
  before any implementation file. Implementation (rng.zag,
  build.sh, runs, REPORT.md) follows in a later commit.
