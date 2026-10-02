# NAMECHECK: Post-Freeze Adversary (W6, W9)

Date: 2026-09-30. Task: design sealed post-freeze worlds W6 (active inquiry)
and W9 (new representational structure) for the Core Freeze Challenge.
Protocol: FREEZE_PROTOCOL.md frozen at 66e3c3f38. Freeze: 87ac95d08.

## Step 0 name-check (standing rules)

The standing-rules sections at the top of the repo-root LOOP_STATE.md apply
to this adversary task as follows. (1) PURE ZAG ONLY is literal: no Python
anywhere in loop work, and disclosure does not cure use. This task authors
only text world files and markdown; there is no code to write, no analysis
to run, and no fixture generation to perform. The world files are
hand-authored line by line (no generator in any language), and the only
byte check used is the shell-only
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
(2) The contaminated paper
docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md is
never edited, staged, committed, or cited; zero diff is verified before
committing. (3) Commits touch only my owned path
docs/lab/research-lead/overnight-20260928/core_freeze/worlds_adversary/,
always with explicit pathspecs after inspecting git status, because other
workers stage their own files on this shared branch. A live
.git/index.lock is never removed; on lock I wait and retry. All commits
stay local; nothing is pushed. (4) No em dashes or en dashes appear in any
loop document I author. (5) Per protocol section 5 (post-freeze adversary
handoff): I design from the frozen interface spec alone (INTERFACE.md,
REGIONS.md, FREEZE_RECORD.md, FREEZE_PROTOCOL.md). I have not read the
candidate's source, I have had no contact with the candidate builders, and
every mechanism-level claim below rests on interface-level evidence only.
The worlds are committed sealed with sha256 published after the freeze
commit 87ac95d08, content revealed only at run time. The worlds are never
executed against the frozen binary in this task; the run phase is separate.

## Adversary stance

I assume the frozen binary is broken and design worlds that expose it. A
world the candidate passes entirely teaches nothing (protocol section 8).
Both worlds below carry a mechanism-level argument for the predicted
failure, stated before any run. Where the interface itself cannot carry
what the protocol asks for, I say so explicitly and make the degeneracy
measured rather than asserted.
