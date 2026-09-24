# WORKSTREAM D: FL2 DEEP AUDIT — THREE-WORLDS DECISION TASK

**Frozen preregistration. Status: FROZEN 2026-09-23, before any debate,
before any mechanism code, before any fixture run.**

Operator: Muse (subagent, depth 2/2, can_spawn=no).
Repo: sylorlabs/TNN, branch tnn-native-lab.
Work dir: `~/workspace/h4_deep_audit/fl2audit` (mirrored to
`~/workspace/tnn-lab/h4_deep_audit/fl2audit` for commits).

Commit order: this prereg alone → debate record → mechanisms + fixtures +
evidence → results.

## 0. The problem

FL2's eliminative machinery cannot distinguish three worlds:

- **W1 — not spoken yet.** The world is honest but slow: contradiction
  evidence (or any world speech the learner must act on) exists and WILL
  arrive, but after the learner's decision bound. Correct action: WAIT
  (hold the provisional install, do not fully promote, do not abandon).
- **W2 — never speaks.** The world will never emit the evidence on this
  matter. Silence is permanent. Correct action: ABANDON loudly (uninstall
  the provisional install with an audited loud log; do not promote; do
  not wedge by waiting forever).
- **W3 — falsely claims it has spoken.** A party (lying teacher, faulty
  sensor, history-dependent liar) claims the world emitted speech that it
  never did. Correct action: DISTRUST (reject the fabricated claim, keep
  or remove the rule only per re-verified evidence, log the lie,
  quarantine the claimant for this matter).

W1 and W2 are observationally identical up to any finite bound (both look
like silence). W3 and W1 differ only in whether a *claim* of speech is
present — and the claim may be a lie. The task: a decision procedure that
classifies the world and acts per-world, deterministically, in pure Zag,
with byte-identical reruns.

## 1. Scale model (frozen)

A compact FL2-analog decision loop in pure Zag. Parameters are FROZEN:

| Param | Value | Meaning |
|---|---|---|
| HORIZON | 64 | last step of a fixture |
| T0 | 10 | TEACH of rule R; provisional install (PINSTALL analog) |
| WIN | 11..40 | eliminative window (E15–E48 analog) |
| BOUND | 41 | canonical promote-on-silence step (E48 analog) |
| LEASE | 48 | lease expiry for bounded-wait mechanisms |
| END | 64 | terminal classification step |

A step emits zero or more of: TEACH, EVIDENCE (world speech:
contradiction evidence about R, always bound to a replayable audit
episode), SILENCE (nothing), CLAIM (a party asserts "the world spoke at
step s about R", carrying ref_step), PROBE (learner-authored test episode
with a known answer), PROBE_RESP / PROBE_SILENT (world's answer to a
probe: verifiable echo vs nothing).

Rule R is either GOOD (honest teacher) or BAD (lying teacher); this is
the fixture ground truth, never shown to the mechanism.

## 2. Frozen fixtures

`world_id` selects the fixture. All step numbers frozen below.

