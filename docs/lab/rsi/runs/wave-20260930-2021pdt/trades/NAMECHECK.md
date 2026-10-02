# NAMECHECK.md (trades lane, wave 20260930-2021pdt)

## Step 0: Toolchain verification (mandatory, first)

Commands run at startup:

```
$ bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)

$ export PATH="$HOME/safebin"
$ command -v python3
(empty, exit 1)
$ command -v python
(empty, exit 1)
$ command -v znc
/home/hatch/safebin/znc
$ znc --version
znc 2026.07.0-dev (edition 2026)
```

SAFEBIN ACTIVE: python3/python do not resolve in this PATH.

No forbidden executable has been invoked in this lane. If one is invoked,
this lane becomes PROCESS-FAIL and this file will record the incident.
