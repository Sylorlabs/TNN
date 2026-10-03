#!/usr/bin/env python3
"""V-NOLIMIT prereg probe: Python mirror of the V-NOLIMIT gate (no 4096B text
cap) + lesson CAL, streamed over the JOINED corpus (stdin).

Predicts: n (installed), g1, g2, g3, lessons, lessons_rejected.
The full-corpus teach must match these EXACTLY (prereg bar).

Gate rules mirrored from gate_nolimit.zag::ig_gate (V-NOLIMIT: G1 text upper
bound removed; all else identical to the frozen gate).
CAL mirrored from ig_process_lesson (frozen V0 semantics: first-4 must-accept
probes; 4 synthetic must-reject probes expecting [1,2,1,3]).

Record layout on stdin: [1B kind][2B klen BE][4B tlen BE][key][text]
Zero RNG. Deterministic.
"""
import struct
import sys

LESSON = 65536


def se_key_ok(key: bytes) -> bool:
    if len(key) < 8:
        return False
    if key[0:3] != b"se:":
        return False
    i = key.find(b":", 3)
    if i <= 3:
        return False
    if i + 3 >= len(key):
        return False
    if key[i + 1] not in (0x71, 0x61):  # q|a
        return False
    if key[i + 2] != 0x3A:
        return False
    j = i + 3
    return all(0x30 <= c <= 0x39 for c in key[j:])


def gate(kind, key, text, prev_key, has_prev):
    # G1: wellformed (V-NOLIMIT: no text upper bound)
    # NOTE: '\n' (10) < 32, so min(key)<32 covers the no-newline rule too.
    if kind < 5 or kind > 8:
        return 1
    if not (1 <= len(key) <= 160):
        return 1
    if min(key) < 32 or 127 in key:
        return 1
    if len(text) < 20:
        return 1
    # text: reject NUL, <32 except \n, 127. Replace \n with space (allowed)
    # so a single min()+membership test decides.
    t2 = text.replace(b"\n", b" ")
    if min(t2) < 32 or 127 in t2:
        return 1
    # G2: adjacent dupe
    if has_prev and key == prev_key:
        return 2
    # G3: consistency
    if kind == 6:
        if not se_key_ok(key):
            return 3
        i = key.find(b":", 3)
        if key[i + 1] == 0x71 and b"\n\n" not in text:
            return 3
    else:
        if b" " not in text:
            return 3
    return 0


# synthetic must-reject probes: (kind, key, text, expected)
R1 = (5, b"zzbad:r1", b"")
R2_TEXT = b"dupe probe of lesson fact zero"
R3 = (6, b"zzbad:\x00:r3", b"nul probe")
R4 = (6, b"se:zzsite:q:1", b"question without separator here")


def main():
    data = sys.stdin.buffer
    g1 = g2 = g3 = ninst = 0
    lessons = 0
    lessons_rej = 0
    prev_key = b""
    has_prev = False
    recs = []  # current lesson buffer: list of (kind, key, text)
    total = 0

    def read_rec():
        h = data.read(7)
        if not h:
            return None
        if len(h) < 7:
            raise ValueError("truncated header")
        kind, klen, tlen = struct.unpack(">BHI", h)
        kb = data.read(klen)
        tb = data.read(tlen)
        if len(kb) < klen or len(tb) < tlen:
            raise ValueError("truncated record")
        return kind, kb, tb

    def close_lesson(final):
        nonlocal g1, g2, g3, ninst, lessons, lessons_rej
        nonlocal prev_key, has_prev
        if not recs:
            return
        lessons += 1
        npeek = recs[:4]
        # CAL dry-run: must-accept (first 4), frozen prev
        cal_ok = True
        for kind, kb, tb in npeek:
            if gate(kind, kb, tb, prev_key, has_prev) != 0:
                cal_ok = False
        # must-reject synthetics
        exp = [1, 2, 1, 3]
        probes = [R1,
                  (5, recs[0][1], R2_TEXT),
                  R3, R4]
        for idx, ((pk, pt, px), e) in enumerate(zip(probes, exp)):
            if idx == 1:
                v = gate(pk, pt, px, recs[0][1], True)
            else:
                v = gate(pk, pt, px, b"", False)
            if v != e:
                cal_ok = False
        if not cal_ok:
            lessons_rej += 1
            return  # dropped: prev chain untouched
        # install with running prev
        for kind, kb, tb in recs:
            v = gate(kind, kb, tb, prev_key, has_prev)
            if v == 0:
                ninst += 1
            elif v == 1:
                g1 += 1
            elif v == 2:
                g2 += 1
            else:
                g3 += 1
            prev_key = kb
            has_prev = True

    while True:
        r = read_rec()
        if r is None:
            break
        recs.append(r)
        total += 1
        if len(recs) == LESSON:
            close_lesson(False)
            recs = []
    close_lesson(True)

    print(f"total_records={total}")
    expected = int(sys.argv[1]) if len(sys.argv) > 1 else 9261548
    assert total == expected, f"expected {expected} records, got {total}"
    print(f"n={ninst} g1={g1} g2={g2} g3={g3}")
    print(f"lessons={lessons} lessons_rejected={lessons_rej}")
    dropped = total - (ninst + g1 + g2 + g3)
    print(f"dropped_in_rejected_lessons={dropped}")


if __name__ == "__main__":
    main()
