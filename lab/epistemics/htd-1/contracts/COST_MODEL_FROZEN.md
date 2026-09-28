# HTD-1 Cost-Model Contract — FROZEN 2026-09-21

**Status: FROZEN.** Delivered by referee crew R1 per KB-HTD-1.6.
No efficiency build (E-DE*, E-LG*, E-SP*) may start until this contract
and the R2/R3 frozen artifacts land. Changes to the taxonomy, weights,
ledger term, baseline formulas, or advancement procedure require a dated
Micah-approved amendment (standing program law). This contract binds all
HTD-1 efficiency builders; the debate-phase briefs
(`metrics-spec.md`, `eff-deliberation.md`, `eff-ledger.md`, `eff-sparse.md`)
are superseded wherever they conflict — see §9 for every frozen reading.

Word size: 4 bytes. One ledger/audit entry = 16 words = 64 bytes
(layout: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60).

---

## §1. Frozen op taxonomy (11 classes)

Every countable operation in every efficiency arm maps to exactly one class.
Class boundaries are exclusive: a composite routine decomposes into its
classes; no operation is counted twice and none is left uncounted.

| ID | Name | Unit — exact inclusion boundary | Excludes (counted elsewhere) |
|----|------|----------------------------------|------------------------------|
| OP-01 | EXPAND | One hypothesis-expansion step: advance one hypothesis node one depth increment, including the loop-guard compare and rule-table threshold lookups. | Memory words written (→OP-05); the ledger entry emitted (→OP-05/06/07/08); evidence reads (→OP-04) |
| OP-02 | EVIDENCE | One evidence-gather call: one deterministic feature-extractor invocation over the item buffer (fixed extractor, frozen rule lists). | Chunk/buffer reads (→OP-04); its ledger entry (→OP-05/06/07/08) |
| OP-03 | CHECK | One verification check: one eliminative threshold application, one provenance re-check, one certificate/debt replay verification, one forensic self-check query step, one staleness re-derivation compare. | Reads (→OP-04); the entry it emits (→OP-05/06/07/08) |
| OP-04 | MEMREAD | One 4-byte word read from any store: memory slots, chunk fetches, ledger-buffer reads, table lookups, index reads, snapshot-serialization reads. | — |
| OP-05 | MEMWRITE | One 4-byte word written to any store: memory slots, chunk stores, ledger staging-buffer appends (16 words per entry appended), sidecar index words, batch-buffer words. | — |
| OP-06 | LBYTE | One durable ledger/audit byte written: the ledger file **and** sidecar index files (E-LG4). Delta-encoded bytes (E-LG2) counted as actually written. Snapshot bytes (E-LG2) counted when written. | — |
| OP-07 | WRITESC | One `write(2)` syscall on any fd, including staging-buffer flushes and sidecar flushes. | — |
| OP-08 | FSYNCSC | One `fsync(2)`/`fdatasync(2)` syscall. | — |
| OP-09 | GATE | One atomic gate/guard primitive: one integer compare, one u64 AND/mask test, one hash-mod, one counter/threshold compare in a gate, budget guard, debt-cap check, exit-condition check, or heuristic multiply-add. | — |
| OP-10 | HASH | One native SHA-256 substrate invocation over ≤512 canonical bytes; longer buffers count `ceil(bytes/512)`. | — |
| OP-11 | CERT | One mechanism-added audit entry's decision/guard cost: field selection, guard evaluation, linkage (episode-open markers, SUFFICIENCY_CERTIFICATE, VERIFICATION_DEBT, DEBT_SETTLED, CACHE_HIT, proposal records, BUDGET_EXHAUSTED, index self-check entries). Applies only to entries the reference pipeline would not emit. | Its 16 staging words (→OP-05), its bytes (→OP-06), its syscalls (→OP-07/08) |

**Subsumption of the debate-phase minimums** (`metrics-spec.md` §1.3):
`delib_step` → OP-01/02/03; `mem_read`/`mem_write` → OP-04/05;
`chunk_store`/`chunk_fetch` → OP-05/OP-04 (per 4-byte word: a 4 KB chunk =
1024 words); `gate_eval` → OP-09; `ledger_append` → OP-11 + OP-05/06/07/08.
Arms may not merge or redefine these classes. Arms may not add classes.

