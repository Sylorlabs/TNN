#!/usr/bin/env python3
"""Prove the wiktionary extractor is deterministic on real dump data.

Extracts the first N pages (default 20000) using the exact same page-split,
byte filters, and parse_page_text as extract/wikt.py, writes records to
<out>. Run twice; byte-identical SHA256 proves per-page determinism
(no RNG, no hash-order dependence, no hidden state in the parse path).

Usage: verify_extract_determinism.py <npages> <out.bin>
"""
import bz2, os, sys, hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wikt_slow import parse_page as parse_page_text

CORPUS = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/corpus")
DUMP = os.path.join(CORPUS, "enwiktionary-latest-pages-articles.xml.bz2")

def extract_n(npages, outp):
    stats = {1: 0, 2: 0}
    n_pages = 0
    h = hashlib.sha256()
    # hash the bytes as written: wrap the file object
    out = open(outp, "wb")
    class H:
        def write(self, b):
            h.update(b)
            return out.write(b)
        def flush(self):
            return out.flush()
    hout = H()
    buf = b""
    off = 0
    with bz2.open(DUMP, "rb") as f:
        done = False
        while not done:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            if off > (1 << 24):
                buf = buf[off:]
                off = 0
            buf += chunk
            while True:
                pe = buf.find(b"</page>", off)
                if pe < 0:
                    break
                n_pages += 1
                ps = buf.rfind(b"<page>", off, pe)
                if ps < 0:
                    off = pe + 7
                    continue
                page = buf[ps:pe + 7]
                off = pe + 7
                if n_pages > npages:
                    done = True
                    break
                # exact same fast filters as wikt.py
                if b"<ns>0</ns>" not in page:
                    continue
                if b"<redirect" in page:
                    continue
                ts = page.find(b"<title>")
                te = page.find(b"</title>", ts)
                if ts < 0 or te < 0:
                    continue
                title = page[ts + 7:te]
                if b":" in title:
                    continue
                xs = page.find(b"<text")
                if xs < 0:
                    continue
                xs = page.find(b">", xs) + 1
                xe = page.find(b"</text>", xs)
                if xe < 0:
                    continue
                text_b = page[xs:xe]
                if b"==English==" not in text_b:
                    continue
                try:
                    title_s = title.decode("utf-8")
                    text_s = text_b.decode("utf-8", errors="replace")
                except Exception:
                    continue
                parse_page_text(title_s, text_s, hout, stats)
    out.close()
    print(f"pages={n_pages} kind1={stats[1]} kind2={stats[2]} sha256={h.hexdigest()}")
    return h.hexdigest()

if __name__ == "__main__":
    npages = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    outp = sys.argv[2] if len(sys.argv) > 2 else "/tmp/wikt_det.bin"
    extract_n(npages, outp)
