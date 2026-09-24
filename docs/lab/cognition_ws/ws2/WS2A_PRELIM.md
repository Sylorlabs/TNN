# WS2-A Preliminary Failure Map — 2026-09-24

Battery v1.1, 51 queries × 3 arms, 2 full runs byte-identical
(rebuild + ingest + choose + census + trace).
Evidence: `results/run1/out/` (trace + census SHAs in RUNLOG.md).
Trace format: `qid|kind|scheme|installed|candidate|lvl-matches|score|rank|top1|nret|outcome|fail_point`.
Self-consistency check (trace predicate vs topk predicate): 0 inconsistencies.

## How retrieval actually works (code-verified, lib.zag)

1. **No index.** Every query full-scans all n items (`topk` loops 0..n).
   "Navigation" is a per-item conjunctive predicate (`is_candidate`):
   at each scheme level, a non-empty hint must byte-equal the item field.
2. **Scheme = which levels are conjunctively gated**, not a tree:
   S1 type→domain→subject, S2 domain→type→subject, S3 subject→type,
   S4 type→subject→domain, S5 domain→subject→type, S6 subject-only,
   IMPOSED type→domain, FLAT none. Different schemes differ only in
   which hint fields can exclude an item.
3. **Scoring = exact token overlap** (lowercased, alnum-split) summed over
   query tokens. No stemming, no synonyms, no weights.
4. **top-k always fills to k** (score desc, id asc tie-break). No score
   threshold → a query matching nothing still returns k items at score 0.
5. **`filing.txt` is never read by retrieval** (write-only bookkeeping;
   `choose`'s `moves=33` is cosmetic). Only `items.dat` + `scheme.txt` matter.
6. **Dedup keeps the FIRST id** silently (`h_ingest`); the dropped twin is
   invisible downstream.

## Failure map

| # | Failure mode | Counts (51 q × arm) | Mechanism | Owning subsystem | Example probe IDs |
|---|---|---|---|---|---|
| F1 | Paraphrase → zero token overlap → gold scores 0 | 6/6 on ALL arms (18/18) | exact-token scoring; synonyms are different tokens | MORG scoring (`tok_count`) | QP01–QP06 (all arms) |
| F2 | Negative query → k junk items at score 0 (cannot abstain) | 6/6 on ALL arms (18/18) | `topk` fills to k with no threshold | MORG `topk` | QN01–QN06 (all arms) |
| F3 | Wrong domain hint → gold excluded at level 1 | 6/6 X1 + 5/6 X3 on IMPOSED (11) | conjunctive exact-hint gating; partition never visited | MORG `is_candidate` (hierarchical arms) | QX101–QX106, QX301–QX305 (imposed) |
| F4 | Duplicate-id twin silently dropped; query for dropped text returns the WRONG twin at rank 0 | 1 probe, all arms | `h_ingest` dedup keeps first; retrieval is id-keyed, content-blind | MORG ingest | QPD01 (PD01 installed = first text `2b167af0…`, query wanted second) |
| F5 | (no failure) aged vs recent: 10/10 both | 0 | no age/decay term exists — install position irrelevant | MORG (by absence) | QPA01–QPA05 vs QPZ01–QPZ05 |
| F6 | (no failure) same-category siblings coexist, individually retrievable | 0 | id-keyed store; no slot collisions in MORG | MORG (by absence) | QPC01–QPC10 |
| F7 | Blob-family clobber (cited, not re-run): D1 post-boundary offsets wrong → `sc_recall` fail-closed; D2 revise undercounts tail by 126 B → destroys unrelated fact | proven by KB-Control Crew A | blob writer `total` excludes inter-chunk padding | `knowledge/ingest_1gb` | crewA run1/run2, ROOTCAUSE_A.md |
| F8 | MA1 slot store: killed/pinned slots unreadable-by-design; retrieval is by slot address, no content query path exists | n/a (by design) | deliberate ops, audited | MA1 `memory_core.zag` | TRIAL_RESULTS_MA1.md 58/58 |
| F9 | CTX partitions: no cross-partition content retrieval path exists (partitions hold regime belief only) | n/a (by design) | deliberate scoping | `wave2/posttable/ctx` | ctx_core.zag |

## Arm contrasts (same battery)

- **FLAT**: 39 FOUND / 6 TOKEN_MISS / 6 FALSE_POSITIVE. Hints ignored; never
  gate-fails (F3 absent); weakest on paraphrase/negatives.
- **IMPOSED**: 28 FOUND / 17 NOT_RETRIEVABLE / 6 FALSE_POSITIVE. Strictest:
  wrong-hint queries gate-fail (F3); 3 of 6 X1 queries abstained cleanly
  (nret=0), 3 returned 1 junk candidate.
- **SELF**: 39 FOUND / 6 TOKEN_MISS / 6 FALSE_POSITIVE — identical outcome
  profile to FLAT. Cause: `choose` picked **S6 for every domain and global**
  on this corpus (scheme.txt: 6× `chosen: S6`). S6 = subject-only gating,
  so a wrong *domain* hint only selects the scheme, then is ignored by the
  gate — X1 queries that IMPOSED rejects, SELF answers. Scheme choice is
  itself a retrieval-behavior switch, invisible unless traced.

## NOT_INSTALLED vs NOT_RETRIEVABLE separation (held)

- Census (id|textlen|sha8) pre/post run: identical SHA
  `6c257346…` across all 3 arms — install set fixed; no mutation.
- Only NOT_INSTALLED-by-fixture is QPD01's second text (DEDUP_DROPPED);
  every other miss is NOT_RETRIEVABLE with a traced fail point.
- CONTENT_CHANGED: none observed (no mutating ops in battery).

## Determinism

Zero RNG anywhere. Run1 vs run2 (full rebuild from clean dirs):
census ×3 and trace ×3 all byte-identical. SHAs in RUNLOG.md.
znc lessons honored: []u8 arenas + u32 accessors only, no `.*` on locals,
no `as []i32` casts, no stray `};`, `i64s()` newline-strip at call sites.
