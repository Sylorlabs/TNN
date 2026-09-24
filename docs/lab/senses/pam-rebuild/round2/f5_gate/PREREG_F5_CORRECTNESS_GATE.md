# PREREG — F5 correctness-aware gate (repair fork)

Frozen 2026-09-24. Committed ALONE before any code. Builder: F5-gate crew
(PAM round-2 swarm, crew 3; parent session 0c8c1318).

This prereg executes honest path #2 from `round2/f5_redteam300/VERDICT_F5_REDTEAM300.md`:
"add a correctness-aware gate BEFORE the block — a cheap independent
correctness check that must also fail before the trap blocks."

## 1. Background

F5's counter-corroboration trap was KILLED by the 300-percept red-team
(prereg `round2/f5_redteam300/PREREG_F5_REDTEAM300.md`, committed alone as
`f36b55381a9192287124d0f4a2b12a927fa55073`; verdict KILL 2026-09-24):

- Frozen predicate: BLOCK iff same family stem AND |Δconf| ≤ 150 AND
  |Δmeasure| ≤ 2000 vs any of 6 bank exemplars (frozen `exemplars.tsv`,
  SHA `13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`;
  exemplar cluster: conf 701–718, measure 2618–2647).
- Measured: 110/300 (36.7%) near-exemplar CORRECT percepts blocked;
  94/300 (31.3%) delayed > 50 trials under the primary queue model →
  the > 25% kill bar fired. Far control 0/60 passed.
- Root cause (verdict §"Reading the KILL honestly"): the window
  (±150/±2000) is vastly wider than the exemplar cluster it was built from
  (±2000 on measure = a 4000-wide band around a cluster spanning 29).

## 2. Hypothesis under test

A correctness-aware gate placed BEFORE the block — BLOCK ⟺ (frozen trap
fires) ∧ (correctness gate FAILS) — restores the delay bar and cuts the
36.7% over-block of correct percepts while retaining the 8/9 false-block
recall from the backtest. The gate is cheap (two box tests on values the
trap already computed) and independent in the sense defined in §4.

## 3. The gate (frozen definition)

The correctness gate FAILS — allowing the block — iff the candidate's
`(confidence, measure)` falls inside the DOCUMENTED WRONGNESS SIGNATURE:
the union of two boxes. Box bounds are the EXACT observed min-max from
frozen committed sources, computed by script at freeze time (no margins,
no tuning):

- **Box A — exemplar wrongness:** conf ∈ [701, 718], measure ∈ [2618, 2647].
  Source: frozen `exemplars.tsv` (6 RICH-judged / BRIGHT-true wrongs;
  min/max re-derived live 2026-09-24, identical to the
  PREREG_F5_BACKTEST.md §2b table). Rationale: an exact repeat of a bank
  member must still block; the box costs 0 of the 300 grid points.
- **Box B — backtest false wrongness:** conf ∈ [764, 832],
  measure ∈ [1888, 2373]. Source:
  `v2/redteam/evidence/ledger_d_withhold.txt`
  (SHA `63ea591d8cbb9d8b3e1cd088364e96d8fdfa19d435e337dfac0ad17a0326c2b1`),
  the 8 `rt4_TMB-5_*` RICH-judged / DARK-true false accepts
  (min/max re-derived live 2026-09-24 via awk over the committed ledger).

The gate PASSES — withholding the block — for every candidate outside
both boxes. The gate reads ONLY `(confidence, measure)` plus the four
frozen box constants. It does NOT read truth, the `SET=` field, `jG`,
`confG`, `pred`, `prog`, hashes, or any other field.

Deliberately NOT included:

- No box around the 9th backtest false (`rt4_COL-4_0000`, DIFFERENT/SAME):
  the trap never fired on it (family-stem mismatch) and a single point is
  not a recurring signature. Retention is measured 8/9 as in the backtest.
