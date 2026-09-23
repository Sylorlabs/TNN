# ALPHABET G–L: Cut-Signal and Identity-Scheme Families

**Crew:** Brainstorm Crew 2 — TNN representation program ("what is a unit of knowledge if not an LLM token")
**Date:** 2026-09-20
**Status:** PROPOSED — frozen arms/bars below await Micah's sign-off before any build (prereg discipline).
**Thesis being served:** LLM tokens are a fixed discretization built for matrix math. TNN's units are
cognitive: chunking is an act TNN performs on the raw stream itself (no fixed tokenizer), vocabulary is
taught/learned like a child learns words, and a chunk is a byte span with a stable ID that memory points
back to, retrieves, and reuses (caching territory).

## The three orthogonal axes

Cut families (G, H) decide **where boundaries fall**. Structure families (I, J) decide **how chunks
relate**. Identity families (K, L) decide **what a chunk's ID means**. These axes are independent: any
cut policy can sit on any identity scheme. The final system will almost certainly take one pick per
column — which is why the arms below are written to compose, and why the K-vs-L comparison is run as a
bake-off rather than settled by argument.

## Cross-cutting laws (bind every arm)

1. **Determinism-from-logged-state.** Every cut/merge/promote/demote decision is a pure function of
   (input bytes, complete logged internal state). The audit log must record every input to the
   decision: evidence cited (`cite_ep`), weights/bars (prereg-frozen, part of state), tie-break order
   (slot/offset ascending, never hash-map iteration order, never wall clock). Then "same input + same
   complete logged internal state → byte-identical output" holds *by construction*. Any decision that
   reads unlogged state is a LAW VIOLATION and fails the build's determinism gate before any experiment
   runs. Judgments (strength is judgment-set, never formulaic) are still deterministic: a judgment is a
   function of logged state, not a formula — reproducibility requires the state be *complete*, not that
   the rule be arithmetic.
2. **Zero randomness in any decision path.** Tie-breaks are by ascending integer (slot, offset,
   tiling). Probing is linear from the hash (deterministic). There is no sampling anywhere.
3. **Bytes are append-only; pressure acts on the index.** The byte store is a sequence of immutable
   segments (each ≤ 2^25 bytes per the znc slice limit). A chunk record points at `(seg, off, len)`.
   `kill` drops the *record*, never the bytes. Segment GC is a deliberate, audited, future op — out of
   scope for these arms. This single rule defuses most "but the bytes are lost" objections below.
4. **New audit opcodes are cheap and visible.** The 16-word entry layout is unchanged
   (op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60); only new `op` codes are
   introduced, so they show up distinctly in the audit-ledger byte histogram (wave-11's first
   measurement). Proposed opcodes: `OP_ADD_CHUNK, OP_KILL_CHUNK, OP_CUT_PROPOSE, OP_CUT_COMMIT,
   OP_CUT_REFUSE, OP_MERGE, OP_SPLIT, OP_SUPER_ADD, OP_LINK_PARENT, OP_TILING_BIRTH, OP_TILING_DEATH,
   OP_DEDUP_HIT, OP_REVISE_LINK, OP_SEG_SEAL`. Existing memory ops (add/kill/pin/promote/demote/
   strengthen/weaken) keep their codes; chunk lifecycle ops are new codes so the histogram can tell
   "memory administration" apart from "representation work".

## Shared record sketch (all arms build on this)

```
Chunk {                       // live-store record, fixed struct, slot-indexed
  id:     u64[4]              // K: sha256 quad | L: (stream,seg,off,len) packed | else: serial in id[0]
  seg:    u32                 // byte-store segment (immutable once sealed)
  off:    u32                 // offset within segment
  len:    u32
  level:  u8                  // I: hierarchy level (0 = finest)
  tiling: u8                  // J: which tiling this record belongs to
  value:  i64                 // MA4 signed judgment (-: negative judgment about this memory)
  strength:u8                 // judgment-set, never formulaic
  flags:  u8                  // bit0 = pin (force-pin is human/trainer-only, audited, visible)
  refcount:u32                // K: dedup reference count
  parent: i32                 // I: parent slot, -1 = none
  child_head: i32             // I: head of child slot linked-list, -1 = none
}
```

- Content compare is **never** slice `==`: byte spans compare via explicit deterministic byte loops;
  IDs compare as integer words. (Zag gotcha honored.)
- Large structs' array fields are aliased to locals before indexing. (Zag gotcha honored.)
- Staging/stream buffers are chunked at ≤ 2^25 bytes. sqlite3.c (~9.5 MB) and Shakespeare (~5.4 MB)
  each fit in one slice, but staging + segment copies are still chunked defensively. (Zag gotcha honored.)

## Corpora and scale for the bake-offs

- **Corpus A (static, repetitive):** Project Gutenberg Shakespeare, ~5.4 MB prose.
- **Corpus B (structured, repetitive boilerplate):** sqlite3.c, ~9.5 MB code.
- **Corpus C (revision-heavy, synthetic):** Corpus B plus a preregistered patch series (N=100
  deterministic edits at known positions) — the revision stressor for K-vs-L.
- Baseline for every cut arm: fixed 64-byte grid (the precedent: 64-byte chunks, byte-exact recall).
  In arm J the baseline is not a separate experiment — it is a competing *tiling*.

---

## ARM G — Memory-pressure cuts: chunking as triage

### G1 — Pressure-driven coarsening (reactive triage)

