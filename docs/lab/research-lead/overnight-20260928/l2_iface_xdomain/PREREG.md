# PREREG: L2 IFACE-XDOMAIN (learner-decided interface adaptation of a learned procedure, cross-domain)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_iface_xdomain/` only.
Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.
Parent mandate: L2 ADAPTIVE REUSE is top priority. The L2 operation matrix
(SUBSTITUTE, TRUNCATE, EXTEND, SPECIALIZE) is validated cross-domain.
This lane pushes INTERFACE-ADAPT across domains as a STANDALONE operation:
take a learned procedure X and adapt ONLY its interface (caller-arg to
callee-param binding, arity bridging for a decoy/missing argument,
entry-relation name binding) WITHOUT changing X's core logic or record,
for use in a different domain.

Predecessors: `l2_substitute_xdomain/` (adapter idiom: entry/fold
discovery, execution verification, provenance edges) and
`l2_specialize_xdomain/` (learner-decided parameters via trial over
inventory-derived candidates, generic counters per its Amendment 1).
The operation under test here is different: SPECIALIZE compiled a new
MAP with FIXED rels/params; INTERFACE-ADAPT creates an interface-adapter
MAP mA carrying ZERO rels (rlen=0) that only binds the call boundary,
while every execution replays the ORIGINAL procedure mX through the
adapter. X's 32-byte record is snapshotted at teach and byte-compared
at arm close (K5).

## 1. What is being tested

