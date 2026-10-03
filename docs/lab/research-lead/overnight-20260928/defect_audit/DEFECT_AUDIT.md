# DEFECT AUDIT: Frozen GEN >4 MAPs Tried-Table Aliasing

Date: 2026-10-03. Worker: SUBSUMPTION-FULL.
Task: audit the swarm's completed experiments for the frozen-GEN >4 MAPs
defect found by GEN-COGOPS-UNIFY (C441), which follows GEN-REDIM (C434).
Analysis only; no code. Local only, never pushed.

## 1. The defect (precise statement)

The frozen GEN base (the `gen_generality/ref_gg_base.zag` lineage) hard-codes
a 4-MAP scratch layout in four overlapping regions (GEN-STRESS REPORT.md,
mechanism section; confirmed by the GU audit that found this defect):

1. MAP table: `mg(A,m,f)` = 776+m*40+f*4. m4's table (936..976) aliases
   GEN's counters: 936 = TRIES, 940 = success flag, 944 = ANS.
2. Second-input contract table: `m2g(A,m,f)` = 968+m*12+f*4 (4 maps,
   968..1016), overlapping m4's and m5's tables.
3. tried1: 2304+(m*64+i)*4, 4 maps x 64 x 4 bytes (2304..3328).
   m4's tried1 (3328..3584) aliases tried2's count (3328) and entries;
   m5's (3584..3840) aliases tried2 entry63 (3584), the pool count nv
   (3588), the widened flag (3592), and the visit stack; m6's
   (3840..4096) aliases the visit tail and done set; m7's (4096..)
   overflows the 4096-byte arena.
4. m4+'s m2g entries (1016+) overlap the value pool (1024+).

Consequences by registered MAP count (all empirically confirmed in
GEN-STRESS):

- nm<=4: every region clean; frozen rules execute faithfully.
- nm=5..7: SILENT cross-region aliasing. Deterministic wrong declines
  and spurious WIDENs that a casual reader could mistake for
  compositional results.
- nm>=8: arena-overflow panic on the first out-of-range tried1 access.

The canonical fix is GEN-REDIM (C434, CLEAN-REPRODUCTION-PASS): a
dynamic NM-parameterized scratch layout, byte-identical to frozen at
nm<=4, verified at NM=2,3,4,6,8. GEN-REDIM is the canonical GEN base
going forward; the frozen pre-redimensioning base is superseded for
any experiment registering more than 4 MAPs.

## 2. Audit method

For every ledgered GEN-adjacent experiment (watchdog ledger C361-C434
per COMPOSITION_SYNTHESIS.md, plus the claim ledger and git history):

1. Identified the composer machinery used (frozen GEN base vs new
   sequence composer vs contract module vs COGOPS machinery vs
   protected-ISA system).
2. Counted registered MAPs from the committed setup code
   (`map_new(A,n,...)` calls; setup census lines).
3. Grepped built sources for the frozen tried layout
   (`2304`, `3328`, `tried1`, `gen_solve`).
4. Classified: confirmed-affected (>4 MAPs on the frozen defective
   base), possibly-affected, unaffected.

## 3. Confirmed-affected experiments

Exactly one experiment ran >4 MAPs on the frozen defective base:

### GEN-STRESS S1 (nm=6), S2 (nm=6), S4 (nm=8) -- C410

- Lane: `gen_stress/`. Source: `gs_new.zag` (setup_s1, setup_s2,
  setup_s4 register m0..m5 / m0..m7).
- Ledger: C410 second assignment, GEN-STRESS BOUNDARY-FOUND ARENA-4MAP.
- What happened: K2 FAIL (S1: predicted ANS=2 TRIES=29; actual ANS=-2
  TRIES=16, 3/3 byte-identical), K3 FAIL (S2: predicted ANS=219 TRIES=48;
  actual ANS=-2 TRIES=62 with spurious WIDEN=1, 3/3 byte-identical),
  K5 FAIL (S4: predicted clean decline ANS=-2 TRIES=48; actual
  `panic: slice index out of bounds`, 3/3 identical).
- Why this is NOT a scientific-integrity incident: the verdict was
  BOUNDARY-FOUND (INFORMATIVE-FAIL). The corrupt outputs were the
  evidence for the defect characterization, not compositional results.
  The mechanism-level cause was identified in the same report and is
  exactly the defect audited here. No positive compositional claim
  rests on these runs. S3 (nm=3) and S5 (nm=4) ran on clean regions and
  PASSED (K4, K6), confirming the defect boundary at 4 MAPs.
