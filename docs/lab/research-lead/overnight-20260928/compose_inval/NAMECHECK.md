# NAMECHECK.md -- Compose-Inval Worker (contract re-teaching, genuine bit invalidation)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null); [ -n "$p" ] && ln -sf "$p" $HOME/safebin/$t 2>/dev/null
done
export PATH="$HOME/safebin"
```

The ambient PATH supplied a non-pinned `znc`; its safebin symlink was
removed (`rm -f $HOME/safebin/znc`) so no znc resolves via PATH. The pinned
compiler is invoked by absolute path only (below), never via PATH.

Verification, run 2026-10-02 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `which znc` -> NOTHING (empty, exit 1; symlink removed)
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

- Read the compose_ledger PREREG/REPORT (C341 PERSISTENT LEDGER HELPS
  (BOUNDED): Q1 2/6/1/2/44, Q2 P 2/3/1/3/44 vs N 2/6/1/2/44, Q3 P
  2/4/1/3/-1 vs N 2/1/0/0/-1; U1-U5 frozen). Do NOT modify the
  compose_ledger lane; work only in
  docs/lab/research-lead/overnight-20260928/compose_inval/.
- Freeze PREREG.md + this NAMECHECK.md Step 0 and commit them ALONE before
  any implementation (prereg commit-order self-check).
- Implement arm P (persistent ledger U1-U5, ledger carried Q1->Q2->Q3P) and
  arm N (frozen hybrid control, fresh ledger per query) in pure Zag.
  Composer fns are byte-copies of the ledger lane; only the world setup
  gains setup_d5x (contract re-teach: teach(A,2,41,44), X.outmask {2} ->
  {1,2}) and main() runs Q1(D5)/Q2(D5)/Q3P(D5X, s=42).
- Frozen predictions in PREREG Section 4; kill bars K1-K7 in Section 5;
  verdict mapping in Section 6.
- Run 3x per arm, byte-identical determinism, record sha256.
