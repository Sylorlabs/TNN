# TRIAL_RESULTS — Deliberate Recall (2026-09-19/20)

## Verdict: POSITIVE

All six preregistered falsification criteria hold (F1–F6). The selection
rule — a fixed conjunction of symbolic predicates over an audited declared
need — beats the similarity+top-k baseline on precision (1.000 vs 0.000
macro mean over adversarial episodes) with zero recall loss, and the
extra-steps falsifier confirms the logic is not thresholded similarity in
disguise. The system is fully deterministic (byte-identical reruns, no RNG
anywhere); the adversity was entirely in the designed curriculum.

## Evidence

Native trial `trial/` (evidence bundle
`trial/EVIDENCE_20260920T002414Z/`): 140/140 `CL_CHECK` lines
actual==expected, `DR_FAILURES,0`, two runs byte-identical, static grep
confirms no `rng|random|seed|_zag_arg` in code lines.

Per-episode (deliberate n, tp / baseline n, tp / deliberate act / baseline act):

```
DR_EP,0,1,1,1,1,10,10      control: both retrieve {T0}, both act right
DR_EP,1,1,1,1,0,11,19      P3 trap: deliberate {T_a}; baseline {D_a} (unverified) -> wrong act
DR_EP,2,1,1,1,0,12,-1      P2 trap: deliberate {T_b}; baseline {D_b2} (lacks op C) -> abstain
DR_EP,3,1,1,1,0,13,10      P4 trap: deliberate {T_c}; baseline {D_c} (stale) -> wrong act
DR_EP,4,2,2,2,0,14,-1      compose: deliberate {T4a,T4b}; baseline {D_c,T_a} -> disagree -> abstain
DR_MEAN,1000,0,1000        macro mean precision permille, adversarial eps
```

Tau-sweep (single τ, all episodes, post-hoc best — the threshold family
gets its best shot):

```
DR_TAUROW,0,139,75 / 1,155,84 / 2,235,133 / 3,444,285 / 4,461,428 / 5,0,0 / 6,0,0
DR_TAU,4,461,428            best τ=4: mean F1 0.461, mean P 0.428 < deliberate 1.000
```

Predicate forensics (audited predmasks; P1=1 P2=2 P3=4 P4=8): D_a=11
(P3 failed), D_b2=13 (P2 failed), D_c=7 (P4 failed), D4=11 (P3 failed in
compose); all relevant traces =15. Every predicate is the excluder
somewhere — none is dead weight.

Audit: `ma_replay_check` and `rc_replay_check` both pass — descriptors,
needs, every scan bitmask, every selection, and every act recompute from
the ledgers. Negative checks pass: KILL refused at stage MANAGE;
safety-critical need with provenance ANY refused at declaration.

## Criterion-by-criterion

- **F1 (primary):** meanP_delib − meanP_base = 1.000 ≥ 0.25; meanP_delib =
  1.000 ≥ 0.9. HOLD.
- **F2 (recall guard):** deliberate recall = 1.0 on all five
  ground-truth required sets. HOLD.
- **F3 (extra-steps):** best single τ reaches (0.428, —) vs deliberate
  (1.000, 1.000). Not replicated. HOLD — the traps' tied scores straddle
  the logical boundary by construction, and the sweep verifies it.
- **F4 (audit):** both ledgers replay exactly. HOLD.
- **F5 (determinism):** byte-identical reruns; static no-RNG. HOLD.
- **F6 (predicate coverage):** P2/P3/P4 each the unique excluder ≥1
  episode (P1 excludes fillers throughout). HOLD.

## What the result does and does not mean

The mechanism claim is confirmed *for the tested form*: hard logical
gates + op-entailment select what compensatory scoring cannot, without
tuning, and every choice is auditable to a named predicate. Downstream,
deliberate recall acted correctly 5/5; similarity retrieval produced 1
right action, 2 wrong actions, 2 abstentions — retrieval quality, not the
act rule, was the difference (same act rule both arms).

Limits (preregistered): need *formation* is protocol-fixed — this trial
tests the selection rule, not how needs are formed; the extra-steps
falsifier scopes to the obvious similarity score; N=16 traces, 5
episodes — generality rides on the scale argument below, not on N.

## Honest notes from the run

1. Two mid-build corrections, both pre-completion and both recorded in
   PREREG.md / RECALL_DESIGN.md amendments: (a) EP4's six-way similarity
   tie resolves to {D_c, T_a} by index order, not the designed {D4, T4a}
   — the trap still fires (baseline P=R=0), via stale/wrong-entity
   distractors rather than the unverified D4; (b) one rc_replay coverage
   failure during development (multiple recalls per need broke the
   scan-coverage invariant) fixed by restructuring to one recall per
   need — the invariant did its job.
2. The static no-RNG grep initially matched the word "RNG" in code
   comments; the runner now checks code lines only. No randomness was
   ever present in code.

## Scale status and next step

Trial: S=16, per-recall O(S) scans × O(1) predicate work (four bitmask
ops; no scores, no sorts on the deliberate path). Next scale test
(preregistered): **10x distractor scale** — replicate filler/distractor
families ×10 (160 traces; same 5 relevant traces and needs); assert
identical precision/recall per episode and per-episode recall time ≤ 15x
trial time. Known scaling parameter: `RC_AUDIT_CAP` ∝ S·recalls (100x
needs the cap raised; documented in RECALL_DESIGN.md §7, not a
redesign). Suggested follow-up after the 10x leg: need *formation* —
the one protocol-fixed piece this trial does not test.

Files:
- `RECALL_DESIGN.md`, `PREREG.md`, `TRIAL_RESULTS.md` (this file)
- `trial/recall_core.zag` — needs, descriptors, NEED_DECLARE, RECALL,
  recall-ledger + replay
- `trial/recall_trial.zag` — driver (SYSTEM / EVALUATOR boundary marked)
- `trial/run_recall.sh` — runner (static no-RNG check, double-run
  determinism, CL_CHECK verification)
- `trial/EVIDENCE_20260920T002414Z/` — compile/run logs, input hashes,
  summary
