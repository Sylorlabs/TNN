# BATTERY-HEALTH AUDIT — frozen-battery parse results

Red team, battery-design leg · 2026-09-21/22. Reproducible:
`audit_batteries.py` (stdlib only, deterministic); full output in
`AUDIT_OUTPUT.txt`. Each finding: CONFIRMED (ran the parse) or DOCUMENTED
(verified against the verdict text).

## A1. Prose v2 NEG sub-battery — CONFIRMED: 36/36 impossible by construction

- Parse: `inputs2/sub_neg_test.jsonl`, n=36. Two probe texts appear twice with
  conflicting expects:
  - id 18 / id 30: `How many members do the "Beatles" have?` → `unknown` vs `value`
  - id 19 / id 31: `How many members does the "Jackson 5" have?` → `unknown` vs `value`
- No learner can satisfy both members of either pair. Maximum achievable
  probe score: **34/36**, not 36/36. (The v2 bar was "0% leakage" — negated
  values never returned — whose literal condition HELD; the 36/36 probe-score
  number was the unachievable one.)
- Status: already found by Worker C, documented in v2 VERDICT §3, and FIXED in
  v3 (PREREG3 §C3: probes 18/19 rephrased; all 36 probe strings now unique).
- Audit value: confirms the defect mechanically; confirms the fix target.

## A2. Cross-sub-battery probe collisions — CHECKED, not a defect

- 50 probe texts appear in more than one v2 sub-battery; 31 with conflicting
  expects (e.g. `Tell me the alphabet position of A.` → `unknown` in NEG,
  `hedged` in HEDGE, `value` in PARA).
- Each sub-battery runs as an INDEPENDENT run (own train file, fresh learner
  state). No state carries across batteries, so no conflict is satisfiable or
  violable. Verified non-issue. (If sub-batteries are ever composed into one
  run, this becomes A1-class.)

## A3. sub_multi_test duplicate probes — CHECKED, benign

- 2 duplicate probe texts with IDENTICAL expects. No conflicting requirement;
  scores normally. Benign.

## A4. Championship sol integer corpus — HEALTHY

- `corpus.json`: 240 teach items, **240/240 distinct probe texts**, 0
  conflicting expects, 0 duplicate observations. The integer channel's headline
  battery is clean on duplicates.

## A5. Principle-detection `expected.json` — HEALTHY on duplicates

- 45 facts, 19 principles, 4 exemptions; 0 exact-duplicate items.
- Health note (not a parse defect): principles are stipulated background and
  refinement is logged-not-applied — documented in the verdict's scope notes;
  see blind-spot map H3.

## A6. Info-source envelopes — HEALTHY structurally, frozen by design

- 17/17 envelope files present, 8/8 results each, recorded 2026-09-22 via
  SearXNG. Structural health is fine; the frozen-vs-live question is a design
  property, not a parse defect — see RANKED_ATTACKS #2.

## A7. New-mechanisms prereg — CONFIRMED: kind-5 n typo (minor)

- PREREG.md construction table says kind 5 n=24; the prereg's own kill bar
  (KB-M-TEMPORAL: "kind-5 = 1.0 (12/12 kept)") and the N=264 total force
  kind-5=12. Code ranges confirm: kind 5 = f in [216,228) = 12 facts.
- Minor doc defect; all verdict numbers use 12 (correct). No verdict moves.

## A8. New-mechanisms implementation — CONFIRMED: kind-dispatched mechanism (major)

- `hypcomp_fact` (`mech_learner.zag`) opens with `let k:i32=bat_kind(f);`
  and dispatches: k==4||k==5 → install-candidate-0 + challenge-candidate-1;
  k==3 → `first_install_pairs` (hardcodes the battery's 32-bit pair encoding);
  k==6 → spoof pre-filter on candidate 0's flag; else scalar trust-sum
  competition. `bat_kind` is the battery's own kind function.
- Battery generator (`bat_kind`/`bat_cand`/`bat_truth`/`bat_lie`) and learner
  share ONE binary (554 lines). The SPEC.md describes the generic
  eliminative version; the implementation is kind-dispatched (the spec itself
  labels Step 4 "pairs (kind 3)").
- Consequence: the 156/156 cannot generalize beyond the taxonomy by
  construction — a novel contradiction class requires editing both the battery
  functions and the dispatch. See RANKED_ATTACKS #1.

## A9. Flaw-battery degeneracy — DOCUMENTED, confirmed against verdict

- Few-shot verdict: distinct probe ids N=192: 24, N=96: 24, N=48: 12, N=24: 6,
  N=16: 4, N=8: 2, N≤4: 1. The 96/96 at full scale = 4 check-types × 24
  distinct probe facts; below N=96 it is repeated probes of the same few facts
  ("each executed check passed" — the checks are honest, the resolution isn't).
- The verdict carries the asterisk and the counts. Transparent handling; the
  instrument's effective resolution (24) should be stated wherever 96/96 is
  quoted — currently it is only in the fewshot verdict.

## A10. B-vs-C absorption discrepancy — RESOLVED, not merely documented

- v2 VERDICT §4 declared the brief's (9,11,11,11) "irreconcilable under any
  coherent metric." GATE0_RESOLUTION (2026-09-22) reproduced all four numbers
  mechanically: the brief's figures = ABS-3 (INSTALL, attitude=asserted,
  exact value, correct multi-token-entity parsing); Worker C's middle row =
  ABS-3 with a parser bug dropping multi-token entities; the "irreconcilable"
  sentence was RETRACTED; ABS-3 frozen as the metric.
- Audit value: this is the system working — documentation led to
  investigation, a parser bug was found, a metric was frozen, a false claim
  retracted. Cited in RANKED_ATTACKS as counter-evidence to the
  metric-shopping charge.

## Batteries NOT audited (deferred)

- §B.7 sealed flaw manifests (8 slices × 12 flaws): parse requires the sealed
  manifest; W7 verified 12-per-slice class mix programmatically (4/4/2/2).
  Sealed by design — the red team did not break the seal. Spot-check via W7's
  evidence only.
- Self-test's 8 compiled-in battery kinds: manifest is compiled into the
  binary (documented limitation #1 in SELFTEST_VERDICT); audit would require
  disassembly. Deferred.
- Dialogue/conversation trial batteries: trial dispatched 2026-09-21, battery
  not yet frozen at audit time.
