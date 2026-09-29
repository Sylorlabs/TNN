# PREREG_ADV_MEM3.md -- H-MEM3 independent red-team preregistration

Adversary: H-MEM3 independent red team (depth-1 subagent).
Target: H-MEM3 builder result at commit 903a2c16c ("H-MEM3 SURVIVES (5/5 bars)"),
  whose preregistration is at commit d00461bff (PREREG_MEM3.md).
Frozen builder output MD5: 486aadc1b838abbe5e474a0c97a7fb38.
Date: 2026-09-29. Timezone: America/Los_Angeles.
Toolchain: /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
  (znc 2026.07.0-dev (edition 2026), observed 2026-09-29).

This preregistration is committed BEFORE the adversary harness is written and
BEFORE any frozen attack is executed. Ordering of commits will be:
  1. this preregistration (alone),
  2. the frozen adversary harness mem3_adv.zag,
  3. raw evidence plus the adversary report ADV_MEM3_RESULT.md.
The prereg commit must strictly precede the harness commit; the harness commit
must strictly precede the evidence/report commit.

## 0. Standing rules and disclosures

Pure Zag: no Python anywhere in this red-team arc, including fixture design,
harness, build, execution, and analysis. This preregistration does not
authorize Python; any Python use would void the arc and must be disclosed.

Pre-prereg exploratory validation (disclosed, not evidence): before writing
this preregistration, the adversary ran two exploratory scratch harnesses in
/tmp (not committed, not part of the repo) to check that the candidate attack
fixtures reach the intended mechanism states (a probation selection-flip state
and an adversarial-future state). Those scratch runs validated feasibility only.
No verdict in this arc rests on them. Every verdict below rests solely on the
frozen adversary harness committed after this preregistration, executed after
both commits, with raw output preserved.

Commits stay local on branch tnn-native-lab. No push is authorized by this
preregistration. Only adversary-owned paths are staged (never broad git add):
  docs/lab/research-lead/overnight-20260928/PREREG_ADV_MEM3.md (this file),
  docs/lab/research-lead/overnight-20260928/mem3_adv.zag,
  docs/lab/research-lead/overnight-20260928/ADV_MEM3_EVIDENCE.txt,
  docs/lab/research-lead/overnight-20260928/ADV_MEM3_RESULT.md.
Concurrent workers own other paths in the working tree (intent_learn.zag,
unified_learn.zag, IU4 files, and others); the adversary does not touch them.

Loop documentation rule: no em dashes in loop docs. This file complies.

The builder's frozen claims under attack (from PREREG_MEM3.md and MEM3_RESULT.md):
  R1: the churn counterfactual is computed for the SELECTED policy (protected
      vs unprotected victim of the argmin winner), with an explicit
      CHURN-PREVENTED:1/0 verdict. MEM3_RESULT.md calls the ev2 :1 verdict
      "genuine (probation shielded proc9)" and the ev1 :0 verdict "honest
      (probation changed nothing for the selected policy)". The causal
      interpretation section presents the counterfactual as genuine causal
      evidence about probation's role.
  R2: all-protected fallback is implemented and covered by a fixture.
  R3: six researcher-frozen shift futures, each machine-checked DIST-DIFFERS
      against the W=20 selection window.
  R4: the selected policy ties the minimum future miss count; n_tying_min
      printed as context. MEM3_RESULT.md prose states the selected policy was
      the unique minimum on all six frozen futures.
  R5: strictness scoped to skewed workloads; a flat round-robin boundary
      fixture demonstrates reported ties.
Builder-disclosed limitations (NOT attacked as surprises; used as reference):
  the menu, windows, and probation constant are authored; futures are
  researcher-frozen and non-adversarial; an adversarial future targeting the
  evicted procedure defeats replay-based selection; probation is age-based
  rather than merit-based; flat workloads tie; H-MEM3 is not integrated into
  the unified learner.

## X-M3-1: counterfactual honesty and whether probation can cause harm

