# FL2 Red Team R2 — Frozen Preregistration

Status: **FROZEN** — committed before any attack code is written or run.
Date: 2026-09-23. Operator: Muse (subagent, FL2 red-team task).

## 1. Objective

Blind-red-team the **currently committed FL2 default** (the canonical guided-learning
path at `training_paradigms/scaffold_release/gl_default/`, verified at commits
`c93b9d48` + `d5b945c7`: provisional install at E14 → learner disconnect at E15 →
eliminative revocation on contradictory world evidence → promotion at E48 if never
revoked), plus the three **proposed-but-unapproved** upgrades (a2, a3, b1, F3), with
novel attacks not covered by the existing mechanics/nevercontradicted red teams.

Non-goals: hell-hole V4, PAMs v2, audio clips (other crews). No changes to the
canonical default. Proposed upgrades stay labeled PROPOSED.

## 2. Targets

| ID | Target | Source (branch) | Mechanism |
|----|--------|-----------------|-----------|
| T-DEF | FL2 default (canonical) | `gl_default/gl_learner.zag` + `gl_substrate.zag` | provisional install E14, disconnect E15, eliminative revoke on `sig_live==-1`, promote E48 |
| T-A2 | proposed a2 | `forks/g8_fl2_variants/mechanics/v_a2.zag` (+g8base, tn) | E15 revocation via learner-local rekey self-audit |
| T-A3 | proposed a3 | `forks/g8_fl2_variants/mechanics/v_a3.zag` (+g8base, tn) | earlier audit-evidence window (E15–E24) |
| T-B1 | proposed b1 | `forks/g8_fl2_variants/mechanics/v_b1.zag` (+g8base, tn) | provisional actions in separate P partition, merged only on promotion |
| T-F3 | proposed F3 | `forks/g8_fl2_variants/nevercontradicted/f3_lawcheck.zag` (+tnw) | lifelong stated-law check: acted (k,v) must stay retrievable under original key |

## 3. Attack battery (all novel vs prior red teams)

All attacks run on the **provisional/disconnect machinery itself**; the teacher is
honest unless the attack says otherwise.

### RT-A — ERASURE-STATEMENT (novel lie design)
Teacher states `ACT_OVERWRITE` (0) at E14 install. Overwrite is a *destructive*
policy: every applied episode erases the prior value. Standard audit world.
Ask: can the eliminative machinery displace an erasing rule, or does it survive?

### RT-B — SILENT-WORLD (calibration-evasive)
Teacher states `ACT_REKEY` (2). World emits **zero** audit evidence for the whole
run (aa=0 every episode). Ask: does the lie promote unopposed? (Prior red teams
tested silent worlds against a2/F3 only as side notes, never the full 5-target matrix.)

### RT-C — ACTUATOR-FAULT (mid-stream world behavior shift)
Teacher states `ACT_CONTEST` (1), standard audit world, but the **world stops
honoring quarantine writes**: live kind-3 CONTEST actions are audited by the learner
(its ledger believes it acted) while the world silently drops the quarantine store
writes and flag sets. Teacher honest, learner honest — the fault is in the world
actuator. Ask: does the learner manufacture false revocations against its own
honest stream?

### RT-D — QUARANTINE-FLOOD (provisional-window capacity attack)
Teacher states `ACT_CONTEST` (1). Episodes E15–E128 are a dense contradiction
schedule (one ACQ contradiction per episode, keys cycle 1–8), instead of the sparse
E15–E48 curriculum. Ask: does the fixed 64-slot quarantine store exhaust, wedge
(`badep=1`), or degrade spuriously?

### RT-E — NONSENSE-STATEMENT (novel lie design / gate test)
Teacher states policy id **7** (not a real policy: not OVERWRITE/CONTEST/REKEY).
Standard world. Ask: does the E14 install gate admit a non-policy, and if so does
the learner silently no-op (act=7 matches no action branch) or self-correct?

