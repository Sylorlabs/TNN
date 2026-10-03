# H-CAUSALV5 Repair Result

**Date:** 2026-09-29 (PDT)
**Lane:** repair of H-CAUSALV4 after independent red-team downgrade
**Verdict: H-CAUSALV5 SURVIVES (K-CV5-1, K-CV5-2, K-CV5-3 all PASS)**
**Classification:** bounded L2, narrowed. Not L3.

## 1. What was broken (H-CAUSALV4 red team, 2026-09-29)

- **X-CV4-1 (varied-cause-context confounder):** SUCCEEDED. Two
  positioned action-1 episodes in DIFFERENT states (seq3 in
  (1,0,0), seq7 in (2,0,0)) each preceded a genuine law-change flip
  (a0 at seq4 s2 1->2, a2 at seq8 s2 1->2). R4's cause-context
  diversity check passes (contexts differ), so R0 CONFIRMED at seq
  8 with st=ACT; the harm probe `Q (0 0 1) | 1 -> (0 0 2)` is
  corrupted (truth (0,0,1)). Narrowed claim: "R4 blocks confirmation
  of confounders that repeat in an identical cause context. It does
  not close the genuine-change confounder class."
- **X-CV4-3 (counter-evidence permanence):** CONFIRMED as severity
  note. Ten action-1 no-op episodes appended after confirmation do
  not retract R0; the probe stays corrupted. No rule-retraction
  machinery existed. Once confirmed, corruption was permanent.
- **X-CV4-2, X-CV4-4:** HOLD (timing honest, 10/10 regression).

## 2. Preregistration and governance

- `PREREG_CAUSALV5.md` frozen and committed at **73be4f687**
  before any implementation, build, or run existed.
  Ordering verified: prereg commit is a strict ancestor of the
  result commit (merge-base --is-ancestor, checked at commit time).
- `causalv5.zag` is a byte-verified copy (cmp, md5
  f640a57f3690b7ab1da320dc238350ad matches the prereg record) of
  committed `causalv4.zag` plus exactly the frozen R5 change.
  No other mechanism change. No new memory; WSZ unchanged.
- Pure Zag throughout. No Python at any stage (prereg, edits,
  fixtures, builds, runs, greps, hashes, cmp). Toolchain:
  znc 2026.07.0-dev (edition 2026). Binaries built in /tmp/cv5
  only, never committed.
- Only H-CAUSALV5-owned paths staged/committed
  (docs/lab/research-lead/overnight-20260928/causalv5_repair/).
  Concurrent workers' files untouched. No broad git add.
- Determinism: every fixture run 3/3, byte-identical.
- No em dashes in loop documentation.

## 3. The repair (R5: counter-evidence retraction)

The X-CV4-1 confirmation is uncloseable by observation, and
H-CAUSALV5 does not attempt to close it. The prereg records the
argument: the 3D genuine delay and the X-CV4-1 confounded stream
are observationally equivalent with respect to every generic
confirmation criterion (2 no-op cause episodes, 2 contradiction
effect episodes, delay_clean passes with identical structure, and
the delay hypothesis at 1 rule is strictly simpler than the
2-law-change alternative in both cases). The learner's decision to
confirm in X-CV4-1 is the correct parsimony choice given the data;
the fixture's stipulated truth is not inferable. Any
observation-only check that confirms 3D must confirm X-CV4-1.

The genuine defect is IRREVERSIBILITY (X-CV4-3). R5 makes every
ACTIVE delay rule defeasible:

- New `dl_retract_check(W, e)`: for each ACTIVE rule
  (xa, d, v := nv), if `d>0` and the action at seq(e)-d was xa
  but the observed outcome `ep_ns(e,v) != nv`, the rule's
  prediction is falsified. The rule is demoted to PROVISIONAL
  (inert on predictions), its support resets to 1 (it must
  re-earn confirmation with a new diverse support), and a loud
  diagnostic is emitted:
  `# delay rule R<r> REFUTED at seq <s>: cause a=<xa> at seq
  <s-d> not followed by s<v>=<nv> (observed <obs>); demoted to
  PROVISIONAL`.
- Hooked in `learn_episode` AFTER `delay_attribution`, so the new
  episode's supporting role is settled before its refuting role.
- Re-confirmation uses the existing R4 path unchanged: a later
  diverse support promotes the demoted rule normally. Refutation
  is loud and re-confirmation requires new evidence; no silent
  resurrection.
- PROVISIONAL rules are not checked (inert; no harm to bound).

Why this is principled, not pattern-matching: it is the general
belief-revision requirement for defeasible causal claims. A
hypothesis that makes a falsified prediction is demoted. It does
not reference the attack fixture, the action involved, or the
number of counter-episodes. One counter-episode suffices because
the rule is a universal claim ("xa at seq-d causes s<v>:=<nv>").

## 4. Frozen kill bars: all pass

