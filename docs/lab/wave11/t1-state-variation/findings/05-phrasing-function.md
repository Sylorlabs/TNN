# Slice 05 — The phrasing variation function

## 1. Slice
Track 1, slice 05: design the pure selection function mapping (input, logged-state projection) → surface phrasing, with every degree of freedom drawn from finite, preregistered inventories — no open-ended generation.

## 2. Falsifiable claim
A deterministic phrasing layer placed strictly after the verdict is fixed can produce ≥3 distinct surface renderings of the same verdict from lawful state variation, while (a) replaying input + full logged state always byte-reproduces the output, and (b) no rendering ever alters the verdict, memory decisions, integrity refusals, or ledger bytes — checked by a fixed equivalence oracle over all rendered outputs in a 100-episode trial.

## 3. Design

### 3.1 Inventory format (frozen at prereg commit, content-addressed)
```
struct Slot { class: u32; members: [][]u8; }   // ordered; members certified equivalent within `class`
struct Template { id: u32; holes: u32; text: []u8; }  // text holds "{0}".."{n}"; holes take verdict fields ONLY
struct Inventories {
  synonyms:    []Slot;   // e.g. class VERB_PROMOTE: ["promoted","elevated","advanced"]
  connectives: []Slot;   // class CONNECT_CAUSE: ["because","since","given that"]
  openers:     []Slot;   // class OPENER: ["For the record,","To be direct,","Plainly,"]
  templates:   []Template;  // finite sentence skeletons
  order_keys:  []u32;    // finite allowed rotation keys for reason-list ordering
  max_depth:   u32;      // cap on elaboration depth
}
```
Certification rule (prereg): every pair of members in a Slot passes a fixed propositional-equivalence check for its class (builder-run, evidence logged under docs/lab/wave11/t1/); a Template is admitted only if every hole-filling entails the same verdict under the oracle.

### 3.2 State projection (Track-1 prereg enumerated fields)
```
struct StateProj {
  ep: u64;          // episode counter
  ctx: u32;         // active context partition id
  store_n: u32;     // live memories
  kills: u32;       // kills in this context
  promotes: u32;    // promotions in this context
  last_op: u8;      // last deliberate memory-op code (prereg enum)
  reasons_n: u8;    // supporting reasons attached to the verdict
}
fn project(s: *FullState) -> StateProj { /* pure field copies; no computation on the input */ }
```

### 3.3 Selection function (pure)
```
fn fold(p: StateProj) -> u64 {   // fixed FNV-1a over the projection bytes
  var h: u64 = 1469598103934665603;
  // for each field byte b: h = (h ^ b) * 1099511628211;
  return h;
}
fn pick(s: *Slot, i: u64) -> []u8 { return s.members[i % s.members.len()]; }
fn render(v: Verdict, p: StateProj, inv: *Inventories) -> []u8 {
  let h: u64 = fold(p);
  let t: *Template = &inv.templates[h % inv.templates.len()];
  let o: []u8 = pick(&inv.openers, h >> 8);
  let c: []u8 = pick(&inv.connectives, h >> 16);
  let depth: u32 = 1 + ((h >> 24) % min(inv.max_depth, v.reasons.len()));
  let rot: u32 = inv.order_keys[(h >> 32) % inv.order_keys.len()];
  // holes filled ONLY from v: {0}=verdict subject, {1}=verdict object,
  // {2}=top-`depth` reasons in rotation-`rot` order
  return assemble(t, o, c, v, depth, rot);
}
```
`v: Verdict` arrives already final; `render` takes it read-only and cannot mutate verdicts, memory ops, refusals, or ledger. Variation lives entirely downstream of the decision.

### 3.4 Purity proof sketch
1. `render`'s only inputs are `(v, p, inv)`: `p` is field copies from the logged FullState, `inv` the prereg-frozen blob. No wall clock, no entropy syscalls, no uninitialized memory (Zag zero-init), no globals — every read traces to an argument.
2. `fold` is total over the projection bytes: same bytes → same `h`, always. All selection is `h >> k % len` — bounded indexing, no data-dependent early exits, no hidden branch.
3. Verdict content enters only through template holes; inventory certification (3.1) guarantees member swaps preserve the entailed verdict within the certified class.
4. Replay: logged FullState → `project` → identical `p` → identical bytes. The audit ledger records each rendering's hash next to its verdict, so any verdict/rendering divergence is provable post-hoc from committed evidence (cf. MA1 audit-with-replay, branch tnn-native-lab).

### 3.5 Worked example — same verdict, three lawful states
Verdict v: "slot 12 promoted — evidence threshold met."
- State A {ep:1041, ctx:3, store_n:40, kills:0, promotes:1, last_op:OP_PROMOTE, reasons_n:1}
  → T2 + OPENER[1] + VERB_PROMOTE[1]:
  "To be direct: slot 12 was elevated, since the evidence threshold was met."
- State B {ep:1042, ctx:1, store_n:38, kills:7, promotes:0, last_op:OP_KILL, reasons_n:2}
  → T5 + OPENER[0] + CONNECT_CAUSE[0], depth=2:
  "For the record, slot 12 was promoted because the evidence threshold was met and no counter-evidence survived elimination."
- State C {ep:1077, ctx:3, store_n:44, kills:1, promotes:3, last_op:OP_PIN, reasons_n:1}
  → T2 + OPENER[2] + VERB_PROMOTE[2]:
  "Plainly: slot 12 was advanced, given that the evidence threshold was met."
Same verdict entailed in all three; opener, verb choice, connective, and elaboration depth differ purely as a function of the projection fields.

## 4. Kill bar
Preregistered 100-episode trial, ≥20 distinct lawful states per verdict class. KILL if: (a) any rendered output fails the equivalence oracle (verdict drift) — dead on first failure; (b) replay of input + logged state reproduces output non-byte-identically even once — dead; (c) any verdict class with ≥20 distinct states shows <3 distinct renderings — dead (variation is the claim); (d) static build check finds any inventory member used in a slot class it was not certified for — dead.

## 5. Honesty notes
- Weakest link: equivalence certification is only as good as the oracle — a builder-checked claim, not a theorem. Near-synonyms ("promoted" vs "advanced") can smuggle connotation drift the oracle misses; Track 3 should red-team the inventory.
- `fold` distribution over tiny state changes is untested; adjacent states may cluster on one template (variation present but lumpy). No-free-lunch: FNV-1a is claimed pure, not optimal — benchmark folds hard.
- NOT claiming human-like style or that the variation is useful — only that it can be lawful and pure. If renderings read as noise rather than state-reflecting expression, that is a product failure, not a purity failure.
- A verdict with zero reasons cannot elaborate; the design must degrade to template-only variation and never invent reasons to fill depth — kill bar (a) covers this.

## 6. Next build step
Build the inventory certification harness first: implement `Slot`/`Template` structs, the pairwise equivalence oracle, and the static slot-class check as a native Zag build gate that fails compilation on any uncertified member — then freeze the first inventory blob and run the 100-episode replay trial against kill bar (b) before testing any variation at all.