**Anti-Goodhart rule (binding).** Any computation that influences the arm's
output but is not counted in any class above is a **prereg violation — the
run is INVALID** (not scored, not a weak win; rejected at review per
KB-HTD-1.5). Work shifted into an uncounted category = invalid run.
Referees audit by code inspection: every loop, recursion, memory touch, hash,
and syscall in the arm's hot path must map to a class. One-time build costs
(partition maps, signature builds, relevance declarations, budget tables,
heuristic tables, τ grids) are harness/prereg artifacts: reported once,
excluded from per-episode C; any revision, snapshot, or re-derivation that
happens *during* a measured run is counted.

---

## §2. Fixed weights and the scalar total-cost formula

Weights are frozen for all of HTD-1 (global, not per task family — §9.2).
OP-01 is the reference unit.

| ID | w_i |
|----|------|
| OP-01 EXPAND | 1.000 |
| OP-02 EVIDENCE | 12.000 |
| OP-03 CHECK | 5.000 |
| OP-04 MEMREAD | 0.200 |
| OP-05 MEMWRITE | 0.500 |
| OP-06 LBYTE | 0.020 |
| OP-07 WRITESC | 20.000 |
| OP-08 FSYNCSC | 1000.000 |
| OP-09 GATE | 0.050 |
| OP-10 HASH | 30.000 |
| OP-11 CERT | 3.000 |

**Total cost (closed form):**

```
C = Σ_{i=01..11} w_i · n_i
```

summed in ascending class-ID order, IEEE-754 double, reported to 6 decimal
places (rounding for display only; verdicts compare unrounded values).
`n_i` are exact integers from the instrumented counters; determinism gate
(R=5, SHA-256 over the op-count vector) applies to every `n_i`.

**Mandatory subtotal decomposition** (every reported C carries all four):

```
C_delib   = w01·n01 + w02·n02 + w03·n03          (deliberation compute)
C_mem     = w04·n04 + w05·n05                   (memory-state updates)
C_ledger  = w06·n06 + w07·n07 + w08·n08          (audit/ledger write volume)
C_verify  = w09·n09 + w10·n10 + w11·n11          (verification overhead)
C         = C_delib + C_mem + C_ledger + C_verify
```

Raw unweighted vectors `(n_01 … n_11)` are always committed alongside C so
anyone can re-rank under different weights; if re-weighting flips a champion,
both champions are reported honestly.

### §2.1 One-time weight-calibration procedure (R2, before any efficiency build)

1. **Reference microbenchmark** (fixed Zag program, committed with R2's
   baselines), run on the lab VM quiescent, median of 5:
   - OP-01: 10⁵ expansion steps on a frozen 16-word node.
   - OP-02: 10³ D-P1 feature-extractor calls over a frozen 300-char passage.
   - OP-03: 10⁴ eliminative threshold applications on frozen evidence.
   - OP-04/05: 10⁶ single-word reads/writes to the memory store.
   - OP-06: 10⁶ bytes appended to the staging buffer.
   - OP-07: 10³ `write(2)` of 4096 bytes.
   - OP-08: 10² `fsync(2)` after a 4 KB write.
   - OP-09: 10⁶ integer-compare / u64-AND primitives.
   - OP-10: 10³ SHA-256 invocations over a 512-byte canonical buffer.
   - OP-11: 10⁴ canonical certificate-record emissions (guard + assembly,
     excluding staging words).
2. **Ratio check:** `ŵ_i = median_ns(i) / median_ns(OP-01)`.
3. **Tripwire (not a refit):** if any `|ŵ_i − w_i| / w_i > 1.0` (deviation
   beyond 2×), the table is re-frozen by dated Micah-approved amendment
   before any efficiency build. If all classes are within 2×, the frozen
   table above stands unchanged — measured values do not silently replace
   frozen values.
4. Calibration runs once. Weights never change mid-trial.

---

## §3. KB-HTD-1.5 compliance — the ledger term

Total cost = compute + memory-state updates + audit/ledger write volume +
verification overhead. The ledger term is:

```
C_ledger = 0.020·n_LBYTE + 20.000·n_WRITESC + 1000.000·n_FSYNCSC
```

**Mandatory in every reported win.** Any reported efficiency win computed
without `C_ledger` is **INVALID** — rejected at review, not scored as weak.
Consequences builders must internalize:

- Skipped deliberation ops also skip their ledger entries (bytes + syscalls):
  deliberation-economy savings propagate through `C_ledger` proportionally.
  This is legitimate and counted.
- Terser entries (fewer bytes per entry, fewer syscalls per entry) are
  **ledger economy**, not deliberation economy — see the SKB-SIBLING
  normalization in §7.
