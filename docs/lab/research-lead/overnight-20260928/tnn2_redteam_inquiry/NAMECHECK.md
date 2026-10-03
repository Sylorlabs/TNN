# NAMECHECK.md: TNN-2 Inquiry Red Team

Date: 2026-09-30. Task: Red-team TNN-2's inquiry mechanism (causal-chain verification + ambiguous/misleading evidence attacks).

## Step 0: Toolchain guard check

Command run: `which python3 python 2>/dev/null; echo "guard-check-done"`

Result: empty (neither resolves). Guard active for this shell.

This is an analysis-only wave: source reading, no compilation, no
test execution, no research computation. Zero forbidden executables
invoked. Target read read-only; never modified.

## Scope

Owned path: `docs/lab/research-lead/overnight-20260928/tnn2_redteam_inquiry/`

Contains: NAMECHECK.md (this file), INQUIRY_REDTEAM.md (report).

Target (read-only): `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
frozen at commit `f4de7ff46`, SHA-256 verified
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.

## Governance

- No em dashes (byte-verified before commit).
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` zero-diff.
- No sealed FW1-FW9 accessed.
- Explicit pathspecs only.
- Target directory untouched (read-only analysis).
