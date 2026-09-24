# PREREG MORG — Memory Self-Organization (FROZEN 2026-09-24)

Micah's question: can TNN organize its own memory neatly — choosing its own
categorization (sometimes facts-as-parent, sometimes subject-first with facts
as children — ITS choice) — or does self-organization make memory WORSE?
Test both sides.

## Arms (3)

1. **SELF**: TNN chooses its own scheme from a candidate space, by MEASURED
   retrieval quality on a frozen calibration query set (not by human fiat).
   It records its scheme + per-candidate scores in an inspectable SCHEME
   record (conscious KB control: it must explain its scheme; the scorer
   re-derives the choice independently). It re-files deliberately, and
   re-evaluates at t1 when a new domain arrives (drift test).
2. **IMPOSED**: fixed human taxonomy, top level = type (FACT/CODE/PROC/QUOTE),
   second level = domain. No choice, no reorganization.
3. **FLAT**: append-only, no organization; retrieval by deterministic
   content-match scoring.

All arms share one storage substrate implementing the deliberate mutation
protocol (verify target before write, isolate slots, read back after write).
Zero-RNG, pure Zag, pinned znc
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`), 3x
byte-identical reruns (SHA-256 over all outputs).

## Candidate schemes (SELF)

S1 type->domain->subject | S2 domain->type->subject | S3 subject->type |
S4 type->subject->domain | S5 domain->subject->type | S6 flat multi-tag
(type,domain,subject tags; filter+rank).
Selection: argmax mean F1 on calibration queries; tie-break: fewer levels,
then lowest scheme index. Deterministic.

## Frozen fixtures (formats; content built by crew 1)

`corpus.txt`: `id|domain|type|subject|text` — 240 items: 6 domains
(physics, cooking, coding, history, gardening, music) x 4 types
(FACT, CODE, PROC, QUOTE) x 10. IDs: PH/CO/CD/HI/GA/MU + 01..40.
`corpus_holdout.txt`: same format, 40 items, domain=astronomy, IDs AS01..AS40.
`queries.txt`: `qid|split|class|thint|dhint|shint|text|gold` — 48 queries:
24 PURE (category-pure), 12 SUBJ (subject-wide cross-type), 12 AMBIG
(cross-domain ambiguous). split: 16 calib (8/4/4), 32 test. thint/dhint/shint
are the query's intended type/domain/subject hints (same for all arms; the
experiment is organization, not query parsing). gold = comma-separated ids.
`queries_holdout.txt`: 12 astronomy queries (4/4/4), same format, split=test.

## Arm binary contract (crew 2)

One Zag binary per arm, subcommands:
`ingest <corpus> <storedir>` | `choose` (SELF only: evaluate S1..S6 on calib,
write `scheme.txt` = chosen + all 6 scores + rationale, re-file store) |
`retrieve <queries> <out>` (writes `qid|ranked_ids` top-20 per query) |
`revise <id> <newtext>` | `verify` (prints sha256 over canonical sorted
item records + count) | `deletecat <type>` | `exportcat <type> <file>` |
`importcat <file> <storedir>` | `opscount` (reads/writes/moves since reset).
Retrieval navigation: hierarchical schemes walk the tree matching
thint/dhint/shint; S6/FLAT use identical deterministic keyword scoring
(term occurrences in text+subject+domain+type, tie-break id ascending).

## Battery (frozen order)

B1 retrieval: ingest corpus, (SELF: choose), retrieve test queries -> F1 per
query, macro per class + overall, per arm.
B2 interference: on PURE queries, fraction of top-10 hits with wrong type
(for type-pure) / wrong domain (for domain-pure), per arm.
B3 revision locality: revise 10 spread items; verify all other items
byte-identical. Zero collateral required.
B4 separability: deletecat CODE; hash(rest) == hash(fresh ingest of corpus
minus CODE). Export FACT, import into fresh store; hash == original FACT set.
B5 reorg cost: SELF opscount for choose+refile (moves/reads/writes).
B6 drift: t0 = scheme on base corpus; ingest corpus_holdout; choose again;
record change y/n; holdout-query F1 under old scheme vs new scheme.
B7 unseen domain: holdout queries F1 per arm (SELF under its t1 scheme).
B8 scheme report: SELF's chosen scheme(s) per domain — one scheme or
per-domain? (Implement per-domain choice: choose runs per domain; report.)

## Kill bars

- KB-1 non-inferiority: SELF overall test F1 >= IMPOSED - 0.02.
- KB-2 separability: ALL arms pass B4 byte-identical. (Portable-chunks
  load-bearing.)
- KB-3 revision locality: ALL arms zero collateral damage in B3.
- KB-4 consciousness: SELF scheme.txt present; scorer re-derives the argmax
  choice from recorded scores under the frozen tie-break. Must match.
- KB-5 superiority probe (REPORTED, not a kill): SELF - IMPOSED per class;
  note any class where SELF wins by >= 0.03, and where it loses.

Also report: FLAT vs organized deltas; per-domain scheme choices; drift
outcome (switch helped/hurt/neutral); holdout F1; sol's failure modes
(self-reinforcing misorganization, popularity bias, misleading cross-domain
links) checked against B2/B6/B7 evidence.

## Deliverables

`docs/lab/memory_org/PREREG_MORG_FROZEN.md` (this file),
`corpus.txt`, `corpus_holdout.txt`, `queries.txt`, `queries_holdout.txt`,
`scorer.py`, three arm sources + `run_battery.sh`, `RESULTS_MORG.md`,
`VERDICT_MORG.md`. No binaries, no .zagd in commits.
