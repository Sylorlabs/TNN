# AMENDMENT-01 — sequence pattern index range (2026-09-20)

Amends `PREREG_SENSES_PHASE2_AUDIO.md` §7 (frozen pre-build, commit
ed5f29bc7931). No other section changes.

## Defect found in the frozen text

§7 states: sequence frame (q,r) uses pattern `k=100+q*4+r` with the §2
formula `pat(k,i) = ((i*(k*7919+17) + k*131 + 7) % 60001) - 30000`,
claimed i32-safe. The claim is FALSE for k ≥ 28:

- k=100: multiplier = 100*7919+17 = 791,917;
  i=7999 → 7999 * 791,917 = 6,334,544,083 > 2,147,483,647 (i32 max).
  Signed overflow in the fixture generator — the exact class of silent
  corruption this program exists to prevent.

## Amendment

Sequence frame (q,r) uses pattern **k = 8+q*4+r** (k = 8..23).

- i32-safety: max multiplier = 23*7919+17 = 182,154;
  7999 * 182,154 = 1,457,049,846 < 2,147,483,647. Safe, with the same
  proof shape as §2.
- Disjoint from the §E single frames (k=0..7): no pattern reuse across
  the 8 round-trip frames and the 16 sequence frames.
- All 16 sequence frames remain pairwise distinct patterns
  (multiplier k*7919+17 strictly increasing in k).

Verify mode rebuilds frame (3,0) with k = 8+3*4+0 = 20 and frame (3,1)
with k = 21, consistent with this amendment.

## What does NOT change

The §2 formula itself, the 16,000 B envelope, the 4×4 sequence shape,
and every check count / expected code / pass criterion in the frozen
prereg. This amendment narrows an under-specified parameter into the
range where the prereg's own safety proof holds. It does not lower any
bar.
