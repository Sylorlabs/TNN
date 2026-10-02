# RT-GOV NAMECHECK (wave-20261001-2321pdt)

## Step 0: worker toolchain guard (mandatory, first)

Command: `cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"`

Verification output (exact):
```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```
Follow-up checks with PATH=/home/hatch/safebin:
- `which python3` printed nothing, exit code 1 (not found)
- `which python` printed nothing, exit code 1 (not found)

RESULT: PASS. Safebin active, no python3/python on PATH. Pure Zag constraint honored for this review wave (reviewer uses shell tools only: grep, sha256sum, cmp, git).
