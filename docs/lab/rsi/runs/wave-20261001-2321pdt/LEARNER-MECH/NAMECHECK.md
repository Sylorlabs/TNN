# NAMECHECK: LEARNER-MECH (wave-20261001-2321pdt)

Lane: LEARNER-MECH. Task: root-cause analysis of CONTLEARN-OWNED
MACHINERY-DEPENDENT (analysis lane, no experiments).

## Step 0

Command: `cd ~/workspace/tnn-rsi && sh
docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
&& export PATH="$HOME/safebin"` then `which python3`.

Exact output:

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
which python3 -> (no output, exit 1)
```

`which python3` prints nothing under the safebin PATH. Pure-Zag work only
in this lane; shell for git/file ops.
