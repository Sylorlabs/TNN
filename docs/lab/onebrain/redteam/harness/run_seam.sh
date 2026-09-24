#!/bin/bash
# run_seam.sh — ONE-BRAIN SEAM RED TEAM runner.
#
# Usage:
#   ./run_seam.sh mock <defect>        build+run the mock with MOCK_DEFECT=<defect> (0..11)
#   ./run_seam.sh --selftest           build all 12 mock binaries, verify the
#                                      frozen oracle expectations (harness self-test)
#   ./run_seam.sh /path/to/impl.zag    build+run a one-brain variant's
#                                      seam_target_impl.zag  *** EXECUTION GATE ***
#                                      Do NOT run this mode until the parent
#                                      relays the frozen prereg + variant locations.
#
# Every mode: static no-RNG grep, compile with the pinned znc, two runs with
# byte-identical stdout required.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
BUILD="$D/build"
OUT1="$BUILD/run1.txt"
OUT2="$BUILD/run2.txt"

note() { echo "RUNNER: $1" >&2; }
fail=0

stage() { # $1 = impl selector ("mock" or path), $2 = defect (mock only)
    rm -rf "$BUILD"
    mkdir -p "$BUILD"
    cp "$D/seam_contract.zag" "$D/seam_world.zag" "$D/seam_oracle.zag" "$D/seam_driver.zag" "$BUILD/"
    if [ "$1" = "mock" ]; then
        { echo "// generated mock config — do not edit by hand";
          echo "const MOCK_DEFECT:i32=$2;";
          cat "$D/mock_target.zag"; } > "$BUILD/seam_target_impl.zag"
    else
        cp "$1" "$BUILD/seam_target_impl.zag"
    fi
}

static_checks() {
    if sed 's|//.*||' "$BUILD"/seam_*.zag | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
        note "FAIL no-randomness grep hit:"
        sed 's|//.*||' "$BUILD"/seam_*.zag | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'
        fail=1
    else
        note "no-randomness static check OK"
    fi
}

compile() {
    # NOTE: znc resolves @import paths relative to the CWD, not the source
    # file — compile from inside the staged build dir so the staged copies
    # (not the harness originals) are the ones imported.
    ( cd "$BUILD" && "$ZNC" "seam_driver.zag" --no-zagd --no-analyze --no-foreground-cache -o "seam_bin" ) 2>"$BUILD/compile.txt"
    if [ $? -ne 0 ]; then
        note "FAIL compile:"; cat "$BUILD/compile.txt"; exit 1
    fi
    note "compile OK"
}

run_twice() { # prints "ok" or "fail"; leaves OUT1/OUT2
    "$BUILD/seam_bin" > "$OUT1" 2>&1; e1=$?
    "$BUILD/seam_bin" > "$OUT2" 2>&1; e2=$?
    s1=$(sha256sum "$OUT1" | cut -d' ' -f1); s2=$(sha256sum "$OUT2" | cut -d' ' -f1)
    if [ "$s1" != "$s2" ]; then note "FAIL determinism: $s1 != $s2"; fail=1; echo "fail"; return; fi
    if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; echo "fail"; return; fi
    note "determinism OK (sha256 $s1)"
    echo "ok"
}

verdict_of() { # $1 = attack id -> "KILL"/"SURVIVE"
    grep "^SEAM,$1," "$OUT1" | cut -d, -f3
}
reason_of() { # $1 = attack id -> reason int
    grep "^SEAM,$1," "$OUT1" | cut -d, -f4
}

if [ "${1:-}" = "--selftest" ]; then
    # expected reason per defect binary: "attack:reason,..." (defect 0: all survive)
    declare -A EXP
    EXP[0]=""
    for d in 1 2 3 4 5 6 7 8 10 11; do EXP[$d]="$((d-1)):1"; done
    EXP[9]="8:2"
    bad=0
    for d in 0 1 2 3 4 5 6 7 8 9 10 11; do
        stage mock "$d"
        static_checks
        compile
        if [ "$(run_twice)" != "ok" ]; then bad=$((bad+1)); continue; fi
        atk_expect="${EXP[$d]}"
        for a in 0 1 2 3 4 5 6 7 8 9 10; do
            v="$(verdict_of $a)"; r="$(reason_of $a)"
            if [ -z "$atk_expect" ]; then
                if [ "$v" != "SURVIVE" ]; then
                    echo "SELFTEST D$d A$a: expected SURVIVE got $v,$r"; bad=$((bad+1))
                fi
            else
                ea="${atk_expect%%:*}"; er="${atk_expect##*:}"
                if [ "$a" = "$ea" ]; then
                    if [ "$v" != "KILL" ] || [ "$r" != "$er" ]; then
                        echo "SELFTEST D$d A$a: expected KILL,$er got $v,$r"; bad=$((bad+1))
                    fi
                else
                    if [ "$v" != "SURVIVE" ]; then
                        echo "SELFTEST D$d A$a: expected SURVIVE got $v,$r"; bad=$((bad+1))
                    fi
                fi
            fi
        done
        note "defect $d matrix checked"
    done
    if [ $bad -ne 0 ]; then note "SELFTEST FAILURES: $bad"; exit 1; fi
    note "SELFTEST ALL PASS (12 binaries x 11 attacks, byte-identical reruns)"
    exit 0
fi

if [ "${1:-mock}" = "mock" ]; then
    DEFECT="${2:-0}"
    stage mock "$DEFECT"
    static_checks
    compile
    run_twice
    cat "$OUT1"
    [ $fail -ne 0 ] && exit 1
    exit 0
fi

# variant mode — execution gate: only with the parent's relay
if [ -f "${1:-}" ]; then
    stage "$1" 0
    static_checks
    compile
    run_twice
    cat "$OUT1"
    [ $fail -ne 0 ] && exit 1
    exit 0
fi

echo "usage: $0 [mock <defect> | --selftest | /path/to/variant_impl.zag]"
exit 2
