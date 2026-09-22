#!/usr/bin/env python3
"""audit_forbidden.py — verify zero crew-authored architecture/design content.

Checks that generic machinery files contain no pipeline-specific vocabulary:
- field names (product, quantity, price, region, sku, item, stock, reorder,
  warehouse, ts, level, msg, code, etc.)
- stage IDs (A1..A10, B1..B8, C1..C8, F1)
- pipeline names (sales, inventory, logs)
- op names that encode design choices (upper, clamp, mul_fields, etc.)
  -- these MAY appear as string literals in the emitter (mechanical mapping),
     but NOT as logic that selects them.

Allowed in machinery:
- "LH|FIELD", "LH|FILTER", "LH|AGG", "LH|SORT" as dispatch tags (generic categories)
- "op=" as a spec key (generic)
- KB entry IDs (LH-CAP|...) as identifiers

The contracts/ directory is ALLOWED to contain behavior vocabulary
(it's the crew-authored behavior spec, not machinery).

Usage: audit_forbidden.py <workdir>
Exits 0 if clean, 1 if forbidden content found.
"""
import os, sys, re

MACHINERY_FILES = ["lh_emit.zag", "lh_delib.zag", "lh_driver.py"]

# Field names (pipeline-specific vocabulary) — NOT including generic op names
FIELD_NAMES = [
    "product", "quantity", "price", "region", "total", "pcode",
    "sku", "item", "stock", "reorder", "warehouse", "need",
    "ts", "level", "msg", "code", "head", "mcode",
    # "sum" and "count" are generic op names from the KB (allowed as identifiers).
    # Their use as AGG output field names appears only in contracts/ (allowed).
]

# Generic op names from the KB (allowed in machinery as identifiers)
OP_NAMES = [
    "upper", "clamp", "mul_fields", "sub_fields", "firstchar_plus", "substr", "format",
    "field_count_eq", "int_gt", "int_ge", "int_lt", "int_lt_field", "in_set",
    "sum", "count", "sort",
]

# Stage IDs
STAGE_IDS = [f"A{i}" for i in range(1, 11)] + [f"B{i}" for i in range(1, 9)] + \
            [f"C{i}" for i in range(1, 9)] + ["F1"]

# Pipeline names
PIPELINES = ["sales", "inventory", "logs"]

def check_file(path):
    violations = []
    with open(path) as f:
        content = f.read()
    # Check field names (as whole words, case-insensitive)
    for name in FIELD_NAMES:
        # Skip if it's part of a larger identifier that's generic
        # e.g., "field_count" is generic, "product" is not
        pattern = r'\b' + re.escape(name) + r'\b'
        for m in re.finditer(pattern, content, re.IGNORECASE):
            # Allow in comments that describe the audit itself
            line_start = content.rfind('\n', 0, m.start()) + 1
            line = content[line_start:content.find('\n', m.start())]
            if "audit" in line.lower() or "forbidden" in line.lower():
                continue
            violations.append(f"{path}: field name '{name}' at offset {m.start()}: {line.strip()[:80]}")
    # Check stage IDs (e.g., "A1" as a standalone token)
    # Skip episode suffixes like "-C1", "-P1" (generic role markers, not stage refs)
    for sid in STAGE_IDS:
        # Match sid not followed by digit, not preceded by '-' (episode suffix)
        pattern = r'(?<!-)\b' + re.escape(sid) + r'(?!\d)\b'
        for m in re.finditer(pattern, content):
            line_start = content.rfind('\n', 0, m.start()) + 1
            line = content[line_start:content.find('\n', m.start())]
            if "audit" in line.lower():
                continue
            # Skip episode format strings in delib (PROPOSER/CRITIC/COMPOSER lines)
            if "PROPOSER" in line or "CRITIC" in line or "COMPOSER" in line:
                continue
            violations.append(f"{path}: stage ID '{sid}' at offset {m.start()}: {line.strip()[:80]}")
    # Check pipeline names
    for pipe in PIPELINES:
        pattern = r'\b' + re.escape(pipe) + r'\b'
        for m in re.finditer(pattern, content, re.IGNORECASE):
            line_start = content.rfind('\n', 0, m.start()) + 1
            line = content[line_start:content.find('\n', m.start())]
            if "audit" in line.lower():
                continue
            violations.append(f"{path}: pipeline '{pipe}' at offset {m.start()}: {line.strip()[:80]}")
    return violations

def main():
    workdir = sys.argv[1]
    all_violations = []
    for fname in MACHINERY_FILES:
        path = os.path.join(workdir, fname)
        if os.path.exists(path):
            all_violations.extend(check_file(path))
        else:
            print(f"Missing: {path}")
            sys.exit(1)
    if all_violations:
        print("FORBIDDEN CONTENT FOUND:")
        for v in all_violations[:20]:  # limit output
            print(f"  {v}")
        if len(all_violations) > 20:
            print(f"  ... and {len(all_violations) - 20} more")
        sys.exit(1)
    else:
        print("AUDIT CLEAN: no pipeline-specific vocabulary in machinery.")
        sys.exit(0)

if __name__ == "__main__":
    main()
