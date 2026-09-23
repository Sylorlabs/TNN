# HTD-1 DEBATE — Ledger / IO / Storage Economy (eff-ledger)

Phase: DEBATE only. No building. Hypotheses below are preregistration-ready:
each carries mechanism, falsifiable predictions, numeric kill bars (including
a REPLAY bar and a SAVINGS bar), a proxy task, and required head-to-heads.

Standing constraints for every hypothesis:
- Pure Zag. Zero randomness in any decision path.
- The byte-identical replay law: same input + same logged state → byte-identical
  output. Every proposal states exactly how replay reconstructs byte-identical
  state, and every proposal carries a REPLAY kill bar that fires on a single
  divergent byte.
- Deterministic ordering everywhere: episode counters and slot indices, never
  wall-clock time, never memory addresses, never hash-map iteration order.
- Audit entry layout (fixed, 16 words): op@0, slot@4, rc@8, b1..b5@12..28,
  a1..a5@32..48, stage@52, d1@56, d2@60.

Baseline for all comparisons: the current unoptimized ledger — every
deliberation event written and fsync'd individually, full entry detail forever,
verification by linear rescan. Reference cost anchor: the M8 battery uses
16MB ledgers × 10 runs.

---

## E-LG1 — Ledger-write batching (group commits per deliberation episode)

### Mechanism sketch
Today each ledgered event is one durable write. E-LG1 accumulates all entries
of one deliberation episode in an in-memory per-episode buffer (a contiguous
word array; entries appended in fixed field order, entry count in the header
word) and performs a single durable write at the episode close
(commit/refuse/rollback boundary).

Durability gap handling: the episode's input bundle (episode id + canonical
input record) is written FIRST as a small durable "episode-open" marker, then
the batch at close. If the process dies mid-episode, the open marker plus the
logged inputs allow deterministic re-execution of the episode, which — by the
no-randomness law — reproduces the lost batch byte-identically. Replay from a
surviving batch: episode-open + batch entries → the identical entry stream as
the unoptimized ledger.

What is stored: identical entry bytes as baseline, plus one open marker per
episode. What is skipped: N−1 durable write syscalls per episode of N entries.

What breaks if the hypothesis is wrong: any non-determinism in entry content
(wall-clock timestamps, addresses, unlogged inputs) makes a lost batch
irrecoverable — the REPLAY bar below catches exactly this. A second failure
mode: the open marker itself adds bytes, so pathological episodes with 1–2
entries could bloat rather than save; the SAVINGS bar guards it.

### Falsifiable predictions
1. Durable write syscalls drop by ≥60% on deliberation-heavy workloads while
   total bytes written stay within 110% of baseline (open markers are small).
2. Crash at any episode boundary followed by re-execution reproduces the batch
   byte-identically in ≥99% of episodes (the <1% allowance is for episodes whose
   inputs were not fully loggable — each such case must be individually
   documented, not silently absorbed).
3. Batching changes zero ledger bytes for surviving episodes: byte-compare of
   the batch-decoded entry stream vs the baseline entry stream is identical.

### Kill bars
- **REPLAY bar:** replay of N=500 episodes from the batched ledger (including
  10 kill-and-restart trials at episode boundaries 64/128/256/384/448 with
  re-execution from open markers) diverges by ≥1 byte from the unoptimized
  ledger replay → FAIL.
- **SAVINGS bar:** durable write syscalls saved ≥60% AND total bytes written
  ≤110% of baseline. If syscalls drop but bytes grow >110%, FAIL (batching
  must not buy fewer syscalls with fatter writes).

### Proxy task + metric
500-episode debate/revision curriculum over pg100.txt chunks (each episode =
deliberate over a chunk, commit or refuse). Count write()/fsync() syscalls,
measure total bytes, then replay-compare batched vs baseline ledgers
byte-for-byte.

### Head-to-heads required
- E-LG1 vs unoptimized baseline (same seed curriculum, same episodes).
- E-LG1 vs E-LG3: does batching compose with tiering, or does the open marker
  interfere with compaction boundaries?
- E-LG1 internal: episode-close batching vs fixed-count batching (every 64
  entries regardless of episode) — fixed-count may win on pathological
  long episodes; test both, no minimizing.

---

## E-LG2 — Checkpoint + delta (periodic full-state snapshots, deltas between)

### Mechanism sketch
Every K episodes, write a full state snapshot: deterministic serialization
with canonical field order, slots iterated in numeric order, all references
offset-relative (no pointers). Between checkpoints, entries are stored as
word-level XOR-deltas against the previous entry (first entry after a
checkpoint stored in full): for 16-word entries this is exactly reversible,
purely deterministic, and typically much smaller than full entries because
consecutive entries share op/slot/stage structure.

Replay = load nearest checkpoint at or before the target episode, apply deltas
forward. Worst-case replay cost is bounded by K episodes + one snapshot load,
vs O(total episodes) today. Snapshot cadence K is a preregistered parameter,
not tuned mid-run.

