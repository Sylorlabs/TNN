# PREREG: SEM-L3 — Learner-Invented Concept Unification from Experience

**Status:** FROZEN (committed before any implementation)
**Date:** 2026-09-28 (overnight research session)
**Track:** Track 7 (Semantic understanding), L3 target
**Research question:** Can TNN invent the equivalence "different surfaces → same concept"
from experience, without being taught the equivalences, in a way that is
white-box, causal, revisable, and transfers?

---

## 1. Exact hypotheses

**H-SEM-0 (null):** Without taught equivalences, a TNN learner cannot exceed the
literal-retrieval floor on paraphrase-heavy probes. Semantic gain requires
hand-supplied equivalence tables (L0) or taught derivation edges (L1).

**H-SEM-1 (candidate — consequence-anchored unification):** A learner equipped
with a generic unification mechanism will create concept nodes unifying surfaces
that systematically license the same predictions, achieving paraphrase and
composition performance far above the literal floor, while correctly refusing to
unify near-misses. The concept nodes are learner-created (L3): the specific
groupings are not enumerated in source, arise after experience, are visible in
white-box state, and their removal causally degrades performance.

**H-SEM-2 (alternative — relational-role equivalence):** Unification based on
identical relational roles (same relations to same relata, ignoring outcomes)
suffices. If H-SEM-1 and H-SEM-2 both pass, the discriminating test is the
distinguishing-consequence probe: H-SEM-1 refuses unification when a
distinguishing consequence exists even under identical relational roles;
H-SEM-2 unifies anyway (and should fail that probe).

## 2. Why it matters

Large-scale ingestion proved TNN can store 9M facts (L0) but cannot use them
(3/250 audited; retrieval is keyword IR). Semantic competence — understanding
that different surfaces refer to the same concept — is the largest measured gap
between TNN and LLM-style systems, and the likeliest reason a rational user
would still prefer an LLM. This experiment tests whether TNN can close that gap
by invention (L3) rather than by importing embeddings (forbidden) or hand-coded
synonym tables (L0).

## 3. Minimum implementation (pure Zag, zero RNG, deterministic)

Three components, all pure Zag:

1. **World generator** (`sem_world.zag`, frozen at prereg): deterministic
   synthetic world. Entities E1..En, properties, relations. Each entity/property/
   relation has 2–3 surface variants (e.g., E1 = "norpal" / "the squeezer" /
   "object-7"). Emits teaching facts (sentences with mixed surfaces) and sealed
   probes. The generator's internal entity IDs are NEVER visible to the learner.
   Includes near-miss entities (similar surface, different consequences) and
   distinguishing facts.

2. **Learner** (`sem_learn.zag`): experience store (surface triples +
   provenance episode IDs); signature builder (for each surface, the relational
   contexts it appears in); unifier (proposes concept nodes on high signature
   overlap with no distinguishing triple); inference (resolves query surfaces
   to nodes, retrieves via nodes, composes multi-hop); splitter (on later
   distinguishing evidence, splits the node, records provenance).

3. **Evaluator** (`sem_eval.zag`): runs sealed probes, scores against generator
   ground truth. Evaluator/cognition separation: probes reference entity IDs;
   learner sees only surfaces.

**Forbidden:** any file, table, or code path mapping surface variants to each
other or to entity IDs inside the learner. The learner discovers groupings or
it fails.

## 4. Teaching protocol

- Teaching set: ~150 facts over ~30 entities, surfaces mixed randomly per fact
  (seeded, deterministic). No equivalence statements. No paraphrase pairs.
- Near-miss entities: 6 (surface-similar to a real entity, ≥1 distinguishing
  consequence taught).
- Late distinguishing evidence: 4 facts taught AFTER initial unification that
  force a split (Track 6).
- The learner processes teaching once, in fixed order, then unifies, then is
  evaluated. No teaching item appears in the probe set (surface-disjoint probes).

## 5. Sealed evaluation

Probe classes (all surfaces disjoint from teaching surfaces where applicable):
- **P-PARA** (60): paraphrase queries — same underlying fact, novel surface
  combination. Literal retrieval scores ~0 by construction.
- **P-NEAR** (40): near-miss — similar surface, different entity. Correct =
  WITHHOLD or correct distinct answer (no false unification).
- **P-SHIFT** (30): meaning shift — same words, different relational role.
  Correct = not conflated.
