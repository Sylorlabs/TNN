# HTD-1 Measurement Spec — METRICS REFEREE (debate-phase draft)

Status: DEBATE PHASE — this document defines the rules of measurement. It is not yet
preregistered. It becomes binding only after Micah approves it (with or without amendments).
Open measurement questions that the referee could not resolve alone are listed in §7;
nothing here is to be treated as settled until those are answered.

This spec is the measurement standard every HTD-1 hypothesis (G-AR*, G-PA*, G-CO*,
E-SP*, E-DE*, E-LG*) is scored against. The debate workers propose hypotheses; this
document says what counts as winning.

Program laws that constrain this spec (not up for debate):
- Pure Zag. No randomness in AI decision paths. Byte-identical reruns (same input +
  same logged state → byte-identical output). Preregister with kill bars before building.
- Corpora fixed for HTD-1: `~/workspace/tnn-lab/corpora/pg100.txt` (5.6MB) and
  `~/workspace/tnn-lab/corpora/sqlite3.c` (9.5MB). No additional corpora without
  Micah's sign-off, so efficiency and quality numbers stay comparable across arms.

---

## 1. Defining "efficiency": primary vs secondary metrics

### 1.1 Candidate metrics and their failure modes

| Metric | What it measures | Strength | Failure mode |
|---|---|---|---|
| Wall-clock on fixed hardware | Real elapsed time | Closest to "can this run affordably" | Noisy: thermal throttling, scheduler jitter, cache state, background load. On a shared lab VM, ±5–10% run-to-run wobble is normal and can swamp real small wins. |
| Deterministic op counts (Zag-instrumented) | Exact operations performed | Byte-deterministic given state; reruns agree to the unit; directly comparable across arms | Needs instrumentation discipline: every arm must count the same operation taxonomy, or counts are incomparable. Risks Goodharting — an arm could shift work into an uncounted category. |
| Ledger bytes written | Audit/ledger economy | Directly measures one of HTD-1's stated questions (ledger economy); deterministic | Narrow: a system could write fewer ledger bytes by doing more memory traffic elsewhere. |
| Peak resident memory | Memory footprint | Deterministic to measure (in practice, within noise); bounds deployability | Coarse; allocators fragment; not the question HTD-1 is asking. |

### 1.2 Referee's verdict (the debated choice)

**PRIMARY: deterministic operation counts instrumented in Zag.** Rationale: HTD-1's
efficiency question is "how far can deliberate efficiency go" — that is a question about
the *mechanism's own cost*, not about one afternoon's VM noise. Wall-clock can be gamed
by the lab's own jitter; op counts cannot, and they are the only candidate that is
byte-deterministic, which is a program law. Efficiency claims in TNN must be as
deterministic as the systems they measure.

**SECONDARY (all reported, none binding for PASS/KILL):**
- Wall-clock on the fixed lab VM (report median + range; used only as a sanity cross-check).
- Ledger bytes written per episode/task (binding only for E-LG* ledger-economy claims,
  where it is the thing under test — see §5.3).
