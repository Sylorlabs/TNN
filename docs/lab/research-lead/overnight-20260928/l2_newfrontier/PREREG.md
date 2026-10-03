# PREREG: L2 COMBINE-XDOMAIN (cross-domain combine, learner-chosen binding)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_newfrontier/` only.
Worker: L2-NEWFRONTIER subagent (depth 2/2), 2026-10-02.
Parent mandate: push to a NEW L2 frontier beyond the completed
adaptive-reuse matrix (SUBSTITUTE/TRUNCATE/EXTEND/SPECIALIZE,
all BUILD-PASS). This wave tests L2-COMBINE-XDOMAIN: the learner
combines TWO old structures (not merely adapts one) to solve a
cross-domain problem, choosing the source pair and the
combination binding itself. Parent kill bars K1-K8 govern.

## 1. What is being tested

Whether a learner holding (X) an arithmetic aggregation MAP mA
learned in an arithmetic episode (entry + 3 fold pairs, 7 hops)
and (Y) a planning ROUTE MAP mB0 learned in a planning episode,
when asked for an aggregation in the planning domain whose
grounding chain is a ROUTE segment followed by a FOLD segment
(neither X alone nor Y alone grounds it), (1) runs its native
pipeline and records that no single learned MAP reaches the
query terminal, (2) searches its MAP inventory by capability
signature across domains, selecting one AGG source (X) and
collecting partner-capability sources (examining and rejecting
the distractor mD, a ROUTE MAP whose relation pattern cannot
ground from the query start), (3) enumerates (partner-source,
binding) combinations in a fixed generic order and commits to
the FIRST combination whose full grounding executes to the query
terminal with the required value, where binding b=1 means
AGG-head/partner-tail and binding b=2 means partner-head/AGG-
tail, (4) builds the combined Z as head-segment facts+rels
followed by tail-segment facts+rels, verifies Z by execution,
promotes Z with derived-from (type-16) provenance to BOTH
sources, and (5) answers the re-asked query through Z with no
re-combination. The winning (partner-source, binding) pair
(mB0, b=2) is chosen by the learner's verification loop, never
passed by the driver: the driver issues Q2 as (start, terminal,
value, cap, dom) with no MAP id, no source pair, no binding,
and no segment information.

Concrete scenario (all ids frozen):

Domain A (arithmetic aggregation), facts:
  0:(40,5,30) 1:(30,6,41) 2:(41,5,31) 3:(31,6,42)
  4:(42,5,32) 5:(32,6,43)
  6:(43,2,11) 7:(100,18,40)
  rel 5/6 = fold pair, rel 18 = entry, rel 2 = VAL.
  mA (id 1): dom=A(1), cap=AGG(1),
  relseq [18,5,6,5,6,5,6], facts [7,0,1,2,3,4,5],
  start 100, end 43.
  Descriptor (extracted generically at teach time, never
  hardcoded): entry=18, r1=5, r2=6, nf=3, valrel=2.
  Home query QA (100,43,11,AGG,A): walk
  100-18->40-5->30-6->41-5->31-6->42-5->32-6->43,
  VAL(43)=11.

Domain B (planning), facts:
  8:(90,7,91) 9:(91,7,92) 10:(92,17,80) 11:(80,15,81)
  12:(81,16,82) 13:(82,15,83) 14:(83,16,84) 15:(84,15,85)
  16:(85,16,86) 17:(86,2,42)
  rel 15/16 = fold pair, rel 17 = entry, rel 2 = VAL,
  rel 7 = route.
  mB0 (id 2): dom=B(2), cap=ROUTE(2), relseq [7,7],
  facts [8,9], start 90, end 92.
  mD (id 0, distractor): dom=A(1), cap=ROUTE(2), relseq [6],
  facts [1], start 30, end 41. Taught FIRST so it sorts
  before mA and mB0; the partner-source collection must
  examine it and the verification loop must reject it (its
  strict rel-6 walk from 90 finds no hop).

Queries (driver-issued, no MAP id, no source pair, no binding):
  QA:  (100,43,11, cap=AGG, dom=A) -> via mA (X works at home)
  QB:  (90,92,-1, cap=ROUTE, dom=B) -> via mB0 (Y works at home)
  Q2:  (90,86,42, cap=AGG, dom=B)  -> pipeline fails (mA: no
         rel-18 fact from 90; mB0: reaches 92, not 86; mD: no
         rel-6 fact from 90); COMBINE builds Z from (mB0, b=2).
  Q2B: (90,86,42, cap=AGG, dom=B)  -> re-asked; must go via Z
         with no combine phase (persistence + reuse).

