# H1 — VERDICT (FINAL, 1x)

**Arm:** H1 (Full deliberation per boundary)
**Date:** 2026-09-21
**Status:** COMPLETE — full 1x battery run (M1–M9, all legs double-run byte-identical).
**Final binary:** `work/arm_bin_v4` (built from `cl/arm.zag` with frozen toolchain
`znc_linux_x86_64_abed8aa1`; changes vs the first crew's binary: `spans-1x-*`
analysis modes, t_m2 METRIC_JSON framing fix, t_m8 iddk/iddv serialization fix.
m1-1x-prose and m1-1x-code re-ran double-run byte-identical under v4; the
v3→v4 delta is confined to t_m8's artifact path, so all other legs' v2/v3
evidence carries by construction and by the v2→v3 stdout-identity proof).

## Verdict: H1 SURVIVES

None of the three kill criteria fire. All margins are large and re-verified on
the final binary.

## Kill Criteria Assessment

### Criterion (i): Reuse hit rate ≤ fixed-64B baseline + 10pp — SAFE (does not fire)

**Definition used** (coordinator operationalization): reuse hit rate = fraction of
ingested units whose content exactly matches an already-live stored span,
content-keyed and offset-independent. This is deliberately NOT H1's
offset-including span key (which would make reuse 0% by construction and the
comparison meaningless).

**Protocol:**
- Single ingest of each frozen corpus (prose.bin 5,422,721 B; code.bin 9,515,341 B),
  units walked in file order; each unit's SHA-256 content hash checked against
  all previously-ingested units.
- Live-store slots: equal for both arms and ample (capacity ≥ max unit count of
  either arm), so zero evictions occur and "already-live" = every previously
  ingested unit. The only difference between the arms is the segmentation.
- H1 spans: the arm's own dry segmentation (`spans-1x-prose` / `spans-1x-code`
  modes; same `h1_segment_dry` mask-15 path as M1 ingest; spans verified to tile
  [0, n) contiguously; unit counts match M1 exactly: 22,508 prose / 39,501 code).
  Spans dumped twice, byte-identical.
- B-64 spans: the fixed-64B rule (offsets 0, 64, 128, …, last = remainder) —
  deterministic from the frozen corpora, no B-64 rebuild needed. Unit counts
  reproduce the official B-64 evidence exactly (84,731 prose / 148,678 code).

**Results:**

| Corpus | H1 reuse | B-64 reuse | H1 − B-64 | Kill bar (B-64 + 10pp) | Fires? |
|---|---|---|---|---|---|
| prose | 15.892% (3,577/22,508) | 0.001% (1/84,731) | **+15.891 pp** | 10.001% | No |
| code  | 23.802% (9,402/39,501) | 0.396% (589/148,678) | **+23.406 pp** | 10.396% | No |

H1 exceeds the fixed-64B baseline by ≥ 10 absolute points on **both** corpora.
Deliberation buys real reuse: H1's boundary-finding aligns cuts with recurring
natural content (15.9% prose / 23.8% content-dedup in a single ingest) while the
fixed grid's arbitrary phase alignment captures ~0%.

**Cross-check (independent operationalization):** H1's own m7-1x implements the
lookup-hit reading of the same criterion (re-ingest ID-stability + 5,000 lookups
vs a slot-limited B-64 baseline at S = H1's live slots — the literal
"equal live-store slots" construction): prose H1 100.0% vs baseline 32.7%,
code H1 100.0% vs baseline 40.9%, `m7_kill_i_triggered: false`. Both
operationalizations agree: criterion (i) does not fire.

### Criterion (ii): Refusal > 30% AND mean delib ops/cut > 10^4 — SAFE (does not fire)

Re-verified on the final binary (m1-1x-prose, m1-1x-code, double-run):

| Corpus | Refusal | Mean delib ops/cut | Bar |
|---|---|---|---|
| prose | 0.0% (0 / 62,009 candidates) | 253 | 30% / 10,000 |
| code  | 0.0% | 252 | 30% / 10,000 |

Refusal is 30 pp below bar; ops are ~9,750 below bar (39× headroom). Deliberation
is cheap integer evidence accumulation; the BAR (60) is calibrated so valid
boundaries commit.

### Criterion (iii): BAR ±10% sensitivity flips > 25% — SAFE (does not fire)

Re-verified on the final binary: 0.0% flips on both corpora (0 / 62,009
candidates; bar 25%). Commit decisions are robust to BAR 54/66; evidence scores
are decisively above or below the bar, not clustered at it.

## Full 1x Battery Results

| Metric | Prose | Code | Notes |
|---|---|---|---|
| M1 recall / boundary | 100.0% / 100.0% | 100.0% / 100.0% | 22,508 / 39,501 units |
| M1 ID probe (A15) | PASS 64/64 | PASS 64/64 | PROVISIONAL-PENDING-FREEZE |
| M1 ablation (grid-only) | 6,698/6,698 valid | 10,738/10,738 valid | noticers are proposal-only |
| M2 ETC (T1/T2/T3) | 1 / 1 / 1 | 1 / 1 / — | uncensored; ep0 recall 0.0 (no leak); final 100/100 |
| M9 shape (T1) | fast-then-flat | fast-then-flat | takeoff ep 1, steepness 100.0, late gain 0.0 |
| M3 survival / fresh recall | 100.0% / 100.0% | — | 1,000 valuable; 1,920 mgmt entries; 50/50 weakens; CLEAR |
| M4 rev boundary/content | 100.0% / 100.0% | 100.0% / 100.0% | kill rate 0.0%, no kill-substitution, 1 episode |
| M5 memory | 2.413 B/B (**bar 1.5: FAIL**) | — | audit 8.326 entries/KB (bar 10: PASS); 22,508 units; ledger 44,092 entries |
| M6 transfer rec/bnd/rev/tax | 100/100/100/0.0 | 100/100/100/0.0 | p2c and c2p identical |
| M6 memorizer gate | — | — | p2c drop 54.8 (≥15) → **validity gate PASS** |
| M7 hit / reuse | 100.0% / 100.0% | 100.0% / — | kill_i_triggered: false; reread 2,406,170 B |
| M8 gate | **PASS** (5 perturbations × 2, byte-identical) | GATE.txt | |

