#!/usr/bin/env python3
"""Glue: deterministic fixture generator for red-team batteries (Python glue only;
all gates/decisions run in the Zag ingest binary)."""
import struct, sys, os

def rec(kind, key: bytes, text: bytes) -> bytes:
    assert 1 <= len(key) <= 160 and 0 <= len(text) <= 4096
    return bytes([kind]) + struct.pack(">H", len(key)) + struct.pack(">I", len(text)) + key + text

def write_facts(path, records):
    records = sorted(records, key=lambda r: r[1])
    with open(path, "wb") as f:
        for k, key, text in records:
            f.write(rec(k, key, text))
    return records

def write_bad(path, last_key):
    # frozen 1200-record negative control: 200 G2 dupes, 250 empty, 250 NUL-key,
    # 250 circular dict, 250 no-terminal-punct -> expect g1=500,g2=200,g3=500,inst=0
    bad = []
    for _ in range(200):
        bad.append(rec(1, last_key, b"dupe of the last real key probe"))
    for i in range(250):
        bad.append(rec(1, f"zzbad:e1:{i:04d}".encode(), b""))
    for i in range(250):
        bad.append(rec(1, b"zzbad\x00:e2:%04d" % i, b"nul key probe text"))
    for i in range(250):
        w = f"zzcirc{i:04d}".encode()
        bad.append(rec(1, b"wikt:en:" + w + b":noun:1", w))
    for i in range(250):
        bad.append(rec(3, f"zzbad:w:{i:04d}".encode(), b"this sentence has no terminal punctuation"))
    assert len(bad) == 1200
    with open(path, "wb") as f:
        for b in bad:
            f.write(b)

def battery_a(d):
    # 60 false + 20 honest
    F, H = [], []
    for i in range(15):  # misattributed dict glosses
        F.append((1, f"wikt:en:rtf{i:04d}:noun:1".encode(),
                  f"a large marine mammal of the arctic ocean, specimen {i}".encode()))
    for p in range(5):  # swapped sense pairs (10 records, both false)
        F.append((1, f"wikt:en:rtswp{p:02d}a:noun:1".encode(), f"a hand tool for driving nails, type {p}b".encode()))
        F.append((1, f"wikt:en:rtswp{p:02d}b:noun:1".encode(), f"a sweet baked dessert topped with icing, type {p}a".encode()))
    for p in range(5):  # subtle-negation contradictory pairs (10 records, both false)
        F.append((3, f"sw:rtn{p:02d}a".encode(), f"The Eiffel Tower stands in Berlin, sector {p}.".encode()))
        F.append((3, f"sw:rtn{p:02d}b".encode(), f"The Eiffel Tower does not stand in Paris, sector {p}.".encode()))
    for i in range(10):  # false inflections naming the headword
        w = f"rtfi{i:04d}".encode()
        F.append((2, b"wikt:en:" + w + b":verb:3", w + b" is the past tense form meaning to photosynthesize at night"))
    for i in range(10):  # false wiki sentences
        F.append((3, f"sw:rtw{i:04d}".encode(), f"The capital of France is Berlin, according to survey {i}.".encode()))
    for i in range(5):  # false wordnet glosses
        w = f"rtwn{i:04d}".encode()
        F.append((4, b"wn:" + w + b".n.01:" + w, b"a flightless bird native to antarctica"))
    assert len(F) == 60
    H.append((1, b"wikt:en:apple:noun:1", b"a round fruit that grows on trees"))
    H.append((1, b"wikt:en:paris:propn:1", b"the capital city of france"))
    H.append((1, b"wikt:en:water:noun:1", b"a clear colorless liquid"))
    H.append((1, b"wikt:en:gold:noun:1", b"a precious yellow metal"))
    H.append((1, b"wikt:en:dog:noun:1", b"a domesticated carnivorous mammal"))
    for i in range(5):
        H.append((3, f"sw:rthon{i:04d}".encode(), f"Water boils at 100 degrees Celsius at sea level, note {i}.".encode()))
    for i in range(5):
        w = f"rthonw{i:04d}".encode()
        H.append((4, b"wn:" + w + b".n.01:" + w, b"a domesticated mammal kept as a pet"))
    for i in range(5):
        w = f"rthonv{i:04d}".encode()
        H.append((2, b"wikt:en:" + w + b":verb:1", w + b" means to move swiftly on foot"))
    assert len(H) == 20
    recs = write_facts(f"{d}/facts.bin", F + H)
    write_bad(f"{d}/bad.bin", recs[-1][1])
    # save attack keys + expected texts for query verification
    with open(f"{d}/attack_keys.tsv", "w") as f:
        for k, key, text in F:
            f.write(key.decode() + "\t" + text.decode() + "\n")
    with open(f"{d}/honest_keys.tsv", "w") as f:
        for k, key, text in H:
            f.write(key.decode() + "\t" + text.decode() + "\n")

def battery_b(d):
    P = []
    P.append((1, b"wikt:en:rtparis:propn:1", b"the capital city of france"))
    P.append((1, b"wikt:en:rtparis:propn:2", b"the capital city of italy"))
    P.append((3, b"sw:rtbird1", b"All birds can fly without exception."))
    P.append((3, b"sw:rtbird2", b"No birds can fly under any circumstance."))
    P.append((1, b"wikt:en:rtgold:noun:1", b"a precious yellow metal"))
    P.append((1, b"wikt:en:rtgold:noun:2", b"a cheap grey plastic"))
    P.append((2, b"wikt:en:rtrun:verb:1", b"rtrun means to move fast on foot"))
    P.append((2, b"wikt:en:rtrun:verb:2", b"rtrun means to stay completely still"))
    P.append((3, b"sw:rttower1", b"The Eiffel Tower is in Paris."))
    P.append((3, b"sw:rttower2", b"The Eiffel Tower is in Berlin."))
    assert len(P) == 10
    recs = write_facts(f"{d}/facts.bin", P)
    write_bad(f"{d}/bad.bin", recs[-1][1])

def battery_e(d):
    # 3 lessons x 65536; poison (kind1 empty text) at lesson positions 0, 1000, 4
    recs = []
    poisons = {0: {0}, 1: {1000}, 2: {4}}
    for L in range(3):
        for i in range(65536):
            key = f"rte{L}:{i:07d}".encode()
            if i in poisons[L]:
                recs.append((1, key, b""))
            else:
                recs.append((3, key, f"Record number {i} states that the sky appears blue during daytime.".encode()))
    assert len(recs) == 196608
    out = write_facts(f"{d}/facts.bin", recs)
    write_bad(f"{d}/bad.bin", out[-1][1])

def battery_g(d, n=260000):
    recs = []
    for i in range(n):
        key = f"rtg:{i:07d}".encode()
        text = f"Statement {i} records that engineered systems require deliberate verification before deployment in production.".encode()
        recs.append((3, key, text))
    out = write_facts(f"{d}/facts.bin", recs)
    write_bad(f"{d}/bad.bin", out[-1][1])
    print("g facts bytes:", os.path.getsize(f"{d}/facts.bin"))

if __name__ == "__main__":
    which = sys.argv[1]
    d = sys.argv[2]
    os.makedirs(d, exist_ok=True)
    {"a": battery_a, "b": battery_b, "e": battery_e, "g": battery_g}[which](d)
    print("done", which, d)
