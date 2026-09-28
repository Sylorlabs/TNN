# HTD-1 DEBATE — Generation slice: autoregressive / sequential styles

**Worker slice:** sequential generation only. **Phase:** DEBATE — hypotheses only, nothing built.
**Date:** 2026-09-20. **Standing laws:** pure Zag, zero randomness in decision paths
(byte-identical reruns: same input + same logged state → byte-identical output),
preregister with kill bars before building, head-to-head testing, honest failures,
evidence committed under `docs/lab/htd-1/`.

## What "generation" means here (no decoder exists yet)

Generation is defined operationally as **emission of symbolic output units from TNN
memory state**, where each emitted unit is traceable to ledger entries. The unit of
emission is NOT an LLM token — the representation arms are still deciding what the
atoms of knowledge are. Each hypothesis below treats "unit" abstractly
(chunk / span / candidate) so it can bind to whatever the representation program
delivers. The shared proxy task (below) measures whether sequential emission works
*at all* and at what cost, before any decoder exists.

## Shared proxy task: HELD-OUT SPAN RECONSTRUCTION (HOSR)

1. **Store:** TNN ingests a document from the shared corpora (pg100.txt or sqlite3.c,
   read in place) via its existing deliberate-commit memory substrate. 100 test spans
   are redacted from what the generator may see (the memory substrate holds them;
   the generator path does not get the plaintext span).
2. **Generate:** the hypothesis emits the redacted spans sequentially, one unit per step.
3. **Score** on 100 spans × 2 corpora (200 trials):
   - **Fidelity:** byte-exact span match rate (span regenerated == original bytes).
     No partial credit, no BLEU — byte-identical or not.
   - **Citation validity:** % of emitted units carrying a valid audit-ledger citation
     chain back to the stored evidence (the ledger proves provenance).
   - **Cost:** median wall-clock per emitted unit; total wall-clock for 200 trials;
     ledger entries per unit (replay cost proxy).
4. **Shared baseline:** G-GREEDY — emits the best-guess unit with zero deliberation
   (no commit check, no gate, no elimination, no checkpoint). Every hypothesis must
   beat greedy on (fidelity × citation-validity) / cost, or justify why not.

Unit granularity is fixed per experiment run (all hypotheses compared on the same
unit definition: e.g., clause-level spans in pg100.txt, statement-level spans in
sqlite3.c), so cost/fidelity comparisons are apples-to-apples. Determinism check:
each trial is run twice; any byte divergence between reruns = protocol violation,
hypothesis disqualified for that run.

---

## HYPOTHESIS G-AR1 — Deliberative Chunk Commit (DCC)

**One-line:** every emitted chunk passes through the same commit/refuse/rollback
machinery TNN already uses for memory — generation *is* deliberate commitment.

### Mechanism sketch
- **Emitted per step:** one chunk (a variable-length symbolic unit, e.g., a clause or
  code statement). Chunk boundaries are proposed by trace composition over the
  active memory partition.
- **Deliberation per step:** before the chunk becomes output, TNN runs its native
  commit protocol on it: (a) evidence check — is the chunk supported by held memory
  traces? (b) deliberative refusal — does it trip any refusal standard
  (contradicts committed knowledge, cites dead evidence)? Refuse → the chunk is
  rejected and the proposer must emit a different one; Rollback → the last *k*
  committed chunks are unwound to the last consistent prefix and generation
  resumes from there.
- **State carried:** the committed output prefix (immutable once committed), the
  current proposal buffer, and the active memory partition set.
- **Ledger records:** per step: `GEN_PROPOSE(chunk_id, trace_cites)`, then exactly one
  of `GEN_COMMIT`, `GEN_REFUSE(reason_code)`, `GEN_ROLLBACK(to_chunk_id)`. The output
  is the ledger — replaying the ledger regenerates the exact output byte-for-byte.