**M5 note (honest):** H1 fails the M5 memory bar (2.413 B/B > 1.5). This is a
metric bar, not a kill criterion — it does not affect the SURVIVES verdict, but
it is real: the deliberate machinery (slot tables, per-window staging, retained
ledger) costs ~2.4 bytes per source byte at 1x. Worth watching at 10x.

## Determinism

- Every leg ran twice via `run_metric.sh`; all stdouts byte-identical
  (IDENTICAL), rc=0, no FATAL.
- M8 gate: 5 perturbations (clean/frag/aslr/starve/freelist) × 2 runs, artifacts
  compared by `m8_compare.py` — **M8GATE PASS** (all 10 runs byte-identical).
- Zero RNG in decision paths (all tie-breaks by priority/position/ID).
- v2→v3 binary change (t_m2 JSON framing fix) proven not to alter other paths:
  v3 m1-1x-prose stdout byte-identical to v2.

## Fixes Made by This Crew (vs first crew's binary)

1. Added `spans-1x-prose` / `spans-1x-code` analysis modes (dry segmentation dump
   for the criterion-(i) adjudication). Additive; no existing path touched.
2. Fixed t_m2 METRIC_JSON framing: the `M9,...` diagnostic line was printed
   between the last JSON field and `j_end()`, truncating the JSON object
   (missing closing brace in fragment.jsonl). Moved after `j_end()`. Only
   affected m2-t1-prose/code fragments; both legs re-ran clean under v3.
3. Fixed t_m8 store-image serialization bug (found 2026-09-21): the artifact
   dump appended `s.iddk`/`s.iddv` with size `dcap*8`, but the ID-map tables
   are allocated `dcap*4` (4-byte slots; the 8-byte size was copy-pasted from
   the dedup-key table). This read 2× past the allocation → deterministic
   "panic: slice index out of bounds" on every m8-1x run. Fixed to `dcap*4`
   for both. Bug was in the m8 artifact path only (m1/m3 pass standalone);
   the arm's core logic is untouched. Final binary is v4.

## M8 gate status (2026-09-21)

- The m8-1x mode had never successfully run: every invocation panicked
  deterministically (empty stdout, "panic: slice index out of bounds").
- Root cause: t_m8's store-image serialization read `dcap*8` bytes from the
  `dcap*4`-byte ID-map tables (see fix 3 above). Located via an instrumented
  debug binary (phase prints showed the panic between the img-dump start and
  the hash write; audit of img_append sizes vs h1_new allocations found the
  2× mismatch on iddk/iddv).
- After the fix, m8-1x clean completes: `M8,100.0,100.0,125858` with all
  artifacts written (ledger.bin, ledger_chain.txt, store_hashes.txt,
  store_chain.txt, alloc_trace.txt).
- Full gate (clean/frag/aslr/starve/freelist × 2, v4 binary): **M8GATE PASS**.
  All 10 runs rc=0 with stdout `M8,100.0,100.0,125858`; `m8_compare.py`
  confirms byte-identical artifacts across all perturbations (ledger chain
  `afc7e9ab…`, store chain `2c3450ea…`, alloc trace identical). The
  entropy/time-starved run is identical too — the arm reads no clock or RNG.
  Full log in `work/battery_full/m8/GATE.txt`.

## Ambiguities (remaining)

1. **Criterion-(i) definition** — RESOLVED per coordinator: content-keyed
   single-ingest dedup (this document). The alphabet doc's "fraction of recalls
   served from existing chunks" reading (H1's m7) agrees on the verdict.
2. **A15 ID probe** — still PROVISIONAL-PENDING-FREEZE (Micah has not frozen the
   remap schedule/function). H1's 64/64 PASS is against the proposed procedure.
3. **Nomination overflow:** 256-entry cap per 4 KiB window may truncate
   punctuation-heavy windows before top-16 selection. Not observed in M1 (max
   nominations < 256), not proven.
4. **Span-key collision:** `(cid<<36)|(off<<12)|len` collides when `len=4096`.
   Window size caps len < 4096 in practice, but not enforced.
5. **M3 operation counts:** whether the arm's chunks literally realize the
   3k-add/3k-kill/4k-add schedule is not verified by chunk counts (mgmt entries
   = 1,920 logged).
6. **M8 capacity reading:** the validator implements M8 as one large-capacity
   instance (see harness AMBIGUITIES.md A17); H1's t_m8 follows the same
   construction.

## Files

- Spec: `docs/lab/units/arms/H1/ARM_SPEC.md`
- Build log: `docs/lab/units/arms/H1/BUILD_LOG.md`
- Source: `tnn-lab/units/arms/H1/cl/arm.zag`
- Scorecard: `tnn-lab/units/arms/H1/scorecard_r1_1x.json` (complete; replaces the partial)
- Battery evidence: `tnn-lab/units/arms/H1/work/battery_full/` (per-leg run1/run2, STATUS.txt)
- Reuse analysis: `tnn-lab/units/arms/H1/work/reuse_crit1.py` (+ spans dumps)
- Binary: `tnn-lab/units/arms/H1/work/arm_bin_v4` (not for commit)
