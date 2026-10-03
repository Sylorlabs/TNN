# NAMECHECK (Step 0) - L3B Constructor-Redesign Builder

Standing rules name-check (LOOP_STATE.md top, four sections):

(1) PURE ZAG ONLY: every line of implementation, build, runs, and analysis
in this task is pure Zag plus POSIX shell; zero Python at any stage,
including verifiers, harnesses, and byte checks.

(2) Shell-only byte checks: em/en dash checks use only
worker_snippets/check_no_dash.sh, never python3.

(3) Pure-Zag red-line scope: fixture and episode provisioning counts as
loop work, so the A2/B2 episode lists are frozen literals in the Zag
source, produced by no external tool.

(4) Fork testing is a standing loop rule owned by the fork-battery worker;
this task creates no branches or forks.

Git discipline: this prereg is committed alone before any implementation
file exists (merge-base verified at commit time). Explicit pathspecs on
every git add and git commit, with git status inspected first. The
prohibited paper
docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
is never touched, staged, or committed. On a live .git/index.lock I wait
and retry; I never remove it.

u8-backed cells only in all new Zag code (never `as *i32` slices inside
functions; see ~/AGENTS.md toolchain lesson).
