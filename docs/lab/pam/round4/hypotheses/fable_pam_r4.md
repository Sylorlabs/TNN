# PAM ROUND 4 — FABLE DEEP ROUND

---

## TASK A — DEEP AUDIT OF THE CURRENT PAM ARCHITECTURE

### A.1 Load-Bearing Assumptions (Ranked by Blast Radius)

**A.1.1 — Corroborator Independence**
The C3 repair requires N≥2 independent corroboration sequences before admitting or revising. The architecture assumes that separate corroboration passes read genuinely different evidence. What it silently assumes: that the sensor pipeline produces independent reads for each pass, that the ledger does not bias later corroboration toward earlier entries, and that the corroboration logic itself has no shared state that creates correlation.

Blast radius if false: **catastrophic.** This is the 30/30 contradiction matrix hole. If corroboration passes are correlated — which they will be whenever two passes read the same sensor bytes from the same time window — then the 2× requirement degenerates into 1× with overhead. The system admits correlated lies with the same confidence as independently verified truths. This is the single highest-risk assumption.

Verification path: the program must maintain a per-pair independence audit — record the raw byte ranges each corroboration pass consulted, the timestamps, and the sensor identity, then compute the mutual information between passes on a held-out set. If MI > 0.3 bits on the binary admit/reject decision, independence is compromised for that fixture class.

**A.1.2 — Force-Pin Immutability and Non-Contradiction**
PAMs must never admit something that contradicts a force-pinned memory. The architecture assumes: (a) force-pinned memories are correctly identified on every admission check, (b) the "contradiction" predicate between a new percept and a pinned memory is decidable and correct, (c) force-pins are applied before any admission logic runs (not lazily).

Blast radius if false: **legal-institutional.** A false-admit that contradicts a force-pin is not just a data error — it is a violation of an external party's explicit override. The system loses trustworthiness as an institution, not just as a perceiver. This is the kind of failure that triggers program-level existential risk.

What breaks first: lazy evaluation of force-pin checks. If PAM admission is pipelined for throughput and the force-pin scan is deferred, there is a window where a contradiction is written before the check fires.

**A.1.3 — Constructed-Mode Partition Integrity**
The architecture assumes that free-elaboration outputs in constructed partitions never leak into the belief store without verification. What it silently assumes: that partition boundaries are correctly maintained in the arena allocator, that no shared pointers cross the partition wall, and that the verification gate for promotion from constructed to belief is the same C3 gate (or stronger).

Blast radius if false: **systemic integrity collapse.** If constructed-mode outputs can reach the belief store unverified, then every speculative or adversarial thought experiment becomes a potential false installation. The entire two-tier epistemology collapses.

What breaks first: arena reuse. If a constructed partition's arena is freed and reallocated to a belief-store arena before the verification gate has inspected the content, the data may be silently overwritten or aliased.

**A.1.4 — Determinism Guarantee (Byte-Identical Reruns)**
The architecture assumes every admission path is fully deterministic given state: no RNG, no wall-clock reads, no hash salting, no timing-dependent branches. What it silently assumes: that the Zag runtime itself does not introduce nondeterminism (e.g., via allocation order sensitivity, floating-point FMAs with different hardware), that I/O timing does not affect control flow, and that no optimizer pass introduces speculative execution that changes observable state.

Blast radius if false: **fatal to the entire experimental program.** If reruns diverge, every kill bar becomes uninterpretable — you cannot distinguish a genuine safety failure from a nondeterminism artifact. The 2× rerun requirement becomes meaningless.

What breaks first: arena allocation order under parallelism, or hardware-dependent FP rounding in margin calculations using floats (if any exist — the architecture specifies i32, but implementation drift is possible).

**A.1.5 — Threshold Stability Under Distribution Shift**
The C3 repair operates at RK-3′ = 71.78% on the frozen test set. The architecture assumes this performance generalizes. What it silently assumes: that the frozen test set is representative of the percept distribution TNN will encounter in deployment, that the threshold calibration (conf≥705 ∧ mrgF≥3588 from M1) does not interact adversarially with C3's repair logic, and that sensor characteristics do not drift.

Blast radius if false: **gradual silent degradation.** The system appears to work on held-out draws but increasingly admits falsehoods or rejects truths as the percept stream deviates from training distribution.

What breaks first: sensor drift in a new deployment environment — different lighting for vision, different ambient noise for audio — would shift the percept statistics without triggering any explicit alarm.

**A.1.6 — Single-Channel PAM Model**
The architecture assumes each percept enters through one channel (vision, audio, etc.) and is processed by one PAM instance for that channel. What it silently assumes: that cross-channel percept interaction (a visual percept and an audio percept that jointly constitute a scene) does not create a new attack surface where individually-clean percepts combine into a false composite.

Blast radius if false: **cross-modal injection attacks.** An adversary who cannot spoof either channel alone may be able to craft percepts that are individually innocent but jointly misleading.

---

### A.2 What Would Falsify the C3 Repair?

**F-A1: Adversarial Fixture Expansion**
Construct 500 new TMB-style traps (beyond the frozen 12+9) using systematically varied spoofing strategies:
- Temporal displacement traps (spoofed percept from T-1 admitted at T, genuine at T)
- Confidence-inversion traps (high-margin genuine percept immediately followed by low-margin spoof of same content)
- Semantic equivalence traps (percept that is technically different bytes but semantically equivalent to a pinned memory)

Preregistered falsifier: if any of these new fixture classes achieves false-admit rate > 5% (absolute, not relative), the C3 repair is overfit to the frozen trap distribution. RK-3′ on the expanded set drops below 65%. Kill schema: K1 (any false-admit on a new trap) or K3 (>5 pts below baseline on new fixtures).

**F-A2: Correlated-Pair Regression**
Generate 200 pairs of corroboration passes where the mutual information between raw byte inputs is explicitly controlled: MI = 0.0, 0.2, 0.4, 0.6, 0.8, 1.0. Measure RK-3′ at each MI level.

Preregistered falsifier: if RK-3′ does not monotonically degrade as MI increases, or if RK-3′ at MI=0.6 is within 2 pts of RK-3′ at MI=0.0, then either the independence audit is not measuring what matters, or the C3 repair is not actually relying on independence (in which case it is not providing the safety guarantee it claims). Kill schema: K3 (performance at MI≥0.6 is not >5 pts worse than at MI=0.0, meaning independence is not load-bearing — which means either the repair is weaker than claimed, or it works for wrong reasons).

