# H-CAUSALV2 Red Team: Adversary Report (CV2-ADV)

**Date:** 2026-09-29 (PDT)
**Researcher:** H-CAUSALV2 Red Team (subagent)
**Branch:** tnn-native-lab
**Prereg:** PREREG_CV2_ADV.md (frozen at commit 8217143ab, strictly before
any attack fixture, code, or execution)
**Target:** H-CAUSALV2 SURVIVES (4/4), causalv2.zag
**Verdict: H-CAUSALV2 DOWNGRADED (not killed).**

Two of four preregistered attacks succeed (X-CV2-1, X-CV2-2). The frozen
K-CV2-1..K-CV2-4 bars are not invalidated; both downgrades narrow the
repair claims.

## X-CV2-1 (spurious confirmation via two positioned confounders): SUCCEEDS

Both frozen kill criteria hold.

**Fixture** (cv2_adv_double_obs.txt, md5 b6fce3dde4c7768602b1a56da7d3b37e):
8 episodes. seq1-2 teach a0: s2:=1. seq3 positions action 1 (no-op).
seq4 is the first law-change flip (a0, s2 stays 0). seq5-6 teach a2:
s2:=1 in a separate entry. seq7 positions action 1 again. seq8 is the
second law-change flip (a2, s2 stays 0).

**Observed** (CV2_ADV_DOUBLE_RUN.txt, md5 ff454d2c2d05c9afb76bf2b1794dfe02,
3/3 byte-identical, sha256 c624af5b7bbb7b456e0e6817c59dbc0cf7978aecb54c3ce48fc2e19958f062c5):
```
# PROVISIONAL-DELAY-RULE R0: cause a=1 d=1 -> s2 SET(0) support=1 (unconfirmed)
# delay-attributed var s2 of seq 4 to R0
# delay rule R0 CONFIRMED at seq 8 support=2 (provisional -> active)
# delay-attributed var s2 of seq 8 to R0
# DL R0 cause=1 d=1 var=s2 fx=SET(0) st=ACT support=2
=== PROBES ===
Q (0 0 1) | 1 -> (0 0 0)
```

Criterion (a): the delay-rule dump shows `cause=1 d=1 var=s2
fx=SET(0) st=ACT support=2`. The spurious correlation is CONFIRMED to
ACTIVE. HOLD.

Criterion (b): the harm probe predicts `Q (0 0 1) | 1 -> (0 0 0)`.
Action 1 is a no-op throughout the fixture (seq3, seq7 leave s2
unchanged), so the truth is (0,0,1). The ACTIVE spurious rule fired
and corrupted the prediction. HOLD.

**Why it works (mechanism analysis):** delay_clean's correlational
cross-check requires same-outcome episodes to share the cause action.
Two positioned confounders with the same (cause=1, delay=1, var=s2)
and the same outcome value (s2:=0) satisfy this by construction, so
both pass. dl_add_or_support matches on (cause, delay, var) only;
the outcome value is not part of the match key, so the second
confounder confirms the first. The R1 rationale, frozen in
PREREG_CAUSALV2.md ("Genuine delays repeat; confounders do not"), is
falsified under adversarial stream control: a positioned confounder
CAN be repeated, and the two-tier system then produces a harmful
ACTIVE spurious rule. The single-confounder fix (K-CV2-1) is real,
but the repair claim is narrowed: the two-tier system is humbler
against one-off confounders, not safe against repeated ones.

Side observation (verified by reading fx_codes_f): delay-explained
episodes (ep_dx flag) are excluded from the entry fx computation, so
entry 0 stayed ACTIVE with SET(1) after seq4 instead of going
CONFLICTED as in the single-confounder fixture (where the second,
unexplained a0 episode forced UNRES). This is consistent mechanism
behavior, not a defect.

## X-CV2-2 (threshold fiat between t=0 and t=1): SUCCEEDS

Both frozen kill criteria hold.

**Fixture** (cv2_adv_thr_obs.txt, md5 00a4fce411fa91fd79c1bfbb758c50f1):
true world law (frozen): depressurize (action 3) is blocked iff temp
(s0) >= 2; training observes only temp 0 and 2:
```
T 0 1 0 | 3 | 0 0 1
T 2 1 0 | 3 | 2 1 0
```
At seq2 the a3 entry holds s0 values {0,2} with conflicting pressure
outcomes. THR t=0 ({s0<=0}|{s0>0}): 2 cells, resolves. THR t=1
({s0<=1}|{s0>1}): 2 cells, resolves. EQ: 2 cells, resolves. Code
inspection of split_search confirms enumeration order t=0, t=1, then
EQ, with first-added winning ties via strict `<`.

**Observed** (CV2_ADV_THR_RUN.txt, md5 a87e26c862fbfe201df557334880f8f6,
3/3 byte-identical, sha256 318206affab60018fb9ac9167ef3348af0991627007ab7d8f1615e2e40ad309c):
```
# SPLIT-THR entry 3 by s0 threshold 0 into 2
# ENTRY 5 a=3 cond=[s0<=0] fx=[UNCH,SET(0),SET(1)]
# ENTRY 6 a=3 cond=[s0>0] fx=[UNCH,UNCH,UNCH]
=== PROBES ===
Q (1 1 0) | 3 -> (1,1,0)
```

