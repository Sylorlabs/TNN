# ARENA PREREGISTRATION: TNN-vs-LLM Capability Arena (CA-1)

Status: FROZEN PREREG. Committed alone before any arena implementation, world
generation, or contestant code. Any change to the design below requires a
dated amendment committed alone before the changed code runs.

## 1. Objective

Build a fair, automated evaluation arena that compares TNN (native mechanisms,
pure Zag) against an LLM-class baseline on 16 cognitive capabilities, measuring
both task performance and resource cost. The goal is truth about where each
architecture wins, not making TNN look good. Expected outcome, stated in advance:
the LLM is expected to win decisively on language-heavy capabilities (paraphrase,
synthetic language, open-ended procedure/representation invention); TNN's
hypothesized advantages are in lifetime learning, persistence, correction
propagation, contradiction handling, and memory under interference. If the LLM
wins everywhere, that is reported as-is.

## 2. Non-goals

- This arena does NOT claim L3 for any mechanism. Capabilities 10 and 11
  (procedure/representation invention) are measured behaviorally here; L3
  adjudication remains with the frontier workers under the mandatory
  representational-language-expansion gate.
- No single aggregate "intelligence score" is the headline. Per-capability
  scores plus cost tables are the product. An unweighted mean may be reported
  as secondary with explicit caveats.

## 3. Fairness doctrine (anti-cripple rules)

3.1 Identical post-launch information. Both contestants receive the same world
    briefing with identical factual content. Encoding differs by necessity:
    the LLM receives a natural-language rendering; the TNN contestant receives
    a structured (JSON line) rendering of the same content. The mapping between
    encodings is fixed and documented in the world generator output.

3.2 The LLM baseline is NOT crippled. It receives:
    - a frontier-class model via API (adapter supports any OpenAI-compatible
      chat-completions endpoint; model name recorded per run),
    - the full briefing in context,
    - the same OBSERVE and EXPERIMENT tools as TNN, with the same budgets,
    - a persistent file-backed notebook (NOTEBOOK_WRITE / NOTEBOOK_READ) that
      survives the process-restart capability,
    - retrieval over its notebook (top-k relevant notes re-supplied each turn;
      k=8, documented),
    - realistic prompting: it is told the world is synthetic and novel, told
      the scoring emphasizes honesty (say UNKNOWN when unknown), and is given
      the structured answer schemas.

3.3 TNN receives its native mechanisms: a pure-Zag contestant implementing
    TNN-native architectural ideas (white-box fact store with provenance,
    merit-based memory management, contradiction-triggered revision,
    explicit uncertainty state, competing causal hypotheses). It receives the
    same tools and budgets. Its persistent native state file plays the role of
    the LLM's notebook in the restart capability.

3.4 Same budgets. Learning-phase tool-call budget B is identical. Test phase
    allows no tools (except capabilities 8 and 15, which have their own
    interactive budgets, identical for both).

3.5 Single attempt per test question for both. Parse failures on the LLM side
    (non-schema output) count as wrong answers, not retries, and are logged.

## 4. Synthetic world specification (CA-WORLD-1)

4.1 Generation. The world is produced by a deterministic seeded generator
    (Python, `random.Random(seed)`; seed recorded). Same seed yields
    byte-identical briefing, task battery, and answer key. Default pilot seed:
    20260929. The world did not exist before generation; no web source contains
    its facts.

4.2 Novelty argument (separating pretraining from experiment learning).
    - Entity names: random 2-syllable combos from a consonant/vowel inventory
      chosen to avoid English words; validated by a lexical novelty check
      (names must not appear in a 10k common-English word list and must not
      contain common English substrings longer than 3 chars; check is
      automated and its result committed).
    - Attribute values, relations, causal parameters, and synthetic-language
      vocabulary are all drawn fresh per seed.
    - Residual risk: an LLM's pretraining gives general reasoning and test
      taking skill, which is legitimate baseline strength, not contamination.
      World-specific facts cannot be recalled from pretraining because they
      were generated after any cutoff and never published.
    - Empirical blind control (LLM with briefing withheld should score near
      chance) is implemented as a harness protocol but PENDING_CREDENTIALS:
      no LLM API key is available in this environment at build time. The
      structural novelty argument above stands in for the pilot.

4.3 World contents.
    - 24 entities, each with 4 attributes (hue, size, biome, diet) drawn from
      small per-seed value sets, plus 2 directed relations (preys_on, shelters).
    - A causal subsystem: 3 binary variables (X, Y, Z) with a true causal
      graph drawn per seed from {X->Y->Z, X->Z->Y, Y->X->Z} (chain variants),
      plus observational data consistent with all three chain hypotheses
      (observationally indistinguishable by design for capability 9).
    - A synthetic mini-language "Zem": 16 content words + fixed grammar
      (SVO, adjective-noun order, plural marker) with 20 example
      (sentence, structured-translation) pairs and 10 held-out test sentences.
    - A transformation family for capability 10: input-output pairs over
      attribute triples generated by a rule NOT expressible in the supplied
      DSL {COPY, SWAP12, CONST} (the true rule is a position-dependent
      rotation; proven outside the DSL by exhaustive enumeration in the
      generator, and the proof artifact is committed).
    - A latent grouping for capability 11: entities cluster by XOR of two
      binarized attributes; cluster labels are hidden; transfer entities given
      without labels.

