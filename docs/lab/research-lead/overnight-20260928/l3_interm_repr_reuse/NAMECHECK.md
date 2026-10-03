# NAMECHECK: L3-INR prereg freeze (design worker)

Worker: L3-INR design worker (subagent, 2026-10-02). Design only; no
implementation in this task.

## Step 0: Worker toolchain guard (MANDATORY, recorded)

The mandated setup script path
docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
does NOT exist in this checkout (verified: no such file or directory).
The canonical pre-existing safebin at $HOME/safebin was used instead. It
contains 49 tools matching the documented allowed set (coreutils, git,
pinned znc): awk basename bash cat chmod cmp comm cp cut date diff
dirname echo file find git git-receive-pack git-upload-pack grep head join
ln ls mkdir mktemp mv nl od paste printf rm sed sh sha256sum sleep sort
stat strings tail tee timeout touch tr uname uniq wc which xargs znc.
No python3, no python, no other interpreter is present in it.

Verification performed under the safebin PATH (export
PATH="$HOME/safebin") before any other work:

- `which python3` returns nothing.
- `which python` returns nothing.
- `which znc` returns /home/hatch/safebin/znc (pinned compiler,
znc 2026.07.0-dev).

No code was executed in this design task beyond shell builtins, git
worktree administration, and file writes. No shell computation, no
builds, no runs, no binaries. The deliverables (PREREG.md and this file)
were written directly as documentation. Therefore no interpreter of any
kind was invoked for scientific computation, and the toolchain guard is
satisfied both actively (verified above) and vacuously (nothing to guard).

Per Micah's 2026-09-30 governance ruling: any forbidden executable
invocation would make the scientific wave PROCESS-FAIL. None occurred.

Follow-up workers (implementation, adversary, red team) MUST perform the
full safebin Step 0 in their own NAMECHECK.md files before their first
execution. This note does not cover them.

Workspace note: the first worktree attempt at
~/workspace/lane-l3nir-20261002 was abandoned after the path was claimed
by unrelated workspace content (docs/generations, docs/hypotheses)
belonging to another worker; nothing of this lane was written there. This
lane uses ~/workspace/lane-l3inr-20261002 on branch lane-l3inr-20261002,
branched from tnn-native-lab, with its own private index. No other
worker's files were touched.

## Step 1: Scope check

- Design the L3 intermediate-representation experiment as a frozen prereg
that survives the specific L3-REDTEAM attacks that killed C281/C284,
adapted from procedure invention to representational invention.
- Do NOT implement. No .zag source, no binaries, no run logs exist under
l3_interm_repr_reuse/ at freeze time.
- Deliverables: PREREG.md (frozen first), NAMECHECK.md (this file).
- Commit with EXPLICIT pathspecs, PREREG.md + NAMECHECK.md ALONE, on
branch lane-l3inr-20261002 (from tnn-native-lab). Never amend shared
history, never git reset, never push.
- Do not touch TNN_RESEARCH_PAPER_20260929.md or other workers' files.
- No em/en dashes in loop documentation (verified with
worker_snippets/check_no_dash.sh before commit).

## Step 2: Pre-registration

PREREG.md was written and is committed BEFORE any implementation source,
binary, or run log exists. Frozen contents:

- Objective: test runtime invention of a novel intermediate
representation (a directed relational graph over learner-internal entity
ids) against the 12 L3 criteria plus Criterion 0 A through D, with
cross-task reuse (pairwise prediction to total ranking) as the C0-D
evidence. Differentiated from L3-NIV2 (procedure invention, same-function
transfer): this is representational invention with different-task reuse.
- Attack-defeat table: each of the 7 successful L3-REDTEAM attacks (A1,
A2, V1, V2, V3, V4, V5) enumerated with the exact design feature that
defeats or sidesteps it in this design; the 3 failed attacks (A3, A4-byte,
V6) preserved as audit arms.
- Frozen world protocol: two-process LEARNER/WORLD with ACCEPT/REJECT
consequence channel; learner never receives expected values.
- Frozen construction constraints: frozen generic graph machinery, 0 new
opcodes, variable-size edge sets, propose-and-test over complete edge
sets, no per-edge positive-gain requirement, ADD-EDGE/DEL-EDGE operators
(the L2 adaptive-reuse vocabulary applied to structure), DEFINE for named
edge-set slots, disclosed simplicity tie-break, frozen TEST budgets.
- Frozen battery: TREAT arms T1, T2, T3, T3b, T4, T5a, T5b; controls C0,
C1, C2, C3, C4, C5; audits A-INFO, A-TRACE, A-LIT, A-ORDER.
- Adversary generation constraints G1 through G8, including the
post-code-freeze independent adversary, the MAP-insufficiency attestation
(G2), the hop-count exhibits (G1), and the information firewall.
- Kill bars K1 through K12 mapped to the 12 criteria (K12 encodes the
7/12 rule: all bars must pass), plus KC0A through KC0D mapped to
Criterion 0 A through D. Every bar is defined over world consequences
and structural trace properties (event types, parent pointers, edge
counts, shared-edge lineage); no bar references program bytes, edge
encodings, or entity identifiers (anti-V4). The compression bar (|E| <=
10) plus the no-probe trace audit carry the anti-brute-force load for
binary pair outcomes (G7, disclosed).
- K8 operationalized as representation transfer across a surface recode
(T3b) plus task transfer with re-derived queries (T3, with C5 failing);
the difference from L3-NIV2's surface-encoding transfer is stated in the
prereg, not hidden.
- Architecture accounting with a 0-new-machinery budget: 0 new
protected-core ops, 0 new modes/bridges/handlers/routers/semantic
opcodes, 0 new menu entries; 1 new learner-state kind (named edge-set
slot with lineage, explicitly learner-created structure, not machinery).
- Known boundaries, stated honestly: L3-vs-strong-L2 left to the bars;
the simplicity tie-break disclosed as a researcher-chosen pressure with
its failure mode named; adversary independence is procedural; N = 10 and
6 held-out pairs per arm make this a mechanism demonstration, not a
generality proof; infeasibility means BUILD-FAIL, not amendment.
- Frozen sequencing: prereg freeze, then implementation, then code
freeze, then adversary design, then evaluator-mediated results, then
independent red team, then verdict from the frozen bars.
- VOID conditions (terminal; fresh prereg required on violation).
- No hand-derived order, entity set, pair, or edge set appears anywhere
in the prereg. The adversary designs all sealed content post-freeze.

## Step 3: Freeze verification (recorded at commit time)

- New directory l3_interm_repr_reuse/ contains exactly PREREG.md and
NAMECHECK.md; no other files.
- check_no_dash.sh passes on both files.
- git add uses explicit pathspecs for the two files only.
- The freeze commit contains the two files ALONE (verified with git show
--stat HEAD); the commit message marks it local-only, never pushed.
