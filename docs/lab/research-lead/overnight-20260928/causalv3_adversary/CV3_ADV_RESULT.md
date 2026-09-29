# H-CAUSALV3 Red Team: Adversary Report (CV3-ADV)

**Date:** 2026-09-29 (PDT)
**Researcher:** H-CAUSALV3 Red Team (subagent)
**Branch:** tnn-native-lab
**Prereg:** PREREG_CV3_ADV.md (frozen at commit 72fd6f3ac, strictly before
any attack fixture, code, or execution)
**Target:** H-CAUSALV3 SURVIVES (9/9), causalv3.zag (committed)
**Verdict: H-CAUSALV3 DOWNGRADED (not killed).**

One of four preregistered attacks succeeds (X-CV3-1). One succeeds as
a preregistered boundary (X-CV3-3). Two fail (defense holds). The frozen
K-CV3-1..K-CV3-4 bars are not invalidated; the downgrade narrows the
repair claims.

## X-CV3-1 (genuine-change double confounder): SUCCEEDS — DOWNGRADE

Both frozen kill criteria hold.

**Fixture** (cv3_adv_double2_obs.txt, md5 d8a3375f3df376d134c5ee9e7093231e):
8 episodes. seq1-2 teach a0: s2:=1. seq3 positions action 1 (no-op).
seq4 is a law-change flip (a0, s2 0->2, GENUINE CHANGE). seq5-6 teach
a2: s2:=1 in a separate entry. seq7 positions action 1 again. seq8 is
the second law-change flip (a2, s2 0->2, GENUINE CHANGE).

**Observed** (3/3 byte-identical, md5 d32d0c76230278c094ba81953f0cbbd8):
```
# PROVISIONAL-DELAY-RULE R0: cause a=1 d=1 -> s2 SET(2) support=1 (unconfirmed)
# delay-attributed var s2 of seq 4 to R0
# delay rule R0 CONFIRMED at seq 8 support=2 (provisional -> active)
# delay-attributed var s2 of seq 8 to R0
# DL R0 cause=1 d=1 var=s2 fx=SET(2) st=ACT support=2
=== PROBES ===
Q (0 0 1) | 1 -> (0 0 2)
```

Criterion (a): the dump shows `cause=1 d=1 var=s2 fx=SET(2) st=ACT
support=2`. The spurious correlation is CONFIRMED to ACTIVE. HOLD.

Criterion (b): the harm probe predicts `Q (0 0 1) | 1 -> (0 0 2)`.
Action 1 is a no-op throughout (seq3, seq7 leave state unchanged),
so the truth is (0,0,1). The ACTIVE spurious rule fired and
corrupted the prediction. HOLD.

**Why it works (mechanism analysis):** R1a requires genuine change
(ep_ns != ep_s). Both confounded episodes show s2 0->2 (genuine).
delay_clean's correlational cross-check passes because the two
positioned confounders are "clean": every a0 episode with outcome
s2=2 was preceded by action 1, and every a0 episode with a different
outcome was not. dl_add_or_support matches on (cause, delay, var,
outcome); both confounders share outcome 2, so R1b does not block.
The second confounder confirms the first to ACTIVE.

**What this means:** R1a closes the STASIS confounder subclass
(X-CV2-1), but NOT the genuine-change confounder subclass. The
prereg's R1a rationale ("Stasis is not an effect... such
contradictions belong to the contest machinery") assumes that
genuine change implies genuine causation. This is false: a
positioned no-op action can coincide with a genuine law-change
flip. The "confounders do not repeat" rationale remains false
under adversarial stream control, even with R1a+R1b.

**Scope:** The frozen K-CV3-1 bar (stasis double fixture) still
passes. This is a NEW attack, not a reopening. But the general
claim that "positioned confounders cannot confirm spurious rules"
is narrowed to stasis confounders only.

## X-CV3-2 (two covering candidates agree wrong): FAILS — defense holds

**Fixture** (cv3_adv_twothr_obs.txt): s0 in {0,2} with s2 conflict.
**Observed:** `# entry 3 AMBIGUOUS over 3 tied candidates (no fiat
split)`, `CAND=[THR s0<=0,THR s0<=1,EQ s0]`, `Q (1 1 0) | 3 ->
WITHHOLD` (3/3 byte-identical).

The two THR candidates cover s0=1 but DISAGREE (THR t=0 predicts
from {s0>0} cell, THR t=1 predicts from {s0<=1} cell, different fx).
EQ abstains. Disagreement → WITHHOLD. As preregistered, two
same-variable THR candidates cannot agree-wrong on an unseen value
while maintaining the split (agreement would imply no UNRES, hence
no split). The ambiguity machinery is robust against this shape.
Positive finding.

## X-CV3-3 (vacuous unanimity via abstention): SUCCEEDS — BOUNDARY

Both frozen kill criteria hold.

