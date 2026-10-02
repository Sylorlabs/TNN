# SUBSTRATE_PREREG: minimal learner-reachable construction / contradiction / standing package

Lane: TNN3-SUBSTRATE, wave-20261001-2321pdt.
Status: FROZEN. This document is the preregistration for the substrate addition package.
Frozen: 2026-10-01, wave wave-20261001-2321pdt.
Frozen substrate referenced: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag,
1591 lines, SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
(hash re-verified by this worker with sha256sum on 2026-10-01; matches character for character).
Documentation rule observed: no em-dashes in this document.

## 1. Problem statement

The 2021pdt TNN3-SYNTH synthesis (docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3-SYNTH/SYNTHESIS.md)
concluded TNN-3 needs ADDITIONS not compression. Six lanes stopped at substrate
verification with SUBSTRATE-ABSENT findings against the frozen TNN-2 core:

- H2 (inversion): no learner-reachable construction path; deletion would remove the only
  graph construction. PREREG_H2.md section 2, verification (a).
- H3 (procedure-as-operand): no event-interface path stores a graph root as a fact
  operand; fact operands hold scalars only. PREREG_H3.md verification (c).
- H4 (projection authoring): no learner-reachable path allocates cells with
  learner-chosen guard/set content; protected EXECUTE unreachable from ev_act.
  PREREG_H4.md verifications (b), (c).
- H6 (standing): no learner-reachable path updates standing on UNCERT nodes; no
  CONFIRM/CONTRADICT events; no learner-maintained standing field for selectors.
  PREREG_H6.md verifications (b), (c).
- H7 (re-derivation): no learner construction process exists to re-derive with; no
  contradiction-to-construction trigger (ev_observe contradiction never invokes
  mp_run/t2_trial). PREREG_H7.md verifications (b), (c).
- H10 (unified workspace): no learner-addressable workspace; no generic query
  mechanism. PREREG_H10.md sections 3, 5.

This package supplies the three missing affordances the synthesis named, as generic
machinery: (a) a learner construction service, (b) a contradiction trigger,
(c) learner-writable standing. It unblocks the H2/H4/H6/H7 re-attempts. H3 and H10
follow from (a) plus their own follow-on work (named in section 7, not in this package).

## 2. Governing constraints

- ONE-SYSTEM RULE: no new modes, no bridges, no routers, no task-specific handlers.
  Capability-source delta is positive here (the synthesis proved deletion cannot work)
  and is recorded exactly; the design minimizes it (section 6).
- PROTECTED CORE ISA RULING: the core basis is frozen and never grown one benchmark at
  a time. This package adds ZERO protected-core operations: no new opcodes, execute()
  unmodified, alloc_node/link_edge/ng/ns unmodified. All new functions live in the
  cognition layer (the same layer as the assemblers and the trial loop) and are composed
  only of ALLOC/READ/WRITE/LINK plus the existing EXECUTE. Forbidden class check:
  no function below detects a target-domain regularity or encodes benchmark semantics.
- EXECUTE placement: EXECUTE(root, frame) is approved protected-core machinery and is
  not re-litigated here. This package does NOT wire EXECUTE into ev_act; that placement
  is the pending ruling (amendments A-C, awaiting Micah) and H4R's full loop stays
  gated on it (kill bars section 8).
- Verification-first (H1 red-team rule): section 3 verifies the absences against
  committed source before any bar below is frozen.

## 3. Substrate verification (the absences, re-verified by this worker)

Against the frozen tnn2.zag (hash above), by grep on 2026-10-01:

(a) The six cell constructors (t2_lit, t2_cell, t2_guard, t2_set, t2_mov, t2_inc;
lines 338-361) are invoked only from the three researcher-written assemblers
(lines 363-410) and from t2_revise_graph (lines 725-726). No invocation is reachable
from ev_observe, ev_query, or ev_act. Learner-reachable construction: ABSENT.

(b) ev_observe (lines 836-857): the contradiction branch (lines 845-856) calls
revise_on_contradict and teaches the new fact; it never invokes mp_run or t2_trial.
Contradiction-to-construction trigger: ABSENT.

(c) The only standing-like writes on the event path are the ET_CFM (type 7) and ET_CON
(type 3) self-edges in ev_observe; there is no accumulator, no CONFIRM/CONTRADICT
event with a payload, and no learner-writable field any selector reads. bid()
(lines 237-248) is the only selector math, called at lines 145 (activate), 259
(evict_node), 872 and 884 (ev_act). Learner-writable standing: ABSENT.

