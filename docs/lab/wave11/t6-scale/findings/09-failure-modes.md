# Slice 09 — Pre-mortem: everything that breaks at 1000x that works at 1x (Track 6)

## 1. Slice
Pre-mortem survey of 1000x scale failures: performance, correctness, robustness, operational.
Ranked by expected hit order. Each entry: detection, mitigation, scale-bug (fixable) or
scale-wall (fundamental).

## 2. Falsifiable claim
Of the six failure modes below, at most three can appear in a 1000x developmental trial
after their listed mitigations are applied; kill this survey if a 1000x dry run surfaces
an unlisted, unmitigated failure mode — or if any listed mitigation costs more than 10%
of its organ's per-episode compute budget.

## 3. Design
Ranked by expected hit order at 1000x (assumes 1x ≈ 12–500 episodes; 1000x ≈ 12k–500k episodes,
audit bytes/episode constant).

**F1 — Audit ledger exceeds the znc 2^25-byte single-slice indexing limit.**
Hit order #1: 500k episodes × ~70 bytes/entry (16-word entries, brief §audit layout) crosses
33,554,432 bytes far earlier than anything else. Detection: per-episode byte accounting +
pre-run projection `E × bytes/ep` vs 2^25; hard assert before each write. Mitigation:
chunked ledger with identical logical semantics (validated workaround, brief §toolchain).
**Scale bug.**

**F2 — Index/counter width exhaustion below u64.**
Logical clocks are u64 (slice 17 replay protocol) and never wrap at 1000x — but every
u32 index, packed word counter in the 16-word audit entries, `st_snap` bounds arrays, and
episode-indexed VAR tables are width-limited. Detection: static audit of every counter's
type + pre-run worst-case capacity proof at 1000x; runtime 90%-of-width watermark assert.
Mitigation: u64-only counters; wrap plan = epoch-segmented ledger — at 90% width on any
counter, close the epoch segment and open a new one with cross-epoch pointers; a full
epoch boundary is itself a prereg-declared event, replayed deterministically.
**Scale bug.**

**F3 — Per-episode cost grows superlinearly (big-O per organ).**
- Eliminative hypothesis logic: elimination sweep is O(H) per episode; if live hypothesis
  pool H grows with E, total is O(E²). Bounded pool → O(1)/ep; unbounded → this fires.
- Memory substrate: 32-slot bounded store → kill/pin/promote O(1)/ep. Safe by construction.
- Audit replay / deliberative standards checks: full-trail scan is O(E) per episode →
  O(E²) cumulative; post-change verification in reasoning control is O(state) per
  self-change — constant per event, fine at 1000x if self-changes are rare.
- Composition/symbolic recall: per-episode trace scan O(T); unbounded trace growth → O(E²).
Detection: per-organ per-episode timing series, kill if regression slope of cost vs
episode > 0 over the first 10% of the trial (projection gates the remaining 90%).
Mitigation: bounded pools, amortized full scans (every K episodes), audit indexing.
**Scale bug — unless unbounded hypothesis history proves load-bearing for integrity,
in which case it becomes a scale wall (flagged, not resolved here).**

**F4 — Fault rates multiply by 1000 (Track 1 corrupted-state work at scale).**
Slice 22's render-gate catches single-variable corruptions with checksums+range checks —
but at 1000x, 1000x more turns means 1000x more expected faults, and the documented
honesty gap (corruption between gate and render) gets 1000x more rolls of the dice.
Detection: existing mask + per-turn `OP_STATE_DEGRADED` log; add fault-rate monitor:
kill if degraded-turn fraction exceeds prereg baseline ×3. Mitigation: double-gate
(pre-render + post-render hash comparison), per-segment checksums so one bad segment
rotates out instead of failing the run, and a 1000x fault-injection trial (10M faults
per class) as the gate before the real trial. **Scale bug** for detection coverage;
**scale wall** only against an adversary with arbitrary internal write access
(slice 22's threat-model boundary, unchanged).

**F5 — Replay determinism becomes unverifiable.**
Byte-identical replay from full logged state works at 1x; at 1000x the log is
unreplayable-in-practice in one pass. Detection: checkpoint chain with hash chaining —
replay-verify random checkpoint windows during the trial; kill if any window
reproduces non-byte-identically. Mitigation: segment checkpoints every N episodes,
each checkpoint independently replay-verified; replay = chain of verified segments.
**Scale bug.**

**F6 — Operational: nobody is watching the 1000x trial.**
The overnight-run watchman pattern (human check-ins, cf. wave8 RESULTS_V3.md,
wave9 S10 archive note) does not scale to a multi-week developmental run.
Detection/mitigation: automated watchman — a deterministic sentinel, separate process,
with authority to freeze the trial on invariant violation (audit growth rate, per-episode
cost slope, degraded-turn fraction, integrity refusal rate all monitored against
prereg bands) and page a human. Human on-call rotation replaces "Micah wakes up to
a verdict sheet" for the live phase; the verdict sheet is the handoff format, not the
watch mechanism. **Scale bug** (organizational, fixable).

## 4. Kill bar
Run the 1000x dry run (same mechanism, prereg-shortened curricula). Kill the 1000x
program plan if ANY of: (1) a per-episode cost series shows slope > 0 after the first
10% (F3); (2) any counter reaches 90% width without a clean epoch rollover (F2);
(3) any replay-verified checkpoint window fails byte-identity (F5); (4) degraded-turn
fraction exceeds prereg baseline ×3 (F4); (5) a failure mode appears that is not
F1–F6 above (survey incomplete). All mitigations must cost ≤10% of their organ's
per-episode budget or they count as fired.

## 5. Honesty notes
Weakest point: F3's eliminative-hypothesis case. I do not know whether bounding the
live hypothesis pool preserves the load-bearing behavior that stopped cheats at 10x/100x
(integrity attribution, wave-6 evidence). If bounding degrades eliminative verification,
the honest outcome is a scale wall, and I am NOT claiming the mitigation preserves
integrity — that needs its own falsification trial before any 1000x integrity claim.
Second weakness: the kill bar's "unlisted failure mode" clause makes the survey's
completeness itself falsifiable, which is the point, but a dry run can only surface
modes reachable by the dry curriculum — silent divergences (e.g. slow corruption of
judgment weights) may need full 1000x to appear. I am NOT claiming this survey covers
sensor-spoofing at scale — the accepted truthful-but-sensor-deceivable hole is
orthogonal and gets worse with longer horizons; it is owned by the trust-tiers line,
not this slice.

## 6. Next build step
Build the per-organ per-episode timing + byte-accounting harness first (F1, F3
detectors) in Zag on the current codebase, and run it on the existing 100x evidence
to establish the slope≈0 baseline — before any 1000x build. If the harness shows
slope > 0 already at 100x, the 1000x program is gated until F3 is fixed, not after.
