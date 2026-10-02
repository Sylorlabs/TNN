# FROZEN PREREG: H5R2-SYNTH, the newest-live-among-all-live gate test

Lane: HPI, wave-20261002-0221pdt. Status: FROZEN PREREG.

Lineage: the 2321pdt H5R2-SYNTHESIS named the next hypothesis: test
whether a newest-live-among-all-live gate discriminates better than
the existing gates on tied-provenance conflicts. H5R2 is SEPARATED
with a mandatory scope boundary (debate Q5 UPHOLD): the re-teach
separator family is an explicit open gap, not a retroactive bar move;
no general provenance-policy citation; oldest-first is an enumeration
artifact. The 2321pdt record carries an honest caveat: the separator
family discriminates tie-breaking policies without crowning one. This
lane builds the named gate, tests it against the frozen
no-regression suite plus new tied-provenance discrimination trials,
and red-teams it.

ORDERING RULE: this prereg is committed (with NAMECHECK.md) before
any implementation file is written. Any synth artifact whose mtime
predates the prereg freeze commit is UNVERIFIABLE ORDERING and the
comparison is VOID. Kill bars never move after freezing.

## 1. Question under test

Does the SYNTH gate (arm S), newest-live tie-breaking among all
verifying candidates under the H5R2 provenance filter, resolve
strictly more tied-provenance conflicts than either existing gate
(H5R2, arm H; NEWEST-LIVE-ON-KEY, arm N) without regressing the H5R2
sealed suite?

## 2. Exact gate definition (frozen)

Eligibility: the unchanged H5R2 filter. A candidate with licensing
facts f[0..nf-1] is eligible iff every fact is live tag-1
non-superseded: ng(W,fnn,36)==1 and ng(W,fnn,0)==1 and
is_superseded(W,fnn)==0.

Selection: among all verifying eligible candidates in a promote
site, promote the one whose licensing set has the highest maximum
node id (the newest live licensing fact); ties are broken by the
site's enumeration order (chain site: k ascending 2..4, then path
order; sum site: subset size descending, then mask descending; count
site: relation order; single-hop site: path order). This is
newest-live among all live licensing facts: the promoted candidate is
always licensed by the globally newest live fact appearing in any
verifying eligible candidate's licensing set; when several candidates
share that fact, the first in enumeration order wins.

The four t2_trial promote sites are restructured from
first-verifying early-exit to best-selection within the site; site
order (chains k=2..4, then sums, then counts, then single hops) is
unchanged. Exact replacement code is in the appendix. The substrate is
otherwise byte-identical to H5R2 (diff-verified: only the gate
function and the four site loops differ).

Frozen differences from the existing gates:
- vs H5R2 (t2_prov_ok): the filter is identical; oldest-first (first
  in node-id enumeration order) is dropped in favor of newest-first.
- vs NEWEST-LIVE-ON-KEY (t2_newest_live_ok): the per-key newest-live
  requirement is dropped; a newer fact on an unrelated key can win
  the tie-break. On keys holding exactly one live fact the two
  skeptics coincide in eligibility and differ only in selection
  order.

## 3. Compared arms (sources extracted read-only from recorded commits)

- H (H5R2): source extracted via git show from
  9db334bd4a01d21cce52da3bb2a1c45a10c4c172, SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a
  (must match before use).
- N (NEWEST-LIVE-ON-KEY): source extracted via git show from
  f461e812d (bl_newest.zag), SHA-256
  e5df3ddb28858b60efb01f3d8df524a98ce79686e199532e53713c24f367b649
  (must match before use). Do NOT rebuild from working files.
- S (SYNTH): built in this lane from the H5R2 base per the appendix,
  after this prereg's freeze commit (diff-verified: only the gate
  regions differ).

## 4. No-regression suite (frozen; reused sealed families)

