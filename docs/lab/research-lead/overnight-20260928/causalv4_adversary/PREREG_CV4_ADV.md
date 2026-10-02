# Preregistration: H-CAUSALV4 Independent Red Team (CV4-ADV)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any adversary fixture, build-for-attack, or run)
**Researcher:** H-CAUSALV4 Red Team (subagent, independent of builder)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV4 SURVIVES (K-CV4-1/2/3 all PASS; R4 cause-context
diversity; bounded L2). Assume the claim is false. Attack it.

## Target mechanism (from committed causalv4.zag, read-only)

- `dl_add_or_support`: PROVISIONAL->ACTIVE promotion requires
  support>=2 AND the confirming support's cause context (state
  triple at seq-d) differing from the creation cause context in at
  least one coordinate. Identical context: support recorded, rule
  stays PROVISIONAL (inert), diagnostic emitted. The check runs on
  every support while PROVISIONAL.
- `delay_clean`: genuine-change gate (R1a) + correlational
  cross-check scoped to episodes with the same action as the flip
  episode ("every positive episode preceded by xa; no negative
  episode preceded by xa").
- Builder's disclosed limitation (CV4_RESULT.md section 6): "R4
  raises the bar but does not close the genuine-change confounder
  class: an adversary positioning confounders in varying cause
  states defeats the diversity check. Explicit new attack surface
  for the independent red team."
- Builder's headline claim under test: "cause-context diversity
  closes genuine-change confounder confirmation."

## Attacks (all fixtures hand-derived below; no execution before prereg commit)

### X-CV4-1 (varied-cause-context confounder): the disclosed stronger adversary

Construction: the frozen X-CV3-1 double-confounder fixture, except
the two positioned action-1 confounder episodes occur in DIFFERENT
states. Both flips remain genuine law changes; both confounders
remain correlationally clean under delay_clean.

Fixture `cv4_adv_vary_obs.txt` (seq = file order, 1-based):

```
T 0 0 0 | 0 | 0 0 1
T 0 0 0 | 0 | 0 0 1
T 1 0 0 | 1 | 1 0 0
T 0 0 0 | 0 | 0 0 2
T 0 0 0 | 2 | 0 0 1
T 0 0 0 | 2 | 0 0 1
T 2 0 0 | 1 | 2 0 0
T 0 0 0 | 2 | 0 0 2
```

Rationale, step by step (hand-derived from the committed source):

- seq4: entry a0 predicts (0,0,1), observes (0,0,2): genuine-change
  contradiction on s2. delay_attribution tries d=1: xa=0 fails
  (obs_action_at(3)=a1); xa=1: delay_clean passes (genuine change;
  obs_action_at(3)=a1; global over a0-episodes: seq1 skipped
  (seq<=d), seq2 outcome 1 != 2 with ha=a0 != 1). Rule R0 created
  PROVISIONAL, creation cause context = state at seq3 = (1,0,0).
- seq8: entry a2 predicts (0,0,1), observes (0,0,2): genuine-change
  contradiction on s2. delay_attribution d=1, xa=1: delay_clean
  passes (genuine change; obs_action_at(7)=a1; global over
  a2-episodes: seq5, seq6 outcome 1 != 2 with ha=a0, a2 != 1).
  Support matches (cause=1, d=1, var=s2, outcome=2); support=2.
  Diversity: cause context of support = state at seq7 = (2,0,0),
  creation context = (1,0,0): differ in coordinate 0 -> CONFIRMED,
  R0 -> ACTIVE.
- Probe `cv4_adv_vary_probe.txt`:
```
H 0 0 0 | 1
Q 0 0 1 | 1
```
  ACTIVE R0 (cause=1, d=1) fires because ha[0]=a1: predicts
  (0,0,2). Truth: action 1 is a no-op in every episode of the
  fixture, so truth is (0,0,1). The probe is corrupted exactly as
  in X-CV3-1.

Kill criterion: the raw output contains BOTH
`# delay rule R0 CONFIRMED at seq 8` (st=ACT) AND the probe line
`Q (0 0 1) | 1 -> (0 0 2)`.
If both hold: ATTACK SUCCEEDS -> H-CAUSALV4 DOWNGRADED (not
killed): R4's diversity guarantee is defeated by the disclosed
stronger adversary; the headline "closes genuine-change
confounder confirmation" is false as stated and must be narrowed
to "closes identical-cause-context confounder confirmation".
Frozen K-CV4-1 (identical contexts) still holds; K-CV4-2/K-CV4-3
unaffected.
If R0 stays PROVISIONAL (or the probe is uncorrupted) for a
mechanism reason I missed: ATTACK FAILS, defense holds; report
the actual trace.

### X-CV4-2 (support-timing honesty): identical-then-diverse supports

Construction: creation in context X, a second support in the SAME
context X (must be withheld), then a third support in a DIFFERENT
context Y (must confirm). Tests that the per-support diversity
check neither fires early nor misfires late, and that emitted
support counts are honest.

Fixture `cv4_adv_timing_obs.txt`:

```
T 0 0 0 | 0 | 0 0 1
T 0 0 0 | 0 | 0 0 1
T 1 0 0 | 1 | 1 0 0
T 0 0 0 | 0 | 0 0 2
T 0 0 0 | 2 | 0 0 1
T 0 0 0 | 2 | 0 0 1
T 1 0 0 | 1 | 1 0 0
T 0 0 0 | 2 | 0 0 2
T 0 0 0 | 2 | 0 0 1
T 0 0 0 | 2 | 0 0 1
T 2 0 0 | 1 | 2 0 0
T 0 0 0 | 0 | 0 0 2
```

Hand-derived expectations: R0 created PROVISIONAL at seq4 with
creation context (1,0,0). seq8 support: context at seq7 =
(1,0,0), identical -> "NOT CONFIRMED at seq 8", stays PROVISIONAL,
support=2. seq12 support: context at seq11 = (2,0,0), diverse ->
"CONFIRMED at seq 12", support=3, R0 -> ACTIVE.
(delay_clean at seq12 over a0-episodes: seq2 ha=a0 ok; seq4
outcome 2 with ha=obs_action_at(3)=a1 ok; seq12 outcome 2 with
ha=obs_action_at(11)=a1 ok.)

Kill criteria (ANY fires -> mechanism bug):
(a) "CONFIRMED at seq 8" appears (identical context confirmed) ->
DOWNGRADED at minimum (diversity check bypassed); KILL if the
probe also corrupts on identical contexts (R4 wholly inert).
(b) No "CONFIRMED at seq 12" (diverse support fails to promote)
-> DOWNGRADED (check misfires; genuine diverse confirmation
broken).
(c) Emitted support counts diverge from actual supports
(e.g. "support=3" at seq8) -> honesty bug, DOWNGRADED.
If the trace matches expectations exactly: TIMING HOLDS
(defense holds; documents correct per-support behavior).

### X-CV4-3 (counter-evidence permanence): blast-radius probe

Construction: the X-CV4-1 fixture followed by ten action-1 no-op
episodes (counter-evidence: a1 at seq-d NOT followed by s2=2),
then the harm probe again.

Fixture `cv4_adv_perm_obs.txt` = `cv4_adv_vary_obs.txt` plus:

```
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 1 | 0 0 0
```

Probe `cv4_adv_perm_probe.txt`:
```
H 0 0 0 | 1
Q 0 0 1 | 1
```

The no-op episodes cause no contradiction, so delay_clean is never
re-invoked; the committed source contains no rule-retraction
machinery. Expected: R0 remains ACTIVE and the probe still yields
`Q (0 0 1) | 1 -> (0 0 2)`.

Kill criterion: if R0 is retracted/weakened by counter-evidence or
the probe uncorrupts -> unexpected self-healing -> ATTACK FAILS
(defense holds beyond the design). If R0 persists ACTIVE and the
probe stays corrupted -> blast radius CONFIRMED (the X-CV4-1
corruption is permanent under the current design; severity note
for the DOWNGRADE, not an independent kill).

### X-CV4-4 (regression): no silent changes

Re-run all 9 frozen K-CV3 fixtures plus the K-CV4-1 fixture through
a fresh build of the committed `causalv4.zag`, 3/3, and cmp against
the committed `CV4_*_RUN.txt`. Kill criterion: any byte difference
-> investigate; if the mechanism as committed differs from the
evidence -> DOWNGRADED (evidence does not match source). Expected:
all byte-identical (this is a verification, not an attack).

## Verdict rule

- X-CV4-1 SUCCEEDS -> H-CAUSALV4 DOWNGRADED (headline narrowed;
  R4 is a bar-raise against identical-context confounders, not a
  class-closer). Not killed: frozen K-CV4-1/K-CV4-2/K-CV4-3 stand.
- X-CV4-1 FAILS (defense holds) and X-CV4-2/3/4 show no bug ->
  H-CAUSALV4 SURVIVES this red team.
- Any X-CV4-2(a) KILL-level finding -> KILLED.
- No frozen bar may be weakened. A builder disclosure does not
  convert a successful falsification of the headline claim into a
  non-finding: the verdict headline is what is under test.

## Governance

- Pure Zag. No Python at any stage (fixtures are hand-written
  text; builds/runs/greps/hashes via shell and znc only).
- Prereg committed strictly before any adversary fixture is run
  or any attack build exists. (A build of the committed
  causalv4.zag for REPRODUCTION of frozen evidence was done
  pre-prereg to validate the toolchain; no attack fixture existed
  then and none was executed.)
- Only `docs/lab/research-lead/overnight-20260928/causalv4_adversary/`
  paths will be staged/committed. Concurrent workers' files
  untouched. No broad git add. Binaries in /tmp only, never
  committed. No em dashes in loop documentation.
- Every attack run 3/3; byte-identical required for evidence.