Z (built by the learner, id 3): relseq
[7,7,17,15,16,15,16,15,16], facts
[8,9,10,11,12,13,14,15,16], start 90, end 86, dom=B,
cap=AGG, descriptor (0,0,0,0,2) (combined MAPs carry no
entry-fold descriptor; d_valrel is copied generically from
the AGG source). Walk:
90-7->91-7->92-17->80-15->81-16->82-15->83-16->84
-15->85-16->86. Terminal VAL 42.

The learner's verification loop (fixed generic order):
partner sources in MAP-id order [0, 2]; for each, binding
b=1 (AGG-head, partner-tail) then b=2 (partner-head,
AGG-tail). Attempt outcomes in this world:
  (mD, b=1): AGG-head from 90: entry (90,7,91), fold rels
    discovered s1=7, s2=17, fold 2 needs rel 7 from 80:
    (80,15,81) mismatches -> FAIL.
  (mD, b=2): partner-head strict rel-6 walk from 90: no
    live (90,6,?) fact -> FAIL.
  (mB0, b=1): AGG-head fails identically (route-source
    independent) -> FAIL.
  (mB0, b=2): partner-head rel-[7,7] walk 90->91->92;
    AGG-tail from 92: entry (92,17,80), fold rels s1=15,
    s2=16 discovered at runtime, 3 folds to 86,
    VAL(86)=42 -> VERIFY-OK. Committed.
The order (query-capability-led binding first, partner
sources in id order) is fixed generic policy, not tuned to
the answer: which combination verifies is decided at
runtime by execution against world facts. The ABLATE-B arm
shows the same enumeration verifying nothing when mB0 is
retired, so position in the order does not decide.

## 2. Frozen learner machinery (disclosed)

Standalone pure-Zag learner (learner.zag, cb_ prefix, CB-
trace tags) + environment side (world.zag: 18-fact table) +
experiment side (driver.zag: teaching, five arms, in-Zag bar
evaluation). The frozen TNN core is not used. Unfrozen only;
no frozen source touched.

State: one u8 buffer. Offsets: 0 NF, 1 NM, 2 NE,
3 COMBINE_ON (driver-set causal-control flag, never written
by the learner), 4 NN, 5 unused, 6 STALE_MAP, 7 STALE_HOP,
8 STALE_FACT, 9 LAST_VIA, 10 unused, 11 IN_CB, 12 CB_ENTERED.
Facts: 38 x 8 bytes at 16..319 [sub,rel,obj,live,0,0,0,0].
MAPs: 16 x 40 bytes at 320..959 [tag=20,live,start,end,rlen,
flen,reason,pad, rels x12 @+8, facts x12 @+20, dom @+32,
cap @+33, d_entry @+34, d_r1 @+35, d_r2 @+36, d_nf @+37,
d_valrel @+38, pad @+39].
Edges: 64 x 4 bytes at 960..1215 [from,to,type,pad].
Answer nodes: 8 x 4 bytes at 1216..1247 [via,0,0,0].
Stats: SEARCH i32 @1248, EXEC i32 @1252, A_SEARCH i32 @1256,
A_EXEC i32 @1260. LAST_VAL i32 @1264, AGG_SRC i32 @1268,
ROUTE_SRC i32 @1272, BINDING i32 @1276, BIND_DECIDED i32
@1280, BIND_TRIES i32 @1284 (binding attempts made),
PIPE_HIT i32 @1288 (1 if the pipeline delivered), LAST_TERM
i32 @1292. Scratch at 1296+.

Edge-type semantics (reused, zero new types):
- type 16: derived-from. At Z promotion: 3->1 AND 3->2
  (Z is derived from BOTH sources; dual provenance is the
  white-box proof of combination).
- type 14 (LINK14): answer-node -> delivering MAP on deliver.
- No other edge types may appear.