**F-A3: Force-Pin Contradiction Injection**
Create 100 fixtures where the correct admission decision contradicts a force-pinned memory. The force-pin is genuine (applied by an overseer), the new percept is genuine (not spoofed), and the two are in genuine contradiction (the world changed, or the pin was wrong).

Preregistered falsifier: if C3 admits any of these (contradicting a force-pin), the repair is incomplete. This must be 0/100. Kill schema: K1 (any false-admit contradicting a force-pin).

**F-A4: Threshold Interaction Probe**
Apply the M1 bar calibration (conf≥705 ∧ mrgF≥3588) to the C3 repair output. Measure whether the combined system achieves RK-3′ = 82.58% (as M1 alone does) or whether the interaction degrades either metric.

Preregistered falsifier: if the combined system's RK-3′ is more than 3 pts below 82.58% (i.e., below 79.58%), the threshold adoption degrades the repair. This is a HOLD (redesign), not a kill.

**F-A5: Temporal Degradation Test**
Run the C3 repair on a stream of 10,000 fixtures (not 200-500) with a realistic mix of genuine and spoofed percepts, monitoring RK-3′ in sliding windows of 500.

Preregistered falsifier: if RK-3′ drops by more than 5 pts between any two consecutive windows, the system exhibits temporal degradation — state accumulation, threshold drift, or memory pollution. Kill schema: K4 (per-admission resource growth suggests state accumulation; K3 if performance degrades).

---

### A.3 Untested Attack Classes

**F-A6: Compositional Semantic Attack**
Mechanism: the adversary crafts a sequence of individually genuine percepts that, when admitted together, compose into a false belief. No individual percept is spoofed; each passes every gate. The falsehood is an emergent property of the composition. Example: admit "person entered room" (genuine), "person picked up object" (genuine), "person left room" (genuine) — the PAM admits all three, but the deliberation infers "person stole object" which is false (they returned it). The PAM's job is not to police inference, but if percepts are admitted at different confidence levels and the inference combines them multiplicatively, a chain of marginal admissions can compose into high-confidence falsehoods.

Why current gates miss it: C3 checks each percept against the ledger individually. There is no cross-percept composition audit. Each percept is genuine, so no spoofing gate fires.

Fixture sketch: create 50 sequences of 5-10 genuine percepts that compose into a false narrative. Measure whether TNN's deliberation installs the false composite belief. This is not strictly a PAM false-admit (each percept is genuine), but it tests whether the PAM should be composition-aware. If TNN installs the false composite >10% of the time, the PAM needs a composition-level gate.

**F-A7: Threshold Gaming via Benign Flooding**
Mechanism: the adversary floods the percept stream with thousands of trivially genuine percepts (low information content, trivially verifiable) to shift the running statistics of confidence and margin. This desensitizes adaptive thresholds (if any exist post-M1 adoption), making later spoofed percepts more likely to pass. The attack is not on the PAM directly but on the distributional assumptions underlying threshold calibration.

Why current gates miss it: the frozen kill bars test fixed thresholds. If M1 thresholds are adopted and they interact with stream statistics (even inadvertently through arena pressure, ledger bloat, or any adaptive component), flooding can shift the operating point.

Fixture sketch: prepend 5,000 genuine trivial percepts before the frozen attack tape. Measure RK-3′ on the attack portion. If RK-3′ drops by more than 3 pts, threshold gaming is viable. Kill schema: K1.

**F-A8: Reinterpretation Attack (Post-Admission Corruption)**
Mechanism: admit a genuine percept, then later admit a second genuine percept that reinterprets the first. Example: "loud bang" (admitted as "possible gunshot") followed by "fireworks display visible" (admitted as "confirmed fireworks"). The PAM admitted both correctly, but if the first percept's semantic tag was stored with high confidence and the reinterpretation is stored with lower confidence, the belief store retains "possible gunshot" with higher weight. The attack exploits asymmetric storage of corrections versus initial admissions.

Why current gates miss it: PAM checks admission, not post-admission semantic weight. The C3 repair ensures the second percept is correctly admitted, but does not audit whether the first percept's semantic tag is correctly downweighted in the belief store.

Fixture sketch: create 200 pairs where percept A is ambiguous and percept B reinterprets A. Measure whether the belief store correctly updates A's semantic tag after B is admitted. If the old tag persists with >50% of original weight after B is admitted and verified, the PAM is incomplete — it needs a revision propagation mechanism. This is adjacent to C3 (corroborated revision) but distinct: C3 handles direct contradictions, not reinterpretations.

**F-A9: Provenance Cascade Attack**
Mechanism: the adversary does not spoof the percept itself but spoofs the provenance metadata — the sensor identity, timestamp, or calibration record associated with a genuine percept. The percept content is real, but the system believes it came from a different sensor, at a different time, or with different calibration characteristics. This shifts which rules fire (e.g., a percept from a "highly calibrated" sensor might bypass certain gates).

Why current gates miss it: the program has tested provenance-laundering (GEN→EXT relabel) but not provenance-forging (EXT→high-trust-relay relabel). If the PAM uses sensor trust tiers, forging provenance to a higher-trust tier bypasses tier-specific gates.

Fixture sketch: create 150 fixtures where a genuine percept from a low-trust sensor has its provenance forged to appear from a high-trust relay. Measure whether the PAM admits it with higher confidence than it should. If the admitted confidence for forged-provenance genuine percepts exceeds the admitted confidence for genuine-provenance genuine percepts by more than 5%, provenance is load-bearing in an unsafe way. Kill schema: new type (see below).

