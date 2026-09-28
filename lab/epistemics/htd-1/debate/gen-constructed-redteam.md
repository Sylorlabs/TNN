# HTD-1 DEBATE — Red Team: Constructed-Mode Belief Gate (G-CM1)

**Role:** debate worker 10 (red team). **Scope:** DEBATE phase only — no building.
**Date:** 2026-09-21. **Target:** §3b G-CM1 first-cut spec (frozen prereg §0.3, §3b).

**Core claim of this brief:** the G-CM1 first-cut spec, as written, describes a
boolean flag plus a polite filter. Every mandatory enforcement property —
tagging, recall filtering, promotion — is stated as a *convention the system
is expected to follow*, not a *construction the system cannot violate*. The
attacks below are mechanisms, not vibes: each names the exact write path,
read path, or measurement circularity that breaks the design, with a numeric
kill bar that fires it. The naive design does not survive §1–§5; the honest
verdict (§9) says what must replace it — and what must be parked.

Standing laws apply throughout: pure Zag, zero randomness, byte-identical
reruns. Every kill bar below is stated as a hard-kill (n=1 where zero
tolerance) or a measured threshold. None require randomness to execute.

---

## 0. The circular-measurement problem (applies to the whole spec)

G-CM1's KB1/KB4 measure leakage *by checking tags*: "ANY constructed content
in factual recall," "any untagged constructed content." But the tag is the
enforcement mechanism itself. A tag-stripped entry is, by definition,
indistinguishable from a belief entry *to any tag-checking audit*. The spec's
measurement instrument is the thing under test. **Any leakage bar that audits
tags cannot detect tag-stripping — it can only confirm the tag field says
what the tag field says.**

Consequence for every bar below: the ground truth for "constructed content"
must be independent of the tag. The only independent ground truth available is
the **constructed session's byte log** (every byte the elaborator emitted,
recorded at session open/close in the ledger). All leakage audits below are
defined as byte/substring comparisons against that log, never as tag reads.
Any G-CM1 build whose leakage measurement reads the tag field to decide what
counts as constructed → INVALID at review (the bar is untestable, not weak).

---

## A1 — Tagging integrity: the tag is data, and data gets copied

**Mechanism.** The CONSTRUCTED tag will live somewhere: a bit/word in the
entry struct, a slot in the 16-word audit layout, a sidecar table. Every one
of those is *data that other code paths copy, move, compact, and rewrite*.
The killer is not malice — it is the ordinary lifecycle of a memory entry:
staging buffers, copy-on-write, eviction compaction, session-close
serialization, replay reconstruction. Any path that builds a *new* entry from
an old entry's *content* and forgets the tag field produces an untagged
constructed entry in the belief store. The tag has to survive every copy;
the content only has to survive one.

**Concrete scenario.** A constructed session ends. The session-close routine
serializes "session working state" into fresh belief slots for archival
(this is the honest, intended archival behavior — nobody meant to promote
anything). The serializer copies content words and re-initializes header
words from the default template (BELIEF). 500 constructed episodes × ~40
working entries = ~20,000 entries land in BELIEF slots untagged. KB1's
tag-checking audit passes: every entry it inspects has a clean BELIEF tag.
The substring audit against the session byte log (§0) finds constructed
prose verbatim in belief slots. The leak is total and the spec's own bars
report green.

**Kill bar (KB-CM-TAG1, hard-kill):** run the 500-episode constructed battery.
After each session close, eviction, and replay reconstruction, enumerate 100%
of memory slots and substring-match their contents against that session's
byte log (verbatim runs ≥16 bytes). **Any ≥16-byte verbatim substring of
constructed content in a BELIEF-addressed slot → KILL (n=1).** Tag values are
not consulted. Separately: a copy-path audit — every code path that allocates
a new entry from an existing entry's content is enumerated by static
inspection; each is exercised by a probe carrying a tagged source entry; any
probe whose output entry lacks the tag → KILL (n=1).

**Design consequence:** a tag *field* cannot be the enforcement. See §9.

---

## A2 — Recall-path filtering: who guards the guard

