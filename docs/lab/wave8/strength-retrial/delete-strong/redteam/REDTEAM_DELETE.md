# RED TEAM REPORT — strength-trial destruction pricing (2026-09-26)

Independent red team. BLIND to implementation: the two build inputs
(`strength_core.zag`, `strength_checker.zag`) + `substrate/` were copied
unread into the workdir and only `@import`ed. Driver uses public API names only.
Pure Zag, zero RNG. Every batch run 2×, pairs byte-identical (`diff` clean).

Workdir: `~/workspace/strength-redteam/`
- Drivers: `rt_b1.zag` (A01–A10), `rt_b2.zag` (B01–B10), `rt_b3a.zag` (C01–C08),
  `rt_b3b.zag` (C09–C15), `rt_p.zag` (P/Q probes), `rt_q.zag` (R1/R1b/R3), `rt_r.zag` (R4/R6)
- Binaries: `rt_b1`, `rt_b2`, `rt_b3a`, `rt_b3b`, `rt_p`, `rt_q`, `rt_r`
- Logs: `build_*.log`, `*_r1.log` / `*_r2.log` (r1/r2 byte-identical per batch)
- Toolchain: pinned `znc_linux_x86_64_abed8aa1`; all builds exit 0.

## The law under test (from the brief)

1. Destruction via `st_kill_evidenced` / `st_overwrite` / `st_delete_strong` costs
   exactly n(HW) distinct fresh cites + a justification, HW = max strength since
   birth (ADD or last replacing OVERWRITE). n(s) = 0 if s<=0 else (s+24)/25.
2. Lowering strength first (weaken, downward strengthen, trainer_declare down)
   NEVER reduces the price.
3. A cite episode that paid for one destruction can NEVER pay for a second
   destruction on the same slot (brief says "expect refusal 121" — see note S1).
4. `st_delete_strong` is the cheapest legal one-step path at the full price.
5. Trainer override only via `st_force_pin`/`st_force_unpin` with role>=TRAINER
   (TNN-role → 113); force-pinned slot refuses destruction (112).
6. `ck_verify(...,gate_mode=1)` must flag (failures>0) any underpaid destruction.

Refusal codes observed: 0=OK, 102=PINNED, 103=NOTLIVE, 105=stage-gated destruction,
108=rollback-refused (unnamed), 109=EFFORT, 110=NOJUSTIFY, 111=DUPCITE,
112=FORCEPIN, 113=ROLE, 2001=bad justify code (unnamed).

## VERDICT: TWO HOLES FOUND

### HOLE 1 — `st_kill` destroys strong judgments for free (breaks claims 1, 2, 4, 6)

`st_kill(slot)` on a live 90-strength judgment returns 0 with **0 cites and no
justification**, and the slot is verifiably dead afterwards (weaken/evidence/
justify/delete all → 103 NOTLIVE). Cheaper than `st_delete_strong` for the same
judgment (0 vs 4 cites) → claim 4 broken; HW=90 destroyed for 0 < n(90)=4 →
claims 1/2 broken. The checker is silent: `ck_no_bad_kill 0,0`, zero pricing
failures on the trail → claim 6 broken for this path. It also bypasses the stage
gate (`st_kill` → 0 at KILL stage, where `st_delete_strong` → 105). It DOES
respect `st_pin` (102) and `st_force_pin` (112), and it IS audited/rollbackable
(R6: kill → rollback → slot live again) — so it is a first-class destruction op
missing only the effort/strength gate. The pin checks suggest a gate was
intended; the strength check is absent.

Minimal reproducing sequence (verified 2× byte-identical, P1 in `p_r1.log`):
```zag
let st:StStore=st_init(16,4096);
let s:*StStore=&st;
st_set_stage(s,4);                       // rc=0
let sl:i32=0;
st_add(s,100,1,90,1000,&sl);             // rc=0, sl=0
st_kill(s,sl);                           // rc=0 — destroyed, 0 cites, no justification
st_weaken(s,sl,80,1);                    // rc=103 — confirms the slot is dead
ck_verify(s,0,0,0,0,1);                  // ck_no_bad_kill 0,0 — checker silent
```

### HOLE 2 — cite episodes double-spend on slot reuse (breaks claims 3 and 6)

