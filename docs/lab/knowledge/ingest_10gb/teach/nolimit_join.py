#!/usr/bin/env python3
"""V-NOLIMIT corpus inverter.

Joins every `...~N` chunk group back into one whole record WITHOUT re-running
the 40h source pipeline, and PROVES the join exact: re-splitting each joined
text with the REAL r9_split_para_HISTORICAL must reproduce the original chunks
byte-identically (100% of joined groups, 0 failures tolerated).

Canonical inverse separator
----------------------------
The splitter cuts at the LAST sentence terminator inside each 4096-byte
window. A naive "\n\n" join fails on 111 groups: the joined text pulls a
later sentence terminator INTO the 4096 window, so the re-split cuts later
than the original boundary. The reason is GEOMETRIC, not whitespace
recovery: padding the separator pushes the next chunk's later terminator
outside the current window. (An earlier draft wrongly attributed large L to
"exotic whitespace" length — not proven and generally false. The original
boundary whitespace was irreversibly discarded by rstrip()/lstrip() and is
NOT recovered; this is a deterministic canonical preimage.)

Fix: separate chunks with "\n"*L where L is the MINIMAL L>=2 such that
r9_split_para(join)==chunks (deterministic search with the real splitter;
L<=8192, abort fail-loud beyond). Larger L only shrinks the next-chunk
prefix covered by each 4096 window, so the first working L is well-defined
and every group carries its own proof. 51,496 multi-chunk groups keep L=2;
107 need L=3..119; 4 need L=459..1711 (the 111 naive-join failures). 197
single-chunk groups need no separator. Chunks are byte-identical; only the
(already-lost) boundary whitespace is canonicalized.

Modes:
  proof : stream FACTS, verify round-trip for 100% of groups, print stats.
          Exit 0 iff 0 failures (any failure raises).
  build : stream FACTS, write joined corpus records to stdout (binary) and
          ALL diagnostics to stderr. Exit nonzero on any round-trip failure.

Record layout out: [1B kind][2B klen BE][4B tlen BE][key][text] (same as FACTS).
Non-tilde records pass through byte-identical, in order.
Tilde groups are emitted in place of their FIRST chunk's position, key =
base key (tilde suffix stripped), chunks sorted numerically by N.
Collision guard: a base key that also exists as a non-tilde record aborts
(the join would silently merge two distinct records).

Zero RNG. Deterministic: sorted group emission, minimal-L search.
"""
import re
import struct
import sys

sys.path.insert(0, "/home/hatch/workspace/tnn-lab/knowledge/ingest_10gb/teach")
# NOTE: nolimit_join.py must use the HISTORICAL r9_split_para (the 4096B
# splitter that created the corpus), NOT the patched clean2.py (which no
# longer splits, per the no-stupid-limits law, patched 2026-09-24). The
# original is embedded below; do NOT import it from clean2.
SENT_END_RE = re.compile(r"[.!?](?=\s|$)")

def r9_split_para_HISTORICAL(p: str):
    """The ORIGINAL 4096B splitter (pre-2026-09-24 patch). Used ONLY to verify
    the join inverts the historical chunking. Deterministic."""
    b = p.encode("utf-8")
    chunks = []
    while len(b) > 4096:
        window = b[:4096].decode("utf-8", errors="ignore")
        cut = -1
        for m in SENT_END_RE.finditer(window):
            cut = m.end()
        if cut > 0:
            head = window[:cut]
        else:
            head = b[:4096].decode("utf-8", errors="ignore")
            if not head:
                head = window[:2048]
        chunks.append(head.rstrip())
        rest = p[len(head):].lstrip()
        p = rest
        b = p.encode("utf-8")
    if p:
        chunks.append(p)
    return chunks

CHUNK_RE = re.compile(rb"^(.*)~(\d+)$")
FACTS = "/home/hatch/workspace/scratch_10gb_work/dryrun/dryrun_facts.dat"
MAX_L = 8192


def read_records(f):
    while True:
        h = f.read(7)
        if not h:
            return
        if len(h) < 7:
            raise ValueError("truncated header")
        kind, klen, tlen = struct.unpack(">BHI", h)
        kb = f.read(klen)
        tb = f.read(tlen)
        if len(kb) < klen or len(tb) < tlen:
            raise ValueError("truncated record body")
        yield kind, kb, tb


