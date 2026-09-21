# Metric Operationalization — TNN Representation Program ("unit of knowledge")

**Crew 7 deliverable.** Status: PROPOSED — Micah signs before any build. Prereg discipline applies:
any change to procedures, counting rules, bars, or the blowout rule after approval needs his re-approval.

**Binding decision (Micah, 2026-09-20):** NO single crown metric. The FULL scorecard is reported
for every arm; SECTION CHAMPIONS are named per metric; an overall winner is declared ONLY on
blowout (formal rule in §BLOWOUT); otherwise the verdict is **Pareto frontier + scenario-fit map**.

**Program invariants (load-bearing, not decoration):**
- Pure Zag. ZERO randomness in any AI decision path.
- Byte-identical reruns: same input + same logged state → byte-identical output.
- Append-only audit ledger; all memory ops deliberate (add/kill/pin/promote/demote/strengthen/weaken).
- Scale precedent: 64-byte chunks; 64 deterministic corruptions, all-and-only killed; 100/100 byte-exact
  recall at 1x; 10x leg = 61,440 chunks passed (O(n²) free-slot scan cost noted); ~233k chunks hit the
  2^25 slice-indexing wall — all scale protocols must chunk buffers ≤ 33,554,432 bytes.
- Corpora: Project Gutenberg Shakespeare (~5.4MB prose, "prose"), sqlite3.c (~9.5MB code, "code").
  Already pipelined. Hold-out plan in M2.

---

## M1 — BYTE-EXACT RECALL

**What it answers:** can the arm store units and hand back exactly what was given, byte for byte,
through its own addressing layer?

**Procedure (ingest→recall trial):**
1. Take corpus C (prose, then code separately). Fixed chunking policy per arm: the arm's own
   segmentation mechanism cuts C into units of its chosen granularity (byte-arm: 64-byte chunks;
   ID arms: whatever the ID layer addresses). The chunking policy is logged as part of the run —
   the metric does NOT prescribe chunk size, it measures what the arm claims as units.
2. Ingest all units in fixed corpus order (deterministic: file order, no shuffling).
3. After ingest completes, recall each unit by the arm's own retrieval path (ID lookup for ID arms,
   address/offset for flat arms) and emit bytes to the output buffer.
4. Compare emitted bytes to source bytes with a byte-diff utility. Two sub-scores:
   - **Content recall rate** = fraction of units whose returned bytes are byte-identical to the source
     bytes for that unit (exact content match).
   - **Boundary fidelity** = fraction of units whose (start, end) span in the source corpus is exactly
     the span the arm claims. Recorded separately, never folded into content recall.
5. Sample sizes: full-corpus ingest at 1x (prose ≈ 5.4MB, code ≈ 9.5MB); recall is performed over
   ALL units (not a sample — storage is cheap, the point is the store). 10x leg = 10x the corpus
   by concatenation with deterministic separators (the 61,440-chunk precedent), still full recall.
   A "spot sample" of 1,000 units at 100x is allowed only if 10x passes 100%.

**Success definition:** a unit succeeds iff returned bytes == source bytes for the claimed span AND
the claimed span equals the span assigned at ingest. Partial credit: none. Silent bit-flips are
counted as failures of the arm, not of the trial.

**Proposed bar:** content recall = 100.0% at 1x on both corpora, 100.0% at 10x (precedent: 100/100 at
1x, 61,440/61,440 at 10x already demonstrated by the baseline). Boundary fidelity ≥ 99.5% at 1x,
≥ 99.0% at 10x. An arm that stores whole-file blobs passes content trivially but fails boundary
fidelity — that is the metric working as intended (see §CONFOUNDER granularity).

**ID-indirection anti-corruption check (mandatory for ID arms):** recall must go through the ID layer
end-to-end: the recall request carries only the unit ID; the ID→storage resolution is exercised
live; the returned bytes are hashed (SHA-256, native Zag) and compared against the hash logged at
ingest for that ID. In addition, the trial injects a **swap probe**: N=64 deterministic ID→content
remappings are applied mid-trial (the ID table is patched to point at wrong slots, deterministic
schedule logged in advance); the arm's recall path must either (a) return the remapped content
honestly labeled as remapped (i.e., the ID layer is genuinely consulted), or (b) fail loudly with
an audit entry. An arm that returns the correct content DESPITE the remap has a side channel that
bypasses the ID layer → metric scored 0 (silent corruption risk), regardless of content recall.
Precedent analogue: the 64 deterministic corruptions "all-and-only killed" trial.

**Controls:** identical corpora, identical file order, identical host; reruns byte-identical (see M8).

---

## M2 — EPISODES-TO-CRITERION ON NOVEL MATERIAL

**What it answers:** how fast does the arm learn genuinely new material, measured in discrete
learning episodes?

**"Novel" — operational definition (three tiers, all preregistered):**
- **T1 held-out:** the last 10% of each corpus file, never seen during the arm's development or any
  prior trial. Split is by fixed byte offset recorded in the prereg (e.g., prose[0..4.86MB] train /
  prose[4.86MB..5.4MB] novel). Same for code.
