# EXPLORATORY — NOT EVIDENCE

**WIDE EXPLORATION track — BEYOND THE ALPHABET**
Date: 2026-09-20/21. Worker: wide-exploration subagent.

This document is **exploratory and NON-BINDING**. It is not program evidence. It proposes
nothing into the frozen program. The prereg (`docs/lab/units/PREREG_FREEZE.md`, Micah-signed
2026-09-21) is FROZEN: no bar, metric, or kill criterion in it is changed, reinterpreted, or
softened anywhere below. **No design in this file may enter the program without a dated
amendment proposal signed by Micah** — stated per design below.

**Hard laws every sketch below obeys (inherited, not negotiable):** pure Zag; ZERO
randomness in any AI decision path; byte-identical reruns from (input + full logged state);
real mechanisms, no stubs as headline evidence; no binaries, no `.zagd`, no `.zag-cache`
in this work.

**Background assumptions of the 53-arm catalog this file deliberately breaks.** The whole
catalog (arms A–Z8) shares unspoken premises:
1. A unit is a **contiguous byte range** (a span). (Y5 loosens this to a span *set*; we go further.)
2. A unit is **something stored** — a noun memory points TO.
3. A unit is defined **positively** — by the content it contains.
4. **Chunking precedes retention** — you cut first, forget later.
5. Identity is **content-based or position-based** (same bytes → same ID, or ID = where).
6. **One mechanism owns segmentation** — every arm has a single cutter.
7. Teaching vocabulary requires a **message protocol** between teacher and learner (the TST tapes).
8. Every unit **corresponds to observed bytes** — nothing is coined for what was never seen.
9. A unit is a **property of the content alone**, not of who will recall it.

Each design below breaks exactly one of these, names it, and sketches the mechanism in
TNN-native terms (five organs: deliberate memory substrate, eliminative hypothesis logic,
deliberate consolidation/promotion, symbolic recall and trace composition, native structural
revision). Each carries a falsifiable prediction, a proposed kill criterion (binding if the
arm is ever admitted), and the amendment-path statement.

---

## W1 — Motif units (discontinuous template chunks)

**Assumption broken:** #1 — a unit is a contiguous byte range.

**Mechanism sketch.** A unit is a *template with slots*, e.g. `error <NNNN> at <LINE>` or the
C idiom `for (<i>=0;<i><N>;<i>++)`. The template (constant parts + slot descriptors) is the
unit; instances are never materialized as spans — only template ID + slot bindings are
stored. Candidate motifs are proposed by the deliberate memory substrate from repeated
co-occurrence structure; the eliminative hypothesis organ tries to falsify the template
(find instances the template claims to match that it shouldn't, or productive variants it
misses); deliberate consolidation/promotion promotes the motif to a unit only if it survives
challenge AND beats its byte-span competitors on reuse count. Symbolic recall binds slots
deterministically at query time; the native structural revision organ may deliberately
narrow or widen a template when eliminative probes find near-misses.

**Falsifiable prediction.** On the code corpus at 10x, W1 retains D-arm (self-cut span) mastery
within ±3% while storing ≥40% fewer unit IDs.

**Proposed kill criterion.** If mean per-query slot-bind cost exceeds 3× D-arm span recall
latency at 10x, the arm is killed (templates must earn their keep in retrieval, not just storage).

**Amendment path.** Admissible only via dated amendment proposal signed by Micah; needs a new
metric (bind-latency) ratified before build. Not evidence until then.

## W2 — Negative units (exclusion-defined chunks)

**Assumption broken:** #3 — a unit is defined positively, by what it contains.

**Mechanism sketch.** A unit is a *complement*: "everything in this region that is NOT one of
these known patterns." Used for noise, boilerplate, and stop-regions — the system deliberately
decides what it refuses to dignify with a unit. The eliminative hypothesis organ holds the
exclusion list and must certify each exclusion (the pattern is genuinely non-informative, not
merely unfamiliar); the deliberate memory substrate stores the unit as (region, exclusion
certificates); symbolic recall enumerates exclusions to reconstruct what the complement
covers. Revising an exclusion (admitting a previously-excluded pattern was informative after
all) is a deliberate act recorded in the ledger, priced like any revision.

**Falsifiable prediction.** On the prose corpus, W2 cuts stored IDs ≥2× vs D-arm with no
mastery loss (full scorecard, blowout rule unchanged).

