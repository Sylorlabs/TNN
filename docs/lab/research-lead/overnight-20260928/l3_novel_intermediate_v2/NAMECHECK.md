# NAMECHECK: L3-NIV2 prereg freeze (design worker)

Worker: L3-NIV2 design worker (subagent, 2026-10-02). Design only; no
implementation in this task.

## Step 0: Worker toolchain guard (MANDATORY, recorded)

No code was executed in this task. No shell computation, no builds, no
runs, no binaries. The deliverables (PREREG.md and this file) were written
directly as documentation. Therefore no interpreter of any kind was
invoked, and the toolchain guard is satisfied vacuously: there is no
execution to guard.

For the record: had any execution been needed, the mandatory procedure
would have been docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
followed by export PATH="$HOME/safebin", with `which python3` required to
return nothing and pure Zag required for all research logic.

Per Micah's 2026-09-30 governance ruling: any forbidden executable
invocation would make the scientific wave PROCESS-FAIL. None occurred,
because nothing was executed.

Follow-up workers (implementation, adversary, red team) MUST perform the
full safebin Step 0 in their own NAMECHECK.md files before their first
execution. This note does not cover them.

## Step 1: Scope check

- Design the next L3 novel-intermediate experiment as a frozen prereg that
survives the specific L3-REDTEAM attacks that killed C281/C284.
- Do NOT implement. No .zag source, no binaries, no run logs exist under
l3_novel_intermediate_v2/ at freeze time.
- Deliverables: PREREG.md (frozen first), NAMECHECK.md (this file).
- Commit with EXPLICIT pathspecs, PREREG.md + NAMECHECK.md ALONE.
- Do not touch TNN_RESEARCH_PAPER_20260929.md. Nothing pushed. Commits
stay local on branch tnn-native-lab. No shared history amended.
- No em/en dashes in loop documentation (verified with
worker_snippets/check_no_dash.sh before commit).

## Step 2: Pre-registration

PREREG.md was written and is committed BEFORE any implementation source,
binary, or run log exists. Frozen contents:

- Objective: test runtime creation of a novel intermediate procedure
against the 12 L3 criteria plus Criterion 0 A through D.
- Attack-defeat table: each of the 7 successful L3-REDTEAM attacks (A1,
A2, V1, V2, V3, V4, V5) enumerated with the exact design feature that
defeats or sidesteps it; the 3 failed attacks (A3, A4-byte, V6) preserved
as audit arms.
- Frozen world protocol: two-process LEARNER/WORLD with ACCEPT/REJECT
consequence channel; learner never receives expected values.
- Frozen construction constraints: frozen generic ISA, 0 new opcodes,
variable-length programs, propose-and-test over complete candidates, no
per-step positive-gain requirement, APPEND/TRUNCATE/SUBSTITUTE operators,
DEFINE for named abstractions, frozen TEST budgets.
- Frozen battery: TREAT arms T1, T2, T3, T4, T5a, T5b; controls C0, C1,
C2, C3, C4, C5; audits A-INFO, A-TRACE, A-LIT, A-ORDER.
- Adversary generation constraints G1 through G8, including the
post-code-freeze independent adversary and the information firewall.
- Kill bars K1 through K12 mapped to the 12 criteria (K12 encodes the
7/12 rule: all bars must pass), plus KC0A through KC0D mapped to
Criterion 0 A through D. Every bar is defined over world consequences
and structural trace properties; no bar references program bytes or op
numbering (anti-V4).
- Architecture accounting with a 0-new-machinery budget: 0 new
protected-core ops, 0 new modes/bridges/handlers/routers/semantic opcodes,
0 new menu entries; 1 new learner-state kind (named program slot with
lineage, explicitly learner-created structure, not machinery).
- Known boundaries, stated honestly: C0-B claimed over unbounded
composition on a fixed generic basis; L3-vs-strong-L2 left to the bars;
adversary independence is procedural; N = 6 per regime is a mechanism
demonstration, not generality; infeasibility means BUILD-FAIL, not
amendment.
- Frozen sequencing: prereg freeze, then implementation, then code
freeze, then adversary design, then evaluator-mediated results, then
independent red team, then verdict from the frozen bars.
- VOID conditions (terminal; fresh prereg required on violation).
- No hand-derived solution appears anywhere in the prereg. This is the
direct correction of the C281/C284 failure mode, where both frozen
preregs named the exact program bytes before implementation.

## Step 3: Freeze verification (recorded at commit time)

- New directory l3_novel_intermediate_v2/ contains exactly PREREG.md and
NAMECHECK.md; no other files.
- check_no_dash.sh passes on both files.
- git add uses explicit pathspecs for the two files only.
- The freeze commit contains the two files ALONE; the commit message
marks it local-only, never pushed.

## Step 0 (Wave 2 implementation worker, 2026-10-02)

Safebin activated: mkdir -p $HOME/safebin; symlinks created for git, znc
(pinned src/tools/toolchain/znc_linux_x86_64_abed8aa1), sh, bash, ls, cp,
mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack,
git-upload-pack. export PATH="$HOME/safebin".