- Peak resident memory (informational; a kill bar can be set on it per-arm if an arm's
  own prereg names one, but it is not in this spec's default bars).

### 1.3 Instrumentation discipline (the op-count contract)

Because op counts are primary, every efficiency arm must implement the same
instrumentation contract, or the primary metric is worthless. The prereg for each E-*
hypothesis MUST include:

1. **A named operation taxonomy**, committed before building. Minimum categories:
   `delib_step` (one deliberate deliberation step), `mem_read`, `mem_write`,
   `chunk_store`, `chunk_fetch`, `gate_eval`, `ledger_append`. Arms may add categories
   but may not merge or redefine the minimums.
2. **A counter harness in Zag** that emits, per task episode: total counts per category,
   summed to a single **deterministic cost scalar** `C = Σ w_i · n_i`, where the weights
   `w_i` are fixed per task family and published in the prereg.
3. **Anti-Goodhart rule:** any computation that influences the output but is not
   counted in any category is a *prereg violation* — the run is invalid, not a win.
   Referees audit by code inspection: every loop, recursion, and memory touch in the
   arm's hot path must map to a category. This is the discipline cost of choosing
   op-counts; it is non-negotiable.
4. **Weight calibration:** `w_i` values are set by measuring a reference microbenchmark
   once (e.g., cost of one `mem_read` vs one `delib_step` on the lab VM), recorded in
   the prereg, and frozen for the whole of HTD-1. Weights do not change mid-trial.

Wall-clock is reported as: median of the valid reruns (see §3), plus the min–max range.
If wall-clock and op-count disagree on which arm won (e.g., fewer ops but slower
wall-clock), the op-count verdict stands and the discrepancy is flagged as an open
question for the TEST phase to explain (possible causes: cache behavior, allocator
pathologies, instrumentation overhead).

---

## 2. Defining "generation quality" without a settled decoder

TNN has no settled generation style — that is the point of HTD-1 — so quality cannot
mean "perplexity" or "BLEU against a reference decoder," because there is no reference
decoder to be faithful to. Instead, quality is measured by **what the generated output
can provably do**: reconstruct held-out material, compose traces without loss, and fill
constrained gaps. Three proxy tasks, each scored exactly.

Corpus split (fixed for HTD-1, committed at prereg): each corpus is split into
**memorization segments** (the system may store these as memory chunks) and
**held-out segments** (never shown during memorization; used only at test time).
Split rule: deterministic — every 10th 4KB block is held out (blocks indexed by byte
offset, so the split is reproducible and corpus-version-pinned). The system is told
which segments are held out only via a manifest file it must not read during the
memorization phase (enforced by the harness: memorization runs see only the
memorization manifest).

### Proxy A — Held-out span reconstruction from memory chunks
**What it is:** the system stores memorization segments as memory chunks through its
own pipeline (whatever the arm's chunking/deliberation scheme is). At test time it is
given a *pointer* (document ID + byte offset) into a held-out segment and must
reconstruct the following N bytes from its stored knowledge alone — no access to the
held-out text.

**Scoring (exact):**
- For each of K=200 held-out probes (100 per corpus, offsets fixed in prereg by a
  deterministic stride, NOT random — e.g., every (heldout_size/100)-th offset),
  request reconstruction of N=256 bytes.
- Score per probe: `exact_byte_match_fraction` = (# bytes identical to ground truth) / 256.
- Aggregate: mean over 200 probes. Report also the 10th percentile (worst-decile
  behavior matters — a system that nails 180 probes and hallucinates 20 is different
  from one that is uniformly mediocre).
- Determinism gate (§3) applies to every probe: rerunning a probe must reproduce the
  reconstruction byte-identically.

**What it proves:** that the memory/chunking pipeline preserves information with
fidelity — the load-bearing requirement for any generation style that claims to
"speak from memory." **What it does NOT prove:** that the system can generate
*novel* text well, compose ideas, or choose what to say. A lookup table scores
perfectly here and is useless at generation. This proxy is necessary, not sufficient.

### Proxy B — Trace-composition fidelity
**What it is:** the system is given M=8 short memorized passages (from the memorization
segments, identified by chunk handles its own pipeline produced) and a deterministic
composition instruction (e.g., "concatenate passages 3,1,7 in order, then emit the
first 64 bytes of passage 5"). It must produce the composed output. The composition
instructions are fixed in the prereg (a list of 50 deterministic compositions).

**Scoring (exact):**
- Per composition: byte-exact match against the reference composition (computed by
  the harness from ground truth, not by any arm). Score is binary: 1 if byte-identical,
  0 otherwise.
- Aggregate: (# exact) / 50.
- Partial credit is NOT given: composition is a fidelity task; near-miss composition
  is failed composition. (Rationale: if a generation style cannot faithfully compose
  what it remembers, its "creativity" is untrustworthy output.)

**What it proves:** that the generation path preserves content through multi-step
assembly — the minimum bar for compositional and all-at-once styles. **What it does
NOT prove:** quality of novel composition, style, or relevance. It tests the plumbing,
not the poetry.

### Proxy C — Constrained fill-in-the-blank over the corpora
**What it is:** the system is shown a memorized passage with a masked span (the mask
location and length are fixed in the prereg; 200 masks, 100 per corpus, deterministic
offsets), plus a *constraint* drawn from a fixed preregistered list (e.g., "the missing
span is a C function signature," "the missing span is a dialogue attribution," "the
missing span must be ≤ 32 bytes"). It must emit a fill. This is the closest proxy to
real generation: the answer is underdetermined, so exact match is the wrong bar.

**Scoring (exact):**
- **Constraint satisfaction (binary, 30% of proxy score):** did the fill satisfy the
  stated constraint? Judged by a deterministic checker written in the prereg (e.g.,
  byte-length check, "parses as a C function signature" via a fixed grammar, "contains
  a dialogue verb from the fixed list"). No LLM judge, no human judge — the checker
  is code, committed before building.
- **Corpus consistency (binary, 40%):** does the fill appear verbatim *anywhere* in
  the memorization segments? (A fill that invents vocabulary the corpus never used is
  penalized; a fill that reuses the corpus's own material is rewarded. This is a
  deliberate bias toward grounded generation — debatable, see §7.)
- **Exact-match bonus (binary, 30%):** is the fill byte-identical to the true masked
  span? Rewards genuine reconstruction where the context determines the answer.
- Per-mask score ∈ {0, 0.3, 0.4, 0.6, 0.7, 1.0}; aggregate = mean over 200 masks.

**What it proves:** that the system can produce *plausible, grounded, constrained*
output when the answer is not fully determined — the actual generation skill.
**What it does NOT prove:** anything about long-form coherence, factuality beyond the
corpus, or style. The corpus-consistency component deliberately rewards
conservatism; a genuinely creative-but-unseen fill scores lower. That bias is
documented here so the TEST phase can add a novelty-tolerant variant if a hypothesis
demands it (as a separate preregistered proxy, not a rescoring of this one).

### Proxy applicability by generation hypothesis
- G-AR* (autoregressive): all three proxies apply directly.
- G-PA* (parallel/all-at-once): all three apply; Proxy B is its home turf — if it
  cannot beat the baselines on B, its core claim fails.
- G-CO* (compositional): all three apply; Proxy B is load-bearing for its claim.
- Any hypothesis may propose ONE additional preregistered proxy of its own design
  (with exact scoring committed before building), but it cannot substitute for A/B/C.

---

## 3. The determinism gate (every test, no exceptions)

Program law: same input + same logged state → byte-identical output. The gate
operationalizes it:

1. **Reruns:** every scored run is executed **5 times** (R=5). The 5 runs are the
   measurement; there is no separate "main run."
2. **Byte-identical criterion:** all scored artifacts (reconstructions, compositions,
   fills, op-count vectors, ledger bytes) must be byte-identical across all 5 runs.
   Comparison is by SHA-256 of the concatenated artifact bytes (the harness computes
   it; arms do not self-report hashes).
3. **"Logged state" is defined as:** the complete, serialized, human-inspectable
   record the arm's prereg names as its state — at minimum: (a) the memory store
   contents after the memorization phase, (b) the deliberation ledger/audit trail,
   (c) the arm's configuration (weights `w_i`, taxonomy version, probe manifests).
   The harness snapshots (a)–(c) before the test phase and restores from the snapshot
   before each of the 5 runs. If the arm's output depends on anything not in the
   snapshot (wall-clock time, memory addresses, uninitialized memory, file iteration
   order), the gate fails — that is the gate working as intended.
4. **Failure consequence:** any byte-difference across the 5 runs INVALIDATES the run
   set. It is not a low score; it is not a FAIL — it is invalid, the arm does not
   advance, and the arm's crew must diagnose and rerun. Two consecutive invalid run
   sets on the same test = the hypothesis is BLOCKED pending Micah's review (not
   killed — nondeterminism is a harness/implementation defect, and killing a hypothesis
   for an implementation bug would be the wrong verdict).
5. **Determinism evidence is committed:** the 5 SHA-256 hashes per test are written to
   the evidence log under `docs/lab/htd-1/`. A verifier rerunning from the committed
   snapshot must reproduce the same hashes — this is the "hardened re-run" standard
   the program already adopted for the scanner work.

Note on the ledger-vs-state tension (program-open question, Micah has not ruled):
if the byte-identical-vs-state-varying tension from the wave-11 ledger debate is
decided in favor of relaxing byte-identity for *ledger-internal* bytes, this gate
still applies unchanged to *scored artifacts*. The gate governs what the hypothesis
is measured on, not the ledger's internal encoding.

---

## 4. Head-to-head protocol

### 4.1 Baselines (every hypothesis must beat these; beating them is necessary, not sufficient)

**Efficiency arms (E-*)** face two baselines:
- **B-E1 "always-awake deliberation":** a deliberation pipeline with no sparsity, no
  routing, no economy mechanism — every deliberation step runs at full width, every
  memory touched is read. This is the "20W brain vs datacenter" floor: an efficiency
  hypothesis that cannot beat always-awake on the primary metric (op-count cost `C`)
  has no efficiency claim at all.
- **B-E2 "uniform-random routing (fenced)":** routes/sparsifies using a *seeded,
  logged, non-AI* mechanism (e.g., fixed stride pattern — explicitly NOT randomness in
  the AI's decision path; the pattern is a constant of the harness). This tests
  whether the arm's *deliberateness* adds anything over a dumb-but-cheap pattern.
  An efficiency claim that loses to a fixed stride is not deliberate efficiency, it
  is just sparsity.

**Generation arms (G-*)** face two baselines:
- **B-G1 "naive emit":** emits memorized chunks verbatim (nearest-chunk lookup by
  byte-offset proximity, no deliberation, no composition logic). This is the floor
  for Proxies A and B — any generation style must beat verbatim lookup, or it is
  worse than not generating.
- **B-G2 "fixed-template fill":** fills masks with a deterministic template (e.g.,
  the most frequent span of matching length from the memorization segments). The
  floor for Proxy C — beats "say the most common thing."

Baselines are implemented once, by the referee's crew (not by the hypothesis crews),
committed before any arm builds, and frozen for HTD-1. Baselines must themselves pass
the determinism gate (§3).

### 4.2 Repetitions and aggregation
- Every hypothesis-vs-baseline comparison runs the full proxy battery (A+B+C for
  generation; the efficiency task battery defined in each E-* prereg for efficiency)
  with R=5 reruns per §3.
- The reported number for each metric is the value from the (byte-identical) run set —
  since all 5 agree byte-for-byte, there is no averaging and no variance to report.
  (If the gate passes, mean = median = every run. This is a feature: determinism
  removes the statistics.)
- Wall-clock, the noisy secondary, IS reported as median + range over the 5 runs.

### 4.3 Deterministic tie-breaks (no RNG)
Ties on the primary metric are expected (deterministic systems tie exactly, not
approximately). Tie-break order, applied lexicographically:
1. Primary metric (op-count cost `C` for efficiency; proxy aggregate for generation).
2. Secondary metric: ledger bytes written (for efficiency) / Proxy B exact-match count
   (for generation — fidelity before flair).
3. Peak resident memory (lower wins).
4. Wall-clock median (lower wins).
5. **Final tie-break, tested BOTH directions** (per the program's standing decision to
   test both tie-break directions in the frozen tests): 
   - Direction 1 ("incumbent wins"): the hypothesis listed earlier in the prereg
     document order wins.
   - Direction 2 ("challenger wins"): the hypothesis listed later wins.
   
   Both directions are computed and both results are reported. If the verdict
   (PASS/KILL/champion) is *sensitive* to tie-break direction — i.e., the two
   directions name different winners — the result is reported as **TIE (direction-
   sensitive)** and neither hypothesis may claim a win on that comparison. This is
   the honest outcome: a tie that depends on an arbitrary rule is not a win.

---

## 5. Verdict rubric: PASS / FAIL / KILLED / champions

### 5.1 Per-hypothesis verdicts (scored against baselines + kill bars)

Each hypothesis preregisters **kill bars** (numeric, e.g., K1–K9 style from wave-11).
The referee's rubric maps measured results to verdicts:

- **PASS:** beats BOTH baselines on the primary metric (strictly, after tie-breaks —
  a direction-sensitive tie against a baseline is not a win) AND clears every
  preregistered kill bar. A PASSed hypothesis advances; it is a candidate for
  section champion.
- **FAIL:** beats at least one baseline but misses ≥1 kill bar, or beats neither
  baseline but shows a preregistered "progress signal" the prereg named in advance
  (e.g., "within 10% of B-E1 on cost C with 3x fewer ledger bytes"). FAIL is honest,
  documented with evidence, and the hypothesis may be revised and re-entered ONCE
  (re-entry needs a prereg amendment; Micah re-approves the amended bars).
- **KILLED:** loses to BOTH baselines on the primary metric, OR trips a preregistered
  kill bar marked **hard-kill** (a bar the hypothesis's own authors marked as
  load-bearing — e.g., "if Proxy B < 40/50 the compositional claim is dead"). KILLED
  is terminal for HTD-1: the hypothesis does not advance, is not revised into the
  same trial, and its evidence is committed as a negative result. (Per program law,
  kill criteria are binding — a KILLED hypothesis stays dead even if its crew has
  ideas for fixing it. New ideas become new hypotheses in a later HTD.)

Minimum default kill bars if a hypothesis prereg is thin (the referee imposes these;
crews should set stricter ones):
- Efficiency: hard-kill if `C` ≥ B-E1's `C` (fails to beat always-awake at all).
- Generation: hard-kill if Proxy A mean < 0.50 (worse than a coin-flip byte match —
  the memory pipeline is not preserving information) OR Proxy B < 25/50.

### 5.2 Section champions and the overall champion

- **Section champion (efficiency):** among PASSed E-* hypotheses, the one ranked first
  by the §4.3 tie-break order. Named per the frozen prereg's Verdict §7 convention:
  section champions are the deliverable (they are TNN's efficiency answer).
- **Section champion (generation):** among PASSed G-* hypotheses, ranked first by
  proxy aggregate (mean of A, B, C aggregates), then §4.3 tie-breaks. This names
  TNN's provisional generation style.
- **"No overall winner" is an acceptable and expected outcome.** Efficiency and
  generation are different sections; a single overall champion is NOT required and
  should not be forced. The two section champions can coexist (they answer different
  questions).
- **Overall champion (blowout only):** an overall champion across BOTH sections may
  be named only on a **blowout**, defined numerically as: one hypothesis (or one
  tightly-integrated pair, preregistered as a pair) that (a) PASSes in its own
  section, (b) beats the other section's champion head-to-head on the other
  section's primary metric by **≥ 2x margin** (half the op-count cost, or +0.25
  absolute on proxy aggregate — the margin must hold under BOTH tie-break
  directions), and (c) trips no hard-kill bar anywhere. Rationale for the high bar:
  naming an overall champion collapses two research questions into one answer, and
  that should only happen when the evidence leaves no room for argument. Anything
  short of a blowout → two section champions, honestly reported.

### 5.3 Ledger economy (E-LG*) — the metric exception
E-LG* hypotheses test ledger economy specifically. For those arms ONLY, the prereg
may promote **ledger bytes written** to co-primary with op-count cost `C` (both must
beat baselines; the kill bars name thresholds for each). This is the one place a
secondary metric becomes binding, because for E-LG* the ledger IS the thing under
test. All other arms: ledger bytes stay secondary.

---

## 6. Evidence and commit discipline

- Every scored run commits: the 5 SHA-256 hashes (§3.5), the op-count vectors, the
  proxy scores per probe/mask/composition (not just aggregates — per-item scores let
  the TEST phase do worst-decile analysis), wall-clock median+range, peak memory,
  and the snapshot manifest of the logged state.
- Evidence lives under `docs/lab/htd-1/` in the tnn-native-lab repo (per program
  law), organized per hypothesis: `docs/lab/htd-1/<hypothesis-id>/evidence/`.
- Verdict sheets (PASS/FAIL/KILLED, champion namings, tie declarations) are committed
  as `docs/lab/htd-1/verdicts.md`, updated as results resolve (report-as-they-resolve
  per HTD standing instruction).
- Baselines are committed first, before any arm's evidence, with their own passing
  determinism-gate hashes — so no arm can claim the baselines were rigged after the
  fact.

---

## 7. Open measurement questions (unresolved — referee's recommendation each)

1. **Op-count weights `w_i`: who calibrates, and against what?** The weights turn a
   vector into the scalar `C`, and whoever sets them influences which arm wins.
   *Recommendation:* calibrate once against the reference microbenchmark described in
   §1.3, publish the weights in the frozen prereg, and additionally report the raw
   unweighted vectors so anyone can re-rank under different weights. If re-weighting
   flips a champion, report both champions honestly.
2. **Proxy C's corpus-consistency bias against novelty.** Rewarding fills that appear
   verbatim in the corpus punishes genuine creativity. *Recommendation:* keep the
   bias for HTD-1 (groundedness first; TNN must be truthful before it is creative —
   this matches the program's integrity line), but preregister a named follow-up
   proxy variant ("C-novel") for the next HTD that scores novelty-tolerant fills,
   so the bias is revisited rather than fossilized.
3. **Is 200 probes / 50 compositions / 200 masks enough?** Larger batteries cost more
   lab time; smaller ones risk noise (though determinism removes sampling noise —
   the remaining risk is *coverage* noise: the fixed offsets might miss a regime).
   *Recommendation:* keep these sizes for HTD-1, but choose the deterministic offsets
   by striding across the *whole* corpus (not clustered), and add a preregistered
   "offset-shift sensitivity check": re-run Proxy A with all offsets shifted by a
   fixed constant; if the ranking flips, the battery is too small and the result is
   declared coverage-sensitive rather than a win.
4. **Should wall-clock ever override op-counts?** A purist says no (noise); a
   pragmatist says a 2x-slower system with fewer counted ops has a real cost the
   metric hides (cache/allocator effects are real engineering). *Recommendation:*
   for HTD-1, op-counts rule and wall-clock is a flag, not a verdict — BUT any arm
   whose wall-clock is ≥2x worse than the op-count ranking predicts must write up
   the discrepancy as a required evidence appendix. If the pattern repeats across
   arms, the TEST phase proposes an instrumentation fix (e.g., a `cache_miss`
   category) for HTD-2.
5. **Cross-section comparison fairness.** Efficiency arms and generation arms run
   different batteries; the blowout rule (§5.2) compares across them. Is that
   comparing apples to oranges? *Recommendation:* yes, it is — which is exactly why
   the blowout bar is set at 2x and requires winning on the *other* section's home
   metric. The bar is deliberately almost unreachable; "no overall winner" is the
   expected honest outcome.
6. **Who referees the referee?** This spec concentrates power: the metric choice
   decides winners. *Recommendation:* the metric spec itself is debated (this
   document), then frozen by Micah's approval like any prereg. Post-freeze metric
   changes need his re-approval, same as any rule change. The G-* and E-* debate
   crews get one round of written objections before the freeze; sustained objections
   are committed as dissent appendices, not silently dropped.

---

*End of metrics spec (debate draft). Next step: circulate to hypothesis debate crews
for one round of objections, then freeze for Micah's approval.*
