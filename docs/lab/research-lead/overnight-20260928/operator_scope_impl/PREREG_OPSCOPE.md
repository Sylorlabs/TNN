# PREREG: Operator/Scope R1-R4 Implementation (Retry)

## Ancestry

- Design: commit `71f98aa72` (OP_SCOPE_DESIGN.md, 399 lines, DESIGN-COMPLETE).
- Review trigger: SEG_REVIEW2, commit `842638d15`.
- Previous builder: OPSCOPE-MISSING (no output). This is the retry.
- This prereg is frozen before any implementation. K1.

## Mission

Implement R1 (compositional interpretation over spans, OPREC), R2
(operator discovery from systematic prediction residuals, DELETION
signature, zero-parameter gate, re-grounding replay), R3
(scope-conditioned grounding with residual attribution), and test the
R4 frozen falsifiers F1-F5. Report OPSCOPE-PASS or OPSCOPE-FAIL.

No L3 claim is made. The discovery criterion, span combiner, record
structure, signature family, routing, and all constants are
researcher-authored machinery. Bounded L2 direction, per the design.

## Frozen constants

| Constant      | Value | Meaning                               |
|---------------|-------|---------------------------------------|
| B0 burn-in    | 20    | episodes before first discovery check |
| E interval    | 10    | discovery/retirement check cadence    |
| N_ep recur    | 5     | min episodes containing W             |
| Fmax elig     | 1     | max features in record(W, DEFAULT)    |
| N support     | 4     | min residual events for W             |
| C consistency | 0.75  | min signature-match fraction          |
| K diversity   | 3     | min distinct scope unit forms         |
| OPMAX         | 8     | operator table cap                    |

These are frozen. No change after this commit.

## Battery (frozen)

The frozen DEVANG battery, defined by `gen_episodes` in
`docs/lab/research-lead/overnight-20260928/devang4/devang4.zag`
(seed 123456789, 100 train episodes one-pass online, 20 test
utterances). The world-generation code (RNG, word tables,
gen_direct, gen_neg, gen_rel, gen_size, gen_d3, build_utt,
gen_episodes) is copied verbatim into `opscope_world.zag`. No
modification to the episode sequence.

### Frozen item ids

- T1 (NEG-novel, F1): episodes **109, 110, 111** ("tak not grn").
- T3 (scope-shift, F2): episodes **109, 110, 111** ("grn" is familiar
  affirmatively from phase-2 training episodes 60-79 and never negated
  in training; T1 and T3 coincide on this battery, documented here).
- SIZE group (F5 K6): episodes 115, 116, 117.

### Units (segmentation interface)

The design (section 6) leaves segmentation orthogonal and consumes
its output through the existing unit-output interface. This build
uses the true word-id sequence as the unit sequence U (oracle
segmentation interface), which factors out the segmentation confound
that SEG_REVIEW2 already ruled non-binding. Word ids:
0=tak 1=not 2=red 3=blu 4=grn 5=bal 6=sph 7=cub 8=tri 9=big
10=biger 11=smal.

### Observed target T (feature set)

Consequence-feature vocabulary: the 12 word ids. For each episode,
with target object tobj (color c, shape s, size z):

- T = { w in U : tobj satisfies w }, as a 12-bit mask.
- Satisfaction: tak always; not never; red iff c==0; blu iff c==1;
  grn iff c==2; bal/sph iff s==0; cub iff s==1; tri iff s==2;
  big iff z==1; smal iff z==0; biger iff z==1 and some other object
  shares tobj shape with size 0.
- Check: DIRECT "tak C S" gives {tak,C,S}; NEG "tak not C" gives
  {tak}; REL "tak biger S" gives {tak,biger,S}; SIZE gives
  {tak,sizeword,S}; 3WAY "tak big grn bal" gives {tak,big,grn,bal}.

The learner never sees objects, target index, or template. It sees
only (U, T) per episode.

## Learner specification (frozen)

### Records

- `cnt[u][f]`, `occ[u]`: DEFAULT context counts. Update (R3 routing):
  no active operator: every u in U gets occ[u]++, and cnt[u][f]++
  for each f in T. Active operator O with trigger at position i:
  units before i update DEFAULT with T; units after i update
  record(u,O) with residual R = T minus rest_pred (rest_pred uses
  current DEFAULT records of pre-trigger units); the trigger unit
  gets no update while its operator is active.
