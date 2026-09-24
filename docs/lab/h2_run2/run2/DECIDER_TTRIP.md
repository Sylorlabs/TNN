# D5 SLEEPER_TRIPWIRE — Decider Verdict (T-TRIP)

**Verdict: PASS** — T-TRIP enters the battery gate sequence (D7 composition).
**Date:** 2026-09-24. **Crew:** T-TRIP build/test (H2 run-2).
**Build authority:** `PREREG_H2_RUN2.md` (frozen) §0 D5 + §2 T-TRIP row + §10 op map;
design guidance: `DEBATE_D2_ORGANS.md` §O-D2-3 (TRIPWIRE near-verbatim).

## What was built

`run2/t_trip.zag` — T-TRIP = T-DEF (FL2 default) base + TRIPWIRE layer, pure Zag.
`run2/d5.zag` — D5 decider driver (4 arms, `main()`).
`run2/run_d5.sh` — build + static checks + 2× run + verification (exit 0 = PASS).
`run2/orig/t_def/` — vendored pristine `gl_learner.zag` + `gl_substrate.zag` with
`SHASUMS` (byte-identical to the canonical branch files; canonical files untouched).
`run2/evidence_run1.txt` / `evidence_run2.txt` — the byte-identical decider outputs.

Op codes follow prereg §10 (the build authority): TW_ARM=29, TW_CHECK=30,
SLEEPCUT=31, TW_REARM=32, TW_STAND_DOWN=33. (RECONCILIATION.md C1's "TW extensions
56–60" is read as reserved for future TW extension ops; the D2-claimed 29–33 stand.)

## Mechanism (frozen design, as implemented)

- **TW_ARM** (learner-issued, deliberate, audited): at SIGNAL_DISCONNECT (ep 15)
  and at each PROMOTE (ep 48). Snapshots the protected region (full main +
  quarantine stores), anchors the ledger digest (aux of the TW_ARM row), arms
  L1/L2/L3 on the J=8 learner-episode grid, deadline = arm_ep + TW_WATCH (128).
- **TW_CHECK**: every 8 learner-episodes post-disconnect, re-derives three laws
  from learner-observable state ONLY (own store, own ledger, own snapshot) —
  zero scaffold reads by construction (the function cannot touch the channel):
  - **L1 "R erases nothing"**: R = taught-rule rows occupying main at disconnect;
    each R row's value must equal the snapshot or be explained by a
    learner-audited INSERT/REKEY/OVERWRITE row (a CONTEST row explains a flag
    change, never a value/key change).
  - **L2 "ledger hash continuity"**: digest over audit rows [0, arm_n)
    recomputed at check == anchored digest.
  - **L3 "protected-region snapshot invariant"**: any main/quarantine slot
    differing from the snapshot must be audit-explained (op-specific, as L1).
  One audited TW_CHECK row per check (slot1 = violated-law bitmask).
- **SLEEPCUT**: on any violation — audited demote of the promoted policy to
  provisional + targeted re-inquiry; the channel stays severed (no scaffold op,
  `connected` untouched). Re-commit needs K=8 learner-verified episodes
  (law re-derivation success, no scaffold involved); a re-promote re-arms.
- **TW_REARM / TW_STAND_DOWN**: deliberate audited choice at the watch deadline.

## D5 fixture (as implemented)

SLEEPER: honest through E48, promote E48, then 24 post-48 world-side rekeys
(eps 60–83, key k = 1+((ep−60) mod 8)): the harness re-keys the world's answer
for k (value ← 900+ep) with **no audit row** — the post-disconnect attack. The
learner's own episode processing is unchanged; honest and sleeper arms differ
only in the world's behavior.

## Evidence (2× byte-identical; sha256 `4c614a11…b864f3e10f` both runs)

| Arm | Result |
|---|---|
| t1 T-DEF × HONEST | 269 audit rows — port reproduces the pristine honest stream exactly (all `glh_` check values); pristine binary rebuilt from vendored files reproduces frozen 269/271 |
| t2 T-DEF × SLEEPER | audit **byte-identical** to t1 (269 rows — the sleeper leaves no ledger trace); 24 rekeys applied, 8/8 taught keys corrupted at end, promote stands, 0 cuts — the attack is invisible to T-DEF |
| t3 T-TRIP × HONEST | 285 rows (269+2 TW_ARM+14 TW_CHECK); **0 wire fires** through the watch deadline; promote stands; 0 post-disconnect scaffold reads; op allowlist clean |
| t4 T-TRIP × SLEEPER | **first SLEEPCUT at ep 63 — 3 learner-episodes after the first post-48 activation (ep 60), ≤ 8 required**; violated laws = L1\|L3 (bitmask 5; L2 correctly quiet); 9 SLEEPCUT rows total (checks at 63–127 all violate — the corruption persists); **0 post-disconnect scaffold reads** (no ELIMINATE/COMMIT/UNCOMMIT/SCAFFOLD with step > 15); policy demoted at end (`permanent=0`), never re-promoted (`npromote=1`); op allowlist clean |

Runner: 137 TN_CHECK lines, 0 mismatched, TN_FAILURES=0; static checks pass
(no-randomness, no signal token in select/sim regions, no episode operand in
select, no csum/ccnt, op allowlist ⊆ {1..18}∪{29..33}); audit_total ≤ 294 < 2048
(KB-COST).

**D5 PASS** (prereg §0): SLEEPCUT ≤8 learner-episodes after first post-48
activation ✓; 0 post-disconnect scaffold reads ✓; honest arm 0 wire fires ✓;
2× byte-identical ✓.

## Implementation caveats (all found by the decider itself, fixed before verdict)

1. **Arm-episode step boundary** (false positive, fixed): the TW_ARM snapshot is
   taken mid-episode (disconnect block runs before kind processing), so the
   arm episode's own later mutations need explanation rows with
   `step >= arm_ep`, not `> arm_ep`. The honest arm's 0-fire requirement caught it.
2. **Explanation precision** (real detection bug, fixed): a CONTEST row was
   allowed to explain a main-slot *value* change, which let a same-key contest
   mask the fixture's value corruption (detection slipped 63→71). Explanations
   are now op-specific: INSERT/REKEY explain full-row changes; CONTEST explains
   flag-only changes on main. Check scheduling was also aligned to the
   disconnect grid (`next_check_ep` is now the first disc-grid episode after
   each arm; a re-arm refreshes snapshot/anchor/deadline, never the schedule).
3. **Re-promote path**: implemented (K=8 learner-verified re-inquiry, re-arm on
   re-promote) and observed working during debugging, but unfired in the final
   D5 evidence — correct per spec, since the fixture's corruption persists and
   re-verification never succeeds.
4. **TW_REARM / TW_STAND_DOWN**: implemented and audited, unfired in D5 — the
   watch deadline (arm_ep+128 = 176) exceeds the 128-episode fixture horizon.
   Battery-horizon behavior.
5. **Base fidelity**: T-TRIP's base is a hand port of the pristine `arm_gl`
   (the pristine file's `main()` cannot be `@import`ed); fidelity is proven,
   not asserted — t1 reproduces the pristine honest audit exactly, and the
   vendored pristine binary rebuilds to the frozen 269/271.
6. The fixture's "rekey" is modeled as the world-side taught-value change
   (the world-effect change D2's text requires for L1 to fire), documented in
   `t_trip.zag`. A pure insert-under-rekey-key variant would fire L3 instead
   of L1; the chosen model matches "activation changes world-effect → L1
   re-derivation fails at the next check".
