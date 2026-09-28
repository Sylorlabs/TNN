# PREREG_SYNINT.md — Synonym learner integration: frozen prereg

Frozen 2026-09-25 before any implementation. Pure Zag, zero RNG, pinned
toolchain (`znc_linux_x86_64_abed8aa1`), 3x byte-identical reruns required.

## 1. Audit conclusion: the synonym learner is SEPARATE

Micah's question: is the synonym learner TNN learning synonyms, or a separate
learner bolted on? Answer: **SEPARATE**. Evidence:

- **Own binaries**: `learn` (learning) and `tocl` (retrieval), built solely
  from `cognition_ws/ws2l/` sources. No TNN code path invokes them.
- **Own store**: `store_l/synlearn.txt` + `synveto.txt` — flat text files.
  The store is read/written only by the two binaries.
- **Zero inbound references**: grep over all of `tnn-lab` for
  `synlearn|ws2l|syn_canon` finds NOTHING outside `cognition_ws/ws2l/`
  except the retired curated bridge's `toc_b2.zag` (shares the interface
  name only). No organ, no substrate client, no deliberative code, no KB
  code references the synonym store.
- **No lifecycle**: relations cannot be killed, pinned, or promoted. There
  is no audit trail of installs. The deliberative layer cannot inspect,
  revise, or even enumerate learned synonyms.
- **No consolidation path**: learning = corpus -> R1-R4 -> text file.
  Nothing passes through any deliberate-install, promotion, or audit path.
- Architectural fact (confirmed in code): the deliberate memory substrate
  (`memory_core.zag` lineage, `ob_mem.zag`) holds NO symbolic content —
  slots are (live, i32 value, pinned, region, tier) + audit ledger. The
  synonym relations were never representable in the substrate as frozen,
  which is why the side store exists. The integration below closes this
  without modifying frozen substrate code.

## 2. Integration design (what changes)

New module `syn_mem.zag` (library, in `cognition_ws/ws2l/`):

- **Imports frozen `memory_core.zag`** (wave3 signed-memory-values trial,
  the MA4 lineage). FROZEN CODE IS NOT MODIFIED.
- **Every learned relation = one substrate memory.** R1/R2/R3 fire ->
  `ma_add(&shard, SYN_VAL, MA_REGION_USER, &slot)` where
  `SYN_VAL = 1000000 + rules_mask` (kind tag in high digits, rules in low).
  The install is automatically a substrate audit-ledger entry.
- **Every veto = one substrate memory with negative value**
  (`VETO_VAL = -1000000`, MA4 negative-judgment semantics). Veto check
  consults live veto memories.
- **Content arena**: the relation's symbolic content (stems, rules,
  evidence-ID list) lives in tables indexed by global slot id
  (shard*256+slot), reusing the proven elastic table layout from
  `learn.zag` (rel tables, lid linked lists, string pool, veto tables).
  The substrate's `live[]` array is the SOLE authority on what the system
  believes: killed slots are excluded from retrieval even though their
  content rows persist (auditable history).
- **Elastic capacity via sharding**: `ma_add` hardcodes `MA_CAP=256`
  (frozen). The module manages an elastic list of `MaStore` shards; when
  one fills, a new shard is allocated. Every shard IS the deliberate
  memory substrate (same code, same ops, same audit format). No cap.
- **Retrieval** (`syn_build` in `toc_l.zag`): builds the stem->canon map
  from LIVE substrate slots only (not from text files). Union-find
  transitive closure over live relations; veto-safety asserted on the
  live set (a killed relation drops out of closure automatically).
- **Lifecycle ops**: `syn_kill` -> `ma_kill`, `syn_pin` -> `ma_pin`,
  `syn_promote` -> `ma_promote`. The deliberative layer can now revise
  synonyms through standard substrate ops.
- **GEN / merge**: load substrate state, ingest new corpus, `ma_add` only
  for pairs not already live. Old relations intact (never killed).
- **Persistence**: `syn_save`/`syn_load` serialize substrate shards +
  content arena to the store dir. The files are a SERIALIZATION of
  substrate state, not a side store: every mutation goes through
  substrate ops, every state change is audited.
