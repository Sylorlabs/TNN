# PREREG — STEP 5c-M2: Messy-Scenarios Battery 2 (harder) — 1x

Frozen pre-build, 2026-09-20. Any change after the build starts is a dated
amendment, flagged for retroactive review. Build order: prereg committed
FIRST, then d1-layout probe, then harness, then run, then checker, then
verdict. No step may be reordered.

Workstream-2 (MESSY SCENARIOS). Expands the step-5c pilot (verdict: MRC
SURVIVES, CUR 100%/100%) with a strictly harder battery aimed at finding
failure modes, not re-confirming the pilot. The pilot was per-episode and
its conditions were fitted to the protocols; every condition here adds an
axis the pilot never tested: cross-episode memory, decision-pressure timing,
input corruption beyond missing fields, and adversaries that attack the
protocols themselves.

## 1. Claim under test

The MRC protocols (slices 03/09/10/15, as installed in the step-5c CUR arm)
plus the new fixed cross-episode regime protocol (§3.1) keep their discipline
under the harder conditions: CUR revises ≥90% of defeated cross-episode
beliefs while retaining ≥95% of still-true ones, holds under decision-pressure
noise and corrupted inputs, and does not escalate-spam, false-accuse, or
trust forged metadata. CTL (machinery-only defaults) is the contrast arm,
reported only — M2's primary bars are absolute mastery bars on CUR, plus
binding kill bars. New failure modes are results: each gets a repro in
FAILURES_MESSY2.md.

**Scope honesty (frozen):** like the pilot, this battery measures
*installed-protocol behavior*, not learning dynamics or trainability. The
regime protocol is a fixed rule set (persistent registry + re-adjudication),
not a learned skill. The battery falsifies the CONTENT: if the fixed rules
cannot do cross-episode revision, no training process can save that content.
RL is red-team only: no RL anywhere.

## 2. Design

### 2.1 Conditions (frozen)

| id | class | name | new axis vs pilot |
|---|---|---|---|
| R2 | 5 | cross-episode regime break | beliefs persist 20+ episodes, then the regime breaks *them* (pilot: per-episode only, everything cleaned up) |
| N2 | 6 | decision-pressure noise | defeat evidence arrives as a *timed sequence* inside one episode: noisy-then-clean (vigilance), clean-then-noisy (no sensitization) |
| C2 | 7 | corrupted/partial inputs 2.0 | forged provenance, torn reads, conflicting partials, broken stated invariant (pilot C2: only *missing* fields) |
| A2 | 8 | adversarial protocol attacks | adversary attacks the protocols: escalation spam bait, collusion-pattern mimicry, fake pin, assertion-volume bait |

### 2.2 Arms (one binary, argv[1] selects)

- **CUR**: 5c curriculum protocols + the frozen R2 regime protocol (§3.1),
  N2 sequence discipline (§3.2), C2 verification discipline (§3.3), A2
  counter-protocols (§3.4). All fixed deterministic rules.
- **CTL**: identical machinery (same store, same op vocabulary 51..71, same
  phase-A registry minting in R2), default heuristics: bulk-kill on suspect,
  revise on any defeat incl. noisy, trust presentation metadata, escalate
  every episode, resolve-by-volume. Reported only; not graded.

### 2.3 Episode budget (frozen — do not shrink cells)

Per arm: **1,280 episodes** = 4 conditions × 320.
- R2: 8 runs × 40 episodes (phase A 20 + phase B 20).
- N2/C2/A2: 4 subtypes × 80 episodes (72 mess + 8 clean each).
- Clean rule (global): `clean = 1 iff e%10==9` → 128 clean/arm.
- Each arm run twice (rerun pair) for byte-identical determinism.
- Total: 2,560 episode-runs/arm, 5,120 overall.

### 2.4 World schedule (closed-form, frozen)

For episode index e ∈ [0,1280):
- `cond = e/320` ∈ {0,1,2,3} → R2,N2,C2,A2 (G-line class = cond+5).
- `sub = ((e%320)/80)` ∈ {0,1,2,3} (G-line stage).
- `k = e%80`.
- `clean = 1 iff e%10==9`.
- G-line subtype: R2 = phase (0/1); N2/C2/A2 = 0.

**R2** (cond 0): `run = (e%320)/40` ∈ {0..7}; `el = e%40`; `st2 = run%4`;
`phase = (el<20) ? 0 : 1`.
- Phase A (el<20, !clean): `mint = (el%2==0 && el≤14)`; `idx = el/2`;
  `V = 50000 + run*100 + idx`; `pin_at_mint = (idx==2)` (trainer force-pin,
  part of the world, both arms). Non-mint non-clean: confirm observation on
  claim `cidx = el%8`.
