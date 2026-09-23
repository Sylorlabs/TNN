#!/usr/bin/env python3
"""TNN Track A corpus pipeline — builds the deterministic corpus directory.

Reads raw downloads from corpora/raw/, writes the frozen corpus set into
corpora/<stamp>/. Deterministic: no RNG anywhere. Every derived file is a pure
function of the raw downloads + constants below.

Layout produced:
  prose.bin        full Shakespeare (corpus A, "prose")
  code.bin         full sqlite3.c   (corpus B, "code")
  t1_prose.bin     last 10% of prose.bin by fixed byte offset (T1 novel tier)
  t1_code.bin      last 10% of code.bin  by fixed byte offset (T1 novel tier)
  t2_prose.bin     KJV Bible (T2 third corpus, prose)
  t2_code.bin      CPython Objects/longobject.c (T2 third corpus, code)
  t3.bin           synthetic deterministic bytes, xorshift64* seed T3_SEED (T3 tier)
  churn_fresh.bin  448000 bytes deterministic fresh material for the M3 rig
  mem_vocab.txt    top-5000 whitespace tokens of prose train split (memorizer control)
  MANIFEST.json    byte sizes + sha256 of every file + split offsets + seed

T1 split: offset = floor(len * 9 / 10); t1 = data[offset:].
10x legs are built on demand by legs10x.py (not stored here).
"""
import hashlib
import json
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "corpora", "raw")
T3_SEED = 0x544E4E3300000033  # "TNN 3" — logged, fixed, environment input
T3_LEN = 1 << 20              # 1 MiB synthetic
CHURN_FRESH_LEN = 448000      # 7000 units x 64 bytes (M3 fresh material)
MEM_VOCAB_N = 5000
SEP10_FMT = b"\n<<<TNN-UNIT-10X-SEP-%08d>>>\n"  # deterministic 10x separator

MASK64 = (1 << 64) - 1


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def xorshift64star(state: int):
    while True:
        state ^= (state >> 12) & MASK64
        state ^= (state << 25) & MASK64
        state ^= (state >> 27) & MASK64
        state = (state * 0x2545F4914F6CDD1D) & MASK64
        yield state


def build_t3() -> bytes:
    """Deterministic synthetic stream with controlled statistics.

    Cycles every 4096 bytes: 2048 xorshift bytes, 512-byte constant run,
    1024-byte ascending sawtooth, 512 bytes of 2-byte alternating pattern.
    Seed fixed (T3_SEED); this is environment input, not an AI decision.
    """
    gen = xorshift64star(T3_SEED)
    out = bytearray()
    const_byte = 0
    while len(out) < T3_LEN:
        for _ in range(2048):
            out.append(next(gen) & 0xFF)
        const_byte = (const_byte + 0x11) & 0xFF
        out.extend([const_byte] * 512)
        base = next(gen) & 0xFF
        for i in range(1024):
            out.append((base + i) & 0xFF)
        a = next(gen) & 0xFF
        b = next(gen) & 0xFF
        for _ in range(256):
            out.append(a)
            out.append(b)
    return bytes(out[:T3_LEN])


