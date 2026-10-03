# NAMECHECK: L3-INR implementation worker (fresh implementation)

Worker: L3-INR-IMPL worker (subagent, depth 2/2, 2026-10-02).
Task: implement the frozen L3-INR prereg (K1-K12, KC0A-D), DEV validation
only (no sealed worlds), 3/3 byte-identical runs, commit implementation +
runs + REPORT.md. Work directory: `l3_inr_impl/` (this directory). The
frozen prereg directory `l3_interm_repr_reuse/` is never touched by this
worker.

## Step 0: Worker toolchain guard (MANDATORY, recorded)

Safebin activated at startup: `export PATH="$HOME/safebin"`.
The mandated template path
`docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
does not exist in this checkout; the canonical pre-existing safebin at
$HOME/safebin was used instead (same as the design worker's Step 0).

Verification performed under the safebin PATH before any implementation
work (2026-10-02):

- `which python3` returns nothing.
- `which python` returns nothing.
- `which znc` returns /home/hatch/safebin/znc (pinned compiler,
  znc 2026.07.0-dev, edition 2026).

All scientific computation is implemented in pure Zag and executed via
the pinned znc. Shell is used only for: invoking znc, running compiled
binaries, git operations, file moves/copies, sha256sum digesting, and
text plumbing in the file-mediated driver (no computation). No Python,
no other interpreter is invoked for any research computation at any
point. Per Micah's 2026-09-30 governance ruling, any forbidden
executable invocation would make this wave PROCESS-FAIL. None occurred.

Pinned-znc defect workarounds applied in all new Zag code (per AGENTS.md):
u8-backed cells with ig/put32 helpers (no `as *i32` + slice in fns);
single-buffer output with one raw syscall per line (no _zag_print for
dynamic content); `as []f64` never used on u8 slices; if-nesting kept at
3 or fewer with call results hoisted; no `!(A && B)` in while conditions
(De Morgan form); no hash-table probe loops (linear scans only);
`_zag_malloc(n) as *u8` threaded through (never `[]u8 as *u8`).

## Step 1: Scope check

- Implement LEARNER and WORLD binaries in pure Zag under the frozen
  prereg. Follow the prereg exactly; do not weaken any frozen kill bar.
- DEV validation only: the sealed worlds S1/S2/S3/S1p do not exist yet
  (adversary worker designs them post-code-freeze). This worker runs the
  full arm machinery (T1-T5b, C0-C5) against hand-built DEV worlds
  labeled DEV ONLY, 3/3 byte-identical runs per arm, sha256 digests.
- Never inspect sealed-world contents (none exist at this stage); the
  learner binary never opens a world file (protocol firewall).
- Commits stay local, never push. Explicit pathspecs for git add/commit.

## Step 2: Commit-order self-check (prereg strictly precedes implementation)

- Prereg freeze on this branch: commit ca7cfca77 ("L3-INR: design freeze
  (prereg K1-K12, KC0A-D)... No implementation yet"), containing ONLY
  `l3_interm_repr_reuse/PREREG.md` and `l3_interm_repr_reuse/NAMECHECK.md`.
- The freeze tree is byte-identical to the design lane's freeze commit
  2a0ce93cf: `git diff 2a0ce93cf ca7cfca77 --
  docs/lab/research-lead/overnight-20260928/l3_interm_repr_reuse/` is empty.
- ca7cfca77 is an ancestor of this implementation branch
  (lane-l3inr-impl-20261002, HEAD 2ec76f977): verified with
  `git merge-base --is-ancestor ca7cfca77 HEAD`.
- The implementation commit for this work is a descendant of ca7cfca77,
  so the frozen prereg strictly precedes the implementation.
- The committed PREREG.md/NAMECHECK.md blobs are untouched by this
  worker (verified: `git diff ca7cfca77 HEAD -- <dir>` shows no changes
  to those two files).

Note: the working tree of this lane contains uncommitted files from a
prior implementation attempt under `l3_interm_repr_reuse/` (impl/, dev/,
CODEFREEZE.md, MAP_INVENTORY.md, REPORT.md, run_arm.sh, plus an appended
Step 0 in the working-tree NAMECHECK.md). That attempt never committed.
This worker does not touch, reuse, or repair those files; the fresh
implementation below is written and verified independently in
`l3_inr_impl/`. The prior attempt's REPORT.md is noted as reference
only: it claimed BUILD-PASS on evidence from a binary that could not be
rebuilt, with most arms unvalidated and no 3/3 runs. This worker treats
that claim as unverified.

## Step 3: L2 operator availability (prereg section 10 note)

Searched the repo for a landed stable L2 adaptive-reuse ADD-EDGE/DEL-EDGE
operator set (l2_l3_adv, l2_l3_trunc, l2_l3_spec lanes): none found as a
shared stable operator library. Per prereg section 4(c) and section 9,
ADD-EDGE and DEL-EDGE are implemented here as persistent-state edits over
the learner's edge-set slot, executed through the existing slot store
(the frozen generic machinery). This is the prereg-specified form, not
parallel machinery. Recorded at code freeze; not a BUILD-FAIL (the
operators are available in the specified form).