**Proposed kill criterion.** If any mastery metric drops >5% vs D-arm at 1x, killed — exclusion
must never be a euphemism for ignorance.

**Amendment path.** Admissible only via dated amendment proposal signed by Micah. Not evidence until then.

## W3 — Stigmergic teacher (teacher as environment)

**Assumption broken:** #7 — teaching requires a message protocol between teacher and learner.

**Mechanism sketch.** No proposal protocol, no TST tapes, no cut-negotiation messages. The
teacher (human trainer or hand-wired white-box peer) shapes the *stream itself*: repetition,
ordering, pacing, and salience cues embedded as ordinary content (the way a parent repeats a
word in different sentences, never saying "this is a word"). The learner segments unassisted
using its own deliberate memory machinery; the eliminative hypothesis organ checks boundary
stability across reshaped exposures (a boundary that moves when the stream is re-paced was
never real). The only channel is the corpus. Teacher intent is readable only through its
effects on the stream — stigmergy, not messaging.

**Falsifiable prediction.** W3 reaches ≥90% of the hand-protocol taught arm (O) mastery at 1x
with zero protocol messages exchanged.

**Proposed kill criterion.** If W3 mastery <80% of O-arm mastery at 1x, killed — the protocol
is load-bearing, not overhead, and stigmergy is insufficient.

**Amendment path.** Admissible only via dated amendment proposal signed by Micah; note it
interacts with the sealed-flaw-manifest rules of Track B and needs a stream-shaping audit
rule added to the prereg. Not evidence until then.

## W4 — Units as recall procedures (verbs, not nouns)

**Assumption broken:** #2 — a unit is something stored; memory points TO it.

**Mechanism sketch.** A unit is a deterministic *re-derivation procedure*: e.g. "the span from
the third blank line after marker X to the next `}` at depth 0." Memory stores the procedure,
never the span. Symbolic recall and trace composition is the organ that owns these units —
recall IS execution. The eliminative hypothesis organ verifies each procedure by re-executing
it against the stream and checking the result against the ledger's recorded outcome; the
native structural revision organ may deliberately rewrite a procedure when the stream's
structure drifts (a revision, priced and audited like any memory revision). Nothing is cached:
every recall is a fresh, byte-identical derivation.

**Falsifiable prediction.** After a ledger-wipe leg (delete all stored spans; procedures and
the raw corpus survive), W4 recovers 100% of units while D-arm collapses to chance — because
W4 never stored what the wipe deleted.

**Proposed kill criterion.** If re-execution cost exceeds 10× cached recall latency at 10x,
killed — procedural purity must not price recall out of existence.

**Amendment path.** Admissible only via dated amendment proposal signed by Micah. Not evidence until then.

## W5 — Cross-modal identity (anti-content-addressing)

**Assumption broken:** #5 — identity is content-based or position-based.

**Mechanism sketch.** One unit ID covers a byte span AND its paraphrase — identity by
*meaning-equivalence judgment*, not bytes. The deliberate judgment machinery (the TNN
itself, in TNN-native terms the deliberative layer over the memory substrate) certifies
equivalence; the eliminative hypothesis organ then tries to falsify it (find a context where
the paraphrase diverges); the ID is issued by a monotonic counter and carries the
equivalence certificate in the ledger. A later falsification revokes the certificate —
publicly, in the ledger — and the arm's integrity accounting tracks revocation rate.

**Falsifiable prediction.** On paraphrase-query legs of the prose corpus, W5 mastery is ≥2×
the content-addressed K arm's.

**Proposed kill criterion.** If the certificate revocation rate exceeds 2% (the system's own
eliminative probes falsify its past equivalence judgments more than 2% of the time), the arm
is killed as integrity-unsafe — a unit that lies about sameness corrupts everything downstream.

**Amendment path.** Admissible only via dated amendment proposal signed by Micah; requires
the paraphrase-query leg to be added to the evaluation battery. Not evidence until then.

## W6 — Forgetting-first segmentation

**Assumption broken:** #4 — chunking precedes retention; you cut first, forget later.

**Mechanism sketch.** The learner first decides *evictions*, and the surviving islands become
chunks — boundaries are defined by what was deliberately forgotten. Under the memory-pressure
leg, the deliberate memory substrate runs audited forgetting passes (each eviction a deliberate,
logged act, priced per the strength-trial rulings); the consolidation/promotion organ then
promotes the surviving islands as units; eviction sites are recorded as scar tissue and become
the boundaries. Chunking is what retention leaves behind, not what precedes it.

