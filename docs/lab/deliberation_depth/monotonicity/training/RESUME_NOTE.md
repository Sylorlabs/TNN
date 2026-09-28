# RESUME_NOTE — H5 training crew (H-0), 2026-09-24

## Completion record (2026-09-24 ~20:00 PDT, 2nd-resume coordinator)

All prereg gates executed; program complete. Verdict: **H FALSIFIED AT
TRAINING LEVEL** (VERDICT.md).

**Checklist disposition (§8):**
1. Feature extraction ×2 → byte-identical: PASS (12/12 family-runs,
   5240 cells; run_feat.sh + run_feat.log).
2. Training ×2 → byte-identical params: PASS (10× and 100×; mt_params_10x/
   mt_params_100x.zag + log_10x/log_100x.tsv).
3. Policy binary ×2 → byte-identical: PASS (policy_bin_10x_a/b,
   policy_bin_100x_a/b; built from frozen params + trivial mt_gate.zag).
4. Every (battery, policy, depth) leg ×2 → byte-identical: PASS (37/37 legs
   for MT-CONF-100x, mech 11; eval_100x.log).
5. Release-identity vs M4: PASS — 5240/5240 identical cells.
6. Baselines re-analyzed with same analyzer: done (M4: 1→0=0, V1=0,
   V2=160, Gviol=14).

**Decisive numbers:** 100× → w=init exactly, b=−99928 → conf=0 on all
4,467 released eval cells (mean 0.000 < 0.05 → DEGENERATE). Loss plateaued
(35M/95M, 0% move over final 30 epochs) with 2 G-violations/epoch persisting
on training cells through epoch 599 → §3 training-level falsification.
Theater term fired 0/600 epochs. Eval: 1→0=0, V1=0, V2=0, Gviol=2 (redteam).

**Root causes found (both documented in VERDICT.md):**
(a) train.zag feature off-by-one — feats[k] read field (8+k), training on
(f2..f8, 0) not (f1..f8); the ×4 theater penalty compared depth-fractions
and never fired (chain itself verified working via scratch/chainprobe.zag).
(b) Frozen §5 design is a one-way ratchet: upward calibration steps are
arithmetically impossible (|numerator| < DIV=4000000 always for correct
cells), every surviving term pushes confidence down; fixed point conf=0.
Fixing (a) would not save v1 — the destination is structural.

