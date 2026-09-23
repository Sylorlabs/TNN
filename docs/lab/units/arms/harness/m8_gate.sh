#!/bin/bash
# m8_gate.sh — M8 determinism gate: N=5 adversarial perturbations × 2 reruns each.
# Every leg runs twice (double-run rule); the gate additionally requires N=5
# perturbations with byte-identical artifacts across all ten runs.
# Perturbations: clean, frag (deterministic heap pre-fragmentation), aslr
# (1,234,567-byte base pad), starve (entropy/clock starvation via LD_PRELOAD
# shim), freelist (reversed free-list init order — accepted no-op for
# id-derived placement; see AMBIGUITIES.md A11).
# Usage: m8_gate.sh <arm-bin> <corpus-root> <workdir>
set -u
BIN="$1"; CROOT="$2"; WORK="$3"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$WORK"

# build the starvation shim (workdir-only; never committed, never installed)
cat > "$WORK/shim.c" <<'EOF'
// entropy/clock starvation shim: getrandom/getentropy always fail;
// clock_gettime returns fixed zeros. Only loaded for the starve leg.
#define _GNU_SOURCE
#include <sys/syscall.h>
#include <unistd.h>
#include <time.h>
#include <errno.h>
long getrandom(void *b, unsigned long n, unsigned f){ errno=EIO; return -1; }
int getentropy(void *b, unsigned long n){ errno=EIO; return -1; }
int clock_gettime(clockid_t c, struct timespec *t){ t->tv_sec=0; t->tv_nsec=0; return 0; }
EOF
gcc -shared -fPIC -O2 -o "$WORK/shim.so" "$WORK/shim.c" 2>"$WORK/shim_build.log" || {
    echo "shim build failed"; cat "$WORK/shim_build.log"; exit 2; }

run_one() { # <outdir> <perturbation>
    local d="$1" p="$2"
    rm -rf "$d"; mkdir -p "$d"
    if [ "$p" = "starve" ]; then
        LD_PRELOAD="$WORK/shim.so" "$BIN" m8-1x "$CROOT" "$d" "$p" \
            >"$d/stdout.txt" 2>"$d/stderr.txt"
    else
        "$BIN" m8-1x "$CROOT" "$d" "$p" >"$d/stdout.txt" 2>"$d/stderr.txt"
    fi
    echo "$?"
}

PERTS="clean frag aslr starve freelist"
for p in $PERTS; do
    r1=$(run_one "$WORK/$p/run1" "$p")
    r2=$(run_one "$WORK/$p/run2" "$p")
    echo "run $p rc1=$r1 rc2=$r2"
    [ "$r1" = "0" ] && [ "$r2" = "0" ] || { echo "M8GATE FAIL: $p exited non-zero"; exit 1; }
    if ! diff -q "$WORK/$p/run1/stdout.txt" "$WORK/$p/run2/stdout.txt" >/dev/null; then
        echo "M8GATE FAIL: $p reruns diverged on stdout"; exit 1
    fi
done
python3 "$HERE/m8_compare.py" \
    "$WORK/clean/run1" "$WORK/clean/run2" \
    "$WORK/frag/run1" "$WORK/frag/run2" \
    "$WORK/aslr/run1" "$WORK/aslr/run2" \
    "$WORK/starve/run1" "$WORK/starve/run2" \
    "$WORK/freelist/run1" "$WORK/freelist/run2"
