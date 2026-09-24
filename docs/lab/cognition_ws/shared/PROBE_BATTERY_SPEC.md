# WS2 Probe Battery Spec — Memory Retrieval White-Box Investigation

**Status:** FROZEN (preregistered 2026-09-24, before any probe execution).
**Owner:** WS2-A (white-box investigator). **Consumers:** WS2-B (ToC scheme crew),
WS2-C (self-found scheme crew) — same battery, same corpus, same verdict rules.
**Corpus:** `cognition_ws/ws2/fixtures/probe_corpus.txt` (self-contained;
does NOT reuse `memory_org/corpus.txt`).
**Queries:** `cognition_ws/ws2/fixtures/probe_queries.txt`, 8-field format
`qid|split|class|thint|dhint|shint|text|gold` (same as `memory_org/queries.txt`).

## 0. Scope

White-box investigation of where TNN memory retrieval fails TODAY.
Instrumented in pure Zag, zero RNG, byte-identical reruns. We distinguish
four terminal outcomes per probe:

| Outcome code | Meaning |
|---|---|
| `FOUND` | gold id present in returned top-k **with score > 0** |
| `NOT_INSTALLED` | gold id absent from the store at query time (never ingested, dedup-dropped, evicted, clobbered) |
| `NOT_RETRIEVABLE` | gold installed, but the retrieval path cannot surface it (partition gate, token miss, rank past k — **including** a gold that appears in top-k only by id tie-break at score 0: the path produced no evidence for it) |
| `FALSE_POSITIVE` | negative probe: store correctly holds nothing, but retrieval returned items anyway |

"Lookup can't find it" (`NOT_RETRIEVABLE`) is always separated from
"it was never installed / was overwritten" (`NOT_INSTALLED`) by an
installation census taken immediately before the query run.

## 1. Probe classes

### P-AGE — recent vs aged facts (install-position bias)
- 10 items: `PA01..PA05` (sort first → installed first = "aged"),
  `PZ01..PZ05` (sort last → installed last = "recent"). Same type/domain,
  disjoint distinctive keywords per item.
