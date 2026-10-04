# L3-RX PREREG (frozen)

**Status: FROZEN.** Committed alone before any implementation file exists
in this lane. Any change after this commit is a new preregistration, not
an amendment. Verdicts name the exact bars below; VOID is terminal.

**Provenance.** Design: L3-NEXT worker, `tnn-native-lab@e7adec947`,
`l3_next/L3_NEXT_DESIGN.md` (prereg-ready; "proposed thresholds").
This document freezes exact numbers. Deviations from the design prose
are listed in section 16 — all are narrowings, none widen researcher
degrees of freedom.

**One-paragraph concept.** The learner starts with the frozen L_old
capability: binary edge sets over two entity slots, with an exact
consistency decision procedure. It faces context-gated order worlds
whose ground truth is provably inexpressible in L_old (theorem,
section 4). The learner must detect the inadequacy itself
(empty hypothesis set + re-verified observations -> contradiction
certificate), invent a new form by composing four generic operators
(arity-lift, guard-attach, union, project — never enumerated as
complete forms in source), solve hidden instances, reuse the form,
transfer it across opaque recode, revise it under regime change, and
let it retire on a plain world. The anti-S1 completeness invariant
governs every loop exit.

## 1. Observation and form language (frozen)

- Observation: `(s0, s1, s2, d)`. `s0..s2` are opaque u8 identifiers
  (no semantics attached; the learner never sees what they denote).
  `d` in {0,1} is the label to predict.
- Worlds are deterministic: the same triple always yields the same `d`.
- L_old form (frozen): a total map `dir` from unordered id-pairs
  `{x,y}` (x,y drawn from slots s1,s2) to {0,1}. Prediction for
  `(s0,s1,s2)` = `dir[{s1,s2}]`; slot s0 is ignored by L_old.
  This is the frozen "binary edge set" capability.
- L_new form (invented, not in source): a list of guarded chain
  rules. Rule = (guard set G of s0-values, permutation P of the
  item ids). Prediction: first rule with `s0 in G`; `d = 1` iff
  `pos_P[s1] < pos_P[s2]`, else 0.
- `|structure|` = number of top-level guarded-chain rules.
  Compression cap C = 10 rules.

## 2. Operator set (frozen; genericity argument per operator)

Source may contain exactly these four form operators, each addressed
only by slot indices and index sets:

- OP-LIFT (arity-lift): add one slot index to a form's key set.
  Generic: it names no slot, no domain; "add slot k to the key".
- OP-GUARD (guard-attach): restrict a rule's applicability to a
  subset of values of one key slot. Generic: value-set partition,
  no semantics of what the values mean.
- OP-UNION: the committed structure is a disjunction (list) of
  guarded rules. Generic: list concatenation of rule sets.
- OP-PROJECT: drop a slot index from a form's key set.
  Generic: key-set deletion.

No operator branches on world properties, slot meanings, or the
values' interpretation. No complete form (guarded edge set, ternary
relation, chain pair) appears in source as a constructor, template,
or enumerated candidate (audit A3).

## 3. HYP_BUILD completeness (honest empty-H; answers design section 7.1)

L_old hypothesis = total map `dir` over unordered pairs.
Consistency with training T: for every `(s0,s1,s2,d)` in T,
`dir[{s1,s2}] == d`.

**Theorem (frozen):** Let `labels({x,y})` = set of `d` values observed
in T for pair `{x,y}` over all s0. Then the L_old hypothesis set H is
empty IFF some pair has `labels = {0,1}`.

*Proof.* (->) If some pair has both labels, no total map can match
both observations on that pair, so H is empty. (<-) If every pair
has at most one label, the map `dir[{x,y}] = the unique label`
(or arbitrary where unobserved) is consistent, so H is nonempty.
The per-pair decision is independent because consistency factors
per unordered pair. QED.

**Consequence frozen:** empty-H is decided by an EXACT linear scan
for a conflicting pair — not by bounded enumeration. There is no
enumerator bound to tune, so "H empty" cannot be an artifact of
search incompleteness. The conflicting pair and the two observation
sequence numbers are the contradiction certificate.

For probe worlds (section 8, family F2): gap pairs (unobserved) make
H a finite explicit set of size 2^g, g <= 6 frozen (64 hypotheses,
all enumerated; budget exceeded -> honest DEFER). No bound issue.