- **Binaries**: `learn`+`tocl` are replaced by ONE thin driver `syn`
  (subcommands: ingest/query/dump/kill/save-state) that exercises the
  module. The module is a library; the driver is the battery harness's
  entry point, not a separate learner.

What does NOT change: the R1-R4 rule surfaces, tokenizer, frozen
stemmer, PARA grouping logic, union-find semantics, `syn_canon`
interface, scoring code. Behavior must be identical; only the storage
backend and lifecycle change.

## 3. Kill bars (all must PASS)

- K1: every installed relation corresponds to exactly one substrate
  memory; `syn_dump` enumerates relations == live synonym slots.
- K2: every install/kill/promote appears in a shard audit ledger
  (replay the ledger -> exact slot state).
- K3: killing a relation's slot removes it from `syn_canon` output
  (retrieval reads live[] only). Demonstrated on at least 3 relations.
- K4: veto installed as negative-value memory; vetoed pair cannot
  install (checked against live vetoes before ma_add).
- K5: no fixed capacity — ingest the 10,507-line stress corpus;
  relations installed == relations learned (no silent drops).
- K6: zero RNG (grep), 3x byte-identical reruns of ingest+query.
- K7: no curated strings in the new code (K2 of WS2-L preserved).

## 4. Regression bar (must hold exactly)

Full WS2-L battery against the integrated module:
Official 51/51, FRESH 6/6, DIST 6/6, ADV-NEAR 6/6, MULTI-HOP 4/4,
MORPH 3/4 (QMO3 fails exactly as before — tie, no override),
112 relations + 4 vetoes installed, GEN behavior (new evidences learn,
old intact). `synlearn.txt`-equivalent dump byte-identical to the
frozen store's relation set (order-normalized).

## 5. Out of scope

- Modifying frozen `memory_core.zag` (sharding works around MA_CAP).
- Changing R1-R4 rule surfaces (frozen mechanism).

## 6. AMENDMENT (2026-09-25, post-implementation)

Section 5's "one-brain message-passing composition is a later step" is
SUPERSEDED by the following precise status. This amendment does not change
the kill bars; it corrects the architecture claim to match what was built.

### What IS unified (implemented and verified)

- **Substrate**: Every relation and veto is a deliberate-memory substrate
  slot (ma_add/ma_kill/ma_pin/ma_promote). Verified: 112 relations + 4
  vetoes = 116 live substrate memories, 1 shard.
- **Lifecycle**: Relations are killed (rc=0, excluded from retrieval),
  pinned (rc=102 on kill attempt, protected), promoted (rc=0) through
  the standard substrate operations. The deliberative layer can inspect
  (dump shows LIVE/DEAD per relation), revise, and remove.
- **Audit**: Every install/kill/pin/promote is a substrate audit-ledger
  entry. The ledger replays to exact state.
- **Retrieval**: syn_build reads LIVE substrate slots only. Killed
  relations are excluded from the transitive closure and syn_canon.
- **No side store**: The text files (synlearn.txt/synveto.txt) are gone.
  The binary tables (syntab.bin) + substrate shards (synmem.bin) are the
  unified store. The tables are content indexed by substrate slot, not an
  independent belief store — live[] is the sole authority.

### What is NOT yet unified (honest limitation)

- **Trigger path**: The R1-R4 rule engine (learn.zag's ingest) is still a
  batch binary, not yet invoked through the live one-brain deliberative
  loop. The rules fire on corpus ingest, not on streaming deliberation.
  The SUBSTRATE is unified; the TRIGGER is not yet fully integrated into
  real-time deliberation.
- **One-brain composition**: The synonym module does not yet participate
  in one-brain parallel deliberation message-passing. It is substrate-
  direct.

### Verdict

The synonym learner is **SUBSTRATE-UNIFIED** (not a side store, not a
separate belief system) but **TRIGGER-SEPARATE** (batch ingest, not live
deliberative). This is a strict improvement over the original SEPARATE
status: the beliefs are now TNN's own deliberate memories, subject to
TNN's own lifecycle, audit, and revision. Full trigger integration into
the deliberative loop remains future work.