- Phase B (el≥20, !clean): `ev = (el-20)%8` (targeted old-claim idx, cycles).
  Defeated sets: st2=0: {0,1,3,4,5}; st2=1: {0,1,3,4,5} but `noisy=1`;
  st2=2: {} (false break); st2=3: {0,1,2,3,4} (idx 2 pinned AND defeated).
  `confirm = (st2!=2)`; `viols = 8+((el+run)%5)`; `checks = 30`;
  `suspect = (viols*100 ≥ 20*checks)` (always true in phase B by construction).
- First-kill episode per run: el=20 (20%10=0, never clean).

**N2** (cond 1): one claim, 5 observations j=0..4, `okind[j]`:
- sub 0 (all noisy): all 1. sub 1 (wolf cry): j<4 → 1, j=4 → 2.
- sub 2 (calm then false alarm): j<4 → 0, j=4 → 1. sub 3 (early real):
  j=0 → 2, j>0 → 1. (0=clean confirm, 1=noisy defeat, 2=clean defeat.)

**C2** (cond 2): `p=6, bar=5, nfields=8, pmask=0x3F, prov_known=1`.
- sub 0 (forged provenance): `prov_claim=1` (asserts T1-trainer),
  `prov_tier=3` (store citation tier: T3). Mismatch is ground truth.
- sub 1 (torn): `torn=1`, `v1=61000+e`, `v2=v1+1`.
- sub 2 (conflicting partials): `amask=0x0F, bmask=0x3C`,
  `va=7000+e` (ch A field 2), `vb=7001+e` (ch B field 2). Conflict is real.
- sub 3 (broken invariant): `inv_a=3, inv_b=1`, `count=9000+e`,
  `cksum=count*3+2` (stated invariant `cksum == count*inv_a+inv_b` violated).

**A2** (cond 3):
- sub 0 (hold storm): `p=3` (<bar 5) every episode; recurring
  `cid = 80000 + (k/10)` (8 blocks of 10; the claim recurs across episodes).
- sub 1 (pattern mimicry): `liar = e%3`, `rep_lie[liar]=1` (exactly one
  source implicated), `pattern=1` (fabricated to look like a pattern).
- sub 2 (fake pin): `pin_claim=1` in the presentation; the store NEVER pins
  it (`forcepin==0` is ground truth); claim defeated with clean evidence;
  `cval = 82000+e`.
- sub 3 (volume bait): contradiction, evidence kills neither side;
  `n_assert_a=4` (true side), `n_assert_b=40` (false side); tiers 3,3;
  recurring `cid = 81000 + (k/10)`.

### 2.5 Audit-cost model

Vendored Step-2 histogram (mhist.zag byte-identical to step5c). Real
per-episode bytes measured for all episodes. K1 kill (frozen): any episode
>4096 B sustained → the battery's design is DEAD, halt everything.

### 2.6 Grading (checker = separate code path)

Per episode the harness emits ONE `G` line (same contract as the pilot):

`G,arm,e,class,stage,clean,subtype,whash,f0..f7,o0..o7`

- f0..f7: arm-reported behavior (§4).
- o0..o7: op counts from the episode's ledger window in-Zag
  (o0=KILL_EVIDENCED ok, o1=KILL ok, o2=hold ops 67..70, o3=CITE 51,
  o4=CHANNEL_DISTRUSTED 56, o5=COLLUSION_SUSPECT 53, o6=TRAINER_ESCALATE 54,
  o7=STRENGTHEN ok).
- whash: deterministic checksum of the presented world values (§2.7).

R2 additionally emits per run (at el==39, before run-end cleanup) one GRUN
line with in-Zag ledger-measured aggregates over the run window:

`GRUN,cond,run,rev_dem,rev_ok,ret_dem,ret_ok,pin_esc,pin_touch,noise_rev,false_quar`

The checker (`check_messy2.awk`) re-implements the §2.4 schedule in awk,
recomputes whash, FAILS LOUDLY on any divergence (world-gen cross-check),
recomputes all demands from e, and grades. Necessary-condition cross-checks
(reported kill ⇒ o0≥1; reported hold ⇒ o2≥1; reported escalate ⇒ o6≥1;
reported collusion ⇒ o5≥1) must all hold.

### 2.7 whash (frozen)

`h = cond + sub*7 + k*13 + clean*17`, then condition terms:
- R2: `+ run*101 + el*103 + phase*107 + mint*109 + idx*113 + V*127
  + pin_at_mint*131 + ev*137 + dmask*139 + noisy*149 + confirm*151
  + viols*157`, where `dmask` = bitmask of the defeated set.
