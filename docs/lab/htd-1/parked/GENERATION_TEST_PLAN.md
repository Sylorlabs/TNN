# HTD-1 Parked Generation Track — Runnable Test Plan

**Status: PARKED / SUSPENDED.** Written by crew P1 (parked-plan polish) on 2026-09-21.
**Purpose:** turn the generation-slice debate output into a test plan that can start
the day the suspension lifts. No hypotheses are built here; nothing here is an
architecture commitment.

**Why suspended:** KB-HTD-1.2 fires — no units section champions exist, and emission
order / step cost / parallelism are atom-relative properties (frozen prereg §1, §4).
KB-HTD-1.1's verdict at freeze: test not executable (no settled arm outputs exist);
the firing test is preserved verbatim in §2 of this plan and executes when arm
outputs exist. G-CO2, G-CO3 (narrowed to output-gating, atom-agnostic), and G-CM1
proceed under the frozen prereg and are NOT covered by this plan.

**Provenance of every bar in this document:** transcribed from the three debate
briefs (`debate/gen-autoreg.md`, `debate/gen-parallel.md`,
`debate/gen-compositional.md`) and verified by grep — 18 K-bar lines in
gen-autoreg.md (4 + 5 + 4 + 5), 16 KB-bar lines in gen-parallel.md (4 × 4), 17
KB-bar lines in gen-compositional.md (5 + 4 + 4 + 4). Battery definitions from
`debate/metrics-spec.md` (DEBATE-PHASE DRAFT — not yet frozen; the frozen prereg §3e
says the metrics spec proceeds and the referee crew freezes the closed-form cost
model per KB-HTD-1.5/1.6 before any efficiency build; battery numbers below stand as
the parked plan's working definitions pending that freeze + Micah's approval).
KB-HTD-1.x definitions from `debate/redteam.md` §3 and frozen prereg §1. Dual
anchoring + slice legs from the draft prereg §5 (`prereg/HTD1_PREREG_DRAFT.md`;
kept verbatim because the frozen prereg points at them).

**Bar-semantics convention (frozen prereg §2):** hard-kill (KB/KILL-labeled) =
terminal, binding. Fail (K/FAIL-labeled) = documented, one re-entry. NOTE: the
G-AR* briefs write their bars as "FAILS" (fail semantics: documented, one re-entry
per §2); the G-PA* and G-CO* briefs write theirs as "→ KILL" (hard-kill: terminal).
The G-AR* bars are the weaker tripwire class; the briefs mean that literally.

**Determinism gate (program law, applies to every run below):** every scored run
executes 5 times (R=5); all scored artifacts byte-identical across all 5 runs
(SHA-256 of concatenated artifact bytes, computed by the harness, not self-reported);
logged state = (a) memory store after memorization, (b) deliberation ledger/audit
trail, (c) arm config (weights, taxonomy version, probe manifests), snapshotted by
the harness and restored before each run. Any byte difference across the 5 runs
INVALIDATES the run set (not a score, not a FAIL). Two consecutive invalid run sets
= hypothesis BLOCKED pending Micah's review (not killed — nondeterminism is an
implementation defect). G-PA1 KB4, G-CO1 KB5 are determinism restatements, not
independent bars.

---

## §1. Hypothesis registry with kill bars

### G-AR1 — Deliberative Chunk Commit (DCC)

Every emitted chunk passes through the commit/refuse/rollback machinery TNN already
uses for memory — generation *is* deliberate commitment. (Source:
debate/gen-autoreg.md, "HYPOTHESIS G-AR1".)

KILL BARS (preregistrable on HOSR, 200 trials):
- **K1 (cost):** FAILS if median per-chunk wall time > 3× G-GREEDY **and** fidelity
  gain < 5 percentage points over greedy. Deliberation must pay for itself.
- **K2 (starvation):** FAILS if refuse rate > 25% of proposals. A generator that
  rejects a quarter of its own proposals is not generating.
- **K3 (theater):** FAILS if refuse rate < 1% **and** fidelity < 95%. Zero refusal
  with imperfect fidelity means the gate never fires when it should.
- **K4 (provenance):** FAILS if citation validity < 99% on committed chunks. A
  committed chunk without a ledger trail is a fabrication channel.

### G-AR2 — Span-Tape Emission with Verification Gates (STVG)

Planner lays variable-length spans onto a tape fast; an independent verification
gate (not the planner) decides whether each span is fixed. (Source:
debate/gen-autoreg.md, "HYPOTHESIS G-AR2".)

- **K1 (gate quality):** FAILS if gate false-reject rate > 10% measured on spans
  that byte-match the original (rejecting correct output is a broken gate).
- **K2 (planner quality):** FAILS if first-pass span acceptance < 85% on clean
  memory (the planner is proposing junk and the gate is doing the real work —
  then it's not a two-stage system, it's a slow one-stage one).
- **K3 (escalation abuse):** FAILS if > 10% of spans go through ESCALATE, or any
  span remains unresolved at final pass (holes must close; an unclosed tape is
  not output).
- **K4 (sparsity honesty):** FAILS if median woken partitions ≥ 80% of total
  partitions. If everything is awake, the free-lunch claim is false.
- **K5 (net win):** FAILS if total wall time ≥ G-AR1 on HOSR with fidelity ≤ G-AR1.
  Two stages must beat one deliberate stage or the split is unjustified.