def canonical_join(chunks):
    """chunks: list of (n:int, text:bytes) for one group.
    Returns (joined_text:str, L:int). Raises on failure (fail-loud)."""
    texts = [t.decode("utf-8") for _, t in chunks]
    if len(texts) == 1:
        # single surviving chunk: join is identity; still verify
        if r9_split_para_HISTORICAL(texts[0]) != texts:
            raise ValueError("single-chunk group does not round-trip")
        return texts[0], 0
    L = 2
    while L <= MAX_L:
        joined = ("\n" * L).join(texts)
        if r9_split_para_HISTORICAL(joined) == texts:
            return joined, L
        L += 1
    raise ValueError(f"no separator L<={MAX_L} round-trips group")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "proof"
    assert mode in ("proof", "build"), "mode must be proof|build"

    out = sys.stdout.buffer if mode == "build" else None
    log = sys.stderr

    n_tilde = 0
    n_groups = 0
    n_nontilde = 0
    n_single = 0
    l_hist = {}
    max_chunks = 0
    max_joined = 0
    max_L_used = 0
    seen_bases = set()
    n_written = 0

    def emit_group(kind, base, chunks):
        nonlocal n_groups, max_chunks, max_joined, max_L_used, n_written
        nonlocal n_single
        chunks.sort(key=lambda c: c[0])
        # duplicate chunk indices = corrupt group -> fail loud
        idxs = [c[0] for c in chunks]
        if len(set(idxs)) != len(idxs):
            raise ValueError(f"duplicate chunk index in group {base!r}")
        max_chunks = max(max_chunks, len(chunks))
        joined, L = canonical_join(chunks)
        max_joined = max(max_joined, len(joined.encode("utf-8")))
        max_L_used = max(max_L_used, L)
        if len(chunks) == 1:
            n_single += 1
        else:
            l_hist[L] = l_hist.get(L, 0) + 1
        n_groups += 1
        if mode == "build":
            tb = joined.encode("utf-8")
            out.write(struct.pack(">BHI", kind, len(base), len(tb)))
            out.write(base)
            out.write(tb)
            n_written += 1

    cur_kind, cur_base, cur_chunks = None, None, []
    prev_nontilde_kb = None  # last non-tilde key seen (for before-case collision)
    with open(FACTS, "rb") as f:
        for kind, kb, tb in read_records(f):
            m = CHUNK_RE.match(kb) if b"~" in kb else None
            if m:
                base, n = m.group(1), int(m.group(2))
                n_tilde += 1
                if base != cur_base:
                    if cur_base is not None:
                        emit_group(cur_kind, cur_base, cur_chunks)
                        seen_bases.add(cur_base)
                    # before-case: in sorted byte order a bare base key
                    # sorts immediately before its ~N group (no key can fall
                    # between B and B~0 under the corpus key grammar), so the
                    # previous non-tilde key is the only possible collider.
                    if prev_nontilde_kb == base:
                        raise ValueError(f"base-key collision (before): {kb!r}")
                    cur_kind, cur_base, cur_chunks = kind, base, []
                cur_chunks.append((n, tb))
            else:
                if cur_base is not None:
                    emit_group(cur_kind, cur_base, cur_chunks)
                    seen_bases.add(cur_base)
                    cur_kind, cur_base, cur_chunks = None, None, []
                # after-case: non-tilde key equal to an already-seen tilde base
                # (cannot happen in sorted order, but kept as defense in depth)
                if kb in seen_bases:
                    raise ValueError(f"base-key collision (after): {kb!r}")
                prev_nontilde_kb = kb
                n_nontilde += 1
                if mode == "build":
                    out.write(struct.pack(">BHI", kind, len(kb), len(tb)))
                    out.write(kb)
                    out.write(tb)
                    n_written += 1
    if cur_base is not None:
        emit_group(cur_kind, cur_base, cur_chunks)

    print(f"mode={mode}", file=log)
    print(f"tilde_records={n_tilde}", file=log)
    print(f"groups={n_groups} (single_chunk_groups={n_single})", file=log)
    print(f"nontilde_records={n_nontilde}", file=log)
    print(f"max_chunks_per_group={max_chunks}", file=log)
    print(f"max_joined_bytes={max_joined}", file=log)
    print(f"max_L_used={max_L_used}", file=log)
    print(f"L_histogram={dict(sorted(l_hist.items()))}", file=log)
    if mode == "build":
        print(f"records_written={n_written}", file=log)
        # expected: 9,209,744 + 51,804 = 9,261,548
        if n_written != 9261548:
            print(f"ERROR: expected 9261548 records, wrote {n_written}",
                  file=log)
            sys.exit(1)
    print("ROUND_TRIP_OK: 100% of joined groups reproduce chunks exactly",
          file=log)


if __name__ == "__main__":
    main()
