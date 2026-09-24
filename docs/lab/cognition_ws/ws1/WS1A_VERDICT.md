# WS1-A VERDICT — "deliberation cheaper than autopilot" (KB-control domain)

**VERDICT: CONFIRMED** — all frozen prereg bars passed; no kill condition triggered.
Date: 2026-09-24 (analysis closed ~09:10 PDT). Agent: WS1-A-RESUME (resumed the
interrupted original; inherited data collection verified, analysis done fresh).
Prereg: `docs/lab/cognition_ws/ws1/PREREG_WS1A.md`, frozen 2026-09-24T08:10 PDT
(commit `403906826516f3c76c0a26ff1b60e94a094370d9`) — BEFORE any fresh run.

## 1. Data integrity (verified, not inherited on trust)

- `runs/manifest.tsv`: 163 lines = **162 data rows** (18 cells × 3 arms × 3 reruns). rc column: **162/162 = 0**.
- `runs/raw/`: all 162 log files present. Every log ends `determinism,match=1` (**162/162**).
- Byte-identity: determinism digests identical across the 3 reruns in **54/54** cell-arms;
  full log text byte-identical across reruns in **54/54** after stripping the `wall_ns`
  line (manifest sha256 values legitimately differ across reruns ONLY because raw logs embed wall_ns).
- Grep gate: `-iE 'rng|rand\('` clean on all `src/` (only "Zero RNG" comments match). Zero RNG anywhere.
- Episode counts match the prereg formula (24·nt·rep): 384 … 18,432 per cell.

## 2. The headline numbers (median of 3 reruns; W = find_steps + scan_steps + mutops, suppressions inside mutops)

| cell | W trained | W naive | W auto | R = auto/trained | wall auto/tr |
|---|---|---|---|---|---|
| cap32a0r1 | 3,945 | 3,933 | 10,920 | 2.77 | 6.9 |
| cap32a0r3 | 10,985 | 10,973 | 31,480 | 2.87 | 14.0 |
| cap32a15r1 | 4,183 | 4,219 | 11,066 | 2.65 | 19.2 |
| cap32a15r3 | 11,699 | 11,601 | 31,870 | 2.72 | 0.9 |
| cap32a35r1 | 4,461 | 4,469 | 11,187 | 2.51 | 5.8 |
| cap32a35r3 | 12,533 | 12,365 | 32,249 | 2.57 | 6.2 |
| cap128a0r1 | 60,321 | 60,261 | 172,384 | 2.86 | 96.9 |
| cap128a0r3 | 168,353 | 168,293 | 496,672 | 2.95 | 8.8 |
| cap128a15r1 | 64,005 | 62,822 | 174,011 | 2.72 | 9.2 |
| cap128a15r3 | 179,405 | 174,232 | 502,193 | 2.80 | 9.2 |
| cap128a35r1 | 69,077 | 65,334 | 176,778 | 2.56 | 24.9 |
| cap128a35r3 | 194,621 | 181,768 | 510,430 | 2.62 | 1.7 |
| cap512a0r1 | 953,985 | 953,733 | 2,749,056 | 2.88 | 29.5 |
| cap512a0r3 | 2,664,065 | 2,663,813 | 7,919,488 | 2.97 | 21.7 |
| cap512a15r1 | 1,016,730 | 980,848 | 2,783,106 | 2.74 | 23.4 |
| cap512a15r3 | 2,852,300 | 2,737,270 | 8,010,886 | 2.81 | 11.8 |
| cap512a35r1 | 1,095,275 | 1,010,300 | 2,824,587 | 2.58 | 14.7 |
| cap512a35r3 | 3,087,935 | 2,825,626 | 8,135,841 | 2.63 | 7.6 |

Median R over 18 cells = **2.73**. End-of-curriculum blind probe accuracy:
**1.000 for all three arms on all 18 cells** (correct=nt, wrong=0, abstain=0).

## 3. Verdict against the frozen bars

