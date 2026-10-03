# NAMECHECK: COMPOSE-CYCLES (U cycle-composition boundary)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary; verified 2026-10-03).
- Safebin contents: coreutils, git, awk, sed, grep, cmp, diff, sha256sum,
  znc, ...; no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging, znc
  invocation, binary execution, hashing, greps/diffs for the frozen
  audits, git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Reference integrity

Frozen sources copied read-only from
`~/workspace/docs/lab/research-lead/overnight-20260928/domain_blindness/`
(their digests match the canonical COMPOSE-COLLAPSE digests):

- `ref_uc_uni.zag` (THE U mechanism under test; main stripped at build)
  sha256 `ec36df4a01cb1a2b93043184e6e2c84b07658fe7b0c317f9a489ffd6b7b4562e`
- `ref_uc_base.zag` (diff base for cyc_base.zag; never built directly)
  sha256 `736f12e7452fb0a95c2dbfc8115028a4e1afba9529cb6cd727acb65367799218`

GEN: no GEN composition implementation exists (per the domain_blindness
lane's search of compose_collapse, compose_ops, lane-compose-pair6).
U only.

## Step 2: Lane location and commit discipline

Lane repo: this directory
(`~/workspace/docs/lab/research-lead/overnight-20260928/compose_cycles/`),
fresh `git init` 2026-10-03, branch `main`. Nothing is pushed to GitHub;
commits stay local. The prereg-alone-then-implementation commit order is
honored inside this repo: the first commit contains ONLY PREREG.md and
NAMECHECK.md (Steps 0-2). `cyc_base.zag`, `cyc_new.zag`, build script,
binaries, run outputs, and REPORT.md come in later commits.

## Build record (completed 2026-10-03)

- [x] cyc_base.zag constructed per PREREG Section 7; C4 diff audit PASS
      (exactly the 3 frozen hunks: 18c18, 127a128,140, 133a147)
- [x] cyc_new.zag driver written per PREREG Section 5; C5 audit PASS
      (0 exec_map, 0 while); C6 audit PASS (no domain-story tokens)
- [x] uni_nomain.zag stripped; cyc_full.zag assembled; all 3 region
      cmps PASS (S1=7697 S2=3332 S3=1413)
- [x] pinned safebin znc build -> cyc_bin; 3/3 runs byte-identical
      (C2), sha256
      `93e5b0d9c7de054d91f5a1d73f0b3fb7358d73a8a17f117ff1f47e6de89320e2`
- [x] Output matches frozen Section 5.1 enumeration exactly:
      ARM=UNI PROB=QC ANS=-2 TRIES=14, WIDEN=1, INTER sequence as
      predicted; census n=5,5,1,1 (teach counts; zero success-recording)
- [x] C1-C6 all PASS -> verdict INFORMATIVE-FAIL (U) per Section 10
      mapping; REPORT.md written
- [x] Two disclosed mechanical fixes: build.sh C4 hunk-header audit;
      cyc_new.zag comment rewording (no code change)