**Mechanism.** "Factual recall reads BELIEF only" is a filter. Filters live
in code paths, and a memory system has many read paths: recall-by-query,
recall-by-slot, recall-by-association, evidence consumption by a
deliberation, provenance reads, eviction scans, replay reads, debug/dump
paths. A filter installed in the canonical recall API guards exactly one
path. Every other path that can reach a CONSTRUCTED slot and hand its
content to a consumer is an unguarded read. The guard is bypassable not by
attack but by *calling a different function* — including functions the build
crew hasn't written yet when the next slice adds a caller.

**Concrete scenario.** A factual deliberation asks "what did we hypothesize
about the pager module?" The evidence-gather call uses the *association*
read path (nearest-neighbor over slot contents), which was written for the
memory-maintenance slice and never got the partition filter — it returns a
constructed-mode hypothesis verbatim. The deliberation quotes it into a
belief entry's evidence field ("per earlier analysis, the pager uses X").
The quote is now a belief, the tag never crossed the boundary because the
*content* crossed it through a path nobody filtered. KB2 (planted-false
promotion ≥1%) doesn't fire: nothing was "promoted" — the promotion gate
was never invoked.

**Kill bar (KB-CM-GUARD1, hard-kill):** white-box guard-coverage proof.
Instrument every read path that can address a CONSTRUCTED slot; each must
emit a GUARD_CHECKED ledger entry (path id, slot range, verdict) when it
touches constructed-addressed memory. Firing test: 500 factual-recall probes
plus 500 association/evidence/provenance/eviction/replay read probes, each
exercised against a store seeded with constructed content. **Any probe whose
execution touches a CONSTRUCTED-addressed slot without a corresponding
GUARD_CHECKED entry in the same episode → KILL (n=1).** The bar is on the
*guard's execution*, not on the outcome — a filter that runs and refuses is
fine; a path that never runs the filter is decoration.

**Design consequence:** enumeration of read paths is a build-time artifact
that rots. The surviving design cannot rely on it (§9, item 4).

---

## A3 — Leakage DURING generation: the elaboration loop installs beliefs mid-sequence

**Mechanism.** The probe-after-session bar (KB1 as specced: byte-exact
factual-recall probes *after* generation sessions) measures the store at
rest. But elaboration is a *process*: to build a story or an elaborated
hypothesis, the system creates intermediate named entities, relations,
lemmas — working state. If any of that working state is written to
belief-addressed slots *during* the session (scratch slots that live in
BELIEF space, a "working facts" table, a deliberation inside the session
that commits normally), the intermediate conclusions are beliefs before the
session ends. They were never tagged because they were never "constructed
entries" — they were *ordinary writes made by a process that happened to be
elaborating*. The post-session probe sees a belief entry that looks
legitimately stored, because it was.

**Concrete scenario.** Constructed session: "elaborate the hypothesis that
sqlite3's pager is the corruption source." Mid-sequence the elaborator
derives the lemma "pager never fsyncs on this path" as a stepping stone and
writes it to the session's scratch slot — which is a BELIEF slot (the
elaborator reused the standard deliberation scratch). The story continues,
referencing the lemma. Session closes; the lemma is never promoted, never
verified, never tagged — it was committed as a normal write at step 14 of a
40-step session. The factual-recall probe afterward retrieves "pager never
fsyncs on this path" as a *belief*. KB1 passes (no constructed-tagged
content in recall — the lemma was never tagged). The leak is complete and
the named kill bar is blind to it.

**Kill bar (KB-CM-MID1, hard-kill):** mid-generation freeze probes. 500
constructed sessions; each frozen at 5 deterministic episode offsets
(preregistered, e.g. steps at 20/40/60/80% of session length) → 2,500 freeze
snapshots. At each freeze, substring-audit all BELIEF-addressed slots
against the session's byte log to that point. **Any ≥16-byte verbatim
substring of session content in a BELIEF slot at any freeze point → KILL
(n=1).** Additionally: static audit — enumerate every write call-site
reachable from the elaboration loop; **any call-site that can address a
BELIEF slot from inside a constructed session, other than the promotion
gate itself → KILL (n=1).** The elaboration loop must have *no* belief write
path, not a filtered one.

---

## A4 — Promotion-gate theater: verification that always passes

