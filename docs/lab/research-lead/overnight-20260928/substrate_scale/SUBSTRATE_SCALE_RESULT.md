# Substrate Scale (S9): Result

## Verdict: SCALE-TESTED

All four frozen kill bars from PREREG_SUBSTRATE_SCALE.md pass.

## Frozen bars

- K1: S9 specified in prereg (committed alone before implementation;
  order verified below).
- K2: every K2-world frozen prediction holds exactly.
- K3: every K3-world frozen prediction holds exactly; wall time
  reported.
- K4: pure Zag (znc/shell/grep/git only, zero Python invocations),
  zero em/en-dash bytes, 3/3 byte-identical runs, exit 0, zero
  stderr bytes.

## What was built

`s9.zag` extends the shared substrate core (workspace layout, string
pool, latest-match query semantics unchanged) with the S9 mechanism:

- Per-slot u32 metadata: bit 31 pin, bits 16..30 last-hit tick,
  bits 0..15 saturating hit count. Metadata lives between the fact
  triples and the string pool; `max_fact` is now a live init
  parameter (default 256).
- Compaction: on a full store, keep only the last triple per (e,a)
  key. Semantics-preserving: the query path returns the latest match,
  so removed triples were unreachable.
- Scored eviction: if still full, evict the unpinned slot minimizing
  (use, tick); pinned slots are never victims; -2 if all pinned.
- New header stats: evict_count (72), compact_count (76),
  learn_ok (80), learn_dropped (84).

## Results (3/3 byte-identical, md5 9d9254db0c6fda04d1c022845d3df8e5)

K2 world (cap 256, 500 mixed learns):

- learn_ok=500, learn_dropped=0, compact=100, evict=144,
  factcount=256, conflicts=100. All match the frozen predictions.
- Important accuracy 150/150 (50 imp + 100 sup-new).
- Pinned survival 15/15 (10 imp + 5 junk).
- Victim order as predicted: junk{0..143} evicted (11/11 absence
  spot checks pass), junk{144..249} present (3/3, including pinned
  junk{249}).

Control (plain append-only store, same 500 learns):

- ok=256, dropped=244. Distinct live keys retained: 156
  (100 slots wasted on dead superseded triples).
- S9 comparison: 500/500 learns accepted vs 256/500; 256/256 live
  keys retained vs 156.

K3 world (cap 1024, 1200 learns):

- learn_ok=1200, learn_dropped=0, compact=0, evict=176,
  factcount=1024. All match the frozen predictions.
- Important accuracy 300/300. Victims bj{0..175} (6/6 absence
  checks), survivors bj{176}, bj{899} present.
- Wall time: 28.9 s real (13.3 s user) for the full program
  (K2 + control + K3), dominated by string-pool interning on
  thousands of queries. Engineering datum, not a threshold.

## Honest scope

- Eviction is score-driven, not learned: the (use, tick) policy and
  pin flag are researcher-authored. The claim is that the mechanism
  preserves what the learner marks important and discards the rest,
  not that the learner chose the policy.
- The string pool still grows monotonically (every learn and every
  query interns strings); S9 reclaims fact slots, not string bytes.
  String GC is the natural next gap.
- Compaction removes pinned-but-superseded triples (pin protects
  against eviction, not against being superseded), as specified.

## Commits (local, tnn-native-lab, owned path only)

- Prereg: 18f3d2a5e (committed alone before implementation)
- Implementation + result: s9.zag, SUBSTRATE_SCALE_RESULT.md,
  S9_RAW_1/2/3.txt, S9_ERR_1/2/3.txt (empty), build.err

## Files

- PREREG_SUBSTRATE_SCALE.md
- s9.zag
- SUBSTRATE_SCALE_RESULT.md
- S9_RAW_1.txt (runs 2/3 identical)

Builder label: SCALE-TESTED
