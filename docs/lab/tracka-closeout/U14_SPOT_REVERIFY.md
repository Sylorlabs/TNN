# U14 — Spot Re-verification of PASS Verdicts (independent re-runs)

**Crew:** MARATHON CREW U14 (re-dispatch; first dispatch errored on infra before any work).
**Date:** 2026-09-21.
**Frozen prereg:** `units/PREREG_FREEZE.md`, commit `b0b9140c0eda`, branch `tnn-native-lab`.
§3 rows extracted programmatically (52 arms; "53 arms ratified" footer is an arithmetic
error, per TRACKA_VERDICT_SHEET.md §1). No spec text from memory.
**Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (frozen lab znc).
All sources compiled clean (warnings only); znc quirks in ~/AGENTS.md respected.
No new Zag code was written — only harness shell scripts.

## 1. Sampling rationale

21 PASS arms on the roster; sampled 4 spanning mechanisms, verdict types, and
§7 roles:

| Arm | Verdict type / mechanism | Why sampled |
|-----|--------------------------|-------------|
| **Y5** | STRUCT — §7 blowout champion (7/8 decided columns) | Required by brief; the tokenizer-replacement headline rests on it |
| **U** | STORE — newest PASS (adjudicated 2026-09-21, moved §7) | Required by brief; binding PASS rests on the duel crossover, not on a battery ceiling |
| **L1** | IDENT — the only non-Y5 §7 column holder (M5 cost champion) | Different mechanism family; verdict rests on a constructional promise (position-ID eternity), not a ceiling metric |
| **Z8** | CUT — boundary arm | Kill evaluated on a perturbation battery + revision fuzz trajectory; freshest boundary-type PASS |

Load-bearing legs re-run per arm (the ones its verdict rests on): the kill
clauses, M1 ceiling (where a §7 column depends on it), M4 (revision), M5 (cost),
and the M8 determinism gate — all under the official double-run rule (2 fresh
runs, stdout byte-identical), binaries rebuilt from committed sources (no crew
binaries reused).

## 2. Source provenance (verified, not assumed)

Blobs fetched from `sylorlabs/TNN` via gh-api at each arm's committed verdict
commit; all three committed sources byte-identical to the working tree:

| Arm | Committed source blob | At commit | Worktree match |
|-----|----------------------|-----------|----------------|
| Y5 | `057792f6d6f6691c0be0533ca4e115535245bf28` | `0f07518d0937` | YES (byte-identical) |
| U | `c5ffdc1e788b0d7ede6a20b76dc7d3f7301e8533` | `9c6d9384ef9973fcc96e4e857145c74d72c27769` | YES (byte-identical) |
| L1 | `720209f1198b4b77820f68457dd41c45fb334711` | `ac6c1442b39f522ef27bb6b7d26b0edd72594953` | YES (byte-identical) |
| Z8 | *(never committed)* | `0587e778fcb2` (verdict only) | n/a |