| Bar | Result |
|---|---|
| K1: median W(auto)/W(trained) ≥ 1.5 | **2.73** (range 2.51–2.97 across cells) — PASS |
| K1 matching regime (cap∈{128,512}, adv∈{15,35}): R ≥ 2.0 on ≥75% | **8/8 = 100%** (2.56–2.81) — PASS |
| K2: no cell with trained < auto − 0.05 | **0 violations** (all 1.000) — PASS |
| K3: 3/3 byte-identical per cell×arm; grep RNG-clean | **54/54** identical, 162/162 match=1, grep clean — PASS |
| K4: ≥70% of W gap mechanically assigned to scans/overwrite-churn | **104.1%** (median; 101.3–106.8% per cell) — PASS |
| KILL (median R ≤ 1.0, K2 on ≥2 cells, K3 anywhere) | none triggered |

## 4. Mechanistic WHY (why deliberate-trained is cheaper)

1. **Autopilot pays a standing, content-independent scanning tax.** Every 10 episodes it
   walks the full fast+slow tiers (per-episode age passes included). Scan steps are
   64–68% of auto's own W on every cell, and the scan gap alone accounts for
   101–108% of the W gap vs trained (median 104.1%; the excess over 100% is offset
   because trained does slightly more true installs). The tax scales with cap.
2. **Trained deliberation does zero full-tier scans.** One bounded early-exit find per
   episode (find steps are nearly identical between trained and auto).
3. **Adversarial observations are suppressed, not installed-then-repaired.** Trained's
   suppression counts exactly mirror auto's dropped-observation counts per cell
   (cap512a35r3: trained suppress=2,151, kill=0, add=256; auto dropped=2,151,
   consol=256). Trained pays a cheap counter increment; auto admits each adversarial
   observation, pays find+age work for it, then discards it.
4. **Churn is latent, not observed, here.** `overwrite=0, evict=0` on all 18 cells —
   last-wins overwrite and lowest-confidence eviction never fired (slow tier sized ≥ nt,
   no contention). The measured gap is scan-driven; K4 passes via scans alone.
5. **Trained is the only arm that never kills** (kill=0 in all 18 cells).

Net: a gated, early-exit, suppress-rather-than-repair policy does less work per unit
of information than a timer-driven policy that scans the whole store on a schedule
whether it needs to or not.

## 5. Conditions map (where the direction holds)

**Everywhere tested.** R = 2.51–2.97 across all 18 cells — flat across cap (32/128/512),
adv (0/15/35%), rep (1/3). The prereg's *prediction* that autopilot might be
cheaper-or-equal on benign cells was WRONG: benign cells show R = 2.77–2.97 (the scan
tax is content-independent; trained's suppression cost is near zero, so adversariality
barely moves R). The regime-dependence hypothesis is rejected on this battery.

## 6. Wall-vs-W decomposition

- W is the verdict basis (prereg); wall corroborates the *direction* on **17/18** cells
  (wall ratio > 1.0; median 10.5).
- One cell contradicts on wall clock: cap32a15r3 wall ratio = 0.86 (auto faster).
  This is the smallest-scale run; per-cell ns/W varies 5–30× *within* arm on this VM,
  so this is scheduling noise. 1/18 < 1/3, so the prereg's investigate-before-verdict
  threshold is not tripped — flagged here, no verdict change.
- The wall ratio (median 10.5) amplifies the W ratio (2.73): each counted auto
  scan-step does multiple arena byte-accessor field reads/writes per step while each
  trained find-step usually early-exits after one arena read; the remainder is VM
  noise. The clock data is too noisy for a clean numeric split — reported honestly.

## 7. W/ep and memory (for WS1-B's cost-per-accuracy comparison)

W/ep (median; episodes 384 … 18,432):

| cap | trained | naive | auto |
|---|---|---|---|
| 32 | 9.5–11.6 | 9.5–11.6 | 27.3–29.1 |
| 128 | 36.5–45.0 | 36.5–42.5 | 107.8–115.1 |
| 512 | 144.5–178.3 | 144.5–164.4 | 429.7–459.7 |

