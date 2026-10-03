# NAMECHECK.md -- Compose-Ledger Worker (persistent cross-query missbits ledger)

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
- `which git` -> /home/hatch/safebin/git
- `which znc` -> NOTHING (safebin carries no znc; the pinned compiler is
  invoked by absolute path below, never via PATH)

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

- Read the compose_hybrid PREREG/REPORT (HYBRID MATCHES BEST, R1/R2, D0-D5).
  Do NOT modify the compose_hybrid lane; work only in
  docs/lab/research-lead/overnight-20260928/compose_ledger/.
- Freeze PREREG.md + this NAMECHECK.md Step 0 and commit them ALONE before
  any implementation (prereg commit-order self-check).
- Implement arm P (persistent ledger: U1-U5, priming WTRIG=3, ledger carried
  across Q1/Q2/Q3) and arm N (no-persistence control: frozen hybrid, fresh
  ledger per query) in pure Zag on the D5 world.
- Queries: Q1 seed (s=41, = frozen D5), Q2 transfer (s=42), Q3 staleness
  (s=70); all kin=1, kout=2, exp=2, nm=4. Frozen predictions in PREREG
  Section 5; kill bars K1-K7 in Section 6; verdict mapping in Section 7.
- Run 3x per arm, byte-identical determinism, record sha256.
