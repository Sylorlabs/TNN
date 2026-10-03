# FROZEN PREREG: H5R2-SKEPTIC2, the stronger skeptic and chained decoy worlds

Lane: H5R2-SKEPTIC2, wave-20261001-2321pdt. Status: FROZEN PREREG.

Lineage: H5R2-DECOY reached DECOY-DISCRIMINATES (EVAL_DECOY.md):
H5R2 8/8, REVERT-TO-LATEST 0/8 (8/8 D-DECOY-FAIL), NO-GATE 0/8
(8/8 D-DEP-FAIL), RANDOM-ANCHOR 2/8. The decoy lane recommended
building the stronger skeptic that could plausibly survive the decoy
worlds. This lane builds it and scales the decoy family to chained
decoys (decoy OBSERVEs at multiple chain levels), where the
discrimination must hold at every level.

ORDERING RULE: this prereg is committed (with NAMECHECK.md) before any
implementation file is written. Any skeptic or world artifact whose
mtime predates the prereg freeze commit is UNVERIFIABLE ORDERING and
the comparison is VOID. Kill bars never move after freezing.

## 1. The stronger skeptic: NEWEST-LIVE-ON-KEY

Choice: candidate (a). It is the strongest of the two candidates
because it is the only one that can pass the simple decoy worlds: the
decoy fact lives on an unrelated key, so per-key newest-live anchoring
selects the reverted fact on K exactly as the gate does. Candidate (b)
LIVE-BUT-NO-SUPERSESSION-GATE is rejected as the pick because ignoring
supersession edges makes superseded facts look live, so the trial
promotes the first verifying candidate in node-id order (the stale
original fact): it collapses to NO-GATE behavior and would score 0/8,
weaker than RANDOM-ANCHOR. A skeptic that cannot survive worlds the
gate already survived proves nothing about the gate's necessity.

Exact algorithm (frozen): the H5R2 trial loop with t2_prov_ok replaced
by t2_newest_live_ok. A candidate chain may be promoted iff it
verifies AND every licensing fact fnn satisfies sk2_newest_on_key:
fnn is live tag-1, non-superseded, and no other node g with
ng(W,g,36)==1, ng(W,g,0)==1, ng(W,g,20)==ng(W,fnn,20),
ng(W,g,24)==ng(W,fnn,24), is_superseded(W,g)==0 has g>fnn. Node ids
increase in creation order (alloc_node scans upward; supersession never
frees nodes), so "no higher live id on the key" is exactly "newest live
fact on the (subject, relation) key". Enumeration order is unchanged
(forward, node-id order); only the eligibility predicate changes. The
four t2_trial promote sites call t2_newest_live_ok instead of
t2_prov_ok. Exact replacement code is in the appendix. The substrate is
otherwise byte-identical to H5R2.

Why it differs from t2_prov_ok only on supersession chains: the gate
accepts any all-live lineage and takes the first in node-id order; the
skeptic additionally requires each licensing fact to be the newest
live fact on its key. On every world family run so far each key holds
at most one live fact, so the two coincide there; the chained family
tests whether they still coincide when decoys exist at both chain
levels.

## 2. Chained decoy world family (frozen spec)

Per chained probe (tag EiPj), with chain relations RF1/RF2, MAP
relation RM, a-level decoy relation RD1, b-level decoy relation RD2,
all fresh per world:

1. ev_teach(a,RF1,b); ev_teach(b,RF2,c0).
2. QUERY(a,RM,c0): promote MAP1 (probe P1, full h5r2_probe protocol).
3. ev_observe(b,RF2,c1): contradiction on K=(b,RF2).
4. QUERY(a,RM,c1): promote MAP2 (probe P2).
5. ev_observe(b,RF2,c0): REVERT, teaches the new live fact on K.
6. ev_observe(a,RD1,b): DECOY at chain level 1 (the a-link). Newer
   live fact with object b on the unrelated key (a,RD1).
7. Decoy answerability, a-level: QUERY(a,RD1,b) must return b
   (D-ANS-A check). ev_query short-circuits via activate on the live
   decoy fact; no MAP is promoted, on every arm identically.
