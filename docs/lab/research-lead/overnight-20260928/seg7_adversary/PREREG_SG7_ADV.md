# PREREG H-SEG7 RED TEAM (ADVERSARY) - FROZEN

**Date:** 2026-09-29
**Attacker:** H-SEG7 Red Team (independent subagent)
**Target:** H-SEG7 SURVIVES (4/4), result commit `617957e69`,
prereg `5e5f0b9bb`.
**Stance:** Assume the H-SEG7 repair claim is false. Attack it.
**Status:** FROZEN. Committed alone before any attack code is
written, any build runs, or any test executes. Pure Zag only.
No Python at any stage. No em dashes in loop documentation.

## Target claims under attack

From SEG7_RESULT.md, the H-SEG7 repair asserts provable label
semantics for the widened 64-digit budget (B = 10^576):

- C1: ovf==0 implies the printed NOPT equals the true optimal
  segmentation count T_n exactly (exactness certificate).
- C2: ovf==1 implies the printed NOPT equals T_n mod 10^576, and
  the label says so loudly (marker + SAT-BUDGET-OVERFLOW line).
- C3: the flag fires iff a top carry was dropped during
  accumulation (claimed exact, described as conservative).
- C4: all K-SG6-1..K-SG6-3 behaviors unchanged except the
  preregistered categories (banners, ADD-UNIT lines, SG7-BIG,
  SG7-OVF sections).

## Frozen boundary arithmetic (adversary-pinned)

On the H1 corpus, "ab" x k (n = 2k chars) has T = 2^(k-1):
validated by H1-T ("ab" x 30 -> 2^29 = 536870912) and SG7-BIG
("ab" x 958 -> 2^957, 289 digits).

- 2^1913: 1913 * log10(2) = 575.87 -> 576 decimal digits.
  10^576 has 577 digits, so 2^1913 < 10^576. "ab" x 1914 is the
  LARGEST exact count in this family (builder never tested it).
- 2^1914: 1914 * log10(2) = 576.17 -> 577 decimal digits >
  10^576. "ab" x 1915 is the SMALLEST overflow in this family
  (builder tested this as SG7-OVF).
- Digit counts above are cross-checked by an independent
  pure-Zag repeated-doubling reference (different code path from
  the mechanism), never committed, /tmp scratch only.

## Attacks (frozen)

### X-SG7-1 (Near-boundary: forged near-boundary counts)

Pin the exact 10^576 boundary the builder straddled but never
pinned (builder tested k=958 exact and k=1915 overflow; the
boundary pair k=1914/k=1915 was never run).

Battery (all on the H1 corpus, via an adversary harness whose
mechanism region is lines 1..519 of seg7_learn.zag extracted
byte-verbatim from git HEAD and verified by cmp, plus an
adversary-written main):

- B1: "ab" x 1914 (n=3828). True T = 2^1913 < 10^576.
  Expect: NOPT byte-equal to independent 2^1913, ZERO overflow
  markers.
- B2: "ab" x 1915 (n=3830). True T = 2^1914 > 10^576.
  Expect: exactly one TRUNCATED-BUDGET-EXCEEDED marker and one
  SAT-BUDGET-OVERFLOW line; NOPT byte-equal to independent
  (2^1914 mod 10^576).
- B3: "ab" x 1916 (n=3832). True T = 2^1915.
  Expect: markers present; NOPT byte-equal to independent
  (2^1915 mod 10^576).
- B4: "ab" x 2000 (n=4000). True T = 2^1999.
  Expect: markers present; NOPT byte-equal to independent
  (2^1999 mod 10^576).
- B5: "ab" x 1914 + "q" (n=3829, mixed fallback edge at the
  boundary). True T = 2^1913 (suffix uniquely segmented).
  Expect: exact NOPT, ZERO markers.
- B6: "ab" x 958 cross-check vs committed SG7-BIG section:
  NOPT byte-equal to the raw file's SG7-BIG NOPT line.
- B7: "ab" x 30 cross-check vs committed H1-T: NOPT = 536870912.

**Kill criteria:** KILL if B1 shows any overflow marker (false
positive on the largest exact count), or B1 NOPT != independent
2^1913; KILL if B2/B3/B4 lack the markers (false negative), or
any residue != the independent modular value. DOWNGRADE if B6/B7
cross-checks mismatch the committed raw (evidence inconsistency).

### X-SG7-2 (Overflow-flag spoofing / false negatives)