## 4. Learner-owned inadequacy detection (frozen trigger)

The ONLY path to form expansion is all of the following, in order:

1. OBSERVE: load training T.
2. Exact conflict scan (section 3). If a conflicting pair exists:
3. kb lookup: is there a stored form whose key-slot set is a
   superset of the slots on which the two conflicting observations
   differ (computed by slotwise comparison, no semantics)?
   - YES -> FORM_REUSE (section 6). No re-verification, no expansion.
   - NO -> continue:
4. RE-VERIFY: re-query the two conflicting observations through the
   TEST channel (2 queries, harness-answered from the sealed oracle).
   If either answer differs from training -> DEFER with certificate
   `DATA-UNTRUSTED` (the world is not deterministic; no form claim).
5. CERTIFICATE: emit the minimal conflicting observation pair
   (sequence numbers) to the trace.
6. EXPANSION SEARCH (section 5).

There is no failure-count threshold, no world-property condition, and
no researcher escape hatch anywhere in this path (audit A4).

## 5. Form invention search (frozen order)

Given the certificate pair differing on slot set Dslots (nonempty):

1. For each slot `s` in Dslots in fixed numeric order (MDL: one added
   slot before two):
   a. Candidate form = OP-LIFT(L_old key {1,2}, s).
   b. Content induction under the candidate:
      - Partition T by value of slot s.
      - Per partition: exact pair scan; any conflict -> candidate
        rejected.
      - Per partition: induce chain by tournament score
        (out-degree = #{y : dir=1}; sort descending; deterministic).
        This is pure counting over the pair table, no order
        semantics in source.
      - Re-verify: every training observation must be predicted
        correctly by the induced chains; else candidate rejected.
   c. Compress: group partitions with identical chains;
      OP-GUARD merges each group into one rule (guard = value set);
      OP-UNION assembles the rule list. Log each operator
      application with SEQ and parent pointer.
   d. First candidate passing (b)-(c) is accepted; stop.
2. Post-induction simplify: OP-PROJECT — try dropping each lifted
   slot; if the form stays training-consistent without it, drop it
   and log PROJECT_DROP, else log PROJECT_KEEP.
3. Store the accepted form in kb (FORM_STORED with lineage).
   COMMIT (disagreement empty).
4. If no candidate passes -> honest DEFER with certificate
   `NO-FORM`.

The final form's topology (which slot lifted, how many guarded
rules, which guard sets) is determined by the world's conflict
structure, not enumerated in source.

## 6. Reuse, transfer, revision, retirement (frozen)

- REUSE (families F3/F4/F5): on the kb-match path, instantiate the
  stored form: partition T by the form's key slots, induce chains
  per partition exactly as in 5(b), compress with OP-GUARD/OP-UNION,
  COMMIT. Log FORM_REUSE (never FORM_EXPAND). Content parentage is
  the current world's observation SEQs (purge-auditable).
- TRANSFER (F4): identical to reuse; the world is an opaque id
  permutation of a solved world. Slot positions are NOT permuted
  (documented scope boundary; slot-permutation transfer is future
  work, not claimed).
- REVISION (F5): identical to reuse; the kb form is overwritten by
  the re-induced form (FORM_REVISED lineage). Stale content must be
  fully purged (bar RX-K11).
- RETIREMENT (F6): the learner tries candidate forms in MDL order:
  L_old first (fewest key slots), then kb forms. On a plain world
  L_old is training-consistent, so the binary form is committed and
  the guarded form is never instantiated. Observable: the final
  commit is guard-free. OP-PROJECT is implemented and applied in
  the simplify step (section 5.2); on gated worlds it logs
  PROJECT_KEEP (guard necessary), which the trace audit verifies.

## 7. Anti-S1 completeness invariant (frozen)

Every learning loop in the learner terminates IFF:

- (a) the disagreement set is EMPTY -> COMMIT; or
- (b) honest DEFER with a certificate (`DATA-UNTRUSTED`, `NO-FORM`,
  `BUDGET` with unresolved items named, or `NO-EXPAND` for the
  ablated control).

Disagreement sets:
- Invention loop: training observations mispredicted by the current
  candidate form.
- Probe loop (F2): gap pairs on which the current hypothesis set H
  disagrees; empty IFF |H| = 1.

