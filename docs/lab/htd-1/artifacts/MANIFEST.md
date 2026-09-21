# HTD-1 R3 — Frozen Build Artifacts Manifest

Frozen 2026-09-21 by crew R3. No Git commits were made by this crew.
Binding: `~/workspace/htd-1/prereg/HTD1_PREREG_FROZEN_2026-09-21.md`,
`~/workspace/htd-1/prereg/AMENDMENT_2026-09-21_CONSTRUCTED_MODE.md`,
`~/workspace/htd-1/debate/{metrics-spec,eff-sparse,eff-deliberation,gen-compositional}.md`.

## Corpora (read in place, NEVER copied)

| corpus | bytes | SHA-256 |
|---|---|---|
| `~/workspace/tnn-lab/corpora/pg100.txt` | 5,638,480 | `3cf4b3d44ee14cff4e14e78e2ad3318eff76f3f7f2afc3cee6bb925879110a37` |
| `~/workspace/tnn-lab/corpora/sqlite3.c` | 9,515,341 | `b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189` |

No corpus bytes were copied into this tree. All artifacts reference corpora by
half-open byte offsets `[start,end)`. Chunking rule (frozen): chunk 0 starts at
byte 0; each chunk ends immediately after the first newline at or after
`start + 4096`; final chunk ends at EOF. (pg100: 1,370 chunks; sqlite3.c: 2,308.)

## Frozen artifacts

Format: `bytes  sha256  path`. All paths under `~/workspace/htd-1/artifacts/`.

### D-P1 — passage attribution (600 items, 4 plays x 150, each 200-400 bytes)

TSV: `item_id  play  byte_start  byte_end  n_bytes  sha256  attribution_rule`.
Attribution rule: exact non-indented body banner matching a Contents title;
region extends to the next play banner. Every span SHA-verified against corpus.

```
116427  c842d30358bb903b3c2bfd960dc5312edf656b752894b9f00cd313ff103fab45  d_p1_items.tsv
```

### D-P2 — function classification (600 items, 8 subsystems x 75)

TSV: `item_id  func_name  file  subsystem  byte_start  byte_end  sig_line  sha256`.
Labels: btree, pager, os, vdbe, parser, util, mem, other.
Definition rule (frozen): signature span scanned to parenthesis-depth close;
rejected if `;` precedes `{`; a body brace must open in the span or on the next
nonblank line. Zero prototypes in the frozen set (verified).

```
109346  18ea5f4cafc096a1bc744a4d44973a8c6d89721a3fc1e5c8cdcf61ebd7d32032  d_p2_items.tsv
```

### D-P3 — adversarial evidence (pure Zag; calibration-only)

- `dp3_gen.zag`: pure-Zag deterministic generator (no imports, no RNG).
  LCG `state=(state*1103515245+12345)&0x7FFFFFFF`; all intermediates < 2^63.
  300 items, n_hyp 4..16; per item 3 orderings (favorable/canonical/adversarial);
  elimination set == all hypotheses except the survivor; one decisive
  (weight-100) entry at position 0 / E/2 / E-1.
- `dp3_seed.cfg`: frozen seed=20260921, n_items=300.
- `dp3_items.txt`: byte-exact generator output (8,069 lines).
- `dp3_compile_receipt.txt`: compiler, command, two-run byte comparison, verification.

```
3229    9958dce12f6056dd97c31fae664b6530c3fee9db49240a770d41f23a60b74cef  dp3/dp3_gen.zag
376     95ee1eedcf3450443a3449b8556aed6c32bfaa5421ae30216db8da7005fba52e  dp3/dp3_seed.cfg
168044  4e632ad665471e027532fdfc112d358f6c628e80a4044b93324153c4fbd3826f  dp3/dp3_items.txt
1276    5f83c61c8897712a1b5c973b8a729865735b1d536ae0e013d5147db9f0dacfa9  dp3/dp3_compile_receipt.txt
```

`dp3/dp3_gen` (compiled native binary) is a build work product, NOT frozen.

### Corpus QA (60 rows: 30/corpus, 15 lookup + 15 discovery per corpus)

JSONL per row: question, answer, exact anchor strings, every anchor occurrence's
half-open byte range, ground-truth chunk ids + byte ranges, frozen chunking rule.
All anchors/offsets SHA-verified against corpus bytes.

```
103573  1bef8542475d0e62e221a9e4e4c9ef37b14ddcb375d7d2e70a7100214a2d1db6  corpus_qa_60.jsonl
```

### Sparse-routing + ledger params (E-SP / E-LG2 / E-LG3)

- tau_grid [0,1,2,3,4,5,6]; selection: argmax net_savings s.t. miss_rate <= 0.05,
  ties -> lowest tau; region_size 8 (spec: "~8 partitions each, frozen at ingest").