### G-AR3 — Eliminative Next-Unit Selection (ENUS)

Propose a small deterministic candidate set (3–7, state-driven, no sampling) and
*eliminate* until one survives. Selection by survival, not by scoring. (Source:
debate/gen-autoreg.md, "HYPOTHESIS G-AR3".)

- **K1 (discrimination):** FAILS if elimination changes the winner vs the
  greedy single-guess in < 2% of steps. Machinery that never changes the outcome
  is dead weight.
- **K2 (convergence):** FAILS if no-survivor rollback fires on > 10% of steps.
  Constant rollback means the candidate generator and the eliminator disagree
  about reality.
- **K3 (degeneracy):** FAILS if > 20% of rounds have all-identical candidates or
  if > 15% of rounds end with ≥2 survivors after all rules (indiscriminate rules).
- **K4 (cost):** FAILS if median per-step wall time > 4× G-GREEDY with fidelity
  gain < 5pp. Candidate generation + elimination is the most expensive per-step
  design here; it must show its work in fidelity.

### G-AR4 — Cheap Cascade with Checkpoint Backtrack (C3B)

Generate fast and cheap through a minimal path; verify only at checkpoints
(m=8, preregistered); on failure roll back to the checkpoint and regenerate that
segment through the expensive deliberate path. Deliberation is the exception, not
the rule. (Source: debate/gen-autoreg.md, "HYPOTHESIS G-AR4".)

- **K1 (the efficiency bar — load-bearing):** FAILS if total wall-clock ≥ G-AR1
  (always-deliberate) on HOSR. If the cascade isn't cheaper than deliberating
  everywhere, it has no reason to exist.
- **K2 (fidelity parity):** FAILS if fidelity < G-AR1 fidelity − 3pp. Cheap must
  not mean wrong; the cascade buys speed, not sloppiness.
- **K3 (cascade stability):** FAILS if > 5% of checkpoints trigger backtrack, or
  any backtrack spans more than one checkpoint (multi-checkpoint rollback =
  the verifier is catching errors too late; the interval is wrong or the fast
  path is broken).
- **K4 (verifier blindness):** FAILS if a planted-error probe (10% of trials get
  a deliberately corrupted fast-path unit injected by the harness) is caught by
  the checkpoint verifier < 95% of the time. A verifier that can't catch known
  errors proves nothing.
- **K5 (slow-path share):** FAILS if > 30% of units end up emitted via the slow
  path. Past that point you're just running G-AR1 with extra bookkeeping.

### G-PA1 — "Flag-and-Fix": full skeleton draft + deliberative region refinement

One native pass emits a complete fixed-length skeleton draft (structural
constraints only); a rule-based verifier sweep flags defective regions with typed
defect codes; each flagged region is fixed through commit/refuse/rollback; stops
when a sweep flags zero regions, flag count fails to strictly decrease across two
sweeps (stagnation → item FAIL), or hard cap P passes; oscillation guard halts if
the same region is committed >K times (`OSCILLATED`). (Source:
debate/gen-parallel.md, "Hypothesis G-PA1".)

KILL BARS (any one firing kills the hypothesis):
- **KB1 (quality):** masked-span reconstruction exact-match rate < 85% on the
  pg100 proxy at the fixed budget → KILL.
- **KB2 (convergence):** >5% of items need >5 sweeps, OR any item oscillates
  (same region committed >3 times) → KILL.
- **KB3 (efficiency):** mean cells-touched-per-output-byte ≥ 0.8× the
  autoregressive slice's on the same items → KILL (loses the 20W question).
- **KB4 (determinism):** any two reruns from the same logged state differ by
  even one byte → KILL (violates program law; no appeal).

Falsifiable predictions (carried as progress signals, not bars): P1 ≥90% of items
converge in ≤3 sweeps with strictly decreasing flag counts; P2 total cells touched
grows sublinearly with draft length, beating the AR slice's linear pass cost on long
drafts; P3 stagnation halt fires on <5% of items and partial output remains
structurally valid.

### G-PA2 — "Blank-filling fixpoint": masked tape refined to convergence by rule

Tape starts all-blanks except prompt-anchored pre-filled cells; each pass is a
parallel full-tape fill by a deterministic local rule (cell neighborhood + intent
record); verifier re-blanks cells violating constraints; fixpoint = zero-change
pass AND zero verifier violations; hard cap P; stagnation and per-cell re-blank
caps → FAIL. (Source: debate/gen-parallel.md, "Hypothesis G-PA2".)

- **KB1 (quality):** exact-match reconstruction rate < 85% on the same pg100
  proxy → KILL.
- **KB2 (convergence):** <90% of items reach true fixpoint (zero-change pass)
  within P=8 passes, OR any cell re-blanked >3 times → KILL.
- **KB3 (efficiency):** mean total cell-writes per output byte ≥ 2× the
  autoregressive slice's cell-writes → KILL (parallel passes must not just burn
  the whole tape every round).
