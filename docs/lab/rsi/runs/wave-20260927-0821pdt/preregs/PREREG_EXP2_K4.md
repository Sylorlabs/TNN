# PREREG EXP2-K4: One-Brain Grounded in Real Deliberation Failures, Rescuer-Lens K4 Hardening (DRAFT FOR FREEZE)

Wave: wave-20260927-0821pdt, lane 3 (prereg design).
Status: DRAFT. This document is not frozen. It becomes frozen only when a
future wave adopts it as its prereg freeze commit. Until then, numbers may
change by redraft only, never by post-freeze edit.
Freeze commit: PENDING (to be recorded at freeze time).
Prereg design commit (lane 3, this wave): PENDING.

## 1. Provenance header (machine-checkable)

COMPONENT_LINEAGE:
- EXP2 one-brain dispatch, wave-20260926-2321pdt: fresh 10-problem frozen
  holdout, one-brain 10/10 vs single-deliberation baseline 0/10 vs
  shared-writes-off ablation 0/10, K1-K6 PASS with a K4 caveat (on 2/3
  mechanism-test problems the attack-lens branch independently reached the
  shared verdict).
- EXP2 follow-up, wave-20260927-0221pdt: adopted as a fidelity self-check
  record, NARROWED. The judge's ruling, entered here verbatim in
  substance: S2/S3 are construction-guaranteed mechanism probes authored
  from the frozen mechanism spec; the 8/8 prereg prediction record is
  fidelity evidence, ecological validity untested; the K4-hardened bar
  could not fail by construction and is recorded as a consistency check,
  not hardening; on S3 the rescuer lens b2 alone reaches the shared
  verdict 10/10 (an uncontrolled rival the K1 conjunct does not cover);
  the ablation differs in reconciliation cadence and evidence coverage,
  not just shared writes; the regression sweep exercises the fork path
  only via trap. Forward requirements frozen by that ruling: (a) harden
  K4 against the rescuer lens (b2) next wave; (b) require a
  shared-writes-off control with joint timing before any causal claim
  about the shared channel is adopted. Wire-in stays off the table.

NEW_KNOWLEDGE_CLAIM: none yet. This prereg designs the experiment that
could first test whether the shared channel causes better deliberation
verdicts on failures the mechanism was not authored to fix.

Inherited: the one-brain/ablation/baseline machinery from the 0221pdt
exp2 branch (byte-verified before use), the deliberation-v1 ledger
layout, the poison/scaffold/determinism instruments, and the pinned
toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1 (SHA-256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
New this design: real-failure-trace sourcing with a spec-blind curator,
the KH1-KH4 bar family, and the joint-timing matched ablation.

## 2. Question

Does the shared channel cause correct deliberation verdicts on real
deliberation failures (traces the frozen machinery actually got wrong),
with the rescuer-lens rival excluded and the ablation matched?

## 3. Mechanism (frozen design)

F1. Failure-trace corpus (grounding). The holdout is 12 real deliberation
failure traces: recorded deliberation-v1 ledger traces, committed before
this prereg freezes, in which the frozen single-deliberation machinery
produced a wrong final verdict or a wrongful decline. The corpus is pinned
by SHA-256 at freeze time and must predate the freeze commit. The
selection rule is frozen: the first 12 traces by commit order satisfying
the qualifying rule (wrong verdict or wrongful decline with a recorded
expected outcome), no cherry-picking, no reordering.

F2. Spec-blind curator. The corpus is curated by a worker who has never
read the one-brain mechanism spec or implementation. The curator receives
only the trace files and the qualifying rule. Curator identity and the
blindness attestation are committed in the seal attestation. This is what
breaks the 0221pdt confound: the items cannot be authored from the spec
because the curator has not seen the spec.

F3. The candidate is the unchanged 0221pdt one-brain machinery (byte
verified). No mechanism change is authorized by this prereg; the design
change is entirely in the test: real traces, real rivals, matched
control.

F4. Joint-timing matched ablation. The shared-writes-off control differs
from the candidate in exactly one respect: shared writes are dropped
(and shared reads return empty). Reconciliation cadence, evidence
coverage, driver, fork schedule, and the joint timing schedule are
byte-identical, frozen in the prereg appendix. The 0221pdt ablation's
impurity (cadence and coverage differences) is thereby closed.

F5. Attack lenses. b1 (attacker lens) and b2 (rescuer lens) run as
single-branch deliberations on each trace, per the 0221pdt lens
definitions, frozen.

## 4. Metric it moves

Deliberation verdict accuracy on real failure traces: the fraction of the
12 traces on which one-brain reaches the recorded expected verdict.
Current verified number on real traces: unmeasured (the 10/10 and S2/S3
numbers are on synthetic probes; this prereg does not cite them as
baselines because the bar set is absolute).

## 5. Cost budget

12 traces x 5 modes (one-brain, single-deliberation baseline,
shared-writes-off ablation, b1 lens, b2 lens) x 3 determinism runs = 180
scored runs, op-counted under the frozen F6-equivalent discipline.
Exceeding a frozen 10x per-trace op budget vs the baseline is DEAD.

## 6. Kill bars (frozen; never moved after the seal)

KH1 (grounding): one-brain reaches the recorded expected verdict on at
least 9 of the 12 real-failure traces. Fewer than 9 means DEAD.
KH2 (rescuer-lens rival exclusion): on every trace where one-brain is
correct, the b2 rescuer lens alone is incorrect. Any trace where b2
alone is correct while one-brain is also correct means DEAD (the shared
channel is not shown necessary; the rival explains the outcome).
KH3 (attacker-lens exclusion): on every trace where one-brain is correct,
the b1 attacker lens alone is incorrect. Any b1-alone correct trace
means DEAD.
KH4 (shared-writes-off causal control): the joint-timing matched ablation
is incorrect on every trace where one-brain is correct. Any trace where
the ablation matches one-brain's correct verdict means DEAD (the causal
claim about the shared channel fails).
K2 (poison causality, carried): poison test causal on the traces where
one-brain is correct, with private-ledger control clean. Any failure
means DEAD.
K3 (scaffold removal, carried): with the scaffold removed, verdicts
match on all traces, with zero fan_out calls in the driver. Any mismatch
means DEAD.
K5 (determinism): 3/3 full runs byte-identical (transcripts plus
op-count streams). Zero RNG in any decision path (static grep check).
Any nondeterminism means the run does not count; a second
nondeterministic run means DEAD.
K6 (no RNG): static audit, zero RNG tokens in decision paths.