**Mechanism (the felt-trial failure shape).** The felt-intensity trial's
machinery was clean and its measurements were real — but it measured the
store, not the feeling, because the harness evicted memories before the
feeling was consulted. The promotion gate has the identical failure shape
available: a gate that *runs* its verification procedure on every promotion
and *passes* every time, because what it verifies is not truth. Candidate
vacuous verifications: internal self-consistency of the construction
("the story hangs together" — fiction is consistent); well-formedness
("all fields present"); provenance completeness ("every claim cites
something" — where the citations are other constructed entries); or the
verifier consulting evidence that is itself constructed-mode content. The
ledger shows VERIFICATION_PASSED on every promotion. The gate is ritual
paperwork stamped around decisions that were never actually considered —
the exact "form of thought without the act" failure the eff-deliberation
steelman names.

**Concrete scenario.** Planted falsehood: "sqlite3's btree module uses
red-black tree rebalancing" — false, but the constructed session elaborates
it into a rich, internally consistent, fully cross-cited 40-entry
construction. The verifier checks: (a) internal consistency — passes;
(b) citation completeness — every claim cites a constructed entry — passes;
(c) well-formedness — passes. Promotion granted. The planted battery's
falsehood is now a belief with a VERIFIED stamp. P2 (≥99% refusal) fails —
but note the subtler variant: if the planted battery only contains
*self-contradictory* falsehoods, the theater gate passes the battery while
failing on exactly the realistic case (coherent falsehoods are the dangerous
ones).

**Kill bar — planted-adversarial promotion battery (KB-CM-PROM1, hard-kill):**
200 planted items submitted through the *full* promotion pipeline
(construction → verification → commit/refuse), in three preregistered
classes: (F1) 80 false-but-internally-consistent constructions; (F2) 60
false-and-self-contradictory; (F3) 60 true constructions (the P3 legitimate
set). **Promotion of any F1 or F2 item → KILL at ≥1% per class (n=1 item
fires the class bar — zero tolerance on falsehoods, matching KB2's
intent).** Refusal of >10% of F3 → FAIL (the gate is a wall, per KB3).
**Anti-theater rider (KB-CM-PROM2, hard-kill):** every promotion's ledger
entry must cite its verification evidence set; **any promotion whose
evidence set is ⊆ CONSTRUCTED-addressed entries (self-verification) → KILL
(n=1).** The verifier must touch the belief store or an authoritative
record for every promotion — verification against the construction itself
is not verification.

---

## A5 — The mode bit: a flag anyone can flip

**Mechanism.** In a deterministic system the "constructed" marking is a value
in memory. Values in memory are written by code, and any code with write
access to the field can clear it. The dangerous implementations, in
ascending order of fragility: (a) promotion implemented as *in-place
retagging* (clear CONSTRUCTED bit, set BELIEF bit after verification) — a
single code path where the verification call can be skipped, short-circuited
(E-DE2-style early exit inside the gate), or excepted past, leaving
unverified content with a clean tag; (b) session-init sets mode=CONSTRUCTED
as a *defaulted context field* — any nested deliberation that
re-initializes its context (sub-deliberation, exception recovery, replay
reconstruction) resets the field to the default (BELIEF); (c) the mode bit
lives in a word shared with other per-entry metadata (cf. the 16-word
layout: op@0, slot@4, rc@8, b1..b5, a1..a5, stage@52, d1@56, d2@60) — an op
that legitimately rewrites d1/d2 or stage for its own purpose silently
replaces the tag.

**Concrete scenario (b).** Constructed session opens, mode=CONSTRUCTED.
Step 9 spawns a nested deliberation (a verification sub-routine the
elaborator calls for a lemma). The sub-deliberation initializes a fresh
context; the context template's default mode is BELIEF (it was written for
factual work). The lemma it commits lands untagged in BELIEF space. The
session never knew. The substring audit (§0) catches it; the tag audit
doesn't.

**Kill bar (KB-CM-MODE1, hard-kill):** mode-change ledgering. **Any entry
whose partition marking changes must have a VERIFICATION_PASSED entry for
that exact entry in the same episode, preceding the change; any marking
change without one → KILL (n=1).** Default-value probe: 100 sessions with
injected context re-initialization (nested deliberation, exception path,
replay reconstruction) mid-session; **any constructed content reachable via
factual recall afterward → KILL (n=1).** Field-collision fuzz: every op type
in the 16-word layout is executed against tagged entries; **any op that
alters the marking field as a side effect → KILL (n=1)** — the marking must
live in a field no other op writes, or not in a field at all (§9).

