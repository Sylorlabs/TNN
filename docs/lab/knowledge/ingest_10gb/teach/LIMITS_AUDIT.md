# NO-STUPID-LIMITS — limits audit (2026-09-24)

Micah's law: "TNN should not have a stupid limit like that. Limits are not a
thing TNN needs." This audit inventories every hard limit in the ingestion →
teach → store path, classifies each as LOAD-BEARING or ARBITRARY, and
preregisters a removal/replacement experiment for every arbitrary one.

Scope: `~/workspace/tnn-lab/knowledge/ingest_10gb/teach/` (clean2.py,
gate.zag 2382 lines, merge_zag.zag, GATE_SPEC.md). KB-control and web-crawl
dirs carry no additional numeric caps (checked).

## Classification rule

- **LOAD-BEARING**: physical memory, or the znc 2^25-bytes-per-slice
  toolchain ceiling. These get WORKED AROUND with proven byte-identical
  semantics — never presented as TNN design.
- **ARBITRARY**: a design choice with no physical necessity. These get
  KILLED (or replaced with a principled mechanism). "We always did it this
  way" is not load-bearing.

## Inventory

### L1 — 4096B source chunk-split — ARBITRARY
- `clean2.py::r9_split_para` (L259-272), `r9_emit_unit` assert
  `20 <= len(tb) <= 4096` (L302), same assert in `r9_emit` (L324).
- Splits SE posts >4096B into `se:<site>:<q|a>:<id>~N` chunks. Created the
  entire ~N mess. Protects L2, nothing else.
- **Experiment (IN FLIGHT, Crew A)**: V-NOLIMIT — deterministic chunk-join
  with round-trip proof (re-split reproduces chunks byte-identically),
  whole-record ingest, preregistered counts, full-corpus teach queued
  behind the in-flight `nkey_fullrun.sh`. Kill bars: byte-identical ×2,
  negcontrol 1000/1000, must-reject probes fire, g1/g2 ±0.1% of V0.

### L2 — `IG_MAX_TEXT=4096` gate text cap — ARBITRARY (structural to current code)
- `gate.zag` L37; enforced at `igr_record` L771 (`-2` oversize),
  `ig_gate` G1 L616 (`text.len>IG_MAX_TEXT → 1` reject).
- **Worse than a reject**: during lesson-drop consumption (L1204-1205),
  `rc2!=0 → return -1` — a single >4096B record in facts.dat ABORTS THE
  ENTIRE INGEST RUN, not just a lesson. This is why the source chunks.
- The NUMBER is arbitrary; the fixed-stride probe buffers
  (`key4`/`text4` at L1149-1150, `4×IG_MAX_TEXT`) make it structural.
  The principled bound is the 2^25 slice ceiling, not 4096.
- Same fixed-buffer pattern in query paths (L1306-1309, L1659, L1688-1689,
  L1747, L2208, L2221) — removal must cover the read path end-to-end.
- **Experiment (preregistered)**: scratch gate with dynamic per-record
  allocation (size from the record header, capped at 2^25-1), fixed-stride
  probe buffers replaced by per-probe allocation, G1 text rule keeps only
  the lower bound + the toolchain ceiling. Kill bars: byte-identical rerun
  on the ≤4096 corpus vs frozen gate; V-NOLIMIT corpus installs whole
  records; negcontrol 1000/1000; no g1/g2 drift beyond the predicted
  admission of previously-oversize records.

### L3 — `IG_MAX_KEY=160` key cap — ARBITRARY (+ spec drift)
- `gate.zag` L36; enforced L615 (G1 reject), L771 (`-2` oversize).
- **GATE_SPEC.md L21 says `key_len ≤ 512`** — spec and code disagree.
  Neither number is physically necessary.
- **Experiment (preregistered)**: dynamic key sizing as in L2; reconcile
  spec 160-vs-512 (governance: pick the documented value or remove the
  cap; record the decision).

### L4 — drop-whole-lesson CAL (first-4 must-accept probes) — ARBITRARY
- `gate.zag` L1161-1218. One bad head record → 65,536 records dropped.
  Fate-sharing at lesson granularity with no physical basis.
