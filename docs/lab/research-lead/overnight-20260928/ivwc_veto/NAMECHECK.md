# NAMECHECK.md -- IVWC-VETO Worker (verifier veto / selective execution)

## Step 0: Toolchain Guard (mandatory, executed at worker startup)

```
export PATH="$HOME/safebin"
which python3   # returned NOTHING (rc=1)
which python    # returned NOTHING (rc=1)
```

Result: safebin active at /home/hatch/safebin, no forbidden
interpreter reachable. Builds use the pinned compiler at its
explicit repo path
`~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
All scientific computation in pure Zag via the pinned znc. Shell
only for: znc invocation, binary runs, sha256sum, read-only greps,
file moves, git ops. Any forbidden executable invocation would be
PROCESS-FAIL; none occurred. Guard status: ACTIVE.

## Step 1: Task identity

IVWC-VETO (subagent, 2026-10-03, non-ledger task; claim minting
paused). Natural next step from IVWC-EXPAND3 (BUILD-PASS K1-K9):
the verifier predicts PASS/FAIL but never acts on it. This wave
tests VERIFIER VETO (selective execution): the learner vetoes
low-verdict plans (does not execute them) and executes only
high-verdict plans.

Three questions:
1. Does selective execution improve outcomes? (fewer wasted
   executions? higher success rate among executed plans?)
2. What is the veto threshold? Learner-computed T (from train
   consequences) vs fixed researcher-written rules (strict
   "only bucket 1 executes"; lax "veto only empty bucket").
3. Does vetoing interact with law change? (wp=15/30/45 dial;
   does veto help under degradation where the verifier's
   accuracy edge went +2 -> 0 -> -1?)

World, beliefs, composition, consequence simulator, verifier, and
seeds are bit-identical to IVWC-EXPAND3 (incorporated by
reference: ivwc_expand3/PREREG.md sections 2-4, ivwc_expand3
REPORT.md). The sealed (bucket, eff) pairs are therefore
bit-identical to expand3's; the V-line data from expand3's run1
is used ONLY to calibrate prereg bar directions (prior data, not
a substitute for the fresh run). New: the veto-commit phase, the
three veto policies, per-policy accounting, and bars K1-K8.

Lane: `docs/lab/research-lead/overnight-20260928/ivwc_veto/`.
Prereg: ivwc_veto/PREREG.md (frozen kill bars K1..K8, committed
alone before implementation). Implementation:
ivwc_veto/src/ivwc_veto.zag (pure Zag, single file).

Branch note: stays on tnn-native-lab (shared checkout), commits
only its own lane directory with explicit pathspecs, local only,
never pushed. Git writes via /usr/bin/git directly (safebin git
symlink breaks object writes; AGENTS.md lesson).

## Step 2: Work plan

1. Freeze PREREG.md + this NAMECHECK.md, commit ALONE (prereg
   commit, explicit pathspec). Verify prereg commit strictly
   precedes the implementation commit.
2. Write src/ivwc_veto.zag (pure Zag): expand3's
   world/learner/verifier copied verbatim; revision and shuffle
   arms removed; veto-commit phase + three veto policies +
   per-policy accounting added. Token-hygiene check (A3/A4).
3. Build with pinned znc, run 3x, sha256 determinism check.
4. Run frozen shell audits (A1-A4).
5. Write REPORT.md with verdict and numbers, commit
   implementation + binary + runs + report with explicit
   pathspecs. Local only, never pushed.

## Step 3: Zag pitfall checklist

u8-backed cells, no _zag_print for dynamic content, single
syscall flush, no `as *i32` slices, no `&`/hex, LCG mod 65536,
if nesting <= 3, no `!(A && B)` in while, integer only, no
`as []f64` len trust, hash-only dedup (n/a here), token hygiene
(no expected|answer|key|target or correct|reference_plan|gold
substrings in the .zag; note "counterfactual" is avoided in
identifiers, use cf_ prefix).
