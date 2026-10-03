# H-SEG9 RED TEAM RESULT (SG9-ADV)

**Date:** 2026-09-29 (PDT)
**Adversary:** H-SEG9 Red Team (independent subagent)
**Target:** H-SEG9 SURVIVES (4/4). Builder prereg `43482e649`,
builder result `1ffa82a68`.
**Verdict:** SURVIVES. All four attacks fail to break the claim.
**Classification:** The H-SEG9 repair (NDINFO observability +
sat-boundary sweep) withstands independent adversarial testing.

## Lineage

- Adversary prereg `PREREG_SG9_ADV.md` committed alone as
  `c7e87bd60` BEFORE any attack code, build, or run. No amendments.
- Prereg is a verified strict ancestor of this result
  (`git merge-base --is-ancestor c7e87bd60 <result>`).
- Attack harness = frozen mechanism region (lines 1..535 at
  `1ffa82a68`, cmp-verified byte-identical) + attack-only main.
  Zero mechanism lines edited.
- Pure Zag throughout: harness, builds, runs, greps, md5, cmp,
  diff, independent reference. Zero Python at any stage.
- Toolchain: `znc 2026.07.0-dev (edition 2026)`. Builds in
  /tmp/sg9adv only; no binaries committed.

## Attack X-SG9-1: Saturation branch (exact-999/1000) - INCONCLUSIVE

**Method:** Attempted to forge inputs with T_n exactly 999 and
exactly 1000 using the frozen H1, ADV-1, ADV-2, and B corpora.
Swept "ab" x k (T=2^(k-1): 2,4,...,8192) and "abab" x k
(T=2^(2k-1): 2,8,32,...,32768). All yielded powers of 2.

**Finding:** The available corpora are structured to produce
powers of 2. Constructing T_n=999 (3^3*37) or T_n=1000 (2^3*5^3)
requires a corpus with non-power-of-2 combinatorics, which is
not available through the frozen run_exp interface without
modifying the mechanism (forbidden).

**Verdict:** INCONCLUSIVE per frozen prereg. The builder's honest
limit ("exact-999 approached from both sides, not constructed
exactly") stands. This is not a downgrade: the K-SG9-1 sweep
(512 vs 1024) already tests the sat/no==999 boundary at its
sharpest available point, and the H-SEG5 proof covers the logic.

## Attack X-SG9-2: Memory bound - HOLDS

**Method:**
(a) Rebuilt frozen SEG9 from git blob. Verified NDINFO pairs:
    SG9-BIG (64,1), SG9-HUGE (128,2), SG9-XL (256,3),
    SG9-K11..K14 (64,1) each. All match builder claims byte-identically.
(b) Verified bound nd <= 2*ceil(D/9):
    HUGE: D=577, ceil(577/9)=65, 2*65=130, nd=128 <= 130. PASS.
    XL: D=1204, ceil(1204/9)=134, 2*134=268, nd=256 <= 268. PASS.
(c) Stress: "ab" x 20000 on H1 (T=2^19999, 6021 digits).
    NDINFO: sat=1, nd=1024, iters=5.
    Bound: ceil(6021/9)=669, 2*669=1338, nd=1024 <= 1338. PASS.
    NOPT byte-identical to independent repeated-doubling reference.
    iters=5 correct (64->128->256->512->1024).

**Verdict:** HOLDS. The memory bound is tight and the (nd, iters)
pairs are exact.

## Attack X-SG9-3: Regression and diff purity - HOLDS

**Method:**
(a) Formal diff: frozen SEG8 blob (`5923f16af`) vs frozen SEG9
    blob (`1ffa82a68`). 16 hunks, all in preregistered categories:
    - Header rewrite (R9d): 1 hunk
    - Comment renames (R9c): 9 hunks
    - `iters` declaration/increment (R9a): 2 hunks
    - NDINFO emit block (R9a): 1 hunk
    - Main banner/tags (R9c): 2 hunks
    - K-sweep insertion (R9b): 1 hunk
    Zero undeclared behavioral hunks.
(b) Rebuilt from git blob, ran 3x. All byte-identical, md5
    `983d78de98b90aa2eeaebda216c8c9b6` x3, exit 0, zero stderr.
    Matches builder raw exactly.
(c) Mechanical transform verification: all 410 non-banner SEG8
    lines (SG8->SG9, H-SEG8->H-SEG9) appear byte-identical in SEG9.
    All 374 extra SEG9 lines categorized: 14 NDINFO (non-K),
    347 SG9-K non-NDINFO, 13 SG9-K NDINFO. Zero unexpected lines.

**Verdict:** HOLDS. The SEG8->SEG9 diff is pure R9a-R9d. No silent
changes.

## Attack X-SG9-4: Capacity limits - HOLDS

**Method:**
(a) Move-list cap analysis: MAXL=5 implies at most 5 predecessors
    per DP position (i-1 through i-5). The cap of 8 is unreachable.
    The builder's claim ("bounds only VERDICT/CAND, never NOPT")
    holds vacuously. The big-int accumulation re-derives edges from
    dp scores and does not use the move list, so NOPT is unaffected
    even in principle.
(b) Large input: "ab" x 20000 (6021 digits) terminates in 36s,
    5 adaptive iterations, exact NOPT verified against independent
    reference. No hang, no crash, no incorrect output.

**Verdict:** HOLDS. Capacity boundaries are as disclosed or
more conservative.

## Summary

| Attack | Target | Result |
|--------|--------|--------|
| X-SG9-1 | Sat branch (999/1000) | INCONCLUSIVE (good-faith effort; honest limit stands) |
| X-SG9-2 | Memory bound | HOLDS (pairs exact, bound tight, stress passes) |
| X-SG9-3 | Regression/diff | HOLDS (pure R9a-R9d, 3/3 deterministic) |
| X-SG9-4 | Capacity | HOLDS (cap unreachable, stress terminates exact) |

**Final:** H-SEG9 SURVIVES the red team. No kills, no downgrades.
The NDINFO observability repair and sat-boundary sweep are
mechanically sound and empirically verified.

## Governance disclosures

1. Prereg committed alone before any attack code; strict ancestry
   verified.
2. Pure Zag throughout; zero Python at any stage.
3. Harness uses frozen mechanism region byte-verbatim; zero
   mechanism lines edited.
4. No binaries committed (builds in /tmp/sg9adv only).
5. Only owned `seg9_adversary/` paths staged/committed.
6. No em dashes in loop documentation (byte-checked).
7. Independent reference (repeated-doubling) kept in /tmp only,
   never committed, by design.
