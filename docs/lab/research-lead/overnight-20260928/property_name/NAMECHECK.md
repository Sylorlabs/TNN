# NAMECHECK.md: Property Namer

## Step 0: Toolchain guard (mandatory, recorded before any work)

- Ran safebin setup: `mkdir -p $HOME/safebin`, symlinked allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum), exported `PATH="$HOME/safebin"`.
- `which python3 python` returned nothing (empty output, verified).
- Zero forbidden executables invoked in this task. This task performed file reads and writes only; no code was executed, no binaries run, no sealed world contents inspected.

## Scope

- Task: name and formally define the property TNN-3 must have, per the zero-improvement analysis finding that the TNN-2 diagnosis was pitched at the wrong level (capability missing vs property required).
- Inputs (read-only): zero-improvement analysis (commit `89442946` lineage, `zero_improvement/ZERO_IMPROVEMENT_ANALYSIS.md` as reported by parent), re-clustering draft (`ed2357141`), red-team verdicts (construction `340e94e3e`, inquiry `4e329c772`, revision `687ba0219`), DOF map (`d2af26581`).
- This task adds no implementation, no new data, no sealed content inspection.

## Constraints honored

- Owned path only: `docs/lab/research-lead/overnight-20260928/property_name/`.
- Definition only. No implementation, no evaluation, no score claims.
- Zero em dashes (byte-verified after writing).
- Research paper (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`) untouched.
- No push; local commit only, explicit pathspecs.

## Verdict discipline

- The property definition is a conceptual proposal, not a frozen bar. It is offered as vocabulary for future preregistrations. It does not govern any build until incorporated into a preregistration Micah reviews and freezes.
- The necessity claim rests on the zero-improvement analysis (4/9 byte-identical to TNN-1, zero clusters moved). The sufficiency analysis is explicitly marked as reasoning, not evidence.
