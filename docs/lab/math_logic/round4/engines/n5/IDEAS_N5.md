# IDEAS_N5 — N5 CHAIN-NATIVE (n3-lineage scale-up) — FROZEN SPEC

Crew: MATH R4 engine N5. Parent: round coordinator. Date: 2026-09-25.
Prereg: `docs/lab/math_logic/round4/PREREG_MATH_R4.md` (frozen, commit
`84ed45077a554f9897ec55c2ca1430273c79eb69`, branch `tnn-native-lab`).
Lineage: n3 ONEBRAIN-NATIVE
(`docs/lab/math_logic/round3/engines/n3/n3.zag`, 1439 lines).

## 1. The diagnosis this spec attacks

R3 verdict §3 on n3: "the machinery works (derived a dev pigeonhole
end-to-end; ledger, strikes, strategy-kill all function) but on real
problems every thread exhausts budget (1/37 twins). A native that reasons
correctly small and dies on budget is a SCALING problem, not a wrong-idea
problem."

Reproduced 2026-09-25 by building n3 from frozen sources and running
T2_01 (a 4-step modus-ponens chain: alarm→guard→gates→vault→treasure):
**WITHHELD, BUDGET-EXHAUSTED after 25 rounds.** The ledger shows the
mechanism-level causes, not just the symptom:

- **D1. Premise blindness.** n3's conditional license (L5) and goal licenses
  (L7/L8) iterate only `src==1` (knowledge-store cites). The problem's OWN
  premises — where every twins/b5x/b6x inference lives — are a single
  opaque S0 blob. On T2_01 the four premise conditionals were never
  licensed once. Threads instead definition-expanded irrelevant KB cites
  (S38–S45: "addition and multiplication are commutative…" appended as
  "derivations" on a propositional problem). n3 could only ever fire on
  the KB, never on the problem.
- **D2. Round-robin budget burn.** 25 rounds × 4 threads = 100 thread-steps
  spent in fixed order 0..3 regardless of evidence. Threads with nothing to
  propose still consume rounds; the fixpoint detector only fires when NO
  thread proposes, so KB-noise proposals from D1 keep the loop alive until
  the budget dies.
- **D3. No compositional memory.** A derived fragment evaporates at run
  end. n3 re-derives nothing because it derives nothing, but the deeper
  gap: there is no lemma table — within a run (shared ledger is not an
  index) or across runs. R3 §6's surviving question ("what gives a native
  system COMPOSITION without reintroducing the formalizer?") is unanswered
  by n3.
- **D4. Brittle contradiction detector.** n3's detector (≥2 shared content
  words + negation-polarity flip) has no subject alignment: the TRUE chain
  step "56 is a multiple of 7." vs premise "8 is not a multiple of 7."
  (B5X_NL_L2_01) would be flagged contradictory (flip on "multiple"/"7")
  although the claims are about different entities (56 vs 8). It also
  ignores numerals entirely (words <3 bytes are dropped), so quantitative
  corruptions ("at least 2" vs "exactly one") are invisible.

N5 keeps what n3 proved (shared ledger, licensed steps, contradiction
adjudication, discharge/PBC, strikes, strategy-kill, 3× byte-identical
reruns, zero RNG) and fixes D1–D4.

## 2. N5 architecture

One shared append-only LEDGER (n3's 20-field states: offset, len, src,
kid, lic, p1..p3, depth, status, thread, round, taint, spares) plus three
strategy threads (n3's four, with CONSTRUCT+LEMMA merged — they were the
same license family split by src filter, and the src filter is abolished):

- **T0 CONTRA** — assume the negated goal skeleton; expand/apply licenses
  over premise/cite states; contradiction-driven discharge and PBC (unchanged
  semantics from n3).
- **T1 FORWARD** — all forward licenses over ALL live asserted states
  (premise-sentences, cites, derived): conditional-MP, definition
  expansion, iff-elimination, universal instantiation, disjunctive
  syllogism.
- **T2 GOAL** — backward: definition splice into goal, subgoal
  plant/close, plus lemma-cache firing (cross-problem lemmas).

### 2.1 Premise ingestion (fixes D1)

