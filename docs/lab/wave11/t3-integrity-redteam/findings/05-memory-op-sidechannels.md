# Slice 05 — Memory-op side channels: timing, aliasing, digest feedback (RED TEAM)

## 1. Slice
Track 3, slice 05: attack the EDGES of the memory-judgment firewall (slices 13/20) —
timing/scheduling leaks, shared mutable buffers between expression layer and memory
substrate, and the `st_state_digest` feedback loop. RED TEAM: break the design.

## 2. Falsifiable claim
The two-barrier firewall (import-graph boundary + phase seam) is defeasible at its
edges: I claim at least one of (A) shared resource scheduling, (B) `StStore` slice
aliasing, or (C) digest contamination lets expression state influence a memory
decision, verdict, refusal, or ledger byte — provable by a concrete probe with a
byte-level diff. The design is killed if ANY probe below fires; it survives only if
all three probe families return clean on the reference build.

## 3. Design
Threat model: the attacker is the variation path itself (or a careless builder), not
an outsider. All three probes assume the import checker passes — the leak is through
mechanisms the checker cannot see.

**Probe A — timing/scheduling.** The seam freezes judgment before render, but it does
not freeze shared consumable resources. Two vectors:
- A1 *Budget bleed.* If the deliberation budget (slice 03) is one pool consumed by both
  variation work and judgment work, then elaboration depth (variation state) sets how
  much budget remains for the NEXT episode's `mem_decide` — expression state steers
  memory ops through the wallet. Probe: perturb elaboration cursor min/max (slice 13
  class), log budget-at-judgment-start each episode; any difference = leak.
- A2 *Clock reads.* A deterministic Zag binary has no timing channel unless code reads
  a clock. But `loop_episode` may stamp audit entries with wall time; if any judge-path
  code branches on a timestamp that includes variation compute time, variation duration
  steers memory ops. Probe: static grep for time/clock/syscall imports in the judge call
  graph (extend the no-RNG auditor) + differential: pad vary work with a calibrated busy
  loop, replay, compare `MemOp[]`.
Detection: judge-path budget register and op-count must be invariant under VaryState
perturbation; zero clock-reads in judge graph.

**Probe B — shared mutable buffers / StStore aliasing.** Slice 20 admits this as the
residual vector and rests on `loop.zag` discipline. Zag slices alias the same memory,
and the codebase's own convention is to alias large-struct fields into locals before
indexing. If the render tail (`o4_recall` or loop render) receives a slice into store
memory (trace text, slot buffers) rather than a copy, a write through the alias —
by render code, or by a future vary implementation — lands in the live store and the
NEXT episode's judgment reads corrupted evidence. Probe: (1) canary slots — fill N
guard slots with known bytes, run full render with max-perturbation VaryState,
`st_snap` before / hash-compare after; any diff = write-through. (2) static: any
`.*.field[i]` write or aliased-slice write in the render call graph fails review.
(3) strengthen: mandate `st_snap` before render and refuse all store writes after the
seam — writes post-seam become a hard error, not a convention.

**Probe C — digest feedback loop.** `st_state_digest` is the ONLY legal input to vary.
Two feedback directions:
- C1 *Mid-render digest drift.* If the digest is re-taken per `vary_pick` call rather
  than pinned once at the seam, any render-phase write (logging, memoization) changes
  the digest between picks — variation becomes self-referential: pick₂ = f(state +
  residue of pick₁). Probe: pin digest D₀ at seam; log digest at each vary call and
  after render; require D₀ == D₁ == … == D_post unless a judgment-phase op ran.
- C2 *Variation-log contamination.* Slice 15 logs VARIATION_CHOICE (digest, tag, pick)
  to the render log/ledger. If that log lives in state the digest hashes, then
  expression choices feed the NEXT digest, which feeds the next vary pick, which feeds
  the next digest — a self-amplifying loop unattributable to judgment state. Worse: if
  the log shares the store, future `mem_decide` reads variation-influenced bytes =
  direct memory-decision influence, killing the firewall outright. Probe: two-episode
  differential — identical JudgeInput, perturbed VaryState, compare digest inputs
  episode 2; then compare episode-2 `MemOp[]`. Any VaryState-attributable delta in
  either = kill. Design rule under test: the digest MUST hash (store, judgments,
  constitution) ONLY; render/variation logs are digest-excluded by construction, and
  the exclusion is asserted by a unit test hashing with/without the log present.

## 4. Kill bar
Preregistered, binding, zero tolerance — the firewall design is KILLED if any fires:
- **KA:** budget-at-judgment-start or judge-path op-count differs under VaryState
  perturbation (100 episodes × 4 perturbation classes), or any clock/time read found in
  the judge call graph.
- **KB:** post-render store hash differs from pre-render `st_snap` on any of 100
  max-perturbation render runs, or any aliased write into store memory found in the
  render call graph.
- **KC:** digest drifts between vary calls within one episode without an intervening
  judgment op, or episode-(n+1) digest / `MemOp[]` differs under episode-n VaryState
  perturbation (digest log-exclusion violated).
- Any probe showing memory-decision, verdict, refusal, or ledger-byte influence from
  expression state kills the firewall design — no repair, per the slice brief.

## 5. Honesty notes
- I am red team: these probes test the DESIGN, not an implementation — nothing is built
  yet, so "clean" today means "no flaw found in the spec," not "proven safe."
- A1 is the most likely real leak: budget-as-shared-pool is an attractive engineering
  choice and the seam as specified does not partition consumables. If the design splits
  budgets per phase, say so explicitly — silence here is the vulnerability.
- Probe B's `st_snap`-and-refuse hardening has a cost (slice 20 flags snapshot-freeze);
  I claim the cost is mandatory, not optional, because aliasing in Zag is idiomatic,
  not exceptional.
- C2's ledger interaction touches the honest tension in TRACK1_SYNTHESIS (byte-identical
  ledger vs state-dependent deliberation): if VARIATION_CHOICE entries must be in the
  ledger AND digests must exclude them, the ledger is no longer a pure function of
  digest-hashed state — reconcile before building.
- I am NOT claiming timing attacks via wall-clock exfiltration to an outside observer;
  the claim is strictly in-band: expression state → shared resource/buffer/digest →
  memory decision, all inside one deterministic binary.
- Weakest probe: A2's busy-loop padding assumes vary cost is the only duration variable;
  OS scheduling jitter on Linux is real but out of scope — determinism law covers the
  binary, not the kernel.

## 6. Next build step
Build the three probes as one harness against the five-organ reference build
(`docs/lab/wave9/integration/impl/`): canary-slot render runs, budget/clock
instrumentation, and digest pinning with the log-exclusion assertion. The single most
informative result is the FIRST nonzero diff in any probe — it names the edge the
firewall must close before the Arm C trial may proceed.