- Remediation status: COMPLETE. GEN-REDIM (C429 exploratory,
  C434 CLEAN-REPRODUCTION-PASS canonical) re-ran the full S1-S5 battery
  on the dynamic NM layout at the same MAP counts (S1: 6/6, S2: 6/6,
  S4: 8/7) and verified each against the original stress predictions:
  S1 ANS=2 TRIES=29; S2 ANS=219 TRIES=43 per the preregistered corrected
  trace (the GEN-STRESS prereg's TRIES=48 carried four hand-derivation
  errors, corrected transparently in the GEN-REDIM prereg, binary prints
  the corrected block byte-for-byte); S3 WIDEN=1 ANS=207 TRIES=8;
  S4 ANS=-2 TRIES=48 clean decline, zero WIDEN=1 lines;
  S5 ARM ANS=-2 TRIES=2734. The stress predictions now stand on the
  canonical GEN-REDIM base.

## 4. Possibly-affected experiments

NONE with positive claims. The only >4-MAP frozen-base runs are the
GEN-STRESS S1/S2/S4 boundary runs in section 3, already remediated.

Citation-hygiene note (not a defect): any future citation of
"GEN composition behavior at 6/8 structures" must point to the
GEN-REDIM canonical results (C434: S1 ANS=2 TRIES=29, S2 ANS=219
TRIES=43, S4 ANS=-2 TRIES=48), never to the GEN-STRESS corrupted runs
(K2/K3/K5 FAILs). The GEN-STRESS corrupted outputs remain valuable
only as the defect's empirical signature.

## 5. Unaffected experiments (verified)

Each entry states MAP count, machinery, and why the defect cannot apply.

### 5a. GEN composer, <=4 MAPs on the frozen base

- **GEN-GENERALITY (C402).** Max 4 MAPs (m0..m3; setups at gg_full.zag
  lines 183-217, 280-283, 549-574). Frozen GEN handles fan-in, DAG-4,
  chain-3, partial applicability. Independently re-verified by
  GEN-REDIM C4 (rd_gbin byte-identical to frozen-regenerated baseline).
- **GEN-SUBSUMES-U (C397).** 4 MAPs (census m0..m3 in the frozen output).
  5 pipeline pairs, honest failures, fresh learner.
- **GEN-STATEFIX (C406).** Same batteries as C397 (byte-identical
  regression except the P5 fix). The tried-state reset hunk clears
  2304..3328 (256 cells) plus the tried2 count at 3328, which is exactly
  the 4-map layout; consistent with its <=4 MAP batteries.
- **COMPOSE-PAIR6-ADV diamond (C380 first assignment).** Diamond battery
  at 4 MAPs (GEN-REDIM REPORT sec 5: "diamond: 4/4"). Regress-verified
  byte-identical by GEN-STATEFIX K3 and GEN-CYCLES C6.

### 5b. New sequence composer (cycles family), <=4 MAPs

- **GEN-CYCLES (C414).** New `gc_solve` sequence machinery in
  `gc_uni.zag`: zero references to tried1/2304/3328 (grep-verified).
  Fixpoint workload registers 4 MAPs (cyc_nomain.zag lines 19-22).
  Its frozen GEN regression runs (diamond, generality) are the same
  <=4 MAP batteries as 5a.
- **CYCLES-GENERALIZE (C420), CYCLES-OSCILLATORY (C425),
  CYCLES-CONVERGENT (C428), CYCLES-FEEDBACK (C430/C432).** Built on the
  same gc sequence machinery (gc_base.zag, gc_uni.zag copied per lane;
  grep-verified zero tried-layout references). Setups register m0..m3
  (qo_setups.zag, cc_setups.zag, qf_setups.zag all max map_new(A,3,..)).

### 5c. Contract module, no tried-table machinery

- **CONTRACT-UNIFICATION (C424).** New 5-op contract module
  (induct/check/grow/invalidate/revise). Zero references to the frozen
  tried layout (grep over cu_full.zag). The grammar arm uses the module's
  `check` as admission, not the GEN tried tables.
- **SUBSUMPTION-P0 (in progress).** 5-arm battery of the frozen C424
  module vs C433 goals. sp_module byte-identical to contract_unify's u_*;
  zero tried-layout references in sp_base/sp_module/sp_full.

