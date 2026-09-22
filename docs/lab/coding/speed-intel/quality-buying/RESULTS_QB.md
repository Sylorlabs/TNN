# QUALITY-BUYING — results synthesis (2026-09-22)

**Frozen prereg:** `PREREG_QB.md` (commit `39d4ccb6b4ea550dd7e12ac8af863aae59bcc08b`,
verified, never amended).
**Question:** can qualitatively DEEPER deliberation — a different kind of
compute, not more iterations — buy quality PAST the knee (18/18 coding,
59/94 epistemic)? Budget held at the knee in all arms; only deliberation
structure varies; no new predicates/knowledge (§4).
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Pure Zag, zero RNG, 3 reruns per cell, all canonical logs byte-identical.

## 1. Epistemic domain — `work_epi/` (commit `edae08c50f99b3e6b73a2dfc46e54fbe802f5123`)

`delib_qb.zag`: 2x pipeline + modes d0–d5 on the frozen 94-item A1R battery.
QB-CAL PASS: D0 reproduces 59/94 at 9.000 preds/item, digest
`57cefaa42100f695…23bd650` matching the frozen A1R 2x digest.

| arm | Q_e /94 | ΔQ | preds/item | Δpreds (total) |
|---|---|---|---|---|
| D0 baseline | 59/94 | — | 9.000 | — |
| D1 conflict-driven | 59/94 | +0 | 10.117 | +105 |
| D2 3 critic rounds | 12/94 | **−47** | 12.000 | +282 |
| D3 hypothesis competition | 59/94 | +0 | 12.000 | +282 |
| D4 one-brain phases | 58/94 | −1 | 12.000 | +282 |
| D5 combined | 59/94 | +0 | 17.117 | +763 |

QB-QUALITY: no arm scores (none > 59/94). QB-WORTH: n/a (ΔQ ≤ 0 everywhere).

## 2. Coding domain — `work_code/` (commit `97fcd720ecdec59cd71c05b9a9368a557aa27a91`)

`learner_qb.zag` = `learner_si4.zag` + 908 purely additive lines (0 removed/
modified); `driver_qb.py` plumbing-only, grep-clean. Frozen 20-item SI
battery at budget 4, combo machinery active in all arms. QB-CAL PASS: D0
reproduces 18/18, 2/2 halts, 46 iters, 28 znc, 45 hyp-evals. QB-NOREG PASS
(all arms 18/18, halts preserved). QB-GATE PASS (36/36).

| arm | Q_c | iters | znc | hyp-evals | Δevals | Δznc |
|---|---|---|---|---|---|---|
| D0 | 18/18 | 46 | 28 | 45 | — | — |
| D1 | 18/18 | 46 | 28 | 45 | +0 | +0 |
| D2 | 18/18 | 46 | 27 | 101 | +56 | −1 |
| D3 | 18/18 | 46 | 28 | 137 | +92 | +0 |
| D4 | 18/18 | 46 | 28 | 68 | +23 | +0 |
| D5 | 18/18 | 46 | 27 | 216 | +171 | −1 |

## 3. Quality-per-cost curve (both domains, vs D0)

| arm | ΔQ_e | ΔQ_c | Δcost (epistemic) | Δcost (coding) | worth it? |
|---|---|---|---|---|---|
| D1 conflict-driven | +0 | +0 (ceiling) | +12% preds | +0 evals | no gain |
| D2 multi-round critique | **−47** | +0 (ceiling) | +33% preds | +124% evals | **destructive** |
| D3 hyp. competition | +0 | +0 (ceiling) | +33% preds | +204% evals | no gain |
| D4 one-brain phases | −1 | +0 (ceiling) | +33% preds | +51% evals | no gain |
| D5 combined | +0 | +0 (ceiling) | +90% preds | +380% evals | no gain |

No arm has a defined marginal price per +1 item (no +1 exists anywhere).

## 4. Verdict (frozen rules applied mechanically)

**QB-CEILING: CEILING-CONFIRMED.** No deeper deliberation form buys
past-knee quality in either domain. The knee is the ceiling of
deliberation; further quality must come from new mechanisms or new
knowledge, not more compute.

## 5. What the failures teach (mechanism notes)

1. **The ledger is the binding constraint, not the decision procedure.**
   D1, D3, and D5 — three different deliberation structures — converge to
   exactly the staged verdicts on all 94 epistemic items. Re-reading the
   same evidence more elaborately cannot extract what isn't there.
2. **Critique without a justification requirement is destructive.**
   D2's frozen mechanical challenge-validity rule flipped all 47
   single-evidence-bit items from correct to wrong (59→12/94); rounds 2–3
   could not undo it. It attacks precisely the thin-but-correct evidence.
   A critic that must MEET A JUSTIFICATION BAR before overturning might
   behave differently — that is a new experiment, not a rescue of this one.
3. **Composition can stabilize but not improve.** D5's final d3 stage
   silently rescued all 48 internal stage-flips (traced in logs) — the
   pipeline's end state is an attractor. Depth composes into the same
   answer, not a better one.
4. **The coding mechanisms are functional but the battery never contests
   them.** On crafted probes: D1 overturns a tied argmax on evidence
   count; D2's critic genuinely rejects defective drafts (caught the exact
   TYPE patch that fails znc compile in D0's S06 trajectory); D3's
   competition turned a D0 `halt-no-patch` into a correct brace-closing
   patch on a crafted TYPE-vs-SYNTAX case; D4 strikes a refuted leader.
   On the frozen battery: D1 never contests (0 divergences), D2 reorders
   S06 only (saving 1 znc), D3/D4 never overturn/strike. A harder battery
   with ambiguous diagnoses is needed to test whether deliberation buys
   anything on coding — the current battery is saturated at 18/18.
5. **Deliberation is cheap; it just doesn't help.** On coding, deeper
   deliberation adds ~zero CPU (znc dominates wall-clock). On epistemic,
   the deeper forms cost +12% to +90% more predicate evaluations for zero
   or negative quality. There is no price at which this compute buys
   intelligence here.

## 6. Honest limits (carried from the prereg)

- Coding battery saturates at 18/18; coding cells measured non-regression
  + cost only.
- Epistemic misses are knowledge gaps: 35/70 weird items fire no
  nonfactual predicate by construction and are unrecoverable by any
  deterministic function of the ledger under §4 — confirmed empirically.
- D2's destructiveness is specific to the frozen mechanical
  challenge-validity rule; a justification-barred critic is untested.
- Single-threaded substrate: D4 measures added evaluations, not
  wall-clock parallelism.
- The SI coding battery is 20 synthetic items; real-world repair is
  unmeasured.

## 7. Files

- `PREREG_QB.md` — frozen prereg (commit `39d4ccb6…`)
- `work_epi/` — `delib_qb.zag`, scorer, 54 canonical logs, `RESULTS_QB_EPI.md`
  (commit `edae08c50f99b3e6…`)
- `work_code/` — `learner_qb.zag`, `driver_qb.py`, 18 run JSONs + logs,
  `RESULTS_QB_CODE.md` (commit `97fcd720ecdec59c…`)
- This file — synthesis (to be committed below)