Whether a learner holding (X) a GENERAL parametric ADD MAP mX learned in
an arithmetic episode (descriptor: entry=18, fold rels 5/6, nf=2
parametric, valrel=2, param=1) and (Y) a planning-cost target domain B
whose caller issues ADD queries with a DIFFERENT interface, (1) FAILS to
apply mX's home interface verbatim in B (naive attempt: entry rel 18
absent in B, fold rels 5/6 absent, third arg is a plan tag not an
expected total), (2) DERIVES the interface mapping by trial over
structural candidates: s/t bind to the first two caller args in some
order (ps in {0,1}), the third caller arg either binds v or is DROPPED
(pv in {2,255}), entry-relation candidates are the distinct non-VAL
rels of the bound start node's outgoing facts in fid order ([9,17]),
each candidate verified by execution (entry walk + terminal + VAL +
addend-VAL arity), (3) PROMOTES an adapter MAP mA (id 1, rlen=0,
d=(17,0,1,255,2,2), reason=src id) with type-17 adapted-from provenance
to mX, and (4) answers later B ADD queries through mA by replaying mX's
core (mX's nf/valrel, generically discovered fold pair) with the bound
interface, while mX's own record stays byte-identical and mX still
serves its home domain.

Concrete scenario (all ids frozen):

Domain A (arithmetic, home), facts:
  0:(100,18,60) 1:(60,5,61) 2:(61,6,62) 3:(62,5,63) 4:(63,6,64)
  5:(61,2,3) 6:(63,2,4) 7:(64,2,7)
  mX (id 0): dom=A(1), cap=ADD(1), relseq [18,5,6,5,6],
  facts [0,1,2,3,4], start 100, end 64.
  Descriptor (extracted generically at teach): entry=18, r1=5, r2=6,
  nf=2, valrel=2 (first live fid with sub==64), param=1.

Domain B (planning cost), facts:
  8:(50,9,71) 9:(71,15,72) 10:(72,16,73) 11:(73,2,1)
      [decoy entry rel 9: 1-fold chain, terminal 73]
  12:(50,17,74) 13:(74,15,75) 14:(75,16,76) 15:(76,15,77)
  16:(77,16,78) 17:(75,2,20) 18:(77,2,30) 19:(78,2,50)
      [true entry rel 17: 2-fold chain, terminal 78, total 50]
  NF=20.

Queries (driver-issued, no MAP id ever passed; third arg a3):
  QA:  (100,64,7, cap=ADD, dom=A) -> home via mX
  Q2:  (50,78,99, cap=ADD, dom=B) -> FULL: naive fails;
         adapt promotes mA; delivers via mA.
         ABLATE-X (mX dead): naive nosrc; adapt no-source; -2
  Q2B: (50,78,99, cap=ADD, dom=B) -> FULL: via mA, no re-adapt
  Q2C: (50,78,7,  cap=ADD, dom=B) -> FULL: via mA with a
         DIFFERENT decoy third arg (interface decision does not
         depend on the decoy value)
  Q2D: (50,73,99, cap=ADD, dom=B) -> FULL: mA must NOT fire
         (adapted interface walks entry 17 to terminal 78, never
         73; genuine adapted interface, no spurious accept)

## 2. Frozen learner machinery (disclosed)

Standalone pure-Zag learner (ia_learner.zag) + world side
(ia_world.zag: fact table + mX teaching) + experiment side
(ia_driver.zag: two arms, in-Zag bar evaluation, main).
The frozen TNN core is not used. Unfrozen only; no frozen source touched.

State: one u8 buffer (2048). Header: 0 NF, 1 NM, 2 NE,
3 NAIVE_OK (0/1), 4 IN_ADAPT, 5 ADAPT_ENTERED, 6 SRC_ID (255=none),
7 AD_PS (255=none), 8 AD_PT (255=none), 9 AD_PV (255=none;
decided: 2=bind arg3, 255=dropped), 10 AD_ENTRY (255=none),
11 TRIAL_FAIL_N, 12 TRIAL_TOTAL, 13 ADAPTED.
Facts: 64 x 8 bytes at 16..527 [sub,rel,obj,live,0,0,0,0].
MAPs: 16 x 32 bytes at 528..1039 [tag=20,live,start,end,rlen,flen,
reason,pad, rels x8 @+8, facts x8 @+16, dom @+24, cap @+25,
d_entry @+26, d_r1 @+27, d_r2 @+28, d_nf @+29, d_valrel @+30,
d_param @+31]. Edges: 64 x 4 bytes at 1040..1295 [from,to,type,pad].
S_SEARCH i32 @1296, S_EXEC i32 @1300, LAST_VAL i32 @1304,
LAST_TERM i32 @1308, LAST_VIA i32 @1312.
Scratch: addends 8 x i32 @1472, na i32 @1568, acc_er u8 @1580,
entry-cand rels 8 x u8 @1584, ncand u8 @1592, MX_SNAP 32 x u8
@1600..1631.

Edge-type semantics: type 17 = interface-adapted-from (mA -> mX).
No other edge type may appear (F-EDGE-NEW).

Scan primitives (all fid-ascending over live facts, S+=1 per fid
examined; MAP loops S+=1 per header examined):
- scan1(sub,rel): first live fid with sub==sub, rel==rel.
- scan_nv(sub,valrel): first live fid with sub==sub, rel!=valrel
  (fold-relation discovery; generic machinery).
- scan_val(node,valrel): first live fid with rel==valrel,
  sub==node -> obj (VAL read).

Generic operations (frozen, relation-agnostic, MAP-agnostic,
domain-agnostic; no world/relation/domain/value literal anywhere
in ia_learner.zag):
- f_teach(sub,rel,obj): observe a world fact. No S ticks.
- m_teach(rs,rl,fs,fl,start,end,dom,cap): learn a MAP. If
  cap==ADD, extract the interface descriptor generically:
  d_entry=rels[0], d_r1=rels[1], d_r2=rels[2], require
  rels[1..] to alternate (r1,r2) with (rlen-1) even and >= 2,
  d_nf=(rlen-1)/2, d_valrel = rel of the first live fact
  (fid order) with sub==end, d_param=1.
- mx_snap(): copy mX's 32 record bytes to @1600 (driver-called
  right after teach_maps).
- home_exec(mid,s,t,v): replay of a parametric MAP in its home
  domain: walk d_entry then d_nf folds of (d_r1,d_r2) via
  scan1; terminal==t and (v<0 or scan_val(t)==v) required.
  S_EXEC+=1.
- naive_exec(sm,s,t,v): verbatim home-descriptor application in
  the target domain (the direct-application probe for K2):
  entry=scan1(s,d_entry); exactly d_nf folds of (d_r1,d_r2);
  terminal==t; v>=0 -> scan_val(t)==v. Search only (no E tick).
  Returns 1/0; NAIVE_OK recorded; trace IA-NAIVE-FAIL sm=<id>
  or IA-NAIVE-NOSRC.
- ia_foldwalk(u,valrel,nf): fold-1 rel-pair discovered via
  scan_nv (generic), folds 2..nf via scan1; addend nodes
  recorded @1472/na. Returns terminal or -1.
- ia_check_addends(valrel): every recorded addend has a VAL
  (scan_val hit). The uniform arity check.
