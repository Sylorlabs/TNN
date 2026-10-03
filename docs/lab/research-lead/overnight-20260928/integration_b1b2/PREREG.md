# PREREG: INTEGRATION-B1B2 (port C443 B1/B2 contracts into the COGOPS composer)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/integration_b1b2/` only.
Worker: INTEGRATION-B1B2 worker (subagent, 2026-10-03).
Parent mandate: SUBSUMPTION-P0 (C443) follow-up. C443 found a genuine
partial win: the C424 5-op contract module subsumes COGOPS's judgment
halves (trial-learned bindings as per-tag admission contracts, version
routing as coverage admission) and adds revision-under-counterevidence
that C433's BIND table lacks, while plan assembly, execution, and step
verification stay outside it (G1-G3). This experiment ports B1/B2 back
into the COGOPS composer and tests the integration at the binding
layer.

Commit order: this prereg (plus NAMECHECK.md Step 0) strictly precedes
all implementation. No implementation file exists in this lane at this
commit.

## 1. Question and predicted outcome

Question: can the C443 B1/B2 binding+coverage contracts be integrated
at the COGOPS composer's binding layer, giving the composer
revision-under-counterevidence without losing its procedure
composition ability?

PREDICTED OUTCOME (frozen): INTEGRATION DEMONSTRATED. The ported
contracts replace the BIND trial-count table (B1) and the
coverage-membership version routing (B2); all C433 frozen
composition outcomes still hold exactly (K1-K6); and dedicated
revision stages demonstrate binding revision (K10) and coverage
drift revision (K11) through the composer's live contract state.
Plan assembly, topo order, procedure bodies, and execution are
untouched: the boundary found by C443 (G1-G3) is respected, not
bridged.

## 2. The port (frozen design)

### 2.1 What is ported

From C443's frozen u_* module (subsumption_p0/sp_module.zag,
byte-copied from C424's cu_full.zag lines 55-389), four of the five
ops, function bodies VERBATIM: u_induct, u_check, u_invalidate,
u_revise, plus their helpers (u_feat_xf, u_feat_k, u_feat_val,
u_fval, u_acc, u_rej, u_rejlen, u_check_all, u_write_clause,
u_fiterr). u_grow is EXCLUDED (minimal port: B1/B2 only; grow was
not exercised even in C424). sg/ss (int-indexed state access) are
carried with the module. The module operates on a dedicated
judgment-state array S (z_alloc 16384, zeroed), separate from the
learner state L, with the module's fixed slots: judgment table
300-302 / 304+ / 528+, global counters 900-925, induct scratch
1200-1209, C_Q at slot 7. Contract bases: binding contracts at
2000+bi*100 (bi 0..7, one per binding slot); coverage contracts at
3000 (RETRIEVE), 3100 (VERIFY), 3200 (COUNT).

### 2.2 B1: binding contracts replace the BIND table

C433's BIND table (L+12744, 8 entries x 32 bytes of
[tag,bound_fam,ok0,f0,ok1,f1,ok2,f2]) is REPLACED. In its place:
- L+12744 becomes a tag directory (8 x 4 bytes: need tag per
  binding slot bi). The directory is an index only; the binding
  itself lives in the contract.
- One binding contract per tag over [tag, fam] (nf=2), at
  2000+bi*100.
- learn_bindings keeps its trial loop (same try_family calls,
  same trials stat): for each unbound tag it runs the three
  family trials, loads the judgment table from the REAL trial
  outcomes (accepts [[tag,fam]] for r==1, rejects [[tag,fam]]
  for r==0), and calls u_induct. The bound family is then read
  back through the contract: bind_fam scans fam 0..2 with
  u_check(contract,2,tag,fam); first admitted fam wins, -1 if
  none (CONTRACT_SET=0, as for tag 811, gives principled
  decline exactly as C433).
- clear_bindings resets the binding contracts (CONTRACT_SET=0)
  and the directory.

### 2.3 B2: coverage contracts replace membership routing

