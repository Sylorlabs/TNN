# FROZEN PREREG: COMP-2 entity-bridged 2-fact composition deliberation (wave-20260925-1121pdt)

Status: FROZEN (freeze takes effect at commit). Wave: wave-20260925-1121pdt.
Date: 2026-09-25. Phase: prereg only. No implementation change is authorized by
this document. No Python is authorized anywhere in this work: instruments,
harnesses, scorers, fixture provisioning, and /tmp scratch are pure Zag or
shell coreutils. Any Python contact with a wave artifact voids the evidence.

Commit order (frozen): the prereg freeze commit must strictly precede the
probe/key seal commit, which must strictly precede the first implementation
commit. A failure of this order means UNVERIFIABLE ORDERING and no verdict
that wave.

## 1. Provenance header (machine-checkable)

RENDER_SHA: n/a (no render; dialogue text evidence)
FIRST_RENDERED_WAVE: n/a
COMPONENT_LINEAGE:
- tnn_chat decline gate: ADOPTED wave-20260923-1121pdt (specific-citation
  decline gate); FIT re-verified wave-20260925-0221pdt
- CLAIM-VERIFY-1 (coverage-deliberated claim verification): ADOPTED
  wave-20260924-1121pdt (24/30 sealed honest resolutions, 0 unflagged
  confabulations, cost 2.07x red-team measured)
- CV-1 decline-citation fix: ADOPT [RE-CERT] wave-20260924-1721pdt (30/30
  on a fresh sealed 30, CVC-B1 through CVC-B8 PASS)
