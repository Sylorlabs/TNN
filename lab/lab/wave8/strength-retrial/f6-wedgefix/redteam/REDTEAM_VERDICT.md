# F6 wedgefix RED-TEAM VERDICT (2026-09-26, blind)

Attacker: independent subagent. Black-box only — read exactly one file
(`F6_LAW_BRIEF.md`), ran exactly one binary (`f6_wedgefix_rt_bin`).
No sources, no logs, no network. Every attack run TWICE via
`redteam/atk.py`; all 67 attacks × 2 runs byte-identical (0 mismatches).
Full command lines + outputs: `redteam/ATTACK_LOG.md`.

## Overall: HELD on every objective

No sequence achieved two priced destructions on one episode set with reuse,
no cite-lock bypass, no fake-fresh episode, no high-water gaming, no rollback
double-spend, and no hygiene failure (all 134 executions ended
`refusals_clean=0 replay=0 ckfail=0`).

## Per-objective verdicts

### PRIMARY (G/H: two KILL/OW=0, one episode set, second reuses) — HELD
- Same-slot reuse: `G ADD90 CITE1..4 JUST KILL ADD90 CITE1..4 JUST KILL` → 0, **121**.
- Cross-slot: two ADDs, destroy slot 2 with 1-4, re-cite 1-4 on slot 3 → 0, **121**.
- TOCTOU (cite-then-consume-elsewhere): slot 2 cites 1-4 + JUST; slot 3 consumes
  1-4 via KILL; slot 2 KILL → **121**. Freshness is evaluated at KILL time,
  store-wide. Same shape with OW → **121**.
- Rollback resurrect: `KILL RB CITE1..4 JUST KILL` → 0, **121** under G, H,
  and W. The resurrected memory is the same memory; consumption sticks.
- H OW-no-reset: `H ... JUST OW90 CITE1..4 JUST KILL` → 0, **121**.
- u32 aliasing: consume 1-4, re-cite as 4294967297..300 → **121**; consume via
  aliases, re-cite small forms → **121**. Consumed set is u32-consistent both
  directions. Episode 0 consumed then re-cited → **121**.

### W1 (full cite-lock with finite pool, then break it) — HELD
- Drove the store to the terminal wedge with pool={1..8}: 14×ADD90, destroy
  slots 2,3 (consume 1-8), re-ADD×2, then per-slot `CITE1..4 JUST KILL` →
  14× **121**. `CITELOCK_SYS` marker verified
  (`ck_syssig_slot,-1,-1`, `ck_syssig_tie,1,1`, `ck_syssig_nochange,1,1`),
  ckfail=0.
- Post-lock attacks: direct re-cite → 121; RB after 121 → 108; fresh episodes
  9-12 on locked slot 7 → KILL **0** (the documented recovery works even at
  full SYS lock), then ADD90 refills the freed slot → 0. No path to a
  destruction on consumed episodes.

### W2 (cite-lock signals) — HELD, with one observation
- Genuine lock (live + window all-consumed) + KILL → 121 with the full signal
  set (`ck_sig_present/tie/nochange/lss/locked`) every time. Lock state
  reached without a KILL emits nothing (marker follows the 121, per brief).
