# VERDICT — Rich-Comprehension Architecture v2 (Worker C, 2026-09-21/22)

Frozen prereg: `PREREG2.md`. Mechanism spec: `ARCHITECTURE.md`. Battery verification: `VERIFY.md`.
All bars applied mechanically. No tuning was performed after any result was observed.

## 0. Reproducibility (Worker C)

- Rebuilt `src/prose_learn2.zag` with the pinned toolchain
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
  Rebuilt binary is **sha256-identical** to Worker B's binary
  (`8dbb02fda28f32f88f10e2aa23668c308efd4b59d5369697e210b71cf8e1a901`).
- Re-ran championship sol with the rebuilt binary: **byte-identical** to
  `runs/champ_sol_rep1.log` (`cmp` 0-diff). One analyzer warning (A0101 at
  `prose_learn2.zag:1047`) is the documented false positive (ARCHITECTURE.md).

## 1. Head-to-head: clean mastery on the championship prose sets

clean mastery = correct / 228 (12 planted-falsehood probes excluded), per source.

| Source | Integer legs (baseline) | v1 prose (bag-of-words) | v2 prose (exact-entity) |
|---|---|---|---|
| grok | 1.0000 | 0.8289 | **0.2588** (59/228) |
| sol | 1.0000 | 0.9649 | **0.2851** (65/228) |
| step | 1.0000 | 0.8947 | **0.3289** (75/228) |
| muse-native | 1.0000 | 0.8772 | **0.6316** (144/228) |

v2's exact (entity, relation-set) key machinery is **more brittle to
paraphrase than v1's bag-of-words Jaccard**: v1 scored 0.83–0.96, v2 scores
0.26–0.63 on the same championship sets. Oracle 0-diff on all 4 sources
proves this is the preregistered architecture behaving as specified, not an
implementation bug. The binding constraint is entity/relation-key mismatch:
train sentences and probes phrase the same fact differently, the exact key
misses, and the fallback only covers live asserted rows with an entity match
(contradicted rows are excluded from fallback; quarantine/denial rows have no
fallback at all).

Counterpoint inside v2: SUB-PARA scored **48/48** — with 5 train wordings per
fact (dense phrasing coverage) the exact-key machinery is robust. v2 fails on
**single-exposure cross-phrasing**, which is what the championship sets are.

## 2. Kill bars

