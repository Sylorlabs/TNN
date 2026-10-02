#!/usr/bin/env python3
# voc3_tool.py — VOC2 -> VOC3 feasibility dry-run + converter (upscale round 4, arm P2).
#
# Prereg gate (PREREG_R4.md, arm P2): demonstrate BEFORE any battery run that a
# VOC3 binary vocab format can carry a per-atom source-image index that
# g_vocab_load reads: parse VOC2 byte-exactly, emit VOC3 = VOC2 + per-atom
# source index sourced from TEACH_TRACE.txt, reload it, byte-verify atom
# payloads unchanged. If the dry-run fails, P2 is VOID (reported, not worked
# around).
#
# Usage:
#   python3 voc3_tool.py --trace TEACH_TRACE.txt --voc2 vocab.bin --voc3 vocab_v3.bin
# Exit 0 + "DRY-RUN PASS" on success; exit 1 + "DRY-RUN VOID: <reason>" on failure.
import argparse, hashlib, re, struct, sys

SCALES = [(64, 48), (32, 48), (16, 48), (8, 32), (4, 64)]  # (S, K) per si 0..4
NULL_SRC = 255  # sentinel for the NULL (all-zero) atom 0 at every scale
EXPECTED_VOC2_SHA = "cbead2f7c13e455fb1598defc34182f7b2517dfaeb6f0fa95925e4f1f0d525b2"
EXPECTED_VOC2_SIZE = 1958448


def fail(reason):
    print(f"DRY-RUN VOID: {reason}")
    sys.exit(1)


def parse_trace(path):
    """Returns {(si, atom): src_img}. Raises fail() on any ambiguity."""
    text = open(path).read()
    lines = text.splitlines()
    table = {}
    cur_si = None
    # section headers: "scale S=64 ..." or "thin S=4 ..."
    for ln in lines:
        m = re.match(r'(?:thin )?scale S=(\d+)', ln) or re.match(r'thin S=(\d+)', ln)
        # note: "thin S=4 candidates=..." matches the second alternative
        if m:
            S = int(m.group(1))
            S_list = [s for s, k in SCALES]
            if S not in S_list:
                fail(f"trace: unknown scale S={S}")
            cur_si = S_list.index(S)
            continue
        m = re.match(r'\s*(?:thin )?atom (\d+): src_img=(\d+)\b', ln)
        if m:
            if cur_si is None:
                fail("trace: atom line before any scale section")
            ai, src = int(m.group(1)), int(m.group(2))
            K = SCALES[cur_si][1]
            if not (1 <= ai < K):
                fail(f"trace: si={cur_si} atom id {ai} outside 1..{K-1}")
            if not (0 <= src <= 3):
                fail(f"trace: si={cur_si} atom {ai} src_img={src} outside 0..3")
            if (cur_si, ai) in table:
                fail(f"trace: si={cur_si} atom {ai} listed twice (ambiguous)")
            table[(cur_si, ai)] = src
    # per-scale completeness: every atom 1..K-1 must appear exactly once
    for si, (S, K) in enumerate(SCALES):
        got = sorted(ai for (s2, ai) in table if s2 == si)
        want = list(range(1, K))
        if got != want:
            missing = [a for a in want if a not in got]
            extra = [a for a in got if a not in want]
            fail(f"trace: si={si} (S={S}) atoms != 1..{K-1}: "
                 f"count={len(got)} missing={missing[:8]} extra={extra[:8]}")
    return table


