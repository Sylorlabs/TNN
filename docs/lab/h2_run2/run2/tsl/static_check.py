#!/usr/bin/env python3
"""Static checks for t_sl.zag (T-SL decider build).
KB-STATIC / KB-CHANNEL subset for the T-SL crew:
 1. no randomness tokens anywhere (comments stripped)
 2. no cross-namespace op tokens (AV_*/TW_*/MC_*/SR_*/TRAINER_PIN)
 3. op-code allowlist: every OP_* const in the frozen set, every sl_emit
    code arg is an OP_* const or literal 0 (audit events)
 4. sl_select takes no episode/step operand and references none
 5. no []i32/[]u32/[]u16 casts (ZNC-2026-09-21-007)
 6. no `try` identifier
 7. no @import (self-contained; T import allowlist)
Exits nonzero on any hit. Python is orchestration/analysis only.
"""
import re
import sys

SRC = "t_sl.zag"
ALLOWED_OPS = {16, 17, 18, 24, 25, 26, 27, 28,
               46, 47, 48, 49, 50, 51, 52, 53, 54}

fail = 0


def note(msg):
    print(f"STATIC: {msg}")


src = open(SRC).read()
code = re.sub(r"//.*", "", src)

# 1. no randomness
for pat in [r"\brng\b", r"\brand\s*\(", r"\bsrand\b", r"urandom",
            r"\bseed\b", r"\btime\s*\("]:
    hits = re.findall(pat, code, re.IGNORECASE)
    if hits:
        note(f"FAIL randomness token /{pat}/: {hits[:5]}")
        fail = 1
if fail == 0:
    note("no-randomness OK")

# 2. cross-namespace op tokens
hits = re.findall(r"\b(AV_[A-Z]+|TW_[A-Z]+|MC_[A-Z]+|SR_[A-Z]+|TRAINER_PIN)\b", code)
if hits:
    note(f"FAIL cross-namespace tokens: {sorted(set(hits))}")
    fail = 1
else:
    note("op-namespace OK (SL/UTT/NOVEL only)")

# 3. op-code allowlist
consts = re.findall(r"const\s+(OP_[A-Z_0-9]+)\s*:\s*i32\s*=\s*(\d+)\s*;", code)
opmap = {name: int(val) for name, val in consts}
badops = {n: v for n, v in opmap.items() if v not in ALLOWED_OPS}
if badops:
    note(f"FAIL op consts outside frozen set: {badops}")
    fail = 1
else:
    note(f"op-code consts OK ({len(opmap)} consts, all in frozen set)")
# every sl_emit call: 5th arg (code) must be 0 or an OP_* const
for m in re.finditer(r"sl_emit\(([^;]*?)\)", code):
    args = m.group(1)
    if ":" in args:
        continue  # the fn definition, not a call site
    # find the code arg: strip the leading "st,au,acXXX,step," prefix
    mm = re.match(r"\s*\w+\s*,\s*\w+\s*,\s*&?\w+\s*,\s*[^,]+,\s*([^,]+),", args)
    if not mm:
        note(f"FAIL could not parse sl_emit args: {args[:80]}")
        fail = 1
        continue
    carg = mm.group(1).strip()
    if carg != "0" and not (carg.startswith("OP_") and carg in opmap):
        note(f"FAIL sl_emit code arg not allowlisted: {carg}")
        fail = 1
if fail == 0:
    note("sl_emit code args OK")

# 4. sl_select: no episode/step operand
m = re.search(r"fn sl_select\(([^)]*)\)[^{]*\{(.*?)\n\}", code, re.DOTALL)
if not m:
    note("FAIL sl_select not found")
    fail = 1
else:
    sig, body = m.group(1), m.group(2)
    if re.search(r"\b(ep|step|EP|STEP)\b", sig + body):
        note("FAIL sl_select references an episode/step operand")
        fail = 1
    else:
        note("sl_select OK (no episode operand)")

# 5. no []i32/[]u32/[]u16 casts
if re.search(r"as\s+\[\](i32|u32|u16)\b", code):
    note("FAIL []i32/[]u32/[]u16 cast present")
    fail = 1
else:
    note("no []i32-family casts OK")

# 6. no `try` identifier
if re.search(r"\btry\b", code):
    note("FAIL `try` identifier present")
    fail = 1
else:
    note("no `try` OK")

# 7. no @import
if re.search(r"@import", code):
    note("FAIL @import present")
    fail = 1
else:
    note("no @import OK (self-contained)")

if fail == 0:
    note("ALL STATIC CHECKS PASS")
else:
    note("STATIC FAILURES PRESENT")
sys.exit(fail)