- In the unoptimized baseline (per-event `write`+`fsync`), one 64-byte entry
  costs `16·0.5 + 64·0.02 + 20 + 1000 = 1029.28` units — `C_ledger` dominates
  absolute C. That is the honest price of per-event durability and is exactly
  why E-LG* exist as separate hypotheses. It does not wash out E-DE savings
  bars: bars are relative to the baseline's full cost with identical ledger
  discipline.
- Sidecar index files (E-LG4) count in `n_LBYTE`/`n_WRITESC`/`n_FSYNCSC`.
  E-LG4's "ledger bytes identical with indexes on/off" bar refers to the
  ledger *file*; sidecar bytes are counted separately in `C_ledger`.

---

## §4. Closed-form baseline costs

### §4.1 B0 (always-awake) on CORPUS-QA-60

One deliberation = one frozen question. B0 wakes every partition every time
(wake fraction = 1.0 by definition; gate ops = 0).

```
C_B0(Q, P) = Q · ( |P| · c_part + c_fixed )
```

- `Q = 60` (frozen question set; S10 uses the same 60 questions).
- `|P|` = frozen partition count: S1 = P₁ (R3's partition map; ≈100:
  ~40 pg100 + ~60 sqlite3.c); S10 = 10·P₁ exactly (10 tagged copies,
  partitions stay distinct).
- `c_part = w·ū_part`: scalar cost of deliberating one partition for one
  question. `ū_part` = mean per-partition-per-question op vector of B0,
  measured once by R2 (deterministic: all 5 reruns byte-identical, so the
  mean is exact).
- `c_fixed = w·ū_fixed`: per-question fixed cost (question parse, answer
  emission, episode open/close).
- Builders' expected baseline: plug P₁ from R3 and `c_part`, `c_fixed`
  from R2 into the formula above. R2 verifies the S10 prediction against
  measured S10 within the calibration tolerance; systematic deviation is a
  finding (superlinear baseline tax), not a formula change.

B0's per-question answer correctness (frozen deterministic judge) is the
quality anchor for advancement tests.

Negative controls (own C, own accounting, never efficiency claims):
B-wake-none (wake nothing; must score ≈0 — nontriviality proof),
B-inverted (wake lowest-scoring partitions; must underperform every real gate
by ≥20 points of net savings — signal proof).

### §4.2 FULL-DELIB on D-P1 / D-P2

Per task item (identical items for every arm):

```
n_EXP = H·d            n_EVD = E            n_CHK = H·k
n_MR  = r̄              n_MW  = m̄
ē     = 2 + n_EXP + n_EVD + n_CHK          (episode-open + episode-close + one entry per op)
bytes = 64·ē                               (16-word entries)
n_WR  = n_FS = ē                           (unoptimized: every event written and fsync'd individually)

c_item(H) = w01·H·d + w02·E + w03·H·k + w04·r̄ + w05·m̄
          + w06·64·ē + (w07 + w08)·ē

C_FULLDELIB = N1·c_item(H1) + N2·c_item(H2)
```

- `H1 = 4` (D-P1, 4-play attribution), `H2 = 8` (D-P2, 8-subsystem
  classification); `N1 = N2 = 600` items.
- `d` = fixed expansion depth, `E` = evidence types gathered per item in
  canonical order, `k` = checks per hypothesis, `r̄`/`m̄` = mean memory
  reads/writes per item — frozen by R2 measurement + R3 prereg.
- Baselines carry zero OP-09/OP-10/OP-11 (no economy mechanism).
- D-P3 (synthetic adversarial orderings) is **calibration-only**: arms run
  it and report C, but D-P3 never enters headline C comparisons.

*Illustrative (not frozen):* if R2 measures `d=5, E=6, k=5, r̄=200, m̄=120`,
then a D-P1 item has `n_EXP=20, n_EVD=6, n_CHK=20, ē=48`,
`c_item ≈ 20·1 + 6·12 + 20·5 + 200·0.2 + 120·0.5 + 48·(8 + 1.28 + 1020)
≈ 292 + 49,405 ≈ 49,697`. The ledger term dominates — see §3.

---

## §5. Work vs overhead — per-hypothesis accounting table

Default rule: any class instance incurred by the reference pipeline's own
operation = **W** (work); any instance incurred solely by the economy
mechanism = **O** (overhead). Weights are identical either way — the W/O
label decides subtotal placement for overhead bars (e.g. SH-OVERHEAD), never
the price.

