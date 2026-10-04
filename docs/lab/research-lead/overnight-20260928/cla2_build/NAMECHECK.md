# NAMECHECK: CLA-2 Builder (Step 0, resumed with amended specs)

Date: 2026-09-30. Worker: CLA-2 Builder (resumed).
Task: implement CLA-2 per frozen prereg 24351fd31 + integration amendments
A1-A12 (62e5ebb9f, ALL APPROVED) + ISA boundary ruling (0525377f3, FROZEN)
+ EXECUTE placement amendments A-C (1fc77503b, APPROVED).

## Step 0: Toolchain guard (mandatory, run before any work)

Guard check executed: `which python3 python` returned `/usr/bin/python3`.
Action taken: created `~/workspace/tooling_guard/bin/` containing stub
`python3` and `python` scripts that print a BLOCKED message and exit 1.
Every shell command in this session prepends that directory to PATH via
`export PATH="$HOME/workspace/tooling_guard/bin:$PATH"`, so any accidental
invocation of python3/python fails loudly instead of running. Verified:
`python3 --version` now hits the stub and exits 1.
Commitment: pure Zag for all computational research operations. Shell only
invokes znc, runs binaries, does git ops, and moves/copies files. If a
forbidden executable is invoked, this wave is PROCESS-FAIL.

## Standing rules identified before any work

1. PURE ZAG ONLY for all research logic. No Python, no C, no other language
   for implementation, tests, or analysis. Shell exists only to invoke znc,
   run binaries, do git ops, and move/copy files.
2. Prereg 24351fd31 was committed BEFORE this implementation. Verified via
   git merge-base --is-ancestor. Amendments A1-A12 (62e5ebb9f), ISA ruling
   (0525377f3), and EXECUTE placement A-C (1fc77503b) are all ancestors.
3. Implement EXACTLY what the amended specs specify. No additions, no
   improvements. Zero task-specific handlers, zero hardcoded semantic cases,
   zero modes, zero bridges. Frozen rule: no core operation may encode a
   target-domain regularity detector.
4. Owned path: docs/lab/research-lead/overnight-20260928/cla2_build/ only.
   Do NOT write into continuing_learner/ (prereg territory). Explicit
   pathspecs on add and commit.
5. Do NOT access sealed FW1-FW9 world files. Builders stay blind.
6. Contaminated paper docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md:
   never edited, never cited as evidence. Zero-diff verified at commit.
7. No em dashes in any documentation. Shell-only byte check.
8. Commits stay local. Nothing pushed without Micah's approval.
9. Compiler workaround (AGENTS.md 2026-09-30): never construct function-local
   slices with as *i32; use u8-backed cells with little-endian get32/set32.
10. Python-mirror-developed logic may NOT be adopted. This implementation is
    derived independently from the frozen spec texts.
11. Prior builder started this lane (875-line cla2.zag + tests) against the
    UNAMENDED prereg and was paused. This worker extends that substrate with
    the approved amendments rather than rewriting, preserving tested code.

## Frozen architecture (amended)

Protected core: 7 primitives (ALLOC, READ, WRITE, LINK, ACTIVATE, DECAY,
EXECUTE). EXECUTE(root, frame) dispatches over closed 4-op ISA
{MOVE, BRANCHEQ, INC, DEC}. Frame-slot indirection replaces the HOLE
sentinel (EXECUTE placement Amendment B supersedes integration A10).
Registers: MISS_POLICY (node 1), POLICY_ROOT (node 0), 4-event context
ring. Signed evidence bid (CONTRADICTS = -1). Trial-based discovery;
finite-difference OUT of the core per the frozen ISA rule.

## Kill bars for this build

K1: prereg + all amendments frozen alone before implementation. Verified.
K2: zero task-specific handlers, zero new hardcoded semantic cases, zero
    modes, zero bridges, zero per-world-type branches in the retention path,
    zero researcher-fixed weight/adaptation targets, zero regularity
    detectors in the core. Verified by source inspection.
K3: pure Zag plus shell orchestration only; zero Python (guard enforced);
    documents dash-clean; contaminated paper untouched; commits local with
    explicit pathspecs under cla2_build/ only.

This file was written before any implementation work began.
