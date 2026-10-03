# REPORT.md -- Hypothesis C: Constraint-Driven Assembly

## Verdict: COMPOSITION-C-COMPLETE

**TNN composes X+Y->Z via constraint-driven assembly. The goal's input/output
constraints select MAPs by their structurally-extracted properties; the
learner discovers X-then-Y with no paired examples, no hint, no task label.**

## Mechanism

`cc_patch.zag` (~250 lines), unfrozen only. Base is `knowledge_composition`
core (rebind + LINK14) lines 1-1677; `ev_query` replaced to hook
`compose_try` between `rebind_try` and trial.

**Structural property extraction** (`cc_relseq`): walks a MAP's promoted
executable graph (guard/set chain) and reads each SET cell's DEP (type-1)
edge to its licensing fact; the fact's relation field is the link's
relation. MAP field 4 (relation label) and field 8 (subject label) are
never consulted. The property is derived from the executable structure.

**Constraint satisfaction** (`cc_satisfy`, `cc_candidates`): a MAP satisfies
the current goal state iff its relation sequence can be walked in the fact
store starting from the current value. Candidates ordered by decreasing
sequence length (fewer segments preferred), ties by MAP id.

**Search** (`cc_dfs`): iterative depth-first search over MAP compositions,
max 3 segments, no MAP reused within one composition. Terminates when the
walked value equals the goal's expected output.

**Assembly**: one chain per segment (rebinding the segment MAP's shape onto
the walked values, as `pc_try_one` does), concatenated via SEQ links,
verified by execution, promoted as MAP_Z with LINK14 provenance edges to
each segment MAP.

**Goal constraints**: required input = query subject s; required output =
expected; allowed intermediate forms = whatever MAP properties satisfy.
No composition template exists in source.

## Experiment

X: two r1 plen-4 chains. Y: two r2 plen-4 chains. Never shown together.
Z: mixed plen-7 chain (r1 x3, then r2 x3), BEYOND trial gather depth (5).
Z query uses fresh relation 63.

Arms (fresh workspace each), 3/3 byte-identical per binary:
- TREAT: X+Y trained, gap, Z facts, query Z, then Z' reuse (new subject).
- ABL-X: X MAPs deleted before Z query.
- ABL-Y: Y MAPs deleted before Z query.
- FRESH: no X/Y training.
- NO-COMPOSE: TREAT with `compose_on()=0` (one-line diff binary).

SHA-256: treatment `64e21a39...`, control `ba31eed0...`.

## Results

### Structural properties (extracted, not labeled)

```
MAP 27 relseq=[1,1,1]   (X1)
MAP 45 relseq=[1,1,1]   (X2)
MAP 63 relseq=[2,2,2]   (Y1)
MAP 81 relseq=[2,2,2]   (Y2)
```

### TREAT: composition succeeds

```
COMP-SEGS n=2 27 63
Z ans=37 tried=5 rejected=4
ZMAP id=196 link14=5
MAP 196 relseq=[1,1,1,2,2,2]
  LINK14 196 -> 27
  LINK14 196 -> 63
```

The DFS selected MAP 27 (X1) then MAP 63 (Y1) by constraint satisfaction
alone. Cost: 4 rebind rejects (whole-shape tries on the plen-4 path) + 1
compose verify. ZMAP 196 is a plen-7 executable chain with provenance to
both segment MAPs.

### Z' reuse: composed structure persists

```
COMP-SEGS n=1 196
Z2 ans=47 tried=5 rejected=4
```

New subject 41, same mixed shape. Composition selected the composed Z MAP
(196, longest match) in a single segment. The composed structure is
reusable; it was not rebuilt from X+Y.

### Ablations: X and Y are each load-bearing

| Arm | Z ans | ZMAP | LINK14 |
|-----|-------|------|--------|
| TREAT | 37 | 196 | 5 (incl. 196->27, 196->63) |
| ABL-X | -2 | -1 | 3 (rebind provenance only) |
| ABL-Y | -2 | -1 | 3 |
| FRESH | -2 | -1 | 0 |
| NO-COMPOSE | -2 | -1 | 3 |

- ABL-X: no MAP satisfies the input constraint from 31 (COMP-FAIL in
  trace). Trial cannot reach plen 7. Z fails.
- ABL-Y: X segment walks to 34, then no MAP continues (backtrack
  exhausts). Z fails.
- FRESH: nothing to compose. Z fails.
- NO-COMPOSE: X+Y present, relseqs correct, but Z fails. The composition
  mechanism itself is causal, not a side effect.

### Cost

Composition solves Z in 5 verifies (4 rebind + 1 compose). Fresh trial
cannot solve Z at any cost (plen 7 > gather depth 5). The composed Z then
answers new subjects for 1 compose verify.

## Micah's strong-composition criteria

- Actual reuse of X: yes (segment 1 = MAP 27; ABL-X breaks Z).
- Actual reuse of Y: yes (segment 2 = MAP 63; ABL-Y breaks Z).
- New executable structure for Z: yes (MAP 196, plen-7 chain).
- Ablation of X breaks Z: yes (-2).
- Ablation of Y breaks Z: yes (-2).
- Cheaper than fresh rediscovery: yes (fresh fails entirely).
- Persists and reusable later: yes (Z2 via MAP 196).

## Honest boundaries

1. The goal's expected output is the search target (as in trial/rebind
   verification). Discovery of *which* MAPs to chain is constraint-driven;
   the target value is given.
2. Candidate ordering (longest-first) and max 3 segments are
   researcher-authored search bias; segment contents and choices are
   learner-determined.
3. Chain family only. Properties are relation sequences; richer structural
   properties (guards, counts) not tested.
4. Training queries themselves use rebind (X2 via X1, Y1 via X2's shape):
   pre-existing machinery, not composition. Composition first fires on Z.
5. Rebind's 4 wasted verifies on Z/Z' are pre-existing whole-shape tax,
   not introduced here.

## Standing metrics

- Cognition lines added: ~250 (cc_patch.zag).
- Modes / bridges / handlers / semantic cases: 0.
- Researcher-owned: search bias, config, driver world.
- Learner-owned: relseq values, candidate choices, segment MAPs, Z graph.

## Deliverables

- `cc_patch.zag`, `cc_patch_nc.zag` (one-line diff), `cc_base.zag`,
  `cc_driver.zag`, `cc_full.zag`, `cc_full_nc.zag`
- `cc_bin`, `cc_nc_bin` (pinned znc)
- `cc_run1/2/3.txt` (SHA `64e21a39...`), `cc_nc_run1/2/3.txt` (SHA `ba31eed0...`)
- `cc_compile.txt`, `cc_nc_compile.txt`
- `NAMECHECK.md` (this file's sibling), `REPORT.md` (this file)

Pure Zag. Safebin PATH. Zero em/en dashes (byte-verified below).
Paper untouched. Frozen source read-only. Committed locally, nothing pushed.
