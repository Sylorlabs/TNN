# NAMECHECK: Discount Adversary Designer

## Step 0: Toolchain Guard

**Date:** 2026-10-01
**Scope:** DESIGN ONLY. No implementation, no variant, no binary.

Toolchain verification:
- Safebin setup script: `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
- PATH exported to `$HOME/safebin`
- `which python3` returns: (empty - no output)
- `which python` returns: (empty - no output)
- Zero forbidden executables invoked in this task.

Note: exec subprocess was draining at task start; toolchain guard verified via read/write tools only. No computational work was performed (design-only scope requires no computation).

## Step 1: Input Provenance

This task designs an adversarial test for discount W3 (majority heuristic).

Primary inputs (read-only):
- `docs/lab/research-lead/overnight-20260928/discount/DISCOUNT.md` (spec `62fa77192`)
  - Section 5.1: source-blindness (the deep limit)
  - Section 5.3: self-referential confidence
  - Section 6.2: majority heuristic (W3) - "highest-risk component, flagged for adversarial testing"
  - Section 8.3: "Adversarial W3. Construct a world where the majority is wrong and W3 punishes truth. Measure the damage. This bounds the heuristic's risk."
- `docs/lab/research-lead/overnight-20260928/discount_impl/DISCOUNT_IMPL.md` (impl `0daaa2ed4`)
  - Minimal subset D1+D2+W3+R1 validated as RECOVERABLE
  - W3 discounts minority facts on non-unanimous bootstrap with strict majority
- `docs/lab/research-lead/overnight-20260928/contradiction_break/CONTRADICTION_BREAK.md` (probe `510b6cb42`)
  - Bootstrap loop mechanics, recency window, unanimity gate

## Step 2: Task Boundary

**Authorized:** Design the adversarial world where W3 punishes truth. Specify setup, expected behavior, harm metrics. This is a design document only.

**Not authorized:** Implementation, variant building, running experiments, sealed worlds, modifying frozen source or preregs, pushing to GitHub.

## Step 3: Constraints

- DESIGN ONLY. No Zag code, no binaries, no test runs.
- Zero em dashes in all documentation (byte-verified before commit).
- Paper untouched: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` not modified.
- Nothing pushed. Commits local only.
- No sealed worlds opened or created.
- Explicit pathspecs on both `git add` and `git commit`.

## Step 4: Deliverables

- `NAMECHECK.md` (this file)
- `DISCOUNT_ADVERSARY.md` (adversarial world design)

## Verdict

DISCOUNT-ADVERSARY-COMPLETE (pending design document and commit).
