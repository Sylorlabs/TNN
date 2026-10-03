# REPORT.md -- IVWC-VETO: verifier veto (selective execution)

## Verdict: BUILD-PASS (K1..K8 all PASS)

The learner now ACTS on its self-verdict. Veto decisions are
committed before any sealed consequence (K1); the learner's
veto policy (P1: veto iff the frozen verifier says FAIL, with
the threshold T learner-computed from train consequences)
strictly reduces wasted executions at wp=15 (K3: 1 < 5),
strictly raises the success rate among executed plans (K4:
5/6 > 7/12), and strictly beats the naive fixed rule "veto
only empty plans" (K6: 1 < 3). Under strong law change (wp=45),
where expand3 showed the verifier's accuracy edge over the
trivial baseline goes negative (+2 -> -1), the veto REMAINS
targeted (K7: vetoed mean eff 0 < executed mean eff 33.3) and
still avoids waste (K8: 2 < 11). Deterministic 3/3 (K5); no
oracle tokens (K2). The learner-computed threshold's veto set
is identical to the researcher-written strict fixed rule
"execute only bucket 1" at all three shift levels
(DIFF12 = 0/0/0) -- the table implements exactly the
interpretable "exactly one gather" rule across the dial.

## What was built

`src/ivwc_veto.zag` (pure Zag, single file, ~700 lines, pinned
znc), `bin/ivwc_veto` (frozen binary). World, beliefs,
NAV+GATHER composer, consequence simulator, bucket verifier,
and all seeds are copied verbatim from IVWC-EXPAND3; the
revision protocol and shuffled ablation are removed. New: a
VETO COMMIT phase per sealed shift (compose -> verifier_check
-> three veto decisions stored; world-call counter enforced),
one deterministic harness consequence pass over all committed
plans, and per-policy accounting (P0 no veto; P1 learner; P2
fixed strict; P3 fixed lax). Selective execution is realized
as pre-committed selection over the deterministic consequence
records: vetoed cases contribute no energy and no collection,
executed cases contribute their recorded (collected, energy,
eff). Plans are frozen at commit and the world is
deterministic, so this yields bit-exactly the outcomes
physical selective execution would produce; the veto decision
precedes any sealed world_execute and the learner never
observes the harness pass. Verified: all 36 sealed
(s, bucket, eff) pairs are bit-identical to expand3's run1.

Build: `src/tools/toolchain/znc_linux_x86_64_abed8aa1
src/ivwc_veto.zag -o bin/ivwc_veto`. Analyzer: one
informational zagd-unavailable notice only.

## Kill-bar results

- K1 (commit before signal): PASS. K1T-STRUCT-PASS (world
  calls 0 after train COMMIT); K1S-STRUCT-PASS at sh=0/1/2
  (counter unchanged across each VETO COMMIT). A1: commit-block
  call sites (learner_compose 511, verifier_check 513,
  veto_p1/2/3 515-517) all precede the consequence block's
  world_execute (557). A2: zero world_buf/world_off in the
  LEARNER section.
- K2 (no disguised oracle): PASS. A3/A4: zero
  expected|answer|key|target and zero
  correct|reference_plan|gold tokens; == comparisons are
  verdict/bucket/action/local only; veto decisions use only
  (verdict, bucket); T learner-computed.
- K3 (fewer wasted executions, wp=15): PASS. W[1]=1 < W[0]=5
  (wasted = executed plan with eff < T=20).
- K4 (higher success rate among executed, wp=15): PASS.
  5*12=60 > 7*6=42, i.e. 5/6=83% vs 7/12=58%.
- K5 (determinism): PASS. 3/3 byte-identical, sha256
  d6c7574f093589d180e5b44fccfc2ec90116633663e59c197349a34c5cb8f6bf.
- K6 (learner threshold beats naive fixed, wp=15): PASS.
  W[1]=1 < W[3]=3.
- K7 (veto stays targeted at wp=45): PASS.
  0*3 < 100*9 (vetoed mean eff 0 < executed mean eff 33.3),
  both sets nonempty.
- K8 (veto still avoids waste at wp=45): PASS. W[1]=2 < W[0]=11.

## The three questions, answered

1. Does selective execution improve outcomes? YES, on both
   preregistered measures, at every shift level:
   - Wasted executions (eff < T): 5->1 (wp=15), 4->1 (wp=30),
     11->2 (wp=45).
   - Success rate among executed (eff >= T): 58%->83%,
     67%->83%, 8%->33%.
   - Energy saved by vetoing: 65 / 48 / 23 plan-steps.
   The honest tradeoff (reported, not barred): total
   collection falls (16->5 at wp=15; 15->5 at wp=30; 1->1 at
   wp=45 -- the forfeited plans collected 11/10/0 items), but
   global efficiency 100*sumc/sumu rises (19->27, 23->33,
   3->20). Veto buys efficiency per unit energy at the price
   of absolute collection; at wp=45 the price is zero
   (cforf=0: every vetoed plan collected literally nothing).
2. What is the veto threshold? The LEARNER-COMPUTED threshold
   wins: P1 strictly beats the naive fixed rule P3 (K6), and
   P1's veto set is IDENTICAL to the researcher-written
   strict fixed rule P2 ("execute only bucket 1") at all
   three shifts (DIFF12 = 0, 0, 0). The frozen table's rule
   ("PASS iff bucket mean >= T=20", i.e. exactly-one-gather)
   is stable across the dial; the learner needs no
   researcher-supplied cutoff.
3. Does vetoing interact with law change? The veto's value
   does NOT track the verifier's accuracy edge. Expand3
   showed the edge (acc-maj) degrading +2 -> 0 -> -1; the
   veto benefit in waste avoided stays positive throughout
   (4, 3, 9 fewer wasted executions) and stays targeted
   (K7). At wp=45 the environment is so degenerate (11/12
   plans waste) that skipping is nearly always right even
   though the verdicts are worse than the trivial rule. The
   two failure modes differ: verdict accuracy degrades while
   veto utility persists -- because veto utility tracks waste
   density, not calibration.

## Honest caveats

1. Selective execution is realized as pre-committed selection
   over one deterministic consequence pass, not as physical
   non-execution; the energy-saved and collection-forfeited
   figures are exact under the deterministic world, and the
   veto decision itself (the learner behavior under test) is
   genuinely pre-consequence.
2. The wp dial covers one law-change axis (wall density);
   item law, belief noise, and energy budget are fixed.
3. Mechanism test, not a composition-novelty or L3 claim (per
   PREREG section 6). The verifier is a fixed bucket table;
   the claims concern the veto loop, the threshold
   comparison, and the law-change interaction.
4. The collection/efficiency tradeoff is real: a deployment
   that values absolute items collected over efficiency per
   energy would not veto. The bars measure waste and success
   rate, not total yield.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_veto
~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1 src/ivwc_veto.zag -o bin/ivwc_veto
./bin/ivwc_veto | sha256sum   # expect d6c7574f093589d180e5b44fccfc2ec90116633663e59c197349a34c5cb8f6bf
```

Frozen audits (PREREG section 4): A1 ordering 511/513/515-517
< 557; A2 count 0; A3 count 0; A4 count 0;
A5 sha256 equality across runs/ivwc_veto-run{1,2,3}.txt.

## Branch note

Work committed on `tnn-native-lab` (the shared checkout this
worker was spawned on). Prereg commit 189ee343c strictly
precedes the implementation commit. All commits use explicit
pathspecs confined to `ivwc_veto/`. Local only, never pushed.
Git writes via /usr/bin/git directly.
