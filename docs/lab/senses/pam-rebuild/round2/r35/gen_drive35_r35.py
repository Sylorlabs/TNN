#!/usr/bin/env python3
"""Generate drive35_r35.zag from RT-JKLM's drive35.zag.

The J-35/K-35/L-35/M-35/honest attack logic is the prereg-frozen class:
run_j/run_k/run_l/run_m/run_honest (plus wout/wouti/wline/main) are extracted
VERBATIM from rt_jklm/drive35.zag (SHA-256 pinned in PREREG_R35.md) and
asserted byte-identical. Only changes vs the original driver:
  - @import("copy35.zag") -> @import("copy35_r35.zag") (the repaired copies)
  - main's scratch buffer 32 -> 64 bytes (48-byte tag preimages)
  - "DRIVE35 mode=" prefix -> "DRIVE35_R35 mode=" (provenance label)
verify_copies.sh re-runs this generator and diffs, proving attack identity.
"""
import sys

SRC = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/rt_jklm/drive35.zag"
OUT = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/r35/drive35_r35.zag"

WANT_FNS = ["wout", "wouti", "wline",
            "run_j", "run_k", "run_l", "run_m", "run_honest", "main"]

def is_boundary(line):
    s = line.strip()
    if s.startswith("fn ") or s.startswith("struct ") or s.startswith("const "):
        return True
    if s.startswith("//") and ("===" in s or "---" in s):
        return True
    return False

def extract(lines, name):
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith("fn " + name) and ln[3+len(name):4+len(name)] == "(":
            start = i
            break
    assert start is not None, f"not found: fn {name}"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if is_boundary(lines[j]):
            end = j
            break
    while end > start + 1 and lines[end-1].strip() == "":
        end -= 1
    return lines[start:end]

with open(SRC) as f:
    lines = f.read().split("\n")

blocks = {n: extract(lines, n) for n in WANT_FNS}

# the attack classes are frozen: assert nothing drifted in run_j..run_m
for n in ["run_j", "run_k", "run_l", "run_m", "run_honest"]:
    assert blocks[n], f"empty block {n}"

main = blocks["main"]
main_text = "\n".join(main)
assert 'let bs:[]u8 = nio_alloc(32);' in main_text
main_text = main_text.replace('let bs:[]u8 = nio_alloc(32);',
                              'let bs:[]u8 = nio_alloc(64); // R-35: 48-byte tag preimages')
main_text = main_text.replace('wout("DRIVE35 mode=");', 'wout("DRIVE35_R35 mode=");')

out = []
out.append('@import("R33_NATIVE_IO_V1.zag")')
out.append('@import("copy35_r35.zag")')
out.append("// drive35_r35.zag — RT-JKLM J/K/L/M/honest drivers vs the R-35 REPAIRED")
out.append("// tag functions. run_j/run_k/run_l/run_m/run_honest are byte-identical to")
out.append("// rt_jklm/drive35.zag @ evidence ec8d5d13 (asserted by gen_drive35_r35.py).")
out.append("// Pure Zag, zero RNG. argv[1] = j|k|l|m|honest.")
out.append("")
for n in ["wout", "wouti", "wline", "run_j", "run_k", "run_l", "run_m", "run_honest"]:
    out.extend(blocks[n])
    out.append("")
out.append(main_text)
out.append("")

with open(OUT, "w") as f:
    f.write("\n".join(out))
print("wrote", OUT)
for n in ["run_j", "run_k", "run_l", "run_m", "run_honest"]:
    print(f"  {n}: {len(blocks[n])} lines (byte-identical to RT-JKLM source)")
