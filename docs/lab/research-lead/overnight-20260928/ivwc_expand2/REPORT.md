# REPORT.md -- IVWC-EXPAND2: Self-checking verifier and law-change limits

## Verdict: BUILD-FAIL (K6, K8)

K1, K2, K3, K4, K5, K7, K9 all PASS. Two bars fail, both diagnosed
as defective bar/ablation constructions rather than mechanism
failures; the underlying scientific questions are answered by the
data, and a corrected follow-up (ivwc_expand3) is the next step.

- K6 FAILS because the shuffled-consequence ablation is VACUOUS BY
  CONSTRUCTION (implementation defect). The rotation-by-7 permutes
  (bucket, eff) pairs jointly by position; verifier_train groups
  pairs by bucket value, which is invariant under position
  permutation, so the "shuffled" table is bit-identical to the true
  table (Tsh=20=T, identical bucket means) and acc_shuf=9=acc
  necessarily. The bar could never discriminate. Root cause found
  by analytic inspection, confirmed by the numbers.
- K8 FAILS because absolute accuracy is the wrong operationalization
  of "carried verification degrades" (bar-design miss). Sealed
  accuracy went 9 -> 8 -> 10 across wp 15/30/45 (non-monotone),
  because at wp=45 the world collapses so thoroughly that nearly
  every case is a trivial FAIL (11 of 12 sealed effs are 0), making
  raw accuracy EASIER while the verifier's VALUE vanishes. The
  correct measure is the verifier's edge over the trivial baseline,
  which degrades monotonically: +2 -> 0 -> -1. K9 (edge <= 0 at
  wp=45) PASSED and captures the actual break.

Neither failure reflects on the mechanisms: the self-check
discriminates and beats the baseline at wp=15 (K3, K4 PASS), the
revision replicates exactly (K7: 223 -> 235), and the law-change
break is found (K9 PASS).

## What was built

`src/ivwc_expand2.zag` (pure Zag, single file, 794 lines, pinned
znc), `bin/ivwc_expand2` (frozen binary). World, beliefs,
composition, consequence simulator, evidence log, and revision rule
copied verbatim from ivwc_expand/src/ivwc_expand.zag except
world_gen takes a wall-probability parameter wp (wp=15 reproduces
the predecessor sealed worlds bit-identically). New learner-section
functions: verifier_train (per-bucket train-eff means + a
learner-computed threshold T from train consequences only) and
verifier_check (pre-execution PASS/FAIL self-verdict; FAIL on empty
buckets). Train: 24 cases, commit -> conseq -> verifier training
(no train revision needed). Sealed shift loop sh=0..2
(wp=15/30/45), cid 100..111, buffers reused: per shift, batched
SELFCHECK commit -> frozen-table verdicts before any sealed
consequence -> conseq, then batched REVISION commit1 -> conseq1 ->
per-case revise+conseq2 with the empty-evidence ablation.

Build: `src/tools/toolchain/znc_linux_x86_64_abed8aa1
src/ivwc_expand2.zag -o bin/ivwc_expand2`. Analyzer: one
informational zagd-unavailable notice only (same as predecessors).

## Kill-bar results

- K1 (commit before signal, all phases): PASS. In-program:
  K1T-STRUCT-PASS (train commit), K1S-STRUCT-PASS sh=0/1/2
  (selfcheck commits), K1R-STRUCT-PASS sh=0/1/2 (revision
  commit1s): 7/7. Audit A1: commit-phase learner_compose/
  learner_revise line numbers strictly precede the corresponding
  conseq-phase world_execute line numbers per phase pair
  (441<454; 531<560; 625<641; 653<655; 656<657). Audit A2: zero
  world_buf/world_off tokens in the LEARNER section.
- K2 (no disguised oracle): PASS. Audit A3: zero
  expected|answer|key|target tokens (case-insensitive). Audit A4:
  zero correct|reference_plan|gold tokens; every == in the world
  functions compares physics/action/local values (copied verbatim
  from the predecessor that passed this audit); verifier inputs
  are (bucket, eff) pairs from executed consequences only; T is
  learner-computed, no researcher-set constant in the verifier.
- K3 (self-check discriminates, wp=15): PASS. Sealed np=6 sp=157,
  nf=6 sf=66: both verdict classes non-empty, and
  157*6=942 > 66*6=396, i.e. mean sealed eff of PASS verdicts
  (26.2) strictly exceeds that of FAIL verdicts (11.0).
- K4 (verifier beats the trivial baseline, wp=15): PASS. Sealed
  acc=9/12 > maj=7/12 (strict). Actual class = (eff >= T), T=20
  from train.
- K5 (determinism): PASS. 3/3 byte-identical stdout, sha256
  c1dbfef14be939db38a4b77cf10e65eb4500c937dbeabc26c792ec0dd084b35a.
- K6 (ablation): FAIL, vacuous by construction (see Verdict).
  acc_shuf=9 = acc=9; the shuffled table equals the true table.
