# Muse Leg — convenor-authored steelmanning (NOT independent subagents)

Per 00_BRIEF.md method caveat: at depth 2/2 spawning is disabled, so this leg is
first-person adversarial steelmanning by the convenor, argued against my own
synthesis as hard as I can. Round 2 reacts to the Sol leg's Round 1; Round 3
reacts to both legs' Round 2.

## Round 1 — openings

### (a) Novelty = absence of a matching installed fact — STEELMAN
1. The ledger is the only ground truth about what TNN knows. "Novel" must mean
   "not already known," and "known" is operationally = installed in the ledger.
   Anything else smuggles in a second, un-audited theory of knowledge.
2. It makes "I learned nothing" a checkable claim: scan corpus claims against
   the ledger; if all match, the corpus had nothing new. No new machinery.
3. It cleanly separates novelty from installability — the distinction LI-1
   needs. LI-1's Newton claims were NOVEL (no matching installed fact — the
   ledger held beginner-guides G1–G6, not physics) but UNINSTALLABLE
   (no corroboration). So the honest H3 verdict on LI-1 is "corpus HAD novelty;
   the install gate withheld it by design" — neither "nothing new" nor
   "learner broken." H3's phrasing conflates novelty-detection with
   install-success; (a) is the position that forces the conflation into the open.
4. The audit trail is trivially complete: per claim, the ledger entries
   consulted and the match verdict for each. A replayer reproduces the novelty
   verdict byte-identically.
5. Hardest question: (2) the sockpuppet tension — but note it precisely. (a)
   needs a match function M. M=byte-identity: paraphrases of known facts count
   as novel (over-novelty — safe direction, never installs by itself). M=semantic
   threshold: re-opens the A2/A9-class attacks the adjudication closed, now on
   the novelty side. Honest partial answer: freeze M=byte-identity for the
   operational novelty bit (ungameable, auditable), and run paraphrase
   detection as a separately-labeled HEURISTIC flag that can never cause an
   install. Price of honesty: systematic over-novelty on paraphrase-heavy
   corpora — measurable, bounded, safe.

### (b) Novelty = failure of corroboration — STEELMAN
1. Parsimony: no new machinery, no match function, no threshold. Novelty falls
   out of the existing ≥2-source gate. What nobody else corroborates is exactly
   what "new to the discourse" means.
2. It never asks the gameable question. (b) never compares a claim to the ledger
   semantically; it only asks the byte-identical question the substrate already
   answers deterministically. The sockpuppet tension dissolves — there is no
   paraphrase-tolerant matcher anywhere.
3. The novelty verdict IS the verdict trail: which pages were compared, which
   sentences matched. Auditability for free.
4. Hardest question: (1)/(3) combined — (b) collapses novelty into
   un-installability and makes novelty corpus-relative, not learner-relative.
   A false singleton (A4 red-team) is "novel" under (b): is a made-up claim
   novel? And "already installed and re-corroborated" vs "brand new and
   corroborated" both clear the gate — (b) cannot tell "corpus had nothing new"
   from "corpus had new things I already knew," which is precisely H3's
   distinction. Honest partial answer: (b) must smuggle (a) back in — check the
   ledger too — at which point it is (a) plus a redundant gate. As a standalone
   definition of novelty, (b) fails H3; as a component (installability axis), it
   is indispensable.

### (c) Novelty = surprise relative to the world-model — STEELMAN
1. The only position that makes novelty genuinely learner-relative: a claim is
   novel iff the learner didn't already expect it. A reworded known fact is
   entailed → not novel, with no similarity threshold anywhere — paraphrase
   handled by entailment, not by string comparison.
2. Matches the "figure it out" direction: the learner predicts, the world
   surprises. "I learned nothing" = "nothing surprised me" — the most natural
   reading of H3.
3. Deterministic operationalization exists: NOVEL(c) ⟺ c is not derivable from
   installed facts within a bounded derivation budget. The failed derivation
   trace IS the audit trail — arguably richer than (a)'s match list.