- ia_trial(sm,psv,ptv,pvv,er): ONE interface candidate.
  e=scan1(psv,er); term=ia_foldwalk; codes: 1=ACCEPT,
  0=FAIL-ENTRY, -1=FAIL-WALK, -2=FAIL-TERM, -3=FAIL-VAL,
  -4=FAIL-ARITY. acc_er=er on accept. Search only.
- build_entry_cands(psv,valrel): distinct rels (fid order) of
  live facts with sub==psv and rel!=valrel -> @1584/@1592.
  valrel comes from sm's descriptor (data, not a literal).
- ia_promote(sm,s,ptv,cap,dom): new MAP mA (next id):
  rlen=0, flen=0 (NO rels copied: the core is not duplicated),
  start=s, end=ptv, reason=sm, dom, cap,
  d=(AD_ENTRY,AD_PS,AD_PT,AD_PV,sm.valrel,2). Edge t17 mA->sm.
  Trace IA-PROMOTE id=<n>.
- ia_exec(ma,s,t,a3): tick_exec. sm=reason byte. Bind
  psv/ptv/pvv from the adapter descriptor via qarg
  (pslot->caller arg; pvv=-1 when pvslot==255, i.e. dropped).
  Entry loop over live facts with sub==psv AND rel==d_entry
  (fid order); per entry: ia_foldwalk with sm's nf, terminal,
  pvv, addend checks. First pass delivers
  (val = pvv>=0 ? pvv : scan_val(terminal)). Else -2.
- ia_adapt(s,t,a3,cap,dom): IN_ADAPT=1, ADAPT_ENTERED=1.
  1. sm=find_gen(cap): first live MAP (id order) with
     cap==qcap and d_param==1. None -> trace
     IA-ADAPT-FAIL reason=no-source, ANS -2.
  2. SRC_ID=sm; trace IA-SRC id=<sm>.
  3. for ps in {0,1} (structural arg slots; pt=1-ps):
     entry cands=build_entry_cands(qarg(ps)); trace
     IA-CANDIDATES <rels>; for er in cands: for pvi in
     {0,1} (pv=2 bind / pv=255 drop; pvv=a3 or -1):
     TRIAL_TOTAL++; r=ia_trial(...); trace IA-TRIAL
     ps=<ps> pt=<pt> pv=<pv> er=<er> <reason>; on
     r==1: record AD_PS/AD_PT/AD_PV/AD_ENTRY (data from the
     trial, never literals in logic), ADAPTED=1, trace
     IA-ACCEPT ..., promote, ia_exec, stop all loops.
     else TRIAL_FAIL_N++.
  4. no candidate accepts -> ANS -2.
- ia_query(s,t,a3,cap,dom): reset S/E; pipeline over live MAPs
  in id order: start==s and dom==qdom and cap==qcap ->
  d_param==1: home_exec; d_param==2: ia_exec; first success
  delivers. Else: naive probe (find_gen -> naive_exec), then
  ia_adapt (only if naive did not answer).

Candidate-slot values {0,1,2,255} are STRUCTURAL (caller-arg
positions; 255=dropped), never world values. The learner names
no relation, MAP, domain, domain pair, fact, or parameter value.

## 3. Frozen cost-counting rules

- S_SEARCH += 1 per fact id examined in any learner scan loop.
- S_SEARCH += 1 per MAP header examined in any learner MAP scan loop.
- S_EXEC += 1 per home_exec / ia_exec entry.
- naive_exec, ia_trial, build_entry_cands: search only.
- Teaching (f_teach/m_teach/mx_snap) costs nothing.
- S/E reset at each ia_query entry; driver prints per-query S/E/ANS.

## 4. Frozen arms and hand-derived expectations

Scan-cost atoms (fid-ascending, all facts live, NF=20):
scan1: (100,18)=1 (60,5)=2 (61,6)=3 (62,5)=4 (63,6)=5
(50,18)=20 MISS (50,9)=9 (50,17)=13 (71,15)=10 (72,16)=11
(73,15)=20 MISS (74,15)=14 (75,16)=15 (76,15)=16 (77,16)=17.
scan_nv: 60->2 (5,61); 61->3 (6,62); 71->10 (15,72);
72->11 (16,73); 74->14 (15,75); 75->15 (16,76).
scan_val: 64->8 (v7); 75->18 (v20); 77->19 (v30); 78->20 (v50).