C433's version selection (ret_version/vfy_version/cnt_version via
ret_cov_has/vfy_cov_has/cnt_cov_has over the episode-logged
relation sets) is REPLACED by coverage admission contracts over
[rel] (nf=1):
- specialize_ret/vfy/cnt keep building their bucket indexes from
  the episode-logged relations (execution machinery unchanged),
  and additionally induct the family's coverage contract:
  accepts = the episode-logged relations, rejects = the current
  world's relation vocabulary (generic fact scan, no literals)
  minus the accepts.
- ret_version: u_check(S,3000,1,rel)==1 -> spec (2), else gen
  (0). vfy_version: every step rel admitted -> spec (3), else
  gen (1). cnt_version: admitted -> spec (5), else gen (4).
- ret_cov_clear/vfy_cov_clear/cnt_cov_clear clear the logged
  relations AND reset the coverage contract (CONTRACT_SET=0),
  so cleared coverage routes generic exactly as C433.
- The spec procedures keep their rel_ids bucket guards (the
  contract governs the routing DECISION; the rel_ids+buckets
  remain the execution index). No parallel decision path
  remains: the membership tests are no longer consulted for
  version selection (K12 audits this).

### 2.4 What is NOT ported (C443 boundary respected)

No value production, no ordering/generation, no relational step
verification: topo assembly, plan records, apply_kind1/kind3,
procedure bodies (ret_spec/vfy_spec/cnt_spec, ret_gen/vfy_gen/
cnt_gen), oracles, and the decline path are C433's logic
unchanged. u_grow is not ported. The integration is at the
binding layer only.

### 2.5 Opaque identifiers

No world literals in ib_learn.zag or ib_main.zag (same 17
identifiers as C433 K3a, verified by the same word-boundary
grep). All demo values are runtime-derived: tags from the
binding directory, rels from contract clauses and world-vocab
scans, episode inputs from fact scans. Goal constructors keep
C433's naming convention (tag digits inside names are not
word-boundary matches).

## 3. Frozen predictions: S1A-S8 (C433's goals still pass)

Stages S1A-S8 mirror C433 exactly (same worlds, episodes, goals,
oracles). All per-query predictions are UNCHANGED:

- S1A: LSTATE-RET nrel=2 ids=601,602 cnts=16,16 prov=0,0,3,56
  rev=1.
- S1B: LSTATE-VFY nrel=3 ids=601,602,603 cnts=16,16,16
  prov=1,4,7,56 rev=1.
- S1C: LSTATE-CNT nrel=3 ids=601,602,603 cnts=16,16,16
  prov=4,8,11,56 rev=1.
- S2 E0: st=2 vers=2,3,3,5 ans=7:1,611,0,1,611,1,2 cs=96
  cg=336 agree=1; plans_built=1; trials=9.
- S3 E1: st=2 vers=2,3,3,5 ans=8:1,611,1,611,1,611,1,2 cs=112
  cg=392 agree=1; plans_built=2.
- S4 R0: st=2 vers=2,3,5 ans=6:1,613,1,613,1,2 cs=64 cg=224
  agree=1; plans_built=3.
- S5 B0: st=2 vers=0,1,1,4 ans=7:1,713,0,1,713,1,2 cs=240
  cg=240 agree=1; plans_built=4 (coverages cleared incl. the
  contracts, so all-generic routing as C433).
- S6: LSTATE-CNT nrel=2 ids=701,702 cnts=16,16 prov=4,12,15,40
  rev=2; B1: st=1 vers=0,1,1,5 ans=7:1,713,0,1,713,1,2 cs=216
  cg=240 agree=1; plans_loaded=1.
- S7 X: decline=1; trials=21 total; no plan for 810.
- S8 S8: st=2 vers=0,1,1,5 ans=7:1,713,0,1,713,1,2 cs=216
  cg=240 agree=1; plans_built=5; trials=21; rederive_match=1.
- SUMMARY-DIAMOND: agree=6 plans_built=5 plans_loaded=1
  trials=21 declines=1 cs=944 cg=1672 rs=3 rg=3 vs=5 vg=6
  cts=5 ctg=1. BYTE-COMPARABLE to C433's summary line.

Binding-contract predictions (hand-derived from the frozen
u_induct; section 6):
- After S2, BCONTRACT dump (format tag/induct/clause as
  (field,xform,lo,hi)/active/dc):
  - tag=801 induct=1 clause=(1,0,0,0) active=1 dc=0
  - tag=802 induct=1 clause=(1,0,1,1) active=1 dc=0
  - tag=807 induct=1 clause=(1,0,2,2) active=1 dc=0
