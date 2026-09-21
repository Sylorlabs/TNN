# B-T1 closeout addendum — independent reproduction (2026-09-21)

This addendum records the CLOSEOUT re-run of the B-TOURN-CLOSEOUT assignment
against frozen Track R0 (`PREREG_FREEZE.md` §2, R-1..R-9). The closeout rebuilt
the battery binary from the local source, re-fetched the corpora, re-ran the
battery, re-scored with the frozen probe, and re-ran every expected-value
readback probe. The closeout re-run is the evidence; the 2026-09-21 01:42
VERDICT_SHEET.md is treated as an unverified claim.

## 1. Reproduction status: DISCREPANT — measured numbers differ, bar FAILS

The closeout re-run reproduces the experimental setup (binary, corpora, probe)
but the measured tournament scores differ substantially from the numbers
claimed in VERDICT_SHEET.md (2026-09-21 01:42), and the binding bar FAILS.

| arm / corpus | claimed prose | measured prose (closeout) |
|---|---|---:|
| predictive_surprise / pg100 | 0.6843 | 0.9558 |
| fixed_window_4 / pg100 | 0.5995 | 0.8968 |

The full measured rank table is in `rank_table.json` (§3). Per the assignment's
do-not-tune rule, the measured numbers stand; the 01:42 sheet's numbers are not
reproduced and their provenance could not be established (no earlier scorer or
run outputs survive on disk; the current `bt1_score.py` postdates the sheet).

Evidence chain for the closeout numbers (all verified 2026-09-21):
- Binary: `units/r0/impl/arms/arms.zag` + the additive R-7 leg (diff vs the
  committed original: 26 lines, doc + `maxlen` parameter + `adaptive_mdl_8`
  selector; all ten original selectors pass maxlen=12 explicitly — see §4).
  Built with the pinned toolchain `znc_linux_x86_64_abed8aa1 --no-zagd
  --no-analyze --no-foreground-cache`.
- Regression: new binary vs the arms crew's saved smoke goldens
  (`smoke_out/o_*`, their binary from the committed pre-leg source):
  70/70 arm×input diffs byte-identical. The leg changed nothing for the ten
  original selectors.
- Corpora: re-fetched with `units/r0/impl/harness/fetch_corpora.sh`;
  sha256 matches the frozen manifest and the M-30 record exactly
  (pg100 `3cf4b3d4…`, sqlite3.c `b1dd5d74…`); hashes in `corpora.json`.
- Probe: the frozen `bt1_score.py` / `bt1_rank.py` in this directory, which
  implement `PROBE_MANIFEST.md` §3 verbatim (verified by line-by-line read).
- Determinism: every battery pair run twice, byte-identical SHA-256
  (RUN_MANIFEST.md); M8 gate (N=5 + 3 heap perturbations + `setarch -R`)
  PASS on all 11 selectors (`m8/M8_B-T1.log`); source canary clean.

## 2. Binding bar (closeout-measured): FAIL

Expected: `predictive_surprise > fixed_window_4 > raw_micro`, `raw_micro` DEAD LAST.

Measured:
- predictive_surprise (0.9190) > fixed_window_4 (0.8959) > raw_micro (0.7704): ORDER HOLDS
- raw_micro rank 7 of 10 (not dead last): DEAD-LAST FAILS

The fixed_window_8 (0.7410), fixed_window_16 (0.7103), and fixed_window_64
(0.4604) arms all score below raw_micro. `binding_verdict: FAIL`,
`dead_last_ok: false` in `rank_table.json`.

## 3. Measured rank table (tournament_score = mean of prose/code composites)