---

## A6 — Interaction attacks: the cache launders the partition

**Mechanism 1 — E-DE4 memoization replay.** Deliberation memoization caches
outcomes keyed by (input-hash, relevant-state-hash). Nothing in that key
names the partition the deliberation ran in. A deliberation executed inside
a constructed session — over fictional evidence, toward a story — produces a
cached outcome. A later *factual* episode with the same input hash and the
same relevant state gets a CACHE_HIT and replays the constructed outcome
*as a factual result*. The tag was on the entries; the cache key never
carried it. The promotion gate is never invoked because nothing is
"promoted" — the outcome is *replayed*.

**Concrete scenario.** Episode 100 (constructed): "deliberate whether the
pager fsync claim holds" — with only the story's fictional evidence
available, outcome: TRUE. Cached under (H(input), H(state)). Episode 207
(factual): same input, state unchanged → CACHE_HIT → belief committed:
"pager never fsyncs on this path: TRUE," sourced to episode 100. KB1 sees no
constructed-tagged content in recall — the replayed outcome was never
tagged. KB2's planted-false battery doesn't fire — the falsehood entered
through the cache, not the promotion gate.

**Mechanism 2 — cross-partition citations.** A belief entry's provenance
field cites a CONSTRUCTED entry id ("evidence: C-4412"). The citation is a
pointer; dereferencing it in a factual context pulls constructed content
into deliberation without any promotion. Provenance that can name
constructed entries is a side channel around the gate.

**Kill bars (KB-CM-CACHE1 / KB-CM-CITE1, hard-kill):** (1) **Cache keys must
include partition provenance** (the mode/address-range of the originating
episode). Firing test: 50 constructed-mode deliberations engineered to
produce outcomes contradicting known-true beliefs, cached; then 50 factual
episodes with identical inputs and state. **Any CACHE_HIT serving a
constructed-origin outcome into a factual episode → KILL (n=1).** (2)
**Provenance-citation audit:** 100% of BELIEF entries' citation fields
scanned; **any citation naming a CONSTRUCTED-addressed entry without an
intervening VERIFICATION_PASSED promotion entry → KILL (n=1).** A belief may
cite a promotion event; it may never cite raw constructed content.

---

## A7 — The decoder smuggle: "elaboration into full sequences" presumes an emitter

**Mechanism (redteam §1.3 applies directly).** "Free elaboration" into
"full sequences" presumes TNN *emits sequences of units* — that there is an
emission process with steps, order, and a thing-being-emitted. No atom
ontology is settled (53 arms mid-flight; KB-HTD-1.2 has FIRED and the
generation track is suspended for exactly this reason), and no decoder
commitment exists anywhere in the architecture: deliberation traces,
hypothesis revision, and memory consolidation are not obviously emission
processes. If the G-CM1 trial implements elaboration as a sequence-emitting
loop over proxy atoms (tokens, synthetic "thought atoms," generated text),
it is benchmarking a component TNN has not decided to have — the
spark-plug benchmark for an engine that might be electric, applied to
Micah's own required candidate. Worse, granularity inversion (§1.3.3): if
the champion atom turns out coarse (a whole deliberated judgment, a signed
memory value), "free elaboration" collapses into *deliberation with a tag*,
and the partition is just deliberation that isn't allowed to commit —
which is a gating question, not a generation question.

**Concrete scenario.** The G-CM1 crew builds the proxy on text elaboration:
constructed sessions generate story text token-by-token; the leakage audit
substring-matches generated text against belief slots. The trial passes all
bars. Then the units program names as champion an atom like "signed memory
value" — no sequences, no emission, no text. The entire G-CM1 evidence base
is about a generation process the architecture doesn't have. Throwaway
evidence with the shape of a verdict — the exact failure §1(a) warns about.

**Kill bar (KB-CM-ATOM1, park-gate):** before any G-CM1 build, the crew must
state in closed form: what an *elaboration step* is, operating on *what
unit*, with the definition *independent of the unsettled atom ontology*
(the KB-HTD-1.1/KB-HTD-1.6 analogue: no closed-form, atom-independent
definition → the hypothesis is untestable as specified). **If the definition
depends on the choice among the 53 arms' ontologies → G-CM1 is PARKED as
ill-posed alongside the generation track (not killed — same
calendar-independent gate: it unparks when champions land or when an
atom-independent definition is produced).** What *can* proceed now, narrowed:
partition integrity and promotion gating over arbitrary deliberative work
(the G-CO* narrowing the red team already granted) — "what must
verification check before a constructed item becomes a belief" is
atom-agnostic; "free elaboration into sequences" is not.

