# PREREG WS2-B — Forced Table-of-Contents retrieval scheme (FROZEN 2026-09-24)

Worker: WS2-B. Coordinator: cognition workstream. Status: FROZEN — committed
before any lookup was run. Any change to mechanism, probes, gold sets, or bars
after this commit requires a new dated amendment; results under a changed rule
are a new experiment, not this one.

NOTE (2026-09-24, pre-commit): the first draft of this prereg specified a
WS2-B-authored 56-probe battery. WS2-A's probe battery
(`shared/PROBE_BATTERY_SPEC.md`, fixtures in `ws2/fixtures/`) has since
landed, and the task instructs WS2-B to use it. This frozen version adopts
WS2-A's battery as the PRIMARY retrieval bar and adds only a small
SUPPLEMENTARY maintenance leg (their battery has no install/revise/delete
dimension, which the ToC design explicitly claims). No probe has been executed;
no result is known at freeze time.

## 1. Question

Micah's verdict: "lookups should work EVERYWHERE for its memory. TNN memory
retrieval always needs to be 100%. Try FORCING TNN to use a table of contents."

Build the ToC-forced approach — TNN maintains an explicit, deliberately-managed
table of contents over its memory entries, updated on every install/revise/
delete, consulted on every lookup — and test it against a 100% retrieval bar.

## 2. ToC design (frozen)

### 2.1 ToC contents (all derived from items, all maintained)

Per item `(id, domain, type, subject, text)` the ToC holds:

- Key→id-set buckets: `T:<type>`, `D:<domain>`, `S:<subject>`,
  `TD:<type>:<domain>`, `TS:<type>:<subject>`, `DS:<domain>:<subject>`,
  `TDS:<type>:<domain>:<subject>`.
- Keyword index: per-item stemmed token set `KW(id)` from
  `text + subject + domain + type`; per-subject aggregate `AGG(subject)` =
  union of `KW` over items sharing the subject. The keyword index IS part of
  the ToC: built at ingest, consulted at lookup; the lookup never scans raw
  item text.

On disk (sorted, deterministic): `toc.txt` (`key|id1,id2,...`), `kw.txt`
(`id|tok,tok,...`), `cells.txt` (`subject|tok,tok,...`), `manifest.txt`
(item/key counts after every maintenance op).

### 2.2 Maintenance rules (frozen)

- **ingest**: one line per item `id|domain|type|subject|text`; duplicate ids
  keep the FIRST occurrence, later ones dropped (counted, reported).
- **install**: insert id into every key bucket it belongs to (ids sorted);
  compute `KW(id)`; recompute affected `AGG(subject)`; rewrite files; bump
  manifest.
- **revise(id, newtext)**: recompute `KW(id)` and its subject's `AGG`; slot
  buckets unchanged.
- **delete(id)**: remove id from every bucket; drop empty keys; drop its
  `KW`; recompute its subject's `AGG`.
- Every maintenance op increments op counters (the bill, §5).

### 2.3 Lookup algorithm (frozen) — ToC consulted on EVERY lookup; query HINTS ignored

The battery's query files carry `thint/dhint/shint` fields. The scheme
deliberately IGNORES them: a real lookup arrives as text, and the forced-ToC
test is text→ToC-key routing. (Consequence: WS2-A's X1/X3 "wrong-hint" probes
become pure-text probes for this scheme — reported as such.)

```
normalize(q) = lowercase(q) with all non-alphanumeric chars removed
SLOT HITS (from ToC vocabulary only — never from item text or hints):
  type hit    <=> normalize(<type>)    is a substring of normalize(q.text)
  domain hit  <=> normalize(<domain>)  is a substring of normalize(q.text)
  subject hit <=> normalize(<subject>) is a substring of normalize(q.text)
ROUTE A (subject anchor) — >=1 subject hit:
  anchor = union of S:<subject> over hit subjects
  for each domain hit d: if anchor ∩ D:<d> non-empty: anchor &= D:<d>
                         (empty => d is a distractor, ignored)
  for each type hit t:   if anchor ∩ T:<t> non-empty: anchor &= T:<t>
  candidates = anchor, ranked by (own(i) desc, id asc), truncated to K
ROUTE B (no subject) — >=1 type/domain hit:
  candidates = intersection of hit T:<t>/D:<d> sets, ranked as above, top K
ROUTE C (keyword fallback) — no slot hits:
  Q = stemmed non-stopword tokens of q.text
  own(i)    = |Q ∩ KW(i)| ; cellm(i) = |Q ∩ AGG(subject(i))|
  score(i)  = cellm(i)*1000 + own(i)
  candidates = items with score(i) > 0, ranked by (score desc, id asc), top K
  (score-0 abstention: the scheme CAN return fewer than K ids, including
  none — this answers WS2-A's FALSE_POSITIVE finding for MORG topk)
```

