# NAMECHECK: Floor Spec Erratum Author

## Step 0: Toolchain guard

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 18 allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack), `export PATH="$HOME/safebin"`.
- `which python3 python` returned nothing. Zero forbidden executables invoked.
- Record: guard-check-done.

## Scope

Author a transparent erratum for the frozen floor specification. Erratum ONLY. Do NOT edit `floor_preserve/FLOOR_SPEC.md` or any frozen file.

## Input provenance

- Frozen floor spec: commit `f383dd11c` ("FLOOR-SPEC-COMPLETE: TNN-3 preservation spec"), file `docs/lab/research-lead/overnight-20260928/floor_preserve/FLOOR_SPEC.md`.
- Error identified by doc audit: `docs/lab/research-lead/overnight-20260928/doc_audit/DOC_AUDIT.md` (committed via sweep into `e6261f31e`).
- Micah's ruling (2026-10-01): add a transparent erratum stating 6 capabilities and 7 verification tests; do not alter frozen history silently.
- All spec content verified read-only via `git show f383dd11c:...` (no working-tree reads of frozen content, no edits).

## Constraints

- Do NOT edit `floor_preserve/FLOOR_SPEC.md`.
- Do NOT edit any frozen file.
- Erratum is a separate document in `floor_erratum/`.
- No em dashes.
- Paper untouched (`TNN_RESEARCH_PAPER_20260929.md`).
- No sealed contents inspected.
- Nothing pushed; commit local on `tnn-native-lab` with explicit pathspecs.

## Verdict discipline

FLOOR-ERRATUM-COMPLETE on commit of the two deliverable files.
