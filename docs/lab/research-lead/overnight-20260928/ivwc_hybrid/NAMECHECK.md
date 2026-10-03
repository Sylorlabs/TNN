# NAMECHECK.md -- IVWC-HYBRID Worker

## Step 0: Toolchain Guard (mandatory, executed at worker startup)

Executed 2026-10-03 at worker startup:

```
export PATH="$HOME/safebin"
which python3   # returned NOTHING (rc=1)
which python    # returned NOTHING (rc=1)
which znc       # /home/hatch/safebin/znc
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

IVWC-HYBRID (subagent, 2026-10-03, non-ledger task; claim minting
paused). Follows IVWC-EXPAND3 (consequence-trained bucket verifier,
BUILD-PASS K1-K9: 9/12 wp=15, 10/12 wp=45) and IVWC-ORACLE-FREE
(zero-observation internal-model verifier, BUILD-PASS K1-K8: 10/12
wp=15, 8/12 wp=45). The gap this wave fills: the dissociation --
internal prediction wins in-distribution (finer discrimination, 10/12
vs 9/12) but loses under strong law change (8/12 vs 10/12);
consequence training buys robustness. This wave tests whether a
hybrid gets the best of both or inherits the weaknesses.

Lane: `docs/lab/research-lead/overnight-20260928/ivwc_hybrid/`.
Prereg: ivwc_hybrid/PREREG.md (frozen kill bars K1..K9, committed
alone before implementation).
Implementation: ivwc_hybrid/src/ivwc_hybrid.zag (pure Zag, single
file; world/belief/composer/stepper/verifier copied verbatim from
ivwc_expand3.zag and ivwc_oraclefree.zag; sealed worlds and train
cases bit-identical to expand3's).

Branch note: stays on tnn-native-lab (shared checkout), commits
only its own lane directory with explicit pathspecs, local only,
never pushed. Git writes via /usr/bin/git directly.

## Step 2: Work plan

1. Freeze PREREG.md + this NAMECHECK.md, commit ALONE (prereg
   commit, explicit pathspec). Verify prereg commit strictly
   precedes the implementation commit.
2. Write src/ivwc_hybrid.zag (pure Zag). NO pre-prereg probe of
   any kind was run: K3/K4 replication anchors are hand-verified
   against the published expand3/oracle-free runs, and K5-K9 bar
   directions are theory-fixed per PREREG section 5. A tiny
   /tmp language-semantics check (i32 division on negative
   operands, NOT the mechanism) may be run post-prereg if needed
   for implementation safety; it reveals nothing about outcomes.
3. Build with pinned znc, run 3x, sha256 determinism check (K2).
4. Run frozen shell audits A1-A7.
5. Write REPORT.md with verdict and numbers, commit
   implementation + binary + runs + report with explicit pathspecs.
   Local only, never pushed.

## Step 3: Zag pitfall checklist

u8-backed cells with get32/set32/get8/set8 (copied helpers); no
_zag_print for dynamic content (single ob buffer, one raw-syscall
flush); no `as *i32` slice construction; no `&`/hex; LCG mod
65536; if nesting kept shallow with hoisted flag lets; no
`!(A && B)` in while conditions (De Morgan where needed); integer
arithmetic only; token hygiene in source AND comments (no
expected|answer|key|target or correct|reference_plan|gold
substrings -- note "expected" and "correctly" are banned even
inside longer words). Signed i32 division is used for the bias
means (deterministic; counts guarded against /0).
