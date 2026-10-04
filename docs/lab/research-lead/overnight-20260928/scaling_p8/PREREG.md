# PREREG -- SCALING-P8

Worker: SCALING-P8. Lane: `lane/scalingp8`. Date: 2026-10-03.
Pure Zag for all computation and statistics. Shell/git orchestration only.
Frozen before implementation. Claim IDs reserved C526..C549.

## 0. Why this lane exists

C267 (SCALING-5000) is the canonical scaling result. C299 and C375 both
diagnosed the SAME representation defect: `res_op` (and `t2_guard`,
`t2_set`, `t2_mov`, `t2_inc`, `t2_dec`, `t2_jnz`) reads an operand
`op >= FRAME_BASE` as a FRAME SLOT (`slot = op - FRAME_BASE`) while TRIAL
LITERALS are NODE IDS. One integer namespace, two meanings. A separate
worker is fixing this as a representation invariant on branch
`scale/namespace-invariant`. **This lane does NOT duplicate that work and
does NOT assume its fix.**

Instead this lane (a) verifies the collision independently and locates the
exact threshold **in the engine actually used for scaling** (the C267
`scaling_5000` 65536-node build), and (b) profiles the engine to separate
cognitive inefficiency from implementation inefficiency (charter 94), and
(c) builds sublinear retrieval with LEARNER-MAINTAINED indices whose keys
emerge from learned structure (charter 36), and (d) audits structural
references with explicit invariants (charter 37).

## 1. Instruments

Engine under test: `s5000_full.zag` = `base_64k.zag` (C267, NN=NE=65536,
FRAME_BASE=100000) + `sc_patch_5k.zag` + `s5000_driver.zag`, recovered
from commit b0779fd01.

Infrastructure rule (mandatory, brief section 4.0): the engine's only
output path is `fn emit(s) { _zag_print(s); }`. **Every run asserts
output length > 0.** `_zag_raw_syscall` is INERT on this host and is not
used anywhere in this lane.

## 2. Preregistered hypotheses and kill bars

### K1 (namespace collision, independent confirmation)
H: in the C267 65536-node engine, `FRAME_BASE = 100000 > NN = 65536`, so
the collision CANNOT occur at 5000 MAPs; the canonical 5k result is safe
**by accident of two unrelated constants**, and no invariant anywhere
enforces `FRAME_BASE > max_node_id`.
K1a PASS: `res_op`/frame-constant grep shows FRAME_BASE=100000 and
NN()=65536 and no check of the form `FRAME_BASE > NN`.
K1b PASS (reproducer): a build with FRAME_BASE lowered below the observed
maximum live node id produces a SILENTLY WRONG answer (no crash, no
nonzero exit, wrong `ans=` or `ok=0`), i.e. the failure mode is
silent-corruption, not a crash.
K1c KILL-BAR: if lowering FRAME_BASE produces a CRASH rather than a
silently wrong answer, the defect class is different (fail-loud) and the
"silent corruption" claim is withdrawn.
K1d KILL-BAR: if the canonical 5k output on this host is not
byte-identical to `s5000_run1.txt` (sha256 382e913a...), this lane's
harness is broken and all measurements are void.

### K2 (profiler, charter 94)
H: retrieval cost is dominated by **write-path global scans**, not by the
query path. Specifically `ev_teach`'s "most recent FACT node" lookup is
an unconditional O(NN) scan executed once per taught edge, and `decay()`
is an unconditional O(NE) scan executed once per teach AND once per
query, so total cost is O(E_write * NN + (E+Q) * NE).
K2 PASS: profiler counters show `ev_teach_prev_visits / live_nodes` is
constant in D (i.e. linear in live node count per write) and that
`prev_visits + decay_visits` exceeds `rebind_visits + gather_visits` by
more than 10x at D=4995.
K2 KILL-BAR: if the query-path scans dominate instead, the hypothesis is
falsified and reported as such.

### K3 (learned-key index, charter 36)
H: the key that makes retrieval sublinear can be derived from LEARNED
state, not from a human ontology of categories. Concretely: node tag `t`
(written by the learner's own `promote_graph`/`write_node`) plus the
learner's own subject value is a sufficient emergent key, and
"most-recent-live-node-of-tag-t" is maintained in O(1) by the allocator's
own monotonic allocation order.
K3 PASS: with the index, per-write scan visits fall from O(NN) to O(1)
and the 5000-MAP answer is BYTE-IDENTICAL to the linear answer.
K3 KILL-BAR: if any stress case (below) changes a single emitted answer
relative to the linear reference, the index is REJECTED regardless of
speed. Correctness beats speed.
K3 STRESS BATTERY (all must be byte-identical to the linear/unindexed
reference): stale entries, deletion/eviction, revision, hash collision,
cycle injection, malformed reference injection, heavy churn, adversarial
insertion order (reverse, shuffled-by-construction, clustered).

### K4 (scale progression 10k -> 20k -> 50k -> 100k)
H: with the namespace invariant made structural and write-path scans
removed, MAP count scales with constant per-MAP cost.
K4 records the measured ceiling. There is NO preregistered pass bar; the
deliverable is the measurement plus the location of the real limit.
K4 KILL-BAR: any run whose emitted answer disagrees with the
lower-scale reference is a CORRECTNESS FAIL and stops the progression
immediately, regardless of wall time.

## 3. What is NOT claimed

- No L3 claim. No new cognitive form is proposed.
- No fix of the frozen engine's namespace is landed here (separate lane).
- No claim that index keys are "discovered"; the claim tested is only
  that they are DERIVABLE FROM LEARNED STATE rather than enumerated by a
  researcher-authored category list.

## 4. Determinism bar

3/3 byte-identical stdout for every reported run, sha256 recorded.
