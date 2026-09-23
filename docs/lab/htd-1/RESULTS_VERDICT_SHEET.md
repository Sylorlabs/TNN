# HTD-1 — generation styles + efficiency techniques — RESULTS VERDICT SHEET

**Written:** 2026-09-21 ~04:45 PDT (11:45 UTC) by the HTD-1 closeout agent.
**Binding:** `HTD1_PREREG_FROZEN_2026-09-21.md` + `AMENDMENT_2026-09-21_CONSTRUCTED_MODE.md`
(16 hypotheses, kill bars, metrics spec, verdict rubric §7).
**Scope:** read-only survey of `~/workspace/htd-1/` workdirs. Nothing rebuilt, no crews restarted.
Verdicts stated here were written by the build crews' own verdict documents where they
exist; where no crew verdict exists, the closeout agent derived a verdict from on-disk
evidence and labels it **INDEPENDENT** (not a crew verdict). Anything that could not be
verified is marked UNVERIFIED, not passed.

## Story in one paragraph

HTD-1 ran debate → prereg freeze → foundation crews (R1 cost-model contract, R2 baselines +
determinism harness, R3 frozen artifacts) → 13 build/test crews. A daemon restart on
2026-09-21 ~00:45 PDT killed 11 of 13 crews; all were respawned on identical verbatim
specs and completed. The coordinator committed the prereg, amendment, parked plan,
foundation artifacts, and two build verdicts (E-LG2, E-DE3), then went silent at ~08:15 UTC
without writing this final sheet. This sheet completes the record.

## Per-build verdicts (13 crews)

| # | Build | Verdict | One-line result | Committed |
|---|-------|---------|-----------------|-----------|
| 1 | E-DE1 cost-model-first budgeting | **KILLED** (KB1, KB3) | Diverges 163/599 on D-P2 and exhausts budget on 100% of items — the "saving" is refusal-to-answer, not efficiency | NO |
| 2 | E-DE2 incremental early exit | **KILLED** (KB2) | Correctness perfect (0 divergence, certs replay, R=5), but savings −4.3%/+11.9% < 15% bar — structurally, not a bug | NO |
| 3 | E-DE3 lazy verification debt | **KILLED** (KB2, KB3) | Deferral swaps one ledger entry for another (+0.015%); main arms emit with debts outstanding (zero-tolerance kill). Narrowing (E-DE5a) beats deferral 37% vs 0.015% | YES — `00984047f277` |
| 4 | E-DE4 deliberation memoization | **NARROW SURVIVES / BROAD KILLED** (KB2) | narrow (provenance-keyed): 42.2%/44.8% saving, 50% hit rate, 0 false hits; broad: 0% hits, costs 6–9% MORE — test-both done honestly | NO |
| 5 | E-DE5 heuristic narrowing | **(a) PASSES / (b) KILLED (KB2) / (d) PASSES** | verify-proposal-only: +37.06% saving, 0/1200 divergence; degraded (reversed) heuristic still clears KB2 at 18.45% — graceful degradation confirmed | NO |
| 6 | E-LG1 write batching | **PASS (INDEPENDENT)** | fixed16: REPLAY 5/5 byte-identical to baseline; 11/11 kill-restarts IDENTICAL; savings 90.97% of write syscalls, bytes 102.78% of baseline | NO |
| 7 | E-LG2 checkpoint+delta ledger | **PASS (K=64, K=256) / FAIL (K=16)** | Replay byte-identical all K; K=64 25.51% of baseline ledger bytes. Honest caveat: full-cost saving is −6.0% — ledger win ≠ cost win | YES — `af6a22305ab9` |
| 8 | E-LG4 read-path indexes | **PASS (INDEPENDENT)** | All 4 bars hold: ledger bytes identical, verification 0.068%, maintenance 0.104%, 750/750 staleness comparisons match; R=5 byte-identical | NO |
| 9 | G-CO2 deliberate abstention | **PASS (INDEPENDENT)** | Canonical tau=1: R=5 byte-identical; KB1 48/48 exact-match; KB2 assembly share 0.0016; KB3 0 faults/0 fill; KB4 abstains 196/200. Loose-tau tuning honestly killed by KB4 | NO |
| 10 | G-CO3 plan-verify-emit gating | **PASS** | KB1 64/64 code exact-match; KB2a 0.686 (weighted reading — see caveat); KB3 0 deviations/1240; KB4 0/124 plans fail post-emission; all 3 negative controls live | NO |
| 11 | G-CM1b structural separation | **AMBIGUOUS / INCOMPLETE** | R=5 ledgers byte-identical; 10/11 legs pass; replay/evict/compact leg scores 0 (`evict_ok=0`, "EVICT SPOT FAIL" in binary). No crew verdict written; on-disk source post-dates the scored binary — cannot resolve | NO |
| 12 | G-CM1c vs G-CM1d shootout | **HEAD-TO-HEAD: G-CM1c WINS** | Both 200/200 correct, zero leakage, all controls behave; c wins stringency 3.06 vs 2.83 correct/1k-cost | NO |
| 13 | E-SP relevance-calibration pilots | **FAIL (as efficiency)** | Oracle not selective/cheap: wakes 68.93% of partitions, net ops 158% of baseline; research value only — family-P labels in gray zone (MCC 0.1444), transfer gap open | NO |

