# SHADOW-FACT ROOT-CAUSE DIAGNOSIS (TNN3H5, wave-20261001-2021pdt)

Analysis only. No implementation, no builds, no commits. All line
numbers refer to docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/tnn3_h5.zag
unless noted. No em-dashes used in this document.

## 0. Verdict in one paragraph

H5 grafted MAP supersession onto a substrate in which MAP nodes were
never on any read path. promote_graph (line 543) teaches a tag-1
"shadow fact" holding the promoted answer, and ev_query's activate
(line 150) only ever reads tag-1 facts. The shadow fact is therefore
the sole retrieval handle for the MAP key; the MAP node itself is a
write-only ledger. On contradiction, ev_observe supersedes the
contradicted fact and revise_on_contradict writes CON edges on MAPs
whose DEP edges point at that fact (KB-W2 verified the writes), but
the shadow fact sits on a different key and is not a DEP target of the
MAP, so no contradiction path touches it. The MAP key always hits the
live shadow fact, never misses, and mp_run re-derivation never runs
for MAP keys. The MAP CON edges change no query outcome on any probed
path: they are behaviorally inert writes. Sealed evidence: C1S
bridge-query=100 and C2S bridge-query=900 (stale originals) after
double contradiction, with mapCON-delta=1 on the same runs.

## 1. Where the shadow fact is taught, and why it is uncontradicted

promote_graph, lines 543-554:

```
fn promote_graph(W:[]u8,root:i32,s:i32,r:i32,ans:i32,facts:[]u8,nf:i32)i32 {
  let m:i32=alloc_node(W); if(m<0){return -1;}
  ns(W,m,0,20); ns(W,m,4,r); ns(W,m,8,s); ns(W,m,12,-1); ns(W,m,16,-1);
  write_node(W,m,root,hg(W,24),ans,0);
  link_edge(W,m,13,m,hg(W,0));
  link_edge(W,m,2,m,0); link_edge(W,m,6,m,0);
  let i:i32=0;
  while(i<nf){link_edge(W,m,1,get32(facts,i*4),0); i=i+1;}
  ev_teach_in(W,s,r,ans);
  return m;
}
```

Line 551, `ev_teach_in(W,s,r,ans)`, is the shadow-fact teaching.
ev_teach_in (lines 320-325):

```
fn ev_teach_in(W:[]u8,s:i32,r:i32,o:i32)i32 {
  let n:i32=alloc_node(W); if(n<0){return -1;}
  ns(W,n,0,1); write_node(W,n,s,r,o,hg(W,0));
  link_edge(W,n,9,n,hg(W,4)); return n;
}
```

The shadow fact's fields: tag f0=1 (a plain fact, not a MAP), f20=s,
f24=r (the MAP key), f28=ans (the promoted answer, frozen at promote
time), f36=1 (live). Its edges: a type-9 protection self-edge (line
323), plus type-6 query self-edges accumulated on every ev_query hit
(line 769) and type-7 confirm self-edges on confirmations (line 825);
these only raise its bid() and never invalidate it.

Sealed-world instance (runs/c1_run1.txt dump): N 13 is the MAP
(tag 20, f4=5203, f8=52101, f20=graph root 6, f24=promo index 7,
f28=100); N 14 is the shadow fact (tag 1, f20=52101, f24=5203,
f28=100). After the double contradiction on the fact key
(52201,5202): 100 -> 200 -> 300, N 14 still holds f28=100, live.

Why ev_observe's contradiction path never touches the shadow fact
(ev_observe, lines 819-842):

