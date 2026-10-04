# Preregistration: Unified Beam Build, Clean Rebuild (U1-U7)

Date: 2026-09-30. Worker: Unified Beam Builder (clean rebuild).
Status: FROZEN. Committed before any implementation is written.

## 0. Standing rules name-check

- Pure Zag only. No Python at any stage: authoring, building with znc,
  running, verification (shell tools only: sha256sum, md5sum, cmp, grep,
  wc, git), byte checks (worker_snippets/check_no_dash.sh). Zero Python
  has been invoked from task start. No purity disclosure is needed.
- No em/en dash bytes in loop documentation (shell-verified before commit).
- Prereg commit strictly precedes implementation (commit-order self-check).
- Frozen base sources are never edited; work happens on copies under
  beam_unified_clean/.
- The contaminated research paper is not touched.
- Commits local, owned pathspec only
  (docs/lab/research-lead/overnight-20260928/beam_unified_clean/).
- Other workers' files are not touched.
- If a git lock is encountered, wait; never remove a live lock.

## 1. Design adopted

The reconciled unified design U1-U7 from
beam_recon/BEAM_RECONCILIATION.md (commit 1f303396b, BEAM-RECONCILED),
which unifies Design 1 (beam_redesign/BEAM_REDESIGN.md, 27a8fd108,
niching + tax annealing + diverse IV, sections A/B/D; C rejected) and
Design 2 (beam_evidence/BEAM_EVIDENCE_DESIGN.md, e37b04c47,
Pareto-diverse D1-D5).

No amendment to U1-U7. The builder implements the reconciliation
verbatim, with operationalizations specified in section 3 below.
Any deviation requires a transparent prereg amendment before the
divergent code runs.

Reference: the contaminated first attempt's prereg (1339b4471) is
cited as an operationalization reference only. Its verdict
(BEAM-UNIFIED-FAIL, dac4a4187) is governance-contaminated and is not
adopted. This clean rebuild re-derives baselines, re-implements from
the frozen sources, and freezes its own bars here.

## 2. Scope and files

Owned directory:
docs/lab/research-lead/overnight-20260928/beam_unified_clean/

Implementation files (modified copies of frozen bases):

- r1u.zag: R1 battery (5 seeds, P-RAND, F-PARCOND fam 5) with unified beam.
  Base: q4_r1/r1.zag (commit e40cb1b51, sha256
  26ed9643ebfd90c05bcb2c723f7109ca09a3c8ba722c1e77302e7e188c63c571).
- r3u.zag: R3 battery (Arms 1-2, fams 7-8) with unified beam.
  Base: q4_r3/q4_r3.zag (commit 023b4f84a, sha256
  da830caf4263a6bbccf24b24eea935be98f795d37e3a19ee7ce8c9c9ad92ac73).
- frecu.zag: F-RECFOLD battery (3 instances x 5 seeds, fams 7-9,
  Phase-1 discovery only) with unified beam.
  Base: q4_adv2_clean/frecfold_clean.zag (implementation commit
  5a21bb2b3, sha256
  659e0ca53f5c7b17077328d0a798324af294d57c8aac6968a79841d8cbde7450;
  zero-Python rerun 1c52f7dad).

Measurement-only baseline files (instrumented copies of the frozen
bases, used ONLY to measure the F-BLOAT ceiling; their outputs carry
no verdict):

- r1_base.zag, r3_base.zag, frec_base.zag.

Only the beam/search machinery changes in the implementation files:

- beam_extend replaced by beam_extend_u (U1/U2/U3/U5/U6, F-NODOM and
  F-BLOAT instrumentation).
- select_iv replaced by select_iv_u in r3u.zag and frecu.zag
  (U4: top-1-per-species hypothesis set, disagreement machinery
  otherwise unchanged). r1u.zag keeps select_iv_rand unchanged per
  the frozen R1 policy.
- R1 tie reporting replaced by the U7 tier report in r1u.zag.
- New helpers: tree depth, operator histogram, pattern bitmask,
  species assignment and merge, U5 comparator, novelty selection.
  All generic (no target, family, or library knowledge).

UNCHANGED (verified by diff after assembly):

- Candidate generation loop inside beam_extend (beam members, NOTs,
  pairwise AND/OR/XOR). This is the F-BLOAT basis.
- score_node arithmetic (scalar still computed and stored for
  reporting; not used for retention ranking).
