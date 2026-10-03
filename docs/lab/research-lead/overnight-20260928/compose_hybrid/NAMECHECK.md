# NAMECHECK.md -- Compose-Hybrid Worker (hybrid widening: coverage-selective first, blind-retry backstop)

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
- `which znc` -> /home/hatch/safebin/znc

Result: PASS. No python3/python reachable in PATH. All subsequent commands in
this task run with PATH=$HOME/safebin.

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`

Note: /tmp is a 512M tmpfs at 100% use by other workers at startup; this
worker stages no files in /tmp and works inside its lane directory instead.

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden executable during
this task. All scientific computation is pure Zag (znc-compiled binaries).
Shell is used only for: safebin setup, znc invocation, binary execution, git
operations, file assembly (cat), and byte verification (grep/cmp/sha256sum).

## Scope

- Read the compose_widen PREREG/REPORT (WIDEN-COMP, MIXED verdict, D0-D3, arms
  F and C). Do NOT modify the compose_widen lane; work only in
  docs/lab/research-lead/overnight-20260928/compose_hybrid/.
- Freeze PREREG.md + this NAMECHECK.md Step 0 and commit them ALONE before
  any implementation (prereg commit-order self-check).
- Implement the hybrid arm H (R1 coverage-selective widening first, R2
  failure-triggered blind retry as backstop) in pure Zag, plus fidelity
  copies of arms F and C extended to the two new problems D4/D5.
- Problems: D0-D3 replayed from WIDEN-COMP; D4 (hidden pair, no spurious
  miss) and D5 (long blind tail) are new, designed by this worker, frozen in
  PREREG Section 4.
- Run 3x per arm, byte-identical determinism, record sha256.
- Write REPORT.md with verdict per the frozen mapping (HYBRID MATCHES BEST /
  HYBRID FAILS; HYBRID WINS preregistered as unreachable under the
  decomposition theorem).

## Constraints observed

- No new modes, bridges, or handlers. One hybrid composer; R1/R2 are trigger
  rules on learner-observable state, always on, never learner-selected.
- The S2 pin is FROZEN (used, not re-litigated).
- No em/en dashes in documentation (byte-verified before each commit).
- Never inspect sealed-world contents except via the authorized evaluator
  (no sealed worlds in this battery; all worlds frozen in PREREG Section 4).
- Commits LOCAL only, explicit pathspecs, never push, never git reset, never
  amend shared history. Branch: lane-compinteg2-20261002 (shared; explicit
  pathspecs only).
- Other workers' files untouched.