**(1) Mechanism.** The deliberate memory substrate tracks `occupancy = live_slots / capacity`
(a pure function of logged state). Two prereg-frozen thresholds: WARN at 80%, CRITICAL at 95%.
At CRITICAL the consolidation/promotion organ (organ 3) executes triage: pick the lowest-value
*adjacent* chunk pairs (by MA4 signed `value`, tie → lowest slot — deterministic) and coarsen them:
`add(superchunk covering both spans)` + `kill(left)` + `kill(right)`, each audited
(`OP_ADD_CHUNK` + 2× `OP_KILL_CHUNK` + one `OP_MERGE` linking the three, citing the pressure episode).
Pinned chunks (including human force-pins) are immune and never selected; negative-value chunks are
selected *first* (MA4: TNN may hold negative judgments — triage spends them first). The cut policy for
the *incoming* stream simultaneously coarsens: new chunks are cut at 2× the current mean length until
occupancy drops below WARN (hysteresis, frozen). Bytes are never lost: kills drop records; the spans
remain addressable in the append-only byte store, and the `OP_MERGE` record stores both cut points, so
a later deliberate re-split (`OP_SPLIT`) is byte-exact.

Interaction with kill/pin/promote: triage is implemented *only* from those primitives plus `OP_MERGE`
as the linking record — no new privileged op. A force-pinned chunk can never be merged away; an
overseer-visible audit trail shows every triage victim.

**(2) Falsifiable predictions.**
- *Strength:* granularity becomes a function of remembered value — high-value spans keep fine
  granularity under pressure while low-value spans compress. Predicts: byte-exact recall on pinned /
  top-decile-value chunks stays ≥ 99% at 95% occupancy, while a value-blind coarsener degrades them.
- *Strength:* triage is O(pairs) integer selects — cheapest structural response available.
- *Weakness:* reactive coarsening can thrash — merge under pressure, then deliberately re-split when
  the fine structure is needed. Predicts measurable re-split rate.
- *Weakness:* adjacency-merge is dumb about *meaning*: it can fuse two unrelated spans that merely
  sat next to each other, creating junk superchunks that pollute recall.

**(3) Kill criterion (exact — any one kills G1).**
- Thrash: if ≥ 5% of triage-merged superchunks are re-split by deliberate revision within the same
  run on either corpus → G1 dies (it is destroying structure faster than judgment rebuilds it).
- Value-blindness: if byte-exact recall on pinned chunks drops > 1% vs the no-pressure control at
  matched occupancy → G1 dies (triage is eating what it should protect).
- Junk fusion: if ≥ 10% of superchunks are never recalled *nor* re-split (dead weight created by
  triage) → G1 dies.

**(4) Buildability.** Trivially pure-Zag: occupancy counter, deterministic selection over a fixed
array (insertion sort on `(value, slot)` — no randomness, no slice `==`). Audit cost per merge:
4 entries (1 add + 2 kills + 1 merge-link); a full CRITICAL sweep over M pairs = 4M entries, bounded
by live slots. Hazards: none exotic. The only subtlety is the hysteresis band — WARN/CRITICAL must be
frozen integers in the prereg, not floats, so the pressure signal is bit-reproducible.

### G2 — Pressure-gated deliberate cuts (pressure as trigger, never as policy)

**(1) Mechanism.** Same pressure signal as G1, but crossing WARN never auto-coarsens. Instead it
*triggers* a bounded deliberation session run by the hypothesis organ (organ 2) under the rules of
arm H: propose candidate restructures (merge pairs, re-cut regions, kill negatives), weigh evidence,
commit or refuse, budget-capped. Pressure is the *alarm*; deliberation is the *response*. All
structural change stays inside deliberate ops — G2 is "G's signal + H's discipline." If the session
refuses every proposal (evidence below bar), the system instead sheds load only through already-
deliberated kills of negative-value chunks — never through un-deliberated merges.

**(2) Falsifiable predictions.**
- *Strength:* zero thrash by construction — every merge earned its evidence bar. Predicts re-split
  rate < 1% where G1 shows ≥ 5%.
- *Strength:* under sudden pressure spikes, G2 preserves recall quality better than G1 (deliberation
  picks *which* structure to sacrifice).
- *Weakness:* cost — a deliberation session per pressure event is 10–100× the ops of G1's sweep.
- *Weakness:* latency — the stream keeps arriving during deliberation; the staging buffer must absorb
  it (bounded; overflow is itself a pressure input, audited).

**(3) Kill criterion (exact).** If G2's recall-quality advantage over G1 at matched occupancy is
< 2 absolute points on byte-exact recall *or* its deliberation cost per pressure event exceeds 50×
G1's sweep cost with no quality advantage → G2 dies (deliberation isn't buying anything).

**(4) Buildability.** Same data structures as G1 + H's proposal machinery (see arm H). Audit cost:
session open/close (2) + per-proposal `OP_CUT_PROPOSE` + commit/refuse (bounded by budget B).
Hazard: the trigger itself must be deterministic — WARN crossing is evaluated at fixed episode
boundaries, not mid-stream, so two reruns trigger at the same point.

**G1 vs G2 is the no-free-lunch pair:** cheap/reactive vs expensive/principled, same signal. Build
both; the bake-off decides.

---

## ARM H — Deliberate cuts via inspect/propose/commit: boundaries as cognitive acts

### H1 — Full deliberation per boundary (the most agentic chunking)