- 10 queries, one per item: exact-witness text ("show me FACT items about
  <keyword> in <domain>"), hints exact.
- **Hypothesis:** MORG scoring has no age/decay term; aged and recent must
  retrieve identically. Any asymmetry = install-order bias (fail closed).
- Verdict: per-item FOUND; class verdict FAIL if any item differs by install
  position, with the position recorded.

### P-COLL — cross-slot / clobber family
- **C1 same-category siblings:** `PC01..PC10`, all `FACT|physics|gravity`,
  unique text each ("fact alpha one about gravity pull strength 10", …).
  10 queries, one per item, by unique tokens. Verdict: all 10 FOUND and
  byte-identical pre/post run (no silent overwrite).
- **C2 duplicate-id ingest:** two corpus lines share id `PD01` with different
  text. MORG `h_ingest` keeps the first, drops the second silently.
  1 query for the second line's text. **Expected outcome: NOT_INSTALLED**
  (distinguished from a lookup failure by the census). If the scheme crews
  later want overwrite semantics, this class detects the change.
- **C3 blob-family (knowledge/ingest_1gb):** root-caused by KB-Control Crew A
  (evidence `knowledge/kb_control/crewA/run1`, `run2`; ROOTCAUSE_A.md):
  D1 — post-boundary slot offsets miscounted → `sc_recall` fail-closed
  (`NOT_RETRIEVABLE`, wrong accounting); D2 — revise undercounts tail by
  126 bytes → silently destroys an unrelated fact (`NOT_INSTALLED`,
  overwritten). WS2-A cites their proven geometry; no re-run unless the
  store changes.

### P-CTX — cross-context / partition facts
- 6 items: `PX01..PX06` in distinct (type,domain,subject) triples.
- **X1 wrong-hint gate (IMPOSED/S1-style hierarchical arms):** query carries a
  `dhint` that mismatches the item's true domain. Expect `NOT_RETRIEVABLE`
  with fail point `PARTITION_GATE` (exact-hint matching excludes the gold
  at level 1). This is partition-blind lookup: the fact exists, the path
  never visits its partition.
- **X2 hintless queries (all arms):** same items, `thint/dhint/shint` empty,
  pure-text queries. Expect FOUND via the global token path (FLAT) —
  measures what hintless search recovers when navigation is blind.
- **X3 scheme-mismatch (SELF):** query `dhint` selects a per-domain scheme
  in `scheme.txt` whose level order excludes the gold's levels; records
  which scheme was selected per query.
- CTX partitions (`wave2/posttable/ctx/ctx_core.zag`): by design only the
  active partition's regime belief is visible; there is no cross-partition
  content retrieval path. Recorded as by-design scoping, not a failure —
  flag if a scheme crew ever needs cross-partition recall.

### P-PARA — paraphrased queries
- 6 items `PP01..PP06` with canonical wording; 6 queries restating the same
  need with **zero exact-token overlap** against the item text (synonyms,
  reordering; verified by a token-overlap check in the harness — a query
  that accidentally shares a token is rejected at build time).
- Expect `NOT_RETRIEVABLE` with fail point `TOKEN_MISS` (MORG scores exact
  token overlap only; no stemming, no synonyms). Documents the vocabulary
  gap, the dominant failure mode for natural phrasing.

### P-NEG — negative probes (correctly NOT found)
- 6 queries for topics verified absent from the probe corpus by grep at
  build time (`submarine ballast`, `quantum tunneling`, `origami crane
  folding`, `beekeeping smoker`, `sourdough discard pancakes`,
  `lunar regolith sintering`). `gold` field empty.
- **Expected correct behavior:** empty result set. MORG `topk` always
  returns up to k candidates even at score 0 → expect `FALSE_POSITIVE`
  on all 6 (the mechanism cannot say "not found"). A future scheme that
  can abstain must flip these to clean empties.

## 2. Arms under test

- `FLAT` (kind=2): append-only, global token scoring, no navigation.
- `IMPOSED` (kind=1): fixed `type→domain` hierarchy, exact-hint gating.
- `SELF` (kind=0): `choose` picks per-domain scheme on calib queries, then
  retrieve; scheme selection is itself part of the path and is traced.

## 3. Instrumented trace (per query, one line)

`trace.txt` (TSV), emitted by the pure-Zag probe driver:

```
qid | arm | scheme | gold_installed(0/1) | candidate(0/1) |
lvl0_match lvl1_match lvl2_match | gold_score | gold_rank(-1=absent) |
top1_id | outcome | fail_point
```

`fail_point` vocabulary: `NONE`, `NOT_INSTALLED`,
`DEDUP_DROPPED`, `PARTITION_GATE_L0/L1/L2`, `SCHEME_MISMATCH`,
`TOKEN_MISS`, `RANK_PAST_K`, `FALSE_POSITIVE`, `CONTENT_CHANGED`.

The driver reuses `memory_org/arms/lib.zag` retrieval primitives
(`build_tab`, `build_hay`, `is_candidate`, `tok_count`, `scheme_level`,
`gold_ids`) and adds tracing — no behavioral changes to the scored path
(the trace loop and the scored `topk` loop share the same predicate code;
a differential check asserts trace `candidate` == `topk` candidate set and
trace `gold_score` == `topk` score for every query).

## 4. Determinism contract

- Zero RNG in corpus, queries, driver, scoring. Ingest order fully
  determined by id sort inside `h_ingest`. Two full runs (rebuild +
  ingest + trace) from clean dirs must be byte-identical; SHA-256 of
  `trace.txt` + `census.txt` + `verdicts.txt` recorded in RUNLOG.md.
- No binaries or `.zagd` files committed. Pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- znc codegen lessons honored: `[]u8` arenas with explicit u32 accessors
  (no `as []i32` tables), 8-byte struct field stride, no `.*` on
  non-pointer locals, no single slice ≥ 2^25 bytes.

## 5. Battery freeze

Corpus and query files are frozen at the commit recorded below; any later
edit is a new battery version (bump `battery_version` in the files'
header line, re-freeze, re-run everything).

**Battery version:** v1.1
**Version history:**
- v1 — initial freeze. Frozen commit:
  `df0ea3ecf5c1377762c072f0476eb18abcbd9305` (committed before any run).
- v1.1 — query-file header comment contained 7 pipes and parsed as a
  phantom 52nd query; header rewritten, zero query bytes changed,
  validator re-passed. Runs executed against v1.1. Frozen commit:
  _(filled right after commit)_