- sealed families, passive, do_iv, true_correct, node_new_term,
  node_new_op, node_new_libterm, sigtab, PRNG, drivers (seeds, bars,
  evidence-loop structure), round structure.

Mechanical driver changes allowed (documented here, not deviations):
drivers allocate bspec (32 x i32, species id per beam slot, written by
beam_extend_u) and ulog (2 x i32: maxsims accumulator, nodomv
accumulator, reset per driver invocation) and thread them through
phase1/phase2/run_r1 into beam_extend_u/select_iv_u; call sites pass
the frozen round numbers from section 3/U3. Dead-code drivers
(r1u build_learner32/phase1_rand, r3u phase1, frecu phase2) are
converted to the new call signatures so the files compile; they are
not executed by main.

beam_sort (defined but never called in any frozen file) is dropped.

## 3. U1-U7 operationalization

Node layout (frozen, 28 bytes): off 0 kind (0 term, 1 op), off 4
term-id or op (0 AND, 1 OR, 2 NOT, 3 XOR), off 8 child 0, off 12
child 1 (-1 for terms and NOT), off 16/20 signature lo/hi, off 24
opc. Node ids increase monotonically; children always have smaller
ids than parents.

### U1: Pareto retention within species

Within each species, retention is by the U3/U5 ordering, which is
accuracy-first in both phases. Because a pruned candidate always
ranks below every kept species-mate, no pruned candidate can have
strictly higher accuracy (or equal accuracy with strictly lower opc)
than a kept species-mate. The Pareto property is therefore enforced
by the ordering itself; F-NODOM (section 4) verifies it as a canary.

### U2: Niching

Species signature per candidate: (tree depth, operator multiset
[n_AND, n_OR, n_NOT, n_XOR]), computed generically:

- Depth: 0 for terminals; 1 + max(child depths) otherwise, computed
  in one increasing node-id pass (children have smaller ids, so a
  single 0..nmax pass is exact).
- Histogram: iterative DFS from the candidate root with a
  visit-token array (8192 i32, token incremented per candidate), so
  each distinct reachable node is counted once. No target, family,
  or library knowledge enters the signature.

Species assignment: candidates with equal (depth, h0, h1, h2, h3)
share a species. If more than 8 non-empty species exist, merge the
two smallest iteratively until 8 remain, where smallest is ordered
by (member count asc, best-member accuracy asc); merging unions
member lists. The merged species contributes its top 4 by the
U3/U5 ordering.

Keep rule: species ordered by best member under the U3/U5 ordering;
take top 4 per species in species order until 28 slots fill (U6
reserves 4 of 32). If the species phase yields fewer than 28, fill
the remainder from the global candidate ordering (U3/U5), excluding
already-kept.

### U3: Two-phase tax schedule

Rounds are 0-indexed per evidence loop. The beam_extend_u call sites
pass the round number:

- r1u run_r1 and frecu phase1: loop r=0..23 passes round=r; the
  final extend passes round=24.
- r3u phase2: the initial extend passes round=0; loop r=0..23 passes
  round=r+1. (r3u phase1 is dead code; its call sites pass round=r
  in the loop and round=24 for the final extend. frecu phase2 is
  dead code; initial extend round=0, loop round=r+1.)

Rounds 0-15 (exploration): rank by accuracy alone; the tax (scalar
score) is computed and stored but ignored. Rounds 16-24
(consolidation, including the final extend): rank by accuracy, break
ties by lower opc. The scalar score is never used for retention
ranking in either phase.

### U4: Diverse IV hypothesis set

select_iv_u (r3u.zag, frecu.zag): from the beam in beam order, take
the first member of each distinct species (species ids from bspec,
written by beam_extend_u), up to 8 hypotheses. Disagreement
selection is otherwise unchanged: for each unused x in 0..63,
c1 = ones among the H hypotheses, d = H - |2*c1 - H|, pick max d
(ties: lowest x, as in the frozen code). If H < 1, return -1.
r1u.zag keeps select_iv_rand unchanged.

### U5: Principled tie-breaking

Within the U3 ordering, ties (equal accuracy, and equal opc in
consolidation) break by:

(a) Evidence-disagreement distance: each candidate's
    correct/incorrect pattern on the current evidence is a bitmask
    (en <= 32 always; bit e = 1 iff the candidate is correct on
    evidence e). Candidates are grouped by (species, accuracy);
    with at most 8 species and en <= 32, group index =
    species*33 + accuracy. Within each group of size > 1, the
    bitwise majority pattern is computed (ties at a bit go to 1);
    distance = popcount(pattern XOR majority). Groups of size 1
    get distance 0.