**Readings:** strict → FALSIFIED (2 eval G-violations); refined
(kill-only-if-G-crosses-0) → no refined-violation but DEGENERATE → H not
supported either way. 10× head (b=−10288) identically degenerate; its eval
skipped as redundant (conf=0 ∀ cells ⇒ same metrics as 100×).
**§6 MT-FULL:** not run — gate trainer was never built and its premise (a
functional conf head) failed; recorded as blocked in VERDICT.md.
**Mirror (§7):** release-identity 100% ⇒ P/O mirror's accuracy-bar corollary
untouched; the §3 headline prediction ("no admissible mechanism meets all
SHIP gates") SURVIVES.

**Committed** to tnn-native-lab branch under
docs/lab/deliberation_depth/monotonicity/training/ (binaries and
.zag-cache excluded per workspace rule; _B.tsv duplicates excluded, _A +
eval log kept).

---

## 2nd inheritance record (2026-09-24 ~11:55 PDT, coordinator 2nd resume)

Verified before trusting:

- **Binaries**: `src/feat_bin_a`/`_b` both md5 09e69f7f3038be450ff86ebd56f94a18
  (153,723 B each); `src/train_bin_a`/`_b` both md5 7cb8574b2a283edc344fbda0c2502299
  (170,497 B each). A/B byte-identical — determinism gate 3 (policy builds)
  / gate 1 pre-step hold.
- **Division probe**: `scratch/divprobe` output `0 0 -1 -1 -1 -1` → native
  i64 `/` truncates toward zero exactly like `tr_tdiv` on negatives
  (train's `tr_tdiv` ≡ policy's `pl_conf` native `acc/1000`). No conf mismatch.
- **items/**: ceiling split by `scratch/split_ceil.py` — 20 items each
  P/D/O × even/odd (rep from id tail `H5B-*-NN-RR`; even=RR%2==0), matching
  the prereg Phase B/C even-train / odd-heldout assignment.
- **scratch/**: `.zag-cache` + `.zagd.semantic-ready` present (build artifacts
  of the predecessor's compiles); `divprobe`, `divprobe.zag`, `split_ceil.py`
  all present and valid. No corrupt partials.
- **Sources read**: feat.zag (usage: `feat <items.jsonl> <family> <heldout01>
  <out.tsv> <d1> [d2 ...]`, emits exactly the §4 columns), train.zag
  (usage: `train <features.tsv> <passes> <params_out.zag> <log_out.tsv>`;
  note: `passes` = total passes, 1 pass = 6 epochs, so 10× = passes 10 =
  60 epochs, 100× = passes 100 = 600 epochs; phases A={admit,revoke,logic,
  cost} B={P,D} C={trap,O,redteam}, heldout→ph=-1), policy.zag
  (usage: `policy <items.jsonl> <depth> <gate01> <results.tsv>`; TSV columns
  identical to mech.zag as §9d requires; `mt_gate.zag` trivial pass-through
  = M4 behavior for MT-CONF).
- **writer flags**: `dlb_write_file` uses O_WRONLY|O_CREAT|O_TRUNC — the
  AGENTS.md O_EXCL gotcha does NOT apply; overwrites are safe.
- **Correction to previous checklist**: "12 runs" = 9 training family-runs
  (admit,revoke,logic,cost,trap,redteam @ 1,2,4,8,16; P/D/O-even @
  1,2,4,8,16,32,64) + 3 heldout family-runs (P/D/O-odd @ 7 depths).
  Expected: 4820 training + 420 heldout = 5240 cells < 8192 cap.
- **Baseline**: `mechanisms/run_matrix.sh` matrix confirmed:
  6 batteries × 5 depths (admit/revoke/logic/trap/cost/redteam) + ceiling ×
  7 depths = 37 legs per mech. `analyze.py` keys result files
  `${battery}_m${mech}_d${depth}_A.tsv`; mech ids 10/11/12 planned for
  MT-CONF-10x / MT-CONF-100x / MT-FULL; release-identity vs M4 (=4) is
  computed automatically.
- **Timing**: one feat leg (admit, 1240 cells) = 42 s → full extraction
  ~3 min/pass, ~6 min for A+B. Extraction script
  `training/work/run_feat.sh` launched in background (~11:56 PDT).

---

## Inherited state (verified 2026-09-24 ~11:40 PDT)

Coordinator's daemon died before ANY training or measurement ran under
PREREG_TRAINING.md v1 (frozen; status line still reads "no training or
measurement under this prereg yet" — true as of this note).

**Files inherited and their integrity:**

1. `training/PREREG_TRAINING.md` (v1, frozen) — read in full; checklist
   extracted from it (§§1–9). This note records the extraction below.
2. `training/src/` — 22 .zag files:
   - `feat.zag` (203 ln), `train.zag` (377 ln), `policy.zag` (232 ln):
     H5-specific, written by the previous crew. Review of the source:
     - feat.zag emits exactly the prereg §4 columns
       (id, family, heldout, depth, t, rel4, correct4, f1..f8) at the
       requested depths; M4-skeleton release (L_t==L_1) + correctness.
     - train.zag implements the §5 curriculum verbatim: online
       per-cell updates with the calibration + 2×[Y=0] + 4×theater
       terms, DIV=4000000, `tr_tdiv` truncation-toward-zero, phase
       order A→B→C, 2 epochs/phase/pass, G-batch bias correction
       (b ← b − ΔG/4 per training family/adjacent depth).
     - One thing to verify by probe, not by reading: znc native i64 `/`
       must match `tr_tdiv` for negative dividends (train uses tr_tdiv,
       policy.zag `pl_conf` uses native `acc/1000`). Planned probe below.
     - policy.zag: M4-skeleton release + trained head + optional gate,
       TSV columns identical to mech.zag. `mt_gate.zag` trivial pass
       (gc=1000000) is correct for MT-CONF.
   - `mt_params.zag` — PLACEHOLDER (init weights), correctly not built.
   - `mt_gate.zag` — trivial pass-through gate (v=0, c=1000000), for MT-CONF.
   - `bisect{,0..3}.zag` — scratch copies of feat.zag (bisect scaffolds,
     unused by the program). `probe2.zag`/`probe3.zag` — struct-copy probes,
     unused. Left in place; not part of the build.
   - `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` — SHA256-IDENTICAL
     to `mechanisms/src/` copies.
   - `dlb_util/dlb_json/dlb_cfg/dlb_ledger/dlb_delib.zag` — all
     SHA256-IDENTICAL to the frozen harness copies in `mechanisms/src/`
     (satisfies §9b "copied byte-identical, SHA256-verified").
3. `training/analyze.py` (141 ln, frozen analyzer) — computes per
   (mech,battery,family): 1→0, A→0, V1, V2, G(d) curves, G-violations,
   accuracy, release rates, released-only accuracy, release-identity vs
   M4 (reference mech 4, read from mechanisms/results/).
4. `HYPOTHESIS_BACKLOG_TRAINING.md` — H-0 reference entry (§44): kill bar =
   any L-OVERCONF violation (G(d+1)>G(d) or ≥1 V1/V2) on any battery after
   the developmental curriculum. Wave-2 crew owns T-01..T-27 separately.
5. `training/t01/` — NOT this crew's state: belongs to the wave-2 T-01 crew
   (cloned-prompt mirror-bind experiment). Touched by nobody here; left
   alone. NOT part of the H-0 program.

**No partial/corrupt artifacts:** no features.tsv, no params, no training
logs, no policy results exist. Compile of feat.zag in progress at note
time (background). Binaries `feat_bin_a` etc. not yet produced.

**Battery sources (to be used, from mechanisms/run_matrix.sh):**
items_v2/{admit:248, revoke:113, logic:264, trap:127, cost:125}.jsonl;
ceiling/items/ceiling_battery.jsonl (120: 20 each P/D/O × even/odd);
monotonicity/redteam/redteam_battery.jsonl (3). M0–M7 frozen TSVs in
mechanisms/results/ (reference for release-identity).

## Extracted checklist (from PREREG_TRAINING.md — not from this note)

- §8 gates: (1) feature extraction ×2 byte-identical; (2) training ×2
  byte-identical params; (3) policy binary built ×2 byte-identical;
  (4) every (battery, policy, depth) leg ×2 A/B byte-identical;
  (5) release-identity: MT-CONF release+correct agree with M4 100% of cells;
  (6) baselines re-analyzed with the same analyzer (frozen TSVs, no re-run).
- Curriculum: 1× = 6 epochs (2/phase A→B→C); 10× = 60 epochs → MT-CONF-10x;
  100× = 600 epochs → MT-CONF-100x. Eval on the SAME matrix as M0–M7.
- H SUPPORTED: 0 transitions + zero V1/V2 + zero G(d+1)>G(d) on every
  battery/family at 100× (strict reading; refined reading reported too).
  H FALSIFIED: ≥1 V1/V2 or ≥1 G-rise. PARTIAL: frontier moved only.
  Degeneracy guard: mean released conf < 0.05 → DEGENERATE, no support.
- §6 secondary: trained abstention gate → MT-FULL (60 epochs gate-only +
  60 joint at DIV=8000000); secondary claim = moves SHIP-(v) frontier on
  trap/redteam without breaking §1 or L-OVERCONF.
- §7 mirror confrontation: release decisions are M4's by construction →
  theorem's accuracy-bar corollary untouched; the break (if any) is the §3
  headline prediction that no admissible mechanism meets all SHIP gates.
- Hard requirements: gate/remove the sole-survivor conf=1000 pin (Crew B
  pin criterion); prevent M4's failure mode (conf inflating with depth on
  wrong answers = V2 theater). Record strict vs refined L-OVERCONF reading
  per result.

## Execution plan (order)

1. Build feat/train/policy binaries ×2, byte-compare (gates 3/partial-1).
2. Probe native i64 `/` vs tr_tdiv on negatives (train/eval conf match).
3. Split ceiling battery → P/D/O × even/odd files (even=train, odd=heldout).
4. Feature extraction: 12 runs ×2 (gate 1) → concat features.tsv (4820
   training + 420 heldout cells, under the 8192 cap).
5. Train 10× (60 epochs) ×2 → mt_params_10x.zag + log (gate 2);
   sanity-check: final ≠ init, mean conf on released cells, loss plateau.
6. Build MT-CONF-10x policy binary ×2 → eval matrix (37 battery×depth legs
   ×2 A/B) → analyze.py → release-identity vs M4.
7. If 10× shows no pathologies: train 100× (600 epochs) ×2 → freeze
   MT-CONF-100x → full eval + analysis → H verdict.
8. §6 secondary: gate training → MT-FULL → eval.
9. Mirror-theorem confrontation statement; commit all to tnn-native-lab
   under deliberation_depth/monotonicity/training/.