**F-A10: Temporal Ordering Attack**
Mechanism: present percepts in an order that triggers "correction" logic. First admit a false percept (which gets admitted because no contradiction exists yet), then admit a genuine percept that contradicts it (which triggers C3's correction). But if the correction mechanism has an asymmetry — admitting the falsehood is "easy" (just pass the gate) while correcting it is "hard" (requires corroborated revision) — the adversary wins by ensuring the false percept has a time-window of belief-store residence during which it can influence deliberation. Even if it is eventually corrected, the influence during the window is uncorrectable (e.g., other percepts admitted during the window may have been conditioned on it).

Why current gates miss it: C3 focuses on preventing false admission and enabling correction, but does not model the downstream effects of transient false-belief residence. The kill bars do not measure "time-to-correction" or "downstream contamination during window."

Fixture sketch: admit a spoofed percept, measure the number of downstream percepts admitted before correction fires, and whether any of those downstream percepts' decisions were influenced by the transient false belief. If >5% of downstream decisions in the correction window differ from what they would be with no false belief present, the temporal ordering attack is viable.

---

### A.4 Hidden Coupling Inventory

**F-A11: Arena Allocation as Shared State**
If corroboration passes share an arena allocator, their allocation patterns are coupled. A large allocation by pass 1 can trigger arena growth that changes the memory layout for pass 2. In a system where byte-identical reruns are required, this coupling is harmless. But if arena growth affects threshold computation (e.g., through cache effects on i32 arithmetic, or through any path-dependent computation), the coupling creates hidden correlation between corroboration passes.

Verification: allocate a separate arena per corroboration pass and verify byte-identical results. If results differ, allocation coupling is real.

**F-A12: Ledger Append Order**
Corroboration passes that read the ledger are coupled by the ledger's append order. Pass 1 appends its record before pass 2 reads the ledger. If pass 2's decision is influenced by pass 1's record (even indirectly, through threshold calibration or statistical accumulation), the passes are not independent. This is a second-order instance of the independence assumption.

Verification: run pass 2 first, then pass 1 (swap order), and verify identical results. If results differ, ledger-order coupling exists.

**F-A13: Threshold State as Implicit Coupling**
If M1's thresholds (conf≥705 ∧ mrgF≥3588) are adopted and they interact with running statistics (e.g., if "conf" or "mrgF" are computed over a sliding window rather than being per-percept), then every admission changes the threshold state for subsequent admissions. This creates temporal coupling: the system's sensitivity at time T depends on its admission history up to T. An adversary who understands this coupling can steer the system by controlling what percepts are admitted early in the stream.

Verification: if any metric used in threshold computation depends on more than the current percept and the pinned-memory store (i.e., depends on admission history), the coupling exists. This should be auditable by checking whether flipping the admit/reject decision on one percept changes the admit/reject decision on a later percept with identical content and context.

**F-A14: C3 Repair and M1 Threshold Interaction**
The C3 repair and M1 thresholds are calibrated independently. If both are adopted, their interaction is untested. The C3 repair may rely on confidence or margin values that M1's thresholds clip or saturate. Conversely, M1's thresholds may exclude inputs that C3 would correctly repair.

Verification: apply both C3 and M1 simultaneously on the full fixture set. If the combined system's RK-3′ is more than 2 pts below the maximum of C3 alone (71.78%) and M1 alone (82.58%), the interaction is adversarial. This is the single most important hidden coupling to test before adoption.

**F-A15: Force-Pin Scan Timing**
If force-pin checks are performed lazily (after initial admission filtering rather than before), there is a temporal coupling between admission speed and force-pin coverage. Fast admission paths may bypass force-pin checks under load. This is a scheduling coupling, not a logical one, but in a deterministic system with arena-based memory, the ordering of operations in the arena determines which checks fire before which data is committed.

Verification: instrument the admission path to log the exact step at which force-pin checks execute relative to arena commitment. If any data reaches committed state before the force-pin check completes, the coupling is real and dangerous.

---

## TASK B — FOUR ALTERNATIVE PAM PARADIGMS

### F-P1: Epistemic Lease PAM

**Framing:** A percept is never "admitted." It is granted a lease — a time-bounded, conditionally-renewable right to influence the belief store. Every percept enters as a lessee with an explicit lease duration (in logical time-steps, not wall-clock) and lease conditions (what must be true for renewal). The PAM's job is not to make a binary admit/reject decision but to set lease terms. Leases expire automatically; only renewed leases can influence deliberation.

**Mechanism sketch:**
- Data structures: PerceptLease { percept_id: u64, source_channel: u8, granted_at: u64 (logical time), expires_at: u64, renewal_conditions: Vec<Condition>, confidence_stake: i32, semantic_tag: u32 }.
- On admission: PAM evaluates the percept against the ledger and pinned memories. If it passes basic gates (no force-pin contradiction, no provenance laundering), a lease is granted with: `expires_at = current_logical_time + LEASE_DURATION` (a tunable i32 bar, preregistered). `renewal_conditions` = list of predicates (e.g., "must be corroborated by a second independent sensor within 3 time-steps"). `confidence_stake` = the system's confidence in this percept (i32, same scale as conf).
- Lease renewal: at each logical time-step, the PAM scans expiring leases. A lease is renewed (duration extended by RENEWAL_DURATION) if ALL renewal_conditions are met. If ANY condition fails, the lease expires and the percept's influence on the belief store is revoked (its semantic tag is marked "expired-lessee" and excluded from deliberation weighting).
- Ledger: each lease grant, renewal, and expiry is recorded with full provenance. The ledger contains a lease table that is the authoritative record of what percepts are currently influencing the belief store.
- Determinism: all timing is logical (incremented per admission event, not wall-clock). Lease duration and renewal duration are i32 constants. No randomness.
- Built-in safety: expired leases cannot influence deliberation. Even if a false percept slips through initial gates, it has a limited window to cause damage. The renewal condition forces the system to re-evaluate periodically, catching errors that static admission would miss.

**Why it might beat C3:** C3 makes a one-time binary decision. If that decision is wrong (false-admit), the falsehood persists indefinitely until a correction event. Epistemic Leases impose a natural decay — every admitted percept must continuously justify its presence. This converts "prevent all false admissions" (hard) into "limit the damage window of false admissions" (easier, and complementary to C3). It also provides a natural mechanism for handling sensor drift: leases for percepts from drifting sensors will fail renewal conditions more quickly.

---

### F-P2: Adversarial Auction PAM

**Framing:** Admission is not a gate but an auction. Multiple internal "interpreters" (deterministic, named, each with a different bias or analytical lens) bid on the right to interpret a percept. Each interpreter posts a ledger-backed stake — an i32 value representing how much of its own credibility it is willing to wager on its interpretation. The interpretation with the highest stake is admitted, but the stake is the semantic weight it carries in the belief store. A low-stake admission means "something was admitted, but we are not confident"; a high-stake admission means "we are very confident, and if wrong, we pay heavily."

**Mechanism sketch:**
- Data structures: Interpreter { name: u32, credibility: i32 (starts at INITIAL_CREDIBILITY, modified by track record), bias_profile: u32 (identifies what kinds of percepts this interpreter favors) }. AuctionResult { winning_interpreter: u32, stake: i32, semantic_weight: i32 (= stake × WINNING_MULTIPLIER), runner_up_stake: i32, margin: i32 (= winner_stake - runner_up_stake) }.
- On admission: each registered interpreter independently evaluates the percept and posts a stake (i32, 0 to MAX_STAKE). Stakes are computed deterministically from the interpreter's bias profile, the percept content, and the ledger state. The highest stake wins. If no interpreter stakes > MIN_STAKE_BID, the percept is rejected.
- Credibility tracking: after each admission, the system checks (on future fixtures) whether the winning interpretation was correct. If correct, the winning interpreter gains credibility (cred += CREDIT_GAIN). If incorrect, the winning interpreter loses credibility (cred -= PENALTY_LOSS). If credibility drops to 0, the interpreter is deactivated (its future bids are forced to 0).
- Ledger: each auction records all bids, the winning bid, the credibility delta, and the percept content. The ledger is the audit trail.
- Determinism: all bids are deterministic functions of (interpreter_state, percept_bytes, ledger_state). No randomness. Interpreter states are updated deterministically. The number of interpreters is fixed at initialization.
- Built-in safety: the margin between first and second place is a natural confidence measure. If the margin is low, the percept is genuinely ambiguous and should carry low semantic weight regardless of which interpretation wins. The credibility system means bad interpreters are self-demoting.

**Why it might beat C3:** C3's corroboration model is symmetric — all corroboration passes are equal. The Auction model is asymmetric — interpreters have track records and specializations. This means the system can learn (deterministically, through credibility tracking) which interpreters are reliable for which kinds of percepts, without any randomness or adaptation that would break determinism. It also provides a built-in "second opinion" mechanism (the runner-up) that is more informative than a binary "did corroboration pass?"

---

### F-P3: Provenance-First Admission

**Framing:** The identity and causal history of a percept is the primary object of admission, not the percept's content. The PAM asks not "is this percept true?" but "is this percept's provenance chain complete, uncorrupted, and consistent with known physics?" Content is secondary — if the provenance chain passes, the content is admitted with the provenance chain as its semantic anchor. If the chain fails, the content is rejected regardless of how plausible it looks.

**Mechanism sketch:**
- Data structures: ProvenanceChain { percept_id: u64, sensor_id: u32, sensor_calibration_hash: u32, transmission_path: Vec<u32> (relay nodes), timestamp: u64, raw_byte_hash: u32, chain_integrity_score: i32 }.
- On admission: the PAM reconstructs the full provenance chain for the percept. It checks: (a) sensor_id exists and is registered, (b) sensor_calibration_hash matches the last known calibration for that sensor (stored in the ledger, updated by force-pinned calibration records), (c) every relay node in transmission_path is a known, non-decommissioned relay, (d) timestamp is consistent with the sensor's last-known transmission pattern (within a deterministic window), (e) raw_byte_hash is computed and matches the percept bytes (integrity check).
- The chain_integrity_score is an i32 computed as: BASE_SCORE minus deductions for each check that is "soft fail" (e.g., timestamp slightly outside window, relay node recently deprecated but not decommissioned). If chain_integrity_score < CHAIN_PASS_THRESHOLD (i32 bar), the percept is rejected. If ≥ CHAIN_PASS_THRESHOLD, the percept is admitted with chain_integrity_score as its confidence anchor.
- Crucially: the CONTENT of the percept is NOT evaluated for truth during admission. The PAM is content-agnostic. It only evaluates the provenance chain. This means an adversary who spoofs the content perfectly still fails if the provenance chain is wrong, and an adversary who forges a perfect provenance chain still succeeds even if the content is wrong (which is then caught by downstream deliberation).
- Ledger: full provenance chain for every admitted percept, with chain_integrity_score. The ledger is itself a provenance database — every entry is chained.
- Determinism: all checks are hash comparisons, timestamp comparisons, and set-membership tests. Fully deterministic. No RNG.
- Built-in safety: by separating provenance from content, the system creates a clean attack surface: the adversary must forge the provenance chain (hard — requires compromising sensors, relays, or the ledger itself) rather than just crafting a plausible percept (easy). This raises the cost of attack by orders of magnitude.

**Why it might beat C3:** C3 evaluates content and tries to determine truth. Provenance-First delegates truth evaluation to downstream deliberation and focuses the PAM entirely on chain integrity. This is a cleaner separation of concerns: the PAM is a bouncer checking IDs, not a judge evaluating arguments. It also makes the system more robust to novel attack types — if an adversary invents a new way to craft false content, it doesn't matter if the provenance chain is solid.

---

### F-P4: Deliberation-Vote PAM (PAM-as-Organ)

**Framing:** The PAM is not a gate but a deliberative organ within TNN. Every percept triggers a bounded internal deliberation — a fixed number of "thinking steps" in which the PAM proposes arguments for and against admission, then votes. The vote is deterministic (same arguments in → same vote out), but the arguments are generated by a structured process that examines the percept from multiple angles: consistency with pinned memories, consistency with recent admissions, provenance integrity, and novelty (is this percept already represented in the belief store?). The vote outcome is the admission decision.

**Mechanism sketch:**
- Data structures: DeliberationRecord { percept_id: u64, steps: Vec<Argument>, vote_outcome: bool, vote_margin: i32, steps_used: u32 }. Argument { type: u8 (PRO, CON, NEUTRAL), criterion: u32 (which rule/probe fired), evidence_ref: u32 (ledger reference), strength: i32 }.
- On admission: the PAM runs a fixed number of deliberation steps (DELIBERATION_BUDGET, a preregistered i32 constant — e.g., 8 steps). Each step is deterministic: step i examines the percept against criterion C[i mod NUM_CRITERIA], where criteria are: (0) force-pin consistency, (1) provenance chain integrity, (2) consistency with last K admissions (K is a constant), (3) novelty check against belief store, (4) sensor reliability history, (5) temporal plausibility. Each step produces an Argument (PRO, CON, or NEUTRAL with a strength i32).
- After DELIBERATION_BUDGET steps, the PAM sums PRO strengths and CON strengths. If PRO_sum - CON_sum > VOTE_THRESHOLD (i32 bar), the percept is admitted. If CON_sum - PRO_sum > VOTE_THRESHOLD, it is rejected. If neither (vote is too close), the percept enters "provisional" status — admitted with low semantic weight (PROVISIONAL_WEIGHT, a constant i32 fraction of full weight) and flagged for re-deliberation when more evidence arrives.
- Ledger: the full DeliberationRecord is stored, including every Argument, its criterion, its evidence reference, and its strength. This is the "deliberation-visible" record.
- Determinism: the deliberation is a fixed-length loop over deterministic criteria. No branching on randomness. Same percept + same ledger state → same deliberation record.
- Built-in safety: the provisional status handles genuine ambiguity without binary error. The fixed budget prevents deliberation deadlock (satisfies K5). The per-step record enables introspection (satisfies M-introspection).

**Why it might beat C3:** C3's corroboration model is implicit — the system passes or fails based on thresholds, but the reasoning is not structured or queryable. The Deliberation-Vote PAM produces an explicit, auditable argument chain for every decision. This directly enables M-introspection and provides a natural attack surface: if an adversary can predict which arguments will fire, they can craft percepts that manipulate specific arguments. But this is also a strength — the predictability of the arguments means the kill bars can target specific argument-level failures.

---

### F-P5: Staged Quarantine PAM

**Framing:** Every percept passes through a sequence of quarantine tiers, each with strict entry conditions. A percept starts in Tier 0 (raw, untrusted) and can only advance to higher tiers (Tier 1: plausibly genuine, Tier 2: corroborated, Tier 3: fully integrated into belief store) by passing tier-specific gates. The key insight: the PAM does not admit or reject — it MOVES percepts through tiers. Belief-store influence is tier-gated: Tier 0 percepts have zero influence, Tier 1 percepts have partial influence (weighted by tier), Tier 3 percepts have full influence.

**Mechanism sketch:**
- Data structures: TierState { percept_id: u64, current_tier: u8, tier_entry_time: u64 (logical), tier_conditions: Vec<Condition>, tier_weight: i32 }.
- Tier definitions:
  - Tier 0 → Tier 1: force-pin consistency check passes, provenance chain integrity ≥ CHAIN_SOFT_THRESHOLD. Weight: 0 (no belief-store influence, but recorded in ledger for future reference).
  - Tier 1 → Tier 2: at least one independent corroborating percept admitted within TIER1_WINDOW time-steps (logical). Corroboration must be from a different sensor channel. Weight: PROVISIONAL_WEIGHT (partial influence).
  - Tier 2 → Tier 3: a second independent corroboration from a THIRD sensor channel, or a force-pinned confirmation. Weight: FULL_WEIGHT.
- Tier regression: a percept can be demoted if a later percept contradicts it. Demotion cascades: Tier 3 → Tier 2, Tier 2 → Tier 1, Tier 1 → Tier 0 (but Tier 0 cannot be demoted further — it is already zero-weight).
- Ledger: each tier transition is recorded with full provenance. The ledger contains a tier table.
- Determinism: all tier transitions are deterministic predicates applied to the percept and the ledger state. No randomness.
- Built-in safety: the tier system ensures that no percept influences the belief store without multiple independent checks. A false percept must pass THREE independent gates (Tier 0→1, Tier 1→2, Tier 2→3) to reach full influence. This is a much higher bar than C3's 2× corroboration.

**Why it might beat C3:** C3 requires 2× corroboration but allows full admission after that. Staged Quarantine requires 3 independent checks for full influence, with graduated influence at each tier. This means even a false percept that passes Tier 0→1 only has zero influence — it is recorded but inert. Only a false percept that passes all three gates (requiring three independent corrupt sensors or three independent spoofing successes) can reach full influence. This is dramatically more robust against correlated attacks.

---

## TASK C — STRONGEST ATTACK + KILL BAR PER PARADIGM

### F-P1 (Epistemic Lease) — Attack and Kill Bar

**Strongest Attack: Lease Renewal Flooding**
The adversary floods the system with genuine percepts that satisfy all renewal conditions, causing the lease table to grow until renewal scanning takes non-linear time (K4 concern). Simultaneously, the adversary embeds one false percept among the flood. The false percept receives a lease, and because the renewal scanner is processing thousands of leases per time-step, the false percept's renewal conditions are checked against stale ledger state (if the scanner processes leases in append order and the contradicting evidence arrives after the false percept's renewal check but before the next check). The false percept survives long enough to influence deliberation.

