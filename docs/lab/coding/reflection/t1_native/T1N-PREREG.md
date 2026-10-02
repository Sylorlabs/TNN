## AMENDMENT A1 (2026-09-22, pre-deliberation — no measurement has run)

1. `t1n_gen` signature is `fn t1n_gen(cx:[]u8, goal:[]u8, demo:[]u8)void`.
   Rationale: the battery's `demo` field carries the test inputs (T1/T2
   demo calls, T4x embedded values); the original driver protocol passes
   `gen <spec> <store> <demo>`, so the invented architecture must receive
   it. The wrapper passes the driver's demo verbatim. No bar changes.
2. Two repair probes added to §3.5 (deliberation evidence for the invented
   revision policy; they do not leak T3 items):
   - PR1: seed `fn main()void {\n  _zag_print("hi");\n};\n` → expect `hi\n`
     (tests `};` repair).
   - PR2: seed `fn main()void {\n  let x:i64=5;\n  _zag_print(_zag_i64_to_str(y));\n  _zag_print("\\n");\n}\n`
     → expect `5\n` (tests unknown-identifier repair).
   Probes are never scored; they are deliberation evidence only.

---

# TASK 1 RERUN (T1N) — TNN-NATIVE INVENTION — Preregistration (FROZEN 2026-09-22)

**Order:** Micah 2026-09-22 — "For task 1 everything should've been TNN not
the tnn using the crew. TNN can use its own internal crew which is same brain
multiple agents so I want a better test on that for these tests first teach
it knowledge too maybe it's the lack of knowledge."

**Why a rerun:** the completed Task 1 (2026-09-22) passed KB-R1/R2/R3 with
INFORMED 58/58 vs baseline 50/58, but its honest caveat was fatal to the
"invention" claim: the eight construct schemas, trigger words, and
entry-ID bindings were CREW-AUTHORED fixed learner code. That was
deliberation OVER taught knowledge, not de-novo invention. This rerun tests
whether TNN itself — via its own internal one-brain crew — can invent the
architecture from taught knowledge.

**Status:** FROZEN. Any change to the boundary (§1), arms (§2), deliberation
(§3), bars (§5–§6), or measurement (§7) needs a dated amendment with Micah's
re-approval. This file is committed alone before the first deliberation run.

**Standing law:** pure Zag, zero RNG in any decision path, deterministic,
byte-identical reruns (5 reps). Pinned toolchain: `znc_linux_x86_64_abed8aa1`.
Nothing epistemic hardcoded as fact. The coding engine's knowledge store is
the manipulated variable, and only that.

## 1. THE INVENTION BOUNDARY (crew vs TNN) — the load-bearing section

### 1.1 What "TNN-native" means

"TNN" in this trial = the one-brain deliberation system (§3): sub-deliberations
(proposer, critic, composer, diagnoser) sharing ONE ledger/state, all
architectural decisions recorded as episodes citing taught knowledge.
"Crew" = the outer builders (agents) who write the deliberation MACHINERY,
the harness, tests, oracles, and the taught store.

### 1.2 Crew-authored (allowed) — invention MACHINERY, not architecture

The crew may author ONLY:
- (a) the deliberation loop: episode sequencing, the shared ledger, episode
      recording, deterministic termination (§3.4);
- (b) generic text/code operations: substring search, line split/join, brace
      matching, identifier/keyword extraction, keyword-overlap scoring with
      fixed tie-breaks — all content-free, no coding-architecture vocabulary;
- (c) the generated module's INTERFACE (function signatures, §4.1) — a
      contract, not architecture;
- (d) the harness/driver (decision-free plumbing, §7.2), the probe tasks
      (§3.5), the oracles, the 58-item battery (frozen, reused from Task 1);
- (e) the taught store: the 69-entry coding KB + (informed arm) the 12
      prior-art records — knowledge, not architecture.

### 1.3 TNN-invented (required) — ARCHITECTURE content

The following must be produced by TNN's deliberation, with every element
citing deliberation episodes and taught entries (bar IV-P1, §6):
- (i) the mechanism inventory: which code-generation mechanisms exist;
- (ii) each mechanism's trigger keywords and emitter code;
- (iii) the selection rule: how a goal maps to a mechanism;
- (iv) the revision policy: what happens on compile/test failure;
- (v) the composition rules: how goal parameters fill emitter slots.

