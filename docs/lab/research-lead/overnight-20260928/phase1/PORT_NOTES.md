# PHASE 1 AUDIT -- ZAG PORT NOTES

`audit_v3.py` -> `audit_struct.zag`. This audit gates the lane's most
load-bearing mechanical claim, so it must be re-derivable in pure Zag.

## RESULT: the bound is reproduced

```
.zag sources listed          : 1040
sources containing fn main  : 610
structural writers found    : 574
GENUINE structural levers   : 0
RESULT: 0 structural writers read learner state.
```

## THE WRITER COUNT DIFFERS, AND IT MATTERS WHICH IS WHICH

| auditor | writers found |
|---|---|
| `audit_v3.py` | 137 |
| `audit_struct.zag` | **574** |

Cause: the Python detector requires a function header to match on **one
line** (`^fn\s+(\w+)\s*\(([^)]*)\)[^{]*\{`). The Zag scanner accepts
multi-line parameter lists and a brace on a later line, so it finds more
functions containing a structural sink.

**This does not weaken the claim, it strengthens it.** The claim under
test is `levers == 0`. The Zag port returns 0 while examining **574**
writers instead of 137, so the negative is established over a
strictly larger surface.

**But the two writer counts are not interchangeable.** `phase1/REPORT.md`
states "0 of 137". After this port the defensible statement is:

> 0 of 574 structural writers (Zag scanner) read learner state;
> 0 of 137 (single-line scanner). Both are zero; the denominator depends
> on the function-header grammar the auditor accepts.

The report has been amended accordingly rather than left quoting a
denominator the current tooling no longer produces.

## THE THREE-CONDITION TEST IS PRESERVED

A structural lever counts only when **all three** hold:

1. the writing function has a learner-state **array** parameter
   (`X:[]u8`, not `X:i32`);
2. that array is **self-accumulating**;
3. the structural sink **reads** it.

This is the check that the first two Python auditors lacked, and it is
why they reported 94 and 137 false levers. `audit_struct.zag` implements
all three in Zag.

## LIMITS (unchanged, not narrowed)

* Static scope heuristic, **not** a compiler. Cannot see a structural
  change effected through a pointer alias or a shared global.
* Audits only what is committed on this branch.
* Does not prove the bound is fundamental -- only that it holds here.

## RUNTIME

~30 s for 1,040 sources in a single Zag process, single pass, no
interpreter.