### 5d. Independent machinery (never touched the GEN composer)

- **COGOPS 2-way (C417), 3-way (C422), diamond (C433).** Procedure-body
  composition via trial-learned bindings and topo assembly. Zero
  gen_solve/2304/tried1 references in cc_full.zag, c3_full.zag,
  c4_full.zag.
- **COMPOSE-PAIR5 (C368), U-RETIREMENT (C413),
  DOMAIN/NODE/JOINT blindness (C398/C399/C403/C409).** U-era composer,
  not the GEN tried layout.
- **GENEXEC2 / GENEXEC2P, FHAT-COMPOSE.** Executable-program /
  protected-ISA systems; zero tried-layout references.

### 5e. >4 MAPs but never on the defective base

- **GEN-COGOPS-UNIFY (C441).** 6 MAPs (m0..m5) but the PoC was built with
  the workaround from the start: GU-GEN-DELTA 2 relocates tried1 to
  10080 (6x64) and the tried2 count/entries to 11616/11620
  (gu_gen.zag lines 4-7, 41-57; diff-audited by gu_build.sh lines 26-35).
  The PoC results rest on the relocated layout, not the defective one.
  NOT affected; no re-run needed.
- **GEN-NM10.** 11 MAPs but built on the canonical GEN-REDIM dynamic
  layout (rbase.zag, rgen_nomain.zag referenced by relative path,
  verified byte-identical to GEN-REDIM-CLEAN canonical digests, N5).
  NOT affected; no re-run needed.

## 6. Remediation summary

| Experiment | Ledger | MAPs / base | Classification | Remediation |
|---|---|---|---|---|
| GEN-STRESS S1 | C410 | 6 / frozen (defective) | confirmed-affected | DONE: re-run on GEN-REDIM, canonical C434 |
| GEN-STRESS S2 | C410 | 6 / frozen (defective) | confirmed-affected | DONE: re-run on GEN-REDIM, canonical C434 |
| GEN-STRESS S4 | C410 | 8 / frozen (defective) | confirmed-affected | DONE: re-run on GEN-REDIM, canonical C434 |
| GEN-STRESS S3, S5 | C410 | 3, 4 / frozen | unaffected (clean regions) | none needed |
| GEN-COGOPS-UNIFY PoC | C441 | 6 / relocated tried tables | unaffected (workaround in place) | none needed |
| GEN-GENERALITY | C402 | <=4 / frozen | unaffected | none needed |
| GEN-SUBSUMES-U | C397 | 4 / frozen | unaffected | none needed |
| GEN-STATEFIX | C406 | 4 / frozen (+reset) | unaffected | none needed |
| GEN-CYCLES + 4 follow-ons | C414, C420, C425, C428, C430, C432 | <=4 / sequence composer | unaffected | none needed |
| CONTRACT-UNIFICATION | C424 | n/a / contract module | unaffected | none needed |
| COGOPS 2-way/3-way/diamond | C417, C422, C433 | n/a / procedure bodies | unaffected | none needed |
| GEN-NM10 | (post-C434) | 11 / GEN-REDIM | unaffected | none needed |

No experiment requires re-running beyond the GEN-REDIM re-runs that
already happened (C429/C434). No positive compositional claim is
invalidated by this defect.

## 7. Recommendations

1. **Canonical base rule.** The frozen pre-redimensioning GEN base is
   superseded for all future work registering more than 4 MAPs;
   GEN-REDIM (C434) is the canonical GEN base. GEN-STRESS REPORT.md
   already carries the standing warning that the frozen artifact's
   addressable MAP count is 4; this audit confirms no live claim
   violates it.
2. **Citation rule.** Cite 6/8-structure GEN composition behavior only
   from GEN-REDIM (C434), never from the GEN-STRESS K2/K3/K5 corrupted
   runs.
3. **Prereg rule for future batteries.** Any future GEN battery
   registering more than 4 MAPs must state the base (GEN-REDIM) and the
   NM invariant (world_new_nm(nm) >= defined MAPs) in the prereg.
4. **No further action.** The defect found no un-remediated victim.
   GEN-COGOPS-UNIFY's full test (PREREG_DESIGN.md K10/U10) inherits the
   relocated tried layout via GU-GEN-DELTA 2; no change needed.
