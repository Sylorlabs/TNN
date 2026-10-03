# Polish Note: Reading Guide GW1-GW8 Clarification

## What was checked

Read `reading_guide/READING_GUIDE.md` (commit `46de16972`) to verify the
GW1-GW8 vs GW1-GW9 clarification is clear and prominent.

## Findings

The guide already contained the correct naming in two places:
1. Section 2 (line 39): "the eight sealed adversarial worlds GW1-GW8,
   designed post-freeze from the public architecture claim" - explicit
   and clear.
2. Section 15 (line 230): "It notes the battery is GW1-GW8 (eight
   worlds), not GW1-GW9." - explicit clarification.

However, the one-line bottom line at the top (line 14), which Micah
reads first, said only "The adversarial generality battery scored 2/8"
without naming the battery explicitly. While "2/8" implies eight
worlds, the explicit "GW1-GW8" label was not present at the entry
point.

## Polish applied

One surgical edit to line 14:
- Before: "The adversarial generality battery scored 2/8."
- After: "The adversarial generality battery (GW1-GW8) scored 2/8."

This makes the correct battery name prominent from the very first line,
matching the explicit naming in section 2. It does not change meaning:
"2/8" already implied eight worlds, and section 2 already named them
GW1-GW8. The edit is clarity polish only.

## Verification

- `grep -n "GW1-GW8"` now shows 3 matches: line 14 (bottom line, new),
  line 39 (section 2), line 230 (section 15).
- `grep -n "GW1-GW9"` shows 1 match: line 231, which is the legitimate
  clarifying note "not GW1-GW9" (not an incorrect battery name).
- No other content was changed. No em dashes added (the edit contains
  only parentheses, letters, and digits).
- Paper untouched.

## Deliverables

- `NAMECHECK.md`: Step 0 toolchain guard record
- `POLISH_NOTE.md`: this file
- Modified: `reading_guide/READING_GUIDE.md` (1 line, clarity polish)

**Verdict: DOC-POLISH-COMPLETE.**
