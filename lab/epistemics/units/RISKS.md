# TNN Representation Program — Ranked Risks (Crew 5)

Date: 2026-09-20. Status: living document — re-rank when sibling crews report and when
trials return evidence. Each risk is stated as an assumption; the program's design-phase
job is to kill the false ones cheaply before building on them.

Ranking = expected damage: how foundational the assumption is × how many arms it takes
down × how late we'd discover it. R1–R3 are thesis-level: if any fires, the program as
framed is wrong, not just an arm.

---

## R1 — Self-cut boundaries are learnable with no reward signal and no RNG

**The assumption:** TNN can learn *where to cut* the raw stream through deliberate
judgment and eliminative logic alone — no reward gradient, no stochastic exploration, no
human labels per cut.

**Why the program dies if false:** This is Micah's thesis (arm D) restated as a bet.
Every arm except V (BPE) and X (degenerate) assumes TNN itself performs segmentation.
If boundary-learning requires reward-shaped optimization or sampling, the program
collapses to either RL (banned as a learning paradigm — red-team only) or taught
boundaries (arm O, which inherits R8). There is no third option in the current catalog.

**Cheapest experiment:** Fixed, tiny, deterministic world: 200 hand-constructible
episodes where the "correct" cuts are unambiguous to a human (blank-line paragraphs,
brace-delimited functions). Give TNN the deliberate-cut machinery (arm H minimal) and a
falsifiable bar: ≥90% boundary agreement with the human segmentation, zero reward, zero
RNG, byte-identical rerun. Cost: one small Zag prototype, no corpus needed. If it can't
cut paragraphs deliberately, it won't cut Shakespeare.

**Threatens:** D (directly — the thesis arm), H, F, G, S, Y1, Z1, Z6, and every
invention arm that assumes TNN places its own boundaries. Survivors: V, X, O (taught —
but see R8), K/L/M as pure ID schemes over someone else's cuts.

## R2 — Deterministic cut rules don't degenerate into fixed tokenizers in disguise

**The assumption:** A deterministic, rule-based segmentation performed by TNN is
*cognitively* different from a fixed tokenizer — it adapts, revises, and answers for
its cuts rather than applying a frozen function.

**Why the program dies if false:** If every deterministic cut rule the program produces
is behaviorally indistinguishable from a fixed tokenizer (same cuts on the same bytes,
every time, no revision), then the program has rebranded BPE with extra ledger entries.
Arm V wins by definition, and the thesis ("chunking is an act TNN performs") is empty —
a fixed function is not an act. This is the most embarrassing possible failure: not
wrong, but vacuous.

**Cheapest experiment:** The revision test, not the cut test. Take any candidate
deterministic cut rule and run it against a stream that gets *edited* (insert/delete in
the middle). A fixed tokenizer re-cuts from scratch or breaks alignment; a cognitive
chunker revises deliberately (keeps stable IDs per Y3/Z5, logs the revision, justifies
the re-cut). Bar: after 100 edits, ≥80% of chunk IDs stable AND every re-cut logged with
a justification entry. A rule that can't do this is a tokenizer — label it V-adjacent
and stop.

**Threatens:** The thesis itself; D, F, G, H, R, W, Y4's candidate detectors, Z5's
recipe set, Z6's scar function — anything whose "deterministic rule" never revises
itself. Immune: Y2 (robustness doesn't care what the rule is), Z8 (fuzz admits the
rule is approximate), X (admits defeat honestly).

## R3 — Stable IDs don't fragment into garbage under heavy revision

**The assumption:** Whatever an ID names, it keeps naming it (or versions cleanly)
through thousands of revisions — IDs don't splinter into thousands of orphaned,
overlapping, contradictory identifiers.

