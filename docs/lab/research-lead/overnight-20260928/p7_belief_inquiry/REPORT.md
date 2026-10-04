# REPORT: P7-BELIEF-INQUIRY (competing hypotheses, dependent evidence, one distinguishing experiment)

Worker: P7-BELIEF-INQUIRY, 2026-10-03. Non-ledger lane.
Lane: `docs/lab/research-lead/overnight-20260928/p7_belief_inquiry/`
Verdict: **P7B-PASS with one frozen bar FAILED (41/42)**.
Determinism: K-DET **3/3 byte-identical**,
sha256 `36556c87a8840efa8c142ffe4b00b6ee2f217bd631a7e8eec17fd399e446f1be`.
Output 1637 bytes, non-empty (K-NONEMPTY).
Runtime 0.06 s.
Method: prereg frozen and committed alone (`cf215aba5`), pre-execution
amendment committed alone (`fca56cee8`), implementation and post-run
amendment in this commit. No bar was added, removed, or moved after a
run except the one 1-unit numeric relaxation disclosed in AMENDMENT A2
section A2.3.

## 0. The one thing to read first

**There is no inquiry mode.** The whole epistemic layer contains exactly
one decision rule, `p7b_val`. It builds a candidate set out of what the
frozen store structurally offers, scores every candidate with the same
utility, and takes the strict argmax:

| candidate | present when | source of the candidate |
|---|---|---|
| `COMMIT(h)` | the **frozen** `bp2_select` returns a belief node | frozen R7; it returns `-3` on an exact tie or below bar, so the frozen layer decides whether commitment is available at all |
| `RUN(p)` | probe `p` is a live tag-1 node on Q with `field24` in `[900,990)` and no live tag-20 belief licenses it | structural scan, enumerated, never listed |
| `SAFE` | steps remain | always |
| `WITHHOLD` | always | always |

`RUN` is not privileged: it competes on utility like the other three and
wins only when its computed value is highest. The uncertainty that gates
commitment is the frozen layer's own numeric `-3`, not a flag written by
this lane. Grep attestation (K-SI): `grep -c -E '(if|while)\(.*(uncert|
inquire|mode|need_info|do_ask)' p7b_learner.zag p7b_driver.zag` returns
**0 and 0**.

## 1. What was built

- `p7b_learner.zag` (1011 lines). Section 0 is the `bp2_*` belief layer
  copied from `belief_provenance_9/bp9_learner.zag`; the non-comment
  lines are **byte-identical** (`diff` clean, sha256
  `68c0513ab4e56b9f25fbfc5035a76bd9512b1ed00500d32c0a0c910ba432abc8` on
  both). Zero edits to R1-R7, `eff`, `bp2_retire`, `bp2_relicense`,
  `bp2_bar_after`. Section 1 is new: an append-only provenance ledger,
  Beta(1,1) source reliability, a learned probe-channel contingency, a
  derived mass vector, and `p7b_val`.
- `p7b_driver.zag` (753 lines). Ten arms, 42 in-driver bars, worlds,
  baselines, ablations. Harness-side only.
- `p7b_full.zag` = `xf_block.zag` (frozen, sha256
  `172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a`,
  unchanged) + the two lane files.

**New store vocabulary: none.** 0 new edge types (provenance rides on the
pre-existing `ET_SUP` type-2 edge with the dependency fraction in
`field12`; the REVISION record is a novel `field12` VALUE on the
pre-existing kind-3 self-edge `bp2_retire` already writes). 0 new node
types (tags 1, 3, 20 pre-exist). 0 modes, 0 bridges, 0 handlers.
**0 `_zag_raw_syscall`** anywhere in the lane; output is `_zag_print` /
`_zag_println` only.

## 2. Per-case results (charter 26)

Hidden ground truth for world M is **H1**; the misleading evidence is the
copied chain supporting H0. Scoring is against the evidence available at
each moment.