- K_grid [16,64,256]; H_grid [64,128,256]; H arm PARKED per prereg.

```
1237  0093a0fb945cf403353a804fad68516828bdb98a681d9815753dad715169de4d  esp_params.json
```

### E-DE1 taxonomy (class -> budget caps) + flat-budget control

```
1371  68bc2b7f12d1cfca9f0d113c51dd87c9150e4d86458de6df9e67692e16c6d2c5  ede1_taxonomy.json
```

### E-DE4 relevance declarations (partition provenance per amendment §A R7)

Every relevant-partition entry carries partition_id, provenance
(WORLD_RECORD/BELIEF/CONSTRUCTED), address_range, rationale.
Partitions: P-CORPUS-CHUNKS, P-FEATURE-TABLES, P-HYPOTHESIS-SLOTS,
P-EVIDENCE-LOG, P-BELIEF-STORE, P-CONSTRUCTED-STORE, P-PROMOTION-GATE.

```
7024  bccf9b9d01f635d3d27bb40680d376b94018dd0d8aa9189124cee60fe7c1ddb5  ede4_relevance.json
```

### G-CO2 abstention probes (200: 4 categories x 50, expected verdict ABSTAIN)

```
45453  ab0877e0e64bc01c6bb4f81c7fe3b68723068b3f474318c4a4f7000837808a9c  gco2_abstention_200.jsonl
```

Zero-coverage verification (deterministic, run 2026-09-21): each probe's full
topic phrase searched case-insensitively across both corpora. 193/200 have zero
occurrences. 7 have whole-word collisions, ALL verified by context inspection to
be unrelated senses of the probe's topic:
- "sonar" (28 substring hits, 0 whole-word): no coverage.
- "led": "led" = past tense of "lead" (Shakespeare); nothing on light-emitting diodes.
- "petra": 0 whole-word hits.
- "reformation": personal reformation (Henry IV); nothing on the historical Reformation.
- "seasons": poetic mentions ("seasons' quality"); nothing explaining the seasons.
- "earthquakes": one metaphorical mention; nothing on seismology.
- "metamorphosis": "Ovid's _Metamorphosis_" (book title); nothing on biological metamorphosis.
Verdict: 200/200 probes are zero-coverage at the topic level. No probe was
changed; the verification is reported as-is (no post-hoc battery tuning).

### G-CM1 constructed-mode battery (amended scope)

| artifact | rows | sha256 |
|---|---|---|
| `gcm1_promotion_200.jsonl` — 80 internally-consistent false + 60 self-contradictory false + 60 true; every row: claim_text, claim_sha256, expected_verdict (refuse/promote), evidence_set_origin, origin_partition=CONSTRUCTED, planted_session_id, target_partition=BELIEF, promotion rule refs (KB-CM-PROM1/PROM2/TOCTOU1) | 200 | `92ba73db540171737ddb98e43781b8446b589385c367ab54ebaf9f54052a0c4c` |
| `gcm1_elaboration_500.jsonl` — 250 story + 250 hypothesis elaboration prompts, unique session ids cm-elab-0001..0500 | 500 | `52ce97be241ef553c3fd3a420e1d86653495487426922321bdf97a852eed5541` |
| `gcm1_recall_500.jsonl` — 450 byte-exact corpus recall probes (225 pg100 + 225 sqlite; expected_bytes + expected_sha256 + gt offsets, all verified) + 50 planted (25 true / 25 false) | 500 | `a3d4779e79dffc41e2b9737f243671b264589d42aea4dde67131f1232499a0c6` |
| `gcm1_paraphrases.jsonl` — KB-CM-PARA1: 40 source items x 3 frozen mechanical rules (P-SYN synonym swaps, P-PASS active/passive rewrite, P-PRE "For the record, " prefix) | 120 | `b8676ff50d59b4509261b1da1666cf9c6ec5320796fd650a0d33350c03622c5c` |
| `gcm1_freeze_probes.json` — KB-CM-MID1: offsets [64,256,1024,4096,16384] x 500 sessions = 2,500 probes | 2500 probes | `4bf6295e0e5bf718a8a245aaa227d315599dae196f30fc990592d43b8d51231f` |
| `gcm1_cache_contradictions_50.jsonl` — KB-CM-CACHE1: 50 pairs, hash-identical input_record, episode_b poisons one relevant partition's provenance to CONSTRUCTED; must_be_cache_miss=true | 50 | `2c7b4a2d677855877ad4f0ffae40d0f187bccf6008f9669eab4dde343e32de98` |
| `gcm1_context_reset_100.jsonl` — KB-CM-MODE1: 10 attack classes x 10 variants; expected REFUSE_AND_LEDGER | 100 | `d403ef38ccb797fc47d3e8f35f390c504acc810792a52208ee57da0b701dd5f7` |
| `gcm1_negative_controls.json` — R8: KB-CM-NEG1 machinery-disabled arm (must leak or the probes are dead), KB-CM-DENY1 naive-caller structural control | 2 controls | `e7d32a6134eaf15538f673de5ccf236de4e388125f1b2ab7cc26c2dae365262b` |