FORBIDDEN exits (automatic design violation, caught by trace audit):
stopping because a base hypothesis was eliminated; materializing
only the first disagreeing pair; committing with a nonempty
unresolved disagreement set and no certificate.

Probe loop (F2, frozen): H = all 2^g hypotheses (g <= 6). E* =
all-gap-bits-zero member (frozen deterministic tie-break). Repeat:
recompute disagreeing gap pairs from CURRENT H; probe the first in
id order via the TEST channel; H <- {h consistent with answer}.
Terminate by (a) |H| = 1 -> COMMIT the survivor's full pair table,
or (b) 12 probes exhausted -> DEFER + `BUDGET` naming unresolved
pairs. After EVERY answer the trace logs |H|; the audit verifies
re-filtering happened (no S1 early exit).

## 8. Sealed world families (frozen; materialized post-freeze)

Adversary program `adv.zag`, frozen seed 20261003 (LCG), runs only
after the learner implementation is frozen (CODEFREEZE digest
recorded). 11 worlds total. 8 item ids per world (opaque, adversary-
permuted); 2 context ids per gated world (opaque, arbitrary u8).

- F1 insufficiency (4 worlds): ground truth = (O1, O2), two total
  orders over the 8 items; query (c,x,y) truth = direction under
  O1 if c = c1 else O2. |D| in [6,12] where D = pairs on which O1,O2
  disagree (adversary's choice, recorded in CERT). Training: all
  112 triples minus 6 heldout = 106. Heldout: 6 triples = 3 D-pairs
  x 2 contexts (frozen; never trained, never probed).
  Insufficiency certificate per world: D, the conflicting training
  observation seqs, |D|, cap C=10, and the section-3 theorem
  instantiated (no L_old map consistent).
- F2 S1 probe-ordering (2 worlds): single total order O; s0 = one
  constant pad id; training omits 6 gap pairs (12 triples) = 100
  training triples. Adversary white-box selects O so that probing
  disagreeing gap pairs in id order eliminates E* on the FIRST probe
  (reverse O if needed; frozen selection procedure). Bar: committed
  pair table equals ground truth on all 28 pairs (ALL gaps resolved).
- F3 reuse (2 worlds): fresh F1-style worlds (new O1,O2,D,ids).
- F4 recode (1 world): opaque id permutation (items and contexts)
  of F1-W1, including its heldout triples. Slot positions unchanged.
- F5 regime change (1 world): F1-W2's O1 with a new O2' such that
  |D symdiff D'| >= 4; fresh ids.
- F6 retirement (1 world): single total order; s0 = one constant
  pad id; 106 training + 6 heldout triples.

Oracle: per world, the full 112-triple truth table, sealed in
`oracle.txt`, opened ONLY by the harness answer program. The learner
never opens any world, oracle, CERT, or heldout file (audit: the
string "oracle"/"heldout"/"CERT" appears nowhere in learner source;
the learner takes only explicit argv paths).

Attribute decorrelation note: worlds carry no attributes besides
opaque ids, so Spearman-style decorrelation is vacuous; the design's
decorrelation clause is satisfied by identifier opacity (documented
deviation, section 16).

## 9. Bar table (frozen thresholds)

| Bar | Content | Frozen threshold |
|---|---|---|
| RX-K1 | Final form not in source | Source audit PASS: 0 forbidden-token hits in learner .zag (token list section 12) |
| RX-K2 | Form created after experience | Trace audit: min SEQ(FORM_EXPAND) > max SEQ(OBSERVE or TEST) preceding it, on every expansion world |
| RX-K3 | Persistent learner state | F3 runs: FORM_EXPAND count = 0 AND kb.txt contains a FORM_STORED record from F1 |
| RX-K4 | White-box creation trace | Every FORM_EXPAND/FORM_REUSE/FORM_REVISED has a parent SEQ resolving to a CERTIFICATE or prior FORM record (replay check PASS) |
| RX-K5 | Hidden instances solved | F1 (4 worlds): heldout >= 5/6 each AND \|structure\| <= 10 each; F2 (2 worlds): committed table = truth on all 28 pairs each |
| RX-K6 | Ablation destroys advantage | No-operator control (`noops` flag) on F1-W1..W4: heldout < 5/6 on each (expected 0/6 via honest DEFER) |
| RX-K7 | Reused later | F3 (2 worlds): FORM_EXPAND = 0, TEST_reuse = 0 <= TEST_scratch/2 (= 2/2 = 1), heldout >= 5/6 each. TEST = all TEST-channel queries. Scratch = same learner, kb wiped |
| RX-K8 | Transfers across recode | F4: heldout >= 5/6, FORM_EXPAND = 0; protocol assertion heldout_n = 6 > 0 PASS (regression guard for the T3b 0/0 class) |
| RX-K9 | Beats controls | Memorization control (nearest (s1,s2)-match predictor) on F1: < 5/6 each world; L_old-only control = RX-K6 (recorded as separate bar per design) |
| RX-K10 | Independent red team | PENDING — different instance, follow-up worker. Not claimed by this lane. |
| RX-K11 | Revisable AND retirable | F5: heldout >= 5/6 AND purge audit PASS (0 rules in the F5 commit carry F1 parentage); F6: final commit guard-free AND heldout >= 5/6 |
| RX-K12 | 12/12 rule | Any red among K1-K9, K11, KC0A-D => verdict L3-KILLED. All green with K10 pending => CONDITIONAL-PASS (L3-SURVIVES requires 16/16 including K10) |
| RX-KC0A | Runtime-defined semantics | Audit A1-A5 PASS (section 12) |
| RX-KC0B | Open structural form | Audit: operators have no arity-cap constant and no named-relation constructors; committed forms' rule counts/guard sets vary with worlds (recorded in report) |
| RX-KC0C | Sealed post-freeze worlds | 11 worlds materialized by adv.zag (seed 20261003) after CODEFREEZE; families F1-F6 exactly as section 8 |
| RX-KC0D | Cognitive reuse | RX-K7 and RX-K8 green AND F3/F4 predictions served from the kb-resident form (trace: FORM_REUSE -> COMMIT -> heldout scored >= 5/6) |

## 10. Controls (frozen definitions)

- C-NOOP: learner built with operators disabled (`noops` argv flag;
  the ONLY behavioral difference is the expansion search is
  replaced by DEFER `NO-EXPAND`). Run on F1-W1..W4.
- C-MEM: separate pure-Zag program `mem.zag`: for each heldout
  triple, predicts the majority `d` among training observations with
  equal (s1,s2) (ties -> 0; deterministic). Run on F1-W1..W4.
- C-SCRATCH: the unmodified learner with kb.txt wiped, run on the
  F3 worlds; measures TEST_scratch (expected 2: the re-verify
  queries) and must log exactly 1 FORM_EXPAND.

## 11. Determinism protocol (frozen)

- Learner: no randomness (all orders fixed: numeric id order;
  ties -> lowest id). Adversary: LCG seeded 20261003.
- 3 full battery runs. Digest = sha256 over
  summary.txt + trace.txt + proto.log (protocol log of TEST
  queries/answers). 3/3 byte-identical required.
- Learner invocation cap: 40 per world (anti-hang; exceeding =
  infrastructure FAIL, not a bar).

## 12. Source-audit procedure (frozen; runs on the frozen source)

Auditor: the builder at freeze; K10's independent auditor re-runs.

- A1: `grep -icE` over learner .zag sources for the forbidden
  token set: `order|context|preced|rank|dominan|before|after|disagree|total`.
  Required: 0 hits. (Rationale: these name target-domain
  regularities. Operator names op_lift/op_guard/op_union/op_project
  are allowed: they name structural edits, and A2 checks they are
  generic.)
- A2: operator inventory = exactly {op_lift, op_guard, op_union,
  op_project}; each takes only slot indices / index sets / value
  sets; no branch keyed to a slot's meaning or a world's property.
  Verified by auditor reading the operator definitions.
- A3: no complete form in source: no literal multi-slot pattern
  table, no chain-pair constructor outside the operators'
  generic assembly; the only form constructors are the four
  operators. Verified by auditor reading the induction code.
- A4: the expansion search is called from exactly one site, guarded
  by (conflict AND reverify_ok AND NOT kb_match AND NOT noops).
  Verified by auditor reading the dispatch.
- A5: loop exits are exactly COMMIT-on-empty-disagreement and
  DEFER-with-certificate. Verified by auditor reading the loops
  AND by the trace audit (every run's trace ends in COMMIT or
  DEFER; SEQ monotonic; no other terminal event).

## 13. Trace-audit procedure (frozen)

`audit.zag` (pure Zag) checks, per run:
- SEQ strictly increasing across trace.txt.
- K2: min SEQ(FORM_EXPAND) > max SEQ(OBSERVE|TEST) before it.
- K4: every FORM_EXPAND/FORM_REUSE/FORM_REVISED parent SEQ resolves.
- A5: terminal event in {COMMIT, DEFER} only.
- Anti-S1 (F2): after each PROBE_ANSWER, |H| strictly decreases or
  stays with D recomputed; terminal COMMIT only at |H| = 1;
  every gap pair probed at most once; unresolved set empty at COMMIT.
- K3: F3 traces contain zero FORM_EXPAND.
- K11-purge: every rule in the F5 commit has parent SEQs >= F5's
  first OBSERVE SEQ.
- K8: F4 trace contains zero FORM_EXPAND; heldout_n = 6 asserted
  by the scorer before scoring.

## 14. Adversary instructions + independence statement

- The adversary is the program `adv.zag`, written AFTER the learner
  freeze (post-CODEFREEZE), seeded 20261003, generating the 11
  worlds of section 8 plus per-world CERT.txt and the sealed
  oracle.txt files.
- The learner binary is frozen before `adv.zag` runs; its digest is
  recorded in CODEFREEZE.md and re-verified before the battery.
- The learner's only world contact: train.txt, probe_ans.txt
  (via the harness `answer` program, which alone opens oracle.txt),
  and its own kb/trace/commit files.
- F2 E*-kill selection (frozen): adversary simulates the frozen
  learner's probe order (first disagreeing gap pair in id order);
  chooses O; if O's direction on that pair equals E*'s prediction,
  reverses O. (Reversal preserves total-order-ness; always succeeds.)
- This lane's builder also authors `adv.zag` (single-worker
  limitation, documented). Mitigations: worlds generated
  post-freeze from a frozen seed; learner has no access to world
  internals (file protocol + audit); the F2 adversary is white-box
  by design (it must kill E* first). A fully independent adversary
  and the R1-R5 red team are RX-K10's scope (pending).