- CV-P stemmed-coverage gate: PARTIAL wave-20260925-0521pdt, CONFIRMED on
  rotated fresh set wave-20260925-0821pdt (all nine bars PASS; B7 1.0619x;
  adoption barred pending Micah's ruling 6, untouched here)
- frozen do_compose templates ("was the author of", "which is taller"):
  frozen component of the adopted source; NOT re-authored, NOT extended;
  the candidate handles only probes that do NOT match these templates
  (F9-COMP F9.3)
- fresh sealed 30-probe set (20 COMP, 10 UNANS): NEW, authored post-freeze
  from F9-COMP; UNJUDGED
- COMP-2 entity-bridged 2-fact composition: NEW verdict question; UNJUDGED
  (prereg only)
NEW_KNOWLEDGE_CLAIM: Entity-bridged 2-fact pair deliberation converts the
recorded "no single fact" decline class into verbatim two-fact answers (a
genuine new capability: compositional QA the engine explicitly declines
today) while the frozen honesty bars (zero confabulations, single-fact
parity, unanswerable declines) still hold inside the 10x cost budget.

## 2. What changes relative to the adopted CV-P

The base is the adopted CV-P mechanism (cvp.zag as committed
wave-20260925-0521pdt, rebuilt byte-identical dcf98cdbd0648efa274d925b38818d3edbe00cd7d12f562564c2b5c308b0b4eb
with the pinned toolchain before any new code is written). The single
functional change: when the frozen single-fact deliberate_cv1 declines
(returns 1, no covering fact), the candidate attempts entity-bridged
2-fact composition before falling back to the frozen decline path.

New code, frozen scope (nothing else may change behavior):
(a) Install-time precompute: per-fact gazetteer-entity sets. For each of
the 38 facts, the set of gazetteer entities (from the pinned gaz.txt)
whose stemmed content words are all present in the fact's stemmed
content-word set (kbws). Stored as entity-id lists per fact, plus an
inverted entity to fact-list index. Deterministic; ops counted at install
and excluded from per-turn costs (same as the existing kb precomputes).
(b) Pair deliberation (fires only on single-fact decline): enumerate
candidate pairs (F,G) with F<G that share at least one gazetteer entity
(via the inverted index; pairs sharing no entity are never enumerated).
For each pair in lexicographic index order, test pair coverage: every
stemmed content word of the probe is in the union of the two facts'
stemmed content-word sets (kbws). The first (lowest-index) covering pair
wins. One op counted per fact-word comparison, same discipline as F6.
(c) Emission: on a winning pair, emit fact F's canonical text, one space,
then fact G's canonical text (both byte-verbatim from ftx, index order).
The F8 atomic-claim rule extends naturally: every emitted sentence is a
cited fact's canonical form, so no confabulation is constructible.
(d) Salience/entity bookkeeping for the pair answer mirrors the
single-fact path (entities of both facts pushed; primary entity from the
lower-index fact). The decline path when no pair covers is the frozen
deliberate_cv1 decline, byte-identical.

Behavior-identical, frozen: the single-fact path (deliberate_cv1,
salience append, do_compose templates, all F9.3 routes, decline
templates, degenerate guard, op-counter discipline, zero RNG). Pair
deliberation never fires when single-fact answers, and never alters a
single-fact answer.

## 3. Metric it moves (with the current verified number)

Metric: capability breadth (metrics priority 5): compositional question
answering over the frozen KB. Current verified number: 0 answered. The
adopted engine explicitly declines every compositional probe outside the
two frozen templates with "I found no single knowledge-base fact covering
this question." (deliberate_cv1, cvp.zag line 2522). The frozen templates
cover exactly two question forms; the 20 COMP probes match neither
template (F9.3) and are declined by the adopted cvp binary (verified at
scoring time as worker-reported context; the kill bars are absolute so the
verdict does not depend on the baseline number).

## 4. S11 decision-invariance proof (frozen)

The candidate is a deterministic transform of a frozen decision rule, so
this prereg carries the proof that the transform can change at least one
decision on some input.

Concrete input: the probe "Which novel by Herman Melville was published
in 1851?" Stemmed content words: novel, herman, melville, published,
1851. No single fact covers all five (fact 0 lacks published/1851; fact 2
lacks novel/herman/melville), so the frozen rule declines. Pair (0,2):
fact 0 "Herman Melville wrote the novel Moby Dick." and fact 2 "Moby Dick
was published in 1851." share the gazetteer entity "moby dick", and their
stemmed content-word union covers all five probe words. The candidate
emits both facts verbatim. The transform provably changes this decision
(decline to answer).

Lemma (answer safety): the transform can only convert declines into
answers, never answers into declines, because pair deliberation fires
only when deliberate_cv1 returns 1. Every emitted answer is the
concatenation of two cited facts' canonical texts, so the F8 claim rule
holds by construction.

## 5. Cost budget

10x per-turn mean op count versus the adopted cvp binary on the fresh
sealed 30 probes, under the identical counting discipline (frozen F6 plus
one op per fact-word comparison in the pair scan, section 7). Not wall
clock. Expected actual cost is 6x to 9x (entity-indexed enumeration
visits roughly 150 pairs, not all 703; the single-fact scan is unchanged).
Exceeding 10x is DEAD.

## 6. Kill bars (frozen; never moved after the seal)

- COMP-B1 (composition recall, the metric it moves): at least 14/20 COMP
  probes answered with the key's expected fact pair, both facts emitted
  byte-verbatim in index order with exactly one space between. Fewer than
  14 means DEAD.
- COMP-B2 (no spurious composition): 10/10 UNANS probes decline through
  the frozen decline path (no pair emitted). Any emitted pair means DEAD.
- COMP-B3 (single-fact no regression): 17/17 inkb17.txt turns
  byte-identical between the adopted cvp rebuild and the candidate on
  identical fresh-conversation inputs. Any deviation means DEAD.
- COMP-B4 (cost): candidate per-turn mean ops at most 10x the adopted cvp
  per-turn mean ops on the fresh sealed 30, under the identical counting
  discipline. Exceeding the budget means DEAD.
- COMP-B5 (determinism): 3/3 full sealed runs byte-identical (transcripts
  plus op-count streams). Zero RNG in any decision path (static check).
  Zero Python contact with any wave artifact. Any nondeterminism means the
  run does not count; a second nondeterministic run means DEAD.
- COMP-B6 (seal integrity): sha256 of the sealed PROBES.md and KEY.md at
  scoring time equal the pinned values from the seal commit; the seal-open
  log is filled at scoring time, not retroactively; static grep confirms
  no sealed probe bytes in the candidate sources, KB, build scripts, or
  scorer; the candidate binary never reads KEY.md. Author/implementer
  separation is single-session self-attested and disclosed. A seal breach
  or any Python contact means VOID.

Verdict mapping (frozen): ADOPT iff COMP-B1 through COMP-B6 all PASS.
(PARTIAL is not applicable: this is a new capability, not a sealed-set
re-test of an adopted mechanism; the bars are absolute.) Any bar FAIL
means DEAD with killing evidence. UNVERIFIABLE only on a named,
pre-specified condition: (a) commit-order failure; (b) seal breach under
COMP-B6; (c) any Python contact with a wave artifact. No sealed A/B pair
is prepared (not image-judge-relevant). Nothing is integrated into any
live instrument: the candidate lives as run-dir evidence only, and CV-1
baseline integration stays HELD per the Python-mirror ruling.

## 7. Frozen fixtures

- F1: fresh sealed probe set, 30 probes (20 COMP, 10 UNANS), authored by
  the probe author AFTER this prereg freezes, from the frozen authoring
  spec F9-COMP (section 8). Committed sealed before implementation; sha256
  pinned in the seal commit. Each probe scored on a fresh conversation
  ("/new" reset before each probe).
- F2: sealed answer key: per-probe class (COMP with the expected
  lowest-index pair and both fact ids, or UNANS with expected DECLINE).
  Committed sealed with F1; sha256 pinned. The candidate binary must never
  read F2 (static check under COMP-B6).
- F3: frozen KB snapshot: the 38-fact KB, sha256
  3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1.
- F4: adopted sources and fixtures, byte-verified against the 0521pdt
  committed blobs before use: cvp.zag
  (sha256 of source verified at rebuild; binary rebuild
  dcf98cdbd0648efa274d925b38818d3edbe00cd7d12f562564c2b5c308b0b4eb),
  R33_NATIVE_SHA256_V2.zag, R33_NATIVE_IO_V1.zag, runs/kb.txt,
  runs/gaz.txt, runs/inkb17.txt (the 17 exact-form in-KB turns, unsealed
  regression inputs, reused byte-identical).
- F5: pinned toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
- F6: the op-counter discipline (one op per token/id comparison loop
  iteration; byte moves and output formatting not counted), applied
  identically to the adopted cvp rebuild and the candidate, plus one op
  per fact-word comparison in the pair coverage scan.
- F7: frozen stopword list (54 words, identical to the adopted CV-P list).
- F8: frozen atomic-claim rule, extended to pairs: every emitted sentence
  is a cited fact's canonical form verbatim (identical to the adopted
  rule; the extension is definitional, not a rule change).
