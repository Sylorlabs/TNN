# TRACE_WEDGE.md — Crew A (causal chain): the exact mechanistic causal chain of the F6 G-mode wedge

Date: 2026-09-26. Phase 1 — TRACE ONLY. No mechanism file modified, no fix proposed.
Workdir: `~/workspace/strength-f6/wedge/`

## 0. The whole story in plain English

Under G ("global single-use"), the mechanism derives each slot's consumed-episode set **from the append-only audit ledger** — there is no stored set, and the ledger can only grow, so the derived set can only grow. A priced destruction needs 4 episodes that are *fresh on that slot*; each OK destruction permanently burns the 4 episodes it cited **on its own slot**. With a finite pool of P salient episodes re-cited forever, each user slot is a fuse of exactly P/4 priced destructions: after P/4 OK destructions the slot has burned every pool episode, the next attempt 121-refuses, the memory stays stuck in the slot, and the driver's first-free-slot ADD walks on to the next slot. Fourteen user slots × P/4 destructions each = **3.5×P** evidenced destructions, then all 14 slots hold 121-refused memories, ADD finds no free slot (104 FULL), and every later op dies at the door (2001). Nothing — not rollback, not waiting, not overwrite/strengthen/weaken/trainer-declare — can unburn an episode, because consumption is recomputed from ledger entries that no code path removes.

Two things the headline number hides: (1) the "3.5" is exactly **14 user slots ÷ 4 cites-per-destruction** — a bookkeeping ratio, not a deep constant; (2) the implementation scopes consumption **per slot**, while the signed law English says "on any slot" — a spec/implementation gap (§5) that moves the wedge ceiling from P/4 (specified) to 3.5P (implemented).

## 1. Reproduction

