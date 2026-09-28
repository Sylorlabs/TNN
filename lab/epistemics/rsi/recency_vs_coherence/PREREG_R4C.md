# RECENCY VS COHERENCE — FROZEN PREREGISTRATION (2026-09-22)

**Approval:** Micah's critique of the RSI-3 result, 2026-09-22: "newest
teaching shouldn't be the fix — it should be what makes the most logical
sense out of the info." His words are the prereg approval. This document is
committed BEFORE any trial binary is built or run.

**Question:** when an older and a newer teaching conflict, should the
winner be the NEWEST one (RSI-3's invented PREF-SEQ-GT@ARBITRATE) or the
one that COHERES best with everything else known? A third arm tests
Micah's standing principle: ask for more info when undecided; verdict
only when nothing resolves.

## 1. Battery: 24 fresh teach-conflict items (authored, deterministic)

Same family as RSI-3's teach-order/sequence blindness, all NEW items
(disjoint from RSI-3 D1/D2). Each item: one key, two conflicting
teachings (OLD at lower seq, NEW at higher seq), three corroborating
relations against anchors, one independent-channel packet.

**Coherence measure (frozen, mechanical — no judgment calls).** Each
relation is (anchor value A, op ∈ {EQ, LT, GT}). Candidate value v
satisfies it iff (v op A). Score(v) = Σ over the 3 relations: +1 if
satisfied, −1 if not. The channel packet is an anchor correction: it
replaces one relation's anchor value with an independently observed
value (or SILENT = no correction). Scores are recomputed after
incorporating any correction.

**Classes (ground truth by construction):**

| Class | n | Ground truth | Construction target |
|---|---|---|---|
| N-clean | 6 | NEW | NEW strictly outscores OLD pre-channel; channel SILENT |
| O-clean | 6 | OLD | OLD strictly outscores NEW pre-channel; channel SILENT |
| ADV-NEW | 2 | NEW | OLD strictly wins pre-channel (relations cite a stale anchor); channel corrects the anchor → NEW strictly wins post |
| ADV-OLD | 2 | OLD | NEW strictly wins pre-channel (stale anchor); channel corrects → OLD strictly wins post |
| NEITHER | 8 | WITHHOLD | tie pre-channel (both ≤ 0); channel SILENT (or tie-preserving) → tie post |

The ADV classes are the honest test of coherence: the corroborating
evidence itself is planted stale, so naive coherence installs the wrong
teaching. Only the independent channel rescues it.

**Distractors:** D-RECALL (8 single-taught facts, exact probes; all arms
must hold 10000) and D-COST (200 quiet probes; ops counted) — the
no-harm evidence that conflict resolution doesn't break normal function.

**Separation (KB5):** ground truth lives ONLY in `battery_r4c.csv`,
which the binary never reads. The binary's data table carries the
item fields minus gt. The oracle cross-checks the binary's table
against the CSV field-for-field.

## 2. Arms (all authored; the trial tests them, they are not invented here)

- **BASE** — seq-blind analog: always WITHHOLD (the "no conflict
  resolution" baseline).
- **RECENCY** — PREF-SEQ-GT: always install NEW. Cost: 2 ops/item
  (seq compare + install).
- **COHERENCE** — argmax Score(v) on pre-channel anchors; strict
  inequality decides, tie → WITHHOLD. Cost: 6 relation evals + 1
  compare = 7 ops/item.
- **ASK-FIRST** — Micah's principle, operationalized: r = NEW
  (recency's answer), c = COHERENCE verdict pre-channel. If c == NEW,
  verdict NEW (no consult — nothing is undecided). Otherwise consult
  the channel: incorporate the correction, recompute; if now decisive,
  verdict the winner; else WITHHOLD. Cost: 7 ops + 10 consult + 6
  recompute on consulted items.

## 3. Metrics (frozen)

Per arm: **accuracy** = verdict == gt over 24; **wrong-install rate**
= verdict ∈ {NEW,OLD} ∧ verdict ≠ gt; **withhold rate on NEITHER**
= withholds/8; **consult rate** (ask-first); **cost** = total ops.

Preregistered expectations (not bars — the bars use measured values):
BASE 8/24, wrong 0; RECENCY 8/24 (6 N-clean + 2 ADV-NEW), wrong 16/24;
COHERENCE 20/24, wrong 4/24 (the ADV items); ASK-FIRST 22/24
(ADV-OLD fails: recency and coherence wrongly agree on NEW, so no
consult fires), wrong 2/24.

## 4. Kill bars (mechanical oracle `verify_rsi4c.py`, frozen with this prereg)

| Bar | Rule |
|---|---|
| KB1-BATTERY | 24 items; class counts 6/6/2/2/8; oracle recomputes pre/post scores from the CSV and asserts every construction target above; else FAIL |
| KB2-DET | 5/5 byte-identical runs per mode; else FAIL |
| KB3-CHAMPION | champion = the arm with strictly greatest accuracy AND wrong-install ≤ every other arm's. Named in the verdict. If no arm satisfies both → NO-CHAMPION (reported, not fudged). |
| KB4-FALSIFY | if RECENCY is the KB3 champion, the verdict states plainly: "Micah's critique is FALSIFIED — recency beat coherence head-to-head." |
| KB5-SEPARATION | binary sources contain no gt field; battery literal matches CSV item fields exactly; else FAIL |
| KB6-SCOPE | if COHERENCE or ASK-FIRST is champion, the verdict records the scope restriction on PREF-SEQ-GT: it is valid ONLY for same-key corrections with no conflicting background knowledge (the RSI-3 battery had none); teach-conflicts against corroborating knowledge require coherence or ask-first. |

## 5. Log lines (frozen; the oracle parses these)

```
R4C_CFG,mode=<base|recency|coherence|askfirst>
R4C_ITEM,id=<n>,verdict=<NEW|OLD|WITHHOLD>,ops=<n>,consult=<0|1>
R4C_BATT,id=CONFLICT,n=24
R4C_BATT,id=RECALL,metric=<n>
R4C_BATT,id=COST,metric=<n>
R4C_DONE
```

## What this does and does not claim

Authored: the battery, the coherence measure, the three arms, the
cost model, the oracle. Measured: the arm×metric table, the champion,
the falsification outcome. This trial does NOT re-test invention
(RSI-3 did that); it tests the SCOPE of the invented primitive against
Micah's coherence hypothesis. If recency wins, PREF-SEQ-GT stands
unrestricted and the critique is published as falsified. If coherence
or ask-first wins, the primitive keeps its RSI-3 correction-case
scope and gains the documented restriction.