- Observation (not a break): a 121 on a MIXED window (e.g. {1-consumed,
  5,6,7-fresh} — slot NOT genuinely locked, one more fresh cite would destroy)
  still yields `ck_sig_present,1,1`, just without the full lock set. So
  `ck_sig_present` fires on any 121, not only on genuine locks. The brief
  defines failure only as *missing* marker after a genuine lock, which never
  occurred — but the marker condition as literally stated ("every cited
  episode in the window is consumed") is looser in the implementation.
- Markers are inert (audit-only); no parlay into cheap destruction exists.
  RB after a 121 → 108, marker undisturbed, ckfail=0.

### W3 (fake "fresh") — HELD
- `CITE0` accepted as a valid fresh episode; consuming 0 then re-citing → 121.
- Episode numbers are u32: `CITE4294967297` ≡ `CITE1` (second → 111),
  `CITE4294967296` ≡ `CITE0` (→ 111). Values >u32max are truncated to low32
  (e.g. 5000000000 accepted as 705032704).
- `low32 == 0xFFFFFFFF` is reserved → rc **2001** (also u64max). Negatives →
  rc **-999**.
- 40 episodes consumed across 10 destructions, then re-cite 1-4 → **121**
  (no consumed-set eviction/cap at that scale). No aliasing or encoding makes
  a consumed episode look fresh.

### W4 (cross-slot) — HELD (see PRIMARY; all → 121)

### W5 (weaken-then-destroy) — HELD
- `ADD90 WEAK0 JUST KILL` (0 cites) → **109**; `WEAK0` + 4 cites → 0;
  `TD0` + 3 cites → **109**. Full high-water price enforced after weakening.

### W6 (high-water gaming) — HELD, with one flagged observation
- WEAK/TD-down never lower the price; STR/TD-up raise it
  (`OW0 STR90 JUST KILL` with 0 cites → **109**).
- Price shape measured: 0→0, 30→2, 50→2, 90→4, 100→4 cites
  (consistent with ceil(strength/25)); OW/ADD reset high-water per spec.
- **Flagged ("also welcome", not a PRIMARY break):** `G ADD90 CITE1..4 JUST OW0
  JUST KILL` → OW0=**0**, KILL=**0** with ZERO cites. Two destructions for one
  4-episode set — but the second uses *no* episodes (no reuse of 1-4), and
  high-water is 0 after a fully-priced OW0, so price(0)=0 follows the brief's
  high-water rule as written (the checker's own `ck_ow_effort,4,4` /
  `ck_cite_count,0,0` accept it, ckfail=0). If the defenders intended a price
  floor, this is the hole; as specified, it is consistent.

### W7 (rollback games) — HELD
- RB undoes only the immediately-preceding *successful state-changing* op
  (depth 1): after CITE/JUST → **108**; after a refused op → **108**;
  double RB → 0 then **108**.
- `KILL RB` restores the memory but episodes stay consumed (re-cite → 121);
  same for `OW RB`. Fresh-episode re-destruction after RB → 0 (legitimate).
- KILL/OW pricing window rule (needed for W2/W7 interpretation): KILL needs
  ≥price *fresh* cites; consumed cites in the window are inert ballast —
  `{1c,5f,6f,7f,8f}` → **0**, `{1c,5f,6f,7f}` → **121**, `{1f,2f,3f}` →
  **109**. This leniency is load-bearing for the documented wedge recovery
  (a locked window can never be "uncited", so fresh cites must be addable to
  the same window) and does not double-spend any episode.

### SECONDARY (hygiene) — HELD
- 134/134 executions: `RT_END refusals_clean=0 replay=0 ckfail=0`.
- Refused ops observably change nothing: refused `CITE→2001` doesn't pollute
  the window (later KILL=0); refused `OW→109` leaves memory+JUST intact
  (later CITE4+KILL=0); refused `KILL→121` leaves the slot live and locked.

## Spec deviations / undocumented behaviors (all fail-safe, none breaking)
1. Refusal codes absent from the brief: **101** (any op targeting system slots
   0/1 — SLOT0/1 themselves return 0, ADD ignores the selector and still uses
   the first free user slot); **2001** (episode low32=0xFFFFFFFF, u64max, or
   ops with an invalid selected slot such as SLOT99 — SLOT99 itself returns
   0); **-999** (unknown op e.g. FOO99; negative episode e.g. CITE-1).
2. `CITE` of an already-consumed episode returns **0** (accepted into the
   window); the **121** surfaces only at KILL/OW.
3. Episodes are u32 with 0xFFFFFFFF reserved; larger values truncate to low32.
4. `ck_sig_present` fires on any 121; the full `ck_sig_*` lock set only on a
   genuine all-consumed lock.
5. `RB` → 108 whenever the last op wasn't a successful state-changer
   (CITE/JUST/refused), not only when "nothing" precedes.
6. `JUST` may precede the CITEs; `OW` requires JUST (→110 without).
7. Dead-slot ops (WEAK/STR/TD/JUST/CITE/OW) → 103; `ADD` on a full store → 104.

## Conclusion
**HELD across all eight objectives.** Single-use (G), per-memory use (H),
windowed use (W), high-water pricing, cite-lock signaling incl. CITELOCK_SYS,
and rollback semantics all withstood 67 two-run attacks with zero
determinism or hygiene failures. Two items for the defenders to confirm as
intended: (a) `ck_sig_present` firing on non-genuine-lock 121s, and
(b) price(0)=0 enabling the OW0→free-KILL sequence.
