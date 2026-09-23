# HTD-1 DEBATE — Sparse Activation / Efficient Routing

**Track:** eff-sparse (slice: sparse activation / efficient routing)
**Phase:** DEBATE only — hypotheses, mechanisms, kill bars. No build, no code.
**Date:** 2026-09-20
**Status:** PROPOSED — awaiting coordinator merge into the HTD-1 prereg.

## 0. Framing

Micah's question: "Human brains took the free lunch" — ~20W, sparse activation, only
relevant circuits fire. TNN should do the same: efficient routing that wakes only the
relevant parts per deliberation, not everything awake all the time. The question for
this track: **how far can deliberate efficiency go before the gate costs more than the
thinking it saves, or before sparsity starts losing answers?**

Standing laws apply to every hypothesis below: pure Zag, zero randomness in any
decision path, byte-identical reruns (same input + same logged state → byte-identical
output), kill bars are binding, every fork tested head-to-head, results reported as
they resolve — including honest FAILs.

## 1. Shared operational definitions

These definitions are fixed across all hypotheses so the head-to-head is fair.

- **Partition:** a deliberately-managed memory context (per the 16/16 context-switch
  result). The store is divided into partitions; each holds many chunks.
- **Chunk:** a fixed-size content unit. Ingest chunker: 4 KB, line-aligned,
  deterministic. (pg100 ≈ 1,400 chunks; sqlite3.c ≈ 2,400 chunks.)
- **Dormant:** a partition/chunk that is not scanned, not loaded into any working
  set, and touched by zero deliberation ops during a deliberation.
- **Woken:** a partition/chunk loaded into the deliberation's working buffer and
  eligible for deliberation ops. Waking is a deliberate act: the ledger records
  `(deliberation-id, partition-id, chunk-ids, gate-evidence)` where gate-evidence is
  the exact scores / threshold / citations that caused the wake. Unwoken partitions
  never get to object, so the wake record is the audit trail of what was *not*
  thought about.
- **Wake set:** the exact set woken for one deliberation — a deterministic function
  of (query, logged state). No randomness, no ties broken by chance; tie-breaks are
  by (score desc, partition-id asc) or equivalent frozen rule.
- **Relevance gate:** the mechanism that maps (query, state) → wake set. Its cost is
  counted in native ops like everything else.

## 2. Shared proxy harness — CORPUS-QA-60

All hypotheses run on one frozen harness so numbers are comparable.

- **Corpora (read in place, never copied):** `~/workspace/tnn-lab/corpora/pg100.txt`
  (5.6 MB Shakespeare), `~/workspace/tnn-lab/corpora/sqlite3.c` (9.5 MB SQLite
  amalgamation v3.53.4).
- **Partition map (frozen at prereg):** pg100 partitioned by work (play/poem header
  markers, deterministic splitter, ~40 partitions); sqlite3.c partitioned by
  amalgamation file-boundary markers (verified at ingest, ~60 partitions). The map
  is committed; builders do not re-partition mid-trial.
- **Question set (frozen at prereg):** 60 questions, 30 per corpus, each with
  deterministic ground truth (the exact chunk(s) containing the answer).
  Lookup examples: "In which play does the line 'To be, or not to be' appear?"
  (Hamlet chunk); "Which amalgamation file defines `sqlite3BtreeOpen`?"; "Where is
  `SQLITE_CORRUPT` defined?" Discovery examples (answer not named by the question):
  "Name a play in which no character dies on stage"; "Which internal APIs are called
  from more than three amalgamation files?" The set mixes both classes on purpose —
  the discovery subset is where sparse routing is most likely to fail honestly.
- **One deliberation** = answer one frozen question. The system may wake
  partitions/chunks per its hypothesis, deliberate, and must return an answer plus
  the cited chunks. Correctness = deterministic judge against frozen ground truth.
- **Metrics (per deliberation and aggregate):** native op count (the ledger-visible
  deterministic counter — primary metric), wall-clock ns (secondary; the VM is
  noisy), wake-set size / wake fraction, answer correctness, miss events.
