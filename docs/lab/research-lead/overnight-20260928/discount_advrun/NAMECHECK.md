# NAMECHECK: Discount Adversary Runner

## Step 0: Toolchain Guard

- Safebin configured: `$HOME/safebin` with 36 allowed tools.
- `which python3 python` returns nothing (verified 2026-10-01).
- Zero forbidden executables invoked.
- Pure Zag via pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Shell used only for: invoking znc, running binaries, git operations, moving/copying files.

## Scope

- UNFROZEN VARIANT ONLY. Frozen TNN-2 source untouched.
- Measurement only: runs the majority-wrong adversarial world on the discount variant.
- No implementation changes to the discount mechanism (reuses `0daaa2ed4` pilot).
- No sealed worlds. No paper modifications. Nothing pushed.

## Input Provenance

- Discount adversary design: `b0cd36859` (`discount_adversary/DISCOUNT_ADVERSARY.md`).
- Discount implementation: `0daaa2ed4` (`discount_impl/`, specifically `di_variant.zag` reused verbatim).
- Discount specification: `62fa77192` (`discount/DISCOUNT.md`).
- Contradiction-break probe: `510b6cb42` (battery structure reference).

## Constraints Honored

- UNFROZEN ONLY. Frozen source hash verified before/after (read-only).
- Pure Zag. Zero em dashes and zero en dashes in deliverables (byte-verified).
- Research paper untouched (`TNN_RESEARCH_PAPER_20260929.md`).
- No sealed worlds opened or created.
- Nothing pushed to GitHub (local commits only).
- Explicit pathspecs on `git add` and `git commit`.

## Verdict

DISCOUNT-ADVRUN-COMPLETE (pending execution).