8. ev_observe(b,RD2,c0): DECOY at chain level 2 (the b-link). Newer
   live fact with object c0 on the unrelated key (b,RD2).
9. Decoy answerability, b-level: QUERY(b,RD2,c0) must return c0
   (D-ANS-B check).
10. QUERY(a,RM,c0): promote MAP3, the revert MAP (probe P3).
11. White-box CD-check on the live MAP (section 3).

Frozen constraints: no OBSERVE on any MAP key after its MAP exists;
per-probe (subject, relation) ranges disjoint within each world; key
ranges 89xxx-90xxx, disjoint from FW1-FW9 (3xxxx), the 1421pdt battery
(43xxx), the killed H5 battery (51xxx-54xxx), the killed H5R battery
(61xxx-65xxx, 71xxx-72xxx), the H5R2 sealed battery (83xxx-86xxx), the
decoy family (87xxx-88xxx), and all smoke keys.

### Seeds (frozen before implementation; SHA-256 inputs recorded here)

- e1: "TNN3H5R2|wave-20261001-2321pdt|chaindecoy1" ->
  ebc12e57333f2958d347be6005a3fbb249aaf2816d9fbb889e9366694dc6fb42 ->
  first 4 hex "ebc1" = 60353 -> vo = 60353 mod 7 = 6
- e2: "TNN3H5R2|wave-20261001-2321pdt|chaindecoy2" ->
  d406f746e25a98722273f8dbd4d8fc452713475452000a9ac0cb00b873624a42 ->
  first 4 hex "d406" = 54278 -> vo = 54278 mod 7 = 0

Object values: c0 = base + vo + 10*i (i = 0..3 per probe), c1 = c0+1,
with base 89401 (e1) / 90401 (e2).

### World e1 (chain 8901/8902, MAP 8903, b-decoy 8904, a-decoy 8905)

- E1P1: a=89101 b=89301 c0=89407 c1=89408
- E1P2: a=89102 b=89302 c0=89417 c1=89418
- E1P3: a=89103 b=89303 c0=89427 c1=89428
- E1P4: a=89104 b=89304 c0=89437 c1=89438

### World e2 (chain 9001/9002, MAP 9003, b-decoy 9004, a-decoy 9005)

Materially different relation family and subject distribution from e1.

- E2P1: a=90101 b=90301 c0=90401 c1=90402
- E2P2: a=90102 b=90302 c0=90411 c1=90412
- E2P3: a=90103 b=90303 c0=90421 c1=90422
- E2P4: a=90104 b=90304 c0=90431 c1=90432

8 chained probes total (N=8, satisfies N>=8).

## 3. The CD-check (frozen white-box bar, per probe)

On the live MAP for (a,RM) after step 10, with decoy_a found as the
single live tag-1 fact on (a,RD1), decoy_b as the single live tag-1
fact on (b,RD2), klive as the single live tag-1 fact on (b,RF2), and
alive as the single live tag-1 fact on (a,RF1):

- exactly 2 superseded MAPs on (a,RM); exactly 1 live MAP with
  f28==c0 (else CD-SUP-FAIL / CD-LIVE-FAIL / CD-F28-FAIL);
- decoy_a>=0 and decoy_b>=0 (else CD-DECOYID-FAIL);
- every DEP (type-1) edge target of the live MAP is live tag-1
  non-superseded (else CD-DEP-FAIL);
- no DEP edge target is decoy_a or decoy_b (else CD-DECOY-FAIL; the
  pre-registered recency failure signature, now required to be absent
  at BOTH chain levels);
- at least one DEP edge target is klive (else CD-KEY-FAIL: wrong
  b-level anchor);
- at least one DEP edge target is alive (else CD-AKEY-FAIL: wrong
  a-level anchor).

"CD ok" is emitted only if all conjuncts pass. The discrimination must
hold at every chain level: a MAP that anchors correctly at the b-link
but takes the a-level decoy fails via CD-AKEY-FAIL just as surely as a
b-level decoy anchor fails via CD-DECOY-FAIL.