```
fn ev_observe(W:[]u8,s:i32,r:i32,o:i32)i32 {
  hs(W,0,hg(W,0)+1); decay(W); ctx_push(W,s);
  resolve_uncertainty(W,s,r);
  let n:i32=activate(W,s,r);
  if(n>=0){
    if(ng(W,n,28)==o){
      link_edge(W,n,7,n,0); ref_prot(W,n);
      log_ev(W,4,s,r,o,1,0,0); return 1;
    }
    supersede(W,n);
    revise_on_contradict(W,n,o);
    ...
    let nn:i32=ev_teach_in(W,s,r,o);
    if(nn>=0){link_edge(W,nn,4,n,0);}
    log_ev(W,4,s,r,o,0,0,0); return 0;
  }
  ev_teach_in(W,s,r,o); log_ev(W,4,s,r,o,1,0,0); return 1;
}
```

Three reasons, each code-verified:

a. activate is keyed by the OBSERVED (s,r). In the sealed C-worlds
contradictions arrive on the fact key (b,5202), e.g. sw_c1_double
calls ev_observe(W,b,5202,c1). activate (line 150) requires
ng(W,n,20)==s and ng(W,n,24)==r; the shadow fact carries
(f20,f24)=(a,5203)=(52101,5203), a different key, so it is never the
selected node n and supersede(W,n) (line 830) never hits it.

b. revise_on_contradict (lines 687-704) only supersedes tag-20 nodes
(line 692: `if(ng(W,m,36)==1 && ng(W,m,0)==20)`), and only those whose
ET_DEP (type-1) edge runs MAP->contradicted-fact (line 696:
`eg(W,e,0)==m && eg(W,e,4)==1 && eg(W,e,8)==factn`). The MAP's DEP
edges (promote_graph line 550) point at the LICENSING facts (the chain
facts in the `facts` array), which include the contradicted fact but
never include the shadow fact: the shadow fact is taught at line 551,
after the DEP loop, and is not in the `facts` array. So the shadow
fact is never superseded via provenance either.

c. The sealed worlds never call ev_observe on the MAP key (a,5203) at
all. The one path that could supersede the shadow fact (direct
observation on its key) is never exercised.

Net: the shadow fact remains live (is_superseded==0) with
f28=stale original for the entire sealed run.

Baseline comparison: the frozen TNN-2 baseline
(docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag, lines
533-542) contains the identical promote_graph with the identical
ev_teach_in call at line 541. In TNN-2 this was harmless: no CON edge
ever touched a MAP (baseline comment at line 676: "Topology change,
not standing demotion: no CON edge touches the MAP"), so shadow fact
and MAP agreed forever. H5 added MAP supersession but left the shadow
fact in place; the combination is what kills the re-derivation story.

## 2. The exact query path: why the MAP key never misses

ev_query (lines 765-785):

```
fn ev_query(W:[]u8,s:i32,r:i32,expected:i32,flags:i32)i32 {
  hs(W,0,hg(W,0)+1); decay(W); ctx_push(W,s);
  let n:i32=activate(W,s,r);
  if(n>=0){
    link_edge(W,n,6,n,0); ref_prot(W,n);
    log_ev(W,2,s,r,ng(W,n,28),1,0,0); return ng(W,n,28);
  }
  ...
  // trial loop first (learner-set miss policy)
  let ans:i32=mp_run(W,s,r,expected,flags);
  if(ans!=-2){log_ev(W,2,s,r,ans,1,0,0); return ans;}
  ...
}
```

activate (lines 150-161):

```
fn activate(W:[]u8,s:i32,r:i32)i32 {
  let best:i32=-1; let bb:i32=-1; let n:i32=2;
  while(n<1024){
    if(ng(W,n,36)==1 && ng(W,n,0)==1 && is_superseded(W,n)==0){
      if(ng(W,n,20)==s && ng(W,n,24)==r){
        let b:i32=bid(W,n);
        if(b>bb){bb=b; best=n;}
      }
    }
    n=n+1;
  }
  return best;
}
```

The decisive filter is line 153: `ng(W,n,0)==1`. activate scans
tag-1 facts ONLY. A tag-20 MAP node can never be returned, superseded
or not. On the MAP key (52101,5203), the live shadow fact N 14 always
qualifies, so `n>=0`, and ev_query returns `ng(W,n,28)` (line 770)
without ever reaching mp_run (line 777). The key therefore never
misses; the trial loop never runs; no fresh MAP is ever promoted for
MAP keys. The prereg 3.6 story ("on the next miss for the key,
ev_query's trial loop (mp_run) runs against live facts and
promote_graph creates a fresh MAP") depends on a miss that the
unchanged activate + promote_graph make impossible. The prereg itself
froze this in: "What is explicitly NOT changed: ... activate lookup
logic, promote_graph, ev_teach_in, ..." (PREREG_H5.md, section 3.6
area).

## 3. Inertness proof: MAP supersession is write-only

Write paths that touch tag-20 MAP nodes:

- promote_graph line 545-546 (creation; field28=ans written once, never
  patched afterward).
- revise_on_contradict line 699 (`if(hit==1){supersede(W,m);}`), reached
  via ev_observe on a licensing fact's key. KB-W2 measured this:
  mapCON-delta=1 on all four C1 double-contradiction probes.
- contradict_map (lines 588-590): called only in dev tests t_p7
  (line 1143) and t_xcap (line 1193), never on the cognition path.

Read paths that consult tag-20 MAP nodes or MAP CON edges: NONE.

- activate requires tag==1 (line 153); MAPs are invisible to it.
- t2_trial's gather helpers (inc_fill lines 556-566, comb_present,
  t2_rels, t2_chain) scan tag-1 facts (and tag-8 combination nodes);
  candidate graphs are built fresh from facts, never by consulting
  existing MAPs.
