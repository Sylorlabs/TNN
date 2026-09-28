#!/usr/bin/env python3
"""Extract en.wiktionary English entries -> kind-1 (senses) and kind-2 (inflections).
Fast bytes-based streaming scanner (no per-line UTF-8 decode of the full dump).
Writes run/wikt.bin records: [1B kind][2B key_len BE][4B text_len BE][key][text].
Deterministic: dump order.
"""
import bz2, re, struct, os, html, sys

CORPUS = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/corpus")
RUN = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/run")
DUMP = os.path.join(CORPUS, "enwiktionary-latest-pages-articles.xml.bz2")

# (parser functions: expand_templates, clean_def, english_section, parse_page
#  imported from the slow module to avoid duplication)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wikt_slow import parse_page as parse_page_text

def main():
    os.makedirs(RUN, exist_ok=True)
    stats = {1: 0, 2: 0}
    n_pages = 0
    # checkpoint: number of pages already processed (for resume after restart)
    ckpt_path = os.path.join(RUN, "wikt.ckpt")
    skip_pages = 0
    if os.path.exists(ckpt_path):
        with open(ckpt_path) as f:
            skip_pages = int(f.read().strip() or "0")
        print(f"resuming: skipping {skip_pages} pages", flush=True)
    out_path = os.path.join(RUN, "wikt.bin")
    # append mode if resuming, write mode if fresh
    out = open(out_path, "ab" if skip_pages > 0 else "wb")
    buf = b""
    off = 0
    with bz2.open(DUMP, "rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            # append without copying the consumed prefix: compact occasionally
            if off > (1 << 24):
                buf = buf[off:]
                off = 0
            buf += chunk
            # process complete pages
            while True:
                pe = buf.find(b"</page>", off)
                if pe < 0:
                    break
                n_pages += 1
                # fast skip for already-processed pages on resume (no parsing)
                if n_pages <= skip_pages:
                    off = pe + 7
                    continue
                # find start of this page (only for non-skipped)
                ps = buf.rfind(b"<page>", off, pe)
                if ps < 0:
                    # malformed; skip
                    off = pe + 7
                    continue
                page = buf[ps:pe + 7]
                off = pe + 7
                # checkpoint every 50k pages
                if n_pages % 50000 == 0:
                    with open(ckpt_path, "w") as cf:
                        cf.write(str(n_pages))
                    print(f"  ... {n_pages} pages, senses={stats[1]}, infl={stats[2]}", flush=True)
                # fast filters on bytes
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
    # remove checkpoint on successful completion
    if os.path.exists(ckpt_path):
        os.remove(ckpt_path)
    print(f"wiktionary: {n_pages} pages, kind1={stats[1]}, kind2={stats[2]}")

if __name__ == "__main__":
    main()
