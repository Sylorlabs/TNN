# NAMECHECK: MA4c (learner-driven redundancy proxy)

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
  integer ratios out of DIAG audit lines; no scientific computation).
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging,
  znc invocation, binary execution, hashing, cmp/diff/grep audits,
  git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/meta_architecture4c/`
on branch `tnn-native-lab` (worktree `/home/hatch/workspace/tnn-rsi-gpi3`).
Nothing is pushed to GitHub; commits stay local with explicit
pathspecs. Commit order: the diagnostic prereg commit contains ONLY
PREREG_DIAG.md and NAMECHECK.md (Step 0 + Step 1 + diagnostic design
record). The diagnostic implementation strictly postdates it. The
frozen prereg (PREREG.md) commits strictly before the frozen
implementation. No frozen kill bar is evaluated before its prereg
commit.

## Design record (pre-prereg, no implementation run)

MA4b repaired the detector (current-band tripwire sees the E795
kill) but left the proxy researcher-supplied: redun() declares
cell i redundant iff a protected cell j has |mean_i - mean_j| <=
RDDM=10. MA4c asks whether the learner itself can determine
redundancy, replacing the domain-scale distance threshold with a
criterion in the learner's own measurement units.

Key observation: redun() is consulted only at the two W triggers
(E735, E795) in the entire MA4b run (TRIGX shows only U-path
triggers; TRIGY n=0). The experiment is therefore a clean
two-case discrimination: fire on genuine R/R redundancy (E735),
stay silent on adversarial B4/R conflation (E795).

Design: cross-error substitutability. Redundancy is a claim about
substitutability ("j can take over i's explanatory role"), and the
learner already computes every cell's per-episode prediction error
for scoring. New learner state xerr[16]: for each ordered pair
(j,i), the cumulative prediction error of cell j on episodes won
by cell i. Updated every episode from revealed values only;
row v and column v zeroed on reseed of v (the destroyed model's
evidence is gone, mirroring the wblkc discipline from MA4b).

Candidate proxy rule (frozen form; K adopted from the diagnostic):
cell i is redundant given protected cell j iff i is protected and
xerr[j][i] <= K * wpsm[i], where wpsm[i] is i's own cumulative
winner error. Both sides are learner-measured error tallies; K is
dimensionless (takeover cost vs current cost), not a domain
value-distance. The victim's wins are selection-biased toward the
victim (it won them), so K must exceed 1; the diagnostic measures
the actual ratios.

Why victim-normalized (not anchor-normalized, not symmetric):
the question is directional (can j absorb i's role). A symmetric
variant was rejected on mechanism grounds: at E795 the B4 model
covers the R anchor's B4-block wins adequately (bands overlap in
values 78..81), so the reverse direction would fire and destroy
the discrimination. The diagnostic measures the forward direction
only.

Stages:
1. Diagnostic (PREREG_DIAG.md, exploratory): MA4b + write-only xerr
   (identical update/zeroing as the future learner state) +
   per-trigger DIAG audit. Verifies byte-identical trajectory to
   MA4b and measures the cross-error ratios at E735/E795.
2. Frozen (PREREG.md): exact rule with adopted K, frozen bars,
   frozen implementation where redun2() drives the real victim
   rule, the old RDDM=10 proxy kept as a write-only shadow, and
   MA4b's tripwire kept intact (real + shadow-driven).

B7: the 29-word list grep must return empty in ma4c_diag.zag and
ma4c.zag; comments and string labels avoid the listed words
("count"->"n"/"tally", "event"->"episode", "regime"->"band",
"learn"/"learner"->"cell"/"mechanism" wording, etc.).