**Falsifiable prediction.** Under the 10x memory-pressure leg, W6 retains ≥15% higher mastery
than D-arm — because its boundaries were chosen by the same pressure that now tests them.

**Proposed kill criterion.** If the arm fails the M8 determinism gate (eviction order is
state-path-dependent in a way that breaks byte-identical reruns from input + full logged
state), killed immediately — determinism is law, not a metric.

**Amendment path.** Admissible only via dated amendment proposal signed by Micah. Not evidence until then.

## W7 — Adversarial co-designed segmenter

**Assumption broken:** #6 — segmentation is cooperative within one mind; the spoiler (Y2) is
a post-hoc red team, never the training loop itself.

**Mechanism sketch.** Segmenter and spoiler co-evolve deterministically. The spoiler is not a
random mutator — it uses eliminative hypothesis logic to *construct* the falsifying case: the
corpus, trap span, or boundary violation most likely to break the current cut policy, built by
reasoning, not sampling. The segmenter then deliberately revises its cut policy via the native
structural revision organ; every round is ledger-recorded. Zero RNG anywhere: the spoiler's
"creativity" is eliminative construction from the segmenter's own logged weaknesses.

**Falsifiable prediction.** On the adversarial-corpus leg, W7 holds ≥95% of its clean-corpus
mastery while D-arm degrades >20%.

**Proposed kill criterion.** If the spoiler discovers a degenerate equilibrium (segmenter
collapses to X-degenerate — one unit or byte-level — and the spoiler can no longer construct
a falsifying case that isn't trivially absorbed), killed — co-evolution that converges on
degeneracy taught nothing.

**Amendment path.** Admissible only via dated amendment proposal signed by Micah; the spoiler's
construction rules need preregistering as carefully as any curriculum. Not evidence until then.

## W8 — Time-as-unit (duration chunking)

**Assumption broken:** the content side of #5 — units are content-based at all.

**Mechanism sketch.** Chunks are fixed-duration *processing windows*: identity = clock interval
(episode-clock windows, extending T-arm episode-alignment from "one chunk per episode" to
arbitrary fixed durations). Content is whatever fell inside the window. The deliberate memory
substrate assigns IDs to intervals; symbolic recall retrieves (interval, content-filter)
pairs. Boundaries never move when content shifts — only the clock cuts.

**Falsifiable prediction.** W8's segmentation compute cost is ≥3× lower than content-based
arms' at 10x, with mastery within 10% of D-arm on the code corpus.

**Proposed kill criterion.** If a content-shift-within-window leg (same windows, perturbed
content) drops W8 mastery >15% vs D-arm, killed — the clock is cutting where meaning isn't.

**Amendment path.** Admissible only via dated amendment proposal signed by Micah. Not evidence until then.

## W9 — Relation units (chunks that are edges, not nodes)

**Assumption broken:** #2's corollary — a unit is a piece of content. W9 makes units
second-order: the *relation between spans* gets the stable ID; spans are just endpoints.

**Mechanism sketch.** Units like DEFINES(X,Y), CONTRADICTS(X,Y), EXEMPLIFIES(X,Y) are
first-class citizens with stable IDs. The deliberate memory substrate stores edges with
endpoint pointers; the eliminative hypothesis organ verifies each relation claim against
world records (a CONTRADICTS claim must survive challenge — find the reading where both
hold, and the edge dies); promotion requires the relation to survive. Trace composition
walks edges; recall of "what contradicts X?" is a native operation, not a scan.

**Falsifiable prediction.** On contradiction/definition query legs at 10x, W9 answers ≥3× more
accurately than span-only D-arm.

**Proposed kill criterion.** If edge count explodes to >10× span count at 10x (combinatorial
bloat — relations about relations about relations), killed — the arm must price edge creation
or drown in it.

**Amendment path.** Admissible only via dated amendment proposal signed by Micah; needs an
edge-pricing rule in the prereg before build. Not evidence until then.

## W10 — Consensus-of-organs units (no single cutter)

**Assumption broken:** #6 — one mechanism owns segmentation.

**Mechanism sketch.** No organ cuts alone. Each of the five organs proposes boundaries from
its own view (substrate: pressure; eliminative: challenge-survival; consolidation: reuse;
recall: retrieval success; structural revision: revision sites). A unit exists only at the
deliberate consensus intersection — generalizing the Y1 negotiated protocol from two organs
to five, with mutual veto. Deadlock is not an error: it is recorded as a live open question
in the ledger and adjudicated by a deliberate decision, itself audited.

**Falsifiable prediction.** W10's false-boundary rate (boundaries later revised by the system's
own revision machinery) is ≥50% lower than D-arm's at 10x.

