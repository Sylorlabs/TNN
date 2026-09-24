#!/bin/bash
# KB3 tamper battery: the partition must detect 100% of tampering.
# Each case: tamper corpora/c1/partition.dat (keep the ORIGINAL head.txt),
# run `forkD verify`, and run the c1 battery against the tampered partition.
# Expected: every verify -> INVALID; every battery -> all WITHHOLD (safe failure).
set -u
cd "$(dirname "$0")/src"
TDIR=../evidence/tamper
rm -rf "$TDIR"
mkdir -p "$TDIR"
SRC=corpora/c1/partition.dat
HEAD=corpora/c1/head.txt
pass=0; total=0

check_invalid() { # $1=name $2=partition
    total=$((total+1))
    out=$(./forkD verify "$2" "$HEAD" 2>&1)
    if echo "$out" | grep -q "^VALID"; then
        echo "TAMPER-$1: FAIL (verify said VALID)"
    else
        echo "TAMPER-$1: PASS (INVALID detected)"
        pass=$((pass+1))
    fi
}

check_battery_withhold() { # $1=name $2=partition
    total=$((total+1))
    d="$TDIR/bat-$1"
    mkdir -p "$d"
    cp "$2" "$d/partition.dat"          # tampered partition
    cp "$HEAD" "$d/head.txt"            # ORIGINAL anchor
    cp corpora/c1/manifest.txt "$d/manifest.txt"
    cp -r corpora/c1/drafts corpora/c1/delib "$d/"
    ( cd "$d" && /home/hatch/workspace/scratch-h6r3/w1/src/forkD battery manifest.txt > battery.out 2> battery.err )
    bad=$(grep -c "|INSTALL|" "$d/battery.out" || true)
    if [ "$bad" = "0" ]; then
        echo "BATTERY-$1: PASS (all WITHHOLD on invalid partition)"
        pass=$((pass+1))
    else
        echo "BATTERY-$1: FAIL ($bad INSTALL on invalid partition)"
    fi
}

# T1: entry flip (atom field changed, digest kept) -> digest mismatch.
sed '2s/|mammal|/|mammax|/' "$SRC" > "$TDIR/t1.dat"
check_invalid "t1-entry-flip" "$TDIR/t1.dat"

# T2: digest flip (flip the LAST hex char of entry 1's digest) -> digest mismatch.
python3 - "$SRC" "$TDIR/t2.dat" << 'PYEOF'
import sys
src, dst = sys.argv[1], sys.argv[2]
lines = open(src).read().splitlines()
head, rest = lines[1].rsplit("|", 1)
last = rest[-1]
flipped = "0" if last != "0" else "1"
lines[1] = head + "|" + rest[:-1] + flipped
open(dst, "w").write("\n".join(lines) + "\n")
print("t2: flipped digest tail", last, "->", flipped)
PYEOF
check_invalid "t2-digest-flip" "$TDIR/t2.dat"

# T3: swap entries 1 and 2 -> seq mismatch.
{ head -1 "$SRC"; sed -n '3p' "$SRC"; sed -n '2p' "$SRC"; tail -n +4 "$SRC"; } > "$TDIR/t3.dat"
check_invalid "t3-swap" "$TDIR/t3.dat"

# T4: truncation (drop last entry) -> head != anchor.
head -n -1 "$SRC" > "$TDIR/t4.dat"
check_invalid "t4-truncate" "$TDIR/t4.dat"

# T5: forged suffix - a VALIDLY-CHAINED extra entry against the STALE anchor.
# Computed with python (independent implementation of the chain rule).
python3 - "$SRC" "$TDIR/t5.dat" << 'PYEOF'
import sys, hashlib
src, dst = sys.argv[1], sys.argv[2]
lines = open(src).read().splitlines()
prev = bytes.fromhex(lines[-1].rsplit("|",1)[1])
n = len(lines) - 1  # entries
seq = n + 1
atom = b"UNIT|moon|POS|LOC_ON|table"
d = hashlib.sha256(prev + seq.to_bytes(8,"big") + atom + b"\x0a").digest()
open(dst,"w").write("\n".join(lines) + f"\n{seq}|{atom.decode()}|{d.hex()}\n")
PYEOF
check_invalid "t5-forged-suffix" "$TDIR/t5.dat"
# also confirm the forged suffix is a *valid* chain under its own head
python3 - "$TDIR/t5.dat" << 'PYEOF'
import sys, hashlib
lines = open(sys.argv[1]).read().splitlines()
assert lines[0]=="EVPART1"
prev = bytes(32)
for ln in lines[1:]:
    s,a,h = ln.split("|",1)[0], ln.rsplit("|",1)[0].split("|",1)[1], ln.rsplit("|",1)[1]
    d = hashlib.sha256(prev + int(s).to_bytes(8,"big") + a.encode() + b"\x0a").digest()
    assert d.hex()==h, "chain broken"
    prev = d
print("t5 chain self-consistent: yes (detection is via the external anchor)")
PYEOF

# T6: unpartitioned live-state mutation must not move any verdict.
# Copy the c5 corpus, add a bogus live_state.txt full of forged GEN entries,
# run the battery on the copy -> verdicts must equal the pristine run.
mkdir -p "$TDIR/c5live"
cp -r corpora/c5/partition.dat corpora/c5/head.txt corpora/c5/manifest.txt corpora/c5/drafts corpora/c5/delib "$TDIR/c5live/"
python3 - << 'PYEOF'
# bogus live state: forged GEN entries an attacker wishes were trusted
ls = open("/home/hatch/workspace/scratch-h6r3/w1/evidence/tamper/c5live/live_state.txt","w")
for i in range(25):
    ls.write(f"UNIT|gen{i}|POS|IS_A|robot|GEN\n")
ls.close()
print("wrote bogus live_state.txt (25 forged GEN entries)")
PYEOF
total=$((total+1))
( cd "$TDIR/c5live" && /home/hatch/workspace/scratch-h6r3/w1/src/forkD battery manifest.txt > ../bat-t6.out 2> ../bat-t6.err )
if diff -q <(grep -v "^digest=" ../evidence/run1/c5.out) <(grep -v "^digest=" "$TDIR/bat-t6.out") > /dev/null; then
    echo "TAMPER-t6-live-state: PASS (verdicts unchanged by unpartitioned mutation)"
    pass=$((pass+1))
else
    echo "TAMPER-t6-live-state: FAIL (verdicts moved)"
fi

# Safe-failure batteries on the invalid partitions.
check_battery_withhold "t1" "$TDIR/t1.dat"
check_battery_withhold "t4" "$TDIR/t4.dat"
check_battery_withhold "t5" "$TDIR/t5.dat"

echo "KB3: $pass/$total tamper checks passed"
[ "$pass" = "$total" ]