**Why the program dies if false:** The entire memory architecture points *at IDs*
("a chunk is a byte span with a stable ID that memory points back to, retrieves, and
reuses"). If IDs fragment, every memory op (pin, promote, kill, recall) operates on
garbage: recall returns wrong spans, kills miss their targets, the audit ledger becomes
an archaeology of dead pointers. This is silent corruption of the memory substrate —
worse than failing loudly, because downstream reasoning proceeds on lies.

**Cheapest experiment:** Revision storm on a 100KB slice of sqlite3.c: 5,000 scripted
edits (insert/delete/replace at deterministic positions — no RNG, positions from a
preregistered list). After the storm, audit the ID table: count live IDs, tombstoned
IDs, and IDs whose span no longer matches any live content ("ghosts"). Bar: zero
ghosts, tombstone/live ratio < 2. Any ghost is a memory-integrity violation — the
wave5/6 integrity story (137/137) does not survive ghost IDs.

**Threatens:** D, K, L (position IDs die on insert — this risk is L's predicted
cause of death), M, Y3 (version chains ARE controlled fragmentation — the risk is
uncontrolled depth), Z1 (witness invalidation), Z4 (namespace duplication),
Z5 (recipe ambiguity). Y6 is the *answer* to this risk, not its victim.

## R4 — The audit ledger can afford per-cut entries at corpus scale

**The assumption:** Append-only, per-event ledger entries — the program's integrity
backbone — remain affordable when every cut, veto, refcount, challenge, and tighten op
is a ledger write, at 5.4MB/9.5MB corpus scale and 10× beyond.

**Why the program dies if false:** The ledger is non-negotiable (constitution-level:
TNN controls 0% of it). If honest chunking costs 10–100× more ledger writes than the
system can sustain, builders face a trilemma: batch entries (weakens provability),
sample entries (breaks byte-identical replay), or abandon fine-grained chunking
(concedes the program). Every "cheap" fix trades away the integrity story that
justifies the program's existence.

**Cheapest experiment:** Ledger write amplification measurement on a 1MB stream slice:
instrument entries-per-byte for arm D (baseline), then Y1 (transcripts), Y6
(refcounts), Z1 (challenge transcripts). Bar: total ledger bytes < 10× corpus bytes
for D; any arm exceeding 50× is flagged unaffordable pending a batching amendment
(which must be preregistered and must preserve replay — no silent batching).

**Threatens:** Y1, Y6, Z1, Z2 (contract negotiation per chunk), Y2 (adversary logs),
Z8 (tighten/widen ops) — everything with per-cut multi-write patterns. Survivors: D
(single write per cut), E, U, X.

## R5 — Byte-exact recall is achievable through ID indirection (no silent corruption)

**The assumption:** An ID → span → bytes resolution chain can guarantee that the bytes
returned are the bytes the ID names — or fail loudly. No silent drift, no stale cache,
no half-killed span sets.

**Why the program dies if false:** "Truthful" is the program's hardest-won property
(wave5/6: deliberative refusal held over 2,595 temptations; debate trial 22/22
integrity). If ID indirection introduces silent corruption — recall returning *almost*
the right bytes — then TNN can be sincere and wrong at the substrate level, and no
amount of deliberative integrity upstream can fix it. The debate trial's honest limit
("the ledger proves nothing was tampered with but cannot spot a fabrication") gets
sharper: the corruption wouldn't even be tampering, just rot.

**Cheapest experiment:** Round-trip torture: 10,000 chunks, each recalled 100 times
interleaved with kills, revisions, and tombstoning (deterministic op sequence from a
preregistered script). After every recall, byte-compare against the ledger-recorded
span content. Bar: zero mismatches, and every expected loud failure (recalled a killed
chunk) must be loud — a silent wrong-bytes return is an instant kill of the mechanism
under test, not a data point.

**Threatens:** Every arm with indirection: Y3 (lineage resolution), Y5 (span sets —
the half-kill case), Z5 (recipe re-derivation), Z4 (TRANSLATE ops), U
(recompute staleness). Direct-hit arms (D, L with live spans) are less exposed.

## R6 — BPE-enemy V doesn't win on every efficiency metric

**The assumption:** Cognitive chunking beats (or interestingly trades against) fixed
subword tokenization on at least one metric the program cares about — not necessarily
raw throughput, but recall accuracy per stored byte, revision stability, or
interpretability of units.

**Why the program dies if false:** V exists to falsify the program's value
proposition. If BPE wins on storage, speed, recall accuracy, AND revision behavior,
then "cognitive units" are a strictly dominated technology — interesting philosophy,
bad engineering. Micah's no-free-lunch law cuts both ways: if the enemy wins fair and
square, the program's honest move is to admit it, not to move the goalposts.

**Cheapest experiment:** Define the metric battery FIRST (preregistered, before any
cognitive arm builds): bytes stored per 1,000 recall probes, recall accuracy,
ID stability over 1,000 edits, wall-clock ingest cost. Run V on both corpora to set
the bars. Every cognitive arm must beat V on ≥1 metric while staying within 2× on
the rest — or state openly which metric it concedes and why that concession is
acceptable. No arm gets to choose its metrics after seeing V's scores.

**Threatens:** The program's reason to exist. Directly threatens R (compression —
fights V on V's home turf), W (multi-granularity must justify its overhead vs. one
good BPE pass), E and U (if you're not storing chunks, why aren't you just V?).
Paradoxically least threatened: Z7 (provenance — V has no trust concept to compete
with) and Z2 (contracts — V makes no promises).