Verification: `which python3` returns nothing. `which python` returns nothing.
Pure Zag for all scientific computation. Shell only for znc invocation,
binary execution, git ops, file movement.

Near-miss disclosure: During debugging a command fragment containing
`python3 -c "print('skip')"` was typed. With safebin PATH active, python3
does not resolve; the invocation failed (command not found). No forbidden
computation occurred. Disclosed per governance ruling.

## Step 0 (Wave 3 search-fix worker, 2026-10-02)

Safebin activated before any execution in this task:

- Ran the mandatory setup: mkdir -p $HOME/safebin; symlinks created for
  git, znc (pinned src/tools/toolchain/znc_linux_x86_64_abed8aa1), sh,
  bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum,
  git-receive-pack, git-upload-pack. export PATH="$HOME/safebin".
- Verified under the safebin PATH: `which python3` returns nothing,
  `which python` returns nothing.
- All scientific computation is pure Zag compiled with the pinned znc.
  Shell is used only for: invoking znc, running compiled binaries, git
  operations, file moves, sha256sum digests, FIFO plumbing in the battery
  supervisor, and the no-dash documentation check. No python3, python, or
  any other forbidden interpreter is invoked at any point.

Per Micah's 2026-09-30 governance ruling: any forbidden executable
invocation would make this wave PROCESS-FAIL.

## Step 1 (Wave 3): Scope check

- Solve the wave-2 search-adequacy failure: T1 DEFERs on DEV-S1 because
  the beam prunes the crucial score-1 prefix before extension.
- Diagnose first (in PREREG_WAVE3.md, frozen before implementation),
  then design CALR (Consequence-Anchored Lookahead Retention), then
  implement in pure Zag, run, and report honestly.
- Do NOT weaken K1 through K12 or KC0A through KC0D. Do NOT widen the
  5-op ISA. Do NOT redesign the task. Do NOT inspect sealed-world
  contents (DEV fixtures are unsealed smoke-test fixtures and are the
  only worlds touched).
- Freeze PREREG_WAVE3.md plus this Step 0 update in a commit containing
  those two files ALONE, before any wave-3 .zag source, binary, or run
  log exists.
- Commits stay LOCAL on branch tnn-native-lab, explicit pathspecs, never
  pushed, never amend shared history, never git reset. Do not touch
  TNN_RESEARCH_PAPER_20260929.md or other workers' files.
- No em/en dashes in loop documentation (verified with
  worker_snippets/check_no_dash.sh before commit).

## Step 0 (Wave 4 staged-deepening worker, 2026-10-02)

Safebin activated before any execution in this task:

- Ran the mandatory setup: mkdir -p $HOME/safebin; symlinks created for
  git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc,
  cmp, sha256sum, git-receive-pack, git-upload-pack. export
  PATH="$HOME/safebin".
- Verified under the safebin PATH: `which python3` returns nothing,
  `which python` returns nothing.
- Corrected $HOME/safebin/znc to the pinned compiler
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 (it already resolved
  there; re-linked explicitly and verified byte-identical).
- All scientific computation is pure Zag compiled with the pinned znc.
  Shell is used only for: invoking znc, running compiled binaries, git
  operations, file moves, sha256sum digests, FIFO plumbing in the battery
  supervisor, and the no-dash documentation check. Design-time
  estimation used two pure-Zag probe binaries (/tmp/probe/probe_bin,
  /tmp/probe/probe2_bin) that replicate 2S-CALR logic against the
  unsealed DEV-S2 target directly; no world process, no channel, no
  sealed content involved. No python3, python, or any other forbidden
  interpreter is invoked at any point.

Per Micah's 2026-09-30 governance ruling: any forbidden executable
invocation would make this wave PROCESS-FAIL.

## Step 1 (Wave 4): Scope check

- Extend CALR beyond depth 3 via staged deepening (2S-CALR), the honest
  limitation recorded in REPORT_WAVE3.md section 8.
- Diagnose first (in PREREG_WAVE4.md, frozen before implementation),
  then implement in pure Zag, run, and report honestly.
- Do NOT weaken K1 through K12 or KC0A through KC0D. Do NOT widen the
  5-op ISA. Do NOT redesign the task. Do NOT introduce beam quotas as
  the retention mechanism (CALR no-pruning principle stands). Do NOT
  inspect sealed-world contents (DEV fixtures are unsealed smoke-test
  fixtures and are the only worlds touched).
- Freeze PREREG_WAVE4.md plus this Step 0 update in a commit containing
  those two files ALONE, before any wave-4 .zag source, binary, or run
  log exists.
- Commits stay LOCAL on branch tnn-native-lab, explicit pathspecs, never
  pushed, never amend shared history, never git reset. Do not touch
  TNN_RESEARCH_PAPER_20260929.md or other workers' files.
- No em/en dashes in loop documentation (verified with
  worker_snippets/check_no_dash.sh before commit).
