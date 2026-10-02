The 2b deadlock is real for any learner whose decision features are exactly the current generic firing pattern. Curriculum cannot separate two test items that still collide on those features, and no HARD0-clean rule may peek at marker bytes, item concept ids, or speaker. A broader fix has to change the feature space, factor the label, or amend the bars. Ranked by promise:

### 1. Scope-indexed markers (representation)
**Change.** Stop installing bare 2-grams. Install markers as `(governor-slot, bigram)` on a concept graph you already have: matrix governor vs embedded complement. "Ask if the shop is open" fires `(REQUEST-governor, if the)` because `if` sits under an ask/check/tell concept. "If the shop is open, …" fires `(MATRIX, if the)` because there is no governor. Governor-slot is an anonymous structural role (cluster of concept indices that take interrogative complements), not the bytes `if`, not a type constant, not an item id.

**Why it breaks 2b.** The sincere lookalike and the matrix hypothetical no longer share a firing pattern, so the banned distinctions are unnecessary. The split is compositional scope, which is in the utterance, not in the bars. Joke/deadpan only stays collapsed with the lookalike if you built those items to be scope-identical; then this approach does not touch that pair (see 3 and 5).

**Label.** FITS FROZEN CONSTRAINTS if roles are induced from dependency/concept-graph shape and decisions stay on integer indices. NEEDS PREREG AMENDMENT only if HARD0 is read as "n-gram identity is the only legal feature."

**Curriculum (needed so FL2 can revoke the old bare marker).** About 48 items, same supervision you already use (endorse / withhold), no type strings in the learner:
- 16 SINC endorse, embedded: "Ask if …", "Check whether …", "Tell me if …", governors varied, complements drawn from the frozen pool.
- 16 hypothetical withhold, matrix: "If …, then …" with no request governor.
- 16 holdouts that reuse the bigrams under the opposite scope.

FL2 then sees endorse and withhold on different scoped keys, so it can kill unscoped `("if the" → hypothetical)` without a handwritten if-rule. Volume matches your 8–16 exemplar regime; the extra count is only to cross the revocation threshold on both scopes.

### 2. Factored decision: illocution vs overlay modality (architecture)
**Change.** Two deterministic heads over the same indices. Head A is content/structure only: assertion, directive, matrix-supposition. Head B is overlay: joke, deadpan, quotation, roleplay. Hypothetical-SINC scoring reads Head A. Joke withhold reads Head B and may not consult speaker or discourse state. A later rule combines them (deadpan overlay suppresses SINC endorse; matrix-supposition is not SINC) without ever branching on type keywords.

**Why it breaks 2b.** The two bars stop demanding opposite polarity from one predicate. Joke content-only WITHHOLD and hypothetical discourse/structure sensitivity are no longer the same decision. You do not legitimize a banned feature; you stop forcing one score to satisfy both constraints.

**Label.** NEEDS PREREG AMENDMENT. State the change as: bars apply to named heads, not to a single endorse bit. Joke bar = Head B, content features only. Hypothetical-SINC bar = Head A, structure allowed, speaker still banned.

**Curriculum.** Keep current TR/PA/NO sets. Add the 48 scope items from (1) as Head A labels only. Add 8–16 joke/deadpan overlays whose *content head* matches a sincere twin, so Head B must carry the withhold. If a joke twin is byte-identical at Head A features, Head B still needs a content cue that is generic (known-fact contradiction, impossible degree). If no such cue exists, that pair is bar-impossible; do not invent an item id.

### 3. Redefine "content" in the joke bar to include composition (prereg, small)
**Change.** Keep one head, but preregister: legal content features include anonymous syntactic roles and scoped n-grams; illegal features remain marker-byte special cases, type constants, speaker, and item concept ids.

**Why it breaks 2b.** Crew 2b treats "generic firing pattern" as unscoped n-grams. Scope is generic and compositional, so the identical-pattern premise is an artifact of the feature inventory, not a fact about the world. This is the same mechanism as (1), with the audit trail written into the prereg so a later crew cannot re-ban it as if-specific.

**Label.** NEEDS PREREG AMENDMENT. One sentence: "content-only" = any feature computable from the utterance's concept graph without speaker, item id, or lexical lists of type words.

**Curriculum.** Same 48 as (1). No extra signal.

### 4. Contrastive endorse pool alone (curriculum under current features)
**Change.** Add sincere if-constructions to the frozen endorse pool so FL2 finally observes `("if the")` on both endorse and withhold.

**Why it does not break 2b.** It only fixes the characterized mechanism (pool never contained the contradiction). After revocation, every item that still fires the same generic pattern gets the same bit. The must-ENDORSE lookalike and the must-WITHHOLD joke then move together. You trade 3/10 for a joke-bar regression, or you refuse to revoke and stay at 3/10.

**Label.** FITS FROZEN CONSTRAINTS. Low promise; do it only as an ablation to confirm 2b, not as the fix.

**Curriculum.** 16 SINC endorse if-sentences, 16 existing hypotheticals. Predict both bars cannot clear together.

### 5. If the critical pair is scope-identical on purpose (architecture of the eval, not the net)
**Change.** Publish the minimal pair. If they differ only by speaker or by which concept id was memorized, no representation of the utterance can separate them without a banned feature. Split the eval: hypothetical-SINC items must be scope-different from hypotheticals; joke items must carry a generic content cue or be scored only on Head B. Drop any item whose gold label is not a function of legal features.

**Why it breaks 2b.** It accepts the proof. The asymmetry lives only in the joint bars, so the bars must be weakened or the items rebuilt until a legal feature carries the label.

**Label.** NEEDS PREREG AMENDMENT. Exact text: an item is admissible only when its gold endorse/withhold is determined by features allowed under HARD0 plus the amended content definition; speaker-only and item-id-only contrasts are unscored.

**Curriculum.** None until the admissible set exists. Then the 48 scoped items above.

**Order to run.** Implement (1) first; it is the only change that can move hypothetical-SINC without touching joke items that are actually scope-different. Turn on (2) or (3) before you touch joke-deadpan, or you will reintroduce the contradiction. Use (4) solely to show the frozen feature space cannot pass both bars. Use (5) on whatever remains tied after scoped features: those items are not a learner bug.