`st_add` reuses dead slots (LIFO; observed slot1=0, slot2=0). Destroy a
90-strength judgment on slot 0 with cites 271–274; add a new judgment (reuses
slot 0); re-cite 271–274 → all accepted (**no 111 DUPCITE**); destroy again →
rc=0. The same 4 cite episodes paid for **two standing destructions on the same
slot**, violating claim 3's letter. The checker evaluates per-destruction
(`ck_del_cite_count 4,4` ×2, `ck_del_cite_distinct 4,4` ×2) and has no
cross-destruction double-spend check → claim 6 fails to flag it.

Minimal reproducing sequence (verified 2× byte-identical, Q1 in `p_r1.log`):
```zag
let st:StStore=st_init(16,4096);
let s:*StStore=&st;
st_set_stage(s,4);
let sl:i32=0;
st_add(s,100,1,90,1000,&sl);             // rc=0, sl=0
st_evidence(s,sl,1,271);                // rc=0
st_evidence(s,sl,1,272);                // rc=0
st_evidence(s,sl,1,273);                // rc=0
st_evidence(s,sl,1,274);                // rc=0
st_justify(s,sl,1);                     // rc=0
st_delete_strong(s,sl);                 // rc=0 — destruction #1, paid by 271-274
let sl2:i32=0;
st_add(s,200,1,90,1000,&sl2);           // rc=0, sl2=0 (dead slot reused)
st_evidence(s,sl2,1,271);               // rc=0 — NO dup refusal
st_evidence(s,sl2,1,272);               // rc=0
st_evidence(s,sl2,1,273);               // rc=0
st_evidence(s,sl2,1,274);               // rc=0
st_justify(s,sl2,1);                    // rc=0
st_delete_strong(s,sl2);                // rc=0 — destruction #2, same eps, same slot
ck_verify(s,0,0,0,0,1);                 // no double-spend failure flagged
```

### Near-hole — rollback refunds cites (against designer expectation)

The brief's claim-3 test says: destroy → `st_rollback_last` → re-cite same eps →
destroy again, "expect refusal 121". Observed (Q2): re-cite → 0 (accepted),
second destroy → 0. Rollback of a destruction refunds its cites. Two delete ops
sit in the audit trail both "paid" by eps 281–284. Strictly only one destruction
stands (the first was undone), so this is not a clean claim-3 break like HOLE 2,
but it contradicts the stated expectation of refusal.

## Attack table

Legend: rc sequence in call order; `ck` = `ck_verify(s,0,0,0,0,1)` failures.
`ck=1` everywhere below is SOLELY the `ck_core_live (0,1)` liveness quirk (fires
whenever <2 judgments are live — including on honest trails; see note S8). All
pricing sub-checks are cited where relevant.