| # | case | result |
|---|---|---|
| 1 | only evidence supports H1 | `P=(208,23,23)`, frozen `bp2_select` returns the H0 MAP belief (not `-3`), derived status `KNOWN`, reported share 208/255. **Not penalised for the hidden truth being H1.** K-B10/11/12 PASS |
| 2 | contradictory credible evidence | world M: `P=(115,115,23)`, frozen `select==-3`, **zero** kind-3 edges on any belief, all 3 hypothesis facts live, all 6 ledger records live, derived status `CONTESTED`. Not a silent overwrite. K-B22 PASS |
| 3 | strong independent evidence for H2 | 2 roots H1 (tie, `select==-3`, **no** revision edge, K-B23A) then a 3rd root H1: `select` returns the H1 belief, `b_rev` incremented, REVISION reason edge present, `bp2_has_k3(m_H0)==0` at that moment. K-B23B PASS |
| 4 | evidence swings back | +2 roots H0: `P=(139,106,8)`, argmax back to H0, **second** REVISION edge, both beliefs live, no retirement edge on either, all 7 records survive. K-B24B PASS. **K-B24 (frozen, `live==8`) FAILS: the prereg miscounted the world's claims as 8 when it has 7** (A2.1) |
| 5 | three sources repeating one copied claim | copied sweep `n=1..5`: `P[H0] = 115,115,115,115,115` (max-min **0**). Independent sweep: `115,152,174,188,198` (rise **83**). Ablation `ABL_PLAIN` on the copied sweep: `120,160,182,195,204` (rise **84**) and it crosses the commit threshold at `n>=2` (`select` returns the H0 belief) while the honest learner never commits: **decision flip = 1**. K-B14/15/16 PASS |
| 6 | reliable source starts lying | reliability `127 -> 212 -> 106`, strictly falling when it starts lying; mass `218 -> 145`. K-B17/18 PASS |
| 7 | unreliable source improves | `106 -> 174` after 8 correct resolutions; mass `145 -> 193`. Rehabilitation is reachable by the same symmetric update. K-B17/18 PASS |
| 8 | direct observation vs testimony | arm a (self `rel=204`, witness `rel=127`): `P=(185,69)`, argmax **observation**. Arm b (self `rel=51`, witness `rel=229`): `P=(64,190)`, argmax **testimony**. The verdict **flips**. K-B20/21 PASS |
| 9 | causal experiment resolves | learner action `RUN(channel 0)`; outcome becomes a direct-observation claim through the **same** append path; `P=(85,152,17)`, `select` returns the H1 belief, action `COMMIT(H1)`, realised **+100**, ledger 6 -> 7 with no record touched. K-B07/09/26 PASS |

## 3. Did it discount copied evidence?

**Yes, and the ablation puts the number back.** A copied claim has
`residual = residual(parent)*(255-dep)/255 = 0`, so it carries **zero**
mass and applies **no frozen rule at all** (R2/R3 are gated on
`residual > 0`). One root report read by three sources leaves `P[H0]`
exactly where one report leaves it (115). With `ABL_PLAIN` the same
evidence yields 164 and rising with the copy count. On the main world the
honest learner sits at 115/255 (a genuine tie, frozen `select` refuses)
while the ablation sits at 164/255 and would have crossed the commit
threshold. Independently, charter 133 holds exactly: a chain
`A -> B -> C -> D` of inferences leaves `P` unchanged (181,181) with
`mass(inference) = 0`, and all four records remain live. Charter 131
holds too: masses `127 : 63 : 127` for root / half-dependent /
independent, and two half-dependent siblings total 253 where full
independence would give 381.

## 4. Did it choose the information-gaining action over random?

**Yes.** Information gained is the drop in the learner's own Gini
impurity (0 at a point mass, maximal at uniform), integers only.

| policy | info gained | realised payoff |
|---|---|---|
| **learner** (`argmax U`) | **15** | **+100** |
| random inquiry (mean of 30 seeds) | 3 | -30 |
| passive waiting | 0 | -30 |
| fixed researcher query | 15 | +100 |
| stupid baseline, "believe whoever spoke last" (charter 79) | 0 | **-100** |

The learner strictly beats random on both metrics (K-B35). It matches
the fixed query **on this world only because the researcher-chosen probe
happens to be the informative one**: in the probe-order-swapped twin
store, `p7b_sel_fixed` returns channel 1 (the flat proxy) while
`p7b_sel_learn` still returns channel 0, i.e. the learner is not the
fixed-query policy (K-B06). Random picks the separating channel 9/30
times (K-B05).

## 5. Ablation evidence

Three switches, one predicate each:
- `ABL_NODEP` — `residual := 255` regardless of the provenance edges.
- `ABL_NOREL` — `rel := 128` for every source.
- `ABL_PLAIN` — both, plus `rel := 255`: every claim is one independent
  unit vote.

Measured: `ABL_PLAIN` on world M gives `P=(164,85,5)` against the honest
`(115,115,23)`, and the frozen layer then returns the H0 MAP belief
instead of `-3` (K-B13). `ABL_NOREL` freezes reliability at 128 and the
reliability curve, and the claim masses, go flat (K-B19). Disabling
`ABL_NODEP` on world M is a no-op (K-B-ABLREL), which is itself the
point: on that world every source has no track record, so only the
dependency switch can move the number.

## 6. Derived epistemic status (charter 46/74) and rational ignorance (129)

Six statuses, all computed from (mass record, probe availability,
consequence scalars); nothing stored, nothing labelled:

| world | status | why |
|---|---|---|
| C1, one-sided strong evidence | `KNOWN` | share 208 >= 127 (the share at which committing pays, `C_WRONG*255/(C_RIGHT+C_WRONG)`), no evidence against |
| world M | `CONTESTED` | share 115 < 127, evidence on both sides, and a probe exists that can clear the threshold (`maxgain = 225`) |
| C8a | `CONTRADICTED` | share >= 127 but evidence against |
| world M with only the flat proxy probe | `REP-INS` | contested, but `maxgain = 115 < 127`: **no available measurement can separate them** |
| world M with `C_PROBE = 20000` | `WITHHELD` | a path exists (`maxgain = 225`) but its cost exceeds its value; action is `WITHHOLD`, `COMMIT` is **never** chosen, and **this is not scored as failure** |

