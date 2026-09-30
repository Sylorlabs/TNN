# Database Baseline for C2 Machine-Native Stress Test

## Verdict: DB-BASELINE-COMPLETE

**Date:** 2026-09-30
**Method:** Implemented all 7 query types from PREREG_MNSTRESS1.md in SQLite.
This is a BASELINE, not a TNN mechanism. SQL is the tool.

## What was built

**Files:**
- [schema.sql](sandbox://workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/db_baseline/schema.sql) (68 lines): 6 tables with indexes
- [gen_world.sql](sandbox://workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/db_baseline/gen_world.sql) (139 lines): synthetic world generation
- [queries.sql](sandbox://workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/db_baseline/queries.sql) (81 lines): all 7 query types
- [world.db](sandbox://workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/db_baseline/world.db) (828KB): the database

**Total:** 288 lines of SQL. Zero Python. Zero em dashes.

**World scale (matches prereg structure):**
- 1000 entities, 240 sources, 8600 claims (6000 base + 500 contradictions + 60 supersessions + 40 corrections + 2000 junk)
- 5000 relationship claims, 100 derived beliefs, 500 contested slots

## The 7 query types in SQL

| Query | SQL construct | Result |
|-------|---------------|--------|
| Q1 current belief | `SELECT ... ORDER BY seq DESC LIMIT 1` | Works |
| Q2 provenance | `JOIN sources`, filter by value | Works, exact claim-id sets |
| Q3 contradicting | `WHERE value != (subquery)` | Works |
| Q4 derived/context | `SELECT FROM derived WHERE entity_id=?` | Works |
| Q5 discriminating | `SELECT FROM contested` | Works |
| Q6 withdrawal | `WITH RECURSIVE` dependency closure | Works |
| Q7 load-bearing | Correlated subquery `COUNT(*)=1` | Works, 6500 found |

All 7 query types are implemented. All return correct results.

## Performance (measured)

| Query | Time |
|-------|------|
| Q1 (belief lookup) | 65 microseconds |
| Q6 (recursive withdrawal, 100x) | 0.8 ms per query |
| Q7 (full load-bearing scan) | 53 ms (6500 results) |

DB file: 828KB. Schema + queries: 288 lines.

## Comparison: What does TNN add?

**What SQLite does:**
- All 7 query types with exact set semantics
- 65 microsecond lookups, sub-millisecond complex queries
- 828KB for the full world
- 288 lines of declarative SQL
- Battle-tested, ACID, concurrent access

**What TNN (mnstress1.zag) would add:**
- The same queries implemented in Zag (procedural, not declarative)
- Must manually implement indexes, query planning, recursion
- No ACID, no concurrency, no query optimizer
- The "advantage" is: it runs in Zag

**What TNN does NOT add:**
- No new query capability (SQL does all 7)
- No performance advantage (SQLite is faster than hand-rolled Zag)
- No scale advantage (SQLite handles millions of rows)
- No correctness advantage (SQL set semantics are exact)

## Answer to the key question

**Is there anything TNN-native here, or is it just a database in Zag?**

It is just a database in Zag.

Every substantive capability in the C2 prereg (provenance tracking, contradiction retention, dependency closure, withdrawal analysis, load-bearing identification) is standard relational database functionality. The SQL implementation is shorter (288 lines), faster (microseconds), and more robust (ACID) than any Zag reimplementation.

The "machine-native" label does not survive this baseline. The correct label is "database-native." The TNN implementation, if it passes, demonstrates that epistemic bookkeeping CAN be done in Zag. It does not demonstrate that TNN does it BETTER than a database, or that the capability is TNN-specific.

## What would be genuinely TNN-native

1. **Learning the schema:** If TNN invented the tables/indexes from experience, that would be TNN-native. The prereg discloses query handlers are authored.
2. **LLM comparison on Q2/Q6:** Exact provenance and withdrawal closure are where LLMs fail. That comparison (currently PATH-BLOCKED) would show a real advantage.
3. **Integration with learning:** A standalone epistemic engine is a component. The value comes when it is part of a learner that uses provenance to guide learning.

## Honest restatement

SQLite implements all 7 query types in 288 lines, 828KB, microseconds per query.

If C2's mnstress1.zag passes its kill bars, the fair claim is: "Epistemic bookkeeping at 1000-entity scale can be implemented in pure Zag." The fair non-claim: this is not TNN-native, not an advantage over databases, and not evidence against LLMs.

The Machine-Native Audit (48f9765b5) is confirmed: the prereg tests database functionality, not TNN-specific architecture.