- ARM-FULL:
  QA: pipeline headers 1 + home_exec (1+2+3+4+5) + VAL 8 = 24,
    E=1, ANS 64,7 via 0.
  Q2: pipeline headers 1; naive: find_gen 1 + scan1(50,18)=20
    MISS -> IA-NAIVE-FAIL sm=0, NAIVE_OK=0; adapt: find_gen 1
    (sm=0); ps=0: entry cands scan 20 -> [9,17], trace
    IA-CANDIDATES 9,17.
    T1 (ps=0,pt=1,pv=2,er=9): 9+10+11+20=50 FAIL-WALK.
    T2 (ps=0,pt=1,pv=255,er=9): 50 FAIL-WALK.
    T3 (ps=0,pt=1,pv=2,er=17): 13+14+15+16+17=77 walk,
      term 78 OK, VAL 20 -> 50 != 99 FAIL-VAL. =95.
    T4 (ps=0,pt=1,pv=255,er=17): 77 + VALs 18+19 = 114
      ACCEPT. trace IA-ACCEPT ps=0 pt=1 pv=255 er=17.
    Promote mA id 1: rlen=0, d=(17,0,1,255,2,2), reason=0;
      t17 1->0 (NE=1); trace IA-PROMOTE id=1.
    ia_exec: entry loop 13 + walk 14+15+16+17 + VAL 20 +
      addends 18+19 = 132, E=1.
    Q2 frozen: S=1+1+20+1+20+50+50+95+114+132=484, E=1,
      ANS term=78 val=50 via=1, TRIAL_TOTAL=4, TRIAL_FAIL_N=3,
      AD=(0,1,255,17), NM=2.
  Q2B: pipeline headers 2 (id0 skip, id1 mA) + ia_exec 132 =
    134, E=1, ANS 78,50 via 1, no re-adapt.
  Q2C: as Q2B: 134, E=1, ANS 78,50 via 1 (a3=7 ignored;
    pv dropped, so the decoy value cannot matter).
  Q2D: pipeline headers 2 + ia_exec: entry loop 20 (all fids;
    hit at 12 walks to 78 != 73) + walk 14+15+16+17 = 84,
    E=1, ANS -2,-2 via -1.
- ARM-ABLATE-X (mX live=0 right after teach+snap, before QA):
  QA: pipeline headers 1 (id0 dead); naive: find_gen 1 -> none,
    IA-NAIVE-NOSRC; adapt: find_gen 1 -> none,
    IA-ADAPT-FAIL reason=no-source. S=3, E=0, ANS -2,-2 via -1.
  Q2: same as QA: S=3, E=0, ANS -2,-2 via -1.
    NM=1, NE=0, no mA, TRIAL_TOTAL=0.

## 5. Kill bars (frozen)

- K1 (source X exists and works in home domain): in-Zag (FULL):
  qa_via==0 AND qa_term==64 AND qa_val==7. Shell: output line
  number of `Q QA` < `Q Q2` in run1.
- K2 (direct application in target domain fails: interface
  mismatch): in-Zag (FULL): naive_ok==0. Shell (verbatim grep
  -F on run1): `IA-NAIVE-FAIL sm=0`. mX's home interface
  (entry 18, folds 5/6, v-check) matches nothing in B.
- K3 (learner derives the interface mapping; not
  researcher-provided): in-Zag (FULL): trial_total==4 AND
  trial_fail_n==3 AND ad_ps==0 AND ad_pt==1 AND ad_pv==255
  AND ad_entry==17. The learner tried the decoy entry rel 9
  (FAIL-WALK), tried binding the decoy third arg as v
  (FAIL-VAL on er=17), and fixed (ps=0,pt=1,pv=dropped,
  er=17) only on execution-verification success. Shell
  (verbatim grep -F): `IA-CANDIDATES 9,17`,
  `IA-TRIAL ps=0 pt=1 pv=2 er=17 FAIL-VAL`,
  `IA-ACCEPT ps=0 pt=1 pv=255 er=17`.
  Candidate slots are structural arg positions; entry rels come
  from the learner's own fact scan; the choice is by trial,
  never a researcher-supplied value.
- K4 (adapted interface enables X to work in target domain):
  in-Zag (FULL): q2_via==1 AND q2_term==78 AND q2_val==50.
