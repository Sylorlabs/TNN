# NAMECHECK.md -- IVWC-PERBUCKET Worker

## Step 0: Toolchain Guard (mandatory, executed at worker startup)

Executed 2026-10-03 at worker startup:

```
export PATH="$HOME/safebin"
which python3   # returned NOTHING (rc=1)
which python    # returned NOTHING (rc=1)
which znc       # /home/hatch/safebin/znc -> pinned znc_linux_x86_64_abed8aa1
```

Result: safebin active at /home/hatch/safebin, no forbidden
interpreter reachable. `cmp` confirmed the safebin znc is
byte-identical to
`~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the binary IVWC-HYBRID used). All scientific computation in pure
Zag via the pinned znc. Shell only for: znc invocation, binary
runs, sha256sum, read-only greps, file moves, git ops. Any
forbidden executable invocation would be PROCESS-FAIL; none
occurred. Guard status: ACTIVE.

## Step 1: Task identity

IVWC-PERBUCKET (subagent, 2026-10-03, non-ledger task; claim
minting paused). Follows IVWC-HYBRID (BUILD-FAIL K5/K6/K7):
the hybrid (bias-corrected internal prediction C = P - bias_bkt,
PASS iff C >= T_hyb) repairs one pure-approach error per regime
but introduces one bar-boundary error per regime on exact ties
(s=10@15: adj=21 == thyb=21; s=5@45: adj=17 == thyb=17), landing
9/12 on both regimes -- never strictly best. This wave tests the
report's own suggested follow-up: can per-bucket bars or a bar
margin rescue the hybrid to strict dominance (beat OF
in-distribution AND beat X3 under law change)? A negative result
is valid, with the mechanism shown.

Lane: `docs/lab/research-lead/overnight-20260928/ivwc_perbucket/`.
Prereg: ivwc_perbucket/PREREG.md (frozen kill bars K1..K11,
committed alone before implementation).
Implementation: ivwc_perbucket/src/ivwc_perbucket.zag (pure Zag,
single file; world/belief/composer/stepper/verifier copied
verbatim from ivwc_hybrid.zag; sealed worlds and train cases
bit-identical).

Branch note: stays on tnn-native-lab (shared checkout), commits
only its own lane directory with explicit pathspecs, local only,
never pushed. Git writes via /usr/bin/git directly (safebin git
symlink is known-broken for writes).

## Step 2: Work plan

1. Freeze PREREG.md + this NAMECHECK.md, commit ALONE (prereg
   commit, explicit pathspec). Verify prereg commit strictly
   precedes the implementation commit.
2. Write src/ivwc_perbucket.zag (pure Zag). NO probe of any kind
   was run before the prereg: the margin-variant prediction
   (10/12 @15, 10/12 @45) is derived from the published hybrid
   per-case analysis in the hybrid REPORT.md, not from any
   execution; the per-bucket variant's outcome is not derivable
   from published data (sealed per-bucket C means are unknown).
   The hybrid's committed runs/*.txt were NOT read (they would
   reveal per-case sealed triples and destroy the experiment's
   blindness). K3/K4 anchors are hand-verified against published
   numbers; K5-K11 directions are theory-fixed per PREREG
   section 6.
3. Build with pinned znc, run 3x, sha256 determinism check (K2).
4. Run frozen shell audits A1-A7.
5. Write REPORT.md with verdict and numbers, commit
   implementation + binary + runs + report with explicit
   pathspecs. Local only, never pushed.

## Step 3: Zag pitfall checklist

u8-backed cells with get32/set32/get8/set8 (copied helpers); no
_zag_print for dynamic content (single ob buffer, one raw-syscall
flush); no `as *i32` slice construction; no `&`/hex; LCG mod
65536; if nesting kept shallow with hoisted flag lets; no
`!(A && B)` in while conditions (De Morgan where needed); integer
arithmetic only; token hygiene in source AND comments (no
expected|answer|key|target or correct|reference_plan|gold
substrings -- "correctly" and even "monkey" are banned by
substring). Signed i32 division for bias/bar means (deterministic;
counts guarded against /0).
