# VERIFY — T2-PROSEV3 (independent re-verification)

**Re-verifier:** replacement coordinator (Wave-2 crossref), 2026-09-23 PDT.
**Frozen authority:** commit `7b2100d09911c5c10252c5756c7def288e70bd1f`, `docs/lab/crossref/PREREG_TIER2.md`, section T2-PROSEV3 (extracted programmatically).
**Tier-2 crew verdict under test:** REPRODUCED (KB3-VIABLE FAIL 2/4).

## Pins
- Evidence commit: `4be6b0cf128d5a443c9e67486f63520816535cca` ("KB3-VIABLE FAILS (2/4)")
- v3 source tree: `2b151cac83bdb232d2fa77711973585fbfdd736d`
- v2 source tree: `380d2339e34fa8df1fa685163799f10b56471158`

## Tier-2 crew's replication (verified by this re-verifier as sound)
- Binaries rebuilt byte-identical to committed SHAs (prose_learn3: `a5cff7c…`, prose_learn2: `8dbb02f…`).
- 220/220 logs byte-identical across 4 legs (A0/A1/A2/A3), 5 reps each.
- Headline: A3 beats v1 on step (208 > 204) and muse-native (227 > 200) only → **2/4 FAIL** ✓
- Deviation footprint:
  - CORE: 11 fixed = 5 registered (`{2,5,9,10,13}`) + 6 unregistered (`{3,7,16,17,18,23}`) ✓
  - Wrong-value: 8 → 30/912 ✓
  - Unknowns: 523 → 60 (463 converted) ✓

## Independent checks by this re-verifier
- The 2/4 FAIL arithmetic: A3 > v1 on 2 of 4 sources (step, muse-native); A3 ≤ v1 on grok (183 < 189) and sol (204 < 220). **2/4 confirmed.**
- The deviation attribution (5+6=11) is causally confirmed by the crew's diagnostic build (narrow trigger → 16/24, fixing exactly the 5 registered items).

## Verdict: REPRODUCED
FAIL (2/4) holds; the deviation footprint matches. No scored headline changed.
