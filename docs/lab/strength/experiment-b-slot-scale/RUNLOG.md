# RUNLOG — Experiment B: slot scale (Micah, 2026-09-25 ~22:41 PDT)

"How expensive is it to scale up slots and have you tried it?" Honest
baseline: nobody had tried — the strength core ran 14 user slots, never
varied. This is the first variation: 14 / 28 / 56 / 140 user slots.

Program rule under test: nothing may degrade with more scale/power.

## Build

- Base: `~/workspace/strength-recycle/` at tnn-native-lab commit
  `5610c1215d7f` ("strength-recycle: P3-expiry-vs-lien law clarification"),
  verified via gh-api. Current law: hole-1 (st_kill trainer-gated), hole-2
  (delete never recycles; st_recycle explicit), high-water erase pricing,
  F4 single-use cites, B2 arm, P2+P3.
- Cite-mode switch (W/G/H) ported from `~/workspace/strength-f6/` into the
  recycle core via `merge_citemode.py` (exact-match replacements, fail loud).
  Law invariant: default mode is WINDOWED and the WINDOWED path of
  `st_cite_consumed` is the base-commit body VERBATIM. G/H branches port
  F6's `st_consume_lo`/`st_pay_lo`/`st_last_add_idx` onto the current-law
  consuming op set (KILL/KILL_EVIDENCED/OVERWRITE/DELETE_STRONG).
- Merge bug caught by bisection: the first merge_citemode.py inserted
  `st_set_cite_mode` INSIDE `st_init` (replacement didn't span the
  function's closing brace); znc reported only a misattributed E0204 at an
  unrelated line. Fixed; both binaries build clean.
- Two binaries from one driver (`slot_driver.zag`):
  - `build_merged/slot_bin` — merged core (law + cite_mode)
  - `build_base/slot_bin` — pristine recycle core; `[CITEMODE]` lines
    stripped by `build.py`. Base copy verified byte-identical to the repo
    source (`diff` clean).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Verification

- W-mode law equivalence: `build_base` vs `build_merged` on FUNC/14 →
  byte-identical output (proves the merge preserves base-commit law under
  the default mode). Re-verified after every driver rebuild.
- Every functional leg (FUNC, WEDGE) run ×2 per config; `cmp` clean.
- Checker (`ck_verify`), replay check, and refusals-hygiene clean on every
  run (ckfail=0 everywhere).

## Timing methodology (important)

First COST attempt used wall clock (CLOCK_MONOTONIC). It measured
scheduler noise, not op cost: a run showed real=72s vs user=3.2s on this
shared oversubscribed VM, and per-op max samples spiked 100× over medians.
Switched the cost clock to CLOCK_PROCESS_CPUTIME_ID via
`_zag_raw_syscall(228,2,...)` — CPU time is the honest per-op cost here.
Medians over 21 batches (1 warmup round discarded); min/max reported.
Timing is cost measurement only, never mixed into functional evidence.

COST leg ops (fresh store per round, 21 rounds):
- add_empty: 10 adds to an empty store (first-free-slot scan breaks early)
- add_fullscan: fill all slots, then 5 REFUSED_FULL adds (full slot scan)
- cite: 20 distinct-episode st_evidence on one live slot
- destroy: 5 × (add + 4 cites + justify, setup untimed) then timed
  st_kill_evidenced incl. the priced effort check
- checker: 5 timed ck_verify passes over a FIXED 100-episode honest
  curriculum (14-slot rotation on every config → identical ledger,
  audit_n=323; deltas isolate the slot-array scan cost).
  - Caught a workload bug: first version rotated t%ucap, leaving the
    140-slot ledger destroy-free (103 entries, adds only) — the 140
    checker looked 5× FASTER than 14. Fixed to a fixed 14-slot rotation.

## Legs

- BYTES: allocation inventory per config (audit_cap=32768 fixed, recorded).
- COST: per-op CPU-time medians per config (2 rounds each).
- FUNC: 400-episode deterministic honest curriculum per config
  (add → cite-4-freshest → justify → destroy; checker+replay at end).
- WEDGE (G mode only): finite salient pool P ∈ {8,16,32}, rotating cites,
  slots ∈ {14,28,56,140}; measures ok destructions / 121 refusals /
  first-121 iteration / full-wedge (ADD→FULL) iteration.

## Sequencing note

## Results

The CKL leg (checker vs ledger size) was added to the driver AFTER the
BYTES/FUNC/COST/WEDGE battery. The rebuild only adds a new function and
one dispatch branch; spot-check: the final binary reproduces the
pre-CKL FUNC (all 4 configs), BYTES (all 4), and WEDGE 14/8 logs
byte-exactly. The battery stands on one binary's semantics.

(see VERDICT_B.md for the tables)

- Memory: strictly linear, +31 bytes/user-slot; 14→140 adds 3,906 bytes
  total (2,753,008 → 2,756,914 at audit_cap=32768). Largest single
  allocation 688,128 bytes « 2^25 ceiling (ceil_ok=1 all configs).
- Per-op: add_empty / add_fullscan / cite / destroy FLAT across 14→140
  (all within noise of each other, both rounds).
- Checker: flat vs slot count on the identical 323-entry ledger (~29ms
  at 14 and at 140 — slot scan negligible); superlinear vs ledger size
  (CKL leg: 163→1,383 entries = 8.5× → 11.4→332.7 ms = 29×, ~n^1.6;
  14 vs 140 agree within 3% at every ledger size). Ledger length, not
  slots, is the checker's cost driver.
- Ledger growth: ~3.4 entries/episode, independent of slot count.
- WEDGE: cliff scales LINEARLY with slots — total ok destructions =
  slots × P/4, then one 121 per slot, then ADD→FULL wedge. 14/8
  reproduces the F6 measurement exactly (28 ok, 14×121, wedge@42).