The S arm runs the frozen sealed families via the frozen 11.1
assembly rule, reusing the recorded fragments (hashes verified before
assembly):
- Separator s1/s2: SEP_FRAG.zag, SHA-256
  65875ee5ea47dbb0866e9611204739c3d8b3c494f84e1f93d84a1327221447c2.
  Bar: S emits SEP-NEW on 8/8 probes (N recorded 8/8 SEP-NEW; H
  recorded 8/8 SEP-OLD).
- Decoy d1/d2: DECOY_FRAG.zag, SHA-256
  6acc0965bc456e17229c24c6e7859b0a0dc5533c74e3b81f5708848014f99a6f.
  Bar: S emits "D ok" on 8/8 probes (H and N recorded 8/8).
- Chained e1/e2: CHAIN_FRAG.zag, SHA-256
  6d3c767600bf06340d7d6eafd6a8b4317114df0feab4a70fed810f832552abd1.
  Bar: S emits "CD ok" on 8/8 probes (H and N recorded 8/8).
- Built-in battery: S substrate with main=run_all, 3/3 runs. Bar:
  46/46 (H and N recorded 46/46).

DRIVER_TMPL.zag for all assemblies: SHA-256
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af.

## 5. Discrimination trials: tied-provenance conflicts (frozen spec)

Rationale: the trials must be conflicts where both existing gates TIE
(agree), so that a strict improvement by S is measurable. Per the
frozen analysis, on a tied-provenance conflict (two verifying
all-live all-key-newest candidates) the protocol-grounded correctness
criterion is the frozen F2 semantics of the built-in battery: the
masked query prefers the composition-preserving (first-taught)
reading. No independent criterion crowns the newer reading there; the
prereg does not invent one.

Per DT probe (tag TwPp), with chain relations R1/R2/R3/R4 and MAP
relation RM, all fresh per world:
1. ev_teach(s,R1,m1): fact Fa on (s,R1).
2. ev_teach(m1,R2,o1): fact Fb on (m1,R2).
3. ev_teach(s,R3,m2): fact Fc on (s,R3).
4. ev_teach(m2,R4,o2): fact Fd on (m2,R4).
5. QUERY(s,RM,-2,1): masked probe (flags=1). Both candidates [Fa,Fb]
   (answer o1) and [Fc,Fd] (answer o2) verify and are all-live
   all-key-newest, so H and N tie on the first-enumerated candidate.
6. White-box DT-check on the live MAP (arm-neutral): exactly 1 live
   MAP on (s,RM); exactly 2 DEP edges, one to the single live fact on
   (s,R1) or (s,R3) and one to the single live fact on (m1,R2) or
   (m2,R4); MAP f28 == query answer v == object of the anchored
   second-link fact. "DT ok" is emitted iff all conjuncts pass; then
   "DT-FIRST" if the anchored pair is {Fa,Fb} (v=o1), "DT-LATER" if
   {Fc,Fd} (v=o2).

Frozen favored answer: DT-FIRST (o1), the first-taught
composition-preserving reading, per the frozen F2 semantics. This
extends the battery's own disambiguation semantics to fresh keys; it
does not move any frozen bar.

Frozen constraints: no OBSERVE on any key in any DT world; no OBSERVE
on any MAP key; per-probe (subject, relation) ranges disjoint within
each world; key ranges 93xxx-94xxx, disjoint from FW1-FW9 (3xxxx),
the 1421pdt battery (43xxx), the killed H5 battery (51xxx-54xxx), the
killed H5R battery (61xxx-65xxx, 71xxx-72xxx), the H5R2 sealed battery
(83xxx-86xxx), the decoy family (87xxx-88xxx), the chained decoy
family (89xxx-90xxx), the separator family (91xxx-92xxx), and all
smoke keys.

Seeds (frozen before implementation; SHA-256 computed pre-freeze):
- t1: "TNN3H5R2|wave-20261002-0221pdt|synth-dt1" -> debb -> 57019 ->
  vo = 57019 mod 7 = 4
- t2: "TNN3H5R2|wave-20261002-0221pdt|synth-dt2" -> abbb -> 43963 ->
  vo = 43963 mod 7 = 3
Object values: o1 = base + vo + 10*i (i = 0..3 per probe),
o2 = o1+1, with base 93401 (t1) / 94401 (t2).

