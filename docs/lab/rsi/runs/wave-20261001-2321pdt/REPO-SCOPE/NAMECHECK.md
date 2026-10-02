# NAMECHECK: REPO-SCOPE replacement worker, wave wave-20261001-2321pdt

## Step 0 (worker toolchain guard, mandatory first)

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
$ which python3
(which python3 exit: 1, printed nothing)
```

Toolchain verified: python3 does not resolve under safebin PATH. Pure-Zag constraint active for this worker.
