# PREREG_WB3 — Selective audit at scale (written BEFORE any trial run, 2026-09-19)

Agent: Wave-3 investigator (whitebox-at-scale). Native Zag, this Linux VM only.

## Program-law amendments recorded (Micah, 2026-09-19 — effective immediately)

- **A1 — scaling allowed.** The ban was on scaling *toy mechanisms* (N×N
  score tables), never on scaling itself. This prereg adds an explicit
  **scale dimension**: the mechanism must be designed to survive 10x/100x
  (more slots, larger ledger, longer op sequences). The trial runs the same
  protocol at 1x (64 slots) and 10x (640 slots) and asserts per-op ledger
  cost is constant across scales (linearity). The 100x run is named as the
  explicit next test (WB3-SCALE-100x); it is NOT claimed here.
- **A2 — no randomness in the AI, stronger than before.** No RNG anywhere
  in the *system's* decision paths: no random exploration, no random
  tie-breaks, no stochastic policies, no seeded RNG inside the learner.
  This prototype contains **zero RNG in system and zero RNG in harness**:
  the batch digest is a deterministic logic-driven integer mixer (FNV-1a
  shape, documented in §Mechanics), batching is count-deterministic,
  all op sequences are explicitly designed. A double-run check asserts
  byte-identical ledgers across two independent runs of the full protocol.
- **A3 — the world may be unpredictable; adversity is designed.** All
  adversarial cases are explicitly designed sequences (tamper injections,
  ledger-overflow, illegal level changes) — no seeded RNG even as harness
  scaffolding. The verdict distinguishes "the system is deterministic"
  (double-run evidence) from "the test was adversarial" (enumerated below).

## Hypothesis

A memory store with **deliberate per-slot audit levels** (FULL vs SUMMARY)
preserves the MA1 "conscious" property for the audited subset — full replay
reconstructs exact state and deterministically verifies every summary batch —
while giving the learner a deliberate, audited mechanism to bound audit cost.
Capability manifests and inspection APIs derived from the ledger give an
overseer ground-truth answers with no "trust me" layer.

## Mechanics (native Zag, `trial/`)

Store `wb3_core.zag`: slots carry MA1 fields (live/value/pinned/region/tier/
step) **plus `alevel`** (0=FULL, 1=SUMMARY). Two append-only arrays:
- `audit[]` — FULL entries, 10 words each (op,slot,rc,b1,b2,b3,a1,a2,a3,stage),
  identical layout to MA1.
- `sum[]` — compact records for successful SUMMARY-slot ops, 6 words each
  (op,slot,a1,a2,a3,batch_seq). Before-words are NOT stored for summarized
  ops (the declared, audited tradeoff: per-op rollback degrades to
  batch-boundary rollback; see §What it does NOT show).

Op set: MA1's ADD/KILL/PIN/UNPIN/PROMOTE/DEMOTE (same refusal semantics) plus:
- `AUDIT_SET(slot, level)` — the learner deliberately sets a slot's audit
  level. Stage ≥ MANAGE required. **Always a FULL ledger entry** (the
  visibility decision is itself maximally visible). Structural floors:
  CORE-region slots and pinned slots refuse SUMMARY (`WB_AUDIT_LOCKED=109`).
- `SUM_FLUSH()` — deliberately closes the open summary batch. Always FULL.
  Refuses on empty batch (`WB_FLUSH_EMPTY=110`), refusal audited.
- `MANIFEST_UPDATE()` — writes the capability manifest words; always FULL.

Batching (deterministic, no RNG): the open batch auto-closes every
`BATCH=8` successful summary ops; `BATCH_CLOSE` is a FULL entry carrying
(batch_id, count, digest, clock_first, clock_last, sum_offset). Digest =
deterministic FNV-1a-style 32-bit mixer over the batch's compact records in
order: `d = ((d ^ w) * 16777619)` wrapping i32 arithmetic, seeded with
2166136261. **Refusals are always FULL entries** regardless of slot level
(a refusal is high-signal; MA1 invariant 1 — clean refusals — stays
globally testable).

Replay `wb_replay_check`: folds FULL entries (after-words) and compact
records (after-words) from genesis, recomputes every batch digest from
`sum[]`, compares against the BATCH_CLOSE entries; returns exact state
equality AND digest equality. Any divergence or digest mismatch = TAMPER.

