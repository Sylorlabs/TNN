# PREREG: HOOK-PHASE1 (frozen)

Non-ledger task. Lane
`docs/lab/research-lead/overnight-20260928/hook_phase1/`, file prefix
`hq_`. Repo `tnn-rsi-gpi3`, branch `tnn-native-lab`, commits local
only, never pushed.

## 1. Task

Implement MUTATION-HOOK Phase 1 (A2.3 inert dispatch) as pure
infrastructure on the HOOK-PHASE0 substrate. No invention claim is
made or tested: the installed probe body is RESEARCHER-WRITTEN, and
the bars verify dispatch mechanics only (inert default, exact
once-per-mutation fire, payload plumbing, uninstall). A2.2, A2.4,
A2.5 and the strong sense of A2.3 are explicitly out of scope; A2.2
is gated on Micah's pending EXECUTE placement ruling and is not
implemented here.

## 2. Frozen design answers (before implementation)

**Cell layout additions (frozen, audited free on the hp_* sources).**
Zero literal hits for 1063-1069 in any hp_* source. The only
computed access near the region is the Phase-0 registry at
1030+n*4 with n<8 (max cell 1061) and its count at 1062; the alloc
region is bytes [3736,4120) = cells 934..1029. New cells:

- S cells 1063, 1064: hook slot. i64 bits of the installed hook body
  (a Zag fn value), little-endian halves: 1063 = low 32 bits,
  1064 = high 32 bits. Value 0, the zeroed-arena default, means no
  hook installed: the consult is behaviorally inert.
- S cell 1065: probe fire counter (written only by the
  researcher-written probe body).
- S cells 1066, 1067, 1068: probe payload stash (p0, p1, p2 of the
  last fire).

**Hook section (frozen, appended to hq_base.zag).** Lane-base code
only: get32/set32, arithmetic, branch, plus fn-to-i64 and i64-to-fn
casts with an indirect call (T1/T2-tested Zag language machinery,
re-verified pre-prereg; no new protected-core operation).

```
// ---- HOOK-PHASE1 A2.3: inert hook dispatch infrastructure ----
// Hook slot: S cells 1063 (low 32 bits) and 1064 (high 32 bits) hold
// the i64 bits of the installed hook body (a Zag fn value),
// little-endian halves via set32/get32. Slot value 0, the
// zeroed-arena default, means no hook: the consult is inert.
// Installable bodies are researcher-compiled fn values (menu
// selection); the strong sense (learner-constructed bodies) is
// gated on A2.2 and the EXECUTE ruling. The consult fires AFTER
// the mutation commits, co-located with the A2.6 counter bump, so
// a rejected store fires neither the counter nor the hook.
// Reload masks the low half to 32 bits: get32-as-i64 sign-extends
// bit 31, which would corrupt the pointer under ASLR whenever the
// code address has bit 31 set (pre-prereg probe: unmasked form
// segfaulted intermittently; masked form 12/12 stable).
fn hk_install(S:[]u8,bits:i64)void {
  set32(S,1063*4,bits as i32);
  set32(S,1064*4,(bits>>32) as i32);
  return;
}
fn hk_uninstall(S:[]u8)void {
  set32(S,1063*4,0);
  set32(S,1064*4,0);
  return;
}
fn hk_bits(S:[]u8)i64 {
  let lo:i64=(get32(S,1063*4) as i64)&4294967295;
  let hi:i64=get32(S,1064*4) as i64;
  return lo|(hi<<32);
}
// Dispatch: reload the fn value and indirect-call it with
// (S, A, p0, p1, p2). Payload convention (researcher-defined
// infrastructure detail, no semantic claim): fact_add passes the
// stored triple (s, r, o); fact_set_obj passes (idx, 0, o).
fn hk_fire(S:[]u8,A:[]u8,p0:i32,p1:i32,p2:i32)void {
  let bits:i64=hk_bits(S);
  if(bits!=0){
    let h:fn([]u8,[]u8,i32,i32,i32)void=bits as fn([]u8,[]u8,i32,i32,i32)void;
    h(S,A,p0,p1,p2);
  }
  return;
}
```

