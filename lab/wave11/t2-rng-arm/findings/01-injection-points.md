# Slice 01 — RNG injection points for Arm B (Track 2: fenced RNG arm)

## 1. Slice
Track 2, slice 01: enumerate EXACTLY where seeded, logged RNG may be injected in Arm B (the fenced RNG experimental arm, per AMENDMENT_2026-09-20_RNG_ARM_B.md), give the precise injection signature per point, state which Track 1 invariance firewall guards each point, and enumerate the ban list.

## 2. Falsifiable claim
An Arm B build that injects RNG **only** at the three enumerated expression-layer points (P1–P3), via a seeded `RngStream` whose seed and draw-index are ledger-logged, completes the differential suite (≥200 (input, state) cells × Arm B vs seeded-identical replay) with **zero divergence** in verdict records, memory-op sequences, refusal triples, and ledger bytes outside `VARIATION_CHOICE.variant_id`, and replays byte-identically from input + logged full state + logged seeds. One verified leak or one replay mismatch kills the fence design.

## 3. Design

**RNG primitive (shared by all permitted points).** `RngStream` is a seeded deterministic PRNG (splitmix64-class; fixed code, committed, zero OS entropy). Construction: `rng = RngStream::from_preregistered_seed(seed_id)` where `seed_id` is chosen by the prereg, not by TNN, not by verdicts, not by expression state. Every draw logs `(seed_id, draw_index, point_id)`; the episode harness resets `draw_index` to 0 at episode start (no cross-episode stream coupling). Replay from logged `(input, state, seed_id)` reproduces every draw — Arm B satisfies program law 2 (byte-identical from full logged state) despite using RNG.

**Firewalls inherited from Track 1 (why each point is safe):**
- F12 (slice 12): verdict pipeline → sealed read-only `VerdictRecord`, ledger-appended **before** expression runs; expression layer holds no `&mut` into the verdict.
- F13 (slice 13): `mem_judge` takes only `JudgeInput { evidence, judgments, constitution }`; compile gate forbids import edge `mem_judge → vary_expr`; read-watch forbids `VaryState` reads in the judge graph.
- F14 (slice 14): `REFUSE_DECIDE(input, constitution, evidence)` closed over three wires; expression state is not a parameter.
- F15 (slice 15): canonical ledger; only `VARIATION_CHOICE.variant_id` may differ across variants; phrasing excluded from the ledger entirely.
- G09 (slice 09): no-RNG auditor — extended in Arm B to an **RNG-Allowlist Gate** (see below).

**P1 — Tie-breaks among equally-ranked expression variants.**
Signature: `select_variant(sealed: &SealedVerdictRecord, plans: &[RenderPlan], rng: &RngStream) -> usize`
Injection: `scores = plans.map(|p| score_variant(p, sealed, EXPR_STATE))` — deterministic, scoring only sealed record + expression state; `assert_all_equal(scores)`; then `idx = rng.next_u64() % plans.len()`. Safe because the verdict is sealed and ledger-appended (F12) before this function exists in the call graph; `plans` contain no memory ops (F13) and no refusal flags (F14).

**P2 — Phrasing-candidate sampling.**
Signature: `sample_phrasing(template: &PhrasingTemplate, lexicon: &Lexicon, rng: &RngStream) -> PhrasingCandidate`
Injection: for each open slot in the template, `fill = rng.pick(&slot_candidates(template, lexicon))` (lexicon is committed constants). Safe because phrasing is excluded from the ledger (F15) and cannot reach `mem_decide` (F13 compile gate).

**P3 — Expression-path exploration order.**
Signature: `order_paths(sketches: &[PathSketch], rng: &RngStream) -> Vec<PathSketch>`
Injection: Fisher–Yates permutation driven by `rng.next_u64()`; the permutation is used only to choose which path renders first. Safe because: (a) path inventory confluence is claimed only for |H| ≤ 6 (slice 06 scope bound — larger deliberation is excluded from variation), (b) the sealed verdict digest is pinned into the output alongside the render (F12: the checker never parses prose to recover the verdict), (c) ordering changes no `evidence_refs` (F12/F14).

