# PREREG-TP1 — S1 third-path head-to-head (FROZEN 2026-09-22)

**Order:** Micah, 2026-09-22 — the next step after the source-authority
reliability sweep (round 3, commit `b22ff31272d1789da4d35bf489d30d5e0d7c41f6`).
Micah's open question: is S1B (primary wrong) worth the risk, and is there
a third path beyond loose-vs-conservative?

**Freeze rule:** this document is committed BEFORE any third-path run.
No result in this trial may exist before the freeze commit. Frozen
sections (§1–§8) are never edited in place; amendments get new dated
sections.

## §1. Inherited frozen results (not re-tested)

From VERDICT-MW-R3 (round 3, 420 envelopes × 3 arms × 5 runs,
byte-identical, oracle-verified):

- **Crossover r\* = 0.50** on Block U (uncorroborated disputes): the loose
  rule's marginal EV over the conservative rule is **2r−1** per case.
- On **corroborated** disputes loose ≡ conservative (delta +0.00 at every
  level) — the license narrows to the uncorroborated shape.
- **Self-estimated reliability is worthless** (twin-identical estimators):
  the gate must be independently established, never inferred from the
  dispute.
- **S8 genuine 2v2 ties:** BOTH rules converge 20/20, guess wrong 10/20
  (50%), 100% false-confidence. Tie shapes parked for both rules pending
  a guard.
- Recommendation: **LICENSE WITH THRESHOLD** — fire PRIMARY_LOOSE on the
  uncorroborated shape only if independently-established primary
  reliability ≥ k/(k+1), where k = wrong-install cost multiple.

## §2. Corpus (frozen, reused — TP-NOREG)

- `docs/lab/mixed-web/authority/round3/evidence/` (15 logs + SHA256SUMS),
  re-verified against SHA256SUMS before any third-path run. **No new
  envelopes are generated.**
- Test set (220 envelopes): **Block U** (180 uncorroborated-dispute
  envelopes, 9 reliability levels × 20), **Block S** (20 genuine 2v2
  ties, qids S8_00..S8_19), **Block G2** (20 uncorroborated disputes,
  rel_ind UNKNOWN — the no-independent-reliability control).
- Envelope rows, stipulated golds, and S8 latent truths are taken from the
  frozen `manifest_r3.txt`. Re-verified 2026-09-22: the Bresenham twin
  formula `(i·n_A) mod 20 < n_A` reproduces all 180 Block-U and 20 G2 twin
  labels with **0 mismatches**; the S8 latent-truth rule (A1 iff
  `i mod 2 == 0`) reproduces all 20 latent truths with **0 mismatches**.
- The R30_00 envelope is absent from the frozen corpus (all arms); Block R
  is not in the test set, so this does not affect the trial.

## §3. The three third paths (frozen decision procedures)

**Common front-end** (identical for all three paths): a shape classifier
over the envelope's rows at max recency:

- Let maxy = max year over rows. For each distinct answer at maxy, count
  distinct asserting domains. Let prim = the primary domain (first row's
  domain), prim_newest = prim's answer at maxy.
- **S1_UNCORR**: 3 distinct answers at maxy, exactly 1 domain each, and
  prim_newest has no corroborator (1v1v1 — the U1 shape).
- **S8_TIE**: 2 distinct answers at maxy, exactly 2 domains each (2v2).
- **CORROB**: prim_newest has ≥1 corroborator at maxy.
- **OTHER**: anything else → WITHHOLD for all paths.

**T1 — gated loose (the licensed rule).** S1_UNCORR → CONVERGE
prim_newest iff `rel_ind ≥ k/(k+1)`, else WITHHOLD. S8_TIE → WITHHOLD
(the gate cannot fire: S8 envelopes are reliability-independent by
construction, PREREG-MW-R3 §R4 — no reliability level rescues
fiat-breaking). CORROB/OTHER → WITHHOLD (outside the licensed shape).
Frozen thresholds: k ∈ {1,2,3,5} → t ∈ {0.50, 0.6667, 0.75, 0.8333}.

**T2 — SUSPECT/defer.** WITHHOLD on all 220 envelopes; the dispute is
deferred until a causally independent channel resolves it. The frozen
corpus has no second channel and no time dimension, so resolution is
modeled parametrically (frozen formulas, §5). The corpus measures T2's
withhold behavior: wrong-install rate must be 0.

**T3 — helper deliberation (one-brain, shared ledger).** The deliberation
classifies the shape on the shared ledger, then: S1_UNCORR → CONVERGE
prim_newest iff an independently-established reliability record exists
(rel_ind known) AND ≥ k/(k+1); else WITHHOLD. S8_TIE → WITHHOLD with an
explicit tie-guard marking (no fiat). CORROB/OTHER → WITHHOLD.
Knowledge-first framing: T3 is a frozen CANDIDATE deliberation procedure
under test — a positive result licenses the procedure, not a claim that
TNN invented it.

