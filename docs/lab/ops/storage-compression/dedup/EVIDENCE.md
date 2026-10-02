# Duplicate-fact investigation — EVIDENCE

Date: 2026-09-23. Workload: deterministic synthetic (see Limitations).
Binary: pure-Zag `dd_main`, built with pinned
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Store: S5 canonical layout (copy in `src/s5_store.zag`; one 1-line hardening
added vs `adopt/` — see §7).

Every mode below was run twice; outputs are **byte-identical** across reruns
(`cmp` clean on all of scan/prove/exp1-p1/exp1-p5/exp2). Zero randomness
anywhere: fixture generation, scanner, policy, and experiments are fully
deterministic. Each mode completes in under a minute on the lab VM.

## 1. Workload

40,000 base claims `(subject=c, relation=(c*7)%64, object=c)`.
Copies per claim follow a deterministic long-tail: `1 + 16/(1+(c%17))`
(1–17 copies), total **157,650 facts**. Injected structure:

- **exact duplicates**: every copy repeats the claim value verbatim;
- **semantic variants**: subject aliases (`100000+s`, c<4096, c%11==0) and
  relation aliases (`1000+r`, c%13==0);
- **conflicts**: last copy asserts `object^0xBEEF` on single-valued
  relations (c%29==0, r<32);
- 50 deterministic source ids (not used by the scanner; used by exp2).

Claim encoding: `value = subject | (relation << 20) | (object << 32)`.

## 2. Scanner

Three pure-Zag open-addressing hash passes over live facts:

1. **EXACT** — groups by raw packed value; every id points at its group's
   first id (representative).
2. **SEMANTIC** — groups by canonical value (alias-normalized subject and
   relation); a group counts only if >1 member and values are not all
   byte-identical.
3. **CONFLICT** — groups by canonical (subject, relation) on single-valued
   relations; a group counts only if ≥2 distinct objects appear.

## 3. Scan results (`run_scan.txt`)

- facts=157,650 live; distinct values=43,837; conflict groups=649.
- exact-grouped ids: 150,553 (95.5%); semantic ids: 13,186 (3,188 groups);
  conflict ids: 2,657; unique: 2,352.
- exact group sizes: 18,237×2, 6,980×3, 2,354×4, 2,351×5, 2,112×6,
  236×8, 4,470×9+.
- Classification accuracy vs ground truth (refined definitions, §4):
  **sem_miss=0, sem_spurious=0, conflict_miss=0, conflict_spurious=0**,
  exact groups 100% pure (0 impure of 36,740).
- Store: 1,897,740 bytes = **12.04 B/live fact**; manifest=0, replay=0.

## 4. What "miss" means — two apparent misses that are correct behavior

Naive scoring showed sem_miss=209, conflict_miss=41. Investigation proved
all 250 are definitionally out of scope, and the scanner is exactly right:

- **41 lone conflicting assertions**: claims asserted exactly once whose
  single copy carries a conflicting object. A conflict needs ≥2 parties; a
  singleton has nothing to conflict *with*. These belong to the verdict /
  corroboration layer (withhold as uncorroborated), not the duplicate
  scanner. Verified: every one is a 1-copy claim (`miss_non_singleton`
  accounting + refined scorer).
- **28 variant+conflict pairs**: 2-copy claims where one copy is a wording
  variant and the other is a conflicting assertion. After canonicalization
  the two copies are genuinely different claims (different objects), so the
  pair is a **conflict**, not a semantic duplicate. All 28 are correctly
  flagged conflict members (`variant_conflict_pairs_flagged=28`).

The refined scorer (`DD_SCORE2`) encodes these definitions and reports
0/0/0/0. Lesson for the intelligence: "duplicate" is a verdict-relative
notion — the same byte pattern is waste, evidence, or contradiction
depending on what it is paired with.

## 5. Deletion-safety proof (`run_prove.txt`, `ok=1`)

Policy: delete exact-duplicate non-representative ids, **skipping** any id
in a conflict group. Deleted **112,481** ids (71.3% of facts);
skipped 1,332 conflicted ids. Six checks, all pass:

- **P1** retained ids recall bit-identical values; deleted ids no longer
  recall (first id 156673 caught a real bug — §7);
- **P2** distinct live claim values unchanged: 43,837 → 43,837;
- **P3** replay check and manifest verification pass after reseal;
- **P4** live count 157,650 − 112,481 = 45,169 exactly; every deletion has
  an audit event;
- **P5** all 2,657 conflict ids survive; no contradiction silently erased;
- **P6** semantic variants untouched by exact-dedup.

**Honest space accounting (P6b):** bytes went 1,897,740 → 4,147,360.
S5 deletion is tombstone + one 20-byte audit event per deleted fact
(112,481 × 20 B = 2,249,620 B — exactly the increase), while slot bytes are
retained. **Deleting duplicates with the current store does not reclaim a
single physical byte; it costs ~20 B/fact in audit log.** B/live-fact went
12.04 → 91.82. Logical cleanliness improves; physical bytes get worse.
Physical compaction is an unbuilt fork. The policy conclusion (§8) is
therefore *merge-on-add*, not *add-then-delete*.

## 6. Experiment 1 — is redundancy good for anything? (`run_exp1_p*.txt`)