- **T2 third corpus:** a corpus neither arm has seen: specify in prereg (candidate: Project Gutenberg
  *King James Bible* prose + *CPython's `longobject.c`* code — similar sizes to the main corpora).
  T2 is the integrity tier: if an arm is overfit to the main corpora's statistics, T2 exposes it.
- **T3 synthetic:** a deterministic generator (seeded, but the SEED IS LOGGED AND FIXED — the
  generator is an environment input, not an AI decision) producing novel token sequences with
  controlled statistics. Tests learning independent of corpus style.

**Criterion (what counts as "learned"):** per-episode probe: after each ingest episode, run the M1
recall trial on the novel material. Criterion = content recall ≥ 99.5% on the novel material AND
boundary fidelity ≥ 95% on the novel material, sustained for 3 consecutive probe episodes
(the sustained rule prevents a lucky single probe from ending the count). The criterion is a recall
threshold — deliberately downstream of mechanism, so taught and emergent arms are judged identically.

**Episode definition and counting:** one episode = one full pass over the novel material (ingest +
probe). Count starts at episode 0 = recall on novel material with NO ingest yet (must score ~0;
if it doesn't, the "novel" material leaked → trial invalid). Episodes-to-criterion (ETC) = the index
of the first probe in the first sustained-3 run (i.e., the earliest episode at which the arm
crossed the bar and stayed across for 3). Episodes are discrete, deterministic, and logged;
no partial episodes, no time-based normalization (wall-clock is a confounder, reported in the
audit but never scored).

**Proposed bar:** report ETC as a number, not pass/fail, per tier (T1/T2/T3) and per corpus type
(prose/code) — 6 numbers. Bar proposal for champion naming: ETC ≤ 3 episodes on T1-prose,
≤ 3 on T1-code, ≤ 5 on T2, ≤ 5 on T3 (rationale: the 1x baseline already ingests to 100% in one
pass on familiar corpora; novel material should cost at most a few extra passes; the numbers are
proposed, Micah signs). Arms that never reach criterion within 50 episodes are scored ETC = 50+
(censored) and the censoring is flagged.

**Controls for corpus difficulty:** the difficulty of T1/T2/T3 differs across corpus types. Control:
report ETC **normalized against the taught-baseline arm's ETC on the same tier+type**
(relative ETC = arm ETC / taught-arm ETC). The raw number is the scorecard cell; the normalized
ratio is the comparison column. Also: every arm faces the identical novel bytes in identical order.

---

## M3 — RETENTION UNDER CHURN/PRESSURE

**What it answers:** when the store is pressured, do the valuable units survive — by deliberate
management, not by accident?

**Churn protocol (fully deterministic pressure schedule — no RNG anywhere):**
1. Ingest a fixed "valuable set" V: 1,000 units drawn from both corpora by a deterministic schedule
   (every k-th unit, k = total_units/1000, fixed offsets — no sampling randomness). Each unit in V
   is **deliberately marked valuable**: pin or promote per the arm's own mechanism, with the marking
   logged in the audit ledger. "Valuable" is thus operationally defined: units the arm (or the
   trainer acting through the arm's deliberate ops) explicitly designated as keep-worthy.
2. Pressure phase, in fixed order, 10,000 churn steps:
   - Steps 1–3,000: ingest 3,000 fresh units (new material, deterministic), no deletions allowed by
     the protocol — the arm must manage capacity itself.
   - Steps 3,001–6,000: issue 3,000 deliberate kills of the FRESH units only (kill targets chosen by
     fixed schedule; V units are never named as kill targets).
   - Steps 6,001–10,000: ingest 4,000 more fresh units while the store is at capacity (forces the
     arm's eviction/replacement policy to act, if it has one; if it has no eviction policy and
     overflows, that's a scored failure, not a crash).
3. After step 10,000, run M1 recall on V only. **Survival rate** = fraction of V recalled byte-exact.

**Proposed bar:** survival ≥ 90% (the felt-trial precedent: 25% retention vs 90% bar was scored an
honest FAIL — the bar is load-bearing). Champion bar proposed at ≥ 95%.

**Freeze-vs-retention distinguisher (mandatory — closes the "frozen store retains trivially" loophole):**
a store that silently freezes under pressure (stops accepting new units, stops evicting, stops all
management) will score 100% on survival. The distinguisher runs three checks, all required:
1. **Fresh-material accounting:** the churn phases ingest 7,000 fresh units; after the trial, recall
   a deterministic 500-unit sample of the fresh material. A genuinely managing store shows fresh
   recall ≥ 80% (it absorbed the pressure material); a frozen store shows ≈ 0% (it rejected
   everything). Freeze verdict requires BOTH high V survival AND low fresh recall.
2. **Audit-liveness check:** the append-only ledger must show management activity during the
   pressure phase (kill/promote/demote/replace entries proportional to the churn schedule).
   A frozen store's ledger goes quiet. Threshold proposed: ≥ 1 management entry per 10 churn steps
   during steps 3,001–10,000, else flagged.
3. **Deliberate-change probe:** mid-pressure (after step 6,000), the protocol issues 50 deliberate
   weaken ops on V units via the arm's own API. A live store processes them (audit shows entries,
   recall of those units reflects the weaken or the arm's documented refusal policy); a frozen
   store ignores them. Ignored deliberate ops during pressure = freeze flag.

An arm flagged FROZEN-UNDER-PRESSURE scores M3 = 0 regardless of survival rate. This is not a
judgment that freezing is always bad — a deliberate, declared freeze (audited, with expiry, per
the strength-trial force-pin-as-law precedent) is a legitimate policy and is scored on its declared
terms. The flag targets only *undeclared* freezing: retention by paralysis.

---

## M4 — REVISION SUCCESS

**What it answers:** when a unit is wrong (bad boundaries, wrong words), can the arm deliberately
fix it — not just delete it?

**Defect-planting protocol (deterministic):**
1. Take 200 units from each corpus (fixed offsets, logged). Plant two defect classes:
   - **Boundary defects (100 units):** shift the unit's recorded span by a deterministic offset
     pattern (±1, ±2, ±4, ±8, ±16, ±32 bytes, cycling) so the stored bytes are wrong at the edges
     while the unit's ID/label claims the original span.
   - **Content defects (100 units):** substitute words/tokens by a deterministic rule
     (e.g., every 7th byte XOR 0xFF in prose; identifier rename by fixed map in code). The defect
     is applied to the STORED unit, not the source; the source remains the ground truth.
2. Planting is logged in the audit ledger as external-trainer ops (not arm decisions).
3. The arm is then presented with the defective store plus access to the source corpus
   (the "world evidence" analogue from the debate precedent) and instructed through its own
   deliberate-revision API to reconcile. 20 revision episodes maximum (deterministic count).

**Measurement — three mutually exclusive outcomes per defective unit:**
- **REVISED (wrong→right):** the unit's stored bytes now match the source bytes for its claimed
  span, AND the unit's ID/lineage is continuous (same ID, audit shows a revise/repair entry —
  not a kill+re-add, which is a new unit wearing the old ID).
- **KILLED:** the unit (or its ID) is gone from the store. Recorded separately.
- **UNFIXED:** still defective, or "revised" to something that matches neither source nor the
  defect (counts as unfixed).

**Revision rate** = REVISED / 200 per defect class. **Kill rate** reported alongside, never merged.

**Proposed bar:** revision rate ≥ 80% per defect class at 1x (rationale: the debate precedent showed
180/180 deliberate revisions at 10x when world evidence was available; 80% leaves headroom for the
harder boundary class). Champion ≥ 90%.

**Anti-gaming rule (explicit):** an arm that kills every defective unit scores revision rate 0%,
not 100% — REVISED requires wrong→right with lineage continuity, and KILLED is a separate outcome
that does not numerator into revision rate. Further: an arm whose kill rate on defective units
exceeds 50% while its revision rate is below the bar is flagged KILL-SUBSTITUTION and its M4 is
scored 0 — killing everything is not revising. Also: an arm may not "revise" by re-ingesting the
whole corpus and claiming the defect is gone; revision must be per-unit through the revision API
with per-unit audit entries, else the whole M4 run is invalid.

---

## M5 — MEMORY + AUDIT COST PER UNIT LEARNED

**What it answers:** what does a learned unit cost — in store and in the audit trail that proves it?

**"Unit learned" — operational definition:** a unit counts as learned iff it (a) was ingested by
the arm's deliberate add path, (b) is recalled byte-exact (M1 procedure) at the end of the trial,
and (c) survived a 1,000-step churn mini-pressure (M3 phases compressed: 500 fresh ingests +
500 kills, deterministic). All three, no partial credit. Rationale: a unit that can't be recalled
or can't survive routine management was never "learned" — it was written.

**Counting procedure:**
1. Run a fixed ingest trial: full prose corpus (1x) through the arm, then the churn mini-pressure.
2. L = number of units learned (per the definition above).
3. Memory cost = total bytes of live store attributable to learned units at trial end, measured by
   the arm's own allocator accounting (reported per the harness's byte counter, not the arm's
   self-report — the harness measures process RSS delta attributable to the store region, plus the
   arm's declared slot table size; both reported).
4. Audit cost = number of audit ledger entries (and total ledger bytes) consumed from first ingest
   op to end of churn, divided by L.
5. **Cost per unit learned** = (memory bytes)/L and (audit entries)/L, reported as a pair.

**Cross-granularity normalization — per-BYTE cost as the common denominator:** arms choose
different granularities (64-byte chunks vs superchunks vs whole files), so per-unit cost is not
comparable raw. The scorecard reports per-unit cost AND **per-source-byte cost** =
total memory bytes / total source bytes learned, and total audit entries / total source bytes
learned. Per-byte is the comparison column (justification: the corpus is the fixed common ground;
every arm must account for the same ~5.4MB of prose; how finely it cuts is its design choice, and
the per-byte cost shows what that choice costs). An arm with huge units and tiny overhead wins
per-byte only if it genuinely stores less per source byte — the M1 boundary-fidelity sub-score
keeps coarse arms honest about what their units actually pin down.

**Proposed efficiency bar:** per-byte memory cost ≤ 1.5x source bytes (i.e., ≤ 50% storage overhead
vs the raw corpus) and per-1KB-learned audit entries ≤ 10 (proposed; rationale: the audit must be
fine-grained enough to replay to exact state — the MA1 precedent — but an arm that logs 1,000
entries per KB has bought its recall score with ledger bloat; Micah signs the exact numbers).
Champion: lowest per-byte pair on the Pareto frontier (see §BLOWOUT — cost is a "lower is better"
metric and participates in blowout counting).

**Controls:** same corpus, same churn schedule, same allocator harness; the audit ledger format is
fixed by the harness (16-word entries per the audit-layout precedent) so entry counts are
comparable; ledger byte totals are reported alongside counts in case an arm games entry granularity.

---

## M6 — CROSS-DOMAIN GENERALIZATION

**What it answers:** does the arm learn a *representation method*, or does it memorize one domain's
statistics?

**Transfer design (both directions, never averaged):**
- **Direction P→C:** arm trains (ingest + deliberate organization, per its own method) on prose
  only, to the M2 criterion on prose. Then, with NO further tuning of the representation method
  (ingest of code is allowed — the arm must store the code — but its segmentation/vocabulary
  policy is frozen), it faces the code corpus: run M1 (recall + boundary fidelity) and M4
  (revision on planted code defects) on code.
- **Direction C→P:** mirror image.
- **Transfer task, exactly:** (1) byte-exact recall on the new domain at 1x (M1 procedure,
  segmentation policy frozen from training domain); (2) boundary fidelity on the new domain;
  (3) revision rate on 100 planted boundary defects in the new domain (M4 compressed).
  Three numbers per direction, six total.

**Asymmetry analysis (mandatory):** report P→C and C→P as separate scorecard columns. Rationale:
code has rigid structure (braces, keywords) that may transfer differently than prose's loose
statistics; averaging the two directions would hide an arm that only works prose→code. The
scorecard template (§SCORECARD) has separate columns; any summary that averages them is
non-compliant with this prereg.

**Proposed bar:** transfer recall ≥ 95% in both directions (vs 100% in-domain bar — a 5-point
transfer tax is proposed as acceptable); transfer boundary fidelity ≥ 90% both directions;
transfer revision ≥ 70% both directions. Champion: smallest transfer tax
(in-domain score − transfer score) per direction.

**Negative control (the metric must catch memorizers):** include a **memorizer control arm**: an
arm whose segmentation policy is hardcoded to prose statistics (e.g., splits on English word
boundaries and caches frequent n-grams; on code it must still operate but its policy is frozen
prose-tuned). The metric is valid only if the memorizer shows a large, visible transfer tax in
at least one direction (proposed validity threshold: transfer recall drops ≥ 15 points vs
in-domain in C→P or P→C). If the memorizer passes the bar, the transfer task is too easy and the
bar must be raised before scoring real arms — the negative control gates the metric, not the arms.

---

## M7 — CACHE HIT/REUSE RATE (ID-based arms)

**What it answers:** for arms with an identity layer, how much work does the ID system save —
and is the dedup real?

**Definitions:**
- **Hit:** a retrieval request for a unit that is served from the ID→content mapping without
  re-ingesting or recomputing the unit's bytes. Hit rate = hits / total retrieval requests.
- **Reuse:** one ID serving more than one memory (the same unit content referenced by multiple
  memories/contexts). Reuse factor = total ID references / distinct IDs live.
- **Dedup ratio (content-addressed arms):** 1 − (distinct stored contents / total ingest units)
  over a repeated-ingest schedule. A ratio of 0.5 means half the ingested units were already
  present and correctly deduplicated.

**Measurement — deterministic repetition protocol:**
1. Ingest corpus C (1x). Log every ID issued.
2. Ingest C again, byte-identical (repetition round 1). Then ingest C′ = C with a deterministic
   edit schedule (every 100th unit replaced by a fixed alternative; logged in advance).
3. During all three ingests, route a fixed retrieval schedule: 5,000 ID lookups in deterministic
   order (every k-th live ID, cycling). Count hits vs re-ingests.
4. Dedup ratio computed over rounds 1–3: repeated units must resolve to the SAME ID
   (content-addressed) or be explicitly marked as new versions linked to the old ID (versioned
   arms) — either is acceptable if declared and audited; silently issuing fresh unrelated IDs
   for identical content scores dedup 0.

**Proposed bar:** hit rate ≥ 90% on the fixed retrieval schedule; reuse factor ≥ 1.5 on the
repetition protocol (i.e., the average live ID serves ≥ 1.5 memories); dedup ratio ≥ 0.4 on
rounds 1–2 (round 3 with edits is reported, not barred — edits legitimately create new content).
Champion: highest hit rate, then highest dedup.

**How non-ID arms are scored:** **N/A with justification, and N/A is not a penalty.** A flat
byte-store with no identity layer cannot have "cache hits" — scoring it 0 would punish an
architecture for not having a part it never claimed. The scorecard marks non-ID arms `N/A (no ID
layer)` for M7's three sub-cells, and M7 is excluded from that arm's blowout denominator
(see §BLOWOUT: blowout counts only metrics applicable to the arm). HOWEVER — non-ID arms must
still report a **fair equivalent**: bytes re-read from source during the repetition protocol
(an ID arm avoids re-ingest; a flat arm that re-reads the whole corpus from disk on round 2 is
doing the work the cache would have saved). The equivalent is reported as informational only,
not scored, to keep the comparison honest without forcing a foreign metric.

---

## M8 — DETERMINISM GATE (hard gate, not a score)

**What it answers:** is the arm deterministic, byte-for-byte, or is it disqualified?

**This is a gate, not a metric.** There is no partial credit, no percentile, no "mostly
deterministic." FAIL on any check below = the arm is **disqualified from the program's results**
— its scorecard is marked DISQUALIFIED and its numbers are reported for forensics only, never
for champion naming or the Pareto frontier. (Rationale: the no-randomness law is Micah's standing
law; a non-deterministic arm has violated a law, not underperformed a metric.)

**Byte-identical rerun procedure:**
- **N = 5 full runs** of the complete M1+M3 trial sequence (the two trials with the most
  allocation churn), each run starting from the same logged initial state and the same input
  bytes. Justification for N=5: the hardened-replay precedent caught uninitialized-memory, ASLR,
  entropy-source, and clock cases 8/8 — those defects are per-run flaky, not per-thousand-run
  flaky; 5 runs give 4 independent diffs, which the precedent suggests is sufficient to catch
  the known defect classes, while keeping the gate affordable at 10x scale. (N is proposed;
  Micah signs. Raising N is always allowed without re-approval; lowering it needs his sign-off.)
- **Diff protocol (exact):**
  1. After each run, capture: (a) the full memory-store byte image (the arm's slot region,
     chunked ≤ 2^25 per the slice-indexing wall, hashed per chunk with native SHA-256 then the
     hashes concatenated and hashed again — the diff is on the hash chain, with per-chunk hashes
     retained for localization); (b) the complete append-only audit ledger bytes; (c) stdout/stderr
     bytes; (d) the harness's allocator trace (allocation order + sizes, not addresses — addresses
     are ASLR-tainted by design and are normalized out, NOT compared).
  2. "Identical" = byte-identical hash chains for (a), (b), (c), and identical allocator traces
     for (d), across all 5 runs. Any single differing byte in any artifact = FAIL.
  3. The diff tool itself is versioned and its source committed; diffs are re-verifiable by a
     third party from the retained artifacts.

**Adversarial variation battery (runs 2–5 are not clean-room reruns — each carries a perturbation):**
- Run 2: heap perturbation — the harness pre-fragments the heap with a deterministic allocation
  pattern before the arm starts (catches uninitialized-memory reads: fresh garbage differs
  run to run).
- Run 3: ASLR-equivalent — the harness maps the store region at a different base offset
  (catches pointer-identity leaks into stored state).
- Run 4: entropy/clock starvation — `/dev/urandom` reads and wall-clock syscalls return fixed
  canaries via the harness shim (catches hidden entropy/clock dependence; any arm behavior
  change vs run 1 = FAIL even if outputs happen to match — the shim logs whether the canary
  was consulted).
- Run 5: allocation-order shuffle — the harness reverses the order of the arm's own free-list
  initialization (catches order-dependent tie-breaking that isn't state-driven).
- Precedent: the hardened replay work caught all 8 seeded defect classes (uninitialized memory,
  ASLR, entropy, clock × 2 variants each); this battery is that precedent operationalized as a gate.

**Scope note:** "identical" covers memory bytes, audit bytes, stdout/stderr, and allocator traces.
It does NOT cover wall-clock elapsed time, RSS high-water marks, or ASLR-affected raw addresses —
those are environment, not mind. The no-randomness law binds the AI's decision paths; the world
may be unpredictable, the mind may not be dice.

---

## M9 — NOVEL-MATERIAL LEARNING CURVE SHAPE (bonus discriminating metric)

**What it answers:** beyond *how fast* (M2's episodes-to-criterion), *how* does the learning
happen — and does the shape discriminate taught vs emergent vs self-cut arms?

**Rationale for "bonus":** M9 does not name champions and does not count toward the blowout rule.
It exists to test the hypothesis that curve shape carries architectural signal. If after the
first full trial round the shapes do not separate arm classes, M9 is retired to informational
status by prereg amendment (Micah signs the retirement).

**Operationalization (deterministic curve comparison):**
1. During the M2 trial (novel material, T1 tier), record the per-episode probe scores:
   content recall r(e) and boundary fidelity b(e) for episodes e = 0..ETC (criterion episode).
   The curve is the vector [(r(0),b(0)), (r(1),b(1)), …] — discrete, deterministic, no smoothing,
   no curve fitting (fitting introduces analyst degrees of freedom; raw points only).
2. **Shape descriptors (computed, not fitted):**
   - **Takeoff episode:** first e with r(e) ≥ 50%. (When does it get off the ground?)
   - **Steepness:** max over e of (r(e+1) − r(e)) — the largest single-episode jump.
   - **Late gain:** r(ETC) − r(takeoff) — how much learning happens after takeoff vs at takeoff.
   - **Shape class (rule-based, deterministic):** "fast-then-flat" iff steepness ≥ 40 points AND
     late gain ≤ 15 points; "slow-then-sudden" iff takeoff ≥ 3 AND steepness ≥ 40 points;
     "gradual" iff steepness < 40 points; else "other". The 40/15/3 thresholds are proposed
     (Micah signs); the classification is a pure function of the recorded points.
3. **Curve comparison across arms:** curves are compared by exact vector match on shape class
   first, then by (takeoff, steepness, late gain) triples. No statistical tests with p-values —
   with N=1 curve per arm per tier, inference is inappropriate; the comparison is descriptive
   and the discrimination claim is: *do taught arms cluster in one shape class and emergent arms
   in another?* That question is answered by inspection of the scorecard's M9 column, not by a test.

**What would make M9 load-bearing in future rounds:** if shape class predicts transfer tax (M6)
or revision rate (M4) better than ETC alone does — i.e., if two arms with equal ETC but different
shapes show systematically different M4/M6. That analysis is preregistered as exploratory; it
promotes M9 to a scored metric only by Micah-signed amendment.

---

## SCORECARD TEMPLATE

One row per arm, one column group per metric. Cell formats are normative: results drop straight in,
and any cell not matching its format invalidates the row until fixed.

| Arm | M1 recall % (prose/code) | M1 boundary % (prose/code) | M1 ID-probe | M2 ETC T1/T2/T3 (prose,code) | M3 survival % | M3 freeze flag | M4 revised % (bound/content) | M4 kill % | M5 mem B/B | M5 audit entries/KB | M6 P→C (rec/bnd/rev) | M6 C→P (rec/bnd/rev) | M6 transfer tax | M7 hit % | M7 reuse × | M7 dedup | M8 gate | M9 shape class | M9 (takeoff,steep,late) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A (taught) | 100.0 / 100.0 | 99.7 / 99.6 | PASS | 2,2 / 2,3 / 3,4 | 96.2 | CLEAR | 88 / 91 | 6 | 1.32 | 7.1 | 97/93/74 | 96/91/71 | −3.5/−4.0 | 94.1 | 1.8 | 0.52 | PASS | fast-then-flat | (1,52,11) |
| B (emergent) | … | … | … | … | … | … | … | … | … | … | … | … | … | N/A (no ID layer) | N/A | N/A | PASS | gradual | (2,31,28) |

**Column specs:**
- Percentages: one decimal, `0.0–100.0`. Recall/boundary/revision/survival/hit/dedup-as-%.
- M1 ID-probe: `PASS` / `FAIL (side channel)` / `N/A (no ID layer)`.
- M2 ETC: integers per tier, prose then code, comma-separated; censored values as `50+`; T2/T3 single
  numbers (one corpus each). Add a companion column of relative-ETC ratios vs the taught baseline.
- M3 freeze flag: `CLEAR` / `FROZEN-UNDER-PRESSURE` (flag → M3 scored 0, see M3).
- M4: revised % per defect class; kill % alongside; `KILL-SUBSTITUTION` flag if triggered.
- M5: `mem B/B` = memory bytes per source byte (2 decimals); audit entries per KB learned (1 decimal).
  Lower is better — mark with ↓ in the header.
- M6: per direction `rec/bnd/rev` percentages; transfer tax = mean(in-domain − transfer) per direction
  (1 decimal, signed). **P→C and C→P are never merged into one column.**
- M7: hit % (1 decimal), reuse factor (2 decimals, ×), dedup ratio (2 decimals). Non-ID arms:
  `N/A (no ID layer)` + informational re-read-bytes figure in a footnote column.
- M8: `PASS` / `FAIL — DISQUALIFIED`. A FAIL blanks the arm's champion eligibility everywhere.
- M9: shape class + (takeoff, steepness, late gain) triple. Informational; excluded from blowout.

**Machine-readable schema (for the results ledger):** one JSON object per arm per trial round,
keys: `arm, round, scale, m1_recall_prose, m1_recall_code, m1_boundary_prose, m1_boundary_code,
m1_id_probe, m2_etc{…}, m3_survival, m3_freeze_flag, m4_revised_boundary, m4_revised_content,
m4_kill_rate, m4_kill_substitution_flag, m5_mem_per_byte, m5_audit_per_kb, m6_p2c{rec,bnd,rev},
m6_c2p{rec,bnd,rev}, m6_tax_p2c, m6_tax_c2p, m7_hit, m7_reuse, m7_dedup, m7_na_reason,
m8_gate, m9_shape, m9_triple, disqualified`. Numbers as numbers, flags as strings, N/A as null
with reason in `m7_na_reason`. Schema version `metrics-v1`; any field addition needs Micah's sign-off.

---

## BLOWOUT RULE (formal)

An overall winner may be declared **iff** all of the following hold:

1. **Applicability:** the arm passed the M8 determinism gate (no disqualified arm can win).
2. **Breadth:** the arm is section champion (best scorecard value; ties broken by the better
   transfer-tax / lower-cost secondary, then declared co-champions of that section) in **≥ 6 of
   the 8 scored metrics** (M1–M8 excluding M8-as-gate; M8 contributes only eligibility, M9 is
   informational and never counts).
3. **No weak flank:** in the remaining scored metrics (the ones it did not win), the arm scores
   **at or above the 50th percentile** of all non-disqualified arms on every one of them —
   i.e., it is never below-median anywhere it is scored. (Percentile computed over arms with
   applicable scores; N/A cells excluded from that metric's percentile computation.)
4. **N/A discipline:** metrics marked N/A for the arm (M7 for non-ID arms) are excluded from both
   the numerator and denominator of rule 2 — the threshold is ≥ 6 of *applicable* scored metrics,
   or ≥ 75% of applicable scored metrics rounded up, whichever is larger. (So an arm with M7 N/A
   needs ≥ 6 of 7.)
5. **Scale confirmation:** the blowout must reproduce at the next scale leg up from where it was
   first observed (1x → 10x): the arm must again satisfy rules 1–4 at 10x before the overall-winner
   declaration is final. A 1x-only blowout is reported as PROVISIONAL BLOWOUT.

If any rule fails: **no overall winner. Verdict = Pareto frontier + scenario-fit map** (§SCENARIO-FIT).
Co-blowout (two arms both satisfying 1–5) is declared a tie and likewise collapses to
Pareto + scenario-fit — the rule does not manufacture a winner.

*One-sentence version for the report-back: an overall winner is declared only if a
non-disqualified arm is section champion in ≥6 of its 8 applicable scored metrics (M9 excluded),
is never below-median on any scored metric, and reproduces the result at the next scale leg —
otherwise the verdict is Pareto frontier plus scenario-fit mapping.*

---

## SCENARIO-FIT MAP TEMPLATE

**Purpose:** when there is no blowout (the expected case), the verdict states *which arm wins in
which conditions* — this template makes that assignment procedural, not impressionistic.

**Fit dimensions (each arm is rated per dimension from its scorecard, not from narrative):**
1. **Corpus type:** prose-heavy vs code-heavy vs mixed workloads. Assignment rule: the arm with the
   best M1+M6-transfer-tax pair on that corpus type owns the dimension. (M6 asymmetry respected:
   an arm may own "prose→code transfer" without owning "code→prose transfer.")
2. **Scale:** 1x / 10x / 100x-projected. Assignment rule: best M1-at-scale + M5-cost pair at the
   highest scale leg the arm has completed. An arm untested at 10x cannot own the 10x row —
   mark `UNTESTED`, never extrapolate.
3. **Pressure regime:** low-churn archival vs high-churn live store. Assignment rule: M3 survival
   (with freeze flag CLEAR required) for high-churn; M5 cost for archival (cheap deep storage).
4. **Teaching availability:** teacher-present (taught arms allowed their trainer) vs autonomous
   (no teacher at trial time). Assignment rule: M2 ETC and M9 shape on T2/T3 (unseen-by-teacher
   tiers) — the arm that learns novel material without teacher touch owns autonomous.
5. **Integrity criticality:** settings where silent corruption is catastrophic. Assignment rule:
   M1 ID-probe PASS + M8 PASS + M4 revision rate (deliberate repair beats silent rot). Arms with
   any FAIL here are excluded from this row regardless of other scores.
6. **Budget constraint:** memory/audit budget capped. Assignment rule: M5 per-byte cost ranking;
   the cheapest arm that still clears the M1 bar owns this row.

**Assignment procedure:** for each dimension, rank arms by the named metric pair; the top arm is
named dimension champion with its margin (absolute point gap to runner-up) reported. Margins
< 2 points (or < 5% relative for cost metrics) are declared TIED — the map shows both arms.
The map is a table: rows = dimensions, columns = champion arm(s) + margin + the deciding metrics.
Recompute per scale leg; a dimension champion at 1x that loses at 10x is reported as a scale
interaction, not an error.

---

## CONFOUNDER REGISTER

Every cross-arm comparison hazard identified, with its control. Controls are mandatory parts of
the trial harness, not suggestions.

| # | Confounder | How it biases comparisons | Control |
|---|---|---|---|
| C1 | **Granularity differences** — a whole-file arm vs a 64-byte-chunk arm face different unit counts for the same corpus | Per-unit metrics (M5 cost, M7 reuse) favor coarse arms; per-byte metrics favor fine arms | M5's per-source-byte normalization is the comparison column; M1 boundary fidelity is reported separately so coarse arms can't hide vagueness; never rank arms on raw unit counts |
| C2 | **Corpus order effects** — ingest order interacts with replacement/eviction policies | An arm tuned to the fixed file order looks better than it is | Order is fixed AND identical for all arms (fairness), plus one **reversed-order leg** at 1x reported informationally to detect order dependence; an arm whose M1 drops >2 points on reversal is flagged ORDER-SENSITIVE |
| C3 | **Teacher quality in taught arms** — a brilliant teacher makes the arm look good | M2 ETC and M9 shape confound teacher skill with arm learnability | T2/T3 novel tiers are unseen by the teacher by construction; report teacher-touch count (number of deliberate teacher ops during the trial, from the audit ledger) alongside M2 — an arm needing 10x the teacher touches for equal ETC is not equally good |
| C4 | **Audit-ledger capacity interactions at scale** — ledger growth is O(ops); at 10x/100x the ledger itself becomes the bottleneck | M5 audit cost explodes for chatty arms; worse, ledger pressure can throttle the arm's own ops, depressing M1–M4 | Ledger capacity is fixed per scale leg and identical across arms; ledger bytes are a measured M5 cost (not free); any arm that stalls on ledger capacity is scored on what it completed, with `LEDGER-BOUND` flagged — the flag is data, not an excuse |
| C5 | **The 2^25 slice-indexing wall** — buffers > 33,554,432 bytes can't be indexed in one slice (znc limit) | Scale legs near ~233k chunks break arms that assumed one flat buffer; breakage looks like an arm failure but is a toolchain limit | All scale harnesses chunk buffers ≤ 2^25 by construction; chunking is declared a build note (equivalence proven by byte-identical reruns per precedent), never a prereg amendment; arms are scored on logical behavior, not on dodging the toolchain |
| C6 | **O(n²) free-slot scan cost** (noted at the 61,440-chunk 10x leg) — allocator policy interacts with scale | An arm with a naive free-list looks fine at 1x and collapses at 10x; wall-clock tempts analysts to "adjust" | Wall-clock is never scored (M8 explicitly excludes it); what IS scored is whether the arm completes the leg and its M5 cost — if O(n²) scan shows up as audit/memory bloat it lands in M5 where it belongs |
| C7 | **Defect-planting realism (M4)** — planted defects may not resemble real errors | Arms overfit to the deterministic defect pattern; revision rate overstates real repair ability | Two defect classes (boundary + content) with cycling magnitudes; the exact offsets are logged but the *class distribution* is what the bar targets; future rounds rotate the planting schedule by prereg amendment |
| C8 | **"Valuable" designation gaming (M3)** — an arm could mark everything valuable, making survival trivial | Survival rate 100% by declaring the whole store precious | The valuable set V is fixed at 1,000 units by the protocol (not the arm); the arm only chooses the *marking mechanism* (pin/promote), and the freeze distinguisher (fresh-material accounting + audit liveness) catches mark-everything paralysis |
| C9 | **Memorizer arms gaming M6** — a lookup table with the test corpus baked in | Transfer metrics look fine because the "novel" domain was secretly seen | T2 third-corpus tier + the memorizer negative control arm (M6): the metric is valid only if the control fails visibly; corpus hashes are committed before arms are built |
| C10 | **ID-layer side channels (M1/M7)** — recall that bypasses the ID table | ID arms claim dedup/hit benefits while actually re-reading source | The M1 swap probe (64 deterministic remaps) is mandatory for ID arms; M7 dedup requires same-ID resolution proof, not just byte equality |
| C11 | **Churn-schedule overfitting (M3)** — the pressure schedule is public and deterministic | Arms could hardcode responses to the exact 10,000-step schedule | The schedule's *structure* (phases, counts) is public but the *unit identities* at each step derive from fixed corpus offsets the arm can't reasonably precompute against without actually implementing general management; plus the reversed-order leg (C2) perturbs identities |
| C12 | **Survivor bias in ETC censoring (M2)** — arms that never reach criterion (ETC=50+) distort means | Averaging ETC with censored values understates the gap | Censored ETC values are never averaged; report medians with censoring flags, and rank arms by (reached-criterion?, then ETC) lexicographically |
| C13 | **Harness allocator normalization (M8)** — comparing allocator traces across arms with different allocators | A custom allocator's trace looks "different" without being nondeterministic | M8 compares each arm against *itself* across 5 runs, never arm-vs-arm; cross-arm allocator comparison is out of scope for the gate |
| C14 | **M9 shape-class threshold gaming** — the 40/15/3 cutoffs are arbitrary | Arms near a cutoff flip class on noise — except there is no noise (deterministic); still, cutoffs could mislabel | Cutoffs are proposed and Micah-signed; shapes are reported as raw triples alongside the class so any analyst can re-derive; class is descriptive, never scored, so mislabeling costs nothing |
| C15 | **Scale-leg selection bias** — reporting only the scale where your arm shines | 1x results presented as the headline when 10x failed | The scorecard requires a row per scale leg attempted; a missing 10x row for an arm that attempted it is marked `ATTEMPTED — FAILED` (never silently dropped); blowout rule 5 requires 10x confirmation |

**Open confounders (no control yet — flagged for Micah):** cross-contamination between trial
rounds (an arm's M4 revision experience changing its M2 behavior — mitigated by fresh arm instances
per metric, at the cost of 9× compute; proposed: fresh instance per metric, Micah signs the
compute); teacher-touch counting for emergent arms with no teacher concept (count = 0 by definition,
but then "autonomous" comparisons need care — see scenario-fit dimension 4).

---

*End of Crew 7 deliverable. Proposed bars, N=5, blowout thresholds, and M9 cutoffs await Micah's
signature before any build. Schema version: metrics-v1.*