## 4. Compared arms (sources extracted read-only from recorded commits)

- H5R2: source extracted via git show from
  9db334bd4a01d21cce52da3bb2a1c45a10c4c172, SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a
  (must match before use).
- NEWEST-LIVE-ON-KEY: built in this lane from the H5R2 base per the
  appendix (diff-verified: only the gate regions differ).
- REVERT-TO-LATEST, NO-GATE, RANDOM-ANCHOR: sources extracted via git
  show from 1203b865d352ae8ba380f57350218edd4d637b3a; SHA-256
  d929d50c3b3499b4c1b17bcd9e1319eecf4044f9fb96125e01de35ad1d520220,
  d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384,
  c03b4575993ecbdb3a851c75972f4281e210340f90d0c7c6622b8160cf1a0ee1
  (must match before use). Do NOT rebuild from working files.

## 5. Frozen kill bars

SB-1 (gate holds at every level): H5R2 emits "CD ok" on 8/8 chained
probes: every revert MAP anchors DEP edges to the live tag-1 facts on
both chain keys, never either decoy, never a superseded fact.

SB-2 (stronger skeptic, pre-registered): the skeptic is expected to
MATCH H5R2. SB-2-MATCH: NEWEST-LIVE-ON-KEY emits "CD ok" on 8/8
chained probes. Rationale recorded before any run: on each chained
probe the gate's promoted candidate [via the (a,RF1) fact, via the
reverted (b,RF2) fact] is also the skeptic's first verifying eligible
candidate, because each of those facts is the newest live fact on its
key and the decoy facts live on unrelated keys. SB-2-FAIL-SIG (the
pre-registered failure signature): "CD ok" <= 3/8 with
(CD-DECOY-FAIL + CD-AKEY-FAIL) >= 5/8, i.e. the skeptic anchors to a
decoy fact at one of the two chain levels. Any other failure pattern
is UNEXPECTED-SIGNATURE and yields no verdict.

SB-3 (old arms behave as before): REVERT-TO-LATEST 0/8 "CD ok" with
CD-DECOY-FAIL on a frozen majority (>=5/8; expected 8/8, anchoring to
the decoy facts at both levels); NO-GATE 0/8 "CD ok" via CD-DEP-FAIL
to the superseded original fact (expected 8/8); RANDOM-ANCHOR does not
reach 8/8 "CD ok" (chance-level over 6 verifying candidates, expected
about 1-2/8).

SB-4 (determinism): 3/3 byte-identical full-stdout runs per arm per
world, SHA-256 compared (the KB-D1 protocol).

SB-5 (decoy genuineness): D-ANS-A ok and D-ANS-B ok on all 8 probes on
all 5 arms (target 16 answerability markers per arm: 8 a-level, 8
b-level). Any D-ANS failure makes the affected world VOID as
adversarial-by-brokenness.

## 6. Frozen decision rule

- SKEPTIC-SURVIVES iff SB-1 and SB-2-MATCH and SB-3 and SB-4 and SB-5
  all hold: the stronger skeptic matches H5R2 on the chained family;
  the gate's necessity is still unproven against THIS skeptic. Report
  honestly; name the next discriminating world family that could
  separate newest-live-on-key from the gate (one where the node-id-
  first all-live candidate licenses a live-but-not-newest fact on some
  key while the key-newest fact licenses a later candidate).
- GATE-STILL-NECESSARY iff SB-1 and SB-2-FAIL-SIG and SB-3 and SB-4
  and SB-5 all hold: the gate survives its strongest available
  skeptic.
- Otherwise INCONCLUSIVE: report the exact per-arm per-bar numbers
  with hashes; no verdict claimed.

## 7. Worlds and evaluation protocol (frozen)

7.1. Assembly per arm per world (10 worlds), after the implementation
commit, by the frozen rule: byte-copy of the arm substrate with the
single line `fn main()i32 { return run_all(); }` changed to
`fn main()i32 { return sealed_main(); }` (verified by diff: exactly
one line differs), plus the frozen DRIVER_TMPL.zag appended (SHA-256
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af,
extracted from 9db334bd4), plus the frozen CHAIN_FRAG.zag appended
(SHA-256 recorded before assembly), plus one alias line selecting the
world (`fn sealed_main()i32 { return sealed_main_e1(); }`, etc.).

