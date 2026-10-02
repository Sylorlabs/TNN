# FROZEN PREREG: Arena Procedure Lane (genuine procedure invention via TCNP)

Status: FROZEN PREREG. Written before any implementation. Any change to the
design below requires a dated amendment written before the changed code runs.
This file is committed by the coordinator alone, before any implementation
source exists, so prereg commit order is verifiable from git history
(prereg commit timestamp strictly precedes any implementation commit
timestamp; UNVERIFIABLE ORDERING voids this prereg).

Date: 2026-10-01 PDT
Worker: ARENA lane worker, wave-20261001-2021pdt (phase 1: prereg only)
Parent state: v6 candidate 0.794 (54/68) CONFIRMED [RE-CERT]; canonical clean
score stays 0.573; zero on inquiry, causal, procedure, transfer, goal,
language (see NAMECHECK.md Step 1 for the re-derived map).

## 1. What "procedure" means here, and why a new battery is needed

The sealed 16-capability battery's C10 items are operationally identical to
the C16 zemprod morphology items (world_gen.zag line 514; established in
PREREG_LANGUAGE_AMEND1.md). The CA-1 prereg text described C10 as a
rotation-rule procedure battery with a DSL exhaustion proof; that battery
was never implemented. Consequence: no sealed battery in the repo tests
genuine procedure invention. The v6 C10 score is a language-mechanism
artifact, not procedure evidence.

This prereg therefore defines BOTH a new learner mechanism AND the sealed
test protocol that will measure it. The sealed worlds are designed
post-freeze by an independent adversary (section 5); the rule family is
held out from this prereg (the prereg fixes the protocol, the generic op
set, and the battery structure, but no rule, no values, no names, no seeds).

This is a CANDIDATE capability demonstration, arena-side. It is not an L3
claim, not a TNN-2 substrate claim, and does not move the canonical 0.573.
No TNN-beats-LLM claim is permitted (the LLM baseline is pending; no
credential, no spend authorized; the baseline must never be crippled).

## 2. Why procedure is the highest-information zero capability

1. It connects to the F1 frontier and the TNN-3 H1 hypothesis on named
   procedures: a procedure win arena-side is the strongest cross-lane
   evidence for that hypothesis family.
2. Procedure invention requires constructing novel executable structure from
   experience (the closest behavioral proxy to structural learning in the
   arena), strictly harder than the pattern-fitting that suffices
   elsewhere. A genuine win here is the strongest single evidence the arena
   can produce this wave.
3. The frozen TNN-2 mechanisms M1/M2 failed on procedure and inquiry
   abstraction, so the field is open: a win must come from a genuinely new
   learner mechanism, which is exactly what this prereg designs (section 3).
   This lane does substrate repair nowhere; TNN3H5/TNN3H1 test substrate
   hypotheses in parallel. No patch treadmill: one mechanism, frozen bars,
   adversary-designed worlds.
4. Measurement gap: inquiry (C8) and causal (C9) at least have sealed
   batteries that return honest zeros; genuine procedure has no valid
   battery at all. Building the battery plus the mechanism yields the most
   information per unit of work.

## 3. Mechanism: TCNP (trial-constructed named procedures)

### 3.1 Learner-owned structures (all in learner state, none in source)

- Procedure table: up to 8 named procedures. Each entry: name (byte
  string), step count, step list (each step: op id plus operand indices),
  creation trace (task id, number of candidates tried, minimal length
  found, count of minimal fitters, rebound flag).
- Trial log: per task, the count of candidates tested and the winning
  candidate index in canonical enumeration order.
- Per-item verdict records: for each hidden item, answer or UNKNOWN plus
  the fitter agreement count.

The procedures themselves (the intelligence) live only in learner state.
Source contains only generic machinery (section 3.2) plus the fixed
protocol handlers (section 3.4).

### 3.2 Frozen generic op set (machinery, not intelligence)

Eight domain-neutral ops over a vector register file. Vectors have length
4, elements are integers 0..7. Ops:

1. COPY(d, s): v[d] = v[s], d, s in 0..3, d != s (12 variants)
2. SWAP(a, b): exchange v[a], v[b], a < b (6 variants)
3. ROTL: rotate left by 1 (1 variant)
4. ROTR: rotate right by 1 (1 variant)
5. REVERSE: reverse element order (1 variant)
6. INC(i): v[i] = (v[i] + 1) mod 8 (4 variants)
7. DEC(i): v[i] = (v[i] - 1) mod 8 (4 variants)
8. SET0(i): v[i] = 0 (4 variants)

33 single-step variants total. Every op is a generic computational
primitive of the kind the protected-core ISA ruling allows (comparable to
MOVE/INC/DEC machinery). No op encodes any target-domain regularity: there
is no rotate-by-hidden-constant, no detect-pattern, no apply-rule op. The
op set is published in this prereg and frozen; the adversary knows it
(knowing the ISA is legitimate, like knowing the CPU); the sealed part is
which composition the worlds use.

### 3.3 Algorithm (deterministic; zero randomness in decision paths)

For each task (a set of shown pairs sharing a task id):

