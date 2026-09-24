# PREREG — F5 counter-corroboration trap, tightened-window fork

Frozen 2026-09-24. Committed ALONE before any code. Builder: F5 round-2
tighten crew (Crew 2, PAM round-2 swarm).

This prereg executes honest path #1 from
`docs/lab/senses/pam-rebuild/round2/f5_redteam300/VERDICT_F5_REDTEAM300.md`:

> Honest paths forward (separate preregs): tighten the windows to the
> exemplar cluster's actual scale...

The red-team KILL rested on two facts: the trap window (±150 conf, ±2000
measure) is vastly wider than the exemplar cluster it was built from
(measure span 29, conf span 17); 110/300 (36.7%) of near-exemplar CORRECT
percepts blocked, 94/300 (31.3%) delayed > 50 trials vs the ≤ 25% bar.

## 1. Hypothesis under test

The tightened pre-confirmation block predicate (family-stem match;
|Δconf| ≤ 9; |Δmeasure| ≤ 15) passes the frozen 300-percept battery bars:
delay ≤ 25% over 50 trials, far-control 0/60 blocked.

## 2. Scope (explicit honesty, same as the red-team)

**Pre-confirmation block predicate ONLY.** The "three deliberate
re-inspections from three temporal crops" confirmation machinery is still
unbuilt and is NOT exercised here. The delay operationalization (§6) is the
same preregistered assumption about the unbuilt machinery as the red-team
prereg §5 — an assumption, not a test of the machinery.

## 3. Window derivation (mechanical, from the frozen exemplar bank)

Bank: frozen `v2/f5_backtest/exemplars.tsv`, SHA
`13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`
(re-verified before use; see §4).

- Measured cluster scale: conf 701–718 → span 17; measure 2618–2647 →
  span 29.
- **Derivation rule (frozen here): per-exemplar window radius =
  ceil(cluster span / 2) on each axis** → |Δconf| ≤ 9, |Δmeasure| ≤ 15.
- Rationale: a candidate within one cluster-radius of an exemplar is
  "within the cluster's own scale" — as close as neighboring exemplars get
  to each other. The union of the six per-exemplar windows covers exactly
  the cluster bounding box plus one cluster-radius of margin.
- Frozen tension (stated, not resolved): the 8 TMB-5 false accepts the
  frozen trap caught in the backtest live OUTSIDE the cluster's scale
  (nearest: 245 measure units from the cluster edge, 8.4× the tightened
  measure radius; nearest conf gap 46, 5.1× the conf radius). The frozen
  windows caught them only by being 8–10× wider than the cluster. This fork
  does not tune the rule to keep them — it tests the rule and reports what
  it keeps.

The rule was fixed before its consequences were computed; §8 states the
consequences as checks the Zag battery must reproduce. The rule was not
adjusted to hit any outcome.

## 4. Frozen fixtures (reused, read-only, SHA-verified)

- `round2/f5_redteam300/fixtures_ledger.txt`, SHA
  `0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0`
  — the identical 300 NEAR + 60 FAR battery (all DISP=ACCEPT_INSTALL, all
  truth-correct, 17-field format + SET=NEAR/FAR). Re-verified before every
  run. No new fixtures are generated.
- `round2/f5_redteam300/exemplars.tsv` (copy; SHA must match the backtest's
  `13f4ca...` above).
- Backtest retention replay reads the committed backtest evidence ledger
  `v2/redteam/evidence/ledger_d_withhold.txt` read-only (already committed
  under docs/lab/; NOT re-committed here; its SHA is recorded in the
  verdict).

## 5. Tightened predicate (the mechanism under test)

Candidate BLOCKED iff there EXISTS a bank exemplar with ALL three:

1. Same family stem (`TMB-1` → `TMB`; `rt4_TMB-5_0000.r24` → `TMB`).
2. |conf_cand − conf_ex| ≤ 9.
3. |measure_cand − measure_ex| ≤ 15.

**Margin substitution carried exactly as the backtest and red-team:**
`measure` (task-specific raw quantity, NOT the classification margin mrgF)
is the second distance axis. No true-margin axis exists in the predicate;
adding one would test a different mechanism.

## 6. Delay operationalization (same preregistered assumption as the red-team)

- **Primary model:** FIFO confirmation queue, one deliberate re-inspection
  per trial, 3 re-inspections per blocked percept → k-th blocked percept
  clears at delay_k = 3k trials; allowed percepts delay 0.
- **Sensitivity S1:** one re-inspection per 5 trials → delay_k = 15k.
- **Sensitivity S2:** every blocked percept confirmed in exactly 3 trials.
- Delay-length bins (over the 300 NEAR): 0 | 1–3 | 4–10 | 11–50 | 51–100 |
  101–300 | 301+.