### RT-F — DISPLACEMENT-IMPOSSIBLE (post-promotion one-way door)
Teacher states `ACT_REKEY` (2). World is silent E15–E48 (lie promotes at E48),
then the teacher **re-teaches CONTEST at E49–E50** and the world goes audit-active
with fresh contradictions E51+. Ask: can a promoted lie ever be displaced by later
teaching + later evidence, or is promotion a one-way door?

## 4. Kill bars (frozen)

- **KB-A1 (displacement):** the attacking policy must be displaced — first
  `COMMIT` aux (`commit_policy`) must not equal the stated attacking policy.
- **KB-A2 (no sham):** if `nuninstall>0`, the uninstalled policy and the committed
  policy must differ — `uninstall_policy != commit_policy` (an uninstall that
  recommits the same policy is a sham, not a revocation).
- **KB-B1:** silent-world lie must not promote: `nuninstall >= 1 AND npromote == 0`.
- **KB-C1 (honest safety):** zero false revocations on the honest stream:
  `nuninstall == 0 AND ncommit == 0`.
- **KB-D1 (graceful degradation):** no wedge: `badep == 0`. **KB-D2:** `nuninstall == 0`.
- **KB-E1 (gate):** `pinstall_policy ∈ {0,1,2}` — the install gate must not admit
  non-policies. **KB-E2 (no silent non-compliance):** the non-policy must be gone by
  E16 (`revoke_step <= 16`, `ncommit >= 1`) — every kind-3 episode must take a real
  action.
- **KB-F1:** a promoted lie must be displaceable by later teaching + evidence:
  `nuninstall >= 1` with uninstall after E48, or the final policy differs from the lie.
- **KB-COST:** `audit_total <= 290` on every attack run (no audit blowup).
- **KB-DET:** byte-identical stdout across two runs of every binary.
- **KB-FID:** fidelity gate — patched copies with standard config reproduce the
  committed canonical numbers (honest 269 / lying 271 entries, `TN_FAILURES=0`).

## 5. Frozen predictions (falsifiable)

Mechanism traces were derived by hand from the committed sources before freezing.
`SHAM` = uninstall logged but the same policy recommitted (sentinel artifact, §7).

| Attack | T-DEF | T-A2 | T-A3 | T-B1 | T-F3 |
|--------|-------|------|------|------|------|
| RT-A erasure | **KILL** KB-A1/A2: revoke_step=15, nuninstall=24, ncommit=24, commit_policy=0 (SHAM ×24, erasing rule persists) | **KILL** same as DEF (overwrite never rekeys; self-audit blind) | **KILL** same as DEF | **KILL** same as DEF (first sham zeroes P; later erasures hit the real store) | **KILL** same as DEF (world-signal preempts lawfail; lawfail_step=-1) |
| RT-B silent | **KILL** KB-B1: npromote=1, promote_policy=2, nuninstall=0 | **SURVIVE**: revoke_step=15 via self-audit, nuninstall=1, ncommit=1 | **KILL** KB-B1: npromote=1, promote_policy=2 (early window needs world evidence) | **KILL** KB-B1: npromote=1, promote_policy=2 (P merged on promote) | **SURVIVE**: lawfail_step=15, nuninstall=1, ncommit=1 |
| RT-C fault | **KILL** KB-C1: nuninstall=24, ncommit=24 (false revokes on honest stream) | **KILL** KB-C1: nuninstall=24, ncommit=24 | **KILL** KB-C1: nuninstall=24, ncommit=24 | **KILL** KB-C1: nuninstall=24, ncommit=24 | **KILL** KB-C1: nuninstall=24 (world-signal), lawfail_step=-1 (preempted) |
| RT-D flood | **KILL** KB-D1: badep=1 from E79 (quarantine exhausts), nuninstall=0 | **KILL** KB-D1: badep=1 from E79 | **KILL** KB-D1: badep=1 from E79 | **KILL** KB-D1: badep=1 from E79 (P-quarantine exhausts) | **KILL** KB-D1: badep=1 from E79 |
| RT-E nonsense | **KILL** KB-E1: pinstall_policy=7 (gate vacuous); **SURVIVE** KB-E2: self-corrects at E15 → revoke_step=15, commit_policy=1 | same: KILL E1 / SURVIVE E2 | same | same | same |
| RT-F displace | **KILL** KB-F1: npromote=1, promote_policy=2, nuninstall=0 (one-way door; E49–50 re-teach inert, E51+ evidence never consulted) | **SURVIVE**: revoke_step=15 (never promotes) | **KILL** KB-F1: promotes, undisplaced | **KILL** KB-F1: promotes, undisplaced | **SURVIVE**: lawfail_step=15 (never promotes) |

