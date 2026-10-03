# PREREG: Operator/Scope Rebuild with K=2

## Ancestry

- Design: commit `71f98aa72` (OP_SCOPE_DESIGN.md, DESIGN-COMPLETE).
- Design revision: commit `0140e93af`
  (opscope_rev/OPSCOPE_REV_DESIGN.md, OPSCOPE-REV-COMPLETE).
  Single constant change: K diversity 3 -> 2. All other constants
  unchanged. Strict-majority binarization (Amendment 1) inherited.
- Prior prereg: commit `37300ceae` (PREREG_OPSCOPE.md).
- Amendment 1: commit `6828c7228` (strict majority `cnt*2>o`).
- Prior result: commit `f01c6b69d` (OPSCOPE-FAIL). Root cause:
  K=3 unsatisfiable by generator construction on the frozen battery
  (training NEG episodes negate exactly two forms, so div=2<3 for
  every seed and every run). Design-parameter bug, not machinery.
- This prereg is frozen before any implementation. K1.

## Mission

Rebuild the R1-R4 operator/scope learner against the revision
(K=2), reusing the frozen battery, item ids, falsifiers, and
interfaces. Test the R4 frozen falsifiers F1-F5. Report
OPSCOPE-REBUILD-PASS or OPSCOPE-REBUILD-FAIL.

Expected mechanism outcome (revision section 8): the true trigger
(w=1) now passes all bars (sup=16>=4, 16/16>=0.75, div=2>=2,
100>84 strict), so the OPREC installs and F1, F2, F4 become
evaluable. A PASS is not entailed by this expectation.

No L3 claim is made. Bounded L2 direction.

## Frozen constants (revised table, revision section 3)

| Constant      | Value | Meaning                               |
|---------------|-------|---------------------------------------|
| B0 burn-in    | 20    | episodes before first discovery check |
| E interval    | 10    | discovery/retirement check cadence    |
| N_ep recur    | 5     | min episodes containing W             |
| Fmax elig     | 1     | max features in record(W, DEFAULT)    |
| N support     | 4     | min residual events for W             |
| C consistency | 0.75  | min signature-match fraction          |
| K diversity   | 2     | min distinct scope unit forms         |
| OPMAX         | 8     | operator table cap                    |

The only change from the prior preregistered table is K: 3 -> 2.
These are frozen. No change after this commit.

## Code change from the prior implementation

Exactly one change to the prior committed learner source
(`operator_scope_impl/opscope_learner.zag`, commit `f01c6b69d`):
the R2 proposal check `popcnt(scopeforms) >= 3` becomes
`popcnt(scopeforms) >= 2`. No other learner, world, or harness
logic is modified. The strict-majority binarization
(`c*2>o` in recmask/recmaskO) is carried over unchanged.

## Battery (frozen, unchanged)

The frozen DEVANG battery: `gen_episodes` from
`docs/lab/research-lead/overnight-20260928/devang4/devang4.zag`
(seed 123456789, 100 train episodes one-pass online, 20 test
utterances). The world file is copied verbatim from the prior
implementation. No modification to the episode sequence.

### Frozen item ids (unchanged)

- T1 (NEG-novel, F1): episodes 109, 110, 111 ("tak not grn").
- T3 (scope-shift, F2): episodes 109, 110, 111 ("grn" familiar
  affirmatively in training, never negated in training; T1 and T3
  coincide on this battery).
- SIZE group (F5): episodes 115, 116, 117.

### Units (oracle segmentation, unchanged)

True word-id sequence as the unit sequence U. Word ids:
0=tak 1=not 2=red 3=blu 4=grn 5=bal 6=sph 7=cub 8=tri 9=big
10=biger 11=smal.

### Observed target T (unchanged)

12-bit consequence-feature mask per episode: tak always; not never;
red/blu/grn by color; bal/sph/cub/tri by shape; big/smal by size;
biger iff z==1 and some other object shares tobj shape with size 0.
The learner sees only (U, T) per episode.

## Learner specification (frozen, unchanged except K)

Records, R1 interpret (OR combiner), R2 discovery (episode store,
residual events, DELETION signature, proposal checks, gate,
re-grounding replay, retirement), R3 routing: all as specified in
the prior prereg, with K=2 and strict-majority binarization.

## R4 falsifiers (frozen bars, unchanged)

- F1: T1 items 109,110,111 all pass AND white-box dump shows an
  OPREC with trigger_form == wid 1, signature DELETION,
  created_at > 0, support >= N.
- F2: T3 items 109,110,111 all pass.
- F3: source audit on the committed learner file listed below:
  grep for byte string "not" returns 0 hits; grep -i "negat"
  0 hits; grep "is_negator" 0 hits. Routing predicate references
  only OPREC.trigger_form_id (inspection note in result doc).
- F4: ablated copy of trained state with operator table emptied,
  re-run T1 with no further learning. Pass iff
  T1_ablated < T1_full (strict). Report full 20-item scores under
  ablation; the drop must be localized to negation items.
- F5: 20-item test accuracy >= 16/20 AND SIZE group (115,116,117)
  == 3/3.

## F3 file paths (this rebuild)

- Learner (audited):
  docs/lab/research-lead/overnight-20260928/opscope_rebuild/opscope_learner.zag
- Excluded world:
  docs/lab/research-lead/overnight-20260928/opscope_rebuild/opscope_world.zag
- Excluded harness:
  docs/lab/research-lead/overnight-20260928/opscope_rebuild/opscope_harness.zag

The word table (including the "not" string) lives only in the
excluded world file. The learner operates purely on integer unit
ids and contains no word literals.

## Kill bars (this build)

- K1: this prereg committed before any implementation file. PASS
  requires the prereg commit hash to precede implementation commits.
- K2: F1-F5 executed with per-item results reported. PASS requires
  results, not passes.
- K3: pure Zag, deterministic, 3/3 byte-identical. Any Python at any
  stage (including scratch, byte checks, verification) fails K3.

## Governance

- Pure Zag only. No Python anywhere. Byte checks via the
  shell-only snippet
  docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
- No em dashes in source or docs.
- Owned path only:
  docs/lab/research-lead/overnight-20260928/opscope_rebuild/.
- Do not modify the research paper or any other worker's files.
- Verdict: OPSCOPE-REBUILD-PASS iff K1+K2+K3 hold and F1-F5 all
  pass; otherwise OPSCOPE-REBUILD-FAIL with per-falsifier results.
- Do not weaken K=2 or any other bar after seeing results.
