# NAMECHECK.md -- IVWC-EXPAND3 Worker (corrected K6/K8 re-run)

## Step 0: Toolchain Guard (mandatory, executed at worker startup)

Re-verified for this follow-up wave (2026-10-03, same session):

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

IVWC-EXPAND3 (subagent, 2026-10-03, non-ledger task). This is the
corrected follow-up to IVWC-EXPAND2 (BUILD-FAIL on K6 and K8, both
diagnosed as defective bar/ablation constructions, mechanisms
intact). Two surgical corrections, everything else identical:

1. K6 ablation fixed: the shuffled-consequence verifier now rotates
   ONLY the eff array (buckets stay put), which genuinely breaks
   the bucket->eff mapping while preserving marginals (T and
   bucket counts unchanged). The expand2 joint rotation was
   permutation-invariant for bucket means and therefore vacuous.
2. K8 bar fixed: degradation of carried verification is now
   measured as the verifier's EDGE over the trivial baseline,
   (acc-maj) at wp=45 < (acc-maj) at wp=15 (strict), instead of
   absolute accuracy. Expand2 showed absolute accuracy conflates
   environment predictability with verifier quality (9->8->10
   while the edge went +2 -> 0 -> -1).

All worlds, seeds, belief noise, composition, consequence
simulator, revision rule, verifier, shift levels (wp=15/30/45),
case identities, and the remaining bars K1-K5/K7/K9 are unchanged
from the frozen expand2 design, so this wave is a clean
correction, not a new experiment.

Lane: `docs/lab/research-lead/overnight-20260928/ivwc_expand3/`.
Prereg: ivwc_expand3/PREREG.md (frozen kill bars K1..K9 with the
two corrections, committed alone before implementation).
Implementation: ivwc_expand3/src/ivwc_expand3.zag (pure Zag, single
file; expand2 source with exactly the two corrections).

Branch note: stays on tnn-native-lab (shared checkout), commits
only its own lane directory with explicit pathspecs, local only,
never pushed. Git writes via /usr/bin/git directly.

## Step 2: Work plan

1. Freeze PREREG.md + this NAMECHECK.md, commit ALONE (prereg
   commit, explicit pathspec). Verify prereg commit strictly
   precedes the implementation commit.
2. Copy ivwc_expand2.zag -> ivwc_expand3.zag; apply exactly two
   edits: (a) shuffled arm rotates seff only (sbkt[t]=tbkt[t]);
   (b) K8 verdict uses edge comparison (acc2-maj2)<(acc0-maj0).
   No other logic changes. Token-hygiene re-check (A3/A4).
3. Build with pinned znc, run 3x, sha256 determinism check.
4. Run frozen shell audits (A1-A5, same as expand2).
5. Write REPORT.md with verdict and numbers, commit
   implementation + binary + runs + report with explicit pathspecs.
   Local only, never pushed.

## Step 3: Zag pitfall checklist

Same as expand2 (copied source): u8-backed cells, no _zag_print
for dynamic content, single syscall flush, no `as *i32` slices,
no `&`/hex, LCG mod 65536, if nesting <= 3, no `!(A && B)` in
while, integer only, token hygiene (no expected|answer|key|target
or correct|reference_plan|gold substrings in the .zag).
