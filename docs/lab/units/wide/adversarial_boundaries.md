# EXPLORATORY — NOT EVIDENCE

**Adversarial boundary-case probe designs for the TNN representation program**
**Status:** EXPLORATORY RED-TEAM DESIGN. Non-binding. Nothing in this document counts as
program evidence, fires no kill bar, changes no frozen metric, and softens no frozen
criterion. It is a *design* for probe suites the frozen battery does not cover, written so
the execution tracks could implement them later via dated amendment (Micah's re-approval
required per prereg §0 RULE-9).
**Date:** 2026-09-21. **Author:** wide-exploration worker (adversarial track).
**Parent refs:** `../PREREG_FREEZE.md` (frozen), `../ALPHABET_*.md` (53-arm catalog),
`../ARCHAEOLOGY_R31.md` (R31 mechanism), `../RISKS.md` (R1–R10), `../METRICS.md`.

## 0. What this is and is not

- **Is:** 8 adversarial probe families (17 sub-probes) with exact deterministic
  constructions, named target arms, predicted failure modes, and falsifiable predictions
  of the form "arm X will do Y on input Z". Plus a pure-Zag probe-harness design
  (code sketches; full builds not required at this stage).
- **Is not:** evidence. A probe *outcome*, however dramatic, is a diagnostic signal. It
  does not fire kill criteria, does not enter any scorecard, and does not reinterpret
  frozen bars. Where a probe design exposes a tension with a frozen assumption, the
  tension is recorded in §9 as an **amendment PROPOSAL** — a request for Micah's ruling,
  not a change.
- **Frozen items referenced, never modified:** PREREG_FREEZE §0 RULE-1..9, §3 kill
  criteria, §6 M1–M9, §8 program kill bars, R-2 giant-span bar, A-9/A-12/A-24/A-32/M-48..50
  parameter sign-off items. Predictions below are conditioned on the *proposed* values in
  those items; each probe spec records the assumed values so a sign-off change re-grounds
  the prediction mechanically.

## 1. Probe conventions (bind all families)

1. **Zero randomness.** Every stream is a closed-form function of the byte index
   (arithmetic progressions, fixed tables, modular maps with frozen constants). No PRNG
   state, no seeds, no sampling. Where the frozen battery uses a "deterministic
   permutation seed", probes use the identity order or bit-reversal — stated per probe.
2. **Falsifiable prediction format.** Each sub-probe states: input Z (exact), arm X,
   predicted observable Y (counts, cut offsets, table sizes — all integers), and the
   fork: what it means if Y holds vs fails. A failed prediction kills the *probe's
   theory*, not the arm.
3. **Diagnostic, not evidentiary.** Probe runs use fresh arm instances and never share
   state with battery runs. Outcomes are reported as "probe signal", never as metric
   values.
4. **Measurement, not wall-clock.** Latency claims use deterministic op counts
   (table probes, byte compares, ledger entries), never wall-clock (informational only
   per M-56).
5. **Byte-identical reruns.** Every probe stream + recall script must itself satisfy the
   M8 shape: same input + same logged state → byte-identical output, or the *probe* is
   malformed (not the arm).
6. **Size discipline.** No probe stream exceeds 2^25 bytes (toolchain wall); most are far
   smaller. Generators assert this.

---

## Family PATH — Pathological byte streams

### PATH-1 · NULL-ZERO — the stream with no information
**Construction.** `Z[i] = 0x00` for `i` in `[0, 2^20)`. 1,048,576 bytes. No structure at all.
**Targets & predicted failure modes.**
- **D:** every candidate span (lengths 2..64) has `contdiv = 1` (continuation is always
  `0x00`) → the eliminative bar (`contdiv ≥ 2`) eliminates the entire candidate space.
  **Prediction:** D proposes 0 chunks and commits 0 chunks; a fixed recall script (1,000
  closed-form 64-byte span queries) scores 0% hits — D has no vocabulary and therefore no
  recall. Fork: if D commits *any* chunk, the `contdiv ≥ 2` bar is not implemented as
  specified → implementation bug, flag to the execution track.
- **F-S:** the order-2 predictor reaches perfect confidence (`P(0x00|0x00,0x00) = 1`) and
  never misses → **Prediction:** exactly 0 cuts.
- **F-B:** `contdiv = 1 < BR_BAR = 3` everywhere → **Prediction:** exactly 0 cuts.
- **R31-native (predictive-surprise):** prediction error is ~0 at every position; the
  82nd-percentile cut rule operates on a constant distribution.
  **Prediction:** cut count ∈ {0, N} only (0 = percentile-of-constant yields no
  boundary; N = degenerate tie-break cuts everywhere). *Any other count proves the
  percentile tie-break is unspecified* → spec-forcing probe: the execution track must
  freeze the tie-break before the redo can claim M8.
- **S:** atoms are recallable from t=0; joint-recall counters on adjacent atom pairs grow
  monotonically under the recall script; there is never a divergence signal
  (`I_a = I_b = 0`). **Prediction:** S fuses monotonically and never splits — converging
  to one chunk ID covering the full 2^20 stream. S cannot represent "nothing to learn
  here"; its crystallization machinery has no abstain path (contrast R31's
  support-gap `-1` abstain).