1. Rebind attempt: test each tabled procedure against ALL shown pairs by
   simulation. If one reproduces every shown output, rebind it to this
   task: zero new search trials, trace records rebound name. (This is the
   named-procedure reuse path; the D world tests it, and the mechanism is
   never told which world reuses which rule.)
2. Trial construction (only if no rebind): enumerate candidate step
   sequences in canonical order: length 1, then 2, 3, 4 (bound K = 4);
   within a length, lexicographic over (op id, operands). Simulate each
   candidate on all shown inputs. Find the minimal length L* (1..4) with
   at least one candidate reproducing all shown outputs. Collect ALL
   length-L* candidates that fit (full enumeration at that length, not
   first-only). Store the canonical-first as the named procedure with its
   trace; keep the full fitter set for consensus.
3. Hidden items: simulate every L*-fitter on the hidden input. If all
   fitters agree on the output, reply "w0,w1,w2,w3" (no spaces). If they
   disagree, reply "UNKNOWN" (learner-originated uncertainty guiding
   abstention, not a guess). If step 2 found no fitter at any length up to
   4, record a no-procedure trace and reply "UNKNOWN" to all hidden items
   of that task.

The K = 4 bound is an explicit, stated simplicity prior (Occam), not a
claim about the world. Enumeration is exhaustive within the bound, so for
any rule expressible in at most 4 generic steps the search necessarily
finds fitters; consensus abstention handles underdetermination honestly.

Distinction from the killed M1 path-follower (required by task): M1
followed demonstrated paths. TCNP never sees a demonstrated path: it sees
only input/output pairs and constructs the path by trial over generic
machinery. M1 had no abstention and no named persistent procedures; TCNP
has both. This is construct-and-apply (an approved frontier), not
path-following.

### 3.4 Event protocol (fixed interface; rules remain sealed)

- Expo: {"t":"pshow","task":"<id>","in":[v0,v1,v2,v3],"out":[w0,w1,w2,w3]}
- Test: {"t":"ptest","task":"<id>","in":[v0,v1,v2,v3]}
- Reply to ptest: "w0,w1,w2,w3" or "UNKNOWN".

Handlers dispatch on event type only (pshow/ptest), exactly as the v6
zemprod/zemclass handlers dispatch on question type; answers are computed
solely from learner state (procedure table, fitter sets). No
benchmark-specific logic: the handlers carry arbitrary vectors and contain
no rule-specific branches.

## 4. Sealed battery structure (protocol fixed here; worlds sealed)

Five worlds, adversary-designed post-freeze:

- Worlds A, B, C: novel rules, each a composition of at most 4 ops from
  the section 3.2 set. Each world: 4 shown pairs, 6 hidden items.
- World D (reuse): the abstract rule is identical to world A's rule, with
  fresh surface values and fresh names. 4 shown pairs, 6 hidden items. The
  D-to-A linkage is NOT revealed to the mechanism; reuse must be
  discovered via the procedure table.
- World E (honesty probe): the rule requires more than 4 generic steps
  (adversary composes 6 or more, or uses an op outside the set such as
  element-wise multiplication). 4 shown pairs, 6 hidden items. Honest
  behavior is abstention, not confident wrong answers.

Total scored: 24 hidden items (A through D) plus 6 honesty probes (E).
The adversary ensures hidden inputs are novel (absent from shown pairs)
and not near-duplicates of shown inputs (so the memorization control in
K7 is meaningful).

## 5. Adversary air-gap protocol

1. After this prereg is committed (coordinator commits it alone), the
   coordinator assigns an independent adversary worker (a different lane;
   no shared implementation source).
2. The adversary designs the five worlds from THIS PREREG ONLY. The
   adversary never sees the implementation source. The builder never sees
   the worlds, the answer keys, the rule descriptions, or the seeds.
3. The coordinator mediates every run: the coordinator holds the sealed
   world files, invokes the frozen contestant binary on them, and reports
   scores (and only scores, plus pass/fail per bar) back to the builder.
4. The adversary writes a sealed attestation file recording, per world:
   design timestamp (must be strictly after the prereg commit timestamp),
   the rule in sealed form, and a statement that the rule appears in no
   builder-visible material (dev logs, fixtures, prior wave lanes,
   practice worlds).
5. Builder self-testing during implementation uses ONLY builder-generated
   practice worlds in /tmp. Practice worlds are contaminated by
   construction, are documented as such, and never count toward any bar.
   All bars run on adversary-sealed worlds via the coordinator.

## 6. Scoring rule

Per hidden item: 1 if the reply string exactly equals the answer key
entry, else 0. Abstentions ("UNKNOWN") score 0 on that item (never
negative). Capability score: mean over the 24 A-D hidden items. Honesty
score: mean abstention rate over the 6 E items (an exact correct answer on
E, should one occur by coincidental fit, counts as non-abstain but is
tracked separately in the wrong-answer count).

## 7. Frozen kill bars

K1 (procedure construction): hidden-item exact-match accuracy on worlds
  A-D >= 18/24 (0.750). Target 24/24. The 6-item allowance covers honest
  consensus abstentions under underdetermination. Below 18/24: FAIL.

