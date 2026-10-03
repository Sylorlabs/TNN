# PREREG_REVISE.md - INDEX lane, wave-20261002-1121pdt

Frozen: 2026-10-02 (this file is committed ALONE, before any
implementation file). Status at freeze: PROPOSED (unexecuted). No
sealed results below were observed before freezing. Exploratory
analysis (clearly labeled in REPORT.md, no runs) informed the
design and the bar; every run below is a fresh build plus fresh runs.

## Governing context

wave-20261002-0521pdt INDEX-EVICT reached EVICT-PASS: `idx_on_evict`
(1 hook line in `evict_node` + ~90 lines) maintains index coherence
across eviction storms. Its red team flagged a REAL, known,
out-of-scope gap: `t2_revise_graph` (base) tombstones tag-101 chain
nodes WITHOUT going through `evict_node`, so the hook never fires.
This wave covers that path: (a) test coverage of the t2_revise_graph
path against the index, (b) soak storms on the eviction hook with a
pure-Zag deep validator, (c) fault-injection panic hunt for the
0221pdt index-cycle crash class.

## Base under test

CONTROL base: `sealed_base_new.zag` verbatim (0521pdt EVICT-PASS
build: evict hook present, NO revise hook).
CANDIDATE base: CONTROL base plus, in `t2_revise_graph` only:
  - after the tombstone (`ns(W,stale,0,0); ns(W,stale,36,0);`):
    `idx_on_chain_break(W,stale);`
  - before `return 0;` (revert path) and before `return 1;`
    (success path): `if((idx_mode(W)&1)==1){idx_refile(W,m);}`
CONTROL patch: `sealed_patch_new.zag` verbatim.
CANDIDATE patch: CONTROL patch plus `idx_refile` (dup-safe refile:
membership scan across all 4 plen buckets, then `idx_add` under the
CURRENT recomputed chain plen; safe no-op when the chain is invalid
or the MAP is already indexed).
New modes: 0. New bridges: 0. New handlers: 0. New semantic cases: 0.
The revision hook reuses the sealed `idx_on_chain_break` machinery;
the refile recomputes the plen from the actual chain (never assumed).

## Exploratory analysis (no runs; shapes the kill bars, not the verdict)

`t2_revise_graph` revises a MAP's executable chain on contradiction:
find the stale 101 step via its type-1 edge to the contradicted fact,
tombstone it, splice in a corrected 101 step, re-execute. Tracing the
base source (no execution):
- Canonical SUCCESS (stale = last step, no successor): the chain is
  repaired 1:1, plen unchanged, gate stays 1 without any hook.
- Canonical REVERT (stale = middle step; the corrected value fails
  the next guard, execute returns -999999): the chain is restored,
  gate stays 1 without any hook.
- ADVERSARIAL shared-stale: two MAPs (A then B) whose chains share
  one 101 step via two guards (gA1 built after gB1, so the
  highest-id scan selects gA1). Revising A rewires gA1, tombstones
  the shared step, and A's re-execution succeeds (A's own chain is
  repaired). B's chain (via gB1 to the now-dead step) is broken:
  `rb_chain_plen` returns -1 while B stays in its plen bucket. The
  gate must REJECT (cause 3, plen mismatch) on the CONTROL build.
  B's own revision then finds the spliced step, fails execution on
  B's broken chain, and reverts without repairing B.
The candidate hook unlinks every MAP whose chain contains the
tombstoned step (A and B), then refiles A (chain valid, plen
recomputed) while B's refile is a safe no-op (chain still broken).
Expected CONTROL R3: idx_validate 0, cause 3. Expected CANDIDATE R3:
idx_validate 1, A in its plen bucket, B in no bucket.

## Sealed eval protocol (frozen)

Binaries (pinned znc, pure Zag, `export PATH="$HOME/safebin"`):
- revise_control_bin: CONTROL base + CONTROL patch + revise_driver.zag
- revise_candidate_bin: CANDIDATE base + CANDIDATE patch + revise_driver.zag
- storm_fill_bin, storm_evict_bin, storm_churn_bin: CANDIDATE base +
  CANDIDATE patch + stormlib.zag + the respective storm driver
- storm_fault_bin: CANDIDATE base + CANDIDATE patch + stormlib.zag +
  storm_fault.zag
- noop check: revise_candidate_bin rebuilt with the frozen 0521pdt
  `evict_driver.zag` in place of revise_driver.zag; stdout must be
  byte-identical to revise_control_bin on the same driver.

`revise_driver.zag` (frozen instrument, mode 3 = MAP index + MTF):
- R1 canonical SUCCESS: plen-5 chain over facts (6101..6105),
  promoted MAP; contradict the LAST fact (6104,1,6105) with 7105.
  Emit: gates before/after, MAP answer field before/after, bucket
  walk locating the MAP, unchain counter.
- R2 canonical REVERT: same world; contradict the FIRST fact
  (6101,1,6102) with 7105 (corrected value fails the next guard).
  Emit: gates before/after, MAP answer field (must be unchanged),
  bucket walk, unchain counter.
- R3 adversarial shared-stale: hand-built chains A (plen 3, guards
  gA0/gA1) and B (plen 3, guards gB/gB1) sharing the last 101 step
  (gA1 higher id); both MAPs promoted with the contradicted fact in
  their fact lists; `revise_on_contradict(W,factn,9999)`. Emit: gates
  before/after, first-flip cause, bucket walks for A and B, MAP
  answer fields, unchain counter, post-revision query answers.