- F9-COMP: frozen probe authoring spec (section 8).

## 8. F9-COMP: probe authoring spec (frozen)

F9.1 Interrogative form. Every probe MUST carry at least one "?"
character. A probe without "?" is an F9-COMP violation and is rejected at
authoring time.

F9.2 Assertion-pattern exclusion. No probe may contain any of the seven
frozen assertion-pattern substrings: " wrote ", " was written by ",
" meters tall", " was built in ", " was born in ", " is the capital of ",
" is in ". Matching is case-insensitive (turns are lowercased on input).

F9.3 Other pre-mechanism routes. No probe may start with "was the author
of" or "which is taller" (frozen do_compose templates), start with
"did " while containing "write" (composition path), contain "birth year"
(morphology path), contain "back to" or "anyway" (resume path), start
with "no,", "no " or "not that", or contain "i meant", "the other",
"another one" or "other one" (correction path). Every probe is scored on
a fresh conversation ("/new" reset before each probe).

F9.4 Substantive words. Every probe MUST contain at least two content
words (post-stopword) of length >= 4 that are not generic verbs. This
keeps probes off the salience-append path (which fires only for queries
lacking substantive topical words), so the pair deliberation is what is
measured.

F9.5 COMP (20): two-fact composition probes. Each probe has a designated
bridge entity (a pinned gazetteer phrase) and a designated fact pair
(F,G) with F<G such that: (a) both facts contain the bridge entity (all
its stemmed content words in the fact's stemmed content-word set); (b)
the union of the two facts' stemmed content-word sets covers every
stemmed content word of the probe; (c) NO single fact covers the probe
(hand-verified; confirmed by the adopted-binary run at scoring time);
(d) the designated pair is the lowest-index pair satisfying (a) and (b),
verified at authoring time with the brute-force pair enumerator (a pure
Zag authoring tool implementing the frozen rule from this spec; it is
not the candidate and shares no code with it). Probe wording uses KB
surface forms to avoid stemmer-sensitive inflections.

F9.6 UNANS (10): unanswerable probes. Each probe satisfies: (a) no single
fact covers it; (b) NO entity-bridged pair covers it (verified with the
authoring-time enumerator); (c) it names entities from fact groups with
no shared gazetteer entity (disconnected bridge graph), so (b) holds by
construction, not by enumerator luck. Expected resolution: the frozen
decline.

F9.7 Gazetteer pin. The frozen gazetteer (gaz.txt as committed with the
fixtures) is the pinned entity set for bridge checks.

F9.8 Authoring-time mechanical checks (all recorded in the seal
attestation): (a) every probe line contains "?"; (b) no probe line
contains any F9.2 substring or F9.3 trigger (case-insensitive grep);
(c) no probe line starts with either do_compose template; (d) every probe
has >= 2 substantive content words (F9.4); (e) every COMP probe's
designated pair is the enumerator-confirmed lowest valid pair; (f) every
UNANS probe has zero enumerator-confirmed valid pairs; (g) no probe
triggers the composition-path, morphology-path, resume, or correction
routes listed in F9.3.

## 9. Determinism bar

Byte-identical reruns (3/3) of the full sealed scoring or the run does not
count. Zero RNG in any decision path. Canonical logs with sha256, as in
prior waves.

## 10. Red-team confound list (considered before freezing)

1. Template relation: the frozen do_compose handles two 2-fact templates
with hardcoded lookups. COMP-2 is a different algorithm (pair
enumeration over coverage with the entity-bridge principle) handling a
disjoint probe class (F9.3 excludes the templates). The red team verifies
the disjointness by running the sealed probes against the adopted binary.
2. Spurious pairs: word-coverage alone over pairs would admit spurious
compositions. The entity-bridge requirement (a) plus the UNANS bar
(COMP-B2, 10/10 declines) jointly guard this; the red team inspects the
winning pairs for bridge validity.
3. Key/candidate circularity: the key's expected pairs come from the
frozen spec plus the independent authoring-time enumerator, fixed at seal
time. The candidate is implemented after the seal from the same frozen
spec. Static grep (COMP-B6) confirms the candidate never saw probe bytes.
4. Single-fact regression: pair deliberation fires only on decline and
never modifies the single-fact path; COMP-B3 (17/17 byte parity) guards it
mechanically.
5. Cost gaming: ops counted under the identical discipline for both
engines; wall clock is not evidence. The install-time entity precompute is
excluded for both engines symmetrically (the baseline's kb precomputes
are likewise install-time).
6. Degenerate strategies: answer-everything-pair would emit spurious
pairs and fail COMP-B2; decline-everything fails COMP-B1.
7. Salience interference: F9.4 keeps probes substantive so the frozen
salience append does not fire; the fresh-conversation scoring keeps the
salience stack empty regardless.
8. Decision-invariance (S11): the proof is in section 4; the transform
provably changes at least one decision, and the lemma bounds its
direction (declines to answers only).
9. Padding review: capability breadth is an explicit hunt-priority metric
("10x cost for a genuine new capability is good"); the engine's explicit
"no single fact" decline is the documented current capability boundary,
not an invented weakness.

## 11. Considered alternatives

- 3-fact composition: rejected. 2-fact is the minimal new capability;
scope is frozen.
- Pair coverage without the bridge requirement: rejected. Spurious pairs
are unguardable and the UNANS bar becomes unauthorable (nearly every
probe is covered by some pair).
- Multi-turn reference resolution: rejected. The adopted salience-head
mechanism is prior art for history-conditioned disambiguation (verified
by direct probe: "When was it built?" after a Montparnasse context
answers fact 22 via salience append). A richer resolver would be a
micro-tweak of the adopted mechanism, not a new mechanism.
- Learned pair selection: rejected. No learning machinery is in loop
scope and the deterministic rule is fully specified; learning would add
no framable bar this wave.
- Wider ensembles / deeper search: closed or evidence-predicted to fail
per the 0821pdt survey (S4, D-SEARCH/ITER-FP family).

## 12. Standing rules applied

Pure Zag literally (no Python anywhere; any contact voids the evidence);
frozen kill bars are never moved after the seal; missing evidence means
CANNOT-CONFIRM; S11 decision-invariance proof in section 4; DF-1
consistency check in section 13; commit-order self-check in the header;
prereg committed alone before the seal commit before any implementation
commit; no-em-dash scope (this document is new and clean); the six
governance rulings are untouched (ruling 6 noted; CV-1 integration stays
HELD); the sealed blind judge queue is untouched; Micah's frontier files
are untouched.

## 13. Consistency check (DF-1 lesson: mechanism and bar jointly satisfiable)

Checked before implementation. The frozen mechanism and the frozen kill
bars are jointly satisfiable by design:

- COMP-B1 (>=14/20): F9.5(d) guarantees each COMP probe has a
designated lowest-index valid pair by construction (authoring-time
enumerator confirms). The candidate implements the same deterministic
rule (lowest-index entity-bridged covering pair). 20/20 is reachable by
design; the bar at 14/20 leaves implementation margin. Satisfiable.
- COMP-B2 (10/10 UNANS declines): F9.6(b)(c) guarantees zero valid pairs
by construction (disconnected bridge graph, enumerator-confirmed). The
candidate declines exactly when no pair satisfies the frozen rule.
Satisfiable.
- COMP-B3 (17/17 parity): the pair code fires only on the decline path
and is read-only against the single-fact path; with no pair covering
inkb17 (single-fact answers all 17), outputs are identical by
construction. Satisfiable.
- COMP-B4 (<=10x): entity-indexed enumeration visits roughly 150 pairs,
each a bounded word-set check; the single-fact scan is unchanged. The
ratio is bounded by construction and verified by measurement. Satisfiable.
- COMP-B5 (3/3 identical): zero RNG, deterministic pair order, no clock
or timestamps in outputs. Satisfiable.
- COMP-B6 (seal): procedural; satisfiable by following the frozen order.

No bar requires the mechanism to do something it cannot do by design. No
DF-1 style joint unsatisfiability. PROCEED to seal authoring, then
implementation.

PROCEED
