# Red-team attack plan (prereg, 2026-09-26)

Target: adoption commit `94625817c6f65e07c4ac99abde5dd533f0e810a5`,
mechanism `docs/lab/strength-pricing-meter-adoption/src/strength_core.zag`.
Law S-D6: one citation funds one destruction store-wide; consumed citations
stay tombstoned forever. Pure Zag, zero RNG, pinned toolchain
`znc_linux_x86_64_abed8aa1`.

## Class R1 — resurrection after slot reuse (120 sequences)
Destroy a strong memory with citation set E (kill_evidenced and delete_strong).
Re-add a new judgment into the reused slot number. Re-cite E (plus f < price
fresh top-ups in 4 attack modes, 1 honest control mode). Oracle: the second
destruction must return 121 (consumed), never OK. The honest control (full
fresh payment) must succeed — the battery is not vacuously failing.
Skeletons: 12 (prices 1..4, incl. overwrite-lineage variants).

## Class R2 — cross-slot double-spend (128 sequences)
Cite E on slot A and slot B (4x4 price combos, pa/pb in 1..4). Destroy A
(consumes E store-wide under GLOBAL cite mode). B's destruction must return
121, never OK. Both cite orders (B-cited-before-A-destroyed, B-cited-after),
both destroy ops on each slot.

## Class R3 — weakening + framing (108 sequences)
12 skeletons x 9 framings (JUSTIFY tiers 1..7, no-justify, multi-justify).
Identical stores; meter price must be identical across all framings: JUSTIFY
tier is not a meter input, and high-water + fought history must survive WEAKEN.
Oracle: all 9 prices equal the tier-1 price, which equals the predicted price.

## Class R4 — overwrite-reset (105 sequences)
5 strengths x 3 overwrite-target strengths (always <= original, so the
attacker cannot raise high-water) x 3 sunk levels x 2 fought levels (+15 pure
revision overwrites). Oracle (security): post-overwrite price >= pre-overwrite
price — the meter sees through the reset via high-water + revision lineage.
Oracle (exact): post price == clamp(2+m_hw+m_sunk+m_fought) with revs=1.
Also: packed r1 reason still reads the original high-water band, and a priced
destruction at the new price succeeds.

## Class R5 — kind-switch (120 sequences)
6 scenarios x 20 variants (5 strengths x 2 destroy ops x 2 cite modes):
(a) DELIB/HIST deliberate -> METER; (b) DELIB/FRESH -> METER;
(c) METER -> DELIB/HIST; (d) METER -> DELIB/FRESH;
(e) METER with no deliberation; (f) METER deliberate then priced overwrite
(stale record). Oracle: deliberate dry-run -1, destruction 122, and the
independent checker `ck_verify_delib_binding` disagrees (>0). Extra fresh
cites must not bypass the kind binding.

## Class R6 — over-cite bricking (104 sequences)
4 skeletons x 2 destroy ops x 13 attempts: citing beyond the bound price must
be refused at cite time (122) before it can brick the slot; the slot must stay
usable for a legitimate destruction. Attempts cover: p+1, 2p+2, post-destroy
re-add over-cite, spent re-cites not counting toward fullness, under-cite 109
then top-up, duplicate 111, invalid episode, cross-slot isolation, price-0
slot, interleaved spent+fresh, alternate cite code.

## Determinism
Every battery runs twice; the two outputs must be byte-identical (cmp).
Any nondeterminism is a FAIL. Any reproduced hole is reported with its
reproducer and NOT fixed.
