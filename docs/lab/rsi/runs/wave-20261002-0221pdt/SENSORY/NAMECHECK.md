# NAMECHECK.md - wave-20261002-0221pdt SENSORY lane

Worker: sensory lane research worker (depth 2/2), started 2026-10-02 02:27 PDT.
Lane dir (ALL output): docs/lab/rsi/runs/wave-20261002-0221pdt/SENSORY/
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
No git push, .wave_lock untouched. No child subagents.
Commits: local only, lane dir only, explicit pathspec only; prereg committed
alone before any implementation artifact exists (commit-order self-check).
No Python anywhere. Dash checks via worker_snippets/check_no_dash.sh.

## Naming note (recorded at lane start)

The task text asks for PREREG_SENSORY_H2.md, but the prior wave
(wave-20261001-2321pdt) already froze PREREG_SENSORY_H2V1.md for its own
H2v1 FORWARD-SCATTER DECK FIELD candidate. Reusing the H2 name would
collide in the provenance record and risk presenting my candidate as a
re-certification of H2v1. This lane names its candidate H3
(SUN-ANCHORED SKY-DOME LUMINANCE GRADIENT) and its prereg
PREREG_SENSORY_H3.md. The task's H2 intent is satisfied by the new-wave
candidate; the rename is documented here, in the prereg, and in the
final report.

## Step 0: Toolchain guard activation (recorded before any other work)

Commands run:
```
cd ~/workspace/tnn-rsi
bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
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
which python3 -> NOTHING (exit 1)
```
Guard check: PASS, not blocked. Effective PATH during all work:
/home/hatch/safebin only.
Toolchain pinned: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(matches the frozen toolchain hash from wave-20260924-1121pdt).
Pure Zag only.

Forbidden set: python3, python, node, any compiler or interpreter outside
safebin. Shell, git (local commits in lane dir only, no push), znc, and
safebin coreutils only. Em/en dash byte checks use the shell-only snippet
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.

## Step 1: Prior-wave records (read in full before designing)

- docs/lab/rsi/runs/wave-20261001-1721pdt/SENSORY/VERDICT_H1_DISCARDED.md
  (H1 LIT CLOUD DECK, DISCARDED on KB3: wrong sign, diff -2.13 vs >= 6.0;
  projection warp misaligned the sun march; silver lining did not compensate)
- docs/lab/rsi/runs/wave-20261001-2021pdt/SENSORY/h1v2/IMPLEMENTATION.md
  (H1v2 TRANSPORT-ANCHORED LIT CLOUD DECK, BUILD-FAIL on KB3
  sun +0.64 vs >= 3.0, diff +0.72 vs >= 6.0, and KB9 2.36x vs <= 2.0x;
  mechanism-level negative: per-blob light logic averages to zero at
  half level; +26 fbm octave-evals per sky pixel)
- docs/lab/rsi/runs/wave-20261001-2321pdt/SENSORY/PREREG_SENSORY_H2V1.md
  (H2v1 FORWARD-SCATTER DECK FIELD, deck-scale angular field, zero new
  fbm evals; verdict NEVER RECORDED by the prior wave: h2v1c stalled at
  row 704/960, wave ended mid-pipeline, no verdict file, blind/ empty)
- docs/lab/rsi/runs/wave-20261001-2321pdt/SENSORY-CHECK/SENSORY_STATUS.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/SENSORY-PREP/SENSORY_PREP.md

## Step 2: Read-only analysis of prior-wave H2v1 renders (design input, NOT a verdict)

The prior wave left out/base1, out/h2v1a, out/h2v1b complete and
out/h2v1c incomplete. To design a structurally different candidate I
needed to know whether H2v1's deck-scale FSDF actually moved the
half-means on real renders. I ran the prior lane's frozen verifier
binary (bin/h2v1_verify, read-only, no lane files modified) with copies
of its existing BMPs in /tmp/h2v1check. Results (base1 vs h2v1a):

KB2 0.2916 PASS; KB3 sun +3.92 (bar >= 3.0) PASS, anti -6.00,
diff +9.92 (bar >= 6.0) PASS, matching the prereg predictions
(3.94 / 9.80) within rounding; KB4 198.34 PASS; KB5 1.03 vs <= 1.0
FAIL by 0.03; KB6 0.00 PASS; KB7 -0.54 / 0.2013 PASS; KB8 1.090 PASS;
KB10 argx 320 / range 0.60 PASS; KB11 0 PASS.

Design lessons, all derived from this analysis:
(a) Deck-scale angular fields DO move cloud half-means where per-blob
logic provably could not: H2v1's KB3 PASS is real on renders.
(b) KB5 1.03 vs <= 1.0 is a terrain leak, not a cloud failure: the FSDF
field sits inside b_sky's cirrus block, and b_tshade calls b_sky for
its hemisphere ambient samples (dy=0.12 ring sample and normal sample),
so the field fires for terrain pixels too. The prereg's calculator
admitted it did not model the ambient b_sky call sites; the real
renders exposed it. Any sky mechanism placed inside b_sky inherits
this leak. My H3 design avoids it BY CONSTRUCTION: the dome gradient
lives in a NEW function b_skydome called only from the 3 direct-sky
main-loop call sites; b_tshade keeps calling the original b_sky
byte-identical, so KB5/KB6 are 0.00 by construction.
(c) This analysis is NOT an H2v1 verdict. The verdict belongs to the
prior wave's lane and coordinator. Lineage status for H2v1:
UNJUDGED-OPEN (renders exist 2/3, verifier run by that lane never
completed, no verdict recorded, never judged by Micah). I claim no
verdict here; the KB5 1.03 figure is my read-only analysis input.

## Step 3: New mechanism decision (pre-prereg design)

Candidate H3 SUN-ANCHORED SKY-DOME LUMINANCE GRADIENT (SDLGRAD), tag
[NEW]. A sun-anchored luminance gradient applied to the CLEAR-SKY dome
color on the direct-sky path only, leaving the cirrus block
byte-identical. Physical basis: on the deliberated dusty 0.6-bar world,
forward scattering brightens the clear sky toward the sun across the
whole dome and the anti-solar sky cools and dims; the baseline already
does this at the horizon ring (T2 azimuth gradient) but the k1/k2
zenith mixes wash sunAmt out above dy ~ 0.18, leaving the upper dome
azimuthally flat, a classic CG tell. The lever extends the
sun-anchored gradient through the dome.

Structural difference from H1/H1v2/H2v1 (all three replaced the cirrus
block's cloud lighting; none touched the clear-sky dome itself):
different scene layer (clear sky, not cloud deck), different
information pathway (dome luminance multiplier from sunAmt, no cloud
density or alpha involvement), different fidelity path (sky gradient
realism, not cloud lighting). It is the first candidate to operate on
the background the whole scene is judged against, and the first to
eliminate the terrain leak by construction rather than by hope.

Constants derived in the pure-Zag design calculator h3/design_calc.zag
(pre-prereg, geometry only, no renders consulted), documented in the
prereg. Frozen gains chosen at the grid point with margin on every
predicted bar.
