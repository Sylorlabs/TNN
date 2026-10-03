# Preregistration: Unified Beam Build (U1-U7)

Date: 2026-09-30. Worker: Unified Beam Builder.
Status: FROZEN. Committed before any implementation.

## 1. Design adopted

The reconciled unified design U1-U7 from `beam_recon/BEAM_RECONCILIATION.md`
(commit `1f303396b`, BEAM-RECONCILED), which unifies:

- Design 1: `beam_redesign/BEAM_REDESIGN.md` (`27a8fd108`, niching + tax
  annealing + diverse IV, sections A/B/D; C rejected).
- Design 2: `beam_evidence/BEAM_EVIDENCE_DESIGN.md` (`e37b04c47`,
  Pareto-diverse D1-D5).

No amendment to U1-U7. The builder implements the reconciliation
verbatim, with operationalizations specified in section 3 below.
Any deviation requires a transparent prereg amendment before the
divergent code runs.

## 2. Scope and files

Three implementation files under
`docs/lab/research-lead/overnight-20260928/beam_unified/`:

- `r1u.zag`: R1 battery (5 seeds, P-RAND, F-PARCOND fam 5) with unified beam.
  Base: `q4_r1/r1.zag` (commit `e40cb1b51`).
- `r3u.zag`: R3 battery (Arms 1-2, fams 7-8) with unified beam.
  Base: `q4_r3/q4_r3.zag` (commit `023b4f84a`).
- `frecu.zag`: F-RECFOLD battery (3 instances x 5 seeds, fams 7-9,
  Phase-1 discovery only) with unified beam.
  Base: `q4_adv2_clean/frecfold_clean.zag` (commit `1c52f7dad`
  wave; source from `q4_adv2_clean/`).

Each file is a modified copy of its frozen base. ONLY the
beam/search machinery changes:

- `beam_extend` replaced by `beam_extend_u` (U1/U2/U3/U5/U6, F-NODOM
  and F-BLOAT instrumentation).
- `select_iv` replaced by `select_iv_u` (U4: top-1-per-species
  hypothesis set, disagreement machinery otherwise unchanged).
- R1 tie reporting replaced by U7 tier report.
- New helpers: species computation, pattern bitmask, histogram,
  U5 comparator, novelty selection. All generic (no target, family,
  or library knowledge).

UNCHANGED (byte-identical, verified by diff after assembly):

- Candidate generation loop inside beam_extend (beam members, NOTs,
  pairwise AND/OR/XOR). This is the F-BLOAT basis.
- `score_node` arithmetic (scalar still computed and stored for
  reporting; not used for retention ranking).
- `sealed` families, `passive`, `do_iv`, `true_correct`,
  `node_new_term`, `node_new_op`, `node_new_libterm`, sigtab,
  PRNG (`rng_next`, `rng_range` per-file variant preserved),
  drivers (`run_r1`, `phase1`, `phase2`, `main`), seeds, bars,
  evidence-loop structure (8 passive + 24 rounds + final extend).

`beam_sort` (defined but never called in any frozen file) is dropped.

## 3. U1-U7 operationalization

### U1: Pareto retention within species

Within each species, a candidate is retained iff no species-mate
strictly dominates it on (accuracy, then opc). Dominance: A dominates
B iff acc(A) >= acc(B) and opc(A) <= opc(B) with at least one strict.
Because opc is fixed within a species (species key includes the full
operator multiset; opc equals multiset size), this reduces to: within
a species, candidates are ordered by accuracy descending and the top
of the accuracy order is never pruned for a lower-accuracy species-mate.

### U2: Niching

Species signature: (tree depth, sorted operator multiset), computed
generically from the expression tree by iterative walk. No target,
family, or library knowledge enters the signature. Operator multiset
is the count vector [n_AND, n_OR, n_NOT, n_XOR]; depth is max
root-to-leaf edges (terminals depth 0).

Keep rule: top 4 per species by the U3/U5 ordering (section 3/U3,
3/U5). At most 8 species: if more than 8 non-empty species, merge the
two smallest (fewest members; tie broken by lower best accuracy)
iteratively until 8. Merging unions member lists; the merged species
then contributes its top 4.

Species slots: 28 of 32 (U6 reserves 4). Species are ordered by best
member (U3/U5 ordering); members are taken top-4-per-species in
species order until 28 slots fill. If the species phase yields fewer
than 28 (short species), fill the remainder from the global candidate
ordering (U3/U5), excluding already-kept.

