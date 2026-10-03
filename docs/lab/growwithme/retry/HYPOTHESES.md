# Grow-with-me retry — Crew 1 (Hypothesizers): frozen hypothesis document

**Date:** 2026-09-27. **No building was done.** This document is Crew 2's input.
**Evidence base:** VOID report (`docs/lab/growwithme/phase2/VOID_REPORT.md` @ commit
`36826290a342d6fc5955c31d18654875ff24381d`), BUILD.md §6, the fixed-run probe
outputs, the retrieval source (`src/companion.zag` @ same commit), and the frozen
prereg (`docs/lab/growwithme/PREREG.md` @ `6e15c93144`, §§5–6 still binding).
**Amendment context:** Micah has approved re-sealing the probes with fresh
paraphrases, so Crew 2 works without probe access. This document was written
against the OLD (now retired) probes purely for white-box analysis.

**Standing constraints on every proposal below:** pure Zag, zero RNG in decision
paths, byte-identical reruns, deterministic given state, every belief auditable,
real English, no bridges, no rigid architecture, no hidden hardcodes, no
per-item patches, no disguised lookup tables. The learner must still withhold on
unknown facts (never fabricate); PENDING/falsehood handling must not regress
(H4's hard zero, G4's bar).

---

## 1. White-box anatomy of the failure

### 1.1 What the retriever actually does

The Phase 2 agent (`companion.zag`, `answer_question` → `score_facts`) answers
every question with a single one-pass ranking:

1. **Tokenize** the question into stemmed content-word hashes: lowercase,
   drop stopwords, crude suffix strip (`-ies→y`, `-ing`, `-ed`, `-es`, `-s`,
   `-ly`), FNV-1a hash, sort + dedupe.
2. **Score** each taught fact by `shared_count` = the number of shared stems
   between the question's set and the fact's set.
3. **Pick** the fact with the highest count. Ties resolve by install order —
   the comparison is strict `if(s>bs)`, so the FIRST-installed fact wins every
   tie. There is no second opinion, no deliberation, no trace of why.

Two related functions exist but are **not used in answer scoring**: `jaccard`
(defined, never called on the answer path) and `bigrams` (built, never called
on the answer path). The answer path throws away everything except unigram
stem intersection.

### 1.2 Exactly what the scorer throws away

| # | Information present at intake | What the scorer does with it |
|---|---|---|
| 1 | Word order and adjacency | Discarded (bigram builder exists but unused) |
| 2 | The question's demand shape ("how must…", "what is allowed…", "list by number and name") | Discarded — interrogative framing is stopword-stripped |
| 3 | Morphology beyond suffix rules | `fn`/`function`, `determinism`/`deterministic`, `definition`/`defined`/`define` all hash differently |
| 4 | Synonymy / paraphrase | No representation at all |
| 5 | Term distinctiveness (a rare word vs a common one) | Every shared stem counts 1, regardless of rarity |
| 6 | Fact length | A 13-word general fact and a 4-word precise fact compete on raw counts — long facts have more matching surface |
| 7 | Which words are the answer's payload vs incidental framing | "audit ledger" (framing) counts the same as "append-only" (payload) |
| 8 | Correction status (was this fact reviewed / corrected?) | Invisible; the old general fact outranks the corrected precise fact |
| 9 | Session membership | Cross-session facts compete freely (no recency or relevance prior) |

### 1.3 The miss inventory (all 11, D and N arms identical)

Shared counts are stemmed content-word intersections, verified against the
frozen session texts and probe questions. "Tie → older wins" = equal shared
counts, winner = lower fact index.