### PATH-2 · SINGLE-BYTE — the stream with exactly one symbol
**Construction.** `Z[i] = 0x41` for `i` in `[0, 2^20)`.
**Targets.** Same D/F predictions as PATH-1 (contdiv = 1 everywhere → 0 commits, 0 cuts).
The new target is **K1/K2 + the frozen battery**:
- **K1:** the probe presents all 64 span lengths × their occurrences through the add
  path. **Prediction:** exactly 64 live records; payload savings vs sequential IDs
  → ~100% trivially; M7-style dedup ratio saturates at its maximum on degenerate input.
  This is a **metric-gaming demonstration**: M-32's `dedup ≥ 0.4` bar is satisfiable by a
  single repeated byte. → Amendment proposal **P3** (§9): the dedup bar needs a
  non-degenerate-input qualifier.

### PATH-3 · NESTED — `(ab)^n` inside `(ab cd)^m`: the nesting ladder
**Construction.** `n = 32`: A-run = `(ab)^32` (64 bytes), C-run = `(cd)^32` (64 bytes);
block = A-run + C-run (128 bytes); stream = block^8192 (1,048,576 bytes). Exact,
closed-form: `Z[i] = "abcd"[i mod 4]` — note the stream is *also* `(abcd)^262144`; the
nesting is in the repetition structure the arms must discover.
**Targets.**
- **D:** spans `(ab)^k`, `k = 1..32`: `rep ≈ 8192 ≥ REP_BAR`, continuation ∈ {`a`,`c`}
  → `contdiv = 2 ≥ 2` → all pass the eliminative bar. Odd-phase spans `(ba)^k`:
  continuation ∈ {`a`,`c`} → also pass. Same for `(cd)^k`, `(dc)^k`.
  **Prediction:** D commits ≥ 100 chunks, all nested prefixes of the two 64-byte runs
  (both phases), max depth 32. The commit gate's reuse forecast is the only filter in
  the spec — the probe measures whether it prunes the ladder or waves it through.
  Fork: < 20 commits → the forecast or the gate is doing un-specified work → the
  execution track must write down what.
- **R31-native:** compression gain `(n-1)*seen-(n+3)` is maximized at the longest span:
  gain(64) = 63·8192 − 67 = 516,029; utility ≈ 267 vs ≈ 34.5 for a length-8 subspan
  (purity = 1.0 both — recall succeeds byte-exactly). **Prediction:** the redo recruits
  the length-64 `(ab)^32` span (top utility); greedy longest-match covers the stream in
  16,384 sixty-four-byte chunks; a probe recalling the 2-byte span `ab` *as a unit*
  returns 32 literal fallbacks (negative IDs), never a chunk — unit-recall fails while
  byte-recall passes. Under the R-2 cap (`L_max ≤ 8`) the same probe detects cap
  enforcement: any committed span with `len > 8` = R-2 violation flagged.

### PATH-4a · STARVE — candidate-table starvation by high-count junk (D)
**Construction.** Junk block `J` = 127 × `0x58` + `0x59` (128 bytes; every internal span
has `contdiv = 1` — uncommittable by D's eliminative bar, but every span has huge
`rep`). Stream = `J^10000` (1,280,000 bytes) followed by the frozen 2 MiB Shakespeare
head (`corpus[0, 2097152)`). Deterministic.
**Target — D's 4096-slot candidate table** (frozen eviction: lowest `(count, seq)`,
insert on second repeat). Junk spans sit at count ≈ 10,000 — never the eviction
minimum. Shakespeare spans (counts in the tens, spread over 2 MB) churn among the
remaining slots, evicting each other before reaching `REP_BAR` (counts reset on
eviction per the spec as written).
**Prediction:** D's Shakespeare-derived commits ≤ 20% (by count) of the commits D makes
on the same 2 MiB Shakespeare slice *without* the junk prefix; ≥ 80% of D's total
commits are junk-block substrings (committed only if a continuation plant exists —
see PATH-4b; in 4a the junk is uncommittable, so the sharper form of the prediction is
*near-total vocabulary collapse*: total commits ≤ 15% of the unpoisoned baseline).
Fork: if Shakespeare commits hold at ≥ 80% of baseline, candidate counts must be
surviving eviction somewhere — the spec then owes the execution track a persistence
rule it does not currently contain (spec-forcing either way).