- **KB4 (ledger proportionality):** ledger bytes per output byte > 10× on the
  median item → KILL (a mechanism whose audit trail dwarfs its output fails
  TNN's replay economics).

Predictions: P1 fixpoint reached (not capped) on ≥95% of items; P2 wall-clock
advantage grows with tape length vs sequential generation; P3 ≥70% of re-blanks
within 8 bytes of an anchor or a previously violated cell.

### G-PA3 — "Eliminative drafts": parallel multi-hypothesis drafting with eliminative selection

N complete candidate drafts (N=4 fixed in prereg) from different deterministic
drafting policies, in parallel; eliminative battery — a candidate dies when it
fails a challenge no survivor has failed (genuine discriminating evidence);
survivors get one deliberative repair pass per round; stop at one survivor, or
zero-elimination + zero-repair round (tie-break by fixed deterministic rank:
fewest verifier flags, then lowest tape offset of first flag, then policy index),
or rounds > R=6; zero survivors in a round → item FAIL. (Source:
debate/gen-parallel.md, "Hypothesis G-PA3".)

- **KB1 (quality):** winner exact-match rate < 88% on the pg100 proxy → KILL
  (must beat single-policy baselines to justify N× work).
- **KB2 (selection value):** winner correctness − best-single-policy
  correctness < 3 points → KILL (if selection adds nothing, the machinery is
  theater).
- **KB3 (convergence):** >10% of items reach the round cap R=6 without a
  single survivor, OR >20% resolved by tie-break rather than elimination
  → KILL.
- **KB4 (efficiency):** total cell-writes across all N drafts + rounds > 4×
  the autoregressive slice's → KILL (parallel hypotheses must pay for
  themselves; ties directly to the 20W question).

Predictions: P1 winner correctness > max individual policy correctness by ≥5
points; P2 ≥80% of items resolve by genuine elimination; P3 losing drafts
eliminated for cited, checkable reasons in ≥95% of elimination events.

### G-PA4 — "Frozen checkpoints": coarse-to-fine passes with level freezing

Fixed preregistered levels: L1 coarse outline (1 marker byte per 32 output
bytes), L2 mid-resolution spans, L3 full byte resolution; certified levels are
FROZEN (later passes may not alter them outside the repair path); repair confined
to the failing level, max Q repairs per level; terminates at L3 certification,
Q exhaustion, or `BUDGET_FAULT` (frozen level's budget unsatisfiable). (Source:
debate/gen-parallel.md, "Hypothesis G-PA4".)

- **KB1 (quality):** exact-match reconstruction < 85% on the shared pg100
  proxy → KILL.
