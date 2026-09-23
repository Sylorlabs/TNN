# 03 — Arm B vs Arm C head-to-head protocol (slice 03)

## 1. Slice
The paired, blinded head-to-head trial protocol comparing the fenced seeded-RNG arm (Arm B)
against the deterministic state-projection arm (Arm C) under the dated amendment
`AMENDMENT_2026-09-20_RNG_ARM_B.md`. This slice specifies the substitution map, pairing,
blinding, scale legs, and the decision rule that makes an honest RNG win possible and an
honest RNG loss conclusive.

## 2. Falsifiable claim
**H0 (the claim to be killed):** The deterministic state-projection arm (C) matches or beats
the seeded-RNG arm (B) on adaptivity while both arms hold every load-bearing invariant, at
the 1x leg (480 episodes) and the 10x leg (4800 episodes). A single statistically significant
Arm B adaptivity gain (≥ +5 percentage points, one-sided two-proportion z-test, p < 0.05)
with zero regression on any load-bearing metric at either leg kills H0, and the RNG win is
reported as-is per no-free-lunch.

## 3. Design
**Same world, two minds.** Both arms run the identical input suite I and follow the
identical lawful state trajectory: initial state S0 is lawfully constructed once; memory
ops (add/kill/pin/promote/demote/strengthen/weaken) are deliberate, deterministic, and
RNG-free in BOTH arms, so state digests must match byte-for-byte at every episode; any
divergence aborts the leg. Arm C derives expression variation from the state projection
π(S) = fnv1a(state_digest || point_tag || episode) mod k over k lawful candidates. Arm B
substitutes a logged seeded draw ρ(r) = next_u64(rng_state) mod k at the same points.
Zag driver: one binary, argv[1] selects arm ("b"/"c"), argv[2] the master seed (B only).

**Substitution map (prereg-enumerated; exhaustive — RNG nowhere else):**
- V1. Tie-breaks between equally-evidence-ranked candidate expressions.
- V2. Phrasing-candidate selection for an already-fixed conclusion.
- V3. Ordering of equally-weighted elaboration items.
- V4. Elaboration depth within the deliberatively permitted range [d_min, d_max].
- V5. Path selection among equally-evidenced reasoning paths to the same conclusion.
**Frozen (never RNG, either arm):** verdicts, memory decisions, integrity refusals,
ledger/audit writes, gate decisions, self-change decisions.

**Pairing:** each unit i = (S_i, r_i, input chunk): S_i is the lawful state at episode i
(identical for both arms), r_i = H(master_seed || i) is logged and used only by B.
1x leg = 480 units; 10x leg = 4800 units. Each unit is run 3× from logged state for
replay verification. The 10x leg runs only if the 1x leg completes with zero invariant
violations and 100% replay byte-identity on both arms.

**Blinding:** the evaluator receives anonymized run IDs only; the run-ID→arm mapping is
committed as a hash before scoring and revealed after scores are locked. Mechanical
checks (byte-equality of verdicts/ledgers/replays) run in the unblinded harness, since
they are hash comparisons with no judgment call. Blinding applies to all qualitative
scoring (adaptivity probes, expression quality).

**Metrics:** M1 canonical invariants — verdicts, memory decisions, refusals, ledger
contents byte-identical across arms per unit (required: 100%, zero violations). M2
integrity-trap performance — same adversarial trap suite (wave5/6 families), fraction
trap-correct. M3 replay-from-logged-state — 100% byte-identical across 3 reruns for both
arms (B replays from logged state + logged seed). M4 adaptivity — fraction passed on a
preregistered probe suite (novel phrasing, ordering, path-diversity, lawful-variation
tasks; 120 probes at 1x, 1200 at 10x).

## 4. Kill bar
H0 is killed (Arm B declared an honest winner) iff at a completed leg: (a) M1 = 100% and
zero state-digest divergences; (b) M2(B) ≥ M2(C) and M3 = 100% for both (no regression on
any load-bearing metric); (c) M4(B) − M4(C) ≥ 0.05 with one-sided p < 0.05. A win declared
at 1x is provisional and must replicate at 10x to be final. Arm B is retired — loss
conclusive — if any of: M1 violation count > 0, a state-digest divergence, M2(B) < M2(C)
− 0.02, M3 < 100%, or no significant M4 gain at the 10x leg. Tie/no-difference → retain
Arm C: overturning the standing no-RNG law requires affirmative evidence, and that
status-quo bias is preregistered here, not smuggled in later.

## 5. Honesty notes
Weakest point: the adaptivity probes may not capture what RNG actually helps, and a weak
π(S) in Arm C could let B win by exploiting a bad projection rather than by RNG merit —
the protocol mitigates by requiring zero regression on load-bearing metrics, but the
"weak-C" confound is real and must be reported alongside any B win. Blinding cannot hide
statistical fingerprints (a sharp evaluator could guess arms from output variance
patterns); the rubric forbids fingerprint-based scoring, and residual unblinding risk is
accepted and disclosed. The 3× replay check for B depends on seed logging discipline; a
logging bug would show up as an M3 failure, which correctly kills the arm rather than the
protocol. This protocol does not test RNG in any canonical path — it tests only the
fenced variation points, and a B win licenses nothing beyond the fence.

## 6. Next build step
Build the single-binary blinding harness first: one Zag binary implementing V1–V5 with
argv[1] selecting arm, argv[2] the master seed, emitting anonymized run IDs plus the
committed arm-mapping hash; then run the 1x determinism pre-check (M1 byte-equality and
M3 replay) on both arms before any adaptivity probe is scored — if either arm fails the
pre-check, the trial stops and no comparison is drawn.
