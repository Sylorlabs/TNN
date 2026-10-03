# Independent reproduction report: REPEXPAND-1

Verdict: REPRODUCED.

Worker: independent reproduction worker (step 4 of the 11-step frontier
promotion pipeline). Pure Zag verification only. No Python anywhere in this
reproduction. No em dashes in this report.

## Source provenance

- Builder result commit: 675fdf4af82e27375c3cc1421e878242fb5111d5
- Builder prereg commit: cb352368427c006b1872d76acbcf3d056e80fd7d
- `git merge-base --is-ancestor cb3523684 675fdf4af`: YES (strict ancestor,
  verified by this worker).
- Extracted source: `repexpand.zag` (534 lines) taken from the committed blob
  at 675fdf4af via `git show`, never from the working tree.
- Commit range scan: `git diff --name-only cb3523684..675fdf4af` contains
  exactly 3 files (REPEXPAND_RAW.txt, REPEXPAND_RESULT.md, repexpand.zag)
  and zero .py files.

## Toolchain

- Frozen toolchain: znc 2026.07.0-dev (edition 2026) at
  /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc.
- Compilation of the committed source succeeded. Analyzer emitted 7
  non-fatal warnings (string buffer, adding 0, ignored return values);
  build not blocked.

## Determinism (K-RX-7)

- Compiled binary run 3 times. md5 of all three outputs:
  ed7c79a110742dba862b7db9f06aeaf2.
- Claimed builder raw md5: ed7c79a110742dba862b7db9f06aeaf2. MATCH.
- `cmp` of each reproduction run against the committed REPEXPAND_RAW.txt
  blob: byte-identical. 3/3 byte-identical runs.

## Kill-bar verification against the frozen prereg

All 8 bars checked from the committed raw output against the definitions in
PREREG_REPEXPAND.md (committed at cb3523684, strict ancestor of the result).

- K-RX-1 impossibility: reported `max604=3 checkset=12`, verdict PASS.
  Bar requires max over the 604 canonical L-expressions on E_1..E_12 < 12.
  3 < 12. PASS.
- K-RX-2 creation: 2 nodes created, both with type tag 7 (COUPLED),
  outside L's frozen {1,2,3,4}. TRACE-CREATE lines carry the episode index
  (ep=2, ep=29), the discovered relation (EQ(0),EQ(0) then EQ(0),MUL(2)),
  and evidence count 3 (evid_ns lists 3 spec counts). PASS.
- K-RX-3 hidden success: HIDDEN 4/4 and EXTENDED 3/3, both with the created
  v1 node as primary. PASS.
- K-RX-4 ablation: growth-disabled learner scores 0/4 on ABLATION-HIDDEN.
  Bar requires <= 1/4. PASS.
- K-RX-5 reuse and transfer: TRANSFER 4/4 (including new spec byte '$',
  new alphabet "xy", unscored distractors). node_assisted_exact=16 >= 10.
  PASS.
- K-RX-6 revision: TRACE-RETIRE names v1 contradicted by v2; v2 created
  with rel2=MUL(2) (different from v1's EQ(0)); FOLLOWUP 2/2 with v2.
  PASS.
- K-RX-7 determinism: 3/3 byte-identical raw outputs, md5 matches the
  committed raw md5. PASS.
- K-RX-8 purity: zero .py files in the prereg..result commit range; byte
  scan of all three committed documentation blobs found no em dash bytes.
  Verification performed without Python. PASS.

Result: 8/8 frozen kill bars reproduced from committed source.

## What the raw trace shows (white-box evidence, verbatim semantics)

- Episodes 0-2 (TRAIN, n=2,3,5): primary=BESTL, all predictions fail
  (pred=0,0,0,0 vs act=97,2,98,2 etc.).
- RX-TRACE NOTICE consecutive_failures=3 at ep=2 triggers relation search.
- RX-TRACE SEARCH: both content runs EQ to the spec length on all 3
  failures; symbol binding to head positions holds.
- RX-TRACE CREATE node=3 type=COUPLED v=1 ep=2 evid_ns=2,3,5.
- Episodes 3-16: NODEv1 primary, exact predictions on TRAIN remainder
  (3/3), HIDDEN (4/4), EXTENDED (3/3), TRANSFER (4/4): 14 consecutive
  exact predictions with v1, uninterrupted by the transfer surface change.
- ABLATION learner (growth disabled): 0/4 on the same HIDDEN set.
- Episodes 27-29 (CONTRADICTION, content a^n b^(2n)): v1 fails 3
  consecutive times; NOTICE fires at ep=29; SEARCH finds
  rel1=EQ(0), rel2=MUL(2); v1 retired with reason naming v2; v2 created.
- Episodes 30-31 (FOLLOWUP): NODEv2 primary, 2/2 exact.
- Final node table: slot 2 type=7 v=2 status=1 (active),
  slot 3 type=7 v=1 status=2 (retired).

## Verdict scope

This reproduction confirms the builder's BUILD-PASS claim at step 4 of the
promotion pipeline: committed source compiles under the frozen toolchain
and reproduces the committed raw output byte-identically, and the 8 frozen
bars read as PASS against the committed prereg. This worker does NOT
promote the mechanism to SURVIVES; steps 5-11 (simple-baseline comparison,
alternative-explanation attack, OOD, ablation, transfer/reuse, independent
red team, governance audit) remain.

## Key attack surface for the independent adversary

The prereg freezes a defense against the "disguised menu" objection in
section 9: the EQ/MUL/ADD relation search is presented as generic binary
relations over observed features rather than enumerated solution
structures, and the reified production (runtime parameter binding across
run positions) has no counterpart in L. The adversary should attack exactly
this: whether the three-template {EQ, MUL, ADD} search plus fixed trigger
(3 consecutive failures), fixed evidence window (F=3), and fixed type tag
assignment amount to a researcher-authored menu of solutions with
data-determined parameter filling, i.e. strong L2+ parameter learning
rather than L3 representational expansion. Relevant prereg lines for the
adversary: section 6c (failure monitor, F frozen), 6d (EQ/MUL/ADD checked
in fixed order), 6e (reification condition), 6g (phase permissions), 7
(what counts as learner-created), 9 (pre-registered defense), 10 (honest
limitation: relation search restricted to source=observed run and
{EQ, MUL, ADD}). A successful attack would construct a world needing a
relation outside {EQ, MUL, ADD} or a creation trigger the fixed monitor
cannot reach, and show the learner's "expansion" collapses to template
fitting; a failed attack would strengthen the claim that the production
with runtime-bound parameters is genuinely new.