Differential battery against an INDEPENDENT pure-Zag exact
counter (ref.zag, adversary-written): H1 corpus training + DP
scores via the validated score logic, but a separately written
256-base-1e9-digit exact counter (budget 10^2304, far above any
battery input) with an assertion that no top carry is ever
dropped at 256 digits, printing the full exact decimal count.
Different accumulation code path from the mechanism.

Inputs: B1..B5 above, plus small handcrafted H1 strings
("xab", "yabzab", "wababxab", "zabzab") for sanity.

For every input, with M = mechanism (NOPT value, flag) and
R = independent true count:

- flag=0 requires M.value == R exactly.
- flag=1 requires R >= 10^576 AND M.value == R mod 10^576.

**Kill criteria:** KILL on any input where flag=0 but
M.value != R (silent wrong count), or flag=1 but
M.value != R mod 10^576 (corrupt residue).

### X-SG7-3 (Conservative-flag edge: false-positive hunt)

The result claims the flag "fires iff a top carry was dropped",
which by the accumulation math implies flag=1 can only happen
when the true T_n >= 10^576 (every optimal full path has an
optimal prefix, so T_n >= T_bnp for every accumulated position;
a dropped carry implies T_bnp >= 10^576). Hunt for a
counterexample: any input where the mechanism fires the flag
but the independent true count is < 10^576. Probes:

- B1 and B5 (largest exact counts: the sharpest false-positive
  risk).
- P1: ("ab" x 2000) + "xab" (huge prefix count, complex suffix
  chunk interactions; exercises accumulation across mixed
  optimal edges). Expect flag=1 with residue == R mod 10^576;
  a flag=1 with R < 10^576 would be the kill.
- P2: "ab" x 1914 + "xab" (boundary-exact prefix, suffix with
  real chunk matches). Expect flag=0 iff R < 10^576.

**Downgrade criteria:** DOWNGRADE (not kill: the signal still
fires loudly, but the provable "iff" semantics are false) if
any input yields flag=1 with R < 10^576, or flag=0 with
R >= 10^576.

### X-SG7-4 (Regression: silent changes)

- Rebuild seg7_learn.zag pristine from git HEAD in /tmp.
  Run 3x. All 3 runs byte-identical (cmp) to each other and
  byte-identical to committed SEG7_RAW_OUTPUT.txt
  (md5 adfa444130bd93a56f000d66817452f7).
- Diff seg6_learn.zag vs seg7_learn.zag from git HEAD:
  every hunk must fall in the preregistered R1-R6 categories
  (header comment, NDIGITS, bigint_add_of + comment, ovf
  declaration, two call sites, label block, overflow line,
  banners, ADD-UNIT block, SG7-BIG/SG7-OVF fixtures).
- Re-verify the 4/4 builder behaviors from the pristine
  rebuild: SG7-BIG exact 2^957 with no markers, SG7-OVF one
  marker + one overflow line with residue == 2^1914 mod 10^576,
  U1/U2/U3 PASS with zero FAIL, H1-T NOPT 536870912.

**Downgrade criteria:** DOWNGRADE on any byte difference vs the
committed raw, any 3x nondeterminism, or any diff hunk outside
the preregistered categories.

## Methodology (frozen)

1. Mechanism extraction: `git show HEAD:<seg7 path> | head -519`
   (lines 1..519, everything before `fn main` at line 520),
   cmp-verified against the working tree file's first 519
   lines. Adversary main() appended in /tmp only.
2. Reference: independently written ref.zag (256-digit exact
   counter), /tmp only.
3. Comparison: shell grep/cmp/md5/diff on program text output.
   Raw evidence preserved in SG7_ADV_RAW.txt.
4. Builds in /tmp/sg7adv only. No binaries committed.
5. Determinism: every battery input run 3x, cmp byte-identical.
6. Pure Zag: .zag sources, znc builds, shell text tools only.
   No Python at any stage.

## Verdict rule (frozen)

H-SEG7 SURVIVES iff X-SG7-1..X-SG7-4 all PASS under the kill /
downgrade criteria above. Any KILL criterion met -> H-SEG7
KILLED. Any DOWNGRADE criterion met (and no kill) -> H-SEG7
DOWNGRADED. The classification (bounded L2) is not under
attack; only the repair's correctness and label semantics are.

## Governance (frozen)

- This prereg committed alone before any attack code, build,
  or run.
- Only seg7_adversary/ paths staged/committed by the red team.
- seg7_learn.zag, SEG7_RAW_OUTPUT.txt, SEG7_RESULT.md,
  PREREG_SEG7.md untouched.
- No em dashes in loop documentation (byte-checked before
  commit).
