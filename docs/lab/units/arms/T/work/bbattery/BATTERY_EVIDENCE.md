# B-BATTERY EVIDENCE — Arm T (episode-aligned chunks), adjudication

**Date:** 2026-09-21 · **Crew:** marathon U10 · **Branch:** `tnn-native-lab`
**Frozen spec** (`units/PREREG_FREEZE.md` §3, extracted programmatically via
`grep`, never from memory):

> `| T — Episode-aligned chunks | STRUCT | Chunks = episodes; segmentation follows the episode clock (τ quiescence gap). | Any one: (i) B2 within 2× of X's on either corpus; (ii) >80% of battery recall queries address sub-episode spans (the "unit of experience" claim falsified); (iii) determinism gate fails; (iv) floor rule fires. |`

"**B-battery + X evidence**" (verdict sheet line 56) = run the Crew-4 shared
prereg battery (`units/ALPHABET_S-X.md`, "Shared prereg battery") for **T** and
for **X**, producing B2 (partial-recall cost) for both arms on both corpora,
the battery query-span distribution for (ii), and X's B2/B4/B5/B9 for the
universal floor rule (iv): *"any arm that fails to beat X on any of B2, B4, B5,
B9 is dead on arrival. Ties permitted on B1 (100% = 100%) and B7 (pass = pass)."*

## Battery design (frozen battery + crew decisions D1–D7)

