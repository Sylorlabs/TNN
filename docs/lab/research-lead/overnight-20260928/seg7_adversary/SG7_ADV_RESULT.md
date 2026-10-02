# H-SEG7 RED TEAM RESULT: SURVIVES (all 4 attacks fail)

**Date:** 2026-09-30 UTC
**Attacker:** H-SEG7 Red Team (independent subagent)
**Target:** H-SEG7 SURVIVES (4/4). Builder result commit `617957e69`,
builder prereg `5e5f0b9bb`.
**Stance:** Assumed the repair claim false; attacked it. It held.
**Verdict:** SURVIVES. X-SG7-1 PASS, X-SG7-2 PASS, X-SG7-3 PASS,
X-SG7-4 PASS. Classification unchanged: bounded L2
structural-learning repair (budget widening + honest overflow
signaling). Not L3.

## Lineage and governance

- Adversary prereg `PREREG_SG7_ADV.md` committed ALONE as
  `7c56eb3b3` BEFORE any attack code was written, any build ran,
  or any test executed. No amendments.
- Mechanism region for the attack harness: lines 1..519 of
  `seg7_learn.zag` (everything before `fn main` at line 520),
  extracted from git HEAD and cmp-verified byte-identical
  against the working tree. Only the harness `main()` is
  adversary-written.
- Pure Zag throughout: .zag sources, znc builds, shell
  grep/sed/cmp/md5/diff. Zero Python at any stage.
- Builds in /tmp/sg7adv only. No binaries committed.
- Only `seg7_adversary/` paths staged/committed. `seg7_learn.zag`,
  `SEG7_RAW_OUTPUT.txt`, `SEG7_RESULT.md`, `PREREG_SEG7.md`
  untouched.
- No em dashes in loop documentation (byte-checked).

## What was attacked

The H-SEG7 provable label semantics for the widened 64-digit
budget (B = 10^576):

- C1: ovf==0 implies printed NOPT equals the true count T_n
  exactly.
- C2: ovf==1 implies printed NOPT equals T_n mod 10^576, labeled
  loudly.
- C3: the flag fires iff a top carry was dropped during
  accumulation.
- C4: no silent behavior changes vs SEG6 outside R1-R6.

## Attack X-SG7-1 (near-boundary): PASS

Pinned the exact 10^576 boundary the builder straddled but never
pinned (builder ran k=958 exact and k=1915 overflow; the boundary
pair k=1914/k=1915 was never executed). On the H1 corpus,
"ab" x k has T = 2^(k-1) (validated: H1-T gives 2^29 for k=30).

Independent pure-Zag repeated-doubling anchor (no DP, no corpus,
different code path) confirms: 2^1913 has 576 digits and uses 64
base-1e9 digits (< 10^576); 2^1914 has 577 digits and uses 65
base-1e9 digits (> 10^576). So "ab" x 1914 is the largest exact
count in this family and "ab" x 1915 the smallest overflow.

Results (mechanism vs independent 256-digit reference, all
byte-exact):

- B1 "ab" x 1914 (n=3828): NOPT = 2^1913 exactly (576 digits),
  ZERO markers. No false positive on the largest exact count.
- B2 "ab" x 1915 (n=3830): exactly one TRUNCATED-BUDGET-EXCEEDED
  marker + one SAT-BUDGET-OVERFLOW line; NOPT = 2^1914 mod 10^576
  byte-exact. No false negative on the smallest overflow.
- B3 "ab" x 1916: flagged, residue = 2^1915 mod 10^576 exact.
- B4 "ab" x 2000: flagged, residue = 2^1999 mod 10^576 exact.
- B5 "ab" x 1914 + "q" (mixed fallback edge at the boundary):
  exact 2^1913, zero markers.
- B6 "ab" x 958: NOPT byte-equal to committed SG7-BIG section
  AND to independent 2^957; zero markers.
- B7 "ab" x 30: NOPT = 536870912 = 2^29.

Kill criteria were: false positive on B1, false negative on
B2/B3/B4, residue mismatch anywhere, cross-check mismatch on
B6/B7. None met.

## Attack X-SG7-2 (overflow-flag spoofing / false negatives): PASS

Differential battery of 13 inputs against the independent
256-digit exact counter (separately written big-add, 10^2304
budget with a hard assertion that no carry ever escapes 256
digits; the assertion never fired). For every input the pair
(flag, value) matched exactly:

- flag=0 (9 inputs): mechanism NOPT byte-equal to the true
  count, no markers.
- flag=1 (4 inputs: B2, B3, B4, P1): true count >= 10^576
  confirmed, mechanism NOPT byte-equal to true count mod
  10^576, exactly one marker + one overflow line each.

Kill criteria were: flag=0 with wrong value (silent wrong
count), flag=1 with corrupt residue. None met. 13/13 PASS.

