#!/usr/bin/env python3
"""RT-X derived-source generator (B-3034-X battery).

Derives, from the COMMITTED composition driver (ad0e1ddd, byte-verified by
SHA-256 below), the mechanical variants the prereg requires:

  drive3034_lib.zag        — pristine driver, ONLY `fn main()` renamed to
                             `fn comp_main_unused()` (znc rejects duplicate
                             `main`; the X-driver provides its own).
  drive3034_ablate_p1.zag  — lib + grok's pass-1 "34-half nops":
                               while(e < 3) -> while(e < 1)
                               delete tv<t_present / td<tv lines (F3 vacuous)
                               delete he!=h0 line (F2 identical args)
                               if(e < (maxv as i64)) -> if(1 == 1)
                             The final `if(maxv == 3)` all-K gate and the
                             `forge == 1` fiat line are KEPT (not vacuous;
                             prereg section 9).
  drive3034_ablate_p2.zag  — ablate_p1 with the common import retargeted to
                             b303134_common_ablate_p2.zag.
  b303134_common_ablate_p2.zag — pristine common with bind_ok -> return 1.

Every replacement is exact-string with an asserted occurrence count; any
deviation aborts. Diffs are written to DIFFS.md.
"""
import difflib
import hashlib
import sys

SRC = "/home/hatch/workspace/b3034comp/extract/frozen/drive3034_ad0e1ddd.zag"
COMMON = "/home/hatch/workspace/b3034comp/extract/frozen/b303134_common_6e74ce54.zag"
IO = "/home/hatch/workspace/b3034comp/src/R33_NATIVE_IO_V1.zag"
OUT = "/home/hatch/workspace/rtx/derived"

PIN_SRC = "1b1eb68ab4d0b704546b75ee0a6a7207cb7dcd59b6b6c53b5850d4b991e410b4"
PIN_COMMON = "79257900bc1ccb1518ff0d286615a4f8ce90bb02c9dfcb724b50ca26af286218"
PIN_IO = "e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def rep_once(text, old, new, expect=1):
    n = text.count(old)
    if n != expect:
        raise SystemExit(f"ABORT: expected {expect} occurrence(s) of {old!r}, found {n}")
    return text.replace(old, new)


def main():
    assert sha(SRC) == PIN_SRC, "pristine driver SHA mismatch"
    assert sha(COMMON) == PIN_COMMON, "pristine common SHA mismatch"
    assert sha(IO) == PIN_IO, "io SHA mismatch"
    with open(SRC) as f:
        src = f.read()
    with open(COMMON) as f:
        common = f.read()

    diffs = []

    # 1. lib: rename main only.
    lib = rep_once(src, "fn main() void {", "fn comp_main_unused() void {")
    diffs.append(("drive3034_ad0e1ddd.zag -> drive3034_lib.zag",
                  list(difflib.unified_diff(src.splitlines(), lib.splitlines(), lineterm=""))))

    # 2. ablate pass 1: grok's 34-half nops.
    p1 = lib
    p1 = rep_once(p1, "    while(e < 3) {", "    while(e < 1) {")
    p1 = rep_once(p1, "            if(tv < t_present) { temporal_ok = 0; }\n", "")
    p1 = rep_once(p1, "            if(td < tv) { temporal_ok = 0; }\n", "")
    p1 = rep_once(p1, "            if(he != h0) { all1 = 0; }\n", "")
    p1 = rep_once(p1, "        if(e < (maxv as i64)) {", "        if(1 == 1) {")
    diffs.append(("drive3034_lib.zag -> drive3034_ablate_p1.zag",
                  list(difflib.unified_diff(lib.splitlines(), p1.splitlines(), lineterm=""))))

    # 3. ablate pass 2 driver: retarget the common import.
    p2 = rep_once(p1, '@import("b303134_common.zag")',
                  '@import("b303134_common_ablate_p2.zag")')
    diffs.append(("drive3034_ablate_p1.zag -> drive3034_ablate_p2.zag",
                  list(difflib.unified_diff(p1.splitlines(), p2.splitlines(), lineterm=""))))

    # 4. ablate pass 2 common: bind_ok -> return 1.
    old_bind = ("fn bind_ok(pin:i32, attached:i64, id:i64, label:i64, conf:i64, meas:i64, extra:i64, seed:i64) i32 {\n"
                "    let re:i64 = verdict_bound(pin, id, label, conf, meas, extra, seed);\n"
                "    if(re == attached) { return 1; }\n"
                "    return 0;\n"
                "}")
    new_bind = ("fn bind_ok(pin:i32, attached:i64, id:i64, label:i64, conf:i64, meas:i64, extra:i64, seed:i64) i32 {\n"
                "    return 1;\n"
                "}")
    common_p2 = rep_once(common, old_bind, new_bind)
    diffs.append(("b303134_common.zag -> b303134_common_ablate_p2.zag",
                  list(difflib.unified_diff(common.splitlines(), common_p2.splitlines(), lineterm=""))))

    import os
    os.makedirs(OUT, exist_ok=True)
    outs = {
        "drive3034_lib.zag": lib,
        "drive3034_ablate_p1.zag": p1,
        "drive3034_ablate_p2.zag": p2,
        "b303134_common_ablate_p2.zag": common_p2,
    }
    for name, text in outs.items():
        with open(f"{OUT}/{name}", "w") as f:
            f.write(text)
        print(f"wrote {OUT}/{name} sha256={sha(f'{OUT}/{name}')}")

    with open(f"{OUT}/DIFFS.md", "w") as f:
        f.write("# RT-X derived-source diffs (mechanical, script-applied)\n\n")
        for title, dl in diffs:
            f.write(f"## {title}\n\n```diff\n")
            f.write("\n".join(dl) + "\n```\n\n")
    print(f"wrote {OUT}/DIFFS.md")


if __name__ == "__main__":
    main()