**Proposed kill criterion.** If the deadlock rate exceeds 10% of cut decisions (paralysis —
the organs veto more than they agree), killed.

**Amendment path.** Admissible only via dated amendment proposal signed by Micah. Not evidence until then.

## W11 — Dreamt units (consolidation-synthesized chunks)

**Assumption broken:** #8 — every unit corresponds to observed bytes.

**Mechanism sketch.** During deliberate consolidation, the system *synthesizes* abstractions
it never observed: a "for-loop idiom" unit distilled from 40 instances, a "boilerplate
header" unit, a "tragic-messenger speech" shape. The consolidation/promotion organ proposes
the abstraction; the eliminative hypothesis organ must try to falsify it against held-out
instances BEFORE promotion (find an instance the abstraction claims to cover that breaks
it); symbolic recall can retrieve the dreamt unit directly. Dreamt units are labeled as such
in the ledger — provenance is never laundered.

**Falsifiable prediction.** On the idiom-heavy code corpus at 10x, W11 uses ≥50% fewer IDs
than D-arm at equal mastery.

**Proposed kill criterion.** If >5% of promoted abstractions are falsified by held-out
instances (hallucination rate), killed — a dreaming arm that dreams wrong is a lying arm.

**Amendment path.** Admissible only via dated amendment proposal signed by Micah; requires
the held-out falsification protocol preregistered. Not evidence until then.

## W12 — Audience-relative units (chunking for the recipient)

**Assumption broken:** #9 — a unit is a property of the content alone.

**Mechanism sketch.** The same stream is cut differently depending on *who will recall it*:
a chunk is a (content, audience) pair, extending Z4-dialect namespacing from vocabulary to
segmentation itself. The deliberate memory substrate maintains audience-indexed cuts; the
audience tag is part of the logged state, so byte-identical reruns hold per audience.
Cross-audience shared ground is maintained deliberately — the system tracks which units are
audience-private vs shared, and shared-ground drift is itself a measured quantity.

**Falsifiable prediction.** On the Phase-4 per-person recall leg, W12 beats single-vocabulary
D-arm mastery by ≥20%.

**Proposed kill criterion.** If audience-indexed stores diverge so far that shared-ground
mastery drops >10% vs D-arm, killed — private lexicons must not dissolve common ground.

**Amendment path.** Admissible only via dated amendment proposal signed by Micah. Not evidence until then.

---

## Ranking: the 3 that deserve amendment proposals first

**1. W1 — Motif units.** Closest to Micah's thesis (chunking as a cognitive act the system
performs, not a tokenizer applied to it) while breaking the catalog's deepest unspoken
premise — contiguity. The code corpus is motif-rich, so the falsifiable prediction is cheap
to test; compression and reuse are already program metrics, so the arm needs only one new
metric (bind-latency). Highest information value per build cost.

**2. W6 — Forgetting-first.** The program has a live wound here: the felt-intensity trial
failed at retention (25% of valuable memories vs the 90% bar), and the strength trial is
still settling freeze-vs-retention. W6 attacks the exact inversion the program needs tested —
whether retention should *define* segmentation rather than follow it — and its kill criterion
(the M8 determinism gate) is already a frozen bar, so the arm is cheap to adjudicate.

**3. W5 — Cross-modal identity.** This is the philosophical core of the program question
("what is a unit of knowledge, if not an LLM token?") made experimental: it tests whether
identity can be meaning-based rather than byte-based, which is the anti-tokenizer stance in
its purest form. The revocation-rate kill criterion doubles as an integrity instrument, which
serves the program's integrity line beyond this one arm.

**Why not the others first:** W4 (procedures) is the boldest break but its 10× latency
ceiling makes it a likely early kill — better as a second-wave probe after W1 establishes
whether non-span units work at all. W3 (stigmergy) interacts with Track B's sealed manifests
and would complicate the teacher line mid-flight. W7/W9/W10/W11/W12 are all strong but each
needs new prereg machinery (spoiler construction rules, edge pricing, five-organ protocol,
held-out falsification, audience indexing) — propose after the first three prove the
beyond-span territory is fertile.

---

*End of exploratory document. Nothing above is evidence. Nothing above enters the program
without a Micah-signed dated amendment.*
