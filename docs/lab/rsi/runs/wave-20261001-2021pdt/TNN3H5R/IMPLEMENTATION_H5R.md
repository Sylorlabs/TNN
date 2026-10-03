# H5R Implementation Record: Option A substrate change

Lane TNN3H5R, wave-20261001-2021pdt. Implements the frozen prereg
PREREG_H5R.md (commit 67ed888e4, coordinator rulings Q1-Q5 all CONFIRM)
section 4 exactly. Pure Zag, safebin toolchain, no forbidden
executables (KB-P1 clean).

## Ordering and base verification (NC-7)

- Prereg freeze commit: 67ed888e4 (2026-10-02 04:14:04 UTC), committed
  alone. Implementation files in this lane were created after:
  NAMECHECK_IMPL.md 04:15:41 UTC, tnn3_h5r.zag 04:16:23 UTC,
  tnn3_h5r.bin 04:16:50 UTC. No implementation artifact predates the
  prereg freeze.
- Base: docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/tnn3_h5.zag.
  Worktree copy byte-identical to the git-committed version at the H5
  sealed-eval commit 6b4ed149e, SHA-256
  f83571a0285fa99f0b184a2773ebfb3e74cdc80c9c67e3fa98a46e91a0857706.
- Independent chain-of-custody check: the verified base file rebuilt
  with the pinned znc reproduces the frozen H5 binary record exactly:
  344ac89fb338ddbf46bea6be4c526d99410ea643278ab91fb06d76b7e33c4eb7
  (matches IMPLEMENTATION.md in TNN3H5). The base is the file that
  built the verified tnn3_h5.bin.
- Working file tnn3_h5r.zag created by byte-copy; copy SHA-256 verified
  identical to the base before any edit.

## Changes (prereg section 4, exact; Option A)

Hunk 1, promote_graph (was line 551): deleted
`ev_teach_in(W,s,r,ans);`. promote_graph now creates the tag-20 MAP
node only. Net -1 line. ev_teach_in itself unchanged (still used by
ev_observe and bootstrap_miss).

Hunk 2, activate (was lines 150-161): the tag filter is extended so a
node qualifies iff it is live, not superseded, and either (a) tag 1
with (f20,f24)==(s,r) (the unchanged fact path), or (b) tag 20 with
(f8,f4)==(s,r) (the new MAP path). Net +3 lines (5 added, 2 removed),
within the +10 budget. The answer still comes from f28 in ev_query
(unchanged). Implementation uses an `ok` predicate variable:

```
fn activate(W:[]u8,s:i32,r:i32)i32 {
  let best:i32=-1; let bb:i32=-1; let n:i32=2;
  while(n<1024){
    if(ng(W,n,36)==1 && is_superseded(W,n)==0){
      let ok:i32=0;
      if(ng(W,n,0)==1 && ng(W,n,20)==s && ng(W,n,24)==r){ok=1;}
      if(ng(W,n,0)==20 && ng(W,n,8)==s && ng(W,n,4)==r){ok=1;}
      if(ok==1){
        let b:i32=bid(W,n);
        if(b>bb){bb=b; best=n;}
      }
    }
    n=n+1;
  }
  return best;
}
```

Full diff (base tnn3_h5.zag -> tnn3_h5r.zag):

```
@@ -150,8 +150,11 @@
 fn activate(W:[]u8,s:i32,r:i32)i32 {
   let best:i32=-1; let bb:i32=-1; let n:i32=2;
   while(n<1024){
-    if(ng(W,n,36)==1 && ng(W,n,0)==1 && is_superseded(W,n)==0){
-      if(ng(W,n,20)==s && ng(W,n,24)==r){
+    if(ng(W,n,36)==1 && is_superseded(W,n)==0){
+      let ok:i32=0;
+      if(ng(W,n,0)==1 && ng(W,n,20)==s && ng(W,n,24)==r){ok=1;}
+      if(ng(W,n,0)==20 && ng(W,n,8)==s && ng(W,n,4)==r){ok=1;}
+      if(ok==1){
         let b:i32=bid(W,n);
         if(b>bb){bb=b; best=n;}
       }
@@ -548,7 +551,6 @@
   link_edge(W,m,2,m,0); link_edge(W,m,6,m,0);
   let i:i32=0;
   while(i<nf){link_edge(W,m,1,get32(facts,i*4),0); i=i+1;}
-  ev_teach_in(W,s,r,ans);
   return m;
 }
```

Nothing else changed: ev_teach, ev_observe, ev_query, ev_act,
miss_inquire, mp_run, t2_try_verify, bid, ref_prot, is_superseded,
supersede, resolve_uncertainty, revise_on_contradict, the 4-op ISA and
execute are byte-identical to the base. map_standing stays dormant.