**Z8 provenance caveat (documented, not hidden):** `cl/arm.zag` was never
committed (commit `0587e778fcb2` carries only VERDICT.md + evidence; "battery
binary build-only, never committed"). The re-verification built the working-tree
`cl/arm.zag` (1,643 lines — matches the VERDICT.md description; `git log` on both
repo paths returns zero commits for it). Zero RNG/clock hits in the source
(`grep -c rand/lcg/getrandom/clock()` = 0); compiled clean first try. This is the
only arm whose PASS verdict rests on a source that cannot be independently
re-fetched from the branch. Flagged for the record; the numbers below are from a
clean rebuild of exactly that source.

Corpora: Y5, U, L1 used `units/arms/harness/corpora/r1` (prose.bin 5,422,721 B,
SHA-256 `a023115c2d4e2ee12221bdd780fdf2ac5a864fe225948656f51f8be462c7fffb` — the
frozen r1 prose corpus; code.bin 9,515,341 B, SHA-256
`b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189`). Z8 used
`tnn-lab/corpora/r1` per its own `evidence/r1/BATTERY_LOG.txt` (`CROOT:
tnn-lab/corpora/r1/`). Note: `tnn-lab/corpora/r1/prose.bin` (5,638,480 B) is a
*different* file from the frozen r1 prose corpus. Y5's crew used the frozen one.
U14 initially ran Y5/L1 against the wrong corpus root, caught it by unit-count
mismatch (Y5 prose 18,568 vs committed 17,867 units), and re-ran everything
against the correct root before recording results. U's duel was killed before
producing numbers and re-run correctly from scratch.

## 3. Per-arm results

### Y5 — STANDS

- Rebuilt: `znc: wrote native binary y5_u14` (233,333 bytes main), warnings only.
- `m4-1x-code` ×2: rc=0/0, stdout byte-identical.
  `M4,m4-1x-code,100.0,100.0,0.0,0,0.0,0` — rev_boundary 100.0, rev_content 100.0,
  kill 0.0, ksub 0, **link degradation 0.0%** (frozen kill bar: >20% fires),
  **atomicity violations 0** (bar: any). Kill does NOT fire. Matches VERDICT.md.
- `m1-1x-prose` ×2: `M1,prose.bin,100.0,100.0,17867,1575,PASS` — 17,867 units,
  exact match to `evidence/scorecard_y5_1x.json` (prose units 17,867).
- `m1-1x-code` ×2: `M1,code.bin,100.0,100.0,32930,2048,PASS` — exact unit-count
  match (32,930).
- M8 gate (`harness/m8_gate.sh`, 5 perturbations × 2 reruns): all rc=0,
  **M8GATE PASS**.
- §7 blowout inputs re-confirmed at 1x: M1-content 100.0, M1-boundary 100.0,
  M8 PASS. (M2/M3/M6-tax/M7 columns were not re-run — no mechanism for drift
  was identified and the load-bearing kill legs plus M1 are reproduced; M5
  prose-only harmonized 1.659 stands from M5-HARMONIZE, not re-measured here.)

**Verdict: PASS — STANDS.**

### U — STANDS

- Rebuilt: `znc: wrote native binary u_u14` (236,105 bytes main) — exactly the
  byte size ADJUDICATION.md records for the crew's post-fix binary
  ("236,105 bytes main — identical size to the crew's post-fix binary").
- `duel-1x` ×2: rc=0/0, stdout byte-identical. Fragment:
  `duel_crossover_E=-1, duel_kill_i_fires=0, duel_kill_ii_fires=0,
  duel_cpu_u_total=14182612, duel_cpu_d_total=279875710,
  duel_cost_u_at_100=1727480888, duel_cost_d_at_100=2219096277,
  duel_byte_mismatches=0` — **every number exactly matches the adjudicated
  evidence** (ADJUDICATION.md §3: cpu_u = 14,182,612, cpu_d = 279,875,710,
  total_u(100) = 1,727,480,888, total_d(100) = 2,219,096,277).
  - Kill (i): cpu_u/cpu_d = **0.0507×** (frozen bar: >10× AND B4<10% fires).
    Does NOT fire.
  - Kill (ii): U wins at 100 edits by 22.1%. Does NOT fire.
  - Kill (iii): determinism — see M8.
- M8 gate: **M8GATE PASS** (5 perturbations × 2 reruns, all rc=0).
- Radius note: the duel ran at the binary's default radius (R=64 configuration).
  The adjudication already swept R ∈ {32,64,128,256} with a bounding argument
  for R≥512; this re-verification confirms the default-configuration result,
  which is the load-bearing one (kill_i 0, kill_ii 0 at all four swept radii).

**Verdict: PASS (binding) — STANDS.**

### L1 — STANDS

- Rebuilt clean with the frozen znc.
- `m4-1x-prose` ×2: `M4,m4-1x-prose,100.0,100.0,0.0,0,eternal=0,frag_segs=7`;
  `m4-1x-code` ×2: `...,eternal=0,frag_segs=11`. Frozen kill (ii): "any revision
  batch changes an existing position ID — dies outright." **eternal=0 both
  corpora — zero eternity violations; kill does NOT fire.** frag_segs 7/11
  match VERDICT.md exactly. Kill (i) and (iii) remain UNEVALUABLE as frozen
  (K1 cost and corpus C unavailable), as the verdict itself states.
- `m5-1x` ×2: `m5_units_learned=233409, m5_source_bytes_learned=14938062,
  m5_slot_table_bytes=12531232, m5_ledger_bytes=14939200` —
  **all four numbers exactly match** `scorecard_r1_1x.json` →
  12,531,232/14,938,062 = **0.839 B/B ≤ 1.5 bar**. (rss_delta = 0 in the
  committed scorecard, same reading.)
- M8 gate: **M8GATE PASS**.

**Verdict: PASS — STANDS.**

### Z8 — STANDS (with the §2 provenance caveat)

- Rebuilt from the working-tree source (never committed — see §2), clean.
- `z8-perturb` ×2: rc=0/0, byte-identical;
  `err_rate_tenths=50.0` (1,280/2,560 errors each boundary) at fuzz=16.
- `z8-perturb-d` ×2: rc=0/0, byte-identical;
  `err_rate_tenths=100.0` (2,560/2,560) at fuzz=0 (the D-surrogate).
  → **50.0% boundary-error reduction ≥ 40% bar.** Frozen kill clause 1 does
  NOT fire. Matches KILL_EVALUATION.md exactly.
- `m4-1x-prose`/`m4-1x-code` ×2: `m4_fuzz_traj_tenths=[160,148,135,121,104,89,
  74,57,41,26,9,4,1,0,0,0,0,0,0,0,0]`, `m4_fuzz_bounded=true` — **exactly the
  series in VERDICT.md**, converging to 0.0; revision correctness 100.0/100.0.
  Frozen kill clause 2 does NOT fire.
- M8 gate: **M8GATE PASS**.

**Verdict: PASS — STANDS.**

## 4. Summary

| Arm | Load-bearing legs re-run | Key numbers vs frozen bars | M8 | Verdict |
|-----|--------------------------|----------------------------|----|---------|
| Y5 | m4-1x-code ×2, m1 ×2 (prose/code) | deg 0.0% (bar >20%), atomicity 0 (bar any), M1 100.0/100.0 both | PASS | **STANDS** |
| U | duel-1x ×2 (full E=0..1000) | cpu 0.051× (bar >10×), U wins @100 by 22.1%, crossover none, 0 mismatches — all numbers exactly match adjudicated evidence | PASS | **STANDS** |
| L1 | m4 ×2, m5-1x ×2, m5-baseline ×2 | eternity violations 0 (bar: any), M5 0.839 B/B (bar ≤1.5) — scorecard numbers exactly reproduced | PASS | **STANDS** |
| Z8 | z8-perturb/perturb-d ×2, m4 ×2 | 50.0% reduction (bar ≥40%), fuzz → 0.0 bounded — series exactly matches | PASS | **STANDS** |

**No REVERIFY-FAILED arms. All four PASS verdicts STAND on independent
re-verification.** No verdict is overturned, none is altered; nothing is
recommended for adjudication.

## 5. Open items / caveats (do not affect verdicts)

1. Z8's `cl/arm.zag` was never committed — its PASS verdict's source
   provenance is the working tree only (documented §2; recommend committing
   the source on a future pass).
2. Two corpus roots exist on disk (`tnn-lab/corpora/r1` vs
   `units/arms/harness/corpora/r1`); the latter holds the frozen r1 prose
   corpus (5,422,721 B, SHA-256 `a023115c…`). Each arm's CROOT was taken from
   its own evidence; Y5/L1 re-runs against the wrong root were caught by
   unit-count mismatch and redone.
3. Y5's M2/M3/M6-tax/M7 columns were not re-run (kill legs + M1 + M8 were);
   they sit at ceiling from the committed battery with no identified drift
   mechanism.
4. U14's own working binaries and run artifacts live in
   `~/workspace/u14-work/` (workspace, not the branch); no binaries, no
   `.zag-cache`/`.zagd` are committed with this report.
