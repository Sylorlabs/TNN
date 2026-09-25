# IDEAS ADDENDUM — MATH R3 native engine specs (DRAFT — freezes with prereg)

Four native architectures (reason DIRECTLY over raw utterance bytes; no
NL→schema translation; byte-span operations only). Chosen for mechanism
diversity: forward-rewrite (N1), backward-eliminative (N2), parallel
shared-ledger (N3), analogical (N4). Fable designed N1 (full design doc:
`/tmp/r3_fable_design.txt`, to be committed with the round); N2/N3/N4 are
coordinator designs from the same constraint set. Grok-4.7 was unavailable
(3 empty provider responses); diversity was constructed by mechanism sketch
instead.

Anti-bridge line (all four): at NO point may the engine construct typed
variables with scope, a well-formedness grammar distinguishing formulas from
terms, unification in the logic-programming sense, or a domain-independent
procedure over a formal syntax. Byte-span holes (regex-group-like captures)
are not semantic variables. Assigning spans to a fixed vocabulary of
meaning-bearing units is the bridge and is forbidden. Every derivation step
must cite byte-spans of input/store text or prior steps.

---

## N1 — NATIVE-ENTAIL (fable design)

Forward text-state rewriting via byte-pattern licenses.

- STATE: stack of TextStates (id, bytes, source, depth). Source ∈ {Input,
  KnowledgeCite(kid), Inference(rule_id, hole_map: (hole, span) list,
  premise_ids)}. States are independent byte blobs; no shared bindings.