(b) Operator-histogram novelty: L1 distance between the candidate's
    [n_AND, n_OR, n_NOT, n_XOR] and the summed histogram over the
    previous round's beam members (computed from the beam as it
    stands on entry to beam_extend_u, before replacement). Prefer
    larger distance.

(c) Recency: higher node id (allocated later). Prefer larger.

Full candidate ordering:
- Exploration: accuracy desc, (a) desc, (b) desc, (c) desc.
- Consolidation: accuracy desc, opc asc, (a) desc, (b) desc, (c) desc.

### U6: Diversity floor

4 of 32 slots reserved for structurally novel candidates. Among
candidates not kept by the species phase, with accuracy fraction
>= 50% ((correct*100)/en >= 50), compute novelty = L1(histogram,
mean histogram of the species-kept set), compared in integer
arithmetic as sum_i |h_i * C - sum_i| with C = species-kept count
(monotonic in the true L1). Take the top 4 by (novelty desc,
accuracy desc, node id desc). If fewer than 4 qualify, fill from
the global candidate ordering (U3/U5), excluding already-kept.
The kept set (species-kept + floor) is then globally ordered by
(accuracy desc, opc asc, (a) desc, (b) desc, (c) desc) so beam[0]
remains the accuracy-first pick. Beam slots store (node, score,
correct, opc) as in the frozen code; bspec stores the species id
per slot.

### U7: Honest tie reporting (r1u.zag)

Replace taxoff_unique with: compute max accuracy A over the beam;
N = count of beam members with accuracy == A; omin/omax = opc range
within the max-accuracy tier. Emit:

- " TIE=UNIQUE" if N == 1.
- " TIE=UNDERDETERMINED N=<N> OPCRANGE=<omin>-<omax>" if N > 1 and
  the tied members are not all the same node id.
- " TIE=DEFECT" only if N > 1 and all tied members are the same
  node id (dedup failure canary; impossible under sigtab dedup).

A self-check recomputes N by an independent loop; on mismatch emit
" TIECHECK=FAIL", otherwise emit " TIECHECK=OK". The R1 per-seed
line keeps all other fields byte-identical in form
(R1 SEED= COV= EVFIT= TACC= OPC=) with the TIE/TIECHECK report in
place of TAXOFF_UNIQ.

## 4. Instrumentation

- F-NODOM: evaluated on the species-phase retention (the 28 slots),
  before the U6 floor is added. For every candidate p not kept by
  the species phase, and every species-kept member k with
  species(k) == species(p): violation iff (p.acc > k.acc) or
  (p.acc == k.acc and p.opc < k.opc). Accumulate NODOMV per driver
  invocation (in ulog); emit at end of the invocation. Any
  NODOMV > 0 fires F-NODOM.
- F-BLOAT: each beam_extend_u records tn (candidate count, equals
  score_node calls; the pattern/histogram walks do not call
  score_node and do not count). Track max tn per driver invocation
  (in ulog); emit "MAXSIMS=<max tn>" per driver invocation.
  Baseline: instrumented copies of the frozen files (r1_base.zag,
  r3_base.zag, frec_base.zag) record tn identically and emit
  "BASEMAX=<max tn>" per driver invocation. BASE_battery = max over
  all driver invocations in the battery. The ceiling uses explicit
  integer arithmetic with truncation:
    CEIL_battery = (BASE_battery * 110) / 100
  computed with integer division (all values non-negative). Example:
  BASE=1109 gives (1109*110)/100 = 121990/100 = 1219. F-BLOAT fires
  iff any unified driver invocation's MAXSIMS > CEIL_battery for its
  battery. The ceiling is frozen after the baseline runs and before
  any unified battery runs.

Per-driver-invocation emission lines (in addition to the frozen
report lines, which are unchanged):

- r1u run_r1: "R1U SEED=<seed> MAXSIMS=<m> NODOMV=<v>"
- r3u phase2: "R3U <tag> MAXSIMS=<m> NODOMV=<v>"
- frecu phase1: "FRECU <tag> MAXSIMS=<m> NODOMV=<v>"

## 5. Frozen control baselines (reproduced before the unified build runs)