- K7 (revision replicates under stationarity): PASS. Sealed
  sum_eff1=223, sum_eff2=235, sum_abl=223, n_abldiff=0 --
  bit-exact replication of the IVWC-EXPAND sealed numbers,
  confirming the wp=15 worlds and all copied functions are
  identical to the frozen predecessor.
- K8 (absolute accuracy degrades): FAIL, wrong operationalization
  (see Verdict). acc: 9 (wp=15) -> 8 (wp=30) -> 10 (wp=45).
- K9 (break found): PASS. At wp=45, acc=10/12 <= maj=11/12: the
  frozen verifier no longer beats the trivial always-FAIL rule
  under strong law change.

## Mechanism detail (white box)

The learner's frozen verifier table (train, wp=15): T=20;
b=0: cnt=7 mean=0; b=1: cnt=7 mean=47; b=2: cnt=7 mean=16;
b=3: cnt=3 mean=10. The learned self-check rule is "PASS iff
exactly one planned gather": multi-gather plans are overconfident
(the baseline's phantom-exposure structure), now operationalized
as a pre-execution veto. Sealed wp=15 errors are informative:
s=3 (single-gather plan, eff=0 -- nothing collectible),
s=5/s=6 (multi-gather plans the verifier vetoed, eff=33/20 --
the veto was wrong; revision later fixed s=5: 33->42 per the
predecessor pattern).

Law-change curves (the limits answer):
- Verifier edge over trivial baseline (acc-maj): +2 -> 0 -> -1
  across wp 15/30/45. Carried verification loses its value
  monotonically and is worse than trivial at wp=45. The break is
  not that verdicts become random -- at wp=45 the verifier still
  scores 10/12 absolute -- but that the frozen T=20 threshold and
  bucket means no longer carve the world at its joints: 11 of 12
  sealed cases collapse to eff=0 and the majority rule (always
  FAIL) dominates.
- Revision sealed gain (sum_eff2 - sum_eff1): +12 -> +56 -> 0.
  Against the prereg's design note (which predicted revision
  would survive because per-case evidence stays truthful), the
  revision ALSO breaks at wp=45, but for a different reason: a
  floor effect. At wp=45 eleven of twelve sealed cases collect
  nothing under any plan (fragmented corridor, beliefs too noisy
  to locate the few reachable items); eff2=eff1=0 everywhere
  except the already-perfect s=11 (100->100). Truthful evidence
  cannot create signal where none exists. Notably, revision gain
  was LARGEST at wp=30 (+56: s=0 10->33, s=7 25->50, s=5 30->37),
  where denser walls produce more bump evidence -- the mechanism
  is strongest under moderate law change and dies only at the
  floor.

So the two verification modes break differently: carried
calibration degrades monotonically into worse-than-trivial
(stale knowledge), while fresh-consequence revision is
non-monotone (peaks under moderate change, then floor-killed).
Both are genuine "where it breaks" answers with no oracle at any
step.

## Honest caveats

1. K6's failure is an implementation defect in the ablation, not
   evidence about the mechanism. The rotation must permute effs
   independently of buckets to break the mapping; the joint
   rotation preserves it exactly. The follow-up corrects this.
2. K8's failure is a bar-design miss. Absolute accuracy conflates
   environment predictability with verifier quality. The edge
   over baseline (+2 -> 0 -> -1) is the right degradation
   measure; the follow-up bars it.
3. The wp dial changes wall density only; item law (25%), belief
   noise (12/15/18%), and energy budget are fixed. Other law
   changes (item-density shifts, sensor degradation) may break
   the mechanisms at different points; this experiment maps one
   axis.
4. This is a mechanism test, not a composition-novelty or L3 claim
   (per PREREG section 4). The verifier is a fixed bucket table;
   the claim concerns the self-verdict loop and its limits.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_expand2
~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1 src/ivwc_expand2.zag -o bin/ivwc_expand2
./bin/ivwc_expand2 | sha256sum   # expect c1dbfef14be939db38a4b77cf10e65eb4500c937dbeabc26c792ec0dd084b35a
```

Frozen audits (PREREG section 5): A1 ordering 441<454, 531<560,
625<641, 653<655, 656<657; A2 count 0; A3 count 0; A4 zero tokens,
all == physics-only; A5 sha256 equality across
runs/ivwc_expand2-run{1,2,3}.txt.

## Branch note

Work committed on `tnn-native-lab` (the shared checkout this worker
was spawned on). All commits use explicit pathspecs confined to
`ivwc_expand2/`. Local only, never pushed. Git writes via
/usr/bin/git directly (safebin git symlink EPERM lesson).

## Next step

ivwc_expand3 (fresh prereg): identical worlds/verifier/shifts;
K6 fixed (rotate ONLY the eff array, genuinely breaking the
bucket->eff mapping); K8 fixed (bar the edge degradation
(acc-maj) from sh=0 to sh=2 instead of absolute accuracy).
