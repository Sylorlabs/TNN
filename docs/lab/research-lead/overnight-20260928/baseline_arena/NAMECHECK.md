# NAMECHECK.md: Fair Baseline Arena Designer

## Step 0: Toolchain Guard (mandatory)

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 21 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc,
  cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` before all work.
- Verification: `which python3 python` returned nothing. Output was the
  bare string `guard-check-done` with no interpreter paths.
- Zero forbidden executables invoked in this wave. All work below is
  document authoring via file writes plus git operations.
- This worker is DESIGN-ONLY: no implementation, no API calls, no model
  evaluations, no binaries built, no sealed contents inspected.

## Scope

- Task: Design the TNN-vs-LLM fair competitive evaluation arena.
  Frontier backlog Q16.
- Parent: main agent (research coordinator), session
  7878ec62-13a6-4406-9b10-b60d9b07a8df.
- Branch: `tnn-native-lab`, repo `~/workspace/tnn-rsi`.
- Deliverables (this directory only):
  - `NAMECHECK.md` (this file)
  - `BASELINE_ARENA_DESIGN.md` (DRAFT-NOT-FROZEN)

## Input provenance

- Micah's standing requirements (from parent handoff, 2026-10-01):
  - "always compare against serious baselines, never a deliberately
    crippled LLM"
  - "The TNN-vs-LLM arena needs a capable non-crippled baseline,
    15 measured capabilities, honest resource charging, and capability
    curves rather than a superiority declaration."
  - GPT-3-class systems as a milestone: "a system a rational user would
    prefer over them for broad intelligent work, focusing on capabilities
    GPT-3 handles awkwardly (persistent one-shot learning, long-lived
    corrections, learner-owned memory, traceable beliefs, conflicting
    hypotheses, active inquiry, invention, structural adaptation,
    continuing life), with fair comparison."
  - North star: "demonstrate capability/cost advantages against serious
    LLM baselines."

## Constraints honored

- Design only. No model names pinned (capability floors specified
  instead, since model names change).
- DRAFT-NOT-FROZEN: this design is not a preregistration and freezes
  nothing.
- Zero em dashes (byte-verified before commit).
- Paper untouched. Nothing pushed. Commits local only.
- No sealed H2/FW world contents opened or referenced beyond their
  public bar summaries already in the parent's handoff.

## Verdict

BASELINE-ARENA-DESIGN-COMPLETE (pending parent review).
