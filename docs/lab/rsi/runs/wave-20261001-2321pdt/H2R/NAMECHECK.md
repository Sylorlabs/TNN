# H2R NAMECHECK (wave-20261001-2321pdt, lane H2R, replacement worker)

## Step 0 (toolchain guard, mandatory first)

Executed 2026-10-01 (PDT), before any other work:

```
cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"
```

Setup output:
```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```

Verification command: `which python3` under the safebin PATH.
Exact output: nothing printed; exit code 1 (`which-exit:1`).

Result: PASS. python3 does not resolve. Pure-Zag constraint in force for
this worker. No forbidden interpreter invoked at any point (this file is
updated if that ever changes; a forbidden invocation would be disclosed
as PROCESS-FAIL per the worker toolchain guard).

## Provenance of substrate artifacts (read-only extraction)

The TNN3-SUBSTRATE lane directory was treated as read-only. All substrate
artifacts in this lane were extracted with `git show` from the recorded
commits, never copied from the working tree:

- prereg: commit be112b78faadc672f885237a825054779e35269f
  -> SUBSTRATE_PREREG_ref.md (551 lines, pre-amendment freeze text)
- prototype: commit a11dde4b92527ec29fed940c67f397c3f7f7ac16
  -> substrate_proto.zag (1931 lines, sha256 77303b829516e95489a0c9be97dbbe0d7a1bf8cb84b2b8025591bb609772eede)
  -> substrate_dev_checks.zag (141 lines)
  -> pkg_extract.zag (197 lines, the PKG block)

## Commit discipline

- Branch: tnn-native-lab. No push, ever. Local commits only.
- Commits restricted to docs/lab/rsi/runs/wave-20261001-2321pdt/H2R/.
- Prereg frozen alone first; implementation strictly after (commit-order self-check).
- No git reset --hard, no rebase.
- Frozen tnn2.zag never modified. The prototype substrate (PKG block and
  SUBSTRATE-HOOK lines) is never modified by this worker; the H2R experiment
  is a dev harness appended to a verbatim copy of the extracted prototype.
- No em-dashes in lane docs; every doc checked with
  sh docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
  before commit.