**(1) Mechanism.** The incoming stream is held in a staging buffer (window W bytes, frozen, e.g.
4 KiB). Nothing is cut until decided. The hypothesis organ (organ 2) proposes candidate cut points;
the proposal space is bounded: deterministic "noticers" (byte-class transitions — alnum→space,
newline runs, punctuation clusters — *heuristics that propose, never decide*) nominate at most C
candidates per window (C frozen, e.g. 16; surplus candidates are dropped lowest-priority-first by a
frozen priority order — deterministic). For each candidate, evidence is weighed by the eliminative
logic:
  (a) **separation evidence** — does the cut separate internally-predictable spans? (integer
      n-gram surprise delta over the staged bytes; pure function of staged bytes);
  (b) **reuse evidence** — do the resulting spans already exist in store (dedup hits under K, or
      exact-span matches)? Caching territory: a cut that creates re-findable chunks is rewarded;
  (c) **value evidence** — signed prior value of the resulting spans (cheap, from taught vocabulary
      and pinned chunks);
  (d) **vocabulary alignment** — does either side match a taught/pinned chunk?
  Score = frozen-weight integer sum (weights in prereg, part of logged state). Commit iff
  score ≥ BAR (frozen); else `OP_CUT_REFUSE` (refusal is a first-class audited outcome — the system
  *decided not to cut*, citing the episode). Committed cuts advance the frontier; refused regions are
  re-staged or emitted as one coarse fallback chunk (`OP_CUT_COMMIT` with `fallback=1` — the
  "no-decision decision," still audited). **Rollback:** a bad cut is revised by the structural-revision
  organ (organ 5): `OP_MERGE` fuses what shouldn't have split; a bad non-cut is re-proposed at the
  next trigger. Rollback cites the recall-failure episode that exposed the bad cut (`cite_ep`).

**(2) Falsifiable predictions.**
- *Strength:* every boundary earns its existence — predicts the highest reuse hit rate (fraction of
  recalls served from existing chunks with no new adds) of any cut arm, and best alignment with
  taught vocabulary (taught chunks are rarely re-cut).