### PATH-4b · POISONED WELL — the composed nasty (D) ★
**Construction.** `J' = 63 × 0x58 + 0x59` (64 bytes) × 20,000 (1,280,000 bytes) +
the same 2 MiB Shakespeare head. The single-byte change from PATH-4a is load-bearing:
span `X^k` (`k ≤ 62`) inside `J'` has continuations {`0x58`, `0x59`} → `contdiv = 2` —
the junk now *passes* the eliminative bar.
**Target — D.** Table starvation (PATH-4a mechanism) keeps Shakespeare spans out;
planted-variety continuation lets junk spans through all three bars
(`rep ≥ REP_BAR`, `len ≥ 3`, `contdiv ≥ 2`).
**Prediction:** ≥ 90% of D's committed chunk *types* are substrings of `J'`
(the full ladder `X`, `XX`, … up to length 62, plus cross-boundary `YX…X` spans);
Shakespeare-derived commits ≤ 10% of the unpoisoned baseline. D's verification probe
(byte-exact recall of junk ✓) and reuse forecast (junk recurs ✓) both pass — the arm
commits the attacker's vocabulary with full deliberative confidence. *D does not fail
to learn; it learns exactly the wrong thing, and the ledger certifies it.*
This is the single nastiest probe in the suite (§8).

---

## Family GSPAN — Giant-span traps (the barred exploit, relocated)

Background: the R31 tournament winner won partly via giant spans (mean len 32.3); the
prereg explicitly bars the exploit (R-2: `L_max` cap, proposed ≤ 8; compression term
capped so grounding dominates). These probes ask: *can it still trigger — and if the
cap holds, where does the bias go?*

### GSPAN-1 · BOILERPLATE — a true 60-byte unit, recurring verbatim
**Construction.** Frozen table `T[i] = 33 + ((i·37 + 11) mod 94)` for `i` in `[0,256)`
(printable, aperiodic, closed-form). `B = T[0..60]` (60 bytes, asserted by the
generator). Fillers `F_i = T[64 + ((i·13) mod 128) .. +40]` (40 bytes each, varying
with `i`). Stream = `(B + F_i)^60` (6,000 bytes). `B` is a genuine recurring unit with
purity 1.0 under the R-1 operationalization (recall succeeds; discrimination consistent).
**Targets.**
- **R31-native:** utility(B) ≈ 267 dominates every subspan (≈ 34.5 at len 8).
  **Prediction (fork):** (a) cap *enforced*: 0 committed spans with `len > 8`; each `B`
  occurrence is covered by ≥ 7 chunks; measured mean committed length saturates at the
  cap (8.0 ± 0.5) vs 3.2 ± 1.0 on the Shakespeare control — **the compression bias is
  not removed by capping, it relocates to the cap boundary**; (b) cap *not* enforced:
  ≥ 1 committed span with `len > 8` → R-2 violation flagged, implementation bug.
- **D:** internal subspans of `B` occur only inside `B` → `contdiv = 1` → eliminated as
  "mere prefixes" — but they are *infixes of a true unit*, and the bar cannot tell the
  difference. Spans touching `B`'s right edge (suffixes) see varying filler bytes →
  `contdiv ≥ 2` → pass; `B` itself sees varying filler starts → passes.
  **Prediction:** D commits exactly the ladder `B` + its 57 proper suffixes of length
  3..59 (58 chunks), and zero internal subspans. The eliminative bar misfires
  systematically on infixes — falsifiable to the chunk.
- **F-S / F-B / S:** no `L_max` exists in their frozen params.
  **Prediction:** F-S cuts only at filler boundaries (the `B` interior is perfectly
  predictable after the first occurrence) → mean chunk length ≈ 100 bytes, unbounded by
  any cap → the exploit is *unbarred* for the surprise arms. → Amendment proposal
  **P4** (§9): scope R-2 to the R31 line explicitly, or extend the cap to all cut-signal
  arms.

---

## Family BAMB — Boundary ambiguity storms (two tilings, equally good)

### BAMB-1 · PHASE-DUPLICATE — even vs odd tiling, statistically identical
**Construction.** A-block = `(ab)^32` (64 B), C-block = `(cd)^32` (64 B);
separators `s1, s2 ∈ {x, y}` cycling over the 4 combos `(x,x),(x,y),(y,x),(y,y)` across
macros. Macro = A-block + s1 + C-block + s2 (130 bytes). Stream = 4096 macros
(532,480 bytes). Every span `(ab)^k` has continuation ∈ {`a`, `x`, `y`} → `contdiv = 3`;
every odd-phase span `(ba)^k` likewise → the two tilings are statistically
indistinguishable to any count/continuation statistic.
**Targets.**
- **D:** **Prediction:** vocabulary contains `(ab)^k` for `k = 1..32` AND `(ba)^k` for
  `k = 1..31` (≥ 60 phase-duplicate chunks) with identical `(rep, contdiv)` profiles;
  a fixed 1,000-query recall script over `abab` occurrences resolves phase-consistently
  (≥ 95% one phase — deterministic) but the winning phase is order-contingent:
  **rerunning the probe with the separator cycle rotated (`(y,x)` first) flips the
  winning phase.** The "cognitive act" of cutting is a primacy artifact; M8 still holds
  (both runs byte-identical) — determinism is not the same as content-determination.
- **S:** recall script queries even-phase spans only (first leg), then odd-phase spans
  only (second leg). **Prediction:** both tilings crystallize (merges fire in both
  legs); divergence `δ` never reaches `σ_split` (both keep getting joint recalls) →
  nothing ever splits; mean reuse per committed chunk ≤ 0.6× S's reuse on the
  unambiguous PATH-3 control — the duplicate tilings split the reuse the arm exists to
  concentrate. (S's kill criterion (ii) is about merge-then-split churn; this probe
  shows the *other* failure: merge-then-never-split duplication.)
- **J1 (informational contrast):** J1 is *designed* to hold competing tilings; BAMB-1 is
  its home turf. **Prediction:** J1's arbitration cost per recall ≥ 2× D's (two live
  tilings scored per query) — the probe prices the no-canonical-cut philosophy.

---

## Family IDCOL — ID collision & masquerade (content-addressed arms)

### IDCOL-1 · LOW-32 MASQUERADE — distinct spans, same FNV-1a low 32 bits (K2)
**Construction (closed-form, no search randomness).** 200,000 spans:
`span_i = "K2PROBE:" || LE32(i) || "." || "z"×7` (20 bytes, pairwise distinct).
Compute FNV-1a-64 in the harness (15-line reference). Birthday expectation:
C(200000,2)/2^32 ≈ 4.7 pairs share low 32 bits — enumerate all pairs deterministically
(i < j order), keep the actual colliding pairs found (expect 3–7; the probe asserts
≥ 1 found, else the corpus size doubles by fixed rule — still deterministic).
Feed all 200,000 spans through K2's add path.
**Target — K2's "honest, counted collisions" path.**
**Prediction:** 0 `DEDUP_HIT`s on the colliding pairs (byte-compare must reject every
one); 200,000 live records; max probe-chain length recorded. **Any `DEDUP_HIT` on a
colliding pair = false merge = R5 silent-corruption FAIL of the implementation** —
the probe is built to catch exactly the plausible shortcut of comparing truncated
digests. (Full 64-bit FNV-1a collisions need ~2^32 work; the probe does not attempt
them — it attacks the *comparison discipline*, which is where implementations
actually break.)

### IDCOL-2 · FORCED-ALIAS — exercising K1's chain path at scale
**Construction.** 100 chosen distinct span pairs `(S_i, T_i)` (`S_i ≠ T_i`, 32 bytes
each, closed-form from the frozen table `T`). A harness test-seam forces digest
equality for these pairs only (this is what the catalog's A-24 "synthetic collision
vectors" must mean — real SHA-256 collisions are computationally out of scope).
**Target — K1's insertion-order chain + byte-compare confirmation.**
**Prediction:** 200 live records; 10,000 interleaved recalls (closed-form order)
return byte-exact spans with 0 wrong-byte returns; chain length exactly 2 per slot.
Any wrong return = R5 FAIL. → Amendment proposal **P2** (§9): A-24's vectors should be
*defined* as forced-injection (IDCOL-2) + birthday-bounded prefix collisions
(IDCOL-3); "synthetic" must not be read as "real".

### IDCOL-3 · PREFIX-CLUSTERING — 40-bit SHA-256 prefix collisions (K1)
**Construction.** 2,097,152 spans: `span_i = "K1P:" || LE32(i) || "#" || "q"×11`
(20 bytes). SHA-256 via the native import (`R33_NATIVE_SHA256_V2.zag`). Expected pairs
sharing low 40 bits: C(2^21,2)/2^40 ≈ 2. Deterministic enumeration.
**Target — K1's probe discipline** (linear probe from `digest[0] mod capacity`).
**Prediction:** max probe-chain length ≤ 4 on this input; the table sizing rule
(2× expected uniques) absorbs prefix clustering. If max chain > 4, K1's table
inherits K2's chain-bar shape → table-capacity amendment proposal. Honest statement:
a *full-digest* masquerade against K1 is infeasible by design — that infeasibility *is*
K1's security assumption, and this probe documents its boundary rather than testing it.

---

## Family SSPOOF — Surprise spoofing (cuts at attacker-chosen points)

### SSPOOF-1 · MARKOV SPOOF — confident predictor, planted misses (F-S, R31)
**Construction.** `("abc"^200 + "abX")^40` with `X` cycling `w,x,y,z` (fixed order);
24,080 bytes. The 200-repetition training run drives the order-2 predictor to
`P(c|ab) ≈ 1` with count ≫ `CONF_BAR`; each `abX` is a confident miss at a
attacker-chosen offset (offsets 602, 1204, …, 24080), spaced 602 ≥ `MIN_GAP`
(record the signed A-12 values in the spec).
**Targets.**
- **F-S:** **Prediction:** exactly 40 cuts, each within ±W of a spoof offset, 0 cuts
  elsewhere. The inter-cut chunks are 602-byte `abc…ab` runs — giant spans with no
  applicable cap (GSPAN fork (b) applies: the exploit is unbarred for F-S).
  Fork: any cut > W from a spoof site = signal leak (predictor cutting on its own);
  any spoof site with no cut within ±W = missed forced cut (confidence model wrong).
- **R31-native:** the 40 errors sit at the 99.8th percentile of prediction error →
  cuts at all 40 sites; inter-spoof runs covered per the GSPAN-1 cap fork:
  **Prediction:** with `L_max ≤ 8` enforced, boundary *recall* = 40/40 sites hit
  (within ±8) but boundary *precision* ≈ 40/(40 + ~3000) ≈ 1.3% — the cap converts the
  giant-span exploit into a precision collapse. Report precision, not just recall.

### SSPOOF-2 · CONTDIV PHASE TRANSITION — three bytes that detonate F-B
**Construction.** `("ab"^500 + "c")^200` (200,200 bytes) with planted variants at macro
indices 50, 100, 150: `("ab"^500 + "X")`, `("ab"^500 + "Y")`, `("ab"^500 + "Z")`.
**Target — F-B** (cut where a repeated span's `contdiv ≥ BR_BAR = 3`; `contdiv` is a
*global* accumulator). Before plant 3, `contdiv("ab") = 2` (`a`,`c`) → no cuts at
`ab` sites. The third distinct continuation flips the global counter to 5 ≥ 3 —
permanently, for all past and future occurrences.
**Prediction:** cut count in `[0, plant3_offset)` ≤ 5; cut count after `plant3_offset`
≥ 0.4 × remaining `ab` occurrences (≥ 30,000 cuts); the transition offset equals the
plant-3 offset ± 64. **Three attacker bytes cause a 10,000× cut-density detonation** —
F-B's branching signal is plant-fragile because global accumulation has no notion of
*rate*: a continuation seen 3 times in 200,000 bytes counts the same as one seen
3,000 times. **Contrast prediction for D on the identical stream:** D's bar is
`contdiv ≥ 2`, already satisfied natively (`a`,`c`) → D commits the `(ab)^k` ladder
on the *unplanted* stream too → D cannot distinguish planted from clean by vocabulary;
F-B distinguishes them catastrophically. Two failure modes, one stream: F-B is
plant-fragile, D is plant-blind. → Amendment proposal **P6** (§9): rate-normalized or
per-window `contdiv` as a test-both leg (RULE-2), not a change.

---

## Family CHURN — Revision storms vs ID stability (catalog risk R3)

All edit scripts are closed-form (no RNG): positions from `pos_i = (i·2654435761) mod N`
(Knuth multiplicative constant, fixed), op types cycling deterministically.

### CHURN-1 · EDIT STORM — 10,000 edits on 100 KB of sqlite3.c (D, ledger)
**Construction.** Fixed slice `sqlite3.c[0, 102400)`. 10,000 edits: `pos_i` as above
(`N` = current length, recomputed deterministically per edit — the script is a pure
function of `i` and the evolving length, still closed-form); `op = i mod 3`
(0 = insert 1 byte `0x41 + (i mod 26)`; 1 = delete 1 byte; 2 = replace with
`0x61 + (i mod 26)`).
**Targets.**
- **D:** **Prediction:** tombstone/live ID ratio > 2 (the R3 cheap-experiment bar,
  measured diagnostically); ghost IDs (span matching no live content) = 0 — any ghost
  is an R5 FAIL, not a data point; ≥ 1% of 1,000 fixed pre-storm recall probes traverse
  ≥ 3 tombstone hops ("stable ID" degrades to "stable lineage" under churn).
- **Ledger (R4):** count `CUT_SPLIT`/`CUT_MERGE`/`CUT_KILL`/`CHUNK_REUSE` per edit →
  ledger-bytes per source-byte vs M-25's `≤ 10 entries/KB` (diagnostic). **Prediction:**
  the storm exceeds 10/KB by ≥ 5× → amendment proposal **P5** (§9): scope M-25 to
  quiescent streams; churned streams need their own ledger-economics bar.

### CHURN-2 · CHAIN STRETCH — 10,000 single-byte edits, one span (K1)
**Construction.** One 64-byte span; 10,000 replacements: `pos = i mod 64`,
`byte = i mod 256`. Every edit re-IDs the span → `OP_REVISE_LINK` chain length 10,000.
**Target — K1's revision-link chains** (catalog kill shape: chain > 8 AND latency > 2×).
**Prediction:** let E* = smallest edit count with recall op-count ≥ 2× baseline;
E* ≤ 12. K1 without chain compaction has essentially no long-revision lifetime — the
catalog's own churn-swamp conjunction is reached almost immediately. The probe reports
the full latency-vs-edits curve (op counts), which the frozen battery never measures.

### CHURN-3 · SINGLE-INSERT CATASTROPHE — L1's predicted cause of death
**Construction.** 1 MiB stream; L1 position IDs over 1 KiB segments (1024 segments).
Insert 1 byte at offset 0.
**Target — L1** ("identity is WHERE"; catalog: *any* revision batch changing an
existing position ID kills it outright).
**Prediction:** re-keyed segments = 1023 (all downstream) → per-edit cost Θ(corpus),
not O(1); moreover, any recall issued between the insert and re-key completion
returns bytes shifted by 1 — a **silent wrong-span window** (R5). The probe measures
the window width in ops. This is L1's death made mechanical: position identity cannot
survive insertion, and the failure is silent unless re-keying is atomic.

### CHURN-4 · MERGE COLLISION — counter IDs across two stores (M)
**Construction.** Two stores A, B each ingest the same 1,000-chunk closed-form script
independently (counter IDs 0..999 in both), then merge.
**Target — M's cross-store identity** (catalog kill shape: ≥ 1 dangling/misdirected
pointer on remap in the two-TNN merge trial).
**Prediction:** naive merge → 1,000 ID collisions; after remap, references still
resolving to pre-remap IDs = 1,000 unless the remap rewrites *every* referencing entry
atomically. The probe counts post-merge dangling references as a function of remap
strategy (no remap / lazy remap / atomic remap) — three deterministic legs.

### CHURN-5 · LINEAGE AVALANCHE — Y3 under sustained single-span revision
**Construction.** Same 10,000-edit script as CHURN-2, on a Y3-versioned chunk.
**Target — Y3** (catalog kill shape: mean lineage depth > 50).
**Prediction:** lineage depth = 10,000 = edit count (no compaction exists in the arm);
10,000 tombstone records for one logical unit; recall op-count ≥ 10,000 hops (linear).
Y3's "controlled fragmentation" is uncontrolled under sustained revision of one span —
the version chain *is* the fragmentation R3 warns about, just labeled.

---

## Family JSPAM — Judgment spam (arm N)

### JSPAM-1 · SIGN-FLAP — alternating evidence forces the flap-or-fossilize dilemma (N)
**Construction.** Fixed 32-byte chunk C. 200 episodes: blocks of 10 episodes alternate
10 teacher-confirm events (+1 each, cited) and 10 contradiction events (−2 each,
cited); repeat 10×. All evidence cited in ledger form per N's ingress rule.
**Target — N's re-judgment path** (kill shape: > 10% of chunks flip sign > 2× per
100-episode window).
**Prediction:** judgment sign flips ≥ 8× over the 200 episodes (≥ 4 per 100-episode
window — the kill-bar *shape*, measured diagnostically) — **or** the arm stops
re-judging, in which case a final 50-confirm run leaves the judgment negative:
staleness FAIL. The probe forces N's dilemma into the open: *flap or fossilize*.
There is no third option in the arm as specified; the probe asks the execution track
to name which one N chooses (damping rule? flap budget? — currently unspecified).

### JSPAM-2 · SATURATION PIN — 10,000 confirms, then one contradiction (N)
**Construction.** Chunk C; 10,000 confirm events (+1 each, i64 saturating per A-32) →
judgment = i64::MAX. Then 1 contradiction event (−1000, cited).
**Target — N's saturating overflow + W4 soft-freeze hazard.**
**Prediction:** judgment after the contradiction = i64::MAX − 1000 — recall rank
unchanged, the contradiction absorbed without effect → **de-facto unrevisable ranking
= force-pin-by-saturation**, reachable with pure confirming evidence: no attacker, no
trainer, no malice. N's W4 hazard ("deeply negative judgments suppress chunks") has a
mirror image the catalog does not name: deeply *positive* saturation immunizes chunks
against contradiction. Side measurement: 10,001 `JUDGE_SET` entries for one chunk →
ledger cost per chunk under evidence flood (M-25 diagnostic).

---

## Family XDOM — Domain jump without a marker (catalog risk R7)

### XDOM-1 · PROSE→CODE JUMP — the poisoning mechanism, naturalistic
**Construction.** 5 MiB Shakespeare head + 5 MiB sqlite3.c head, concatenated, no
marker. Fixed recall scripts per half (closed-form offsets). Controls: prose-only and
code-only runs of the same arms.
**Targets.**
- **D:** the candidate table after 5 MB of prose is dominated by prose-span counts
  (the PATH-4a mechanism, no attacker needed). **Prediction:** commits in the code
  half's first 1 MB ≤ 15% of the commits the code-only control makes in its first
  1 MB — D's code vocabulary starves on arrival; recovery (commits/MB within 20% of
  control) takes > 2 MB of code. Frequency learned in one domain is a tax on the next.
- **F-S:** the prose-trained predictor meets code. **Prediction:** cut density in the
  first 64 KB of code ≥ 5× the prose density (surprise spike → cut storm), then slow
  re-convergence: density within 2× of the code-control density only after > 512 KB —
  the predictor has no deliberate reset; prose counts must be outvoted byte by byte.
- **R31-native:** same shape via the 82nd-percentile mechanism; report both arms'
  re-convergence distances. R7's "train on prose, test on code" becomes a *temporal*
  probe: the arm carries its past as a liability.

---

## 8. The nastiest probe, and why

**PATH-4b POISONED WELL** is the nastiest single probe in this suite:

1. **It inverts the flagship's claim.** D does not merely underperform — it learns the
   *attacker's* vocabulary (the `X^k` ladder, 62 deep) while starving on the real text
   (≤ 10% of baseline commits). The ledger — the program's integrity backbone — certifies
   every junk commit: byte-exact recall ✓, reuse forecast ✓, `CUT_COMMIT` with
   just-codes. A downstream memory organ pinning and promoting these chunks is doing its
   job correctly on poisoned foundations.
2. **It exploits frozen mechanics.** The attack needs only two frozen facts: the
   `(count, seq)` eviction comparator (A-9 — counts are trusted absolutely, with no
   provenance on *why* a count is high) and the `contdiv ≥ 2` bar (a single planted
   continuation variety flips a span from "eliminated prefix" to "word-like unit").
   Neither can be tuned without a dated amendment — the vulnerability is structural,
   not parametric.
3. **It is cheap and deterministic.** 1.28 MB of junk + 2 MB of fixed corpus head;
   closed-form; byte-identical reruns; pure-Zag generatable in milliseconds. No crypto,
   no search, no attacker model beyond "the stream starts with repetitive junk" — which
   XDOM-1 shows happens *naturally* at domain boundaries.
4. **It composes.** PATH-4b = PATH-4a (table starvation) + SSPOOF-2's mechanism
   (continuation planting) applied to D's eliminative bar. The families are not
   independent attacks; they are one attack surface viewed from four sides
   (frequency trust, continuation trust, order trust, cap trust).

Runner-up: **SSPOOF-2** — three planted bytes causing a 10,000× cut-density detonation
in F-B is the cheapest break per attacker byte in the suite, and it exposes that
*global* accumulation (no rate, no window, no forgetting) is the shared flaw in D's
`contdiv`, F-B's branching signal, and S's `J` counters alike.

## Which leading arm is most expected to break, and why

**Arm D (self-cut + stable ID) — the flagship.** Three converging reasons:

1. **Its learning signal trusts input statistics absolutely.** Count-based table
   residency (PATH-4a/4b, XDOM-1), global continuation diversity (SSPOOF-2, GSPAN-1's
   infix misfire), and arrival-order tie-breaks (BAMB-1's phase flip) are all *functions
   of the stream as presented* — and the stream as presented is attacker-controllable
   (or domain-shifted, same mathematics). D has deliberation *over* its statistics but
   no deliberation *about* them: nothing in the five-organ pipeline asks "is this count
   high because the world is like this, or because the input was arranged?"
2. **Its failure mode is silent wrong knowledge, the worst kind.** Per R3/R5: a
   poisoned vocabulary is worse than no vocabulary, because every downstream organ
   (pin, promote, recall, the debate-trial spectator) treats committed chunks as
   knowledge. K fails loud (chain limits), S fails visibly (churn), N fails
   measurably (flap counts) — D fails *successfully*, with a clean ledger.
3. **Its defenses are frozen.** The eviction comparator, `REP_BAR`, `contdiv ≥ 2`,
   `LMAX = 64` are sign-off items; D cannot adapt its statistical trust without an
   amendment. S was *built* to revise (split/dissolve are first-class); D's revision
   organ revises *cuts*, not the counting machinery that produced them.

Honest counterweight (this document is red-team, not a verdict): D is also the most
*instrumented* arm — every failure above is ledger-visible, which is exactly what makes
these probes writable as falsifiable predictions. An arm that cannot be probed this
precisely would be more dangerous, not less.

---

## 9. Amendment PROPOSALS (non-binding — Micah's ruling required for any)

None of these change anything. Each is a numbered request the execution tracks may
bring to Micah if a probe signal warrants it.

- **P1 — Scope the giant-span cap.** A-9 freezes D's `LMAX = 64`; R-2 proposes the
  R31-line cap `L_max ≤ 8`. GSPAN-1 will produce a > 8-byte commit under D's frozen
  params on boilerplate input — the two items contradict on the same input class.
  *Proposal:* unify the cap across cut-signal arms, or scope R-2 to the R31 redo line
  explicitly and write down why D is exempt.
- **P2 — Define A-24's "synthetic collision vectors".** Real SHA-256 collisions are
  computationally out of scope; "synthetic" must not be misread as "real".
  *Proposal:* define the vectors as IDCOL-2 (forced-injection, 100 pairs) +
  IDCOL-3 (birthday-bounded 40-bit prefix collisions, 2^21 spans). IDCOL-1 covers K2.
- **P3 — Qualify the dedup bar.** PATH-2 games M-32's `dedup ≥ 0.4` trivially
  (single-byte stream). *Proposal:* add a non-degenerate-input qualifier to M-32, or a
  companion "degenerate-input" reporting leg.
- **P4 — Extend or scope R-2.** SSPOOF-1 and GSPAN show the giant-span bias is
  unbarred for F-S/F-B/S (no `L_max` in their frozen params); capping relocates the
  bias to the cap boundary rather than removing it (GSPAN-1 fork (a)).
  *Proposal:* extend the cap to all cut-signal arms, or scope it explicitly with
  rationale; add cap-saturation (mean committed length vs cap) as a reported
  diagnostic.
- **P5 — Scope M-25 to quiescent streams.** CHURN-1 is predicted to exceed
  `≤ 10 audit entries/KB` by ≥ 5×. *Proposal:* M-25 governs quiescent learning;
  churned streams get their own ledger-economics bar (to be preregistered, not
  discovered).
- **P6 — Rate-normalize `contdiv`.** SSPOOF-2 shows three rare events permanently flip
  a global counter (F-B detonation; D's plant-blindness is the mirror image).
  *Proposal:* per-window or rate-normalized `contdiv` as a **test-both leg** per
  RULE-2 — global vs windowed, head-to-head — not a change.
- **P7 — Clarify S's threshold typing.** M-48 proposes `θ_merge = 0.15` under a rule
  stated as `J ≥ θ_merge` (count ≥ fraction does not typecheck).
  *Proposal:* sign-off note clarifying whether θ_merge is a count, a fraction of a
  window, or a rate — the probe specs need the semantics to be executable.

---

## 10. Pure-Zag probe-harness design (sketches, not a build)

Layout (under the unit's working dir; nothing committed until an amendment authorizes
a build): `probe/spec.zag`, `probe/streamgen.zag`, `probe/measure.zag`,
`probe/arm_shim.zag`, `probe/main.zag`.

**Design rules.** The harness contains *no AI decision logic* — every adversarial
choice is a frozen constant in the spec. Generators are closed-form arithmetic over
the byte index (no PRNG state). All iteration is in ID/offset order; addresses are
normalized out of captures (M-36 shape); no floats; no wall-clock in any scored
quantity (op counts only).

```zag
// probe/spec.zag — probes are selected by integer id, never parsed from text.
pub const FAM_PATH: u8 = 1; pub const FAM_GSPAN: u8 = 2; pub const FAM_BAMB: u8 = 3;
pub const FAM_IDCOL: u8 = 4; pub const FAM_SSPOOF: u8 = 5; pub const FAM_CHURN: u8 = 6;
pub const FAM_JSPAM: u8 = 7; pub const FAM_XDOM: u8 = 8;