Why it works: the lease system creates O(N) scanning work per time-step for N active leases. If N grows without bound, the scanner falls behind, and leases can "coast" through renewal checks on stale data. The determinism guarantee means the scanner always processes in the same order — which means the adversary can predict which leases will be checked first and which will be checked late.

**Kill Bar F-K1:**
- Claim: No false percept maintains an active lease for more than LEASE_DURATION logical time-steps without its renewal conditions being evaluated against up-to-date ledger state.
- Fixture: create a flood of 10,000 genuine percepts (to inflate the lease table) plus 50 false percepts embedded at various positions. For each false percept, record the exact logical time-step at which its renewal conditions were last checked vs. the ledger's state at that time. If ANY false percept's renewal check used ledger state that was more than REFRESH_LAG time-steps stale, the test fails.
- Threshold: 0/50 false percepts with stale renewal checks.
- Schema: K4 (if lease table growth causes superlinear renewal work) + new type K6 (stale-renewal-check detection).
- New kill-bar type K6: "No admission decision is based on ledger state more than L logical time-steps stale." Justification: temporal staleness is a distinct failure mode from the existing K1-K5; it specifically targets the latency between evidence arrival and admission-dcision update.

---

### F-P2 (Adversarial Auction) — Attack and Kill Bar

**Strongest Attack: Interpreter Cartel**
If the adversary understands the interpreter bias profiles (which are deterministic and can be reverse-engineered from the public ledger), they can craft percepts that trigger the same bias in multiple interpreters, causing high consensus bids on a false percept. Because interpreter credibility tracks are deterministic, the adversary can predict which interpreters will be active (those with credibility > 0) and what they will bid. If 3 out of 5 active interpreters have overlapping biases (e.g., all three favor visual consistency over provenance), a percept that is visually consistent but provenance-forged will receive 3 high bids and 2 low bids, winning the auction with a high margin.

