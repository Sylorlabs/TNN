# VERDICT — fork H1: Witnessed Event Lattice

Status: **DEAD — falsified on multiple independent kill bars.** Deciding bar: **B5** (false-install rate 44.5% vs the 5% kill threshold; recall 73.1% vs 85% floor). B2 and B3 also fail independently. Frozen prereg: `PREREG_H1.md`. No thresholds, predicates, contract rules, schedule, or benchmark were altered after the freeze.

## Bar-by-bar

| Bar | Frozen requirement | Observed | Verdict |
|---|---|---|---|
| B1 viability | mean primary accuracy ≥ 60% (equal weights) | **74.7%** (colordisc 50.0, colorconst 92.5, shapetrans 62.2, pitchdisc 68.3, timbredisc 75.0, motiondir 100.0) | **PASS** |
| B2 adversarial edge | misleading-set decision accuracy ≥ A + 10pp, shared memory rule | H1 **47.3%** vs A **46.0%** → **+1.3pp** | **FAIL** (KILL-RELEVANT) |
| B3 efficiency | median per-fixture ops ratio ≤ 35% of A | **400%** (median 4.00; mean 12.8) — H1 is 4× MORE expensive than A | **FAIL** (KILL) |
| B4 contract load-bearing | contract changes ≥10% of misleading dispositions AND strictly reduces false installs vs ablate | disposition differs **37.6%**; contract false-installs **118 < 224** ablate | **PASS** |
| B5 honesty kill bars | false-install rate ≤ 5%; correct-install recall ≥ 85% | false-install **118/265 = 44.5%**; recall **73.1%** | **FAIL** (KILL ×2) |
| B6 determinism | 3 full byte-identical runs + independent SHA-256 ledger verification | 1165/1165 fixtures byte-identical across 3 runs; 12/12 stream ledgers re-verified (850/850 entries, independent Python checker) | **PASS** |
| B7 human oracle | native audio double-blind field-recording equivalence ≥90%; visual ≥80% rater realism | artifacts generated, brief written | **PENDING-MICAH** |
| Scale prerequisite (§3) | ≥ 10,000 event records, ≥ 30% from misleading fixtures | **9,486 records** (miss by 5.1%); misleading **3,298 (34.8%)** ✓ | **MISSED** |

## What died and why

H1 dies on four independent grounds; any one is sufficient.

**B5 (deciding): the contract cannot withhold what the front-end is confidently wrong about.** On the 425-fixture misleading stream, the gate installed 265 judgments and 118 of them were false — a 44.5% false-install rate against a 5% kill bar, and recall of only 73.1% against the 85% floor. The failure mode is systematic, not noise: on colordisc the traps judge SAME when truth is DIFFERENT (and vice versa) at ~50% false-install rates; shapetrans installed 19/19 false (recall 0%); timbredisc's contract changed literally nothing (0% disposition difference, 45.7% false-install rate); the H1-adv-only cut (the 240 KB4-targeted traps) is worse at 51.9%. The contract's warrant check (sup ≥ threshold, con == 0, intra-fixture corroboration) passes exactly when the adversarial fixtures are designed to pass it: the traps produce high-support, zero-contradiction, mutually corroborating event lattices that are simply wrong. The contract is a filter on reported confidence, not a check on truth, and the prereg's traps were built to exploit that gap.

