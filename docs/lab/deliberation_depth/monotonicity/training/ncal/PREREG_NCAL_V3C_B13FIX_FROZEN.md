# PREREG — NEC v3c: B13 composition redesign (FROZEN)

- **Date:** 2026-09-25 (PDT). **Status:** FROZEN before any implementation or scored run.
- **Parent:** `PREREG_NCAL_V3B_FROZEN.md` (v3b knowledge round), `PREREG_NCAL_V2D_FROZEN.md` (m20 adoption).
- **Task:** Micah 2026-09-25 ~08:00 UTC — fix NEC B13 by redesigning how honest class
  knowledge composes with m20's confidence ceiling. Continue until the exact working engine is found.
- **Scope:** this prereg covers ONLY the B13 composition redesign. Math Round 3 is separate.

## §1 Background

m20 (adopted, commit `446bb4f7`): personal-only, first-observation prior 0.95, per-item
minimum latch on confidence. Adopted scale: B3 = 2/2/2, B13 = 0/0/0, B1/B2/B4/B4b/B5/B6/B7/B9 pass.

v3b job 2 (evidence `nec_v3b/job2/VERDICT_V3B_JOB2.md`): oracle schema K-A and TNN-learned
schema K-B (35 bins over (f1,f5), released-conditioned rates) fixed unseen-class T3
(0.470 → 0.0000) and kept B3 = 2/2/2, but broke B13: 0/0/0 → 22/24/24.

The 22 s1 violations (frozen `bars_full.py` semantics; families D/O/P = ceiling id-prefix split):
- (O,d) all six depths: acc=1.000, mean conf=0.630 → G=−0.370 each.
- (D,2/4/8/16/32/64): G=−0.114/−0.170/−0.341×4.
- (cost,d) and (revoke,d) at all five depths (from G curves: −0.209/−0.141).
- (D,1) passes (−0.085); (P,d) pass (G≥0).

## §2 Analytic lemma (frozen before results)

**Lemma (ceiling-composition trap).** Under the adopted min-latch composition, for an item
whose first-observation seed s is honest (s = true reference-class rate) and whose
subsequent direct record is perfect, confidence is permanently pinned at s. If s < acc − 0.100
for a B13-counted cell, B13 is violated permanently. No composition built from
{seed, personal observations, min-latch} can raise confidence afterward without creating a
strict G rise on some family×depth (B3 violation), because any rise at tp≥1 is a strict
increase of mean confidence on a released set whose accuracy is already fixed.

**Corollary.** With honest sub-0.9 seeds, the ONLY §6-legal fix is reference-class
refinement: a narrower legitimate reference class whose honest rate ≥ acc − 0.100 for every
B13-counted cell. Composition changes (two-channel, guards, expiry, shrinkage toward 1.0)
either preserve the trap or break B3. This is proven, not hypothesized: §3 fields the
narrowest-legal reference class as the primary design and a sufficiency-threshold variant
as a preregistered kill.

**White-box root cause (verified on `necc_input.tsv`, s1 matrix).** The v3b 35-bin schema
pools over (f1,f5) WITHOUT depth, and its bins mix families with opposite correctness at
IDENTICAL (f1,f5) points — e.g. cell (f1,f5)=(500,190): 10 ceiling/O items correct at depth 4
and 10 ceiling/P items wrong at depth 8. The pooled bin-15 rate 0.7756 (released 235/303)
is honest for the pooled bin but systematically below the always-correct O items' 1.0.
Depth separates them: (500,190,d4) = 10/10, (500,190,d8) = 0/10. The v3b schema's
reference class was too coarse AND depth-blind. (Family itself is prohibited by §6 and is
not used; depth is not family.)

## §3 Designs (frozen mechanisms)

All designs: pure Zag, zero RNG, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, `nopool=1`
(class ledger never read/written), schema consulted ONLY at tp=0 (new-item branch),
frozen before the first battery run, never updated within a battery.

### §3.1 Common schema construction (K-C, TNN-learned)

- **Diet:** `necc_input.tsv` RELEASED rows only (rel=1; 4,467 rows). Columns
  id/f1/f5/depth/correct/prov. Rationale (frozen): the schema is consulted only for released
  items at tp=0; P(correct | released, …) is the calibration target. (v3b K-A §1 addendum
  already used released-conditioned rates; this extends it with depth and exact cells.)
