# NAMECHECK: empty-mask semantics (S1 vs S2)

Date: 2026-10-02. Worker: subsumption-reproduction replacement (empty-mask
discrimination). Lane: `docs/lab/research-lead/overnight-20260928/empty_mask_sem/`.

## Step 0: toolchain guard (mandatory)

Safebin activated at startup:
`$HOME/safebin` contains symlinks for git, znc, sh, bash, ls, cp, mv, rm,
mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack,
git-upload-pack (36 tools). `export PATH="$HOME/safebin"` executed before any
scientific work.

Verification (this session):
- `which python3` returns NOTHING (empty).
- `which python` returns NOTHING (empty).
- `znc` in safebin resolves to the pinned compiler
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1` (2026.07.0-dev).

All scientific computation is pure Zag compiled with the pinned znc. Shell is
used only for: znc invocation, binary execution, git operations, file
movement, checksums. Any forbidden-executable invocation would be
PROCESS-FAIL; none occurred.

## Scope

Decide the S1 vs S2 empty-mask semantics question left open by the
compose-collapse reproduction (branch `repro-compose-collapse`, REPORT.md
Section "Prereg ambiguities", item 3; PREREG_AMEND3.md). Four frozen
discriminating problems (Q1-Q4), two arms (S1 arm, S2 arm) differing by exactly
one source line (the empty-mask effectiveness function, diff-verified), 3/3
byte-identical runs per arm.

## Prior-source disclosure

- Read (read-only, never modified): the original lane
  `compose_collapse/PREREG.md` (Section 3 admission rule and Compatibility
  sentence), and from branch `repro-compose-collapse` the files
  `compose_collapse_repro/REPORT.md` and `compose_collapse_repro/PREREG_AMEND3.md`.
- Read (read-only) for operational semantics:
  `compose_collapse_repro/rr_base.zag` and `compose_collapse_repro/rr_uni.zag`
  (arena layout, fact/behavior/kind/observation mechanics, output idiom). This
  is a follow-up discrimination experiment, NOT an independent reproduction;
  reusing the disclosed operational semantics is intentional so the experiment
  varies only the S1/S2 admission reading. No code was copied verbatim into
  committed lane files without being rewritten in this lane's own files; the
  base file `em_base.zag` is written fresh in this lane following the same
  mechanics.
- The sibling lanes `compose_collapse/`, `compose_collapse_repro/`,
  `mask_transfer/`, and `spec_mask_revision/` were never modified.

## Commit discipline

Commits local only, never pushed. Explicit pathspecs limited to this lane
directory. No `git reset`, no history amendment. Prereg commit (this file +
PREREG.md) strictly precedes any implementation commit.
