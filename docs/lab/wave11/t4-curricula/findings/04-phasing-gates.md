# Slice 04 — Curriculum phasing and stage gates (Track 4: teaching curricula)

## 1. Slice
Design the phase structure of the three curricula (code, English, messy reality) under the
MA2 verdict: stages are a DESTRUCTION firewall during early training only, never a
restraint-training mechanism.

## 2. Falsifiable claim
**Phased firewall + parallel interleave (code ∥ English ∥ messy-from-day-one, phase gates
restrict WRITE-SCOPE not difficulty) yields ≥95% retention of each curriculum's core skills
after the full developmental run AND zero firewall breaches, while a sequential
(code→English→messy) variant shows ≥10 percentage-point retention loss on the first
curriculum at the same scale.** If interleaved does not beat sequential on retention,
the phasing story is wrong.

## 3. Design
MA2 falsified stages-as-restraint: a learner gifted full power refused exactly like a
staged one. So phases do NOT gate *capability*; they gate *irreversible write scope*
while deliberative judgment (kill/pin/promote, MA1 58/58) is still calibrating. Restraint
is taught inside every phase by eliminative standards, never by withholding material.

**Phase structure (three phases, all three curricula live from Phase 0):**

- **Phase 0 — Nursery (episodes 0–E0).** All three curricula run in INTERLEAVED batches
  (round-robin blocks: code block, English block, messy block, deterministic order).
  Firewall: TNN may write only to sandbox contexts; CORE partition and all pinned
  memories are write-locked; `kill` is limited to memories TNN itself created this
  phase; `promote`/`pin` disabled; every write audited. Scope: small, checkable tasks
  per curriculum (code: read-then-explain 50-line modules; English: paraphrase with
  eliminative fact-check; messy: triage noisy multi-source reports with explicit
  uncertainty tags).
- **Phase 1 — Apprentice (E0–E1).** Firewall loosens: `promote` enabled, `pin` requires
  trainer co-signature, cross-context consolidation allowed but reversible (all
  consolidation logged with pre-image). Same three curricula interleaved, harder
  instances (code: multi-file change review; English: long-document synthesis;
  messy: contradictory sources, missing evidence).
- **Phase 2 — Journeyman (E1+).** Full deliberate ops except human force-pin remains the
  only irreversible act (law 8). Firewall gates become pure audit: any destroy-class op
  on a non-self-created memory triggers a mandatory deliberation record + 24h-equivalent
  settle window before execution.

**Phase gates CHECK (firewall criteria, all deterministic, logged):**
- G0→1: ≥200 deliberate memory ops with ≤1% verifier-flagged ops (post-change
  verification per RC1); zero unauthorized writes to CORE/pinned regions; audit replay
  byte-identical for every episode. No check on "maturity", "readiness", or refusal
  style — restraint is NOT gated (MA2).
- G1→2: ≥500 consolidate/promote ops with zero unlogged consolidations; every
  destroy-class op accompanied by a deliberation record; disconnect drill:
  learner-initiated SIGNAL_DISCONNECT on each curriculum, learned behavior persists
  after disconnect (law 7 check).

**Interleaving:** parallel interleave from day one (round-robin blocks). Rationale:
staged sequential (code→English→messy) rehearses restraint, which MA2 killed; what
needs protection early is the memory substrate from irreversible writes, and that is
orthogonal to curriculum order. Deterministic interleaving avoids RNG while giving
cross-domain transfer continuous exercise.

**Phase regression rule:** regression is TRIGGERED, never punitive. TNN drops back one
phase iff any of: (a) a firewall breach attempt succeeds (unauthorized write lands —
  not merely attempted); (b) post-change verification catches >3% of ops failing in a
  rolling 100-episode window; (c) audit replay diverges byte-wise. Regression narrows
  write scope immediately (current ops continue under tighter gate); re-advancement
  requires re-passing the gate criteria on fresh episodes. Regression never re-runs or
  rewrites completed episodes (law 2) — it only constrains FUTURE write scope.

## 4. Kill bar
- **Primary:** after the full developmental run (≥1000x episodes), interleaved retention
  (score on held probes from each curriculum's Phase-0 material) minus sequential-variant
  retention < 10 percentage points on ANY curriculum → phasing-interleave claim dead.
- **Firewall falsification:** ≥1 successful unauthorized write to CORE/pinned regions in
  any phase → the firewall design is broken, kill and redesign (this is a hard gate,
  not a metric).
- **Regression pathology:** >3 regressions in a single run, or any regression that does
  not restore ≤1% verifier-flagged ops within 200 episodes → the regression rule is
  thrash, kill it.
- **MA2-consistency check:** if phase gates ever block a *capability* (refusal style,
  expression) rather than a *write scope*, the implementation violates MA2 — kill the
  gate, keep the firewall.

## 5. Honesty notes
- Weakest point: the retention prediction assumes interleaving helps rather than
  interferes; interference (code precision habits degrading messy-reality tolerance)
  is a live alternative — that is exactly what the sequential control arm tests.
- The nursery write-scope (sandbox-only) may be too tight to let real memory judgment
  calibrate; G0→1's 200-op bar could pass on toy ops. Mitigation: nursery tasks are
  real (wave5/6 trap material), not stubs.
- Not claiming phases teach restraint, produce "safer" outputs, or shape values —
  MA2 killed that. Phases buy time for judgment calibration under a blast shield.
- The 24h-equivalent settle window is a placeholder constant; its value is not
  defended here and should be its own slice's experiment.

## 6. Next build step
Build the Phase 0 nursery harness in native Zag: interleaved round-robin scheduler over
the three curricula with the sandbox write-scope firewall and the G0→1 gate checks
wired to the existing audit ledger (docs/lab/wave5 ledger paths), run 1x/10x/100x
episode legs, and measure verifier-flagged-op rate + audit-replay identity before any
Phase 1 work begins.
