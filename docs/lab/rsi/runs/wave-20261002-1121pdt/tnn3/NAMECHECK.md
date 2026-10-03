# NAMECHECK.md - lane TNN3, wave-20261002-1121pdt

Lane: TNN3 (queue item 14: TNN-3 substrate design, trial-reclamation integration).
Branch: lane-tnn3-20261002-1121pdt, worktree
~/workspace/tnn-rsi-work/wave-20261002-1121pdt/tnn3/.
Task: design only (no substrate code changes); committed as docs.

## Step 0: toolchain guard

Safebin setup executed at startup:

```
$ bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```

Guard verification (literal outputs):

```
$ which python3
rc=1 (no output; python3 does NOT resolve in this PATH)
$ which znc
/home/hatch/safebin/znc
```

PURE ZAG ONLY this lane. No Python, no C/C++, no JavaScript, no Rust
anywhere in analysis, verifiers, harnesses, or scratch. A forbidden
interpreter invocation makes this lane's wave automatically
PROCESS-FAIL with measurements quarantined; only clean safebin
reproduction promotes. There are no code executions at all in this
lane: the deliverable is a design document, but any supporting
scratch (if any) would run under the safebin PATH above.

## Standing rules observed

- Commit pathspec limited to the lane branch, lane dirs only:
  docs/lab/rsi/runs/wave-20261002-1121pdt/tnn3/ and lane-local docs.
- Never commit to tnn-native-lab; never rebase; never git reset --hard;
  never push; never Google Drive; no spend/publish/contact/irreversible
  commitments.
- Untracked files in the main worktree belong to other processes:
  read-only, never touched.
- No writes into docs/lab/research-lead/overnight-20260928/scaling_5000_fixed
  or scaling_10000 (live scaling binaries executing there).
- Docs verified with
  bash docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
  before each commit (no em-dashes in loop docs).
- Pinned znc defect workarounds on record for any future Zag work in
  this lane (see AGENTS.md lessons): one preallocated output buffer +
  cursor-returning emit helpers + single _zag_raw_syscall for dynamic
  stdout; no `as *i32` + q[0..n] inside functions; no .len trust on
  cast slices; 2-byte getter for PCM16; flag hoisting with if-nesting
  <= 3; capacity plan problems x 40 + teaching < 1024 nodes; supply
  minimal ev_query since ma_base.zag is not self-contained.
- One-system rule: no new modes/bridges/handlers; new capability needs
  experience leading to new learned state/structure. Protected-core
  boundary unchanged by this lane (design only, nothing implemented).
