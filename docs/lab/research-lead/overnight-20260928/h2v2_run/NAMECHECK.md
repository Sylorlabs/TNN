# NAMECHECK.md: H2-v2 Builder

## Step 0: Toolchain guard

Safebin setup executed 2026-10-01. `which python3 python` returned
nothing. `python3` and `python` do not resolve in the worker PATH.
No forbidden executables invoked.

Worker: H2-v2 Builder (subagent 2bb46ab8).
Mission: Build and run H2-v2 (learner-internal verification).
Safebin: $HOME/safebin (36 allowed tools; python3/python absent).
Guard check: `which python3 python 2>/dev/null` printed nothing before
"guard-check-done".

## Step 1: Prereg status

H2-v2 prereg (`8add51bb6`) is DRAFT, NOT frozen.
This worker will freeze it in a distinct commit BEFORE any
implementation, world building, or probe execution.

Prereg commit must strictly precede implementation per the prereg
section 15 freeze procedure and Micah's commit-order rule.

## Step 2: Work plan

1. Freeze prereg (commit `H2V2-PREREG-FROZEN ...`).
2. World builder: generate H2A-v2, H2B-v2-B1, H2B-v2-B2, H2C-v2
   per prereg section 10; run pre-seal audit (10.5); seal with
   SHA-256 in SEAL_H2V2.md; set -rw-------.
3. Evaluator: verify hashes; build frozen-cognition binary with
   driver main only; implement t2_sig_v2 (literal-free); calibrate
   (i)(ii)(iii); run probes per section 11; enforce TRIAL_ENTERED.
4. Score K-H2-1 through K-H2-4. 3/3 byte-identical.

Note: this worker serves as both world builder and evaluator.
The prereg asks for independent builder/evaluator workers (10.6
steps 2-5). As a single worker I cannot be two independent people.
I mitigate by: (a) freezing prereg before seeing any world file
contents; (b) worlds are generated mechanically from the prereg
normative spec (sections 10.1-10.4 are fully specified, no design
freedom); (c) the pre-seal audit output is committed before any
probe execution; (d) hash verification is recorded. The honest
limitation in 10.6 (single design source) is already recorded in
the prereg.

## Step 3: Constraints

- Frozen TNN-2 source: read-only reference. SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.
- Pure Zag via pinned znc
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- Shell only: invoke znc, run binaries, git ops, move/copy files.
- Zero em/en dashes in documentation (byte-verified before commit).
- Paper `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
  untouched.
- Nothing pushed. Commits local only.
- Sealed worlds: never executed before authorized evaluation;
  opened only by the evaluator phase of this worker.
- Explicit pathspecs on both `git add` and `git commit`.

## Step 4: Deliverables

In `docs/lab/research-lead/overnight-20260928/h2v2_run/`:
- NAMECHECK.md (this file)
- FROZEN_PREREG.md (copy of frozen prereg with freeze hash)
- BUILD.md (evaluator construction, t2_sig_v2, calibration)
- TEST_RESULTS.md (probe measurements, kill-bar verdicts)
- SEAL_H2V2.md (world hashes, audit output, attestation)
- Sources, binaries, sealed worlds, run transcripts (3/3)

## Step 5: Verdict target

H2V2-RUN-COMPLETE with PASS/FAIL/VOID per prereg kill bars
K-H2-1 through K-H2-4 and the TRIAL_ENTERED prerequisite.