**Mutation-function deltas (frozen).** hq_base.zag = hp_base.zag
plus exactly: in `fact_add`, inside the existing `if(n<64)` guard
after the 932 bump, one line: `hk_fire(S,A,s,r,o);`. In
`fact_set_obj`, after the 932 bump, one line:
`hk_fire(S,A,idx,0,o);`. Post-commit placement: a rejected store
is not a mutation and fires neither the counter nor the hook.

**Probe body (frozen, top-level fn in hq_main.zag, stage code).**
RESEARCHER-WRITTEN. Menu-selection demo of the dispatch path, not
invention.

```
// hq1_probe_body: RESEARCHER-WRITTEN probe body for the HP-P1
// dispatch probe. Installed via fn bits into the hook slot; this
// exercises dispatch only and is menu selection, NOT invention
// (A2.2 is gated on the EXECUTE ruling). Counts fires in S cell
// 1065 and stashes the last payload (p0, p1, p2) in S cells
// 1066, 1067, 1068.
fn hq1_probe_body(S:[]u8,A:[]u8,p0:i32,p1:i32,p2:i32)void {
  set32(S,1065*4,get32(S,1065*4)+1);
  set32(S,1066*4,p0);
  set32(S,1067*4,p1);
  set32(S,1068*4,p2);
  return;
}
```