Control step: recompile each frozen source with znc (same pinned
compiler), run 3x, verify byte-identical to the committed raw
outputs. If any control fails to reproduce, halt and report; do not
run the unified build against a moved baseline.

- R1: e40cb1b51, 3/3 byte-identical md5
  6f15d782940abdf824be99721dcc2d36, verdict R1-FAIL, 0/5 seeds
  (bar: >=4/5 seeds with 8/8 coverage AND 64/64 true).
- R3: 023b4f84a, 3/3 byte-identical md5
  7ed09fda269b59cdbbf75e0df720661c, verdict R3-FAIL
  (A1-PASS=1: 64/64, hit_iv=0; A2-PASS=0: hit_iv=24, 53/64, HAS_D=1;
  bars: 64/64 AND reuse_iv*2 <= scratch_iv AND HAS_D=1).
- F-RECFOLD: 1c52f7dad wave (source 5a21bb2b3), 3/3 byte-identical
  sha256 fef761afc5e72daa833e7bb4a12b1525efbffafef2294219bb7d650632f2d048,
  verdict FREC-ZERO-FAIL (B1 0/5 on all 3 instances; I2 traps on
  constant-0 at 63/64 on all seeds).

## 6. Falsifiers (frozen)

- F-FIT: fewer than 4 of 5 R1 seeds reach EVFIT=32/32 under the
  unified beam (R1 driver, P-RAND, fam 5).
- F-DIVERSE-FAIL: R3 Arm 2 still fails its frozen bar (A2-PASS=0:
  requires 64/64 AND reuse_iv*2 <= scratch_iv AND HAS_D=1).
- F-NODOM: NODOMV > 0 in any driver invocation.
- F-TIE-HONEST: "TIE=DEFECT" or "TIECHECK=FAIL" appears in R1 output.
- F-REGRESS: R3 Arm 1 A1-PASS goes from 1 (frozen) to 0
  (requires 64/64 AND reuse_iv*2 <= scratch_iv).
- F-BLOAT: any unified driver invocation's MAXSIMS exceeds
  CEIL_battery for its battery, with CEIL defined by the explicit
  integer rule in section 4.
- F-CASE: audit finds any new-machinery component keying on target,
  family, or library identity (target value, fam number, or
  installed-D signature/behavior). Generic machinery only.

F-RECFOLD (frecu.zag) is an exploratory run, not a falsifier: the
unified beam targets W1/W3/W4 (R1/R3); W2 (I2 constant-prediction
ceiling) is a distinct failure the design does not claim to fix.
Report B1/B2/B3 per the frozen F-RECFOLD bars for information.

## 7. Kill bars (this build task)

- K1 (prereg frozen before implementation): this document committed
  strictly before any unified-beam source is written. Commit-order
  self-check required (prereg commit timestamp/hash precedes the
  first implementation commit).
- K2 (all controls run): R1 (5 seeds), R3 (Arms 1-2), and F-RECFOLD
  (3x5) complete under the unified beam; every falsifier in
  section 6 evaluated and reported. Frozen controls reproduced
  first (section 5).
- K3 (pure Zag, deterministic): Zag at every stage (authoring,
  building with znc, running, verification via shell tools only:
  sha256sum, md5sum, cmp, grep, wc, git). Zero Python at every
  stage, from task start. 3/3 byte-identical runs per battery,
  zero stderr bytes. Zero em/en dash bytes in loop documentation
  (shell-verified with worker_snippets/check_no_dash.sh).

## 8. Verdict rule (frozen)

- BEAM-UNIFIED-PASS iff K1-K3 hold AND no falsifier in section 6 fires.
- BEAM-UNIFIED-FAIL otherwise, naming each fired falsifier and the
  measurement that fired it.

Honest scope (frozen): a PASS is bounded-L2 search robustness for
compositional reuse and evidence fitting. Not L3, not Criterion 0,
not a Q4 revival (the revival conjunction is dead: R1-FAIL,
R3-FAIL, R4-FAIL). Fitting 32/32 does not imply 64/64
generalization; generalization still depends on the evidence being
representative.

## 9. Governance

- Prereg-first; no implementation before this commit.
- Frozen base sources are never edited; work happens on copies in
  beam_unified_clean/.
- The contaminated research paper is not touched.
- Commits local, owned pathspec only
  (docs/lab/research-lead/overnight-20260928/beam_unified_clean/).
- Other workers' files are not touched.
- If a git lock is encountered, wait; never remove a live lock.
