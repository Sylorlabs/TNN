# PREREG_SG9_ADV.md - H-SEG9 Red Team Preregistration

**Date:** 2026-09-29 (PDT)
**Adversary:** H-SEG9 Red Team (independent subagent)
**Target:** H-SEG9 SURVIVES (4/4). Builder prereg `43482e649`,
builder result `1ffa82a68`.
**Mission:** Independently attack the H-SEG9 repair claim. Assume it is false.

## Frozen verdict rules

- **KILLED:** If any X-SG9-N attack demonstrates the mechanism
  produces a wrong NOPT, wrong sat flag, wrong NDINFO, or violates
  the stated memory bound, H-SEG9 is KILLED.
- **DOWNGRADED:** If an attack narrows a builder claim without
  breaking correctness (e.g., a boundary is sharper than disclosed,
  or a claim holds only in a narrower regime), H-SEG9 is DOWNGRADED.
- **SURVIVES:** If all attacks fail, H-SEG9 SURVIVES the red team.

## Attack X-SG9-1: Saturation branch (exact-999/1000 construction)

**Background:** Builder K-SG9-1 sweeps k=2..14 (T=2,4,...,8192),
showing sat flips between k=10 (512, i32 path) and k=11 (1024,
big-int path). Honest limit: "the exact-999 case is approached
from both sides, not constructed exactly."

**Attack:** Forge inputs where the true optimal-segmentation count
T_n is EXACTLY 999 and EXACTLY 1000, using the frozen H1 corpus
or a constructed variant available through the public run_exp
interface. Verify:
  (a) T_n=999: no==999, sat[n]==0, printed NOPT is "999" via i32 path.
  (b) T_n=1000: no==999 (saturated), sat[n]==1, big-int prints "1000".

**Kill criterion:** If the mechanism prints a wrong value for
T_n=999 or T_n=1000, or sat[n] is incorrect, H-SEG9 is KILLED.

**Downgrade criterion:** If exact-999/1000 cannot be constructed
with the available corpus machinery after good-faith effort, the
attack is INCONCLUSIVE (builder honest limit stands; not a
downgrade).

**Method:** Pure Zag harness. Mechanism region copied byte-verbatim
from frozen `seg9_learn.zag` at `1ffa82a68` (lines 1..527, everything
before `fn main`), cmp-verified. Attack-only main. Independent
reference via repeated-doubling big-int (own code path).

## Attack X-SG9-2: Memory bound (nd <= 2*ceil(D/9))

**Background:** Builder K-SG9-2 asserts NDINFO (nd, iters) pairs:
SG9-BIG (64,1), SG9-HUGE (128,2), SG9-XL (256,3), SG9-K11..K14
(64,1). General bound nd <= 2*ceil(D/9) verified on two fixtures.

**Attack:**
  (a) Independently rebuild the frozen mechanism and verify all
      six (nd, iters) pairs byte-identically.
  (b) Stress: "ab" x 20000 on H1 table (T=2^19999, 6021 digits),
      forcing 4+ doublings. Verify NDINFO (nd, iters) satisfies
      nd <= 2*ceil(D/9) with D read from printed NOPT, and NOPT
      is byte-identical to independent reference.
  (c) Verify iters counts actual loop iterations (no off-by-one).

**Kill criterion:** If any (nd, iters) pair mismatches, or
nd > 2*ceil(D/9), or NOPT is wrong on the stress input, H-SEG9
is KILLED.

## Attack X-SG9-3: Regression and diff purity

**Attack:**
  (a) Formal diff audit: `diff` frozen SEG8 blob (`5923f16af`)
      vs frozen SEG9 blob (`1ffa82a68`). Every hunk must fall in
      preregistered R9a-R9d categories. Any undeclared behavioral
      hunk is a finding.
  (b) Rebuild SEG9 from the git blob (not the worktree). Run 3x.
      Must be byte-identical to builder raw md5
      `983d78de98b90aa2eeaebda216c8c9b6`.
  (c) Verify K-SG9-3: mechanical transform (SG8->SG9, H-SEG8->H-SEG9)
      of SEG8 raw. All 410 non-banner lines must appear
      byte-identical; all extra lines must be NDINFO, K-sweep, or
      banners.

**Kill criterion:** If any undeclared behavioral hunk exists, or
the rebuild mismatches, or the transform verification fails,
H-SEG9 is KILLED.

## Attack X-SG9-4: Capacity limits

**Background:** Builder honest limits: "counts above 2^19999
untested (machine memory bound)"; "move-list cap (8) and 5-candidate
cap bound only VERDICT/CAND, never NOPT."

**Attack:**
  (a) Move-list cap: construct a fixture with >8 optimal moves at
      a single DP position. Verify NOPT remains exact (unaffected
      by the cap) via independent reference. If NOPT is wrong,
      that is a kill.
  (b) Large input: longest feasible "ab" x k within time/memory.
      Verify termination, exact NOPT, and NDINFO bound.

**Kill criterion:** If NOPT is wrong under move-list pressure, or
the mechanism hangs or crashes on a feasible large input, H-SEG9
is KILLED.

**Downgrade criterion:** If a capacity boundary is sharper than
disclosed (e.g., the move-list cap affects NOPT in an untested
regime), H-SEG9 is DOWNGRADED.

## Governance

- This prereg is committed ALONE before any attack code, build,
  or run.
- Strict ancestry verified via `git merge-base --is-ancestor`.
- Harness = frozen mechanism region (lines 1..527 at `1ffa82a68`,
  cmp-verified) + attack-only main. Zero mechanism lines edited.
- Pure Zag throughout. Zero Python at any stage.
- No binaries committed. Only `seg9_adversary/` paths staged.
- Zero em dashes (byte-checked).
