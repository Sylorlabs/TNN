# NAMECHECK: PROXY-REDESIGN (structural proxy via interventional interchangeability)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which perl` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which ruby` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which node` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary; verified 2026-10-03).
- `which git` returns `/home/hatch/safebin/git`; git write ops invoked via
  the resolved `/usr/bin/git` path (the safebin git symlink has a known
  EPERM failure mode on object/index writes per the 2026-10-03 workspace
  lesson; same tool, resolved path).
- `which awk` returns `/home/hatch/safebin/awk` (used only for reading
  printed integers out of audit lines; no scientific computation).
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging,
  znc invocation, binary execution, hashing, cmp/diff/grep audits,
  git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/proxy_redesign/`
on branch `tnn-native-lab` (worktree `/home/hatch/workspace/tnn-rsi-gpi3`).
Nothing is pushed to GitHub; commits stay local with explicit
pathspecs. Commit order: this prereg commit contains ONLY PREREG.md
and NAMECHECK.md (Step 0 + Step 1 + design record). The implementation
(pr_*.zag) strictly postdates it. No frozen kill bar is evaluated
before its prereg commit.

## Design record (pre-prereg; exploratory basis disclosed in PREREG.md)

MA4C-MULTISTREAM disclaimed the (R) ratio: it measures contingent
error overlap, and no integer K separates genuine/adversarial on
all streams (ratios coincide on T1/T2/T3, invert on T4).

Exploratory analysis (write-only diagnostic in /tmp, frozen
MA4C-MULTISTREAM data, no mechanism changes) recorded runner-up
tallies at decision points. Finding: the genuine/adversarial
difference is coverage SYMMETRY, not magnitude.
- E735 (genuine, all streams): cov[3][2]=98.5%, cov[2][3]=100%.
  Symmetric: interchangeable duplicates.
- E795 (adversarial, W6/T4): cov[3][2]=100%, cov[2][3]=80-87%.
  Asymmetric: cell 3 is a superior model; cell 2 has a distinct
  active role (became a B4 model; no longer covers cell 3's wins).
- E795 (T1/T2/T3): state frozen from E735; cov symmetric
  (98.6% vs 100%). Benign late consolidation, not a kill.

The frozen proxy (redun3) decides by the ordinal symmetry
comparison cov[i][j] >= cov[j][i] (integer-exact
cross-multiplication), plus prot, wpart[j]>=wpart[i], and mutual
PACT>=5 runner-up evidence. No threshold on any ratio; no error
magnitudes; no mean distance. Causal-intervention framing:
runner-up = the do-operator on cell removal (removing i affects
only i's win episodes, since means update only on wins).

## Build record

(recorded after the prereg commit; implementation has not begun)
