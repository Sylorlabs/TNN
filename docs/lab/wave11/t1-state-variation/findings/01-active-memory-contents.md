# Slice 01 — Active-memory contents as a state variable (Track 1)

## 1. Slice
Formalize exactly which live-memory contents feed the deterministic variation function: slots,
fields, canonical order, and the pure projection it consumes — plus what is excluded and why.

## 2. Falsifiable claim
Let `P(M)` be the projection defined below. Claim: over a benchmark of 200 lawfully-different
memory states (identical verdicts, pins, kills, ledger), at least 15% of pairs produce
byte-different expression with byte-identical verdict sections; and replay of any (input,
logged full state) reproduces output byte-identically across 1,000 reruns. If either fails,
the claim — and this slice's design — is dead.

## 3. Design
The variation function consumes ONLY `P(M)`, a pure deterministic projection of live slots.
Canonical read-out (never hash-map order):

```
fn project_memory(m: *Mem, out: *u8 /*32 bytes*/) void:
    h = sha256_new()
    for ctx in 0..m.n_ctx:                    // ascending context id
        for s in 0..m.ctx[ctx].n_slots:        // ascending slot index
            slot = &m.ctx[ctx].slot[s]
            if slot.state != LIVE: continue    // killed/archived slots excluded
            h.update(slot.ctx_id)
            h.update(slot.slot_idx)
            h.update(slot.content_sha)         // 32B content fingerprint, precomputed at add
            h.update(slot.salience_tier)       // u8 tier, not raw float
            h.update(slot.strength_level)      // judgment-set level; never formula-accumulated
            h.update(slot.prov_code)           // 0=self,1=world,2=sensor,3=trainer
            h.update(slot.pin_flag)            // 0/1 human force-pin (audited, law 8)
            h.update(slot.epoch_added)         // u64; deterministic age ordering
    h.finalize(out)
```

Per-slot tuple fields enumerated above are the preregistered state-variable list for this
slice (Track 1 law: no mystery variables). `content_sha` is computed once at deliberate-add
time via the substrate's native SHA-256 (`R33_NATIVE_SHA256_V2.zag`, per MA1 audit design —
see `docs/lab/wave3/...` memory substrate notes). The expression layer takes `P(M)` as a
seed for lawful choice among pre-deliberated expression alternatives (ordering of supporting
points, which salient live example to cite first, elaboration depth); the verdict path never
reads `P(M)` — architectural separation, not discipline. Verdict code and expression code are
separate Zag modules with disjoint inputs: verdict sees `(input, memories)`; expression sees
`(verdict-record, P(M))`. Full state (all slots incl. killed, all fields) is logged per MA1
audit; replay uses the logged state, not the live one.

## 4. Kill bar
KILL if any of: (a) any replay of logged full state yields a byte difference vs the original
run over 1,000 reruns (reproducibility law); (b) any of the 200 benchmark pairs shows a
verdict-section byte difference when only `P(M)`-visible metadata differs (verdict leak);
(c) fewer than 15% of the 200 lawful-state pairs produce byte-distinct expression
(variation bar missed — this slice contributes nothing); (d) any field outside the
preregistered list is observed influencing expression output (mystery variable).

## 5. Honesty notes
Weakest point: the verdict/expression module split is enforced by builder discipline in Zag,
not by the toolchain — a future edit could wire `P(M)` into verdict code silently. A static
check (gated import list: verdict module may not reference `project_memory`) is needed and
not yet designed. `content_sha` covers only live slots, so a kill op changes `P(M)` — that
is lawful (kill is a deliberate memory decision, logged). Excluded fields: raw content bytes
(too large; the hash is sufficient and avoids content resurfacing through expression),
verdict-status flags of hypotheses (leaking those would let expression encode the verdict
path — expression may *reflect* the verdict via the verdict-record input, never via `P(M)`),
audit entries, and killed slots' contents (expression must never resurrect killed material).
Not claiming: that 15% variation is "enough humanity" — only that this slice's contribution
is measurable and non-zero.

## 6. Next build step
Build `project_memory` in Zag over the committed MA1 substrate, wire it to a toy expression
layer (3 pre-written phrasings of one conclusion), and run the 200-pair benchmark: generate
pairs by lawful salience/strength edits only, diff expression bytes vs verdict bytes, and
report the variation rate plus any verdict byte-diffs. This single run tests the claim,
exercises the kill bar, and produces the canonical-order determinism evidence.