- K5 (core logic of X unchanged; only the interface adapted):
  in-Zag (FULL): snap_ok==1 (mX's 32 record bytes identical
  teach->close) AND ma_rlen==0 (adapter carries no rels; the
  core is never duplicated or rewritten) AND qa_via==0 (mX
  still serves home). Every B execution replays mX's own
  descriptor (nf, valrel) through the adapter.
- K6 (determinism): 3/3 runs byte-identical (sha256 equal).
- K7 (no domain-pair template): 8 frozen grep patterns return
  0 hits on ia_learner.zag (section 6).
- K8 (ablation: no X fails): in-Zag (ABLATE-X): q2_term==-2
  AND q2_via==-1 AND nm==1 AND ne==0 AND qa_term==-2 (no mA
  promoted, no provenance; without X there is nothing to
  adapt).

Verdict L2-IFACE-XDOMAIN-PASS iff K1-K8 all PASS, no falsifier
fires, F-COUNT silent.

## 6. Frozen K7 grep audit spec (run on ia_learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `50,17,74` (B entry fact literal; world data stays out)
2. `74,15,75` (B chain fact literal)
3. `99` (decoy third-arg value; driver/query-side only)
4. `78,50` (B answer literal)
5. `_MODE` (zero modes)
6. `bridge` (case-insensitive; no bridge handlers)
7. `python` (case-insensitive; pure Zag)
8. `as *i32` (the pinned-znc miscompile pattern; u8 cells
   + get32/set32 only)

## 7. Frozen falsifiers

- F-NAIVE: FULL naive_ok != 0 (direct application must fail).
- F-NOADAPT: FULL Q2 via != 1.
- F-BIND: ad_ps != 0 or ad_pt != 1 or ad_pv != 255 or
  ad_entry != 17.
- F-TRIAL: trial_total != 4 or trial_fail_n != 3 (the learner
  did not genuinely run the 4-trial decision).
- F-CORE: snap_ok != 1 or ma_rlen != 0.
- F-Q2B: FULL Q2B via != 1 or term/val != 78/50.
- F-Q2C: FULL Q2C via != 1 or term/val != 78/50.
- F-Q2D: FULL Q2D via != -1 (spurious fire).
- F-ABLX: ABLATE-X Q2 ans != -2 or NM != 1 or NE != 0.
- F-EDGE-NEW: any edge with type != 17; FULL t17-count != 1.
- F-COUNT: any frozen per-query S or E != frozen value
  (a pure arithmetic slip in this prereg's hand derivation
  may be transparently amended pre-verdict; an algorithmic
  counting change may not).
- F-AUDIT / F-NONDET / F-PYTHON: as in prior waves; any
  fires voids the build.

## 8. Determinism spec

No RNG. MAP-id order, fid-ascending scans, first-match rules,
fixed candidate order (ps 0..1, entry rels fid order, pv bind
then drop) everywhere. Output via one preallocated buffer and
a single raw-syscall write loop (the pinned-znc stdout
workaround). 3/3 byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The interface-adapt operator, candidate-slot structure
  (s/t bind to the first two caller args in some order; third
  arg binds v or is dropped), entry-candidate rule (distinct
  non-VAL rels of the bound start's facts), fold-pair
  discovery (scan_nv), addend-VAL arity check, descriptor
  extraction, edge-type convention, and cost counters are
  researcher-supplied generic machinery, frozen here. None
  names a relation, MAP, domain, domain pair, fact, or
  parameter value. The L2 claim is narrow: the learner derives
  the call-boundary mapping (arg slots, decoy drop, entry-rel
  name) by execution-verified trial, promotes a zero-rel
  adapter MAP with adapted-from provenance, reuses it for
  later target queries, and leaves the source procedure's
  record byte-identical; the ablation without X fails outright.
- One world family (arithmetic ADD x plan-cost aggregation).
  No generality claim beyond the two arms. The world (fact
  table, decoy entry rel 9, decoy third arg 99) is
  builder-designed, not adversary-designed. Sealed-adversary
  generality is open future work.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types beyond the
  disclosed t17, 0 new opcodes, 0 new semantic cases. Pure Zag,
  safebin toolchain, zero forbidden executables.
- No em/en dashes in loop documentation. Paper untouched.
  Nothing pushed. Commits local with explicit pathspec.
- Unfrozen only: no frozen source touched. The frozen TNN
  core is not used here; this is a standalone
  learner-mechanism experiment in the chain family.