- **Experiment (preregistered)**: V2 peek-window (already built,
  `gate_v2_bin`) — 256-record window, lesson proceeds iff ≥4 window
  records pass; stuck-gate canary preserved. Kill bars: CP2 lessons
  rescued (194,478), must-reject probes still fire 4/4 per lesson,
  negcontrol 1000/1000. Composes with L1/L2 removal.

### L5 — `IG_LESSON=65536` lesson size — ARBITRARY (operational)
- `gate.zag` L34. Pure batching granularity; no semantic necessity.
- **Experiment (preregistered)**: lesson as pure accounting unit —
  vary lesson size 2^14/2^16/2^18, require installed-set identical
  across sizes (byte-identical store modulo lesson-index audit lines).
  Kills the idea that 65536 is load-bearing.

### L6 — `IG_BLOB_CHUNK=33488896` (32MiB-64KiB) — LOAD-BEARING workaround
- `gate.zag` L35, explicitly "under the 2^25 slice limit". Correct as-is:
  a documented toolchain-ceiling workaround, not a TNN design limit.
- **Experiment**: none — but verify the byte-identical-semantics proof
  for the chunking exists and is referenced from the code comment.

### L7 — text lower bound 20 (G1) — ARBITRARY heuristic
- `gate.zag` L616, `clean2.py` L302. "Unit of knowledge" floor, but 20
  is a magic number.
- **Experiment (preregistered)**: A/B with bound 1 vs 20 vs 100 on a
  held-out source; measure installed-quality delta (downstream retrieval
  precision on probe queries). Keep, tune, or kill by measurement —
  not by assertion.

### L8 — kind-6 digits-only key grammar — ARBITRARY (proven)
- `ig_se_key_ok` L579. ~N investigation proved no downstream consumer
  parses the post id numerically (G2 byte-equality, merge/sindex byte
  order, panswer citation display).
- **Experiment (preregistered)**: V1 admit-`~N` (already built,
  `gate_v1_bin`) — or moot if L1 removal wins (no `~N` keys exist).

### L9 — `ncap` pre-declared store capacity — ARBITRARY (pre-allocation convenience)
- `gate.zag` L407 (`ncap=cap*2`), `ig_ingest` L1288; `id>=ncap → -1`
  abort (L1229, L1260). A real KB grows; a capacity abort is a stupid
  limit wearing a malloc costume.
- **Experiment (preregistered)**: growable store (geometric growth,
  amortized); kill bars: ledger byte-identical between pre-sized and
  grown runs on the same corpus.

### L10 — negcontrol 1000 fixed — NOT A TNN LIMIT
- Measurement artifact (`gate.zag` L1334-1366). Leave alone.

### L11 — `IG_READ_BUF=1048576`, `SC_CHUNK_*` slot constants — OPERATIONAL
- Syscall batching / internal arena geometry (`gate.zag` L39-45).
  Invisible to ingest semantics. Leave alone unless a semantic effect
  is demonstrated.

## Priority order for the removal crew

1. L2 (+L3) — the structural 4096/160 caps. Unblocks L1's victory.
2. L1 — V-NOLIMIT (in flight).
3. L4 — V2 peek-window (built, awaiting full-corpus numbers from the
   in-flight run).
4. L9 — growable store.
5. L5, L7 — measurement-driven.

## Governance notes (need Micah's word, not applied)

- G1: any gate change (L2/L3/L8) amends frozen GATE_SPEC G1/G3.
  V-NOLIMIT needs NO spec amendment (no `~N` keys exist) — a point in
  its favor.
- G2: key-cap spec/code drift (512 vs 160) — pick one or remove.
- G3: L4 changes CAL semantics (frozen behavior).

## Status

- L1 experiment: Crew A running (`scratch_10gb_work/nolimit/`).
- L4/L8 experiments: built, full-corpus numbers pending in-flight run.
- L2/L3/L5/L7/L9: preregistered above, awaiting a removal crew.
