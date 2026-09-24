# H5 Item-Encoding Spec v1 (frozen)

- **Status:** FROZEN under H5 coordinator §12 amendment, 2026-09-23
  (see `../AMENDMENT_S12.md`). Any change requires coordinator sign-off,
  a version bump, re-translation of all 877 items, and re-measurement.
- **Scope:** a mechanical, deterministic translation of the 877 frozen
  battery/red-team items into the harness item format
  (`../harness/ITEM_FORMAT.md`). This is an **input bridge, not a spec
  change**: DEPTH_DEF.md v1 and PREREG_H5.md v1 are unchanged.
- **Non-goals:** the spec does not re-execute any battery program, does
  not interpret natural language, and assigns no per-item hand-authored
  weights. Every weight below is either a fixed constant or a fixed
  scaling of a number already present in the item payload.

## §1 Source inputs (frozen)

| Battery | Frozen commit | File | n |
|---|---|---|---|
| admit | `50a62d38c8353eff2169e5a676c45b046f81729f` | `batteries/admit_battery.jsonl` | 248 |
| revoke | `50a62d38c8353eff2169e5a676c45b046f81729f` | `batteries/revoke_battery.jsonl` | 113 |
| logic | `50a62d38c8353eff2169e5a676c45b046f81729f` | `batteries/logic_battery.jsonl` | 264 |
| trap | `ba05b096f12ee7dd7404838c95845330d2a7da5a` | `redteam/trap_battery.jsonl` | 127 |
| cost | `ba05b096f12ee7dd7404838c95845330d2a7da5a` | `redteam/cost_attacks.jsonl` | 125 |
| **total** | | | **877** |

Blob-level verification of these inputs is in
`../results/evidence/frozen_input_verification.txt` (Crew 5).

## §2 Target format

Harness judgment items (JSONL), one object per line:

```json
{"id":"<item id>","task_type":"admit|revoke|logic",
 "input":{"hypotheses":[{"id":"<H>","label":"<H>"}...],
          "evidence":[{"id":"e1","supports":{"<H>":500},"attacks":{},"text":"..."}...]},
 "ground_truth":"<H>"}
```

