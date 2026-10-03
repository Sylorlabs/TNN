# NAMECHECK.md -- Decline-Gate Adversary

## Step 0: Toolchain Guard (mandatory)

Date: 2026-10-01
Worker: Decline-Gate Adversary (subagent)

Setup executed:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returns nothing (empty output). Guard check passed.
Safebin active. Zero forbidden executables invoked.

## Scope

ADVERSARIAL TESTING ONLY. Unfrozen variant only.

Target: decline gate mechanism from `f3e6985d4` (DYN-1 BENDS).

Task: Build adversarial worlds to attack the decline gate:
1. Late-success world (trial would succeed on attempt 4+, gate withholds after 3)
2. Intermittent world (non-consecutive failures, total-not-consecutive tally)
3. Novel-domain world (decline transfer across domains)
4. Re-engagement world (teach after declines, measure unstick cost)
5. N sensitivity (N=1,2,3,4,5)

Verdict: DECLINE-ADV-COMPLETE (SURVIVES or NEEDS-FIX with specific failures).

## Constraints

- Unfrozen variant only. Frozen TNN-2 source read-only (reference only).
- Pure Zag via pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Shell only for: invoking znc, running binaries, git ops, moving/copying files.
- Zero em dashes and zero en dashes in all documentation (byte-verified).
- Research paper untouched: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`.
- No sealed worlds. Nothing pushed. Commits local only with explicit pathspecs.

## Input Provenance

- Decline gate report: `docs/lab/research-lead/overnight-20260928/decline_gate/DECLINE_GATE.md` (commit `f3e6985d4`)
- Gate cognition: `docs/lab/research-lead/overnight-20260928/decline_gate/dg_gate.zag`
- Base cognition: `docs/lab/research-lead/overnight-20260928/decline_gate/dg_base.zag` (SHA-256 `a29972ca...`, verbatim frozen)
- Driver: `docs/lab/research-lead/overnight-20260928/decline_gate/dg_driver.zag`
- Full variant: `docs/lab/research-lead/overnight-20260928/decline_gate/dg_full.zag`

All inputs read-only. No modifications to source materials.