Generic operations (frozen, relation-agnostic, MAP-agnostic,
domain-agnostic; no capability literal except comparison
against the query's own cap):
- f_teach(sub,rel,obj): observe a world fact.
- m_teach(rs,rl,fs,fl,start,end,dom,cap): learn a MAP (facts
  must be live and rel-matching; rl,fl <= 12). If cap==AGG,
  extract the interface descriptor generically: d_entry=
  rels[0], d_r1=rels[1], d_r2=rels[2], require rels[1..] to
  alternate (r1,r2) with (rlen-1) even and >= 2, d_nf=
  (rlen-1)/2, d_valrel = rel of the first live fact (fid
  order) with sub==end. No rel literal anywhere in this
  procedure.
- m_exec / chain_exec: hop walk with licensing checks.
- ex_find_sub_skip / ex_find_subrel / ex_valof: counted
  scans (frozen counting rules, section 3).
- ex_foldwalk(st,u,k,vrel,ff): from entry node u, walk k
  alternating folds. Fold 1 discovers (s1,s2) as rels of the
  first live facts with sub==u then sub==a0 (skipping
  vrel-annotated facts); folds 2..k require rel==s1 /
  rel==s2. Fills ff[0..2k) fact ids. Returns 0 on fail,
  else s1 + s2*256 + term*65536.
- cb_agg_seg(st,ob,atp,s,k,vrel,final,t,v,tr,tf): entry
  scan over fids ascending (first live fact with sub==s),
  then ex_foldwalk with k folds and runtime rel discovery.
  If final==0 (midpoint segment): shape success suffices.
  If final==1 (terminal segment): require term==t AND
  VAL(term,vrel)==v. Records segment rels into tr and fact
  ids into tf. Returns the foldwalk pack or 0. Prints
  CB-ENTRY-CAND lines.
- cb_route_seg(st,s,rsrc,hr,hf): strict walk over the
  partner source's stored relseq rels from s (a missing hop
  fails the segment; this is what rejects mD). Records hop
  rels into hr and fact ids into hf. Returns the head
  terminal or -1.
- cb_combine(st,ob,atp,s,t,v,qdom,qcap,agg_src,
  combine_on): partner-source collection (single id-order
  header pass; the first distinct live cap != qcap becomes
  the partner cap; all live MAPs with that cap are partner
  candidates), then the (partner-source, binding)
  enumeration of section 1. On the first verifying
  combination: BIND_DECIDED=1 (set ONLY in this branch),
  build Z (head rels/fids followed by tail rels/fids),
  CB-ZBUILD print, verify by chain_exec (must reach t),
  CB-VERIFY, promote Z via map_create with descriptor
  (0,0,0,0,agg_vrel) and cap=qcap dom=qdom, e_add(Z,
  agg_src,16), e_add(Z,rsrc,16), CB-PROMOTE, deliver
  through Z. The enumeration stops at the first verifying
  combination.
- ex_query(s,t,v,cap,dom,combine_on): pipeline over live
  MAPs in id order from s; first terminal==t delivers
  (value read through the MAP's stored d_valrel; skipped
  when 0) and sets PIPE_HIT=1. Else combine phase (IN_CB=1,
  A_* reset, CB_ENTERED=1): CB-QUERY print;
  CB-PIPELINE-FAIL; AGG-source search: first live MAP (id
  order) with cap==qcap, printing CB-ASEARCH id/cap
  SKIP/MATCH; partner collection printing CB-RSEARCH
  id/cap SKIP/PCAP; CB-SRC-AGG with the AGG descriptor;
  then cb_combine. If combine_on==0 the enumeration is
  skipped (searches still counted, informational). Without
  a verifying combination the query fails with ans=-2.

## 3. Frozen cost-counting rules

- A_SEARCH += 1 per fact id examined in any learner scan
  loop (entry scan, fold rel-match scans, VAL scans,
  partner-walk hop scans).
- A_SEARCH += 1 per MAP header examined in any learner MAP
  scan loop (AGG search, partner collection). The partner
  cap is the first distinct live non-query cap met in that
  same pass; no separate cap-code loop is counted.
- A_EXEC += 1 per m_exec/chain_exec call while IN_CB==1.
- A_SEARCH/A_EXEC reset at combine-phase entry; IN_CB=0
  outside the combine phase. Global SEARCH/EXEC count
  always (informational).

## 4. Frozen arms and hand-derived expectations

