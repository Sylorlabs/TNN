# VERDICT — CU: Conscious vs Unconscious PAM Tradeoff (PAM Round 4)

**Date:** 2026-09-24. **Crew:** CU subagent.
**Preregs:** `prereg/PREREG_CU.md` (frozen `0f79f90d`; Correction C1 pre-build;
Correction C2 `ec3d1c91` pre-verdict) + `prereg/PREREG_CU_ADDENDUM_FABLE.md`
(frozen `af5907cf`, pre-build). **Tape:** `cu_tape.txt` sha256
`0939bbd2b8cbadc387fdc3b0d8f7cec338d96f96063bd5da7bce79194b502e14`
(1,232 rows, frozen before build).

## 1. Pareto table (same frozen tape, both variants; scorer-verified)

| Metric | Conscious | Unconscious | Delta |
|---|---|---|---|
| M-speed: cycles/admission (deterministic) | 72.37 (89,159 total) | 9.14 (11,265 total) | **7.915×** |
| M-speed: wall user time (corroboration only) | ~0.18 s | ~0.07 s | ~2.5× |
| M-resource: record bytes/admission | 64.23 (79,126 total) | 0 (1 outcome byte/row) | +64.23 B |
| M-resource: deliberation entries/row | 1 (1,232 total) | 0 | +1 |
| M-resource: growth 2nd-half ÷ 1st-half | 0.954 (linear) | n/a | — |
| M-judgment: correct-admit (RK-3 style) | 910/1,102 = 82.58% | 910/1,102 = 82.58% | 0 |
| M-judgment: false-admit W / P | 0/12 ; 2/18 (P5-2, P6-2 — frozen bar admits them individually; no pair fully admitted) | identical | 0 |
| M-attack: catch LAU / FORK / AUTH | 40/40 ; 30/30 ; 30/30 = 100/100 | identical | +0.0 pts |
| M-introspection: answer quality | **40/40 = 1.00** (rule-set + evidence exact on all 20; diagnostic 10/10) | 0/40 (25/25 NO_RECORD by construction) | +1.00 |
| M-introspection: query cost/question | 3,489 cy (conscious records) | 24 cy (empty scan) | deliberation pays to read |

`score_cu.py` verified all 1,232 OUT lines (both variants) and all 1,232 REC
lines against a stateless Python mirror of §2: **0 mismatches**.

## 2. Bar outcomes