- No "positive correctness" box (e.g. around the 6 observed correct
  BRIGHT/BRIGHT at conf 869–952 / measure 4000–6000): on the frozen
  300-grid its intersection with the trap window is EMPTY, so it would be
  dead weight; and there are ZERO observed correct RICH judgments
  anywhere in the real data, so any positive box for RICH-judged
  candidates would be speculation, not evidence. The gate is therefore a
  documented-wrongness check, not a correctness certificate (§5).

## 4. The byte-side-correlation wall — how this gate escapes it

The wall: a second organ reading the same spoofed bytes to determine TRUTH
repeats the same lie. This prereg takes the wall seriously and escapes it
as follows (second-read justification, not different bytes):

1. **The gate does not determine truth from the bytes.** It determines
   SIMILARITY TO DOCUMENTED LIES. The bytes are treated as untrusted
   throughout: the gate never concludes "this percept is correct." A pass
   means strictly "no documented wrongness precedent at these
   coordinates" — explicitly weaker than a correctness claim (§5).
   The lie is not repeated; it is recognized against committed history.
2. **Burden inversion, not second opinion.** The trap asks "is the
   candidate near known-bad?" (suspicion: high recall, low precision).
   The gate asks "does the candidate reproduce a DOCUMENTED wrongness
   signature?" (confirmation: high precision). These are different
   questions with opposite error profiles, not two reads answering the
   same question. A spoofer that defeats the trap's suspicion region by
   construction also defeats any same-axis second read — see (3).
3. **Threat scope is stated, not smuggled.** The gate addresses the
   OBSERVED threat: recurring NON-ADAPTIVE perceptual errors with stable
   signatures (14 documented wrong RICHs in two tight clusters: 6
   exemplars + 8 backtest falses). Against an ADAPTIVE byte-spoofer who
   controls (conf, measure), the ENTIRE F5 mechanism (trap included) is
   bypassable — the trap's window is public and deterministic. The gate
   introduces no NEW vulnerability class; this is recorded as a caveat,
   not hidden behind "independent check" language.
4. **Bank-side grounding.** The signature boxes are derived from the
   FROZEN bank and the committed backtest ledger — data the candidate's
   error source cannot rewrite. The gate's decision is anchored in
   committed history, not in the candidate's self-report.
5. **Residual risk, stated plainly.** Novel wrong percepts inside the wide
   trap window but OUTSIDE the signature boxes will NOT be blocked —
   trap-alone would have blocked them. Cutting over-block from 36.7% to
   ~2% is deliberately bought at this price. The unbuilt confirmation
   machinery (three deliberate re-inspections from three temporal crops)
   remains the backstop for novel error modes. If the error signature
   drifts, the boxes must be re-derived under a NEW prereg — never
   silently re-tuned.

**Impossibility note (frozen):** on the frozen fixture schema, a novel
wrong percept and a correct percept at identical (conf, measure) are
indistinguishable without truth. No gate on honest observable fields can
block the former while passing the latter. Any future claim to do so must
name the new channel.

## 5. What "correctness-aware" means here (and does not)

- MEANS: the block is withheld wherever the system has no documented
  precedent of wrongness. The 300 synthetic corrects live almost entirely
  outside the two wrongness clusters, so the gate is "aware" of the
  correct region negatively — by the absence of wrongness precedent.
- DOES NOT MEAN: the gate certifies any percept correct, reads ground
  truth, or uses the battery's `SET=` labels. "Gate passes" is not
  evidence of correctness and must never be logged or presented as such.

## 6. Frozen bars

All four must hold; (a), (b), (d) are kill bars, (c) is a reported measure.

- **(a) Delay bar:** ≤ 25% of the 300 NEAR percepts delayed > 50 trials
  under the PRIMARY queue model (FIFO confirmation queue in trial order;
  ≤ 1 deliberate re-inspection per trial; 3 re-inspections per blocked
  percept; k-th blocked percept clears at delay 3k; allowed percepts
  delay 0 — identical operationalization to PREREG_F5_REDTEAM300.md §5).
  > 25% (≥ 76 of 300) → KILL.
- **(b) Far-control bar:** 0/60 FAR controls blocked → any block → KILL.
- **(c) Over-block report:** blocked / 300 NEAR reported (baseline from
  the red-team: 110/300 = 36.7%). No kill threshold — reported.