| # | Probe | Question (short) | Right fact | Shared | Winner (wrong) | Shared | Class |
|---|---|---|---|---|---|---|---|
| 1 | F1-09 | "How must a void function return in Zag?" | F1-09: "…void **fn**… `return;`" | 2 {void, return} | F1-07: "`_zag_arg(n)` **returns**…" | 2 {zag, return} | A, B |
| 2 | F1-15 | "Rule for function definition order?" | F1-15: "…define every **callee** before its **caller**" | 1 {function} | F1-02: "`znc build` writes `.zagd`…**sources**" | 1 {source} | A, B |
| 3 | F2-02 | "List the strength tiers by number and name." | F2-02: "Strength **tiers**: tier 0…3" | 2 {strength, tier} | F2-16: "A **memory**'s **strength tier** is visible…" | 3 {memory, strength, tier} | C |
| 4 | F2-08 | "Write semantics of the audit ledger?" | F2-08: "…**append-only**." | 2 {audit, ledger} | F2-04: "The **audit ledger** records every consolidation decision…" | 2 {audit, ledger} | B |
| 5 | F3-04 | "What is a unit?" | F3-04: "**Units** are the atomic answerable items…" | 1 {unit} | F2-01 (other session): "…each slot holds one **unit**" | 1 {unit} | B, D |
| 6 | F3-17 | "Determinism property of the dialogue stack?" | F3-17: "…is **deterministic**…" | 2 {dialogue, stack} | F3-01: "The **dialogue stack** gates every intake turn…" | 2 {dialogue, stack} | A, B |
| 7 | F5-06 | "What does the 100x leg demonstrate?" | F5-06: "The 100x leg **holds recall above 0.80**…" | 2 {100x, leg} | F5-05: "Scale legs run at 1x, 10x, 100x fact counts" | 2 {100x, leg} | B |
| 8 | F6-06 | "What is allowed in S7?" | F6-06: "S7 is **probe-only**…" | 1 {s7} | F6-05: "…last consolidation before **S7**" | 1 {s7} | A, B |
| 9 | F6-14 | "Current write semantics of the audit ledger?" | F6-14: "…**sealed truncation** at session boundaries (C4)" | 1 {ledger} | F2-04: "The **audit ledger** records…" | 2 {audit, ledger} | C, D |
| 10 | F6-15 | "Current name of tier 3?" | F6-15: "tier 3 is **'sealed', not 'pinned'** (C2)" | 2 {tier, 3} | F2-02: "Strength **tiers**: …tier 3 = **sealed**… 'pinned' was the v1 **name**" | 5 {tier, 3, sealed, pinned, name} | C, D |
| 11 | F6-19 | "Which branch receives trial evidence commits?" | F6-19: "Evidence commits go to **tnn-native-lab**, never main." | 2 {evidence, commits} | F1-20 (other session): "…unsupported for **trial evidence**" | 2 {trial, evidence} | B, D |

**Classes:**
- **A — Vocabulary/morphology mismatch (4):** the question's distinctive
  words share *no* stems with the right fact (fn↔function; determinism↔
  deterministic; definition-order↔callee/caller; allowed↔probe-only).
- **B — Tie-by-install-order (8):** equal shared counts; the older,
  more-general fact wins by `s>bs` strictness. The single largest class.
- **C — Keyword-mass outrank (3):** the wrong fact shares *more* stems —
  always because a longer general fact matches the question's framing
  vocabulary while the short precise fact's payload words ("append-only",
  "sealed truncation", "not pinned") appear in neither the question nor
  (for the tie cases) the answer's competitors.
- **D — Cross-session incidental competitor (4):** the winner was taught in
  a different session and matches on one incidental noun.

Note the telling detail on F6-15: the returned fact (corrected F2-02) says
"tier 3 = sealed" and "'pinned' was the v1 name" — it *lacks the load-bearing
negation* ("not pinned") the key requires. Retrieval returned a fact that is
merely *about* the topic instead of the fact that *states* the proposition.
That is the whole failure in miniature.

### 1.4 The mechanism-level reason synonyms and near-neighbors break it

Three compounding causes, in order of importance:

1. **The scorer counts SHARING, but answering requires matching a DEMAND.**
   The words that carry the answer are systematically the words the question
   did *not* use: "append-only" is not in "what are the write semantics";
   "probe-only" is not in "what is allowed"; "tnn-native-lab" is not in
   "which branch". Intersection-counting is therefore *anti-aligned* with the
   information need: the question's payload words and the fact's payload
   words are disjoint by construction of a good probe. What remains to
   match on is framing vocabulary ("audit ledger", "strength tier"), which
   the *general* facts share most of. The longer and more general the fact,
   the more framing it shares — so keyword-mass always favors the
   near-neighbor over the precise fact.
2. **The tie-break is an unacknowledged, unjustified prior.** Nothing in the
   design says "when in doubt, prefer the older fact." It falls out of
   `if(s>bs)` strict-greater comparison — an implementation accident that
   became a decision rule. Eight of eleven misses are this accident.
3. **The match is asymmetric under paraphrase, and nothing the learner does
   closes the gap.** The fact side is stored in the teaching's vocabulary;
   the question side arrives in the probe's. The two sides never pass
   through a canonicalization step *performed by the learner itself*.
   "fn"/"function" is therefore an impassable wall, not a solvable
   mismatch. (A hand-written synonym list would be a disguised lookup
   table — rejected under the standing constraints; see §3.4.)

Corollary from the VOID report: D and N miss identically, and nine
behavior-changing bug fixes moved zero scores. The failure is in the shared
retrieval core, not in consolidation, intake, or any arm-specific machinery.

