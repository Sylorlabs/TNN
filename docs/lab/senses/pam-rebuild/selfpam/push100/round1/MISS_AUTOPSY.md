# Self-PAM push-to-100% — Round 1 miss autopsy

**Date:** 2026-09-27 · **Crew:** round-1 autopsy · **Gate:** `selfpam-fact-gate` (candidate id 2)
**Corpus:** R2P 1,200 pairs, frozen seed 20260923 · **Baseline:** 1,099 / 1,200 withheld (91.58%)

## Verdict up front

All **101 admitted pairs are genuine should-withhold misses. Zero correct admits.**

- The preliminary finding is **confirmed** on the 100 motiondir pairs: every one is a
  `reversed` pair (even pair index), and the mechanism is exactly as suspected —
  the candidate's byte-sum judgment is permutation-blind, so the reversed F blob
  scores identically to the forward G blob.
- The preliminary finding is **corrected** on the 101st pair: the colordisc
  `illuminant-drift` admit (ledger idx 135, truth=SAME) is **not** a correct admit.
  It is a real miss by a second, distinct mechanism — an exact byte-sum collision
  between two different renderings. The reference gate withholds it, the generator
  certifies its F as fooled, and the program's bar has no truth-based carve-outs.

## How this was verified (independent reproduction)

1. Parsed the committed ledger `ledger_selfpam_r1.txt` with fresh code: **1,099
   withheld / 101 admitted**, matching the admission report's `pairs_withheld=1099`.
2. Verified the three runs are byte-identical entry sequences (r1/r2/r3 ledgers share
   md5 `3b1fe7145677a7a41b83480f94feff76`).
3. Recomputed every ledger judgment from scratch in Python — `span_sum` = raw byte
   sum mod 2^31, judgment = `span_sum // 8` — over the actual F/G bytes of all 1,200
   pairs: **0 mismatches / 1,200**. The ledger is faithful to the bytes, and the
   measurement behaves exactly as the Zag source says.
4. Verified corpus integrity: all 1,200 `.pair` files in the working corpus match the
   committed `MANIFEST.r2p.sha256` (**1,200/1,200**), covering both the 600 committed
   pairs and the 600 regenerated from the frozen generator.
5. Proved each miss's F/G byte relationship at byte level (see mechanism proofs below).

Note on ledger fields: each entry is `e <idx> <jf> <jg> <0|1> <hash>` — the admit/withhold
flag is the **5th** whitespace-separated field (0 = admitted, 1 = withheld); `jf`/`jg`
are the two span judgments.

## Per-task results

| Task | Pairs | Withheld | Admitted |
|---|---|---|---|
| colordisc | 200 | 199 | 1 |
| colorconst | 200 | 200 | 0 |
| shapetrans | 200 | 200 | 0 |
| pitchdisc | 200 | 200 | 0 |
| timbredisc | 200 | 200 | 0 |
| motiondir | 200 | 100 | 100 |
| **Total** | **1,200** | **1,099** | **101** |

Admitted ledger indices: 135, then 1000, 1002, 1004, …, 1198 (all 100 even indices of the motiondir block).

## Mechanism taxonomy

Two mechanism classes, both **gate-measurement limitations** (the corpus is doing its
job in both cases — every F below is generator-certified fooled, every G certified clean).

| Class | Name | Count | Verdict |
|---|---|---|---|
| A | Permutation-blindness (frame-reversed video) | 100 | MISS × 100 |
| B | Exact byte-sum collision (illuminant rendering) | 1 | MISS × 1 |

### Class A — permutation-blindness (100 misses, all motiondir / note=`reversed`)

**Causal chain.** The generator (`gen_r2p.py::r2p_t5`, mode 0 = even pair index) builds
F as the G frame list in exact reverse order: 50 distinct 24×24 frames, identical 8-byte
payload header. Proven for all 100 admits: `F_frames == G_frames[::-1]` byte-for-byte
(100/100; the reversal is nontrivial — all 50 G frames distinct in the sampled pair).
The candidate's judgment is `span_sum(evidence)/8` (`codec.zag::span_sum` — raw byte sum
mod 2^31), which is **order-blind**: a permutation of bytes has the identical sum. So
`sum(F) == sum(G)` exactly (e.g. pair 0: 12,170,466 both sides), `jf == jg` exactly
(e.g. 1521308), and the instrument admits. The ÷8 tolerance plays no role — the sums are
exactly equal, not merely in the same bucket.

**Why it is a miss, not correct behavior.** The reversed F genuinely depicts a different
motion direction than G (the naive front-end reports the wrong direction on F — that is
what "fooled" means here, asserted at generation time). The gate's job is to catch that
the formation measurement is corrupted relative to the independent re-measurement. A
byte sum cannot see order, so the corruption passes through.

**Classification:** gate-measurement limitation. Not a corpus artifact (the pair is a
legitimately fooled pair), not correct behavior.

### Class B — exact byte-sum collision (1 miss: ledger idx 135, colordisc_135, note=`illuminant-drift`)

**Causal chain.** Pair 135 is a mode-1 (odd index) colordisc pair: F renders the base
color under two illuminants (left half d65, right half warm), G renders it uniformly
under d65. Byte anatomy of one frame (60 identical frames per span):

- F left-half pixel (d65): `(48, 167, 159)`, per-pixel channel sum **374**
- F right-half pixel (warm): `(137, 155, 82)`, per-pixel channel sum **374**
- G pixel (d65): `(48, 167, 159)`, per-pixel channel sum **374**