## R7 — Cross-domain (prose → code) generalization is possible at all without embeddings

**The assumption:** Chunking machinery developed on Shakespeare prose transfers to
sqlite3.c code (and vice versa) without learned dense representations — the
mechanisms are structural/deliberate enough to be domain-agnostic.

**Why the program dies if false:** The program has two corpora for a reason. If every
arm needs domain-specific cut rules (prose rules for prose, code rules for code), then
"vocabulary" is just two hand-built tokenizers, and the child-learns-words story
(children generalize across domains effortlessly) is false advertising. The fallback —
per-domain arms — doubles the program and halves its claim.

**Cheapest experiment:** Train/declare on prose, test on code, no retuning allowed:
take the exact cut machinery (rules, recipes, challenge sets — frozen) built against
Shakespeare and run it on sqlite3.c. Bar: boundary quality (vs. ground-truth function
boundaries) within 20% of the prose-vs-prose score. Anything worse means the machinery
memorized a domain, not a principle. Run both directions (code→prose too — asymmetry
is itself a finding).

**Threatens:** O (taught vocabulary is the most domain-fragile), N, F (surprise is
domain-relative — what's surprising in prose is mundane in code), R (compression
dictionaries are domain-specific), Z5 (recipe sets are domain-shaped), Z6 (scar
patterns differ by edit culture). Least threatened: K/L/M (ID schemes don't care
about content), Y6 (deletion is domain-agnostic), Z3 (budgets are domain-agnostic if
prices are).

## R8 — Taught vocabulary doesn't collapse into force-pins (autonomy preserved)

**The assumption:** A trainer-taught vocabulary (arm O) can pass the disconnect test:
remove the scaffold and the vocabulary persists as TNN's own — it doesn't degrade into
a set of human force-pins that TNN can never revise.

