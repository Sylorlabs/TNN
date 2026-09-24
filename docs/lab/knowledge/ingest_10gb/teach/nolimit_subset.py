#!/usr/bin/env python3
"""V-NOLIMIT cherry-pick subsets (deterministic).

CP1nol: all 51,804 joined whole-record groups (the "tilde-only" analog).
CP2nol: joined records whose source position (first-chunk position for groups;
        own position for non-tilde) falls in original lessons {84,116,124}
        (the 3 V0-dropped lessons).

Usage: nolimit_subset.py cp1|cp2  > out.dat   (binary records to stdout,
        diagnostics to stderr)

Record layout: [1B kind][2B klen BE][4B tlen BE][key][text].
Zero RNG.
"""
import struct
import sys

sys.path.insert(0, "/home/hatch/workspace/scratch_10gb_work/nolimit")
from nolimit_join import read_records, canonical_join, CHUNK_RE, FACTS

LESSON = 65536
DROP_LESSONS = {84, 116, 124}


def main():
    which = sys.argv[1]
    assert which in ("cp1", "cp2"), "cp1|cp2"
    log = sys.stderr
    out = sys.stdout.buffer

    n_written = 0
    n_pos = 0  # original 0-based record position
    cur_kind, cur_base, cur_chunks = None, None, []
    cur_nfirst = 0

    def emit_group(kind, base, chunks, nfirst):
        nonlocal n_written
        chunks.sort(key=lambda c: c[0])
        joined, L = canonical_join(chunks)
        take = (which == "cp1") or (nfirst // LESSON in DROP_LESSONS)
        if take:
            tb = joined.encode("utf-8")
            out.write(struct.pack(">BHI", kind, len(base), len(tb)))
            out.write(base)
            out.write(tb)
            n_written += 1

    with open(FACTS, "rb") as f:
        for kind, kb, tb in read_records(f):
            m = CHUNK_RE.match(kb) if b"~" in kb else None
            if m:
                base, n = m.group(1), int(m.group(2))
                if base != cur_base:
                    if cur_base is not None:
                        emit_group(cur_kind, cur_base, cur_chunks, cur_nfirst)
                    cur_kind, cur_base, cur_chunks = kind, base, []
                    cur_nfirst = n_pos
                cur_chunks.append((n, tb))
            else:
                if cur_base is not None:
                    emit_group(cur_kind, cur_base, cur_chunks, cur_nfirst)
                    cur_kind, cur_base, cur_chunks = None, None, []
                if which == "cp2" and (n_pos // LESSON in DROP_LESSONS):
                    out.write(struct.pack(">BHI", kind, len(kb), len(tb)))
                    out.write(kb)
                    out.write(tb)
                    n_written += 1
            n_pos += 1
    if cur_base is not None:
        emit_group(cur_kind, cur_base, cur_chunks, cur_nfirst)

    print(f"subset={which} records_written={n_written}", file=log)


if __name__ == "__main__":
    main()