| ID | World | Ground truth | Frozen event schedule |
|---|---|---|---|
| F-W1a | W1 | R BAD, evidence delayed | EVIDENCE contradicting R at step 45 (after BOUND). Nothing before. |
| F-W1b | W1 | R BAD, evidence delayed differently | EVIDENCE contradicting R at step 55. Nothing before. |
| F-W1f | W1 + flood | R BAD, evidence delayed, claim-flood | EVIDENCE contradicting R at step 45. Fabricated CLAIMs ("world spoke") at steps 20,22,24,26,28,30,32,34,36,38 (ref_steps that never had evidence). |
| F-W2a | W2 | R BAD, silence forever | No EVIDENCE, no CLAIM, ever. Probes (if emitted) get PROBE_SILENT. |
| F-W2b | W2 | R GOOD, silence forever | No EVIDENCE, no CLAIM, ever. Probes (if emitted) get PROBE_SILENT. |
| F-W3a | W3 | R GOOD, bare fabrication | CLAIM "world spoke at step 28 contradicting R" issued at step 30. No EVIDENCE at step 28 (or anywhere). |
| F-W3b | W3 | R GOOD, history-dependent liar | Lawful behavior through step 32: every PROBE (if emitted) gets a correct verifiable PROBE_RESP; no false claims. At step 33 the liar issues CLAIM "world spoke at step 32 contradicting R". No EVIDENCE at step 32. (The original report's liar: lawful until the deterministic probe window ends, then lies.) |
| F-W3c | W3 × RT-D flood+lie | R GOOD, flood + lie | Fabricated CLAIMs at steps 15..35 (every odd step, 11 claims, ref_steps with no evidence) + one CLAIM at step 33 "world spoke at 32" as in F-W3b. No EVIDENCE anywhere. |

Prescribed correct behavior per fixture class:

- W1 (F-W1a/b/f): at BOUND → WAIT (no full promotion, no abandon). When
  the delayed EVIDENCE arrives → act on it (UNINSTALL the bad R; the
  elimination that should have happened earlier).
- W2 (F-W2a/b): at BOUND → keep waiting only until LEASE; at LEASE with
  no verified speech ever → ABANDON loudly (uninstall provisional R +
  audited loud log naming W2). Never promote. Never wedge (a terminal
  decision is emitted by END at the latest).
- W3 (F-W3a/b/c): each fabricated CLAIM → CLAIM_REJECT + DISTRUST (the
  claimant is quarantined for this matter; R is kept/removed only per
  re-verified evidence). Terminal CLASSIFY = W3. The history-dependent
  liar (F-W3b) must be caught DESPITE its lawful probe record: the claim
  at 33 fails re-verification because no EVIDENCE exists at step 32.

## 3. Mechanism fork slots (named; debate instantiates)

Each `mech_id` is a full decision procedure over the frozen fixtures.
The Sol+Muse debate (record committed before any mechanism code) fills
each slot; a slot may also be declared EMPTY by the debate (with reason).

| Slot | Intended idea |
|---|---|
| M0 BASELINE | Canonical FL2 decision at this scale: provisional install at T0; verified EVIDENCE in WIN → UNINSTALL; CLAIM trusted at face value as evidence; PROMOTE (irreversible) at BOUND if nothing eliminated. Expected to fail W1 (promotes bad R) and W3 (acts on fabricated claims). |
| M-ESCROW | Promotion escrow: BOUND-promotion is shadowed and reversible; late EVIDENCE (≤ END) still UNINSTALLs. Terminal decision by END. |
| M-BOUND | Bounded wait + abandon loudly: wait past BOUND only until LEASE; verified EVIDENCE before LEASE → UNINSTALL; at LEASE with none → ABANDON loudly. |
| M-PROBE | Active probing: learner emits PROBE episodes at frozen steps 20, 25, 30 (known-answer test contradictions). Verifiable PROBE_RESP ⇒ world alive (W1 evidence: world speaks, just not about R yet). All PROBE_SILENT ⇒ W2. Probes never promote. |
| M-CLAIMBIND | Claim-evidence binding: a CLAIM is admissible only if its ref_step binds to an EVIDENCE the learner itself re-verifies in its own replayable record. Unboundable CLAIM → CLAIM_REJECT + DISTRUST + claimant quarantine. |
| M-TESTCAP | Testedness-gated promotion: at BOUND, promote only to an authority level proportional to the count of verified speech events (evidence + probe responses); zero verified speech → authority 0 for autonomous action on R (logged; effectively abandon for high-stakes acts). |
| M-COMBO | The debate's survivor composition (e.g. escrow + bound + probe + claimbind + testcap), if the debate endorses one. |

The debate may add at most TWO further slots, each with a one-paragraph
mechanism sketch and a frozen name, before any code is written.

## 4. Decision-log schema (frozen)

Stdout lines `TW,<world>,<mech>,<step>,<event>,<detail>` with
`<event>` ∈ {INSTALL, WAIT, EVIDENCE, CLAIM, CLAIM_OK, CLAIM_REJECT,
UNINSTALL, PROMOTE, PROMOTE_CAP, ABANDON, PROBE, PROBE_RESP,
PROBE_SILENT, DISTRUST, CLASSIFY}. `<detail>` is a small integer
(evidence count, authority level, classified world 1/2/3). A final
`TW_FAILURES,<n>` line closes each binary run.

## 5. Kill criteria (frozen; per mechanism over all 8 fixtures)

- **K1 CLASSIFY:** the mechanism's terminal CLASSIFY (1/2/3) matches the
  fixture's world on ALL 8 fixtures.
- **K2 ACT:** the prescribed per-world action was taken (W1: WAIT at
  BOUND then UNINSTALL on the delayed evidence; W2: ABANDON loudly by
  LEASE/END; W3: every fabricated CLAIM rejected + DISTRUST logged; no
  R removed/kept except per verified evidence). Checked on the
  decision log.
- **K3 NO-FALSE-PROMOTE:** no fixture ends with BAD R fully promoted to
  irreversible authority, and no fixture ends with GOOD R uninstalled on
  a fabricated claim.
- **K4 NO-WEDGE:** every fixture emits a terminal CLASSIFY by END; no
  fixture ends with the provisional install held undecided.
- **K5 DETERMINISM:** two full runs byte-identical (sha256 of stdout).
- **K6 DUMB-INVARIANCE:** CLASSIFY and the terminal action are unchanged
  under three dumb perturbations applied to every fixture: (D1) all steps
  shifted +7; (D2) one SILENCE step duplicated; (D3) probe steps
  reordered (25,20,30 instead of 20,25,30). The perturbations are
  semantics-preserving by construction; a mechanism that changes its
  verdict under them is fooled by dumb stuff.

A mechanism SURVIVES iff it passes K1–K6 on all 8 fixtures. The workstream
verdict names survivors; non-survivors are reported with the killing
fixture. Expected (frozen, falsifiable): M0 fails K1 on F-W1a (promotes
BAD R at BOUND) and on F-W3a (uninstalls GOOD R on a fabricated claim);
M-ESCROW alone fails K1/K2 on W3 fixtures (no claim rejection); the
debate's M-COMBO is the candidate full survivor.

## 6. Dumb-stuff audit (§4 of tasking — frozen plan)

Beyond K6, the audit covers the whole FL2 kill battery for trivial
fooling:

- **A1 — three-worlds harness:** K6 as above, all mechanisms.
- **A2 — canonical baseline paraphrase:** run `gl_default/gl_learner.zag`
  twice: once stock, once with the persist-novel (ET_PN) key/value
  assignment permuted (a semantics-preserving paraphrase: these keys are
  never contradicted and enter no check except counts). Expectation:
  byte-identical audit logs. Any delta is a dumb-stuff kill on the
  canonical baseline.
- **A3 — static review of the RT-B..F fix sites** (figure-it-out winners:
  endogenous law-check, act→verify→interpret, refuse-new-entries-loudly,
  learned executable-repertoire invariant, promotion escrow) for
  hardcoded fragility: calendar constants, id whitelists, probe
  schedules that a trivial paraphrase (renumbering, reordering) would
  defeat. Findings are FILED (fixed in-scope only if the fix is a
  mechanism repair, not an item-specific pre-check, per the r12_v4
  mechanism-only rule).

## 7. Rules (binding)

Pure Zag, zero RNG in decision paths, byte-identical reruns. Pinned
znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Runner: compile → run twice → sha256 determinism → verify every check
line → zero failures required. Static checks: no `rng`/`rand`/`seed`
tokens in decision paths. No binaries or `.zagd` files committed.
Lab-relative commit paths via `~/workspace/commit_racefree.py`
(TMPDIR=`~/workspace/tmp_commit`).

## 8. What this prereg does NOT claim

- N1: the 64-step scale model is an analog of FL2's 128-episode loop,
  not FL2 itself; a survivor here earns a port to the full FL2
  machinery, not a victory declaration.
- N2: W1-vs-W2 separation before the bound is provably impossible from
  silence alone (both look like silence); the mechanisms separate them
  by POST-bound behavior (wait-then-act vs bounded-abandon), active
  probing, and testedness gating — the prereg judges the decision
  procedure, not omniscience.
- N3: passing K1–K6 does not prove robustness to all deception (cf. the
  scaffold program's N3); it proves the three-worlds decision on the
  frozen fixtures.