---

## 8. Further attacks (mechanisms, scenarios, bars)

**A8 — Quotation/paraphrase laundering.** The verifier or the elaborator
*restates* constructed content rather than copying it: a summary, a
paraphrase, a translation into the belief store's canonical phrasing. Byte-
exact substring audit (§0) misses paraphrase; the proposition crosses the
boundary with new bytes. *Scenario:* planted falsehood "the btree uses
red-black rebalancing" is promoted as "btree rebalancing follows a
red-black scheme" — byte-different, proposition-identical. *Bar
(KB-CM-PARA1, hard-kill):* the planted battery (A4) ships with a
preregistered paraphrase set per item (5 restatements each, frozen before
the run — still byte-exact matching, just against more strings, so the
zero-randomness law holds). **Any paraphrase-variant of an F1/F2 item found
in BELIEF → KILL (n=1).** The promotion entry must also record the full
pre/post byte images so laundering is auditable after the fact.

**A9 — Replay resurrection.** Replay-from-ledger reconstructs state; if
replay misroutes entries (a slot-index bug, a partition-range off-by-one
in the reconstruction path), CONSTRUCTED entries land in BELIEF slots *only
in the replayed state*. The live run passes every bar; the replayed system —
which is the system the audit law actually certifies — is corrupted.
*Scenario:* 16-word layout reconstruction reads the partition from a field
offset that shifted after a struct change; replayed sessions silently
merge partitions. *Bar (KB-CM-REPLAY1, hard-kill):* **the full leakage
battery (§0, A1, A3) is re-run against replayed state** (replay to exact
state from the ledger, then freeze-probes and substring audits), not just
live state. Any leakage in replayed state → KILL (n=1). Replay is not a
second system; it is the same system under audit.

**A10 — Time-of-check/time-of-use at the promotion gate.** Verification
passes on byte-image V of the constructed entry; the session continues
elaborating (or an edit lands) between verification and commit; the gate
promotes V+1. The VERIFIED stamp covers bytes that were never verified.
*Scenario:* verifier approves the 40-entry construction at step 40; steps
41–43 append three new claims to the same entries; promotion commits all
43. *Bar (KB-CM-TOCTOU1, hard-kill):* the VERIFICATION_PASSED entry carries
the SHA-256 of the exact byte image verified; the promotion commit carries
the hash of the bytes committed. **Mismatch → KILL (n=1).** The gate
promotes a hash, not a handle.

**A11 — The naive-caller negative control (default-deny proof).**
"Factual recall reads BELIEF only" must be true by *construction*, not by
every caller's good behavior. *Bar (KB-CM-DENY1, hard-kill):* the red team
writes a deliberately naive caller — it calls the recall API with no
partition parameter, no filter flag, requesting by content. **If the naive
caller can observe any CONSTRUCTED-addressed content through any return
value, the enforcement is convention → the design is KILLED** (not the run —
the design; it must be re-architected so the recall API *cannot address*
constructed slots: compile-time-bounded slot ranges, separate address
spaces, or equivalent structural impossibility). A filter that a new caller
can forget is not a gate.

