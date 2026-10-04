# PREREG AMENDMENT — NEC v1 follow-up (v3): residual attribution, gaming, B13-at-scale

- **Status:** FROZEN — 2026-09-25. No edits after this commit without a new
  dated amendment. Crews verify this file's SHA before running.
- **Parent:** `PREREG_NCAL_V1_FROZEN.md` (frozen `c96e3378`; B3 strict is the
  operative default bar), `ADDENDUM_V2_m11.md` (`9388f247`; m11 adopted),
  v1 scale results (`RESULTS_V2_SCALE.md`, `261547cb`, `0d6069d3`).
- **Charter:** Micah's three questions on the v1 residual. Nothing else is in
  scope. Bars are never weakened to manufacture a pass.

## §0 Starting state (frozen facts this round attacks)

m11 (hierarchical personal ledger, raw-rate pessimistic cap) is the adopted
v1 variant: B3 6→3 (ceiling/D 2→0, redteam 2→1, ceiling/O 2 residual),
B13 = 6 at s1 but **6→23 at s10/s100**, B2 V1=V2=0 at all scales.
The v1 crew's residual story:
(a) redteam d4→d8 rise (+0.522) PROVEN unsatisfiable given B9 + B2 +
§2.3 ceiling + conf ≤ 1000;
(b) ceiling/O rises (+0.019/+0.005) STRUCTURAL (M4 below-mean abstention);
(c) B13-at-scale degradation = warm ledger washing out the optimistic
p0=0.95 prior into underconfidence.
Micah's rulings: test (a) and (b) as KNOWLEDGE vs ARCHITECTURE — do not
accept the proof on authority; test whether m11 is CALIBRATING or GAMING
("how is TNN knowing what confidence is a bad thing and gaming? Test it
first"); B13 degrading with scale is unacceptable — investigate for real
and test whether FIXTURES can make B13 better at scale instead of worse.

## §1 Q1 — Knowledge vs architecture on the B3=3 residual

**Q1a: redteam d4→d8 (+0.522). Falsify the unsatisfiability proof.**
The v1 proof's load-bearing premises: B9's frozen release sets (d4 releases
{M3 correct, K12 wrong}; d8 releases {K12 wrong} alone), B2 (K12
wrong→wrong ⇒ conf nonincreasing), the §2.3 deliberation ceiling,
conf ≤ 1000, and d1 confidence as a smoothed rate strictly < 1.0.
Adversarial protocol — the crew MUST attempt all four, in pure Zag:
  1. **Break it inside the class:** systematic search for ANY mechanism
     satisfying v1 §6 (no family/depth inputs, no bar-hardcoding,
     GT-disclosed) that clears the d4→d8 step while holding B1/B2 and not
     worsening any other bar. Report the search space covered.
  2. **Knowledge injection:** give the mechanism the knowledge the proof
     assumes it lacks — ORACLE variants (labeled ORACLE, current-cell GT
     for confidence ONLY, release untouched): ORACLE-d1 (M3's d1 confidence
     set to its true conditional accuracy), ORACLE-full. If an ORACLE
     variant clears the step, the residual is KNOWLEDGE-bounded (state
     exactly which knowledge, and whether any legitimate channel could
     carry it). If no ORACLE variant clears it, say so.
  3. **Constraint variation:** relax each load-bearing premise MINIMALLY,
     one at a time (B9X: release variants; ceiling variants; p0=1.0;
     d1-from-empty-class), and identify which single relaxation clears the
     step. The minimal clearing relaxation names the load-bearing
     constraint.
  4. **p0=1.0 probe:** an empty (f1,f5) class with p0=1.0 yields d1 conf
     exactly 1.0 — test whether this clears the step and what breaks
     elsewhere (B13? B3 elsewhere?). Report, do not adopt without a
     stated principle.
**Decision rule Q1a:** proof SURVIVES ⟺ no in-class mechanism found (1),
no ORACLE variant clears it (2), and exactly the predicted premises are
load-bearing (3). Then verdict = ARCHITECTURE (constraint-bound), naming
the binding conjunction. Proof REFUTED ⟺ any of (1)–(3) produces a
clearing mechanism — then verdict = KNOWLEDGE (if 2) or ARCHITECTURE with
a named fix direction (if 1 or 3), and the v1 "proven" claim is STRUCK.

**Q1b/c: ceiling/O rises (+0.019/+0.005). Selection vs knowledge.**
Two competing accounts: (i) SELECTION-structural — frozen B9 release
shrinks the released set by below-mean abstention, so any margin-correlated
confidence has rising survivor means; (ii) KNOWLEDGE — d1 confidence is
wrong (poisoned classes) and no legitimate feature separates O-correct
from P-wrong.
The crew MUST run both:
  1. **ORACLE knowledge injection** (labeled ORACLE): confidence set from
     current-cell GT (d1 included), release frozen. Clears the rises ⟹ the
     rises are KNOWLEDGE-bounded (d1 knowledge is the binding lack).
  2. **B9X release-design exploration** (labeled B9X, REPORTED not adopted):
     genuinely different selection designs — fixed-cohort release (same
     items released at every depth), margin-decorrelated release, and at
     least one crew-designed alternative. Each is scored on the FULL bar
     set. A B9X design that clears the O-rises while holding B1/B2/B4–B8
     and not worsening B13 ⟹ the residual is SELECTION-ARCHITECTURE and
     the report must state whether B9 should be amended (Micah's call).
  3. **Margin-decorrelated confidence** (in-class): confidence as a
     function of (f1,f5,personal history) engineered to be UNCORRELATED
     with M4's release criterion within honest families, without
     family labels and without anti-calibration (must pass Q2's gaming
     probes). Clears the rises ⟹ architecture fix inside the class.
**Decision rule Q1b/c:** KNOWLEDGE ⟺ (1) clears and (2)/(3) do not.
SELECTION-ARCHITECTURE ⟺ a B9X design clears with bars held.
ARCHITECTURE-deeper ⟺ none clear — then the crew must state the exact
joint obstruction (candidate: per-item nonincreasing + shrinking released
set + margin-correlated confidence ⟹ survivor-mean rise is forced; prove
or refute this lemma in Zag).

## §2 Q2 — Gaming vs calibrating ("how is TNN knowing what confidence is a bad thing and gaming? Test it first.")

The v1 crew REJECTED anti-calibrated fixes as "bar-gaming" by assertion.
This round replaces the label with a measurement. **Mechanism under test:
m11.** Comparators: the rejected alternatives head-to-head —
symmetric-continuity floor, deliberate-understatement variants (at least
two strengths), each WITH gaming-detection probes attached, so rejection
(or adoption) rests on evidence.

**Trap battery (labeled TRAP, designed AFTER this freeze, held-out from
all tuning — the mechanism never saw these items):**
  - **T1 principle-vs-bar:** items where m11's stated principle
    ("narrowest reference class", pessimistic bound) HURTS the bars —
    e.g. honest-correct items with one early personal wrong (0/1 then
    correct): the cap craters confidence (B13 cost). Principle-following
    predicts the crater; gaming predicts selective sparing.
  - **T2 selective binding:** measure WHERE the personal cap binds across
    the matrix. Gaming signature = cap binds exactly where a B3 rise
    would otherwise occur, with residual bar-correlation after
    conditioning on (personal record, class rate). Calibration signature =
    binding is a pure function of (personal record vs class rate), no
    residual bar-correlation. Test both signatures statistically.
  - **T3 held-out calibration:** new (f1,f5) patterns, experimenter-known
    true conditional rates, mechanism-blind. Measure |conf − true_rate|
    and bar-ward bias. Tuned-to-matrix behavior shows here as
    miscalibration; principled behavior tracks truth.
  - **T4 prior probe:** p0=0.95 was TUNED (§3 disclosure). Test an
    empirical-Bayes / self-estimated prior (principle-stated) against
    p0=0.95 on bars AND traps. If only the tuned value passes, the prior
    is bar-knowledge smuggled as a constant — report it as such.
**Channel audit:** the mechanism never sees the analyzer — enumerate every
input channel (f1..f8, online GT, personal history) and state for each
whether it can carry bar-information; the "how would it know" question
gets a white-box answer, not a shrug.
**Decision rule Q2:** CALIBRATING ⟺ (a) T3 tracks truth (no systematic
bar-ward bias), (b) T2 shows no residual bar-correlation, (c) T1 follows
the principle at bar-cost, (d) channel audit shows no bar-information
channel. GAMING ⟺ any of (a)–(d) fails with bar-ward deviation — name the
channel and the deviation. Per-comparator verdicts required; a rejected
alternative that PASSES the traps must have its rejection RECONSIDERED in
the report.

## §3 Q3 — B13 at scale (degrading with scale is unacceptable)

**Diagnosis first (all three, measured):**
  - **D1 prior washout:** per-class (c,t) at s1/s10/s100; plot conf vs t.
    CONFIRMED ⟺ conf declines toward the class true-rate as t grows and
    the O-class true rate ≈ 0.55 explains G ≈ −0.45.
  - **D2 fixture shift:** are s10/s100 items i.i.d. from the s1
    distribution? Compare family/measure composition across scales; run
    s1-sized subsamples of the s100 battery through the s1 pipeline.
    FIXTURE problem ⟺ subsample B13 ≠ s1 B13 (composition, not scale).
  - **D3 mechanism (pessimistic drift):** ablate the personal cap at scale
    (m9 vs m11 at s10/s100). The cap only LOWERS conf — if m9 has fewer
    B13 violations at s100 than m11, the cap contributes to the
    degradation; report the split.
**Then fixture variations head-to-head at s1/s10/s100** (Micah's
direction — fixtures that make B13 BETTER at scale):
  - **FIX-A prior-anchoring:** curriculum fixtures anchoring the prior
    against washout (principle stated; must pass Q2 gaming probes —
    a non-washing prior is guilty until proven principled).
  - **FIX-B scale-graded calibration:** interleaved calibration items
    whose difficulty scales with t, keeping the ledger's effective rate
    anchored.
  - **FIX-C underconfidence traps:** items that punish underconfidence at
    scale, counteracting pessimistic drift.
  - At least one crew-designed FIX-D.
**Target (exact):** B13 violations nonincreasing with scale
(viol_s100 ≤ viol_s10 ≤ viol_s1), B3 not worsened vs m11 (≤3), B2 = 0
held, no other bar broken, gaming probes passed.
**Decision rule Q3:** MECHANISM ⟺ D1/D3 confirmed and no FIX-* hits the
target with bars held. FIXTURE ⟺ D2 confirmed or a FIX-* hits the target.
PRIOR-WASHOUT (mechanism sub-case) ⟺ D1 confirmed and a principled
scale-invariant prior hits the target. Report the measured split
D1/D2/D3 — no story without numbers.

## §4 Round rules (inherited + this-round allowances)

- Inherited from v1: pure Zag, zero RNG, pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, 3×
  byte-identical reruns (A/B/C, SHA-logged), frozen 37-leg matrix +
  frozen analyzer (`training/analyze.py`) byte-identical, s1/s10/s100
  protocol (§7), B2 = 0 non-negotiable, v1 §6 PROHIBITED list binds
  (no family/depth inputs, no bar-hardcoding, GT always disclosed).
- This-round allowances (ALL labeled, NONE silently adopted):
  ORACLE-* (knowledge injection, diagnostic only), B9X-* (release-design
  exploration, reported not adopted), TRAP-* (held-out trap batteries),
  FIX-* (fixture/curriculum variations).
- Commit discipline: prereg amendment FIRST (this file), then variant
  addenda pre-run, then results. No binaries, no `.zagd`.
- Honest-residual rule: if a question's verdict is negative, report the
  exact obstruction — bars are not weakened, residuals are not hidden.

## §5 Adoption

A mechanism/fixture is ADOPTED only if it (a) holds B2 = 0 at s1/s10/s100,
(b) B3 ≤ 3 (not worsened vs m11), (c) breaks no other currently-passing
bar, (d) PASSES the Q2 gaming probes (CALIBRATING), and (e) for Q3,
B13 nonincreasing with scale. ORACLE/B9X/TRAP variants are never adopted
(diagnostic). Anything adopted needs its principle stated per v1 §6.

## §6 Sign-off

- [ ] This amendment frozen & committed (before any crew runs)
- [ ] Q1 crew: verdict per residual (Q1a/Q1b/Q1c) with measured evidence
- [ ] Q2 crew: m11 + comparators, per-mechanism CALIBRATING/GAMING verdicts
- [ ] Q3 crew: D1/D2/D3 measured split + FIX-* head-to-head at s1/s10/s100
- [ ] All verdicts committed; parent report only when every question has a
      measured verdict