- After S7, additionally: tag=811 induct=0 (no clause; empty
  accept set).
- Coverage contracts after S1: RET (0,0,601,602); VFY
  (0,0,601,603); CNT (0,0,601,603). After S5: all three reset
  (CONTRACT_SET=0). After S6: CNT (0,0,701,702); RET/VFY still
  reset. (Internal state; verified via the version routing and
  the S9 reads, not dumped per stage.)

## 4. Frozen predictions: S9 revision demos (the new capability)

S9 runs AFTER S8 (no frozen query follows it) on scratch state;
it does not touch the frozen stats. Global counters 900-925 are
explicitly zeroed at S9 start, slot 908 preset to -1, S slot 7
set to 500.

### S9A BIND-REVISE (B1: binding revision under counterevidence)

Target: binding slot bi=1 (tag 802 in the frozen S2 learn order;
tag read from the directory at runtime). Its live contract is
(1,identity,[1,1]).
- Build a synthetic single-need goal (w_* helpers): need tag =
  the directory tag (802), COUNT shape [rel,1,0] where rel =
  the CNT coverage clause lo read at runtime (701), subj=0.
- Run the REAL trials: try_family fam0 -> 0 (arity), fam1 -> 0
  (not chain-shaped), fam2 -> 1 (shape admits; cnt_gen executes
  on scratch). Logged as tr0=0 tr1=0 tr2=1.
- Three counterevidence probes: u_invalidate(cb,1,0) x3, where
  judgment=1 is the standing commitment's verdict (P0 protocol;
  the actual u_check reads 1,1,0 across the probes as the
  clause retires; disclosed in REPORT). Predicted: dc=2,
  active=0 after probe 2; fail run=3 latches req=1,
  first_detect=500 after probe 3.
- Load the new table from the trial outcomes: accepts
  [[802,2]], rejects [[802,0],[802,1]]; u_revise(cb,1).
  Predicted: C_OLDERR_ON_NEW=2 (old clause errs on the new
  accept and on reject [802,1]), new clause (1,identity,[2,2]),
  C_REV_COUNT=1, req=0, run=0.
- Verify: u_check(cb,2,802,2)=1, (802,1)=0, (802,0)=0.
- Frozen BINDREV line: tag=802 probes=3 dc=2 active=0 req=1
  olderr=2 revcount=1 nclause=(1,0,2,2) route2=1 route1=0
  route0=0 tr0=0 tr1=0 tr2=1.

### S9B COV-REVISE (B2: coverage drift revision)

Uses the LIVE RET coverage base (3000); all values
runtime-derived.
- Phase 1 (old world): setup_worldA; run 4 real RET episodes
  (ids 0-3); specialize_ret (real: buckets + coverage induct
  from the logged rels {601,602}, rejects = world-A vocab scan
  {601,602,603,607,609} minus accepts = [[603],[607],[609]]).
  Predicted clause: (0,identity,[601,602]). Save the A vocab.
  Verify old routing over the A vocab scan order:
  COVOLD n=5 route=1,1,0,0,0.
- Phase 2 (drift): setup_worldB (no clearing: this is the
  drift). Scan B vocab: {701,702,707}. Three probes: rp =
  clause lo read at runtime (601); each probe observes rp
  admitted by the commitment (judgment=1, P0 protocol) but
  absent from the current world's vocab (consequence=0);
  u_invalidate(3000,1,0) x3. Predicted: dc=2, active=0,
  run=3, req=1, first_detect stays 500 (908 already set).
  Frozen COVPROBE line: rp=601 chk=1,1,0 inv=3 dc=2 active=0
  req=1.
- Phase 3 (re-log): watermark w0 = nrel; run 2 real RET
  episodes on B with rels = first two B-vocab rels (701,702)
  and objs = first obj per rel from the fact scan (721,722).
  New accepts = rels logged since w0 = {701,702}; rejects =
  (A vocab union B vocab) minus accepts =
  [[601],[602],[603],[607],[609],[707]]. u_revise(3000,1).
  Predicted: C_OLDERR_ON_NEW=4 (old clause errs on both new
  accepts and on rejects [601],[602]), new clause
  (0,identity,[701,702]), C_REV_COUNT=2 (global), req=0.
  Verify: check(701)=1, check(702)=1, check(601)=0.
  Frozen COVREV line: olderr=4 revcount=2 nclause=(0,0,701,702)
  route701=1 route702=1 route601=0.