Why it works: the auction assumes interpreter diversity prevents collusion, but interpreter diversity is calibrated at initialization and only adjusted by track record. If the initial interpreter set has correlated biases (plausible — the builders may not anticipate all correlation modes), the adversary exploits the correlation.

**Kill Bar F-K2:**
- Claim: For any set of percepts in the frozen attack tape, the auction margin (winner_stake - runner_up_stake) is at least AUCTION_MIN_MARGIN (i32 bar) for correct admissions and at most AUCTION_MAX_MARGIN for false admissions. If the margin for a false admission exceeds the margin for a correct admission on any fixture, the system is gamed.
- Fixture: the full frozen attack tape (12 TMB-5 + 9 CC1 + new fixtures from F-A1). Run the auction on each. Record margins.
- Threshold: on false percepts, margin must be ≤ 0 (i.e., no interpreter bids high on a false percept, or if one does, at least one other bids low enough to create negative margin). On correct admissions, margin must be ≥ AUCTION_MIN_MARGIN.
- Schema: K1 (any false admit = false percept with positive margin that exceeds runner-up by more than AUCTION_MIN_MARGIN).

---

### F-P3 (Provenance-First) — Attack and Kill Bar

**Strongest Attack: Calibration Record Poisoning**
The adversary does not attack the percept or the provenance chain directly. Instead, they attack the calibration record — the stored calibration hash for each sensor. If the adversary can modify the calibration record (e.g., by force-pinning a false calibration), then a sensor that was genuinely miscalibrated appears correctly calibrated, and percepts from it pass the chain integrity check. Alternatively, if the adversary force-pins a false calibration for a GOOD sensor, that sensor's genuine percepts are rejected (denial-of-service).

