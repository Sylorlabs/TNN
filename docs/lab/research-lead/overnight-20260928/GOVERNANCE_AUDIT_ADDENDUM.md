# Governance Audit Addendum: Procedure-Invention Frontier

**Date:** 2026-09-29 07:45 PDT
**Auditor:** Scientific-Governance Auditor

## New Artifacts Reviewed

1. **Builder prereg** (`PREREG_PROC_INVENT.md`, commit 6cd2e95a7, 14:09:41):
   Targets reverse (PI-1a) and identity (PI-1b) via compositional index-program search.
   Kill bars K-P1 through K-P5 frozen.

2. **Builder implementation** (`sem_l3/proc_learn.zag`, untracked, 442 lines):
   Implements program enumeration (1055 programs), search, hidden tests.
   Does NOT compile (streq linking issue). Work in progress, no results claimed.

3. **Adversary prereg** (`pi_adversary/PI_ADVERSARY_PREREG.md`, untracked):
   Frozen attack battery A1-A8. Governance rules G1-G6.

4. **Adversary RT1** (`pi_adversary/PI_RT1_GOVERNANCE_AUDIT.md`, untracked):
   Scaffold clean (PASS). Design doc leaks target (FLAG).

## Findings

### F1. Builder prereg ordering: CORRECT
Prereg committed (14:09:41) before implementation (still untracked). Kill bars
frozen. No post-hoc adjustment possible yet.

### F2. Implementation has no hardcoded solution: PASS (preliminary)
Source inspection: search enumerates 1055 compositional programs systematically.
Solution selected via `prog_fits` testing, not planted. Training examples are
hardcoded in main() (acceptable for v1 mechanism validation).

### F3. Family pre-naming conflict: FLAGGED (not invalidated)
- Builder targets REVERSE, named in NEXT_FRONTIER_DESIGN.md.
- Adversary G6 disqualifies pre-named families for true L3 claims.
- Builder's prereg explicitly states expected solution (honest hypothesis, not hidden).
- **Resolution:** Current work is **mechanism validation** (does search find the
  program?), not **true invention** (undisclosed family). For L3 claim, Adversary
  must assign family post-freeze per G1.

### F4. Implementation incomplete: NOTED
Does not compile (streq issue). PI-1b implemented. Memorization baseline (K-P3)
not yet implemented. No results claimed, so no violation.

### F5. Adversary independence: CONFIRMED
Adversary prereg frozen before Builder implementation commit. Attack battery
is principled (A1-A8). G6 is a valid anti-enumeration rule.

## Verdicts

- **Builder prereg:** VALID (properly frozen, honest about target).
- **Builder implementation:** WORK IN PROGRESS (no claims to audit yet).
- **Adversary prereg:** VALID (independent, principled).
- **L3 claim for reverse:** WOULD BE VOID under G6 if claimed as "invention"
  (family pre-named). As "mechanism validation," it is legitimate.

## Recommendation to Coordinator

1. Allow Builder to complete reverse/identity as **mechanism validation**.
2. For **true L3 claim**, require Adversary-assigned undisclosed family per G1.
3. Builder should commit implementation before running (prereg ordering).
4. Adversary should commit its prereg files (currently untracked).