Inspection API (native, ground truth from store+ledger only):
- `INSPECT_MANIFEST` — cached manifest vs manifest re-derived by folding
  the ledger's AUDIT_SET/MANIFEST entries (must match; else tamper signal).
- `INSPECT_COVERAGE` — per-region full/summary op counts folded from ledger.
- `INSPECT_WHY(slot)` — last entries touching the slot ("why this state").
- `INSPECT_REPLAY` — reruns the replay check.

Manifest words: (stage, policy_id, config_digest, full_ops, summary_ops,
batches). `config_digest` = deterministic mixer over per-slot alevels;
the learner's audit policy choice is declared data, advisors never decide
(the MA1 anti-RL clause extends to audit: no optimizer, no sampling).

Protocol (deterministic designed sequence, run at 1x and 10x):
1. init; stage→KILL(3) via audited op.
2. ADD 1 CORE + 6 USER slots. AUDIT_SET(SUMMARY) on CORE → must refuse 109.
3. PIN one USER slot; AUDIT_SET(SUMMARY) on pinned → must refuse 109.
4. AUDIT_SET(SUMMARY) on 2 scratch slots → OK (FULL entries in ledger).
5. Churn: 40 (1x) / 400 (10x) deliberate ops on SUMMARY slots
   (ADD/KILL/PROMOTE/DEMOTE with index-derived values, e.g. value=1000+i —
   logic-driven, no RNG) interleaved with FULL-slot ops; batches auto-close
   every 8; explicit SUM_FLUSH at end.
6. MANIFEST_UPDATE; run all four INSPECT_*; assert re-derived == cached.
7. Determinism: run steps 1–6 twice on fresh stores → byte-identical
   main ledger + sum array (folded checksums equal).
8. Scale check: ledger bytes per summary op == 24 and per full op == 40
   at BOTH scales (linearity: constant per-op cost).

Designed adversity (no RNG):
- T1: dedicated store, mini-protocol, then overwrite one compact record's
  after-word out-of-band (simulated ledger-bypass mutation) → replay MUST
  report TAMPER (digest mismatch). Tamper undetected = FAIL.
- T2: dedicated store, poke a live slot field out-of-band → replay MUST
  report divergence.
- T3: dedicated store with tiny ledger cap; drive ops until refusal →
  mutation refused (fail-closed), ledger intact, replay still passes.
  Dropped/silent entries = FAIL.

## Falsification criteria

- FAIL if replay diverges from live state at either scale.
- FAIL if T1/T2 tamper is NOT detected.
- FAIL if T3 drops entries or allows mutation past capacity.
- FAIL if any illegal op succeeds (SUMMARY on CORE/pinned; FLUSH on empty
  batch succeeding; mutation at stage < required).
- FAIL if the two deterministic runs differ in any ledger/sum byte.
- FAIL if manifest re-derivation disagrees with the cache.
- FAIL if per-op ledger bytes differ between 1x and 10x (nonlinearity).
- FAIL if a refusal mutates state (before != after on any refused op).

## Amendment A1 (2026-09-19, after first trial run — honest record, not silent)

The first run failed 9 checks and caught three implementation bugs against
the invariants above (documented in TRIAL_RESULTS_WB3.md). Two were pure
ordering bugs. The third was a design refinement: KILL no longer resets a
slot's region/audit-level (MA1 did reset region). Rationale: a killed slot
stays attributable to its region (coverage folds the true region) and keeps
its visibility budget until reallocated by ADD; this also keeps the
main-ledger-only level fold exact, since compact KILL records then have no
level effect to miss. The scale gate was restated on the margin
(`dbytes*26 == dops*952`) because fixed setup cost amortizes differently
across scales — the naive cross-multiplication was the wrong formalization
of the linearity claim, not a system nonlinearity.

## What it does NOT show

- That the learner's audit-*level choices* are wise (values/levels are
  protocol-fixed here, exactly as MA1 fixed values). Judgment quality of
  the visibility budget is later work; this trial proves the *machinery*:
  deliberate levels, structural floors, digest-verified summaries, exact
  replay of the audited subset.
- Whether losing per-op before-words on SUMMARY slots is acceptable policy
  in general — that is a declared design tradeoff (batch-granular rollback),
  tested mechanically here, judged later.
- 100x scale (named next test WB3-SCALE-100x), real deployment, or
  multi-region serving.
- The manifest schema is v0; schema evolution across development steps is
  future work.