pub struct ProbeSpec {
    fam: u8,        // family
    sub: u8,        // sub-probe within family
    stream_len: u32,// asserted <= 1<<25 by the generator
    p0: u32, p1: u32, p2: u32, p3: u32, // frozen numeric params (counts, offsets)
    assume: u32,    // bitmask of sign-off assumptions used (A-9, A-12, M-48..50...)
}

pub fn spec_path4b() -> ProbeSpec {
    // PATH-4b POISONED WELL: 20000 x 64B junk + 2MiB Shakespeare head.
    return ProbeSpec{ fam: FAM_PATH, sub: 4, stream_len: 1280000 + 2097152,
                      p0: 20000, p1: 64, p2: 2097152, p3: 0,
                      assume: ASSUME_A9 }; // eviction comparator, REP_BAR, LMAX...
}
```

```zag
// probe/streamgen.zag — closed-form generators. `out` is caller-owned, len asserted.
pub fn gen_zeros(out: []u8) void {           // PATH-1
    assert(out.len <= (1<<25));
    for (0..out.len) |i| { let o: []u8 = out; o[i] = 0x00; } // alias-before-index (AGENTS.md)
}
pub fn gen_poison_well(out: []u8) void {     // PATH-4b
    assert(out.len == 1280000 + 2097152);
    var i: u32 = 0;
    for (0..20000) |_rep| {
        for (0..63) |_k| { let o: []u8 = out; o[i] = 0x58; i += 1; } // 63 x 'X'
        { let o: []u8 = out; o[i] = 0x59; i += 1; }                  // 1 x 'Y'
    }
    corpus_copy(out, i, CORPUS_A_HEAD, 0, 2097152); // frozen corpus slice
}
pub fn gen_churn_script(n_edits: u32, len0: u32, ops: []u8, poss: []u32, bytes: []u8) void {
    // CHURN-1..5: pos_i = (i * 2654435761) mod len_i — closed form, no RNG.
    // ops[i] = i mod 3; bytes[i] fixed rotation. Pure function of i.
    var len: u32 = len0;
    for (0..n_edits) |i| {
        let p: []u32 = poss; let o: []u8 = ops; let b: []u8 = bytes;
        p[i] = (i *% 2654435761) % len; o[i] = i % 3; b[i] = 0x41 + (i % 26);
        if (o[i] == 0) { len += 1; } else if (o[i] == 1) { len -= 1; }
    }
}
```

```zag
// probe/measure.zag — fixed-size, integer-only measurement struct.
pub struct Meas {
    commits: u32,          // CUT_COMMIT count
    cuts_total: u32,       // cut offsets observed
    cut_first: u32, cut_last: u32,
    live_ids: u32, tomb_ids: u32, ghost_ids: u32,
    max_chain: u32,        // longest revision/probe chain walked
    recall_hit: u32, recall_miss: u32, recall_wrong_bytes: u32, // wrong_bytes>0 = R5 FAIL
    ledger_ops: u64,       // total 16-word entries
    op_count: u64,         // deterministic cost (table probes + byte compares)
    sign_flips: u32,       // JSPAM: judgment sign changes
}
pub fn recall_script(meas: *Meas, arm: *ArmShim, base: u32, stride: u32, n: u32, span: u32) void {
    // closed-form recall probes: offsets base + k*stride. Byte-compare every hit.
    for (0..n) |k| {
        let off: u32 = base + k * stride;
        let r: Recall = arm.recall(off, span);
        if (r.status == HIT) {
            meas.recall_hit += 1;
            if (!bytes_equal(r.bytes, expect_bytes(off, span))) { meas.recall_wrong_bytes += 1; }
        } else { meas.recall_miss += 1; }
    }
}
```

```zag
// probe/arm_shim.zag — the arm exposes three entry points; until arms are built,
// a SPEC-FAITHFUL STUB may stand in, marked STUB (calibration only, never evidence,
// per the testing standard: stubs never headline).
pub struct ArmShim { ingest: *const fn([]u8) void, recall: *const fn(u32,u32) Recall,
                     dump: *const fn(*Meas) void, is_stub: bool }
