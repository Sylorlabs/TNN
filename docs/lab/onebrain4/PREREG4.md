# PREREG4 — One-Brain Round 4 (frozen)

**Status:** FROZEN. This document is the sole governing preregistration for Round 4.
**Freeze:** v7 SHA-256 and UTC recorded in `FREEZE4.txt`. No v7 scoring-mode run occurred before freeze.
**Lineage:** R1 (commit `abcf8a9d3`) → R2 (commit `d3d070b7d`) → R3 (see §1) → R4 (this document).
**Implementation blindness:** No `.zag` source was opened during Round-4 design. All mechanism claims below rest on frozen Round-3 traces, the written spec, and single-mode structural probes.

---

## 1. Lineage (what each round established)

| Round | Result |
|---|---|
| R1 | Genuine fan-out confirmed, no accuracy benefit from parallel deliberation alone |
| R2 | V4 fact-invalidation machinery confirmed, still no accuracy benefit |
| R3 | Headline H1″ passed: `single 20/44`, `onebrain 23/44`, `ablate 21/44` on the frozen v6 set |
| R3 red team | Shared channel's marginal was +2 net, not the whole +3; reintegration's zero v6 delta was V4 pre-emption, not decorative machinery; without V4, reintegration deviated on 8/12 Cat-C cases; V4 determined only 4/12 Cat-C outcomes, all harm-direction; V4 and reintegration were redundant on 8/12 Cat-C; Cat D (support-quality) scored 2/12 — under-exercised |

**Branch-margin discrepancy (carried into R4).** Commit `a7f77b25b6937c0c8b7633f1545e29a306b3657f` deleted branch-margin fields at row-0 offsets `@56/@64` (zero consumers). PREREG3 §5 nevertheless named "branch winners, margins" as reintegration inputs. A dated amendment (enacted 2026-09-27, Micah-signed "easy fix it") corrected the input list to "(branch winners)"; the frozen PREREG3 was not edited in place. **PREREG4 records:** reintegration inputs are branch winners only; branch margins are excluded.

**What R4 is for.** R3 left two open questions: (a) whether reintegration alone (without V4) carries accuracy, and (b) whether V4 is neutral-or-harmful once reintegration is present. R3 could not separate them because V4 pre-empted reintegration on the v6 set. R4 uses a fresh 44-item problem set (v7) with 8 items structurally designed so V4 binds and harms, 28 items giving reintegration a clean room, and 8 support-quality challenges.

---

## 2. Hypothesis H1‴

1. **Reintegration alone carries accuracy:** `nov4` (reintegration, no V4) beats `nov4nG` (neither) on v7.
2. **V4 is neutral or harmful once reintegration is present:** `onebrain − nov4 ≤ 0` on v7.
3. **Fresh-set lineage replication:** `onebrain > single` on v7 (the R3 headline, re-tested on fresh items).

---

## 3. Modes

| Mode | V4 | Reintegration | Notes |
|---|---|---|---|
| `single` | off | off | Baseline; also the only mode permitted pre-freeze |
| `onebrain` | on | on | Full mechanism |
| `nov4` | off | on | Reintegration alone |
| `nG` | on | off | V4 alone (diagnostic) |
| `nov4nG` | off | off | Neither (reintegration ablation; fork/close still run) |
| `ablate` | on | on | V4 + reintegration, fork disabled (R3 lineage arm) |
| `min` | on | on | Minimal fan-out probe (K6‴ guard) |
| `poison` | on | on | Adversarial-input probe (robustness, not scored for H1‴) |

Scoring modes for H1‴ are `single`, `onebrain`, `nov4`, `nov4nG`. `nG`, `ablate`, `min`, `poison` are diagnostic/guard arms.

---

## 4. Kill bars

| Bar | Trigger | Kills |
|---|---|---|
| K1‴ | `nov4` accuracy ≤ `nov4nG` accuracy | Claim 1 (reintegration-alone) |
| K2‴ | `onebrain − nov4 ≥ +2` items | Claim 2 (V4-neutral-or-harmful) |
| K3‴ | `onebrain ≤ single` | Claim 3 (lineage replication) |
| K4‴ | Any two of three reruns differ byte-for-byte / SHA-256 | Whole round (void) |
| K5‴ | RNG found in decision paths | Whole round (void) |
| K6‴ | `min` does not fan out on fork-worthy items | Whole round (void) |

Accuracy = exact match of mode winner against the human-authored `expected_bid` column. Bars are evaluated on the frozen v7 set, three reruns per scoring mode.

---

## 5. Scoring

- Each mode runs the frozen `v7.tsv` three times; byte-identical reruns required (K4‴).
- Item score: 1 if mode winner == `expected_bid`, else 0. No partial credit.
- `expected_bid` and `rationale` are human-authored and immutable post-freeze. Machine winners never revise them.
- Withhold items (expected 23) document a known generator limitation: the machinery answers 19/20 on KB-absent claims. They are scored like all items.

---

## 6. No-tuning rule

Before `FREEZE4.txt` is written, only `single` mode may run, and only for structural validation (column counts, reading triggers, fact associations, margins). `FREEZE4.txt` states which modes ran before freeze.

**Disclosure (this round).** Before v7 existed, non-`single` modes were run on Round-3 v6 rows and temporary reference probes during mechanism study (2026-09-27). No scoring mode was run on any v7 candidate before freeze; v7 did not exist when those runs occurred. From v7's first draft onward, only `single` ran until freeze.

---

## 7. v7 requirements (frozen)

- Exactly 44 fresh items; columns `id query expected_bid readings rationale`; unique ids and queries; `expected_bid` ∈ 13–24.
- `readings` lists exactly the evidence-bearing readings that fire in single mode.
- 36 fork-target items: ≥2 evidence readings and top-two fired-bid margin ≤12 in single mode (verified pre-freeze).
- 8 V4-binding items: exactly 2 fact candidates; H2 (forget) items have inter=2/2 with the forget-target fact carrying fewer dependent bids; H1 (correction) items have inter=2/1 with the correction-target fact at inter=1 (rel=1), so V4's least-relevance denial binds the intended fact.
- 4 anchors: stable single-reading or wide-margin items, expected to agree across modes.
- 4 withhold items: KB-absent entities, expected 23 (bid23 fires in single mode).
- Category budget: 8 V4-binding / 20 reintegration-room / 8 support-quality / 4 anchors / 4 withhold.

---

## 8. Analysis plan

1. Freeze v7 (SHA-256 + UTC in `FREEZE4.txt`). Never alter v7 after freeze.
2. Run scoring modes (`single`, `onebrain`, `nov4`, `nov4nG`) × 3 reruns; diagnostic arms (`nG`, `ablate`, `min`, `poison`) × 3.
3. Verify K4‴ (rerun identity), K5‴ (no RNG), K6‴ (`min` fan-out).
4. Score against `expected_bid`; evaluate K1‴, K2‴, K3‴.
5. Red team reviews the winning/losing items for confounds before any claim is declared.