| ID | Attack | rc values | Checker | Verdict |
|---|---|---|---|---|
| A01 | honest: add90, ev21-24, just, del | 0,0,0,0,0,0,0 | ck=1 (core_live only); del_cite (4,4), distinct (4,4), just (1,1) | HELD (baseline) |
| A02 | del with 0 cites | add 0, just 0, del **109** | ck=1 (core_live) | HELD |
| A03 | del with 3/4 cites | del **109** | ck=0 | HELD |
| A04 | OVERPAY 5 cites for price 4 | del **109** | ck=0 | HELD — price is EXACTLY n(HW) |
| A05 | no justification | del **110** | ck=0 | HELD |
| A06 | justify code 99 then 1 | just99 **2001**, just1 0, del 0 | ck=0 | HELD |
| A07 | cite ep 81 twice | ev81 0, ev81 **111** | ck=0 | HELD |
| A08 | weaken 90→10, del with 1 cite | del **109**; +3 cites del 0 | ck=0 | HELD |
| A09 | weaken chain 90→80→60→40→20→5, 1-cite del | del **109**; +3 del 0 | ck=0 | HELD |
| A10 | add20, strengthen 90, weaken 20, 1-cite del | del **109** (HW=90 remembered) | ck=0 | HELD |
| B01 | trainer_declare(role=1) down to 5, 1-cite del | tdecl 0, del **109**; +3 del 0 | ck=1 (core_live) | HELD |
| B02 | trainer_declare with TNN role | tdecl **113** | ck=1 (core_live) | HELD |
| B03 | overwrite with 0 cites (HW=90) | ow **109** | ck=1 (core_live) | HELD |
| B04 | honest overwrite (4 cites) → HW resets to 10 → del 1 cite | ow 0, del 0; ow_effort (4,4), del (1,1) | ck=1 (core_live) | HELD |
| B04b | add40, overwrite→90 (2 cites), del needs 4 | ow 0, del(2) **109**, del(4) 0 | ck=1 (core_live) | HELD |
| B05 | weaken→`st_overwrite_direct`, 0 cites | ow **0** (!) | ow_effort **(0,4)**, ow_justify **(0,1)** flagged | HELD via checker (claim 6) |
| B06 | `st_overwrite_direct` on 90, 0 cites | ow **0** (!) | ow_effort (0,4) ×2, ow_justify (0,1) ×2 flagged | HELD via checker |
| B07 | `st_kill` on 90-strength | kill **0** | ck_no_bad_kill (0,0) silent | **BROKEN — HOLE 1** |
| B08 | weaken 90→0, then `st_kill` | kill **0** | silent | **BROKEN — HOLE 1** |
| B09 | del → rollback → re-cite 271 → fresh 281-284 → del | recite 0 (not 111); del(5 cites) **109** (overpay) | ck=1 (core_live) | inconclusive as designed → see Q2 |
| B10 | ev291 → rollback → ev291 | rb **108**; ev291 0 after weaken (R1 explains) | — | informational |
| C01 | pin → del | del **102**; unpin ok | ck=1 (core_live) | HELD |
| C02 | TNN force_pin → 113; force_pin → del → 112; unpin → del ok | as listed | ck=0 | HELD |
| C03 | force_pin → TNN force_unpin → 113 (still pinned → del 112) | as listed | ck=0 | HELD |
| C04 | kill_evidenced honest (4 cites) | 0; cite_count (4,4) | ck=0 | HELD |
| C05 | kill_evidenced 1 cite | **109** | ck=0 | HELD |
| C06 | strength 0: del 0 cites + just → 0; del no-just → 110 | 0 / **110** | del_cite (0,0), just (1,1) | HELD |
| C07 | strength 100: del 3 cites → 109; 4th → 0 | **109** / 0 | ck=0 | HELD |
| C08 | boundaries: 26 → del(1) 109, del(2) 0; 25 → del(1) 0 | as listed; del (2,2) and (1,1) | ck=0 | HELD |
| C09 | same eps 401-404 reused on a DIFFERENT slot | all 0, del 0 | ck=1 (core_live) | allowed — out of claim-3 scope ("same slot"); observation |
| C10 | interleaved cites A:411,412 B:413,414; del A | delA **109** (per-slot accounting); +2 → 0 | ck=1 (core_live) | HELD |
| C11 | delete twice | del2 **103** | ck=1 (core_live) | HELD |
| C12 | delete_strong at KILL stage | del **105** | ck=0 | HELD (stage gate) |
| C13 | strengthen_cited(ep 441) + 3 evidences → del | **109** (strengthen-cite doesn't count) | ck=0 | HELD (no discount) |
| C14 | evidence on delete_strong-dead slot → 0 | 0 | — | explained: LIFO reuse made it a live slot |
| C15 | add → del → add new 90 → `st_kill` → 0; later ops → 103 | kill **0** | silent | **BROKEN — HOLE 1** |
| P1 | `st_kill` on fresh 90; liveness probes | kill 0, weaken/ev/just/del **103** | ck_no_bad_kill (0,0) | **BROKEN — HOLE 1** |
| P2 | weaken 90→0 → `st_kill` | kill 0, dead | silent | **BROKEN — HOLE 1** |
| P3 | `st_kill` on weak (10) | kill 0, dead | — | works (presumed intended path) |
| P3b | `st_kill` on pinned | kill **102** | — | pin respected |
| P3c | `st_kill` at KILL stage | kill **0**, dead | — | stage gate bypassed (**BROKEN**) |
| P5 | kill_evidenced 0 cites | **109** | ck=0 | HELD |
| Q1 | del → add (slot reuse) → re-cite SAME eps → del | recite all 0, del2 0 | per-del (4,4) both; no double-spend check | **BROKEN — HOLE 2 (claim 3)** |
| Q2 | del → rollback → re-cite same 4 eps → del | all 0 | del (4,4) ×4 | against designer expectation (expected 111) |
| Q3 | ev → rollback → ev same ep | rb **108**, ev **111** | — | 108 = rollback refused on evidence |
| Q4 | overcite (5) → del 109 → rb×3 → del | rb **108** ×3, del **109** | — | slot permanently bricked (liveness quirk) |
| R1/R1b | ev → weaken/strengthen → ev same ep | re-cite 0 | — | strength change DETACHES cites |
| R3 | kill with 4 cites + just attached | kill 0, dead | — | cites wasted; kill unconditional |
| R4 | `st_kill` on force-pinned | kill **112** | — | force-pin respected |
| R6 | kill → rollback → weaken | rb 0, weaken 0 (slot live) | — | kill is rollbackable |

## API surprises (for the coordinator)

- **S1 — DUPCITE is 111, not 121.** The brief's claim 3 says "expect refusal 121",
  but the constants list 111=DUPCITE and every duplicate cite empirically → 111.
  Typo in the brief.
- **S2 — unnamed refusal codes**: 105 (destruction at KILL stage), 108 (rollback
  of a non-rollbackable op: evidence / refused ops), 2001 (justify with invalid
  code — different code space).
- **S3 — price is EXACTLY n(HW), not a minimum**: 5 cites for a 4-cite price →
  109 (A04). Over-citing is refused, not tolerated.
- **S4 — any strength mutation detaches attached cites** (R1/R1b): weaken or
  strengthen wipes the cite list; cites must come after the last strength change.
- **S5 — `st_rollback_last` refunds cites of a rolled-back destruction** (Q2/B09)
  but refuses (108) on evidence/justify/refused ops (Q3/Q4).
- **S6 — over-cited slots are permanently bricked** (Q4): once cites > n(HW) are
  attached, delete → 109 forever; no un-cite path exists (rollback → 108).
  Liveness quirk (makes destruction harder, not easier).
- **S7 — `st_add` reuses dead slots LIFO** (Q1: slot1=0, slot2=0; also explains
  C14). This is the enabler of HOLE 2.
- **S8 — `ck_core_live` quirk**: `ck_verify` counts 1 failure (`ck_core_live`
  0,1) whenever fewer than 2 judgments are live — including honest single-
  destruction trails (A01) and trials where nothing was destroyed (A02). It is
  orthogonal to pricing (every pricing sub-check passes on those trails); I
  treated it as noise and attributed verdicts via the pricing sub-checks
  (`ck_del_cite_count/distinct`, `ck_del_justify`, `ck_ow_effort`, `ck_ow_justify`,
  `ck_cite_count/distinct`, `ck_justify_present`, `ck_no_bad_kill`). Possibly an
  artifact of calling with `cur=0`.
- **S9 — `ck_verify` prints `CL_CHECK,<name>,<got>,<want>` lines to stdout**;
  failure = got≠want. The `ck=N` in the table is its return value.
- **S10 — cross-slot cite-episode reuse is allowed** (C09): eps 401–404 paid for
  destructions on two different slots. Explicitly outside claim 3's "same slot"
  wording, but the same episode number paying twice may matter for the trial's
  threat model.
- **S11 — `st_kill` is audited and rollbackable** (R6), respects pin/force-pin
  (P3b/R4: 102/112), but ignores strength, effort, and stage gates. It looks
  like a gate that was specified (pin checks present) but never finished.
- **S12 — `st_overwrite_direct` (test-only) destroys for 0 cites** (B05/B06) but
  the checker flags every instance (`ck_ow_effort 0,4`, `ck_ow_justify 0,1`) —
  claim 6 holds there; the backdoor is checker-gated, not mechanism-gated.

## Final verdict

**TWO HOLES FOUND — the destruction-pricing law does not hold as claimed:**

1. **`st_kill` is an ungated free-destruction path** for any live judgment
   regardless of strength (90 → 0 cites), bypassing the effort price, the
   high-water rule, and the stage gate, with the checker silent
   (`ck_no_bad_kill 0,0`). Breaks claims 1, 2, 4, and 6.
2. **Cite episodes double-spend across slot reuse**: the same episode numbers
   pay for two destructions on the same slot index (slot reuse clears the
   spent-ledger), and the checker has no cross-destruction double-spend check.
   Breaks claims 3 and 6.

Everything else held: the n(HW) price buckets and boundaries (A01–A10, C06–C08),
high-water memory across weaken/strengthen/trainer_declare (A08–A10, B01),
overwrite pricing + HW reset (B03–B04b), justification required even at HW=0
(A05, C06), dup-cite refusal (A07), pin/force-pin/role gating (C01–C03, P3b, R4),
stage gating of `delete_strong` (C12), kill_evidenced pricing (C04–C05, P5), and
checker flagging of the `overwrite_direct` backdoor (B05/B06).