| rank | arm | tournament_score | prose | code |
|---:|---|---|---:|---:|
| 1 | predictive_surprise | 0.9190 | 0.9558 | 0.8823 |
| 2 | fixed_window_4 | 0.8959 | 0.8968 | 0.8950 |
| 3 | random_chunks (informational) | 0.8854 | 0.8812 | 0.8895 |
| 4 | hierarchical_mdl | 0.8473 | 0.8615 | 0.8330 |
| 5 | adaptive_mdl_8 | 0.8399 | 0.8481 | 0.8316 |
| 6 | adaptive_mdl | 0.8358 | 0.8459 | 0.8258 |
| 7 | raw_micro | 0.7704 | 0.7823 | 0.7586 |
| 8 | fixed_window_8 | 0.7410 | 0.6965 | 0.7854 |
| 9 | fixed_window_16 | 0.7103 | 0.7134 | 0.7071 |
| 10 | fixed_window_64 | 0.4604 | 0.1984 | 0.7223 |
| — | grounded_adaptive_mdl | CRASHED | — | — |

grounded_adaptive_mdl segfaults (SIGSEGV) on both corpora due to a heap
buffer overflow in the grounded MDL path (see GROUNDED_BUG.md). It cannot be
scored. The 01:42 sheet's claimed scores for this arm (0.5850/0.5799) are
unreproducible with the frozen binary.

## 4. Additive-leg diff summary (local arms.zag vs committed original)

Committed blob `32f02976a541da1302e7a97355311dbaa8079593` (34,443 bytes).
Local file: 34,989 bytes. 26 diff lines, all in `mdl_fit` / `arm_adaptive_mdl`
/ selector dispatch / help text:
1. `mdl_fit` gains a `maxlen:i32` parameter; `while(L<=12)` → `while(L<=maxlen)`.
2. `arm_adaptive_mdl` gains a `maxlen:i32` parameter, forwarded to `mdl_fit`.
3. Every original call site passes `12` explicitly (`adaptive_mdl`,
   `grounded_adaptive_mdl`, hierarchical MDL's direct `mdl_fit` call).
4. New selector `adaptive_mdl_8` calls the same ungrounded MDL path with `8`.
5. Documentation comments for the R-7 leg.
No other behavior changed. 70/70 regression vs arms-crew goldens: clean.

## 5. M8 determinism gate: PASS (m8/M8_B-T1.log)

N=5 reruns + 3 heap perturbations (perturb1/2/3) + `setarch -R`, byte-identical
required, all 11 selectors × 7 smoke inputs: 11/11 OK. Source canary: no
clock/entropy/pid/RNG in `arms.zag`; only `_zag_raw_syscall` sites are
syscall-0 stdin reads; `random_chunks` is the closed-form deterministic analog
(h = (Σ(j+3)·b[i+j] + 17·i) mod 7).

Note: M8 used only 0–14KB smoke inputs, so it did not catch the
grounded_adaptive_mdl heap overflow (crash threshold ~80–100KB).

## 6. Expected-value readbacks: PASS (logs/READBACK_CLOSEOUT.md)

Independent Python MDL reimplementation vs binary: 12/12 SEG-row comparisons
pass (6 inputs × maxlen {8,12}). Hand-computed FNV-1a ids (fixed_window_4,
raw_micro, random_chunks) match the binary. Hand-traced predictive_surprise cut
on "AB" (p=p18=82595524, cut at 1; ids 565918/236231) matches the binary.
`probe_stores.zag` (ZNC-2026-09-19-001 targeted): P1–P4 bad=0, STORE-PROBE PASS.

## 7. Commits

- Commit 1 (implementation + evidence): `0489675d58e436b6a432e241d0336d3a34ed43d7` — `docs/lab/units/r0/impl/arms/arms.zag`,
  `docs/lab/units/r0/evidence/tournament/b_t1/` (manifest, scripts, rank table,
  corpora hashes, M8 log, scorecards, readback logs, grounded bug report,
  this addendum).
- Commit 2 (closeout pointer): `<hash2>` — VERDICT_SHEET.md commit field filled
  with `0489675d58e436b6a432e241d0336d3a34ed43d7`.

## 8. Constraints compliance

1x only (both corpora < 2^25, single slice each). Pure Zag for the binary.
Zero RNG in AI decision paths. Byte-identical reruns (M8 + run-pair hashes).
No tuning — measured numbers reported as-is. No binaries/corpora/`.zagd`/
`.zag-cache`/`__pycache__` committed. Scratch under `~/workspace`, not `/tmp`.