Phase 0 (all arms except FRESH): teach facts 0..17; m_teach
mD(0), mA(1), mB0(2). QA -> term 43 val 11 via 1. QB ->
term 92 val -1 via 2.

- ARM-FULL (combine_on=1): Q2. Pipeline: mD/mA fail from
  90, mB0 -> 92 != 86; PIPE_HIT=0; CB-PIPELINE-FAIL.
  Combine phase:
  AGG search: id0 SKIP (cap 2), id1 MATCH (cap 1) (A=2);
    trace CB-ASEARCH id=0 cap=2 SKIP / id=1 cap=1 MATCH.
  partner collection: id0 PCAP (first non-query cap 2),
    id1 SKIP, id2 PCAP (A=3).
  CB-SRC-AGG id=1 entry=18 r1=5 r2=6 nf=3 valrel=2
    (descriptor read from state).
  (mD, b=1): CB-SRC-ROUTE id=0; AGG-head from 90:
    entry scan fids 0..8 (A=9): fid 8 (90,7,91): re=7,
    u=91; foldwalk: f1 sub==91 skip rel 2: 0..9=10
    (s1=7); f2 sub==92: 0..10=11 (s2=17); fold 2 needs
    rel 7 from 80: 0..17=18 FAIL. (48)
    trace CB-ENTRY-CAND r=7 u=91 FAIL-SHAPE /
    CB-BIND b=1 FAIL. BIND_TRIES=1.
  (mD, b=2): partner-head strict rel-[6] walk from 90:
    hop scan 0..17=18, no (90,6,?) fact -> FAIL. (18)
    trace CB-BIND b=2 FAIL. BIND_TRIES=2.
  (mB0, b=1): CB-SRC-ROUTE id=2; AGG-head fails
    identically (48). trace CB-BIND b=1 FAIL.
    BIND_TRIES=3.
  (mB0, b=2): partner-head rel-[7,7] walk: hop1
    0..8=9 (->91, fid 8), hop2 0..9=10 (->92, fid 9).
    (19) trace CB-HEAD term=92. AGG-tail from 92:
    entry scan 0..10=11: fid 10 (92,17,80); foldwalk:
    f1 0..11=12 (s1=15), f2 0..12=13 (s2=16),
    fold2 0..13=14 / 0..14=15, fold3 0..15=16 /
    0..16=17, term=86; VAL scan (2,86): 0..17=18,
    v=42==42 VERIFY-OK. (116)
    trace CB-ENTRY-CAND r=17 u=80 SHAPE-OK term=86
    VERIFY-OK / CB-BIND b=2 OK. BIND_TRIES=4.
  CB-ZBUILD rels=7,7,17,15,16,15,16,15,16
    facts=8,9,10,11,12,13,14,15,16.
  verify: chain_exec -> 86 (E=1); CB-VERIFY term=86 OK.
  promote Z id 3; t16 3->1 and 3->2; CB-PROMOTE z=3
    t16=3->1 t16=3->2; LINK14 ans->3; deliver exec (E=2).
  Frozen: ANS term=86 val=42 via=3; A_SEARCH=254;
  A_EXEC=2; t16=2 {3->1, 3->2}; e_has_to(3,14)=1; no edge
  type outside {14,16}; Z: id 3, rlen 9, rels
  [7,7,17,15,16,15,16,15,16], facts
  [8,9,10,11,12,13,14,15,16], start 90, end 86, dom 2,
  cap 1, live 1, descriptor (0,0,0,0,2); AGG_SRC=1;
  ROUTE_SRC=2; BINDING=2; BIND_DECIDED=1; BIND_TRIES=4;
  PIPE_HIT=0.
  A_SEARCH derivation: 2 + 3 + (48+18+48+135) = 254.
  A_EXEC: verify + deliver = 2.
  Q2B: pipeline mD/mA fail, mB0 -> 92, Z -> 86 val 42.
  Frozen: ANS term=86 val=42 via=3, CB_ENTERED=0,
  Z live=1.
- ARM-NOCOMBINE (combine_on=0): as FULL through the
  searches (A=2+3=5 informational); enumeration skipped;
  ans=-2. Frozen: ANS term=-2 val=-2 via=-1; t16=0; NM=3.
  (Proves combination is REQUIRED: no single structure
  grounds Q2.)