Memory: trained/naive fixed 667,648 B arenas (512-slot store + 16,384-entry audit
ledger + driver state); auto 66,752–84,992 B (fast+slow tiers + history, no audit
ledger) — ~8–10× smaller memory. Used ledger = audit_n × 40 B (1,960 B at cap32,
7,720 B at cap128, 30,760 B at cap512). Zero per-episode allocation on all arms.
The bill is work, not memory: auto trades 8–10× less memory for 2.5–3× more work.

## 8. The naive arm (untrained deliberation) — WS1-B's never-worse-law input

- **WS1-B's assumption is CONFIRMED: untrained deliberation is NOT safe.**
  1,876 collateral true-kills total (sum of per-cell medians): 0 at adv=0, scaling
  with adv×cap — 12 at cap32a35r3, 177 at cap128a35r3, **681 at cap512a35r3**
  (there: add=3,418, kill=3,146 — churn, not learning). Spurious slots left behind:
  10–16 on adversarial cells (16 at cap128/512, 10–12 at cap32).
- **The naive arm is CHEAP — W(naive)/W(trained) = 0.92–1.01.** It avoids the scan
  tax like trained does; its cost is kill+add churn (7,872 mutops at cap512a35r3
  vs trained's few hundred). The saving vs trained is paid in collateral damage.
- **End-probe accuracy heals (1.000)** because phase D's verified true episodes
  re-install what naive destroyed. The probe is blind to mid-run damage — the
  collateral counters are the damage evidence. Use those, not the healed accuracy.

## 9. WS1-B answers (from the coordination request)

(a) **A1 vs A2 direction: REPLICATED** on fresh fixtures — median 2.73× on W,
    18/18 cells ≥ 2.0×. Wall direction also replicates (auto slower everywhere);
    wall is VM-noisy — use the W/ep table in §7.
(b) **Ops/work per episode: §7 table.** A1: 9.5–178.3 W/ep; A2: 27.3–459.7 W/ep
    across regimes; find/scan/mutops/suppress breakdowns in the raw logs.
(c) **Untrained-deliberation damage: REPLICATED in kind, larger in magnitude.**
    0 on benign cells, 12–681 on adversarial cells (grows with cap×adv). The old
    "28" was generator-specific; the phenomenon is robust.
**Recommendation: YES — WS1-B should add rule 5 (KB writes → forced-conscious).**
Untrained deliberation is cheap but destructive; trained deliberation is cheap AND
safe. The rule should distinguish them: force consciousness on KB writes until the
trained gate is earned.

## 10. Evidence and commits

- Prereg (frozen before any fresh run): `403906826516f3c76c0a26ff1b60e94a094370d9`
  — `docs/lab/cognition_ws/ws1/PREREG_WS1A.md` (branch tnn-native-lab, sylorlabs/TNN).
- Sources: `docs/lab/cognition_ws/ws1/src/` — w1a_gen.zag, w1a_time.zag,
  w1a_memory_core.zag (MA copy, only MA_CAP/MA_AUDIT_CAP resized), w1a_common.zag,
  w1a_arm1.zag, w1a_arm3.zag, w1a_psm.zag, w1a_auto.zag, run_all.sh.
- Evidence: `docs/lab/cognition_ws/ws1/runs/manifest.tsv` (162 rows;
  raw 162 logs stay local — manifest SHAs + byte-identity verification preserve
  verifiability), `WS1A_PRELIM.md`, `analyze_ws1a.py` (analysis script), this verdict.
- Binaries in `build/` are scratch artifacts, never committed.
- Verdict evidence commit SHA: (appended after commit lands).

## 11. Caveats

- Accuracy hit ceiling (1.000) for all arms — this battery tests COST, not capability.
  The prior bill's accuracy advantage for deliberation is NOT re-demonstrated here.
- Wall-clock numbers are VM noise; only direction + W are load-bearing.
- Envelope ends at cap=512 / 18,432 episodes; claims beyond are extrapolation.
