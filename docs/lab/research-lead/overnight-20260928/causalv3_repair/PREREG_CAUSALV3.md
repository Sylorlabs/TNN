# Preregistration: H-CAUSALV3 (Causal Vocabulary Repair, Round 3)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any H-CAUSALV3 implementation)
**Researcher:** H-CAUSALV3 Repair Researcher (subagent)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV2 DOWNGRADED (red team CV2_ADV_RESULT.md, 2 attacks succeed).
This hypothesis repairs both downgrade findings at the mechanism level.

## Background and failures being repaired

H-CAUSALV2 SURVIVES 4/4 (bounded L2) was DOWNGRADED by independent red team:

- **X-CV2-1 (spurious confirmation via two positioned confounders):**
  SUCCEEDED. In fixture cv2_adv_double_obs.txt, two positioned
  action-1 episodes (seq3, seq7) each preceded a law-change flip
  (a0 at seq4, a2 at seq8) where s2 stayed 0. delay_clean's
  correlational cross-check passed for both; dl_add_or_support
  matched on (cause, delay, var) only, so the second confounder
  CONFIRMED the first: `# DL R0 cause=1 d=1 var=s2 fx=SET(0)
  st=ACT support=2`. The ACTIVE spurious rule corrupted the harm
  probe (`Q (0 0 1) | 1 -> (0 0 0)`, WRONG; action 1 is a no-op).
  Root cause (design-level): (a) delay attribution explains
  stasis (0->0) as if it were an effect; the SET(nv)
  representation cannot express prevention, so a "delayed cause"
  of no-change is indistinguishable from no effect; (b) the
  confirmation match key is nv-blind, so even outcome-mismatching
  episodes would confirm. The frozen R1 rationale ("Genuine delays
  repeat; confounders do not") is falsified under adversarial
  stream control.

- **X-CV2-2 (threshold fiat between t=0 and t=1):** SUCCEEDED. In
  fixture cv2_adv_thr_obs.txt (s0 values {0,2} observed, true law
  blocked iff s0>=2), THR t=0, THR t=1, and EQ all resolve with 2
  cells. Enumeration order (t=0, t=1, then EQ; first-added wins
  ties via strict `<`) selected t=0 by fiat. The probe at the
  unseen s0=1 predicted (1,1,0) (blocked), WRONG (truth (1,0,0);
  warm works). Root cause (design-level): tied candidates
  generalize differently to unseen values, so the tie-break is
  harm-capable, not a representational preference. The code
  comment claiming "tied candidates are behaviorally identical"
  is true only on observed cells.

Revised classification stands: bounded L2, narrowed. Not L3.

## Repairs (frozen mechanism specification)

causalv3.zag = byte-copy of frozen causalv2.zag (md5
ed81506fba7c52bcbc98e639d71dc275) plus ONLY the R1a/R1b/R2
changes below. No other mechanism change.

### R1a: Delay attribution requires a genuine change

In `delay_clean`, at the top (before any other check):

```
if(ep_ns(W,e,v)==ep_s(W,e,v)){return 0;}
```

with the comment: a delayed cause must explain a genuine change.
Stasis (ns==s) is not an effect the SET(nv) representation can
attribute; such contradictions (entry predicted change, observed
stasis) belong to the contest machinery, not delay attribution.

Rationale: in X-CV2-1 both confounded episodes show s2 0->0
(stasis). The contradiction that triggers delay_attribution is
"the entry predicted SET(1), observed 0" -- the entry's error,
honestly a law change, which the contest machinery must see. In
the genuine obs3d world both attributed episodes (seq7, seq11)
show lamp 0->1 (genuine changes), so the K-CV3 genuine-delay bar
is preserved. In the K-CV2-1 masking fixture seq4 shows s2 0->0,
so no PROVISIONAL rule is created at all (stronger than K-CV2-1's
"no ACTIVE rule").

Documented limitation: genuine delayed prevention (a delayed
cause keeping v unchanged when it would otherwise have changed)
is not learnable. The mechanism learns delayed changes only.
This is a narrowing of the "delayed-cause" claim, stated here.

### R1b: Outcome-aware confirmation matching

In `dl_add_or_support`, the support-match key becomes
(cause, delay, var, outcome): the scan additionally requires
`dl_fp(W,r)==nv`. A supporting episode with a different outcome
does NOT increment support; it creates a separate PROVISIONAL
rule (competing hypothesis) via the existing creation path.

Rationale: confirming SET(0) with a SET(1) episode is
incoherent. Note (honest): R1b alone does NOT close X-CV2-1
(both confounders share outcome 0); R1a closes it. R1b is
coherence hygiene. No demotion of ACTIVE rules on competing
evidence (future work, documented).

### R2: Within-variable ties become AMBIGUOUS (no enumeration fiat)

In `split_search` Phase 1, replace the per-variable best
(strict-`<` first-added wins ties) with minimum-collection: for
each variable, compute the minimum cell count over its resolving
candidates and collect ALL candidates achieving it.

- Exactly one variable has candidates and its minimum is unique:
  apply it (unchanged behavior; 3i2's THR t=1 2-vs-3 still wins
  outright).
- Otherwise (a variable with a tied minimum, or multiple
  variables with candidates): mark the entry ST_AMB over the
  union of all minimum-achieving candidates (existing
  en_cand_set storage, cap 8 slots with an explicit WARN if
  exceeded; amb_update refutes non-resolving candidates over
  time exactly as before).
- nvars==0: Phase 2 unchanged.

Enumeration order is now provably irrelevant to tie outcomes
(all tied minima are collected regardless of order); the
THR-before-EQ amendment tie-break is removed, not merely
disclosed. The H-CAUSALV2 tie-break ablation is moot and is
retired (documented, not silently dropped).

Provenance: when a within-variable tie exists (or nvars==1 with
a tie), emit `# entry N AMBIGUOUS over K tied candidates (no
fiat split)`. For the multi-variable no-internal-tie case, keep
the exact old message `# entry N AMBIGUOUS over K candidates`
(B2 byte-identical).

Rationale: tied candidates generalize differently to unseen
values (X-CV2-2: t=0 vs t=1 disagree at s0=1; THR vs EQ differ
on unseen-value coverage). Withholding via the existing
AMBIGUOUS machinery (agreed-under-ambiguity predicts only on
candidate agreement, else WITHHOLD) is the honest posture.

Documented limitation: amb_update refutes non-resolving
candidates but does not re-optimize by cell count among
survivors (e.g. old 3i at seq5: THR t=0 at 2 cells vs EQ at 3
cells stays ambiguous). Re-optimization is future work.

## Explicit supersessions (not silent)

- **S1 (old 3i trace):** the `# SPLIT-THR entry 3 by s0 threshold
  0 into 2` line (and children entries 5, 6) is replaced by
  `# entry 3 AMBIGUOUS over 2 tied candidates (no fiat split)`
  (THR t=0 vs EQ, 2-vs-2 tie). The 3i probe predictions are
  expected UNCHANGED via agreed-under-ambiguity (both tied
  candidates predict (1,1,0) on I1 and (0,0,1) on I2; verified
  by hand analysis in this prereg, confirmed at execution). 3i
  becomes the tie-withholding demonstration; 3i2 remains the
  threshold-learning demonstration.
- **S2 (tie-break ablation):** retired as moot (enumeration order
  provably irrelevant under minimum-collection).

## Frozen fixtures (md5, reused byte-identical)

- double (X-CV2-1): causalv2_adversary/cv2_adv_double_obs.txt
  (b6fce3dde4c7768602b1a56da7d3b37e),
  causalv2_adversary/cv2_adv_double_probe.txt
  (19e0a41655e781cd06de4a9cf78c6a0d)
- thr (X-CV2-2): causalv2_adversary/cv2_adv_thr_obs.txt
  (00a4fce411fa91fd79c1bfbb758c50f1),
  causalv2_adversary/cv2_adv_thr_probe.txt
  (fe34ea27a55998b80f186c9138e4a503)
- mask (K-CV2-1): causalv_adversary/cv_adv_mask_obs.txt
  (6f93b3fcb36ab9b890175c46a378faeb),
  causalv_adversary/cv_adv_harm_probe.txt
  (19e0a41655e781cd06de4a9cf78c6a0d)
- 3i2 (K-CV2-2): causalv2_repair/obs3i2.txt
  (48e49c7563e26b457964499407d6d8df),
  causalv2_repair/probe3i2.txt (679954e5b0d82c1de9b1b86669b367f5)
- 3c: causal3/obs3c.txt (67d5244a00ab96c14af7134c33a35c15),
  causal3/probe3c.txt (8efcff12c671adac4b5b9e33bacd93ac)
- 3d: causal3/obs3d.txt (21ab3ba4067e49a71f5f25fb15cd2091),
  causal3/probe3d.txt (0ecab21ebd0ec990ddf0e5a6bb411271)
- 3i: causal3/obs3i.txt (0bdaaffde738f924bd92ab9bc9903910),
  causal3/probe3i.txt (6ca83d043a37212ec503b3be258be2a5)
- B2: causal/obs_B2.txt (8337498d64687404f9be2f83a05109f6),
  causal/probe_B2.txt (eb6803440eab62fc853a060c38ae52f2)
- C2: causal/obs_C2.txt (e072a91cca92802c7b7aace59b782fee),
  causal/probe_C2.txt (868ee716b0572dd0e78d9a57f1add397)

## Kill Bars (FROZEN, all must pass for H-CAUSALV3 to survive)

- **K-CV3-1 (double confounder):** cv2_adv_double_obs.txt through
  causalv3: ZERO delay rules created (not even PROVISIONAL; the
  dump shows no `# PROVISIONAL-DELAY-RULE` and no `# DL R`
  lines). The harm probe `Q (0 0 1) | 1` must NOT predict
  `(0,0,0)`. ((0,0,1) or WITHHOLD both pass; (0,0,0) fails.)
- **K-CV3-2 (threshold tie):** cv2_adv_thr_obs.txt through
  causalv3: the a3 entry is ST_AMB over exactly 3 tied
  candidates (THR t=0, THR t=1, EQ) with the `(no fiat split)`
  provenance. The probe `Q (1 1 0) | 3` must WITHHOLD (not
  predict (1,1,0)).
- **K-CV3-3 (regressions):**
  (a) mask: no delay rule created; harm probe not (0,0,0).
  (b) 3i2: byte-identical to committed CV2_3I2_RUN.txt
  (`# SPLIT-THR entry 3 by s0 threshold 1 into 2`, all 4 probes
  correct).
  (c) 3c, 3d, B2, C2: byte-identical to committed
  CV2_3C_RUN.txt, CV2_3D_RUN.txt, CV2_B2_RUN.txt, CV2_C2_RUN.txt.
  (d) 3i: trace shows the S1 supersession (AMBIGUOUS over 2
  tied candidates); probe predictions (1,1,0), (0,0,1),
  (2,0,0) unchanged.
- **K-CV3-4 (determinism):** all of the above 3/3 byte-identical
  across runs.

## Governance

- Prereg committed alone before any implementation edit or test
  run; ordering verified via merge-base --is-ancestor.
- Pure Zag throughout: no Python in implementation, fixtures,
  builds, runs, or analysis. Shell inspection via
  grep/cmp/md5sum only.
- Only owned files staged/committed
  (causalv3_repair/PREREG_CAUSALV3.md, causalv3.zag,
  CV3_*_RUN.txt, CV3_RESULT.md). Concurrent workers' files
  untouched. No binaries committed (builds in /tmp only).
- No em dashes in loop documentation.
- Classification: bounded L2, narrowed. Not L3.
