# REPORT.md -- Sealed Strong Composition (X + Y -> Z)

## Verdict: COMPOSITION-SEALED-COMPLETE with causal reuse proof

**TNN learns skill X (scalar transform) and domain Y (sequences)
independently, then composes them to solve a sealed novel goal Z with no
paired X+Y examples, no combination hint, and no task label. Ablating X
or Y destroys Z. All ten frozen kill bars passed. 3/3 byte-identical.**

## Mechanism

`sc_full.zag` (309 lines), unfrozen only, standalone binary.

**Skill X as executable graphs.** `sc_teach_proc` induces a scalar
procedure from three (in,out) examples: k = out0 - in0, verified on the
other two, fails closed otherwise. The procedure is stored as a 2-node
executable graph (OP_IN -> OP_ADD(k)) in the pool; `sc_exec_proc` walks
the graph with generic op dispatch. Learned: X1 = add7 (proc 0),
X2 = add2 (proc 1, distractor). Gap examples (4,9),(5,11),(6,10) with
non-constant delta induce nothing (`GAP non-constant induct=-1`).

**Domain Y as sequence structures.** `sc_reg_seq` registers sequences
with indexed read and length: SA, SB, SC (len 4/4/3), SD (len 6,
distractor). Sequences are never transformed during Phase 2.

**Sealed solver.** `sc_solve` receives an unlabeled input sequence S*
and a target T*, with T*[i] = X1(S*[i]). Candidate families over LEARNED
structures only: COPY (any registered len-matching sequence) then ELTWISE
(any learned scalar proc applied elementwise to any registered
len-matching sequence). Elementwise verification decides; first verified
candidate wins. No labels, no hint, no "combine" call. On success a new
executable Z record is created (ELTWISE with proc = X1) with provenance
links provx -> X1 and provy -> Y domain. `sc_zapply` applies Z directly
to a fresh sequence (no search) for the reuse test.

**No-paired-examples machine check.** Every `sc_eltwise` execution
increments ELTCT. The transcript prints ELTCT-PRE-SEAL = 0 in all arms:
no elementwise application of X to any sequence occurred before the
sealed phase.

## Experiment

Arms (one binary, fresh workspace per arm, fixed order), 3/3 byte-identical:

- TREAT: X1/X2 taught; SA/SB/SC/SD taught; gap; sealed Z; then Z2 reuse.
- ABL-X: proc records deleted after training; sealed Z.
- ABL-Y: sequence domain disabled after training; sealed Z.
- FRESH: no training; sealed Z.
- NO-COMPOSE: training intact; ELTWISE family disabled; sealed Z.

Sealed values (never seen during training): S* = [4,0,11,5,7,3] (len 6,
a length never trained), T* = [11,7,18,12,14,10]. Z2: S2* = [9,2,6,0,4,8],
target [16,9,13,7,11,15].

## Results

### TREAT: composition succeeds

```
TRY COPY seq=3 / REJECT        (SD distractor)
TRY COPY seq=4 / REJECT        (S* input is not the target)
TRY ELTWISE proc=0 k=7 seq=3 / REJECT   (add7 over SD distractor)
TRY ELTWISE proc=0 k=7 seq=4
Z ans=1 via ELTWISE proc=0 seq=4
ZMAP provx=0 provy=1
tried=4
Z2 reuse: direct Z apply, no search
Z2 ans=1
tried-after-Z2=5
```

The solver tried distractors first (COPY of SD and S*, ELTWISE of X1
over SD) and rejected each by verification. It selected proc 0 (k=7,
read from the stored executable graph, not from a label) and the sealed
input sequence. The composed Z record persisted and answered a fresh
unseen sequence with exactly 1 additional verify and no search.

### Ablations: X and Y are each load-bearing

| Arm        | Z ans | ZMAP | tried |
|------------|-------|------|-------|
| TREAT      | 1     | provx=0 provy=1 | 4 |
| ABL-X      | -2    | none | 2 |
| ABL-Y      | -2    | none | 0 |
| FRESH      | -2    | none | 1 |
| NO-COMPOSE | -2    | none | 2 |

- ABL-X: COPY candidates rejected, no procs for ELTWISE. Z fails.
- ABL-Y: input cannot be registered as a sequence. Z fails immediately.
- FRESH: one COPY try (the bare input), nothing else available. Z fails.
- NO-COMPOSE: X+Y present and correct, but without the ELTWISE family Z
  fails. The composition mechanism itself is causal, not a side effect.

## Kill-bar audit (frozen in PREREG_SEALED.md)

1. TREAT solves Z with proc X1 (k=7) and seq S*: PASS.
2. Z record with provenance to X1 and Y domain: PASS (provx=0 provy=1).
3. Z2 via direct Z apply, exactly 1 verify, no search: PASS (tried 4->5).
4. ABL-X fails: PASS (-2). 5. ABL-Y fails: PASS (-2).
6. FRESH fails: PASS (-2). 7. NO-COMPOSE fails: PASS (-2).
8. ELTCT-PRE-SEAL = 0 in all arms: PASS.
9. 3/3 byte-identical transcripts: PASS (cmp clean).
10. Induction fails closed on non-constant examples: PASS (-1).

## Micah's strong-composition criteria

- Actual reuse of X: yes (Z executes X1's stored graph; ABL-X breaks Z).
- Actual reuse of Y: yes (Z traverses Y's sequence structures; ABL-Y
  breaks Z).
- New executable structure for Z: yes (Z record: ELTWISE with proc=X1,
  directly applicable to new sequences).
- Ablation of X breaks Z: yes (-2).
- Ablation of Y breaks Z: yes (-2).
- Cheaper than fresh rediscovery: yes (FRESH cannot solve at any cost;
  TREAT solves in 4 verifies; Z2 reuse costs 1).
- Persists and reusable later: yes (Z2 via direct Z apply).

## Honest boundaries

1. The target T* is given and used for elementwise verification, as in
   trial/rebind. What is discovered, not given: which proc, which
   sequence, and the fact that elementwise application is the answer.
2. Candidate families (COPY, ELTWISE), simplest-first order, and the
   induction family {out = in + k} are researcher-authored. The learned
   k values, the selected structures, and the Z record are learner-owned.
3. One scalar family (addition) and one domain (sequences). Cross-domain
   pairs (e.g. formal language + algorithm) remain future work.
4. The solver enumerates procs x sequences; cost is bounded here by tiny
   stores. Scaling the candidate space is not tested.
5. This is an unfrozen standalone experiment binary, not yet integrated
   into the TNN-2 core. Integration with the shared consequence substrate
   is the natural next step, not a claim made here.

## Standing metrics

- Cognition lines added: 309 (sc_full.zag).
- Modes / bridges / handlers / semantic cases: 0.
- Researcher-owned: induction family, candidate families, order, driver.
- Learner-owned: k values, proc/seq selection, Z record, provenance.

## Deliverables

- `PREREG_SEALED.md` (frozen bars, committed `a9fa821f3` before
  implementation)
- `sc_full.zag`, `sc_bin` (pinned znc), `sc_compile.txt`
- `sc_run1/2/3.txt` (SHA-256
  `bc4cf4bc1ff14070bbb62e169a63129feb43ccd0da7297613f96982370e4c28d`)
- `NAMECHECK.md` (this file's sibling), `REPORT.md` (this file)

Pure Zag. Safebin PATH. Zero em/en dashes (byte-verified).
Paper untouched. Frozen source read-only. Committed locally, nothing pushed.