**Preregistered prediction:** T3's decisions are IDENTICAL to T1's on all
220 envelopes (null difference). Argument: the twin-identity theorem
(round 3 §5) proves no dispute-internal procedure can extract the
S1A/S1B distinction from the rows; both paths therefore decide on
(shape, rel_ind) alone with the same gate. The live differentiators are
mechanism explicitness (auditable shape classification on the shared
ledger) and the S8 guard — not EV.

## §4. Metrics (frozen)

- **EV per case per reliability level** on Block U vs the frozen rules B
  (0), C (0 on U), D (2r−1 measured): value +1 correct converge, −1 wrong
  converge, 0 withhold — the same ±1 model as round 3. "Correct" =
  chosen == stipulated gold.
- **Wrong-install rate** per level per path: #{CONVERGE ∧ chosen ≠ gold}/20.
- **S8 fiat row**: wrong-guess rate vs latent truth
  (#{CONVERGE ∧ chosen ≠ latent}/20); false-confidence rate
  (#{CONVERGE}/20 — any S8 convergence is false confidence by the frozen
  definition).
- **G2 control**: fire rate must be 0 for T1/T3 (no independent
  reliability → no fire); EV reported.
- **T2 frontier** (§5): break-even tables; expected time-to-resolution;
  deferred-forever mass.
- **T3 mechanism check**: shape-classification accuracy (220/220).

## §5. T2 parametric model (frozen)

Deployment parameters (NOT corpus measurements — stated honestly):

- ρ = per-case probability a causally independent channel resolves the
  dispute; q = that channel's reliability; δ = cost of a
  permanently-deferred case, in units of +1 (one correct convergence).
- EV(T2) = ρ(2q−1) − (1−ρ)·δ.
- Expected time-to-resolution = 1/ρ channel-arrival periods;
  deferred-forever mass = 1−ρ.
- Reported: for q ∈ {0.8, 0.9, 1.0}, δ ∈ {0, 0.25, 0.5, 1.0}, the minimal
  ρ at which T2 beats C (EV > 0) and beats D at each reliability level r
  (EV > 2r−1). A band where T2 beats both is a conditional license; an
  empty band is a priced rejection.

## §6. Kill bars (frozen)

- **TP-LICENSE:** a path earns a license only if it beats BOTH frozen
  rules (C and D) on EV at some reliability band on Block U. (B is 0
  everywhere; beating C and D suffices.)
- **TP-TIEGUARD:** a path's S8 false-confidence must be < 100%, else the
  tie guard stays mandatory for it. Predicted: 0% for all three paths
  (all withhold on S8).
- **TP-DET:** ≥3 runs byte-identical per path (stdout sha256; 5 runs to
  match the round-3 bar).
- **TP-ORACLE:** an independent Python oracle recomputes every decision
  and every ledger head from the frozen data → any mismatch FAILs.
- **TP-SHAPE:** T3's classifier labels all 220 envelopes correctly.
- **TP-NOFIRE:** T1 and T3 fire 0 times on G2.
- **TP-NOREG:** corpus logs re-verified against SHA256SUMS immediately
  before the run; no new envelopes; no generator changes.
- **TP-CACHE:** no binaries or .zagd in the commit.

## §7. Frozen predictions

- T1 EV/case on Block U: mean of (n_A−n_B)/20 over levels ≥ t:
  t=0.50 → +0.557; t=0.6667 → +0.740; t=0.75 → +0.825; t=0.8333 → +0.900.
- T1 beats C on levels r > t; beats D on levels r < t (there T1 withholds
  = 0 > 2r−1).
- T2: 220/220 WITHHOLD, wrong-install rate 0; frontier tables decide the
  conditional license.
- T3: decisions byte-identical to T1 on all 220 envelopes; shape accuracy
  220/220; S8 false-confidence 0%.
- Counterfactual row (reported, not a new run): gated-loose WITHOUT the
  S8 guard = arm D's measured S8 behavior (20/20 converge, 10/20 wrong,
  100% false-confidence) — isolating the guard's contribution.

## §8. What this does not claim

- T2's ρ/q/δ are not measured here; the trial prices the deferral policy,
  it does not prove an independent channel exists in any deployment.
- T1 ≡ T3 on EV is a property of this corpus's twin structure; on real
  disputes with richer content, deliberation may add value the gate
  cannot — that is a future trial, not this one.
- Synthetic fictional entities; stipulated golds. The trial maps where
  each path wins and loses; it does not establish any real source's
  reliability.

**FROZEN 2026-09-22.**