### 1.4 Automatic FAIL conditions (invention claim)

- Any element of (i)–(v) whose text matches crew-authored content (engine,
  driver, or harness sources): checked by the provenance audit (§6.1).
- Any element of (i)–(v) lacking a deliberation-episode citation, or citing
  a non-existent episode, or citing a non-taught entry: checked by §6.1.
- The deliberation trace missing required episode types for any invented
  element: checked by §6.2.
- The engine source containing architecture content per the frozen
  forbidden-vocabulary audit (§6.3).

### 1.5 What the deliberation MAY do (explicitly permitted invention)

- ADOPT taught programs as mechanism implementations, provided the DECISION
  to adopt (which program, for which mechanism, with what triggers, and why)
  is TNN's recorded deliberation citing the taught entry. Adoption is
  assembly-by-deliberation, not crew authorship.
- SYNTHESIZE novel emitters by deliberated recombination of taught code
  blocks (block = brace-matched unit of a taught program), guided by the
  mechanism record's described steps and validated by compile+run evidence.
- DERIVE triggers, selection rules, and revision policy from taught records
  and probe evidence, recording ≥2 considered alternatives for the selection
  rule and the revision policy (§6.2).

## 2. ARMS (identical machinery, different knowledge)

- **ARM INFORMED:** 69-entry coding KB + the FROZEN 12 prior-art records
  (C-ARCH-01..12, `task1/corpus/records.txt`, sha256 frozen at teach time).
  Records C-ARCH-02..09 describe eight mechanism families; C-ARCH-01/10/11/12
  describe meta-level deliberation knowledge (composition, revision,
  plan-before-emit, provenance).
- **ARM FROM-SCRATCH:** 69-entry coding KB ONLY. No prior-art records.
- **Teach-first:** both arms install the KB via the existing installer with
  audit BEFORE any deliberation; informed additionally installs the corpus
  with audit. The deliberation engine records the sha256 of every taught
  file it reads. Store control: the scratch arm's read-set must exclude the
  corpus (any corpus read in the scratch trace voids the arm comparison).
- **Arm difference:** ONLY the taught prior-art records. The deliberation
  machinery, probes, budget, and battery are identical.

## 3. THE ONE-BRAIN DELIBERATION

### 3.1 Roles (Micah's "same brain, multiple agents")