### U3: Two-phase tax schedule

Rounds are 0-indexed per evidence loop. Rounds 0-15 (exploration):
rank by accuracy alone; the tax is computed and stored but ignored.
Rounds 16-24 (consolidation, including the final extend): rank by
accuracy, break ties by lower opc. The scalar score is never used
for retention ranking in either phase.

Round numbering: R1/F-RECFOLD phase1 loop r=0..23 are rounds 0..23;
the final extend is round 24. R3 phase2 initial extend is round 0;
loop r=0..23 are rounds 1..24 (phase follows the round number even
on early break).

### U4: Diverse IV hypothesis set

`select_iv_u`: from the beam (in beam order), take the first member
of each distinct species (species ids from `bspec`, written by
`beam_extend_u`), up to 8 hypotheses. Disagreement selection is
otherwise unchanged: for each unused x, c1 = ones among the H
hypotheses, d = H - |2*c1 - H|, pick max d (ties: lowest x, as in
the frozen code). R1 keeps P-RAND (`select_iv_rand`) unchanged per
its frozen policy.

### U5: Principled tie-breaking

Within the U3 ordering, ties (equal accuracy, and equal opc in
consolidation) break by:

(a) Evidence-disagreement distance: each candidate's correct/incorrect
    pattern on the current evidence is a bitmask (en <= 32 always).
    Within each (species, accuracy) group of size > 1, compute the
    bitwise majority pattern (ties at a bit go to 1); distance =
    popcount(pattern XOR majority). Prefer larger distance. Groups
    of size 1 get distance 0.

(b) Operator-histogram novelty: L1 distance between the candidate's
    [n_AND, n_OR, n_NOT, n_XOR] and the summed histogram over the
    previous round's beam members. Prefer larger distance.

(c) Recency: higher node id (allocated later). Prefer larger.

Full candidate ordering:
- Exploration: accuracy desc, (a) desc, (b) desc, (c) desc.
- Consolidation: accuracy desc, opc asc, (a) desc, (b) desc, (c) desc.

### U6: Diversity floor

4 of 32 slots reserved for structurally novel candidates. Among
candidates not kept by the species phase, with accuracy fraction
>= 50% ((correct*100)/en >= 50), compute novelty = L1(histogram,
mean histogram of the species-kept set); take the top 4 by
(novelty desc, accuracy desc, node id desc). If fewer than 4
qualify, fill from the global candidate ordering (excluding kept).
The 4 are appended after the 28 species-kept; the final 32 are then
globally ordered by (accuracy desc, opc asc, (a) desc, (b) desc,
(c) desc) so beam[0] remains the accuracy-first pick.

### U7: Honest tie reporting (R1)

Replace `taxoff_unique` with: compute max accuracy A over the beam;
N = count of beam members with accuracy == A; omin/omax = opc range
within the max-accuracy tier. Emit:

- `TIE=UNIQUE` if N == 1.
- `TIE=UNDERDETERMINED N=<N> OPCRANGE=<omin>-<omax>` if N > 1 and the
  tied members are not all the same node.
- `TIE=DEFECT` only if N > 1 and all tied members are the same node
  id (dedup failure canary; impossible under the sigtab dedup).

A self-check recomputes N by an independent loop; mismatch emits
`TIECHECK=FAIL`.

## 4. Instrumentation

- F-NODOM: after each retention, for every pruned candidate p with
  species s, check kept members k of species s: violation iff
  (p.acc > k.acc) or (p.acc == k.acc and p.opc < k.opc). Accumulate
  `NODOMV` per driver run; emit at end. Any NODOMV > 0 fires F-NODOM.
- F-BLOAT: each `beam_extend_u` records tn (candidate count, equals
  score_node calls). Emit `MAXSIMS=<max tn>` per driver run. The
  frozen baseline MAXSIMS is measured from instrumented copies of
  the frozen files (measurement only; baseline verdicts use the
  exact frozen binaries).

## 5. Frozen control baselines (to reproduce before the build runs)

- R1: `e40cb1b51`, 3/3 byte-identical md5
  `6f15d782940abdf824be99721dcc2d36`, verdict R1-FAIL, 0/5 seeds.
