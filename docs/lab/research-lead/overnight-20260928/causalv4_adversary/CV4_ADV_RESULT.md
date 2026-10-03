# H-CAUSALV4 Independent Red Team: Result

**Date:** 2026-09-29 (PDT)
**Target:** H-CAUSALV4 SURVIVES (K-CV4-1/2/3 all PASS; R4
cause-context diversity; bounded L2)
**Verdict: H-CAUSALV4 DOWNGRADED (not killed).**
**Classification:** bounded L2, narrowed. Not L3.

## 1. Preregistration and governance

- `PREREG_CV4_ADV.md` frozen and committed alone as **512df2dc3**
  before any adversary fixture was run or any attack build existed.
  No amendments. Kill criteria quoted verbatim from the prereg
  below.
- All four attack fixtures hand-derived from the committed
  `causalv4.zag` source (read-only) before the prereg commit; the
  prereg's hand-derived expectations matched implementation output
  exactly on first execution, zero tuning.
- Pure Zag throughout. No Python at any stage (fixtures are
  hand-written text; builds, runs, greps, hashes, cmp via shell
  and znc 2026.07.0-dev (edition 2026) only).
- A build of the committed causalv4.zag for reproduction of frozen
  evidence was done pre-prereg to validate the toolchain; no
  attack fixture existed then and none was executed. Disclosed.
- Every attack run 3/3; all runs byte-identical (md5s below).
- Binaries built in /tmp/cv4adv and /tmp/cv4reg only, never
  committed. Only
  `docs/lab/research-lead/overnight-20260928/causalv4_adversary/`
  paths staged. Concurrent workers' files untouched. No broad git
  add. No em dashes in loop documentation.

## 2. X-CV4-1 (varied-cause-context confounder): SUCCEEDS -> DOWNGRADE

The frozen X-CV3-1 double-confounder construction, except the two
positioned action-1 confounder episodes occur in DIFFERENT states
(seq3 in (1,0,0), seq7 in (2,0,0)). Both flips remain genuine law
changes; both confounders remain correlationally clean under
delay_clean (verified by the trace: the rule is created and
supported, so both gates passed).

Raw (3/3 byte-identical, md5 d32d0c76230278c094ba81953f0cbbd8):

```
# PROVISIONAL-DELAY-RULE R0: cause a=1 d=1 -> s2 SET(2) support=1 (unconfirmed)
# delay-attributed var s2 of seq 4 to R0
# delay rule R0 CONFIRMED at seq 8 support=2 (provisional -> active)
# delay-attributed var s2 of seq 8 to R0
...
# DL R0 cause=1 d=1 var=s2 fx=SET(2) st=ACT support=2
=== PROBES ===
Q (0 0 1) | 1 -> (0 0 2)
```

Both preregistered kill criteria hold: `# delay rule R0
CONFIRMED at seq 8` with st=ACT, and the probe line `Q (0 0 1) |
1 -> (0 0 2)`. Truth: action 1 is a no-op in every episode of the
fixture (both a1 episodes are no-ops; the s2 flips are genuine
law changes under a0 at seq4 and a2 at seq8, coincidentally
preceded by a1). Truth is (0,0,1). The probe is corrupted exactly
as in X-CV3-1.

Why this is a downgrade and not a boundary confirmation: the
builder's verdict headline claims R4 "closes genuine-change
confounder confirmation." The builder disclosed the varied-context
adversary as a limitation, but the SURVIVES verdict headline was
left standing on the unqualified claim. This attack falsifies the
headline as stated: R4 closes only the identical-cause-context
subclass of genuine-change confounders. A disclosure does not
convert a successful falsification of the headline claim into a
non-finding; the verdict headline is what was under test
(prereg section "Verdict rule").

Why not killed: frozen K-CV4-1 (identical contexts stay
PROVISIONAL, probe uncorrupted) still holds; K-CV4-2 (all 9
regressions byte-identical) and K-CV4-3 (determinism) still hold.
The mechanism does exactly what was preregistered; the failure is
the scope of the guarantee, not the implementation.

Narrowed claim (replaces the headline): "R4 blocks confirmation
of confounders that repeat in an identical cause context. It does
not close the genuine-change confounder class: an adversary that
positions confounders in varying cause states defeats the
diversity check."

## 3. X-CV4-2 (support-timing honesty): HOLDS, no bug

Identical-then-diverse supports, 3/3 byte-identical
(md5 86653a700baa318497499257c16b26f8):