Criterion (a): `# SPLIT-THR entry 3 by s0 threshold 0 into 2`. The
first-enumerated threshold won the three-way tie by fiat. HOLD.

Criterion (b): the probe `Q (1 1 0) | 3` (s0=1, never observed)
predicts `(1,1,0)` (blocked). Under the frozen true law (blocked iff
s0>=2), warm works: truth is (1,0,0). WRONG. HOLD.

**Why it matters:** the two resolving thresholds generalize
DIFFERENTLY to the unseen value s0=1 (t=0: {s0>0} -> UNCH; t=1:
{s0<=1} -> SET(0)). The enumeration order picked the wrong one. This
refutes the code comment's framing that "tied candidates are
behaviorally identical" (split_search, causalv2.zag): they are
identical only on observed cells, while the learner predicts on
unseen cells where the fiat choices differ. The amendment tie-break
is not merely a "representational preference"; it is harm-capable in
tie cases. R2's 3i2 world (2-vs-3, genuinely data-driven) is
unaffected, but the tie-break remains in the code and remains
load-bearing wherever a tie occurs.

## X-CV2-3 (regression on frozen bars): FAILS (regression holds)

All four K-CV2 worlds re-run through the unmodified committed
causalv2.zag:
- K-CV2-1 mask + harm: sha256 f8255b2b... (matches committed),
  harm probe `Q (0 0 1) | 1 -> (0 0 1)` CORRECT.
- K-CV2-2 3i2: sha256 f522cc7a... (matches committed), all 4 probes
  correct.
- K-CV2-3: obs3c sha256 bbe28798... (match), obs3d sha256
  74d2c5b3... (match), obs3i/probe3i byte-identical to CV2_3I_RUN.txt
  (cmp), obs_B2/probe_B2 byte-identical to CV2_B2_RUN.txt (cmp),
  obs_C2/probe_C2 byte-identical to CV2_C2_RUN.txt (cmp).
- K-CV2-4: attack fixtures 3/3 byte-identical (sha256, above).

No frozen bar fails to reproduce. The downgrade narrows the repair
claims only.

## X-CV2-4 (source audit): FAILS (spec fidelity holds)

Direct reading of causalv2.zag:
- (a) R1 matches the frozen spec: ST_PROV=5 (line 97); new rules
  start PROVISIONAL (line 768); promotion at support>=2 (line 752)
  with honest CONFIRMED provenance; emit labels PROV/ACT (lines
  1031-1032).
- (b) The probe runner fires only ST_ACT rules (line 1075); the
  match scan accepts PROV+ACT solely for confirmation (line 748),
  per spec.
- (c) No test-answer literals in mechanism code (grep for fixture
  value patterns returns nothing outside comments).
- (d) dl_add_or_support match key is (cause, delay, var); the
  outcome value nv is not part of the key (line 748). This
  nv-blindness is the mechanism property X-CV2-1 exploits; it is
  spec-faithful, not a spec deviation.
- (e) split_search enumerates THR t=0..vmax-1 before EQ per variable
  (lines 566-579); per-variable best is fewest cells with first-added
  winning ties (strict `<`, lines 588-592). The tie-break X-CV2-2
  exploits is the code as specified.

No spec deviation found. The vulnerabilities are design-level, not
implementation errors.

## Revised classification

Bounded L2, narrowed. The R1 two-tier system genuinely neutralizes
single positioned confounders (K-CV2-1 stands), but repeated
positioned confounders still confirm a harmful ACTIVE spurious rule;
"confounders do not repeat" is false under adversarial control. The
R2 threshold is genuinely data-driven on 3i2 (K-CV2-2 stands), but
the amendment tie-break remains in the code and causes confident
wrong predictions on unseen values in tie cases. Not L3 (unchanged).

## Methodology and governance

- Prereg PREREG_CV2_ADV.md committed alone at 8217143ab before any
  attack fixture, code, or execution. Ordering verified
  (merge-base --is-ancestor against this result commit).
- Attack fixtures frozen verbatim in the prereg; executed unchanged
  (md5s recorded above).
- Target binary compiled from the unmodified committed
  causalv2_repair/causalv2.zag with znc 2026.07.0-dev; builds in
  /tmp/cv2adv only, no binaries committed.
- Pure Zag. No Python anywhere (fixtures, execution, analysis).
  Shell inspection via grep/sed/sha256sum/cmp/md5sum only.
- No em dashes in this documentation.
- Only adversary-owned files staged/committed (PREREG_CV2_ADV.md,
  cv2_adv_double_obs.txt, cv2_adv_double_probe.txt,
  cv2_adv_thr_obs.txt, cv2_adv_thr_probe.txt, CV2_ADV_DOUBLE_RUN.txt,
  CV2_ADV_THR_RUN.txt, CV2_ADV_RESULT.md). Concurrent agents' files
  untouched.

## Suggested follow-ups for the parent

1. R1 rework: confirmation should require the outcome value to match
   (nv in the match key), or require supporting episodes from
   distinct cause contexts, or cap provisional influence so that a
   repeated confounder is at least flagged. The double-confounder
   fixture is the regression test.
2. R2 rework: ties should withhold or mark the threshold choice
   explicitly provisional (like delay PROV), rather than resolving
   by enumeration fiat. The t=0/t=1 fixture is the regression test.
3. Update the research paper's H-CAUSALV2 section with this
   downgrade.
