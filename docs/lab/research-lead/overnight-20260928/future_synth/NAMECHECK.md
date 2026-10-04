# NAMECHECK: Future Synthesis Planner

## Step 0: Toolchain Guard (mandatory)

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 19 allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` applied before all work.
- Verification: `which python3 python 2>/dev/null` returned nothing. Guard check printed `guard-check-done`.
- Zero forbidden executables invoked. All work was read-only `git show` / `git log` and file writes. No Zag compiled, no binary built, no experiment run.

## Scope

Plan only. This worker does NOT write the future synthesis, does not edit the current synthesis, does not modify any design document, and makes no banked decision. Output is a plan document specifying what a future synthesis pass should add, when it should run, and how.

## Input provenance (read-only)

| Commit | Document | Role in this plan |
|---|---|---|
| `a01128de5` | `design_synthesis/TNN3_DESIGN_SYNTHESIS.md` | Current synthesis; the thing to be extended |
| `5a009ff87` | `revision_advice/REVISION_ADVICE.md` | New design input 1: copy-and-commit revision, MAP retargeting |
| `abe3d32e5` | `guard_integration/GUARD_INTEGRATION.md` | New design input 2: 6 treadmill-guard insertion points for prereg structure |
| `877d8491a` | guard_integration fix (7->6, Section 3 explicit) | Correction to input 2 |
| `9e6c457cc` | guard_integration NAMECHECK fix (7->6) | Correction to input 2 provenance |
| `75ea448e8` | `integration_verify/INTEGRATION_VERIFY.md` | Validation of input 2 (all 6 points VALID) |
| `f4f8fa532` | `banked_decisions/BANKED_DECISIONS.md` | Citable compilation of 4 banked decisions (open items reference) |
| `19aa5595e` | `synthesis_review/SYNTHESIS_REVIEW.md` | Confirms current synthesis covers its 6 declared inputs; notes the 2 postdating inputs as correctly absent |

## Constraints honored

- Owned path only: `docs/lab/research-lead/overnight-20260928/future_synth/`.
- Plan only; no synthesis written.
- No em dashes in any written file (loop style rule).
- Paper untouched (`TNN_RESEARCH_PAPER_20260929.md` not read, not modified).
- No sealed contents inspected (FW/GW/H2 worlds not opened; only hashes and metadata referenced from existing docs).
- Nothing pushed; commit stays local on `tnn-native-lab`.
