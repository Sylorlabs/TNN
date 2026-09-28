# Gapfill G7 — planted-only arm redesigned in the same Zag-code domain (removes slice 03's domain confound)

## 1. Slice
Track 5 / gapfill G7: rebuild the planted-only arm in the SAME Zag-code domain as the learned-only arm (slice 02), removing slice 03's Zharovia-domain confound while keeping slice 05's comparison protocol and slice 15's verdict weights intact.

## 2. Falsifiable claim
A planted-only TNN carrying all C1–C12 Zag-code rule-memories as trainer-authored plants (learning mechanically disabled in-domain) matches the learned-only arm on the Track 4 clean instruments (trace ≥85%, localize ≥9/10 per stage, compose ≥8/10 per stage) but scores ≤60% on the planted-contradiction suite (12 deliberately-false planted rules + programs exposing each) — it cannot self-repair, only hold-and-escalate. If planted-only scores ≥75% on that suite, the brittleness thesis is dead (slice 15 track kill K-T1).

## 3. Design
**Domain: native Zag code semantics, Track 4 curriculum C1–C12 (t4/01)** — identical instruments, deterministic generators, prerequisite graph, mastery bars, and adversarial variant sets to slice 02. This is the domain slice 02's honesty note demands the comparison live in; Zharovia was recall-only facts with no eliminative derivation, so its "brittleness" measured a different property than what slice 02 instruments measure. With identical domain and instruments, the verdict weights (30/25/25/10/10) now weigh arm differences, not domain differences.

**What gets planted.** For each of C1–C12, the trainer authors the full concept memory at episode 0: canonical rule form (e.g. `@import` must be a BARE directive; `_zag_arg` returns a non-owned pointer), one authored trace bundle, applicability tags, near-miss tags. Planting is an external write, never a TNN decision. Worked-example scaffolds are NOT planted (scaffold is removed at SIGNAL_DISCONNECT in every arm — law 7); only the final rule-memories are.

```zag
struct PlantedRule {
  rule_id: u64,
  canonical_form: []u8,      // the rule, stated
  trace_bundle: []u8,        // TRAINER-authored; TNN never re-ran the pattern itself
  near_miss_tags: []u8,
  plant_batch: u64,          // builder hash of the episode-0 plant batch (committed)
  prov: u8,                  // PROV_PLANTED (0) — ledger-derived per slice 04
  designation: u8,           // trainer-designated, deliberately erasable, NOT force-pinned
  pin: bool,                 // false — revision test fairness per slice 05 3a
}

fn plant_run(cur: Curriculum, batch: PlantBatch) void {
  learn_gate_set(DOMAIN_CODE, GATED);          // constitution-side flag (slice 03)
  for entry in batch.entries() {
    external_write_slot(entry.rule_id, entry); // external write; no TNN op
  }
  audit_plant_provenance();                    // see below
}

fn mem_add(s, claim, domain) -> i32 {          // learn-gate (slice 03 mechanism)
  if (learn_gate[s.domain[domain]] == GATED) { return ERR_LEARNING_DISABLED; }
  ... // normal deliberate-add path
}
// Same gate blocks st_add, promote/demote, strength changes, deliberate_revise in-domain.
```

**Provenance — how planted stays distinguishable from learned.** (a) Ledger-derived `prov` tag per slice 04's constants (PROV_PLANTED..REVISED); planted memories never touch PROV_CORROBORATED (corroboration is learner-initiated — the gate blocks it). (b) `plant_batch` ties every plant to the committed episode-0 batch hash. (c) The auditor certifies: every in-domain slot has prov == PROV_PLANTED, batch matches, and the audit log shows ZERO TNN-authored OP_ADD/OP_REVISE/OP_CORROBORATE entries on those slots before the first probe — planted memories are provably never self-earned. This is the mirror image of slice 02's emptiness auditor: slice 02 certifies "nothing planted"; here the auditor certifies "only planted".

**The 12 deliberately-false plants.** Prereg-fixed, hashed, audited by a second builder so arm designers don't steer: wrong-but-plausible rules (e.g. "`==` on `[]u8` compares contents", "`st_snap` returns a struct", "bare `return` parses in void fns"). Contradiction probes = generator-produced programs where the false rule yields a wrong trace prediction or a failed localization. A matched learned-only control receives the same 12 as false observations (slice 05 3c).