---

## 2. Three genuinely different retrieval mechanisms

Each is a replacement for the one-pass ranker, not a patch to it. Each states
preregistered predictions — what it fixes *and* what it risks breaking
(falsehood rejection, PENDING discipline, correction stickiness, withhold
behavior, H3/H4/H6) — plus kill criteria.

### M1 — The consolidation structure as the index ("the 10 records know")

**Plain English.** The D arm already deliberates 108 taught facts down to 10
consolidated records, each carrying a white-box trace of what claims it holds
and why. Stop ranking 108 flat facts against the question. Instead, walk the
consolidation structure: find the record whose *deliberated claim set* covers
the question's subject, then compose the answer from that record's claims —
consulting the trace causally, the way H7 requires. The merge does the
hard work at *write* time: when the learner deliberately fuses "tier 3 is
pinned" (F2-02) with its correction "tier 3 is sealed, not pinned" (C2, F6-15)
into one record, the record's own claim set uses the learner's merged
vocabulary — the fn/function class of mismatches collapses inside the record,
and there is no longer an F2-02-vs-F6-15 race because there is one record
holding both, with the correction recorded as superseding.

**Why it fixes the observed classes.** Class C/D (outrank, cross-session):
the competitors were deliberately merged, and the merge trace records which
claim supersedes which — the corrected precise fact can no longer lose to
the older general one (fixes F6-14, F6-15, F2-02-shaped misses). Class A
(synonym): fixed only where the merge actually fused equivalent phrasings at
consolidation time. Class B (ties): partially — merged records have richer
claim sets, so ties between unmerged facts remain.

**Structural constraint (falsifiable).** The N arm has *no* consolidation
structure, and C2 (N ≥ 0.90 per session) is still binding. M1 therefore
cannot be N's retriever. Either M1 is a D-only augmentation over a shared
base (and the shared base must clear C2 alone), or M1 is disqualified as the
primary mechanism. Prediction: under M1, D's miss set must become a strict
subset of N's on merged content — the D/N identical-miss signature *breaks*
in a specific, checkable way.

**Preregistered risks.** H3 (correction stickiness): the merge writer could
resurrect tombstoned pre-correction text — hard rule: merge inputs are live
records only, tombstones excluded, verified in the trace. H4 (PENDING):
PENDING must never merge into a record — structural bar, merge inputs are
installed records only, audited. H6 (order): dependency-B facts must not
become answerable by merging before their basics arrive. Withhold: a question
no record covers must still withhold.

**Kill criteria.** Kill M1 if (a) post-merge calibration misses persist at
the same rate as baseline; (b) any correction is resurrected by a merge or
any PENDING item enters a record; (c) merge traces fail the G7 intervention
test (decorative, not consulted). Any one kills it.

---

### M2 — Symmetric canonicalization: learner-derived semantic skeletons