| Hypothesis | W (work) | O (overhead) | Notes |
|---|---|---|---|
| E-DE1 | OP-01/02/03 within budget; OP-04/05; OP-06/07/08 (SKB-SIBLING-normalized, §7) | OP-11 BUDGET_EXHAUSTED entries; OP-09 budget-guard compares; budget-table reads (OP-04 subset); whole petition-for-budget episodes | Flat-budget head-to-head arm: own C, same table |
| E-DE2 | OP-01/02/03 up to exit; OP-04/05; OP-06/07/08 normalized | OP-11 SUFFICIENCY_CERTIFICATE; OP-03 revival-guard monotonicity checks; OP-09 exit-condition checks; certificate replay verification (OP-03 subset) | Arm (a)/(b) guard costs reported separately |
| E-DE3 | OP-01/02; OP-03 load-bearing checks only; OP-04/05; OP-06/07/08 normalized | OP-11 VERIFICATION_DEBT + DEBT_SETTLED; OP-03 settlement checks + trigger-classification runs; OP-09 debt-cap checks; forced-settlement extras | Settled-before-end checks count (deferred ≠ saved). debt-cap=0 sanity arm: byte-identical ledger+outputs required; op-vector equality not required |
| E-DE4 | OP-01/02/03 on cache miss; OP-04/05; OP-06/07/08 normalized | OP-10 input+state hashing; OP-09 key compares; OP-11 CACHE_HIT; hostile-collision arm (all O, safety case) | Relevance-declaration build = one-time (excluded). False hit = KILL regardless of C |
| E-DE5 | OP-01/02/03 verification in proposal order; OP-04/05; OP-06/07/08 normalized | OP-09 heuristic scoring primitives (+ OP-04 weight-table reads); OP-11 proposal records; degraded-heuristic & random-proposal controls (separate arms, own C) | KB3 denominator frozen: heuristic O-cost ≤ 5% of mean per-item `c_item` (§4.2). Fallback episodes' full cost counts |
| E-DE2+E-DE4 stack | Same rules composed | Same rules composed; report the interaction term | Divergence > either alone → "do not compose" annotation |
| E-LG1 | Baseline deliberation OP-01–08 at per-entry price | OP-11 episode-open markers (+ their words/bytes/syscalls); kill-restart re-execution ops; batch-buffer words beyond per-entry baseline (OP-05 subset) | Lost-batch bytes never hit disk: not counted. Re-executed ops counted |
| E-LG2 | Deliberation; delta bytes as written (OP-06); per-entry syscalls as issued | Snapshot serialization reads (OP-04); snapshot bytes/syscalls (OP-06/07/08); per-word XOR/delta (OP-09 per word); checkpoint-load replay reads | K ∈ {16,64,256} = separate measured arms. Snapshot share ≤20% is a ratio bar, not amortization in C |
| E-LG4 | Baseline deliberation; ledger-*file* OP-06/07/08 unchanged | Index build/maintenance (OP-05 sidecar words + OP-06/07/08 sidecar flushes); OP-11 self-check entries; staleness re-derivation (OP-03/04) | Verification battery scored with the same taxonomy (index reads = OP-04) |
| E-SP1..6 pilots | Deliberation over woken partitions (OP-01/02/03/04/05); answer emission; deliberation-event ledger (OP-06/07/08) | OP-09 all gate tiers; OP-11 wake-set records (deliberation-id, partition/chunk ids, gate evidence); signature/mask maintenance during run (OP-05); E-SP5 revisions (OP-05 + OP-11) | E-SP6: OP-09 must verify as exactly 0 (any nonzero = K2). Warmup/convergence legs (E-SP5 600-delib run) counted per deliberation. Pilot scorecard bars (SH-*) retained; no architecture claim without §6 |

G-CO2/G-CO3/G-CM1 (gating, not efficiency): use the same taxonomy for their
op-based bars (G-CO2 KB2 "assembly ops >30% of total", G-CO3 KB2 planning-op
share); their verdicts are quality-gated, not cost-gated.

---

## §6. KB-HTD-1.3 advancement test — executable procedure

