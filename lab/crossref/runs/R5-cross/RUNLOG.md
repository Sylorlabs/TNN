# R5-CROSS Run Log (Type C cross-check crew)

## 0. Environment

- Date: 2026-09-22/23 (UTC; user TZ PDT)
- Run dir: `~/workspace/scratch-crossref/R5/cross/`
- Scratch only; `TMPDIR=/home/hatch/workspace/tmp_commit`; no slice near 2^25 bytes.
- Toolchain: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (`znc 2026.07.0-dev (edition 2026)`), built locally from `r5cross.zag` — no copied
  binaries, no `.zagd`.

## 1. Fresh clone (required `clean-cross/`)

- First full clone (~61 min) failed: `unexpected disconnect`, `early EOF`,
  `invalid index-pack output`. Retries also disconnected/timed out.
- Background shallow clone `git clone --depth 1 <tnn-native-lab> clean-cross/`
  (session `proc_61f35afc1e59`) **completed**: HEAD `2f5e22aaa729a64a9300ef667d426c7b0d770944`
  ("rsi: ask-first+coherence COMBINED trial — verdict").
- Both evidence pins fetched by exact SHA (depth 1) and verified with `git cat-file -e`
  **before** official runs:
  - `66fbb329aa831c14f3f3100a20e177bbb12e27b1` → commit "KB4 autopsy — bad learning or bad architecture? (Micah's question)"
  - `bc6d130539e4a5539ea3361f57e02e39378f26ba` → commit "KB4 why-swarm report: …"
- Spot-check: blob `out_pa1_rep1.txt` at the autopsy pin, SHA-256
  `411fc737c7843fd06bd276ae70ab3fcd56bbf2ab6d10755151c01ef8bca164c0`,
  byte-identical to `evidence/probes/out_pa1_rep1.txt`.
- Frozen `SCOPE.md` / `PREREG_TIER1.md` (from `7b2100d…`) held separately in `doc-stage/`.

## 2. Evidence intake (2026-09-22/23, before official runs)

- All 37 blobs under `docs/lab/kb/autopsy/` at the autopsy pin downloaded via Git
  object APIs; Git blob SHA-1 recomputed independently for each — all matched.
- Original KB4 ledger under `cross/evidence/epistemic_wave/kb4_rerun/` likewise
  blob-SHA verified.
- Committed rep1/rep2/rep3 outputs: identical blob SHAs within each probe (determinism
  of the committed evidence itself confirmed).
- No R5-PRIMARY scratch/output was used or trusted at any point.

## 3. Independent verifier development (`r5cross.zag`, ~1,380 lines)

Pure-Zag reasoning/verification; Python used only as glue (file staging, SHA checks).
Zero RNG. Committed `R33_NATIVE_IO_V1.zag` used as the I/O substrate (byte-identical
copy of the pinned `docs/lab/kb/autopsy/probes/R33_NATIVE_IO_V1.zag`).

Development-run bugs found and fixed (none of the failing development runs were
accepted as evidence):

1. **R5-2 match/differ marginals reversed** — cell index odd = match (`pam=1`), even =
   differ; initial code had them swapped. Fixed; expected cells confirmed:
   A match 47/33, differ 44/60; B match 52/41, differ 32/60.
2. **MI denominator bug** — the (match, adv-wrong) term used `cg0*cy1`; correct is
   `cg1*cy0`. Caught by unit-testing `log2_1e6` in isolation (exact: log2(2)=1e6).
   Final: A 19265 µbits (0.019265), B 32740 µbits (0.032740).
3. **F5 semantics inverted** — L4-removal must leave zero M3 *withholds* (adv-correct &
   differ & not installed), not zero installs. Fixed; both legs withhold 0.
4. **P3 demoted to informational** — the full-observation simplex admits a memorizing
   policy on the frozen set, so P3 cannot carry the impossibility claim. The
   impossibility (W5/autopsy-S6) is over the gate's operational observable (match-bit),
   verified exactly: maxTP@≤15% = 0/420 (A), 0/541 (B); min-rate@TP≥50 = 28.4% (A),
   42.2% (B). Judgment-only algebra coefficients printed: A match 420 / differ 888,
   B match 541 / differ 924 — all positive, so ≤15% false-install rate forces zero
   installs (violates the ≥50 true-install bar).
5. Confidence means: nearest-tenth rounding (B wrong = 861.4, not 861.3).

Also added: deterministic enumeration semantics for the match/differ policy table
(π00/π01/π10/π11 accuracy + ceiling), and explicit LP-as-fractional-knapsack for the
oracle partition.

## 4. Official runs

- Build: `znc build r5cross.zag -o r5cross` (pinned toolchain, local build).
- `./r5cross evidence` → `run1.txt`, `run2.txt`, `run3.txt`.
- Result: **ALL CHECKS HOLD** on every run.
- SHA-256 of all three outputs: `6713f286a9518bad759728fa9fa0b05cb9ec8f1b2370a45b0536794c6e621922`;
  `cmp run1 run2`, `cmp run2 run3` clean — **byte-identical ×3**.

## 5. Cleanup

- Removed after the official runs: the `r5cross` binary, `.zag-cache/`,
  `.zagd.semantic-ready`, all `dbg*.zag`/debug binaries, `tlog.zag`/`tlog`.
- **Rule violation disclosed:** during development a temporary log-table file was
  written to `/tmp/logtbl.txt` (scratch-only rule). It has been deleted; no evidence,
  source, or result ever transited through it — it held only generated log2 table
  constants, and all subsequent work used workspace scratch.

## 6. Deliverables

- `VERDICT.md` — verdict NOT REPRODUCED (mechanical), all committed-vs-derived
  numbers, the three failing claims, attribution assessment, caveats, frozen pins.
- `RUNLOG.md` — this file.
- `r5cross.zag` — the independent verifier. `R33_NATIVE_IO_V1.zag` — I/O substrate.
- `run1.txt`/`run2.txt`/`run3.txt` — the three byte-identical official outputs.
- `evidence/` — SHA-verified committed evidence (probes, truth files, AUTOPSY.md,
  WHY_REPORT.md).

No binaries, caches, or `.zagd` files remain. No R5-PRIMARY material was used.
No live workstreams were touched.
