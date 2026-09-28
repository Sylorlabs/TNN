# ALPHABET S–X — Representation Arms: "What is a unit of knowledge if not an LLM token"

**Crew:** Brainstorm Crew 4 (representation program)
**Date:** 2026-09-20
**Status:** CATALOG PROPOSAL — frozen arms and bars are PROPOSED here. Nothing builds until Micah signs. Per prereg discipline: this document proposes; Micah disposes.
**Scope:** Arms S, T, U, V, W, X. Arms A–R belong to Crews 1–3. Arm D (referenced below) is Micah's cached chunk-ID hypothesis: *a chunk is a byte span with a stable ID that memory points back to, retrieves, and reuses* (caching territory).

## Micah's thesis (the thing being tested)

LLM tokens are a fixed discretization built for matrix math. TNN's units must be **cognitive**: chunking is an act TNN performs on the raw stream itself (no fixed tokenizer); vocabulary is taught/learned the way a child learns words; a chunk is a byte span with a stable ID that memory points back to, retrieves, and reuses. These six arms test that thesis from three directions — use-driven (S), structural (T, W), and adversarial (U anti-caching, V the LLM enemy, X the degenerate floor).

## Hard context every arm designs inside

- **Five organs:** (1) deliberate memory substrate · (2) eliminative hypothesis logic · (3) deliberate consolidation/promotion · (4) symbolic recall and trace composition · (5) native structural revision.
- **Memory ops:** add, kill, pin, promote, demote, strengthen, weaken. Strength is judgment-set, never formulaic. Force-pin is human/trainer-only, audited, visible.
- **Audit ledger:** append-only, 16-word entries: `op, slot, rc, b1..b5, a1..a5, stage, d1, d2`. Every segmentation decision (merge, split, granularity selection, episode open) is a reasoning-control commit: inspect → propose → commit/refuse, with rollback on post-change verification failure. Chunk IDs are integers, never reused; retired IDs become tombstones so old ledger entries still resolve (provenance survives revision).
- **Laws:** pure Zag; **zero randomness** in any AI decision path; byte-identical reruns (same input + same logged state → byte-identical output); no-free-lunch head-to-heads, no assumed winners.
- **Corpora:** Project Gutenberg Shakespeare (~5.4 MB prose), sqlite3.c (~9.5 MB code). ~15 MB total, ~245,000 sixty-four-byte atoms at the base layer. Precedent: 64-byte chunks, byte-exact recall.
- **Zag gotchas honored throughout:** no single slice indexed above 2^25 bytes (corpus buffers striped at ≤2^24 regardless); slice `==` is not content identity — integer chunk IDs and selectors everywhere; large structs' array fields aliased to locals before indexed access; `_zag_arg(n)` returns a non-owned pointer (never freed).

## Shared prereg battery (all arms, same corpora, same scripted queries)

