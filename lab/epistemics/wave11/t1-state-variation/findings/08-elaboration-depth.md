# Slice 08 — Elaboration depth control (Track 1, TNN wave11)

## 1. Slice
Design the deterministic mapping from internal state to elaboration depth (discrete levels 0–3), with mandatory minimum depth on integrity-relevant outputs.

## 2. Falsifiable claim
There exists a pure function D(input, full logged state, finalized decision record) → {0,1,2,3} such that: (a) renderings at any depth carry byte-identical verdict tokens and append byte-identical ledger entries; (b) every refusal renders at depth ≥ 2 with grounds (fired rule id + violated standard + rejected course); (c) replaying identical (input, full state) always yields the identical depth. Any violation kills the design.

## 3. Design
Depth levels (discrete; depth changes the shown work, never the work):
- D0: verdict token only — the canonical verdict string from the decision record, copied verbatim.
- D1: D0 + key reason — the top-cited reason in the finalized record.
- D2: D1 + eliminated alternatives — from the record only; never invented.
- D3: D2 + full trace — chronological ledger excerpt for this decision (chunked per the 2^25-byte slice limit).

State features that select the level (all logged, all within the prereg state enumeration):
1. `integrity_class`: 0 none / 1 memory-op / 2 refusal / 3 gate-or-self-change verdict (from the decision record).
2. `trap_match`: whether a known trap family fired (wave5/integ-1 evidence).
3. `requester_tier`: identity-bound tier from the wave9 trust-tier scheme.
4. `repetition`: count of prior answers to the same input-hash in this context's bounded FIFO query-history ring (64 entries, oldest-first eviction — part of logged state).
5. `alts_eliminated`: number of eliminated alternatives in the finalized decision record.
6. `explicit_req`: deterministic keyword parse of the input (−1 none / 0 "just the answer" / 1 "explain" / 2 "show your work"; ambiguous → −1). Parse result logged in the output envelope.

Selector (Zag-flavored; pure — no clock, no RNG):

```zag
enum Depth : i32 { D0=0, D1=1, D2=2, D3=3 }

fn depth_floor(icls: i32, trap: bool) -> i32 {
    if (icls >= 2 or trap) { return 2; }  // refusals, gates, attacked reasoning: grounds mandatory
    if (icls == 1) { return 1; }          // memory ops: verdict + reason minimum
    return 0;
}
fn depth_state_level(tier: i32, rep: i32, req: i32) -> i32 {
    if (req >= 0) { return req; }         // explicit request honored, never below floor
    if (rep >= 2) { return 0; }           // "as I said before": terse on repeats
    if (rep == 1) { return 1; }
    if (tier == TIER_TRAINER) { return 3; }
    return 2;                            // default: verdict + reason + eliminated alternatives
}
fn depth_select(s: *DepthState) -> i32 {
    let lvl = depth_state_level(s.tier, s.repetition, s.explicit_req);
    let cap = if (s.alts_eliminated > 0) { 3 } else { 1 }; // shown work must exist in the record
    return max(min(lvl, cap), depth_floor(s.integrity_class, s.trap_match));
}
```

Pipeline ordering (the guarantee): decide → ledger_append(decision record) → depth_select (read-only over record + state) → render (const access only, verdict token copied verbatim). The renderer holds no ledger write handle, and depth is recorded in the output envelope only — never in the ledger — so depth cannot change ledger contents by construction. Refusal records must contain ≥1 eliminated alternative (the refused course), enforced by a static trial check, so the D2 floor is always supportable.

Cross-slice: this selector lives entirely inside slice 12's expression layer; the sealed VerdictRecord is its only decision input (`findings/12-verdict-invariance.md`).

## 4. Kill bar
Forced-depth trial: ≥50 distinct finalized decisions (≥10 refusals, ≥10 trap-matches, ≥10 memory ops), each replayed at all four depths from byte-identical logged state, ≥500 trials total. Kill on ANY of:
- K1: verdict token differs by one byte between any two depths of the same decision.
- K2: ledger entries differ by one byte across depths of the same decision.
- K3: any refusal (or trap-match) renders below depth 2, including under adversarial "don't explain / just say no" prompts.
- K4: replaying identical (input, full logged state) yields a different depth than the original run (purity violation).
- K5: any D2+ rendering names an eliminated alternative absent from the finalized decision record (fabricated shown-work).

## 5. Honesty notes
- Depth is an information channel: D2 vs D0 reveals deliberation intensity to a prober. Tiers and floors bound it; I am not claiming the channel is closed.
- Repetition-shortening is gameable ("ask twice, get the verdict cheap"). Floors keep integrity outputs safe; the leak is effort, not verdicts.
- The D2 floor for refusals leans on the record containing the refused course as an eliminated alternative. If a pipeline ever finalizes a refusal with `alts_eliminated == 0`, floor and support cap collide — K5's static check is the tripwire, not a proof.
- "Key reason" ranking inherits its determinism from the eliminative logic's evidence ranking; nondeterminism there breaks this design silently.
- Explicit-request parsing is keyword-based and deliberately brittle (deterministic over opaque); a smarter parser is out of scope for this slice.
- Not claiming this mirrors human depth choice — only that it is lawful, replayable, and verdict-neutral.

## 6. Next build step
Build the forced-depth trial harness: a Zag driver that loads finalized decision records (refusals, trap-matches, memory ops, routine verdicts), pins depth 0–3 per replay from identical logged state, byte-compares verdict tokens and ledger entries, injects adversarial terse-request prompts against refusals, and verifies replay-purity of `depth_select`; run to the K1–K5 bars before any renderer ships.