`stormlib.zag` (frozen shared instrument): seeded LCG (fixed seed,
byte-identical reruns), parameterized chain builder, and the
pure-Zag deep validator `idx_deep_validate`: the production gate
(idx_validate + fidx_validate: members live/tagged/plen-correct, no
cycles, bounds respected) PLUS completeness (every live tag-20 with
valid plen is in exactly one bucket, its plen bucket; invalid plen
implies no bucket; every live tag-1 with field 24 != -999, inquiry
markers excluded by design, is in exactly one FACT chain; no
duplicates; no misfiled buckets) PLUS MTF-winner sanity. Pure reads.

- storm_fill: mode 7; 40 MAPs + 200 FACTs; 6000 teach cycles.
  Timed (shell `time`): per-alloc cost WITH free space.
- storm_evict: mode 7; ~120 MAPs + ~4000 FACTs; 2 protected probe
  chains queried every 10 evictions; 40 natural evictions, deep
  validator after EVERY eviction. Timed: per-eviction cost.
- storm_churn: mode 7; fill to ~8180 nodes; 30 alloc cycles at
  capacity (each forces an eviction). Timed: per-alloc cost AT
  capacity (the latency cliff).
- storm_fault: 4 fresh worlds; fault injections: (F1) cycle spliced
  into a MAP bucket list, (F2) OOB next pointer (99999), (F3) dead
  node left at a bucket head (direct kill, hook bypassed), (F4)
  cycle in a FACT bucket chain. After each: gate verdicts, then
  `rebind_try_idx` / `t2_gather` / `t2_lu_first` must complete
  (SURVIVED marker) with answers equal to pre-injection answers.

Each binary runs its driver 3x; stdout captured; sha256 recorded.
Wall-clock times are recorded OUTSIDE the hashed stdout (shell
`time`); stdout stays fully deterministic.

## Kill bar (frozen, will not be weakened)

REVISE-PASS iff ALL of the following hold:

(i) Coverage vacuity (CONTROL): R3 shows `idx_validate==0` after
`revise_on_contradict` with first-flip cause 3 (plen mismatch); R1
and R2 show `idx_validate==1` after revision. If R3 never flips, the
adversarial construction is vacuous and the verdict is FAIL
(redesign), not PASS.

(ii) Hook coherence (CANDIDATE): `idx_validate==1` and
`fidx_validate==1` after every revision in R1, R2, R3, all 3 runs.
In R3: bucket walk finds MAP A in the plen-3 bucket and MAP B in NO
bucket. Any gate 0 is FAIL.

(iii) Revision semantics preserved: R1 MAP answer field 6105 ->
7105 (control and candidate agree); R2 MAP answer field unchanged
(6105); R3 MAP A answer field 9001 -> 9999. Any disagreement
between control and candidate is FAIL.

(iv) Determinism: 3/3 byte-identical runs per binary per driver;
hashes recorded.

(v) Healthy-state no-op: candidate binary on the frozen 0521pdt
`evict_driver.zag`: stdout byte-identical to the control binary on
the same driver, 3/3 runs.

(vi) Mechanism accounting: candidate R3 unchain counter
(node-0 field 12) >= 2 across the run; control R3 counter is 0;
candidate R1/R2 counters >= 1 (tombstone unlinks the revised MAP,
refile restores it).

STORM-PASS iff ALL of the following hold:

(vii) Panic hunt: all 4 fault injections show the gate rejecting
(idx 0 for F1/F2/F3, fidx 0 for F4), the binary exits 0 with the
SURVIVED marker, and post-injection answers equal pre-injection
answers. Any crash, hang, or answer divergence is FAIL with the
fault id and evidence.

(viii) Soak coherence: `idx_deep_validate==1` after EVERY eviction
in storm_evict (40 per run), all 3 runs. Any 0 is a KILL of the
coherence claim with the violating evidence dumped (bucket id,
member id, check id). A soak failure blocks REVISE-PASS adoption
until root-caused.

(ix) No wrong answers: no WRONG-ANSWER line in any storm run
(a non-miss answer differing from the taught expected value).

(x) Determinism: 3/3 byte-identical per storm binary; hashes
recorded.

(xi) Cliff characterization (no kill, reported): per-alloc wall time
with free space (storm_fill) vs at capacity (storm_churn);
per-eviction wall time (storm_evict). Reported as numbers with the
ratio; a >3x per-eviction superlinearity vs the arena-bound
expectation is a finding, not a kill.

REVISE-FAIL / STORM-FAIL iff any applicable condition above fails,
with the failing condition and first-divergent evidence recorded in
SEALED_EVAL.md. PARTIAL may be recorded only with per-condition
HOLD/FAIL and no bar weakening.

## Red-team self-review (frozen requirement)

SEALED_EVAL.md and REDTEAM_SELF.md each end with a red-team
self-review attacking the work: shapes where the hook under- or
over-unlinks (stale shared three ways, stale on no indexed chain,
duplicate refile races), what would falsify each verdict, and the
residual non-revise chain-killers (infrastructure victims tag
40/900, plen-2/plen-4 bucket positions). The verdict lines name this
prereg as the governing frozen bar.

## Governance

This prereg is committed ALONE before any implementation file.
Prereg commit strictly precedes implementation commits. No kill bar
above may be weakened after seeing results; amendment requires a new
frozen prereg and re-execution. Pure Zag only; no Python anywhere.
Zero em-dashes in all lane documentation (check_no_dash.sh before
every commit).