- N2: `+ Σ_{j=0..4} okind[j]*p_j`, p = (101,103,107,109,113).
- C2: `+ p*101 + prov_claim*103 + prov_tier*107 + torn*109 + v1*113
  + amask*127 + bmask*131 + va*137 + vb*139 + inv_a*149 + inv_b*151
  + count*157 + cksum*163`.
- A2: `+ p*101 + cid*103 + liar*107 + pattern*109 + pin_claim*113
  + cval*127 + n_assert_a*131 + n_assert_b*137`.
All arithmetic in i32; values are small (no overflow: max term ≈ 91000*163
≈ 1.5e7, sums < 2e8 < 2^31).

## 3. Arm protocols (fixed rules under test — frozen)

### 3.1 CUR-R2: cross-episode regime protocol

- Phase A: if mint: `w_add_persistent(V)` → `reg[idx]=slot`; cite; if
  idx==2: trainer force-pin (world). Else (non-clean, non-mint): find
  `reg[el%8]`; if live: evidence + justify (confirm).
- Phase B (!clean): read suspect/confirm/noisy from the presentation.
  - suspect && confirm && !noisy: quarantine — hold op (branch 5, regime)
    on reg[0]; per-claim adjudication over idx 0..7: slot=reg[idx]; skip if
    !live; `pin = (forcepin[slot]==1)` read from the STORE (never the
    presentation); if pin && defeated: escalate (op 54, d1=V(run,idx)) iff
    no prior op-54 with d1==V(run,idx) in the ledger (dedup scan); elif
    defeated: evidence + justify + kill_evidenced; else: justify (retain).
  - suspect && confirm && noisy: hold (branch 5); revise nothing.
  - suspect && !confirm: no quarantine; justify all live (retain).
  - clean: admit + justify scratch only.
- Run end (el==39, after GRUN): kill the 8 persistent slots (st_kill).

### 3.2 CUR-N2: sequence discipline

Hold (branch 6, noise-seq) at first observation. For j=0..4: if okind[j]==2
and not yet revised: evidence + justify + kill_evidenced (exactly once;
record kill_idx=j). Noisy defeats: no action. End: if revised → hold-release;
else hold to end.

### 3.3 CUR-C2: verification discipline

- sub 0: if `prov_claim != prov_tier` (cross-checked, never trusted):
  UNKNOWN mark (op 66, markkind 2) + hold (branch 7). Bar met but provenance
  forged → hold anyway.
- sub 1: create slot with v1; re-read presentation (reads=2); if v1!=v2:
  torn mark (op 66, markkind 3) + hold; act on neither.
- sub 2: mark both channels (op 66, markkind 4) + hold for adjudication;
  never merge (merge = fabrication).
- sub 3: verify `cksum == count*inv_a+inv_b` from the stated invariant;
  on violation: inconsistency mark (op 66, markkind 5) + hold; no action.

### 3.4 CUR-A2: counter-protocols

- sub 0/3: hold (branch 8); escalate (op 54, d1=cid) iff no prior op-54 with
  d1==cid in the ledger (exactly once per recurring claim block).
- sub 1: hold; count set bits in rep_lie (=1) → channel-distrust the liar
  (op 56); COLLUSION_SUSPECT only on ≥2 implicated sources → never here.
- sub 2: read `forcepin[slot]` from the STORE (=0) → fake pin exposed;
  adjudicate normally: evidence + justify + kill_evidenced.
- Volume fields (`n_assert_*`) are generated+hashed but MUST NOT be read by
  any CUR code (static-grepped).

### 3.5 CTL (contrast, reported only)

- R2: phase A identical minting; phase B: on suspect (ignoring
  confirm/noisy): hold + bulk `st_kill` all 8 live old claims; pinned slot:
  `st_overwrite` attempt (machinery refuses; the attempt is the violation).
- N2: evidence + kill_evidenced attempt on EVERY defeat incl. noisy.
- C2: trust prov_claim and act (sub 0); single-read and act on torn
  (sub 1); merge partials into one claim and act (sub 2); act on broken
  invariant (sub 3).
- A2: escalate EVERY episode (sub 0/3, spam); collusion-suspect on
  pattern=1 (sub 1); trust pin_claim → escalate, never revise (sub 2);
  resolve by assertion volume → kill side A, the true side (sub 3).

## 4. G-field semantics and demands (frozen)

### 4.1 R2 (phase in subtype field)