7.2. World file SHA-256s recorded before any run. Each world compiled
separately with the pinned znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1); 3/3 runs;
full-stdout SHA-256 compared per world (SB-4).

7.3. Scoring uses the driver's own markers: "CD ok" (target 8: 4 per
world), "D-ANS-A ok" (target 8), "D-ANS-B ok" (target 8),
"CD-DECOY-FAIL" / "CD-DEP-FAIL" / "CD-KEY-FAIL" / "CD-AKEY-FAIL" /
"CD-SUP-FAIL" / "CD-LIVE-FAIL" / "CD-F28-FAIL" / "CD-DECOYID-FAIL"
counts, VAL-FAIL, and zero unexpected FAIL marker lines. The canonical
full state dump ends each world for SB-4.

7.4. Negative controls: NC-S0 (a world file is not a valid assembly
per 7.1: that arm is VOID, not scored); NC-S1 (any
forbidden-executable invocation: PROCESS-FAIL, terminal); NC-S2
(prereg freeze does not strictly precede implementation: UNVERIFIABLE
ORDERING, VOID).

## 8. Pure-Zag construction

Builder PATH is $HOME/safebin (36 tools, no python3, verified at lane
startup and recorded in NAMECHECK.md Step 0). All research logic is
Zag compiled/run with the pinned znc. Shell is used only to invoke
znc, run binaries, do git ops, and move/copy files.

## 9. Documentation

No em-dashes in any lane documentation. Every doc is checked with
sh docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
before commit.

## Appendix: exact skeptic gate replacement (frozen)

In bl_newest.zag, the t2_prov_ok comment block and function

```
// Provenance gate (H5R2): a superseded fact licenses nothing. Candidate
// chains may only be promoted from live, non-superseded facts, so a
// revert MAP anchors DEP edges to the current (post-revision) fact and
// never to a superseded fact. The trial loop carries provenance forward
// through each revision step.
fn t2_prov_ok(W:[]u8,f:[]u8,nf:i32)i32 {
  let i:i32=0;
  while(i<nf){
    let fnn:i32=get32(f,i*4);
    if(ng(W,fnn,36)!=1 || ng(W,fnn,0)!=1 || is_superseded(W,fnn)==1){return 0;}
    i=i+1;
  }
  return 1;
}
```

is replaced by

```
// Stronger skeptic (SKEPTIC2): NEWEST-LIVE-ON-KEY. A candidate may only be
// promoted from facts that are each the newest live non-superseded fact on
// their (subject, relation) key. Node ids increase in creation order, so
// "newest" is the highest node id among live non-superseded facts sharing
// the key. Unlike t2_prov_ok, an older-but-live fact never licenses a
// candidate; unlike recency, a newer fact on an unrelated key is irrelevant
// because keys are per (subject, relation).
fn sk2_newest_on_key(W:[]u8,fnn:i32)i32 {
  if(ng(W,fnn,36)!=1 || ng(W,fnn,0)!=1 || is_superseded(W,fnn)==1){return 0;}
  let s:i32=ng(W,fnn,20); let r:i32=ng(W,fnn,24);
  let g:i32=fnn+1;
  while(g<1024){
    if(ng(W,g,36)==1 && ng(W,g,0)==1 && ng(W,g,20)==s && ng(W,g,24)==r && is_superseded(W,g)==0){return 0;}
    g=g+1;
  }
  return 1;
}
fn t2_newest_live_ok(W:[]u8,f:[]u8,nf:i32)i32 {
  let i:i32=0;
  while(i<nf){
    if(sk2_newest_on_key(W,get32(f,i*4))==0){return 0;}
    i=i+1;
  }
  return 1;
}
```

and the four t2_trial call sites change `t2_prov_ok(` to
`t2_newest_live_ok(`. Diff of bl_newest.zag vs the verified H5R2 base
must show only these regions changed.
