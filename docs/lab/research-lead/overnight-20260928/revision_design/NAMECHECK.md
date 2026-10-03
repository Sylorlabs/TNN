# NAMECHECK: Revision Design Drafter

**Step 0: Toolchain guard (mandatory, verified before any work)**

- Ran the safebin setup: created `$HOME/safebin`, symlinked the allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp,
  sha256sum, git-receive-pack, git-upload-pack), exported `PATH="$HOME/safebin"`.
- `which python3 python` returned nothing under the safebin PATH.
- Zero forbidden executables invoked during this task. Pure read (git show) and
  file writes only. No compilation, no binary execution, no world runs.

**Scope:** Draft the TNN-3 revision design from the architecture advisor's
guidance (commit `5a009ff87`).

**Inputs (read-only):**
- `docs/lab/research-lead/overnight-20260928/revision_advice/REVISION_ADVICE.md`
  (commit `5a009ff87`, read via `git show`, not modified)
- `docs/lab/research-lead/overnight-20260928/bug_report/REVISION_BUG.md`
  (referenced by the advice as Constraint A source)

**Deliverables:**
- `REVISION_DESIGN.md`: the design draft (design only, no implementation)
- This file.

**Verdict discipline:** The design is DRAFT-NOT-FROZEN. It adopts no kill bar,
freezes nothing, authorizes no implementation. It becomes binding only if a
TNN-3 preregistration references it and Micah approves.

**Constraints honored:**
- Owned path only:
  `docs/lab/research-lead/overnight-20260928/revision_design/`
- Draft only. No source modified, no binary built, no Zag compiled, no
  experiment run, no sealed asset inspected (FW/GW/H2 contents untouched).
- No em dashes in any documentation (byte-verified before commit).
- Paper untouched (`TNN_RESEARCH_PAPER_20260929.md` not opened).
- Nothing pushed. Local commit only.
- No banked decision made (protected-core Alt C / structural ops untouched).

**Verdict: REVISION-DESIGN-COMPLETE.**