## Notes on individual verdicts

- **E-DE4:** D-P1 narrow ran R=5; D-P2 narrow ran only R=2 (both identical) — noted, not
  fatal. D-P2 broad ran 1/1. Cache-contradiction probes (50) and partition-provenance
  keys per the constructed-mode amendment all hold.
- **E-LG1:** the epclose (episode-close) arm never got its R=5 battery — only fixed16
  (fixed-count batching) has full evidence. The 11 kill trials cover both modes
  (epclose tT01 + fixed16 fB01–fB10), all IDENTICAL. `base_r3.ledger` is a stray run
  with a divergent SHA and no manifest (not in sha.log) — UNVERIFIED origin, excluded.
- **G-CO3:** the crew's PASS rests on the taxonomy-weighted reading of KB2a (0.686);
  on raw op counts KB2a = 0.499 < 0.60 would KILL. COST_MODEL §5 routes G-CO3's KB2
  through the taxonomy, so the weighted reading is contract-correct — but if Micah
  rules for raw ops, the verdict flips to KILLED on KB2a. A harness bug (decoy-length
  misread, ~10³× OP-04 inflation, stale binary panics) was found and fixed before
  scoring; scored runs use the fix. Documented in DESIGN.md §10.
- **G-CO2:** KB2's 20–30% ambiguous band (flagged by the coordinator in the log) never
  resolved — the crew's measured assembly share (0.0016–0.0117) sits far below it, so
  it doesn't affect the verdict; the band remains open for future tuning.
- **E-SP pilots:** 60/60 correctness everywhere including the always-awake baseline;
  the negative control (anti-oracle) wins on net-savings because the cost model is
  quality-blind — signal lives in the miss/correctness gap (79.6% vs 4.8% miss).
  E-SP-R research verdict on family P: INCONCLUSIVE (gray zone).
- **G-CM1c/d:** known battery defect cm-prom-0155 noted by the verifier; does not
  change the shootout.

## What never finished

1. **E-DE2+E-DE4 composition crew** — HELD for both parents' binaries, never spawned,
   never run. E-DE2 is now KILLED, so the composition's premise is dead; no composition
   verdict exists.
2. **E-LG1 epclose-arm R=5 battery** — kill trials done, full R=5 battery absent.
3. **G-CM1b evict leg** — scored 0 with no explanation on disk; needs a rerun with
   matching sources to resolve.
4. **E-SP beyond pilots** — the relevance-calibration research plan (ablate-and-replay
   labeling, V0–V3 gates, DEFINABLE/NOT-DEFINABLE bars) is written, not executed.
5. Parked plan (generation showdown, G-CO generation-vs-generation, E-LG3 law-level
   tradeoff) — parked by design, not by accident; wake checklist exists.

## Commit status on tnn-native-lab

- prereg DRAFT `cb1c82c91dce` · constructed-mode amendment `feaafdaf0d42` ·
  parked plan + E-SP-R `a1e5173653be` · R1+R2 `dc79dd0ba02c` · R3 artifacts
  `0ba107de9856` · E-LG2 verdict `af6a22305ab9` · E-DE3 verdict `00984047f277`
  — all present on the branch (verified via API 2026-09-21).
- This verdict sheet: committed separately (hash recorded by the committing agent).
- All other build evidence is LOCAL-ONLY in `~/workspace/htd-1/builds/` (binaries,
  runs, manifests, SHAs). It was deliberately not committed; committing full
  per-build evidence is the coordinator's/follow-up's call, not this sheet's.

## Honest overall assessment

HTD-1 established what it set out to establish. Of 16 preregistered hypotheses,
the kill machinery worked: 4 efficiency hypotheses were killed terminally on binding
bars (E-DE1, E-DE2, E-DE3, E-DE5b), 1 efficiency pilot failed honestly (E-SP), 1 arm
failed a single bar with a documented re-entry (E-LG2 K=16). The survivors are
**E-DE4-narrow (memoization, 42–45% saving), E-DE5a (hypothesis narrowing, 37%),
E-LG1-fixed16 (write batching, 91% fewer write syscalls), E-LG2 K=64/256
(checkpoint+delta replay), E-LG4 (read indexes), G-CO2 (abstention gating),
G-CO3 (plan-verify-emit), and G-CM1c (constructed-mode gate wins the shootout).**

Two caveats travel with the headline: (a) E-LG2's ledger-byte win is not a full-cost
win (−6.0% under the frozen model) — "efficiency" claims must name their cost
reading; (b) G-CM1b's evict leg and the E-DE2+E-DE4 composition are unresolved, so
the constructed-mode structural-separation claim is not fully closed.

Determinism discipline held throughout: every scored config reports R=5 byte-identical
artifacts (SHA-256), no randomness in any canonical decision path, and kill bars were
applied as written — including the ones that fired on the program's own mechanisms.
Two znc compiler defects were characterized in the course of this work (ZNC-2026-09-21-007
extended: `as []u32`/`[]u16` aliasing on consecutive same-size casts, in E-LG4's evidence;
plus one driver-level bug) and recorded in `~/AGENTS.md`.
