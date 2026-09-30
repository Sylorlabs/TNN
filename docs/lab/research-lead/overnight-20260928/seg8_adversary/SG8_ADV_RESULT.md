# H-SEG8 RED TEAM RESULT: SURVIVES (all 4 attacks fail)

**Date:** 2026-09-29 (PDT)
**Adversary:** H-SEG8 Red Team (independent subagent)
**Target:** H-SEG8 SURVIVES (4/4), builder result commit `5923f16af`
**Verdict: H-SEG8 SURVIVES.** No KILL criterion fired. No DOWNGRADE
criterion fired. Classification remains bounded L2 (adaptive
exactness repair), not L3.

## Preregistration and governance

- `PREREG_SG8_ADV.md` committed **alone** as `79b324819` before any
  attack code, build, or run. Strict ancestry verified:
  `git merge-base --is-ancestor 79b324819 <result>` passes.
- Harness `adv.zag` = lines 1..527 of committed `seg8_learn.zag`
  at `5923f16af` (everything before `fn main`), cmp-verified
  byte-identical against `git show 5923f16af:...`, plus an
  attack-only `main()`. Zero mechanism lines edited.
- Independent reference `dbl.zag` = same 527-line head (for
  `z_alloc`/`set32`/`get32`/`emit_padded9`/`i32s` only) plus an
  owned repeated-doubling big integer (2048 base-1e9 digits, its
  own doubling routine): no DP, no chunk table, no saturation
  logic, no `bigint_add_of`. Different code path from the
  mechanism by construction.
- Pure Zag throughout: zag sources, znc builds, shell grep/cmp/
  md5/diff. Zero Python at any stage. Toolchain pinned:
  `znc 2026.07.0-dev (edition 2026)`.
- Builds in /tmp/sg8adv only; no binaries committed. Only
  `seg8_adversary/` paths staged. No other worker's files
  touched. No em dashes in adversary-authored docs
  (byte-checked: 0 U+2014).

## Attack outcomes

### X-SG8-1 (many doublings): HOLD

Input "ab" x 20000 (n = 40000) on the H1 table. True count
T = 2^19999 = 6021 decimal digits = 669 base-1e9 digits, forcing
the adaptive loop to discard at nd = 64, 128, 256, 512 (4 failed
iterations, twice the doubling depth the builder tested) and
succeed at nd = 1024.

- Printed NOPT is **byte-identical** (`cmp`) to the independent
  reference rendering of the exact 2^19999 (6021 digits).
- Binary exited 0 in 24 seconds, far inside the frozen 900
  second termination budget. Zero FAIL lines. Zero overflow
  markers/lines in output.
- KILL-K1 does not fire (exactness holds after 4 discards).
  DOWNGRADE-D1 does not fire (terminates promptly, no crash).

### X-SG8-2 (discarded-iteration safety): HOLD

(a) Inspection of the committed blob at `5923f16af`: inside the
adaptive loop the only written buffer is `bc` (`set32(bc,0,1)`
and `bigint_add_of` into `bc` blocks). `dp`, `sat`, `cht`,
`unc` are never written (only `get32`/`ch_cnt`/`ch_match`/
`ch_uscore` reads). On ovf==1 the buffer is abandoned and `bc`
is rebound to a fresh `z_alloc((n+1)*nd*4)` before the full
in-order re-accumulation from bi = 0. The failed iteration
cannot poison the successful one by construction.

(b) Behavioral: "ab" x 1915 (1 discarded iteration) prints NOPT
byte-identical to the exact 2^1914; executed twice inside one
process (two `run_exp` calls), both outputs byte-identical (no
cross-call contamination; `bc` is call-local).

- KILL-K2 does not fire.

### X-SG8-3 (termination, degenerate/pathological): HOLD

- The X-SG8-1 4-discard stress input terminates in 24 s (part
  (a), inside budget).
- Degenerate inputs, all exit 0 promptly: "a" (n = 1, NOPT 1),
  "ab" (n = 2, NOPT 1 = 2^0, matches reference), "a" x 5000
  (NOPT 1), "zzz" unseen characters (NOPT 1, fallback path).