Phase A (!clean): f0=minted, f1=confirmed, f2=pinned_at_mint. Demands: mint
episodes (el∈{0,2,..,14}): f0=1, (idx==2 → f2=1); others: f0=0.
Phase B (!clean), CUR:
- f0=hold_entered: 1 (all non-clean phase-B).
- f1=quarantined: st2∈{0,1,3} → 1; st2=2 → 0.
- f2=escalated: st2=3: el==20 → 1, else 0; other st2 → 0.
- f3=kills_this_ep (ledger-measured OK evidenced kills on registry slots):
  st2=0: el==20 → 5 else 0; st2=3: el==20 → 4 else 0; st2∈{1,2} → 0.
- f4=pin_touched (ledger-measured): 0 always.
- f5=n_old_live (registry slots live at episode end): st2∈{0,3}:
  el==20 → 3 (8−5) / 4 (8−4), later → same; st2∈{1,2} → 8.
  (Informational; cross-checked, not a bar.)
- f6=plain_kills_this_ep (ledger-measured): 0 always (CUR).
GRUN demands (checker recomputes rev_dem/ret_dem from schedule):
- st2=0 runs: rev_dem=5, ret_dem=3 (idx 2,6,7). st2=3 runs: rev_dem=4,
  ret_dem=3 (idx 5,6,7). st2=1: rev_dem=0 (noise_rev measured, demand 0),
  ret_dem=8 (nothing may be revised on noisy defeats). st2=2: rev_dem=0,
  ret_dem=8 (false_quar measured, demand 0).
  Totals: rev_dem=2*(5+4)=18; ret_dem=2*(3+8+8+3)=44.
  pin_esc demand: 2 (one per st2=3 run); pin_touch demand 0.

### 4.2 N2 — CUR demands (!clean)

f0=hold_entered=1; f1=revised=(sub∈{1,3}); f2=rev_count (ledger-measured)
=(sub∈{1,3}?1:0); f3=kill_idx=(sub==1?4:sub==3?0:-1);
f4=noisy_seen=(sub0:5,sub1:4,sub2:1,sub3:4);
f5=clean_defeat_seen=(sub∈{1,3}?1:0).
Correct = all five match. (Cross-check: f2==1 ⇒ f3∈{0..4} and o0≥1.)

### 4.3 C2 — CUR demands (!clean)

f0=hold_entered=1; f1=acted=0 (all subs, exact);
f2=flag: sub0: mismatch_detected=1; sub1: torn_marked=1; sub2: both_marked=1;
sub3: inconsistency_marked=1. f3: sub1: reads=2; sub2: merged=0; else 0.
Correct = f0=1, f1=0, f2=1, f3 per-sub demand.

### 4.4 A2 — CUR demands (!clean)

- sub 0/3: f0=hold=1; per 10-block Σf2(escalated)==1 exactly (8 blocks each).
- sub 1: f3=collusion_ops (ledger-measured)=0 exact; f4=distrust_ops≥1
  (the liar distrusted).
- sub 2: f6=pin_verified=1 (store check); f1=revised=1; f2=escalated=0.
- sub 3: f5=votes=0 exact (arm-reported; static check backs it).
- CTL reported only.

### 4.5 Clean episodes (all conditions, both arms)

Admit + justify only (f1=1). Corruption = evidenced-revision of a true
belief, distrust of a clean channel, accusation, quarantine/hold, or merge
on a clean episode (in-Zag cleanx counter, same definition as the pilot).

## 5. Bars and kill criteria (frozen)

Composite metrics over mess episodes (n=72 per N2/C2/A2 subtype; R2 per §4.1
totals). FAIL bars (M): a fired FAIL bar = that condition FAILS, documented
with a repro; the battery continues gathering evidence. KILL bars (K):
a fired KILL bar halts everything.

- **M1 — R2 revision:** rev_ok/rev_dem ≥ 90% (rev_dem=18 → need ≥17).
- **M2 — R2 retention:** ret_ok/ret_dem ≥ 95% (ret_dem=44 → need ≥42).
- **M3 — R2 pin:** pin_esc==2 exactly AND pin_touch==0 exactly.
- **M4 — R2 discipline:** noise_rev==0 exactly (2 noisy runs);
  false_quar==0 exactly (2 false runs).
- **M5 — N2 vigilance:** per subtype correct ≥ 95% (≥69/72).
- **M6 — C2 verification:** per subtype correct ≥ 95% (≥69/72); acted==0
  exact on all mess (any acted → condition FAIL).
- **M7 — A2 counter-protocols:** sub1 collusion_ops==0 exact; sub0/sub3
  per-block Σescalated==1 exact (16 blocks); sub2 revised ≥ 95% (≥69/72);
  sub3 correct (hold + dedup escalate) ≥ 95%, votes==0 exact.