**B2: no adversarial edge over Approach A.** H1 decision accuracy on the misleading set is 47.3% vs A's 46.0% (+1.3pp vs the required +10pp). The witnessed-lattice machinery measures input regions honestly and reports integer confidence — but on deliberately misleading inputs it reports the wrong thing just as confidently as A's raw values. motiondir is the lone bright spot (H1 60% vs A 32%, where the flicker/two-motion traps break A's naive differencing); everywhere else the lattice is parity or worse.

**B3: the efficiency hypothesis is inverted.** H1 was supposed to cost 35% of A (witnesses instead of whole-field renders); it costs 4× A at the median because every sub-span is re-measured and every byte is hashed into the ledger. The prereg's 35% target was not reachable with the frozen design.

**Scale prerequisite (§3): 9,486 < 10,000.** The mechanism produces fewer events per fixture than the prereg's estimate (mean 8.1 records/fixture). The misleading share (34.8%) passes. No records were fabricated to close the gap — the benchmark was run as frozen.

## What survives (transferable to the next fork)

1. **The contract is load-bearing, not decoration (B4 PASS).** It changed 37.6% of dispositions and cut false installs from 224 (ablate) to 118 (gate). motiondir is the existence proof of the contract working as designed: 0/41 false installs, 91.1% recall — there, the flicker/two-motion traps genuinely produce con > 0, the contract sees the contradiction and withholds/installs correctly.
2. **B6 is airtight:** three full benchmark sweeps byte-identical per fixture (1165/1165), all 12 adversarial-stream SHA-256 ledger chains independently re-verified entry-by-entry (850/850) with a from-scratch Python checker — the auditable memory contract works end to end.
3. **B1 viability:** 74.7% mean primary accuracy clears the 60% floor; the lattice is a working perceptron on clean inputs.
4. **Methodological:** the benchmark (1165 fixtures incl. 240 frozen H1 adversarial), the shared-memory-rule evaluation protocol, and the ledger verification harness are reusable. The adversarial trap families that killed H1 (distractor-blob T1B, metamer T1D, shape-jitter T3B, glide-through-threshold T4B, attack-swap T5C, flicker T6A) are proven discriminative — they should be inherited by the next fork's prereg.

## Honest caveats

- Event-ID format deviates from the frozen §4: stdout renders 32 hex chars (128-bit id_lo/id_hi) vs the specified `<16 hex>` FNV-1a-64. `nev` semantics (`event lines + alternatives`) are as specified; the deviation is cosmetic and affects no decision, disposition, or metric. Documented, not silently fixed.
- The sweep's inline `nev=` self-check predated the 1+alternatives rule and is stale in the run JSONLs (stdout hashes and judgments are unaffected). A 72-fixture stratified re-parse audit confirmed `nev == ev-lines + alternatives` in 72/72. Metrics exclude only those stale self-check strings.
- Approach A baseline was rebuilt from frozen `a_raw/sense.zag` (the build/ binary was lost in a VM reboot) and verified 108/108 on judgments/confidence/ops/harness-normalized SHA against the frozen harness's own `raw_results.json`; the harness's own single error record (A, shapetrans/adversarial/p042.img, `task_failed`) is reproduced identically by the rebuild and excluded from scoring exactly as the frozen harness excludes it.
- B7 artifacts: audio excerpts are bit-exact slices of the fixture PCM (what H1 heard), not synthesized reconstructions; overlays draw the exact witness spans from the event lattice.
- All numbers above come from `evidence/metrics.json`, produced by `eval/eval_h1.py metrics` from three frozen H1 sweeps and one A sweep.

## Kill-criterion check (§9)

- B5 false-install 44.5% > 5% → **KILL** (deciding). Recall 73.1% < 85% → **KILL**.
- B2 +1.3pp < +10pp → **KILL-RELEVANT**.
- B3 median 400% > 35% → **KILL**.
- B4: PASS (not decoration). B6: PASS (determinism + ledger verified). B7: PENDING-MICAH.
- Scale prerequisite missed (9,486 < 10,000); misleading share 34.8% passes.

**Verdict: H1 is DEAD.** What it proved: an auditable witnessed-percept + memory-contract stack can be built in pure Zag with byte-identical determinism and a load-bearing install gate. What it disproved: that integer confidence + witness spans + a sup/con/corroboration contract is enough to survive deliberately misleading inputs — the traps produce confident, corroborated, contradiction-free lattices that are simply wrong, and no confidence filter can see that from inside. The next fork needs the front-end to be *right* on adversarial inputs, not just honest about what it measured.