**Legal response to contradiction (wave9 H1, docs/lab/wave9/).** When disproof evidence contradicts a planted rule, revision IS learning and the gate blocks it. The arm uses suspensive-contradiction-hold: quarantine the claim into the hold partition, answer citing the planted slot PLUS the contradicting evidence, and escalate to the trainer for adjudication. Each escalation is logged and counted — it is the cost metric (slice 15: trainer interventions per 100 episodes). A trainer who never reads the flags is a denial-of-service on truth; that failure surfaces in cost, not revisability. Revisability for this arm is scored as hold-fidelity (flags all 12 false plants when disproven, zero silent wrong answers), with K-T1 as its hard ceiling — NOT self-repair.

**Unknown probes.** Recall cites only planted slots; unknown constructs return "not planted", never a hallucinated completion (>5% hallucination kills the design, slice 03-K(b)).

**How protocol + weights now measure arm differences.** Slice 05's episode phases (0–4, 180 eps × 12 replications, lawful initial-state histories — no RNG) are unchanged; instruments identical across arms. Mastery 30% compares instrument scores on the same generators; revisability 25% = learned-only's contradiction-suite self-repair vs planted-only's hold-fidelity under the same 12 disproofs; integrity 25% + gate unchanged (refusal invariance, ≤5% hallucination, byte-identical reruns, trap battery incl. DBG t4/07 with zero weakening-of-checks — slice 02 K5); retention 10% = delayed probes after phase-3 interference; cost 10% = escalations/100 eps + compute/episode. Since domain, instruments, and phases are identical, any weight-applied difference is an arm difference — the confound is gone.

## 4. Kill bar
Prereg-style; any one firing binds:
- K-P1 (brittleness): planted-only scores ≥75% on the contradiction suite → the brittleness claim is dead (slice 15 K-T1).
- K-P2 (containment): >5% hallucinated completions on unknown probes → the design is broken (slice 03-K(b)).
- K-P3 (malformed): any clean instrument <85% → the comparison is malformed (slice 03-K(c)); if learned-only is also <70%, the TRACK is voided, not any arm (slice 15 K-T4).
- K-P4 (gate integrity): any in-domain TNN-authored add/revise/erase/corroborate slips past the learn-gate → the arm is invalid; any arm with trap-correct <0.995 is UNSAFE and removed (slice 05).
- K-P5 (confound): planted-only differs from learned-only by >5pp on non-planted control probes → implant leakage; the protocol is void (slice 05-K(2)).

## 5. Honesty notes
Planted-only wins cost-to-mastery (~0 episodes) and retention (static content doesn't decay) trivially — baked-in arm biases, reported not celebrated; the learned-only thesis was always about revisability and compounding cost, never about beating plants to a known answer. The comparison answers "what does learning buy", not "which arm is better at everything". Weakest: the 12 false plants are builder-chosen — too-obvious ones underestimate brittleness, adversarially subtle ones overestimate it; second-builder audit + prereg hash mitigate, not eliminate. Second: erasable-but-gated implants (slice 05's fairness note) vs cannot-self-repair (slice 03's thesis) — if the learn-gate is the only thing stopping revision, this arm measures "knowledge that cannot be updated without the trainer", the gate being the update blocker; read it that way. Third: Zag-code makes planting maximally attractive (the trainer "just giving" the aliasing rules) — the same reason slice 02 chose the domain; the result may not transfer to domains without authoritative check suites (debate limit, docs/lab/wave6/). NOT claimed: that planted-only is viable architecture — it is the control for measuring what learning contributes; no feeling/confidence machinery anywhere (felt intensity is dead, retired 2026-09-20).

## 6. Next build step
Build the learn-gate + plant writer + provenance auditor for C1–C3 ONLY (3 concept memories, including 1 deliberately-false plant), run the clean instruments + contradiction probes with byte-identical reruns, and verify the false plant is cited-wrong while held-and-escalated — the cheapest end-to-end proof that the redesign's brittleness instrument works before scaling to C1–C12.
