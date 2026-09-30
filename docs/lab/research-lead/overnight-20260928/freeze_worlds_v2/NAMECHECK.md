# STEP 0 NAME-CHECK: Fresh Adversarial Worlds Designer (FW1-FW9)

Date: 2026-09-30. Task: design the second-generation adversarial worlds for the Core Freeze Challenge.

Standing rules from the top of LOOP_STATE.md that apply to this task, and how they are honored:

(1) PURE ZAG ONLY. No Python anywhere in loop work. This task produces pure text and markdown design documents only. No Python is used or will be used for design, hashing, or verification. Shell (sh, sha256sum) only.

(2) Shell-only byte checks. Dash cleanliness is verified with docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh, never python3. Disclosure does not cure use.

(3) No em dashes in loop documentation. This document and WORLD_DESIGN.md use hyphens only.

(4) Owned paths and explicit pathspecs. All writes and commits stay inside docs/lab/research-lead/overnight-20260928/freeze_worlds_v2/ with explicit pathspecs. git status is inspected before every commit. No other worker's files are touched.

(5) The contaminated paper (docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md) is never edited, staged, cited as evidence, or modified in any way.

(6) Commits stay local. Nothing is pushed.

(7) Preregistration precedes implementation. This is a DESIGN task only. No world files are implemented here. The design must be reviewed before any implementation task begins. Sealing (hash commitment) happens after implementation, before any core changes.

Name-check written before any design work began. Designer: Fresh Adversarial Worlds Designer.

---

# STEP 0 NAME-CHECK: FW1-FW9 World Sealer (sealing phase)

Date: 2026-09-30. Task: implement the nine FW world files from WORLD_DESIGN.md (approved at 200387b42; Micah approved FW1-FW9 with the restriction that they are sealed evaluator/adversary assets, never design hints), verify, seal with hashes in SEAL.md, commit.

Standing rules honored:

(1) PURE ZAG ONLY for all research logic. No Python, no C/C++, no JavaScript, no Rust anywhere: not for world generation, not for the FW6 responder, not for hashing, not for id-disjointness verification, not for DAG reachability computation. Per Micah's 2026-09-30 tooling ruling, all computation (generation, parsing, verification, hashing) is written in Zag. Shell exists only to invoke znc, execute Zag binaries, run git operations, and move/copy files or clean scratch directories.

(2) Shell-only byte checks. Dash cleanliness verified with the shell-only check_no_dash.sh. Disclosure does not cure use.

(3) No em dashes in loop documentation. Hyphens only.

(4) Owned paths and explicit pathspecs. All writes and commits stay inside docs/lab/research-lead/overnight-20260928/freeze_worlds_v2/ with explicit pathspecs. git status inspected before every commit. No other worker's files touched. Build sources live in seal_src/; sealed worlds in worlds/.

(5) The contaminated paper (docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md) is never edited, staged, cited as evidence, or modified. Verified zero-diff before commit.

(6) Commits stay local. Nothing is pushed.

(7) These worlds are EVALUATOR/ADVERSARY ASSETS. After sealing, substrate builders remain blind to the hidden world details. No tuning of learner architecture to FW1-FW9.

(8) The design was reviewed and approved before this implementation began. Implementer decisions forced by design ambiguities are documented in SEAL.md, never silently resolved.

Name-check written before any sealing work began. Sealer: FW1-FW9 World Sealer.