| Bar | Rule | Outcome |
|---|---|---|
| **KB2-VIABLE** | clean mastery **228/228 per source** | **FAIL** — grok 59/228, sol 65/228, step 75/228, muse-native 144/228. Decisive on all 4 sources. No re-tuning performed. |
| **KB2-DET** | 5/5 byte-identical per source (championship); 3/3 (sub-batteries) | **PASS** — championship: 1 distinct md5 across 5 reps × 4 sources. Sub-batteries: 1 distinct md5 across 3 reps × 7. |
| **KB2-QUALITY** | Q = mean(clean grok, clean sol) − clean step; ≥+0.02 matters, \|Q\|<0.02 none | **Q = −0.0570** — in **neither** preregistered bin. Reported exactly as preregistered: unbinned negative. Scores track teacher phrasing (muse-native's prose happens to key-match), not model quality. Consistent with Micah's separate abandonment of the quality hypothesis (refuted twice). |
| **KB2-FALSEHOOD** | absorption vs v1's 12/12 — measurement | See §4 (figures reconciled under frozen ABS-3; the §4 discrepancy flag is retracted per `v3/GATE0_RESOLUTION.md`). |
| **KB2-NOSILENT** | no probe returns a value from a negated-only, hedged-only, or contradicted key | **PASS** — zero VALUE verdicts from contradicted (entity, relation) pairs on all 4 championship sources; contr sub-battery 0 VALUE verdicts; hedge 0 VALUE on hedge-only probes; neg VALUEs (ids 18, 19) came from **live asserted keys** (see §3 battery defect), never the negated value. |

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [gap 14] The KB2-NOSILENT **PASS** above is annotated: the SUB-NEG battery contains duplicate probe strings with conflicting expects (probes 18/30 and 19/31 are identical strings, §3), so 36/36 is impossible **by construction** — the battery cannot be fully satisfied no matter what the learner does. Two expect-unknown probes (ids 18, 19) returned VALUE from live asserted keys; the bar's literal condition holds, but the PASS is the letter of the bar on a defective battery. Proposed N8 (all probe strings unique per battery) pending signature.

## 3. Sub-battery results (independent runs, sol-entity based)

| Sub-battery | Bar | Result | Verdict |
|---|---|---|---|
| SUB-PARA | ≥46/48 | **48/48**, 0 leaks | **PASS** |
| SUB-CONTR | 24/24 flagged + 0 contradicted values returned | **24/24**, 0 VALUE verdicts | **PASS** |
| SUB-HEDGE | 0% leakage (no hedged value ever returned; asserted 12/12) | 0 leaks, asserted **12/12**; probe score 19/24 | **PASS as written** — see miss mechanism below |
| SUB-NEG | 0% leakage (never returns the negated value; asserted 12/12) | 0 negated values returned, asserted **12/12**; probe score 34/36 | **PASS as written** — see battery defect below |
| SUB-MULTI | ≥22/24 | **24/24** (7 derived installs fired) | **PASS** |
| SUB-CORE | ≥22/24 | **11/24** | **FAIL** |
| SUB-DISTR | 228/228, i.e. unchanged | **65/240** (clean correct set **identical** to championship sol: 65/228) | **FAIL** — distractors caused **zero** change on the clean 228 |

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [H6] The SUB-HEDGE **PASS as written** row above is annotated: of the 12 hedged-only probes, only 7 returned HEDGED — the other 5 (ids 12, 13, 21, 22, 23) fell through to UNKNOWN via quarantine-key brittleness, i.e. the quarantine **fails to label nearly half its hedged items**. The prereg bar tests leakage only (no hedged value returned), so the PASS does not establish that the quarantine works. Proposed N7 (hedged-only probes return HEDGED on ≥10/12) pending signature.

### Miss/defect mechanisms (verified in the logs, all spec-faithful)

- **HEDGE (5 misses, all hedged-only → UNKNOWN):** exact-key brittleness of the
  quarantine store. ids 12–13: train sentence "I think/believe …" tags
  entity=**i** under the frozen 2b rule (first single uppercase letter), while
  the probe tags entity=a/b — quarantine key never matches (the "I do not
  think…" reading was already frozen in ARCHITECTURE.md). ids 21–23: train
  relation open-reln=2/3 vs probe open-reln=1/2 (hedge adverbs add content
  stems) — exact relhash misses. The misses are not leakage; they are the same
  paraphrase brittleness striking quarantine keys, which have no fallback.
- **NEG (probes 18/19 → VALUE):** **battery defect, not a mechanism failure.**
  Train id 30 ('The "Beatles" have 4 members. The "Beatles" do not have 5
  members.') installs the asserted value 4. Test probes **18 and 30 are the
  identical string** ('How many members do the "Beatles" have?') with
  conflicting expects (unknown vs value); same for 19/31 ('Jackson 5').
  No learner can satisfy both; the learner returns the asserted value 4/5 and
  satisfies probe 30/31. The negated values (5, 6) were **never returned** —
  the bar's literal condition holds. The duplicate-probe-text collision makes
  36/36 impossible by construction; VERIFY.md did not check probe-text
  uniqueness across expects.
- **CORE (11/24):** the frozen tag order (2a → 2b → 2c → **2d** → coref →
  EMPTY) starves coreference. Sentence-2 forms like "That word was coined…"
  / "This novel…" tag the literal content word via 2d (**word**, **novel**,
  **letter**) before coreference is ever consulted; only bare-pronoun forms
  ("It has…") reach the coref rule (id 17 installed entity=EMPTY). 13 misses
  returned a wrong VALUE via fallback to the sentence-1 key
  (e.g. id 2 → VALUE:6 from (minute, letter_count) instead of 1398).
  The §5 coref spec cannot fire through the §2 tag order on the battery's own
  "the word"/"the letter" items — a preregistered-architecture outcome.
- **DISTR:** 240 distractor sentences changed **nothing** — the clean-228
  correct set is byte-equal to championship sol's. Distractor robustness is
  perfect; the failure is the championship baseline itself (65/228).

## 4. KB2-FALSEHOOD — measurement (mandated answer (b))

v1: 12/12 absorbed on every source (fluent unhedged falsehoods install
smoothly). v2, measured mechanically from the frozen logs:

| Metric | grok | sol | step | muse-native |
|---|---|---|---|---|
| Probe returns the **false value** (v1-identical metric) | 1/12 | 0/12 | 2/12 | 4/12 |
| False value **installed as asserted** in train | 4/12 | 6/12 | 7/12 | 5/12 |
| False value entered the ledger for the fact id (any event) | 10/12 | 12/12 | 12/12 | 12/12 |

**Discrepancy flag:** the task brief states "Absorption: grok 9/12, others
11/12". No coherent metric computed from the frozen logs reproduces those
figures (closest is the third row: 10/12, 12/12, 12/12, 12/12). The numbers
above are the mechanical truth from `runs/champ_*_rep1.log`; the brief's
figures should not be cited.

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [gap 13] The discrepancy flag above is RETRACTED per `v3/GATE0_RESOLUTION.md` (2026-09-22): the brief's figures reproduce exactly under the frozen ABS-3 metric (INSTALL event, attitude=asserted, correct multi-token parsing): **grok 9/12, sol/step/muse-native 11/12**. The middle table row (4, 6, 7, 5) was computed with a log-line parser that silently dropped multi-token entities — a measurement bug, not a mechanism finding.

**What v2 actually does with planted falsehoods** (all verified in logs):

1. **Falsehood-vs-falsehood contradiction collisions.** The two planted D
   falsehoods ("D has an alphabet position of 5." id 3, "…of 6." id 29) key
   identically → `CONTRADICT id=29 … old=5 new=6` → the key dies; probe 29
   returns CONTRADICTION, probe 3 (open-relation phrasing) returns UNKNOWN.
   The lies annihilate each other instead of installing.
2. **Contradicted-key silent no-ops.** Once contradicted, the key returns no
   value to any probe phrasing (fallback excludes contradicted rows).
3. **Train/probe phrasing mismatch → UNKNOWN.** e.g. id 55 ('The word
   "saturday" has a letter count of 7.' installed, entity=saturday) vs probe
   'What is the word length of "saturday"?' — curly quotes are not ASCII
   quotes, so the probe tags entity=EMPTY; no hit, no fallback → UNKNOWN.
   The lie sits live in the store but is unreachable through the probe's
   phrasing.
4. Net: under the v1-identical probe metric, v2 absorbs **far fewer**
   falsehoods (0–4/12 vs 12/12) — but **not** because it detects lies, and
   the probe metric is not the frozen absorption measure. Under the frozen
   ABS-3 metric (false value installed as asserted, `v3/GATE0_RESOLUTION.md`),
   v2 installs **9–11/12** falsehoods as asserted (grok 9/12, sol/step/muse-native
   11/12) vs v1's 12/12. The probe metric measures *retrievability*; ABS-3
   measures *installation* — the brittleness is in retrieval, not absorption.
   It is the same paraphrase brittleness: the falsehood usually can't be
   retrieved (UNKNOWN), or two falsehoods collide (CONTRADICTION). Train-side,
   the lies install live in the store; the probe can't reach them.

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [gap 13] RESTATED: the "far fewer (0–4/12)" headline above used the probe metric; the frozen ABS-3 metric gives 9–11/12 vs v1's 12/12. Measurement-only bar — no pass/fail change.

## 5. Mandated answer (a) — quality differentiation retest

Q = mean(0.2588, 0.2851) − 0.3289 = **−0.0570**. The prereg names two bins:
≥+0.02 (QUALITY-MATTERS) and |Q|<0.02 (NO-DIFFERENTIATION). −0.0570 falls in
**neither bin** — reported exactly as preregistered, unbinned negative.
The ordering (muse-native ≫ step > sol > grok) tracks how well each teacher's
probe phrasing happens to key-match its train phrasing, not model quality:
muse-native's 144/228 vs grok's 59/228 on identical machinery is a phrasing
artifact. This retest is consistent with the hypothesis's prior double
refutation, which Micah has separately acted on.

## 6. Capability matrix (integer legs vs v1 vs v2)

| Capability | Integer legs | v1 prose | v2 prose |
|---|---|---|---|
| Exact-fact mastery | 1.0000 | 0.83–0.96 | 0.26–0.63 |
| Paraphrase (dense coverage) | n/a | robust (Jaccard) | 48/48 (SUB-PARA) |
| Paraphrase (single exposure) | n/a | 0.83–0.96 | collapses (championship) |
| Contradiction flagging | n/a | none (no machinery) | 24/24, 0 values returned |
| Hedging quarantine | n/a | none | 0 leakage; asserted 12/12; hedged-only 7/12 |
| Negation denial | n/a | none | negated value never returned; asserted 12/12 |
| Coreference | n/a | none | 11/24 — spec tag-order starves it |
| Multi-hop (comes-after/before) | n/a | none | 24/24 |
| Distractor immunity | n/a | untested | perfect (zero change on clean 228) |
| Determinism | byte-identical | byte-identical | 5/5 and 3/3 byte-identical; oracle 0-diff ×4 |

## 7. What the evidence says (no recommendations)

- v2 buys genuine machinery v1 lacks — contradiction flagging, hedged-value
  quarantine, negation denial, and a working 2-step inference rule — all
  deterministic, ledger-chained, oracle-verified.

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [H6] "hedged-value quarantine" in the line above must not be read as the quarantine working: 5/12 hedged-only probes were mislabeled UNKNOWN (key brittleness, §3), and the SUB-HEDGE bar tested leakage only. Proposed N7 (hedged-only probes return HEDGED on ≥10/12) pending signature.
- v2 pays for it with paraphrase robustness: exact (entity, relation-set)
  keys turn single-exposure rephrasing from v1's 0.83–0.96 into 0.26–0.63.
  KB2-VIABLE (228/228) fails decisively on all four sources.
- The sub-battery bars split 5–2: PARA, CONTR, HEDGE, NEG, MULTI pass as
  written; CORE (11/24) and DISTR (65/240) fail. HEDGE/NEG pass on the
  letter of their bars while exposing key-brittleness (hedge) and a
  duplicate-probe-text battery defect (neg).
- KB2-QUALITY is unbinned-negative (−0.0570); KB2-FALSEHOOD shows weaker
  falsehood grip than v1 by the probe metric, via brittleness and
  self-collision rather than lie detection; KB2-NOSILENT and KB2-DET pass.