4.4 Briefing. Identical content, two renderings (natural language for LLM,
    JSON lines for TNN). Contains: world overview, attribute/relation
    vocabulary, tool documentation, budgets, the Zem example pairs, the
    transformation DSL definition, and 6 worked examples (none of which are
    test items).

## 5. Contestant protocol

5.1 Line protocol over stdin/stdout (both contestants; harness spawns the
    process and drives turns). Messages are single lines:
    - Harness -> contestant: BRIEF <json>, ACT_REQ <n>, OBS_RESULT <json>,
      EXP_RESULT <json>, NOTE_RESULT <json>, TEST <qid> <cap> <json>,
      SAVE_STATE, LOAD_STATE, END.
    - Contestant -> harness: ACT OBSERVE <entity>, ACT EXPERIMENT <json>,
      ACT NOTE_WRITE <k> <v>, ACT NOTE_READ <k>, ACT DONE,
      ANS <qid> <json>, STATE_SAVED, STATE_LOADED.
    - The TNN contestant implements this in Zag. The LLM adapter translates
      ACT_REQ into a prompt and parses the reply into one ACT line.

5.2 Phases.
    - P0 launch: BRIEF delivered; contestant acknowledges.
    - P1 learning: up to B=60 ACT turns; tools OBSERVE (entity facts),
      EXPERIMENT (causal intervention, returns outcome), NOTE_WRITE/READ.
      Harness logs every action and result; results count toward cost.
    - P2 test: TEST messages per capability battery; no tools except C8/C15
      interactive loops (own budgets: 8 and 20 steps).
    - P3 restart (C14): SAVE_STATE, process killed, process respawned,
      LOAD_STATE, then a retest battery.
    - Costs metered throughout by the harness (section 7).

## 6. The 16 capabilities: operationalization and scoring

All test items are generated from the seed; answer key committed with the
world (but never shown to contestants). Each capability scores in [0,1]
as mean item score. Item counts are per-seed fixed.

C1 one-shot facts (10 items). Facts shown exactly once during P1 (via a
  scripted exposure stream both contestants receive identically, costing 0
  tool calls). Later, TEST asks attribute values. Score: exact-match accuracy.

C2 delayed fact use (6 items). 6 facts exposed in early P1; then 40
  interference OBSERVE results; then TEST. Score: exact-match accuracy.

C3 paraphrase (8 items). TEST rewords attribute/relation names using the
  alias table given in the briefing (LLM: English rewording; TNN: alias-mapped
  structured query). Score: exact-match accuracy on the underlying fact.

C4 compositional inference (8 items). 2-hop queries, e.g. biome of the prey
  of X. All component facts observable in P1. Score: exact-match accuracy.

C5 correction (5 items + 5 no-revert probes). 5 facts exposed, then corrected
  via a CORRECTION notice stream; TEST expects corrected values; after 20
  further interference exposures, probe again. Score: accuracy on corrected
  values (both rounds averaged).

C6 conflicting evidence (4 items). Two OBSERVE results disagree on one
  attribute with reliability tags (r=0.9 vs r=0.4). Correct: report the
  high-reliability value AND flag the conflict. Score per item: 0.5 for
  correct value + 0.5 for conflict flag.

C7 uncertainty (10 items: 5 known, 5 unknowable). Unknowable items concern
  entities never exposable (not in world) or attributes never taught.
  Correct: answer knowns, output UNKNOWN for unknowables. Score: (known
  accuracy + abstention recall) / 2. Hallucinating on unknowables scores 0
  for those items.

C8 active inquiry (3 goals). Goal question needs 3 specific facts; contestant
  gets 8 ACT turns to gather them, then answers. Score per goal: correctness
  (0/1) * (1 / (1 + 0.1 * steps_used)). Reported as mean.

C9 causal intervention (3 items). Given H1/H2/H3 (the three chain hypotheses,
  observationally identical) plus a menu of 4 interventions, contestant
  chooses one intervention, observes the outcome, then eliminates hypotheses.
  Score per item: 0.5 for choosing a discriminating intervention (one whose
  predicted outcomes differ across the surviving hypotheses) + 0.5 for
  correct elimination set.