```
ADVANCEMENT-TEST(arm A, workload W, held-out W'):
  0. PRECONDITIONS
     - A cleared its pilot bars; this contract + R2/R3 artifacts frozen.
     - W = ≥500 REAL deliberative episodes (MA logs, strength-trial traces,
       debate-trace corpora; R3 assembles). Each episode = one genuine
       deliberate decision with logged inputs. Synthetic episodes excluded.
     - W' disjoint from W, with mean deliberation depth per episode differing
       by ≥2× from W, OR memory-churn rate (OP-05 per episode) differing by
       ≥2× from W (KB-HTD-1.4 "different deliberation depth, different
       memory churn").
  1. Run reference R (always-awake = full-deliberation pipeline, the §4
     baseline for the workload) on W, R=5 reruns. Require byte-identical
     (SHA-256 over op-count vectors, ledger bytes, outcomes). Record
     C_R(W) = Σ_episodes C(episode); outcomes O_R.
  2. Run A on W, R=5. Require byte-identical. Record C_A(W) (full formula,
     ledger term included — omission = INVALID); outcomes O_A.
  3. QUALITY: q = |{e ∈ W : O_A(e) == O_R(e)}| / |W|. REQUIRE q ≥ 0.98
     ("within 2%" = outcome agreement; the "same thought, cheaper" criterion).
     Where ground-truth correctness exists, also report the correctness gap;
     require ≤ 2 percentage points as a secondary check.
  4. SAVING: s = (C_R(W) − C_A(W)) / C_R(W). REQUIRE s ≥ 0.20.
  5. TRANSFER (KB-HTD-1.4): repeat steps 1–4 on W' → s', q'.
     Transfer gap g = |s − s'| / s. If g > 0.50 → VOID: claim void,
     A returns to pilot. A second VOID on any further W'' → PARKED.
  6. VERDICT: PASS iff q ≥ 0.98 ∧ s ≥ 0.20 ∧ g ≤ 0.50 (and q' ≥ 0.98).
     Below bar on s or q → PARKED (not killed), per frozen prereg §1.
  7. EVIDENCE: commit per-episode op vectors (n_01…n_11), the 5 SHA-256
     hashes, outcomes, C with all four subtotals, wall-clock median+range,
     peak memory. Verdict sheet under docs/lab/htd-1/verdicts.md.
```

Wall-clock is secondary: reported as median + range over the 5 reruns. If
wall-clock disagrees with the op-count verdict by ≥2×, the arm files a
required evidence appendix explaining the discrepancy (cache/allocator
effects are real engineering); the op-count verdict stands.

---

## §7. SKB-SIBLING normalization (E-DE* savings bars)

For E-DE1…E-DE5, savings bars are evaluated on the **sibling-normalized
cost** C†, which holds ledger price and wake set at FULL-DELIB levels:

```
C†_arm = C_delib,arm + C_mem,arm + C_verify,arm
       + ē_arm · (64·w06 + w07 + w08)      ; bytes-per-entry and syscalls-per-entry
                                            ; fixed at baseline (64 B, 1+1)
```

where `ē_arm` = the arm's actual entry count (certificates included — they
pay the standard per-entry price; no discount for terser entries, no penalty
for honest ones). Routing: E-DE arms run with FULL-DELIB's wake set (same
awake machinery — the slice boundary); any measured saving attributable to
waking fewer partitions is reclassified to E-SP*, not counted here.

Headline reporting uses actual C; the ≥15% savings bar uses C†. Both are
committed. SKB-SIBLING fires (reclassification, savings not counted) if an
arm's headline saving comes from per-entry ledger price or routing while its
C† saving is <15%.

---

## §8. Determinism, reruns, tie-breaks (frozen)

- R=5 reruns from the same logged state (frozen prereg §8: R2's harness is
  R=5, SHA-256). All scored artifacts byte-identical across the 5 or the run
  set is INVALID (two consecutive invalid run sets = BLOCKED pending Micah's
  review, per debate spec — implementation defect, not a kill).
- Logged state = memory-store contents + deliberation ledger/audit trail +
  arm configuration (weights, taxonomy version, manifests), snapshotted by the
  harness before the test phase and restored before each rerun.
- Tie-breaks per the debate spec §4.3 order (primary C → ledger bytes →
  peak memory → wall-clock median → both tie-break directions; direction-
  sensitive verdicts reported as TIE, never a win).

---

## §9. Frozen readings — ambiguities resolved

Debate-phase documents conflicted or left gaps in the following places. The
frozen prereg (2026-09-21) is binding; where it is silent, the reading below
is frozen. Both defensible readings are recorded; the frozen one is marked ★.