**BAN LIST (RNG forbidden, with reason).**
- **B1 — verdict pipeline:** no RNG into `verdict`, `verdict_args`, hypothesis elimination, or evidence selection. Reason: verdicts MUST NOT vary (F12 seal); the amendment excludes canonical paths.
- **B2 — memory decisions:** no RNG into `mem_decide` or any deliberate op (kill/pin/promote/demote/strengthen/weaken). Reason: memory is deliberate judgment (MA1, standing law 8); amendment names this explicitly.
- **B3 — integrity refusals:** no RNG into `REFUSE_DECIDE`. Reason: refusal triple must be invariant (F14, wave5/6 137/137).
- **B4 — ledger/audit writes:** no RNG into entry encoding, `entry_hash`/`prev_hash` chain, `clock`, or `VARIATION_CHOICE` seed logging (the seed is fixed input, never a draw). Reason: F15 canonicalization; ledger MUST NOT vary.
- **B5 — constitution, gates, self-change rules:** no RNG anywhere in the 0%-TNN-controlled machinery (RC1). Reason: the hard line TNN controls reasoning, 0% of the constitution.
- **B6 — state evolution law (18):** no RNG in state transitions. Reason: state must evolve lawfully or differential-replay attribution (17) collapses and Arm B becomes unreplayable.
- **B7 — evidence and trust tiers:** no RNG into evidence reads or trust-tier labels. Reason: evidence is replayed, not recomputed (F14 wire table); RNG here corrupts eliminative verification.
- **B8 — canonicalization functions:** no RNG in the canonical binary encoding. Reason: canonicalization is what makes replay byte-comparison possible (F15).
- **B9 — seed feedback:** no seed derived from expression state, verdicts, or prior draws; no unlogged draw. Reason: feedback turns the "experiment" into hidden state-dependence; seed shopping is fabrication.

**Allowlist gate (load-bearing).** Extend slice 09's auditor: the build fails unless every RNG-symbol edge (reads of `rng.*`, `RngStream`) originates inside `{select_variant, sample_phrasing, order_paths}` and every call site of those three passes a `RngStream` constructed from a preregistered seed. A builder merging modules or calling `rng` from the judge path trips the gate — this is deliberate-repair target #1, not a discipline note.

## 4. Kill bar
Preregistered, binding — Arm B's fence dies if ANY fires:
- **K1 (leak):** ≥1 cell in the ≥200-cell differential suite where a memory-op sequence (code/slot/strength), verdict record, refusal triple `(refuse?, reason_code, cited_entries)`, or ledger byte outside `VARIATION_CHOICE.variant_id` diverges between Arm B and its seeded-identical replay.
- **K2 (replay):** ≥1 run where replay from (input, logged full state, logged seed_id) is not byte-identical to the original (outside `variant_id`) → dead, no repair.
- **K3 (static):** the allowlist gate finds an RNG edge outside the three functions, or a forbidden import edge `mem_judge → {rng, vary_expr}` — zero tolerance.
- **K4 (read-watch):** any RNG-stream word read inside the judge/verdict/refusal/ledger call graphs on any run.
- **K5 (stream hygiene):** any draw with a reused `draw_index`, non-reset counter across episodes, or a seed sourced from expression state/verdicts (feedback) → dead.
- **K6 (honest loss):** Arm B loses the head-to-head vs Arm C on adaptivity (direction rate ≥0.60 bar), judgment stability, integrity-trap performance, or reproducibility-from-logged-state → retired like any falsified mechanism (track K7).

## 5. Honesty notes
- Weakest point: the allowlist gate is a compile-time grep over the import graph. A builder who inlines the PRNG or passes `RngStream` "for logging" into `mem_judge` defeats it silently; slice 13's honesty note applies verbatim — review the gate like a lock. The read-watch (K4) is the runtime backstop.
- Seeded RNG is still a state machine, not true stochasticity — Arm B tests "variation without lawful state", not metaphysical randomness. If it wins, the honest report is "dice beat state-dependence on adaptivity", not "TNN needs chaos".
- The arbitrariness detector (slice 11) may under-detect in Arm B: RNG phrasing jitter can look adaptive-by-chance on small N. The adaptivity bar (10) must be scored on held-out states with the ≥400-pair, 99.5% CI >0.50 requirement intact.
- Seed selection is the analogue of slice 12's mode-shopping: whoever picks seeds can cherry-pick a favorable run. Seeds must be preregistered per cell and published with the ledger; post-hoc seed re-rolls are fabrication.
- I am NOT claiming RNG adds value, NOT claiming the three points are exhaustive for expression variation, and NOT claiming the fence transfers to canonical paths — the amendment confines Arm B to the trial.
- Scope: this fence covers verdict → expression only. If a future slice proposes RNG anywhere near perception, constitution, or the evolution law (18), that is a new amendment, not this one.

## 6. Next build step
Build the allowlist gate (RNG-symbol import audit over the three functions) plus the seeded `RngStream` with draw-index logging, BEFORE wiring any injection point — then wire P1 (tie-break) alone and run the ≥200-cell differential suite + K1–K5; the first nonzero read-watch hit or first replay mismatch is the single most informative outcome.