- **Miss:** a question *misses* if any ground-truth chunk is not in the wake set.
  (For citation-only E-SP6: misses if no ground-truth chunk was cited-and-woken.)
- **Baselines:** B0 = always-awake (every partition deliberated every time — the
  "leave everything awake" regime Micah wants beaten). Negative controls:
  B-wake-none (wake nothing; must score ≈ 0 — proves the task is nontrivial) and
  B-inverted (wake the *lowest*-scoring partitions; must underperform every real
  gate by ≥ 20 points of net savings — proves the gate's signal is real, not decor).
- **Scale legs:** S1 = full corpora / 60 questions. S10 = 10× corpus (10 tagged
  copies concatenated deterministically — partitions stay distinct, ~900
  partitions) / same 60 questions, ground truth = union across copies. S10 exists
  because the program already measured a real scaling tax (memory free-slot
  scanning went O(n²) at 10×) — no sparsity proposal gets to reintroduce a
  superlinear scan through the back door. (Workdirs live under `~/workspace`, never
  `/tmp` — the 512 MB tmpfs must not host the 10× runs.)
- **Determinism protocol:** every reported number is the mean of 3 reruns from the
  same logged state; any non-byte-identical rerun is a hard failure (SH-DET).

## 3. Shared kill bars (apply to every hypothesis)

- **SH-OVERHEAD:** FAIL if (gate + dispatch + commit ops) ≥ **25%** of the gross ops
  saved vs B0. Net savings must be ≥ 75% of gross — the gate must not eat its own
  lunch.
- **SH-RECALL:** FAIL if question-level miss rate **> 5%** (more than 3 of 60).
  Sparsity must not lose answers.
- **SH-NET:** FAIL if total native ops ≥ **90%** of B0 at the same scale leg.
  Must net-save ≥ 10% or the machinery isn't worth it.
- **SH-SCALE:** FAIL if S10 per-deliberation gate overhead > **12×** the S1
  per-deliberation gate overhead (10× linear growth + 20% headroom). Directly
  targets the known O(n²)-style scaling tax: superlinear gate cost dies here.
- **SH-DET:** FAIL (hard gate, not a bar) on any non-byte-identical rerun from the
  same input + logged state. Standing law.

Per-hypothesis bars below are *additional*; the shared bars always apply.

---

## 4. Hypotheses

### E-SP1 — Per-deliberation selective wake (Micah's core hypothesis)

**Mechanism sketch.** One deliberate relevance gate per deliberation. At
consolidation time each partition builds a **signature**: its top-64 token hashes
ranked by (frequency desc, hash asc) — deterministic, revisable only by deliberate
revision. At deliberation time the gate hashes the query terms, scores each
partition by `|query-hashes ∩ signature|`, and wakes partitions with score ≥ τ
(τ from a preregistered grid; ties broken by partition-id asc). Woken = partition's
chunks loaded into the working buffer and deliberated over; dormant = skipped
entirely, zero ops. The ledger records the wake set with per-partition scores and
τ, so a miss is auditable after the fact. Gate cost is O(partitions × 64) integer
compares — cheap, but nonzero, and that is exactly what SH-OVERHEAD polices.

**Falsifiable predictions.** (a) Mean wake fraction ≤ 30% at S1 with miss ≤ 5% —
selectivity without blindness. (b) Net ops scale ~linearly in partitions woken,
not partitions existing. (c) **Honest failure mode:** τ has no operating point —
either the gate wakes too much (overhead eats savings) or too little (discovery
questions miss), particularly on the discovery subset where the query doesn't name
the answer's vocabulary.

**Kill bars.** K1: FAIL if mean wake fraction > **30%** of partitions at S1 (not
sparse, just awake with extra steps). K2: FAIL if **no τ** in the preregistered
grid achieves miss ≤ 5% AND net-save ≥ 10% simultaneously (the gate has no
operating point — the honest-failure mode made numeric).

**Proxy task + metric.** CORPUS-QA-60 vs B0 at S1 and S10. Primary: native ops
ratio vs B0; secondary: miss rate, wake fraction, wall-clock ratio. τ grid frozen
in prereg; the reported number uses the best-τ *by a frozen selection rule*
(highest net savings subject to miss ≤ 5%), never post-hoc τ-picking.

**Head-to-head required.** E-SP1 vs B0 (the core claim); E-SP1 vs E-SP2 (does the
pre-filter earn its keep?); E-SP1 vs E-SP4 at S1 and S10 (flat vs hierarchical);
E-SP1 vs E-SP3 on the cross-partition question subset.

---

### E-SP2 — Two-tier routing: cheap pre-filter, then deliberate deep wake

**Mechanism sketch.** Tier 1 is a *dumb, zero-false-negative* pre-filter: each
partition carries a 256-bit mask (`token-hash mod 256` OR-ed over its chunks,
built at consolidation). Tier 1 passes a partition iff
`(queryMask & partMask) == queryMask` — 4 u64 ANDs per partition. Any chunk
containing all query tokens necessarily sets those bits, so a tier-1 rejection is
provably safe: **zero false negatives by construction**, and any observed FN is a
construction bug, not a tuning issue. Tier 2 is the deliberate deep gate (the
E-SP1 signature gate, possibly with a finer signature) and runs *only* on tier-1
passers. "Woken" means passing both tiers; tier-1-only partitions are counted as
dormant (their 4 ANDs are gate cost, nothing more).

**Falsifiable predictions.** (a) Tier-1 ops ≤ 2% of B0 ops while eliminating ≥ 70%
of partitions before the deep gate runs. (b) Net savings beat E-SP1 at S10, where
the deep gate's per-partition cost hurts most. (c) **Honest failure mode:** the
pre-filter is too coarse on small vocabularies (pg100's Early Modern English
repeats the same tokens everywhere) — tier-1 passes nearly everything, the deep
gate runs anyway, and the extra tier is pure overhead.

**Kill bars.** K1: FAIL on **any** tier-1 false negative (a ground-truth chunk's
partition rejected by tier 1) — Y = 0%, construction guarantee. K2: FAIL if the
deep gate runs on > **20%** of partitions on average at S1 (tier 1 isn't
filtering). K3: FAIL if tier-1 ops > **2%** of B0 ops (the "cheap" tier isn't).

**Proxy task + metric.** CORPUS-QA-60 vs B0 and vs E-SP1, S1 and S10. Primary:
net-savings delta vs E-SP1 — E-SP2 must beat E-SP1 by ≥ **3 points** at S10 or the
extra tier is dead weight. Report tier-1 pass rate and tier-1 FN count (must be 0)
separately.

**Head-to-head required.** E-SP2 vs B0; E-SP2 vs E-SP1 (the money matchup);
E-SP2 vs E-SP5 post-warmup (static coarse filter vs learned masks).

---

### E-SP3 — Partition-local deliberation: reason inside, commit back

**Mechanism sketch.** The wake decision (borrow E-SP1's gate) selects partitions,
but deliberation does *not* happen in a global working set. Instead the
deliberation is dispatched into each woken partition's local arena: reasoning ops
run against only that partition's chunks, producing a local composed result
(summary + citations). A single ledger-visible **commit** writes each local result
back to the shared store; cross-partition synthesis deliberates over the commits,
not the raw chunks. "Woken" = dispatched-to; "dormant" = never dispatched.
This attacks a different cost than E-SP1: not the scan, but the **merge** — the
working-set assembly and cross-partition interference of global deliberation,
which is the cost most likely to go superlinear at scale.

**Falsifiable predictions.** (a) On single-partition questions, ops ≈ E-SP1 (same
wake, no merge to save). (b) On cross-partition questions, E-SP3 beats E-SP1 by
skipping global merge — *unless* the question needs >3 partitions, where dispatch
fan-out exceeds merge cost. (c) **Honest failure mode:** dispatch storms — a
question whose answer spans many partitions fans out to all of them and the
dispatch + commit bookkeeping exceeds the merge it replaced; also, local
deliberation can diverge from what global deliberation would have concluded
(parity risk).

**Kill bars.** K1: FAIL if > **2 of 60** answers differ from the B0 global
deliberation (local reasoning must not change conclusions — parity bar).
K2: FAIL if (dispatch + commit ops) > **10%** of the merge ops saved vs E-SP1 on
the cross-partition subset. K3: FAIL on **any** dispatch or commit missing from
the ledger — local deliberation is invisible by default, so the audit trail is
load-bearing, not decorative.

**Proxy task + metric.** CORPUS-QA-60, reported split by single-partition vs
cross-partition questions (split frozen in prereg from ground-truth chunk
locations). Primary: ops vs E-SP1 on each split; answer-parity count vs B0.

**Head-to-head required.** E-SP3 vs B0; E-SP3 vs E-SP1 (per split — the
hypothesis predicts a crossover, and the crossover point is itself a finding);
E-SP3 vs E-SP4 (local reasoning vs hierarchical wake at S10).

---

### E-SP4 — Hierarchical wake: coarse region, then fine chunks

**Mechanism sketch.** Two-level organization: partitions grouped into **regions**
(~8 partitions each, frozen grouping at ingest). Each region carries an aggregate
signature (bitwise OR of member partition masks — cheap, coarse). Wake proceeds
coarse-to-fine: the region gate (mask-subset test, like E-SP2 tier 1) kills whole
regions at ~4 u64 ops each; the chunk gate (E-SP1-style signature scoring) then
runs only inside surviving regions, selecting individual chunks rather than whole
partitions. "Woken" is chunk-granular: a surviving region's irrelevant chunks
stay dormant. Two gate evaluations per deliberation instead of one — the
hypothesis bets the region kill rate repays the second gate.

**Falsifiable predictions.** (a) At S1 (~100 partitions) hierarchy roughly ties
flat E-SP1 — not enough partitions for the region kill to matter. (b) At S10
(~900 partitions) E-SP4 beats E-SP1 by ≥ 5 points of net savings: the region gate
kills ~7/8 of the search space before any per-partition work. (c) **Honest
failure mode:** region signatures are too coarse — a region survives because one
hot partition sets all the bits, dragging 7 cold partitions through the chunk
gate; or a region is wrongly killed and the FN is catastrophic (a whole region's
ground truth gone at once).

**Kill bars.** K1: FAIL on **any** region-gate false negative (a killed region
containing a ground-truth chunk) — like E-SP2's K1, zero tolerance by
construction. K2: FAIL if S10 net savings do not exceed E-SP1's by ≥ **5 points**
(the hierarchy must earn its keep where it claims to). K3: FAIL if at S1 E-SP4
trails E-SP1 by > **3 points** (hierarchy tax must stay bounded where it's
unneeded).

**Proxy task + metric.** CORPUS-QA-60 vs B0 and vs E-SP1 at S1 and S10. Primary:
net-savings delta vs E-SP1 per scale leg; region-kill rate and region-gate FN
count reported separately.

**Head-to-head required.** E-SP4 vs B0; E-SP4 vs E-SP1 at S1 *and* S10 (the
hypothesis lives or dies on the scale crossover); E-SP4 vs E-SP3 at S10.

---

### E-SP5 — Learned wake-masks, revised by deliberation

**Mechanism sketch.** Wake masks are **memory**, not fixed gates: per query-pattern
(a deterministic pattern key, e.g. the sorted set of query-token hashes, or a
coarse question-type tag assigned by a frozen deterministic classifier), the store
holds a mask = the set of (partition → required signature tokens) learned from
experience. The mask starts from the E-SP1 signature gate (cold start = E-SP1
behavior exactly). After each deliberation, a deterministic revision rule fires:
on a **miss**, add the missed chunk's top discriminative tokens to that pattern's
mask (widen); on a **wasted wake** (woken chunk cited nowhere in the final trace —
contribution judged by citation, not by vibes), remove the tokens that caused the
wake (narrow). No learning rates, no stochasticity — exact add/remove on evidence,
ledger-visible as deliberate revision (this is the MA4/RC1 machinery turned on
the gate itself). Masks converge when warmup ends.

**Falsifiable predictions.** (a) Cumulative ops cross below B0's cumulative ops
within the warmup budget — the learning pays for itself. (b) Post-warmup
per-deliberation ops beat static E-SP1: the mask knows the corpus's actual
query→partition mapping, not just token overlap. (c) **Honest failure mode:**
nonstationary query patterns (the discovery subset keeps inventing new patterns)
keep masks cold forever — revision churns, convergence never arrives, and the
revision bookkeeping is pure overhead on top of E-SP1 behavior.

**Kill bars.** K1: FAIL if cumulative ops do not break even vs B0 cumulative
within **120** deliberations at S1 (warmup budget = 2× the question set; the
hypothesis must pay for its own learning). K2: FAIL if warmup miss rate > **10%**
(relaxed vs the 5% shared bar — learning costs misses honestly) or post-warmup
miss rate > **5%**. K3: FAIL on **any** mask oscillation — a token removed then
re-added (or vice versa) within a 60-deliberation window. Deterministic revision
must converge, not dither.

**Proxy task + metric.** Extended run: the 60-question set × 10 passes = 600
deliberations in a frozen order (tests warmup, convergence, and stability).
Primary: cumulative ops vs B0 and vs E-SP2; miss rate split warmup (first 120) vs
post-warmup; oscillation count (must be 0).

**Head-to-head required.** E-SP5 vs B0 (cumulative); E-SP5 vs E-SP2 post-warmup
(learned vs static — the no-free-lunch matchup); E-SP5 cold-start behavior must
identically match E-SP1 on deliberation #1 (same input + same state →
byte-identical; verified, not assumed).

---

### E-SP6 — Sleep-by-default store: no gate, wake only by citation

**Mechanism sketch.** The radical variant: **there is no relevance gate at all.**
Every partition is dormant by default and wakes *only* by explicit citation — a
query term that exactly names a (partition-id, chunk-id), or a trace citation
already present in the deliberation's own history (deliberation N may wake what
deliberation N−1 cited). Gate ops are definitionally zero. "Woken" = cited;
everything else stays dark. This is Micah's hypothesis with the gate deleted: the
bet is that a deliberate system whose deliberations cite their sources doesn't
need to *predict* relevance — relevance arrives as citations.

**Falsifiable predictions.** (a) On the lookup subset, E-SP6 matches E-SP1's
recall at ~zero gate cost — the best ops number in the battery. (b) On the
discovery subset, E-SP6 fails outright: unknown-unknowns can't be cited before
they're found. (c) **Honest failure mode (expected):** this hypothesis will
likely FAIL SH-RECALL on the full 60-question set — and that failure is the
finding. Its value is mapping the boundary: the exact query class where zero-gate
routing survives, which tells the other hypotheses how much gate they can afford
to delete.

**Kill bars.** K1: FAIL if full-set miss rate > **5%** (shared bar — expected to
fire; the prereg *additionally* requires reporting lookup-subset and
discovery-subset miss rates separately so the failure is informative, not just
fatal). K2: FAIL if **any** wake in any deliberation required a scan (gate ops
must verify as exactly 0 — the hypothesis's entire identity). K3: FAIL if the
prereg cannot name, *in advance*, the query class where E-SP6 survives — no
post-hoc carving of "the questions it was good at."

**Proxy task + metric.** CORPUS-QA-60 vs B0, reported as three numbers:
full-set miss rate, lookup-subset miss rate, discovery-subset miss rate, plus
verified-zero gate ops. The deliverable is the boundary map, pass or fail.

**Head-to-head required.** E-SP6 vs B0; E-SP6 vs every other hypothesis on recall
— any hypothesis whose discovery-subset miss rate lands within **2 points** of
E-SP6's has a gating problem (it's barely beating *no gate at all* where it
matters most).

---

## 5. Head-to-head matchup matrix

| # | Matchup | Scale | Decides | Kill / verdict condition |
|---|---------|-------|---------|--------------------------|
| M1 | E-SP1 vs B0 | S1, S10 | The core claim: selective wake beats always-awake | SH- bars; must net-save ≥ 10% |
| M2 | E-SP2 vs E-SP1 | S10 | Does the cheap pre-filter earn its keep? | E-SP2 net savings ≥ E-SP1 + 3 pts, else tier-1 is dead weight |
| M3 | E-SP3 vs E-SP1 | S1 (per split) | Local deliberation vs gated global | Crossover point on cross-partition subset is itself a finding; E-SP3 must not exceed E-SP1 ops by > 15% on that subset |
| M4 | E-SP4 vs E-SP1 | S1 and S10 | Flat vs hierarchical | E-SP4 ≥ E-SP1 + 5 pts at S10; within 3 pts at S1 |
| M5 | E-SP5 vs E-SP2 | 600-delib run | Learned masks vs static filter | Post-warmup per-delib ops; K1 break-even ≤ 120 delibs |
| M6 | E-SP6 vs all (recall) | S1 | Boundary map | Any hypothesis within 2 pts of E-SP6's discovery miss rate has a gating problem |
| M7 | B-wake-none, B-inverted | S1 | Negative controls | B-wake-none ≈ 0 correct (nontriviality); B-inverted underperforms every real gate by ≥ 20 pts net savings (signal proof) |

Every matchup reports the full metric tuple (ops, miss rate, wake fraction, gate
ops broken out, wall-clock) so SH-OVERHEAD is auditable, not asserted. No
post-hoc τ or threshold tuning: selection rules frozen in prereg.

## 6. Steelman: the strongest objection to sparse routing

The strongest objection is circularity: deliberation *is* TNN's relevance
judgment, so a gate deciding what may be deliberated over is deliberation gating
deliberation — either the gate is cheaper than thought, in which case it is too
dumb to see what only real thinking reveals, or it is as smart as thought, in
which case it costs what it was meant to save. Relevance is frequently
*discovered* rather than predicted: you learn the partition mattered by thinking
inside it, and a gate can only score what the query already names — which biases
the mind toward the already-known and starves exactly the serendipitous
connections a deliberate memory was built to make. And when the gate is wrong the
failure is silent: the unwoken partition never gets to object, so sparse routing
trades the visible cost of thinking for the invisible cost of never thinking, and
no ledger entry records what was never woken. The battery above is designed to
make that silent failure loud: SH-RECALL with a frozen discovery subset, the
B-inverted control proving the gate's signal is real, and E-SP6 mapping the exact
boundary where deleting the gate deletes the answers.

## 7. What this debate does NOT decide (for build/prereg phase)

- Build order and resourcing — the coordinator's call.
- The frozen 60-question set, ground-truth chunk IDs, partition map, τ grid,
  pattern-key definitions, and the S10 construction recipe — all committed at
  prereg; this brief only specifies their *form*.
- Whether τ / region size / warmup budget are per-corpus or global — prereg
  decides; the debate recommends per-corpus with a global-fallback comparison
  (test both — standing rule).
- The deterministic correctness judge's exact string rules — frozen at prereg.
- Cross-track interactions (e.g., if Track A changes the deliberation op mix, the
  B0 baseline is re-measured — baselines are re-baselined, never inherited stale).

## 8. Prereg checklist (must be frozen before build)

1. Partition map (both corpora) + chunker parameters, committed.
2. 60-question set + ground-truth chunk IDs + lookup/discovery split, committed.
3. τ grid, region size, mask pattern-key rule, warmup budget (120), frozen.
4. Native op-counter definition (what counts as one op) + ledger schema for wake
   records (deliberation-id, partition/chunk ids, gate evidence).
5. S10 construction recipe (10× tagged copies) + workdir location (~/workspace,
   not /tmp).
6. Rerun protocol (3× from same logged state; SH-DET hard gate).
7. Selection rules for "best" operating point per hypothesis (frozen, no
   post-hoc tuning).