- DOWNGRADE-D2 does not fire (no hang, no crash).

### X-SG8-4 (regression and provenance): HOLD

(a) Pristine rebuild: `seg8_learn.zag` extracted from the
committed blob at `5923f16af`, compiled, committed `main()` run
3 times: 3/3 byte-identical, md5
`44a071f08ea8594c66413a32d52817a5`, exactly the builder's frozen
hash. Exit 0.

(b) Diff `seg7_learn.zag` -> `seg8_learn.zag` at `5923f16af`,
audited hunk by hunk: every changed line falls in the
preregistered R1-R4 categories (header comment, NDIGITS comment,
adaptive loop with `while(ovf==1)` wrapper and nd substitution,
label block with overflow-signal removal,
`bigint_print(bc,n*nd,nd)`, H-SEG8 banners, SG7->SG8 ADD-UNIT
renames, SG8-BIG/SG8-HUGE/SG8-XL fixtures). No undeclared hunks.

(c) The builder's K-SG8-1/2/3 NOPT outputs (from the pristine
rebuild) are byte-equal to the red-team reference values for
2^957, 2^1914, and 2^3999. The builder's /tmp reference was
never committed, so this re-verification is independent.

- KILL-K3 does not fire.

## Determinism

- Adversary binary: 3/3 runs byte-identical
  (md5 `6301d182c8a6b4626ed6d9baf57b3054`), exit 0.
- Reference binary: exit 0; digit counts self-consistent
  (6021/577/289/1204/1 digits + tags = 8149 bytes total).
- Pristine builder binary: 3/3 byte-identical (md5 above).

## Causal interpretation

The adaptive repair's exactness certificate (loop exits iff an
iteration ends with ovf==0, and ovf==0 implies no top carry was
dropped in any add, hence every partial sum is exact) survived
the strongest stress I could construct within the machine's
means: 4 consecutive discarded iterations followed by an exact
6021-digit count, byte-identical to a fully independent
computation. The discarded-iteration safety is structural (fresh
allocation per iteration; accumulation writes only `bc`), not
empirical luck. Termination held on every input tried, including
degenerate ones.

## Honest limits of this red team

- The many-doubling attack used the "ab" x k family (counts are
  powers of 2); no available corpus family produces counts
  between 2^1913 and 10^576, same limitation the H-SEG7 red team
  disclosed. Counts above 2^19999 were not tested (machine
  memory bound: the 4-discard run peaked well within the 1.4 GB
  available, but deeper runs were not attempted).
- The nd_final <= 2x digits memory-bound claim was verified by
  code inspection (the loop doubles until the first ovf==0
  iteration; an ovf==0 iteration implies all values fit, so the
  exit nd is below twice the needed digits), not by direct
  observation: nd is not printed.
- Classification (bounded L2, not L3) was inherited, not
  attacked.
- Three independent implementations (mechanism DP, 2048-digit
  doubler, closed-form digit counts) agree on every checked
  value.

## Files (branch `tnn-native-lab`, `seg8_adversary/`)

- `PREREG_SG8_ADV.md` (frozen alone at `79b324819`)
- `adv.zag` (harness: committed mechanism head + attack main)
- `dbl.zag` (independent 2^k reference harness)
- `SG8_ADV_FULL.txt` (full adversary output, md5
  `6301d182c8a6b4626ed6d9baf57b3054`)
- `SG8_ADV_REF.txt` (reference 2^k renderings)
- `SG8_ADV_RESULT.md` (this report)

## Suggested follow-up for parent

The segmentation arc (H-SEG through H-SEG8) has now survived two
consecutive full red teams at its tip (H-SEG7: 4 attacks; H-SEG8:
4 attacks, including a 4-discard exactness stress). Per the
standing mandate (survivor -> replication -> stronger red team ->
transfer -> integration), H-SEG8 is a candidate for transfer /
integration into the continuing learner. A future frontier wave
could test counts beyond 2^19999 on a larger machine, or attack
the inherited H-SEG5 sat/no==999 path, which this red team did
not re-open.
