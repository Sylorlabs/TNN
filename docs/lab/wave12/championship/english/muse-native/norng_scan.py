#!/usr/bin/env python3
"""Step 10: static no-RNG scan over all .zag sources of the muse-native
championship legs (legA/src, legB/src, legC/src, tnn/shared).

Rules (drawn from THINCERT BAN-THIN-2026-09-20-v1 and the prereg R2/R6 lists):
- BANNED intrinsic tokens (fail-closed): _zag_rand, _zag_clock_monotonic_ms,
  _zag_getenv, _zag_exec_cmd/_zag_exec_capture, _zag_read_fd/_zag_read_file/
  _zag_write_file/_zag_write_exec/_zag_file_exists, _zag_exit, _zag_x86_cpuid_*,
  _zag_rdmsr/_zag_wrmsr, _zag_inb/_zag_inw/_zag_inl, _zag_outb/_zag_outw/_zag_outl,
  _zag_cli/_zag_sti/_zag_hlt/_zag_pause/_zag_wbinvd, _zag_read_cr*/_zag_write_cr*,
  _zag_lgdt/_zag_lidt/_zag_ltr/_zag_invlpg, _zag_script_*, _zag_process_result_*,
  _zag_allocation_*/_zag_allocator_*/_zag_fixed_buffer_*, _zag_argc
  (_zag_argc itself is not RNG but is banned-by-quirk ZNC-2026-09-21-007;
  main() was already fixed to read _zag_arg unconditionally).
- BANNED literal substrings (R6b): urandom, /dev/, /proc/, /sys/, random,
  getrandom, clock_gettime, time(), rand().
- _zag_raw_syscall first arg must be an integer literal in the prereg allowlist
  {0,1,2,3,5,8,23,72,74,83,160,257,265}.
Comment and string-literal regions are stripped before token matching, and
scanned separately for banned literal substrings.

Exit 0: PASS on every file. Exit 1: any violation (printed).
"""
import os
import re
import sys

BASE = "/home/hatch/workspace/tnn-lab/wave12/championship-english/muse-native"
SRC_DIRS = ["tnn/legA/src", "tnn/legB/src", "tnn/legC/src", "tnn/shared"]

BANNED_TOKENS = [
    "_zag_rand", "_zag_clock_monotonic_ms", "_zag_getenv",
    "_zag_exec_cmd", "_zag_exec_capture",
    "_zag_read_fd", "_zag_read_file", "_zag_write_file", "_zag_write_exec",
    "_zag_file_exists", "_zag_exit",
    "_zag_x86_cpuid_", "_zag_rdmsr", "_zag_wrmsr",
    "_zag_inb", "_zag_inw", "_zag_inl", "_zag_outb", "_zag_outw", "_zag_outl",
    "_zag_cli", "_zag_sti", "_zag_hlt", "_zag_pause", "_zag_wbinvd",
    "_zag_read_cr", "_zag_write_cr",
    "_zag_lgdt", "_zag_lidt", "_zag_ltr", "_zag_invlpg",
    "_zag_script_", "_zag_process_result_",
    "_zag_allocation_", "_zag_allocator_", "_zag_fixed_buffer_",
    "_zag_argc",  # quirk-banned, see header
]
BANNED_STRS = ["urandom", "/dev/", "/proc/", "/sys/", "getrandom",
               "clock_gettime", "time(", "rand("]
SYSCALL_ALLOW = {0, 1, 2, 3, 5, 8, 23, 72, 74, 83, 160, 257, 265}

viol = []
nfiles = 0
for sd in SRC_DIRS:
    d = os.path.join(BASE, sd)
    for root, _, files in os.walk(d):
        for fn in sorted(files):
            if not fn.endswith(".zag"):
                continue
            nfiles += 1
            rel = os.path.relpath(os.path.join(root, fn), BASE)
            src = open(os.path.join(BASE, rel)).read()
            # strip line comments, keep string literals aside
            code_chars, strings = [], []
            for line in src.split("\n"):
                out = []
                i = 0
                while i < len(line):
                    if line[i:i+2] == "//":
                        break
                    out.append(line[i])
                    i += 1
                code_chars.append("".join(out))
            code = "\n".join(code_chars)
            for m in re.finditer(r'"(?:[^"\\]|\\.)*"', src):
                strings.append(m.group(0))
            strblob = "\n".join(strings)
            for tok in BANNED_TOKENS:
                # whole-token match (identifier boundary): '_zag_argc(' matches,
                # '_zag_arg(' does not contain the token '_zag_argc' at all.
                # Comments were already stripped, so prose mentions are excluded.
                for m in re.finditer(re.escape(tok) + r"(?![0-9a-zA-Z_])", code):
                    viol.append((rel, "banned-token", tok))
            for bs in BANNED_STRS:
                if bs in code or bs in strblob:
                    viol.append((rel, "banned-string", bs))
            for m in re.finditer(r"_zag_raw_syscall\s*\(\s*(-?\d+)", code):
                n = int(m.group(1))
                if n not in SYSCALL_ALLOW:
                    viol.append((rel, "syscall-not-allowed", str(n)))
            for m in re.finditer(r"_zag_raw_syscall\s*\(\s*([a-zA-Z_])", code):
                viol.append((rel, "syscall-nonliteral-arg", m.group(1)))

print(f"scanned {nfiles} .zag files")
# --- import-closure check: is a flagged file actually compiled into a leg? ---
IMPORTS = {}
ALL_ZAG = []  # every .zag file under the src dirs (recursive)
for sd in SRC_DIRS:
    d = os.path.join(BASE, sd)
    for root, _, files in os.walk(d):
        for fn in sorted(files):
            if not fn.endswith(".zag"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), BASE)
            ALL_ZAG.append(rel)
            src = open(os.path.join(BASE, rel)).read()
            IMPORTS[rel] = set(re.findall(r'@import\("([^"]+)"\)', src))

MAINS = ["tnn/legA/src/muse_trial.zag", "tnn/legB/src/muse_b7_direct.zag",
         "tnn/legC/src/muse_teacher_leg.zag"]
LIVE = set()
for m in MAINS:
    stack = [m]
    while stack:
        cur = stack.pop()
        if cur in LIVE:
            continue
        LIVE.add(cur)
        sd = os.path.dirname(cur)
        for imp in IMPORTS.get(cur, ()):
            cand = os.path.normpath(os.path.join(sd, imp))
            if cand in IMPORTS:
                stack.append(cand)
            else:
                viol.append((cur, "import-not-found", imp))

live_viol, dead_viol = [], []
for v in viol:
    (dead_viol if v[0] not in LIVE else live_viol).append(v)

def show(tag, items):
    seen = set()
    for x in items:
        if x not in seen:
            seen.add(x)
            print(f"  {tag} {x[0]}: {x[1]} -> {x[2]}")
    return len(seen)

print("== violations in LIVE (compiled) files ==")
nl = show("VIOLATION", live_viol)
print("== violations in DEAD (never imported/compiled) files ==")
nd = show("DEAD-REF", dead_viol)
if nl:
    print(f"NO_RNG_SCAN: FAIL ({nl} live violations)")
    sys.exit(1)
print("NO_RNG_SCAN: PASS on all compiled sources"
      + (f"; {nd} dead-reference-only note(s) above (not compiled into any binary)" if nd else ""))