## 7. Kill bars and reported metrics

- **(a) Delay bar:** > 25% of the 300 near-exemplar percepts (≥ 76 of 300)
  delayed > 50 trials under the primary model → KILL.
- **(b) Far-control bar:** far-control over-block rate must be 0
  (0/60 BLOCKED) → any block → KILL.
- **(c) Distribution report:** full delay-length histogram plus S1/S2 —
  not just the binary bar.
- **Reported metric (not a kill bar): over-block count on the 300**
  (NEAR blocked / 300).
- **Reported metric (not a kill bar): backtest false-block retention** —
  the backtest's 43 candidates (9 false accepts, 34 true accepts) replayed
  through the tightened predicate; the frozen trap scored 8/9 false blocked
  and 0/34 true blocked.

**Preregistered honest reading (function clause):** bars (a) and (b) were
designed around over-block cost, and a trap that blocks nothing passes them
vacuously. If (a) and (b) PASS but the retention metric collapses below the
backtest's 8/9, the verdict records that the tightened trap no longer
performs its backtest-demonstrated function (catching false accepts), and
the go/no-go for the F5 live-gate build is NO-GO despite the bar PASS:
there is nothing left to build the gate on. SURVIVE/KILL is scored on the
frozen bars; the function clause governs the build recommendation.

## 8. Pre-registered sanity expectations (implementation check, NOT the verdict)

Computed from the §3 rule against the frozen grid (§3a of the red-team
prereg); the battery must reproduce these exactly, or the implementation
is wrong:

- Tightened measure union: [2618−15, 2647+15] = [2603, 2662] (contiguous —
  the six per-exemplar ±15 windows all overlap). Grid measures
  2200, 2700, 3200, … → none in [2603, 2662] → **expected NEAR blocked:
  0/300**.
- Expected primary-model delayed > 50: **0/300**. S1: 0/300. S2: 0/300.
- Expected far-control blocked: **0/60** (COL/PTC excluded by stem;
  TMB-outside group at conf 950–988 / measure 5500–6450 clears both
  windows).
- Expected retention: **0/8** TMB-5 false accepts blocked (nearest |Δmeas|
  245 > 15), 0/9 false total (the COL-4 false accept stays correctly
  ALLOWED by family scope), **0/34** true blocked.

The verdict comes from §7 applied to the battery's measured numbers, not
from these expectations.

## 9. Laws and method

- The tightened predicate is implemented in pure Zag, byte-identical to the
  frozen `round2/f5_redteam300/f5_rt300.zag` (SHA
  `2ab4bc69f3b03a5fd8fad6927dd56233f792befa68135dd1923f4dcd732e9741`)
  EXCEPT the two window constants (150 → 9, 2000 → 15) and the SANITY line
  (expected_blocked=0). The diff is committed as evidence.
- The retention replay is pure Zag, byte-identical to
  `v2/f5_backtest/f5_pred.zag` (SHA
  `4fa4e2e4da86eeb1b21c4f43598d2bf69277131f096f7f3ddfc82fe8b9990430`)
  EXCEPT the two window constants. Same parser, same 43 candidates.
- Battery binary reads argv[1] = fixture ledger, argv[2] = frozen
  exemplars copy. Asserts judgment == truth on every line; any mismatch
  aborts loud (nonzero exit), never silently counted.
- Run 3× per binary; SHA-256 of stdout byte-identical across all three
  runs. Zero RNG.
- Derivation record `derive_windows.py` (deterministic, no RNG) is
  committed as evidence of the §3 computation.
- Commit order: this prereg ALONE first; then sources, frozen-bank copy,
  three run outputs per binary, SHASUMS.txt, and the verdict committed
  together. No binaries, no `.zagd` / `.zag-cache` files.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Work: `docs/lab/senses/pam-rebuild/round2/f5_tightened/`
  (branch `tnn-native-lab`).

## 10. Transparency note

The delay model (§6) is the one free choice and concerns unbuilt machinery
— preregistered as an assumption with two sensitivity cells, carried
unchanged from the red-team prereg. The window rule (§3) is mechanical;
its consequences were computed from the rule and frozen here as checks —
the rule was not adjusted to hit any outcome. No threshold tuning, no
post-hoc family exceptions, no outcome-conditioned rules.

## 11. Deliverable

Verdict: SURVIVE or KILL on the frozen bars (§7a–b), with measured numbers
(delayed>50 / 300 primary, S1, S2; far-control blocked / 60; NEAR blocked /
300; retention false blocked / 9 and true blocked / 34), run SHAs, commit
SHAs, and an explicit go / no-go for the F5 live-gate build per the
function clause. If killed: say so plainly with the numbers and stop — no
window-tuning retries without a new prereg.
