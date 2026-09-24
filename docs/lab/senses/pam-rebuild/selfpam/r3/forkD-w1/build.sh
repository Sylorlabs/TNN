#!/bin/bash
# H6-R3 fork D build: write-once evidence partition, two binaries.
#   forkD          — verdict/battery/gen/genm7/atomize/prove/verify (NEVER writes the partition)
#   ingest_sensor  — sensor/ingest path (the ONLY partition writer)
# Deterministic, pure Zag, no RNG. Build-gated structural separation (KB1).
set -e
set -o pipefail
cd "$(dirname "$0")/src"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1

fail() { echo "BUILD KILLED: $1"; exit 1; }

echo "=== KB1 structural gates ==="

# Gate 1: evpart_write.zag is @import'ed ONLY by ingest.zag.
importers=$(grep -l '@import("evpart_write.zag")' *.zag || true)
[ "$importers" = "ingest.zag" ] || fail "evpart_write.zag imported by: $importers (must be ingest.zag only)"

# Gate 2: the forkD binary's source closure contains no writer reference.
# Closure of main.zag: main, io, str, tables, atom, atomize, prover, delib,
# gen, gen_m7, facts, evpart_read.
for f in main.zag io.zag str.zag tables.zag atom.zag atomize.zag prover.zag delib.zag gen.zag gen_m7.zag facts.zag evpart_read.zag; do
    if grep -v '^\s*//' "$f" | grep -q 'part_create\|part_append_entry\|part_seal\|evpart_write'; then
        fail "writer reference in forkD closure file $f"
    fi
done
echo "gate2: forkD closure has no writer path. OK."

# Gate 3: evpart_read.zag has no file-write call.
if grep -q 'file_write(' evpart_read.zag; then
    fail "evpart_read.zag contains a file_write call"
fi
echo "gate3: evpart_read.zag is read-only. OK."

# Gate 4: the ingest binary never imports the draft/deliberation machinery.
for f in ingest.zag ingest_main.zag; do
    if grep -q '@import("gen.zag")\|@import("gen_m7.zag")\|@import("atomize.zag")\|@import("delib.zag")\|@import("prover.zag")' "$f"; then
        fail "generator/delib import in ingest path file $f"
    fi
done
echo "gate4: ingest path cannot fabricate drafts. OK."

# Gate 5: no PROV label literals in code (provenance is physical, not a label).
if grep -n '"|GEN"\|"|EXT"' *.zag | grep -v '^[a-z_0-9.]*:[0-9]*:\s*//'; then
    fail "PROV label literal found in code"
fi
echo "gate5: no PROV label literals. OK."

# Gate 6: no RNG (rand/rng/seed/clock/time(/getrandom), excluding comments).
if grep -rni "rand\|rng\|seed\|clock\|getrandom\|time(" *.zag | grep -v '^[a-z_0-9.]*:[0-9]*:\s*//'; then
    fail "RNG-related token found"
fi
echo "gate6: no RNG. OK."

# Gate 7: no consecutive same-size mistyped casts (ZNC-2026-09-21-007).
if grep -n 'as \[\]i32\|as \[\]u32\|as \[\]u16' *.zag; then
    fail "mistyped slice cast found (use []u8 arenas)"
fi
echo "gate7: no mistyped casts. OK."

# Gate 8: the partition writer is create-only: no O_TRUNC open in evpart_write.zag.
if grep -v '^\s*//' evpart_write.zag | grep -q ',577,'; then
    fail "O_TRUNC open in evpart_write.zag (write-once violated)"
fi
echo "gate8: partition writer is create-only (O_EXCL), no O_TRUNC. OK."

echo "=== compiling ==="
$ZNC main.zag -o forkD 2>&1 | head -5
$ZNC ingest_main.zag -o ingest_sensor 2>&1 | head -5
echo "Build complete: src/forkD src/ingest_sensor"
ls -la forkD ingest_sensor