- map_standing (lines 578-587) is called only in the dev tests above
  and in the sealed white-box counter sw_map_con; it is not on any
  query or action path.
- ev_act scans POLICY_ROOT-linked guide candidates (tag-1), skipping
  superseded ones; it never reads MAP nodes or MAP CON edges.
- ev_query is the single query entry point (grep confirms no other
  query/lookup/recall function); it reads only activate's tag-1 result.

Therefore the CON self-edges written on MAPs (is_superseded checks for
a type-3 self-edge, lines 136-141; supersede writes it at lines
146-149) change no query outcome, no action selection, and no trial
behavior on any probed path. The supersession is behaviorally inert:
write-only evidence. The bridge-query answers (100/900) come from the
shadow fact's field28, not from the MAP node.

The dev test t_t2_revise (line 1262) documents the intended design
("The MAP and the contradicted fact are superseded; re-derivation is
left to the trial loop on a later miss") but only ever re-queries the
FACT key (line ~1289: `ev_query(W,102,12,-2,0)`), never the MAP key
(101,40), so it cannot detect that the later miss never happens.

## 4. Bug or load-bearing design?

Both, at different levels.

Load-bearing for the current query contract. The shadow fact is the
ONLY retrieval handle for promoted answers: with activate fact-keyed
by frozen design, a promoted MAP without its shadow fact is
unreachable. If the shadow fact were simply not taught, MAP-key
queries would miss every time: activate finds nothing; mp_run's
t2_try_verify (lines 507-518) rejects all candidates when unmasked
with expected==-2 (line 514: `if(expected!=-2 && v==expected)` can
never match); bootstrap_miss finds no tag-1 facts on the key
(cnt<2, returns -2); miss_inquire would then construct UNCERTAINTY
nodes and POLICY_ROOT guides on every promoted-key query. The bridge
query (expected=-2, flags=0) would return -2, not a corrected value.
So naive removal breaks the query contract and spams the Change-2
inquiry machinery; the shadow fact is doing real load-bearing work as
the retrieval cache.

A bug relative to H5's hypothesis. The hypothesis requires the
supersession (on the MAP) to drive revision (re-derivation on the next
miss), but the read path consults the shadow fact, which the write
path ignores. Two structures represent the same knowledge; the
invalidation signal and the retrieval handle are wired to different
ones. H5's own Q1 ruling deleted the in-place patch schema
(t2_revise_graph) in favor of "supersede + re-derive on next miss",
yet left the shadow fact guaranteeing the miss never comes. The
prereg froze the defeat mechanism as "NOT changed".

Fix sketch (principle only, not implemented):

- Option A (one-system-rule aligned): make the MAP node itself the
  retrieval structure. Teach no shadow fact; extend activate to admit
  non-superseded tag-20 MAPs on the key, answering from field28 or by
  re-executing the field20 graph. Then revise_on_contradict's
  supersession removes the MAP from candidacy, the key genuinely
  misses, mp_run re-derives against live facts, promote_graph creates
  a fresh MAP. One structure, one read path; supersession becomes
  load-bearing; the duplicated representation is removed rather than
  patched.
- Option B: keep the shadow fact as a cache but link it to its MAP
  (provenance edge either direction) and extend revise_on_contradict
  to supersede the shadow when its MAP is superseded (cache
  invalidation in learner state, no new modes). The key then genuinely
  misses and re-derivation fires.
- Option C (rejected): patch the shadow fact's field28 in place on
  contradiction. This is the deleted t2_revise_graph schema by another
  name and contradicts H5's own Q1 ruling; it also would not re-derive
  the graph.

## 5. What a future H5 re-prereg must specify

Per the red-team requirements, the fresh prereg must:

1. Pin the query key explicitly. Any M3-W2/M3-W3 analog must probe the
   MAP key (the 1421pdt placement: QUERY on the promoted key), not the
   fact key. KB-B2/KB-B3 as operationalized on fact keys pass on
   unmodified TNN-2 (non-discriminating); they must be dropped or
   re-anchored to the MAP key.

2. Confront the shadow-fact root cause with frozen bars, not prose.
   Minimum: a white-box frozen bar that at MAP-key probe time counts
   live tag-1 facts on (s,r) and requires the count to be 0 (or
   requires the answering structure to be the MAP node itself), plus a
   behavioral frozen bar that the MAP-key query returns the
   twice-corrected value after fact-key contradiction, with the
   re-derivation path demonstrated to fire (trial stats showing the
   re-derivation run, or a fresh post-contradiction MAP node whose DEP
   edges anchor to live fact nodes). The prereg must not list
   activate, promote_graph, or ev_teach_in as "NOT changed" while
   claiming re-derivation on MAP keys.

3. Promote selectivity assertions to frozen bars: exact CON counts
   with named structure identity (not >=1 deltas), control-live, and
   wrong-key-resolves-nothing, all as frozen behavioral/white-box bars
   rather than supplementary observations.

4. State the invalidation contract explicitly: which structure the
   read path consults and which structure the supersession writes must
   be the same structure, or the prereg must specify the cache
   invalidation mechanism and bar its firing. A MAP supersession claim
   with no MAP-key read path is a white-box write claim, not a
   cognition claim, and must be labeled as such.

## Evidence index

- tnn3_h5.zag line 551: shadow fact taught (promote_graph).
- tnn3_h5.zag line 153: activate tag-1-only filter.
- tnn3_h5.zag line 770: ev_query returns shadow fact's field28.
- tnn3_h5.zag lines 692-699: MAP supersession writer (revise_on_contradict).
- tnn3_h5.zag lines 136-149: is_superseded / supersede.
- tnn3_h5.zag lines 507-518: t2_try_verify (expected==-2 rejects all unmasked).
- tnn2_build/tnn2.zag lines 533-542, 676: identical shadow fact in frozen baseline; "no CON edge touches the MAP".
- PREREG_H5.md section 3.6: re-derivation story and "NOT changed" list.
- sealed/w_c1.zag lines 1675-1724: sw_c1_double, bridge query.
- sealed/runs/c1_run1.txt line 16: C1S bridge-query=100; dump N 13 (MAP) / N 14 (shadow fact).
- REDTEAM_REVIEW.md Attack 3: independent verification of S1.