## Attack X-SG7-3 (conservative-flag edge): PASS

Hunted false positives: inputs where the flag fires but the true
count is < 10^576, which would break the claimed "iff"
semantics. Probes:

- B1/B5 (largest exact counts, sharpest false-positive risk):
  flag correctly 0.
- P1 ("ab" x 2000 + "xab", huge prefix with chunk suffix):
  flag=1, true count = 2^1999 >= 10^576, residue exact.
  True positive.
- P2 ("ab" x 1914 + "xab", boundary-exact prefix with real
  chunk matches in the suffix): true count = 2^1913 < 10^576,
  flag correctly 0. The flag did NOT fire merely because the
  input is near the boundary or has complex suffix structure.

Downgrade criteria were: any flag=1 with true count < 10^576,
or flag=0 with true count >= 10^576. None met.

Note on the math: the flag semantics are provably exact, not
merely conservative. Every optimal full segmentation crossing
any accumulated position has an optimal prefix (score equality
forces dp[n] = dp[bnp] + bestcomp(bnp)), so T_n >= T_bnp for
every accumulated position; a dropped carry implies
T_bnp >= 10^576, hence T_n >= 10^576 and the printed residue
genuinely differs from T_n. Conversely T_n >= 10^576 forces a
dropped carry during the final accumulation into bc[n]. The
empirical battery above confirms the implementation is
faithful to this proof on all 13 inputs, including the exact
boundary pair.

## Attack X-SG7-4 (regression): PASS

- Rebuilt `seg7_learn.zag` pristine from git HEAD (cmp-verified
  identical to worktree). 3 consecutive runs byte-identical
  (cmp); md5 `adfa444130bd93a56f000d66817452f7`, byte-identical
  (cmp) to committed `SEG7_RAW_OUTPUT.txt`.
- Re-verified all 4/4 builder behaviors from the pristine
  rebuild: SG7-BIG exact 2^957 with zero markers; SG7-OVF
  exactly one marker + one overflow line with residue
  2^1914 mod 10^576; U1/U2/U3 PASS, zero FAIL; H1-T NOPT
  536870912.
- SEG6 -> SEG7 source diff audited hunk by hunk: every removed
  and added line falls in the preregistered R1-R6 categories
  (header comment, NDIGITS 32->64, `bigint_add_of` + comment,
  ovf declaration, the two `bigint_add_of` call sites, label
  block, SAT-BUDGET-OVERFLOW line, banners, ADD-UNIT block,
  SG7-BIG/SG7-OVF fixtures). No undeclared changes. The void
  `bigint_add` is now used only by the U3 unit check (line 546);
  both accumulation call sites use `bigint_add_of`; `ovf` is
  set only at those two sites.

Downgrade criteria were: any byte difference vs committed raw,
any nondeterminism, any out-of-category diff hunk. None met.

## Determinism

- Mechanism harness: 3x byte-identical,
  md5 `630887cd474e7c41e2f46128b81a2ecc`.
- Independent reference: 3x byte-identical,
  md5 `13cf490732ce97a2560f691df714c3ef`.
- Doubling anchor: md5 `7e5e46acb66a1e710d284fe21701d4ec`.
- Pristine seg7 rebuild: 3x byte-identical,
  md5 `adfa444130bd93a56f000d66817452f7`.

## Honest statement of what was NOT tested

- Inputs with T_n between 2^1913 and 10^576 that are not of the
  "ab" x k form: the corpus families available do not produce
  counts in that interval, so the boundary is pinned by the
  family, not swept continuously.
- Counts above 2^1999 (602 digits): the 256-digit reference
  budget (10^2304) was never stressed; the mechanism's flag
  logic is input-size independent by the proof above.
- The classification (bounded L2, not L3) was not attacked;
  it is inherited from the builder and the H-SEG6 red team.

## Files committed (this result commit)

- `seg7_adversary/PREREG_SG7_ADV.md` (committed alone as
  `7c56eb3b3`)
- `seg7_adversary/adv.zag` (attack harness: byte-verbatim
  mechanism region + adversary main)
- `seg7_adversary/ref.zag` (independent 256-digit reference)
- `seg7_adversary/dbl.zag` (independent doubling anchor)
- `seg7_adversary/SG7_ADV_RAW.txt` (evidence: comparison
  table, md5s, full ref + doubler outputs, diff hunks)
- `seg7_adversary/SG7_ADV_FULL.txt` (full harness output,
  md5 `630887cd474e7c41e2f46128b81a2ecc`)
- `seg7_adversary/SG7_ADV_RESULT.md` (this file)

## Final tally

X-SG7-1 PASS. X-SG7-2 PASS. X-SG7-3 PASS. X-SG7-4 PASS.
**H-SEG7 SURVIVES the red team (4/4 attacks fail).**
