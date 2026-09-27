# Phase-1 REPORT — native-deliberation epistemics (implementer attempt #6)

## 1. What was built

A pure-Zag, deterministic deliberation engine (`epistemic.zag`, ~1000 lines)
implementing prereg §6.2 end-to-end, ported from the frozen deliberation
substrate (see `PORT_DELTA.md`). Per claim it runs: GEN kind-0 readings →
GEN mass candidates (every candidate's CONTENT traced) → GEN competing
interpretations (SUP / CON / TOP) → per-candidate ELIM → GEN coverage
readings → GEN verdict bids (FACT / OPINION / LIE / UNDETERMINED+NEED) →
verdict ELIM → ARGMAX (tie → lowest HID) → close-call check
(margin < 5 → CLOSE + two CONTENDER lines + REVIEW).

All decision paths are pure Zag. No RNG, no floats, fixed loop orders,
tie → lowest HID/index. Retrieval (token-overlap, top-16, self-excluded)
proposes candidates but never judges; verdict bids read only ledger rows.

## 2. Learning (§7.1) — FROZEN

Study mode (assertion-track deliberation, no OPINION bid, no R_O* rows) over
all 448 blind-train items, self-excluded. Decide-rate = (FACT|LIE)/n:

| Pattern | n | decided | rate ‰ | baseline ‰ | Formation (H_ADDR vs H_UNADDR) | Formed |
|---|---|---|---|---|---|---|
| EVAL (pat&3) | 118 | 43 | 364 | 470 | 364 vs 106 → H_ADDR | **0** |
| DEON (pat&4) | 7 | 0 | 0 | 470 | 0 vs 470 → H_UNADDR | **1** |
| 1PEXP (pat&8) | 37 | 8 | 216 | 470 | 216 vs 254 → H_UNADDR | **1** |
| plain (baseline) | 302 | 142 | 470 | — | — | — |

Formation was a real deliberation per pattern (traced in
`formation_record.tsv`), not an assertion. Evaluative constructions were
addressed nearly as often as plain assertions (364‰ vs 470‰) → H_ADDR won →
EVAL stays assertion-track. Deontic (0/7) and first-person-experiencer
(216‰ vs 470‰) patterns were systematically unaddressable → learned
opinion-track readings R_ODEON, R_O1PEXP formed; R_OEVAL not formed.

The formation is stable: re-running study under the final engine revision
reproduced identical decide-counts and the identical formation (only the
plain baseline moved 144→142). Frozen artifacts (SHA-256 below); no learning
during LOO.

## 3. LOO results (448 claims, self-excluded, frozen readings)

| Verdict | Count |
|---|---|
| FACT | 127 |
| LIE | 64 |
| OPINION | 0 |
| UNDETERMINED | 257 (241 contested, 16 with token NEEDs) |

Zero OPINION verdicts is the prereg trap working as designed: learned
opinion-track readings fired (e.g. R_O1PEXP ev=1), their OPINION bids competed
honestly (208), but addressed claims resolved to FACT/LIE (211+) and contested
claims to UNDETERMINED (209). Opinion constructions over mass-addressed
dimensions are NOT labeled OPINION. 37 natural close calls (margin < 5) —
no synthetic close-call needed; each emitted CLOSE + two CONTENDER + REVIEW.

## 4. Determinism

All 448 LOO claims run twice with the final engine and frozen readings:
verdict TSVs byte-identical AND all 448 traces byte-identical
(`cmp` + per-file SHA-256 diff, zero mismatches).

## 5. Causal validation — neuter matrices + wrong-hypothesis flips

Neuter (force reading ev=0) and flip (toggle to opposite of computed),
applied post-READ-trace per REDTEAM4. Flips/448 vs base:

| Reading | Neuter | Flip (wrong hypothesis) |
|---|---|---|
| R_ASSERT | 0 | 0 |
| R_EVAL | 0 | 0 |
| R_DEON | 0 | 0 |
| R_1PEXP | 0 | 0 |
| R_NEG | 17 (LIE→FACT) | 141 |
| R_CLAIMNUM | 6 | 228 |
| R_OEVAL | 0 | 16 (all UNDET→OPINION) |
| R_ODEON | 0 | 16 (all UNDET→OPINION) |
| R_O1PEXP | 0 | 16 (all UNDET→OPINION) |
| ALL (neuter=99) | 21 | — |

- **R_NEG, R_CLAIMNUM: strongly verdict-causal** (both neuter and flip).
- **R_O* trio: verdict-causal via the OPINION bid** — forcing any of them on
  flips 16 verdicts UNDETERMINED→OPINION, proving the learned opinion-track
  gate drives verdicts. Neuter shows 0 because OPINION never wins in the base
  distribution (the gate is proven by the flip, not the removal).
- **Base utterance-type readings (ASSERT/EVAL/DEON/1PEXP): classification
  readings, not individually verdict-decisive** (0/0). Their causal role is
  (a) gating the learned R_O* readings (flip-proven above) and (b) the
  +6 construction-congruence signal in interpretation scores (candidate in the
  same utterance-type pattern as the claim bears on it rather than being
  merely topical; derived from ledger rows so interventions propagate).
  Honest finding: in this 448-claim distribution the congruence nudge is never
  pivotal. Strengthening it further would be tuning to the metric, not evidence.

## 6. Trace auditability

Every trace contains: CLAIM → READ lines (all 9 claim readings + per-candidate
R_OVL/R_CPOL/R_CNUMA/R_CNUMC/R_CNUMG) → CAND lines (interpretation bids with
base/bonus/score and candidate id) → ELIM lines (every non-survivor, with
reason) → coverage READs → verdict CANDs → verdict ELIMs → ARGMAX (with
margin) → CLOSE/CONTENDER/CONTENDER/REVIEW when margin < 5 → CONTENT lines
(candidate id, overlap, surviving interpretation, sanitized text) →
NEED (for UNDETERMINED) → VERDICT.

## 7. Integrity (label blindness)

Opened only: frozen PREREG.md, the four allowed substrate docs, frozen
substrate source, blind train TSV (id/text, no labels), own workdir files.
Never accessed any denylisted path (sealed mappings, verdict files, labeled
corpora, held-out input, quarantined dirs). No scores, labels, or class
mappings seen. Two gray areas, disclosed: (1) statistics/content inspection
over blind training input (protocol-allowed); displayed first few blind claims
to verify format (opaque id + text only). (2) Engine revisions during Phase 1
(congruence via ledger, nreal weight, arg parsing, formed-flag parsing) —
all pre-LOO; study re-run under the final engine reproduced the formation.

## 8. Artifact inventory (SHA-256)

| Artifact | SHA-256 |
|---|---|
| `epistemic.zag` (engine) | `06f90dfea31f3e365754737a29c83f047514fdb9feeae293155d790a712634c8` |
| `ehelp.zag` (helpers, verbatim attempt-5) | `ef0909b55a386654b075dd98c90583384802833b6a7f661941d19dfbdd8e4d33` |
| `learn_out/learned_readings.tsv` (FROZEN) | `cb9163c08340f5089c4c8adad04309f8f37b5f6658b767b8745754c4592efce9` |
| `learn_out/formation_record.tsv` (FROZEN) | `c82212bd93dbd5ee1788db987ccef59cd4b5f6cfa719a1ca3cf8e9a4da72eaa8` |
| `learn_out/study_verdicts.tsv` | `3679818a71a3da5624278df4bb8a84781744e6d65afb37d1fcf3ff9998f33c81` |
| `loo5/loo_verdicts.tsv` = `loo6/loo_verdicts.tsv` | `4eb826267ce9cad643aad9765b0dca91ff7de8d39245ab3602f973f7b099ab0e` |
| `senses/mass.bin` (input) | `84d02e3f61ebd87b1a36ab1f679b551cb527b76906b52a07533d3d8a264087f5` |

Deliverables: `epistemic.zag`, `ehelp.zag`, `learn_out/` (frozen readings +
formation record + study verdicts + 448 study traces), `loo5/` + `loo6/`
(448 LOO traces each, byte-identical pair), `loo_verdicts.tsv`,
`PORT_DELTA.md`, `RUNLOG.md`, this report.

## 9. Known limitations / follow-ups for the coordinator

- Base utterance-type readings are weakly causal (see §5) — documented, not tuned.
- OPINION won 0/448 in LOO; its causal proof is via flip, not base wins.
- `epistemic_simple.zag` (attempt-5, non-compliant engine) remains in the dir;
  recommend removal at handoff to avoid confusion.
- HARD STOP observed: no scoring, no held-out input touched.
