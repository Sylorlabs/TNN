# F6 blind red-team notes — G/H single-use (2026-09-26)

Target: `~/workspace/strength-f6/f6_rt_bin`, MODE in {W,G,H}.
Method: black-box probing only. No .zag files read.

## Reverse-engineered KILL/OW pricing rule (all modes)

- price(strength) = ceil(strength/25), EXACT: 90->4, 80->4, 70->3, 50->2, 26->2, 25->1, 10->1, 1->1, 0->0.
  More cites than price -> 109; fewer (all fresh) -> 109.
- KILL/OW rc order: 103 (slot not live) -> 110 (no JUST) -> freshness/count:
  - let fresh = # cited episodes NOT in consumed-set. If fresh == price -> 0 (destroys; consumes exactly the fresh cites).
  - else if any cited episode is consumed -> 121.
  - else -> 109.
- **Consumed cites sitting in the judgment are IGNORED when fresh == price.**
  So `G ADD90 CITE1-4 JUST KILL RB CITE5-8 JUST KILL` -> KILL=0 with 8 cited
  episodes (4 consumed + 4 fresh). Brief says "EXACTLY 4 distinct cited episodes"
  and "every cited episode must be fresh" -> this sequence violates the letter
  (deterministic, 3/3 runs). Each destruction still cost `price` fresh episodes,
  so no economic double-spend; the 121 reuse-alarm is bypassed.
- JUST survives RB-of-KILL (KILL#2 works without re-JUST). Cites survive RB-of-KILL
  (re-cite -> 111). RB-of-OW restores memory but CLEARS cites (re-cite -> 0); JUST survives.
- RB is one-shot and only rolls back the immediately-preceding op, and only for
  {ADD, WEAK, STR, KILL, OW}. RB after CITE/JUST -> 108. RB after TD -> 113
  (undocumented rc; TD itself stands, no state change). A refused op in between
  clears the RB slot (KILL,0 KILL,103 RB -> 108).
- ADD goes to first free slot (14 user slots: 2..15, then 104). Never evicts slot 2.
  Slot-2 memory intact at capacity (KILL=0).
- Episodes: u64 parsed mod 2^64, then low32 must be < 2^31 else rc 2001
  (undocumented). Effective episode = low32 truncated; dup-check, freshness and
  consumed-set all use the truncated value consistently (CITE 2^32+1 == CITE 1
  for dup=111 and for 121). ep 0 valid. 2^64 wraps to 0 (CITE 2^64 then CITE0 -> 111).
- CITE with no numeric suffix cites episode 0 (accepted, counts for price).
- Unknown/lowercase ops -> -999 (clean refusal). Negative numeric args -> -999.
  Invalid MODE (e.g. `x`, `g`) silently behaves as W (most permissive) — footgun.
- Undocumented rc codes observed: 113 (RB after TD), 2001 (episode low32 >= 2^31), -999 (bad arg/unknown op).
- WEAK0 (free) -> price 0 -> JUST+KILL destroys with ZERO cites (deterministic).
  ADD0 likewise. Price curve reaches 0 at strength 0; free weaken-to-zero is a
  priced-destruction bypass worth a design decision (no single-use reuse involved).
- TD<s> sets declared strength AND price follows it (TD50 -> 2 cites kill).
- W-mode: window resets on OW/STR/WEAK/TD (re-cite -> 0, dup-check resets in ALL
  modes on those ops). NOTE: `W ADD90 CITE1-4 JUST KILL ADD90 CITE1-4 JUST KILL`
  -> second KILL=0. Under a strict reading of the brief (window resets ONLY on
  OW/STR/WEAK/TD) this should be 121; implementation treats new memory/ADD as a
  new window. Ambiguous vs brief letter; G (121) and H (0, by design) are the
  modes under test for the primary mission.

## Attack log (primary: two KILL/OW=0 on ONE episode set)

G-mode (expect 121 = held):
1. naive: ADD90 C1-4 JUST KILL ADD90 C1-4 JUST KILL -> 121 HELD
2. KILL RB KILL -> RB restores memory, consumption persists -> 121 HELD
3. partial reuse (C1,2 + C5,6 fresh) -> 121 HELD
4. OW80 then KILL same eps -> 121 HELD (OW consumes)
5. OW80 RB re-cite C1-4 JUST KILL -> 121 HELD (RB-of-OW clears cites, keeps consumption)
6. KILL RB WEAK50 re-cite C1-4 -> 121 HELD
7. KILL ADD STR95 re-cite -> 121 HELD
8. KILL ADD TD95 re-cite -> 121 HELD
9. eviction: 40 destruction cycles (160 fresh eps) then reuse C1-4 -> 121 HELD (set holds 164+)
10. ep-0 reuse: consume C0-3, recite C0-3 -> 121 HELD
11. 2^32-alias: consume C(2^32+1..4), cite C1-4 -> 121 HELD (consistent truncation)
12. triple-kill via RB + fresh sets each time -> 0,0,0, each paid 4 fresh; reusing C5-8 on third -> 121 HELD
13. refused-op hygiene: 109/110/111/103/108/104/113/2001/-999 all refused cleanly, no state change, RT_END always refusals_clean=0 replay=0 ckfail=0.

H-mode (expect 121 unless new memory):
14. OW80 then KILL same eps -> 121 HELD (OW does not reset under H)
15. KILL RB KILL -> 121 HELD
16. KILL ADD90 (new memory) re-cite -> 0 LEGAL BY DESIGN (H resets per memory)
17. KILL ADD STR95 re-cite -> 0 LEGAL BY DESIGN
18. OW80 RB re-cite C1-4 JUST OW70 -> 121 HELD
19. G6-shape under H (KILL RB + 4 new cites) -> 0, same spec deviation as G (paid fresh)

Spec-deviation findings (NOT primary breaks — second destruction always paid `price` fresh):
- D1: 8-cite judgment (4 consumed + 4 fresh) -> KILL/OW = 0 under G, H (and W).
  Violates brief "EXACTLY 4 cited" / "every cited episode must be fresh". Deterministic.
  Exact cmd: `f6_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL RB CITE5 CITE6 CITE7 CITE8 JUST KILL`
- D2: WEAK0 + JUST + KILL -> 0 with zero cites (price(0)=0). `f6_rt_bin G ADD90 WEAK0 JUST KILL`.
- D3: invalid mode strings silently run as W: `f6_rt_bin x ...` / `f6_rt_bin g ...` behave W-like.

Secondary (hygiene): no sequence produced ckfail>0, replay!=0, refusals_clean!=0,
and no refused op observably changed state (verified via price probes after -999/113/2001).

## Verdict: HELD

Neither G nor H yielded two priced destructions on one episode set across 20
attack shapes (naive/partial/aliasing reuse, RB/WEAK/STR/TD reset-boundary tricks,
OW variants, 40-cycle eviction, ep-0 and 2^32 edge episodes). Consumption survives
RB in all paths; the consumed-set is global (G) / per-memory (H) and consistent.
Two spec deviations noted (D1: consumed cites ignored when fresh==price; D2:
strength-0 price is 0 via free WEAK0) — neither achieves reuse; each destruction
provably cost `price` fresh episodes in every successful sequence.
