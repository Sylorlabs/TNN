# NAMECHECK.md -- Compose-Beh Worker (behavior-change invalidation, the true poison flavor)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null); [ -n "$p" ] && ln -sf "$p" $HOME/safebin/$t 2>/dev/null
done
export PATH="$HOME/safebin"
```

Verification, run 2026-10-02 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `which znc` -> /home/hatch/safebin/znc (symlink present, but the pinned
  compiler is invoked by absolute path only, below, never via PATH)
- `which git` -> /home/hatch/safebin/git

Result: PASS. No python3/python reachable in PATH. All subsequent commands in
this task run with PATH=$HOME/safebin.

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden executable during
this task. All scientific computation is pure Zag (znc-compiled binaries).
Shell is used only for: safebin setup, znc invocation, binary execution, git
operations, file assembly (cat), and byte verification (grep/cmp/sha256sum).

## Scope

- Read the compose_ledger PREREG/REPORT (C341) and the compose_inval
  PREREG/REPORT (C345 CONTRACT RE-TEACHING LEAVES AN INERT STALE BIT
  (SELF-SHIELDING)). Do NOT modify the compose_ledger or compose_inval
  lanes; work only in
  docs/lab/research-lead/overnight-20260928/compose_beh/.
- Freeze PREREG.md + this NAMECHECK.md Step 0 and commit them ALONE before
  any implementation (prereg commit-order self-check).
- Implement arm P (persistent ledger U1-U5, ledger carried Q1->Q2->Q3B) and
  arm N (frozen hybrid control, fresh ledger per query) in pure Zag.
  Composer fns are byte-copies of the ledger lane; only the world setup
  gains setup_d5b (behavior change: 44 loses subject status so X stops
  emitting NODE at out while every contract mask stays {1}/{2}; A(42)=2
  relocates the answer to admitted single m0) and main() runs Q1(D5) /
  Q2(D5) / Q3B(D5B, s=42).
- Frozen predictions in PREREG Section 4; kill bars K1-K7 in Section 5;
  verdict mapping in Section 6.
- Run 3x per arm, byte-identical determinism, record sha256.