What is stored: snapshots (full state, canonical bytes) + delta-encoded entry
stream. What is skipped: redundancy between consecutive entries and the need
to replay from episode 0.

What breaks if the hypothesis is wrong: (a) snapshot serialization with
non-canonical order (e.g., hash-map iteration) → replay divergence, caught by
the REPLAY bar; (b) a delta decode bug → silent state corruption, caught only
by byte-compare against baseline — which is why the bar compares full final
state, not just "replay completed"; (c) snapshot write cost exceeding the
delta savings for small K — the SAVINGS bar amortizes snapshot cost
explicitly.

### Falsifiable predictions
1. Total ledger bytes ≤50% of baseline at K=64 over 1000 episodes, with
   snapshot bytes ≤20% of the E-LG2 total (amortization holds).
2. Replay-from-checkpoint at every tested K reproduces baseline final state
   byte-identically.
3. Kill-and-restart at episode boundaries 128/512/896 (non-checkpoint
   episodes) resumes from the prior checkpoint + deltas and converges to the
   continuous-run state byte-identically.

### Kill bars
- **REPLAY bar:** state after replaying N=1000 episodes from (checkpoints +
  deltas) diverges by ≥1 byte from unoptimized-ledger replay → FAIL. Includes
  the three kill-and-restart trials above.
- **SAVINGS bar:** total bytes (snapshots + deltas) ≤50% of baseline at
  K=64; snapshot share ≤20% of E-LG2 total. If deltas save bytes but snapshots
  eat the savings, FAIL.

### Proxy task + metric
1000-episode run over sqlite3.c chunks (deliberate: segment, label, commit).
Vary K ∈ {16, 64, 256}. Metrics: total bytes, snapshot byte share, replay
byte-compare vs baseline, restart-convergence byte-compare.