- ARM-ABLATE-A (combine_on=1, mA retired reason 3 pre-Q2):
  pipeline fails; AGG search id0 SKIP / id1(retired) SKIP
  / id2 SKIP (A=3 informational); no AGG source; ans=-2.
  Frozen: ANS term=-2 val=-2 via=-1; t16=0; NM=3.
- ARM-ABLATE-B (combine_on=1, mB0 retired reason 3
  pre-Q2): pipeline fails; AGG search -> mA (A=2);
  partner collection: id0 PCAP, id1 SKIP, id2(retired)
  SKIP (A=3); enumeration over [mD]: (mD,b=1) 48 FAIL,
  (mD,b=2) 18 FAIL; nothing verifies; ans=-2. Frozen: ANS
  term=-2 val=-2 via=-1; t16=0; NM=3. (Proves mB0
  specifically is required: the distractor mD cannot
  substitute for it.)
- ARM-FRESH (combine_on=1, facts only, no MAPs): pipeline
  empty; AGG search empty; ans=-2. Frozen: ANS term=-2
  val=-2 via=-1; t16=0; NM=0.

## 5. Kill bars (frozen, parent numbering)

- K1 (X and Y exist before the combination task, learned
  independently): in-Zag: qa_via==1 AND qb_via==2 AND
  q2_via==3 AND every rel of mA in {18,5,6} AND every rel
  of mB0 == 7 (disjoint relation sets: no shared
  vocabulary between the two source procedures). Shell:
  output line number of `Q QA` < `Q QB` < `Q Q2`.
- K2 (no single structure solves Q2; combination
  REQUIRED): in-Zag: PIPE_HIT==0 AND ne_val==-2 AND
  ne_t16==0 (the pipeline fails AND the no-combine
  control arm fails the same query). Shell (verbatim
  grep -F on run1): `CB-PIPELINE-FAIL`.
- K3 (learner decides the source pair and the binding,
  not the researcher): in-Zag: AGG_SRC==1 AND
  ROUTE_SRC==2 AND BINDING==2 AND BIND_TRIES==4 AND
  BIND_DECIDED==1 (the flag is set only inside the
  learner's verifying-enumeration branch). Shell
  (verbatim, in order): `CB-SRC-ROUTE id=0`,
  `CB-BIND b=1 FAIL`, `CB-BIND b=2 FAIL`,
  `CB-SRC-ROUTE id=2`, `CB-BIND b=1 FAIL`,
  `CB-BIND b=2 OK`; `grep -c` of
  `AGG_SRC\|ROUTE_SRC\|BINDING\|BIND_DECIDED\|BIND_TRIES`
  in driver.zag == 0 (the driver never names a source or
  a binding; ex_query takes only the COMBINE_ON
  causal-control flag).
- K4 (combined Z succeeds where each source alone fails):
  in-Zag: q2_via==3 AND q2_val==42 AND PIPE_HIT==0.
  Shell (verbatim): `CB-ZBUILD
  rels=7,7,17,15,16,15,16,15,16
  facts=8,9,10,11,12,13,14,15,16`,
  `ANS term=86 val=42 via=3`.
- K5 (BOTH sources are necessary: the load-bearing
  combine claim): in-Zag: ax_val==-2 AND ax_t16==0 AND
  bx_val==-2 AND bx_t16==0 (with mA retired the combine
  phase finds no AGG source; with mB0 retired the
  distractor mD fails every binding verification;
  nothing is promoted either way).
- K6 (determinism): 3/3 runs byte-identical (sha256 equal).
- K7 (no domain-pair template in source): 11 frozen grep
  patterns return 0 hits on learner.zag (section 6).
- K8 (dual provenance: Z is derived from both sources):
  in-Zag: t16==2 AND e_has(3,1,16)==1 AND
  e_has(3,2,16)==1.

Verdict L2-COMBINE-XDOMAIN-PASS iff K1-K8 all PASS, no
falsifier fires, F-COUNT silent. Reuse (Q2B via Z with no
re-combination) is falsifier-guarded: F-Q2B-RE and
F-Q2B-VIA.

## 6. Frozen K7 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `7,7,17,15,16,15,16,15,16` (Z's relseq must not be in
   the learner)
2. `8,9,10,11,12,13,14,15,16` (Z's fact list must not be
   there)
