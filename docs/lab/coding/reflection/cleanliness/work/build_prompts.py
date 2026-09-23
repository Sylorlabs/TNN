#!/usr/bin/env python3
"""Build judge prompts for CLN-1 blind judging. Deterministic, no RNG."""
import json, os, re, sys

BASE = os.path.expanduser("~/workspace/tnn-lab/coding/reflection/cleanliness")
WORK = os.path.join(BASE, "work")

RUBRIC = """- T1 — Naming clarity. 2 = names reveal role (total, found_index); 1 = mostly clear, 1–2 cryptic; 0 = systematically cryptic (a,b,x2) or misleading.
- T2 — Comments where non-obvious. 2 = non-obvious logic explained, obvious code uncommented; 1 = sparse but present where needed; 0 = none where needed, or noise comments restating the code.
- T3 — Error handling completeness. 2 = failure modes handled or honestly surfaced; 1 = partial; 0 = silent wrong behavior possible.
- T4 — Idiom. 2 = uses Zag's own patterns (_zag_print, i64 arithmetic, while loops, slice access); 1 = works but fights the language; 0 = transliterated from another language's idioms."""

TEMPLATE = """You are judging code cleanliness. All four snippets below compile and produce the correct output for the spec; judge ONLY cleanliness per the rubric, not correctness.

SPEC: {spec}

EXPECTED TEST OUTPUT: {expected}

FROZEN RUBRIC (apply verbatim):
{rubric}

For EACH of W, X, Y, Z, give T1, T2, T3, T4 scores (integer 0/1/2) AND an authorship guess assigning each label to exactly one of: {{human programmer, TNN AI coding agent, LLM assistant A, LLM assistant B}}. Each author category may be used multiple times or not at all.

Output ONLY these four lines, in this exact format, one per label:
W: T1=2 T2=1 T3=2 T4=2 AUTHOR=human programmer
X: T1=1 T2=0 T3=1 T4=2 AUTHOR=TNN AI coding agent
Y: T1=0 T2=0 T3=0 T4=0 AUTHOR=LLM assistant A
Z: T1=2 T2=2 T3=2 T4=2 AUTHOR=LLM assistant B
No other text.

=== SNIPPET W ===
{sw}

=== SNIPPET X ===
{sx}

=== SNIPPET Y ===
{sy}

=== SNIPPET Z ===
{sz}
"""

def main():
    specs = json.load(open(os.path.join(BASE, "SPECS.json")))["items"]
    by_id = {s["id"]: s for s in specs}
    mapping = json.load(open(os.path.join(WORK, "SEALED_MAPPING.json")))
    outdir = os.path.join(WORK, "judge_raw", "prompts")
    os.makedirs(outdir, exist_ok=True)
    for spec_id in mapping["specs"]:
        spec = by_id[spec_id]
        m = mapping["mapping"][spec_id]
        codes = {}
        for label in "WXYZ":
            arm = m[label]
            path = os.path.join(BASE, "sources", spec_id, arm + ".zag")
            codes[label] = open(path).read()
        expected = "; ".join(
            f'stdout={t["stdout"]!r}, rc={t["rc"]}' for t in spec["tests"])
        prompt = TEMPLATE.format(spec=spec["spec"], expected=expected,
                                 rubric=RUBRIC, sw=codes["W"],
                                 sx=codes["X"], sy=codes["Y"], sz=codes["Z"])
        # leak check: remove the allowed author-category strings, then no
        # arm-identifying words may remain
        stripped = prompt
        for cat in ("human programmer", "TNN AI coding agent",
                    "LLM assistant A", "LLM assistant B"):
            stripped = stripped.replace(cat, "")
        for pat, why in [(r'\bhuman\b', 'human'), (r'\btnn\b', 'tnn'),
                         (r'\bgrok\b', 'grok'), (r'\bsol\b', 'sol'),
                         (r'sources/', 'path'), (r'\.zag', '.zag'),
                         (r'SEALED', 'sealed')]:
            if re.search(pat, stripped, re.IGNORECASE):
                print(f"LEAK in {spec_id}: matched {why}", file=sys.stderr)
                sys.exit(1)
        open(os.path.join(outdir, spec_id + ".txt"), "w").write(prompt)
        print(f"built {spec_id} ({len(prompt)} chars)")
    print("OK: 14 prompts, leak check passed")

if __name__ == "__main__":
    main()
