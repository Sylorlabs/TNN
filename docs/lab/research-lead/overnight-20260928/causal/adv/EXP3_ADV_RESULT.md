# H-EXP3 Red Team: Adversary Report (X-E3-1..X-E3-4)

Date: 2026-09-29. Pure Zag. Prereg frozen in commit fbea971e4 BEFORE
any attack fixture was built or any attack executed. Builder binary
compiled unmodified from adv/exp_invent3.zag; builder source never
edited. No Python at any stage.

## Verdict: H-EXP3 DOWNGRADED (not killed)

Two of four attacks succeed. The four frozen K-E3-1..K-E3-4 bars are
not retroactively altered (verified intact below); the source audit is
clean. The downgrades narrow the interpretation of both repairs: the
reachability flag overclaims in its positive direction, and the
ranking "safety verification" is a tautological re-computation.

## Attack results

### X-E3-1(b): SUCCESS -> DOWNGRADE (AGENT-SETUP-ABLE overclaim)

Fixture A1 (adv/x_e3_a1.txt): the 11 S1 episodes plus two lamp-toggle
episodes under action 3 (T 0 0 0 | 3 | 0 0 1 ; T 0 0 1 | 3 | 0 0 0).
The action-2 ambiguous entry is preserved: AMBIGUOUS action 2
candidates={s0,s2}, top pick still (0 0 1)|2, identical to S1.

Output:
```
CONTROLLABILITY (from 13 episodes): temp=controllable (4 changes);
pressure=controllable (3 changes); lamp=controllable (2 changes)
...
[0] state (0 0 1) | 2 :: s0 -> (0 1 1) ; s2 -> (0 0 1) :: differ=v1 ndiff=1
    REACHABILITY: AGENT-SETUP-ABLE
...
TOP PICK (by heuristic): state (0 0 1) | 2
REACHABILITY: AGENT-SETUP-ABLE
```

The label "AGENT-SETUP-ABLE" asserts the agent can set the pick up.
What the learner actually computed: each variable changed at least
once as an action outcome (ctrl[v]=1). What the learner did NOT
compute and does not represent:

1. Which action changes which variable. ctrl[] is per-variable; the
   action that changed lamp (action 3 in A1) is discarded. The
   learner cannot answer "which action do I apply to set lamp==1",
   yet labels the pick setup-able.
2. Whether the SPECIFIC required values are achievable. No
   per-value achievability check exists anywhere in the new code.
3. Whether the state as a combination is reachable. Variable-level
   change counts do not entail state-level reachability.

This contradicts the prereg's own conservative principle ("the
learner only knows what it has seen"): the learner saw lamp change
(under action 3), but has not seen that it can set up state (0,0,1)
for action 2 — it does not even know which action to use. The
positive label therefore silently recommends the pick as runnable on
evidence that does not support the claim — the exact failure mode
("silently recommended") the X-A1 repair was supposed to eliminate,
reintroduced in the positive direction.

The negative direction is sound: NEEDS-EXTERNAL-SETUP is
conservative (over-flags rather than under-flags) and names the
variable, required value, and change count. S1's K-E3-1 bar still
passes.

Downgrade: the reachability flag is reliable as a hazard flag but
unverified as a clearance. Honest repair direction: replace
"AGENT-SETUP-ABLE" with "no uncontrollable variables detected (setup
not verified)", or compute per-(action,variable,value)
achievability from the causal entries (which DO map actions to
effects, but are not consulted).

Determinism: 3/3 runs byte-identical, md5
96cbbd331a5c1af5d32085b6e1f91273.

### X-E3-1(a): CONFIRMED -> INFORMATIONAL (documented limitation)