- *Strength:* refusals are informative — predicts the refusal log *predicts* future re-splits
  (regions refused-then-fallback-cut get re-cut more often than committed regions; the system knows
  what it doesn't know).
- *Weakness:* cost — deliberation per candidate is the most expensive cut decision in the alphabet;
  per-byte cost is 100–1000× the fixed grid.
- *Weakness:* the evidence weights are themselves judgments — infinite regress is stopped only by the
  prereg-frozen bar. If the bar is wrong, every cut is confidently wrong.

**(3) Kill criterion (exact — any one kills H1).**
- No advantage: if H1's reuse hit rate does not exceed the fixed-64B baseline by ≥ 10 absolute
  points at equal live-store slots on both corpora → H1 dies (deliberation buys nothing).
- Non-convergence: if refusal rate > 30% *and* mean deliberation ops per committed cut > 10^4 →
  H1 dies as untestable at scale (H2 inherits the question at lower cost).
- Bar brittleness: if shifting BAR by ±10% (sensitivity run, preregistered) flips > 25% of cut
  decisions → H1 dies (decisions are bar-noise, not evidence).

**(4) Buildability.** Pure-Zag: staging buffer (chunked ≤ 2^25), fixed-size candidate array,
integer scoring, deterministic selection. Audit cost per window: ≤ C proposes + ≤ C commit/refuse +
frontier advance — bounded by B (budget). Hazard: the noticers must be *provably* proposal-only —
a test asserts that disabling all noticers except the coarsest still yields valid (if coarse) cuts,
so no tokenizer is smuggled in as a "heuristic." Second hazard: evidence (a) needs n-gram tables —
fixed-size integer arrays, deterministic updates, no randomness.

### H2 — Budgeted deliberation (H1 under a compute cap)

**(1) Mechanism.** Identical to H1 except: hard budget of B candidate-evaluations per window
(B frozen, e.g. 8); candidates are evaluated in frozen priority order; when the budget is spent, all
remaining candidates are refused in bulk (one `OP_CUT_REFUSE` with `bulk=1`) and the frontier advances
with the fallback coarse cut. Deliberation becomes a *scarce resource the system allocates* —
which is itself a cognitive act worth studying (where does TNN spend its cut budget?).

**(2) Falsifiable predictions.**
- *Strength:* predicts ≥ 80% of H1's reuse-hit-rate advantage at ≤ 25% of H1's deliberation cost
  (deliberation has diminishing returns; the first few candidates carry the signal).
- *Weakness:* budget starvation on complex windows (code with dense structure) — predicts H2's
  fallback rate spikes on corpus B vs corpus A, while H1's does not.

**(3) Kill criterion (exact).** If H2's reuse advantage over baseline is < 5 absolute points *or*
its fallback rate on corpus B exceeds 40% of windows → H2 dies (the budget destroys the deliberation).

**(4) Buildability.** H1's structures plus a decrementing budget counter. Audit cost strictly ≤ H1.
Hazard: none beyond H1's.

---

## ARM I — Hierarchical chunks: chunks of chunks

### I1 — Strict tree (single parentage)

**(1) Mechanism.** Level 0 = finest cuts (from G/H or the baseline grid). **Level-formation rule:**
a run of 2–8 adjacent same-level chunks becomes a superchunk candidate when either (a) their
co-recall count (recalled together within one trace-composition episode, organ 4) reaches T_co
(frozen, e.g. 7), or (b) the consolidation organ (organ 3) deliberately promotes the group on other
cited evidence. Formation = `OP_SUPER_ADD` (new record at level+1, own ID) + `OP_LINK_PARENT` per
child (both directions linked: child→parent slot, parent→child list head). **ID scheme across
levels:** `(level, serial)` packed into `id[0]` — integer selectors, level in high bits; a chunk's
full identity is level-scoped, so "the word" (level 1) and "its bytes" (level 0) are distinct
addressable units. **Recall traversal:** top-down (superchunk → children spans, for "give me the
phrase") or bottom-up (span → parent chain, for "what is this part of"); the trace-composition organ
walks deterministically (children in slot order). **Demotion:** a superchunk unrecalled for E
episodes (frozen) is demoted by organ 3 — `OP_KILL_CHUNK` on the superchunk; children survive
(structure dissolves downward, never upward). Max level 4 (frozen) — depth is a deliberate cap, not
an emergent accident. Revision cascade: if a level-0 chunk is re-cut (H rollback) or revised (K),
its ancestors are marked stale (`OP_LINK_PARENT` with `stale=1`) and rebuilt or dissolved by organ 5
— stale parents are never silently served.

**(2) Falsifiable predictions.**
- *Strength:* linguistic hierarchy without a tokenizer — predicts level-1 chunks converge on
  word-like spans on corpus A and token-like spans on corpus B *without any language-specific code*
  (measured: boundary agreement with whitespace/punctuation ≥ 70% at level 1, emergent not imposed).
- *Strength:* multi-granularity recall — recalling a phrase costs one lookup instead of N; predicts
  recall-op count drops ≥ 3× on repeated phrases vs flat chunks.
- *Weakness:* parent-maintenance overhead — every level-0 revision cascades; predicts maintenance
  ops dominate on revision-heavy corpus C.
- *Weakness:* level explosion of junk — frequent-but-meaningless co-occurrences (e.g. `";\n"` in
  code) become superchunks; predicts ≥ 15% of level-1 nodes are never recalled above their children
  (hierarchy for hierarchy's sake).

**(3) Kill criterion (exact — any one kills I1).**
- No depth value: if level-2+ superchunks account for < 5% of successful recalls at equal store cost
  vs flat chunks → I1 dies (hierarchy beyond words is decoration).
- Maintenance swamp: if parent-maintenance + stale-rebuild ops exceed 20% of total audit ops on any
  corpus → I1 dies (the tree costs more than it saves).
- Non-emergence: if level-1 boundary agreement with natural breaks is < 50% on corpus A (no better
  than chance given the cut distribution) → the "emergent words" claim dies with it.

**(4) Buildability.** Pure-Zag: chunk records in a fixed array, child linked-lists via slot indices
(`child_head`/`next_sibling` as i32 — no pointers, no allocation), parent backlink per chunk.
Co-recall counting = fixed-size integer counters on candidate groups. Audit cost per formation:
1 super-add + k link entries (k ≤ 8). Hazard: traversal must be cycle-free — enforced structurally
(single parent, strictly increasing level), asserted by a build-time checker. Hazard 2: the
`child_head` linked list under merge/split — updates must be total (every affected link re-audited)
or traversal silently skips children; a deterministic invariant checker runs per episode in test
builds.

### I2 — DAG (multi-parent: one span, several wholes)

**(1) Mechanism.** I1 except a chunk may have up to P parents (P=3 frozen) — the same byte span can
belong to "the phrase," "the idiom," and "the code block" simultaneously. Parent slots stored as a
small fixed array `parents[P]` (integer selectors; -1 = empty), ordered by slot. Formation rule as
I1, but a group may attach to an *existing* superchunk as an additional parent link rather than
always forming a new node (dedup of wholes — the hierarchy gets K-like sharing). Demotion kills one
parent link at a time (link-level `OP_KILL_CHUNK` with `link_only=1`); the superchunk dies only when
its last link/reference goes.

**(2) Falsifiable predictions.**
- *Strength:* sharing of substructure — predicts 20–40% fewer superchunk records than I1 at equal
  recall coverage (the same words serve many phrases).
- *Weakness:* ambiguity — bottom-up recall ("what is this part of?") now returns up to P answers;
  predicts arbitration picks the wrong parent ≥ 10% of the time vs ground-truth phrase on corpus A
  unless a parent-ranking rule (highest superchunk value, tie → lowest slot) is added — which is
  itself a new judgment to preregister.

**(3) Kill criterion (exact).** If I2's record savings over I1 are < 10% *or* parent-arbitration
error exceeds 10% → I2 dies (complexity without payoff); I1 remains the hierarchy candidate.

**(4) Buildability.** `parents[P]` fixed array — pure Zag, no hazard beyond I1's. Audit cost per
formation: 1 super-add (sometimes 0, if attaching) + link entries. Hazard: the attach-vs-form
decision must be deterministic — rule: attach iff an existing superchunk covers *exactly* the group
(coverage test is integer span equality); else form. No similarity threshold (thresholds are
judgments needing bars; exact coverage keeps it mechanical).

---

## ARM J — Overlapping tilings: no canonical cut

### J1 — Fixed-k competing tilings

**(1) Mechanism.** The stream carries **k simultaneous segmentations** (k=3 frozen): T0 = deliberate
cuts (H output), T1 = T0 phase-shifted by half the running mean chunk length (deterministic shift,
recomputed per sealed segment), T2 = fixed 64-byte grid (the baseline, demoted from "experiment" to
"competitor"). Every chunk record is tagged with its tiling (`tiling: u8`); the same bytes exist as
*separate records* in each tiling (under K identity they share payload via hash; under L they are
distinct position records — tilings compose with either). **Coexistence:** tilings are peers; none is
canonical. **Recall arbitration:** a query span gathers covering chunks from all tilings; score =
α·value + β·recency − γ·overhang (overhang = bytes the chunk covers beyond the query; α,β,γ frozen
integers); pick max, tie → lowest (tiling, slot). Arbitration is a pure function of logged state —
no randomness, reproducible. **Explosion prevention:** (i) hard cap k; (ii) tiling-level accounting —
each tiling's chunks carry a running recall-share; a tiling whose share < 5% over a frozen window is
put to deliberate death (`OP_TILING_DEATH`, its chunks killed in one audited sweep unless individually
pinned); (iii) new tilings are born *only* through H-style deliberate proposal (`OP_TILING_BIRTH`
cites the evidence — e.g. arbitration systematically prefers a phase no tiling covers).

**(2) Falsifiable predictions.**
- *Strength:* robustness to bad cuts — predicts byte-exact recall under adversarial cut placement
  (cuts forced through the middle of taught words) degrades ≤ 3 points with k=3 vs ≥ 15 points for
  any single tiling (some other phase always covers the span cleanly).
- *Strength:* boundary uncertainty is *represented* rather than prematurely collapsed — predicts
  arbitration disagreement rate (top-2 tilings within γ of each other) correlates with regions H
  refused to cut (the system visibly doesn't know, in the right places).
- *Weakness:* k× memory for chunk records (payload shared under K, but records/index ×k).
- *Weakness:* arbitration can be systematically wrong — if T2's grid chunks have high recency
  (recently added), recency bias can outvote better-fitting T0 chunks; predicts arbitration error
  concentrates where tilings differ most in chunk age.

**(3) Kill criterion (exact — any one kills J1).**
- No robustness gain: if best-of-3 arbitration recall ≤ best single tiling recall + 2 points at
  equal total chunk budget on the adversarial-cut corpus → J1 dies (the extra tilings are passengers).
- Arbitration failure: if arbitration picks a chunk that does not byte-cover the query span
  (coverage bug) even once, or picks a lower-scoring-by->γ-margin chunk > 5% of recalls →
  J1 dies (the arbiter can't be trusted; recall must be exact).
- Tiling churn: if the birth/death cycle turns over all k tilings within one corpus pass (no tiling
  survives — perpetual disagreement) → J1 dies (competition never converges).

**(4) Buildability.** Pure-Zag: tiling tag is one byte in the record; per-tiling counters are small
integer arrays; arbitration is a linear scan with deterministic tie-break. Audit cost: each tiling's
adds (×k records vs single) + arbitration needs *no* audit (read-only; reproducible from state) +
birth/death sweeps (bounded). Hazard: T1's phase shift must be a deterministic function of sealed
segment state — compute at seal time, log the shift in `OP_SEG_SEAL`, never recompute mid-stream.

### J2 — Evidence-gated tiling birth/death (tilings as hypotheses)

**(1) Mechanism.** J1 except k is not frozen at 3 — it is bounded above by K_max (frozen, e.g. 5) and
tilings are treated as *hypotheses about the stream's natural joints*, managed by the eliminative
organ: birth requires committed H-style evidence (a phase that arbitration demonstrably needs);
death requires sustained low recall-share *or* subsumption (another tiling's chunks cover ≥ 95% of
its recall wins — the tiling is redundant, killed by evidence not by cap). k=1 is allowed if
evidence supports a single canonical tiling — J2 can *discover* that J is unnecessary, which is the
honest outcome.

**(2) Falsifiable predictions.**
- *Strength:* predicts k converges to 2 on corpus A (prose has one dominant phrasing + one offset
  shadow) and 3 on corpus B (code's nested structure sustains more phases) — a testable,
  corpus-specific prediction about the stream, not the machine.
- *Weakness:* birth/death deliberation is another H-cost center; predicts tiling-management ops
  exceed 10% of total ops on corpus C (revisions keep invalidating phases).

**(3) Kill criterion (exact).** If k does not converge (oscillates birth→death→birth for the same
phase twice on one corpus pass) *or* converges to 1 on all corpora (tilings were never needed) →
J2 dies (and J1 with it — the family collapses to single-tiling).

**(4) Buildability.** J1's structures + birth/death evidence records. Audit cost: birth = 1 +
full tiling adds (the expensive part — a newborn tiling re-segments sealed history, bounded by
K_max); death = 1 + sweep. Hazard: re-segmenting sealed history must not mutate sealed segments —
new tiling records point at the same immutable `(seg, off, len)` byte ranges; only records are new.

---

## ARM K — Content-addressed IDs: identity is WHAT

### K1 — Full SHA-256 identity (git-style, native)

**(1) Mechanism.** `ID(chunk) = SHA-256(byte content)`, computed with the substrate's native
`R33_NATIVE_SHA256_V2.zag` (already imported by `substrate/cl/common.zag` — no new crypto code, and
per AGENTS.md the trial substrate dir must carry that file next to `cl/`). The 256-bit digest is
stored as `u64[4]` in the record — compared as four integer words, never slice `==`. **Dedup table:**
open-addressing hash table keyed on the digest quad; on `add`, compute digest, probe deterministically
(linear probe from `digest[0] mod capacity`); hit → `OP_DEDUP_HIT` (refcount++, audited — reuse is
visible work, not a silent shortcut) and the existing slot is returned; miss → new record.
Identical spans anywhere — across tilings (J), across streams, across time — are *one* record:
this is Micah's "caching territory" in its purest form. **Collision handling without randomness:**
on digest equality, full bytes are compared deterministically (explicit byte loop over the
append-only byte store); a true digest collision chains by *insertion order* (logged) in a
slot-linked list — the ID stays the digest, disambiguated by chain position. The chain path is
exercised in tests with synthetic forced collisions (deterministic vectors, preregistered — not
random). **Revision:** a revised chunk's content hashes differently, so its identity **dies by
definition** — this is honest, not a bug. Lineage is preserved by `OP_REVISE_LINK(old_id → new_id,
reason, cite_ep)` from the structural-revision organ; recall follows revision links (append-only
chain) to the live ID. References never dangle; history is never rewritten.

**(2) Falsifiable predictions.**
- *Strength:* dedup on repetitive corpora — predicts ≥ 40% payload-byte savings on corpus A
  (Shakespeare repeats character names, common words, verse patterns) and ≥ 25% on corpus B
  (boilerplate, repeated idioms) vs sequential IDs. The caching claim is *measured*, not asserted.
- *Strength:* byte-identical reruns fall out of the design — the ID is a pure function of content,
  so replays cannot diverge on identity.
- *Strength:* cross-tiling sharing — under J, the same span in two tilings shares one payload
  record (two records, one payload); predicts J's memory cost drops to ~1.2× single-tiling instead
  of ~3×.
- *Weakness:* position-blindness — "the" at line 10 and "the" at line 10,000 are one chunk; role
  and context must come from *links* (parents in I, tiling tags in J), never from the ID. Predicts
  disambiguation failures where link context is thin (isolated single-word recalls).
- *Weakness:* revision churn — every edit re-IDs; predicts reference-following cost (link-chain
  length) grows linearly with edit count on corpus C, and recall latency degrades unless chains are
  compacted (compaction = deliberate audited op, future work).
- *Weakness:* near-dupe brittleness — spans differing by one byte share nothing; cut-phase
  differences (J's whole point) defeat dedup at the byte level.

**(3) Kill criterion (exact — any one kills K1).**
- Dedup failure: if payload savings are < 15% on corpus A (the friendliest corpus) vs sequential
  IDs at equal recall accuracy → the caching claim dies with K1.
- Churn swamp: if on corpus C the mean revision-link chain length exceeds 8 *and* recall latency
  exceeds 2× the no-revision baseline → the revision-link mechanism dies (keep hash IDs, drop links,
  accept dangling references as a documented limit — or kill K1 outright if references must not dangle).
- Disambiguation failure: if > 5% of single-span recalls return a contextually wrong occurrence
  (right bytes, wrong role — measured against annotated ground truth on a corpus-A sample) → K1
  dies as a *standalone* scheme (survives only composed with L, i.e. the K3 hybrid).

**(4) Buildability.** The easiest strong arm to build: native SHA-256 import exists; the table is a
fixed-capacity array of quads + slots with linear probing (deterministic, no randomness); digest
compare is four integer compares. Audit cost: 1 `OP_ADD_CHUNK` per unique span, 1 `OP_DEDUP_HIT`
per repeat (cheap, fixed size). Capacity: table sized at 2× expected unique spans (frozen); resize =
deliberate audited rebuild (rare; corpora sizes are known up front). Hazards: (i) the SHA-256 import
path — trial substrate dirs must carry `R33_NATIVE_SHA256_V2.zag` + `R33_NATIVE_IO_V1.zag` next to
`cl/` (AGENTS.md lesson); (ii) hashing streams the chunk bytes — chunks are ≤ 64 B–4 KiB, far under
the 2^25 slice limit; (iii) **never** use slice `==` on digests — quad integer compare only.

### K2 — 64-bit FNV-1a identity (cheap hash, honest collisions)

**(1) Mechanism.** K1 except `ID = FNV-1a-64(content)` — ~15 lines of pure Zag, no native import,
computable anywhere. The dedup table, linear probing, insertion-order chains, byte-compare
confirmation, and revision links are identical. The point of K2 is not to beat K1 on strength but to
price the hash: how much dedup survives when the ID is 64 bits and collisions are *expected* at
scale (birthday bound ~2^32 spans — reachable in long runs, unlike SHA-256).

**(2) Falsifiable predictions.**
- *Strength:* predicts ≥ 95% of K1's dedup savings at ~10× lower hash cost per add (measured ops).
- *Weakness:* predicts collision chains actually engage on corpus B at 10× scale (the honest-collision
  path gets real exercise, not just synthetic tests) — chain-walk cost becomes measurable.

**(3) Kill criterion (exact).** If K2's dedup savings are within 2 points of K1's *and* its per-add
cost is lower → K1 dies on cost grounds (keep K2; strength was never the differentiator). If chain
lengths exceed 4 on any corpus run → K2 dies (64 bits is too small for the store's lifetime).

**(4) Buildability.** Trivially pure-Zag; no native dependency — K2 builds even where the SHA-256
substrate file is absent. Same audit costs as K1. Hazard: none beyond K1's slice/`==` rules.

**K1 vs K2 is the no-free-lunch pair:** cryptographic strength + native dependency vs 15 lines of
Zag + real collisions. The bake-off prices the hash.

---

## ARM L — Position-addressed IDs: identity is WHERE

### L1 — Absolute position (stream, segment, offset)

**(1) Mechanism.** `ID(chunk) = (stream_id, seg_id, local_off)` packed into `id[0..1]` — identity is
*where the bytes live*, not what they are. **Surviving insertions/revisions:** segments are immutable
once sealed (`OP_SEG_SEAL`); an insertion or revision never shifts existing offsets — it appends a
*new* segment, and a revision map (`old (seg,off) → new (seg,off)`, append-only, audited via
`OP_REVISE_LINK`) records the move. A position ID is therefore **eternal**: position p keeps its ID
forever, even as its bytes change — the exact inverse of K, where the bytes keep their ID and the
position doesn't. Lookup is O(1): fixed-size segments ⇒ `seg_id = off >> SHIFT` (or a binary search
over the sealed segment table for variable segments — deterministic either way). Sequential recall
("what comes after X") is free: offset order *is* stream order, no index needed.

**(2) Falsifiable predictions.**
- *Strength:* reference stability — predicts **zero** ID churn across the entire corpus-C patch
  series (100 revisions; K re-IDs every touched span). The "current text at position p" query is
  always answerable.
- *Strength:* ordered traversal with no index structure — predicts sequential-scan recall is the
  fastest of any arm (no table probe, no tree walk).
- *Weakness:* no dedup — "the" at 10,000 positions is 10,000 chunks. Predicts store cost ≥ 2× K1
  on corpus A with *identical* recall accuracy (pure waste, measured not argued).
- *Weakness:* segment fragmentation — 100 revisions on corpus C produce ≥ 100 segments; predicts
  the segment table stays correct but positional *locality* degrades (adjacent logical positions
  scatter across segments), hurting prefetch-style recall.

**(3) Kill criterion (exact — any one kills L1).**
- Waste without win: if store cost exceeds 3× K1 on corpus A with no recall-accuracy advantage →
  L1 dies as a *primary* scheme (may survive as a secondary index — see K3).
- Stability failure: if *any* revision batch changes an existing position ID (eternity violated) →
  L1 dies outright (its one promise, broken).
- Fragmentation collapse: if mean segments-touched per sequential recall exceeds 4 on corpus C →
  L1 dies (fragmentation ate the locality advantage).

**(4) Buildability.** The simplest arm: segment table = fixed array of `(base, len, sealed)`;
position pack/unpack is integer shifts; the revision map is a small append-only array with linear or
binary lookup. Audit cost: 1 `OP_SEG_SEAL` per segment + 1 `OP_REVISE_LINK` per moved span.
Hazards: none — no hashing, no probing, no trees. (This simplicity is itself a finding: position
identity is nearly free; content identity is where the machinery lives.)

### L2 — Epoch-relative position (compact, translating)

**(1) Mechanism.** L1 except the ID is `(epoch, off)`: a *major* revision (deliberate, audited,
organ 5) bumps the epoch and installs a translation table old-epoch → current segments. Minor edits
stay inside the epoch as L1 segments. The ID is shorter (two words) and epoch comparison answers
"is this reference current?" in one integer compare — but old-epoch references need translation
(the table is append-only and audited, so translation is reproducible).

**(2) Falsifiable predictions.**
- *Strength:* predicts ID width and comparison cost drop vs L1 with identical stability *within* an
  epoch.
- *Weakness:* predicts translation-table misses (reference to a compacted-away epoch) on long
  corpus-C runs — the "eternal ID" promise now has fine print.

**(3) Kill criterion (exact).** If any within-epoch ID changes (same bar as L1) *or* translation
misses exceed 1% of cross-epoch recalls → L2 dies (it kept L1's complexity costs while breaking
L1's promise).

**(4) Buildability.** L1's structures + epoch counter + translation table (fixed array, linear
search — epochs are few). Audit cost: +1 per epoch bump. Hazard: epoch-bump criteria must be
prereg-frozen ("major revision" needs a definition — e.g. > 5% of segments touched — or the bump
is itself an undeliberated judgment; frozen integers only).

---

## IDENTITY-SCHEME COMPARISON: K vs L head-to-head

K and L are duals. K says a unit of knowledge is **what it is** (bytes → ID; position is accidental).
L says a unit of knowledge is **where it stands** (position → ID; bytes are accidental). Micah's
"caching territory" is K's home field; "the current text at position p" is L's. Neither subsumes the
other — the honest question is *under what stream conditions each wins*, settled by experiment, not
by which sounds deeper.

### On-paper conditions

| Condition | Winner | Why |
|---|---|---|
| High repetition, static text (corpus A) | **K** | Dedup converts repetition into saved bytes; L pays per occurrence. |
| Revision-heavy stream (corpus C) | **L** | Zero ID churn; K re-IDs every touched span and grows link chains. |
| Positional recall ("next", "at offset") | **L** | Offset order is stream order; K needs a separate order index. |
| Cross-stream / cross-time reuse ("have I seen these exact bytes before?") | **K** | The dedup table *is* the answer; L cannot even ask the question without byte comparison. |
| Near-duplicate spans (edits of one byte) | **neither** (both fail differently) | K: no sharing at all. L: shares position, not content. This is the known hole both schemes leave — flagged for a future arm (similarity-addressed IDs), not smuggled into this bake-off. |
| Taught vocabulary ("the word *quark*") | **K** (with links) | The taught thing is a byte pattern; K gives it one eternal ID. L gives it one ID per occurrence — teaching becomes enumeration. |
| Sensor-spoofing / lying inputs (integrity red-team) | **K** | Content identity makes tampering *visible*: changed bytes = changed ID = new record + revision link. Under L, spoofed bytes at a trusted position keep the trusted ID — L is the weaker scheme under adversarial input, and the red team should attack it there. |

### The discriminating experiment (preregistered, Micah signs)

Three corpus conditions × two schemes (+ hybrid, below), all at 10× scale, byte-identical reruns:
- **(a)** corpus A static; **(b)** corpus B static; **(c)** corpus C revision series (100 deterministic
  patches); **(d)** adversarial permutation: corpus A with paragraphs deterministically reordered
  (tests K's position-blindness against L's content-blindness — same knowledge, new positions).

Metrics (all integer-counted, no floats in bars):
1. `store_cost` = total bytes (payload + index + audit) per input MB. Lower wins.
2. `dedup_ratio` = 1 − unique_payload_bytes / input_bytes (K's home metric).
3. `ref_stability` = fraction of pre-revision references whose ID is unchanged after each patch
   batch (L's home metric; K is *expected* to score low — the question is how low).
4. `recall_latency` = mean deterministic ops per byte-exact recall.
5. `recall_accuracy` = byte-exact recall success rate on a preregistered query set (includes
   positional queries "bytes at p" and content queries "occurrences of span s" — each scheme gets
   its home queries *and* the other's, so neither wins by query selection).

**Kill rules for the comparison:**
- If K does not beat L on `store_cost` by ≥ 2× on condition (a) → K's caching claim dies; K is
  demoted to a secondary content index.
- If L scores < 100% on `ref_stability` on condition (c) → L's eternity claim dies; L is demoted.
- If either scheme's `recall_accuracy` trails the other by > 5 points on the *combined* query set
  → it dies as primary.
- If the hybrid (below) beats both pure schemes on ≥ 3 of 5 metrics → both pure schemes are
  demoted to *components*; the hybrid becomes the identity substrate.

### K3 — The composite both schemes are secretly asking for (proposed 13th design)

`ID = (content_hash, stream, seg, off)`: the **payload** is content-addressed (K1's dedup table owns
the bytes; identical spans share one payload record), the **reference** is position-addressed (L1's
eternal position ID is what memory points at). A chunk record holds both: `id_content = sha256
quad` for the bytes, `id_pos = (stream, seg, off)` for the reference. Revision changes the content
hash (new payload, possibly deduplicated against existing spans — an edited span that now matches
another span *merges for free*) while the position ID stands still. Teaching points at content
hashes ("the word *quark*" = one payload); sequential recall walks position IDs. The audit records
both (`OP_ADD_CHUNK` carries the quad in b1..b4 and the position in a1..a2 — the 16-word layout has
room). Cost: both indexes maintained — the experiment prices it. **K3 is not smuggled in as the
winner; it is the third arm in the bake-off**, per no-free-lunch. If it loses, the program takes the
pure winner and documents what the loser was good for.

---

## Recommended experiment matrix (no-free-lunch order)

Build order follows dependency, not favoritism — every cut arm needs an identity scheme underneath:

1. **Identity substrate first:** K1 vs K2 vs L1 bake-off on conditions (a)–(d) + K3 composite.
   (Nothing above can run without IDs; L1 is nearly free to build, so include it from day one as
   the secondary-index candidate even if K wins primary.)
2. **Cut bake-off on the winning substrate:** G1 vs G2 (pressure) and H2 (budgeted deliberation)
   vs fixed-64B baseline; H1 runs only as a cost-ceiling probe (its kill rule may fire on cost
   alone — that result is itself a finding).
3. **Structure on top of the winning cut:** I1 vs I2 (hierarchy), then J1 vs J2 (tilings) *only if*
   I's kill rules don't fire — tilings multiply whatever the cut layer costs, so they go last.
4. **Cross-cutting gates before any scale leg:** the determinism gate (same input + same logged
   state → byte-identical output, verified by diffing two reruns per leg) and the no-RNG scanner
   (uncertified variation could masquerade as cognitive chunking — the scanner must survive its red
   team before Arm C-style state-varying claims are trusted here too).

## Prereg sign-off checklist (Micah)

For each arm, the frozen items below must be signed before build. Anything unlisted is unbuilt.
- G: WARN=80%, CRITICAL=95% occupancy; hysteresis rule; merge-select key `(value ASC, slot ASC)`;
  thrash bar 5%; pinned-recall bar 1%; junk-fusion bar 10%.
- H: W (window bytes), C (max candidates), B (H2 budget), noticer list (frozen, proposal-only),
  evidence weights (4 integers), BAR, fallback rule, refusal semantics; reuse bars (+10 H1 / +5 H2);
  cost ceiling 10^4 ops/cut; BAR-sensitivity bar 25%.
- I: T_co=7 co-recalls; group size 2–8; max level 4; demote-after E episodes; P=3 (I2);
  attach-iff-exact-coverage; depth-value bar 5%; maintenance bar 20%; emergence bar 70%/50%.
- J: k=3 (J1) / K_max=5 (J2); α,β,γ arbitration weights; death-share 5%; subsumption 95%;
  adversarial-cut recall bars (≤3 vs ≥15 degradation); coverage-correctness bar (zero tolerance).
- K: hash choice per variant; table capacity (2× expected uniques); probe rule (linear from
  `digest[0] mod cap`); chain order (insertion); synthetic collision vectors; dedup bars
  (40%/25% predicted, 15% kill); chain-length bars (8 links / 2× latency; K2: length 4);
  disambiguation bar 5%.
- L: segment sizing (fixed SHIFT vs variable + binary search); revision-map lookup rule; epoch-bump
  definition with frozen integers (L2); eternity bar (zero tolerance); cost bar 3×; fragmentation
  bar 4 segments/recall.
- Comparison: conditions (a)–(d) frozen (including the 100-patch series and the permutation seed —
  deterministic, preregistered, *not* random); query set frozen; the five metrics; all kill rules
  above including the hybrid-promotion rule.

## Open tensions (documented, not resolved — experiments decide)

1. **Near-duplicates** defeat both K and L. A similarity-addressed arm is future work; it is not
   claimed here.
2. **L under adversarial input** is the weaker scheme (trusted position, spoofed bytes). The
   integrity red team should attack L1/L2 at positions holding high-value chunks.
3. **H's evidence weights** bottom out in preregistered integers — the regress stops by fiat, and
   the BAR-sensitivity kill rule is the honesty mechanism for that fiat.
4. **G1's junk fusion** vs **G2's cost**: the reactive/principled trade-off is the oldest one in
   the alphabet and is settled by the bake-off, not by taste.
