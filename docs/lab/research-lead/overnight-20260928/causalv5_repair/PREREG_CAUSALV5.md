# Preregistration: H-CAUSALV5 (Causal Vocabulary Repair, Round 5)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any H-CAUSALV5 implementation)
**Researcher:** H-CAUSALV5 Repair Researcher (subagent)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV4 DOWNGRADED (red team CV4-ADV, CV4_ADV_RESULT.md).
This hypothesis repairs the downgrade finding at the mechanism level.

## Background and failure being repaired

H-CAUSALV4 (R4: cause-context diversity for confirmation) was DOWNGRADED
by independent red team:

- **X-CV4-1 (varied-cause-context confounder):** SUCCEEDED. The frozen
  X-CV3-1 double-confounder construction with the two positioned
  action-1 episodes in DIFFERENT states (seq3 in (1,0,0), seq7 in
  (2,0,0)). Both flips remain genuine law changes; both confounders
  remain correlationally clean. R0 CONFIRMED at seq 8 with st=ACT;
  the probe `Q (0 0 1) | 1 -> (0 0 2)` is corrupted (truth (0,0,1)).
  Narrowed claim: "R4 blocks confirmation of confounders that repeat
  in an identical cause context. It does not close the genuine-change
  confounder class."

- **X-CV4-3 (counter-evidence permanence):** CONFIRMED as severity
  note. Ten action-1 no-op episodes appended after the X-CV4-1
  confirmation do not retract R0; the probe stays corrupted. The
  committed source contains no rule-retraction machinery. Once a
  spurious rule is confirmed, the corruption is permanent.

- **X-CV4-2, X-CV4-4:** HOLD (support-timing honest, 10/10 regression).

## Why the X-CV4-1 confirmation is uncloseable by observation

The 3D genuine delay (frozen K-CV3/K-CV4 bar) and the X-CV4-1
confounded stream are observationally equivalent with respect to
every generic (non-fixture-specific) confirmation criterion:

- 3D: cause episodes seq5 (a4 in (0,0,0), no-op) and seq9 (a4 in
  (2,0,0), no-op); effect episodes seq7 (a3, s2 0->1, contradiction)
  and seq11 (a0, s2 0->1, contradiction). delay_clean passes for
  (xa=4, d=2): every same-action episode with outcome s2=1 was
  preceded by a4 at d=2; every same-action episode with another
  outcome was not.
- X-CV4-1: cause episodes seq3 (a1 in (1,0,0), no-op) and seq7 (a1
  in (2,0,0), no-op); effect episodes seq4 (a0, s2 1->2,
  contradiction) and seq8 (a2, s2 1->2, contradiction).
  delay_clean passes for (xa=1, d=1) with the identical structure.
- In both, the competing hypothesis is "the current actions' laws
  changed" (2 law changes: a3+a0 in 3D, a0+a2 in X-CV4-1). The
  delay hypothesis (1 rule) is strictly simpler in both cases.

Therefore any observation-only confirmation check that confirms
3D's genuine rule must also confirm X-CV4-1's spurious rule. The
learner's decision to confirm in X-CV4-1 is the correct parsimony
choice given the data; the fixture's stipulated "truth" (a1 is a
no-op; two laws changed simultaneously) is not inferable from the
observations. Closing the confirmation itself would require
fixture-specific pattern matching or breaking 3D. H-CAUSALV5 does
not attempt it.

The genuine defect is IRREVERSIBILITY (X-CV4-3): the learner commits
permanently to a defeasible hypothesis. A continuing learner must
revise its causal hypotheses when counter-evidence arrives. That is
what R5 repairs.

## Repair (frozen mechanism specification)

causalv5.zag = byte-copy of frozen causalv4.zag (committed in
causalv4_repair/, md5 f640a57f3690b7ab1da320dc238350ad) plus ONLY
the R5 change below. No other mechanism change. No new memory
(WSZ unchanged). In particular, confirmation logic (R1a, R1b, R4),
delay_clean, contest behavior, and prediction are untouched.

### R5: Counter-evidence retraction for ACTIVE delay rules

An ACTIVE delay rule is a defeasible causal hypothesis: "action xa
causes var v := nv with delay d". If a later episode shows the
cause action at seq-d WITHOUT the effect following, the hypothesis
is refuted.

Mechanism:

1. New function `dl_retract_check(W, e)` (e = index of the newly
   learned episode). For each delay rule r with `dl_st==ST_ACT()`:
   let xa=dl_cause, d=dl_d, v=dl_var, nv=dl_fp. If `d>0` and
   `obs_action_at(ep_seq(e)-d)==xa` and `ep_ns(e,v)!=nv`, then the
   rule's prediction ("s<v> = <nv> at seq <s>") is falsified by
   observation. Refute: set `dl_st=ST_PROV()` (inert on
   predictions), reset `dl_sup=1` (the rule must re-earn
   confirmation with a new diverse support), and emit:
   `# delay rule R<r> REFUTED at seq <s>: cause a=<xa> at seq <s-d>
   not followed by s<v>=<nv> (observed <obs>); demoted to
   PROVISIONAL`.
   PROVISIONAL rules are not checked (inert; no harm to bound).