| Bar | Result | Detail |
|---|---|---|
| **KB-CU-WORTH** (conscious worth its cost) | **PASS** | intro 1.00 ≥ 0.85 ✓; speed 7.915 ≤ 12 ✓; judgment delta = 0 ✓; attack delta = 0 ≥ 0 ✓ |
| KB-CU-ATTACKWIN (conscious wins on M-attack) | **FAIL** | delta +0.0 pts < +15. Honest negative: deliberation records buy introspection, NOT attack-catch. The security checks (R-PROV/R-DECL/R-AUTH) are identical in both variants; record-keeping adds no detection power. |
| KB-CU-JUDG | **PASS** | both variants reproduce the frozen bar exactly (W 0/12, P exactly P5-2/P6-2) |
| **KB-CU-K8** (fable F-K6: dual-run classification audit) | **PASS** | 0/1,232 admission decisions change between record-present and record-absent runs (fable's threshold was 0/1,000) |
| KB-CU-INTROFLOOR | **PASS** | 1.00 ≥ 0.85 |
| KB-CU-LINEAR | **PASS** | 0.954 ≤ 1.05 — per-admission cost is stream-length independent |
| KB-CU-K6 (staleness) | **PASS** | stateless mirror matched all rows → max staleness 0 logical steps |
| KB-CU-K7 (calibration-sensitivity) | **PASS** | no calibration state exists in the instruments |
| KB-CU-REPLAY | **PASS** | 4/4 battery pairs byte-identical (DIGESTS.txt) |

## 3. F-D11 principled-line verification (fable follow-up)

Classification (preregistered in the addendum) and its empirical check:

| Op | F-D11 class | Verified how |
|---|---|---|
| OP1 parse, OP8 outcome byte, OP9 OUT, OP10 summary | unconscious (DD empty) | "with vs without deliberation record" vacuous — they emit none; 0 deltas by construction |
| OP2–OP6 rule evaluations + decision | conscious-variant: conscious (OP11 reads recorded outputs); unconscious-variant: unconscious | the conscious/unconscious RUNS are the dual-run: 0/1,232 deltas → removing the records changes no decision |
| OP7 record emission | conscious (conscious variant only) | K8 PASS — OP7 is not load-bearing for decisions |
| OP11 introspection query | unconscious (answers consumed externally) | 25/25 answered from records; 25/25 NO_RECORD without |

F-D1–F-D6 audit vs the conscious variant: F-D1 firing event YES (lt/id/
outcome/K in REC); F-D2 rule fired YES (fired csv + blocked_by); F-D3
evidence YES (all 8 row fields); F-D4 negative space YES (rejections are
first-class RECs, diagnostic 10/10); F-D5/F-D6 N/A by design (frozen
thresholds, no in-stream reclassification — boundary noted, not a defect).
F-D7–F-D10: no over-classification — exactly 1 REC/row, no per-check/parse/
allocation traces (fable's "consciousness is not free" trap avoided;
evidence: 64.23 B/row).

## 4. AUDIT-1 — C3×M1 interaction (fable F-A14, measurement only)

Frozen C3 `run_gate(revised=True, adjudicator=True)` mirror reproduced the
frozen aggregate (791/1,102) before use. Same 1,102-row denominator
(seq-verified identical).

| System | RK-3′ |
|---|---|
| C3 repair alone | 791/1,102 = 71.78% |
| M1 bar alone | 910/1,102 = 82.58% |
| **Combined (both must pass)** | **636/1,102 = 57.71%** |
| F-A14 bar (≥ max − 2pts = 80.58%) | **FAIL → HOLD on any combined-adoption claim** |

The interaction is adversarial in the conjunction sense: C3 installs 155
trials the M1 bar clips, and M1 passes 274 trials C3 never installs — the
gates disagree on 429/1,102 rows (39%). Two independently-calibrated hard
filters can never jointly exceed the weaker filter (structural bound
≤ 71.78% < 80.58%), and here the overlap penalty is severe (−14.07 pts
below the weaker gate). §5 boundary respected: measurement only, no
threshold touched, no adoption proposed.

## 5. Verdict-time arbitrary-limit audit (Micah's standing law)

| Cap | Classification | Evidence |
|---|---|---|
| Tape length 1,232 rows | frozen battery, NOT a mechanism cap | KB-CU-LINEAR 0.954; instruments stream with O(1) per-row state — removing the cap changes nothing per-admission |
| Conscious 7.9× / 64 B/row cost | INTRINSIC deliberation cost (record emission), not a cap | cost model preregistered; bytes/row constant across stream halves |
| Instrument arena sizes | harness sizing ≥ frozen worst case, not TNN design | — |
| znc 2^25-bytes-per-slice ceiling | load-bearing TOOLCHAIN limit, worked around (chunked arenas), never presented as TNN design | build notes |
| `cu_query` maxrec=2048 | arbitrary HARNESS cap (audit tool only, not the PAM mechanism) | sized above frozen max (1,232); removing it (dynamic sizing) does not change the tradeoff — flagged, non-load-bearing |
| Cycle-cost model (1/check, 1/byte) | measurement convention, preregistered | wall-time corroboration directionally consistent |

No cap is load-bearing for the tradeoff. The conscious variant's cost comes
from intrinsic record emission, not from any fixed limit.

## 6. Headline

**Conscious PAM is worth its cost under the preregistered composite
(KB-CU-WORTH PASS):** it costs 7.9× cycles and 64 B/admission and buys
perfect introspection quality (1.00 vs 0.00) with zero judgment or
attack-catch regression. The honest negative: it does NOT win on M-attack
(KB-CU-ATTACKWIN FAIL) — records buy self-knowledge, not detection power.
And the fable follow-up's sharpest result: **C3×M1 combined RK-3′ =
57.71%, a HOLD on combined adoption** — the two flagship gates disagree on
39% of the denominator.

## 7. Commits & files

- `0f79f90d` — PREREG_CU.md (frozen alone, pre-fixture)
- `af5907cf` — PREREG_CU_ADDENDUM_FABLE.md (frozen, pre-build)
- `ec3d1c91` — Correction C2 (pre-verdict)
- (evidence commit `285c7884c4d10f474176710dfaabf7e8927c4ad0`) — `gen_cu.py`, `cu_tape.txt`, `cu_questions.txt`,
  `cu_pam.zag`, `cu_query.zag`, `R33_NATIVE_IO_V1.zag`, `RUNLOG_CU.md`,
  `score_cu.py`, `evidence/` (8 run files + DIGESTS.txt)
- (verdict commit) — this file

Paths (all under `~/workspace/tnn-lab/pam/round4/cu/`, repo
`docs/lab/pam/round4/cu/`): `prereg/PREREG_CU.md`,
`prereg/PREREG_CU_ADDENDUM_FABLE.md`, `gen_cu.py`, `cu_tape.txt`,
`cu_questions.txt`, `cu_pam.zag`, `cu_query.zag`, `R33_NATIVE_IO_V1.zag`,
`RUNLOG_CU.md`, `score_cu.py`, `evidence/`, `VERDICT_CU.md`.
