# ALPHABET_Y-Z — Invention Arms (Brainstorm Crew 5)

Date: 2026-09-20. Status: PROPOSAL (not preregistered; each arm needs Micah's sign-off on
arms/bars before any build). Pure-Zag, zero-RNG, byte-identical-rerun compatible by
construction unless noted.

Reading: this file is Crew 5's contribution. Front door: `INDEX.md`. Riskiest assumptions:
`RISKS.md`. Sibling crew files follow the naming convention `ALPHABET_<range>.md`
(see `INDEX.md` § Placeholder).

---

## Y1 — NEGOTIATED CHUNKS (two-organ protocol, mutual veto)

**Claim:** Chunk boundaries decided by a two-party protocol between the ingesting organ and
the recall organ are more recall-stable than boundaries decided by either alone.

**Mechanism (TNN-native):** Ingestion proposes a candidate cut (span, provisional ID). Recall
may VETO with a written justification ("this cut splits a unit I retrieve as one") or
COUNTER-PROPOSE an alternative boundary. Ingestion may accept or veto the counter. Deadlock
(>N rounds, N fixed and preregistered) escalates to the deliberate-consolidation organ, which
issues a binding cut logged to the audit ledger with both organs' proposals attached as
evidence. No randomness anywhere: veto reasons are drawn from a fixed, preregistered
justification enum; tie order is ledger order. The negotiation transcript is itself an
auditable memory (killable, but the final cut's ledger entry is append-only).

**Strengths (falsifiable):** Predicts negotiated boundaries survive ≥2× more revisions than
unilateral cuts without ID reassignment (measurable on the revision curriculum). Predicts
veto rate declines as the shared vocabulary matures (learning signal without reward).

**Weaknesses:** Two organs can collude into lazy agreement (veto rate → 0, boundaries
degenerate to whatever ingestion proposed — then Y1 ≡ D with extra ledger cost). Negotiation
doubles per-cut ledger writes (see RISKS.md R4). Deadlock escalation is a single point of
bureaucratic failure.

**Falsification criterion:** If, over 10,000 cuts, negotiated boundaries show ≤10% better
recall-stability than arm-D unilateral cuts at the same granularity, Y1 is dead. If veto
rate collapses to <1% within the first 1,000 cuts (lazy agreement), Y1 is dead as designed.

**Buildability:** Medium. The two organs already exist in the five-organ architecture;
add a propose/veto message type and a ledger schema for transcripts. Byte-identical replay
requires logging the full transcript (or: log only the final cut + both final proposals —
deterministic replay needs the transcript only if the consolidation organ's rule is not a
pure function of the proposals; make it one).

## Y2 — ADVERSARIAL CHUNKING (red-team segmentation, robustness objective)

**Claim:** A chunking scheme is only trustworthy if recall stays correct under worst-case
re-segmentations; the objective is robustness, not fit to one "true" segmentation.

**Mechanism (TNN-native):** Inside TNN, a red-team process (a dedicated revision organ with
no write access to memory — read-only) deliberately proposes worst-case segmentations:
pathological cuts (byte-by-byte, mid-word, maximal spans, permuted ID assignments within
legal bounds). After each red-team proposal, the recall organ must answer a probe set from
the corrupted-but-legal segmentation; eliminative hypothesis logic adjudicates whether
recall is still correct. Failures are logged as negative evidence against the *current*
chunking scheme, which the native structural-revision organ (organ 5) may revise via
propose/commit/rollback. The red team is deterministic: worst cases are generated from a
fixed preregistered adversary grammar, never sampled.

**Strengths (falsifiable):** Predicts schemes surviving Y2 red-teaming keep byte-exact
recall at 10× the revision rate that kills arm-D cuts. Directly attacks the sensor-deceivable
hole (the adversary models spoofed observation boundaries).

**Weaknesses:** Compute cost is brutal (adversary grammar × probe set per cut); likely
unaffordable at corpus scale (see RISKS.md R10). The adversary grammar is designed by
humans — a fixed grammar can be gamed by the chunking scheme, giving false confidence.
Worst-case thinking can veto genuinely good segmentations that fail only pathological cases.

**Falsification criterion:** If a scheme passes the full adversary grammar yet loses
byte-exact recall on a *held-out* adversary grammar (written by a different crew after
preregistration), Y2's certification is worthless — kill the certification claim. If
red-teaming cost per cut exceeds 100× the cut cost at 10× scale, Y2 is not buildable as
an online mechanism (survives only as offline certification).

**Buildability:** Hard online, feasible offline. The red team needs no new organs (read-only
probe harness + the existing five organs). Preregister the adversary grammar FIRST — it is
the entire claim. No RNG: adversary cases enumerated in grammar order, deduplicated by
content hash.

## Y3 — TEMPORAL / VERSIONED CHUNKS (identity = span + ingestion order + lineage)

**Claim:** A chunk is not a static span but a versioned entity; its identity must include
WHEN it was ingested and WHAT it became through revision.

**Mechanism (TNN-native):** Chunk ID = `(serial, birth_epoch, lineage_root)`. When revision
alters a chunk's span (split, merge, re-cut), the old ID is tombstoned in the ledger and a
new version `(same serial, epoch+1, lineage_root)` is issued; the ledger chains
`supersedes` pointers. Recall resolves an ID through the lineage chain to the live span —
old references never dangle. `kill` on a chunk kills the lineage head; history remains
auditable but unrecallable. Deterministic: versions are totally ordered by ledger sequence
number, no timestamps from the wall clock.

**Strengths (falsifiable):** Predicts zero dangling references after 10,000 revisions
(provable from the ledger: every tombstoned ID has a live successor or an explicit kill
entry). Revision-heavy curricula (code editing on sqlite3.c) keep recall correct where
position-addressed arm L breaks.

**Weaknesses:** Version chains can grow unboundedly (a hot chunk revised 10⁶ times = 10⁶
ledger entries; see RISKS.md R3/R4). Resolve-through-lineage adds indirection cost to every
recall; deep chains may violate recall-latency bars. Two chunks merged then split may never
recover their original IDs (lineage is a tree, not a group — history is not invertible).

**Falsification criterion:** If mean lineage depth exceeds 50 on the standard revision
curriculum (indicating fragmentation, not versioning), Y3 is dead. If any recall resolves
to a tombstoned span (dangling reference observed in the ledger), the mechanism is broken —
kill and fix before any further claim.

**Buildability:** Medium-hard. Needs a lineage index structure in Zag with the 2^25 slice
limit respected (chunk the index; corpora at 5.4MB/9.5MB are each indexable as one slice,
so the prototype fits). Tombstone GC policy must be preregistered (never silent).

## Y4 — QUESTION-DRIVEN CHUNKS (lazy, task-conditioned segmentation)

**Claim:** There is no correct segmentation until a question arrives; the question determines
the cut. Ingestion stores the raw stream plus cheap boundary *candidates*; commitment to a
segmentation happens at query time.

**Mechanism (TNN-native):** Ingestion performs only candidate-marking: deterministic,
low-cost boundary detectors (punctuation, blank lines, brace depth, indent shifts — a fixed
preregistered detector set) emit candidate cut points into the ledger. No chunks are formed.
On a recall question, the recall organ selects a subset of candidates conditioned on the
question's terms (deterministic selection rule: e.g., minimal covering span set under the
question's keyword constraints, ties broken by ledger order) and materializes chunks with
stable IDs for exactly the selected spans. Materialized chunks enter memory as first-class
citizens (kill/pin/promote apply). The question + selection rule + candidate set are logged,
so replay is byte-identical: same logged question, same cuts.

**Strengths (falsifiable):** Predicts 5–10× fewer stored chunks than eager arm D for the
same recall accuracy (storage efficiency is the claim). Predicts questions from a new
domain reuse the same candidate set without re-ingestion (no re-cut cost).

**Weaknesses:** Replay requires the question in the log — a chunk referenced by memory but
whose question is gone is unresolvable (see RISKS.md R9). Cold questions pay full
materialization cost; adversarial question streams can force materialization of the entire
candidate set (eager chunking in disguise, at higher cost). Candidate detectors are a fixed
tokenizer's shadow (see RISKS.md R2).

**Falsification criterion:** If, on the standard probe battery, Y4's recall accuracy is
>5% below eager arm D at equal total ledger cost (candidates + materializations), Y4 is
dead. If >30% of materialized chunks are never recalled twice (one-shot waste), the laziness
claim fails — kill.

**Buildability:** Medium. Candidate detectors are simple Zag string scans. The hard part is
the deterministic question-conditioned selection rule — it must be a pure function of
(question, candidates) to keep replay byte-identical. Preregister the detector set; changing
it later is a prereg amendment.

## Y5 — CROSS-STREAM CHUNKS (non-contiguous spans, one ID)

**Claim:** Some units of knowledge are discontinuous: a function's signature and its
distant call site, a name's definition and its uses. One ID should cover a span SET.

**Mechanism (TNN-native):** A chunk = `(ID, [span₁, span₂, …, spanₙ])`, spans ordered by
ledger sequence. Linking is deliberate: the consolidation organ issues a LINK op (audited)
binding spans, with a written justification (e.g., "definition-use pair, verified by
eliminative check E-17"). Recall of the ID returns all spans in order with their gaps
marked. `kill` on one span kills the LINK (the whole unit), never silently half of it —
kill cascades are atomic and logged. Pin/promote apply to the unit, not the spans.
Deterministic: span order is insertion (ledger) order.

**Strengths (falsifiable):** Predicts recall of definition-use and declaration-reference
pairs succeeds as ONE retrieval on sqlite3.c where contiguous-span arms (D, L) need ≥2
retrievals + a join the system must invent. Predicts fewer "lost reference" failures on
the code-revision curriculum.

**Weaknesses:** Kill semantics are aggressive (killing a call site kills the definition's
chunk) — may cause cascade amnesia; the atomicity rule is doing heavy lifting (see RISKS.md
R9/R11). Span sets can sprawl (a widely-used name links 10⁴ spans — recall cost explodes).
Overlaps with arm J (overlapping chunks) need a crisp boundary: J = spans that overlap in
bytes; Y5 = spans that are disjoint but semantically one unit.

**Falsification criterion:** If >20% of Y5 units on sqlite3.c degrade to single spans
within the revision curriculum (links die faster than they pay), Y5 is dead weight. If any
kill leaves a live span pointing at a dead LINK (dangling half-unit), the atomicity
mechanism is broken — kill the implementation.

**Buildability:** Medium. Span-set storage is a small extension of the span table; the
LINK op and cascade rule need new ledger entry types. Byte-identity is straightforward
(spans + ledger order). The eliminative justification for each LINK is the expensive part —
preregister which checks qualify.

## Y6 — FORGETTABLE CHUNKS (tombstone-native IDs, refcounted, kill cascades)

**Claim:** Units should be designed for clean death: deletion is a first-class operation,
not an afterthought, and a chunk's ID format should make deletion provably total.

**Mechanism (TNN-native):** Every chunk ID carries a generation + refcount in the ledger:
`(serial, gen, refs)`. Memory ops that reference a chunk (recall caching, Y5 links,
promotion lists) increment `refs` via audited REF entries; releasing decrements. `kill`
on a chunk with `refs > 0` either (a) fails loudly (logged refusal — the deliberate
choice) or (b) cascades, per a preregistered per-chunk policy set at creation. Tombstoned
IDs are never reused (`gen` increments; serials are never recycled). The audit ledger can
prove total deletion: chunk C is gone iff a KILL entry exists and no live REF entries
postdate it — a checker-verifiable invariant. No silent GC: any reclamation is a ledger op.

**Strengths (falsifiable):** Predicts zero unreclaimable-but-unreferenced chunks ("memory
leaks") after the churn curriculum, vs. measurable leak rates in arms without refcounting.
Predicts the kill-cascade policy is auditable by a third party from the ledger alone
(checker-verifiable — the integrity story extends to deletion).

**Weaknesses:** Refcounting every recall is ledger-expensive (every read becomes a write;
see RISKS.md R4). Refcount cycles (A refs B refs A) leak unless the checker also does
cycle detection — more machinery. Loud kill refusal can deadlock memory under churn
(everything pinned by something).

**Falsification criterion:** If ledger write volume under Y6 exceeds 10× arm D on the same
curriculum (refcount writes dominate), Y6 is unaffordable as designed — kill or move to
batched REF accounting (which weakens the provability claim and must be re-preregistered).
If any checker audit finds a live reference to a tombstoned ID, the mechanism is broken.

**Buildability:** Medium-hard. REF/UNREF ledger types, a refcount index, cascade-policy
table, and a checker proof procedure. Prototype on the 5.4MB prose corpus first (lower
churn). The 2^25 slice limit is not a binding constraint at prototype scale.

## Z1 — WITNESS-BOUND CHUNKS (a cut must survive elimination to exist)

**Claim:** A chunk boundary is a hypothesis. It becomes real only if it survives
deliberate attempts to eliminate it — the cut carries its own justification as
first-class evidence.

**Mechanism (TNN-native):** Every proposed cut enters a challenge window: the eliminative
hypothesis organ (organ 2) runs a preregistered challenge set against it ("this boundary
splits a recall unit," "this boundary is undetectable by an independent re-cut,"
"shifting it ±k bytes changes nothing"). A cut that survives becomes a chunk; its ID binds
`(span, challenge_transcript_hash)` — the witness. A cut that fails is logged as a
refuted proposal (auditable, not silent). Recall may cite the witness when justifying why
these bytes travel together. The challenge set is fixed at preregistration; the native
structural-revision organ may propose challenge-set revisions via commit/rollback, never
silent edits.

**Strengths (falsifiable):** Predicts witness-bound chunks have the lowest
"regretted cut" rate (cuts later revised away) of any arm — the challenge window is
pre-revision. Predicts the refuted-proposal log becomes a training corpus for better
cut proposals (negative evidence with provenance).

**Weaknesses:** Challenge windows serialize ingestion (throughput collapse under
streaming input). The challenge set is human-designed — same gaming risk as Y2's adversary
grammar. Binding the ID to the transcript hash means re-running challenges (e.g., after a
challenge-set revision) invalidates old witnesses — ID instability by design tension (see
RISKS.md R3).

**Falsification criterion:** If the regretted-cut rate is not ≥50% lower than arm D on
the revision curriculum, the challenge window buys nothing — kill. If challenge-set
revision invalidates >10% of live witnesses, the binding is too brittle — kill the binding,
keep the window.

**Buildability:** Hard. Needs the eliminative organ to expose a challenge API, a transcript
hash scheme (native SHA-256 substrate exists: R33_NATIVE_SHA256_V2.zag), and ID formats
that embed witness references. Byte-identical replay requires the challenge outcomes
logged, or challenges re-run deterministically from the log.

## Z2 — CONTRACT CHUNKS (a chunk is an audited obligation between organs)

**Claim:** Chunk identity should encode the promise, not just the bytes: "ingestion
promises recall these bytes byte-exact; recall promises to use them only for declared
purposes." Violations are detectable from the ledger.

**Mechanism (TNN-native):** Chunk creation issues a CONTRACT ledger entry:
`(ID, span, provider_obligations, consumer_restrictions, expiry)`. Provider obligations:
byte-exact recall, lineage notification on revision. Consumer restrictions: declared at
materialization (e.g., "recall-only," "may-compose," "may-quote"). A consumer op outside
its restrictions is a contract breach — refused loudly and logged (not silent). Expiry is
deliberate (set at creation, visible). MA4 signed memory values attach: the contract
carries the value-sign both organs agreed the chunk carries. Breach handling is
preregistered: refuse + log, never auto-repair.

**Strengths (falsifiable):** Predicts contract breaches catch misuse patterns (e.g.,
recall composing a "recall-only" chunk into a new claim) that silent arms miss — measurable
as breach-detection rate on a misuse probe battery. Predicts expiry reduces stale-chunk
recall vs. arms with no expiry concept.

**Weaknesses:** Contract negotiation per chunk is heavyweight (Y1's negotiation cost
squared — now the terms are negotiated too). Declared purposes require the consumer to
know its purpose in advance — fails for open-ended reasoning (the common case). Expiry
reintroduces time into identity (tension with Y3's versioning: is an expired chunk a new
version or a dead one?).

**Falsification criterion:** If breach-detection rate on the misuse battery is <80%
(contracts miss the misuse they exist to catch), Z2 is theater — kill. If >30% of
legitimate recall ops are refused as breaches (purpose declarations too narrow), the
restrictions are unusable — kill the restriction half, keep obligations.

**Buildability:** Hard. New ledger entry type with obligation/restriction schema, a breach
checker on the recall path (hot path — mind the znc hot-path miscompile history;
characterize before trusting), MA4 sign plumbing. Prototype with obligations-only first.

## Z3 — BUDGETED CHUNKS (granularity as an economic decision under scarcity)

**Claim:** Storage and access should be priced in one scarce currency; the system should
cut where the budget says cuts pay, not where a rule says cuts go.

**Mechanism (TNN-native):** A preregistered attention budget B per epoch (epochs are
ledger-delimited, not wall-clock). Creating a chunk costs `c_create` (ledger + index);
each recall costs `c_recall`; each revision costs `c_revise`. The consolidation organ
(organ 3) allocates: fine cuts where recall frequency × recall savings exceed creation
cost, coarse spans elsewhere. All prices are preregistered constants (no learned prices —
that would be reward-by-another-name; the felt-intensity retirement, 2026-09-20, is the
warning). Budget exhaustion refuses new chunks loudly (logged), never degrades silently.
The budget ledger is auditable: anyone can recompute spend from entries.

**Strengths (falsifiable):** Predicts total cost (storage + recall compute) on the
10× curriculum is lower than any fixed-granularity arm at equal recall accuracy —
the efficiency claim. Predicts graceful behavior under budget cuts (halve B → coarser
chunks, accuracy degrades smoothly, never catastrophically).

**Weaknesses:** Preregistered prices are human guesses — wrong prices produce pathological
granularity (everything one chunk, or byte soup). "No learned prices" keeps it honest but
also keeps it dumb: the system cannot discover that code wants different prices than
prose. Budget refusal under load looks like amnesia from the outside.

**Falsification criterion:** If Z3's total cost at equal recall accuracy is not ≥20%
below the best fixed-granularity arm, the economic machinery buys nothing — kill. If
halving B causes accuracy cliff-drops (>15% drop for 50% budget cut) rather than smooth
degradation, the pricing model is wrong — kill.

**Buildability:** Medium. Cost accounting is simple integer arithmetic in Zag; the
allocation rule is the research content. Danger: this smells like reward machinery —
the prereg must state explicitly why fixed prices + hard budget ≠ reward signal
(answer: no optimization pressure toward any behavior except cost accounting; the
allocation rule is deliberate, audited, and human-readable).

## Z4 — DIALECT CHUNKS (per-interlocutor lexicons; Phase 4 hook)

**Claim:** The same byte stream is cut differently for different minds: TNN should keep
one lexicon per interlocutor, because what counts as a unit depends on who you're
talking to.

**Mechanism (TNN-native):** Phase 4 (differentiation — TNN distinguishes who's talking to
it; experimental, unparked per 2026-09-20 law) provides a speaker tag on ingested input.
Chunk IDs are namespaced: `(speaker_tag, local_ID)`. The same raw bytes ingested from two
speakers may be cut differently with no conflict — lexicons are independent. Cross-speaker
recall requires an explicit, audited TRANSLATE op (chunk A's span re-cut under speaker B's
lexicon rules, logged as derivation, not identity). Shared/common-ground chunks live in a
preregistered `common` namespace both parties' organs may reference. No speaker tag, no
dialect (falls back to arm D semantics).

**Strengths (falsifiable):** Predicts that per-speaker vocabularies converge faster
(fewer cuts to stable reuse) than a single shared vocabulary when the two speakers use
systematically different phrasing (testable on parallel prose/code corpora with speaker
tags). Predicts TRANSLATE-op frequency measures genuine conceptual divergence between
speakers — a new observable.

**Weaknesses:** Namespace explosion (N speakers × M chunks); the `common` namespace
becomes a political object (who decides what's common ground?). Speaker tags depend on
Phase 4 working — if differentiation fails, Z4 has no foundation. Adversarial speaker
spoofing inherits the sensor-deceivable hole directly.

**Falsification criterion:** If per-speaker lexicons do not converge ≥30% faster than a
shared lexicon on the two-speaker curriculum, the namespacing buys nothing — kill. If
>40% of chunks end up duplicated across namespaces (no real divergence), it's overhead
without content — kill.

**Buildability:** Medium, conditional on Phase 4. Namespacing is a small ID-format change;
the TRANSLATE op and `common`-namespace governance are the new machinery. Byte-identical
replay needs speaker tags in the log (they're input metadata — fine).

## Z5 — RECIPE CHUNKS (identity = the cut-recipe, not the bytes)

**Claim:** Under revision, spans move and bytes change; what survives is the *rule that
found the span*. Identify the chunk by its recipe and re-derive the span on demand.

**Mechanism (TNN-native):** Chunk ID = `(recipe_hash, recipe_params)`. A recipe is a
deterministic, preregistered cut-program: e.g., `("brace_block", depth=2, nth=3)` or
`("paragraph", containing="keyword:K")`. Recall re-runs the recipe against the current
stream to recover the span — no stored span at all (contrast arm U recompute-on-demand,
which recomputes *segmentation*; Z5 stores the *identity* as a program and derives spans
per recall). If the recipe no longer matches (stream changed beyond recognition), recall
fails loudly with the recipe and last-known span logged — never silently. Recipes are
memory citizens: they can be pinned, killed, promoted.

**Strengths (falsifiable):** Predicts ID stability across revisions that destroy every
other arm's addressing: position (L) breaks on insert, content-hash (K) breaks on edit,
but `("function", name="main")` survives both. Predicts zero ID-reassignment churn on
the sqlite3.c edit curriculum.

**Weaknesses:** Recipe re-runs cost compute per recall (no cached span — or cache it and
reintroduce staleness). Recipes can become ambiguous (two functions named `main` after a
merge — which one? loud failure is honest but useless). The recipe language is designed,
not learned — expressiveness ceiling is human imagination (RISKS.md R2's shadow again).

**Falsification criterion:** If >15% of recalls on the edit curriculum hit recipe-ambiguity
or recipe-failure (loud failures still count — the claim is stability, not honesty), Z5
is dead. If recipe re-run cost exceeds 50× cached-span recall cost at 10× scale, it's
unaffordable online — survives only as an ID-stability layer over cached spans (which
concedes the mechanism).

**Buildability:** Medium-hard. Needs a small deterministic recipe interpreter in Zag
(fixed op set, no loops over unbounded input without fuel limits — preregister fuel).
Recipe set preregistered; extending it is a prereg amendment. Byte-identical replay is
natural (recipes are pure functions of the logged stream).

## Z6 — SCAR CHUNKS (boundaries form where revision happened)

**Claim:** Meaning lives where things changed. Chunk boundaries should form at revision
sites — kills, rollbacks, caught lies, re-cuts — the scar tissue of the system's history.

**Mechanism (TNN-native):** The audit ledger already records every revision event. Z6
reads the ledger as a segmentation signal: spans adjacent to high-revision-density regions
get boundaries; long-undisturbed spans stay whole. Concretely: a deterministic scar-density
function over ledger sequence ranges proposes boundaries; the consolidation organ ratifies
or rejects each (deliberate, logged). A chunk's ID binds its birth scar
`(ledger_seq_of_forming_revision, span)`. Scars are never edited (append-only ledger) —
so scar-bound IDs are revision-proof by construction. New revisions create new scars,
which may re-cut — the vocabulary breathes with the system's history.

**Strengths (falsifiable):** Predicts scar boundaries align with human-meaningful units
(functions edited as units, paragraphs revised as units) better than any content-blind
rule — testable by comparing against sqlite3.c's actual function boundaries and
Shakespeare's act/scene structure. Predicts "regretted cut" rate near zero for scars
(the boundary exists because something happened there).

**Weaknesses:** Cold start: a fresh stream has no scars — Z6 cannot cut anything until
revision happens (needs a bootstrap arm, e.g., D, for first contact). Scar density is a
statistic over history — it smells like accumulation, and strength-by-accumulation is
banned; the prereg must argue scars are *events*, not accumulation (each scar is a
deliberate op with an author). Quiet regions of the stream may contain the most important
stable knowledge and get the coarsest chunks (inverted importance).

**Falsification criterion:** If scar boundaries match ground-truth units (functions,
scenes) no better than random cuts at the same count (±10%), the "meaning lives where
things changed" claim is dead — kill. If the bootstrap arm's cuts are never displaced by
scars after 10,000 revisions (scars never take over), Z6 is decorative — kill.

**Buildability:** Medium. Scar-density is a ledger scan (integer arithmetic); ratification
plumbs into organ 3. The bootstrap dependency must be preregistered honestly (Z6 is not
standalone). Respects the 2^25 limit trivially (ledger scans chunk naturally).

## Z7 — PROVENANCE CHUNKS (cut at trust-tier boundaries)

**Claim:** The most load-bearing boundaries in a deceivable world are trust boundaries:
a chunk should be the maximal span sharing one provenance — one source, one trust tier.

**Mechanism (TNN-native):** Wave9 trust tiers (proven, corroborated, single-source,
untrusted) are already in the architecture. Z7 cuts wherever the trust tier changes:
a paragraph from a proven record and the next paragraph from an untrusted observation
are different chunks even if topically continuous. Chunk ID = `(tier, source_serial,
span)`. Tier *upgrades* (untrusted → corroborated via the corroborated-elimination
defense, 35/35) re-cut: the upgraded span becomes a new chunk with a `derived_from` link
to the old (audited, Y3-compatible lineage). Recall returns the tier with the bytes —
consumers never receive bytes without their trust label (this is the anti-spoofing
payoff: sustained observation spoofing corrupts only untrusted-tier chunks, which are
quarantined by construction).

**Strengths (falsifiable):** Predicts spoof-injection attacks are contained to
untrusted-tier chunks with zero cross-tier contamination on the spoof battery (directly
attacks the accepted "truthful but sensor-deceivable" hole). Predicts tier-labeled
recall reduces wrong-belief formation vs. tier-blind arms on mixed-provenance corpora.

**Weaknesses:** Trust tiers must be assigned at ingestion — who assigns, and by what
deterministic rule? (If a human assigns tiers, Z7 is taught-vocabulary O in disguise.)
Tier changes re-cut aggressively: a source whose tier oscillates fragments its chunks
(RISKS.md R3). Maximal-tier-spans may be enormous (an entire proven document = one chunk)
or tiny (alternating sources = byte soup).

**Falsification criterion:** If the spoof battery shows any cross-tier contamination
(spoofed bytes recalled with a proven-tier label), the containment claim is broken —
kill the claim, keep the labeling. If tier assignment cannot be made deterministic and
auditable without human judgment per chunk, Z7 collapses into arm O (taught) — merge or
kill.

**Buildability:** Hard. Depends on wave9 trust-tier machinery being deterministic and
complete; needs tier-change detection on the ingest path and re-cut logic. The
`derived_from` lineage needs Y3's versioning or a subset of it. Prototype on a
two-source corpus (one proven, one adversarial) before touching the big corpora.

## Z8 — FUZZY CHUNKS (boundaries carry explicit ±n byte uncertainty)

**Claim:** Every other arm pretends cuts are exact. They aren't — boundary placement is
uncertain, and honest systems should carry the uncertainty instead of hiding it.

**Mechanism (TNN-native):** A chunk = `(ID, span, fuzz_left, fuzz_right)` where fuzz
values are byte counts: the true boundary lies within `[start−fuzz_left, start+fuzz_left]`
(resp. end). Recall returns the span *plus* the fuzz intervals marked; consumers see which
bytes are boundary-certain and which are boundary-adjacent. Fuzz shrinks deliberately:
successful recalls of the chunk's interior (bytes far from the fuzz zone used without
correction) let the consolidation organ *tighten* the boundary via audited TIGHTEN ops;
contradictory evidence widens it via WIDEN. Fuzz is integers in the ledger — fully
auditable, byte-identical replay trivial.

**Strengths (falsifiable):** Predicts fuzzy chunks eliminate the silent-off-by-k-bytes
recall errors that exact-boundary arms suffer when their cut rule misfires — measurable
as boundary-error rate on a boundary-perturbation battery. Predicts TIGHTEN converges:
fuzz → small on stable content, stays wide on genuinely ambiguous content (honest
uncertainty, not false precision).

**Weaknesses:** Consumers must handle fuzz intervals — every downstream mechanism
(recall composition, Y5 links, contracts) gets more complex. Widen/tighten ops are
judgment calls by organ 3 — the determinism story needs the judgment logged as data
(it is: ops are ledger entries; fine). Risk of fuzz inflation: lazy organs widen instead
of thinking (cap total fuzz per chunk in the prereg).

**Falsification criterion:** If boundary-error rate is not ≥40% lower than arm D on the
perturbation battery, carrying fuzz buys nothing over exact cuts — kill. If mean fuzz
grows without bound on the revision curriculum (widen dominates tighten), the mechanism
diverges — kill or cap.

**Buildability:** Medium. Fuzz is two integers on the chunk record; TIGHTEN/WIDEN are new
ledger ops; recall formatting marks fuzz zones. The consumer-complexity cost is the real
price — prototype recall-only before wiring fuzz into composition and contracts.

---

## Arm index (this file)

| Arm | Name | One-line thesis |
|-----|------|-----------------|
| Y1 | Negotiated | Two organs, mutual veto, deadlock escalates to deliberate adjudication |
| Y2 | Adversarial | Red-team worst-case segmentations; robustness is the objective |
| Y3 | Temporal/versioned | Identity = serial + birth epoch + lineage; revisions version, never dangle |
| Y4 | Question-driven | Lazy: candidates at ingest, commitment at query time, question logged |
| Y5 | Cross-stream | One ID over a non-contiguous span set; kills cascade atomically |
| Y6 | Forgettable | Tombstone-native IDs, refcounted, checker-provable total deletion |
| Z1 | Witness-bound | A cut must survive eliminative challenge to become a chunk |
| Z2 | Contract | Chunk = audited obligation between organs; breaches refused loudly |
| Z3 | Budgeted | One scarce currency prices storage + access; granularity is economic |
| Z4 | Dialect | Per-interlocutor lexicons namespaced by speaker tag (Phase 4 hook) |
| Z5 | Recipe | Identity = deterministic cut-program; spans re-derived per recall |
| Z6 | Scar | Boundaries form at revision sites; the ledger's scar tissue segments |
| Z7 | Provenance | Cut at trust-tier boundaries; maximal single-provenance spans |
| Z8 | Fuzzy | Boundaries carry explicit ±n byte uncertainty; tighten/widen deliberately |

14 invention arms. None relabel A–X: the nearest neighbors are Y1↔H (H is unilateral
deliberation; Y1 is bilateral with veto), Y3↔T (T aligns to episodes; Y3 versions by
revision lineage), Y5↔J (J overlaps in bytes; Y5 links disjoint spans), Z5↔U (U recomputes
segmentation; Z5 stores identity-as-program), Z7↔O (O is taught content; Z7 is tier
machinery — collapses to O only if tier assignment needs humans, stated as falsifiable).

## Cross-crew combination notes (for the catalog/catalog-holder)

High-synergy pairs worth head-to-head or hybrid trials after single-arm verdicts:
- Y3 × Z1: versioned chunks whose births were witness-bound (lineage of justified cuts).
- Y6 × Y5: refcounted cross-stream units (kill cascades need Y6's provability).
- Z7 × Y4: lazy materialization within trust tiers (don't materialize untrusted spans
  until asked, and label them when you do).
- Z8 × D: fuzzy boundaries on self-cut spans (honest uncertainty about Micah's own
  hypothesis — the cheapest hedge in the program).
- Y2 as certification harness for ALL arms: the adversary grammar is arm-agnostic.
