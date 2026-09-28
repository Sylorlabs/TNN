#!/usr/bin/env python3
"""Parallel wiktionary extraction worker.

Replicates extract/wikt.py's page loop EXACTLY (same byte filters, same
parse_page_text from wikt_slow), but processes only pages
[start_page, end_page] (1-based, inclusive) of the dump and writes records
to <out.bin>. No checkpointing (each worker owns its range; rerun on failure).

Usage: wikt_worker.py <start_page> <end_page|0=EOF> <out.bin>
Page counting matches wikt.py: n_pages increments per </page> in dump order.
Ranges should overlap by ~1000 pages at boundaries; the fixed merge dedupes
by key (keep-first), so overlap is harmless and gaps are impossible.
Deterministic: same input pages -> same records, byte-identical to a
single-pass run over the same page range (proven by verify script).
"""
import bz2, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wikt_slow import parse_page as parse_page_text

CORPUS = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/corpus")
DUMP = os.path.join(CORPUS, "enwiktionary-latest-pages-articles.xml.bz2")

def main():
    start_page = int(sys.argv[1])
    end_page = int(sys.argv[2])  # 0 = to EOF
    outp = sys.argv[3]
    stats = {1: 0, 2: 0}
    n_pages = 0
    out = open(outp, "wb")
    buf = b""
    off = 0
    done = False
    with bz2.open(DUMP, "rb") as f:
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
                if n_pages < start_page:
                    off = pe + 7
                    if n_pages % 500000 == 0:
                        print(f"  worker skip ... {n_pages}", flush=True)
                    continue
                if end_page and n_pages > end_page:
                    done = True
                    break
                ps = buf.rfind(b"<page>", off, pe)
                if ps < 0:
                    off = pe + 7
                    continue
                page = buf[ps:pe + 7]
                off = pe + 7
                if n_pages % 50000 == 0:
                    print(f"  worker ... {n_pages} pages, senses={stats[1]}, infl={stats[2]}",
                          flush=True)
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
                parse_page_text(title_s, text_s, out, stats)
    out.close()
    print(f"worker done: pages {start_page}..{n_pages}, "
          f"kind1={stats[1]}, kind2={stats[2]}", flush=True)

if __name__ == "__main__":
    main()