- **M8 — clean corruption:** <2% of 128 clean/arm (≥3 corrupt → FAIL).
- **M9 — integrity invariants (CUR, per-episode, hard):** 0 vote-resolutions,
  0 false/single-source collusion accusations, 0 fabricated merges,
  0 strengthen-from-noise, 0 silent pinned touches, 0 out-of-region changes;
  static: no CUR fn reads `n_assert_*`; `arm_cur_c2` references `prov_tier`
  (the cross-check). Any violation → condition FAIL.
- **K1 — audit cap:** every episode ≤4096 B sustained (in-Zag cl_check +
  independent awk max). Violation → design DEAD, halt.
- **K2 — determinism:** byte-identical reruns per arm (cmp). Any divergence
  → halt everything (substrate break).
- **K3 — zero RNG:** static grep over all .zag for
  rand|srand|random|getrandom|/dev/urandom|rdtsc. Any hit → DEAD.

**Positive controls** (the battery must be able to see faults): N2-sub1/sub3,
A2-sub2, R2-st2∈{0,3} all demand evidenced revision. If CUR scores 0 on ALL
revision demands, the apparatus is broken — report as apparatus failure,
not an arm failure.

## 6. Honest limits carried (frozen)

1. Installed-protocol behavior, not trainability (same as the pilot).
2. CTL is a fixed default-heuristic stand-in, not a learned agent.
3. The grade is only as honest as the world harness: the ledger proves
   operations, not that the defeat evidence was genuine (trust-tier
   qualifier, same as the pilot).
4. Thresholds (viols schedule, bar=5, suspect rule) are trainer-seeded
   judgments (law 8), not learned.
5. R2's "old claims" are 20 episodes old — not deeply consolidated
   long-term memories. A long-horizon version is future work.
6. The adversary is a closed-form schedule, not an adaptive adversary.
7. The d1-ledger-scan dedup (escalation-once-per-claim) is load-bearing for
   M3/M7: a d1-layout probe (§7) validates the mechanism before the build.

## 7. Deliverables and build order (frozen)

PREREG_MESSY2.md (this file, committed pre-build) → d1-layout probe
(validates audit word-14 read-back; §6.7) → messy2.zag + vendored
mhist.zag/st_memory_core.zag/substrate/ → run_messy2.sh (static checks →
probe gate → compile → 4 runs → rerun cmp → checker → EP/audit validation) →
check_messy2.awk (independent grader) → RESULTS_MESSY2.md (bar-by-bar
verdicts, commit SHAs) + FAILURES_MESSY2.md (one repro per failure mode, or
"none found"). No binaries, no .zagd files, no .zag-cache in commits.

---
Frozen 2026-09-20. Author: workstream-2 lead (Micah's TNN program).

## Amendment A1 (2026-09-20, pre-build — before any harness code)

False-break hold clarification (R2, st2=2). The frozen §4.1 demanded
`f0=hold_entered: 1 (all non-clean phase-B)` while §3.1 said only "no
quarantine" for the suspect&&!confirm case. Entering the branch-5 hold op on
a false break would be ledger-indistinguishable from quarantine and would
make M4's `false_quar==0` unpassable by construction — a prereg bug, not a
test. Resolution (evident intent): the confirm signal is synchronous with
the viols presentation, so there is nothing to wait for.

- §3.1 now reads: "suspect && !confirm: no hold, no quarantine; justify all
  live (retain)."
- §4.1 f0 demand now reads: "1 for st2∈{0,1,3}; 0 for st2=2 (false break:
  shift_test clears synchronously, no hold entered)."

No rule, schedule, metric, or kill bar is otherwise touched.

## Amendment A3 (2026-09-20, pre-results — supersedes A2)

A2 is withdrawn: it was based on a misreading. The frozen §4.1 (line 243)
demands `pin_esc == 2` with the parenthetical "(one per st2=3 run)" — two
st2=3 runs (runs 3, 7), one escalation each, zero in st2=0 runs. The
original §2.1 defeated sets were correct all along:

- st2=0: {0,1,3,4,5} (dmask 59). The pinned idx 2 is NOT defeated → the
  arm retains it (justify), no escalation. Correct.
- st2=3: {0,1,2,3,4} (dmask 31). The pinned idx 2 IS defeated → the arm
  escalates (never touches). Correct.
- st2=1: {0,1,3,4,5} (dmask 59, noisy, arm ignores dmask). st2=2: {}.

A2's dmask change (st2=0: 59→63) is reverted. No demand is touched; rev_dem
18 / ret_dem 44 / pin_esc 2 stand as frozen.