The warm illuminant's per-channel gains on this particular base color happen to net to
zero after rounding (+89 R, −12 G, −77 B = 0), so the two *different* renderings have
*exactly* the same per-pixel byte sum. Per-frame sums: 47,872 both sides. Total:
`sum(F) == sum(G) == 2,872,404` exactly → `jf == jg == 359050` → admit. The F/G bytes are
neither identical nor a permutation (`byte_relationship = distinct-content`) — this is a
pure aggregate-statistic collision. Critically, the ÷8 tolerance is **not** the cause:
tightening the tolerance to 1 would not fix this pair.

**Why it is a miss, not a correct admit.** Three independent grounds:
1. The generator certifies this F as fooled (naive front-end reports DIFFERENT, truth
   is SAME) and this G as clean — the pair was built to be withheld.
2. The reference gate withholds 1200/1200, including this pair.
3. The program's bar (B5, VERDICT_R2-3) counts withholds over all 1,200 pairs with no
   truth-based carve-outs: "every R2P F is verified fooled and every G verified clean
   at generation time." A "truth=SAME ⇒ correct admit" category does not exist in this
   battery.

**Classification:** gate-measurement limitation. Not a corpus artifact, not correct behavior.

## Fixable vs information-theoretic

| Class | Fixable? | Reason |
|---|---|---|
| A permutation-blindness | **Fixable** | The distinguishing information (frame order) is present in the bytes; the measurement discards it. Any order-sensitive judgment (position-weighted sum, byte-sequence hash — note `codec.zag` already ships `fact_evhash`/SHA-256) separates all 100. |
| B sum collision | **Fixable** | The distinguishing information (different pixel values) is present in the bytes; the sum collides. A collision-resistant measurement (e.g. SHA-256 over the span) separates it. Merely tightening the ÷8 tolerance would **not** fix it — the sums are exactly equal. |

Neither class is information-theoretic: in both cases the F/G bytes contain the evidence
needed to tell them apart. The limitation is entirely in the `span_sum` aggregate. The
common root cause is one sentence: **the SPAN-SUM family claim is insensitive to
rearrangements and sum-preserving content changes, and the R2P corpus contains both.**

## What is NOT implicated

- **The ÷8 tolerance** — neither class needs it; both collide exactly.
- **Corpus integrity** — 1,200/1,200 pair SHAs match the committed manifest; ledger
  judgments re-verified 0/1,200 mismatches against the actual bytes.
- **Determinism** — 3/3 runs byte-identical ledgers and reports.
- **Other tasks** — colorconst, shapetrans, pitchdisc, timbredisc: 0 admits (800/800 withheld).

## Notes for the fix crew (not enacted here)

- Any replacement judgment must separate (a) all 100 frame-reversals and (b) the
  illuminant sum-collision, while keeping the 1,099 current withholds and the 3×
  byte-identical determinism. `miss_table.tsv` in this directory is the regression list.
- `fact_evhash` (SHA-256 of the evidence bundle, already in `codec.zag`) separates both
  classes trivially — but changing the judgment changes the gate's declared claim
  semantics (TECH_BRIEF §5 item 4), so that is a design decision for the fix round, not
  taken here.
- Watch for overfitting to these two instances: the general defects are
  "order-blindness" and "aggregate collisions," not "motiondir" and "colordisc_135."

## Provenance (every number → its source)

| Number | Value | Source file (repo-relative) | Git blob SHA |
|---|---|---|---|
| Baseline withheld/admitted | 1099 / 1200 (91.58%) | `docs/lab/senses/pam-rebuild/round2/forks/R2-3/evidence/admission_report_selfpam_r1.txt` | `969aba52dbec10baa363320512b5929cb9eba291` |
| 101 admitted indices | § per-task table | `docs/lab/senses/pam-rebuild/round2/forks/R2-3/evidence/ledger_selfpam_r1.txt` (r2/r3 byte-identical) | `dfaf242955ae7487ce7a176046c6965005e31ec7` |
| Reference gate | 1200 / 1200 (100.00%) | `docs/lab/senses/pam-rebuild/round2/forks/R2-3/evidence/admission_report_reference_r1.txt` + `ledger_reference_r1.txt` | `3a509419abe12331607ca145d1aea6454874fe3e` / `ffe97a7ea19a71fe629d7c4e1cccbe545dffcc52` |
| Gate definition (span_sum/8) | — | `docs/lab/senses/pam-rebuild/selfpam/src/g1_candidate.zag`, `.../src/codec.zag` | `8991ad51c54559b2b883e3ddb0388f3bd4b0040c` / `0b3218793c1cb55c524421e05c4b8d4560505b65` |
| Corpus manifest (1200 SHAs) | 1200/1200 verified | `docs/lab/senses/pam-rebuild/round2/fixtures/r2p/MANIFEST.r2p.sha256` | `33b5fc5d9787011bbf1161c64350ce3ee5e9cddb` |
| Pair construction / fooled-clean asserts | — | `docs/lab/senses/pam-rebuild/round2/fixtures/gen_r2p.py` (frozen seed 20260923) | `3567ed980cdc4c1172dc549a58e2df4588c64921` |
| Truth oracle (per-pair) | `*.pair.truth` | `docs/lab/senses/pam-rebuild/round2/fixtures/r2p/` (1200 files, committed) | per-file (see manifest dir) |

Analysis scripts that produced `miss_table.tsv` from the above: `scripts/analyze_admits.py`
(ledger parse + full 1,200-pair judgment re-verification), `scripts/prove_mechanisms.py`
(byte-level mechanism proofs), `scripts/build_miss_table.py` (final table from the
committed truth oracle). All deterministic, zero RNG.