Four sub-deliberations on ONE shared ledger (all episodes visible to all
roles; one role's failure is instantly visible to the others):
- **PROPOSER:** proposes mechanism candidates (adopt or synthesize), each
  with: name, trigger keywords (subset of cited records' K: fields),
  emitter code, source citations (taught entry IDs), and reasons quoting
  the cited records.
- **CRITIC:** checks each candidate: citations resolve to taught entries;
  trigger keywords ⊆ union of cited K: fields; emitter code contains the
  cited records' code-tokens (record-fidelity); candidate distinct from
  accepted ones. ACCEPT/REJECT with recorded reasons.
- **COMPOSER:** writes accepted candidates into the architecture module
  draft behind the fixed interface (§4.1), with provenance comments.
- **DIAGNOSER:** compiles each candidate (via the driver, §7.2), smoke-runs
  it, runs the probe tasks through the composed module, records pass/fail
  with VERBATIM evidence. Failures return to PROPOSER with the evidence.

No manager-and-staff separation: there is no outer agent writing
architecture. The outer crew writes only §1.2 machinery.

### 3.2 Deliberation phases (engine modes)

1. `propose`: PROPOSER emits candidates for basic mechanisms (from EMIT
   templates, ALGO entries, IDIOMs) and — informed arm only — novel
   mechanisms (from C-ARCH-02..09). Writes candidates + compile queue.
2. Driver compiles the queue (plumbing only).
3. `critique`: CRITIC accepts/rejects; PROPOSER revises failures (≤3 rounds
   per novel mechanism, ≤1 round per basic mechanism). Writes new queue if
   revising.
4. `compose`: COMPOSER writes the module draft `t1n_arch.zag`.
5. `validate`: the module solves the 6 probe tasks (§3.5); driver
   compiles+runs; DIAGNOSER records.
6. `diagnose`: probe failures → limited revision (≤1 extra round) or
   recorded as known gaps.
7. `freeze`: the deliberation trace is frozen (sha256) BEFORE any battery
   measurement. Post-freeze edits void the trial.

### 3.3 Episode record (the trace IS the deliverable)

Every episode: `EP <id> <role> <phase> <cites:entry-ids> <input-hash>
<decision> <reasons-text>`. The trace must show, for EVERY invented element
(mechanism, trigger set, selection rule, revision policy, composition rule):
≥1 PROPOSE + ≥1 CRITIQUE + ≥1 COMPOSE + ≥1 DIAGNOSE episode. For the
selection rule and revision policy: ≥2 alternatives proposed with a
recorded comparison on probe evidence.

### 3.4 Budget and termination (deterministic)

- ≤3 propose→critique rounds per novel mechanism; ≤1 per basic mechanism.
- ≤120 znc compilations during invention per arm.
- ≤1 validate→diagnose revision round.
- Termination is by fixed round counts, never by wall-clock or convergence
  heuristics. All scoring integer; ties → lowest index. Zero RNG.

### 3.5 Probe tasks (frozen; crew-authored TESTS, not architecture)

Six basic goals, distinct from the 58-item battery and from all T4x
families. They validate the pipeline and teach the goal format (structured
`T1|...` specs; natural-language GOAL specs with embedded numbers):

- P1: `T1|PRINT|name=hello|op=print_const|text=hi` → stdout `hi\n`
- P2: `T4|GOAL|print the sum of the integers from 1 to 10` → `55\n`
- P3: `T1|STR|name=nbytes|op=count_bytes` with argv `hello` → `5\n`
- P4: `T4|GOAL|print the first command-line argument reversed` argv `abc` → `cba\n`
- P5: `T4|GOAL|print the largest of the integers 3 7 2` → `7\n`
- P6: `T4|GOAL|print the factorial of 10 computed with a loop` → `3628800\n`

P6 is deliberately ITERATIVE so it does not leak the recursive solution
(C-ARCH-02 / t4x_01). Probes are never scored; they are deliberation
evidence only.

## 4. THE GENERATED ARCHITECTURE

### 4.1 Fixed interface (crew-authored contract)

```zag
// T1N architecture module — generated by TNN deliberation (see TRACE).
// Every function below cites deliberation episodes + taught entries.
fn t1n_gate(cx:[]u8, goal:[]u8)void   // emit "ALLOW" or "REFUSE:<reason>"
fn t1n_gen(cx:[]u8, goal:[]u8, demo:[]u8)void
                                     // emit a complete Zag program, or "UNKNOWN_GOAL"
fn t1n_diag(cx:[]u8, goal:[]u8, demo:[]u8, evtype:[]u8, evidence:[]u8)void
                                     // emit "DIAG ..." + revised source, or "halt-<reason>"
```

### 4.2 Content requirements

- `t1n_gate`: consults the G-RULES entry's trigger terms (extracted at
  invention time, episode-cited); REFUSE cites the entry.
- `t1n_gen`: applies the invented selection rule; on no match emits
  `UNKNOWN_GOAL` (honest halt — never guesses).
- `t1n_diag`: applies the invented revision policy: on compile/test
  failure, ONE deliberated revision attempt (e.g. next-ranked base recorded
  at invention), then `halt-<reason>`. Blind retry of the identical
  emission is forbidden (stall guard: byte-identical revision stops).
- A thin crew-authored wrapper exposes gate/gen/diag as a CLI protocol for
  the battery driver; the wrapper makes NO decisions (static audit, §7.2).

## 5. "BETTER" BARS (carried from Task 1, vs the pinned baseline)

Baseline: `coding/src/learner.zag` (sha256
`b7e74d1ebe6af2dd7b7863b77d2953a51637dd30b3158420b667d1ef0e74d9ef`),
measured: T1 10/10, T2 8/8, T3 10/10 final, T4 12/12, T4m 4/4, T4x 0/8,
T5 6/6 refused; total 50/58.

| Bar | Rule |
|---|---|
| **KB-R1** | Challenger ≥ baseline on EVERY tier (T1,T2,T3-final,T4,T4m,T4x,T5) AND strictly better on ≥1 tier. Any tier below → claim KILLED. |
| **KB-R2** | At equal-or-better mastery: mean iters ≤75% baseline, OR znc ≤50%, OR store entries ≤50%. Measured on T3+T4+T4x. |
| **KB-R3** | PRIMARY: challenger ≥6/8 T4x first-attempt with baseline ≤2/8 (baseline measured 0/8 — primary applies). |

Kill bars RK1–RK5 carry over: RK1 any tier below baseline kills; RK2 gate
weakening/concealment = critical FAIL; RK3 any of 5 reps not byte-identical
(trace text, module, builds, verdicts, digests) = FAIL; RK4 any coding or
architectural decision in the driver/wrapper (not the deliberation or the
generated module) = trial VOID; RK5 trace omits a rejected alternative
present in the episode log, or any post-freeze edit = finding void
(integrity failure).

## 6. INVENTION BARS (new in T1N)

| Bar | Rule |
|---|---|
| **IV-P0** | Static audit of the deliberation ENGINE source (frozen forbidden list,
  `t1_native/audits/FORBIDDEN.md`): no T4x/probe solution code, no
  `em_f_*` names, no hardcoded trigger lists, no schema-name-indexed
  tables. Run BEFORE the first deliberation; any hit = trial VOID. |
| **IV-P1** | Provenance: EVERY generated-module element (each emitter fn, trigger
  set, selection rule, revision policy, composition rule, gate) carries a
  comment citing ≥1 episode ID + ≥1 taught entry ID. Automated check:
  (a) all cited episodes exist in the frozen trace; (b) all cited entries
  exist in the taught read-set; (c) no element shares a contiguous 200+
  char substring with any crew-authored source (engine/driver/wrapper).
  Any failure = invention claim FAIL (reported; the mastery numbers stand
  as a separate finding). |
| **IV-P2** | Deliberation completeness: the frozen trace shows for EVERY invented
  element ≥1 PROPOSE + ≥1 CRITIQUE + ≥1 COMPOSE + ≥1 DIAGNOSE episode;
  for the selection rule and revision policy ≥2 considered alternatives
  with a recorded probe-evidence comparison. Missing = FAIL. |

## 7. MEASUREMENT

### 7.1 Order (enforced by the driver)

teach → IV-P0 audit → deliberate (propose→…→freeze) → IV-P1/IV-P2 checks
→ build generated module + wrapper → Phase-2 battery (58 items, same
driver protocol as Task 1) → 5-rep byte-identical canonical logs →
bar table. The T4x battery is first read in Phase 2; the deliberation
never sees it (driver asserts: no `t4x.json` read before freeze).

### 7.2 Driver discipline (extends RK4)

The invention driver is deterministic plumbing ONLY: it compiles the
engine's queues, runs binaries, and records rc/stdout/stderr VERBATIM. It
makes NO decision: no branch on the CONTENT of compiler output, test
output, or candidate code (branching on file existence / queue emptiness
is orchestration, allowed). Static audit (grep) of the driver + wrapper
verifies this before the first run; the audit script is frozen here.

### 7.3 Honest-failure clause (carried)

An incoherent proposal, a module that never compiles, invented emitters
that underperform the crew-authored schemas, or a failed KB-R1..R3 is a
REPORTED FINDING about TNN-native invention capability, not a failure to
hide. In particular: if TNN's invented architecture scores BELOW the
original Task 1 numbers (informed 58/58, scratch 55/58), report the numbers
plainly — that bounds what "teach knowledge first" buys. The deliberation
trace is itself the deliverable: every proposal, the deliberation that
produced it, rejected alternatives and why, each build attempt and its
evidence.

### 7.4 Comparison (descriptive, not bars)

Report rerun-informed vs baseline (bars §5), rerun-informed vs original
Task-1 informed (58/58), rerun-scratch vs original Task-1 scratch (55/58),
and the arm gap. The original used crew-authored schemas, so the original
numbers are a REFERENCE, not a bar — matching or beating them with
TNN-invented architecture is the question, not the requirement.

## 8. DELIVERABLES

- This frozen prereg (committed alone).
- The deliberation engine source (pure Zag) + IV-P0 audit result.
- The frozen deliberation trace per arm (sha256) + TEACH-AUDIT per arm.
- The generated architecture module per arm (`t1n_arch.zag`) + IV-P1/IV-P2
  check results.
- Phase-2 canonical logs (5 reps/arm), bar table (KB-R1/R2/R3, RK1–RK5,
  IV-P0/P1/P2), and the honest comparison (§7.4).
- Commit under `docs/lab/coding/reflection/t1_native/` (lab-relative
  paths), verify via GitHub API, report head SHA.