3. `(90,7,91)` (B route fact literal; world data stays out)
4. `(92,17,80)` (B entry fact literal)
5. `(86,2,42)` (B terminal VAL fact literal)
6. `86,42` (query target pair must not be there)
7. `90,86` (query start/target pair must not be there)
8. `_MODE` (zero modes)
9. `bridge` (case-insensitive; no bridge handlers)
10. `python` (case-insensitive; pure Zag)
11. `as *i32` (the pinned-znc miscompile pattern; u8 cells
    + get32/set32 only)

## 7. Frozen falsifiers

- F-NO-GROUND: FULL q2_via != 3.
- F-WRONG-Z: promoted Z header/rels/facts/(start,end)/
  (dom,cap)/descriptor != frozen section 4 values.
- F-PIPE-HIT: FULL PIPE_HIT != 0 (a single MAP must not
  deliver Q2).
- F-NOCOMB-PASS: NOCOMBINE ans != -2.
- F-ABLA-PASS: ABLATE-A ans != -2 OR t16 != 0.
- F-ABLB-PASS: ABLATE-B ans != -2 OR t16 != 0.
- F-FRESH-PASS: FRESH ans != -2.
- F-Q2B-RE: Q2B CB_ENTERED != 0 (re-combination happened).
- F-Q2B-VIA: Q2B via != 3.
- F-Q2B-VAL: Q2B val != 42.
- F-T16-COUNT: FULL t16 != 2.
- F-NO-T16-A: e_has(3,1,16) != 1.
- F-NO-T16-B: e_has(3,2,16) != 1.
- F-NO-LINK14: e_has_to(3,14) != 1.
- F-SRC: AGG_SRC != 1 OR ROUTE_SRC != 2.
- F-DISTR-SURVIVES: mD live != 1.
- F-EDGE-NEW: any edge with type outside {14,16}, any arm.
- F-COUNT: FULL A_SEARCH != 254 or A_EXEC != 2
  (implementation must match the frozen counting rules
  exactly; a pure arithmetic slip in this prereg's hand
  derivation may be transparently amended pre-verdict,
  an algorithmic counting change may not).
- F-AUDIT / F-NONDET / F-PYTHON: as in prior waves; any
  fires voids the build.

## 8. Determinism spec

No RNG. MAP-id order, fid-ascending scans, first-match
rules, fixed (partner-source, binding) enumeration order
everywhere. Output via one preallocated buffer and a
single raw-syscall write loop (the pinned-znc stdout
workaround). 3/3 byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The cross-domain COMBINE operator, descriptor
  extraction, entry/fold search with runtime relation
  discovery, strict partner-segment walk, first-verifying-
  combination enumeration, and cost counters are
  researcher-supplied generic machinery, frozen here. None
  names a relation, MAP, domain, source pair, binding, or
  domain pair. The partner capability is the first
  distinct live non-query cap met in id order (no
  capability literal in the learner). The L2 claim is
  narrow: a planning query with no native aggregation is
  served by a combination of a learner-selected arithmetic
  aggregation structure and a learner-selected planning
  route structure, where neither structure alone grounds
  the query, the source pair and binding are chosen by the
  learner's verification loop, both ablations fail, the
  combined form is verified by execution, carries dual
  type-16 provenance, persists, and is reused.
- COMBINE_ON is a driver-set causal-control flag (the
  composition_l2 adapt_on precedent), never written by the
  learner. It enables the lesion comparison; it is not a
  runtime mode.
- One world family (arithmetic aggregation x plan-route +
  plan-cost aggregation). No generality claim beyond the
  five arms. The world is builder-designed, not
  adversary-designed. Sealed-adversary generality is open
  future work.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types, 0 new
  opcodes, 0 new semantic cases. Pure Zag, safebin
  toolchain, zero forbidden executables.
- No em/en dashes in loop documentation. Paper untouched.
  Nothing pushed. Commits local with explicit pathspec.
- Unfrozen only: no frozen source touched. The frozen TNN
  core is not used here; this is a standalone
  learner-mechanism experiment in the chain family.
- This wave does not integrate a composition engine into
  the protected core or any continuing learner; like the
  L2 matrix waves, it tests a learner-mechanism claim in a
  standalone harness. Whether one general composition
  operation subsumes the H1/H2/A/B/C mechanisms remains an
  open comparative question, not decided here.