2. Hook: call `dl_retract_check(W, ne2)` in `learn_episode`
   AFTER `delay_attribution`, so the new episode's attributional
   role (creation/support) is settled before its refuting role is
   assessed. A single episode may support one rule and refute
   another; the two operate on different (cause,var,outcome) keys
   and do not conflict.

3. Re-confirmation uses the existing path unchanged: a later
   supporting episode for the demoted (PROVISIONAL, support=1)
   rule promotes it via R4's diversity check. The trace shows
   REFUTED then, if re-earned, CONFIRMED. No silent resurrection.

Rationale: this is not pattern-matching the attack. It is the
general belief-revision requirement for defeasible causal claims:
a hypothesis that makes a wrong prediction is demoted. It bounds
the X-CV4-1 harm class by making every confirmation revisable,
and it directly closes X-CV4-3 (permanence).

### Hand-derived expectations (frozen before implementation)

- X-CV4-3 fixture (causalv4_adversary/cv4_adv_perm_obs.txt, 18
  episodes: X-CV4-1 vary + ten a1 no-ops at seq9..18):
  - seq9 (a1 no-op): obs_action_at(8)=a2 != 1. No refutation.
  - seq10 (a1 no-op): obs_action_at(9)=a1==xa;
    ep_ns(s2)=0 != 2. REFUTED. R0 -> PROVISIONAL, support=1.
  - seq11..18: R0 PROVISIONAL, not checked. No further diagnostics.
  - Probe (H 0 0 0 | 1; Q 0 0 1 | 1): R0 inert. Base a1 law is
    no-op. `Q (0 0 1) | 1 -> (0 0 1)`. Uncorrupted.
- X-CV4-1 vary fixture, 8 episodes
  (causalv4_adversary/cv4_adv_vary_obs.txt): R0 CONFIRMS at seq 8
  exactly as under CV4 (no counter-evidence within the 8
  episodes; R0 PROVISIONAL before seq 8). Trace byte-identical to
  the red team's CV4 raw (md5 d32d0c76230278c094ba81953f0cbbd8).
  The confirmation is NOT prevented; it is made revisable.
- 3D (frozen): R0 (xa=4, d=2, s2:=1) ACTIVE from seq 11. Only
  episodes with a4 at seq-2 are seq7 (ns(s2)=1==nv) and seq11
  (ns(s2)=1==nv). No counter-evidence. No refutation. Trace
  byte-identical.
- K-CV4-1 double2 fixture: R0 stays PROVISIONAL throughout
  (never ACTIVE). Not checked. Trace byte-identical.

### Deferred (considered, not implemented)

Per-action contest competition between delay attribution and
law-change hypotheses (the red team's suggested principled fix).
Deferred again: it is a redesign, not a repair, and the builder's
CV4 analysis stands (action-blind contest resolves OLD-LAW-WINS;
opening contests on explained vars alters the frozen 3D trace).
R5 addresses the confirmed severity note (permanence) at the
mechanism level with zero trace impact on frozen bars.

## Frozen kill bars

- **K-CV5-1 (harm closed, no overcorrection):**
  (a) cv4_adv_perm_obs.txt + cv4_adv_perm_probe.txt through
  causalv5.zag: `# delay rule R0 REFUTED at seq 10` emitted;
  the `# DL R0` dump shows `st=PROV`; the harm probe predicts
  `Q (0 0 1) | 1 -> (0 0 1)` (uncorrupted; was (0,0,2) under
  CV4). 3/3 byte-identical.
  (b) cv4_adv_vary_obs.txt + cv4_adv_vary_probe.txt through
  causalv5.zag: R0 still CONFIRMS at seq 8 with st=ACT; trace
  byte-identical (cmp) to the red team's committed CV4 raw
  output for X-CV4-1. R5 revises; it does not prevent the
  (correct, underdetermined) confirmation.
- **K-CV5-2 (regressions):** all 10 frozen fixtures re-run
  through causalv5.zag are byte-identical (cmp) to the committed
  CV4_*_RUN.txt: the 9 K-CV3 fixtures (double, thr, mask, 3i2,
  3c, 3d, 3i, B2, C2) and the K-CV4-1 fixture (double2). This
  subsumes K-CV4-1 (identical contexts stay PROVISIONAL) and
  K-CV4-2.
- **K-CV5-3 (determinism):** every fixture run 3/3, byte-identical
  (this is K-CV4-3).

Verdict rule: SURVIVES iff K-CV5-1, K-CV5-2, K-CV5-3 all PASS.
Any FAIL -> KILLED (mechanism) or DOWNGRADED per the failing bar.
No frozen bar may be weakened. Classification stays bounded L2;
nothing here bears on L3.

## Governance

- Pure Zag. No Python at any stage (fixtures, implementation,
  builds, runs, analysis, hashing).
- Prereg committed strictly before any implementation, build, or
  run. Ordering verified via merge-base --is-ancestor.
- causalv5.zag starts as a byte-verified copy (cmp) of committed
  causalv4.zag; the result commit contains the full source plus
  a diff summary of exactly the R5 change.
- Only H-CAUSALV5-owned paths staged/committed
  (docs/lab/research-lead/overnight-20260928/causalv5_repair/).
  Concurrent workers' files untouched. No broad git add.
- Binaries built in /tmp only, never committed.
- No em dashes in loop documentation.
