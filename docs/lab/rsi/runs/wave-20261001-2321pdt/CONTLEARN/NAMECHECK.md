# NAMECHECK: CONTLEARN learner-ownership probe

Wave: wave-20261001-2321pdt. Lane: CONTLEARN. Date: 2026-10-01.
Worker: phase-1 (prereg only). Pure Zag plus shell orchestration.

## Step 0 (mandatory, first)

Executed before any other work:

```
cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin" && which python3; echo "which-python3-exit=$?"
```

Exact verification output:

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
which-python3-exit=1
```

Result: `which python3` prints nothing (exit 1). Toolchain guard satisfied.
Safebin activated at worker start; all subsequent commands run with
PATH="$HOME/safebin". No forbidden interpreter will be invoked at any stage
(source, znc build, execution, analysis). A forbidden-interpreter invocation
is PROCESS-FAIL by governance rule.

## Phase discipline

- Phase 1 (this commit): prereg only. No implementation in this commit.
- Phase 2 (after coordinator commits prereg alone): implementation, build,
  sealed runs, verdict. Implementation files first appear strictly after the
  prereg commit; verified via `git merge-base --is-ancestor` before any
  verdict is reported.

## No-dash check

Every doc in this lane is checked with
`sh docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`
before commit. No em dashes anywhere in lane documentation.
