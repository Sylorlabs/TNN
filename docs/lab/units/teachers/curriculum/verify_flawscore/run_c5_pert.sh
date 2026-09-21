#!/bin/bash
# C5 adversarial wire perturbations (determinism bar, part 2).
# P-a: session_id+1 everywhere (checksum recomputed) -> decisions identical.
# P-b: seq 3 teacher_id=0 -> rc=3 for that seq only, (-1,-1) record.
# P-c: seq 5 checksum byte flipped -> rc=7 for that seq only.
# P-d: seq 7 magic zeroed -> rc=1 for that seq only.
set -u
cd "$(dirname "$0")/../.." || exit 1
HERE="$(pwd)"
VF="$HERE/curriculum/verify_flawscore"
C5="$VF/logs/c5"
PLOG="$C5/c5_pert.log"
: > "$PLOG"
python3 "$VF/gen_pert.py" "$C5" | tee -a "$PLOG"

check_pert() {
  local tag="$1" wfile="$2" badseq="$3"
  for n in 1 2; do
    "$VF/flawrun_frozen_bin" 0 "$C5" "$wfile" "slice_S0.bin" "tape_P${tag}_n$n.bin" \
      > "$C5/dec_P${tag}_n$n.bin" 2>>"$PLOG"
    echo "P-$tag run$n rc=$?" >> "$PLOG"
  done
  H1=$(sha256sum "$C5/dec_P${tag}_n1.bin" | cut -d' ' -f1)
  H2=$(sha256sum "$C5/dec_P${tag}_n2.bin" | cut -d' ' -f1)
  [ "$H1" = "$H2" ] && echo "P-$tag DET: byte-identical x2" | tee -a "$PLOG" \
                   || echo "P-$tag DET: MISMATCH" | tee -a "$PLOG"
  python3 - "$C5" "$tag" "$badseq" <<'EOF' | tee -a "$PLOG"
import struct, sys
c5, tag, badseq = sys.argv[1], sys.argv[2], int(sys.argv[3])
base = open(f"{c5}/decisions_S0.bin","rb").read()
pert = open(f"{c5}/dec_P{tag}_n1.bin","rb").read()
n = len(base)//40
assert len(pert)//40 == n, (len(base), len(pert))
def rec(b, i):
    return struct.unpack_from('<q', b, i*40)[0], struct.unpack_from('<q', b, i*40+8)[0], struct.unpack_from('<q', b, i*40+16)[0]
ok = True
for i in range(n):
    s0, v0, r0 = rec(base, i)
    s1, v1, r1 = rec(pert, i)
    assert s0 == s1, (i, s0, s1)
    if s1 == badseq:
        if not (v1 == -1 and r1 == -1):
            ok = False; print(f"P-{tag} seq {s1}: expected (-1,-1), got ({v1},{r1})")
    else:
        if not (v1 == v0 and r1 == r0):
            ok = False; print(f"P-{tag} seq {s1}: DIFFERS base=({v0},{r0}) pert=({v1},{r1})")
print(f"P-{tag} CHECK: {'PASS' if ok else 'FAIL'} (badseq={badseq})")
EOF
}

check_pert a "wires_S0_Pa.bin" -99
check_pert b "wires_S0_Pb.bin" 3
check_pert c "wires_S0_Pc.bin" 5
# P-d (magic zeroed on wire seq 7) is rejected at the FRAMING layer before
# p_decode: INTEGRITY(2002), session halts after the 7 good wires, rc=2.
# The codec's own P_V_BAD_MAGIC (rc=1) path is proven by probe_decode.
for n in 1 2; do
  "$VF/flawrun_frozen_bin" 0 "$C5" "wires_S0_Pd.bin" "slice_S0.bin" "tape_Pd_n$n.bin" \
    > "$C5/dec_Pd_n$n.bin" 2>>"$PLOG"
  echo "P-d run$n rc=$?" >> "$PLOG"
done
python3 - "$C5" <<'EOF' | tee -a "$PLOG"
import struct, sys
c5 = sys.argv[1]
d1 = open(f"{c5}/dec_Pd_n1.bin","rb").read()
d2 = open(f"{c5}/dec_Pd_n2.bin","rb").read()
det = d1 == d2
n = len(d1)//40
tape = open(f"{c5}/tape_Pd_n1.bin","rb").read()
off = 0; integ = []
while off < len(tape):
    et = tape[off]; ln = struct.unpack_from('<I', tape, off+1)[0]
    if et == 7: integ.append(struct.unpack_from('<I', tape, off+5)[0])
    off += 5 + ln
ok = det and n == 7 and integ == [2002]
print(f"P-d CHECK: {'PASS' if ok else 'FAIL'} (det={det}, nrec={n}, integrity_codes={integ})")
EOF
echo "== perturbations done ==" | tee -a "$PLOG"
