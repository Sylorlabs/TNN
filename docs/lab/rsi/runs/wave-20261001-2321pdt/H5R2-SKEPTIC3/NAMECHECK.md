# NAMECHECK: H5R2-SKEPTIC3

Lane H5R2-SKEPTIC3, wave-20261001-2321pdt. Replacement worker for the
H5R2-SKEPTIC2 lane (verdict SKEPTIC-SURVIVES, commit a8d7b18bb).
Task: build the separator world family the skeptic2 lane named:
two live facts on one key without supersession, discriminating
t2_prov_ok (H5R2) from NEWEST-LIVE-ON-KEY.

## Step 0 (worker toolchain guard, first action)

Ran at lane startup, 2026-10-02 ~07:3x UTC:

```
cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"
```

Exact verification output:

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
PATH=/home/hatch/safebin
which python3 exit: 1
```

`which python3` printed nothing (exit 1). python3 does not resolve.
Pure Zag for all research logic; shell only to invoke znc, run
binaries, do git ops, move/copy files. Zero forbidden-executable
invocations at lane startup. This check is re-run before every
implementation and evaluation step and recorded here.

## Commit-order self-check

- PREREG_SKEPTIC3.md freeze commit: (recorded at freeze time below)
- Implementation commit (SEP_FRAG.zag): strictly after prereg freeze
- EVAL_SKEPTIC3.md: strictly after implementation

Prereg freeze: PENDING (this file is committed with the prereg).