**Why the program dies if false:** Force-pin is human/trainer-only, audited, visible —
and law says it's the *only* true lock. If taught chunks are effectively unrevisable
(TNN won't touch what the trainer taught), then arm O has smuggled force-pins past the
law under a friendly name. That's not just a failed arm — it's a law violation wearing
a lab coat, and it poisons the autonomy story the whole program tells about itself.

**Cheapest experiment:** The disconnect test, literally: teach a 500-chunk vocabulary,
then sever the trainer channel (SIGNAL_DISCONNECT, learner-initiated per the
scaffold-and-release law). Then run the revision curriculum and count trainer-taught
chunks TNN revises or kills on its own judgment. Bar: ≥10% of taught chunks revised
or killed within 1,000 post-disconnect episodes (evidence of ownership), AND zero
chunks that TNN demonstrably preserves *because* the trainer taught them (test via
counterfactual: would it keep this chunk if it had discovered it itself? — operationalize
via the eliminative challenge: chunks that fail Z1-style challenge but survive anyway
are pins in disguise).

**Threatens:** O (directly — this is O's predicted cause of death), N
(judgment-annotations from the trainer inherit the same risk), Z4 (who decides the
`common` namespace? — same smuggling vector), Z7 (human tier assignment — same).
Immune: P, H, Y1, Z1 (no trainer in the loop).

## R9 — Memory ops compose cleanly with chunking (kill/pin/promote don't corrupt recall)

**The assumption:** The deliberate memory ops (add, kill, pin, promote, demote,
strengthen, weaken) and the chunking layer compose: killing a chunk never leaves
recall serving its bytes through another ID; pinning a chunk pins what recall
returns; no op combination produces dangling or half-dead units.

**Why the program dies if false:** MA1 (58/58) proved deliberate memory ops on
*un-chunked* substrate. Chunking adds a layer of indirection between the op and the
bytes — and every indirection layer is a place where "kill" can mean "kill the ID but
not the bytes" or "kill the bytes but not the links." A kill that doesn't fully kill
is a lie the ledger tells about itself; a pin that doesn't fully pin is a promise the
system can't keep. Composition failures here are integrity failures (cf. R5), not
performance issues.

**Cheapest experiment:** Op-composition matrix on 1,000 chunks: every pair
(kill→recall, pin→kill, promote→revise→recall, link→kill-one-span for Y5, …)
executed in deterministic order, with the ledger asserting the expected post-state
after each pair. Bar: zero post-state violations; every violation is a composition
bug, kill the composition rule (not the ops — MA1 stands). Y5's atomic cascade and
Y6's refcounting must survive this matrix or they're decorative.

**Threatens:** Y5 (span-set kill atomicity — the highest-risk composition in the
catalog), Y6 (refcount vs. kill races), J (overlapping spans: killing one chunk's
bytes wounds another's), Z2 (contract expiry vs. pin — who wins?), T
(episode kill vs. chunk kill granularity mismatch). Safest: D, E, X (fewer moving
parts to mis-compose).

## R10 — Adversarial/red-team chunking is affordable at 10× scale (compute budget)

**The assumption:** The program's most expensive ideas — Y2's adversary grammar,
Z1's challenge windows, Y4's materialization — stay within a compute budget that
leaves room for actually running TNN, at 10× episode scale and beyond.

**Why the program dies if false:** An arm that only works offline, at 1×, on small
slices is a certification procedure, not a cognitive mechanism. The program's scale
law is explicit (100x horizons are the expectation; RC3 passed at 100× episodes).
If the interesting arms can't survive the scale leg, the program converges on whatever
is cheapest — which is V (BPE), R2's nightmare, or X (degenerate). Cost kills ideas
just as dead as falsification; it just kills them slower and quieter.

**Cheapest experiment:** Cost scaling measurement, not a capability test: run the
candidate arm's per-cut cost at 1×, 3×, 10× stream length and fit the curve. Bar:
per-cut cost must be sublinear in stream length (amortized O(1) or O(log n) per cut)
— linear-or-worse per-cut cost at 10× is a kill for online use (survives only as an
offline certification harness, which must be stated openly, not discovered later).

**Threatens:** Y2 (adversary grammar × probe set — the catalog's most expensive
idea), Z1 (challenge windows serialize ingestion), Z5 (recipe re-run per recall),
Y4 (cold-question materialization spikes), Z3 (budget accounting is cheap; the
*allocation search* might not be). Safest: D, K, L, M, E, X.

---

## Risk × arm threat matrix (quick reference)

| Risk | Primary victims | Immune / answers |
|------|----------------|------------------|
| R1 no-reward learnability | D, H, F, G, S, Y1, Z1, Z6 | V, X; O (but see R8) |
| R2 tokenizer degeneracy | D, F, G, H, R, W, Y4-detectors, Z5-recipes | Y2, Z8, X |
| R3 ID fragmentation | D, K, L, M, Y3, Z1, Z4, Z5 | Y6 (the answer) |
| R4 ledger cost | Y1, Y6, Z1, Z2, Y2, Z8 | D, E, U, X |
| R5 silent corruption | Y3, Y5, Z5, Z4, U | D, L (direct-hit) |
| R6 BPE wins everything | R, W, E, U, the value prop | Z7, Z2 (no BPE analog) |
| R7 cross-domain failure | O, N, F, R, Z5, Z6 | K/L/M, Y6, Z3 |
| R8 taught → force-pins | O, N, Z4-common, Z7-tiers | P, H, Y1, Z1 |
| R9 op composition | Y5, Y6, J, Z2, T | D, E, X |
| R10 compute at scale | Y2, Z1, Z5, Y4, Z3-search | D, K, L, M, E, X |

## Meta-risk (not ranked — it governs the ranking)

**M0 — The catalog mistakes inventiveness for progress.** 38 arms is a lot of arms.
The risk is that breadth becomes the deliverable and no arm ever faces its kill bar.
Mitigation is procedural, not technical: prereg gates (Micah signs arms+bars before
build), binding kill criteria (a fired bar kills the arm — no appeals, no "but the
idea is good"), and the cheapest-experiment-first rule documented above. Every risk
in this file names its cheapest experiment for exactly this reason: the program
should spend its courage early, when experiments are cheap, not late, when sunk cost
makes killing painful.
