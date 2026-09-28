# PREREG — Job 3: Adversarial Test for the Affine Memorizer (FROZEN 2026-09-27)

**Question (Micah's order, verbatim):** "is there a salt/transformation family
under which genuine combiners pass and affine memorizers provably cannot?"

**Status:** FROZEN 2026-09-27. Any change needs Micah's re-approval.
**Context:** Amended D1 battery complete (commits `de80a32001`, `03ba8919e`).
Crew E (independent red team) found the residual: a per-token offset+slope
(affine) memorizer passes P0 8/8 on droplast and upperfirst and chains pair
(3,4) 3/4 under the enacted A2 salt — generator-algebra exploitation, not
rule learning. Enacted A2 carved the linear-shift memorizer out as "genuine
transformation-learning"; Crew E showed the carve-out's premise does not
survive contact with the mechanism. This job answers Micah's question head-on.

## 1. Operational definitions

**Algebraic memorization** (the Crew-E class under test). An agent that:
- (M1) stores the taught single-part input→output pairs verbatim;
- (M2) for a probe, FITS a per-token algebraic map from the probe to a
  training token — specifically a 2-parameter affine map on raw bytes,
  `p[k] − t[k] ≡ o + s·k (mod 26)` — solved from positions 0,1 and verified
  on the rest (fit requires token length ≥ 2; length-1 admits no fit);
- (M3) emits the taught output transformed by the SAME fitted `(s,o)`
  (per-position, preserving each output position's case);
- (M4) contains NO representation of any rule — no string-rewriting logic,
  no position maps, no per-character semantics.

**Genuine combining** (the positive control). An agent that:
- (G1) implements the six D1 rules as pure string functions (position maps +
  per-character maps; §4), receiving ONLY the probe string — never a token
  index, never a salt constant, never a taught pair;
- (G2) applies the presented rules in the presented order;
- (G3) withholds (emits the input unchanged) when no rule is presented.

**Why the pair discriminates.** The memorizer's correctness is contingent on
TWO algebraic facts it does not control: (i) the probe/train cross-phase
difference must lie in its fitted family (affine in k); (ii) each rule must
commute with the fitted map family. The combiner's correctness depends on
neither: its mechanism is the rules themselves. A salt family that breaks
(i) while leaving the rules untouched kills the memorizer and cannot move
the combiner. Salt-sensitivity of scores is itself the signature:
a memorizer’s scores move with the salt; a combiner’s do not (K-J3-3).

**Threat model (scope of "provably cannot").** The claim is relative to the
FIXED 2-parameter affine class (M1–M4) — the class Crew E flagged. It does
not cover memorizers with more parameters (see §9, the degree ladder) and
it cannot cover the fully-general per-position-delta clone on
position-identity rules (see §9, principled limit). Both boundaries are
characterized, not hidden.

## 2. The six rules (unchanged from D1)

0 reverse · 1 dupfirst · 2 rotleft · 3 droplast · 4 upperfirst · 5 sortchars.
Pure string functions; byte-exact definitions in the test source.

## 3. Salt arms (the families under test)

Token `tok(arm,phase,i)`, length `2+(i%4)`, byte `k` (0-based):

- **Arm A — AFFINE (baseline, enacted A2 formula verbatim):**
  `97 + (7i + C1[ph]·k + k²) mod 26`, C1 = train 13, P0 17, P2 19, P3 23.
  Cross-phase difference: `7Δi + ΔC1·k` — affine in k (the k² cancels).
  The memorizer is known to survive here (Crew E).
- **Arm C — QUADRATIC (second family, new):**
  `97 + (7i + C1[ph]·k + C2[ph]·k²) mod 26`,
  C2 = train 3, P0 5, P2 7, P3 11.
  Cross-phase difference: `7Δi + ΔC1·k + ΔC2·k²` — genuinely quadratic.
- **Arm B — CUBIC (non-affine arm; the governance question):**
  `97 + (7i + C1[ph]·k + C2[ph]·k² + C3[ph]·k³) mod 26`,
  C3 = train 2, P0 3, P2 6, P3 7.
  Cross-phase difference: `7Δi + ΔC1·k + ΔC2·k² + ΔC3·k³` — genuinely cubic.

**Constant-selection rules (frozen; part of the design, not tunable per run):**
- (R1) For every phase pair and every salted degree d: `ΔC_d ≢ 0 (mod 26)`
  (else that degree's protection vanishes for the pair).
- (R2, cubic arm) For every phase pair: `2·ΔC2 + 6·ΔC3 ≢ 0 (mod 26)` —
  the second difference of the cross-phase polynomial at k=0; if it vanished,
  the cubic difference would be affine on positions {0,1,2} (found by
  prototype 2026-09-27: C3[P2]=5 gave `2·4+6·3=26≡0`, admitting affine fits
  on length-3 probes; corrected to C3[P2]=6).
- (R3) Length-2 tokens admit VACUOUS affine fits (2 parameters, 2 points —
  always solvable). This is not a defect; it is a mechanism-named boundary
  (see §7 predictions). Item lengths stay 2–5 (D1 structure).

## 4. Items (fresh; per arm)

- **Teach:** token indices 0–5 and 700–705 with train salt; all 6 rules
  applied to each (72 taught pairs). The memorizer memorizes these; the
  combiner never sees them.
- **P0 (mastery):** 48 probes, 8 per rule. Indices: the first 48 integers
  ≥100 whose tokens are NOT already sorted under ANY arm (item-validity
  gate G5 — a sorted probe cannot test sortchars; the memorizer's identity
  fallback would score it without any fit). Fixed list, committed with the
  test. Per-rule length-2 counts: [1,0,2,2,2,2] (rules 0–5).
- **P2 (composition):** all 30 ordered pairs (i≠j) × 4 items (lengths
  2,3,4,5), indices 200–319, P2 salt. The pair is presented directly
  (amended-D1 direct-pair style); the agent applies both in order.
- **P3 (reflex):** 8 probes, indices 400–407, P3 salt, no rule presented;
  correct = emit input unchanged, or explicit "?" withhold. Any other
  output = reflexive-application count.

**Pre-run gates (logged; must pass or the run is void):**
- G1: zero probe tokens byte-identical to any same-length train token
  (a byte-identical pair admits the trivial (s,o)=(0,0) fit under any salt).
- G2': zero NON-VACUOUS affine fits (length ≥ 3) of any P0/P2/P3 probe
  against any same-length train token — on arms B and C (on arm A the fits
  are expected: 360 counted in prototype).
- G3: R1/R2 hold (verified in code, logged).
- G4: byte-identical rerun (run twice, diff).

## 5. The affine memorizer (clean-room spec of the Crew-E class)

- **P0** (rule r, probe p length n): if r=5 (sortchars) and p already sorted,
  emit p (Crew E's identity fallback; unreachable under G5, kept for
  fidelity). Else for each train token t of length n in index order: fit
  `(s,o)` from k=0,1 in RAW-BYTE space mod 26, verify k≥2; first success
  wins; emit `taught_r(t)` with per-position `+o+s·k'` in that position's
  case space (upper stays upper). No success → "?".
  (Raw-byte fitting reproduces Crew E's (4,3)=0 fragility: the
  uppercase/lowercase boundary breaks the fit — a documented class
  property of their implementation, kept deliberately.)
- **P2** (rules a,b; probe p): fit `(s1,o1)` on p vs first length-matching
  train token; synthesize step-1 intermediate
  `m1[k'] = taught_a(t)[k'] + o1 + s1·k'`; fit `(s2,o2)` on m1 vs first
  length-matching train token; emit transformed `taught_b(t2)`.
  Length-1 intermediates admit no fit → "?".
- **P3** (probe p, no rule): try rules 0–5 in order with the full P0
  procedure; emit the first successful output; "?" iff all fail.
  (Constructed policy, preregistered: a fit-driven agent emits whenever any
  fit fires.)

## 6. The genuine combiner (positive control)

Pure string functions on the probe string only (white-box audited: no
generator constants, no indices, no taught pairs in its code path).
P0: apply the rule. P2: apply a then b. P3: emit the input unchanged.

## 7. Predicted signatures (mechanism-derived, EXACT — the test asserts these)

**Memorizer.**
| Arm | P0 | P2 | P3 |
|-----|----|----|----|
| A (affine) | [0,0,0,8,8,0] = 16/48 | 5/120: (3,4)=3/4 (lengths 3,4,5; length-2 miss: length-1 intermediate admits no fit); (5,3)=1/4 idx312; (5,4)=1/4 idx316 | 0/8 (every fit fires, every emission wrong) |
| B (cubic) | [0,0,0,2,2,0] = 4/48 — the 4 are EXACTLY the length-2 probes of rules 3,4 (vacuous fits: 2 parameters on 2 points always solve; droplast/upperfirst have identity position maps so the vacuous fit is exact) | 2/120: (5,3)=1/4 idx312; (5,4)=1/4 idx316 — both are the sorted-train accident (below); (3,4)=0/4 | 6/8 — withholds on the 6 length≥3 probes (no fit exists); emits-wrong on the 2 length-2 probes (vacuous fits fire) |
| C (quadratic) | identical to B: [0,0,0,2,2,0] = 4/48 | identical to B: 2/120 | identical to B: 6/8 |

Accident characterizations (all deterministic; red team re-verifies each):
- **Sorted-train accident** (idx312 (5,3), idx316 (5,4), all arms): probe
  length-2 AND sorted, first length-2 train token (idx 0) sorted
  ('ao'/'ar'/'ap' on A/B/C). Step-1 fit vacuous; sort(t₀)=t₀ makes the
  step-1 intermediate exactly the probe; step-2 (droplast/upperfirst,
  identity position maps) then scores exactly. Salt-independent.
- **(3,4) on arm A** (lengths 3,4,5): the genuine Crew-E chain —
  droplast and upperfirst both commute with per-position affine maps, so
  the fitted map propagates through both steps. NOT an accident: this is
  the flagged residual itself.
- P3 on B/C is "withhold for the wrong reason" (no fit exists) — reported
  as mechanism evidence, not as mastery.

**Genuine combiner:** P0 48/48, P2 120/120, P3 8/8 on ALL THREE arms
(salt-invariant by construction: pure string functions).

## 8. Kill bars

- **K-J3-1 (DISCRIMINATION):** On arm B the memorizer scores EXACTLY the
  §7 row (P0 = [0,0,0,2,2,0] with the 4 hits exactly the length-2 probes of
  rules 3,4; P2 = 2/120 exactly the two characterized accidents; zero
  non-vacuous exploitation anywhere) AND the combiner scores 48/48,
  120/120, 8/8. → the cubic salt discriminates the affine class.
  If the memorizer scores ≥7/8 on ANY arm-B part, or >2/120 on arm-B P2
  beyond the named accidents, or any length≥3 arm-B probe is passed via a
  fitted map → the family FAILS to discriminate: claim killed.
- **K-J3-2 (FIDELITY):** On arm A the memorizer reproduces the Crew-E
  essential signature EXACTLY: P0 = [0,0,0,8,8,0] (sortchars 0/8 per G5;
  Crew E had 2/8 via two sorted probes, excluded here by the item-validity
  gate — difference documented, mechanism identical), P2 = 5/120 with the
  §7 pattern including (3,4)=3/4 and (4,3)=0/4, P3 = 0/8. Else the
  reimplementation is unfaithful: rebuild, no verdict.
- **K-J3-3 (INVARIANCE):** the combiner's per-phase scores are identical
  across arms A/B/C (48/48, 120/120, 8/8 each). Else the positive control
  is salt-sensitive and the instrument is confounded: no verdict.
- **K-J3-4 (RED-TEAM):** the independent red team (§10) must FAIL to
  (a) extend the memorizer WITHIN the 2-parameter class (no new parameters,
  no per-position free deltas) to pass any arm-B part at ≥7/8 or any arm-B
  pair at ≥1/4 beyond the §7 accidents; and (b) exhibit any
  generator-algebra access (indices, salts, taught pairs, fitted maps) in
  the combiner's probe code path. If (a) succeeds → "provably cannot" is
  killed. If (b) succeeds → the positive control is void.

## 9. Verdict logic

- If K-J3-1–K-J3-4 all hold → **answer YES**: the cubic (non-affine) salt
  family — cross-phase token differences genuinely cubic in k — is a family
  under which genuine combiners pass (48/48, 120/120, 8/8, salt-invariant)
  and the affine memorizer provably cannot (its fit step is an
  overdetermined inconsistent congruence system on every length≥3 probe;
  verified zero non-vacuous fits, G2'). Proof mechanism: the k² term that
  A2 left unsalted is exactly the hole (it cancels cross-phase); salting
  the k² AND k³ coefficients with R1/R2 constants removes every affine
  cross-phase relation while the rules — pure string functions — never see
  the salt.
- Honest boundaries (part of the verdict either way):
  (i) **degree ladder**: a 3-parameter (quadratic-fit) memorizer beats arm C
  but not arm B; the kill is relative to the 2-parameter class, not an
  absolute "memorizer-proof" claim;
  (ii) **vacuous fits**: on length-2 tokens the affine model has 2
  parameters for 2 points — the memorizer is exact there on identity-
  position-map rules under ANY salt (predicted, §7);
  (iii) **principled limit**: a fully-general per-position-delta clone is
  behaviorally identical to the genuine rules on droplast/upperfirst under
  EVERY salt — no salt family can separate those behaviorally; the
  separation lives in the non-identity position-map rules, where the affine
  class already scores 0.

## 10. Independent red-team charge (BEFORE verdicts)

1. **Fidelity:** independently reimplement the memorizer from Crew E's
   report + §5 (not from the test source); arm-A outputs must match the
   test's item-by-item (or the deviation is adjudicated against §5).
2. **Within-class extension:** attempt to beat arm B WITHOUT new parameters
   (subset fits, robust fits over position pairs, transformed propagation
   of (s,o) through rule position maps, any 2-parameter trick). Success on
   any part/pair beyond §7 kills K-J3-4(a).
3. **Degree ladder:** build the quadratic-fit (3-parameter) memorizer; it
   SHOULD beat arm C and MUST NOT beat arm B (confirms the kill is
   degree-relative and arm B's constants are well-formed).
4. **Free-delta clone:** build it; it SHOULD score droplast/upperfirst 8/8
   on ALL arms (confirms the principled limit, §9(iii)) and MUST NOT score
   the other rules — else the analysis is wrong.
5. **Combiner audit:** white-box — the combiner's probe path touches no
   generator state; its arm-A/B/C outputs are identical.
6. **New angles:** any other exploitation (salt self-fitting, length
   oracle, train-token choice oracle, P3 policy variants). Characterize;
   kill bars only move if K-J3-4 is violated.

## 11. Deliverables & build notes

- This prereg (frozen, committed alone).
- `affine_test.zag` — pure-Zag instrument (generation, both agents,
  per-item scoring), zero RNG, pinned toolchain
  `znc_linux_x86_64_abed8aa1`; modes genA/genB/genC/memA/memB/memC.
- `score_job3.py` — deterministic aggregation + bar checks (no RNG).
- Run evidence: all six modes ×2 runs, byte-identical diffs.
- `redteam/` — independent report + attack code.
- `VERDICT_JOB3.md` — the plain-English answer.
- Commit to `tnn-native-lab` only (never main). No binaries, no `.zagd`,
  no caches (repo content standard).