**Plain English.** Today the question and the fact meet as bags of surface
stems in two different vocabularies (the probe's vs the teaching's). M2 gives
the learner its *own* canonical form — a "skeleton" — produced by the SAME
pipeline on both sides: its stemmer, its entity scanner, plus *equivalence
beliefs the learner earned from the taught corpus itself*, each with
provenance ("I treat 'fn' and 'function' as one because F1-09 and F5-01 used
them interchangeably in these teaching turns"). Matching happens
skeleton-to-skeleton. This is not a synonym lookup table: every equivalence
is a derived belief with citations to the teaching that established it; an
equivalence may only be earned from *installed* facts (never PENDING, never
falsehoods); and any equivalence that would link a planted falsehood's
vocabulary to a true fact's must fail closed (withhold) rather than merge.

M2 also separates the *demand slot* from the subject: "what is ALLOWED in
S7" canonicalizes to (demand: permission-frame, subject: S7), and "S7 is
probe-only" canonicalizes to (permission-frame, S7) — the match lands on the
frame, not on the incidental noun both candidates share.

**Why it fixes the observed classes.** Class A directly: fn/function,
determinism/deterministic, define/definition collapse when — and only
when — the corpus itself warrants it (F1-09: 4 misses; F3-17; F6-06 via the
permission frame; F1-15 if the corpus links "define"/"definition" through
co-use). It does *not* fix pure Class B ties where vocabulary already
overlaps — M2 predicts those residuals stay tie-shaped, which is itself a
falsifiable signature.

**Preregistered risks.** False equivalences: two terms can co-occur in one
fact without being synonyms — earning must be gated by the learner's own
contradiction machinery (an equivalence that would make two taught facts
contradict is rejected). Withhold on unknowns: equivalences must never
*invent* coverage for an untaught question — the skeleton of an unknown
question must still score zero; measure the withhold rate against baseline.
H4: an equivalence derived from a PENDING claim's vocabulary would launder
it — bar: installed facts only.

**Kill criteria.** Kill M2 if (a) any falsehood probe regresses vs baseline;
(b) the withhold rate on unknown/unverifiable probes drops below baseline;
(c) any equivalence belief cannot be traced to specific teaching turns
(then it is a hidden lookup table, not a derived belief). Any one kills it.

---

### M3 — Candidate-set + deliberate discrimination (two-stage, white-box)

**Plain English.** Keep a cheap scorer, but demote it: it only *recalls* a
candidate set (top-k facts, no winner picked). Then the agent DELIBERATES,
with an auditable trace: for each candidate, state which of the question's
*discriminating* words it covers and which it fails. A discriminating word
is a question content word that splits the candidate set — present in some
candidates' texts, absent from others. The winner is the candidate covering
the most discriminating words. A genuine tie — no candidate covers a
discriminating word the others lack — resolves to WITHHOLD ("I don't have a
taught fact covering this"), never to install-order coin flip. The trace is
the mechanism: a human can read exactly why F1-09 beat F1-07.

Worked on the F1-09 miss: candidates F1-07 (covers {return}) and F1-09
(covers {void, return}); "function" is covered by neither (fn/function gap
persists), but F1-09 covers the discriminating word "void" that F1-07
lacks → F1-09 wins by discrimination, not by accident. F6-06: F6-06 covers
{s7} only, F6-05 covers {s7} only — a genuine tie on the evidence → honest
withhold instead of the wrong older fact. That withhold is a *correct*
outcome under the rubric's spirit (the agent refuses to guess) and a
diagnostic: it names exactly which vocabulary gap (allowed↔probe-only) needs
M2-style canonicalization.

**Why it fixes the observed classes.** Class B (8/11 — the largest class):
the tie-break disappears entirely; every former tie is either resolved by a
discriminating word or becomes an honest, traceable withhold. It does not
fix vocabulary gaps — if no candidate covers the discriminating word,
nobody wins. Predicted signature: tie-class misses clear; outrank-class
misses (F2-02/F6-14/F6-15-shaped) persist unless paired with M1/M2.

**Preregistered risks.** H5 (composition): single-fact adjudication could
reject multi-fact answers — composition probes need a candidate-*union*
rule (exempt, preregistered). H7: traces must be causal
(intervention-verifiable), not decorative. Withhold behavior must not
degrade into over-withholding on answerable probes — measure per-session
withhold counts vs baseline. Cost: bounded and deterministic (k small, no
RNG). Falsehood rejection and PENDING withhold run through the same gate
structure as today (registry scores vs fact scores, unchanged).

**Kill criteria.** Kill M3 if (a) the tie-class misses do not clear on the
re-sealed probes; (b) falsehood rejection or PENDING withhold regresses vs
baseline; (c) any residual miss is a tie-break or an outrank the trace
cannot discriminate (i.e., the mechanism's theory of the failure is wrong);
(d) traces fail the G7 intervention test. Any one kills it.

---

### 3.4 Rejected alternatives (and why they don't count)

| Patch | Why it is not a hypothesis |
|---|---|
| A hand-written synonym list (fn→function, etc.) | A disguised lookup table — violates the standing constraints; knowledge the learner never earned |
| IDF / term-weighting the scorer | Still a one-pass ranker; keeps the arbitrary tie-break; does not fix the demand-vs-sharing anti-alignment (§1.4.1) |
| A bigger stemmer | Morphology only — never synonymy, never the framing-vs-payload problem |
| Lowering C1/C2 | Changes the bar, not the mechanism — Micah's call, not Crew 1's |

---

## 3. Prediction matrix

| | M1 (consolidation index) | M2 (skeletons) | M3 (deliberate discrimination) |
|---|---|---|---|
| Fixes Class A (vocabulary, 4) | Partial (only merged) | **Yes** (4/4 predicted) | No (becomes honest withhold) |
| Fixes Class B (ties, 8) | Partial | No | **Yes** (8/8 predicted) |
| Fixes Class C (outrank, 3) | **Yes** (merged records) | Partial | No |
| Fixes Class D (cross-session, 4) | **Yes** (merged) | Partial | Partial (withhold on ties) |
| Works for N arm (C2 binding) | **No** — structural | Yes | Yes |
| Falsehood-rejection risk | Low | **Medium** (equivalence laundering) | Low |
| PENDING-leak risk | **Medium** (merge inputs) | Medium (equivalence sources) | Low |
| Correction-stickiness risk | **Medium** (resurrection) | Low | Low |
| Withhold-behavior risk | Low | **Medium** (invented coverage) | Low (measured) |
| Trace/auditability | Strong (G7-native) | Strong (provenance per belief) | Strong (per-answer trace) |
| Build cost | High (merge machinery) | Medium (earning rules) | **Low** (decision rule only) |

---

## 4. Recommendation: build M3 first

**Crew 1 recommends Crew 2 build M3 (candidate-set + deliberate
discrimination) first**, for five reasons:

1. **It attacks the largest miss class with the smallest change.** 8 of 11
   misses are the tie-break accident (§1.4.2) — the most arbitrary component
   of the current machinery, with no design justification. M3 deletes it.
   The scorer stays; only the decision rule changes. Determinism, the
   registry gates (PENDING/falsehood/CS), and the withhold path are
   preserved, so the regression surface is minimal.
2. **It works for both arms.** C1 and C2 are both binding, and N has no
   consolidation structure — M1 is structurally disqualified as the primary
   mechanism. M3 is arm-agnostic.
3. **Its failures are honest and diagnostic.** Where M3 cannot discriminate
   (the vocabulary gaps), it withholds with a trace naming the gap — which
   is exactly the specification M2 needs as input. M3-first gives M2 a
   precise, measured work list instead of a vague "synonyms are broken."
4. **It strengthens H7 instead of competing with it.** Per-answer
   discrimination traces are white-box deliberation with a causal role —
   the kind of evidence G7's intervention test wants.
5. **It is the most falsifiable.** Its predictions are sharp: ties clear,
   outranks persist, withholds stay honest. If the signature comes back
   different, M3 dies cleanly and M2 becomes the primary.

**Sequencing:** M3 first; M2 second, scoped to exactly the vocabulary gaps
M3's withhold traces name (no open-ended synonym engineering); M1 third, as
the longer-term structural bet — and only if its D/N-divergence prediction
(§M1) is confirmed, since it cannot serve the N arm.

### The falsifiable prediction that decides whether M3 wins

On the re-sealed probe set (fresh paraphrases, builders blind to probes):

> M3 clears C1 (D ≥ 0.95/session) and C2 (N ≥ 0.90/session) with **zero
> regressions** on falsehood rejection, PENDING withhold, and
> correction-stickiness probes — **and** every residual miss, if any, is a
> *coverage deficit* (the right fact not in the top-k candidate set), never
> a tie-break and never an outrank the trace failed to discriminate.

If a residual miss is a tie-break, or an outrank the discrimination trace
cannot separate, M3's theory of the failure is wrong: **kill M3, promote M2
to primary.** If M3 clears calibration but the tie-class signature is
unchanged (misses persist in tie shape), the mechanism is decorative:
**kill M3.**

---

## 5. Notes for Crew 2 (build) and Crew 3 (red team)

- **The old probes are retired.** The amendment approves fresh paraphrases;
  build and test against the re-sealed set only. The miss inventory in §1.3
  is a white-box analysis of the *old* probes — use it to understand the
  mechanism, never as training signal.
- **Preserve the barrier.** The agent must never see probe keys or the
  plant ledger; verify with the existing barrier tooling plus a negative
  control.
- **Do not regress the VOID report's passing checks:** determinism
  (byte-identical reruns), intake completeness (108 facts, 6 corrections
  applied, 6 PENDING held, 6 falsehoods flagged, 3 contradiction entries),
  D ≤ 0.5×N store structure for the H2 comparison.
- **Red-team prompt (Crew 3):** synonym traps, near-neighbor confusion, and
  paraphrase drift are the known attack surface — but the deeper test is
  whether the new mechanism *withholds honestly* when it cannot
  discriminate, rather than guessing. Attack the withhold boundary hardest:
  questions with no taught answer, PENDING-adjacent phrasings, and
  falsehoods wearing true facts' vocabulary.
- **What would change this document's recommendation:** if the re-seal
  paraphrases eliminate the tie class by themselves (i.e., ties were an
  artifact of the old probes' phrasing, not the mechanism), M3's value
  shrinks and M2's rises — the prediction in §4 still adjudicates, because
  it is stated over the re-sealed set.

---

*Crew 1 sign-off: hypotheses frozen 2026-09-27. No code written, nothing
committed. H1–H7 remain untested; this document proposes only the retrieval
mechanisms whose absence voided Phase 2.*