### Head-to-heads required
- E-LG2 vs unoptimized baseline.
- E-LG2 internal: K=16 vs 64 vs 256 (small K bounds replay cost but writes
  more snapshots; find the knee, don't assume 64).
- E-LG2 × E-LG1: do batching and deltas compose (batched durable writes of
  delta-encoded entries), or does batch framing defeat delta locality?

---

## E-LG3 — Audit-tiering (hot detail for recent episodes, compacted summaries for old)

### Mechanism sketch
Two tiers. Hot tier: the last H episodes in full entry detail (H preregistered,
e.g. 128). Cold tier: older episodes compacted into per-episode summary
records: (episode id, entry count, final-state hash, per-op-code counts, and
the net slot-write set). The compaction function is a pure, fixed, deterministic
function of an episode's entries. Crucially, the compaction decision itself is
deliberated and ledgered as an entry in the hot tier — compaction is audited,
not silent.

Honest statement of the law: E-LG3 deliberately splits the replay law in two.
State-replay (reconstruct exact final state) is preserved byte-identically:
replay = cold summaries' final states (hash-verified) + hot tier entries.
Stream-replay (reconstruct the exact entry stream of old episodes) is
intentionally NOT preserved for cold episodes — this is declared in the prereg,
not hidden. If any future verification needs cold entry detail, E-LG3 is the
wrong hypothesis; the FORENSIC bar below is the tripwire.

What is stored: full detail for H episodes + one summary record per older
episode + compaction-decision entries. What is skipped: per-entry detail of
cold episodes.

What breaks if the hypothesis is wrong: a forensic or provenance query needing
cold entry detail returns a wrong or incomplete answer — the FORENSIC bar
fires. Also: compaction summaries that are too lossy to verify (e.g., hash
collisions in final-state hashes — use the native SHA-256 substrate, and the
bar requires hash match AND state match on sampled re-derivations).

### Falsifiable predictions
1. Total bytes ≤40% of baseline at H=128 over 1000 episodes.
2. State-replay from the tiered ledger is byte-identical to baseline replay.
3. A fixed 20-query forensic battery (e.g., "all commits to slot S in episodes
   0..999", "every refusal with reason code R", "provenance chain of promoted
   memory M") returns identical answers on tiered vs baseline ledgers.

### Kill bars
- **REPLAY-STATE bar:** final state after replaying N=1000 episodes from the
  tiered ledger diverges by ≥1 byte from baseline → FAIL.
- **SAVINGS bar:** total bytes ≤40% of baseline at H=128 → else FAIL.
- **FORENSIC bar:** any of the 20 forensic queries returns a different answer
  on the tiered ledger than on the baseline → FAIL. This bar is non-negotiable:
  it is what keeps tiering honest about what it destroys.

### Proxy task + metric
1000-episode run over pg100.txt; H ∈ {64, 128, 256}. Metrics: total bytes,
state byte-compare, forensic battery pass/fail per query.

### Head-to-heads required
- E-LG3 vs unoptimized baseline.
- E-LG3 internal: H=64 vs 128 vs 256 (smaller H saves more but risks forensic
  loss; the FORENSIC bar decides, not intuition).
- E-LG3 × E-LG2: does tiering compose with delta compression of the hot tier
  (cold summaries + delta-encoded hot entries)?

---

## E-LG4 — Read-path indexes (kill the O(n²) rescan; indexes as derived data)

### Mechanism sketch
Build deterministic auxiliary indexes alongside the ledger; indexes are
DERIVED data, never the source of truth:
- (a) per-slot last-writer index: slot → (episode, entry offset) of latest
  write. This directly attacks the O(n²) free-slot scan measured at 10x.
- (b) per-episode index: episode → (entry count, byte offset of first entry).
- (c) op-code histogram index: op → count, maintained incrementally.

Index format: fixed-size arrays sorted by key, built in one deterministic pass.
Write-through discipline: index updates are part of the same durable write as
the entries they describe (composes with E-LG1's batch boundary). Trust rule:
any index entry can be challenged by re-derivation from the ledger; periodic
self-check entries record index-hash == ledger-derived-hash. If they ever
differ, the index is discarded and rebuilt — the ledger is never "corrected"
to match the index.

What is stored: the ledger bytes are UNCHANGED (indexes live in sidecar
files); verification reads go to indexes first. What is skipped: linear
rescans for slot lookups, episode seeks, and op histograms.

What breaks if the hypothesis is wrong: (a) an index used as truth instead of
the ledger → corruption hides; the STALENESS bar below injects appends and
demands index answers equal from-scratch scan answers. (b) index maintenance
cost exceeding the read savings — the bar caps it. (c) stale index after a
crash between entry write and index write — prevented by the shared durable
write boundary; the bar tests kill-and-restart explicitly.

### Falsifiable predictions
1. A fixed 20-query verification battery (slot lookups, episode seeks,
   forensic scans) runs in ≤25% of baseline elementary-op count (≥4x speedup).
2. Index build + maintenance costs ≤10% of total run time.
3. The ledger file bytes are identical with and without indexes enabled
   (indexes change zero ledger bytes).

### Kill bars
- **REPLAY bar (ledger-integrity form):** byte-compare of the ledger file with
  indexes enabled vs indexes disabled over N=500 episodes — any difference →
  FAIL. Indexes must be pure derivation.
- **SAVINGS bar (read-path form):** verification battery op count ≤25% of
  baseline AND index maintenance ≤10% of run time. If reads speed up but
  maintenance eats the budget, FAIL.
- **STALENESS bar:** 50 targeted appends interleaved with queries; every index
  answer must equal a from-scratch ledger scan answer. Any mismatch → FAIL.
  Plus 5 kill-and-restart trials: post-restart index must equal a fresh
  rebuild from the ledger, byte-identically.

### Proxy task + metric
The 10x-scale run where the O(n²) free-slot scan was measured. Metric:
elementary ops for the 20-query battery (scan vs indexed), index maintenance
op share, ledger byte-compare, staleness trials.

### Head-to-heads required
- E-LG4 vs unoptimized baseline (same queries, same episodes).
- E-LG4 × E-LG1: batching + indexes — does the shared batch boundary make
  index write-through cheaper than per-entry updates?
- Combination leg (if each survives its bars): E-LG1 + E-LG2 + E-LG4 vs
  baseline — do the savings compose or interfere (e.g., does delta encoding
  slow index maintenance past its 10% cap)?

---

## Considered but not proposed

Content-addressed dedup of repeated deliberation patterns (hash repeated entry
subsequences, store once, reference by hash): deferred, not rejected. It is
strictly weaker than E-LG2's word-level deltas for the entry stream (deltas
subsume repeated-pattern savings deterministically), and for the state side it
risks turning the ledger into a garbage-collected store — liveness of
referenced blocks becomes a new correctness burden. Revisit only if E-LG2's
SAVINGS bar fails while profiling shows repeated-pattern redundancy dominating.

---

## Steelman: the strongest objection to ledger economy

The ledger is the trust root — it is the thing that makes "TNN does not lie to
itself about what it did" a checkable claim rather than a slogan. Every
optimization of the trust root is a new place for corruption to hide: batching
delays durability so a crash can erase an episode's evidence; deltas add a
decode step whose bug corrupts silently; tiering deliberately destroys evidence
and lets the system grade its own homework when it deliberates the compaction;
indexes tempt every future builder to trust the derived over the primary. The
current ledger's only real security property is its dumb simplicity — there is
almost nothing to get wrong. Each clever mechanism here is a loan against
trust, and the kill bars are the collateral: that is why every hypothesis above
carries a REPLAY bar that fires on a single divergent byte and why E-LG3
carries a FORENSIC bar that treats destroyed evidence as failure unless the
prereg said so in advance. If any bar is ever "relaxed for practicality," the
objection wins outright — a cheaper ledger that can't prove what happened is
not an efficiency gain, it is the end of the auditability the whole program
rests on.