- Frozen COVCNT line: total=6 correct=0 revcount=2
  first=500 olderr=4 fiterr=0.

## 5. Kill bars (frozen)

- K1 DIAMOND CORRECTNESS: agree=6/6 (frozen per-query answers).
- K2 EFFICIENCY: cs=944 < cg=1672.
- K3 LEARNER-NOT-RESEARCHER: (a) word-boundary grep for the 17
  identifiers in ib_learn.zag and ib_main.zag returns empty;
  (b) no diamond handler: the only link-semantics delta vs
  C422 is the multi-source apply_kind3, exercised on the S4
  chain with C422-identical behavior; (c) binding contracts
  inducted per tag with the frozen clauses of section 3, 811
  uninducted with decline; (d) same bindings produce diamond
  plans (813/814/815) and the chain plan (808).
- K4 DIAMOND EXECUTION: E0 ans=7:1,611,0,1,611,1,2
  vers=[2,3,3,5]; E1 ans=8:1,611,1,611,1,611,1,2
  vers=[2,3,3,5]; plan dumps show [0,2,1,3] topo order.
- K5 REUSE AND RE-DERIVATION: plans_loaded=1; rederive_match=1.
- K6 DECLINE: decline=1, trials=21, no plan for 810.
- K7 DETERMINISM: 3/3 byte-identical stdout; stderr empty.
- K8 TOOLCHAIN: safebin every command; `which python3` and
  `which python` return nothing; zero forbidden invocations;
  pure Zag via the pinned znc; shell only for
  znc/binary/git/assembly/byte-verification.
- K9 HYGIENE: zero em/en dash bytes in all lane docs
  (byte-verified).
- K10 B1 REVISION: S9A BINDREV line exactly as frozen in
  section 4 (olderr=2 revcount=1 nclause=(1,0,2,2) routing
  flipped; trial outcomes tr0=0 tr1=0 tr2=1 from real
  try_family calls).
- K11 B2 REVISION: S9B COVOLD/COVPROBE/COVREV/COVCNT lines
  exactly as frozen in section 4 (olderr=4 revcount=2
  nclause=(0,0,701,702) routing flipped; probes from real
  vocab scans; episodes real).
- K12 BINDING-LAYER INTEGRATION: source audit shows
  bind_fam and ret/vfy/cnt_version decide SOLELY through
  u_check on the ported contracts; no trial-count or
  coverage-membership test remains in the decision path;
  u_invalidate/u_revise are wired to the binding and coverage
  contracts (exercised in S9).

## 6. Hand derivations (frozen)

B1 (nf=2, field 0 clauses invalid wherever rejects share the
tag; induct scans p=0..10, strictly-greater width wins):
- 801: accepts [[801,0]], rejects [[801,1],[801,2]]: field-1
  p=0 (identity) gives [0,0] w=0 > -1, valid (rejects outside);
  later valid p's have w=0, no replace. Clause (1,identity,
  [0,0]).
- 802: accepts [[802,1]], rejects [[802,0],[802,2]] ->
  (1,identity,[1,1]).
- 807: accepts [[807,2]], rejects [[807,0],[807,1]] ->
  (1,identity,[2,2]).
- 811: accepts [] -> u_induct returns 0, CONTRACT_SET=0.
- S9A re-induct: accepts [[802,2]], rejects [[802,0],[802,1]]
  -> (1,identity,[2,2]) (p=0 w=0 wins; div2/mod variants
  either invalid or w=0 no-replace).
- S9A olderr: old (1,identity,[1,1]) vs new table: accept
  [802,2] errs, reject [802,1] errs -> 2.

B2 (nf=1):
- RET S1: accepts [[601],[602]], rejects [[603],[607],[609]]:
  p=0 -> [601,602] w=1 valid, wins; mod16 [9,10] and mod32
  [25,26] valid w=1, no replace. Clause
  (0,identity,[601,602]).
