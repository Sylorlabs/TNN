# PREREG H-SEG8 RED TEAM FROZEN

**Date:** 2026-09-29 (PDT)
**Adversary:** H-SEG8 Red Team (independent subagent)
**Target:** H-SEG8 SURVIVES (4/4), builder result commit `5923f16af`
(builder prereg `44cee8122`). Repair R: adaptive digit budget in
`run_exp` (nd starts at 64 base-1e9 digits; on any dropped top carry
nd doubles and the accumulation re-runs from scratch; the loop exits
only with ovf==0, claimed as the exactness certificate; the SEG7
overflow signal is retired as unreachable).
**Status:** FROZEN. Committed alone before any attack code, build, or
run. Pure Zag at every stage. No Python anywhere. No em dashes in
loop documentation (byte-verified before commit).

## Assumed-false claim under attack

For every input, the printed NOPT equals the exact optimal-path
count T_n (no budget boundary, no truncation mode), and the adaptive
loop always terminates. The builder tested at most 2 doublings
(SG8-XL: 64 -> 128 -> 256) and never tested: (a) many doublings with
several discarded iterations, (b) that a discarded (ovf==1)
iteration cannot poison the successful re-run, (c) termination on
degenerate/pathological inputs, (d) the result against a red-team
owned independent reference.

## Attack harness (frozen design)

`adv.zag` = lines 1..643 of committed `seg8_learn.zag` at
`5923f16af` (everything before `fn main`), cmp-verified
byte-identical against `git show 5923f16af:...`, plus an
attack-only `main()` that trains the H1 table (mode 4, same as the
builder) and calls `run_exp` on the attack inputs below. No
mechanism line is edited. Builds in /tmp/sg8adv only; no binaries
committed.

Independent reference `dbl.zag` (pure Zag, /tmp scratch, never
committed): repeated-doubling big integer with 2048 base-1e9
digits, its own doubling add routine (not `bigint_add_of`), prints
the exact decimal rendering of 2^k for each k the attacks need.
Different code path from the mechanism: no DP, no move
enumeration, no chunk table, no saturation logic.

NOPT extraction: the `NOPT` line following each attack `TEST` tag,
byte-compared with `cmp` against the reference rendering.

## X-SG8-1: adversarial count forcing many doublings

Input: "ab" x 20000 (n = 40000) on the H1 table. True count
T = 2^19999 (6021 decimal digits = 669 base-1e9 digits), so the
adaptive loop must discard at nd = 64, 128, 256, 512 (4 failed
iterations) and succeed at nd = 1024. This is twice the doubling
depth the builder tested.

- KILL-K1: the printed NOPT is not byte-equal to the exact 2^19999
  from the independent reference. Then the ovf==0 exit certificate
  is unsound (a wrong count survived all doublings) and H-SEG8 is
  KILLED.
- DOWNGRADE-D1: the binary does not exit within 900 seconds, or it
  crashes / is OOM-killed. Then "for every input the printed NOPT
  equals T_n" fails operationally and the termination claim fails;
  H-SEG8 is DOWNGRADED (exactness-in-principle unrefuted, but the
  unconditional claim does not hold in practice).
- HOLD otherwise: exact count printed after 4 discarded iterations.

## X-SG8-2: discarded-iteration safety

(a) Inspection of the committed blob at `5923f16af`: inside the
adaptive loop the only written buffer is `bc`; `dp`, `sat`, `cht`,
`unc` are never written; on ovf==1 the buffer is abandoned and
`bc` is rebound to a fresh `z_alloc` before `set32(bc,0,1)` and a
full in-order re-accumulation from bi = 0.

(b) Behavioral: exactness of "ab" x 1915 (1 discarded iteration)
and of the X-SG8-1 input (4 discarded iterations) against the
reference; plus "ab" x 1915 executed twice inside one process (two
`run_exp` calls) to check for cross-call contamination.

- KILL-K2: any NOPT mismatch in (b), or inspection (a) finds a
  write to dp/sat/cht/unc inside the loop or any reuse of the
  failed iteration's buffer. Then a discarded iteration can poison
  the successful one and H-SEG8 is KILLED.
- HOLD otherwise.

## X-SG8-3: termination on degenerate and pathological inputs

(a) The X-SG8-1 input under the 900 second timeout (maximal
doubling stress; the termination proof must survive 4 discards).

(b) Degenerate inputs on the H1 table, each must exit 0 promptly
(300 second budget each; all are tiny): "a" (n = 1), "ab" (n = 2,
T = 2^0 = 1, checked against the reference), "a" x 5000 (long
uniform input; termination only), "zzz" (unseen characters;
termination only).

- DOWNGRADE-D2: any hang past its budget or any crash. Then the
  unconditional termination claim fails and H-SEG8 is DOWNGRADED.
- HOLD otherwise.

## X-SG8-4: regression and provenance

(a) Pristine rebuild: extract `seg8_learn.zag` from the committed
blob at `5923f16af`, compile, run the committed `main()` 3 times:
3/3 byte-identical, md5 equal to the builder's frozen
`44a071f08ea8594c66413a32d52817a5`, exit 0.

(b) Diff `seg7_learn.zag` -> `seg8_learn.zag` at `5923f16af`,
audited hunk by hunk: every changed line falls in the
preregistered R1-R4 categories (header/banners, adaptive loop,
label block, overflow-line removal, ADD-UNIT renames, new
fixtures). No other hunks.

(c) The builder's K-SG8-1/2/3 NOPT outputs (from the pristine
rebuild in (a)) byte-equal to the red-team reference values for
2^957, 2^1914, 2^3999.

- KILL-K3: md5 mismatch in (a) with any behavioral difference,
  any diff hunk outside R1-R4 in (b), or any NOPT != reference in
  (c). Then the committed artifact is not what was tested, or the
  repair scope was misdeclared, or exactness fails on the
  builder's own fixtures; H-SEG8 is KILLED.
- HOLD otherwise.

## Verdict rule

H-SEG8 SURVIVES this red team iff no KILL criterion (K1, K2, K3)
and no DOWNGRADE criterion (D1, D2) fires. Classification
(bounded L2, not L3) is inherited from the builder and the H-SEG7
red team and is not re-attacked here.

## Governance (frozen)

- This prereg is committed alone before any attack code, build,
  or run. Strict ancestry will be verified with
  `git merge-base --is-ancestor` at result time.
- Pure Zag: fixtures, harness, reference, builds, runs, greps,
  md5, cmp, diff. No Python at any stage.
- Only `seg8_adversary/` paths will be staged. No binaries
  committed. No other worker's files touched.
- No em dashes in loop documentation.
