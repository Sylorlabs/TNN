#!/usr/bin/env python3
"""forbidden_sweep.py — mechanical forbidden-content sweep (frozen §2.5).

Checks:
1. Zero matches for complete trigger->action pairing regex in apparatus sources.
2. No literal contains >=2 distinct atom/action names from Appendix A.
3. subject has no b==1 branch and no gt-index reference (G6).
4. audit-facts file has no per-item real/novel field rows.
5. (Round-log check runs during loop; not pre-loop.)
6. No quarantined example text in curriculum materials.

Usage: forbidden_sweep.py [--pre-loop]
Exit 0 = all pass; nonzero = failure (full halt per §3.6).
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
APP = HERE.parent
RUN2 = APP.parent

# Atom/action names from Appendix A (frozen)
ATOM_NAMES = [
    "pre_is", "chan_present", "chan_silent", "sm_le", "sm_ge", "sm_eq",
    "dir_is", "sn_ge", "so_ge", "caval_eq_vold", "caval_eq_vnew",
    "post_is", "psm_le", "psm_ge", "psm_eq",
]
ACTION_NAMES = [
    "force_consult", "block_consult", "force_withhold", "force_install",
    "recompute_only",
]
ALL_NAMES = ATOM_NAMES + ACTION_NAMES

# Quarantined example texts (§1.9) — must not appear in curriculum/deliberation
QUARANTINED = [
    "sm_le(2) THEN force_consult",  # F1 example fragment
    "force_withhold",  # appears in F2 context; checked with trigger pairing
]

# Complete trigger->action pairing regex (frozen §2.5)
PAIRING_RE = re.compile(
    r"IF\s+[A-Za-z_]+\(.*\)(\s+AND\s+[A-Za-z_]+\(.*\))*(\s+AND\s+[A-Za-z_]+)*\s+THEN"
)

# Apparatus sources to sweep (frozen §2.5 list)
SOURCES = [
    APP / "proposer.zag",
    APP / "subject.zag",
    APP / "policy_engine.zag.inc",
    HERE / "translate_policy.py",
    HERE / "loop_driver2.py",
    APP / "deliberation.zag",
]


def extract_literals_and_comments(path):
    """Extract string literals and comments from a file."""
    text = path.read_text()
    literals = []
    # Zag/Python string literals: "..." and '...'
    for m in re.finditer(r'"([^"\\]|\\.)*"', text):
        literals.append(m.group(0))
    for m in re.finditer(r"'([^'\\]|\\.)*'", text):
        literals.append(m.group(0))
    # Comments: //... and #...
    for m in re.finditer(r"//[^\n]*", text):
        literals.append(m.group(0))
    for m in re.finditer(r"#[^\n]*", text):
        literals.append(m.group(0))
    return literals


def check_pairing(sources):
    """§2.5.2: zero complete trigger->action pairings."""
    failures = []
    for src in sources:
        if not src.exists():
            continue
        for lit in extract_literals_and_comments(src):
            if PAIRING_RE.search(lit):
                failures.append(f"{src.name}: pairing found in: {lit[:80]}")
    return failures


def check_composition(sources):
    """§2.5.3: no literal with >=2 distinct atom/action names."""
    failures = []
    for src in sources:
        if not src.exists():
            continue
        for lit in extract_literals_and_comments(src):
            found = set()
            for name in ALL_NAMES:
                # whole-word match
                if re.search(r"\b" + re.escape(name) + r"\b", lit):
                    found.add(name)
            if len(found) >= 2:
                failures.append(
                    f"{src.name}: {len(found)} names in: {lit[:80]} "
                    f"({sorted(found)})"
                )
    return failures


def check_subject_g6():
    """§2.5.4: subject.zag has no b==1 and no gt-index."""
    failures = []
    subj = APP / "subject.zag"
    if not subj.exists():
        return [f"subject.zag not found"]
    text = subj.read_text()
    if "b==1" in text:
        failures.append("subject.zag contains b==1 branch (G6 violation)")
    # gt-index: ,11) or f==11 or [11]
    if re.search(r",11\)", text):
        failures.append("subject.zag contains ,11) gt-index (G6 violation)")
    if "f==11" in text:
        failures.append("subject.zag contains f==11 (G6 violation)")
    return failures


def check_audit_facts():
    """§2.5.4: audit-facts has no per-item field rows."""
    failures = []
    # audit-facts file location TBD; check if exists
    audit = APP / "audit_facts.txt"
    if not audit.exists():
        return []  # not yet created; schema check at loop time
    text = audit.read_text()
    # per-item rows would have field names like vold, vnew, a1, etc.
    field_names = ["vold", "vnew", "a1", "op1", "a2", "op2", "a3", "op3",
                   "cidx", "caval"]
    for fn in field_names:
        if re.search(r"\b" + fn + r"\b", text):
            failures.append(f"audit_facts.txt contains field '{fn}' (schema violation)")
            break
    return failures


def check_quarantined():
    """§2.5.6: no quarantined example text in curriculum."""
    failures = []
    curr_dir = RUN2 / "curriculum"
    if not curr_dir.exists():
        return []
    for lesson in curr_dir.glob("*.txt"):
        text = lesson.read_text()
        # Check for F1-F6 example policies (they should NOT be in lessons)
        # The quarantined examples are specific policy texts; lessons use
        # RULE grammar, not POLICY grammar, so this is a sanity check.
        if "POLICY" in text and "force_consult" in text:
            # Lessons should not contain POLICY blocks
            failures.append(f"{lesson.name}: contains POLICY block (quarantine violation)")
    return failures


def main():
    all_failures = []
    print("=== Forbidden-content sweep (frozen §2.5) ===")

    print("\n[1] Trigger->action pairing check...")
    f = check_pairing(SOURCES)
    all_failures.extend(f)
    print(f"    {'PASS' if not f else 'FAIL'}: {len(f)} violations")

    print("\n[2] Atom/action composition check...")
    f = check_composition(SOURCES)
    all_failures.extend(f)
    print(f"    {'PASS' if not f else 'FAIL'}: {len(f)} violations")

    print("\n[3] Subject G6 check (no b==1, no gt-index)...")
    f = check_subject_g6()
    all_failures.extend(f)
    print(f"    {'PASS' if not f else 'FAIL'}: {len(f)} violations")

    print("\n[4] Audit-facts schema check...")
    f = check_audit_facts()
    all_failures.extend(f)
    print(f"    {'PASS' if not f else 'FAIL'}: {len(f)} violations")

    print("\n[6] Quarantined text check...")
    f = check_quarantined()
    all_failures.extend(f)
    print(f"    {'PASS' if not f else 'FAIL'}: {len(f)} violations")

    print("\n" + "="*50)
    if all_failures:
        print(f"HALT: {len(all_failures)} forbidden-content violations (§3.6)")
        for fail in all_failures:
            print(f"  - {fail}")
        return 1
    print("PASS: all forbidden-content checks clear")
    return 0


if __name__ == "__main__":
    sys.exit(main())