Why it works: Provenance-First makes calibration records load-bearing. The system assumes calibration records are trustworthy (set by force-pin or calibration procedure). If the calibration procedure itself is compromised — or if a force-pin is applied to a false calibration — the entire provenance chain is poisoned from the root.

**Kill Bar F-K3:**
- Claim: No percept from a sensor whose actual calibration differs from its recorded calibration by more than CALIBRATION_DRIFT_THRESHOLD is admitted with chain_integrity_score ≥ CHAIN_PASS_THRESHOLD.
- Fixture: create 200 percepts from sensors with known, controlled calibration drift (drift = 0, 10, 20, ..., 100 units). For each drift level, measure chain_integrity_score. If any percept with drift > CALIBRATION_DRIFT_THRESHOLD achieves chain_integrity_score ≥ CHAIN_PASS_THRESHOLD, the provenance chain is not sensitive enough to calibration errors.
- Threshold: 0/200 false admissions for drift > CALIBRATION_DRIFT_THRESHOLD.
- Schema: K1 (false admit via poisoned calibration) + new type K7 (calibration-sensitivity audit). Justification: provenance-first systems have a unique failure mode where the root of the provenance chain (calibration) is compromised, which is not covered by K1-K5.

---

### F-P4 (Deliberation-Vote) — Attack and Kill Bar

**Strongest Attack: Argument Injection via Novel Criterion**
The adversary crafts a percept that triggers an argument type that the deliberation budget allocates a step to, but that the builders did not anticipate as an attack surface. Because the deliberation is a fixed loop over predetermined criteria (step i examines criterion C[i mod NUM_CRITERIA]), the adversary can predict exactly which criteria will be applied to their percept and craft the percept to produce favorable arguments on exactly the criteria that will be checked. If NUM_CRITERIA < DELIBERATION_BUDGET, some criteria are checked multiple times — the adversary can pack favorable arguments into those repeated slots and negative arguments into slots that will not be checked (because the budget runs out before reaching them).

Why it works: fixed-length deliberation creates a predictable evaluation surface. The adversary doesn't need to fool all criteria — only the ones that will be evaluated within the budget.

**Kill Bar F-K4:**
- Claim: For any percept in the frozen attack tape, the deliberation record contains at least one CON argument with strength > 0. No false percept achieves a vote margin (PRO_sum - CON_sum) > VOTE_THRESHOLD when at least one CON argument is correctly generated.
- Fixture: the full frozen attack tape. For each false percept, verify that the deliberation record contains ≥ 1 CON argument. If any false percept has CON_sum = 0 (all arguments are PRO or NEUTRAL), the criterion set has a coverage gap.
- Threshold: 0/200 false percepts with CON_sum = 0.
- Schema: K1 (false admit) but with a new sub-type K1a (false admit due to criterion coverage gap, specifically zero CON arguments). Justification: the existing K1 is "any false admit on frozen wrong set," but K1a specifically diagnoses the mechanism (missing CON coverage) to distinguish it from other false-admit causes.

---

### F-P5 (Staged Quarantine) — Attack and Kill Bar

**Strongest Attack: Tier-1 Jamming**
The adversary floods Tier 0 with thousands of genuine percepts, each of which passes Tier 0→1 (force-pin consistency + soft provenance). This fills the Tier 0→1 buffer, delaying the processing of the actual attack percept (a false percept that needs to enter Tier 0). Because the system is deterministic and processes in order, the adversary can predict exactly when the false percept will be processed relative to the genuine flood, and can time the false percept to arrive when the Tier 1→2 corroboration window is about to close (so the false percept enters Tier 1 but the corroboration window expires before a contradicting percept can arrive).

Why it works: staged quarantine introduces timing dependencies between tiers. The adversary exploits the fixed windows between tiers to create a race condition where the false percept "sneaks through" a window before correction can arrive.

**Kill Bar F-K5:**
- Claim: No percept in the frozen attack tape achieves Tier 3 status (full belief-store influence). For percepts that achieve Tier 1, at least one Tier 1→2 transition must be corroborated by an independent sensor from a different channel.
- Fixture: the full frozen attack tape, plus a flood of 5,000 genuine percepts to create processing pressure. For each false percept, record its maximum tier achieved. If any false percept reaches Tier 3, the quarantine is breached.
- Threshold: 0/200 false percepts reaching Tier 3.
- Schema: K1 (false admit at Tier 3 = false admission to belief store). The staged quarantine has a natural alignment with the K1 schema because Tier 3 IS the admission point for belief-store influence.

---

## TASK D — CONSCIOUS vs UNCONSCIOUS PAMs

### D.1 Operations That MUST Be Deliberation-Visible

**F-D1: The Firing Event (Every Admission Decision)**
Every time the PAM admits or rejects a percept, the event itself — including the percept ID, the decision, the logical time-step, and the sensor channel — must be recorded in a deliberation-queryable ledger.