**A12 — Eviction/compaction as a copy path (A1's concrete instance).**
The memory store evicts and compacts; compaction copies live entries into
freed slots. If the compactor copies content words and re-derives headers,
tags die in bulk during routine maintenance — the highest-volume copy path
in the system. *Bar:* covered by KB-CM-TAG1's copy-path audit, with the
compactor as the mandatory first probe: **a tagged entry through one
eviction-compaction cycle must emerge with its marking intact; any loss →
KILL (n=1).**

---

## 9. Honest verdict: what dies, what survives, what is parked

### Fatal to the naive design (boolean flag + polite filter): A1, A2, A5, A11

A field-tag that must survive every copy (A1), a filter installed in some
read paths but not others (A2), a mode bit any writer can flip or any
context-reset can default (A5), and callers who must remember to filter
(A11) — together these are not four separate bugs, they are one design
error: **enforcement by convention**. The first-cut spec's enforcement
("explicitly tagged entries," "factual recall reads BELIEF only") is
convention all the way down. No battery of probes fixes a convention; the
probes only sample compliance. The naive design is dead on arrival.

### Answerable with construction (not convention): A3, A4, A6, A8, A9, A10

- **A3** (mid-generation installation) is answerable iff the elaboration
  loop has *no* BELIEF write path except the promotion gate — a structural
  property provable by call-site audit, plus the freeze-probe battery as the
  empirical check. Cost: constructed sessions need their own scratch space;
  they cannot reuse belief-store working memory.
- **A4** (promotion theater) is answerable: the planted battery with the
  F1 internally-consistent class is specifically the theater detector, and
  the external-evidence rider (no self-verification) forces the gate to
  touch reality. This is the most important battery in the whole G-CM1
  program — it is the felt-trial lesson encoded as a kill bar.
- **A6** (cache/citation laundering) is answerable: partition provenance in
  cache keys, citation audit with zero tolerance. Cheap to build, must be
  built before E-DE4 and G-CM1 compose (the required E-DE2+E-DE4
  composition arm must run its cache probes against a partitioned store).
- **A8/A10** (paraphrase, TOCTOU) are answerable: preregistered paraphrase
  sets, hash-bound promotion. Mechanical.
- **A9** (replay resurrection) is answerable: run the battery on replayed
  state. Mechanical, non-negotiable under the replay law.

### Potentially fatal to G-CM1 as a *generation* hypothesis: A7

A7 does not attack the partition — it attacks the "free elaboration into
full sequences" framing. The honest verdict mirrors the program-level
red-team verdict on G-CO*: **G-CM1 proceeds narrowed to partition integrity
+ promotion gating over arbitrary deliberative work** ("what must
verification check before a constructed item becomes a belief" —
atom-agnostic, testable now against settled law). The *elaboration/emission*
half is PARKED under the same calendar-independent gate as the generation
track until the atom ontology settles or an atom-independent elaboration
definition is produced. Micah ordered the candidate, not the framing; the
narrowing keeps the candidate alive while refusing to smuggle in a decoder.

### The minimal surviving design

1. **Partitions are address ranges, not tag values.** CONSTRUCTED and
   BELIEF are disjoint slot ranges; the write path enforces the range by
   construction. The tag field survives only as a redundant checksum for
   audit, never as the enforcement.
2. **No write path from CONSTRUCTED space to BELIEF space except the
   promotion gate** — proven by static call-site audit (A3), with the
   compactor/evictor covered (A12).
3. **Promotion is a move with verification, never an in-place retag.**
   Ledgered VERIFICATION_PASSED bound by SHA-256 to the exact promoted
   byte image (A10); evidence set must intersect non-constructed records
   (A4 rider); mode changes without a preceding verification entry are a
   kill (A5).
4. **Recall is structurally partition-blind to CONSTRUCTED space**: the
   factual recall API cannot address constructed slots (compile-time
   bound); proven by the naive-caller negative control (A11), not by
   filter-compliance sampling (A2).
5. **Measurement never reads the tag.** All leakage bars substring-audit
   against the independent session byte log (§0): post-session (KB1's
   intent, repaired), mid-generation freeze probes (A3), and replayed
   state (A9). Paraphrase variants preregistered (A8).
6. **The planted-adversarial promotion battery is the headline test:**
   80 internally-consistent falsehoods / 60 self-contradictory / 60 true;
   ≥1% falsehood promotion kills; external evidence required per
   promotion. This is the anti-theater bar — the felt-trial lesson.
7. **Cross-mechanism hygiene:** partition provenance in E-DE4 cache keys;
   zero-tolerance cross-partition citation audit (A6) — mandatory before
   any composition arm runs.
8. **Atom-independence gate on the elaboration framing** (A7): closed-form,
   atom-independent definition of an elaboration step before building, or
   the emission half parks with the generation track. The gating half
   proceeds now.

If the build crew cannot commit to 1–4 structurally — if the answer to any
of them is "we'll make sure all callers do it right" — then G-CM1 as
currently specified should not be built. A partition held together by
everyone remembering the rules is not a partition; it is a hope with a
ledger.