World t1 (chain 9301/9302/9303/9304, MAP 9305):
- T1P1: s=93101 m1=93301 m2=93351 o1=93405 o2=93406
- T1P2: s=93102 m1=93302 m2=93352 o1=93415 o2=93416
- T1P3: s=93103 m1=93303 m2=93353 o1=93425 o2=93426
- T1P4: s=93104 m1=93304 m2=93354 o1=93435 o2=93436

World t2 (chain 9401/9402/9403/9404, MAP 9405):
- T2P1: s=94101 m1=94301 m2=94351 o1=94404 o2=94405
- T2P2: s=94102 m1=94302 m2=94352 o1=94414 o2=94415
- T2P3: s=94103 m1=94303 m2=94353 o1=94424 o2=94425
- T2P4: s=94104 m1=94304 m2=94354 o1=94434 o2=94435

8 DT probes total (N=8). All three arms run both DT worlds (the H/N
tie is measured, not assumed).

DT frag: DT_FRAG.zag is written post-freeze to this spec (probe
functions, sealed_main_t1/sealed_main_t2, arm-neutral markers,
canonical state dump); its SHA-256 is recorded in SEALED_EVAL.md
before any DT run.

## 6. Frozen kill bars

SYN-NR-SEP: S emits SEP-NEW on 8/8 separator probes.
SYN-NR-DECOY: S emits "D ok" on 8/8 decoy probes.
SYN-NR-CHAIN: S emits "CD ok" on 8/8 chained probes.
SYN-NR-BATT: S scores 46/46 on the built-in battery.
SYN-DT: on the 8 DT probes, S_DT-FIRST_count >
max(H_DT-FIRST_count, N_DT-FIRST_count), with "DT ok" on 8/8 probes
on all three arms (world validity).
SYN-DET: 3/3 byte-identical full-stdout runs per arm per world
(battery, s1/s2, d1/d2, e1/e2, t1/t2), SHA-256 compared.
SYN-PURE: pure Zag only; zero forbidden-executable invocations
(automatic PROCESS-FAIL); zero em/en dashes in lane docs
(check_no_dash.sh before every commit).
SYN-ORDER: this prereg's freeze commit strictly precedes every synth
implementation artifact (mtime and commit order); violation is
UNVERIFIABLE ORDERING, VOID.
SYN-SCOPE (debate Q5 boundary): the verdict and all lane docs (a) do
not re-litigate H5R2's BUILD-PASS, (b) name the re-teach separator
family as an explicit open gap, not a retroactive bar, (c) make no
general provenance-policy claim beyond the tested families and the
three named tie-breaking rules, (d) name oldest-first and
newest-first both as enumeration artifacts. Violation voids the
verdict.
SYN-ARCH: no protected-core change; S is a substrate variant only.
Record new_semantic_cases=0, modes/bridges/handlers added=0, and the
cognition source delta (lines changed vs the H5R2 base).

## 7. Frozen decision rule

BUILD-PASS iff every bar in section 6 holds. BUILD-FAIL otherwise,
with the exact per-arm per-bar numbers reported honestly. No other
verdict text is permitted on the VERDICT lines.

## 8. Pre-registered expectations (not kill bars; recorded for honesty)

- S on separator: 8/8 SEP-NEW (agrees with N; the newest fact on K
  wins the tie-break).
- S on decoy: 0/8 "D ok", 8/8 D-DECOY-FAIL: the decoy fact is the
  newest live fact in every verifying candidate's licensing set, so S
  anchors every revert MAP to the decoy. This is the pre-registered
  newest-bias failure signature.
- S on chained: 0/8 "CD ok", 8/8 CD-DECOY-FAIL at both levels.
- S on battery: 45/46, failing exactly t_f2 (the masked query
  promotes the later-taught 2-hop reading [F2,F4] -> 202 instead of
  201).
- DT: H 8/8 DT-FIRST, N 8/8 DT-FIRST (tie), S 0/8 DT-FIRST (8/8
  DT-LATER). SYN-DT then fails as 0 > 8.
