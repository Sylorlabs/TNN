#!/bin/bash
# Build all M2 battery targets: for each module, 6 binaries (one per baked
# dirt config D0..D5), each linking the audit allocator via m2_substrate.zag.
# Usage: build_all.sh  (run from evidence/m2)
set -u
E2M=~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m2
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
LOG=$E2M/build/build.log
mkdir -p $E2M/build/mod
: > "$LOG"
fail=0
for mod in $E2M/src/modules/*.zag; do
    name=$(basename "$mod" .zag)
    mkdir -p "$E2M/build/mod/$name"
    for d in 0 1 2 3 4 5; do
        w=$(mktemp -d)
        cp "$mod" "$w/module.zag"
        cp $E2M/src/m2_audit_alloc.zag "$w/"
        cp $E2M/src/m2_config_D$d.zag "$w/m2_config.zag"
        cp $E2M/src/m2_substrate.zag "$w/"
        (cd "$w" && "$ZNC" build module.zag -o "$E2M/build/mod/$name/targ_d$d" >>"$LOG" 2>&1)
        rc=$?
        if [ $rc -ne 0 ]; then echo "BUILD-FAIL $name d$d"; fail=1; fi
        rm -rf "$w"
    done
    echo "built $name"
done
[ $fail -eq 0 ] && echo "ALL BUILDS OK" || echo "BUILDS FAILED (see $LOG)"