**Fixture** (cv3_adv_vac_obs.txt): s0 in {0,1}. s0=0 works
((0,1,0)->(0,0,1)), s0=1 blocked ((1,1,0)->(1,1,0)). s1 and s2
conflict, triggering split. Tie: THR s0<=0 (2 cells) vs EQ s0
(2 cells). THR s0<=1 does not resolve (1 nonempty cell).

**Observed** (3/3 byte-identical, md5 88fbd914fcfa1f36f4fece6edec1c56e):
```
# entry 3 AMBIGUOUS over 2 tied candidates (no fiat split)
# ENTRY 3 a=3 cond=[] st=3 fx=[UNCH,UNRES,UNRES] par=-1 ne=2 CAND=[THR s0<=0,EQ s0]
Q (2 1 0) | 3 -> (2,1,0)
```

Criterion (a): ST_AMB over 2 tied candidates. HOLD.
Criterion (b): Probe Q (2 1 0) | 3 predicts (2,1,0) confidently.
THR s0<=0 covers (cell {s0>0}={1}, fx=[UNCH,UNCH,UNCH] from the
blocked episode). EQ s0 abstains (no s0=2 episodes). Single
covering candidate → "unanimous" → predict. Adversary-defined
truth at s0=2 is (2,0,1) [works]. Predicted (2,1,0) [blocked].
WRONG. HOLD.

**Interpretation (preregistered as BOUNDARY):** This confirms the
documented limitation: "AMEND1 means a single opinionated candidate
predicts alone when all others abstain." Pre-AMEND1 (veto rule),
EQ's non-coverage would have forced WITHHOLD. AMEND1 trades B2's
veto-technicality withhold (correct unanimous suppressed) for
vacuous-unanimity confident predictions (wrong single opinion
amplified). The behavior is disclosed in CV3_RESULT.md section 7,
but is now empirically demonstrated as harm-capable. Not a
downgrade of the survival claim (frozen bars intact, B2 fix real),
but a confirmed boundary on AMEND1's safety.

## X-CV3-4 (regression on frozen bars): FAILS — regression holds

All 9 frozen fixtures re-run through the rebuilt committed
causalv3.zag, compared via cmp to committed CV3_*_RUN.txt:
- CV3_DOUBLE_RUN.txt: PASS (byte-identical)
- CV3_THR_RUN.txt: PASS (byte-identical)
- CV3_MASK_RUN.txt: PASS (byte-identical)
- CV3_3I2_RUN.txt: PASS (byte-identical)
- CV3_3C_RUN.txt: PASS (byte-identical)
- CV3_3D_RUN.txt: PASS (byte-identical)
- CV3_3I_RUN.txt: PASS (byte-identical)
- CV3_B2_RUN.txt: PASS (byte-identical)
- CV3_C2_RUN.txt: PASS (byte-identical)

No frozen bar fails to reproduce. The downgrade narrows the repair
claims only.

## Revised classification

Bounded L2, narrowed. R1a genuinely neutralizes stasis confounders
(K-CV3-1 stands), but genuine-change positioned confounders still
confirm harmful ACTIVE spurious rules; the "delay attribution
requires genuine change" gate is necessary but not sufficient.
R2's tie-ambiguity is robust against multi-candidate
agreement-wrong (X-CV3-2 fails). AMEND1's abstention enables
vacuous-unanimity confident predictions (X-CV3-3 boundary
confirmed). Not L3 (unchanged).

## Methodology and governance

- Prereg PREREG_CV3_ADV.md committed at 72fd6f3ac before any attack
  fixture, code, or execution. Ordering verified (merge-base
  --is-ancestor). Prereg content md5-verified intact in commit.
- **Sweep disclosure:** the prereg commit also contained 4 files
  from a concurrent worker (ROUTER6_*). My prereg content verified
  byte-intact by md5. Only the commit message is mine for those
  files. Recorded, not hidden.
- Attack fixtures frozen verbatim in the prereg; executed unchanged.
- Target binary compiled from the unmodified committed
  causalv3_repair/causalv3.zag with znc 2026.07.0-dev; builds in
  /tmp/cv3adv only, no binaries committed.
- Pure Zag. No Python anywhere (fixtures, execution, analysis).
  Shell inspection via grep/cmp/md5sum only.
- No em dashes in this documentation.
- Only adversary-owned files staged/committed
  (causalv3_adversary/PREREG_CV3_ADV.md, cv3_adv_*.txt,
  CV3_ADV_RESULT.md). Concurrent workers' files untouched.
- 3/3 byte-identical runs for all empirical claims.

## Suggested follow-ups for the parent

1. H-CAUSALV4: confirmation should require more than correlational
   cleanliness. Options: require supporting episodes from distinct
   cause contexts; cap ACTIVE rule influence; flag repeated
   confounder patterns. The genuine-change double fixture is the
   regression test.
2. Consider whether delay attribution should compete with the
   contest machinery (law-change hypothesis) rather than preempting
   it. In X-CV3-1, the "law changed" explanation is never considered
   because delay attribution preempts.
3. Update the research paper's H-CAUSALV3 section with this downgrade.