4. Hardest question: (4), priced honestly. Bounded derivability is budget-fragile:
   a claim entailed by a 10,000-step chain reads as novel under a 100-step
   budget — so "novel" becomes "novel-relative-to-budget," and the budget is a
   free parameter exactly like the similarity threshold. Worse, (c) risks
   circularity: the world-model is built from installed facts, so (c) ≈ (a)
   with "match" replaced by "entailment" — strictly harder to compute, same
   attack surface, new parameter. Honest partial answer: (c) is the right
   *intuition* and the wrong *mechanism* for H3's verdict — unless the mechanism
   crew independently needs derivation-bounded surprise for curiosity-driven
   querying, (c) adds nothing over (a) that H3 can use.

### (d) Novelty = learner uncertainty; determinism challenge — STEELMAN
1. Dissolves a category error: novelty was never a property of claims. "Novel"
   = the learner's epistemic state toward the claim is undecided. A settled
   claim (true OR false) is not novel however worded — paraphrase handled
   without any matcher: rewording doesn't unsettle a settled state.
2. Deterministic uncertainty is real, not faked. A chess engine is uncertain
   without dice: it holds a set of live alternatives and a bounded search that
   hasn't settled. Uncertainty = structure of the undecided set — a
   deterministic function of state. Probabilities were never the essence;
   unsettledness was.
3. "I learned nothing" becomes trajectory-checkable without corroboration and
   without ledger matching: did the undecided set shrink over the run? That is
   the most direct operationalization of H3's contrast.
4. Hardest question: (4) + mechanism gap. (d) gives a per-learner-state
   verdict; the mechanism crew needs a per-claim verdict. A claim can be novel
   (undecided) and false (A4 singleton) — (d) must still say what to DO with
   novel claims, which drags G4 back in. And "undecided" needs a halting rule;
   the halting budget is a free parameter like the similarity threshold. The
   determinism defense is philosophically sound but doesn't hand the crew a
   number: the uncertainty functional (live-alternative count? derivation-budget
   exhaustion? cross-source conflict score?) is unspecified. Honest partial
   answer: (d) is the best *foundation* and an incomplete *mechanism*. For H3's
   verdict, (d) should be recorded as the direction of the uncertainty
   functional, with the functional itself a separate preregistered experiment —
   not load-bearing for the "nothing new vs failed to learn" verdict.

## Round 2 — rebuttals (convenor, reacting to Sol leg Round 1)

### Vs (a) — Sol's firewall, and the worse error direction
Sol's key move — "semantic similarity may establish non-novelty relative to an
already installed fact, but must never establish corroboration or authorize
installation" — is correct and I adopt it: the novelty matcher must be
causally disconnected from the install path. My strongest objection is about
the ERROR ASYMMETRY Sol's "conservative matcher with borderline→unknown" hides.
Two failure modes: (i) over-novelty — a paraphrase of a known fact marked novel
(wastes attention, installs nothing, safe); (ii) false-known — a genuinely new
claim semantically matched to an installed fact ("water boils at 100c at sea
level" vs "water boils at 90c at sea level" share almost all tokens) and marked
not-novel, so the learner never attempts the correction. Mode (ii) LOSES
KNOWLEDGE; mode (i) only wastes attention. A "conservative" semantic matcher
must pick which mode to be conservative against, and the borderline→"unknown"
third verdict just pushes the choice to the consumer of the verdict. The
asymmetry favors byte-identity for the operational novelty bit: its only
failure mode is (i), the safe one.

### Vs (b) — Grok convicted his own position
Grok's "honest partial answer" concedes (b) needs "one explicit
'store-semantic match' clause in the corroboration predicate" to handle
reworded known facts — which is (a)'s match function smuggled into (b)'s
gate. Concession accepted: as a STANDALONE definition of novelty, (b) fails,
because a corroborated-already-known claim and a corroborated-brand-new claim
are both "not novel" under (b), and H3's whole point is telling those apart.
Two further objections: (1) Under (b), "novel" correlates with
evidence-scarcity — the A4 false singleton is the most "novel" thing in the
corpus. If the mechanism crew uses novelty to prioritize corroboration effort
(the obvious use), (b) tells them to spend the budget on the LEAST trustworthy
claims first. Novelty-as-uncorroborated inverts the priority order a learner
wants. (2) (b) makes novelty corpus-relative rather than learner-relative: the
same claim is novel in one corpus and not in another, regardless of what TNN
knows. H3 is about the LEARNER's state ("I failed to learn"), not the corpus's.
Keep (b) as the installability axis — it is indispensable there — but it is
not a definition of novelty.

### Vs (c) — the normalizer relocates the problem into the ontology
Step's canonical-logical-form normalizer is the most interesting new proposal
in Round 1, and my objection is that it moves the paraphrase problem rather
than solving it. The normalizer must collapse semantically IRRELEVANT
distinctions ("Earth orbits the Sun" = "Earth travels around the Sun") while
preserving semantically LOAD-BEARING ones ("boils at 100c" ≠ "boils at 40c").
The distinction between load-bearing and irrelevant IS the semantics problem;
no fixed rule set can be verified to draw it correctly without already having
solved what it was built to avoid. Failure modes: under-collapse → paraphrases
stay novel (back to over-novelty, the safe mode); over-collapse →
contradictions merge into one canonical form, the merged claim reads "not
novel," and the learner never learns the correction (mode (ii) above —
knowledge loss, the catastrophic direction). Further: the "vetted lexical
ontology" is either hand-built — a human policy smuggled into the substrate,
against the figure-it-out law — or learned, in which case novelty verdicts
shift as the ontology learns and Tuesday's "novel" becomes Wednesday's "known"
for reasons opaque to the audit trail. A frozen byte-identity matcher has
exactly one failure mode and it is the safe one; the normalizer has two, and
one of them eats corrections.