Anti-guarantee (frozen, and this is what makes K4 a bar rather than a
consistency check): the item set is NOT constrained to traces where the
lenses fail. If b2 alone is correct on all 12, KH2 kills honestly. If
one-brain is correct on fewer than 9, KH1 kills honestly. Nothing in the
design guarantees passage.

Verdict mapping (frozen): all bars PASS means the EXP2 evidence is
upgraded from fidelity self-check to grounded causal evidence for the
shared channel on real failures, still experimental record only.
Wire-in stays off the table regardless (per the 0221pdt ruling). Any bar
FAIL means DEAD with killing evidence. No causal claim about the shared
channel is adopted without KH4 passing.

## 7. Red-team confound list (considered before this draft freezes)

1. Knowledge vs architecture (spec-authoring confound): cured by F1/F2.
The curator is spec-blind; the traces predate the freeze; the selection
rule is frozen and mechanical. The red team verifies curator blindness
from the attestation and the corpus predating from commit dates.
2. The b2 rival (the 0221pdt finding): KH2 excludes it per item. b2 is
not constrained by design to fail; its failure must be measured.
3. Ablation impurity (the 0221pdt finding): F4 freezes joint timing; the
red team diffs the ablation driver against the candidate driver and
requires the diff to touch only the shared-write path.
4. Regression-sweep inertia (the 0221pdt finding): this prereg does not
claim efficacy from no-breakage sweeps; the sweep is evidence only
against catastrophic breakage and is reported as such.
5. Trace leakage: static grep confirms no trace bytes in the candidate
sources, KB, build scripts, or scorer; the candidate never reads the
expected-outcome file. Curator and implementer are different workers.
6. Poison generality: K2 must pass on the traces where one-brain is
correct, not on a cherry-picked subset.
7. Pure Zag: all implementation, runs, and analysis in Zag; shell only
to invoke the compiler, redirect stdout, and hash outputs. No analysis
of any kind may run before the prereg freeze commit (the 0221pdt
pure-Zag lesson: pre-prereg analysis by the worker is a compliance
failure even when the bytes are clean). Any Python contact with a wave
artifact voids the evidence.

## 8. Standing rules applied

Pure Zag literally (no Python anywhere; any contact voids the evidence).
Frozen kill bars are never moved after the freeze. Missing evidence means
CANNOT-CONFIRM. The prereg freeze commit strictly precedes any
implementation or scoring commit (commit-order self-check). No em-dashes
in this document. The six governance rulings are untouched. The sealed
blind judge queue is untouched. Micah's frontier files are untouched.
Nothing is pushed to GitHub; commits stay local on tnn-native-lab.

## 9. Gate conditions (what this draft waits on)

This is a draft for a future wave's queue. Before freezing, the wave
must confirm the failure-trace corpus exists and predates the freeze
(the specific corpus path and SHA are pinned at freeze time). Wire-in
stays off the table: this prereg authorizes evidence only, never
integration.