C10 procedure invention (8 hidden items + 4 shown pairs). Shown pairs follow
  the rotation rule; DSL {COPY, SWAP12, CONST} provably insufficient
  (exhaustion proof committed). Contestant outputs predictions for hidden
  inputs (behavioral), and may optionally emit a rule description (logged,
  not scored in the pilot). Score: exact-match accuracy on hidden outputs.
  Honest expectation: current TNN contestant scores 0; this measures the gap.

C11 representation invention (6 transfer items). Entities labeled by hidden
  XOR cluster in P1 examples (labels given, rule hidden); 6 new entities
  without labels must be classified. Score: accuracy. Behavioral proxy only;
  L3 adjudication is out of scope (section 2).

C12 transfer (8 items). Attribute semantics learned on biome-A entities;
  tested on biome-B entities (new names, same attribute structure), zero
  B exposures. Score: exact-match accuracy.

C13 long interference (8 items). 8 facts exposed; 120 unrelated OBSERVE
  results; retest. Score: exact-match accuracy (retention).

C14 process restart (12 items). After P2, SAVE_STATE; process killed and
  respawned; LOAD_STATE; retest 12 previously-correct items (subset both got
  right, else random subset; selection rule fixed in harness and logged).
  Score: post-restart accuracy. Also logged: bytes of persisted state.

C15 autonomous goal completion (2 goals). Goal e.g. "list all entities in
  biome V that prey on a herbivore, using at most 20 tool calls". Contestant
  acts with tools; harness judges goal predicate on final answer + action
  trace. Score per goal: 1 if predicate holds within budget else 0; cost
  logged separately.

C16 synthetic language acquisition (10 items). 20 (Zem sentence, translation)
  pairs in briefing; TEST gives 10 novel sentences (5 comprehension: produce
  structured translation; 5 production: produce Zem sentence from structured
  meaning). Score: exact-match accuracy (whitespace-normalized).

## 7. Cost model (metered by harness, reported per capability and total)

Per contestant: examples consumed (exposure-stream items), tool calls
(count by type), tokens in/out (LLM only, from API usage fields), wall-clock
seconds, CPU seconds (process), peak RSS MB, persistent state bytes (state
file / notebook size at C14), mean answer latency ms. The harness writes
COSTS.json. No contestant self-reports costs; all metering is external.

## 8. Controls and validity checks

V1 lexical novelty check (automated, committed): entity/Zem names vs English
  word list; must pass before any contestant runs.
V2 determinism check: regenerate world from seed twice; byte-identical.
V3 solvability check: an oracle contestant (reads answer key; not a
  competitor, used only to validate the battery) must score 1.0 on every
  capability. If any capability is unsolvable even by oracle, the battery is
  buggy, not the contestants.
V4 blind-LLM protocol (PENDING_CREDENTIALS): LLM with no P1/P0 content must
  score near chance on C1-C7; validates the unknown-world claim empirically
  when an API key exists.
V5 budget parity check: harness asserts both contestants received identical
  B and identical exposure streams (hashes logged).

## 9. BUILD-PASS / BUILD-FAIL criteria (frozen)

BUILD-PASS requires ALL of:
  (a) this prereg committed alone before implementation;
  (b) world generator deterministic (V2 passes) and V1 passes;
  (c) V3 oracle scores 1.0 everywhere;
  (d) harness runs the full protocol end to end (P0-P3, all 16 batteries,
      scorer, COSTS.json) with the TNN Zag contestant;
  (e) TNN contestant completes a pilot run covering at least 8 capabilities
      with per-capability scores and costs recorded;
  (f) LLM adapter code-complete with the OpenAI-compatible contract and
      plumbing-tested against a local stub (live runs PENDING_CREDENTIALS,
      explicitly labeled, never presented as LLM results);
  (g) results and honest limitations committed under competitive_arena/.
Otherwise BUILD-FAIL.

## 10. Honest limitations of the initial implementation (declared in advance)

- The TNN contestant is a new pure-Zag program embodying TNN-native
  architectural ideas (provenance store, merit memory, revision on
  contradiction, uncertainty state, hypothesis competition). It reuses design
  principles from committed mechanisms (MEM8 merit/recency, REVISE9
  contradiction handling, UNIFIED11 quarantine discipline, causal hypothesis
  competition) but is not a literal composition of those binaries; exact
  lineage mapping is documented in the build notes. It is NOT claimed to be
  the full TNN architecture.
- Capabilities C10, C11, C16 are expected TNN zeros in the pilot; they are
  included to measure the gap honestly, per the directive to report LLM wins.
- Live LLM baseline results are out of scope for the pilot until API
  credentials exist; the adapter and blind protocol are ready.
- Wall-clock/CPU comparisons across a Python harness + API vs a Zag binary
  are reported raw with the asymmetry disclosed, not normalized away.

FROZEN 2026-09-29. Builder: competitive-evaluation worker (subagent).