- **P-COMP** (40): 2-hop composition with novel surface combinations
  (norpal→glim→vellum chains). No teaching fact contains the full chain.
- **P-DIRECT** (30): literal recall (sanity: learner must also do L0).
- **P-SPLIT** (10): post-split queries after late distinguishing evidence.
- **P-TRANSFER** (30): fresh surface domain (new vocabulary, same latent
  structure), ≤5 teaching examples per new surface.

## 6. Metrics

Per-class accuracy (no averaging into one number). Plus:
- unification precision/recall against generator entity IDs (white-box check)
- false-unification rate (unified distinct entities)
- missed-unification rate (failed to unify same entity)
- split correctness on P-SPLIT
- examples-to-criterion on P-TRANSFER
- CPU time, peak RAM, learner-state bytes

## 7. Negative controls

- **C-LITERAL:** keyword/literal retrieval baseline. Must pass P-DIRECT,
  fail P-PARA/P-COMP (validates the probes test semantics, not recall).
- **C-SHUFFLE:** same unifier, but teaching signatures randomly permuted across
  surfaces. Nodes created must NOT help (validates groupings, not node machinery).
- **C-TAUGHT (L1 upper bound):** learner given the true equivalences. Bounds
  achievable performance; H-SEM-1 must approach it without the gift.

## 8. Ablations

- **A-NODES:** remove invented concept nodes → inference falls back to literal.
  Must drop to C-LITERAL floor on P-PARA/P-COMP (causal evidence nodes do work).
- **A-NOSPLIT:** splitter disabled → P-SPLIT must degrade (late evidence
  corrupts or is ignored).
- **A-NODIST:** distinguishing-triple check disabled → P-NEAR must degrade
  (over-unification).

## 9. Preregistered kill bars

- **SEM-K1:** P-PARA ≥ 80% (C-LITERAL expected ~0%).
- **SEM-K2:** P-NEAR ≥ 85% correct non-conflation.
- **SEM-K3:** P-COMP ≥ 70%.
- **SEM-K4:** A-NODES drops P-PARA+P-COMP to within 10pp of C-LITERAL
  (else nodes aren't causal).
- **SEM-K5:** P-TRANSFER ≥ 70% with ≤5 examples/surface (C-LITERAL needs
  full reteaching by construction).
- **SEM-K6:** determinism — 3 runs byte-identical including allocator
  perturbation.
- **Verdict rule:** H-SEM-1 ADOPTED iff K1–K6 all pass. Any single bar fails →
  H-SEM-1 KILLED (record which bar, preserve evidence). H-SEM-0 survives iff
  K1 fails while C-TAUGHT passes (semantics needs teaching, not invention).

## 10. What positive evidence would establish / NOT establish

**Would establish:** TNN can invent semantic equivalences from experience (L3
on the concept-node structure), use them for paraphrase/composition, refuse
false unifications, revise on distinguishing evidence, and transfer the
mechanism. This is a genuine new semantic mechanism, not embeddings, not a
synonym table.

**Would NOT establish:** general language understanding; that the mechanism
scales to 9M facts (separate experiment); that TNN "understands" in any
philosophical sense; that the unification criterion itself was invented (the
criterion is generic machinery — the L3 claim is on the invented nodes, as
preregistered).

## 11. Likely failure modes

- Over-unification: threshold too lax → P-NEAR fails. (Tune threshold ONLY on
  a dev split; the sealed set is never touched during tuning.)
- Signature sparsity: 150 facts may underdetermine groupings → missed
  unifications. (Mitigation: generator guarantees ≥4 shared contexts per
  true pair; documented in world spec.)
- The unifier discovers the generator's surface-template pattern rather than
  semantics (e.g., "surfaces sharing a prefix unify"). Red team must test
  with template-breaking surfaces.
- Composition fails for lack of multi-hop inference, not unification —
  P-COMP would then fail while P-PARA passes, implicating inference, not
  concepts. (Diagnose, don't patch the probes.)

## 12. Run now or defer

**RUN NOW** as the night's primary L3 experiment. It is the highest-information
single experiment available: it attacks the largest measured gap with a
falsifiable L3 design, reuses the sealed-corpus methodology, and a clean kill
(H-SEM-0 survives) is as informative as a pass — it would pinpoint the exact
architectural limitation blocking semantic invention.