1. **Taxonomy shape.** Debate `metrics-spec.md` proposed minimum classes
   (delib_step, mem_read, mem_write, chunk_store, chunk_fetch, gate_eval,
   ledger_append); the frozen prereg's KB-HTD-1.5 names four cost components.
   ★ Frozen: the 11-class taxonomy in §1, which refines the four components
   and subsumes the debate minimums. Alternative (rejected): keep the 7
   debate classes — rejected because ledger bytes vs syscalls must be priced
   separately (E-LG1's entire claim is their ratio) and gate/hash/cert costs
   must be visible as verification overhead.
2. **Weight scope.** Debate spec: weights "fixed per task family". ★ Frozen:
   one global weight table for HTD-1 — cross-arm and cross-workload
   comparison (KB-HTD-1.3) requires a single yardstick; per-family weights
   would make the 20% bar family-relative and gameable. Fallback: if R2's
   calibration finds a class's cost varying >2× across task families, that is
   an amendment-level finding — report both tables, Micah decides.
3. **Rerun count.** Debate `metrics-spec.md`: R=5; debate `eff-sparse.md`:
   mean of 3 reruns. ★ Frozen: R=5 (frozen prereg §8 assigns R2 the
   "determinism harness (R=5, SHA-256)").
4. **Ledger-term binding scope.** Debate spec §1.2: ledger bytes "binding
   only for E-LG*". ★ Frozen: KB-HTD-1.5 (later, binding) — the ledger term
   is mandatory in every reported win, every arm. Omission = INVALID.
5. **E-DE5 KB3 denominator** ("heuristic cost >5% of full deliberation").
   ★ Frozen: denominator = mean per-item FULL-DELIB full cost `c_item`
   (§4.2) — full cost including ledger, not compute alone. Alternative
   (rejected): compute-only denominator — rejected as understating the
   budget the prereg intended.
6. **E-LG4 sidecar bytes.** ★ Frozen: counted in `C_ledger` (anti-Goodhart:
   shifting ledger volume into sidecars must not make it vanish). E-LG4's
   "ledger bytes identical with indexes on/off" bar refers to the ledger
   file only.
7. **Byte-identical vs state-varying tension** (wave-11 ledger debate, noted
   unresolved in `metrics-spec.md` §3). Micah has not ruled. ★ Frozen
   reading: the determinism gate governs *scored artifacts* (op-count
   vectors, ledger bytes as written, outputs); E-LG* REPLAY bars govern
   ledger-internal encoding. If Micah relaxes byte-identity for ledger-
   internal bytes, scored artifacts stay under the gate unchanged.
8. **D-P3 status.** ★ Frozen: calibration-only per frozen prereg §0(2c);
   D-P1/D-P2 carry headline weight; D-P3 C-values reported separately, never
   in headline comparisons.
9. **"Quality within 2%" (KB-HTD-1.3).** ★ Frozen: primary = outcome
   agreement with the always-awake baseline ≥98% (the §3a "same thought,
   cheaper" criterion); secondary = ground-truth correctness gap ≤2pp where
   ground truth exists. Alternative (rejected): correctness-only — rejected
   because real deliberative episodes (MA logs, traces) have no ground truth,
   only the baseline's own outcomes.
10. **E-DE3 debt-cap=0 sanity arm** ("must reproduce FULL-DELIB
    byte-identically"). ★ Frozen: byte-identical *ledger + outputs*; op-
    vector equality not required (cap-check gate evals are real ops
    FULL-DELIB never performs).
11. **One-time build costs** (partition maps, signatures, relevance
    declarations, budget/heuristic tables). ★ Frozen: reported once,
    excluded from per-episode C (harness/prereg artifacts, identical across
    arms); in-run revisions, snapshots, and re-derivations counted.
12. **Kill-restart re-execution** (E-LG1/E-LG2/E-LG4 crash trials). ★ Frozen:
    re-executed ops counted in C (real work happened); durable bytes/syscalls
    counted only for writes that completed.

---

## §10. What this contract does not do

- It does not set the E-DE1 task-class taxonomy or E-DE4 relevance
  partitions (R3 freezes those).
- It does not implement B0/FULL-DELIB or measure `c_part`, `c_fixed`, `d`,
  `E`, `k`, `r̄`, `m̄` (R2 measures; this contract gives the formulas).
- It does not run the weight calibration (R2 runs §2.1; the tripwire, not a
  refit, governs).
- It does not name champions or award PASS/FAIL/KILLED (verdict sheets do,
  per evidence).

---

*End of frozen cost-model contract. Crew R1, 2026-09-21. Amendments only by
dated Micah-approved amendment.*