`own(i)` in Routes A/B uses the same stemmed keyword sets (lets a
distinctive text token break ties by evidence, e.g. C1 "oak timber").

### 2.4 Tokenizer / stemmer / stoplist (frozen)

- Tokenize: maximal runs of `[a-z0-9]` after lowercasing.
- Stem (identical both sides): len>4 & ends "ing"→strip 3; elif len>3 & ends
  "ed"→strip 2; elif len>4 & ends "es"→strip 2; elif len>3 & ends "s" & not
  "ss"→strip 1 (each kept only if result len≥3).
- Stoplist (keyword layer only): a an the is are was were be been being do
  does did how what why who which when where of to in on at for with by from
  as and or but not no all every about show me tell you your my it its this
  that these those there their them then than into onto

## 3. Primary battery: WS2-A v1 (frozen by WS2-A; 51 probes)

Corpus `ws2/fixtures/probe_corpus.txt` (34 lines; PD01 duplicated → 33 items
after first-wins dedup). Queries `ws2/fixtures/probe_queries.txt`. Grading
adaptation (frozen here): per query, **K = |gold|** (gold field parsed as
comma list; empty gold → K=0); **PASS iff returned id SET ⊇ gold set and
|returned| ≤ K** — i.e. every gold id present, no more than K ids returned.
(For single-gold probes this is exact-match; for K=0 it is abstention.)

Classes: P-AGE (10, exact-hint texts), P-COLL C1 (10, one distinctive token
each), P-COLL C2 (1, duplicate-id; id-level bar: PD01 returned), P-CTX X1/X2/X3
(18, hintless-equivalent under this scheme), P-PARA (6, zero exact-token
overlap by their validator — stemming may bridge a few; reported per probe),
P-NEG (6, gold empty → must abstain).

## 4. Supplementary battery: WS2-B maintenance leg (frozen here; 7 probes)

Same corpus format; separate store dir; runs AFTER the primary battery.

- install `WS2B_MAINT_items.txt` (NW01,NW02 physics/FACT/turbulence;
  NW03 cooking/FACT/fermentation):
  - W01|2|everything about turbulence → {NW01,NW02}
  - W02|1|show me FACT items about fermentation in cooking → {NW03}
  - W03|1|why does miso taste savory? → {NW03}
- revise NW03? no — revise NW01 := `WS2B_MAINT_revise.txt`:
  - W04|1|where do smoke vortices form behind a hull? → {NW01}
  - W05|2|everything about turbulence → {NW01,NW02}
- delete NW02:
  - W06|1|everything about turbulence → {NW01} (deleted id must be absent)
  - W07|0|river rapids churn white → {} (abstention after delete)

## 5. Bars (frozen)

- **PRIMARY BAR: 58/58 probes PASS = experiment PASSES. Any single miss =
  FAIL.** (51 WS2-A + 7 maintenance.)
- **SECONDARY TIERS (diagnostic):** T-exact = all non-PARA probes (52);
  T-para = the 6 P-PARA probes. Reported separately; a PRIMARY FAIL isolated
  to T-para is reported as such with per-miss mechanical diagnosis.
- Per-miss diagnosis is mandatory: for every miss, which route was taken,
  what the slot hits / scores were, and why the gold set was not returned.
  Misses are never averaged away.

## 6. Bill (frozen metrics)

Counted in-binary, reported per phase: per install (3-item batch) — ToC
bucket writes, KW builds, AGG recomputes, bytes rewritten; per revise; per
delete; per lookup by route (key reads, score computations); ToC bytes on
disk at 33 / 36 / 36 / 35 items.

## 7. Determinism

Pure Zag, zero RNG. All iteration sorted (ids, keys, subjects, tokens).
3× full runs (primary + maintenance) from clean rebuilds; SHA-256 over every
output file must match across runs.

## 8. Deliverable

Verdict PASS/FAIL vs the 100% bar, per-class table, per-miss diagnosis,
bill table, commit SHAs, recommendation (adopt / iterate / drop).