def parse_voc2(data):
    """Byte-exact VOC2 parse. Returns (scales, atom_offs, key_offs, body_end)."""
    if len(data) != EXPECTED_VOC2_SIZE:
        fail(f"vocab.bin size {len(data)} != expected {EXPECTED_VOC2_SIZE}")
    if data[0:4] != b"VOC2":
        fail(f"vocab.bin magic {data[0:4]!r} != b'VOC2'")
    (ns,) = struct.unpack_from("<I", data, 4)
    if ns != 5:
        fail(f"vocab.bin ns={ns} != 5")
    scales, atom_offs, key_offs = [], [], []
    off = 48
    for si in range(5):
        (S, K) = struct.unpack_from("<II", data, 8 + si * 8)
        if (S, K) != SCALES[si]:
            fail(f"vocab.bin scale {si}: (S,K)=({S},{K}) != expected {SCALES[si]}")
        scales.append((S, K))
        mb = S * S * 3 * 2
        s2 = S // 2
        kmb = s2 * s2 * 3 * 2
        atom_offs.append(off)
        off += K * mb
        key_offs.append(off)
        off += K * kmb
    if off != len(data):
        fail(f"vocab.bin layout ends at {off}, file size {len(data)} (slop!)")
    return scales, atom_offs, key_offs, off


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trace", required=True)
    ap.add_argument("--voc2", required=True)
    ap.add_argument("--voc3", required=True)
    args = ap.parse_args()

    voc2 = open(args.voc2, "rb").read()
    sha2 = hashlib.sha256(voc2).hexdigest()
    print(f"VOC2: {len(voc2)} bytes, SHA-256 {sha2}")
    if sha2 != EXPECTED_VOC2_SHA:
        fail(f"VOC2 SHA mismatch: got {sha2}, want {EXPECTED_VOC2_SHA}")
    print("VOC2 SHA matches frozen pin cbead2f7c13e455f...")

    scales, atom_offs, key_offs, body_end = parse_voc2(voc2)
    print(f"VOC2 header+body layout sums exactly to file size ({body_end}); zero slop.")

    table = parse_trace(args.trace)
    n_traced = len(table)
    print(f"TEACH_TRACE: {n_traced} traced atoms; per-scale counts match K-1 "
          f"(48,48,48,32,64 incl NULL atom 0).")

    # NULL-atom check: atom 0 at every scale must be all-zero in the binary.
    for si, (S, K) in enumerate(scales):
        payload = voc2[atom_offs[si]: atom_offs[si] + S * S * 3 * 2]
        if any(payload):
            nz = sum(1 for b in payload if b)
            fail(f"vocab.bin si={si} atom 0 not all-zero ({nz} nonzero bytes) "
                 f"— not the NULL atom")
    print("NULL check: atom 0 all-zero at all 5 scales (binary-verified).")

    # src_img distribution (informational)
    dist = {}
    for (si, ai), src in table.items():
        dist[src] = dist.get(src, 0) + 1
    print(f"src_img distribution over traced atoms: {dist} "
          f"(0=brick_wall 1=lake_water 2=foliage 3=stone_wall)")

    # Build the 240-byte table: scale-major, atoms 0..K-1; atom 0 -> 255.
    tab = bytearray()
    for si, (S, K) in enumerate(scales):
        for ai in range(K):
            tab.append(table.get((si, ai), NULL_SRC))
    assert len(tab) == 240, len(tab)
    # every non-NULL atom must have a real src (no accidental 255s)
    for si, (S, K) in enumerate(scales):
        base = sum(k for _, k in scales[:si])
        for ai in range(1, K):
            if tab[base + ai] == NULL_SRC:
                fail(f"internal: si={si} atom {ai} has NULL sentinel")
    print(f"VOC3 table: 240 bytes, scale-major; NULL atoms -> {NULL_SRC}.")

    # Emit VOC3: VOC2 bytes with magic -> "VOC3", table appended after keys.
    voc3 = bytearray(voc2)
    voc3[0:4] = b"VOC3"
    voc3 += tab
    assert len(voc3) == EXPECTED_VOC2_SIZE + 240
    with open(args.voc3, "wb") as f:
        f.write(voc3)
    sha3 = hashlib.sha256(bytes(voc3)).hexdigest()
    print(f"VOC3 written: {len(voc3)} bytes -> {args.voc3}")
    print(f"VOC3 SHA-256: {sha3}")

    # ---- reload + byte-verify ----
    r = open(args.voc3, "rb").read()
    if len(r) != EXPECTED_VOC2_SIZE + 240:
        fail(f"VOC3 reload size {len(r)} != {EXPECTED_VOC2_SIZE + 240}")
    if r[0:4] != b"VOC3":
        fail(f"VOC3 reload magic {r[0:4]!r} != b'VOC3'")
    # header (after magic) identical
    if r[4:48] != voc2[4:48]:
        fail("VOC3 header bytes 4..48 differ from VOC2")
    # every atom payload byte + every key byte identical
    if r[48:body_end] != voc2[48:]:
        # find first difference for the report
        for i, (a, b) in enumerate(zip(r[48:body_end], voc2[48:])):
            if a != b:
                fail(f"VOC3 body differs from VOC2 at file offset {48+i}")
        fail("VOC3 body length mismatch vs VOC2")
    # table round-trips
    if bytes(r[body_end:body_end + 240]) != bytes(tab):
        fail("VOC3 appended table does not round-trip")
    print("Reload check: header identical (mod magic), all atom/key payload bytes "
          "identical, 240-byte table round-trips.")
    print("DRY-RUN PASS")
    print(f"VOC3_SHA256={sha3}")


if __name__ == "__main__":
    main()
