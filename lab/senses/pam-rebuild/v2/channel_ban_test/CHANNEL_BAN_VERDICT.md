# CHANNEL_BAN_VERDICT.md — PAMs v2 follow-up item 3
**Date:** 2026-09-23. **Prereg:** `PREREG_CHANNEL_BAN_TEST.md` (frozen,
committed ALONE, commit `3ffb4962d305463539086d271d1fb4359c4921d4`).
**Micah's ruling:** TEST FIRST — preregistered, tested, decided below.

## Verdict: ADOPT

**Adopted wording (exact, unchanged from the proposal):**

> Ban unregistered judgment-side acceptance channels for the frozen threat
> model; registered C1-class channels allowed with their own
> false-installation budget.

No wording change was forced by the data: the ban is unambiguous on
no-probe families (INSTALL iff a registered probe agrees ⇒ no probe means
no install), and no tested composition recovers truths beyond the ban
without violating the 0-false-install bar.

## What was tested

92-row frozen battery from KB4 measured evidence (sense-A TCP/DPI test
fixtures; 52 honest / 40 fooled judgments). Per row: measured C2 verdict
(DPI ⇒ constant INSTALL), measured C3 noise-agreement verdict, registered
C1-class probe availability (pitchdisc only — the autopsy's honest limit)
with measured analytic/judgment agreement. Gate variants in pure Zag
(`src/cbtest.zag`, zero RNG): **A** (ban: registered C1-class only),
**B-C2** / **B-C3** (unregistered judgment-side channel only), **C-OR2** /
**C-OR3** (both, OR), **C-AND2** / **C-AND3** (both, AND). 3× byte-identical
runs (sha256 `d6c2e5faa33aff6cad68dffc2ac6dbceb1af01ae845ecf14e5416e362188a75e`).

## Results

| variant | installs | false installs | true installs | truth accept. | KB1 |
|---|---|---|---|---|---|
| **A (ban)** | 7 | **0** | 7 | 7/52 (13.5%) | **PASS** |
| B-C2 (unregistered) | 92 | 40 | 52 | 52/52 | **FAIL** |
| B-C3 (unregistered) | 87 | 37 | 50 | 50/52 | **FAIL** |
| C-OR2 | 92 | 40 | 52 | 52/52 | **FAIL** |
| C-OR3 | 87 | 37 | 50 | 50/52 | **FAIL** |
| C-AND2 | 7 | 0 | 7 | 7/52 | PASS (= A) |
| C-AND3 | 7 | 0 | 7 | 7/52 | PASS (= A) |

Kill bars: KB1 (>0 false installs FAILS) — A passes, every variant using an
unregistered judgment-side channel fails (29–40 false installs). KB2 (3×
byte-identical) PASS. KB3 (evidence fidelity: all 92 rows + 21 contingency
tables independently recomputed from the evidence files) PASS. KB4 (zero
RNG) PASS.

Per-leg: on the probe family (pitchdisc, 15 rows) A installs 7/7 truths
with 0 false; B-C2/B-C3 install all 15 (8 false each). AND-compositions are
exactly A — they add nothing. OR-compositions are exactly their B arm —
they add no truths beyond B and inherit all of B's false installs.

## Channel information (bits, recomputed from Zag counts)

| channel | full battery | probe leg | no-probe leg |
|---|---|---|---|
| C1-class | 0.0661 | **0.9968** (reproduces published 0.9968) | 0.0000 (no probe) |
| C2-class | 0.0000 | 0.0000 | 0.0000 |
| C3-class | 0.0046 (≈ published 0.0049 pooled) | 0.0000 | 0.0069 |

## The ban's cost (measured, not hand-waved)

On the 77 no-probe-family rows (45 truths, 32 fools) the ban withholds all
45 truths. The counterfactuals: B-C2 recovers them at 32 false installs;
B-C3 recovers 43 at 29 false installs. **No variant recovers any of those
truths at 0 false installs.** The cost is real and is a *coverage debt*
(families without a registered probe install nothing) — which is exactly why
the v2 architecture must build per-family probes (autopsy honest limit #1),
not a reason to admit unregistered channels. Allowing the unregistered
channel alongside the registered one (C-OR) buys zero additional safe
truths and reintroduces 29–40 false installs.

## Decision-rule audit (prereg §7, applied mechanically)

- F(A)==0 ✓; no B/C variant achieves F==0 with truth acceptance > T(A) ✓
  (all unregistered-channel variants fail KB1); C-compositions add no truths
  beyond A without false installs ✓ (AND = A; OR = B, fails KB1).
- No REJECT condition met; no MODIFY forced. ⇒ **ADOPT**.

## Scope and limits (carried, not buried)

1. Frozen threat model only (one adversary construction δ≲σ band, frozen
   senses, KB4 tasks) — per G1, a new preregistered battery is required for
   any new construction, sense, or task family.
2. Sense A only (F3 legibility PASS; sense B voided on F3, excluded).
3. The 12 sealed novel families (manifest
   `c140013e76c520e3e04ca2f3d4283f56a3e8184cbac01d4e5509ff5fb4f56b9d`,
   288 fixtures + 288 truth sidecars) contributed metadata only — fixtures
   stay sealed; no judge reports or C1 probes exist at the channel level
   for them (prereg §8 rationale).
4. Implication for the v2 build: the ban's truth-acceptance ceiling equals
   probe coverage. Per-family registered probes, each with its own
   preregistered battery and false-installation budget, are the build's
   critical path.

## Evidence index (this commit)

- `src/cbtest.zag` — pure-Zag harness (mechanism).
- `src/extract_battery.py` — evidence→battery extraction (glue).
- `src/battery_strings.txt` — the 92-row battery as embedded.
- `src/score_cbtest.py` — cross-check + bits (glue).
- `src/BUILD_CBTEST.txt` — build/run recipe.
- `out/cbtest_run{1,2,3}.txt` — 3× byte-identical runs.
- `out/cbtest_scores.json`, `out/cbtest.sha256`.
- Binaries and `.zagd` never committed (binary ran from /tmp).