## Build (pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1)

- tnn3_h5r.bin SHA-256:
  59c7648287d1e8a1ae6ea851696aae38b3991e537679fc9fc2d4bd38dded0f9b
- 3/3 byte-identical rebuilds (same SHA-256 across three znc
  invocations). Only compiler warnings (A0102 ignored-return-value,
  pre-existing style), no errors.
- Built-in battery: 46/46 PASS (identical to the H5 base battery).
- Binary stdout 3/3 byte-identical across runs.
- Grep of the incremental diff for time/clock/random/rand/seed/PID:
  none.

## KB-S1 self-check (substrate gate)

The working diff contains both hunks: the activate hunk (tag-20
admission on (f8,f4)) and the promote_graph hunk (deletion of the
ev_teach_in call). KB-S1 SATISFIED on the working tree. The adversary
re-verifies on the committed diff before running the sealed battery.

## KB-G1R self-check (architecture accounting)

- Added cognition lines (non-blank, non-comment): 5, budget <= 15.
  PASS. Removed lines: 3. Net cognition delta: +2. Cumulative diff
  against the TNN-2 base: net -20 (inherits H5's -22, minus 2 for this
  change), still net negative.
- New modes: 0. New bridges: 0. New routers: 0. New handlers: 0.
  The activate extension is a read-path admission predicate over an
  existing node type; the MAP answering from f28 is existing ev_query
  behavior.
- Core-ISA additions: 0. The change uses only existing field reads
  (ng), COMPARE, and edge/link operations already present in these
  functions.
- Forbidden protected semantic operations (FIND_POLYNOMIAL_ORDER,
  DETECT_NEGATION, BUILD_CAUSAL_RULE, LEARN_PROCEDURE, FIND_THRESHOLD,
  MAKE_CONDITIONAL): none present in the diff.
- KB-G1R: PASS.

## Unsealed smoke worlds (NOT sealed; keys 7xxx/8xxx, disjoint from any
sealed battery)

Driver /tmp/h5r_smoke.zag (scratch, not a deliverable): byte-copy of
tnn3_h5r.zag with a smoke main exercising the Option A path.

- S1: fact chain taught on fact key (7011,7012); MAP-key query
  (7010,8012) with expected 8001 promotes MAP node 13, answers 8001;
  white-box scan: exactly 1 live tag-20 MAP on the key, zero live
  tag-1 facts on the MAP key.
- S2: repeat MAP-key query with expected -2 answers 8001 via the MAP
  node (the new read path fires).
- S3: OBSERVE on the fact key with 9001: old MAP (node 13) carries a
  CON self-edge (is_superseded==1).
- S4: MAP-key re-query with expected 9001: the superseded MAP no
  longer answers (no shadow fact); the trial loop re-derives against
  live facts; fresh MAP promoted, answers 9001.
- S5: exactly 1 live tag-20 MAP on the key (node 34, id > 13) with
  f28==9001; zero live tag-1 facts on the MAP key.
- SMOKE PASS. 3/3 byte-identical stdout across runs.

The smoke mirrors the prereg's falsifiable prediction direction:
post-contradiction MAP-key probes are not answerable from any
pre-contradiction structure, and each promotes a fresh MAP.

## Deviations from the prereg

None. The activate implementation uses an `ok` predicate variable
rather than a single widened boolean expression; this is a stylistic
choice within the +10-line budget and changes no semantics. Option B
and Option C were not touched.

## Process (KB-P1)

PATH was $HOME/safebin for every command. `which python3` printed
nothing (exit 1) at lane startup and again at implementation start
(recorded in NAMECHECK_IMPL.md Step 0). Shell invoked only: the pinned
znc, built binaries, git read-only ops (log/show/status/diff), and
file copies. Zero forbidden-executable invocations. No commits by this
worker; no push; no files written outside the lane directory. The
sealed directory was never created or read; no sealed-style worlds
were designed.

## Readiness

READY FOR SEALED EVALUATION. Both substrate hunks are implemented
exactly as pinned in prereg section 4; the base is verified byte-for-byte
against the frozen H5 record; the binary is frozen at SHA-256
59c7648287d1e8a1ae6ea851696aae38b3991e537679fc9fc2d4bd38dded0f9b with
3/3 byte-identical builds; KB-S1 and KB-G1R self-checks pass; the
unsealed smoke world demonstrates the full Option A loop
(promote on MAP key, MAP-key retrieval, supersession on contradiction,
miss, re-derivation, fresh MAP promotion, zero tag-1 facts on the MAP
key at every step). Awaiting coordinator commit, then the independent
adversary's sealed battery per prereg section 6.