S0 remains the whole problem text (id 0, src INPUT). Additionally every
premise sentence (split on `.`/`?`/`!` boundaries) becomes a first-class
ledger state with **src=PREMISE (6)**, depth 0, citable by every license.
Conditional-shaped and definition-shaped premise sentences are licensed
exactly like cites. Bullet prefixes ("- ") are stripped at the byte level
(the span starts after the prefix; the prefix bytes are not part of the
claim — same honesty posture as n3's TARGET joiner).

### 2.2 License set (byte spans only; no typed vars/scope/unification)

- **L-MP** (extends n3 L5): conditional-shaped state C ("if <A>, then <Q>"
  / "if <A> then <Q>" / "if <A>, <Q>", n3's byte parser kept) + asserted
  states covering every " and "-conjunct of <A> by **word-inclusion**
  (conjunct's content words ⊆ state's content words, polarity-aware:
  a negated conjunct needs a negated asserter) → append <Q> bytes.
  Word-inclusion replaces n3's substring match: it is relation-keyed, not
  surface-keyed (paraphrase posture §5).
- **L-DEF** (n3 L3): "HEAD: body" definition expansion over all states.
- **L-IFF** (n3 L4): " iff " forward elimination.
- **L-UNIV** (new): universal instantiation over byte shapes —
  "Every <A> is a/an <B>", "Every <A> is <B>", "Every <A> <VP>",
  "Every <A> that <VP1> <VP2>", "Everyone/Everything who|that <VP1> <VP2>",
  "Everything <PP> <VP>" — plus instance states ("X is a <A>",
  predicate-words(X) ⊇/⊆ content(<A>) either direction on the smaller
  set). Output "<X> <VP>". Verb detection inside <A> is the byte
  heuristic "first word ending in s (len>2)" after U1a/U1b disambiguation.
  No lexicon beyond the closed-class lists (§2.4).
- **L-DS** (new): disjunctive syllogism — "… <L> or <R> …" + asserted
  state denying <L> (polarity-flipped coverage) → append <R> bytes.
- **L-CACHE** (new): cross-problem lemma firing (see §3).
- T0/T2 keep n3's contra-assume / goal-defsplice / goal-lemmasub /
  goal-close with the src filter widened to premise states.

### 2.3 Contradiction detector v2 + strike-based rule discipline (fixes D4; B5X posture)

A proposal P contradicts a live asserted state S iff ALL hold:

1. **Shared vocabulary**: ≥2 shared content words, where content words
   now INCLUDE numerals of any length (n3 dropped them; B5X corruptions
   are quantitative) and light stemming (trailing-s strip on words >3
   chars, so "letter"/"letters" align — a byte rule, not a lexicon).
2. **Flip**: some shared word has flipped negation-scope status (n3's
   rule, kept) **OR quantity mismatch**: the two states share the same
   verb + object noun-stem frame (or the same non-numeral content-word
   set) with DIFFERENT numerals, **and at least one side is asserted**
   (src ∈ {INPUT, PREMISE, CITE}). Derived-vs-derived numeral
   differences are NEVER contradictions — a counter legitimately reads
   1 then 2; only a derived claim against asserted truth is a conflict.
   (Without the asserted-side requirement, B6X's own chain "advances to
   1" vs "advances to 2" would self-destruct at step 2; without the
   same-frame requirement, "120 miles in 2 hours" vs "60 miles per
   hour" would false-fire.)
3. **Subject alignment**: the flipped word lies in the subject word-set
   of at least one side, or the two subject sets overlap. Subject =
   content words before the first auxiliary
   ("is/are/was/were/be/does/did/has/have/do") or before "=";
   existential "There is…" subjects resolve to the associate NP.
   (Blocks the L2_01 false positive — flipped "multiple"/"7" is in
   neither subject {56} nor {8} — while keeping L2_05's "0 divides 19"
   vs "There is no integer c with 19 = 0 x c": flipped 0 ∈ consequent
   subject {0}.)

**Rule discipline** (revised after fable adversarial review — no instant
global taint): when a proposal is REFUSED for contradiction, its
licensing rule-state takes a STRIKE (n3's 3-strikes → SUSPECT/killed
machinery, extended from threads to rule-states). No instant taint, no
premise quarantine, no cross-rule cascade: a true rule on an
inconsistent-premise problem (B6X_NL_CONTRADICTION's R100) takes one
strike and survives; a false rule that keeps contradicting trusted
bytes is killed after 3. The REFUSAL itself blocks the false step —
false chains are linear and each (rule, premises) pair fires at most
once (used-pair guard), so one refusal breaks the chain. This is N5's
native discriminator for B5X-NL: on Kind-D the false chain's first
contradicting step is refused while the true chain (base rules present
in the injected store) proceeds → DERIVED; on Kind-W the only path to
the target runs through the false rule → WITHHELD. No oracle: every
refusal is driven by contradictions against asserted problem/store
bytes. Known residual (N7's territory): a false chain whose outputs
never contradict any asserted byte (pure semantic corruption with no
negation/quantity flip) will not be blocked — reported honestly if
observed. (This is N5's contribution to discrimination; N7 goes further
per prereg. Honest expectation: N5 should at least not regress vs n3's
24/60 universal-withhold, and should convert D-problems to DERIVED.)

### 2.4 Fixed vocabularies (closed-class only, as n3)

n3's stop-word list + negation-marker list are kept. Added: auxiliaries
(is/are/was/were/be/being/been/does/did/has/have/do) for subject
extraction, and the pronouns it/they/them/its/their for §4. No content
lexicon. No NL→schema map anywhere (audited per prereg §7.1).

### 2.5 Thread prioritization + dormancy (fixes D2)

- **Credit**: per thread, +2 per appended proposal, −1 per refusal,
  −1 per dup-skip (floor 0); +3 goal-heat bonus when an appended state's
  content words newly overlap the goal's by ≥2. Each round, live threads
  are ordered by (credit DESC, thread id ASC) — deterministic, derived
  only from the ledger's own evidence. No oracle.
- **Dormancy**: a thread whose propose() returns 0 (no candidate) in 2
  consecutive rounds sleeps until the next append wakes all sleepers.
  Threads that cannot fire stop consuming budget instead of spinning.
- **Termination**: fixpoint when a full round passes with all threads
  dormant or proposing nothing AND no append occurred; budget backstop
  max_rounds = 4×depth_bound + 20 (primary 52; B6X 532). WITHHOLD on
  fixpoint/budget/all-killed, as n3.
- **Depth bound**: state depth = 1 + max premise depth; proposals
  exceeding the bound are not made. Bound from argv (default 8 =
  prereg primary bound; harness passes 128 for B6X-NL, 160 for
  CHAIN50-NL later).

## 3. Lemma caching (fixes D3)

- **Within a run**: the shared ledger is the working set; additionally a
  lemma INDEX keyed by sorted content-word signature → state id, so
  T1/T2 match antecedents against derived fragments in O(index) rather
  than O(ledger) — the compositional memory n3 lacked at the mechanism
  level.
- **Across problems**: single-premise licensed steps (L-MP 1-conjunct,
  L-UNIV, L-DS) with fully grounded, non-tainted premises are cached as
  (antecedent-bytes, consequent-bytes, origin-problem-id) lines in
  `lemma_cache.txt` (sorted by antecedent signature, cap 256, earliest
  kept — deterministic). At run start the cache loads as a cited store;
  L-CACHE fires an entry iff its antecedent's content words are covered
  by current asserted bytes (polarity-aware), citing the cache-file
  byte-span + origin id in the trace. Cache writes go to
  `<cache>.new` per run; the harness merges between problems only after
  3 byte-identical runs (so the 3× determinism assertion is never broken
  by cross-problem state).
- **Safety**: a cached consequent that contradicts asserted states is
  refused and the entry is marked bad (same adjudication as live
  proposals). Cache hits are genuine re-derivations against current
  bytes, not answer smuggling: the fragment was derived by licensed
  steps before, and re-matches now.

## 4. Paraphrase hard gate posture (prereg §7.3, from day one)

- All matching is **word-inclusion over lowercased content words**
  (stop-words excluded, negation-aware), never byte-exact sentence
  equality and never fixed surface templates. A meaning-preserving
  rewording re-fires the same licenses on the new bytes because the
  licenses key on relations (shared content words, polarity, quantity),
  not on the bytes' shape.
- **Goal satisfaction is coverage, not string equality**: DERIVE iff a
  live derived (src=prop, non-defeated) state covers the goal's content
  words with matching polarity. n3 required case-insensitive byte
  equality — surface-keyed, the exact failure mode that voided n1's
  credibility in R3.
- **Pronoun tolerance**: it/they/them/its/their in a derived state may
  cover an uncovered goal word W iff W is a content word appearing in
  the SAME sentence before the pronoun in the step's source bytes (e.g.
  T4_09: "Every living thing that needs water wilts without it."
  covers goal "…without water" because "water" precedes "it" in the
  same sentence). The referent must be in the bytes — never invented;
  the same-sentence restriction blocks antecedent hijacking across
  sentence boundaries.
- **Self-test**: before any bar claim, N5 runs the 12 R3 sealed audit
  variants (paraphrase + nonce) and must show zero verdict flips vs the
  base items; the R4 PARA-INV battery runs only after the seal commit,
  per protocol.

## 5. What N5 is NOT (honest boundaries)

- **No numeral-alignment bridging.** B6X_NL renders each formal atom with
  two inconsistent surfaces ("it advances to N" vs "the counter stands
  at N" / "the gauge reads N"); the chain stalls at step 1 for any
  byte-faithful engine. Learning the text's own numeral convention is a
  real idea (documented for a future crew) but building it now would be
  a B6X-shaped hack; N5 attempts B6X and reports the stall with the
  mechanism reason. B6X is carryover, not a primary bar.
- **No ex falso.** On B6X_NL_CONTRADICTION the chain derives "the alarm
  is armed", contradicting the premise "It is not the case that the
  alarm is armed" — logged as CONTRADICTION-FOUND, verdict WITHHELD.
  Classical explosion to the arbitrary target ("The system must be
  reset") is not implemented: it would be unsound under any accidental
  contradiction and would wreck B5X discrimination.
- **No deep-math licenses.** R3N items needing induction (K001),
  multi-premise algebraic rewriting (R3N_01/03/06: "let n=2k, then
  n²=4k²=2(2k²)"), or geometric construction (R3N_07/08) are out of
  reach; N5 targets the compositional core (chaining licensed steps to
  the goal), which is R4's question. Expected: beat n3's 8/24 R3N via
  Euclid's-lemma+DS (R3N_02), definition/conditional chains, and honest
  withholds on the 8 gullibility traps — not full R3N coverage.

## 6. Audit posture (prereg §7.1–7.2)

Every derivation step cites byte-spans of input/store/cache/prior-step
bytes; the LEDGER section of the output records (src, kid, lic,
premises, depth, status) per state as n3 did, plus SUSPECT flags and
cache citations. No typed variables, no scope, no unification, no
formal syntax, no NL→schema translation step — the build will be
audited for disguised-formalizer patterns (a paraphrase that preserves
meaning must move the cited spans, §7.2; coverage-based matching
guarantees this structurally).

## 7. Why these ideas (and not others)

- Premise-first licensing is the minimal repair of the proven mechanism:
  n3's licenses were correct in shape but blind to the only text that
  mattered. Alternatives (bigger budgets, more threads) were rejected:
  on T2_01 n3 had 100 thread-steps for a 4-step chain and used none of
  them on the premises — the bottleneck was never budget size.
- Credit-ordered scheduling with dormancy is the evidence-driven
  prioritization the task asks for: "which threads deserve budget" is
  decided by appends/refusals in the ledger, visible to all threads
  (one-brain), with zero oracle input.
- The lemma cache is the compositional memory: n3's threads shared a
  ledger but could not REUSE a derived fragment as a unit — every
  match re-scanned raw states, and nothing survived the run. Caching
  single-premise fragments as (antecedent, consequent) byte pairs is
  the smallest unit that is still a genuine lemma.
- Detector v2 + strike discipline is the cheapest honest discriminator:
  B5X's false rules are designed to contradict trusted bytes mid-chain,
  so a contradiction checker that understands subjects and numerals
  already discriminates — no separate veracity oracle needed. Strikes
  (not instant taint) keep inconsistent-premise problems like
  B6X_NL_CONTRADICTION from cascading.
- Coverage-based goal matching + pronoun tolerance is the paraphrase
  defense built into the verdict condition itself, not bolted on.

## 8. Build plan

Pure Zag, zero RNG, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Single file `n5.zag` forked from frozen n3 sources (kept: byte helpers,
word tables, ledger, adjudication skeleton, contra/PBC, 3× rerun
harness, sealed guard, output format with `ENGINE: n5`). New: premise
splitter, L-UNIV, L-DS, word-inclusion matcher, detector v2,
suspect-taint, credit scheduler, dormancy, lemma index + cache
load/stage, pronoun-tolerant goal coverage, depth-bound argv.
CLI: `n5_bin <problem> <out> [store] [cache] [depthbound]`.
Tests: R3 carryover only (r3n, twins, b5x_nl, b6x_nl) + R3 sealed audit
variants (paraphrase self-test); 3× byte-identical reruns per problem
(in-process, asserted, exit 5 on divergence). New R4 batteries
(CHAIN-NL/CHAIN50-NL/PARA-INV) NOT run until the seal commit is handed
over. One build commit after green carryover tests.

## 9. Falsification criteria for N5 (self-imposed)

- If N5 does not beat n3's twins score (1/37) by ≥10×, the premise-first
  repair failed and the design is wrong, not the budget.
- If any B5X Kind-D problem that n3 withheld is still withheld for a
  reason other than a documented detector gap, the strike/refusal
  discriminator misfires.
- If the R3 audit-variant self-test shows any verdict flip, N5 is
  paraphrase-void by its own gate and does not proceed to bar claims.
- If cross-problem cache hits ever fire on bytes that do not cover the
  cached antecedent, the cache is answer-smuggling and gets deleted.