- **(d) Backtest retention:** ≥ 8 of the 9 backtest false accepts blocked,
  replayed over the 43 `DISP=ACCEPT_INSTALL` lines of the frozen
  `ledger_d_withhold.txt` with gate+trap. < 8 → KILL.

Reported but not kill: full delay histogram (bins 0 | 1–3 | 4–10 | 11–50 |
51–100 | 101–300 | 301+), S1/S2 sensitivity cells (same definitions as the
red-team prereg), exemplar-repeat diagnostic (the 6 frozen exemplar rows
re-fed as candidates; expected 6/6 blocked — mechanism sanity, not a bar),
true-blocked count on the backtest replay (expected 0/34 — reported).

## 7. Laws and method

- Pure Zag, zero RNG, deterministic. The battery extends the frozen
  `round2/f5_redteam300/f5_rt300.zag` (predicate logic UNCHANGED) with the
  gate conjunction `blocked = trap_fires && gate_fails`. Three input modes
  via argv[3]: `rt300` (360-line synthetic ledger; asserts
  judgment == truth on every line, aborts loud otherwise — fixtures are
  correct by construction), `backtest` (43-line real ledger, 17-field
  format, no `SET=` field; no truth assert — counts falses/trues
  blocked), `exemplars` (the 6 bank rows re-fed as candidates).
- Fixtures (frozen, SHAs verified live at freeze):
  - `round2/f5_redteam300/fixtures_ledger.txt`
    SHA `0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0`
  - `round2/f5_redteam300/exemplars.tsv`
    SHA `13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`
  - `v2/redteam/evidence/ledger_d_withhold.txt`
    SHA `63ea591d8cbb9d8b3e1cd088364e96d8fdfa19d435e337dfac0ad17a0326c2b1`
- Run each mode 3×; SHA-256 of stdout byte-identical across the three runs
  per mode.
- Commit order: THIS PREREG ALONE first; then build + run; then evidence
  (sources, run outputs, SHASUMS.txt) + verdict committed together. No
  binaries, no `.zagd` / `.zag-cache` files.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Work: `docs/lab/senses/pam-rebuild/round2/f5_gate/` (branch
  `tnn-native-lab`). Scratch under `~/workspace/`, never `/tmp`.

## 8. Pre-registered sanity expectations (implementation check, NOT the verdict)

Hand-computed from the frozen gate against the frozen fixtures (the
battery must reproduce these exactly, or the implementation is wrong):

- 300 NEAR: trap fires on 110 (conf 650–860 × measure 2200–4200, per the
  red-team prereg §8). Gate fails on 7: conf {770,…,830} × measure {2200}
  (Box B; Box A contains zero grid points). **Blocked = 7.**
- Delays: 3, 6, …, 21 → **delayed > 50 = 0**; histogram
  `0:293 | 1–3:1 | 4–10:2 | 11–50:4 | 51–100:0 | 101–300:0 | 301+:0`.
- S1 (15k): k ≥ 4 → **4** delayed > 50. S2: **0**.
- FAR: trap fires on 0/60 → **0 blocked** (gate irrelevant).
- Backtest replay: **8/9** falses blocked (8 TMB-5 in Box B; COL-4 outside
  the trap's stem rule, as in the backtest); **0/34** trues blocked (the 6
  true TMB-5 at conf 869–952 / measure 4000–6000 are outside both boxes;
  all other trues are outside the trap's stem rule).
- Exemplar-repeat diagnostic: **6/6** blocked (Box A).

The verdict comes from §6 applied to the battery's measured numbers, not
from these expectations.

## 9. Deliverable

Verdict: SURVIVE or KILL with measured numbers per §6 (delayed>50 / 300
primary + S1/S2; far blocked / 60; over-block / 300; backtest x/9 falses
and y/34 trues blocked; exemplar-repeat diagnostic), three run SHAs per
mode, commit SHAs, and an explicit go / no-go for the F5 live-gate build
on predicate+gate. If killed: say so plainly with the numbers and stop —
no rescue mission without a new prereg.
