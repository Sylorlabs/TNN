# PREREG: DDES Builder (Difference-Driven Experiment Synthesis)

Frozen before any implementation. This prereg commits the kill bars from
DESIGN.md section 7 verbatim. Any amendment must be committed transparently
and re-frozen before implementation; no bar may be altered after seeing
results.

## Target classification

Strong L2 (guided generation). NOT L3. The design doc section 5 records the
residual researcher authority honestly: action vocabulary, hypothesis format,
analysis algorithm, and schema set are researcher-owned. The learner authors:
whether to intervene, which variable to observe, exact plan length, full
sequence.

## Validity bars (all must pass for any verdict)

- V-NX1: Worlds A and B converge correctly (4/4 configs), exactly 1 real
  execution per config.
- V-NX2: 3/3 byte-identical runs, exit 0, zero stderr.
- V-NX3: pure Zag, zero Python, zero em-dash bytes.

## Kill bars (BUILD-PASS requires all)

- K-NX1 (no enumeration, static): source audit. The committed source must
  contain no routine that generates all sequences of length <= D over the
  primitive set, and no numeric constant that bounds plan length. Method:
  reviewer reads the full synthesis path. Any sequence-generating loop or
  length constant kills the bar.

- K-NX2 (no enumeration, behavioral): instrument the learner to count
  candidate complete plans assembled and compared before selection. On
  Worlds A and B the count must be <= 8. (Guided synthesis assembles
  approximately 1.) Kill: count >= 100.

- K-NX3 (sealed depth): after freeze, the adversary supplies a world
  requiring L actions with L >= 8, where L exceeds every length constant in
  source (there must be none). The learner must converge with exactly 1
  real execution. Kill: NO-DISCRIMINATING-PLAN, or more than 1 execution.

- K-NX4 (structure sensitivity): two sealed worlds differing only in rule
  delays. Without any source change, the learner must produce
  correspondingly different plans matching the analytically computed
  targets. Kill: identical plans for both worlds, or a plan that does not
  match its computed target.

- K-NX5 (variable choice): a sealed world whose hypotheses differ only on
  Z timing. The learner must emit a plan observing Z and converge. Kill:
  an OY-only plan, or failure to converge.

- K-NX6 (C0-A source audit): no branch on specific delay values, variable
  ids, or world ids anywhere in the analysis/synthesis path. Kill: any
  delay==2-style dedicated case.

- K-NX7 (one-shot derivation): on at least one sealed world, the learner
  emits the discriminating plan having assembled <= 3 candidate plans
  (per the K-NX2 instrumentation). This is the positive evidence of
  guidance as opposed to search.

- K-NX8 (empty-frontier honesty): a sealed world on which both hypotheses
  agree everywhere under both schemas. The learner must report
  NO-DISCRIMINATING-PLAN and perform 0 real executions. Kill: any real
  execution, or a fabricated plan.

## Test worlds (frozen)

World A: H0 = [(X,Z,2),(Z,Y,0)]; H1 = [(X,Y,1)].
  Expected derivation: H0 arrivals Z@t0+2, Y@t0+2. H1 arrival Y@t0+1.
  Frontier: Y differs on [t0+1, t0+2). Target (Y, t0+1). Plan [S,W,OY].

World B: H0 = [(X,Z,3),(Z,Y,0)]; H1 = [(X,Y,2)].
  Expected derivation: H0 arrivals Z@t0+3, Y@t0+3. H1 arrival Y@t0+2.
  Frontier: Y differs on [t0+2, t0+3). Target (Y, t0+2). Plan [S,W,W,OY].

World C (A2 sealed killer): H5 = [(X,Z,5),(Z,Y,0)]; H6 = [(X,Y,4)].
  Expected derivation: H5 arrival Y@t0+5. H6 arrival Y@t0+4.
  Target (Y, t0+4). Plan [S,W,W,W,W,OY] (length 6, no bound consulted).

World D (Z-only): H7 = [(X,Z,2)]; H8 = [(X,Z,4)].
  Expected derivation: frontier selects (Z, t0+2). Plan ends with OZ.

World E (empty frontier): H9 = [(X,Y,1)]; H10 = [(X,Y,1)].
  Expected: NO-DISCRIMINATING-PLAN, 0 real executions.

## Sealed worlds (designed after freeze, not specified here)

K-NX3, K-NX4, K-NX5, K-NX7 each require sealed instances designed after the
implementation freezes. Their exact contents are not part of this prereg.

## Commit order

This prereg is committed alone. The implementation commit must be a strict
descendant. Verified via git merge-base --is-ancestor before the result is
reported.