## 15. Governance

- Pure Zag; safebin mandatory (NAMECHECK Step 0).
- Prereg committed BEFORE worlds are materialized (commit-order
  self-check in the build log).
- New experiment, not a repair of L3-INR. L3-INR's C409 kill is
  terminal and is not revisited. L3-INR machinery is NOT reused as
  code; L_old is re-specified and re-implemented here from the
  frozen spec above (cleaner freeze boundary).
- Opaque identifiers throughout; no domain modes, no classifier/
  router (overnight clarification). Standing test applies.
- Commits local, never pushed, explicit pathspecs.

## 16. Deviations from the design prose (all narrowings, frozen here)

1. Design table said "|D_trained| = 8, cap C = 10" in one place and
   "|D| >= 6" in another. Frozen: |D| in [6,12] (adversary's
   choice, recorded); |structure| counts guarded-chain rules
   (expected 2); cap C = 10. The insufficiency argument does not
   need the cap: section 3's theorem gives exact H-emptiness.
2. Design's cap-based insufficiency prose ("needs >= |D_trained|
   edges") is superseded by the section-3 exact theorem, which is
   stronger and has no enumerator bound (answers design 7.1).
3. L_old is re-implemented from the frozen spec, not code-reused
   from L3-INR (cleaner freeze; same behavioral contract).
4. Candidate-form validation via the consequence channel is
   training-consistency (exact), not a separate TEST sample: with
   dense training any fresh TEST triple would be either in training
   (vacuous) or heldout (protocol violation). TEST-channel queries
   are: re-verify (2), F2 probes (<= 12). K7's frozen numbers
   follow: TEST_reuse = 0, TEST_scratch = 2.
5. RX-K7's "probe count" is defined as all TEST-channel queries
   (section 9). The sample-efficiency gain is 2 -> 0 queries plus
   1 -> 0 FORM_EXPAND events.
6. Decorrelation: vacuous by identifier opacity (section 8 note).
7. F4 recode permutes ids only, not slot positions (documented
   scope boundary).
8. RX-K10 is PENDING by construction (different instance required);
   the verdict rule RX-K12 is frozen accordingly
   (CONDITIONAL-PASS, not SURVIVES).
9. OP-PROJECT's observable role: the post-induction simplify step
   (logs PROJECT_KEEP/DROP); F6 retirement is via MDL form
   selection with a guard-free observable commit (section 6).