Calibration is not a label: re-scoring world M under
`(C_RIGHT=200, C_WRONG=50)` moves the threshold from 127 to 51 and the
derived status from `CONTESTED` to `CONTRADICTED` (K-B31). The six
NAMES and their priority order are researcher-authored and disclosed as
such; the ASSIGNMENT is derived.

## 7. Honest accounting

New learner functions this lane: 40 (`p7b_*` in section 1). Zero changes
to any `bp2_*` function. Zero changes to the frozen block. All compute is
Pure Zag under the restricted PATH (`tnn_pure_zag_report` ->
`PURE-ZAG-CLEAN`; `which python3`/`python` resolve only to the fail-shims
in `.env/shims`, never to a real interpreter); shell and git were used
only for the worktree, the concatenation and the pinned `znc` build.

The provenance ledger, the source reliability record and the
probe-channel contingency are **new structures that do not exist in the
frozen store**. They are the main design decision of this lane and they
are counted, not hidden. The ledger and the contingency are learner-side
tables; the provenance graph itself lives in the frozen store as type-2
edges, so an auditor can walk it there.

## 8. What is claimed and what is not

Minted nothing (non-ledger lane). Candidate claims, C5xx block, only if
the bars support them:

- **C500** competing hypotheses are retained simultaneously with no
  overwrite and no deletion; the frozen `-3` refusal is the mechanism.
  Supported: K-B22, K-B23A/B, K-B24B, K-B09.
- **C501** three reports of one copied claim are counted as one
  observation; the ablation restores the double count and the decision
  flip. Supported: K-B14/15/16, `C5 flip 1`, K-B13.
- **C502** self-generated inference is not corroboration for itself.
  Supported: K-B28, K-B27.
- **C503** a measurement channel's usefulness is learned from history, not
  declared; the learner beats random and is not the fixed-query policy.
  Supported: K-CAL-*, K-B04/05/06/32/33/35. **Falsified:** FP-M9.
- **C504** source reliability adapts downward and upward under one
  symmetric update. Supported: K-B17/18/19.
- **C505** observation-over-testimony arbitration is reversible, so it is
  not hardcoded. Supported: K-B20/21.
- **C506** epistemic status is a derived function of evidence and
  consequence scalars, including rational ignorance and
  representation-insufficient. Supported: K-B29/30/31, K-B03, K-B11.

**Not claimed:** L3, open-form strategy invention, cross-question
transfer of calibration (the contingency is trained in the same session
on three questions with revealed truth), or anything about the contested
C377-C466 block.

## 9. Boundaries

- One constructed fixture, one question shape, 3 hypotheses, 2 probe
  channels, at most 96 claims per scenario. The option value is depth-2,
  so the probe-vs-commit margin depends on the horizon; both are disclosed
  parameters, not findings.
- The world supplies the payoff scalars as a description of consequences.
  A learner handed different consequences behaves differently **by
  construction**; that the behaviour tracks the scalars is measured
  (K-B31), but that the scalars are right is not tested.
- `C_PROBE = 20000` in the ignorance arm is far outside any plausible
  regime. It establishes that withholding is reachable and that
  `COMMIT` is then never chosen; it is not evidence about realistic costs.
- The claim ledger is append-only and bounded at 96 records per scenario.
- Scenario resets are harness code. The bug in AMENDMENT A2 section A2.4
  item 4 (stale provenance edges surviving a reset) is a **harness** bug,
  not a property of the belief layer, but it is the one most likely to be
  repeated by anyone reusing this pattern.

## 10. Next experiment

Three things, in priority order.

1. **Make the channel diagnosticity itself the unknown.** Here channel 0
   is calibrated in the same session on questions whose truth is revealed.
   The next lane should hand the learner a probe channel it has never run
   and ask whether it can learn that the channel is worthless from a
   handful of uninformative outcomes, or whether it commits on the
   `+1` smoothing prior. That is the difference between "learned
   calibration" and "a prior that happens to be right".
2. **Transplant the `residual := 0` gate onto the frozen belief layer's
   own counters.** BP-9 measured that `bp2_confirm` saturates at one R2
   per absorb but does nothing about dependence. The structural question
   is whether `b_conf` can be made a function of *independent* evidence
   rather than edge counts, without adding machinery to BP.
3. **Break the horizon.** With depth 2 and `HZN=2` the option value is
   computed almost exactly, so the learner's probe choice may be an
   artefact of a convenient horizon. Sweep `HZN` in {1,2,3,4} and depth in
   {1,2,3} and report the action identity at each point; if the choice
   flips, the "chooses the separating experiment" result is
   horizon-dependent and must be restated.