Hypothesis: the CHURN-PREVENTED verdict is selected-policy-scoped in a way
that misleads, and probation can cause harm. Specifically:
  (a) Scope gap: the verdict compares the selected policy's protected vs
      unprotected victim, but it does NOT recompute the winner under no
      probation. There exist reachable states where the winner flips under
      no probation (protected winner != unprotected winner), the printed
      verdict is CHURN-PREVENTED:0, yet probation is the but-for cause of the
      protected newcomer's survival (without probation the winner would evict
      the newcomer). A reader naturally reads ":0" as "probation changed
      nothing overall", which is false in such states.
  (b) Harm: because probation is age-based rather than merit-based, there
      exist reachable states where probation protects a never-queried newcomer
      and forces the eviction of a queried procedure, producing a strictly
      worse eviction by the mechanism's own window-replay cost metric.

Fixture X-M3-1a/X-M3-1b (frozen; all procedure ids are small ints):
  1. store_init; learn_stream procs 0..7 (8 slots, PROB=10).
  2. A_old, 17 queries: proc0 x4, proc1 x4, proc2 x2, proc3 x2, proc4 x2,
     proc5 x2, proc7 x1.
     Rationale: gives proc0/proc1 high frequency, proc7 the LFU minimum.
  3. T, 20 queries: 6,6, 2,2, 3,3, 4,4, 5, then 2,2,2, 3,3,3, 4,4, 5,5,5.
     Rationale: proc6 queried early then abandoned (recency trap for the
     protected winner), proc2/3/4 build frequency late.
  4. pressure(ev=0, newpid=8). Expected: LFU wins, evicts slot7(proc7),
     stores proc8 at slot7 with prot_until = seq+10.
  5. Qb, 9 queries: 6,6,6, 0,0, 1,1,1, 2.
     Rationale: proc6 queried 3x (baits LFU toward keeping proc6 and evicting
     the never-queried newcomer proc8 if unprotected), proc0/proc1 queried
     (keeps them expensive to evict), proc2 x1.
  6. At ev=1, BEFORE pressure, compute and print:
       bestp1 = argmin_pol(up=1)   (protected winner),
       bestp0 = argmin_pol(up=0)   (unprotected winner),
       pv3 = victim(bestp1, ev=1, up=1),
       uv  = victim(bestp1, ev=1, up=0),
       v1  = victim(bestp1, ev=1, up=1)  (actual eviction with probation),
       v0  = victim(bestp0, ev=1, up=0)  (eviction without probation),
       c_prot = replay_cost(v1 under bestp1's accounting),
       c_unprot = replay_cost(v0 under bestp0's accounting),
       uses_new = uses of proc8's slot, uses_old = uses of proc0's slot.
     Expected values (from exploratory validation; the frozen harness
     re-derives them and asserts them):
       bestp1 = 2 (FIFO), bestp0 = 0 (LFU): the winner FLIPS under no probation.
       pv3 = 0, uv = 0: the selected policy's victims coincide, so the
         mechanism will print CHURN-PREVENTED:0.
       v1 = slot0, v0 = slot7: the actual eviction changes; without probation
         the winner (LFU) evicts slot7, which holds the protected newcomer
         proc8. Hence probation is the but-for cause of proc8's survival
         while the verdict reports 0.
       c_prot = 2, c_unprot = 0: the eviction with probation costs 2 window
         replay misses; without probation it costs 0.
       uses_new (proc8) = 0, uses_old (proc0) = 6: probation shields a
         never-queried newcomer and sacrifices a queried procedure.
  7. Call the real pressure(ev=1, newpid=9) and preserve its printed
     CHURN-PREVENTED line verbatim in the evidence.

Kill/confirm criterion X-M3-1: CONFIRMED iff every expected value above holds
AND the real pressure() prints CHURN-PREVENTED:0 at ev1. If any expected value
differs, the probe is REFUTED (fixture did not reach the intended state; no
downgrade follows from this probe; the miss is documented).

Verdict mapping: X-M3-1 CONFIRMED downgrades the R1 causal claim. The frozen
K-M3-1 bar (selected-policy counterfactual values on the builder's streams)
still passes; the mechanism is not killed. What changes: the "genuine causal
evidence" interpretation is narrowed to "selected-policy-scoped verdict with
a demonstrated scope gap", and the report records a demonstrated case where
age-based probation causes a strictly worse eviction (cost 0 becomes cost 2).
Overall H-MEM3 verdict becomes DOWNGRADED (claim narrowed), not SURVIVES-clean
and not KILLED.

## X-M3-2: adversarial futures

Hypothesis: the K-M3-2 bar ("selected ties the minimum on every future, each
DIST-DIFFERS") holds only because the six frozen futures are non-adversarial.
An adversarial future that still passes the DIST-DIFFERS independence check
can make the selected policy the uniquely WORST policy, confirming the
builder's own disclosed limitation is load-bearing. Separately, the
DIST-DIFFERS check itself is a low bar: a future differing from the window by
a single query passes it.

Fixture X-M3-2a (frozen):
  1. Rebuild the builder's A2 pre-ev0 state exactly: store_init,
     learn_stream 0..7, then AA (33 queries: 5,5, 0x4, 7x4, 3x4, 6x4, 1x5,
     2x5, 4x5), then AW (20 queries: 6,6,5, 0x4, 7x4, 3x4, 1x2, 2x2, 4).
  2. sel = select_win(ev=0, win=20). Expected: sel = 0 (LFU), matching the
     builder's A2 ev0 selection.
  3. Compute v_adv = victim(sel, ev=0, up=1); pid_adv = st_pid(v_adv). This is
     the selected policy's evicted procedure (expected: proc5). The attack
     targets it WITHOUT hardcoding the id: F_ADV[i] = pid_adv for i in 0..19.
  4. r = fut_score2(ev=0, F=F_ADV, nf=20, sel, win=20, tag="A2 F-ADV").
     Also compute per-policy misses directly (count of F_ADV queries equal to
     each policy's victim proc id) and print them.
     Expected: DIST-DIFFERS passes (the future is nothing like the window),
     r = 0 (K-M3-2 FAIL: selected not min), selected misses = 20 while every
     other policy scores 0 (selected uniquely worst).

Confirm criterion X-M3-2a: CONFIRMED iff dist_differs(F_ADV)==1 AND r==0 AND
the selected policy's miss count is strictly greater than every other
policy's. Verdict mapping: BOUNDARY. This confirms the builder's disclosed
limitation ("an adversarial future targeting the evicted procedure defeats
replay-based selection") is load-bearing rather than hypothetical. It does
not kill K-M3-2 (the frozen bar is explicitly non-adversarial), but the
report must state that the "validates against future queries" claim does not
survive adversarial futures.

Fixture X-M3-2b (frozen): F_NEAR = AW with F_NEAR[0] flipped from 6 to 5
(one query differs). Confirm criterion: CONFIRMED iff
dist_differs(F_NEAR, win=20)==1 AND dist_differs(AW, win=20)==0.
Verdict mapping: informational. Documents that the independence check is a
low bar (a single-query difference passes), which is the context in which
X-M3-2a's DIST-DIFFERS pass must be read.

## X-M3-3: regression against all 5/5 frozen H-MEM3 bars

Procedure (frozen):
  1. Extract the committed source at 903a2c16c:
       git show 903a2c16c:docs/lab/research-lead/overnight-20260928/mem3_learn.zag
     and confirm the working-tree file is byte-identical to it (git diff empty
     for that path; verified before this preregistration).
  2. Build with the pinned toolchain znc 2026.07.0-dev.
  3. Run the binary three times; require the three outputs to be
     byte-identical (cmp).
  4. Require md5sum of the output to equal the frozen hash
     486aadc1b838abbe5e474a0c97a7fb38.
  5. Require the output to contain all five K-M3-n PASS lines (K-M3-1 ev1,
     K-M3-1 ev2, K-M3-2 x6, K-M3-3, K-M3-4) and the "ALL CHECKS PASSED" line.
Criterion: X-M3-3 SURVIVES iff all of the above hold. Any failure is a
regression KILL of the corresponding bar and is reported as such.

## X-M3-4: source audit

Scope: mem3_learn.zag at commit 903a2c16c (mechanism = everything before
fn main; harness = fn main). Method: full read plus diff against
mem2_learn.zag at the same tree. Checklist (frozen):
  (a) R1: pressure() computes pv3/uv from the SELECTED policy's victims and
      the verdict logic matches the prereg (pv3<0 fallback path; pv3==uv
      prints :0; else :1 naming the unprotected victim's proc).
  (b) R2: select_win() falls back to the unprotected argmin when the
      protected victim is <0 and emits FALLBACK-ALL-PROTECTED; pressure()
      mirrors the fallback, sets the ST fallback flag, and uses up=0
      consistently in the printed table and is_strict_up.
  (c) R3: dist_differs() compares per-proc frequency vectors of the future
      vs the W=win window; call sites pass win=20; the lo<0 clamp is handled.
  (d) R4: fut_score2() requires DIST-DIFFERS first, then the ties-min bar;
      n_tying_min is computed and printed; the selected policy's entry is
      compared with ==minm.
  (e) R5: the flat round-robin boundary fixture is present and reported as
      scope documentation, not a bar.
  (f) Tie handling: argmin_pol uses strict <, so the earliest menu policy
      (LFU) wins replay ties; the K-M3-4 fallback expectation (unprotected
      LFU by tie-break) follows from this rule.
  (g) No fixture-specific answer literals in mechanism code: no hardcoded
      procedure ids, slot numbers, or expected costs outside fn main.
  (h) replay_cost() guards v<0 (returns 999999); victim() returns -1 only
      when no eligible slot exists; no crash path in the all-protected case.
  (i) RESULT prose accuracy: spot-check that "unique minimum on all six"
      matches the raw n_tying_min lines (n_tying_min=1 of 5 on all six means
      unique minimum; any tie would show n_tying_min>=2).
Criterion: X-M3-4 SURVIVES iff no correctness bug is found in (a)-(h). A
prose inaccuracy in (i) yields a documentation correction, not a mechanism
kill. A correctness bug yields a DOWNGRADE or KILL depending on whether a
frozen bar's truth value changes.

## Overall verdict mapping

  - If X-M3-1 CONFIRMED: H-MEM3 is DOWNGRADED. The 5/5 frozen bars stand
    (X-M3-3, X-M3-4 expected SURVIVES), but the R1 "genuine causal evidence"
    claim is narrowed to a selected-policy-scoped verdict with a demonstrated
    scope gap, and the report records a demonstrated probation-harm case.
  - If X-M3-1 REFUTED and X-M3-2a CONFIRMED: H-MEM3 SURVIVES with a recorded
    boundary (adversarial futures defeat replay selection; disclosed limit
    confirmed load-bearing).
  - If X-M3-3 or X-M3-4 fails: verdict follows the failing bar (regression
    kill or audit downgrade/kill), superseding the above.
  - If every probe refutes/fails to fire: H-MEM3 SURVIVES clean and the
    report says so.

## Determinism and reproducibility

The adversary harness is deterministic: the RANDOM menu policy is
deterministic (k-th eligible slot, k=(ev*5+1)%neligible), no RNG is used, and
all fixtures are fixed literal streams. The build command and every command
run are recorded in ADV_MEM3_EVIDENCE.txt. The mechanism portion of the
harness build is extracted from the frozen commit 903a2c16c (first 352 lines,
everything before "fn main" at line 353), concatenated with the committed
adversarial main; the evidence log records the exact bytes used.

Negative evidence is preserved: refuted probes, unexpected values, and any
harness bug are reported rather than hidden. If the frozen harness fails to
reproduce the exploratory expectations, the verdict follows the frozen
harness, not the exploratory runs.
