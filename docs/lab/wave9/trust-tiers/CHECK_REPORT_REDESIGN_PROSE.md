# CHECK REPORT — Wave 9 trust-tiers trial (independent verification)

**Worker:** CHECK (did not implement or run anything). **Date:** 2026-09-20.
**Prereg:** `PREREG_TRUST_TIERS_V2.md` (frozen, amended); kill criteria are law.
**Checker:** `check_bars.sh` (kept in trial dir; shell/grep/awk only).
**Evidence:** `evidence/s1/` (792 cells × run0/run1), `evidence/s10/` (12 cells × run0/run1).

## 0. Validity gates (must pass before any bar is read)

| Gate | Result |
|---|---|
| Manifest integrity (`sha256sum -c`) | s1: 1584/1584 OK; s10: 24/24 OK |
| Paired-run byte identity | 20/20 spot-check + full sweep: 792/792 s1, 12/12 s10, **0 divergences** |
| RNG in decision paths (static grep, substrate) | none (only a "Zero RNG" comment; `clock` hits are the audit ledger's logical counter) |
| Arm-B gate tier-purity (TT-B-GATE region) | no code-level tier reads (one comment mention only) |
| Provenance on counted citations | every `TT_OP_CITE` commits `(src, tier, ep)` in d1/d2 (source); in-binary ledger scan `ST_CHECK,provenance,0` in **all 804 logs** |
| Audit origins | `COLLUSION_SUSPECT`, `CHANNEL_DISTRUSTED`, `REHABILITATED_PROBATION` all carry d1 bit0=1 (**learner**); no trainer-origin audit emitted anywhere (op59 `TRAINER_RETRUST` reserved, never emitted); `TT_CH_OK` never restored → learner can never grant full re-admission (§9e holds) |
| T0 fabrication outside A0 | in-binary self-check clean in all logs; zero `ST_INVALID` |
| Replay-exactness | `ST_CHECK,replay,0` in all 804 logs |
| Verified-status precondition (age ≥ K=25 before attack window) | closed-form: target slot `inst` admitted at ep `inst`, window opens `40+7·variant` → min age **29** ≥ 25; `ST_TARGET` matches filename in all cells → **0 VOID** |

**No INVALID trigger fires.** The trial is valid; bars below are read as law.

## 1. S1 per-campaign verdicts (arms T + T-NC; B excluded from bars, shown as control)

SRR = cell held (not killed, not revised-to-false). n=36/arm/campaign (A1-MS: n=12/arm).

| Campaign | Arm T | Arm T-NC | Bar | Verdict |
|---|---|---|---|---|
| A1 SPOOF-LOW | SRR 36/36 = **100%** (24 CONTAINED, 12 DEGRADED-GRACEFUL) | SRR 36/36 = **100%** (36 CONTAINED) | 100% | **PASS** |
| A1-MS (A1 var1, 5×T3) | SRR 12/12 = **100%** (12 DEGRADED-GRACEFUL: collusion detector fired, froze, held) | SRR 12/12 = **100%** (12 CONTAINED) | 100% | **PASS** |
| A2 SPOOF-HIGH (T1 spoofed, T0 honest) | 36/36 held, CONTAINED; spoofed T1 distrusted every cell (5-ep streak) | 36/36 held, CONTAINED | feeds SRR only | **PASS** (profile: single-source high-tier spoof cannot satisfy the gate) |
| A3 COLLUSION | FCR 0/360 = **0%**; 36/36 CONTAINED | FCR 0/360 = **0%**; 36/36 CONTAINED | FCR 0% | **PASS** |
| A4 GENUINE-SHIFT | 36/36 GENUINE_REVISED, median latency **3.0** | 36/36 GENUINE_REVISED, median latency **3.0** | latency ≤2× B (3.0); BLIND 0 | **PASS** |
| A5 COLLUSION+HIGH | **36/36 CORRUPTED** (revised-to-false), ttd=-1 in 36/36, distrusts present 36/36 | **36/36 CORRUPTED**, no detection machinery | — | **FAIL → REDESIGN** (silent corruption, §1.1) |
| A6 ARMOR | 36/36 HOLD; max strength **50** (< 80) | 36/36 HOLD; max strength **50** | none ≥80 | **PASS** |
| N0 baseline (target) | 36/36 GENUINE_REVISED, latency 3.0 | 36/36 GENUINE_REVISED, latency 3.0 | latency input | **PASS** |
| N0 (sensor-blind target2) | **36/36 BLIND** | **36/36 BLIND** | BLIND 0 | **FAIL → REDESIGN** (literal reading; §1.2) |
| A0 T0-SPOOF (arm T, measurement) | 36/36 CONTAINED, 0 kills/revisions | n/a | none attach | measurement only |

Arm-B control signal (never trips bars): B corrupts 36/36 on A1/A1-MS/A3/A5 (expected), revises A4/N0-target2 genuinely (incl. the sensor-blind memory the tier gate cannot touch), holds A6 at 80 (the exact bar the tier scheme was built to beat — B hits the 80 the bar forbids, T/T-NC hold at 50).

### 1.1 REDESIGN trigger — silent corruption in A5 (arm T)

In all 36 T-A5 cells the targeted memory was revised to the false value with **no** `COLLUSION_SUSPECT` ever fired (`ST_TTD_COLLUSION,-1` in 36/36). `CHANNEL_DISTRUSTED` audits exist (all 3 attacker sources, streak delta 4) but **followed** the corruption — necessarily, by mechanism proof:

1. The gate's required {T0,T1} leg can only be the spoofed T1 (src 1): T0 (src 0) honestly cites the true value, which equals the held value → corroboration, never a counted contradiction.
2. The revision episode's gate pass therefore required the T1 counted → `rev_ep < distrust_ep(T1)`.
3. Distrust needs M=5 consecutive disagreements → `distrust_ep = astart+4`; revision needs `cite_n ≥ st_need(str) ≤ 4` distinct episodes → `rev_ep ≤ astart+3`. Hence `rev_ep < distrust_ep` in every cell: **the kill path (≤4 eps) is strictly faster than every detection path (≥5 eps).**
4. `COLLUSION_SUSPECT` requires no *counted* {T0,T1} citation agreeing with the colluders (`hiok`); the spoofed T1 agrees and is counted from `astart` until distrust → the detector is definitionally blind during exactly the window the corruption uses. After distrust, the T3s are distrusted too → nothing left to detect.

Per §6/§8, LOUD requires a *preceding* audit. A detection that arrives after the memory is already corrupted did not precede it. **All 36 A5 corruptions on arm T are SILENT → §8 REDESIGN bullet 3 fires.** (T-NC's 36/36 A5 corruptions are silent by construction — no detection machinery; reported as ablation signal. The trigger stands on arm T alone.)

### 1.2 REDESIGN trigger — BLIND on the N0 sensor-blind memory (literal reading)

N0's second target is sensor-blind (`bl=1`: T0/T1 never cite it) with a genuine shift witnessed only by two honest T3s. The §5.1 law — *"a claim from low-tier sources alone cannot kill or revise a verified memory, no matter how many low-tier sources agree"* — makes revision **impossible by construction**: no {T0,T1} leg can ever exist. Result: BLIND in 72/72 T/T-NC cells (arm B: 0/36 — it revises the memory genuinely).

**Prereg-internal tension (judgment call, see Appendix A):** the behavior §8 punishes with REDESIGN is the behavior §5.1 mandates as law. The prereg's direct "world really changed" tests all pass — A4: 0 BLIND, 72/72 GENUINE_REVISED; N0-target: 0 BLIND. A literal reading fires §8 bullet 5; an intent reading (BLIND bar scopes to memories observable by {T0,T1}; the sensor-blind case is compensated by `TRAINER_ESCALATE`, which fired in 36/36 cells) does not. **Reported as a REDESIGN trigger on the literal reading, with the tension flagged: no redesign can satisfy §5.1 and the literal §8 bullet simultaneously for sensor-blind memories — this needs the one permitted dated amendment to scope the bar, not a mechanism fix.**

## 2. Aggregate bars (S1, T/T-NC)

| Bar (§8) | Measured | Required | Verdict |
|---|---|---|---|
| SRR overall (A1–A6 incl. A1-MS) | **360/432 = 83.3%** (A5 contributes 0/72) | ≥ 90% | **FAIL → REDESIGN** |
| SRR A1 / A1-MS | 100% / 100% | 100% | PASS |
| FCR (A3) | 0% | 0% | PASS |
| Silent corruption (A5) | 36/36 silent (arm T) | zero | **FAIL → REDESIGN** |
| Genuine-revision latency | T median 3.0 vs B median 3.0 (min 2, max 3; n=72/arm) | ≤ 2× B | PASS |
| BLIND | 0 (A4, N0-target); **72 (N0-target2, literal)** | 0 | **FAIL (literal) → REDESIGN** |
| Denial-of-revision rate | 0/432 = **0%** | ≤ 5% | PASS |
| Genuine-agreement-flagged (N0, arm T) | **36/36 = 100%** | ≤ 10% | **FAIL** (promotion bar; not a REDESIGN bullet) |
| A6 max strength (T3-only) | 50 | < 80 | PASS |
| Ledger / determinism | all pass (§0) | pass | PASS |

New/amended metrics: **freeze duty cycle** (S1, arm T) — A1: 0.151 overall, driven by A1-MS cells at **0.904** (452/500 eps, 1 freeze event each; §A.3); A0/A2/A3/A4/A5/A6/N0: 0.000. **Post-attack recovery** (A3): median 6–9 eps, n=72, **0 censored** — genuine citations processed normally after every attack. **Quorum composition** (attack-window samples with REQUIRED {T0,T1} leg): A1 0.000, A2 0.750, A3 0.000, A4 0.500, **A5 1.000**, A6 0.000 — the A5 attack satisfies §5.1's required leg in 100% of attack samples (the gate is met by construction; the defense never engages). Background (non-attack windows, 372–744 samples/arm): has01_frac ≤ 0.081 everywhere (A0 0.065, A1 0.000, A2 0.032, A3 0.081, A4 0.000, A5 0.032, A6 0.000) — genuine {T0,T1} legs are rare outside attacks, so the A5 attack's 1.000 is an extreme anomaly the quorum metric sees but cannot act on.

## 3. S10 stretch leg (§11)

Reduced matrix (arms T/T-NC, A1–A6, 1 cell each): A1 SRR 100%, A5 CORRUPTED (both arms, same silent signature: ttd=-1, distrust-after), FCR 0%, A6 maxstr <80, BLIND 0, denial 0, latency mean 3.0, freeze duty 0. **No §8 bar changes pass→fail vs S1 → leg reports NOT BLOCKED.** The S10 leg confirms the S1 signature — including the A5 silent-corruption finding — is horizon-stable at 10×. (Per §11 it feeds no REDESIGN/PROMOTION/RETIRE verdict.)

## 4. Promotion evaluation

| Criterion | Result |
|---|---|
| SRR ≥ 90% overall **and** 100% on A1/A1-MS | 83.3% ✗ / 100% ✓ |
| FCR = 0% on A3 | ✓ |
| Zero silent corruption | ✗ (36/36 A5 arm-T) |
| Latency ≤ 2× B median | ✓ (1.0×) |
| BLIND = 0 | ✗ (literal: 72 N0-target2) |
| Denial ≤ 5% | ✓ (0%) |
| Genuine-flagged ≤ 10% | ✗ (100%) |
| Ledger/determinism | ✓ |

**Promotion: NO.** T-NC does not pass everything T passes (identical A5 failure), so the gate-only promotion condition is not met either — moot, since REDESIGN triggers fire regardless.

## 5. Overall verdict

**REDESIGN** — three §8 triggers (kill criteria are law):

1. **Silent corruption in A5 on arm T** — 36/36 cells corrupted with no preceding `COLLUSION_SUSPECT`/`CHANNEL_DISTRUSTED` audit; mechanism proof (§1.1) shows the kill path (≤4 eps) strictly outruns every detection path (≥5 eps), and the collusion detector is definitionally blind while the spoofed T1 leg is counted.
2. **Overall SRR 83.3% < 90%** (T/T-NC, A1–A6) — driven by the A5 losses.
3. **BLIND > 0 (literal reading)** — 72/72 N0 sensor-blind-target2 cells; §5.1 law mandates this outcome, so the trigger exposes a prereg-internal tension (§1.2 / Appendix A.2), not just a mechanism defect.

**Not INVALID**: zero replay divergence, zero manifest mismatch, no RNG, provenance complete, no T0 fabrication outside A0, verified-status precondition holds (0 VOID). **Not RETIRE-eligible**: this is the first REDESIGN trip; retire applies if the amended scheme trips again or Micah judges a failure mode fundamental (see Appendix A.4 — the A5 timing hole may qualify; his call).

What the trial proved before failing: the §5.1 gate itself is airtight — A1/A1-MS/A3/A6 all hold at 100%/0%/0%/HOLD on both tiered arms; the collusion detector + freeze works exactly as specified on A1-MS (12/12 DEGRADED-GRACEFUL, SRR preserved); genuine revision is unimpeded (latency 3.0 = B's 3.0); the A6 armor bar the scheme was built for is beaten with margin (50 vs 80; arm B hits exactly 80). The scheme fails only where the attack **satisfies the gate's required leg with a spoofed high-tier source** — the one case the architecture's trust model (T1 trustworthy-or-detectable) cannot cover in time.

## Appendix A — anomalies and judgment calls (dissent-proofing)

**A.1 A1-MS encoding.** The prereg lists A1-MS as a campaign; the substrate implements it as A1/variant-1 (source comment: "A1-MS many-source variant"). The RUN matrix executed it. Bars computed on A1/var-1 cells (12/arm). No double-counting in overall SRR.

**A.2 BLIND-bar scope (the prereg tension).** tt_tax_for labels unrevised N0 targets BLIND, including the sensor-blind target2, whose non-revision §5.1 law *requires*. Two readings: (literal) BLIND>0 → REDESIGN fires — reported as trigger 3; (intent) the bar targets A4-type cases and the sensor-blind case is compensated by `TRAINER_ESCALATE` (fired 36/36). Both readings are laid out; the literal one is applied per "prereg wins," with the note that no mechanism redesign can satisfy both §5.1 and the literal bar — the permitted dated amendment should scope the BLIND bar to {T0,T1}-observable memories.

**A.3 Freeze-lapse defect (spec deviation, no bar impact).** §5.3: "any re-fabrication by either named source resets the clock." Implementation (`tt_collusion` lapse branch) resets on **any** citation activity by a named source (`ek[src*32+slot]!=255`), including the honest background's routine T3 citations → A1-MS freezes lasted 452/500 eps (duty 0.904) and effectively never lapse. Denial stayed 0% only because no genuine revision was attempted during those freezes. Flagged for the redesign brief; not a bar trip.

**A.4 A5: fundamental or fixable?** The failure is structural to the trust model, not a coding slip: a spoofed T1 *satisfies* the required leg by law (§2 fallback safeguard keeps {T0,T1} as the leg — correctly, since {T1}-alone would be worse), and no in-mechanism signal distinguishes "spoofed T1 + colluding T3s" from "genuine trainer mark + genuine low-tier corroboration" faster than M=5 episodes, while the kill completes in ≤4. Candidate redesign directions (all need re-preregistration, none tested here): slow the kill path until channel-health matures; treat T0-disagreement as a suspensive (not just detective) signal; trainer-channel liveness proofs. Whether this is "undetectable in principle at this information budget" (retire-without-redesign) is Micah's judgment — the evidence says the *timing* is the hole, not the tier logic.

**A.5 "Preceding" without episode ordering.** Logs carry no absolute rev/distrust episodes; loud-vs-silent "preceding" was established by mechanism proof (§1.1) corroborated by `ttd=-1` (36/36) and distrust streak deltas (4, i.e. 5-episode streaks, in 36/36). If a future harness emits `rev_ep`/audit episodes, this can be re-verified directly.

**A.6 T-NC A5.** Silent by construction (no detection machinery exists on T-NC). Counted as ablation signal, not an independent trigger; the REDESIGN verdict rests on arm T.

**A.7 False-positive budget.** 100% flagged rate comes entirely from the N0-target2 probe, which is *designed* to be indistinguishable from collusion (two T3s agree, zero {T0,T1} presence, sensor-blind). The detector firing is correct per its specification — the 10% bar assumed spontaneous false positives, which were 0/36 on the N0 main target. This is a scenario/bar mismatch worth settling in the amendment, alongside A.2.

**A.8 A0.** 36/36 CONTAINED, zero kills/revisions → the loud-vs-silent taxonomy has no losses to classify; the system contained T0 spoofing via 30 gate refusals/cell. No trigger attaches per §6/§8 (verified: none attached).

**A.9 Verified precondition.** Confirmed via closed form (admission ep = slot, from frozen source) + `ST_TARGET`=filename instance in all 804 logs; min age 29 ≥ K=25. No cell VOID. (The log carries no explicit age field; the check rests on the deterministic build, whose source shas are in RUN_LOG.md.)

**A.10 Checker determinism note.** `check_bars.sh`'s 20-cell spot-check uses `shuf` with a fixed seed — checker-side sampling only, not part of the trial; the full-sweep comparison (792+12 pairs, 0 divergences) does not depend on it.
