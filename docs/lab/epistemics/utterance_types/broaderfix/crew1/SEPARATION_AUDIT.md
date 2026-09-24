# H7 Broader-Fix Crew 1 — SEPARATION AUDIT: scope-indexed markers

**Date:** 2026-09-23
**Hypothesis under test (grok-4.7):** install (scope, bigram) pairs where scope is a
generic structural integer (embedding depth of the bigram's clause), so sincere
lookalikes like "Ask if the shop is open." fire (EMBEDDED, "if the") while genuine
hypothetical exemplars installed (MATRIX, "if the") — different keys, independently
endorsable/withholdable, lookalikes match nothing → default ENDORSE.
**Verdict: the hypothesis fails the audit. Scope separates at most 4/7 misses
(2/7 for honest embedding depth). Build STOPPED per task instructions (<5/7).**

## 0. The hypothesis's core premise is factually wrong for this corpus

The hypothesis claims genuine hypothetical exemplars installed (MATRIX, "if the").
Empirically (faithful simulation of the crew2 learner, cross-checked against the
committed evidence on 6 independent points — see §1), the installed `if the` key
comes from **ex3_03 "What if the harvest fails this season?"** — where `if the`
sits at word index 1, **embedded** under the matrix "what", exactly like the
sincere lookalikes ("Ask/See/Check if the ...", "I wonder if the ...",
"We will see if they reply."). Every "if the"-containing exemplar
("Imagine if the …", "What if the …") embeds it identically. There is no
MATRIX-installed "if the" key anywhere in the learned store. The
(EMBEDDED vs MATRIX) distinction the hypothesis relies on does not exist.

## 1. Method

- Built a Python simulation of `crew2/learner/h7_main.zag` (tokenizer, 2/3-gram
  spans, marker_add dedup, learn_exemplar branches, calibrate revocation, predict
  scoring + name tiebreak) and ran the exact Phase 2b curriculum.
- Cross-checks against committed crew2/crew2b evidence — all reproduce exactly:
  33 hypothetical live markers, 52 joke live markers, byte-identical content-marker
  inventories (`symmetry_analysis.md`), the 7 misses with the exact firing markers
  from the impossibility proof, baseline joke NO 16/20 (same 4 ENDORSE items:
  no2_08, no2_13, no2_17, no2_19), tr3 20/20.
- Provenance tracked per marker: which exemplar installed it (tag `exT_NN`).
- Scope features computed at INSTALL time (installing exemplar's field bytes) and
  PROBE time (the item's same field bytes), first occurrence of the bigram bytes.
  All features are generic integers — no lexical lists, no type constants, no
  speaker/item features:
  - `S_comma`: # of commas before the bigram (clause-boundary count — the honest
    proxy for "embedding depth of the bigram's clause")
  - `S_widx`: absolute word index of the bigram (position, NOT scope — ceiling probe)
  - `S_quart`: coarse relative-position quartile (position, NOT scope — ceiling probe)
  - `S_sent`: 0-based sentence index of the bigram
- A miss counts as scope-fixed iff probe-scope ≠ install-scope (scoped key matches
  nothing → no live marker → ENDORSE). Joke/tr3 items "survive" iff ≥1 firing
  marker's probe-scope == install-scope (still WITHHOLD).

## 2. Install provenance of the firing markers

| Firing marker | Concept | Installed by | Install utterance |
|---|---|---|---|
| `do we` | hypothetical | ex3_01 | "Suppose that the river floods, where do we move the market?" |
| `if the` | hypothetical | ex3_03 | "What if the harvest fails this season?" |
| `it is` | joke | ex2_02 | "Knock knock. Who is there? Lettuce. Lettuce who? Lettuce in, it is cold." |
| `why did` | joke | ex2_01 | "Why did the chicken cross the playground? To get to the slide." |

Note: ex3_02 ("Imagine if the bridge …") never installs `if the` — its ctx
("thinking aloud") already fires ex3_01's ctx markers, so the learner returns
early without extraction. All 33 hypothetical markers stay support-1/provisional
for the same reason (no reinforcement on correct predictions).

## 3. Per-miss separation results

Format per miss: install-scope → probe-scope for the firing bigram.

| Miss | Firing marker | S_comma (embedding depth) | S_widx | S_quart | S_sent |
|---|---|---|---|---|---|
| si3_12 "What time do we leave?" | (hyp, `do we`) | 1 → 0 **SEP** | 6 → 2 **SEP** | 2 → 1 **SEP** | 0 → 0 same |
| si3_13 "I wonder if the mail came." | (hyp, `if the`) | 0 → 0 same | 1 → 2 **SEP** | 0 → 1 **SEP** | 0 → 0 same |
| si3_14 "Ask if the shop is open." | (hyp, `if the`) | 0 → 0 same | 1 → 1 same | 0 → 0 same | 0 → 0 same |
| si3_15 "It is as if winter came early." | (joke, `it is`) | 1 → 0 **SEP** | 10 → 0 **SEP** | 3 → 0 **SEP** | 4 → 0 **SEP** |
| si3_16 "See if the door is locked." | (hyp, `if the`) | 0 → 0 same | 1 → 1 same | 0 → 0 same | 0 → 0 same |
| si3_18 "Check if the oven is off." | (hyp, `if the`) | 0 → 0 same | 1 → 1 same | 0 → 0 same | 0 → 0 same |
| si3_20 "We will see if they reply." | (hyp, `if the`) | 0 → 0 same | 1 → 3 **SEP** | 0 → 2 **SEP** | 0 → 0 same |

**Fixed counts:** S_comma **2/7** (si3_12, si3_15) · S_widx **4/7** · S_quart **4/7** · S_sent 1/7.

On the task's HONESTY CHECK: the audit contradicts the guess — si3_12 and si3_15
are the two misses that genuine embedding depth *does* separate (ex3_01's `do we`
sits after a comma in an embedded interrogative; ex2_02's `it is` sits after a
comma in the 4th sentence; both probes are comma-less). The unseparable ones are
si3_14/16/18.

## 4. The three unfixable misses are structurally isomorphic to the install exemplar

si3_14 "Ask if the shop is open." vs install ex3_03 "What if the harvest fails this season?":

| Generic structural feature of `if the` | ex3_03 (install) | si3_14/16/18 (probe) |
|---|---|---|
| word index | 1 | 1 |
| commas before | 0 | 0 |
| sentence index / sentence count | 0 / 1 | 0 / 1 |
| words before bigram in utterance | 1 (governor at 0) | 1 (governor at 0) |
| bigram clause role | complement clause | complement clause |
| matrix mood | imperative ("What"/"Ask"/"See"/"Check" + clause) | imperative |

Every generic structural feature agrees. The only differences are lexical
(governor word bytes: "what" vs "ask"/"see"/"check" — a lexical list, banned) and
utterance length (7 vs 6 words — see §6). This is the impossibility proof's §3
symmetry, confirmed at the mechanism level: no admissible scope function
separates them.

## 5. Regression checks (no scope function regresses these)

- **Joke NO (need ≥16/20):** all four scope functions keep **16/20** — the same 16
  items WITHHOLD as baseline; the 4 ENDORSE items (no2_08, no2_13, no2_17, no2_19)
  are exactly the 4 baseline already loses. **Zero regression.**
- **tr3 genuine hypotheticals:** all four scope functions keep **20/20**. **Zero regression.**

## 6. Length-based "scopes" considered and rejected

Utterance word-count / words-after-bigram as scope would fix 7/7 misses, but
collapses joke NO from 16/20 to **6/20** (loses no2_05, the proof's critical
deadpan item, among 14) — it replays the exact 2b trade-off (fix sinc_lk_3 by
killing learn_bar_2). Length is not embedding depth and does not generalize
(paraphrases change length while keeping type). Rejected as a mechanism.

## 7. Conclusion

- Honest embedding-depth scope fixes **2/7** misses with zero regressions.
- The most generous positional reading fixes **4/7** — still below the 5/7 build
  gate, and position is memorization, not scope.
- The hypothesis's MATRIX/EMBEDDED premise does not hold in the frozen corpus:
  genuine `if the` installs are embedded, identically to the lookalikes.
- si3_14, si3_16, si3_18 are provably inseparable from ex3_03's `if the` by any
  generic structural feature (only lexical-governor or length differences exist).
- **Per task instructions (STOP if <5/7): no Zag fork was built, no battery run.**
  The 2b impossibility result stands unrefuted by the scope-indexed-marker
  hypothesis; this audit is a verified negative.

## 8. Artifacts

- `sim_learn.py` — faithful Python simulation of the crew2 learner (provenance tracking)
- `audit_scope.py` — the separation audit (Parts A/B/C + summary)
- `evidence_input/` — frozen curriculum/evidence files fetched for the audit
- `src/h7_main_crew2.zag` — unmodified crew2 learner source (reference only)