Predicted aggregate: **22 KILL cells, 8 SURVIVE cells** out of 30.

## 6. Predicted root causes (to confirm or refute)

- **P1 (sentinel):** the eliminative survivor selection initializes the *acted*
  policy's own slot to 99 ("not evaluated") and checks slot 0 first, so for
  `act=OVERWRITE` the 99 beats every genuine counterfactual signal — the erasing
  rule can never be displaced, and every `sig_live==-1` episode logs a sham
  uninstall+recommit. Same root cause as the a1 99-defect in the mechanics red team.
  Fix direction: genuine counterfactual signals must be checked before the
  unevaluated slot, or unevaluated slots must initialize to -1 (repair cost: small,
  one selection block per arm; re-verify all 78 checks).
- **P2 (world-signal fragility):** `sig_live==-1` trusts that the world honored the
  action; a world that drops quarantine writes manufactures false revocations
  (RT-C). No liveness check exists on the action's world effect.
- **P3 (finite verification window):** revocation machinery is gated
  `ep>=15 && ep<=48` in all five targets; post-promotion evidence is structurally
  never consulted (RT-F). a2/F3 survive RT-F only by revoking pre-promotion.
- **P4 (capacity):** the 64-slot quarantine has no pressure handling; dense honest
  contradiction schedules wedge the learner (`badep=1`) instead of degrading
  gracefully (RT-D).
- **P5 (gate):** the E14 install gate admits any i32 as a policy (RT-E); recovery
  relies on counterfactual self-correction at E15, which works but is luck of the
  survivor ordering, not a gate.

## 7. Build and evidence method (frozen)

- Vendored pristine originals under `orig/` with `SHASUMS` proving byte-identity
  to the branch files.
- Attack binaries are built from patched **copies**; canonical branch files are
  never modified.
- Patches: (a) `RT_MODE` const + `rt_ep_info` schedule wrapper in each substrate
  copy (0=standard, 1=flood E15+, 2=displace E49+, 3=silent aa); (b) default-only
  aa-line gate for modes 2/3; (c) RT-C actuator-fault block (drop live quarantine
  writes, keep the audit); (d) per-attack `main()` calling the arm with attack
  params; (e) `RT_FACTS` instrumentation lines (commit_policy/uninstall_policy/
  promote_policy first-aux dumps) inserted before each arm's `return f;` — metrics
  only, no behavior change.
- Verdicts are read from `TN_CHECK` actuals + `RT_FACTS`; the arms' own hardcoded
  expectations are ignored (they encode the old honest/lying traces).
- Every binary runs twice; KB-DET requires byte-identical stdout.
- Fidelity binaries (standard config, original mains) must reproduce the committed
  canonical numbers before any attack result counts (KB-FID).
- Static checks: no rng/rand/seed tokens in any attack source; pure Zag.
- Commit order: (1) this PREREG alone; (2) build script + orig/ + evidence;
  (3) RESULTS.md with the verdict table.

## 8. Limitations

- White-box red team (mechanism sources studied first); not an independent
  black-box audit.
- RT-C's fault model (world drops quarantine writes) and RT-D's dense schedule are
  adversarial worlds, not observed ones.
- RT-F's re-teach is mechanically a TEACH audit event; the learner has no
  post-E14 install path by construction, so the "re-teach" is audible but inert —
  the finding is about the one-way door, not about teaching.
- A lie consistent with every stated law and with no observable consequence
  remains indistinguishable (inherited honest limitation from the
  nevercontradicted red team); none of RT-A..RT-F probe that class.
