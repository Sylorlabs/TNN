# NAMECHECK.md: VERDICT-48-DOC lane

Worker identity: VERDICT-48-DOC (replacement documentation worker), wave wave-20261001-2321pdt.

## Step 0: Worker toolchain guard

Executed, before any other work, in ~/workspace/tnn-rsi:

```
sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"
```

Verification output (exact):

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```

`which python3` printed nothing (exit code 1). Guard holds; documentation lane only, shell for git/file ops, no experiments, no Python.

## Scope check

- Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
- Commits local only, restricted to pathspec docs/lab/rsi/runs/wave-20261001-2321pdt/VERDICT-48-DOC/.
- No push. No git reset --hard. No rebase.
- WAVE_RECORD.md and RT-F2V3/ treated read-only (facts copied verbatim, never edited).

## Dash rule

- No em-dashes in any documentation. Verified with check_no_dash.sh before commit.