(d) Node type 904 is unused in the frozen source (no occurrences); node-0 fields 24
and 28 are written never (only field 20 via pol_set). Register slots free: CONFIRMED.

## 4. The package: three generic components

### 4A. Learner construction service (unblocks H2, H4, H7; enables H3)

A construction SERVICE, not a schema. Researcher-written assemblers choose schemas;
this machinery chooses nothing: it materializes exactly what a learner-authored
ticket specifies, using only ALLOC/WRITE/LINK.

Learner-state vocabulary (all structural, all in the existing store):

- T_TICKET = 904: new node type. Structural, not semantic. 904 is unused in the
  frozen source (verified in 3d), so tickets are invisible to every fact/MAP/UNCERT
  scan (all check tag 1/20/30). This avoids the interference that reusing T_FACT
  would cause in t2_gather/activate.
- R_BUILD = -41, R_REDERIVE = -43, R_STAND = -44: negative relation codes naming
  operations, not domains (same convention as the existing -999 licensing marker).
- BUILD_ROOT register at ng(W,0,24); STAND_ROOT at ng(W,0,28): type-2 GROUP nodes
  (existing type, same as POLICY_ROOT), ET_PRO-pinned, created on demand.
  Membership via ET_MEM (type 10), the same edge type POLICY_ROOT uses for guides.
  No new edge types.

Ticket format (BUILD ticket): 904 node, field20 = opaque context id, field24 = -41,
field28 = build status (0 pending, 1 built, -1 failed), field32 = built root id.
One ET_REF (type 4) edge to the first step; steps are 904 nodes chained by ET_SEQ
(type 12). Step fields: field20 = cell tag (101-104), field24/28/32 = operand specs
for the cell's field4/field8/field12. Steps are identified by topology only
(ticket ET_REF then ET_SEQ walk); no step marker is needed.

Operand spec encoding (generic, documented, no domain content):

- spec >= 1000: frame-slot code (1000+slot), passed through to the cell field.
  The ISA interprets it; the builder does not.
- spec < 0: back-reference to the (-spec-1)-th cell built for this ticket
  (0-based, any earlier or later cell; enables BRANCHEQ true-targets, the H2 case).
- 0 <= spec <= 999: literal value; the builder allocates a fresh 902 literal node
  with field20 = spec (exactly what t2_lit does, inlined).