**Driver:** `~/workspace/strength-f6/wedge/wedge_trace.zag` (new file; mechanism untouched).
It replays `f6_trial.zag`'s `f6_stress()` op-for-op in G mode — identical store setup
(`st_init(16,32768)`, `st_set_cite_mode(GLOBAL)`, two `st_add_core` seeds, stage FULL),
identical 160-cycle loop (`st_add` → 4×`st_evidence` citing `(4n)%pool..+3` → `st_justify` →
`st_kill_evidenced`), ops called unconditionally exactly like the original (bad-slot calls
return `cl_bad()=2001` before touching the ledger, so the ledger is bit-for-bit the original's).

**Instrumentation:** per cycle it prints slot chosen, rc of every op, the live-slot bitmask,
and — via the mechanism's *own* `st_cite_consumed()` (the exact predicate the kill path uses) —
the per-slot consumed-episode bitmask for all 14 user slots. Ends with a full per-slot dump
(live, value, strength, consumed mask, #OK destructions, #121s) plus `ck_verify` /
`st_refusals_clean` / `st_replay_check`.

**Verification:**
- Both pool sizes run twice, outputs byte-identical (`cmp` clean): `trace_S8_r1/r2.log`, `trace_S16_r1/r2.log`.
- Window buckets (ok / 121 / other per 10 cycles) are **identical** to the original F6 logs
  (`../logs/str_G_S8_r1.log`, `../logs/str_G_S16_r1.log`) — the reproduction is faithful.
- A Python model of the mechanism (below) predicts **all 320 cycles with zero mismatches**:
  exact slot, exact ADD rc, exact kill rc per cycle, for both pool sizes.

## 2. The mechanism, precisely

### 2a. Which slots clog, in what order, and why

Slots clog in strict numeric order **2, 3, 4, …, 15** — the first-free-slot order of `st_add`
(`while(slot<slot_cap){if(live[slot]==0)break;}`), slots 0–1 being the CORE seeds.

For pool P there are m = P/4 disjoint cite-sets S^(k) = {4k,4k+1,4k+2,4k+3}, cited in rotation
S^(0),S^(1),…,S^(m−1),S^(0),…. Each slot's visits are *consecutive cycles* (an OK destruction
frees the slot, so the next ADD lands right back on it — the driver only moves on after a 121
leaves the slot occupied). Consecutive cycles cite consecutive rotation sets, all disjoint,
so each slot absorbs **exactly m OK destructions** (one per set) and then the (m+1)-th visit
re-cites an already-consumed set → 121 → slot clogged forever.

Clog schedule (121 cycle for user slot s, s=2..15): **n = (s−2)·(m+1) + m**.
- P=8 (m=2): slot 2 @ n=2, slot 3 @ n=5, …, slot 15 @ n=41. Trace: `C n=2 slot=2 kill=121`,
  `C n=5 slot=3 kill=121`, …, `C n=41 slot=15 kill=121`. ✓
- P=16 (m=4): slot 2 @ n=4, …, slot 15 @ n=69; wedge (first 104) @ n=70. ✓

Trace excerpt (P=8; `cons=` is the 14 per-slot consumed masks, 15=eps{0–3}, 240=eps{4–7}, 255=all):

```
C n=0 slot=2 … kill=0   live=3    cons=15:0:0:…
C n=1 slot=2 … kill=0   live=3    cons=255:0:0:…
C n=2 slot=2 … kill=121 live=7    cons=255:0:0:…      ← first 121; slot 2 stuck
C n=3 slot=3 … kill=0   live=7    cons=255:240:0:…
C n=4 slot=3 … kill=0   live=7    cons=255:255:0:…
C n=5 slot=3 … kill=121 live=15   cons=255:255:0:…     ← slot 3 stuck; walk continues
```

### 2b. Exact op sequence: first 121 → ADD→FULL cascade

**First 121 (P=8, n=2; general: n=m).** Within the cycle, every op *before* the kill succeeds:
`ADD→0` (slot 2), 4×`EVIDENCE→0` (re-citing consumed episodes is legal — the dup-check is
per-window, i.e. since this cycle's ADD — and *citing* is free; only *paying* consumes),
`JUSTIFY→0`, then `KILL_EVIDENCED→121`. Inside `st_kill_effort_check`
(`strength_core.zag`): `lss` = this cycle's ADD index; `total` = 4 distinct cites in the
window; `spent` = `st_count_spent_cites(...)` = 4, because `st_cite_consumed` finds the
earlier OK destruction d₀ on slot 2 whose payment window `(st_last_add_idx(d₀), d₀)`
contains EVIDENCE entries for all four episodes; `cnt = 4−4 = 0 ≠ need = 4`, and since
`spent > 0` it returns **`ST_REFUSED_CONSUMED` (121)** rather than 109. The refusal is
audited with before==after snapshots (`st_refusals_clean` passes). Slot state untouched:
the memory (value 802, strength 90) stays live; live mask goes 3→7.

**The walk (n=m+1 … 14m+13).** Each subsequent cycle: `st_add` scans from slot 0, takes the
first non-live slot, and the new occupant gets m OK destructions (citing the m sets in
rotation order) followed by exactly one 121. Per slot the ledger shows `ok_destroyed=m`,
`r121=1`, consumed mask = full pool.

**The cascade (P=8: n=42; general: n=14(m+1)).** After slot 15's 121, all 16 slots are live
(`live=65535`). The cycle's `st_add` finds no free slot → audits `ST_OP_ADD` with
**rc=104 (`ST_REFUSED_FULL`)**, `out_slot=-1`. Then, op by op, the mechanism does nothing:
`st_evidence(-1)` → `st_badslot` → `cl_bad()` = **2001** (returns *before* any ledger append);
`st_justify(-1)` → 2001; `st_kill_evidenced(-1)` → 2001. Trace: `C n=42 slot=-1 add=104
ev=2001,2001,2001,2001 just=2001 kill=2001`. This repeats identically for n=42..159 —
118 cycles of ADD→FULL. No recovery: every slot's consumed mask is full (255/65535), so
even a freed slot could never again pass a priced destruction citing pool episodes.

Audit-entry accounting at the wedged state (P=8, `audit_n=415`): 3 setup entries
(2×ADD_CORE + SETSTAGE) + 42 live cycles × 7 ops (ADD+4×EVIDENCE+JUSTIFY+KILL) = 294
+ 118 wedged cycles × 1 op (the refused ADD; the 2001s append nothing) = 118. 3+294+118 = 415. ✓

### 2c. Per-slot citation accounting: why exactly 3.5×P

- One priced destruction of a strength-90 memory needs `need = ceil(90/25) = 4` fresh episodes.
- The pool of P episodes contains exactly **P/4 disjoint 4-sets**; a destruction burns one set
  on its slot, and a set burned on a slot can never pay there again.
- Hence each user slot hosts **at most P/4 OK destructions**, each burning 4 *distinct,
  previously-unburned-on-that-slot* episodes → P episode-burns per slot, zero overlap.
- 14 user slots × P episode-burns ÷ 4 per destruction = **14P/4 = 3.5P destructions**.
  The "3.5" is 14 slots / 4 cites-per-kill — pure bookkeeping. (P=8: 28; P=16: 56; P=32: 112. ✓)

The driver is *optimal* against this ceiling: every slot's m sets are each used exactly once
(the model predicting all 320 cycles with 0 mismatches proves no burn is wasted), so no
cite policy over the same pool and slot count can exceed 3.5P under the implemented rule.
Why not P: each destruction burns 4 episodes, not the whole pool. Why not 7P or more: the
per-slot burn sets must be disjoint, capping each slot at P/4.

### 2d. Why the consumed set never shrinks — and who owns it

There **is no stored consumed set**. `st_cite_consumed(s,slot,cite_ep,after_idx,upto)`
(`strength_core.zag`) recomputes the predicate from scratch on every kill check: for each
OK `KILL_EVIDENCED`/`OVERWRITE` destruction d on *that slot* with index in
`(st_consume_lo(...), upto)` — under G, `st_consume_lo` returns −1, i.e. the whole ledger —
it asks whether an OK EVIDENCE entry for `cite_ep` sits in the destruction's payment window
`(st_pay_lo(s,slot,d), d)`, where `st_pay_lo` = `st_last_add_idx(s,slot,d)` under G.

The data it reads is owned by **`st_audit_append`**, and the ledger is strictly append-only:
the only write to `audit_n` outside init is `s.*.audit_n = s.*.audit_n + 1` (line 265); a
grep of the core confirms no decrement, no truncation, no compaction path exists.
`st_rollback_last` does **not** remove the OK destruction entry — it appends a new
`ST_OP_ROLLBACK` entry and restores slot words from the rolled-back entry's before-snapshot
(red-team attacks 2/5 confirmed consumption survives rollback on every path). Therefore the
derived consumed set is **monotonic by construction**: entries only ever become consumed,
never un-consumed. No function — mechanism or checker — owns a mutable set to shrink;
the "set" is a pure function of ledger history.

### 2e. The wedged state, dumped

Final dump (P=8; P=16 identical in shape with mask 65535, ok=4):

```
DUMP audit_n=415 clock=415
DUMP slot,live,value,strength,consmask,ok_destroyed,r121
DUMP 2,1,802,90,255,2,1
DUMP 3,1,805,90,255,2,1
… (slots 4–14 identical in shape: live=1, strength=90, consmask=255, ok=2, r121=1)
DUMP 15,1,841,90,255,2,1
WEDGE ckfail=0
```

Internal picture: every user slot holds a live strength-90 memory (each the occupant whose
destruction was 121-refused — values 802,805,…,841 are the `800+n` tags of the clogging
cycles); every slot's consumed mask covers the entire pool (255 = all 8 episodes burned on
that slot: 2 destructions × 4); each slot's ledger slice shows exactly 2 OK priced
destructions and 1×121. `ck_verify` + `st_refusals_clean` + `st_replay_check` all pass
(**ckfail=0**): the wedge is a *legal* mechanism state, not a corruption — the checker
agrees the memories are unkillable. Not force-pinned, yet not even TNN itself can remove
them through any priced path: a de-facto permanent freeze with no trainer behind it.

## 3. Mechanism-caused vs driver-caused

**Forced by the mechanism (either reading of G):** given a *finite* episode pool and *any*
slot-reuse, the wedge is inevitable. Each priced destruction permanently burns 4 pool
episodes (per-slot under the implementation; store-wide under the specified law); once
cumulative destruction demand exceeds the pool-derived budget, no priced destruction can
ever succeed again, occupied slots never free, and ADD→FULL is the terminal state. The
naive driver already achieves the mechanism's information-theoretic ceiling (3.5P), so the
wedge point is not a driver artifact.

**Driver-caused (the wedge's *preconditions*, not its logic):**
- The "cite the same P salient episodes forever" policy is what makes the pool finite.
  The honest policy ("cite the 4 freshest episodes", pool grows with time) never wedges:
  3986/3986 OK at 10×, zero late-horizon refusals, ledgers byte-identical across modes.
- First-free-slot ADD fixes the clog *order* (2→15) and the exact wedge *timing*, but any
  reuse order converges to the same 3.5P total.
- The driver never abandons a 121-refused memory (it just moves on); a policy that kept
  unkillable memories deliberately would wedge identically — abandonment only changes
  which slots clog, not whether.

**In short:** the driver supplies the finite pool; the mechanism supplies the irreversibility.
Either alone is harmless (infinite pool → no wedge; G without reuse → each slot burns once).
Together they brick the store.

## 4. Spec/implementation gap found during the trace (no fix proposed)

`st_cite_consumed` scopes consumption **per slot**: it only credits destructions with
`st_aw(s,d,1)==slot` (same slot as the check). The code comments are consistent with this
("consumed by ANY earlier OK destruction **on the slot**"; "effort window of an OK
destruction … **on the same slot**"). But the F6 plain-English law, the red-team brief, and
the draft amendment text all state store-global consumption: "**on any slot**" (verdict),
"can pay for only ONE destruction EVER" (brief). Empirically: at n=3 the driver cites
episodes 4–7 on slot 3 and destroys OK, although episodes 4–7 were burned by n=1's
destruction **on slot 2** — under the specified store-global rule that kill would 121.
The F6 attack battery and the blind red team never tested cross-slot reuse (every sequence
used a single slot), so the gap survived both. Consequence for this trace: the measured
3.5P wedge is the wedge *of the implementation*; under the specified law the same driver
would wedge at **P/4** total destructions (pool exhausted once, everywhere — first 121 at
n=P/4, then every slot 121s on first contact).

## 5. Open questions the trace could NOT answer

1. **Intent of the slot scoping (§4):** is per-slot consumption the intended meaning of
   "global" (global = no *time* reset, slot-scoped), or a deviation from the "on any slot"
   amendment text? Only the law's author (Micah) can resolve; it moves the wedge ceiling
   14× (3.5P vs P/4).
2. **Real citation-supply dynamics:** the wedge needs the salient pool to stop growing.
   Whether TNN's actual re-citation behavior resembles the STRESS fixed pool or the HONEST
   ever-fresh policy is outside this trace — the mechanism cannot distinguish them.
3. **Recycling-fork inheritance:** the deliberate-recycling fork reuses slots explicitly;
   under the implemented rule it inherits this wedge verbatim (each recycled slot still
   burns P/4), but that needs its own run, not this trace.
4. **Scale cost:** G's kill path re-scans the ledger per episode per destruction
   (the verdict's 16-min-vs-1-min honest-path gap); I confirmed the scan structure but did
   not profile this driver.
5. **`st_kill` on a wedged slot (not run):** by code reading, the free kill clears liveness
   but the ledger's OK destructions persist, so a re-ADDED memory still cannot be
   *priced*-destroyed with pool episodes on that slot — occupancy recovers, priced
   destructibility does not. Worth one driver run by whoever audits recovery moves.
   (Note: `st_kill` is trainer-gated per Micah's 2026-09-25 ruling regardless.)

## Evidence

- Driver: [wedge_trace.zag](sandbox://workspace/strength-f6/wedge/wedge_trace.zag)
  (imports the unmodified `../strength_checker.zag` → `../strength_core.zag` via symlinks;
  no mechanism file touched).
- Binary: `~/workspace/strength-f6/wedge/wedge_trace_bin`
- Logs (each byte-identical ×2 via `cmp`): [trace_S8_r1.log](sandbox://workspace/strength-f6/wedge/trace_S8_r1.log),
  [trace_S16_r1.log](sandbox://workspace/strength-f6/wedge/trace_S16_r1.log)
  (`_r2` copies co-located).
- Mechanism read: `~/workspace/strength-f6/strength_core.zag`
  (`st_cite_consumed`, `st_count_spent_cites`, `st_consume_lo`, `st_pay_lo`,
  `st_last_add_idx`, `st_kill_effort_check`, `st_audit_append`, `st_rollback_last`).
- Fidelity: instrumented window buckets identical to `../logs/str_G_S8_r1.log` /
  `../logs/str_G_S16_r1.log`; hand-derived causal model predicts all 320 cycles
  (slot, ADD rc, kill rc per cycle) with 0 mismatches.