| Bar | Result |
|---|---|
| K-CV5-1(a): X-CV4-3 fixture, R0 refuted, probe uncorrupted | PASS: `# delay rule R0 REFUTED at seq 10: cause a=1 at seq 9 not followed by s2=2 (observed 0); demoted to PROVISIONAL`; dump shows `# DL R0 cause=1 d=1 var=s2 fx=SET(2) st=PROV support=1`; `Q (0 0 1) \| 1 -> (0 0 1)` (was (0,0,2) under CV4). 3/3 byte-identical (md5 2f9466445079f24da5f1265ad7c8cd76). |
| K-CV5-1(b): 8-episode X-CV4-1, confirmation not prevented | PASS: R0 still CONFIRMS at seq 8 with st=ACT; trace byte-identical (cmp) to the red team's frozen CV4 raw (md5 d32d0c76230278c094ba81953f0cbbd8). R5 revises; it does not prevent the (correct, underdetermined) confirmation. |
| K-CV5-2: all 10 frozen fixtures byte-identical | PASS: double, thr, mask, 3i2, 3c, 3d, 3i, B2, C2, double2 all cmp-identical to committed CV4_*_RUN.txt (md5s recorded below). Subsumes K-CV4-1 (double2 R0 stays PROVISIONAL) and K-CV4-2. |
| K-CV5-3: determinism | PASS: 3/3 byte-identical on all 12 runs. |

## 5. Revisability sanity check (beyond the bars)

X-CV4-3 fixture plus two appended episodes (a1 no-op in (0,0,1)
at seq19; a0 s2 0->2 contradiction at seq20, preceded by a1):
R0 is REFUTED at seq 10, then RE-CONFIRMED at seq 20
(support=2, diverse cause context (0,0,1) vs creation (1,0,0)).
The rule is revisable in both directions: refutation is loud,
re-confirmation requires new diverse evidence. Raw:
CV5_RECONF_RUN.txt (md5 f16358393295b46972959d8141d374b1, 2/2
identical). This was exploratory, not a frozen bar.

## 6. Raw evidence (committed, in causalv5_repair/)

- `CV5_PERM_RUN.txt` (K-CV5-1(a); 3/3 byte-identical;
  md5 2f9466445079f24da5f1265ad7c8cd76)
- `CV5_VARY_RUN.txt` (K-CV5-1(b); 3/3 byte-identical;
  md5 d32d0c76230278c094ba81953f0cbbd8, matches red-team CV4 raw)
- `CV5_RECONF_RUN.txt` (revisability check; 2/2 identical;
  md5 f16358393295b46972959d8141d374b1)
- `causalv5.zag` (md5 1fc56329a2d6da52104050e3e83406b4)
- `PREREG_CAUSALV5.md` (frozen at 73be4f687)
- Regression md5s (each cmp-identical to committed CV4_*_RUN.txt):
  double ef64c15c62371489a783e3efbfda7529,
  thr 37e29647c2408f656af8c9fee81ea19f,
  mask 1820ffc4af41133d821019bdd139f88f,
  3i2 b43d8135c4bba8b495807b7ae04dc5a7,
  3c ec4ad284201d43bbd3f78568ece38388,
  3d 77b0fcb0bd24135b280433ce391aac43,
  3i 5f1e22ffd94fbf1e98e6f94331fe7d82,
  b2 f60ba3ee56c8256d475b76c35285764e,
  c2 5ca096c566b4d7a7923a5bd06a171aee,
  double2 69496cc52890a42bfb35929499cc900e

## 7. Limitations and honest boundaries

- The 8-episode X-CV4-1 confirmation is NOT closed and cannot be
  closed by any observation-only mechanism without breaking 3D
  (prereg section "Why the X-CV4-1 confirmation is uncloseable by
  observation"). It is now a revisable hypothesis instead of a
  permanent commitment. This is the honest bound.
- R5 retracts on the FIRST counter-episode. A rule with 100
  supports and 1 counter-episode is demoted identically to a rule
  with 2 supports and 1 counter-episode. No graded confidence;
  the binary ACTIVE/PROVISIONAL status has no notion of
  evidential weight. A future round could add support-proportional
  demotion thresholds.
- R5 does not address the X-CV3-3 vacuous-unanimity boundary.
  Unchanged from CV3/CV4.
- Per-action contest competition between delay attribution and
  law-change hypotheses remains deferred (redesign, not repair).
- H-CAUSALV5 remains bounded L2: the repair makes causal
  commitments revisable; it does not advance the learning level.
  Not L3.

## 8. Commit lineage

- 73be4f687 PREREG H-CAUSALV5 FROZEN (prereg; strict ancestor)
- <this commit> H-CAUSALV5 implementation + evidence + result

Suggested paper line (for the research paper, parent lane):
"H-CAUSALV5 SURVIVES (K-CV5-1/2/3: counter-evidence retraction
closes X-CV4-3 permanence; R0 refuted at first counter-episode
and probe uncorrupted; 8-episode X-CV4-1 confirmation honestly
bounded as uncloseable underdetermination, now revisable; all 10
frozen fixtures byte-identical; bounded L2). Repair of
H-CAUSALV4."
