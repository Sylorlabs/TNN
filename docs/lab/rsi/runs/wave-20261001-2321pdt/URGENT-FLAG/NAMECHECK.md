# NAMECHECK: URGENT-FLAG (replacement worker), wave-20261001-2321pdt

## Step 0: Worker toolchain guard (mandatory first)

- Setup: `sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
- PATH exported: `$HOME/safebin`
- Exact verification output for `which python3` (run from ~/workspace/tnn-rsi after safebin setup):

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
(exit 1 from which python3; no output printed, python3 does not resolve)
```

Result: PASS. python3 absent from PATH. No Python will be used in this lane.
This is a documentation lane; no experiments, no computation. Shell only for git/file ops.

## Lane scope

- Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab (verified via git branch --show-current).
- Write target: docs/lab/rsi/runs/wave-20261001-2321pdt/URGENT-FLAG/ only.
- ESCALATION-UPDATE/ESCALATION_UPDATE.md treated as READ ONLY.
- Never push, never git reset --hard, never rebase. Commits local only with explicit pathspec.
- No em-dashes in docs; verified with check_no_dash.sh before commit.

## Task checklist

- [x] Step 0 safebin setup and python3 absence verification (recorded above)
- [x] Write URGENT_FLAG.md
- [x] Run check_no_dash.sh on URGENT-FLAG dir (exit 0, clean)
- [x] Commit URGENT_FLAG.md + NAMECHECK.md with explicit pathspec
- [x] Final report to parent
