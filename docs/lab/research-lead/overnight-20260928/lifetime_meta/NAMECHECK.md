# NAMECHECK: LIFETIME-META-1 (examples-to-criterion decrease with experience)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which perl` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which ruby` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which node` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary; verified 2026-10-03).
- Safebin contents: 49 entries (coreutils, git, awk, sed, grep, cmp, diff,
  sha256sum, znc, ...); no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging,
  znc invocation, binary execution, hashing, git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.
- znc smoke test: compiled `/tmp/lm_smoke.zag` (malloc+slice pattern,
  i64 LCG step, `%` operator, single raw-syscall write) and ran it 3x;
  output 3/3 byte-identical, sha256
  `1466b52c54956bbc555d31a2231533ecd6b59fd33885fa0b57f44a715a0f1c22`
  (`LM1-SMOKE 8`). Toolchain verified before prereg freeze.

## Step 1: Lane location and commit discipline

Lane repo: this directory
(`~/workspace/docs/lab/research-lead/overnight-20260928/lifetime_meta/`),
fresh `git init -b main` 2026-10-03. Nothing is pushed to GitHub;
commits stay local with explicit pathspecs. The prereg-alone-then-
implementation commit order is honored inside this repo: the first
commit contains ONLY PREREG.md (v1) and NAMECHECK.md (Step 0); the
second commit contains ONLY the PREREG.md v2 amendment (+ this
NAMECHECK note). The Zag source, binaries, run logs, and REPORT.md
come in later commits, all strictly postdating the v2 commit.

## Prereg amendment record

- v1 -> v2 (before any implementation, no data seen): problem family
  changed from hidden 2-step register programs to biased-coin bias
  learning; learner changed from form-pair inventory + move-to-front to
  shrinkage estimator + learned prior mean; all bars rewritten. Cause:
  design analysis proved the program family has zero headroom (naive
  learner identifies every accepted dominant episode in exactly 2
  examples; see PREREG Section 0). Amendment is transparent and
  re-freezes the design; v1 remains in git history.

## Build record

- 2026-10-03: `lm.zag` written (6798 bytes, neutral identifiers; B6/B7
  audits pass). Compiled with pinned safebin znc -> `lm_bin`
  (33776 bytes); one A0101 analyzer warning, confirmed false positive
  (max flip index 56+e*300+299, in bounds).
- 2026-10-03: 3/3 runs byte-identical, sha256
  `17eedbd39d72d0ee111de6a9da18148d5eb80f34247aba7f57770140e5b4480b`
  (run1/2/3.txt).
- 2026-10-03: REPORT.md written. Frozen verdict: NO META-LEARNING
  (net-advantage claim; B5a FAIL -39 < 150). B5b (within-learner
  decrease) PASSED 226 >= 75; control shows no decrease trend.
  Diagnosis: outlier negative transfer (predicted direction, larger
  than estimated) + overshoot coupling under shared flips (empirically
  confirmed on E02's trajectory) + prereg threshold miscalibration.
  PRNG audited sound via independent /tmp program.
- Commit order self-check: v1 prereg 174f6d0, v2 amendment 80d1edb,
  both strictly before this implementation commit. PASS (B1).
