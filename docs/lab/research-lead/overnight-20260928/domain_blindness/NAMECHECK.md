# NAMECHECK: DOMAIN-BLINDNESS (U composition label-independence)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary; verified 2026-10-03).
- Safebin contents: 49 entries (coreutils, git, awk, sed, grep, cmp, diff,
  sha256sum, znc, ...); no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging, the
  frozen mechanical renaming (sed/grep), znc invocation, binary
  execution, hashing, git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.
- znc smoke test: compiled the frozen `p6_full.zag` in /tmp and ran it
  3x; output 3/3 byte-identical, sha256
  `be713f822779afdd7cf1c3f2e87670dc4b5e903fa73a8bc0ede0a105f3a219d7`,
  matching the P6 lane's frozen K4 digest byte for byte. Baseline
  reproduced before prereg freeze.

## Step 1: Reference integrity

Sources copied from `~/workspace/lane-compose-pair6/compose_pair6_adv/`
(read-only; never modified in this lane):

- `ref_uc_base.zag`
  sha256 `736f12e7452fb0a95c2dbfc8115028a4e1afba9529cb6cd727acb65367799218`
  (matches canonical COMPOSE-COLLAPSE digest and the P6 lane's
  NAMECHECK.md Step 1; verified 2026-10-03)
- `ref_uc_uni.zag` (the unified operation U under test)
  sha256 `ec36df4a01cb1a2b93043184e6e2c84b07658fe7b0c317f9a489ffd6b7b4562e`
  (matches canonical digest; verified 2026-10-03)
- `p6_new.zag` (sole carrier of exercised domain identifiers)
  sha256 `32d84056de2878f8db000ff87b2fb4b96cbf187d6cf42c357081bfb69a123870`
  (verified 2026-10-03)

GEN: searched `compose_collapse`, `compose_ops`, `lane-compose-pair6`
for a GEN composition implementation; none exists. U only.

## Step 2: Lane location and commit discipline

Lane repo: this directory
(`~/workspace/docs/lab/research-lead/overnight-20260928/domain_blindness/`),
fresh `git init` 2026-10-03, branch `main`. Nothing is pushed to GitHub;
commits stay local. The prereg-alone-then-implementation commit order is
honored inside this repo: this commit contains ONLY PREREG.md and
NAMECHECK.md (Step 0). The renaming scripts, renamed sources, binaries,
and REPORT.md come in later commits.

## Build record (completed 2026-10-03)

- [x] rename_a.sh transcribed from PREREG Section 4.1, with two
      disclosed minimal fixes: comment-strip `^[[:space:]]*//`
      (indented comments; required by frozen audit (d)) and uni_solve
      arena alternation `(A[23]?|C)` (A2/A3 call sites; caught by the
      fail-closed audit on first run). Both mechanical, both recorded
      in REPORT.md.
- [x] db_new.zag produced; all four step-8 audits pass
- [x] B5: renaming steps 2-7 on ref_uc_uni.zag change zero bytes;
      U-logic numeric inventory shows no identifier-scale constants
- [x] kindswap.sh per PREREG Section 5; diff audits pass
      (base: exactly 2 lines; driver: exactly 4 lines)
- [x] a_full.zag / b_full.zag assembled; all 6 region cmps pass;
      B6(c) grep for identifier comparisons: empty
- [x] 3/3 byte-identical runs per variant; digests recorded in REPORT.md
- [x] inverse-mapped outputs cmp EMPTY vs frozen baseline
      (`be713f82...` reproduced exactly by both variants)
- [x] REPORT.md with verdict PASS (blind) per Section 9 mapping