### Vs (d) — node identity IS the match function
Swe's "Open node" formulation is the cleanest statement of (d), and it reveals
that (d) does not escape (a): proposition node-identity in the graph IS the
match function. Swe concedes the point: without canonicalization, a paraphrase
of a settled fact opens a new "Open" node and registers as novel — structurally
identical to (a) with M=byte-identity, plus graph overhead. Second objection:
novelty-as-assigned-status cannot PRIORITIZE. The status only exists after the
learner has attempted ingestion and inspected which nodes stayed settled — so
(d) cannot route novel claims to expensive corroboration up front, the most
likely mechanism-crew use case. (d) is an excellent *accounting* of what
happened (the undecided-set trajectory is the most direct H3 verdict), but as a
*detector* it is parasitic on whatever node-identity/match function the
ingestion layer already uses.

### Hardest objection to my own 2×2 + M_byte — the attention attack (conceded)
The "safe direction" claim holds for INSTALLS but not for ATTENTION. If the
mechanism crew spends a corroboration budget prioritized by the novelty bit,
M_byte's systematic over-novelty on paraphrase-heavy corpora becomes a
denial-of-attention vector: flood the corpus with paraphrases of settled facts
and the detector cries "novel" on all of them, starving genuine novelty of
corroboration effort. The heuristic paraphrase-suspect flag only mitigates this
if the crew trusts it — but then the heuristic is load-bearing after all, and
its false-negative rate re-opens the attack through the resource door. I
concede this has real force: the 2×2 decomposition needs a budgeted-attention
story (e.g., corroboration effort priced per claim, paraphrase-suspects
deprioritized but never install-relevant), or the paraphrase problem returns
through the resource door after being locked out of the install door. This is
the strongest reason the prereg crew should test paraphrase-rate effects on any
novelty-prioritized pipeline, not just install correctness.

## Round 3 — convergence (convenor)

### What Round 2 changed my mind about
1. Step's objection to (a) has force: the ledger does not exhaust what a
   richer TNN could know — model-entailed-but-unstated knowledge would
   false-negative under ledger lookup. For the CURRENT substrate (ledger + G4
   is all there is) this is moot, but it sets (a)→(c) as the principled upgrade
   path if implicit knowledge ever exists: "match" becomes "entailment within
   a bounded closure," inheriting the budget-fragility caveat. Noted, not
   load-bearing for H3 now.
2. Swe's "100% novelty rate" objection to (b) is decisive alongside Grok's own
   concession: (b) as a standalone definition is dead. Survives only as the
   installability axis.