- R3: `023b4f84a`, 3/3 byte-identical md5
  `7ed09fda269b59cdbbf75e0df720661c`, verdict R3-FAIL
  (A1-PASS=1, A2-PASS=0; A2: hit_iv=24, 53/64, HAS_D=1).
- F-RECFOLD: `1c52f7dad` wave, sha256
  `fef761afc5e72daa833e7bb4a12b1525efbffafef2294219bb7d650632f2d048`,
  verdict FREC-ZERO-FAIL (B1 0/5 all instances; I2 constant-0
  63/64 all seeds).

Control step: recompile each frozen source with znc, run 3x, verify
byte-identical to the committed raw outputs (md5/sha256 above). If
any control fails to reproduce, halt and report; do not run the
unified build against a moved baseline.

## 6. Falsifiers (frozen)

- F-FIT: fewer than 4 of 5 R1 seeds reach EVFIT=32/32. (R1 driver,
  P-RAND, fam 5.)
- F-DIVERSE-FAIL: R3 Arm 2 still fails its frozen bar (A2-PASS=0:
  requires 64/64 AND reuse_iv*2 <= scratch_iv AND HAS_D=1).
- F-NODOM: NODOMV > 0 in any driver run.
- F-TIE-HONEST: `TIE=DEFECT` or `TIECHECK=FAIL` appears in R1 output.
- F-REGRESS: R3 Arm 1 A1-PASS goes from 1 (frozen) to 0
  (requires 64/64 AND reuse_iv*2 <= scratch_iv).
- F-BLOAT: any driver's MAXSIMS exceeds 1.10 * the frozen
  instrumented baseline MAXSIMS for the same battery.
- F-CASE: audit finds any new-machinery component keying on target,
  family, or library identity (target value, fam number, or
  installed-D signature/behavior). Generic machinery only.

F-RECFOLD (`frecu.zag`) is an exploratory run, not a falsifier: the
unified beam targets W1/W3/W4 (R1/R3); W2 (I2 constant-prediction
ceiling) is a distinct failure the design does not claim to fix.
Report B1/B2/B3 per the frozen F-RECFOLD bars for information.

## 7. Kill bars (this build task)

- K1 (prereg frozen before implementation): this document committed
  strictly before any unified-beam source is written. Commit-order
  self-check required.
- K2 (all falsifiers run): R1 (5 seeds), R3 (Arms 1-2), and
  F-RECFOLD (3x5) complete under the unified beam; every falsifier
  in section 6 evaluated and reported.
- K3 (pure Zag, deterministic): Zag at every stage (authoring,
  building with znc, running, verification via shell tools only:
  sha256sum, md5sum, cmp, grep, wc, git). Zero Python at every
  stage. 3/3 byte-identical runs per battery, zero stderr bytes.
  Zero em/en dash bytes in loop documentation (shell-verified with
  `worker_snippets/check_no_dash.sh`).

## 8. Verdict rule (frozen)

- BEAM-UNIFIED-PASS iff K1-K3 hold AND no falsifier in section 6 fires.
- BEAM-UNIFIED-FAIL otherwise, naming each fired falsifier and the
  measurement that fired it.

Honest scope (frozen): a PASS is bounded-L2 search robustness for
compositional reuse and evidence fitting. Not L3, not Criterion 0,
not a Q4 revival (the revival conjunction is dead: R1-FAIL,
R3-FAIL, R4-FAIL per `563a1b354`). Fitting 32/32 does not imply
64/64 generalization.

## 9. Governance

- Prereg-first; no implementation before this commit.
- Frozen base sources are never edited; work happens on copies in
  `beam_unified/`.
- The contaminated research paper is not touched.
- Commits local, owned pathspec only
  (`docs/lab/research-lead/overnight-20260928/beam_unified/`).
- Other workers' files are not touched. In particular,
  `beam_impl/` (Design-1 builder in flight) is left alone; its
  completion is an independent data point.
- If a git lock is encountered, wait; never remove a live lock.

## 10. Purity disclosure

During task setup the worker invoked `python3 -c "pass"` once as a
scratch shell probe before recalling the absolute pure-Zag rule.
No Python touches any work product (prereg, sources, builds, runs,
verification, byte checks). This disclosure is recorded here so the
K3 claim is auditable: the violation was pre-prereg, process-only,
and is not repeated.