- **Ingest (D2):** each corpus file ingested as ONE continuous intent → T: 1
  episode (id 1, base 0, len n); X: 1 stream unit (id 1). Matches T's M1
  ("1 episode, 0 boundaries by design") and ARM_SPEC ("Whole-file ingest = one
  continuous intent = one episode").
- **D1:** span schedules are fixed deterministic arithmetic (no RNG anywhere;
  the schedule is the measurement apparatus, not an AI decision path):
  B1/B4 `len=8+((i*7919)%4089)`, `off=(i*104729)%(n-4096)`; B9 `len=8+((i*104729)%4089)`,
  `off=(i*99991)%(n-4096)`; B5 edits `off=(i*31337)%n`.
- **D3 (B2 "bytes materialized"):** serving recall(span) touches the addressed
  unit(s); materialized = sum of touched unit sizes. T/X have one unit = whole
  corpus ⇒ materialized = n per query (ALPHABET: X "cannot [do] partial recall
  without touching the whole stream").
- **D4 (B4 reuse):** 2,000 spans × 2 sessions (session 2 repeats session 1);
  reuse = fraction of session-2 recalls served from the already-registered unit
  reference.
- **D5 (B5 blast radius):** 100 single-byte edits applied to the live store and
  re-verified; bytes re-keyed per edit = whole unit bytes (T: episode bytes
  re-keyed, ID stable; X: new stream ID, references re-keyed).
- **D6 (B9 composition):** 1,000 novel spans assembled from unit references;
  success = byte-exact assembly; cost = unit bytes touched per assembled byte.
- **D7 (ii):** a query "addresses a sub-episode span" iff `span_len < episode_len`,
  counted over B1 (10k) + B4-session-2 (2k) + B9 (1k) = 13,000 queries.
- **B1 gate:** every recalled span verified byte-exact against a FRESH
  ground-truth read (second file read, not the retained store). B9 verifies
  against ground truth with the 100 B5 edits applied (deterministic).
- **B7:** driver reruns each (arm, corpus) N=5; requires byte-identical stdout.

Program: `batt.zag` (pure Zag, struct-free; argv[1] selects arm `t`|`x`).
Driver: `run_battery.sh` (build → 20 runs → sha256 gate → ratios).

## Results (N=5 per config; all 20 runs byte-identical — B7 PASS)

| corpus | arm | n (bytes) | B1 | B2 (cost/byte) | B4 (reuse) | B5 (rekeyed/edit) | B9 ok | B9 (cost/byte) | sub-episode q |
|---|---|---|---|---|---|---|---|---|---|
| prose (pg100.txt) | T | 5,638,480 | 10000/10000 | 2747.0191 | 1.0000 | 5,638,480 | 1000/1000 | 2751.8177 | 13000/13000 = 100% |
| prose | X | 5,638,480 | 10000/10000 | 2747.0191 | 1.0000 | 5,638,480 | 1000/1000 | 2751.8177 | n/a |
| code (sqlite3.c) | T | 9,515,341 | 10000/10000 | 4635.7925 | 1.0000 | 9,515,341 | 1000/1000 | 4643.8905 | 13000/13000 = 100% |
| code | X | 9,515,341 | 10000/10000 | 4635.7925 | 1.0000 | 9,515,341 | 1000/1000 | 4643.8905 | n/a |

Run digests (sha256, 5/5 identical per config):
- t/prose `05ca17b078dd89d2109036f6cf4ddc6101c39c81e86a0fa4f774a3215961f254`
- t/code  `4dbca07a0891aaf2cec84b8c72cac4ac7ef379508983669873c5f1d7fd66e62b`
- x/prose `6766b99e8c9400639eebc4b02ffbb885c3551a86d3462563a5bf91c792779dac`
- x/code  `0203c6930ffb1163e9dfd31a44769df603a492e2fab9c7fc5f0303ed93effd49`

Raw outputs: `ev_{t,x}_{prose,code}_r{1..5}.txt` (20 files). Ratios: `VERDICT_NUMBERS.txt`.

## Kill-criterion evaluation (binding, frozen §3 row)

- **(i) B2 within 2× of X's on either corpus:** B2_T/B2_X = **1.000000** on prose
  AND on code (T's episode ≡ X's stream under single-file ingestion). 1.0 ≤ 2
  ⇒ **FIRES** on both corpora. (This is ALPHABET-predicted weakness W1,
  "code-corpus collapse", measured, not assumed.)
- **(ii) >80% of battery recall queries address sub-episode spans:** 13,000/13,000
  = **100%** (every battery span is 8–4096 B; episodes are 5.6/9.5 MB) ⇒ **FIRES**.
  The episode ID carries ~0% of addressing work on knowledge-sized queries: the
  "unit of experience" claim is falsified on this battery — T is X-with-offsets.
- **(iii) determinism gate fails:** M8 10/10 byte-identical (prior evidence) AND
  B-battery B7 20/20 byte-identical ⇒ **does NOT fire**.
- **(iv) universal floor rule fires:** T must beat X on **every** of B2/B4/B5/B9
  (ties permitted only on B1/B7). Measured: B2 tie, B4 tie (1.0 = 1.0),
  B5 tie, B9 tie — T beats X on **0 of 4** ⇒ **FIRES** on both corpora.

## BINDING VERDICT: **T — KILLED**

Kill criteria (i), (ii), and (iv) each fire independently on both corpora;
(iii) does not. Per RULE-7 (kill bars are BINDING; a fired bar kills — no
appeals), arm T is dead as a candidate. The finding is the one the frozen
prereg predicted: on single-file ingestion T degenerates exactly to X, and the
episode ID does no addressing work on knowledge-sized queries.

## X evidence (bonus, for X's record)

X's B-battery now exists (it had none): B1 10000/10000 both corpora; B2
2747.02 (prose) / 4635.79 (code) cost-per-byte; B4 1.0; B5 5,638,480 /
9,515,341 re-keyed bytes per edit; B9 1000/1000, cost 2751.82 / 4643.89.
X's own floor bars (A-44: retire X only if some arm beats it ≥10× on B2 AND B5)
are unaffected — X remains the floor.

## Build notes

- Pure Zag; zero RNG in any decision path; byte-identical reruns (N=5 × 4 configs).
- znc quirks honored: struct-free; `[]u8` arenas + `iput32`/`iget32` (ZNC-007 —
  no `as []i32`); `_zag_slice_ptr` for syscalls (ZNC-002); `return;` in void fns;
  no `};`; `_zag_arg` read unconditionally (ZNC-007/argc); no `@import`.
- Corpora read from `~/workspace/tnn-lab/corpora/{pg100.txt,sqlite3.c}`; each <
  2^24 bytes (one stripe, per the ≤2^24 convention).
- No binaries, `.zagd`, or `.zag-cache` committed (binary `batt_bin` is a local
  build artifact only).