3. Step's concession on (c) (surprise conflates model inadequacy with novelty)
   and Swe's concession on (d) (uncertainty collapses operationally into
   "not yet computed") are both honest and both weaken (c)/(d) as H3 mechanisms.
   (d) survives as accounting (undecided-set trajectory), not as detector.

### Recommended operational definition (for the mechanism crew)
Per claim c, given ledger L and frozen rule version v:
- **NOVEL(c)** ⟺ no entry of L matches c under frozen byte-identity M_v
  (G4's own normalization: lowercase + whitespace-collapse). Frozen,
  versioned, deterministic. A paraphrase of an installed fact counts as NOVEL
  (over-novelty — the safe error direction: it wastes attention, never causes
  an install, never suppresses a correction).
- **INSTALLABLE(c)** ⟺ G4 unchanged (≥2 independent sources, byte-identical).
- The H3 verdict is the **2×2 per claim**, aggregated per run:
  - novel ∧ installed → learned something new;
  - novel ∧ ¬installable → correctly withheld (the LI-1 cell — gate held);
  - ¬novel ∧ installed → re-corroborated known fact;
  - novel ∧ installable ∧ ¬installed → LEARNING FAILURE — the only cell that
    indicts the learner (mechanism bug, not a corpus property).
- "I learned nothing" is replaced by three counts, not one English sentence:
  (∀c ¬NOVEL(c)) → "corpus had nothing new"; (∃c NOVEL(c) ∧ ¬INSTALLABLE(c))
  → "corpus had novelty, nothing clearable"; the failure cell → "learner
  failed." **Hard question (3), settled:** "I learned nothing" is a RUN-claim,
  not a world-claim. G4 corroboration governs claims about the world;
  REPLAYABILITY governs claims about the run. The audit trail is its
  corroboration.
- **Paraphrase (hard questions 1–2), priced:** an optional, explicitly
  heuristic, never-install-relevant PARAPHRASE_SUSPECT(c → ledger entry) flag
  may feed attention-prioritization only, labeled with heuristic version,
  excluded from the audit-critical path. Rationale: error asymmetry —
  false-"known" LOSES knowledge (suppresses corrections like 100c→90c);
  over-novelty only wastes attention. Byte-identity's sole failure mode is the
  safe one. The attention-attack caveat from my Round 2 stands: if novelty
  prioritizes a corroboration budget, paraphrase floods are a
  denial-of-attention vector — the prereg crew should test paraphrase-rate
  effects on novelty-prioritized pipelines.
- **Audit trail per claim (hard question 4):** (i) normalized claim text;
  (ii) frozen rule/matcher version hash; (iii) ledger entries scanned +
  per-entry match verdict; (iv) novelty bit; (v) corroboration set examined
  (pages, sentences compared) + install/withhold verdict + firing gate;
  (vi) heuristic flags with versions, marked non-load-bearing. No timestamps.
  A replayer with the same ledger + corpus reproduces every bit byte-identically.
- **(c) and (d) disposition:** neither is load-bearing for H3's verdict.
  Recommend (d)'s uncertainty functional as a SEPARATE preregistered
  experiment, and (c)-style entailment matching as the upgrade path only if
  the substrate ever holds implicit knowledge beyond ledger sentences.

### Confidence: 70%
The 70% is on the structure: novelty≠installability, the 2×2, M_byte for the
operational bit, run-claims-governed-by-replay, and the error-asymmetry
argument for byte-identity — Round 2 tested all of these and none broke. The
30% uncertainty: (i) whether M_byte over-novelty is operationally tolerable at
web scale — needs the 213-URL measurement of the paraphrase-suspect rate;
(ii) whether the mechanism crew's actual consumer of the novelty bit
reintroduces the attention attack; (iii) the exact audit schema (freeze with
the prereg crew).

### Left open (for prereg/mechanism crews)
1. Empirical: paraphrase-suspect rate at web scale; tolerability threshold.
2. Fault-injection test: is the failure cell (novel ∧ installable ∧
   ¬installed) actually reachable and detectable?
3. The uncertainty functional (d) — separate experiment, own prereg.
4. Entailment-based matching (c) — only if implicit knowledge arrives.
5. Exact audit-trail schema — freeze jointly with the prereg crew.