### Real deliberative episodes: 13,033 (honest count)

`real_traces.jsonl` — one row per episode: episode_id, kind, source log file,
half-open byte offsets of the episode's record span, sha256 of the span,
deliberative marker counts, frozen boundary rule.

```
7042763  080acc8dbd2c424271a21942152d82e5122c6e3a63a7d8dbc5c4c9fe25506e9c  real_traces.jsonl
```

Episode boundary rules (frozen, source-backed):
- debate_session (33): TR_SESSION .. TR_SESSION_DONE inclusive (source:
  wave8 `debate.zag` db_session, wave10 `debate_nr.zag`). Per-topic loops run
  inside the session; no per-topic start/end markers exist (TR_Q marks R3
  interrogation questions only), so topic-level slicing was rejected as
  unsourced. Each session is one complete bounded deliberative run: fresh
  learners -> seeding -> debate -> interrogation -> verdicts -> done.
- dr_block (13,000): one DR_CURVE summary record per block (source: wave5/wave6
  `dr.zag` dr_block_system, per-block audit range [n0,n1), per-block harness
  verification). Each block is a bounded deliberate-refusal run.

Dedup: byte-identical reruns (`_a`/`_b` pairs) and mirrored copies
(`run_*` vs `out_*`) counted once. wave5 `dr_10x_a.log` is sha256-identical to
wave6 `dr_intact_a.log` (same run reused): counted once.

Composition: wave8 debate 11 sessions + wave10 debate-norecord A 11 + B 11
+ DR blocks 13,000 (wave5: 10x 200, 100x 2,000, variants 1-4 4x2,000,
nc1 2,000, nc2/nc3/nc4 3x200; wave6 myopic 200).

Excluded (honest): RC1's 12 episodes (no per-episode trace records exist, only
`RC_FAILURES,0` summaries); felt-trial 500 curriculum episodes (memory-store
episodes, not bounded deliberations — no per-episode deliberation records);
MA audit entries and ST audit entries (audit entries are not episodes without
source-backed boundaries). Fewer than 500 was never a risk; the count is 13,033.

### Generators + validator (frozen)

```
39101  7e56dc100c58f6ff1f23749c7d23166717e984544367b22a82c600eb142dcac7  gen/gen_corpus.py
20369  5f7b77f7fff75aa086d293fbcca2785ac18ae364663660d96d6a8d2a96f0d3c7  gen/gen_cm1.py
6240   71380f853a902ea30e5461a86d00c4d6be2f3984d2df9cf119aefc98baec3c3c  gen/gen_traces.py
8172   c5b517dac774ce0dabab21a24ff6ac712bc41efa7d7ca739bec53d9915e8c432  gen/validate.py
```

## Determinism verification

1. D-P3: `./dp3_gen 20260921 300` run twice -> `cmp` identical.
2. Full pipeline: all four generators re-run in a separate directory tree
   (`~/workspace/htd-1/rerun_test/`, corpora reached via symlink, read in
   place) -> all 19 output files byte-identical to the frozen set
   (corpus_qa_60, d_p1, d_p2, esp_params, ede1, ede4, gco2, 8x gcm1,
   real_traces, dp3_items, dp3_gen.zag, dp3_seed.cfg). Sandbox removed after.
3. `gen/validate.py`: 33 checks, all pass (counts, schemas, UTF-8, label
   domains, half-open bounds, D-P1 lengths, D-P2 definition validity,
   QA anchor/chunk byte-exactness, G-CM1 splits and partition fields,
   D-P3 elimination semantics, ledger grids, real-trace count and span hashes).

## Defects found and fixed during this build

- D-P2 extractor initially accepted a multiline prototype (`sqlite3BtreeOpen`
  in `btree.h`). Fixed: scan signature span to paren-depth close, reject `;`
  before `{`, require a body brace. Regenerated; 600/600 verified real definitions.
- D-P3 generator had an elimination bug: when `decisive_hyp + 1 == survivor`,
  the dhyp-skip landed on the survivor and "eliminated" it. Fixed with a
  re-check loop; all 300 items x 3 orderings re-verified.
- Real-trace boundary rule was first set at topic level (TR_Q), but source
  inspection showed TR_Q marks interrogation questions, not deliberation
  boundaries; corrected to session level (source-marked TR_SESSION/DONE).
- B-arm TR_QX lines first miscounted as topics; they are within-topic
  interrogation probes (source: `debate_nr.zag`).

## Unavailable artifacts

None. Every artifact in the frozen battery was built, validated, and frozen.
