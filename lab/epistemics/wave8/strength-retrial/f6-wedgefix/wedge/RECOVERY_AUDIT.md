# Recovery-move audit at the G-mode wedge — Crew B, Phase 1 (audit only)

Date: 2026-09-26. Pure Zag, zero RNG. Driver: `wedge/wedge_audit.zag`
(built from `~/workspace/strength-f6`; no mechanism file modified).
Binary run twice; outputs byte-identical (`cmp run1.log run2.log`).
Every scenario below ends with the checker triple
`ck_verify / st_refusals_clean / st_replay_check` — **all 32 scenario runs
report 0/0/0: the independent checker agrees with every tested op.**

Wedge construction (deterministic): G mode, 16 slots (2 core + 14 user),
P=8 salient pool, rotating 4-cite kills. Because consumption is per-slot
(see D4 below), each slot needs 3 iterations (2 OK kills + 1 refused kill);
45 iterations total. Final state: **14/14 user slots live, 14/14 cite-locked,
ADD → 104 FULL** (`WA_WEDGE live=14 locked=14 add_probe=104`).

## BOTTOM LINE

**Yes — a latent recovery move exists that the mechanism accepts and the
original stress test never tried. The verdict's "no recovery path" claim is
false as stated.**

The D2 path (KNOWN DEVIATION D2, previously filed under "strength-pricing
question, out of F6 scope") breaks the wedge completely, at zero cost,
through the priced destruction path itself, with the checker's full
agreement:

```
st_weaken(s, slot, 0, ST_J_CONTRADICTED)  -> 0   (free, TNN-reachable)
st_justify(s, slot, ST_J_CONTRADICTED)    -> 0
st_kill_evidenced(s, slot)                -> 0   (need = ceil(0/25) = 0 cites)
st_add(s, value, ST_REGION_USER, 90, ep, &ns) -> 0  (slot re-admitted)
```

Measured (S8): `weak0=0 just=0 kill0cite=0 add_after=0`, checker
`ck_cite_count 0,0 / ck_cite_distinct 0,0 / ck_justify_present 1,1`, triple
0/0/0. Cost: **zero citations, zero consumed-set change**. Repeatable
indefinitely on the same slot (S22: k1=0, add=0, k2=0). Full 14-slot unwedge
plus re-admission demonstrated (S20: 14/14 D2 kills OK, 14/14 re-ADDs OK,
checker clean). The wedge does not survive contact with this path: any
wedged slot can be freed and refilled in 4 ops, forever, without spending a
single citation episode.

Two honest readings of the verdict's claim:
- (a) "No recovery *within the citation economy*" — true only if the
  strength-pricing hole (price(0)=0 via free WEAK0) is closed. The
  high-water-pricing workstream moots D2, but in THIS build D2 is live, so
  the claim does not hold of this build.
- (b) "TNN cannot remove these memories / cannot admit new ones" — false.
  Demonstrated otherwise, byte-identical ×2.

Second, weaker recovery (S1/S5): citing genuinely NEW episodes (outside the
finite pool) destroys wedged memories normally (14/14 slots freed with 56
fresh episodes, checker clean). This exits the finite-pool premise rather
than breaking it — the "salient pool" is a driver fiction; the mechanism
accepts any `cite_ep >= 0`. The wedge binds only if the episode supply is
truly exhausted AND D2 is closed.

## Per-op results (plain English)

Wedge state for every scenario: 14 live user slots (2..15), strength 90,
every pool episode consumed on its slot, ADD → 104.

| # | Op tried at wedge | rc | Slot freed? | Consumed-set delta | Checker agrees? |
|---|---|---|---|---|---|
| S1 | KILL + 4 fresh cites + JUST (slot 2) | 0 | YES | +4 consumed | yes |
| S2 | KILL + 2 consumed + 2 fresh cites | 121 | no | none | yes |
| S2B | KILL + pool cites on all 14 slots | 121 ×14 | no | none | yes |
| S3 | KILL + JUST, zero new cites (str 90) | 121 | no | none | yes |
| S4 | KILL + 4 consumed + 4 fresh (D1 shape) | 0 | YES | +4 (fresh only) | yes |
| S5 | KILL + 4 fresh cites on all 14 slots | 0 ×14 | YES, all | +56 consumed | yes |
| S6 | OVERWRITE + consumed cites | 121 | no (occupant kept) | none | yes |
| S7 | OVERWRITE + 4 fresh cites | 0 | no (occupant REPLACED) | +4 consumed | yes; follow-up kill with same cites → 121 |
| S8 | WEAK0 → JUST → KILL, zero cites (D2) | 0/0/0 | YES | none | yes — ck_cite_count 0,0 |
| S9 | WEAK→{1,25,50,89} → KILL + need fresh cites | 0 each | YES each | +need each | yes |
| S10 | WEAK50 → KILL + consumed cites | 121 | no | none | yes (weaken launders nothing) |
| S11 | STR95 → KILL + consumed cites | 121 | no | none | yes |
| S12 | TD role=TNN → 113; TD role=TRAINER(50) → 0; then KILL + 2 fresh | 113 / 0 / 0 | YES (trainer-assisted) | +2 | yes |
| S13A | RB when last entry is refused ADD | 108 | no | none | yes |
| S13B | RB of an OK ADD | 0 | YES — un-admits (re-ADD re-wedges) | none | yes |
| S13C | RB of WEAK → 0 (strength back to 90); RB of OW → 0 (memory restored, OW's cites stay consumed); RB of TD → 113; RB of PIN → 0 | — | no durable change | none | yes |
| S14 | RB of the D2 kill | 0 | no — memory RESTORED (re-wedged) | none | yes |
| S15 | ADD at wedge (strength 90, strength 0) | 104 / 104 | no | none | yes |
| S16 | re-cite consumed ep → 111; cite new ep → 0; JUST → 0 | — | no | none | yes |
| S17 | PIN → 0; D2 kill while pinned → 102; UNPIN → 0; D2 kill → 0 | — | YES (after unpin) | none | yes |
| S18 | st_kill (free kill) | 0 | YES | none | yes — trainer instrument; mechanism enforces NO role gate |
| S19 | PROMOTE / DEMOTE / STRENGTHEN_CITED / ABANDON → 0; SET_STAGE(MANAGE) → 0 then KILL → 105; SET_STAGE(FULL) → 0 | — | no | none | yes |
| S20 | D2 on all 14 slots, then 14 × ADD | 0 ×28 | YES all, then refilled | none | yes |
| S22 | D2 → ADD → D2 again, same slot | 0/0/0 | YES twice | none | yes |
| S24 | D4: OW consumes 0–3 on slot 2; same eps fund KILL on slot 3 → 0 | 0 | YES (slot 3) | +4 on slot 3 | yes |

Probes: KILL on empty slot → 103; KILL on core slot → 101 (S5). No eviction
op exists — `st_add` never evicts; ADD → 104 whenever full (code-inspected,
S15). `st_force_pin/unpin` reviewed (role-gated; pinning deepens the wedge,
never a recovery). P3 protection-expiry not enabled in this build (p3=0) —
out of scope.

## Mechanism specifics

- **D2 cost model.** `st_n(s) = (s<=0) ? 0 : (s+24)/25`. `st_kill_effort_check`
  with strength 0: `need=0`; with zero cites, `total=0, spent=0, cnt=0`;
  `cnt==need` passes; the JUSTIFY scan passes (JUST after WEAK is in the
  window); destruction proceeds. The checker independently recomputes
  `need=ck_n(0)=0` and passes `ck_cite_count(0,0)`. Nothing in the mechanism
  or checker treats a 0-cite destruction as anomalous.
- **TD reachability.** `st_trainer_declare` refuses role < TRAINER with 113
  (S12: TNN role → 113). But `role` is a caller-supplied `i32` argument —
  the mechanism performs no channel binding; the gate is only as strong as
  the caller. TNN itself (role 0) cannot TD through this function.
- **st_kill gating is law-only.** `st_kill` checks stage/live/region/
  forcepin/pinned only — no role parameter at all (S18: rc=0 at wedge, zero
  cites, no JUST). Micah's "trainer-only instrument" ruling is not enforced
  by the mechanism; any code path that can call `st_kill` can free any
  wedged slot unconditionally.
- **RB semantics at wedge.** One-shot; only the immediately-preceding entry;
  refusals and non-mutating ops clear it (108). RB-of-ADD un-admits a memory
  (S13B: the only RB shape that frees a slot — pure undo; the re-ADD
  re-wedges). RB-of-KILL restores the memory with consumption intact (S14).
  RB of trainer-originated ops → 113.
- **WEAK/STR/TD never launder consumption** (S10/S11: 121 after re-citing in
  the new window). They only move the effort window; G's consumed-set is
  ledger-global per slot, so the 121 follows.

## D4 — new spec deviation: G is per-slot, not "on any slot"

`st_cite_consumed` (strength_core.zag) filters candidate destructions with
`st_aw(s,d,1)==slot` and scans cites with `st_aw(s,i,1)==slot`: a cite_ep
counts as consumed only if it paid for a destruction **on the same slot**.
The code comment matches the implementation ("consumed by ANY earlier OK
destruction **on the slot**"). But F6_VERDICT.md's G rule ("a citation
episode can fund only one destruction ever… **on any slot**") and the
proposed amendment text ("never count toward the price of another
destruction, **on any slot**") promise cross-slot single-use the mechanism
does not enforce.

Measured (S24, byte-identical ×2, checker triple 0/0/0): OVERWRITE consumes
eps 0–3 on slot 2 (rc=0); ADD → slot 3; cite eps 0–3; JUST; KILL → **0**.
One 4-episode payment funded two destructions on two slots.

Notes:
- The blind red team never tested this — `f6_rt.zag` only touches slot 2.
  All F6 attack shapes (A1–A8) are single-slot. The "HELD" verdict for G
  rests on single-slot evidence.
- D4 does **not** unlock a full wedge by itself: at the wedge every slot
  has consumed the whole pool on itself, so there is nothing left to reuse
  cross-slot. The wedge arithmetic is per-slot (3.5×P destructions per the
  verdict = 14 slots × 2 kills at P=8 — consistent).
- But D4 means "global" is a misnomer with teeth: under the amendment's
  written language, G is broken (pay 4 episodes, destroy up to 14 memories).
  Either the implementation must go cross-slot or the amendment text must
  be narrowed to per-slot.

## Q5 — does the mechanism distinguish "wedged" from "healthy-but-full"?

**No.** There is no wedged flag, no 121-counter, no per-slot lock bit
anywhere in `StStore`. The consumed set is derived from the ledger on every
check (`st_cite_consumed`/`st_count_spent_cites` — no new state, by design).
`st_refusals_clean` returns a hygiene-violation count, not a refusal tally;
refusals are audited but never aggregated.

A predicate that discriminates is derivable (used in this audit):
slot is *cite-locked* iff live && ≥1 distinct cited ep in its effort window
&& every one of them is consumed. Measured: wedge → 14/14 locked;
healthy-but-full (14 fresh ADDs, zero cites, S21) → 0/14 locked — while
ADD → 104 in both. A fix could key on this predicate (or on 121 density in
the recent ledger), but the mechanism currently computes neither, and —
fundamental limit — the ledger cannot distinguish "pool truly exhausted"
from "TNN simply hasn't cited fresh episodes yet": both look identical
until TNN tries.

## Evidence

- Driver: `wedge/wedge_audit.zag` (imports only; zero mechanism edits)
- Binary: `wedge/wedge_audit_bin`
- Logs: `wedge/run1.log`, `wedge/run2.log` (byte-identical via `cmp`;
  `WA_*` lines are the scenario summaries, `WA_T` lines carry the
  checker triple, `CL_CHECK` lines are the checker's per-claim prints)

## Open questions (no fix proposed — Phase 1 audit only)

1. Is D2 (price(0)=0 via free WEAK0) intended to survive? Alone it voids
   the wedge claim for this build. If high-water pricing closes it, the
   wedge needs re-testing under the closed build.
2. D4: is per-slot or cross-slot ("on any slot") the intended G semantic?
   Amendment text and code comment contradict; red team never tested
   cross-slot. The written amendment is not what the mechanism enforces.
3. Should st_kill's trainer-only status be mechanism-enforced (role gate)
   rather than law-only? Currently any caller frees any wedged slot.
4. TD's role gate takes `role` as a caller argument — is that acceptable,
   or does the deployment bind role by channel? (Build-level question.)
5. Does "recovery" include citing fresh episodes (S1/S5)? The wedge premise
   needs "no fresh episodes AND D2 closed" to bind; otherwise it never bites.
6. S4/D1 at wedge: 4 consumed + 4 fresh → 0. The brief's "every cited
   episode must be fresh" is not enforced — consumed cites are silently
   ignored when fresh==price. Cosmetic bypass of the 121 alarm, or intended?
7. Should the mechanism compute wedge-ness itself (121 counter / lock bit)
   so a future fix has something to key on? Currently the signal exists
   only as a derived predicate.
8. S13B (RB-of-ADD un-admits): is undoing the last admission an acceptable
   recovery shape, or just undo? It re-wedges on the next ADD.