- **KB2 (hierarchy value):** L1 outlines certified on first attempt < 70% of
  items → KILL (if the coarse level can't plan, the hierarchy is decoration).
- **KB3 (frozen-level fault):** any freeze violation (a later pass altering
  frozen bytes outside the repair path), OR budget-fault rate > 5% → KILL.
- **KB4 (repair confinement):** >15% of items need repairs at ≥2 levels
  (defects cascade across levels instead of localizing) → KILL — the hierarchy
  fails its one job.

Predictions: P1 ≥70% of L3 repairs confined to span interiors with zero marker
movement; P2 budget faults <3% of items; P3 total acts scale with defect count,
not output length.

### G-CO1 — "Deliberate skeleton, constrained fill"

Prompt → task record (fixed rule-based extractor, version pinned); candidate
skeletons from a fixed generator set, eliminative selection (budget sums ≤ B,
every hard constraint assigned to ≥1 region, dependency graph acyclic), scored by
a fixed deterministic scorer, winner COMMITTED as `skeleton_commit`; regions filled
by deliberate recall-and-assembly in deterministic dependency order (one region's
fill may read the skeleton and its dependencies' committed fills, nothing else);
weave + mechanical verification; violating region rolled back, max 2 retries, then
item FAILs. (Source: debate/gen-compositional.md, "Hypothesis G-CO1".)

- **KB1 (quality floor):** exact-match on PROSE-REC < 80% → KILL.
- **KB2 (cost distribution — where the cost goes):** planning-phase ops (parse
  + skeleton deliberation + weave verification) must be ≤ 50% of total
  generation ops on the median item; if > 60% while quality sits below the
  autoregressive baseline → KILL. The claim is that deliberation is *cheap
  relative to what it organizes*; if planning eats the budget, the skeleton is
  overhead, not leverage.
- **KB3 (expected failure mode — skeleton/output mismatch):**
  committed-constraint violation rate in final output, after the 2-retry
  budget, must be < 10%; if ≥ 20% of items ship with ≥1 violated *committed*
  constraint → KILL. A skeleton the output ignores is decoration.
- **KB4 (hierarchy value):** skeletons surviving to output unchanged must be
  ≥ 60% of items; if < 40% (the skeleton is rewritten more often than kept)
  → KILL.
- **KB5 (determinism):** any byte divergence across reruns from the same
  logged state → disqualification (program law, not a kill bar — no appeal).

Predictions: P1 items with zero region rollbacks beat items with ≥1 rollback by
≥15 points of exact-match; P2 reverse-dependency-order fill ablation changes zero
output bytes (any change = hidden cross-region coupling, invalidates the
parallelism claim); P3 ops scale with region count, sublinearly with output length
at fixed region count.

### G-CO4 — "Deliberative templates" (schema-first slot filling)

A small library (≤12 templates, prereg cap) of pre-committed structural templates:
named slot list + per-slot schema + cross-slot constraints; selection by
deterministic precondition checklist (no-template-passing → explicit ledgered
`TEMPLATE_MISFIT`; force-fitting a failing template is a fault); slots filled in
dependency order via recall + constrained assembly, schema failure → re-fill max 2
retries, then `TEMPLATE_MISFIT`; mechanical cross-slot verification. (Source:
debate/gen-compositional.md, "Hypothesis G-CO4".)

- **KB1 (quality):** exact-match on CODE-REC < 80% → KILL.
- **KB2 (cost distribution — the reuse claim):** median per-run ops must be
  ≤ 65% of G-CO1's median per-run ops on identical items; if templates cost as
  much as designing a skeleton from scratch → KILL.
- **KB3 (expected failure mode — schema violation):** final outputs violating
  their committed slot schema must be < 5% of items; ≥ 15% → KILL. A template
  the output can't honor is a lie the system tells itself.
- **KB4 (fit honesty):** on the misfit probe set (100 prompts from a held-out
  genre with no covering template), force-fit rate — emitting under a template
  whose preconditions failed — must be 0%; > 10% → KILL. Companion cap: if the
  build needs > 12 templates to cover the two proxy genres → KILL (prereg cap;
  a bigger library is a different hypothesis).

Predictions: P1 within-genre template reuse ≥ 80%; P2 ≥ 60% of item FAILs are
cross-slot constraint violations, not intra-slot schema failures; P3 median
per-run ops ≤ 70% of G-CO1's median on identical items.

**Ambiguities flagged (source-level, not transcription errors):**
- G-CO2 KB2 contains an internal gap: "recall + selection must be ≥ 50% of total
  ops AND mechanical assembly ≤ 20%; if assembly ops exceed 30% of total →
  KILL." Between 20% and 30% assembly share, neither the must-condition nor the
  kill fires. The referee crew should close this (20% vs 30%) at prereg freeze,
  or Micah amends by dated amendment.
- G-AR* bars are labeled "FAILS" (fail semantics per frozen prereg §2:
  documented, one re-entry) while G-PA*/G-CO* bars are "→ KILL" (terminal).
  This asymmetry is in the debate briefs themselves, not an artifact here.
- G-CO1 KB2 has a compound trigger: >60% planning share kills ONLY "while
  quality sits below the autoregressive baseline." If planning share is 70% but
  quality beats AR, the bar does not fire. Carry that qualifier into the build
  prereg.

---

## §2. KB-HTD-1.1 firing test — exact executable procedure

Verbatim bar (redteam.md §3, adopted in frozen prereg §1): the debate phase must
produce at least one proxy generation task whose definition does not depend on
the choice among the 53 arms' atom ontologies.

### Procedure (executes when settled arm outputs exist)

**Step 0 — Preconditions.** At least three materially different arm families from
the units program have produced settled, committed outputs (e.g., episodic-chunk
atoms, deliberation-trace atoms, signed-value atoms — the families named in the
red-team brief; substitute the actual settled families the units program
delivered). The referee crew has frozen the units' champion atom definitions and
their verifiable independence/granularity properties.

**Step 1 — Select the top two candidate proxy tasks.** From this parked plan's
battery (§3 below): the canonical Proxy A/B/C and the three slice extension legs
are the candidate pool. The referee crew ranks them by atom-independence (which
task's measurement definition leans least on the atom ontology) and takes the top
two. Ranking criteria, preregistered: (a) does the task's measurement definition
reference atom-internal structure (yes = worse); (b) does the scoring function
change meaning if atoms are coarse vs fine (yes = worse); (c) can the task's
"unit" be bound to any settled atom family without rewording the task (yes =
better). The ranking and its criteria are committed before Step 2.

**Step 2 — Re-run each task's measurement definition across ≥3 materially
different arm families.** For each of the two selected tasks: bind the task's
"unit"/"span"/"chunk" to each arm family's settled atoms, with no other change to
the task definition. Run the same minimal generation-strategy set on each binding
(the strategies are the surviving parked hypotheses or the referee's reduced set:
at minimum the section-representative sequential, parallel, and structure-first
strategies plus G-GREEDY/B-G1/B-G2 baselines).

**Step 3 — Void/flip criterion.** For *either* task, the bar FAILS if, in ≥1 arm
family:
- (a) the measurement is **voided** — the task cannot be scored as defined (e.g.,
  the atom family has no meaningful order for an order-sensitive task; the span
  reconstruction has no referent; the composition instruction is unexpressible),
  OR
- (b) the **rank-ordering of generation strategies flips** — the winner by the
  task's primary metric changes relative to the other families' bindings.

**Step 4 — Verdict.**
- If neither (a) nor (b) fires on either task: KB-HTD-1.1 PASSES — the two tasks
  are atom-independent enough to score the generation track, and the track may
  proceed on those tasks per §5 wake conditions.
- If (a) or (b) fires: KB-HTD-1.1 FAILS — per the adopted bar, the generation
  track stays SUSPENDED until the units program names section champions, and a
  rank-flip is committed as evidence that the task measured the proxy atoms, not
  generation strategy (the red-team §1 dilemma, case (a)).

**Evidence committed:** per task, per family: the unit binding used, per-strategy
primary-metric scores, the rank ordering, void records with the reason the
measurement could not be scored, and the final PASS/FAIL of the bar. Under
`docs/lab/htd-1/` per program evidence discipline.

**Note on interaction with KB-HTD-1.2:** KB-HTD-1.2's SUSPEND fires on champion
availability (state of the units program, calendar-independent). This firing test
is the *second* gate: even with champions named, the track runs only on tasks
that survive it. If champions exist but the firing test fails, the failure is
reported to Micah as-is (honest FAIL — the task is atom-relative) and the track
does not proceed until a passing task is found or he issues a dated amendment.

---

## §3. Canonical Proxy A/B/C battery, slice extension legs, dual anchoring

Source: `debate/metrics-spec.md` §§2, 4.1, 5.1 (debate-phase draft — working
definitions pending referee freeze + Micah approval) and draft prereg §5. All
three proxies apply to all twelve parked hypotheses (G-AR*: directly; G-PA*:
all three, Proxy B is its home turf — if it cannot beat the baselines on B its
core claim fails; G-CO*: all three, Proxy B load-bearing). Any hypothesis may
propose ONE additional preregistered proxy of its own design (exact scoring
committed before building), but it cannot substitute for A/B/C.

Shared corpora (fixed for HTD-1, read in place): `~/workspace/tnn-lab/corpora/pg100.txt`
(5.6MB), `~/workspace/tnn-lab/corpora/sqlite3.c` (9.5MB). No additional corpora
without Micah's sign-off.

### Corpus split (fixed, committed at prereg)

Memorization segments (system may store as memory chunks) vs held-out segments
(never shown during memorization, test-time only). Deterministic rule: every 10th
4KB block is held out, blocks indexed by byte offset (reproducible,
corpus-version-pinned). The system is told which segments are held out only via a
manifest file it must not read during memorization (enforced by the harness:
memorization runs see only the memorization manifest).

### Proxy A — Held-out span reconstruction from memory chunks (K=200 probes)

- System stores memorization segments through its own pipeline. At test time it
  is given a pointer (document ID + byte offset) into a held-out segment and must
  reconstruct the following **N=256 bytes** from stored knowledge alone.
- 200 probes: 100 per corpus, offsets fixed in prereg by deterministic stride
  (every (heldout_size/100)-th offset — NOT random).
- Scoring: per probe `exact_byte_match_fraction` = identical bytes / 256.
  Aggregate = mean over 200 probes. ALSO report the 10th percentile (worst-decile
  behavior matters).
- Determinism gate applies to every probe.
- **Proves:** the memory/chunking pipeline preserves information with fidelity
  (load-bearing for any style claiming to "speak from memory"). **Does NOT
  prove:** novel generation, composition quality, or choice of what to say. A
  lookup table scores perfectly here and is useless at generation. Necessary, not
  sufficient.

### Proxy B — Trace-composition fidelity (50 deterministic compositions)

- System is given M=8 short memorized passages (identified by chunk handles its
  own pipeline produced) and a deterministic composition instruction (e.g.,
  "concatenate passages 3,1,7 in order, then emit the first 64 bytes of passage
  5"). 50 fixed composition instructions, committed in prereg.
- Scoring: binary per composition — 1 if byte-identical to the harness-computed
  reference (from ground truth, not from any arm), 0 otherwise. Aggregate =
  (# exact) / 50. NO partial credit.
- **Proves:** the generation path preserves content through multi-step assembly
  (minimum bar for compositional and all-at-once styles). **Does NOT prove:**
  quality of novel composition, style, or relevance. Tests the plumbing, not the
  poetry.

### Proxy C — Constrained fill-in-the-blank (200 masks)

- System shown a memorized passage with a masked span (mask location + length
  fixed in prereg; 200 masks, 100 per corpus, deterministic offsets) plus a
  constraint from a fixed preregistered list (e.g., "the missing span is a C
  function signature," "the missing span is a dialogue attribution," "the
  missing span must be ≤ 32 bytes"). Emits a fill. Underdetermined by design —
  exact match is the wrong sole bar.
- Scoring (exact, checkers are code committed in prereg — no LLM judge, no human
  judge):
  - Constraint satisfaction: binary, 30% of proxy score (deterministic checker:
    byte-length check, fixed-grammar parse, fixed vocabulary list).
  - Corpus consistency: binary, 40% (does the fill appear verbatim *anywhere*
    in the memorization segments? — deliberate bias toward grounded generation).
  - Exact-match bonus: binary, 30% (is the fill byte-identical to the true
    masked span?).
  - Per-mask score ∈ {0, 0.3, 0.4, 0.6, 0.7, 1.0}; aggregate = mean over 200.
- **Proves:** plausible, grounded, constrained output when the answer is not
  fully determined (the actual generation skill). **Does NOT prove:**
  long-form coherence, factuality beyond the corpus, or style. The
  corpus-consistency component deliberately rewards conservatism; a
  novelty-tolerant "C-novel" variant is a named follow-up for the next HTD, NOT
  a rescoring of this proxy.

### Referee default hard-kill bars (metrics-spec §5.1)

Imposed by the referee if a hypothesis prereg is thin (crews should set stricter
ones). For generation: **hard-kill if Proxy A mean < 0.50** (worse than a
coin-flip byte match — the memory pipeline is not preserving information) **OR
Proxy B < 25/50**. These apply to all twelve parked hypotheses via the dual
anchoring rule below. (The load-bearing example in metrics-spec §5.1 —
"Proxy B < 40/50 the compositional claim is dead" — is the *style* of bar an
author marks as load-bearing, not a substitute for the 25/50 default.)

### Slice extension legs (secondary; run after the canonical battery)

Each slice keeps its debate-phase proxy because the slice's own kill bars are
anchored to it:

- **AR slice leg — HOSR** (Held-out Span Reconstruction): 100 test spans
  redacted from what the generator may see; hypothesis emits redacted spans
  sequentially, one unit per step; 100 spans × 2 corpora = 200 trials. Scores:
  fidelity = byte-exact span match rate (no partial credit, no BLEU);
  citation validity = % of emitted units carrying a valid audit-ledger citation
  chain to stored evidence; cost = median wall-clock per emitted unit + total
  wall-clock + ledger entries per unit (replay cost proxy). Shared baseline
  G-GREEDY (best-guess emit, zero deliberation, no commit check/gate/elimination/
  checkpoint) — every hypothesis must beat greedy on (fidelity ×
  citation-validity) / cost, or justify why not. Unit granularity fixed per run
  (pg100: clause-level; sqlite3.c: statement-level), preregistered before any
  run. Determinism: each trial run twice; any byte divergence = protocol
  violation, hypothesis disqualified for that run.
- **PA slice leg — masked-span set:** 1,000 pg100 passages, one 32–128 byte span
  masked per passage (mask positions fixed in the prereg file); metric = exact
  byte-match rate of the reconstructed span + convergence stats (sweeps used,
  cells touched, oscillation count); PLUS 200-item sqlite3.c
  constraint-generation set (200 items × 5 named constraints, e.g., balanced
  delimiters, no undefined identifiers from a fixed allowlist, terminates with
  `;` — G-PA3's discriminating-constraint proxy). All four PA hypotheses + the
  AR slice run identical item lists.
- **CO slice leg — PROSE-REC + CODE-REC:** PROSE-REC — 1,000 pg100 passages;
  prompt = preceding 64 bytes (fixed anchor) + target span 64–256 bytes to
  reconstruct + 3 named constraints per item from a fixed pinned vocabulary;
  CODE-REC — 300 sqlite3.c functions; prompt = function signature + docstring
  comment + required identifier list; target = function body. Item lists
  identical for all four CO hypotheses + the AR slice (+ G-PA4 for the hierarchy
  comparison). G-CO2 additionally: fixed 256-byte corpus chunking as its memory
  load + 200-item out-of-corpus abstention probe set. G-CO4 additionally:
  100-item misfit probe set (held-out genre, e.g., stage directions against
  dialogue templates).

### Dual-anchoring rule (draft prereg §5, kept verbatim)

**A hypothesis must pass its own brief's kill bars on its brief's proxy AND the
referee's floor bars on the canonical battery.** Both anchors, no substitution.
Consequence: every parked hypothesis runs the canonical A/B/C battery first (its
Proxy A/B/C scores must clear the referee's hard-kill floors: Proxy A ≥ 0.50
mean, Proxy B ≥ 25/50), then its slice leg (its brief's bars fire on the leg's
proxy). A hypothesis that clears its brief's bars but trips a referee floor bar
is KILLED, and vice versa. The slice leg is secondary in run order, not in
authority — both anchors bind.

### Shared baselines for the generation track

Built once by the referee crew, committed before any arm builds, frozen for
HTD-1, and passing the determinism gate themselves:
- **B-G1 "naive emit":** emits memorized chunks verbatim (nearest-chunk lookup
  by byte-offset proximity, no deliberation, no composition). The floor for
  Proxies A and B.
- **B-G2 "fixed-template fill":** fills masks with a deterministic template
  (e.g., the most frequent span of matching length from the memorization
  segments). The floor for Proxy C.
- **G-GREEDY** (AR-brief baseline, kept for the AR slice leg): best-guess unit
  emit with zero deliberation. Every AR hypothesis faces it on HOSR.
Beating baselines is necessary, not sufficient (metrics-spec §4.1). Tie-break
order (metrics-spec §4.3, applied lexicographically): primary metric → for
generation, secondary = Proxy B exact-match count → peak resident memory →
wall-clock median → final tie-break tested BOTH directions (incumbent-wins vs
challenger-wins); direction-sensitive verdicts are reported as TIE.

### Anti-shopping and instrumentation (carried into every build prereg)

- Refinement budgets (P, K, Q, R, N, checkpoint interval m=8, candidate-set
  size 3–7, template cap 12, retry counts, coverage threshold C) are fixed in
  prereg; a hypothesis may not adapt its budget per item. Stagnation/oscillation
  halts, abstentions, and misfits are item verdicts, not invitations to try
  harder.
- All tie-breaks deterministic (lowest candidate/chunk/region id); never
  wall-clock time, never memory addresses, never hash-map iteration order.
- Common instrumentation on every run: cells-touched, cell-writes,
  passes/sweeps/rounds used, ledger-bytes-per-output-byte, termination reason
  per item, ops broken down by phase (for CO: parse / skeleton / fill /
  weave-verify; planning-phase op share), memory slots touched ÷ total slots
  (the 20W sparsity read).
- Per-item scores committed, not just aggregates (worst-decile analysis):
  5 SHA-256 hashes per test, op-count vectors, per-probe/mask/composition
  scores, wall-clock median+range, peak memory, snapshot manifest.

---

## §4. Merged generation head-to-head matrix

Assembled from the three debate slices' matrices (AR cross-hypothesis notes;
PA "Head-to-head matrix" table; CO "Head-to-head matrix" table) — no pairing
invented, no pairing dropped. Each pairing is scored per frozen prereg §7
verdict rubric (PASS/FAIL/KILLED/PARKED/VOID/INVALID; section champions per
proceeding family; no overall winner expected; overall champion only on blowout:
≥2× margin on the other section's home metric under both tie-break directions,
no hard-kill trips) plus the dual-anchoring rule (§3). "AR best" = the AR-slice
hypothesis that survives its own HOSR bars and the canonical battery — named at
run time, not in advance.

### A. Within-slice pairings

| # | Pairing | Decides | Source |
|---|---|---|---|
| A1 | G-AR1 vs G-AR2 vs G-AR3 vs G-AR4 (all-pairs on HOSR) | Which sequential-deliberation shape wins at all: per-chunk commit vs split propose/verify vs eliminative selection vs cheap cascade | gen-autoreg cross-hypothesis notes |
| A2 | G-AR2 vs G-AR4 | Whose efficiency mechanism is real: sparse partitions vs cheap cascade; and does a hybrid beat both? | gen-autoreg (AR2 head-to-head; AR4 head-to-head) |
| A3 | G-AR3 candidate-set-size=1 ablation | Does the candidate SET matter or just the elimination rules? (Set=1 must reproduce greedy-plus-rules) | gen-autoreg (AR3 head-to-head) |
| A4 | G-PA1 vs G-PA2 | Flag-driven sparse repair vs blind full-tape fixpoint — the efficiency shootout | gen-parallel matrix |
| A5 | G-PA1 vs G-PA4 | Flat defect-driven order vs hierarchical level order — which localizes work better (20W question) | gen-parallel matrix |
| A6 | G-PA2 vs G-PA4 | Emergent convergence (fixpoint) vs planned convergence (levels) | gen-parallel matrix |
| A7 | G-PA3 vs G-PA1 / G-PA2 | Selection-among-many vs refinement-of-one — the architectural fork of the parallel slice | gen-parallel matrix |
| A8 | G-CO1 vs G-CO4 | Per-task skeleton vs reusable template — the design-cost shootout | gen-compositional matrix |
| A9 | G-CO1 vs G-CO2 | Deliberated fill vs retrieved fill — is designing regions better than citing memory? | gen-compositional matrix |
| A10 | G-CO2 vs G-CO3 | Plan over chunks vs plan over ops — which plan vocabulary wins? | gen-compositional matrix |
| A11 | G-CO3 vs G-CO4 | Generated plans vs pre-committed templates — do cached plans converge to templates under reuse pressure? | gen-compositional matrix |

### B. Cross-slice pairings (style-vs-style — the showdown this track exists for)

| # | Pairing | Decides | Source |
|---|---|---|---|
| B1 | Each G-PAx (PA1–4) vs AR best | Does ANY parallel family beat sequential at all? | gen-parallel matrix (all four) |
| B2 | Each G-COx (CO1, CO4) vs AR best | Does ANY structure-first family beat sequential at all? (CO2/CO3's AR comparisons are gating-scoped and live in the proceeding track) | gen-compositional matrix |
| B3 | G-AR3 vs diffusion slice (G-PA1/G-PA2) | Are elimination rounds and denoising/refinement steps the same idea in different clothes? | gen-autoreg (AR3 head-to-head) |
| B4 | G-AR4 vs all-at-once slice | Is checkpoint-backtrack just all-at-once with extra steps? | gen-autoreg (AR4 head-to-head) |
| B5 | G-CO1 vs G-PA4 | Deliberated per-task skeleton vs fixed-level expansion — which hierarchy localizes work better? (Load-bearing: if these collapse into each other, that is evidence, not a bug) | gen-compositional matrix + PA brief |
| B6 | G-PA3 vs G-PA4 and debate-trial standard | Does draft selection meet TNN's own eliminative-evidence bar (the debate trial's world-evidence rule)? | gen-parallel matrix + PA3 brief |
| B7 | G-CO3 vs RC1 evidence standard | Does the plan-verifier meet the bar the reasoning-control pilot set: inspect own bar, predictions hold, rollback on violation? | gen-compositional matrix |

### C. Baseline / ablation pairings (kill-the-confounder set)

| # | Pairing | Decides | Source |
|---|---|---|---|
| C1 | Every hypothesis vs G-GREEDY (HOSR) | Does deliberation earn its keep over best-guess emission? | gen-autoreg (all four) |
| C2 | Every hypothesis vs B-G1, B-G2 (canonical battery) | Does the style beat verbatim lookup and fixed-template fill? (Necessary, not sufficient) | metrics-spec §4.1 |
| C3 | G-AR2 vs full-wake ablation of itself | Sparsity must earn its keep (paired with AR2-K4) | gen-autoreg (AR2 head-to-head) |
| C4 | G-AR4 fast path alone (= G-GREEDY) | Do checkpoints add value over the fast path by itself? | gen-autoreg (AR4 head-to-head) |
| C5 | G-CO1 vs reverse-dependency-order fill ablation | Hidden cross-region coupling test: any byte change invalidates the parallelism claim (P2) | gen-compositional (CO1 P2) |

### D. Scenario-fit mapping (required for every surviving hypothesis)

Per frozen prereg §7 and the program's no-free-lunch law, the matrix above does
not crown a single winner by default. For each surviving hypothesis the build
crew commits a scenario-fit map with preregistered expectations tested, e.g.:
G-AR4 expected to win on cost for high-fidelity memory; G-AR3 expected to win
fidelity on adversarial/ambiguous prefixes; G-CO4 expected to win on code-like
genres with stable schemas. "No overall winner" is an acceptable and expected
outcome; overall champion only on the §7 blowout (≥2× margin on the other
section's home metric under both tie-break directions, no hard-kill trips).

---

## §5. Wake conditions checklist and day-one actions

### The two gates (both must hold)

- [ ] **Gate 1 — KB-HTD-1.2 lifts (champion-availability).** Observable event:
  the units program commits its verdict sheet naming **section champions per
  the PREREG_FREEZE verdict §7 analog** — i.e., section champions per scored
  metric with the blowout rule (≥6 of applicable scored metrics + no weak
  flank + N/A discipline + scale confirmation) or, absent a blowout, the
  scenario-fit map. Calendar-independent: the crew checks the units program's
  committed verdict artifacts, not a date. A "champions announced in chat"
  without committed verdict artifacts does NOT lift the gate.
- [ ] **Gate 2 — KB-HTD-1.1 firing test executed and PASSED.** Observable
  event: the referee crew has executed the §2 procedure (top two proxy tasks
  re-run across ≥3 materially different arm families) and committed the
  evidence showing neither measurement-voided nor rank-flip in any family. If
  the firing test FAILS, the track does NOT proceed: the failure is reported
  to Micah as-is per the honest-failure law, and the track waits on a passing
  task or his dated amendment. (Note: KB-HTD-1.1 was preserved verbatim for
  execution when arm outputs exist — frozen prereg §1. If only champions exist
  but no settled multi-family arm outputs are available to run the firing test
  on, Gate 2 is unexecutable and the track stays parked.)

**Scope note:** lifting the gates un-parks G-AR1–4, G-PA1–4, G-CO1, G-CO4 only.
G-CO2/G-CO3 (narrowed gating), G-CM1, the E-DE*/E-SP*/E-LG* tracks proceed under
their own frozen terms regardless.

### Day one — first build crew runbook

1. **Verify the gates.** Read the units program's committed verdict sheet;
   confirm section champions are named per the PREREG_FREEZE §7 convention and
   that the KB-HTD-1.1 firing-test evidence is committed with a PASS. If
   either is missing or ambiguous, STOP — do not build; report the gap.
2. **Bind the units.** Pull the frozen champion atom definitions from the units
   verdict artifacts. Write the unit-binding addendum: for each proxy in §3
   (canonical A/B/C + the three slice legs), state exactly what "unit / span /
   chunk / passage" means in champion-atom terms. Bars stay, units swap —
   per the AR brief's interaction note, if the atom decision changed the unit,
   the affected proxies rerun with the new unit; the bars do not move.
3. **Freeze the shared proxy specs.** Before any arm builds: publish the
   deterministic item lists (HOSR 200-trial spans; PA 1,000-passage mask
   positions + 200-item sqlite constraint set; CO PROSE-REC/CODE-REC item
   lists + G-CO2 abstention probes + G-CO4 misfit probes), the Proxy A offset
   stride, the Proxy B 50 composition instructions, the Proxy C 200 masks +
   constraint list + deterministic checkers, the corpus-split manifest, and
   the firing-test task ranking from §2 Step 1. Commit under
   `~/workspace/htd-1/` (frozen artifacts live with the R3 crew's set).
4. **Build and freeze baselines first.** Referee crew implements B-G1, B-G2,
   and G-GREEDY (pure Zag, zero randomness in decision paths), runs the
   determinism gate (R=5, SHA-256 byte-identity) on each, commits their hashes
   before any hypothesis arm's evidence — so no arm can claim the baselines
   were rigged after the fact.
5. **Stand up the determinism harness.** Logged-state snapshot/restore
   (memory store post-memorization, ledger/audit trail, config incl. weights
   and manifests); the harness computes SHA-256 over concatenated artifact
   bytes; arms never self-report hashes. Invalid run set = no score, diagnose
   and rerun; two consecutive invalids = BLOCKED pending Micah's review.
6. **Wire the dual anchors.** Every arm's prereg names BOTH: (a) its brief's
   kill bars on its slice leg, and (b) the referee floor bars (Proxy A ≥ 0.50
   mean, Proxy B ≥ 25/50) on the canonical battery. Run order: canonical
   battery first, slice leg second.
7. **Then build the twelve hypotheses** in the frozen build order, report
   results as they resolve (including honest FAILs and fired bars) under
   `docs/lab/htd-1/`, verdict sheets in `docs/lab/htd-1/verdicts.md`.

### Standing rules this track inherits (do not relitigate)

Pure Zag. Zero randomness in any AI decision path. Byte-identical reruns or
disqualification (not a bar). Prereg before building; kill bars binding; test
head-to-head, never minimize; no-free-lunch (test scenario fit, don't crown by
default); tie-breaks tested both directions — direction-sensitive verdicts are
TIEs. Any change to rules, metrics, thresholds, or scope needs a dated
Micah-approved amendment. Workdirs under `~/workspace`, never /tmp.

---

*End of parked plan. Next touch: the day the two gates lift — until then this
document is read-only except for Micah-approved amendments.*