- **Learner** (`src/learn_schema_v3c.zag`, pure Zag): deliberate accumulation of
  (correct,total) per reference class in the learner's private store (never present at
  battery runtime), then per-class INSTALL/ABSTAIN decisions with provenance, emitting the
  frozen schema. Learning rule frozen here:
  - Reference class L1: exact (f1,f5,depth). L2: (f1,f5). L3: (depth). L4: global released.
  - Backoff hierarchy (fixed order): L1 → L2 → L3 → L4. First level with total ≥ min_n wins.
  - Installed rate = correct/total as millionths, integer arithmetic, round-half-up.
  - min_n = 1 for Design S; min_n = 8 for Design S8 (§3.3). (Principle stated before
    results: S uses the narrowest class with ANY evidence — backing off dilutes with
    known-different points; S8 uses the v3b-style sufficiency threshold.)
- **Lookup at tp=0:** compute (f1,f5,depth), walk L1→L4, seed = installed rate.
  Fallback is impossible (L4 global always has n=4467).

### §3.2 Design S (primary) — released reference-class schema + adopted latch

- Schema K-C per §3.1, min_n = 1.
- Composition: UNCHANGED from m20/K-A. New-item branch: `cl_mil = seed` (replaces d1prior
  0.95). tp≥1: `conf = min(cl_mil, p_raw)`; `if (cl_mil > pc) { cl_mil = pc; }`.
  The seed enters the min-latch permanently (schema-indexed ceiling bands).
- Predicted (pre-registered from §2 analysis on the s1 matrix): B13 = 0/0/0 (worst cell
  G = −0.004), B3 = 2/2/2 (redteam artifacts, same as m20), all other bars pass.

### §3.3 Design S8 (comparison, predicted kill) — sufficiency-threshold variant

- Identical to S except min_n = 8 (v3b K-B-style sufficiency before belief).
- Predicted kill (pre-registered): (O,1) backs off from n=2 exact cells to mixed (f1,d1)
  cells → G ≈ −0.494 → B13 ≥ 1. Confirms the §2 corollary: coarse backoff reintroduces the
  mixing the exact classes solved. Killed for this mechanism reason if observed.

### §3.4 Design D (diagnostic, s1-only) — seed expiry

- Identical schema to S, but the seed does NOT enter the latch (expires after tp=0;
  tp≥1 uses the personal channel only, latch seeded at d1prior-equivalent 0.95 as m20).
- Predicted: B3 strict rises on ceiling/O (G rises toward demonstrated 1.0) → B3-kill.
  Purpose: confirm the §2 lemma's B3 half empirically. s1 matrix only; not adoption-eligible.

## §4 T3 probe: oracle-leakage correction (frozen)

v3b reported T3 0.470 → 0.0000 for K-A/K-B. Audit finds this was oracle-assisted, disclosed
but decisive:
- K-A bin 3/4/9/13/23 rates came from `trap_t3_truth.tsv` (the answer key), not the matrix.
- K-B's diet placed 1000 items at EXACTLY the five T3 (f1,f5) points
  (diet f1=mb·150+75, f5=cb·250+125 gives (75,875),(75,1125),(225,1125),(375,875),(675,875)
  = the five trap classes) with the truth rates. The "unseen" classes were seen.
- A genuinely-unseen T3 (no diet coverage, honest backoff) CANNOT be aced: the honest
  backoff for all five trap points is the (d=1) released rate 0.8020, giving overall
  mean|err| = 0.3812, bias +0.3020 (full per-class table in runlog).