```
# PROVISIONAL-DELAY-RULE R0: cause a=1 d=1 -> s2 SET(2) support=1 (unconfirmed)
# delay rule R0 NOT CONFIRMED at seq 8: cause context identical to creation; remains PROVISIONAL
# delay rule R0 CONFIRMED at seq 12 support=3 (provisional -> active)
Q (0 0 1) | 1 -> (0 0 2)
```

Exactly the hand-derived expectation: withheld at seq 8
(identical context, support=2, stays PROVISIONAL), confirmed at
seq 12 (diverse context, support=3). None of the kill criteria
(a) early confirmation, (b) late misfire, (c) dishonest counts
fired. The per-support diversity check behaves correctly.
TIMING HOLDS. (The probe corrupts after the legitimate diverse
confirmation, consistent with the X-CV4-1 finding.)

## 4. X-CV4-3 (counter-evidence permanence): blast radius CONFIRMED

Ten action-1 no-op episodes appended after the X-CV4-1
confirmation (counter-evidence: a1 at seq-d never followed by
s2=2), then the harm probe re-run. 3/3 byte-identical
(md5 2c278f958f8a71aff262ff6f4ca8ef3d):

```
# delay rule R0 CONFIRMED at seq 8 support=2 (provisional -> active)
...
# DL R0 cause=1 d=1 var=s2 fx=SET(2) st=ACT support=2
=== PROBES ===
Q (0 0 1) | 1 -> (0 0 2)
```

R0 remains ACTIVE; the probe stays corrupted. The committed
source contains no rule-retraction machinery, and none appeared.
Per the prereg verdict rule, this is a severity note for the
downgrade, not an independent kill: once a spurious rule is
confirmed (by identical or varied contexts), the corruption is
permanent under the current design. No self-healing was observed
(attack did not fail).

## 5. X-CV4-4 (regression): HOLDS, 10/10

Fresh build of the committed `causalv4.zag` blob
(`git show HEAD:...causalv4.zag`, cmp-verified identical to the
worktree file, worktree clean): all 9 frozen K-CV3 fixtures plus
the K-CV4-1 fixture re-run 3/3, every run byte-identical to the
committed `CV4_*_RUN.txt`. 10/10 PASS, 0 FAIL. The committed
source matches the committed evidence; no silent changes, no
nondeterminism.

## 6. Causal interpretation

R4's diversity check is implemented exactly as preregistered and
works as specified on identical contexts. Its insufficiency is
design-level, not a bug: "the correlation must hold across
varying background contexts" is a necessary-but-not-sufficient
condition for causation, and a positioned adversary controls the
contexts. Two confounders in different states are no more
causally probative than two in the same state when both are
positioned. The repair raises the bar (the frozen X-CV3-1 replay
is genuinely closed: K-CV4-1 re-verified byte-identical in
X-CV4-4), but the class remains open. A principled fix would need
to go beyond correlational diversity (e.g. the deferred
contest-competition redesign, intervention, or per-action
adjudication), which the builder correctly identified as beyond
repair scope.

## 7. Boundaries and negative evidence

- The timing logic (X-CV4-2) is correct; no implementation bug
  was found in R4.
- The regression surface (X-CV4-4) is fully intact.
- X-CV3-3 (vacuous unanimity) was not re-probed; unchanged from
  CV3/CV4 disclosures.
- Bounded L2; nothing here bears on L3.

## 8. Commit lineage (branch tnn-native-lab, local only)

- 512df2dc3 PREREG H-CAUSALV4 red team (CV4-ADV) FROZEN
  (prereg; strict ancestor of the result commit)
- <this commit> CV4-ADV fixtures, raw evidence, result

## 9. Files

- Prereg: `causalv4_adversary/PREREG_CV4_ADV.md`
- Fixtures: `causalv4_adversary/cv4_adv_vary_obs.txt`,
  `cv4_adv_vary_probe.txt`, `cv4_adv_timing_obs.txt`,
  `cv4_adv_timing_probe.txt`, `cv4_adv_perm_obs.txt`,
  `cv4_adv_perm_probe.txt`
- Raw: `causalv4_adversary/CV4_ADV_RAW.txt`
- Result: `causalv4_adversary/CV4_ADV_RESULT.md`

Suggested follow-ups for the parent: (1) H-CAUSALV5 repair
hypothesis addressing varied-context confounders (contest
competition, per-action adjudication, or intervention) is the
natural next builder lane; (2) the paper's H-CAUSALV4 line must
read DOWNGRADED with the narrowed claim, superseding the
SURVIVES headline; (3) no push attempted per standing rules,
commits are local only.