- Expected overall: BUILD-FAIL via SYN-NR-DECOY, SYN-NR-CHAIN,
  SYN-NR-BATT, SYN-DT. An honest BUILD-FAIL is the informative
  outcome: it would show the named synthesis hypothesis is
  newest-biased in exactly the way the decoy family was built to
  punish, and that no pure tie-breaking rule strictly dominates both
  existing gates on the frozen families.

## 9. Pre-registered red-team self-attack

Attack 1 (relabeling ties): on every tied-provenance conflict the
only protocol-grounded correctness criterion (the update-reading on
same-key revisions) forces H and N to diverge rather than tie; where
they tie, no criterion crowns S's answer. S would therefore relabel
ties, not resolve them. The DT family tests this: if S cannot beat
the H/N tie on DT-FIRST, the attack stands.

Attack 2 (newest-bias): the decoy family was designed so that the
newest live fact is the wrong anchor. Any newest-flavored rule,
including S, must fail it. Passing the separator (newest wins) while
failing the decoy (newest loses) shows S is not a better provenance
policy but a bias that agrees with the update-reading on re-teach
keys and disagrees everywhere else.

Attack 3 (F2 regression): the built-in battery's F2 test freezes
composition-preserving (first-taught) order for masked
disambiguation. S breaks it. A gate that regresses the frozen battery
cannot be called strictly stronger.

If the experiment contradicts these attacks (S passes a bar
predicted to fail), the bars decide, not the predictions: report
honestly.

## 10. Q5 scope boundary (explicit; debate Q5 UPHOLD)

This lane does not re-litigate H5R2's BUILD-PASS: that verdict stands
within its frozen battery scope. The re-teach separator family
remains an explicit open gap in H5R2's scope, named as such, not a
retroactive bar move. No verdict in this lane claims any of the three
tie-breaking rules (oldest-first, per-key-newest, global-newest) is
the correct provenance policy in general; the verdict reports only
which rule won on the tested families. Oldest-first is an enumeration
artifact of forward node-id order (per Q5); newest-first is
symmetrically an artifact of the same order read backward. The
2321pdt honest caveat is carried: these families discriminate
tie-breaking policies without crowning one.

## 11. Worlds and evaluation protocol (frozen)

11.1. Assembly per arm per world, after the implementation commit,
by the frozen rule: byte-copy of the arm substrate with the single
line `fn main()i32 { return run_all(); }` changed to
`fn main()i32 { return sealed_main(); }` (verified by diff: exactly
one line differs), plus the frozen DRIVER_TMPL.zag appended (SHA-256
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af,
extracted from 9db334bd4), plus the frozen family FRAG appended
(hashes in section 4; DT_FRAG hash recorded in SEALED_EVAL.md before
any DT run), plus one alias line selecting the world
(`fn sealed_main()i32 { return sealed_main_s1(); }`, etc.).

11.2. World file SHA-256s recorded before any run. Each world
compiled separately with the pinned znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1); 3/3 runs;
full-stdout SHA-256 compared per world (SYN-DET).

11.3. Scoring uses the driver's own markers per the family preregs,
plus "DT ok" (target 8 per arm), "DT-FIRST" / "DT-LATER" (section 5),
and zero unexpected FAIL marker lines. The canonical full state dump
ends each world for SYN-DET.

11.4. Negative controls: NC-S0 (a world file is not a valid assembly
per 11.1: that arm is VOID, not scored); NC-S1 (any
forbidden-executable invocation: PROCESS-FAIL, terminal); NC-S2
(prereg freeze does not strictly precede implementation: UNVERIFIABLE
ORDERING, VOID).

## 12. Cost accounting (frozen)

S removes the first-verifying early exit: every promote site scans
all its candidates. The trial stats (header field 16:
tried/rejected) are recorded per world and reported; the expected
cost increase vs H5R2 is bounded by the candidate counts of the
sealed worlds (no asymptotic change: still linear in enumerated
candidates per site).

