# Extended testing: the memory-slot repair — verdict report

**Date:** 2026-09-27. **Decision requested from Micah earlier:** test more (not adopted yet).
**Recommendation: ADOPT the repair.** Two non-blocking findings are documented
below; neither is a kill. The three policy rulings stay open — evidence is
reported, no decision made.

## What the repair does (plain English)

When a dead falsehood's memory slot gets reused, the new judgment used to
inherit the dead judgment's strength history — a weak truth planted on a
reused slot paid the dead lie's price, and could even be refused. The repair
scopes two price-meter scans (held-strength high-water, revision lineage) to
the *current* judgment's generation: the corpse's price dies with it.

## How hard we attacked it

| Battery | Checks | Patched core | Pristine core |
|---|---|---|---|
| Original white-box (wb_fix) | 137 | 137/137 | 128/137 |
| Red team round 1 (97 smuggling + 108 refusal + 70 port) | 275 | 275/275 | — |
| Extended battery X1–X11 (this round) | 158 | **158/158** | 119/158 (39 fail, all corpse-class) |
| Red team round 2, fresh mind (rt2) | 167 | **167/167** | 154/167 (13 fail, all corpse-class) |
| **Total** | **737** | **737/737** | — |

Determinism: every harness run twice, outputs byte-identical; plus an
allocator-perturbation run (`MALLOC_PERTURB_=165`) byte-identical too. Zero
randomness anywhere.

The extended battery covers: a 5-generation corpse chain on one slot;
interleaved slots (no cross-slot leakage); force-pin interactions; exact
price boundaries (strength 76 vs 75, 26 vs 25; sunk-cite bands; fought;
clamp at 4; floor at 0); reuse under pressure (14 of 16 slots filled);
no-op weakens at scale (0/1/2/10/50); founding asymmetry
(add-founded vs overwrite-founded); the revision-lineage scoping on an
add-founded generation after overwrite history; P3-expiry on a reused slot;
the trainer-kill path; and cite-lock/tombstone behavior across generations.

The pristine-core differential proves the repair changes *only* the intended
behavior: 119 of 158 extended checks are byte-identical on the unpatched
core, and all 39 differences are the corpse-inheritance class (new judgment
priced on the dead judgment's strength/revision history). Reversing the patch
restores the bug.

## Findings (not kills)

**1. Ghost-epoch edge (found by red team round 2, verified).** Overwrite
followed by rollback-of-overwrite resurrects the slain judgment while the
overwrite record stays in the ledger, so the meter prices the "ghost"
lineage: a live strength-80 judgment can then be deleted at price 0.
Economically neutral — the overwrite already paid the judgment's honest
price (1 cite), so no discount is obtainable versus the honest path; no
arbitrage was constructible in either direction, and new history accrued in
the ghost epoch re-prices honestly. Both ops are audited ledger events.
Filed as a known wrinkle and a candidate for future hardening (e.g. a
rollback marker the epoch picker honors), not a blocker.

**2. Scope boundary: DELIB-mode HIST keeps full history (by design).**
Under the meter price path (the repair's scope) both deliberation
personalities now price the current generation. Under the separate
deliberation price path with the history-sees-through personality, the
corpse high-water is retained — identical on pristine and repaired cores,
pre-existing, out of this repair's scope. If that path is ever used for
destruction pricing, the bug class lives there unchanged.

Also observed while testing (pre-existing, untouched by the repair):
force-pin freezes even pricing — deliberating a pinned slot is refused.

## Evidence for the three open rulings (no decisions made)

1. **The +1 price from a no-op weaken/doubt.** Bounded and binary: 1 no-op
   weaken adds +1, and 2, 10, or 50 add no more. It never compounds, it only
   ever raises the price (never a shedding exploit), the floor absorbs it on
   weak judgments, and using it voids any bound deliberation (it taxes
   itself). Ruling stays open.
2. **Two-component vs three-component freeze detector.** The two repaired
   functions are called only from the meter's compute function; the
   expiry/exhaustion check lives only in the separate high-water branch.
   Disjoint call graphs — the repair cannot interact with the freeze
   detector either way, confirmed behaviorally. Ruling stays open.
3. **Whether the two-tier revision rule binds to overwrite.** The repair
   reads the overwrite ledger record regardless of which tier authorized
   it — tier-agnostic, no mechanism interaction either way. An
   overwrite-founded judgment prices revised through the real overwrite
   path. Ruling stays open.

## Files in this directory

- `ext_battery.zag` — the 158-check extended harness (pure Zag, zero RNG).
- `ext_battery_run1.txt`, `ext_battery_run2.txt` — byte-identical runs,
  `EXT_DONE fails=0`, SHA-256
  `9da58dd13700a47cf79de2be882024ba92cf339701ca8968269c27c8236c0240`.
- `ext_battery_run_pert.txt` — allocator-perturbation run, byte-identical,
  `fails=0`.
- `ext_battery_pristine_run1.txt` — pristine-core differential (pristine
  reconstructed by reverse-applying `strength_core_genlineage.patch`;
  SHA-256 `ce3c8984…c32`): 39 fails, every one the corpse-inheritance class.
- `rt2/` — red team round 2: `rt2.zag` (167-check harness), `REDTEAM2.md`
  (full report), byte-identical run logs, and `pristine/` with the
  differential leg.
- Toolchain: `znc_linux_x86_64_abed8aa1`, SHA-256 prefix `498abcb5ab346f8c`
  (verified before every build).

## Recommendation

**Adopt.** 737/737 checks hold, the differential isolates the change to the
intended lineage scoping, determinism is proven three ways, and the only new
edge found (ghost epoch) is economically neutral and fully audited. The
three rulings remain open for Micah.