Constraints (harness parser, frozen): hypotheses 1–16, evidence 0–64,
≤16 support/attack links per evidence item, ids match
`[0-9A-Za-z_.-]{1,64}`, `ground_truth` must name a hypothesis, every link
must reference a known hypothesis, weights are JSON integers
(fixed-point thousandths), strings contain no `"` or `\`.

## §3 Global mechanical rules

- **G1 — ids.** Item `id` copied verbatim. (All 877 source ids are
  charset-clean; the translator asserts this and fails loudly otherwise.)
- **G2 — ground-truth charset mapping.** Every character outside
  `[0-9A-Za-z_.-]` is replaced with `_`. Applied to ground truths,
  shallow answers, and hypothesis ids derived from them. In the frozen
  batteries this fires exactly twice:
  - `KILL/SURVIVE` → `KILL_SURVIVE` (5 revoke items)
  - `P and not-Q` → `P_and_not-Q` (5 trap items, C6-wason-selection)
  
  The translator asserts the mapped hypothesis set of each item has no
  collisions (verified: none).
- **G3 — text sanitization.** `text`/`label` fields: `"` → `'`,
  `\` → `/`, control characters (`<0x20`) deleted, `\r` stripped,
  truncated to 4000 characters. (The harness ignores `text`; it is
  carried for human audit.)
- **G4 — evidence ids.** `e1 … en` in emission order.
- **G5 — hypothesis labels.** `label` = the (G2-mapped) hypothesis id.
- **G6 — task_type.** Copied from the source item's `task_type`.
- **G7 — determinism.** Fixed key order
  (`id`, `task_type`, `input.hypotheses`, `input.evidence`,
  `ground_truth`); integer weights only; `ensure_ascii` JSON. The same
  frozen inputs always yield byte-identical outputs.
- **G8 — ground-truth anchoring.** The encoded `ground_truth` is the
  source item's `ground_truth` (G2-mapped). Verified pre-freeze: it
  equals the payload's own program verdict on 877/877 items
  (`provenance.gate_program_verdict` for admit,
  `provenance.program_derived_verdict`/`bar_outcome`/`program_verdict`
  for revoke where present; the logic engine's verdict is the GT by
  construction).

## §4 Per-battery rules

### §4.1 admit — PAM gate dispositions (248 items)

- **Hypotheses** (fixed for the battery, alphabetical, 9):
  `ACCEPT_INSTALL`, `CONFLICT_WITHHELD`, `CORROBORATED`,
  `NEGATIVE_EVIDENCE`, `PERMANENT_INSTALL`, `PROVISIONAL_INSTALL`,
  `REVISE_INSTALL`, `SUPPRESSED`, `WITHHELD`.
- **GT:** item `ground_truth`.
- **Evidence:** for each row `r` in
  `[input.prior_same_task (array order), input.trial]` — one evidence
  item with `supports: {GT: r.confidence}` (the row's own confidence,
  already fixed-point thousandths) and text
  - prior: `prior seq=<seq> fixture=<fixture> judgment=<judgment> disposition=<disposition> confidence=<confidence>`
  - trial: `trial seq=<seq> tcode=<tcode> judgment=<judgment> confidence=<confidence> measure=<measure>`
  
  (G3-sanitized.)
- **Rationale (recorded, not a validity criterion):** the gate program's
  verdict for the item's trial is GT; the rows are its supporting
  context. The gate policy text is not re-executed — no mechanical rule
  can do that faithfully. Consequence: the admit curve measures the
  harness's convergence on program verdicts (expected: flat, high).

### §4.2 revoke — FL2 red-team verdicts (113 items)

- **Hypotheses** (fixed for the battery, alphabetical, 6):
  `BROKEN`, `HOLD`, `KILL`, `KILL_SURVIVE`, `PASS`, `SURVIVE`.
- **GT:** item `ground_truth` (G2-mapped).
- **Evidence** (fixed weight 500), by `input.item_kind`:
  - `cell_verdict` with `observed`: one item per key, keys sorted
    ascending: text `observed.<key>=<value>`, `supports: {GT: 500}`.
  - `cell_verdict` with `observed_metrics`: one item per key, keys
    sorted ascending: text `metrics.<key>=<value>`,
    `supports: {GT: 500}`.
  - `kill_bar`: one item: text
    `kill_bar <kill_bar>: <kill_bar_definition>`,
    `supports: {GT: 500}`.
  - `fidelity_gate`: one item per `observed` key (sorted):
    text `observed.<key>=<value>`, `supports: {GT: 500}`; plus one item:
    text `fidelity_gate: <fidelity_gate>`, `supports: {GT: 500}`.
- **Rationale:** the kill conditions live in free-text definitions that
  no fixed rule can evaluate; the payload's recorded verdict is GT.
  Consequence: same as §4.1 — the revoke curve is a convergence check.

### §4.3 logic — native-logic engine verdicts (264 items)

- **Hypotheses** (fixed for the battery, alphabetical, 3):
  `AFFIRM`, `DENY`, `NEUTRAL`.
- **GT:** item `ground_truth`.
- **Evidence:** one item per `input.evidence` string, payload order:
  `supports: {GT: 500}`, text = the proposition (G3-sanitized).
- **Rationale:** the verdicts are the output of a native logic engine
  performing multi-step inference (modus ponens, causal chains,
  inconsistency detection). Per-evidence polarity is not recoverable by
  any fixed syntactic rule — counterexamples in the frozen battery:
  `logic-g_cond-GD-18` (affirmation emerges from the evidence *set* via
  modus ponens although no single evidence affirms alone),
  `logic-g_tmp-GP-18` (inconsistency between two evidences yields DENY),
  `logic-mlogic-ML-20/21/22/23` (DENY via multi-hop causal chains).
  Decomposing these into per-evidence polarities would re-implement the
  engine by hand. Consequence: same as §4.1.

### §4.4 trap — shallow-answer traps (127 items)

- **Hypotheses:** the item's `input.options` array, payload order, each
  G2-mapped. (Assert: GT and shallow_answer are both members.)
- **GT:** G2(`ground_truth`). **SHALLOW:** G2(`shallow_answer`).
  (Verified: GT ≠ SHALLOW on all 127 items.)
- **Evidence:**
  - Misleading set M = `input.surface_evidence` if present and
    non-empty, else `input.premises` (C-family logic traps).
  - Corrective set C = `input.deep_evidence` if present and non-empty,
    else `[input.falsifying_instance]` if present, else
    `[ground_truth_basis]` (the item's own stated basis for GT; this
    branch fires exactly on the 26 C-family items with no falsifying
    instance — the valid-argument families and C3/C4/C6).
  - Emission order: all of M (payload order), then all of C.
  - Each m ∈ M: `supports: {SHALLOW: 100}`, text = m (G3).
  - Each c ∈ C: `supports: {GT: 500}`; additionally, if
    SHALLOW ≠ GT, `attacks: {SHALLOW: 500}`; text = c (G3).
- **Weight derivation (frozen, principled — not tuned):**
  misleading weight Wm = 100, corrective weight Wc = 500, fixed by three
  constraints against the frozen harness constants
  (`elim_margin = 900`, corrective overturn = 500 + 500):
  - (a) the strongest misleading run in the battery (6 premises,
    C6-wason-selection) must not eliminate GT before corrective
    evidence arrives: 6 × Wm < 900 ⟹ Wm < 150;
  - (b) one corrective item must overturn that run:
    Wc + Wc > 6 × Wm ⟹ Wm < 166.7 (with Wc = 500);
  - (c) Wm > 0 so the depth-1 baseline selects SHALLOW.
  
  Any Wm ∈ (0, 150) satisfies (a)–(c); Wm = 100 is the round choice.
  Wc = 500 is the harness's standard decisive-evidence scale (same as
  the base batteries and the Phase-1 smoke items).
- **Intended dynamics (descriptive, not a validity criterion):**
  depth-1 consumes one misleading item → verdict SHALLOW (the prereg
  §2 trap gate); full consumption → GT (see §5 F1/F3).

### §4.5 cost — cost attacks (125 items)

- **Hypotheses:** the item's `input.options` array, payload order,
  G2-mapped. (Assert: GT ∈ hypotheses.)
- **GT:** G2(`ground_truth`).
- **D1-balanced-treadmill** (20 items): rounds in `round` order. Each
  round has a payload `score_delta` (points). Fixed scaling:
  **1 point = 250 thousandths** — the item's own ±4-point decision bar
  maps to the full 1000 confidence scale. Polarity from the payload's
  `decision_rule` via the frozen regex
  `^(\w+) iff cumulative evidence score >= \+(\d+); (\w+) iff <= -(\d+)$`:
  group 1 (case-insensitive) must equal one option (the POS side),
  group 3 must equal the other (the NEG side); the translator asserts
  this on every item. Each round: `score_delta > 0` →
  `supports: {POS: 250×delta}`; `score_delta < 0` →
  `supports: {NEG: 250×|delta|}`; `score_delta = 0` → no links.
  Text = the round text (G3).
- **D2–D8** (105 items): each round (round order):
  `supports: {GT: 500}`, text = the round text (G3). The rounds'
  payload texts all point in the GT direction (rephrases, further
  measurements, more sources); the attack is that a naive judge keeps
  counting them. The harness's clamped-margin confidence is the
  standing defense — the measurement says whether it holds.
- **`optimal_stopping_depth` / `gain_vanishes_proof`:** carried into
  analysis per prereg §3 (adaptive `rounds_used` vs d*; D1's proof is
  verified as a property of the encoded items — cumulative score
  invariant after round 2), not into weights.

## §5 Fidelity checks (all required)

- **F1 — full re-derivation (100%).** Independent of the harness: for
  every translated item, compute
  `argmax_h (Σ_e supports_e(h) − Σ_e attacks_e(h))` with ties broken to
  the lowest hypothesis index (the harness's tie rule). It must equal
  `ground_truth` on **877/877** items. Any failure is a spec/translation
  defect: fix the *rule* globally, never the item.
- **F2 — independent spot re-derivation (10%).** A second,
  independently written implementation of §§3–4 (no shared code with the
  translator) re-translates every 10th item in file order
  (deterministic sample: indices 0, 10, 20, …). Its output must be
  byte-identical to the committed translation on **100%** of the
  sample (~88 items).
- **F3 — harness convergence.** All 877 translated items parse in the
  fixed (§12) harness with 0 errors, and the fixed-depth-16 verdict
  equals `ground_truth` on **877/877** items (the harness's eliminative
  mechanics must converge on the encoded GT).
- **F4 — trap gate pre-check.** The fixed-1-round baseline selects
  `shallow_answer` on **100%** of trap items (prereg §2 gate needs ≥90%
  per family).

## §6 Worked examples

**admit** (`admit-V2-A-clean-0000`, GT `PROVISIONAL_INSTALL`,
trial confidence 931, no priors):
```json
{"id":"admit-V2-A-clean-0000","task_type":"admit",
 "input":{"hypotheses":[{"id":"ACCEPT_INSTALL","label":"ACCEPT_INSTALL"}, ... 9 total ...],
          "evidence":[{"id":"e1","supports":{"PROVISIONAL_INSTALL":931},"attacks":{},
                       "text":"trial seq=0 tcode=3 judgment=HIGHER confidence=931 measure=45743"}]},
 "ground_truth":"PROVISIONAL_INSTALL"}
```

**trap** (`TRAP-A1-001`, GT `REJECT`, SHALLOW `ADMIT`,
2 surface + 3 deep):
evidence `e1,e2`: `supports: {"ADMIT": 100}`;
`e3,e4,e5`: `supports: {"REJECT": 500}, attacks: {"ADMIT": 500}`.
Full-consumption scores: ADMIT = 200 − 1500 = −1300, REJECT = 1500 →
verdict REJECT = GT. Depth-1: ADMIT = 100 → verdict ADMIT = SHALLOW.

**cost D1** (`COST-D1-001`, GT `ADMIT`, deltas `[3,2,1,-1,2,-2,1,-1]`):
`e1: supports {"ADMIT": 750}`, `e2: {"ADMIT": 500}`,
`e3: {"ADMIT": 250}`, `e4: {"REJECT": 250}`, … (250/point).

## §7 Change control

Frozen v1, 2026-09-23, under H5 §12 amendment. Changes require H5
coordinator sign-off, a version bump of this file, re-translation of
all 877 items, and re-measurement of every affected leg. The translator
(`encode_items.py`) is the executable form of this spec; the two are
frozen together — a discrepancy between them is a defect in the
translator, fixed to match the spec.