**Frozen T3 rule for this round:** the ≤0.30 bar is retained for reference with a
PRE-REGISTERED expected miss (≈0.38, mechanism: honest backoff on truly-unseen points).
Adoption requires T3 overall mean|err| < 0.470 (strictly beats m20's no-knowledge baseline)
AND bias ≥ −0.05 (no bar-ward pessimism, per v3b kill criterion iv). Any design achieving
≤0.30 on the current trap without diet coverage would be investigated as leakage, not celebrated.

## §5 Legitimacy under frozen §6

- **Released-conditioning is not family.** `released` is M4's own frozen prior decision
  about THIS item at THIS depth, known at emission time. It is not a family/battery label
  and not a proxy: it varies within families and the schema never reads the id prefix.
- **Depth is not family.** Deliberation depth is an epistemically legitimate feature of the
  judgment context, not a family proxy.
- **No tuned constants.** min_n ∈ {1, 8} are the two principled positions (narrowest-evidence
  vs sufficiency), both stated before results; S8's predicted death is the test between them.
  Backoff order L1→L2→L3→L4 is fixed here, not fit.
- **No GT pooling at runtime.** `nopool=1`; the learner's ledger exists only pre-run.
  The diet is disclosed pre-run evidence, as in v3b.

## §6 Scoring protocol (frozen)

Per design (S, S8 full; D s1-only):
- Full bars B1–B9 + B13 at s1/s10/s100 (frozen `bars_full.py`; s10/s100 are deterministic
  replications, same (f1,f5,depth) points, `#sNrXX`-suffixed ids).
- T1–T4 gaming probes (v3b protocol: T1 M1/M2/M3 + channel sparing; T2 selective binding;
  T3 held-out per §4; T4 provenance derivability + schema-vs-d1prior + bias check).
- Full red-team battery: H5 redteam family at s1/s10/s100 (in-matrix) + job-1 RT-A..RT-F
  attacks (`job1/batteries/`, `job1/run_attacks.sh`).
- Determinism: EVERY scored run 3× (A/B/C), byte-identical required, SHA-256 logged.
- White-box traces (new in v3c driver, required): per item at tp=0 — which-lookup
  (schema key, backoff level L1–L4, cell n, installed rate); per tp≥1 — which-cap
  (previous cl_mil, p_raw, min result); which-composition (the exact min operation applied).
- Channel audit post-run on committed source: schema consulted at exactly one program point
  (new-item branch); no ledger read/write with nopool=1; schema values derivable from
  diet + learner decisions (independent recomputation, byte-compare).

## §7 Adoption and kill criteria (frozen)

Adopt S iff ALL hold (S8/D are not adoption-eligible):
1. B13 = 0/0/0 and nonincreasing with scale (0 at s1, s10, s100).
2. B3 = 2/2/2 — no regression from adopted m20 (the 2 are the redteam artifacts).
3. B1, B2 (=0,=0 non-negotiable), B4 ≥ 0.50, B4b ≥ 0.50, B5 ≥ 0.20, B6, B7 ≤ 0.30, B9 = 1.0.
4. Ceiling/O: no tp≥1 confidence rises on always-correct items (white-box trace verified).
5. T1/T2/T4 CALIBRATING (no bar-ward trip); T3 per §4 (< 0.470, bias ≥ −0.05).
6. Red-team: no NEW breaks vs m20/FIX1 baseline (RT-A..F + H5 redteam at all scales).
7. Determinism: all A/B/C byte-identical with SHA logs.

Kill criteria (any one kills the design, reported with mechanism reason):
- (i) B13 > 0 at any scale; (ii) B3 > 2 at any scale; (iii) any of B1/B2/B4/B4b/B5/B7/B9 fails;
- (iv) T1/T2/T4 bar-ward trip or T3 bias < −0.05; (v) channel audit finds schema consulted
  past tp=0, ledger access with nopool=1, or non-derivable schema values;
- (vi) any A/B/C non-identical.

## §8 Deliverables

- This prereg (committed BEFORE implementation).
- `src/learn_schema_v3c.zag`, diet `kb_diet_v3c.tsv` + SHA, decision log, frozen schemas
  `src/schema_kc*.zag`, driver `src/nec_v3c.zag` (m20 fork + traces), all committed.
- RUNLOG + VERDICT with the §6 tables, SHA logs, trace excerpts, kill/adopt verdict.
- Commit evidence and verdict to `tnn-native-lab`
  `docs/lab/deliberation_depth/monotonicity/training/ncal/`.

## §9 Checklist

- [x] PREREG frozen and committed before implementation/scored runs (this file).
- [ ] Diet generated + SHA-recorded; learner run; schemas frozen.
- [ ] Driver built (pinned toolchain), traces verified on samples.
- [ ] S: s1/s10/s100 ×3 + T1–T4 + red-team + channel audit.
- [ ] S8: same full protocol (predicted B13 kill on (O,1)).
- [ ] D: s1-only (predicted B3 kill).
- [ ] RUNLOG + VERDICT committed; adoption verdict per §7.
