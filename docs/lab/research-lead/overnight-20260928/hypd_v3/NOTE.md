# NOTE: PREREG_HYPD_V3_CLEANED.md (HypD v3 prereg hygiene copy)

## What this file is

`PREREG_HYPD_V3_CLEANED.md` is a dash-hygiene copy of the frozen HypD v3
preregistration document `PREREG_HYPD_V3.md` committed at `3847065e2`
("Prereg: Hypothesis D v3 (selection + carry-over fixes; FROZEN; committed
alone)"). It exists for future reference only.

## Why it exists

The frozen original contains one em dash (U+2014) at line 142:

    would show Fix 2 was sufficient and Fix 1 unnecessary -- reported
    honestly either way.

Under the literal standing rule "no em dashes in loop documentation," this
is a process blemish. The cleaned copy replaces that em dash with a plain
hyphen and is otherwise byte-identical to the frozen original (verified by
diff: exactly one line differs). Shell-only `check_no_dash.sh` passes on
the cleaned copy.

## What this file is NOT

- It does NOT amend, rewrite, or replace the frozen commit `3847065e2`.
  That commit is immutable; its blemish stands as a historical record.
- It does NOT change the C72 ledger verdict. HYPD-V3-PASS stands as
  SURVIVES (bounded L2), with the em-dash blemish recorded in the
  canonical ledger entry.
- It does NOT alter any scientific content, number, or kill bar. Only
  the single dash byte sequence was changed.

## Remaining historical dash

The companion file `NAMECHECK.md` at the frozen commit `3847065e2`
carries one em dash at line 10 ("no Python anywhere in my work -- not in
the implementation..."). It is preserved as committed; this hygiene task
was scoped to the prereg document only. Any future use of that text should
apply the same replacement.

## Provenance

Created 2026-09-30 by the HypD v3 Prereg Document Cleaner. Pure shell
work (git show, sed, grep, sh); zero Python. Contaminated paper
`TNN_RESEARCH_PAPER_20260929.md` untouched.