- LICENSES: ~20 fixed byte-pattern idiom recognizers (MP-SHAPE:
  `from [A] and [A]=>[B], infer [B]`; CONTRA-SHAPE; UNIV-SHAPE; DEF-SHAPE;
  LEMMA-SHAPE: `if [C], then [Q]`; BICON-SHAPE; NEGATION-IDIOM; …).
  Each license = premise patterns (literals + holes + wildcards) +
  byte-equality constraints on holes + output template. Licenses are
  extracted from the NL knowledge text by matching the idiom shapes
  against the knowledge item bytes (e.g. the MP sub-license is cut out of
  K005's bytes between "modus ponens (" and "); proof by contradiction").
- STEP: match license premise patterns against stack states (byte matching,
  holes capture spans); check constraints; emit template with holes filled.
  Every hole in the output must be bound to a span from a premise.
- SEARCH: goal-skeleton-directed forward chaining. Extract goal skeleton
  from "Prove that [X]" → X bytes (+ negated form for contradiction).
  Iterative deepening to 100 steps; candidates ordered lexicographically
  by (license_id, sorted premise ids); goal-overlap scoring prioritizes
  candidates sharing byte spans with the goal skeleton. Deterministic.
- CONTRADICTION: overlap (shared span ≥4 bytes, not a stop-list word) +
  polarity (byte-pattern negative markers around the overlap). On
  contradiction, REFEREE defeats one state by quality score:
  Input=100 > KnowledgeCite=80−10×challenged > Inference=(min premise
  score − 2×depth); +15 per independent corroborating path; +5×uniqueness.
  Ties → deeper defeated → higher id defeated.
- HONESTY: withhold if no license matches; if holes ambiguous (>3 bindings);
  if conclusion asserts about an entity absent from premises; if depth>10
  with zero corroboration. Withholding is default; a step must be licensed.
- Full design: `/tmp/r3_fable_design.txt` (commit with round).

## N2 — NATIVE-DELIM (deliberative elimination, backward)

Backward propose-and-eliminate over raw text. Reasoning direction is the
opposite of N1: start from the goal, eliminate candidate conclusions that
cannot be supported.

- STATE: candidate set. Each candidate = (conclusion byte-span, support
  chain: list of links). A link = (conclusion-span, premise-span,
  link-pattern-id). Plus a shared cited-text pool (problem bytes + cited
  NL knowledge items).
- PROPOSE: from the goal skeleton ("Prove that [X]" → X), generate
  candidates: X itself; X with definition-expansion (replace a defined
  term by its definiens bytes from a cited definition); X negated (for
  refutation attempts). Bounded: ≤8 candidates, deterministic order.
- SUPPORT: for each candidate, build a support chain BACKWARD: find cited
  spans with byte-overlap (≥4 non-stop bytes) with the current span; a
  link is licensed by a small fixed set of SUPPORT patterns (byte-level:
  "X because Y", "since Y, X", "Y. Therefore X.", definitional
  containment: span A's bytes contain span B's key terms). Each link must
  bottom out in a cited span within ≤8 links.
- ELIMINATE (deliberative rounds, H5-style): round = score all candidates
  by (complete links / total links, citation quality); eliminate the
  weakest; repeat. A candidate is eliminated outright if any link
  contradicts a cited span (overlap+polarity as in N1) or requires a
  support step no pattern licenses.
- REFEREE: if two surviving candidates contradict, weigh by chain
  completeness then citation quality (cited text beats derived text).
- VERDICT: exactly one candidate with a complete chain → DERIVE (trace =
  chain reversed into forward order). Zero survivors → WITHHOLD.
- HONESTY: a candidate is never "completed" by inventing a link; links
  must match cited bytes. Ambiguous support (>3 possible premise spans
  for one link) → link marked weak; two weak links → candidate eliminated.
- DIFFERS FROM N1: backward vs forward; elimination of hypotheses vs
  rewriting of states; no output templates — conclusions are spans of
  existing text, never generated bytes.

## N3 — ONEBRAIN-NATIVE (shared-ledger parallel deliberation)

Parallel strategy threads over one shared ledger (Micah's one-brain
direction: one part's failure is instantly known to all).

- STATE: one shared LEDGER: append-only list of text states (id, bytes,
  source, depth, status ∈ {live, defeated}). Four STRATEGY THREADS, each
  with a fixed strategy program:
  - T-CONTRA: assume the negated goal skeleton; seek a contradiction
    against the ledger (prove by contradiction).
  - T-CONSTRUCT: forward-build from cited definitions (expand defined
    terms, apply definitional consequences).
  - T-LEMMA: apply conditional-shaped knowledge ("if [C], then [Q]")
    by byte-matching antecedents against the ledger.
  - T-GOAL: work backward from the goal skeleton seeking ledger states
    with byte-overlap, proposing bridging steps.
- STEP: deterministic round-robin — each live thread proposes exactly one
  step per round (in thread order). A proposal = (license-pattern similar
  to N1's idioms but SMALLER set: only the shapes each strategy needs;
  premise spans; output bytes). EVERY proposal is checked against the
  whole ledger for contradiction (overlap+polarity) BEFORE appending;
  contradicting proposals are refused and the proposing thread logs a
  strike.
- SHARED VISIBILITY: a contradiction or defeat entered by any thread is
  in the ledger all threads read next round. No thread re-proposes a
  defeated step (ledger carries defeat marks).
- STRATEGY ELIMINATION: a thread with 3 consecutive refused proposals
  has its strategy KILLED (logged, deliberate). A killed thread proposes
  nothing further.
- VERDICT: some thread appends a state byte-matching the goal skeleton
  (or its negation, for T-CONTRA deriving the negation → goal proved) →
  DERIVE with that thread's chain. All threads killed or step budget
  (100) exhausted → WITHHOLD.
- HONESTY: same as N1 (licensed steps only, holes bound, no invented
  bytes) plus: a thread may not cite another thread's defeated states.
- DIFFERS FROM N1/N2: parallelism + shared ledger + strategy elimination
  (not hypothesis elimination); contradictions are globally visible the
  round they are found.

## N4 — ANALOG-NATIVE (analogical case-based)

Reasoning by textual analogy: retrieve a similar solved problem, adapt
its trace by byte substitution, verify each adapted step.

- CASE LIBRARY (frozen before batteries are authored): 40 cases from
  round-1/round-2 PUBLIC traces only. Each case = (problem NL bytes,
  trace NL bytes) where trace NL is produced by a FROZEN DETERMINISTIC
  RENDERER: fixed NL templates per schema
  (S_MP → "From [P] and [if P then Q], we get [Q].";
   S_PBC → "Assume [not P]. [chain]. Contradiction. So [P].";
   S_UI → "For [x], [instance].").
  The renderer is mechanical (no intelligence); committed and auditable.
  NO R3 battery content may enter the library (sealed solutions are
  never on an engine input path).
- STATE: current problem bytes + retrieved cases (ranked) + working
  adapted trace.
- RETRIEVE: rank all 40 cases by deterministic byte similarity:
  4-gram byte multiset cosine, tie-broken by id. Top-3 cases tried in
  order. No RNG.
- ALIGN: byte-span alignment between current problem and case problem
  (longest common 4-gram chains, deterministic greedy). Produces a
  span-substitution map (case-span → current-span).
- ADAPT: walk the case trace steps in order; substitute spans via the
  map; VERIFY each adapted step against the NL knowledge store: the
  step's bytes must byte-match a knowledge item's inference shape
  (same idiom recognizers as N1, used ONLY as verifiers, never as
  generators). A step that fails verification is DROPPED (and all
  steps depending on it). If the surviving adapted chain reaches the
  goal skeleton → DERIVE. If all 3 cases fail → WITHHOLD.
- HONESTY: verification is strict byte-shape matching; dropped steps
  can only shrink the chain, never invent. Withholding is default.
- DIFFERS FROM N1/N2/N3: no rule application during search — the
  "reasoning" is retrieve+align+adapt; licenses only verify, never
  generate.

---

## Why these four are genuinely different (not reskins)

| | Search direction | What's eliminated | Role of licenses | Parallelism |
|---|---|---|---|---|
| N1 | forward from premises | defeated states | GENERATE steps | none |
| N2 | backward from goal | candidate conclusions | SUPPORT links only | none |
| N3 | mixed (per-thread) | strategies | generate (per-thread sets) | 4 threads, shared ledger |
| N4 | none (retrieval) | unverified adapted steps | VERIFY only | none |

## Rejected ideas (and why)

- "Learned rewrite rules from R1 traces": the rewrite rules would be
  learned NL→schema mappings in disguise — a bridge. Rejected.
- "Neural embedding similarity": not deterministic/byte-level; rejected.
- Single-engine-with-modes: modes are reskins, not architectures; rejected.
