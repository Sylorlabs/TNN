#!/usr/bin/env python3
"""Parallel wiktionary extraction worker (decompressed-XML version).

Reads a plain (decompressed) XML dump, replicates extract/wikt.py's page
loop EXACTLY for pages [start_page, end_page] (1-based, inclusive), writes
records to <out.bin>. Same byte filters, same parse_page_text from
wikt_slow. Proven byte-equivalent to the single-pass path (see worker test).

Usage: wikt_worker2.py <xml> <start_page> <end_page|0=EOF> <out.bin>
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wikt_slow import parse_page as parse_page_text

def main():
    xml_path = sys.argv[1]
    start_page = int(sys.argv[2])
    end_page = int(sys.argv[3])  # 0 = to EOF
    outp = sys.argv[4]
    feeder_pid = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    import time
    def feeder_alive():
        if not feeder_pid:
            return False
        try:
            os.kill(feeder_pid, 0)
            return True
        except OSError:
            return False
    stats = {1: 0, 2: 0}
    n_pages = 0
    out = open(outp, "wb")
    buf = b""
    off = 0
    done = False
    with open(xml_path, "rb") as f:
        while not done:
            chunk = f.read(1 << 20)
            if not chunk:
                # EOF: if feeder still running, wait for more data; else real EOF
                if feeder_alive():
                    time.sleep(30)
                    continue
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
                        print(f"  worker2 skip ... {n_pages}", flush=True)
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
                    print(f"  worker2 ... {n_pages} pages, senses={stats[1]}, infl={stats[2]}",
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
    print(f"worker2 done: pages {start_page}..{n_pages}, "
          f"kind1={stats[1]}, kind2={stats[2]}", flush=True)

if __name__ == "__main__":
    main()