- Binarized record mask: bit f set iff occ[u] > 0 and
  cnt[u][f]*2 >= occ[u]. (Researcher-chosen; disclosed.)
- Per-operator records: cntO[k][u][f], occO[k][u], same rule.
  OPMAX=8.

### R1 interpret(U)

- Find the first active OPREC (table order) whose trigger_form
  occurs in U; use its first occurrence index i (frozen tie-break).
- None: return OR over u in U of recmask(u, DEFAULT).
- Found: return (OR over u in U[0..i-1] of recmask(u, DEFAULT))
  OR (OR over u in U[i+1..] of recmask(u, O)).
- OR (bitwise) is the frozen generic span combiner.

### R2 discovery

- Episode store: all 100 training (U, T) pairs retained
  (for the gate and re-grounding).
- For training episode t with t >= B0: compute P0 with current
  records. If P0 != T, for each position i with W = U[i], record a
  residual event for W holding scope_pred, rest_pred, T, and the
  scope form mask. Per W accumulators: support (event count),
  match (signature_match count), scopeforms (OR of scope form
  masks), epcount (episodes containing W).
- signature_match(W, event): (a) scope_pred nonempty; (b) rest_pred
  subset of T; (c) (scope_pred minus T) nonempty. DELETION only.
- Proposal check after episode t when (t+1) >= B0 and
  (t+1) % E == 0 (checks at 20, 30, ..., 100 episodes seen).
  For each eligible W ((e1) epcount >= N_ep; (e2) popcount of
  recmask(W, DEFAULT) <= Fmax): require support >= N;
  match*4 >= support*3 (C=0.75, integer); popcount(scopeforms)
  >= K; gate: correct_sig > correct_base (strict), where over all
  stored episodes correct_sig counts sig_predict(W) == T and
  correct_base counts P0 == T, with sig_predict(W) = rest_pred
  (current DEFAULT records, first-W rest) on W-containing episodes
  and P0 elsewhere. On pass and table space: install OPREC
  {trigger_form: W, scope_rule: REST_OF_UTTERANCE, signature:
  DELETION, support, created_at: episodes-seen}.
- Installation: re-grounding replay. Rebuild every DEFAULT record
  from non-O-active stored episodes only; build record(u, O) for
  all u from O-active stored episodes via the R3 router; install
  the OPREC.
- Retirement: every E episodes, re-run the gate per installed
  operator over stored episodes; retire if the gate no longer
  favors it. Specified; the frozen battery does not test it
  (disclosed).

### Determinism

Single-threaded, fixed seed, no randomness in the learner. Three
runs must be byte-identical (md5).

## R4 falsifiers (frozen bars)

- F1: T1 items 109,110,111 all pass (predicted mask == T mask) AND
  white-box dump shows an OPREC with trigger_form == wid 1,
  signature DELETION, created_at > 0, support >= N.
- F2: T3 items 109,110,111 all pass.
- F3: source audit on the committed learner file(s) listed below:
  grep for byte string "not" returns 0 hits; grep -i "negat" 0
  hits; grep "is_negator" 0 hits. Routing predicate references only
  OPREC.trigger_form_id (inspection note in result doc).
- F4: ablated copy of trained state with operator table emptied,
  re-run T1 with no further learning. Pass iff
  T1_ablated < T1_full (strict). Report full 20-item scores under
  ablation; the drop must be localized to negation items.
- F5: 20-item test accuracy >= 16/20 AND SIZE group (115,116,117)
  == 3/3.

## F3 file paths (frozen)

- Learner (audited): `docs/lab/research-lead/overnight-20260928/operator_scope_impl/opscope_learner.zag`
- Excluded world: `docs/lab/research-lead/overnight-20260928/operator_scope_impl/opscope_world.zag`
- Excluded harness: `docs/lab/research-lead/overnight-20260928/operator_scope_impl/opscope_harness.zag`

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

- Pure Zag only. No Python anywhere.
- No em dashes in source or docs.
- Owned path only:
  docs/lab/research-lead/overnight-20260928/operator_scope_impl/.
- Do not modify the research paper or any other worker's files.
- Verdict: OPSCOPE-PASS iff K1+K2+K3 hold and F1-F5 all pass;
  otherwise OPSCOPE-FAIL with per-falsifier results.
- Do not weaken any bar after seeing results.
