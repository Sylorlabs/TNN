# NAMECHECK: H5R2-BASELINE lane process record

Lane H5R2-BASELINE, wave-20261001-2321pdt. Pipeline step 5:
SIMPLE-BASELINE COMPARISON for the TNN3H5R H5R2 mechanism
(BUILD-PASS + REPRO-PASS). Pure Zag; safebin toolchain.

## Step 0: worker toolchain guard (recorded at lane startup)

Commands run (2026-10-02 ~06:4x UTC, lane startup):

```
cd ~/workspace/tnn-rsi
sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3   -> (no output) exit 1
which python    -> (no output) exit 1
```

Exact verification output from the setup script:

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```

`which python3` prints nothing (exit 1); `which python` prints nothing
(exit 1). Guard check: PASS. PATH is $HOME/safebin for every command in
this lane. Any forbidden-executable invocation is automatic
PROCESS-FAIL and will be disclosed.

## Lane directory (write scope)

docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-BASELINE/

Read-only toward the TNN3H5R and H5R2-REPRO lane dirs: committed
sources are extracted with git show from recorded commits only.

## Commit log (this lane)

- (freeze commit goes here): PREREG_BASELINE.md + this NAMECHECK.md
  committed; no implementation artifact exists yet.