**HP-P1 stage (frozen, inserted in hq_main.zag after the
SUMMARY-HOOKPHASE0 line, before `o_flush(B,c);`).** Uses fresh
scratch arenas hS3 (S arena), hA0/hA4/hA5 (world arenas); the
probe triple (hps0,hpr0,hpo0) is fact 0 of the battery arena A,
runtime-derived (611, 601, 621: ES-E re-ran setup_worldA on A and
wrote fact 0's object back unchanged; no later stage touches A).

1. Pre-install inertness: `fact_add(hS3,hA0,hps0,hpr0,hpo0);`
   `fact_set_obj(hS3,hA4,0,hpo0);` then `hf0=sg(hS3,1065)`.
   Both consult paths see slot 0.
2. Install: `hk_install(hS3,hq1_probe_body as i64);`
3. 70x `fact_add(hS3,hA4,hps0,hpr0,hpo0)` (64 stored, 6 rejected).
   `hf1=sg(hS3,1065)`; `hap0..2=sg(hS3,1066..1068)` (last payload).
4. `fact_set_obj(hS3,hA4,0,hs2c);` `fact_set_obj(hS3,hA4,1,hs2c);`
   `fact_set_obj(hS3,hA4,2,hs2c);` with hs2c=506 (HP-P0 capture,
   runtime-derived). `hf2=sg(hS3,1065)`;
   `hlp0..2=sg(hS3,1066..1068)` (last payload).
5. Uninstall: `hk_uninstall(hS3);` then 5x
   `fact_add(hS3,hA5,hps0,hpr0,hpo0)` on a fresh arena (all 5 would
   fire if the slot were live) plus 2x
   `fact_set_obj(hS3,hA4,idx,hs2c)`. `hf3=sg(hS3,1065)`.
6. Print `HP-HOOK f0=<hf0> f1=<hf1> f2=<hf2> f3=<hf3>
   ap0=<hap0> ap1=<hap1> ap2=<hap2> lp0=<hlp0> lp1=<hlp1>
   lp2=<hlp2>`.
7. `hdok=1` unless any of: hf0!=0, hf1!=64, hf2!=67, hf3!=67,
   hap0!=hps0, hap1!=hpr0, hap2!=hpo0, hlp0!=2, hlp1!=0,
   hlp2!=hs2c (relational checks against runtime values; no world
   literals in new code). Print
   `SUMMARY-HOOKPHASE1 dispatch_ok=<hdok>`.

hq_world.zag, hq_module.zag, hq_learn.zag = byte copies of the hp_
originals (verified with cmp). hq_build.sh mirrors hp_build.sh with
the hq_ prefix and the pinned znc path. Runs:
`./hq_bin > hq_runN.txt 2> hq_runN.err`, N=1..3.

**Frozen expected values.**

- hq_run1.txt: 155 lines. Lines 1-146 byte-identical to
  hp_run1.txt lines 1-146 (ES battery). Lines 147-152
  byte-identical to hp_run1.txt lines 147-152 (HP-P0 block).
- Line 153 exactly: `STAGE HP-P1 HOOK-DISPATCH`
- Line 154 exactly:
  `HP-HOOK f0=0 f1=64 f2=67 f3=67 ap0=611 ap1=601 ap2=621 lp0=2 lp1=0 lp2=506`
- Line 155 exactly: `SUMMARY-HOOKPHASE1 dispatch_ok=1`

Derivation of the frozen numbers: f0=0 (slot 0 on the zeroed
arena); f1=64 (70 adds, 64 stored inside the guard); ap=(611,601,
621) = the stored triple; f2=67 (3 set_obj fires); lp=(2,0,506) =
last set_obj payload (idx 2, placeholder 0, o=hs2c=506); f3=67
(5+2 would-be fires after uninstall, none observed).

## 3. Frozen kill bars

- HQ-R1 (regression, additive-only): hq_run1.txt lines 1-146
  byte-identical to hp_run1.txt lines 1-146. Fails if the consult
  changes any battery behavior.
- HQ-A1 (Phase-0 substrate preserved): hq_run1.txt lines 147-152
  byte-identical to hp_run1.txt lines 147-152. Fails if Phase 1
  perturbs Phase-0 machinery.
- HQ-A2 (inert default): the HP-HOOK line has f0=0 exactly. Fails
  if the slot-0 consult fires on either mutation path, or the slot
  default is nonzero.
- HQ-A3 (fact_add dispatch exactness): f1=64 exactly. Fails if the
  consult is missing from fact_add (f1=0), placed outside the guard
  (f1=70), or fires twice per mutation.
- HQ-A4 (add-path payload plumbing): ap0=611 ap1=601 ap2=621
  exactly. Fails if the consult passes wrong arguments.
- HQ-A5 (fact_set_obj dispatch): f2=67 and lp0=2 lp1=0 lp2=506
  exactly. Fails if the consult is missing from fact_set_obj
  (f2=64) or the payload convention is wrong.
- HQ-A6 (uninstall restores inertness): f3=67 exactly. Fails if
  uninstall does not clear the slot (f3 would be 74).
- HQ-A7 (protected core untouched, static audit):
  `cmp hq_world.zag hp_world.zag`, `cmp hq_module.zag hp_module.zag`,
  `cmp hq_learn.zag hp_learn.zag` all identical;
  `grep -c "1063\|1064\|1065\|1066\|1067\|1068\|hk_" hq_world.zag
  hq_module.zag hq_learn.zag` is 0;
  the diff hq_base.zag vs hp_base.zag contains only the two
  hk_fire consult lines and the hook section;
  no file outside the lane is modified; znc is untouched;
  new code uses only get32/set32, arithmetic, branch, and the
  fn-value cast + indirect call (T1/T2-tested language machinery;
  masked reload is the ASLR-robust form, 12/12 stable pre-prereg).
  No protected-core change.
- HQ-H1 (toolchain/hygiene): safebin for all build/run/verify
  commands; pure Zag; pinned znc; prereg committed alone before
  implementation; 3/3 byte-identical runs, stderr empty, exit 0;
  zero em/en dash bytes in authored files; probe body labeled
  researcher-written in REPORT; no invention claimed; no world
  literals in new executable code (probe triple and hs2c are
  runtime-derived; indices 0,1,2 are structural).

## 4. What this does NOT claim

- The probe body is researcher-written. Observing it fire is a
  dispatch test, not learning or invention (menu selection under
  the L3 bar; MUTATION-HOOK G3/G4).
- The slot, consult, install/uninstall helpers are
  researcher-placed infrastructure. A learner writing fn bits to
  the slot would be selection among researcher-compiled bodies,
  not construction.
- Phase 1 changes nothing about what the learner can DO with
  mutation events beyond the inert consult existing. Behavioral
  change in the strong sense arrives no earlier than Phase 2
  (gated on the EXECUTE ruling).
- The masked-reload fix is a toolchain-correctness detail of the
  probe pattern, not a research result.
