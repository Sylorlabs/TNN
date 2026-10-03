# NAMECHECK.md -- Compose-Widen Worker (coverage-directed vs failure-triggered widening)

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

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden executable during
this task. All scientific computation is pure Zag (znc-compiled binaries).
Shell is used only for: safebin setup, znc invocation, binary execution, git
operations, file assembly (cat), and byte verification (grep/cmp/sha256sum).

## Scope

- Read the compose_collapse REPORT/PREREG (C319 SUBSUMPTION), the C325
  reproduction ledger entry, and the C329 S2 pin (empty kind-set reads as
  universal {1,2} in all three admission positions; FROZEN, used not
  re-litigated).
- Freeze PREREG.md + this NAMECHECK.md Step 0 and commit them ALONE before any
  implementation (prereg commit-order self-check).
- Implement the discriminating battery (D0, D1, D2, D3) in pure Zag with two
  arms: F (failure-triggered widening, the frozen U rule) and C
  (coverage-directed selective widening, replacing the blind retry).
- Run 3x per arm, byte-identical determinism, record sha256.
- Write REPORT.md with verdict per the frozen mapping (COVERAGE-DIRECTED WINS /
  FAILURE-TRIGGERED SUFFICES / MIXED with boundary / UNDECIDED).
- Do NOT modify compose_collapse/ or any other lane. Work only in
  docs/lab/research-lead/overnight-20260928/compose_widen/.

## Constraints observed

- No new modes, bridges, or handlers. Each arm has one widening rule, always
  on; the arm difference is the experimental manipulation (two separately
  assembled binaries from one shared base), never a learner-selected mode.
- No em/en dashes in documentation (byte-verified before each commit).
- Never inspect sealed-world contents except via the authorized evaluator
  (no sealed worlds in this battery; all worlds frozen in PREREG Section 4).
- Commits LOCAL only, explicit pathspecs, never push, never git reset, never
  amend shared history. Branch: lane-compinteg2-20261002.
- Other workers' files untouched. Shared checkout used (no lock contention
  observed at startup).
