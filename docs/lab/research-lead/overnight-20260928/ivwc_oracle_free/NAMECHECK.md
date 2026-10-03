# NAMECHECK.md -- IVWC-ORACLE-FREE Worker

## Step 0: Toolchain Guard (mandatory, executed at worker startup)

Executed 2026-10-03 at worker startup:

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

IVWC-ORACLE-FREE (subagent, 2026-10-03, non-ledger task; claim
minting paused). Micah's overnight priority #4: "Internal
verification without expected-answer oracle."

Builds on IVWC-EXPAND3 (consequence-trained bucket verifier,
BUILD-PASS K1-K9) and IVWC-VETO (verifier veto, BUILD-PASS K1-K8).
The gap this wave fills: expand3's verifier trains on TRUE
consequences (train plans executed on true worlds). This wave
derives pre-execution self-verdicts with ZERO consequence
observations -- no train phase at all; verdicts from beliefs +
committed plans only, via (Arm A) internal-model consequence
prediction (`belief_execute` on beliefs) and (Arm B)
re-derivation agreement (finding, near-vacuous by analysis),
plus a belief-content ablation mirroring expand3's K6.

Lane: `docs/lab/research-lead/overnight-20260928/ivwc_oracle_free/`.
Prereg: ivwc_oracle_free/PREREG.md (frozen kill bars K1..K8,
committed alone before implementation).
Implementation: ivwc_oracle_free/src/ivwc_oraclefree.zag (pure Zag,
single file; world/belief/composer/stepper copied verbatim from
ivwc_expand3.zag; sealed worlds bit-identical to expand3's).

Branch note: stays on tnn-native-lab (shared checkout), commits
only its own lane directory with explicit pathspecs, local only,
never pushed. Git writes via /usr/bin/git directly.

## Step 2: Work plan

1. Freeze PREREG.md + this NAMECHECK.md, commit ALONE (prereg
   commit, explicit pathspec). Verify prereg commit strictly
   precedes the implementation commit.
2. Write src/ivwc_oraclefree.zag (pure Zag). Pre-prereg /tmp probe
   (uncommitted) confirmed bar non-degeneracy only; directions are
   theory-fixed per PREREG section 5. Final source may differ from
   the probe in print/diagnostic details only (documented).
3. Build with pinned znc, run 3x, sha256 determinism check (K5).
4. Run frozen shell audits A1-A7.
5. Shell cross-check: sealed (bucket, eff) pairs bit-identical to
   ivwc_expand3 run1 (finding, not a bar).
6. Write REPORT.md with verdict and numbers, commit
   implementation + binary + runs + report with explicit pathspecs.
   Local only, never pushed.

## Step 3: Zag pitfall checklist

u8-backed cells with get32/set32/get8/set8 (copied helpers); no
_zag_print for dynamic content (single ob buffer, one raw-syscall
flush); no `as *i32` slice construction; no `&`/hex; LCG mod
65536; if nesting kept shallow with hoisted flag lets (nearest-
first composer); no `!(A && B)` in while conditions (De Morgan
where needed); integer arithmetic only; token hygiene in source
AND comments (no expected|answer|key|target or
correct|reference_plan|gold substrings -- note "expected" and
"correctly" are banned even inside longer words).