- VFY/CNT S1: accepts [[601],[602],[603]], rejects
  [[607],[609]]: p=0 -> [601,603] w=2 valid, wins; mod16/mod32
  w=2, no replace. Clause (0,identity,[601,603]).
- CNT S6: accepts [[701],[702]], rejects [[707]] (world-B
  vocab minus accepts): p=0 -> [701,702] w=1 wins.
- S9B phase-1: same shape as RET S1 -> (0,identity,[601,602]).
- S9B revise: accepts [[701],[702]], rejects
  [[601],[602],[603],[607],[609],[707]]: p=0 -> [701,702] w=1
  valid, wins (mod16 [13,14], mod32 [29,30] valid w=1, no
  replace). Olderr: accepts 701,702 err (2); rejects 601,602
  err (2); 603,607,609,707 ok -> 4.

## 7. Falsification criteria (frozen)

- F1: any S1-S8 frozen value (sections 3, K1-K6) differs ->
  the port changed composition behavior; the integration
  breaks composition at the binding layer. Diagnose, do not
  amend.
- F2: S9A/S9B lines differ from section 4 -> revision not
  demonstrated through the ported machinery.
- F3: audit finds a non-contract binding/coverage decision
  path, or demo counterevidence not derived from real trial /
  vocab / episode outcomes as specified -> the integration
  claim is VOID.

## 8. Verdict mapping (frozen)

- K1-K12 PASS: INTEGRATION DEMONSTRATED. B1/B2 integrate at
  the COGOPS binding layer: the composer routes bindings and
  versions through revisable contracts, gains
  revision-under-counterevidence (S9A/S9B), and loses none of
  its procedure composition ability (C433's goals still pass
  exactly). The C443 boundary stands: plans, execution, and
  step verification remain composer machinery.
- K1-K9 PASS, K10/K11 FAIL: PARTIAL. Composition preserved
  but revision not demonstrated; the port is behavior-neutral
  plumbing, not the partial win.
- K1-K6 FAIL: INTEGRATION BREAKS COMPOSITION. The contract
  layer cannot carry the binding decisions; diagnose whether
  the failure is in induct bias, check semantics, or the
  trial-to-table mapping.
- K7/K8/K9 FAIL: PROCESS-FAIL per standing governance.

## 9. Build and run plan (post prereg)

Files (prefix `ib_`), all pure Zag, in
`docs/lab/research-lead/overnight-20260928/integration_b1b2/`:
- `ib_base.zag`: byte-copy of cogops_diamond/c4_base.zag
  (cmp-verified).
- `ib_world.zag`: byte-copy of cogops_diamond/c4_world.zag
  (cmp-verified).
- `ib_module.zag`: verbatim port of the u_* ops from
  subsumption_p0/sp_module.zag MINUS u_grow (induct, check,
  invalidate, revise + helpers + sg/ss); function bodies
  diff-verified against the source.
- `ib_learn.zag`: c4_learn.zag with the section 2.2/2.3
  changes: tag directory + binding contracts, contract-based
  version selection, cov_induct + vocab_scan, contract-aware
  clear_bindings; topo/plans/execution unchanged.
- `ib_main.zag`: c4_main.zag stages S1A-S8 (BCONTRACT dumps
  replace BIND dumps) + S9A/S9B demo stages + counters line;
  S threaded through compose/learn_bindings/execute_plan/
  version selection/dumps.
- `ib_full.zag`: concatenation (exactly one `fn main`).
- `ib_build.sh`: assemble + compile with the pinned safebin
  znc (`$HOME/workspace/tnn-rsi/src/tools/toolchain/
  znc_linux_x86_64_abed8aa1`).
- Run 3x (`ib_run1/2/3.txt` + `.err`), sha256sum compare,
  stderr empty. Byte-verify: ib_base/ib_world vs c4 sources;
  ib_module function bodies vs sp_module; zero em/en dash
  bytes in docs; zero of the 17 identifiers in
  ib_learn.zag/ib_main.zag. Write REPORT.md.

Commits (explicit pathspecs, /usr/bin/git, local only, never
pushed): (1) this prereg + NAMECHECK.md alone; (2)
implementation; (3) build artifacts + runs; (4) REPORT.md.