K2 (honest uncertainty): on world E, (correct + abstain) >= 5/6, i.e. at
  most 1 confident wrong answer in 6. A confident wrong answer is a reply
  that is neither the key nor "UNKNOWN". Violation: FAIL.

K3 (named-procedure reuse): on world D, (a) the white-box trace shows the
  task rebound an existing tabled procedure with 0 new search trials
  (reuse flag set to a procedure name created during world A), and
  (b) D hidden accuracy >= 5/6. If D is solved only via fresh search, or
  accuracy is below 5/6: FAIL (reuse was not demonstrated).

K4 (no regression): the existing 68-item sealed arena (seed
  71503461337030) run with the new contestant binary produces
  per-capability scores byte-identical to the v6 refreeze baseline
  (54/68 = 0.794 with the identical per-capability distribution). The new
  pshow/ptest event types do not occur in that battery, so any deviation
  means the mechanism disturbed existing behavior. Deviation: FAIL.

K5 (composition-free contamination check): ALL of the following must hold.
  (a) Ordering: the prereg commit timestamp strictly precedes the
  adversary's per-world design timestamps (coordinator verifies from git
  history and the sealed attestation; UNVERIFIABLE ORDERING voids the
  prereg). (b) Air gap: the builder never opened any adversary world,
  key, or rule file (coordinator attests; access is mediated). (c) Grep
  audit: the mechanism source contains zero adversary-world-specific
  strings (the coordinator runs the audit against the sealed worlds; the
  only shared vocabulary permitted is the protocol keywords pshow/ptest,
  the op names, and integer literals). (d) Novelty: the adversary certifies
  that every hidden input is absent from all shown pairs and from every
  builder-visible file (dev logs, fixtures, prior waves, practice
  worlds). (e) Generality probe: after the sealed runs, the coordinator
  runs the FROZEN binary once on one additional fresh adversary world
  (new rule, new seed, same protocol); the builder sees only the score.
  Probe hidden accuracy >= 4/6. Below 4/6: FAIL (overfit to the five
  battery worlds). Any sub-part violated: FAIL.

K6 (determinism): 3/3 full battery runs (all five worlds) produce
  identical per-world scores and byte-identical reply streams after
  stripping the ms and rss_kb timing fields (the same exclusion class as
  the v6 K6 bar). The mechanism contains no RNG; candidate enumeration
  order is canonical and fixed. Any nondeterminism: FAIL.

K7 (negative controls): (a) Ablation: a binary with procedure
  construction disabled (falls back to "UNKNOWN" on every ptest) scores
  0/24 on worlds A-D. Above 0: FAIL. (b) Memorization control: a
  nearest-shown-pair lookup (reply with the output of the shown pair
  whose input has minimal Hamming distance) scores <= 6/24 on worlds
  A-D. Above 6/24: FAIL (the battery is solvable by memorization, so it
  does not test construction). Controls run on the same sealed worlds via
  the coordinator.

K8 (pure Zag): zero Python in any program, glue, analysis, verifier, or
  harness in this lane; zero em-dash bytes in lane docs. Bash only
  sequences process invocations. Any Python invocation: PROCESS-FAIL
  (reported honestly; the wave is void for this lane).

K9 (architecture): zero new modes, bridges, routers, or task-specific
  admission gates; zero hardcoded semantic cases (the 8 ops are generic
  machinery, each justified in section 3.2; none encodes a target-domain
  regularity); handlers dispatch on event type only. Architecture
  accounting is recorded in the result doc: cognition source lines added,
  new hardcoded semantic cases (must be 0), new modes/bridges/routers
  (must be 0), learner-state structures created (procedure table, trial
  log, verdict records). Violation: FAIL. Capability-source delta target:
  near zero; the capability (the procedures) must live in learner state,
  with source contributing only the generic constructor.

BUILD-PASS requires K1 through K9 all PASS. Any FAIL is BUILD-FAIL.
A positive result is a CANDIDATE score only.

## 8. Honest boundaries

- This prereg claims no L3 representational invention: the op set is
  researcher-supplied machinery (a tiny ISA), and the search bound K = 4
  is a researcher-set prior. What is learner-owned is which procedure is
  constructed, its persistence as a named structure, its reuse, and the
  abstention behavior. That is strong L2-adjacent evidence if the bars
  pass, not an L3 claim.
- Arena-side only: a pass says nothing about TNN-2's substrate. It is
  candidate evidence for the F1/TNN-3 H1 named-procedure direction, to be
  weighed alongside the TNN3H5/TNN3H1 substrate lanes, not a substitute
  for them.
- The 8-op set may prove too weak for richer procedures; world E exists
  precisely to keep that limitation visible instead of hidden.
- No TNN-beats-LLM claim is made or implied. The LLM baseline is pending
  (no credential, no spend authorized).
- A positive result does not move the canonical 0.573; only a clean
  refreeze reproducing composition without contamination can do that.

FROZEN 2026-10-01 PDT. Implementation begins only after the coordinator
commits this file alone.
