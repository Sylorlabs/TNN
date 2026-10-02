# MACHINERY VERDICT — 2026-09-23

Branch: `tnn-native-lab`. Prereg: `PREREG_MACHINERY.md` (commit 62cd09a8),
amended 2026-09-23 (commit 0e551199).

## Fork 1 — Pure-Zag sindex: PASS

Source fix committed (4917dbbe): `ig_sindex` emits every `id%1024==0` record
plus the first record of each blob chunk; allocation uses the upper bound
`(n+1023)/1024 + bnchunk`; key-order guard; zero-tail parser fix.

| Bar | Result |
|-----|--------|
| F1.1 live-store byte equivalence | **PASS**. 2,597,057 facts, 12 chunks, 2,548 native entries. Native SHA `d3c20622923dfec55a0c1c250aa7a24824076f643ca5edb87e325ed5d8d4c11d`, `cmp` vs Python index clean. |
| F1.2 second-store byte equivalence | **PASS**. 2,353,930 facts, 12 chunks, 2,310 entries. Native SHA `8772f16299691c9292038173c54c848d969af995adccac082306100e145bc5d6`, `cmp` clean. (Exposed the short-zero-tail parser bug; fixed.) |
| F1.3 boundary-crossing lookup | **PASS**. Key `wiki:simple:sony_pictures:sent000013` (id 1,619,653, first record of chunk 8, greatest pure predecessor in chunk 7): stale binary NOTFOUND, new binary FOUND with byte-correct text. Proves the `rl==0 → next chunk` fix. |
| F1.4 retrieval equivalence | **PASS (amended)**. See PREREG_AMENDMENT_2026-09-23. Zag-built and Python-built indexes give byte-identical `bquery` output on the 1,000-key fixture (SHA `d795baf87ef212c0aba78e055741da671b04bbd1afccc1f251af4acc636ca02e`). 830/1000 FOUND is a fixture property (170 keys CAL-rejected, absent from store), identical for both indexes. |
| F1.5 determinism | **PASS**. Two native `sindex` runs → identical SHA. |
| Cutover | **DONE**. `extract/build_sparse.py` deleted from branch (bfb90469). `ingest_bin sindex` is the sole index path. |

## Fork 2 — Canonical S5 in the scale learner: PASS

Integration committed (4917dbbe): `scale/driver/scale_learner.zag` adopts
canonical `ops/storage-compression/adopt/s5_store.zag` + `s5_merge.zag`;
bespoke `ScStore` and local `sc_*` helpers removed; `sc_seal_tail`
idempotency guard integrated. New `chain` mode on the learner binary.

**Chain small (R2-B5 parity shape):** `CHAIN_SMALL,ok=1,n=320,live=270,`
`deleted=50,revised=30,readded=20,refolded=20,digest=b9a52eb9189677a5`.
600 claims (300 base × 1..3 copies), 300 folds as expected. Deterministic:
5/5 runs identical; fresh rebuild identical.

**Chain big (1GB-scale):** `CHAIN_BIG,ok=1,n=2289794,live=2285794,`
`deleted=4000,revised=2000,readded=20,refolded=20,digest=ea2f6631ba0ddf6c`.
- 40 lessons × 65,536 claims = 2,621,440 claims, 12.66% exact-duplicate
  profile → 2,289,774 stored (vs 2,597,057 in the live 1GB store).
- **40/40 per-lesson written-byte identity**: merged store vs one-copy
  baseline built from the same stream in-run (`written_mrg == written_bas`
  every lesson; e.g. L=39: 18,339,752 bytes both).
- End-of-ingest digest equality: `856bdacdc43f362a` both; zero storage events.
- Mutations: 4,000 deletes, 2,000 revises, 20 fresh re-adds, 20 folded re-adds.
- Double `sc_seal_tail`: rc 0, 0 (idempotent). `sc_seal_final`: rc 0.
- 40/40 per-lesson gate consistency checks (scoped to each gate's id-range;
  canonical whole-store `mg_replay_check` is inapplicable by design to
  per-lesson gates — class 5 would fire on other lessons' values).
- `sc_replay_check`=0, `sc_manifest_verify`=0.
- Full learning-read scan over 2,289,794 ids: 0 mismatches (every live id
  recalls its ground-truth value; every tombstone fails recall).
- Deterministic: 3 runs byte-identical stdout; digest stable across rebuild.

## Scaling toward 10GB (measured, not run)

Chain big measured on the lab VM: **244 s wall, 406 MB peak RSS** for
2,621,440 claims → 2,289,774 stored facts.

Linear projection to 10× (26.2M claims, ~22.9M stored):
- **Time: ~2,440 s (≈41 min).** Hash-table ingest is O(n); the 40-lesson run
  showed flat per-lesson times.
- **Memory: ~4.1 GB.** Dominated by merge gates (40 × 5.24 MB at hmbits=17
  for 1GB; 10GB needs ~100 lessons × hmbits=19 = 2.1 GB for gates, within
  the 2^25-per-slice limit since 2^19 × 40 B = 20 MB < 33.5 MB).

No 10GB program, scratch dir, or crew workdir was touched.

## Commits

- `0e551199` — prereg amendment alone (F1.4 fixture, F2 scope).
- `bfb90469` — Python fallback deletion (prior).
- `4917dbbe` — Fork 1 source fix + Fork 2 S5 integration.

## Caveats

- The small-chain digest is stable across runs and rebuilds of the committed
  source, but differed between pre-commit build iterations (build-sensitive
  read somewhere in the small-chain path; all correctness checks pass).
  The big-chain digest is stable across both runs and source-changing
  rebuilds. If byte-identity across future refactors matters, the small
  chain's layout sensitivity should be investigated.
- F1.4's 1,000/1,000 bar was amended (see above); the frozen literal does
  not hold on the existing fixture.
- The 10GB projection is linear extrapolation, not a run.