def build_churn_fresh(prose: bytes, code: bytes) -> bytes:
    """448000 deterministic fresh bytes for the M3 churn rig.

    Recipe (fixed): alternate 65536-byte windows of prose and code from offset 0,
    joined by 64-byte separators "---TNN-CHURN-SEP-<k:06d>---" padded with '-'.
    Truncated to exactly CHURN_FRESH_LEN bytes.
    """
    out = bytearray()
    k = 0
    win = 65536
    while len(out) < CHURN_FRESH_LEN:
        src = prose if (k % 2 == 0) else code
        seg = src[(k // 2 * win) % max(1, len(src) - win):][:win]
        out.extend(seg)
        tag = ("---TNN-CHURN-SEP-%06d---" % k).encode()
        out.extend(tag + b"-" * (64 - len(tag)))
        k += 1
    return bytes(out[:CHURN_FRESH_LEN])


def top_tokens(prose_train: bytes, n: int):
    """Top-n whitespace-delimited byte tokens by frequency.

    Deterministic: count, then sort by (-count, token_bytes). Tokens longer than
    64 bytes are truncated to 64 for the vocab file (length cap logged).
    """
    counts = {}
    for tok in prose_train.split():
        counts[tok] = counts.get(tok, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    vocab = []
    for tok, _ in ranked[:n]:
        vocab.append(tok[:64])
    return vocab


def main():
    stamp = sys.argv[1] if len(sys.argv) > 1 else "r1"
    outdir = os.path.join(HERE, "corpora", stamp)
    os.makedirs(outdir, exist_ok=True)

    def raw(name):
        p = os.path.join(RAW, name)
        if not os.path.exists(p):
            sys.exit(f"missing raw download: {p}")
        with open(p, "rb") as f:
            return f.read()

    pg100 = raw("pg100.txt")
    pg10 = raw("pg10.txt")
    longobject = raw("longobject.c")

    # sqlite3.c: prefer an extracted sqlite3.c, else unzip the amalgamation.
    sqlite_c = None
    if os.path.exists(os.path.join(RAW, "sqlite3.c")):
        sqlite_c = raw("sqlite3.c")
    else:
        zp = os.path.join(RAW, "sqlite_amalgamation.zip")
        if not os.path.exists(zp):
            sys.exit("missing sqlite amalgamation (no sqlite3.c and no zip)")
        with zipfile.ZipFile(zp) as z:
            names = [n for n in z.namelist() if n.endswith("/sqlite3.c") or n == "sqlite3.c"]
            if not names:
                sys.exit(f"no sqlite3.c inside {zp}: {z.namelist()[:10]}")
            sqlite_c = z.read(names[0])
            with open(os.path.join(RAW, "sqlite3.c"), "wb") as f:
                f.write(sqlite_c)

    prose, code = pg100, sqlite_c
    t2_prose, t2_code = pg10, longobject

    off_p = (len(prose) * 9) // 10
    off_c = (len(code) * 9) // 10
    t1_prose, t1_code = prose[off_p:], code[off_c:]

    t3 = build_t3()
    churn_fresh = build_churn_fresh(prose, code)
    vocab = top_tokens(prose[:off_p], MEM_VOCAB_N)

    files = {
        "prose.bin": prose,
        "code.bin": code,
        "t1_prose.bin": t1_prose,
        "t1_code.bin": t1_code,
        "t2_prose.bin": t2_prose,
        "t2_code.bin": t2_code,
        "t3.bin": t3,
        "churn_fresh.bin": churn_fresh,
    }
    manifest = {"files": {}, "t1_split": {"prose_offset": off_p, "code_offset": off_c},
                "t3_seed_hex": "0x%016x" % T3_SEED, "t3_len": T3_LEN,
                "churn_fresh_len": CHURN_FRESH_LEN,
                "mem_vocab_n": len(vocab),
                "sep10_format": SEP10_FMT.decode().replace("%08d", "<k:08d>")}
    for name, data in files.items():
        p = os.path.join(outdir, name)
        with open(p, "wb") as f:
            f.write(data)
        manifest["files"][name] = {"bytes": len(data), "sha256": sha256(data)}
    vp = os.path.join(outdir, "mem_vocab.txt")
    with open(vp, "wb") as f:
        for tok in vocab:
            f.write(tok + b"\n")
    with open(vp, "rb") as f:
        manifest["files"]["mem_vocab.txt"] = {"bytes": os.path.getsize(vp),
                                              "sha256": sha256(f.read())}
    mp = os.path.join(outdir, "MANIFEST.json")
    with open(mp, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    print(json.dumps({"outdir": outdir,
                      "prose_bytes": len(prose), "code_bytes": len(code),
                      "t1_prose_bytes": len(t1_prose), "t1_code_bytes": len(t1_code),
                      "t2_prose_bytes": len(t2_prose), "t2_code_bytes": len(t2_code)},
                     indent=2))


if __name__ == "__main__":
    main()