S2 output confirms: temp=UNCONTROLLABLE (0 changes in 4 episodes)
though heat/cool change temp in the true world. The builder's prereg
explicitly predicted and disclosed this ("conservative and honest:
the learner only knows what it has seen"). Confirmed limitation, not
a kill. Recorded so the parent knows the flag's false-positive rate
on small episode sets is 100% of the conservative direction by
design.

### X-E3-2: SUCCESS -> DOWNGRADE (safety check is tautological)

Code-analysis proof (verified by reading exp_invent3.zag):

- Selection records state (t,p,l) only if: state unobserved AND
  ok==1 (pred_under resolves for ALL candidates) AND ncv>=2 AND
  agree==0 (stored predictions disagree). Predictions stored in
  rpr[nrec*9+cc*3+w].
- Safety loop, for each emitted state vx=ord[vr]: re-runs
  pred_under(W,ii,cv[vc],rt[vx],rp[vx],rl[vx],vout) — the IDENTICAL
  deterministic function (pure: reads W, writes only out; no RNG, no
  W mutation, verified at lines 841-858) on IDENTICAL inputs (W
  unmodified between the loops — only emits, sorts, and z_allocs
  intervene; same ii, cv, and the recorded state), then re-checks
  disagreement against the SAME stored rpr values.
- Therefore vok==1 and vagree==0 necessarily whenever the state was
  recorded; nsafe==nrec on every valid execution. The RANKING SAFETY
  VIOLATION branch is dead code.

Empirical: RANKING SAFETY is 3/3 (S1), 2/2 (S2), 3/3 (A1) across all
runs — consistent with the proof, since no fixture can produce a
violation short of nondeterminism or memory corruption.

The builder's claim — "This is a real check, not a label: if any
emitted state failed, it would be reported" — is literally true but
misleading: it implies discriminating power the check lacks. It
verifies determinism/memory-integrity, not discrimination.

Downgrade: the "verified safety property" sub-claim of the X-A2
repair is narrowed to "selection filter applied twice". The OTHER
half of the X-A2 repair stands untouched: the heuristic disclaimers
in output ("informativeness NOT validated", "TOP PICK (by
heuristic)") are real and honest, and the theoretical note
(2-candidate information equivalence) is correct.

### X-E3-3: BOUNDARY confirmed (informational)

Code inspection: ctrl[]/chgct[] are read ONLY by
emit_controllability and emit_reachability (both pure emit
functions). No downstream consumer: the flag does not affect
selection, ordering, withholding, or any decision. The ranked list
is emitted unchanged; the top pick is still presented as TOP PICK.

This matches the disclosed design ("reachability AWARENESS
(flagging), not reachability PLANNING"; "selection unchanged"). Not
a kill. Boundary for the parent: the flag annotates but does not
enforce — nothing stops the learner (or a downstream consumer
ignoring the text) from attempting a NEEDS-EXTERNAL-SETUP pick.

### X-E3-4: PASS (source audit clean)

(a) compute_controllable matches the prereg: scans EP_ACT episodes,
ns[v]!=s[v] sets controllable and increments the change count. No
domain knowledge.
(b) No hardcoded state literals, variable-specific logic, or
fixture-specific branches in new code. emit_varname maps indices to
display names only (labeling, not logic).
(c) Selection mechanism unchanged: diff against exp_invent.zag shows
5 removed lines, all comments or the two intentionally relabeled
header strings ("RANKED EXPERIMENTS n=" and "TOP PICK: state (");
all other changes are additive (4 new functions, 3 call sites, the
safety loop).
(d) Safety loop matches its description.

## Frozen bars re-verified (not altered)

- K-E3-1: S1 top pick flagged NEEDS-EXTERNAL-SETUP naming lamp (0
  changes). PASS (output above; md5 3eef51b231247c9e975c41df0de8fcd9
  matches builder's).
- K-E3-2: heuristic disclaimers present on ranked header and top
  pick; RANKING SAFETY line present. PASS.
- K-E3-3: no regression — S1 top pick (0,0,1)|2, S2 top pick
  (0,0,0)|2, S0 abstains (NO AMBIGUITY), md5s
  3eef51b231247c9e975c41df0de8fcd9 /
  429573a776e0f5dc721cd089118c5b2b /
  b51bdf8cc3713935f347928e124cd6da all match builder's. PASS.
- K-E3-4: 3/3 byte-identical per fixture. PASS.

## Revised classification

Bounded L2 discriminating-state selection with reachability flags
(reliable hazard flagging, unverified positive clearance) and
honestly-labeled heuristic ranking (tautological re-verification,
not independent validation). Not L3. Both H-EXP2 downgrades remain
ADDRESSED in their honest core (no silent recommendation in the
negative direction; no unsupported optimality claim); the repairs'
stronger readings do not survive.

## Artifacts (all committed, adversary-owned only)

- adv/PREREG_EXP3_ADV.md (frozen before execution, commit fbea971e4)
- adv/x_e3_a1.txt (attack fixture)
- adv/EXP3_ADV_RESULT.md (this file)
- adv/evidence/x_e3_a1_raw.txt (md5 96cbbd331a5c1af5d32085b6e1f91273)
- adv/evidence/x_e3_s1_raw.txt (md5 3eef51b231247c9e975c41df0de8fcd9)
- adv/evidence/x_e3_s2_raw.txt (md5 429573a776e0f5dc721cd089118c5b2b)
- adv/evidence/x_e3_s0_raw.txt (md5 b51bdf8cc3713935f347928e124cd6da)

Suggested builder repairs: weaken the positive label or compute
per-(action,variable,value) achievability from causal entries for
X-E3-1(b); either drop the safety loop or replace it with an
independent check (e.g., verify against held-out episodes not used
in selection) for X-E3-2.
