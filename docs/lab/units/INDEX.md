# TNN Representation Program — Arm Catalog (INDEX)

**Program question:** what is a unit of knowledge, if not an LLM token?

**Micah's thesis:** LLM tokens are a fixed discretization built for matrix math. TNN's units
must be COGNITIVE: chunking is an act TNN performs on the raw stream itself (no fixed
tokenizer); vocabulary is taught/learned the way a child learns words; a chunk is a byte
span with a stable ID that memory points back to, retrieves, and reuses (caching territory).

**Status:** design phase. Every arm below is a PROPOSAL. Per program law, the catalog
PROPOSES arms and bars; Micah signs before any build. Nothing here is preregistered yet.

**Corpora:** Shakespeare prose (~5.4MB), sqlite3.c code (~9.5MB). Both fit under the znc
2^25-byte single-slice indexing limit, so prototypes can address each corpus as one slice.

**Hard laws every arm obeys:** pure Zag; zero randomness in any AI decision path;
byte-identical reruns from (input + full logged state); prereg discipline; no-free-lunch
head-to-head testing; real mechanisms, no stubs as headline evidence.

---

## Arm catalog

### Controls (Crews 1)

| Arm | Name | One line |
|-----|------|----------|
| A | Control (TBD) | Baseline arm — exact definition pending crew 1 |
| B | Control (TBD) | Baseline arm — exact definition pending crew 1 |
| C | Control (TBD) | Baseline arm — exact definition pending crew 1 |

### Micah's hypothesis + core mechanisms (Crews 1–4)

| Arm | Name | One line |
|-----|------|----------|
| D | Self-cut byte span + stable ID | Micah's hypothesis: TNN cuts the raw stream itself; a chunk is a byte span with a stable ID memory points to |
| E | Ephemeral | Chunks dissolve after use; no stored IDs, no vocabulary |
| F | Surprise | Cut at surprise/novelty boundaries in the stream |
| G | Pressure | Cut under memory pressure — segmentation as triage |
| H | Deliberate | Boundaries chosen by conscious deliberate decision |
| I | Hierarchical | Nested chunks — chunks inside chunks, tree-structured |
| J | Overlapping | Spans may overlap in bytes; no partition requirement |
| K | Content-addressed | ID = function of content (hash-like); same bytes, same ID |
| L | Position-addressed | ID = position in the stream; identity is where, not what |
| M | Counter | Monotonic ID counter; identity is issuance order |
| N | Judgment-annotated | Chunks carry deliberate annotations from judgment |
| O | Taught | Vocabulary taught by the trainer, child-learns-words style |
| P | Emergent | Boundaries emerge from use/repair cycles, no explicit instruction |
| Q | Hybrid | Deliberate combination of two or more arms |
| R | Compression | Chunks are compression units; cut where it compresses |
| S | Recall-driven | Segmentation shaped by recall success/failure |
| T | Episode-aligned | Chunks = episodes; segmentation follows the episode clock |
| U | Recompute-on-demand | No stored chunks; re-derive cuts whenever needed |
| V | BPE enemy | Adversarial baseline: fixed subword tokenizer, the thing to beat |
| W | Multi-granularity | Several grain sizes simultaneously, no single cut level |
| X | Degenerate | No chunking — whole stream as one unit (or byte-level); null arm |

### Inventions (Crew 5 — this catalog's crew; see `ALPHABET_Y-Z.md`)

| Arm | Name | One line |
|-----|------|----------|
| Y1 | Negotiated | Two-organ cut protocol with mutual veto; deadlock → deliberate adjudication |
| Y2 | Adversarial | Red-team worst-case segmentations; robustness is the objective |
| Y3 | Temporal/versioned | Identity = serial + birth epoch + revision lineage; never dangles |
| Y4 | Question-driven | Lazy: boundary candidates at ingest, segmentation committed at query time |
| Y5 | Cross-stream | One ID over a non-contiguous span set; kills cascade atomically |
| Y6 | Forgettable | Tombstone-native IDs, refcounted, checker-provable total deletion |
| Z1 | Witness-bound | A cut must survive eliminative challenge to become a chunk |
| Z2 | Contract | Chunk = audited obligation between organs; misuse refused loudly |
| Z3 | Budgeted | One scarce currency prices storage + access; granularity is economic |
| Z4 | Dialect | Per-interlocutor lexicons namespaced by speaker tag (Phase 4 hook) |
| Z5 | Recipe | Identity = deterministic cut-program; spans re-derived per recall |
| Z6 | Scar | Boundaries form at revision sites; ledger scar tissue segments |
| Z7 | Provenance | Cut at trust-tier boundaries; maximal single-provenance spans |
| Z8 | Fuzzy | Boundaries carry explicit ±n byte uncertainty; tighten/widen deliberately |