Builder (lb_run / lb_build_ticket): two passes. Pass 1 allocates one cell per step
with the ticket's tag, in order. Pass 2 resolves specs, writes field4/8/12, chains
consecutive cells with ET_SEQ, and defaults a BRANCHEQ cell's field16 (false target)
to the next cell (documented wiring convention; a trailing BRANCHEQ keeps field16=0
and fails closed, the assemblers' convention). On any failure the ticket is marked
-1; partial allocations are left (same as the assemblers' failure behavior).
The builder performs no semantic validation: a ticket that builds a graph which
fails at execute time is a built graph that fails at execute time.

Reachability: lb_run is called at the tail of ev_observe on all three return paths
(teach, confirm, contradict), after the event's own work. Rationale: tickets are
learner state authored by experience; ev_observe is the generic "experience happened"
event. lb_run with no BUILD_ROOT present returns immediately with zero allocation
(lazy root check), so workspaces that never use the service are allocation-identical
to the frozen binary. ev_query/ev_act wiring is deferred (not needed for the
re-attempts; a future decision, not this package).

Content-neutrality (the anti-treadmill property): the SAME code path builds a
guard-on-slot-0 chain (assembler-like), a guard-on-slot-1 graph (the H2 inversion
case the assemblers cannot express), and a content-to-action projection (the H4
case). The prototype (section 5) verifies all three through one service.

### 4B. Contradiction trigger (unblocks H7)

lt_fire(W, oldn, newn): reifies a fact contradiction as a REDERIVE ticket (904,
field24 = -43) under BUILD_ROOT, with ET_REF edges to the old (superseded) fact
node and the new fact node, uninterpreted. Called once from ev_observe's
contradiction branch, after ev_teach_in returns. Generic: no type checks, no MAP
logic, no domain content, fires on every fact contradiction regardless of whether
any MAP exists. REDERIVE tickets are inert data for this package; their
interpretation (re-derivation) is H7R's hypothesis to specify. The package
guarantees only the signal: conflict in, linked ticket out.

### 4C. Learner-writable standing (unblocks H6)

One 904 standing record per target node under STAND_ROOT (field24 = -44, ET_REF to
the target, field28 = standing value, field32 = update count). Updated ONLY by the
generic event polarities: ls_bump(W,n,+1) on ev_observe's confirm branch,
ls_bump(W,n,-1) on the contradict branch. The +1/-1 are event polarities, exactly
analogous to the existing ET_CFM/ET_CON self-edges; the intelligence under test is
in the trajectories, not the constants.

Reader: ls_read(W, target) returns the standing value or sentinel -999999 when no
record exists. Selector integration: lbid(W,n) = ls_read where a record exists,
else the frozen bid(). The four cognition-path call sites (lines 145, 259, 872,
884) call lbid. Cold start (no records) is behavior-identical to the frozen
substrate; the prototype's regression run (existing 46 self-tests) verifies this.

Roots are ET_PRO-pinned on creation and re-pinned (ref_prot) on every touch, so the
workspace roots survive retention pressure; individual tickets/records participate
in the normal bid-based eviction like all learner state (no special retention
logic: one-system rule).

### Frozen package source (transcribed verbatim into the prototype)

```zag
// PKG-BEGIN
// ============ TNN3-SUBSTRATE package (prereg-frozen 2026-10-01, wave-20261001-2321pdt) ============
// Generic machinery only: ALLOC/WRITE/LINK over the existing workspace plus the
// frozen 4-op ISA executed by execute(). No new opcodes, no modes, no bridges,
// no routers, no task-specific handlers, no semantic cases, no domain detectors.
// Learner-state vocabulary: T_TICKET (904) nodes; relations -41/-43/-44 name
// operations, not domains. BUILD_ROOT at ng(W,0,24), STAND_ROOT at ng(W,0,28):
// type-2 GROUP nodes (existing type), ET_PRO-pinned. Membership via ET_MEM (10).
fn T_TICKET()i32 { return 904; }
fn R_BUILD()i32 { return -41; }
fn R_REDERIVE()i32 { return -43; }
fn R_STAND()i32 { return -44; }
fn LS_NONE()i32 { return -999999; }
// one parameterized root constructor (slot 24 = BUILD_ROOT, 28 = STAND_ROOT)
fn lb_root(W:[]u8,slot:i32,mark:i32)i32 {
  let r:i32=ng(W,0,slot);
  if(r>=2 && ng(W,r,36)==1){ref_prot(W,r); return r;}
  r=alloc_node(W); if(r<0){return -1;}
  ns(W,r,0,2); ns(W,r,4,mark);
  link_edge(W,r,9,r,hg(W,4));
  ns(W,0,slot,r); return r;
}
fn lb_broot(W:[]u8)i32 { return lb_root(W,24,-6); }
fn lb_sroot(W:[]u8)i32 { return lb_root(W,28,-7); }
// first ET_REF (type 4) target of t, or -1
fn lb_reftarget(W:[]u8,t:i32)i32 {
  let e:i32=0;
  while(e<4096){
    if(eg(W,e,0)!=-1 && eg(W,e,0)==t && eg(W,e,4)==4){return eg(W,e,8);}
    e=e+1;
  }
  return -1;
}
// last step of ticket t's ET_SEQ chain, or -1
fn lb_laststep(W:[]u8,t:i32)i32 {
  let cur:i32=lb_reftarget(W,t);
  if(cur<0){return -1;}
  let gd:i32=0;
  while(gd<64){
    let nx:i32=seq_nx(W,cur);
    if(nx<0){return cur;}
    cur=nx; gd=gd+1;
  }
  return -1;
}
// authoring API: new ticket (rel -41 build, -43 rederive via lt_fire)
fn lb_ticket_new(W:[]u8,ctx:i32,rel:i32)i32 {
  let br:i32=lb_broot(W); if(br<0){return -1;}
  let t:i32=alloc_node(W); if(t<0){return -1;}
  ns(W,t,0,904); write_node(W,t,ctx,rel,0,0);
  link_edge(W,br,10,t,0);
  return t;
}
// authoring API: append one step; step fields are (tag, f4spec, f8spec, f12spec)
fn lb_step_add(W:[]u8,t:i32,tag:i32,f4:i32,f8:i32,f12:i32)i32 {
  if(ng(W,t,36)!=1 || ng(W,t,0)!=904){return -1;}
  if(tag!=101 && tag!=102 && tag!=103 && tag!=104){return -1;}
  let s:i32=alloc_node(W); if(s<0){return -1;}
  ns(W,s,0,904); write_node(W,s,tag,f4,f8,f12);
  if(lb_reftarget(W,t)<0){link_edge(W,t,4,s,0);}
  else {
    let last:i32=lb_laststep(W,t);
    if(last<0){return -1;}
    seq_link(W,last,s);
  }
  return s;
}
// two-pass materialization of one pending BUILD ticket
fn lb_build_ticket(W:[]u8,t:i32)void {
  let first:i32=lb_reftarget(W,t);
  if(first<0 || ng(W,first,0)!=904){ns(W,t,28,-1); return;}
  let steps:[]u8=z_alloc(256); let nst:i32=0;
  let cur:i32=first; let gd:i32=0;
  while(cur>=0 && nst<64 && gd<64){
    if(ng(W,cur,36)!=1 || ng(W,cur,0)!=904){ns(W,t,28,-1); return;}
    set32(steps,nst*4,cur); nst=nst+1;
    cur=seq_nx(W,cur); gd=gd+1;
  }
  if(nst==0){ns(W,t,28,-1); return;}
  let cells:[]u8=z_alloc(256); let nc:i32=0; let ok:i32=1;
  let i:i32=0;
  while(i<nst && ok==1){
    let tag:i32=ng(W,get32(steps,i*4),20);
    if(tag!=101 && tag!=102 && tag!=103 && tag!=104){ok=0;}
    else {
      let c:i32=alloc_node(W);
      if(c<0){ok=0;} else {ns(W,c,0,tag); set32(cells,nc*4,c); nc=nc+1;}
    }
    i=i+1;
  }
  if(ok==0){ns(W,t,28,-1); return;}
  i=0;
  while(i<nc && ok==1){
    let st:i32=get32(steps,i*4); let c:i32=get32(cells,i*4);
    let p:i32=0;
    while(p<3 && ok==1){
      let spec:i32=ng(W,st,24+p*4); let val:i32=-999999;
      if(spec>=1000){val=spec;}
      else {
        if(spec<0){
          let j:i32=-spec-1;
          if(j<0 || j>=nc){ok=0;} else {val=get32(cells,j*4);}
        } else {
          let ln:i32=alloc_node(W);
          if(ln<0){ok=0;} else {ns(W,ln,0,902); ns(W,ln,20,spec); val=ln;}
        }
      }
      if(ok==1){ns(W,c,4+p*4,val);}
      p=p+1;
    }
    if(ok==1 && i+1<nc){
      seq_link(W,c,get32(cells,(i+1)*4));
      if(ng(W,c,0)==102){ns(W,c,16,get32(cells,(i+1)*4));}
    }
    i=i+1;
  }
  if(ok==0){ns(W,t,28,-1); return;}
  let root:i32=get32(cells,0);
  link_edge(W,t,4,root,0);
  ns(W,t,28,1); ns(W,t,32,root);
  return;
}
// construction service entry: build every pending R_BUILD ticket.
// Lazy root check: no BUILD_ROOT means no tickets can exist; zero allocation.
fn lb_run(W:[]u8)void {
  let br:i32=ng(W,0,24);
  if(br<2 || ng(W,br,36)!=1){return;}
  let pend:[]u8=z_alloc(256); let np:i32=0;
  let e:i32=0;
  while(e<4096 && np<64){
    if(eg(W,e,0)!=-1 && eg(W,e,0)==br && eg(W,e,4)==10){
      let t:i32=eg(W,e,8);
      if(ng(W,t,36)==1 && ng(W,t,0)==904 && ng(W,t,24)==-41 && ng(W,t,28)==0){
        set32(pend,np*4,t); np=np+1;
      }
    }
    e=e+1;
  }
  let i:i32=0;
  while(i<np){lb_build_ticket(W,get32(pend,i*4)); i=i+1;}
  return;
}
// generic contradiction signal: reify (old, new) as a REDERIVE ticket.
// No type checks, no MAP logic, no domain content.
fn lt_fire(W:[]u8,oldn:i32,newn:i32)void {
  if(oldn<2){return;}
  let t:i32=lb_ticket_new(W,ng(W,oldn,20),-43);
  if(t<0){return;}
  link_edge(W,t,4,oldn,0);
  if(newn>=2){link_edge(W,t,4,newn,0);}
  return;
}
// learner-writable standing: one 904 record per target under STAND_ROOT
fn ls_find(W:[]u8,target:i32)i32 {
  let sr:i32=ng(W,0,28);
  if(sr<2 || ng(W,sr,36)!=1){return -1;}
  let e:i32=0;
  while(e<4096){
    if(eg(W,e,0)!=-1 && eg(W,e,0)==sr && eg(W,e,4)==10){
      let r:i32=eg(W,e,8);
      if(ng(W,r,36)==1 && ng(W,r,0)==904 && ng(W,r,24)==-44){
        if(lb_reftarget(W,r)==target){return r;}
      }
    }
    e=e+1;
  }
  return -1;
}
fn ls_touch(W:[]u8,target:i32)i32 {
  let r:i32=ls_find(W,target);
  if(r>=0){return r;}
  let sr:i32=lb_sroot(W); if(sr<0){return -1;}
  r=alloc_node(W); if(r<0){return -1;}
  ns(W,r,0,904); write_node(W,r,target,-44,0,0);
  link_edge(W,r,4,target,0);
  link_edge(W,sr,10,r,0);
  return r;
}
// generic event polarities only: +1 confirm, -1 contradict
fn ls_bump(W:[]u8,target:i32,delta:i32)void {
  let r:i32=ls_touch(W,target); if(r<0){return;}
  ns(W,r,28,ng(W,r,28)+delta);
  ns(W,r,32,ng(W,r,32)+1);
  ref_prot(W,lb_sroot(W));
  return;
}
fn ls_read(W:[]u8,target:i32)i32 {
  let r:i32=ls_find(W,target);
  if(r<0){return -999999;}
  return ng(W,r,28);
}
// standing-aware bid: learner standing where it exists, frozen bid() otherwise
fn lbid(W:[]u8,n:i32)i32 {
  let s:i32=ls_read(W,n);
  if(s!=-999999){return s;}
  return bid(W,n);
}
// PKG-END
```

### Specified adoption diff (mechanical, for the future adoption worker)

Against the frozen tnn2.zag (or its line-identical successor):

1. Append the PKG-BEGIN/PKG-END section above verbatim (cognition layer, after the
   event section, before the test battery).
2. ev_observe (lines 836-857): confirm branch, after `ref_prot(W,n);`, insert
   `ls_bump(W,n,1);`. Contradiction branch, after `let nn:i32=ev_teach_in(W,s,r,o);`
   and its following line, insert `lt_fire(W,n,nn); ls_bump(W,n,-1);`. Before each
   of the three `return` statements in ev_observe, insert `lb_run(W);`.
3. Replace `bid(` with `lbid(` at exactly four cognition-path call sites: lines
   145 (activate), 259 (evict_node), 872 and 884 (ev_act). Test-battery call sites
   (lines 954, 986, 1206, 1211) keep `bid(` (they unit-test the frozen formula).
4. Nothing else. Protected core (execute, ISA tags, alloc_node, link_edge, ng/ns)
   untouched: zero new opcodes.

## 5. Prototype and verification-first checks

The prototype is a dev harness in this lane's directory: a copy of the frozen
tnn2.zag with the adoption diff applied (hook insertions marked SUBSTRATE-HOOK),
the package section appended by mechanical extraction from this prereg
(sed between PKG-BEGIN and PKG-END: no retyping), and dev checks appended with
main replaced by proto_main. The frozen tnn2.zag itself is never modified.

Verification checks (each must pass; any failure kills the package design):

- R0 REGRESSION: the prototype's run_all (all 46 frozen self-tests) passes 46/46.
  This verifies the hooks are behavior-preserving at cold start and under the
  light learner-state use the self-tests exercise (contradictions in t_c3/t_dv/
  t_t2_revise create trigger tickets and standing records; selections must be
  unaffected).
- V1 CONSTRUCTION REACHABLE: author a BUILD ticket with guard slot 1 (inverted
  relative to the assemblers' fixed slot 0; the H2 discrimination), literals 5/7/9,
  and a back-reference true-target. One ev_observe processes it. White-box asserts:
  ticket status 1, built root recorded, cell0 tag 102 with field4 1001 (learner-chosen
  slot honored, not researcher slot 0), literal node values exact, field12 wired to
  cell1. Execute asserts: slot1=5 gives slot0=7; slot1=6 falls through to slot0=9.
  A second assembler-shaped ticket (slot 0) builds through the same code path,
  proving content-neutrality.
- V2 CONTRADICTION TRIGGER: teach (101,11,102); ev_observe (101,11,999) must yield
  exactly one REDERIVE ticket whose ET_REF targets are the old and new fact nodes.
  A confirming observe and a pure teach must yield no further tickets.
- V3 STANDING PERSISTS: three confirms then one contradict on one fact give
  ls_read 2; five interleaved queries leave it unchanged; the new fact's confirm
  gives ls_read 1; lbid equals bid on a record-less node (cold-start identity).

The dev driver authors tickets in V1 explicitly as a stand-in for future
learner-side authoring; what V1 verifies is the SERVICE (reachability, fidelity,
content-neutrality), not learner authorship. Learner authorship is the re-attempts'
burden under the L3 criteria (section 8). This labeling answers the H1 red-team
rule: the harness never claims to be the learner.

## 6. Architecture accounting (frozen with this prereg)

Counted from the package source in section 4 (PKG-BEGIN to PKG-END):

- Cognition source lines added: 176 (14 functions + 5 constant functions; counted
  by the prototype build step and recorded in the implementation commit; if the
  mechanical transcription changes the count, the implementation commit amends
  this line transparently with the exact number).
- New hardcoded semantic cases: 0. No function conditions on domain, task,
  benchmark, relation value (other than the -41/-43/-44 operation codes), or node
  type (other than the 904 ticket type and 101-104 ISA tags, which are machinery).
- New modes: 0. New bridges: 0. New routers: 0. New task-specific handlers: 0.
- Protected-core operations added: 0. execute(), the 4-op ISA, alloc_node,
  link_edge, ng/ns/eg/es: all unmodified.
- Learner-state structures created (enumerated): (1) T_TICKET (904) nodes in three
  roles: BUILD tickets (-41), REDERIVE tickets (-43), standing records (-44);
  (2) BUILD_STEP nodes (904, topology-identified); (3) BUILD_ROOT register
  (node-0 field 24, type-2 GROUP); (4) STAND_ROOT register (node-0 field 28,
  type-2 GROUP); (5) auto-allocated 902 literal nodes (existing literal convention);
  (6) ET_MEM (10) membership edges, ET_REF (4) ticket/step/root edges, ET_SEQ (12)
  step chains and cell spines (all existing edge types; no new edge types).
- Behavior deltas vs frozen (all intended, all verified by R0): ev_observe confirm
  creates/touches a standing record (+1); ev_observe contradict creates a REDERIVE
  ticket and touches a standing record (-1); ev_observe tail runs lb_run (no-op
  without BUILD_ROOT); the four selector call sites read lbid (identical to bid
  where no standing record exists).

Minimality argument: lb_root is parameterized (one function, two roots) rather
than two constructors; steps are topology-identified (no step type or marker);
the builder is two passes because back-references require all cells to exist before
operands resolve (one pass cannot wire BRANCHEQ true-targets, the H2 case);
ls_find/ls_touch/ls_bump/ls_read are the smallest read/write API around one record
format; lbid is the single integration point for all three selectors. Removing any
one function breaks a named re-attempt's requirement.

## 7. Explicit non-goals (what this package does NOT supply)

- Ticket AUTHORING by the learner. The package provides the service, the format, and
  reachability. Which process authors tickets on sealed worlds (and whether its
  output meets the L3 criteria) is each re-attempt's hypothesis. A re-attempt whose
  sealed driver hand-authors ticket content fails the L3 novelty bars by construction.
- REDERIVE ticket interpretation (re-derivation). H7R specifies the consumer.
- EXECUTE wired into ev_act. Pending Micah's EXECUTE placement ruling (amendments
  A-C); H4R is gated on it (section 8).
- Generic cross-type queries (H10's verification-b item). The registers plus existing
  scans make a generic query writable without new machinery; specifying it is
  follow-on work, not part of this minimal package.
- Naming (H1's successor). Expressible only after (a) is adopted; the ticket format
  gives it a place to live.

## 8. Frozen kill bars for the H2/H4/H6/H7 re-attempts

General preconditions (all four re-attempts): (G1) the re-attempt worker re-verifies
the package by committed-source grep plus white-box dump (quoting the adopted
placements from section 4) BEFORE freezing its own bars; (G2) sealed worlds designed
post-freeze by an independent adversary; (G3) deterministic byte-identical runs;
(G4) the L3 criteria govern any authorship claim; builders report BUILD-PASS or
BUILD-FAIL only.

KB-H2R (inversion re-attempt; needs 4A):
- B1 substrate: this prototype's V1 re-run on the adopted build (ticket with guard
  slot != 0 builds; cell field4 equals ticket spec; executes correctly).
- B2 sealed: on adversary-designed worlds requiring inverse-direction derivations,
  at least 80 percent of hidden queries answered correctly via ticket-built graphs
  executed by the frozen ISA.
- B3 source novelty: grep of the adopted source shows no constructor or assembler
  with a hardcoded slot != 0 and no inverse-direction schema; inverse content
  appears only in tickets.
- B4 ablation: tombstoning the ticket-built cells destroys the sealed advantage
  (falls to at most the no-construction baseline).
- KILL: B2 below 80 percent, or B3 fails (inverse schema found in source).

KB-H4R (projection re-attempt; needs 4A):
- B1 substrate: ticket-built projection cells (guard on content fields, set writing
  the action slot) construct via lb_run and execute to the ticketed action value.
- B2 sealed: on informant-discrimination worlds (M2-W1/M2-W3 family, adversary
  variants), the action selects the better informant on at least 80 percent of
  hidden trials, beating the constant-action-30 baseline.
- B3 ablation: removing the projection cells reverts behavior to the constant action.
- GOVERNANCE GATE B4: wiring EXECUTE into ev_act is BLOCKED on Micah's pending
  EXECUTE placement ruling (amendments A-C). H4R may freeze B1-B3 now; it may not
  claim the closed H4 loop until the ruling lands. If the ruling denies ev_act
  wiring, H4R is SUSPENDED (not killed) pending redesign. This bar does not
  preempt the ruling.
- KILL: B2 below 80 percent, or B3 fails to revert.

KB-H6R (standing re-attempt; needs 4C):
- B1 substrate: ls_read trajectories discriminate a singleton contradiction
  (transient dip then recovery under confirms) from a systematic shift (monotonic
  decline); white-box asserted on scripted event sequences.
- B2 integration: grep of the adopted source shows lbid (not bid) at all three
  selector call sites (activate, evict_node, ev_act).
- B3 sealed: on worlds where raw frequency misleads (high-frequency wrong guide
  vs low-frequency right guide), standing-guided selection beats the bid-only
  control by at least 15 percentage points on hidden trials.
- B4 retention: under memory pressure, high-standing nodes survive preferentially
  relative to the bid-only control.
- KILL: B1 trajectories do not discriminate, or B3 margin below 15 points.

KB-H7R (re-derivation re-attempt; needs 4A + 4B):
- B1 substrate: every ev_observe contradiction on scripted sequences yields exactly
  one REDERIVE ticket linking the superseded and the new fact (white-box); this
  prototype's V2 re-run on the adopted build.
- B2 sealed: the H7R re-derivation consumer rebuilds via lb_run against the live
  fact store; post-contradiction hidden queries return the corrected answer.
- B3 non-treadmill: the rebuilt graph's t2_sig signature differs from the stale
  graph's signature on at least 80 percent of contradiction cases (H7's own
  falsifiable prediction: re-learning the same wrong thing is the killed outcome).
- B4 ablation: without the rebuilt graph, answers stay stale.
- KILL: B3 below 80 percent. Per H7's prediction this outcome kills the hypothesis
  rather than triggering repair.

Amendment rule: these bars are frozen with this prereg. If a re-attempt finds a bar
unexecutable as written, it amends transparently and re-freezes; it never moves a
bar silently to force a pass.

## 9. Governance

Adopting any of this package into the protected-core boundary is a GOVERNANCE
DECISION for Micah (protected-core boundary change). This lane recommends (see
ADOPTION_RECOMMENDATION.md) but does not adopt. The package as specified lives in
the cognition layer, not the protected core; even so, landing it in the frozen
TNN-2 lineage changes the frozen baseline, which is itself a governance decision.

## 10. Commit order

This prereg is committed alone, before any implementation. The prototype commit
follows strictly after. The commit-order self-check: the prereg commit's timestamp
precedes the prototype commit's timestamp.