```

**Report format.** Fixed-format text + the metrics-v1 JSON schema fields the probe can
fill; a `probe` extension object for the new fields is a schema addition → needs
sign-off per M-55 (noted, not taken). Every report carries the `assume` bitmask so a
sign-off change re-grounds predictions mechanically.

**Cross-family ledger measurement (R4).** Every probe records `ledger_ops` and the
opcode histogram (256-entry `u64` array, fixed). CHURN-1 and JSPAM-2 are expected to
be the ledger-heaviest; the harness reports ledger-bytes per source-byte per probe —
the number R4's cheap experiment asks for, but on adversarial rather than quiescent
inputs.

## 11. Explicit non-coverage

- These probes do not re-test M1–M9, do not implement the frozen battery, and do not
  touch the teacher track (§4) or the R31 redo track (§2) except as *targets*
  (R31-native is probed; the redo's bars are not re-litigated).
- No probe outcome fires, weakens, or reinterprets a kill criterion. A probe that
  *would* trip a kill-bar shape is reported as "bar-shaped signal — amendment required
  to admit as evidence", never as a firing.
- Social/economic adversaries (malicious teachers, multi-TNN collusion) are out of
  scope — Z2/Y2 own that surface.
- Timing side-channels (M-2's side-channel → 0 rule) are out of scope for this suite.

## 12. Graduation path

A probe graduates from exploratory to battery-admissible only via dated amendment
(Micah's re-approval): the amendment names the probe id, the frozen metric it informs,
and whether it is admitted as (a) a diagnostic leg, (b) a new barred input class, or
(c) a kill-bar-shaping experiment. Until then, §9 proposals are the only upward path.

---
*End of exploratory design. All predictions are pre-implementation and unfalsified —
that is the point of writing them down first.*