| ID | Metric | What is measured |
|----|--------|------------------|
| B1 | Byte-exact recall | 10,000 random spans per corpus, lengths 8–4096 bytes. **Gate: 100% byte-exact or the arm is dead.** |
| B2 | Partial recall cost | Bytes materialized per byte recalled, amortized over the 10k queries. |
| B3 | Boundary alignment | Fraction of chunk boundaries coinciding with corpus-native boundaries (prose: whitespace/punctuation-adjacent; code: reference-lexer token boundaries — the lexer is a *measurement instrument*, never the arm's mechanism). Reported per corpus; scored, not gated. |
| B4 | Reuse rate | Scripted multi-session battery with repeated spans across contexts: fraction of recalls served from an existing chunk reference vs re-derived/re-placed. |
| B5 | Revision blast radius | 100 single-byte edits at random offsets mid-battery: bytes re-keyed / re-indexed per edit. |
| B6 | Segmentation footprint | Bytes of segmentation state per ingested byte. |
| B7 | Determinism | Rerun the battery on identical logged state. **Gate: byte-identical or dead.** (Law, not a metric.) |
| B8 | Cold-start latency | Ops to first correct recall after ingestion, before any learning/warmup. |
| B9 | Composition | Assemble 1,000 novel spans (never recalled before) from chunk references: success rate + cost. |
| B10 | Transfer | Segmenter crystallized/trained on corpus A, evaluated on corpus B: degradation on B2–B4. |

**Universal floor rule (applies to S–W):** any arm that fails to beat X on *any* of B2, B4, B5, B9 is dead on arrival. Ties permitted on B1 (100% = 100%) and B7 (pass = pass). X exists to be beaten; an arm under the floor is worse than doing nothing.

**Proposed composite weights** (PROPOSED — Micah signs): B2 20% · B4 20% · B5 15% · B9 15% · B3 10% · B6 10% · B8 5% · B10 5%. B1/B7 are gates, unscored.

**Threshold convention:** every numeric bar below is PROPOSED and frozen at prereg-sign time. "Warmup" = 5,000 scripted recall episodes unless stated otherwise. All counters and thresholds live in logged state; reruns replay inputs + state, so byte-identical output is a *checkable* property, not a hope.

---

## ARM S — Recall-driven boundaries ("a chunk is whatever gets recalled as one unit")

### (1) Mechanism sketch (TNN-native)

Segmentation does not exist before use; it **crystallizes from recall**. Ingestion lays down 64-byte atomic spans (the standing precedent) — atoms are recallable from t=0, so recall always works. What changes over time is that *adjacent units that are recalled together fuse into larger addressable units*.

- **State:** for every adjacent pair of live units (atoms or chunks), three deterministic counters: `J` (joint recalls — both units retrieved within the same reasoning episode / same recall query), `I_a`, `I_b` (independent recalls of each side alone). Counters are logged state, indexed by integer unit IDs, scanned in ID order. No randomness anywhere.
- **Crystallization (organ 3, deliberate consolidation/promotion):** when `J ≥ θ_merge` **and** cohesion `J / (J + I_a + I_b) ≥ ρ`, consolidation *proposes* a merge. Organ 2 (eliminative hypothesis logic) vets it: the hypothesis "A+B is one unit" must survive elimination attempts — i.e., a sweep of recent recall history for counterexamples where A was needed without B in a context the merge would have mispredicted. If it survives, reasoning control commits: `CHUNK_MERGE` audit entry (op, slots of A and B, counters in d1/d2), new stable integer chunk ID issued, A and B tombstoned (never reused as IDs). Thresholds θ_merge, ρ are **judgment-set** (trainer/TNN decision, logged, frozen per trial) — in the same spirit as strength: decided, audited, never a background formula.
- **Chicken-and-egg bootstrap:** there is none, by construction. Atoms are the base-case chunks. Recall works on day zero at atom granularity; crystallization only *adds* larger units, never removes recall capability. The system recalls before it chunks, exactly as a child points before it names.
- **Dissolution of wrong boundaries (organ 5, native structural revision):** when the parts keep being recalled alone while joint recall stalls — divergence `δ = (I_a + I_b) / (J + 1) ≥ σ_split` (judgment-set, frozen) — revision proposes a split. Committed as `CHUNK_SPLIT`; the merged ID is tombstoned, the parts re-registered under new IDs. Old audit entries still resolve via tombstones, so provenance is never rewritten — only superseded.
- **Memory-op mapping:** crystallized chunks are `add`'ed to the chunk registry (a memory region like any other) and can be pinned, promoted, demoted, strengthened, weakened, killed by the deliberate-memory organ. A killed chunk's ID tombstones; its bytes remain addressable as atoms.

### (2) Falsifiable predictions

**Strengths (S must show these):**
- **S1 — use-alignment:** after warmup, B4 reuse rate ≥ **2.0×** V's on each corpus. (The whole point: boundaries follow use, so use reuses them.)
- **S2 — surgical revision:** B5 blast radius ≤ **4 KB** re-keyed per single-byte edit on either corpus (a bad merge dissolves locally; nothing global re-keys).
- **S3 — prose alignment:** B3 ≥ **70%** of crystallized boundaries whitespace/punctuation-adjacent on Shakespeare after warmup.

**Weaknesses (S is predicted to show these — they are part of the bet):**
- **W1 — cold start:** B8 latency ≥ **10×** V's for the first 500 recalls (atoms-only recall touches ~N atoms per span; no warmup, no shortcuts).
- **W2 — boundary churn:** ≥ **5%** of merges are later split on sqlite3.c (task-dependent co-recall patterns don't settle the way prose habits do).
- **W3 — code misalignment:** B3 ≤ **40%** on sqlite3.c (recall-driven boundaries follow *usage*, not syntax; syntax alignment is not the goal, but we measure it honestly).

### (3) Falsification criterion — S dies if ANY ONE holds

1. After warmup, B4 reuse rate is **< 1.5× V's** on either corpus (the use-alignment advantage — the arm's entire reason to exist — fails to materialize), **OR**
2. merge-then-split churn exceeds **25%** of all merges on either corpus (crystallization never settles → no stable IDs → Micah's caching territory collapses), **OR**
3. B7 determinism gate fails, **OR**
4. the universal floor rule fires (fails to beat X on any of B2/B4/B5/B9).

### (4) Buildability note

Pure Zag, moderate complexity. Counters in fixed integer arrays (striped ≤2^24 entries per array to respect the slice limit); merge/split as reasoning-control commits with 16-word audit entries; merge scan in ascending ID order for determinism; chunk registry keyed by integer ID (never slice `==`). The eliminative vetting pass is a bounded history scan — cost it explicitly in the build plan (it is the most expensive new piece). Estimated: the largest single build of the six arms, but no new primitives beyond what organs 2, 3, 5 already require.

---

## ARM T — Episode-aligned chunks ("the unit of knowledge IS the unit of experience")

### (1) Mechanism sketch (TNN-native)

Chunk boundaries = memory episode boundaries. The thesis: TNN already carves experience into episodes in the deliberate-memory substrate; *language/code units should be those episodes*, not a second segmentation invented for text.

- **What defines an episode boundary (TNN-native, no external segmenter):** an episode is a maximal byte span ingested under one continuous ingestion intent. Operationally it opens on exactly three triggers, all deliberate acts: (i) an explicit `EPISODE_BEGIN` issued by the trainer or by TNN itself (audited, 16-word entry); (ii) a quiescence gap > τ in the input stream (τ judgment-set, logged, frozen); (iii) a source switch (file/socket/session boundary). It closes on the next open. Nothing statistical, nothing learned — boundaries are *acts*, like deciding to start a new paragraph.
- **Sub-episode structure:** a long episode is **not** one giant opaque chunk. The episode is the chunk's *scope*; within it, recall addresses byte-offset ranges `(episode_id, start, len)` — offset addressing is free, bytes are bytes. Optionally TNN may issue deliberate sub-boundaries ("scenes") as audited acts, but the arm does not *require* them: the claim is that the episode ID plus offsets is sufficient addressing.
- **The failure mode, stated plainly:** granularity is hostage to ingestion batching, which is about I/O rather than knowledge. Ingest sqlite3.c as one file → one 9.5 MB episode → T degenerates toward X on that corpus. Ingest chatty one-line-at-a-time input → thousands of byte-scale episodes → T degenerates toward raw bytes. T has no answer to "what if the world's batching is wrong" except the offset-addressing escape hatch — and if >80% of real recall traffic uses sub-episode offsets, the episode ID is doing no work and the arm is X-with-offsets wearing a philosophy costume.

### (2) Falsifiable predictions

**Strengths:**
- **T1 — minimal machinery:** B6 footprint is best-in-class among stateful arms (one ID + base + length per episode; offsets cost nothing to store).
- **T2 — experience queries:** on "unit of experience" probes (recall everything ingested in session N; what arrived between event A and event B), T answers exactly with zero segmentation work — predicts 100% success at O(1) addressing where S must reconstruct.

**Weaknesses:**
- **W1 — code-corpus collapse:** on sqlite3.c ingested as a single file, B2 partial-recall cost lands **within 2× of X's** (the episode *is* the stream; offsets don't save you from materializing it).
- **W2 — composition tax:** B9 novel-span assembly across episode boundaries costs ≥ **5× S's** (no cached sub-units to compose from; every cross-episode span is rebuilt from offsets).
- **W3 — batching fragility:** re-ingesting the same bytes with different batching (one file vs 1,000 line-episodes) changes B2 by ≥ **10×** — the segmentation is a function of plumbing, not content.

### (3) Falsification criterion — T dies if ANY ONE holds

1. On either corpus, B2 partial-recall cost is **within 2× of X's** (it fails to beat the degenerate floor where it matters), **OR**
2. **>80%** of recall queries in the battery address sub-episode spans (the episode ID carries <20% of addressing work — the "unit of experience" claim is falsified; the real unit is the sub-span T refused to name), **OR**
3. B7 determinism gate fails, **OR** the universal floor rule fires.

### (4) Buildability note

Trivial — the easiest arm to build. Episode table `(id, base_offset, len)`; offset arithmetic; `EPISODE_BEGIN` audit entries. Two days' work, most of it the battery harness it shares with everyone. Its value is mostly as a *clean philosophical control*: if experience-aligned units were sufficient, T would win, and its failure modes tell us exactly why they aren't.

---

## ARM U — Recompute-on-demand, no stored segmentation (the radical anti-caching arm)

### (1) Mechanism sketch (TNN-native)

**Nothing about chunking persists.** No chunk registry, no stable chunk IDs, no merge table, no memoization. Every access re-derives the segmentation deterministically from bytes + current logged state, uses it for that one recall, and discards it.

- **Derivation function D(bytes, logged_state, query_span) → unit boundaries over the span.** D is *pure*: the S crystallization rule evaluated on demand over the query span plus a bounded context window (window radius judgment-set, frozen, logged). Given the query span and the logged recall-history counters, D recomputes which merges *would* have fired covering this span and returns the resulting unit boundaries; recall then serves bytes through those boundaries. Same rule as S — the *only* difference between U and D/S is storage.
- **Determinism:** D is a pure function of (bytes, logged counters). Same input + same logged state → byte-identical segmentation, byte-identical recall. B7 holds by construction, and it had better — U's entire pitch is that caching is unnecessary *because* re-derivation is deterministic.
- **Cost model:** per recall, O(window) counter lookups + merge-rule evaluations. No storage cost, no invalidation cost — a mid-stream byte edit changes future derivations automatically; there is literally nothing to re-key.
- **Why it might not be insane:** if the derivation is cheap relative to lookup + invalidation, and if boundaries churn often (U's home turf is a high-churn regime), recompute can win on total cost. U is the falsification battleground for Micah's cached-ID hypothesis D: if U wins anywhere real, caching is a convenience, not a necessity.

### (2) Falsifiable predictions

**Strengths:**
- **U1 — zero revision cost:** B5 blast radius = **0 persisted bytes** by construction — predicts best-in-class B5, uncontested.
- **U2 — zero segmentation footprint:** B6 = **0** for segmentation state (recall-history counters are shared infrastructure with S/D, counted as history, not segmentation — a wash in head-to-head).

**Weaknesses:**
- **W1 — per-recall CPU:** B2 latency (in ops, not just bytes) ≥ **5× D's** — re-derivation is paid on every single access.
- **W2 — no reuse:** B4 reuse rate = **0 by construction** (there is nothing to reuse *from*) — predicts worst-in-class B4, uncontested.
- **W3 — catastrophic amortization:** on the multi-session battery with heavy repeat queries, total CPU scales with *queries*, not with *distinct spans* — predicts ≥ **10× D's** total CPU on the repeat-heavy session.

### (3) Falsification criterion — U dies if EITHER holds

1. Total battery CPU exceeds **D's by >10×** **and** B4 < **10%** (recompute loses on cost *and* reuse with no compensating virtue — the anti-caching thesis has nowhere to stand), **OR**
2. D-with-invalidation beats U on **total cost including 100 mid-stream byte edits** (i.e., even in the churn-heavy battery — U's best-case regime — caching wins; the battleground is lost on its home turf), **OR** B7 fails (which would be embarrassing for an arm whose pitch is determinism).

### (4) Buildability note

Simple to build — it is S's rule with the registry deleted. The subtle work is all in the *measurement*: the head-to-head below must account CPU ops honestly (counter lookups, rule evaluations, window assembly) with no hand-waving. Pure Zag; the derivation window assembly must respect the 2^25 slice limit (window buffers striped like everything else).

### U vs D head-to-head — explicit comparison design (the falsification battleground)

**The fair fight:** D = Micah's cached-ID hypothesis implemented as **S's crystallization rule WITH a persistent chunk registry** (stable IDs; memory points back, retrieves, reuses). U = **the same rule, evaluated on demand, nothing persisted**. Rule-constant, storage-only difference — the *only* thing being tested is whether caching pays.

- **Shared setup:** same corpora, same scripted recall battery (including repeat queries across sessions and 100 mid-stream byte edits), same recall-history counters as logged state in both arms.
- **Metrics:** total CPU ops across the battery; peak resident memory; B4 reuse (D only — U is 0 by construction); B5 re-keyed bytes (D only — U is 0 by construction); B2 per-recall latency distribution (p50/p99, in ops).
- **Decision rule (preregistered):** total_cost = cpu_ops + λ·(resident_bytes × queries) + μ·(rekey_bytes), with λ, μ frozen at sign time (PROPOSED: λ = 1 op per 64 resident bytes per query; μ = 10 ops per re-keyed byte). U wins the battleground iff total_cost(U) < total_cost(D).
- **The crossover analysis (the actual result):** sweep the edit count 0 → 1000 and plot where U overtakes D, if ever. The crossover point *is* the finding. D's caching claim is falsified iff U wins at edit counts at or below the median memory-op rate per 1k episodes read from the MA1/RC1 op logs at prereg-freeze time (i.e., at churn levels representative of real TNN operation, not a torture regime). If the crossover sits above any plausible operating churn, D stands and U is retired to "interesting but uneconomical."
- **What a U win would mean:** caching is an optimization with a measured crossover, not an architectural necessity — D survives as the default but loses its law-like status. What a D win means: the cached-ID hypothesis is load-bearing, and U is dead.

---

## ARM V — BPE-style fixed tokenizer as the ENEMY control (the LLM world's answer, built to be beaten)

V gets **every fair advantage**: a good merge table, trained on the same corpora, generous vocabulary, deterministic implementation. If a TNN-native arm beats V, it must mean something. If it can't, we say so out loud (see the intellectual honesty clause).

### (1) Mechanism sketch

Byte-level BPE (byte-level, not Unicode-level — TNN is a byte stream; GPT-2-style byte BPE is the honest comparison), fully deterministic.

- **Training (build-time):** 16,384 merges learned from the concatenation of both corpora (standard BPE: most-frequent adjacent pair merged iteratively; ties broken by lowest byte value, then leftmost — specified, deterministic, logged). *Provenance note:* the merge-table training is not on the AI's decision path, but we implement it as a build-time **Zag** program anyway — a Python-shaped hole in the provenance story would poison the byte-identical rerun claim the moment anyone asks "where did this table come from."
- **Zag representation:**
  ```
  struct Merge { a: u16, b: u16, out: u16 }   // one BPE merge; rank = array order
  struct BpeTable {
      merges: []Merge,        // 16,384 entries, sorted by rank
      vocab_blob: []u8,       // concatenated token byte strings, striped ≤2^24
      vocab_off: []u32,       // byte offset per token id
      vocab_len: []u16,       // byte length per token id
  }
  ```
  Base vocabulary: 256 byte values + 16,384 merges = 16,640 tokens. Token id = u16. The tokenized corpora are stored as u16 sequences (the "segmentation").
- **Tokenization pass:** start from bytes; repeatedly merge the lowest-rank applicable adjacent pair; ties → leftmost. Deterministic given the table, byte-identical reruns hold. Recall: token ids → `vocab_blob` slices → bytes. Lossless by construction, so B1 (byte-exact) passes trivially.

### (2) Falsifiable predictions

**Strengths (V is *expected* to win these — conceded in advance as BPE's home turf):**
- **V1 — density:** fewest addressing units per byte of any arm (this is literally what BPE optimizes). Predicts ≥ **2×** fewer units per byte than S's crystallized chunks.
- **V2 — cold start:** best B8 — the table is precomputed; first recall pays one tokenization pass, zero warmup.
- **V3 — transfer:** B10 degradation **<15%** on B2–B4 when the table trained on corpus A tokenizes corpus B (fixed tables don't care what they were trained on, within reason).
- **V4 — audit surface:** smallest implementation of any stateful arm (~200 lines for the pass); the easiest determinism proof.

**Weaknesses (where TNN-native arms must draw blood):**
- **W1 — use-misalignment:** token boundaries are fixed before any recall happens; predicts B4 reuse-by-use ≤ **50%** of S's after warmup (V's units are not *anyone's* recall units).
- **W2 — edit blast radius:** the token stream is positional — a mid-stream byte edit shifts downstream token boundaries. Predicts ≥ **50%** of the token stream re-emitted for edits in the first 10% of a corpus.
- **W3 — misaligned spans:** arbitrary-offset recall cuts tokens; predicts B2 ≥ **3×** S's on spans whose offsets don't align to token boundaries.

### (3) Falsification criterion — runs BOTH directions

**V is beaten (retired as a control, thesis advances) iff** at least one TNN-native arm passes **≥2** of the victory conditions VC1–VC4 below. **V survives as a standing embarrassment** for any arm that fails all four.

**Preregistered victory conditions for TNN-native arms over V** (margins frozen at sign time):
- **VC1 — use-alignment:** the arm beats V on B4 reuse rate by **≥2×** after warmup.
- **VC2 — revision:** the arm beats V on B5 blast radius by **≥10×** (bytes re-keyed per single-byte edit).
- **VC3 — partial recall:** the arm beats V on B2 for misaligned spans by **≥3×**.
- **VC4 — composition:** the arm beats V on B9 novel-span assembly success by **≥20 percentage points**.

**Intellectual honesty clause (reverse falsification — read carefully):** if V meets or beats the best TNN-native arm on a **majority of the scored battery** (B2, B3, B4, B5, B6, B8, B9, B10 under the signed weights) **and** the TNN arms fail VC1–VC4 — *in particular*, if V wins or ties on the **use metrics** B2/B4/B9 and not just the compression metrics — then fixed discretization is vindicated **as the addressing layer**, and the thesis retreats honestly: TNN's cognitive chunking becomes a *composition layer over fixed tokens*, not a replacement for tokenization. The "no fixed tokenizer" claim dies; "chunks compose over tokens" takes its place. We further admit in advance that V wins outright on density (V1), cold start (V2), cross-corpus transfer (V3), and implementation audit surface (V4) — the TNN arms are not required to beat V there. But if the cognitive metrics go to V too, the thesis is wrong, full stop, and this document says so before the first line of code is written.

### (4) Buildability note

Straightforward. The tokenizer pass is the simplest stateful-adjacent code in the program; the table is a build artifact with Zag provenance. The main build risk is *fairness theater* — a deliberately weak V (tiny vocab, bad tie-breaks, trained on one corpus) that the TNN arms "beat" meaninglessly. Guard: the prereg freezes vocab size (16,384), training corpora (both), and tie-break rules, and the build is reviewed against a one-page fairness checklist before numbers count.

---

## ARM W — Multi-granularity parallel (bytes + chunks + superchunks coexist; TNN selects per task per moment)

### (1) Mechanism sketch (TNN-native)

Three segmentations are maintained simultaneously over the same bytes: **L0** = 64-byte atoms, **L1** = S-rule crystallized chunks, **L2** = superchunks (the S merge rule applied one level up: adjacent L1 chunks with joint chunk-scale recall fuse). Every recall query is served at exactly one granularity, chosen per query, per moment.

- **Who chooses (organ mapping):** organ 4 (symbolic recall and trace composition) issues the recall need; the **selection is a reasoning-control proposal**. Steps: *inspect* — which levels hold units covering the query span? *propose* — one level, with evidence = logged per-level hit statistics for similar spans (similarity = deterministic bucketing by `(length_log2, corpus_id)` — no learned similarity, no magic); the rule is a pure function of logged counters: pick argmax of expected bytes-saved. *commit/refuse* — committed as `GRAN_SEL` audit entry (op, query span in b1..b3, chosen level in b4, evidence counter snapshot in b5/a1..a5/d1/d2). The selector **cannot see the query outcome before choosing** — only counters.
- **What keeps it honest (anti-opportunism discipline):** (i) the selection rule is a pure function of logged state — replayable, no post-hoc picking; (ii) every selection is audited with its evidence snapshot; (iii) a standing **selection-justification gate**: reasoning control *refuses* a selection whose evidence does not show the chosen level had the best logged expectation at selection time (this is the immune system against "pick whatever works" degenerating into unprincipled opportunism — the choice must be *justified before the fact*, from logged evidence, or it doesn't happen); (iv) no-free-lunch scoring: W is scored head-to-head against fixed-level policies (L0-only, S-only/L1, L2-only) on the same battery — selection must *earn* its overhead.
- **Cost of parallelism:** ~3× S's B6 footprint (three registries) + per-query selection overhead (counter lookups + one audit entry per selection — the ledger grows with queries, which is itself a measured cost).

### (2) Falsifiable predictions

**Strengths:**
- **W1 — best partial recall:** B2 best-in-class overall — small precise spans served at L1, bulk scans at L2, byte-exact verification at L0. Predicts ≥ **20%** better B2 than S alone.
- **W2 — best composition:** B9 best-in-class — compose at L1, verify at L0. Predicts ≥ **10 points** above S on B9 success.

**Weaknesses:**
- **W3 — footprint:** B6 ≈ **3×** S's (three registries; no way around it).
- **W4 — selection overhead:** per-query cost ≥ S's; predicts B8 first-query latency ≥ **1.5×** S's.
- **W5 — selector misfires:** predicts ≥ **10%** of selections are suboptimal vs an oracle policy on sqlite3.c (task-dependent spans defeat the bucket statistics).

### (3) Falsification criterion — W dies if ANY ONE holds

1. Composite battery score does **not** beat S alone by ≥ **15%** (PROPOSED margin — if selection can't clear its own overhead by 15%, W is S with extra steps and unprincipled vibes), **OR**
2. the justification gate refuses **>5%** of selections (the selector is unsound and only the gate is saving it — the mechanism is cheating-shaped), **OR**
3. B7 determinism gate fails, **OR** the universal floor rule fires.

### (4) Buildability note

The heaviest arm: three registries + selector + justification gate, all pure Zag, all audited. L2 derivation reuses S's rule (no new math). The audit-ledger volume is the sleeper cost — one `GRAN_SEL` entry per query means the ledger grows with *query* count, not ingestion; budget it (16 words × queries) and consider ledger-striping in the build plan. If the ledger cost dominates, that itself is a finding about per-decision auditing granularity.

---

## ARM X — Whole-stream-as-one-chunk degenerate control (the absolute floor)

### (1) Mechanism sketch

The entire ingested stream is a single chunk with a single ID. Ingestion appends bytes to one buffer; recall(span) = slice the buffer at the offset; one `ADD` audit entry per ingestion batch. That is the whole arm.

### (2) What X can and cannot do

**Can:** byte-exact recall (B1 passes — slicing is slicing); trivial determinism (B7 passes — nothing to vary); minimal code; minimal B6 (one ID); honest, legible, fast to build.

**Cannot:** partial recall without touching the whole stream (any integrity/verification pass is O(stream)); sub-span reuse across contexts (pin 64 bytes → pin 15 MB; kill a sub-span → impossible; every context referencing any sub-span references the whole stream ID); surgical revision (one byte changes → new stream ID, *all* references re-keyed, audit log records a whole-stream re-key); composition (B9 degenerates to byte-slicing — offsets into the monolith, not assembly from units); **memory-op granularity** — promote/demote/strengthen/weaken/kill/pin become all-or-nothing over ~15 MB, which makes the deliberate-memory organ's entire vocabulary meaningless. X is what you get if "unit of knowledge" has no units.

### (3) Falsification criterion — X is the floor, so its criterion is the bar

X is **dead as a candidate** the moment any arm beats it on B2 by ≥10× **and** on B5 by ≥10× (expected: all of S, U, V, W clear this; T is the live question on single-file ingestion — which is itself a publishable finding about episode granularity). X's purpose is to be beaten. **Any arm S–W that cannot beat X on every one of B2/B4/B5/B9 is dead on arrival** (universal floor rule) — it is worse than doing nothing, and we say so in its verdict sheet.

### (4) Buildability note

An afternoon. Buffer + offset slicing + one audit op. Build it first — it validates the battery harness before any real arm runs, and its numbers are the denominator everything else divides by.

---

## Predicted scoreboard (falsifiable at a glance)

Rows = arms, columns = battery metrics. **best** = predicted class leader · **ok** = competitive · **poor** = predicted weak · **fatal** = predicted floor-level or dead-on-arrival risk · **—** = gate (pass/fail, unscored).

| Arm | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | B9 | B10 |
|-----|----|----|----|----|----|----|----|----|----|-----|
| S recall-driven | — | ok | ok | **best** | **best** | ok | — | poor | ok | ok |
| T episode-aligned | — | poor/fatal* | poor | poor | ok | **best** | — | **best** | poor | poor |
| U recompute | — | poor† | ok‡ | fatal (0) | **best** (0) | **best** (0) | — | ok | poor | **best** |
| V BPE enemy | — | ok | **best**§ | ok | poor | **best** | — | **best** | ok | **best** |
| W multi-granularity | — | **best** | ok | **best** | ok | poor | — | ok | **best** | ok |
| X whole-stream | — | fatal | — | fatal | fatal | **best** | — | **best** | poor¶ | — |

\* T's B2 on single-file sqlite3.c ingestion is predicted within 2× of X — its kill condition; on chatty ingestion it looks much better, which is the batching-fragility finding (W3).
† U's B2 in *bytes* is fine; in *ops* it's ≥5× D's — the table scores bytes, the head-to-head scores ops. Both are reported.
‡ U derives S's boundaries, so its B3 mirrors S's wherever the window covers the span.
§ V's B3 "win" is structural: fixed token boundaries trivially coincide with lexer boundaries more often. Scored honestly, weighted lightly — alignment-with-a-tokenizer is not the thesis.
¶ X "succeeds" at B9 by slicing, which is not composition — reported as a degenerate pass with an asterisk, scored as poor.

## What each arm needs from Micah (sign-offs)

1. **Composite weights** (B2 20 / B4 20 / B5 15 / B9 15 / B3 10 / B6 10 / B8 5 / B10 5 — PROPOSED).
2. **All numeric bars** in §(3) of each arm (1.5×/2×/10× margins, 25% churn, 80% sub-episode traffic, 15% W margin, 5% gate-refusal, λ/μ costing).
3. **U-vs-D:** the MA1/RC1 median memory-op rate per 1k episodes (read at prereg-freeze) that sets the churn level where a U win falsifies D's caching claim.
4. **V fairness checklist:** vocab 16,384, both-corpora training, frozen tie-breaks — before V's numbers count.
5. **Judgment-set parameters** (θ_merge, ρ, σ_split, τ, derivation window radius): values frozen per trial, logged in the prereg record — decided, never fitted mid-trial.

## Appendix: shared Zag representation sketches

```zag
// Integer IDs only. Slices are never compared with ==.
struct ChunkId { id: u32 }                       // tombstoned IDs never reused
struct Span   { chunk: u32, start: u32, len: u32 } // byte-exact addressing

// Audit ledger entry: 16 words, append-only.
struct AuditEntry {
    op: u32, slot: u32, rc: u32,
    b1: u32, b2: u32, b3: u32, b4: u32, b5: u32,
    a1: u32, a2: u32, a3: u32, a4: u32, a5: u32,
    stage: u32, d1: u32, d2: u32,
}
// Segmentation ops (in addition to memory ops):
//   CHUNK_ADD, CHUNK_MERGE, CHUNK_SPLIT, GRAN_SEL, EPISODE_BEGIN
// Counters in d1/d2; evidence snapshots in b1..b5/a1..a5.

// S crystallization state (per adjacent live-unit pair, ID-ordered scan):
struct PairCounters { left: u32, right: u32, j: u32, ia: u32, ib: u32 }

// Corpus buffers: striped, each stripe ≤ 2^24 bytes (well under the 2^25
// indexing limit); large structs' array fields aliased to locals before
// indexed access; _zag_arg(n) pointers never freed.
```

**Determinism note (all arms):** counters, thresholds, tables, and bucket statistics are logged state. A rerun replays inputs + state; the merge scan order (ascending ID), BPE tie-breaks (lowest rank, then leftmost), and selector argmax (lowest level id on ties) are all fully specified. Byte-identical output is a checkable property of every arm — B7 verifies it, it doesn't assume it.

---

*End of Crew 4 catalog: 6 arms (S, T, U, V, W, X). Proposed, not approved. Micah signs before build.*