Duplicate-rich store (157,650 facts) vs one-copy-per-claim store
(40,000 facts). Deterministic per-slot corruption at 1% and 5%;
plurality adjudication over **canonical** values; manifest re-verified.

| corruption | dup-rich survival | dedup survival | redundancy dividend |
|---|---|---|---|
| 1% | 99.35% | 98.98% | +0.37 pp |
| 5% | 97.11% | 95.02% | +2.09 pp |

- Manifest detects tampering in all runs (`manifest_after_corrupt=1`).
- Claims needing adjudication (≥2 distinct canonical values): 2,075 at 1%,
  7,069 at 5% — includes the 649 injected conflicts by design; the rest are
  corruption-induced.
- During the work an adjudication bug was found and fixed: plurality over
  *raw* values mis-scored wording variants as losses (ties between alias
  and canonical form). Canonical-form plurality is the correct rule, and is
  what the numbers above use.

**Reading:** redundancy buys *recovery* (manifest alone only *detects*).
The dividend is real but modest at low corruption rates — it does not
justify 4× slots for ordinary facts. It does justify replicated storage
for facts whose loss is unacceptable (see policy tiers).

## 7. Bugs found by this investigation (all fixed, all in-repo)

1. **Scanner rescan staleness**: `dd_scan()` did not zero class/count arrays
   on entry; `prove` mode's before/after scans accumulated stale counts.
   Fixed: explicit zeroing at function entry.
2. **`sc_seal_tail` double-seal resurrection** (store footgun): calling
   `sc_seal_tail` when the tail chunk is already sealed re-installed the
   chunk from the stale fill buffer, **silently resurrecting tombstoned
   slots** (caught by P1: deleted id 156673 still recalled). Fixed with a
   1-line idempotency guard (`if(n/cs < nsealed) return 0;`) in
   `src/s5_store.zag`. The committed canonical copy at
   `ops/storage-compression/adopt/s5_store.zag` does **not** yet have the
   guard — porting it is recommended (behavior is identical for all
   correct single-seal flows).
3. **Vacuous coordinated-lie run**: the first exp2 design's lie condition
   was arithmetically unsatisfiable — zero claims ever had ≥2 noisy
   sources, so both runs were byte-identical and the experiment tested
   nothing. Found by inspection, confirmed with an independent Python
   check, redesigned (noise 1/9 → 1/3, same rate both runs; only the
   *correlation* of errors differs). The old identical outputs are
   discarded, not reported.

## 8. Experiment 2 — corroboration vs dedupe-first (`run_exp2.txt`)

20,000 claims, 1–5 sources each from a pool of 50 (60,000 assertions),
per-source noise rate 1/3, single-valued relations only (10,005 claims).
Policy A: install iff ≥2 sources assert the identical triple (withhold
otherwise). Policy B: install the first assertion seen (dedupe-first).

**Independent noise** (noisy sources invent *different* false objects):

| policy | false installs | false rate | uncorroborated true misses |
|---|---|---|---|
| A (≥2 sources) | 0 | 0.00% | 2,994 |
| B (first-seen) | 3,402 | 34.00% | — |

Calibration: P(true | 1 source) = 22.7%; P(true | ≥2 sources) = **100.0%**
at 2, 3, and 4 sources.

**Coordinated lie** (same 1/3 rate, but all noisy sources assert the *same*
false object — a shared bad origin):

| policy | false installs | false rate |
|---|---|---|
| A (≥2 sources) | 2,401 | 23.99% |
| B (first-seen) | 3,402 | 34.00% |

Calibration under coordination: P(true | 2 sources) = **56.1%**,
P(true | 3) = 92.2%, P(true | 4) = 100.0%.

**Reading:** source-count corroboration is ~perfect against independent
errors and breaks under correlated errors — 2 agreeing sources are barely
better than a coin flip when they share a bad origin. Agreement is
evidence, not truth. The defense is not a higher count threshold but
**source-independence (provenance diversity) tracking**. Policy B
(dedupe-first / install-on-first-sight) is correlation-blind: 34% false in
both runs. Note the asymmetry: A withholds 2,994 true-but-uncorroborated
claims — the price of the 0% false-install rate, and exactly the
"withhold when evidence cannot resolve" behavior.

## 9. Limitations (stated plainly)

- The workload is **deterministic synthetic**, not the live ≥1 GB store:
  as of 2026-09-23 the ingest has produced extracted corpora
  (`knowledge/ingest_1gb/run/wiki.bin` ≈ 154 MB, `wn.bin` ≈ 12 MB) but
  **no installed `run/store/`**. Rerun the scanner against the real store
  when it exists.
- "Semantic" here means alias-canonicalization (known subject/relation
  aliases), not NLP paraphrase detection.
- Conflicts are modeled only on single-valued relations.
- Exp1 corruption is per-slot deterministic bit-flips within each sealed
  value's width — a model of bit-rot, not of adversarial tampering
  (which the manifest already addresses).
- The coordinated lie models *one* correlation structure (shared bad
  origin); real collusion can be subtler.

## 10. Reproducibility

`run.sh` rebuilds with the pinned toolchain and runs all five modes,
then byte-compares against the committed outputs. All committed outputs
are themselves second-run verified (byte-identical reruns).