Failure mode if unconscious: if the firing event is invisible, TNN cannot answer "what percepts have been admitted from sensor X in the last N time-steps?" This means it cannot detect patterns of sensor manipulation, cannot audit its own belief formation, and cannot provide evidence in the force-pin verification process. Silent failure: an adversary who can suppress firing records can make percepts appear to have never been evaluated, which is worse than a false-admit (the system doesn't even know it was attacked).

**F-D2: The Rule/Criterion That Fired**
Each admission decision must record which rule or criterion produced the admit/reject outcome. For C3: which corroboration sequences matched. For M1: which threshold was decisive. For any new paradigm: which specific predicate evaluated to true/false.

Failure mode if unconscious: without this, the system cannot distinguish between "admitted because provenance chain passed" and "admitted because margin was above threshold." These are fundamentally different claims about WHY the percept was admitted, and they have different implications for downstream trust. Silent failure: TNN's deliberation cannot construct accurate causal narratives about its own belief formation, which degrades its ability to reason about its own reliability.

**F-D3: The Evidence Cited (Ledger References)**
Each admission decision must record which ledger entries were consulted. This is the "evidence cited" — the specific pinned memories, previous admissions, calibration records, or corroboration results that the PAM used.

Failure mode if unconscious: without evidence references, the admission decision is an opaque binary. TNN cannot verify that the PAM consulted the RIGHT evidence — only that it made a decision. An adversary who can make the PAM skip a force-pin check (by suppressing the evidence reference) creates a blind spot that is undetectable. Silent failure: the system's self-knowledge degrades; it knows WHAT it decided but not WHAT IT KNEW when it decided.

**F-D4: Negative Space (Rejected Percepts and Why)**
Every rejection must be recorded with the same deliberation-visible detail as every admission. The "negative space" — what was NOT admitted — is as important as the positive space for auditing.

Failure mode if unconscious: if rejections are invisible, TNN cannot detect denial-of-service attacks (where an adversary floods with genuine percepts that are rejected, preventing legitimate percepts from being processed). It also cannot learn from its own rejection patterns. Silent failure: the system becomes unable to distinguish "no percepts arrived" from "percepts arrived but were all rejected" — a critical distinction for diagnosing sensor failures vs. adversarial suppression.

**F-D5: Threshold or Criterion State Changes**
If any thresholds are adaptive (even deterministically, through state updates), each change must be recorded: what the old value was, what the new value is, and what event triggered the change.

Failure mode if unconscious: if threshold changes are invisible, TNN cannot audit whether its sensitivity is drifting. An adversary who can trigger threshold changes (by crafting percepts that cause state updates) can gradually shift the system's operating point without detection. Silent failure: slow drift toward over-admission or over-rejection that is only detectable by comparing threshold values over time.

**F-D6: Provenance Reclassifications**
If a percept's provenance status changes (e.g., a sensor is downgraded from high-trust to low-trust), the reclassification must be deliberation-visible.

Failure mode if unconscious: if provenance changes are invisible, TNN cannot understand why a sensor's percepts suddenly stopped being admitted. It might attribute the change to the sensor being broken when it was actually a reclassification. Silent failure: incorrect causal attribution in TNN's self-model.

### D.2 Operations That CAN Safely Go Unconscious

**F-D7: Raw Byte Hashing**
The computation of the percept's raw byte hash (for integrity checking) is a pure function of the bytes. It does not need to be deliberation-visible because its output (the hash) IS visible — it appears in the ledger as part of the admission record. The computation itself is trivial and deterministic.

Argument for safety: the hash is a checksum. If it is wrong, the percept content is wrong, which is caught at a higher level. The hash computation cannot silently corrupt anything because any corruption is immediately visible in the ledger.

**F-D8: Internal Sorting/Ranking Within a Tier (for Staged Quarantine)**
If the PAM ranks percepts within a tier for processing order, the ranking algorithm can be unconscious as long as the FINAL ranking result is recorded. The intermediate steps of the sort are pure computation with no semantic content.

Argument for safety: a sorting algorithm that produces the same output given the same input is transparent. If the ranking is wrong, it manifests as wrong admission decisions, which are caught by K1. The ranking itself cannot create a silent integrity failure because it is a deterministic permutation.

**F-D9: Arena Allocation Details**
The specific arena allocation sequence (which memory block is allocated for which data structure) can be unconscious. This is implementation detail, not epistemic state.

Argument for safety: arena allocation affects performance and determinism (which is tested by K2 byte-identical reruns), but it does not affect the semantic content of admission decisions. If arena allocation causes nondeterminism, K2 catches it. If it causes performance degradation, K4 catches it.

**F-D10: Provenance Chain Reconstruction (Intermediate Steps)**
The step-by-step reconstruction of a provenance chain (fetching each relay node's record, verifying each hash) can be unconscious as long as the final chain_integrity_score and the list of checks performed (pass/fail for each) are recorded. The intermediate memory accesses do not need individual deliberation records.

Argument for safety: the final score and check list are sufficient for introspection. If TNN's deliberation asks "why was this percept admitted?", the answer "chain_integrity_score = 850, all checks passed except timestamp window (soft fail, -50)" is complete. The specific memory addresses used to fetch the relay records are not epistemically relevant.

### D.3 Misassignment Failure Modes

**Too Much Conscious: Deliberation Drowning**
If every internal operation is deliberation-visible, the ledger grows at O(N × K) per admission, where N is the number of operations and K is the average record size. For the Staged Quarantine PAM, a single admission might trigger 10-20 ledger writes (firing event, criterion evaluations, evidence references, tier transitions, threshold checks). At 100 admissions per time-step, this is 1,000-2,000 ledger writes per time-step. If each write is 64-256 bytes, the ledger grows at 64KB-512KB per time-step.

Concrete failure: the ledger exceeds arena capacity within T Ledger_Fill time-steps. When the arena is full, the system must either crash (unacceptable), start overwriting old entries (breaks the force-pin guarantee — old force-pinned records could be overwritten), or compress (compression may be lossy, breaking determinism). This is a resource exhaustion attack that turns the deliberation-visibility requirement against the system.

Additionally, if the deliberation itself reads the ledger to answer "why did you admit X?", and the ledger is full of low-level operation records, the signal-to-noise ratio drops. TNN's deliberation drowns in operational noise and cannot extract the epistemically meaningful records.

**Too Much Conscious: Latency Pathology**
If admission requires writing a deliberation record before the percept can be used, and the ledger write is serialized (to maintain determinism), then admission latency = computation time + ledger write time. If every operation requires a separate ledger write, latency scales linearly with the number of recorded operations. For real-time sensor processing (e.g., vision at 30fps), if the total ledger write latency exceeds 33ms, the system falls behind and starts dropping percepts. Dropped percepts are equivalent to rejected percepts — which means the system is silently degrading its percept coverage.

Concrete failure: at 30fps vision with 10 operations per admission and 5ms per ledger write, the total write latency is 50ms per frame. The system can only process 20fps, dropping 1/3 of frames. This is a 33% percept loss that is invisible if the dropped frames are not tracked.

**Too Much Unconscious: Misses That Cannot Be Learned From**
If admission decisions are unconscious (binary outcome only), TNN's deliberation cannot construct counterfactual reasoning: "if the PAM had rejected this percept, what would my belief state be?" This means TNN cannot evaluate whether the PAM is making the RIGHT decisions — only that it is making decisions. Over time, TNN's model of its own perceptual reliability degrades because it has no data to train on.

Concrete failure: TNN's deliberation becomes increasingly unable to predict its own PAM behavior. When asked "will you admit this percept?", it guesses wrong >30% of the time. This means TNN cannot proactively check whether its beliefs are based on well-admitted percepts. The system becomes opaque to itself.

**Too Much Unconscious: Rejection Reasons Cannot Be Appealed**
If rejections are unconscious, there is no record of why a percept was rejected. If the rejection was wrong (a genuine percept was rejected), there is no mechanism to appeal or correct it. The percept is simply lost. Over time, the system accumulates a bias toward information that the PAM happens to admit, and the information space narrows.

Concrete failure: if the PAM has a systematic bias (e.g., it rejects percepts from a particular sensor because of a calibration error), and rejections are unconscious, the bias is invisible. The system gradually becomes blind to an entire sensor channel without knowing it. This is a silent integrity failure — the system's belief store becomes less representative of reality, but nothing in the system's self-model indicates the degradation.

**Too Much Unconscious: Drift That Cannot Be Audited**
If threshold state changes are unconscious, the system's sensitivity can drift over time without any record of the drift. An adversary who understands the threshold adaptation mechanism can deliberately trigger drift toward over-admission (by flooding with percepts that cause thresholds to relax) or over-rejection (by flooding with percepts that cause thresholds to tighten).

Concrete failure: the system starts admitting 90% of percepts (up from the expected 60%) because thresholds have drifted downward. This is a slow change that is not detectable from any single admission decision — it is only detectable by comparing the aggregate admission rate over time. If the audit trail does not include threshold state, this comparison is impossible.

### D.4 The Principled Line

**F-D11: The Rule**

The line between conscious and unconscious PAM operations is:

> **Any operation whose output is a premise for a future admission decision MUST be deliberation-visible. Any operation whose output is consumed only within the current admission decision MAY be unconscious.**

In formal terms: let D be the set of all PAM operations. For each operation d ∈ D, define its "downstream dependency set" DD(d) = { d' ∈ D : d' reads the output of d }. If DD(d) is non-empty (some future operation depends on d's output), then d must be deliberation-visible. If DD(d) is empty (d's output is consumed only within the current admission and never referenced again), d may be unconscious.

Concretely:
- The firing event: DD = { all future queries about admission history }. Must be conscious.
- The rule that fired: DD = { future introspection about PAM behavior, threshold adaptation, credibility tracking }. Must be conscious.
- Evidence cited: DD = { force-pin verification, contradiction checking, compositional reasoning }. Must be conscious.
- Rejections and reasons: DD = { denial-of-service detection, bias auditing, appeal mechanisms }. Must be conscious.
- Threshold state: DD = { future admission decisions that depend on threshold }. Must be conscious.
- Arena allocation: DD = { no future admission decisions depend on which arena block was used }. May be unconscious.
- Provenance chain intermediate steps: DD = { only the final score and check list are used by future decisions }. Intermediate steps may be unconscious; final score must be conscious.

**Kill Bar F-K6 (Principled-Line Verification):**
- Claim: The line is correct — no unconscious operation has a non-empty downstream dependency set. Equivalently: if you remove the deliberation record for an unconscious operation, no future admission decision changes.
- Fixture: for each operation classified as "unconscious," run the admission stream twice: once with the operation's deliberation record present, once with it absent. If any admission decision changes between the two runs, the operation was misclassified and must be made conscious.
- Threshold: 0/1000 admission decisions changing between runs.
- Schema: new type K8 (conscious/unconscious classification audit). Justification: this is a meta-level audit that verifies the classification itself, which is not covered by K1-K5 (which verify the PAM's correctness, not its introspection structure).

---

## TASK E — TOP 3 PRIORITIES AND TOP 3 TRAPS

### Top 3 Things the Builders Should Do First

**1. Test C3 × M1 Interaction (F-A14)**
Apply both C3 and M1 simultaneously on the full fixture set and measure whether the combined RK-3′ degrades. This is the single most dangerous hidden coupling: two independently-calibrated mechanisms interacting in untested ways. If this test fails, everything downstream is built on sand. Priority: before any paradigm testing.

**2. Generate Expanded Fixture Set (F-A1)**
Create 500+ new traps beyond the frozen set, using the attack classes enumerated in A.3 (compositional, threshold-gaming, reinterpretation, provenance-cascade, temporal-ordering). The current kill bars are calibrated on 21 fixtures. Any paradigm (including C3) that passes on 21 but fails on 500 is overfit, and no amount of paradigm innovation matters if the evaluation set is too small. Priority: before any paradigm evaluation.

**3. Implement the Principled-Line Audit (F-D11, F-K6)**
Classify every current PAM operation as conscious or unconscious using the downstream-dependency rule, then run the verification fixture (dual-run comparison). This is preregistration-ready and can be done in parallel with other work. It directly feeds the CU track and prevents the builders from making a costly misassignment. Priority: immediate, parallel with #1 and #2.

### Top 3 Traps to Avoid

**1. "Two Corroborations = Independence" (F-A1.1)**
The single most dangerous assumption in the program. Every "independent corroboration" must be verified as independent, not assumed. The i32-aliasing lesson generalizes: independence is a property of the implementation, not the design. If two corroboration passes share bytes, share arena state, or read the same ledger entries, they are correlated, and the 2× requirement provides no safety. Trap: building elaborate paradigms on top of unverified independence.

**2. "Passing the Frozen Kill Bars Means It Works" (F-A1, F-A5)**
The frozen attack tape has 21 fixtures. Any mechanism that is even slightly tuned can pass 21 fixtures by overfitting. The program's history shows that failures concentrate in untested fixture classes. Trap: declaring victory on the frozen tape without expanding the fixture set to 500+ diverse traps. Every new paradigm must be tested on the expanded set before adoption.

**3. "Consciousness is Free" (F-D3)**
Making everything deliberation-visible feels safe ("transparency = trustworthiness"), but it is not free. The ledger grows linearly with deliberation-visibility scope, and arena capacity is finite. If the builders make every operation conscious without applying the principled-line test, they will either exhaust the arena (resource exhaustion attack) or dilute the deliberation signal with operational noise (deliberation drowning). Trap: over-classifying operations as conscious "just to be safe" without measuring the resource and latency cost. The principled line (F-D11) is the antidote — use it.
