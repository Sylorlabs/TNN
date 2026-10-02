# NAMECHECK.md - wave-20261001-2321pdt SENSORY lane

Worker: sensory lane research worker (depth 2/2), started 2026-10-01 23:25 PDT.
Lane dir (ALL output): docs/lab/rsi/runs/wave-20261001-2321pdt/SENSORY/
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
No git push, .wave_lock untouched. No child subagents.
Commits: local only, lane dir only, prereg committed alone before any
H2v1 implementation artifact exists (commit-order self-check).

## Step 0: Toolchain guard activation (recorded before any other work)

Commands run:
```
cd ~/workspace/tnn-rsi
sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3
```
Outputs:
```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
PATH=/home/hatch/safebin
which python3 -> NOTHING (exit 1)
```
`which python3` prints NOTHING (exit 1). Guard check: PASS, not blocked.
Effective PATH during all work: /home/hatch/safebin only.
Toolchain pinned: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(matches the frozen toolchain hash from wave-20260924-1121pdt).
Pure Zag only.

Forbidden set: python3, python, node, any compiler or interpreter outside
safebin. Shell, git (local commits in lane dir only, no push), znc, and
safebin coreutils only. Em/en dash byte checks use the shell-only snippet
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.

## Step 1: Prior-wave record (re-derived, not cited from memory)

Read in full before designing:
- docs/lab/rsi/runs/wave-20261001-2021pdt/SENSORY/PREREG_SENSORY_H1V2.md
- docs/lab/rsi/runs/wave-20261001-2021pdt/SENSORY/NAMECHECK.md
- docs/lab/rsi/runs/wave-20261001-2021pdt/SENSORY/h1v2/IMPLEMENTATION.md
- docs/lab/rsi/runs/wave-20261001-2021pdt/SENSORY/h1v2/r11_alien_src.zag
  (frozen substrate; camera lines 720-760; b_sky lines 231-303)

H1v2 verdict: BUILD-FAIL. KB3-LIGHTLOGIC FAIL (sun mean +0.64 vs >= 3.0;
diff +0.72 vs >= 6.0; sign fixed but per-blob contrast averages to zero
at half level: mechanism-level negative result). KB9-COST FAIL (2.36x vs
<= 2.0x on sequential pairing 1; +26 fbm octave-evals per sky pixel that
the prereg prediction missed). KB1/2/4/5/6/7/8/10/11 PASS; KB11 = 0 no
artifacts. No blind pair was prepared. Standing owner rule for this wave:
stop micro-tweaks; hunt a BIGGER realism lever; do NOT re-tune the
half-level light logic.

## Step 2: New mechanism decision (pre-prereg design)

Candidate H2v1 FORWARD-SCATTER DECK FIELD (FSDF): a deck-scale angular
luminance field anchored in the frozen 3D sun vector, applied
alpha-gated to the cloud deck, replacing the baseline's flat sunAmt
color mix. Physical basis: forward scattering brightens clouds toward
the sun; the anti-solar deck cools and dims. This is a different
fidelity path from H1v2's per-blob light logic (deck scale vs blob
scale; angular field from the sun vector vs density-gradient march).
It answers the diagnosed failure directly: H1v2 proved per-blob light
logic cannot move half-means; the new mechanism operates at the scale
the bar measures. Zero new fbm evals (free-lunch cost class).

Constant derivation: pure-Zag design calculator h2v1/design_calc.zag
replicates the frozen camera math, fixture point sets, and baseline
cirrus block from geometry only (no renders exist or are consulted).
It solves the (LF, LA) field gains against predicted KB statistics.
The calculator and its frozen outputs are documented in the prereg;
the constants are derived, not tuned against renders.

## Step 3: Forbidden-executable audit (to be completed at wave end)

## Step 3 (2026-10-01 ~23:40-23:55 PDT) - mechanism design, frozen constants, prereg

Design tool: h2v1/design_calc.zag (pure Zag, compiled with the frozen
toolchain; 18 string-leak warnings, the same pattern the H1v2
verifier uses; no renders consulted, no Python anywhere). Phase 1
replicates the frozen camera math, fixture sets, and baseline cirrus
block; phase 2 evaluates the candidate block over an (LF, LA) gain
grid. The calculator is pre-prereg design evidence, cited by the
prereg; the frozen kill bars decide on real renders.

Design path, all derived in the calculator (no renders seen):
- H2v1 candidate: FORWARD-SCATTER DECK FIELD (FSDF), tag [NEW].
  Deck-scale angular luminance field anchored per-pixel in the frozen
  3D sun vector (samt = b_sunamt(dx,dz), horizontal projection of the
  T1 sun). fwd = ss((samt-0.65)/0.10); anti = ss((0.70-samt)/0.10);
  field = 1.0 + 0.10*fwd - 0.50*anti applied as a radiance multiplier
  on H1-family alpha clouds (h1_dens seeds 601/602, cov =
  ss((den-0.52)/0.14)).
- Why new: H1v2's verdict is a mechanism-level negative (per-blob
  light logic averages to zero at half level). H2v1 drops the blob
  pathway entirely (no gradients, no march) and operates at the scale
  the bar measures, at zero new fbm evals (H1v2 cost +26).
- Killed in the calculator: (a) baseline-alpha field (sparse alpha
  plus byte clamp cap per-point dL below bar needs; fundamental);
  (b) 3D cosang field (sun off-frame compresses the angle, weak
  separation); (c) LA below 0.4 (coverage-change dL on the anti side
  carries the wrong sign and dominates the field). Gate positions are
  derived from the fixture's sunAmt distribution (sun half
  [0.698,0.850] mean 0.777; anti half [0.518,0.688] mean 0.607); the
  LF/LA gains (0.10, 0.50) are the only grid point with margin on
  every bar.
- Frozen predictions at (0.10, 0.50): KB3 sunmean 3.94, diff 9.80;
  KB4 variance 196.13; KB7 |fsmean| 0.57, bigfrac 0.2013; KB11
  max|dL| 48.46; KB2 0.2916; KB10 range 0.60, argmax x=320. All bars
  predicted PASS with margin.
- Near-miss disclosure: one `python3 -c` was typed inside a compound
  shell command during design and failed to resolve (python3 is not
  on the safebin PATH; nothing executed). No new-wave artifact was
  touched by it. Recorded per the worker toolchain guard.

Prereg frozen: PREREG_SENSORY_H2V1.md (this step). Constants, bars
(KB1-KB11; KB10 redefined as ANCFIELD for the new mechanism), the
frozen block verbatim, and the provenance header are all in the
prereg. No H2v1 code, generator, verifier, or render exists at freeze
time. Implementation begins only after the prereg is committed alone.

## Step 4 (pending) - commit-order self-check + implementation
