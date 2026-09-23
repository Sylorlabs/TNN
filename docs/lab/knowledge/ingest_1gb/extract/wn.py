#!/usr/bin/env python3
"""Extract WordNet 3.1 synset glosses -> kind-4 fact records.
Reads wordnet31.zip (streamed from the corpus dir), writes run/wn.bin
records: [1B kind][2B key_len BE][4B text_len BE][key][text].
Deterministic. key = wn:3.1:{pos}:{offset:08d}
"""
import struct, sys, zipfile, os

CORPUS = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/corpus")
RUN = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/run")

def clean_gloss(g: str) -> str:
    g = g.strip()
    # drop trailing example quotes in "..."  -- keep the gloss itself
    return g

def parse_data(path_in_zip, pos, out, counts):
    with zipfile.ZipFile(os.path.join(CORPUS, "wordnet31.zip")) as z:
        with z.open(path_in_zip) as f:
            for raw in f:
                line = raw.decode("utf-8", errors="replace")
                if not line or line[0] == " ":
                    continue  # license header
                bar = line.find(" | ")
                if bar < 0:
                    continue
                head, gloss = line[:bar], line[bar + 3:]
                parts = head.split()
                if len(parts) < 4:
                    continue
                offset = parts[0]
                if not offset.isdigit():
                    continue
                g = clean_gloss(gloss)
                gb = g.encode("utf-8")
                if len(gb) < 4 or len(gb) > 4096:
                    continue
                if b"\x00" in gb:
                    continue
                key = f"wn:3.1:{pos}:{offset}".encode("ascii")
                out.write(bytes([4]) + struct.pack(">H", len(key)) + struct.pack(">I", len(gb)) + key + gb)
                counts[pos] += 1

def main():
    os.makedirs(RUN, exist_ok=True)
    counts = {"n": 0, "v": 0, "a": 0, "r": 0}
    with open(os.path.join(RUN, "wn.bin"), "wb") as out:
        parse_data("wordnet31/data.noun", "n", out, counts)
        parse_data("wordnet31/data.verb", "v", out, counts)
        parse_data("wordnet31/data.adj", "a", out, counts)
        parse_data("wordnet31/data.adv", "r", out, counts)
    total = sum(counts.values())
    print(f"wordnet facts: {total} {counts}")

if __name__ == "__main__":
    main()
