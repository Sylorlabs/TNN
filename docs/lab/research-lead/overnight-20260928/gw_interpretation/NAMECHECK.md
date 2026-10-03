# NAMECHECK: GW Interpreter

## Step 0: Toolchain guard

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 14 allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack), `export PATH="$HOME/safebin"`.
- `which python3 python` returns nothing. Zero forbidden executables invoked.
- No code written or executed. Interpretation only, read-only on all inputs.
- No em dashes in documentation.

## Scope

Interpret the committed GW1-GW8 evaluation (`881fbb3d4`) against the frozen predictions (`e409f5eea`) and the re-clustering draft (`ed2357141`).

## Inputs (read-only)

- `docs/lab/research-lead/overnight-20260928/gw_eval/GW_EVAL_REPORT.md` (score 2/8, per-world results)
- `docs/lab/research-lead/overnight-20260928/postfreeze_adversary/ADVERSARY_DESIGN.md` (frozen predictions)
- `docs/lab/research-lead/overnight-20260928/reclustering/RECLUSTERING_DRAFT.md` (4/9 falsification, R1/R2/R3)
- Three red-team verdicts from parent context: construction `340e94e3e`, inquiry `4e329c772`, revision `687ba0219` (all ATTACK-SUCCESS)
- C0-D analysis from parent context (`8bfb80fdd`): promoted graphs shadow themselves

## Output

- `GW_INTERPRETATION.md` (this task's deliverable)

## Constraints honored

- Owned path only: `docs/lab/research-lead/overnight-20260928/gw_interpretation/`
- Interpretation only, no new data, no evaluation reruns.
- Paper untouched. Sealed FW contents not inspected.
- Nothing pushed.