## 13. Pure-Zag construction

Builder PATH is $HOME/safebin (36 tools, no python3, verified at lane
startup and recorded in NAMECHECK.md Step 0). All research logic is
Zag compiled/run with the pinned znc. Shell is used only to invoke
znc, run binaries, do git ops, and move/copy files.

## 14. Documentation

No em-dashes in any lane documentation. Every doc is checked with
sh docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
before commit.

## Appendix: exact SYNTH gate replacement (frozen)

In synth.zag, the t2_prov_ok comment block and function (line 513 of
the verified H5R2 base) is replaced by:

```
// SYNTH gate (H5R2-SYNTH): NEWEST-LIVE-AMONG-ALL-LIVE. Eligibility is
// the unchanged H5R2 provenance filter: a superseded fact licenses
// nothing. Selection is newest-live among all live licensing facts:
// among the verifying eligible candidates in a promote site, the trial
// promotes the one whose licensing set contains the newest live fact
// (highest node id); the site's enumeration order breaks ties. Unlike
// t2_prov_ok, oldest-first is dropped; unlike NEWEST-LIVE-ON-KEY, a
// newer fact on an unrelated key can win.
fn synth_elig(W:[]u8,f:[]u8,nf:i32)i32 {
  let i:i32=0;
  while(i<nf){
    let fnn:i32=get32(f,i*4);
    if(ng(W,fnn,36)!=1 || ng(W,fnn,0)!=1 || is_superseded(W,fnn)==1){return 0;}
    i=i+1;
  }
  return 1;
}
fn synth_score(f:[]u8,nf:i32)i32 {
  let m:i32=-1; let i:i32=0;
  while(i<nf){ let fnn:i32=get32(f,i*4); if(fnn>m){m=fnn;} i=i+1; }
  return m;
}
```

and each of the four t2_trial promote sites (call sites at lines
631, 654, 670, 685 of the base) is restructured from first-verifying
early-exit to best-selection within the site. Chain site:

```
  if(dc==0){
    let bsc:i32=-1; let bv:i32=-2; let br:i32=-1; let bnf:i32=0;
    let bf:[]u8=z_alloc(16);
    let k:i32=2;
    while(k<=4){
      let p:i32=0;
      while(p<np){
        let base:i32=p*48;
        if(get32(paths,base)==k+1){
          let v:[]u8=z_alloc(24); let f:[]u8=z_alloc(16);
          let j:i32=0;
          while(j<=k){set32(v,j*4,get32(paths,base+4+j*4)); j=j+1;}
          j=0;
          while(j<k){set32(f,j*4,get32(paths,base+24+j*4)); j=j+1;}
          let root:i32=t2_asm_chain(W,v,k+1,f);
          let v2:i32=t2_try_verify(W,root,s,expected,masked,st);
          if(v2!=-2 && synth_elig(W,f,k)==1){
            let sc:i32=synth_score(f,k);
            if(sc>bsc){bsc=sc; bv=v2; br=root; bnf=k;
              let c:i32=0; while(c<k){set32(bf,c*4,get32(f,c*4)); c=c+1;}}
          }
        }
        p=p+1;
      }
      k=k+1;
    }
    if(bv!=-2){promote_graph(W,br,s,r,bv,bf,bnf); ans=bv;}
  }
```

Sum site: same restructure; best buffers bf=z_alloc(48), bnf=c;
the sz loop runs sz=m..1 and mask=(1<<m)-1..1 without the ans==-2
early exits; after the loops,
if(bv!=-2){promote_graph(W,br,s,r,bv,bf,bnf); ans=bv;}.

Count site: bf=z_alloc(60), bnf=len-1; per-relation scan without
early exit; promote best after the loop.

Single-hop site: bf=z_alloc(16), bnf=1; path scan without early
exit; promote best after the loop.

Site order (chains, then sums, then counts, then single hops) is
unchanged: a later site runs only if ans==-2 after the earlier
sites. Diff of synth.zag vs the verified H5R2 base must show only
the gate function and the four site loops changed.
