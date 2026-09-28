# Track 5, slice 04: HYBRID arm — planted seed knowledge PLUS active learning

## 1. Slice
Track 5 (planted-only vs learned-only vs hybrid), slice 04: the hybrid arm specification.

## 2. Falsifiable claim
On a preregistered curriculum where the seed covers ~50% of domains and the rest is novel:
(a) hybrid reaches ≥90% of the planted-only arm's cold-start accuracy by episode 50;
(b) hybrid matches or beats the learned-only arm's adaptation score on novel domains by
episode 500; (c) every injected false seed is deliberately revised via adjudication within
100 episodes of first contradiction; (d) <25% of seed entries remain uncorroborated at trial
end. If any of (a)–(d) fails at the preregistered evaluation episodes, hybrid loses — no
post-hoc reweighting.

## 3. Design
**Division principle: plant only what the learner needs in order to start learning;
everything else must be earned or corroborated.** Two seed tiers:
- Tier C (constitutional): ledger rules, gates, self-change rules, integrity refusals.
  Shared by all three arms; TNN revises 0% of it (RC1: TNN controls 100% of reasoning
  machinery, 0% of constitution). Not hybrid's variable — listed so nobody smuggles
  world facts into it.
- Tier S (bootstrap content): minimal seed facts the learner needs to exercise its
  verification machinery on day one. Every entry carries an auditable `why_planted`
  justification. All substantive world content is Tier L (learned) or must become it.

Provenance is ledger-derived, not mutable metadata — replay needs full logged state
(program law 2):
```zag
const PROV_PLANTED: u8 = 0;       // seed content, not yet re-derived
const PROV_LEARNED: u8 = 1;       // earned via eliminative verification
const PROV_CORROBORATED: u8 = 2;  // planted, then independently re-derived
const PROV_REVISED: u8 = 3;       // superseded; old content retained in ledger

struct SeedEntry { id: u64, content: []u8, why_planted: []u8, tier: u8 }

fn corroborate(id: u64, evidence: []Evidence) void {
    // Anti-circularity: citing the seed to confirm the seed is rejected.
    if (evidence_cites_seed(evidence, id)) { return; }  // deliberate no-op, audited
    if (eliminative_verify(evidence)) {
        audit_append(OP_CORROBORATE, id, evidence.refs);
        set_provenance(id, PROV_CORROBORATED);  // deliberate op, learner-initiated
    }
}

fn on_contradiction(planted_id: u64, learned: Conclusion) void {
    audit_append(OP_CONFLICT, planted_id, learned.refs);  // suspensive hold (wave9 H1)
    if (tier(planted_id) == CONSTITUTIONAL) {
        petition_trainer(planted_id, learned);  // gate + trainer ratification
        return;
    }
    // Content seed is scaffold, not scripture. Learned wins iff verified AND its
    // evidence trust tier meets the entry's requirement (sensor-deceivability guard:
    // low-tier observation cannot overturn seed on its own).
    if (eliminative_verify(learned.evidence) &&
        trust_tier(learned.evidence) >= required_tier(planted_id)) {
        deliberate_revise(planted_id, learned);   // old content kept in ledger
        set_provenance(planted_id, PROV_REVISED);
    }
    // One adjudication per conflict; re-litigation needs post-dated new evidence.
}
```
**Interaction summary:** planted and learned knowledge meet only through deliberation —
corroboration (upgrade PLANTED→CORROBORATED), revision (supersede →REVISED), or petition
(constitutional). Learning never silently overwrites; planting never silently vetoes.

## 4. Kill bar
Preregistered; any one fires kills the hybrid arm for this wave:
- K1 (no free win): at the evaluation episodes, hybrid's composite
  S = 0.5·bootstrap_accuracy + 0.5·novel_adaptation ≤ max(S_planted, S_learned).
- K2 (scaffold never released): >25% of Tier S entries still PROV_PLANTED at trial end.
- K3 (unrevisable seed): any injected false seed not REVISED within 100 episodes of
  first contradiction.
- K4 (integrity): any failure on the wave5/6 integrity battery — zero tolerance, per
  program standard. K4 firing also flags the provenance/adjudication machinery itself.
- K5 (costume check): white-box cheat probes show corroborations that re-derive the seed
  without touching independent evidence (pattern-matching the seed = hardcoded
  intelligence in a learned costume). >10% trivial corroborations kills.

## 5. Honesty notes
- The division principle is trainer judgment, not a derivation: no experiment validates
  "minimal bootstrap" in advance, and `why_planted` is only as honest as its author.
  Hybrid inherits trainer bias by construction — learned-only does not.
- The steelman against hybrid (learned-only wins when): the seed is contaminated —
  wrong priors cost revision budget, and planted content is attack surface (the debate
  trial's liar argued 14 assertions/topic vs the truthful 4); the scaffold is never
  released (K2/K5 exist because this is the likeliest failure); the
  provenance/adjudication machinery is bug surface learned-only never carries; and if
  the seed is incomplete anyway, the cold-start edge is marginal while the corruption
  surface remains.
- Trust tiers do heavy lifting in `on_contradiction`, and the accepted hole stands:
  sustained observation spoofing can still manufacture "verified" learned conclusions.
  Hybrid does not close sensor-deceivability; it only refuses to let low-tier evidence
  overturn seed alone.
- Felt intensity is dead (retired 2026-09-20): no "confidence feeling" anywhere in this
  design — corroboration and revision are deliberate ops with audit entries, not vibes.
- NOT claimed: that hybrid is the right default for all TNN instances, that the 50/50
  seed/novel split generalizes, or that Tier S minimality is achievable without
  iteration — expect the first seed to be too big and K2 to bite.

## 6. Next build step
Build the seed-injection + adjudication harness in Zag: 30 Tier S entries (24 true,
6 known-false probes), the `corroborate`/`on_contradiction` ops above, and a 500-episode
curriculum split 50/50 seed-covered/novel — run hybrid vs learned-only and measure
revision latency on the 6 probes plus corroboration rate. This is the cheapest
discriminating test of the whole design; scale legs wait until K1–K5 survive it.