### Falsifiable predictions
- GOOD: refusal rate sits in a sane band (catches bad chunks, doesn't starve output);
  fidelity > greedy with rollback recovering ≥ half of refusal-triggered failures.
- BAD: refusal rate collapses to ~0 (deliberation is theater — the proposer never
  loses) or explodes (the generator is a skeptic, not a generator); rollback never
  fires or fires constantly without fidelity gain.

### KILL BARS (all preregistrable on HOSR, 200 trials)
- **K1 (cost):** FAILS if median per-chunk wall time > 3× G-GREEDY **and** fidelity
  gain < 5 percentage points over greedy. Deliberation must pay for itself.
- **K2 (starvation):** FAILS if refuse rate > 25% of proposals. A generator that
  rejects a quarter of its own proposals is not generating.
- **K3 (theater):** FAILS if refuse rate < 1% **and** fidelity < 95%. Zero refusal
  with imperfect fidelity means the gate never fires when it should.
- **K4 (provenance):** FAILS if citation validity < 99% on committed chunks.
  A committed chunk without a ledger trail is a fabrication channel.

### Head-to-head
Must face: sibling sequential hypotheses (G-AR2, G-AR3, G-AR4) on HOSR;
the diffusion slice (iterative parallel refinement — does per-unit deliberation
beat whole-output refinement?); the all-at-once slice (emit-then-critique —
is committing per chunk better than committing once?); and G-GREEDY always.

---

## HYPOTHESIS G-AR2 — Span-Tape Emission with Verification Gates (STVG)

**One-line:** a planner lays variable-length spans onto a tape fast; an independent
verification gate — not the planner — decides whether each span is fixed.

### Mechanism sketch
- **Emitted per step:** one *span* (planner-chosen length, 1..N units) appended to a
  fixed tape buffer. The planner consults only the memory partitions it wakes
  (sparse activation — Micah's free-lunch question: wake the partitions relevant to
  the span, leave the rest dark).
- **Deliberation per step:** split in two. The planner does NO self-check (fast,
  cheap). Then the **verification gate** — a separate deterministic checker with
  read access to the full audit ledger — validates the span against held evidence
  and consistency rules. Gate verdicts: ACCEPT (span fixed, immutable), REJECT
  (span discarded, planner re-proposes with the rejection reason as added
  constraint), ESCALATE (span held in a pending buffer; generation of later spans
  continues past it — the tape tolerates holes, resolved at a final pass).
- **State carried:** the tape (fixed spans + pending holes), the rejection-constraint
  stack, the set of woken partitions per span.
- **Ledger records:** `GEN_SPAN_PROPOSE(tape_pos, len, partitions_woken)`,
  `GATE_ACCEPT / GATE_REJECT(reason) / GATE_ESCALATE`, `GEN_SPAN_FIX` on final
  resolution. Partition wake/​sleep events are logged so sparsity is auditable.

### Falsifiable predictions
- GOOD: the planner is fast and mostly right; the gate catches the residue;
  partition sparsity is real (median woken partitions ≪ total) with no fidelity
  loss vs full-wake control; ESCALATE resolves without deadlock.
- BAD: gate false-rejects good spans (planner and gate fight); planner leans on
  ESCALATE to dodge the gate (holes never close); sparsity is fake (planner wakes
  everything anyway).

### KILL BARS (HOSR, 200 trials)
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

### Head-to-head
Must face: G-AR1 (is splitting propose/verify better than deliberating per chunk?),
G-AR4 (whose efficiency mechanism is real — sparse partitions vs cheap cascade?),
the diffusion slice (gate ≈ refinement step? or fundamentally different?),
and a full-wake ablation of itself (sparsity must earn its keep).

---

## HYPOTHESIS G-AR3 — Eliminative Next-Unit Selection (ENUS)

**One-line:** don't propose one unit and judge it — propose a small deterministic
candidate set and *eliminate* until one survives. Selection by survival, not by
scoring.

### Mechanism sketch
- **Emitted per step:** one unit, the survivor of an elimination round. Candidate
  set (size 3–7) is generated **deterministically from state** — state-driven
  variation only (the LH program proved the deterministic uncertainty path does
  100% of useful exploration; the RNG verdict was DID-NOT-HELP). No sampling, no
  temperature: same state → same candidate set, byte-identical.
- **Deliberation per step:** eliminative hypothesis logic, TNN's existing machinery:
  each candidate is a hypothesis ("unit U continues the output correctly"); evidence
  from memory traces and the committed prefix eliminates candidates. Elimination
  rules are ordered and deterministic: contradiction with committed prefix kills
  first, unsupported-by-evidence kills second, weakest-trace-support loses ties.
  If exactly one survives → emitted. If zero survive → rollback to last committed
  unit and re-run the round with widened state (wake one more partition). If >1
  survive after all rules → emit is BLOCKED and the round is escalated to the
  trainer-visible pending queue (never silently pick).
- **State carried:** committed prefix, candidate set per step, elimination
  rule-firings per candidate.
- **Ledger records:** `GEN_CANDIDATES(step, [c1..cn])`, `ELIMINATE(c_i, rule, evidence)`,
  `GEN_SURVIVOR(c_j)` or `GEN_NO_SURVIVOR → GEN_ROLLBACK`. The full elimination
  trace is the audit trail — every non-emitted candidate has a recorded killer.

### Falsifiable predictions
- GOOD: elimination usually converges to one survivor quickly (2–3 rule-firings);
  the survivor beats greedy's single guess on fidelity; no-survivor rollbacks are
  rare and recover.
- BAD: candidate sets are degenerate (all candidates identical → elimination is
  theater; or always 5 survivors → the rules can't discriminate); the survivor is
  just the greedy guess with extra steps.

### KILL BARS (HOSR, 200 trials)
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

### Head-to-head
Must face: G-AR1 (one candidate + commit vs many candidates + elimination —
  which deliberation shape wins?), the diffusion slice (elimination rounds ≈
  denoising steps? test whether they're the same idea in different clothes),
  and G-GREEDY with an ablation: candidate-set-size = 1 (does the set matter
  or just the elimination rules?).

---

## HYPOTHESIS G-AR4 — Cheap Cascade with Checkpoint Backtrack (C3B)

**One-line:** generate fast and cheap through a minimal path; verify only at
checkpoints; on failure roll back to the checkpoint and regenerate that segment
through the expensive deliberate path. Deliberation is the exception, not the rule.

### Mechanism sketch
- **Emitted per step:** one unit via the **fast path** — best-guess emission with
  minimal state (committed prefix + local trace window only; deep memory
  partitions stay asleep). Every *m* units (checkpoint interval, preregistered,
  e.g. m=8) the **checkpoint verifier** runs the full deliberate check over the
  segment since the last checkpoint: evidence support, prefix consistency,
  citation validity.
- **Deliberation per step:** none on the fast path (that's the point). Deliberation
  happens at checkpoints and on backtrack: if a segment fails verification, roll
  back to the checkpoint and regenerate the segment through the **slow path**
  (G-AR1-style deliberate commit per unit, full partitions awake). The slow path
  is also what handles any unit the fast path flags as low-confidence *before*
  emitting (a cheap deterministic confidence rule, no RNG).
- **State carried:** committed prefix, current segment buffer, checkpoint ledger
  positions, per-segment path tag (FAST/SLOW).
- **Ledger records:** `GEN_FAST(unit)` × m, `CHECKPOINT_VERIFY(seg_id, verdict)`,
  on failure `GEN_ROLLBACK(checkpoint_id)` + `GEN_SLOW(unit)` × m. Path tags let
  the audit show exactly which output came from which path.

### Falsifiable predictions
- GOOD: fast path is right most of the time; checkpoints rarely fire; total cost
  ≪ always-deliberate with fidelity ≈ always-deliberate. This is the direct
  answer to Micah's free-lunch question: how far can deliberate *laziness* go?
- BAD: checkpoints fire constantly (fast path is wrong too often → you pay fast
  cost + slow cost); or checkpoints never fire but fidelity is low (the verifier
  is blind); or cascading backtracks (a failed segment's regeneration fails the
  next checkpoint → the cascade never settles).

### KILL BARS (HOSR, 200 trials; checkpoint interval m=8 preregistered)
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

### Head-to-head
Must face: G-AR1 (the always-deliberate control — the whole hypothesis is "beat
this on cost at parity fidelity"); G-AR2 (sparse partitions vs cheap cascade —
  which efficiency mechanism wins, and does the hybrid beat both?);
  the all-at-once slice (is checkpoint-backtrack just all-at-once with extra
  steps?); G-GREEDY (the fast path alone, to prove checkpoints add value).

---

## Cross-hypothesis notes for the TEST phase

- **Shared protocol first:** all four run HOSR on identical spans, identical unit
  granularity, identical corpora reads. Preregister unit definitions per corpus
  before any run (pg100.txt: clause-level; sqlite3.c: statement-level).
- **No-free-lunch applies inside the slice too:** the prereg should name
  scenario-conditioned expectations (e.g., G-AR4 expected to win on cost for
  high-fidelity memory; G-AR3 expected to win fidelity on adversarial/ambiguous
  prefixes) and test them, not just crown one champion.
- **Interaction with representation arms:** unit definitions here are placeholders
  until the 53 representation arms name the atoms. If the representation verdict
  changes the unit, HOSR reruns with the new unit — bars stay, units swap.
- **Ledger-growth audit:** every hypothesis must report ledger entries per unit;
  a sequential scheme whose replay cost grows superlinearly in output length
  fails the scaling law (Micah: must survive 100x).
- **Byte-identical rerun gate:** any hypothesis failing the determinism check
  (two runs diverge) is disqualified for that run, no excuses — this is law,
  not a bar.

## Strongest objection to sequential generation (steelman)

Sequential generation bakes in the worst possible error geometry: each committed
unit constrains every unit after it, so an early mistake compounds down the whole
output while the cost of preventing it is paid linearly at every step. A
parallel or diffusion-style scheme can hold the entire output in a revisable
buffer, fix errors globally, and parallelize the work — sequential generation
cannot revise without expensive rollback, cannot parallelize at all, and grows
the audit ledger O(units), making replay cost scale with output length. Worse,
per-unit deliberation multiplies TNN's heaviest machinery (commit protocols,
elimination, verification) by the number of output units, which is exactly the
opposite of Micah's free-lunch instinct: instead of waking only what's relevant,
sequential deliberation wakes the whole cognitive apparatus once per unit.
If any whole-output method reaches parity fidelity, sequential generation is
strictly dominated on cost, parallelism, and error recovery — and should be
killed as a class, not tuned.