**Arm count as of 2026-09-20:** 24 (A–X) + 14 (Y–Z) = **38 proposed**.

---

## Reading-order guide

**If you are new to the program, read in this order:**

1. **This file's glossary** (below) — pin the terms first; every crew means the same
   thing by them or the catalog is noise.
2. **Arm D** (Micah's hypothesis) — the thesis anchor. Everything else is a variation,
   control, enemy, or invention relative to D.
3. **Controls A–C** — what "nothing special" looks like; every claim is measured
   against these.
4. **Arm V (BPE enemy)** — the adversary. If V wins on every metric, the program's
   value proposition is in trouble (see `RISKS.md` R6).
5. **The mechanism families** — H (deliberate), O (taught), P (emergent), K/L/M (ID
   schemes), R (compression), S (recall-driven): the load-bearing design axes.
6. **The inventions (`ALPHABET_Y-Z.md`)** — Y1–Y6, Z1–Z8: negotiated, adversarial,
   versioned, lazy, cross-stream, forgettable, witness-bound, contract, budgeted,
   dialect, recipe, scar, provenance, fuzzy.
7. **`RISKS.md`** — the ranked list of what kills the program; read before proposing
   a build order.
8. **Sibling crew files** (placeholder — see below) — deep designs per arm range.

**If you are Micah signing preregs:** D, then the falsification criteria in
`ALPHABET_Y-Z.md` per invention arm, then `RISKS.md` top 3.

**If you are building:** pick ONE arm, read its crew file section (mechanism sketch +
falsification criterion + buildability note), then check `RISKS.md` for which
assumptions your build leans on.

---

## Glossary — pinned terminology

All crews use these terms with exactly these meanings. If your arm needs a new term,
define it in your crew file and propose it here.

- **chunk** — the concrete, stored realization of a unit: a byte span (or, in arm Y5,
  a span set) treated by TNN as one recallable item. Chunks are what memory ops act on.
- **unit** — the abstract atom of knowledge; the program's central unknown. A chunk is
  one *candidate* for what a unit is. "Unit of knowledge" is the question; "chunk" is a
  proposed answer shape.
- **ID** — the stable identifier a chunk carries across time, revision, and recall.
  Memory points to IDs, not bytes. An ID must survive everything its arm claims it
  survives; when it doesn't, that is falsification, not a bug report.
- **span** — the bytes a chunk currently covers: `(start, end)` offsets into the stream
  (or a set of them in Y5). Spans move under revision; IDs (in most arms) do not.
- **vocabulary** — the set of chunk shapes/IDs TNN knows and reuses. The reusable
  lexicon. Taught, emergent, or designed depending on the arm.
- **segmentation** — the act/process of dividing the raw stream into chunks. Per the
  thesis, segmentation is something TNN *does*, not something a tokenizer did to the
  input beforehand.
- **cut** — a single boundary decision: the atomic event of segmentation. A chunk is
  born from cuts; a cut is where two chunks meet (or where one chunk ends).
- **taught** — boundary/ID knowledge supplied by a trainer or deliberate instruction,
  scaffold-style: TNN may later disconnect from the scaffold (learner-initiated
  SIGNAL_DISCONNECT). Learned = persists after disconnect. (Cf. arm O.)
- **emergent** — boundaries arising from TNN's own use, recall, and repair cycles with
  no explicit instruction about where to cut. (Cf. arm P.)
- **taught vs emergent (the test)** — the disconnect test decides: if the vocabulary
  survives scaffold removal unchanged in behavior, it was learned; if it collapses
  without the trainer, it was merely performed. An arm that cannot pass the disconnect
  test is not "taught" — it is *dependent*.
- **recall** — retrieving a chunk's bytes via its ID. Byte-exact recall is the
  standing bar: the bytes returned must equal the bytes the ID names, or the failure
  must be loud (never silent corruption).
- **revision** — any change to stored material: re-cut, split, merge, edit, kill,
  rollback. The audit ledger records all revisions; arms differ in what revisions do
  to IDs.
- **tombstone** — a dead ID's ledger marker. Tombstoned IDs are never reused; they
  anchor lineage (Y3) and provable deletion (Y6).

---

## PLACEHOLDER — to be filled once all crews report

> Catalog-holder note (2026-09-20): all seven crews delivered. The arm-count table and
> cross-links below reflect actual delivered files. Nine files total, 53 arms.

### Final arm count table

| Crew | File | Arms | Status |
|------|------|------|--------|
| 1 | `ALPHABET_A-F.md` | A–F → 12 arms (controls, D thesis anchor + D-T/D-R variants, ephemeral E, surprise F-S/F-B) | DELIVERED 2026-09-20 |
| 2 | `ALPHABET_G-L.md` | G–L → 13 arms (pressure G1/G2, deliberate H1/H2, hierarchy I1/I2, tilings J1/J2, content-addressed K1/K2/K3, position L1/L2) | DELIVERED 2026-09-20 |
| 3 | `ALPHABET_M-R.md` | M–R → 8 arms (counter M/M2, judgment-annotated N, taught O, emergent P, hybrid Q, compression R/R2) | DELIVERED 2026-09-20 |
| 4 | `ALPHABET_S-X.md` | S–X → 6 arms (recall-driven S, episode T, recompute U, BPE enemy V, multi-granularity W, degenerate X) | DELIVERED 2026-09-20 |
| 5 | `ALPHABET_Y-Z.md` | Y1–Y6, Z1–Z8 (inventions) | DELIVERED 2026-09-20 |
| 6 | `TEACHERS.md` | Teacher protocols (taught-vocabulary track; meets the alphabet at arm D) | DELIVERED 2026-09-20 |
| 7 | `METRICS.md` | Metric operationalization; NO single crown metric — full scorecard + section champions, blowout rule | DELIVERED 2026-09-20 |

Final ratified arm count: **53** (12 + 13 + 8 + 6 + 14). All bars, N values, blowout thresholds, and frozen parameters remain PROPOSED — Micah signs before any build.

### Cross-links to crew files

- [x] Crew 1: `ALPHABET_A-F.md` — arms A–F with shared protocol, frozen arms and kill bars (proposed)
- [x] Crew 2: `ALPHABET_G-L.md` — arms G–L; cut × structure × identity framed as orthogonal axes; K-vs-L bake-off with hybrid-promotion rule
- [x] Crew 3: `ALPHABET_M-R.md` — arms M–R; arm O builds verbatim against Crew 6's TST-1/§P wire format (zero deviations); extras labeled M2/R2 to avoid collisions with S/T
- [x] Crew 4: `ALPHABET_S-X.md` — arms S–X, thesis tested from use-driven / structural / adversarial directions
- [x] Crew 5: `ALPHABET_Y-Z.md` — 14 invention arms with mechanism sketches,
  falsifiable strengths/weaknesses, falsification criteria, buildability notes
- [x] Crew 6: `TEACHERS.md` — teacher protocols; interface boundary: TEACHER PROPOSES, TNN DISPOSES
- [x] Crew 7: `METRICS.md` — binding: no single crown metric; Pareto frontier + scenario-fit map unless blowout

### Ratification checklist (for the catalog-holder)

- [x] All nine catalog files delivered and linked above (7 crews)
- [x] Arm count reconciled: 53 arms, no duplicates, no gaps — crew 3's extras labeled M2/R2 (not S/T) to avoid collisions; nearest-neighbor pairs documented in
  `ALPHABET_Y-Z.md` and `ALPHABET_M-R.md` header
- [ ] Glossary ratified by all crews (new terms proposed → added or rejected)
- [ ] Micah has signed arms + bars (prereg gate) before any build begins
- [ ] `RISKS.md` re-ranked after crew reports (new risks admitted, dead ones retired)
