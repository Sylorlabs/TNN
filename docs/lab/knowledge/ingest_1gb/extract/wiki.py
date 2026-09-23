#!/usr/bin/env python3
"""Extract Simple Wikipedia article sentences -> kind-3 fact records.
Streams simplewiki pages-articles bz2, strips wikitext, splits sentences.
Writes run/wiki.bin records: [1B kind][2B key_len BE][4B text_len BE][key][text].
Deterministic: dump order, per-article sentence numbering.
key = wiki:simple:{slug}:sent{n:06d}
"""
import bz2, re, struct, sys, os, html

CORPUS = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/corpus")
RUN = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/run")
DUMP = os.path.join(CORPUS, "simplewiki-latest-pages-articles.xml.bz2")

def strip_nested(s, op, cl):
    out = []
    i, depth = 0, 0
    n = len(s)
    while i < n:
        if s.startswith(op, i):
            depth += 1
            i += len(op)
        elif s.startswith(cl, i) and depth > 0:
            depth -= 1
            i += len(cl)
        elif depth == 0:
            out.append(s[i])
            i += 1
        else:
            i += 1
    return "".join(out)

def link_repl(m):
    inner = m.group(1)
    for ns in ("File:", "Image:", "Category:"):
        if inner.startswith(ns):
            return ""
    if "|" in inner:
        return inner.rsplit("|", 1)[1]
    return inner

def strip_wiki(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S | re.I)
    s = re.sub(r"<ref[^>]*/>", "", s, flags=re.I)
    s = re.sub(r"{\|.*?\|}", "", s, flags=re.S)
    s = strip_nested(s, "{{", "}}")
    # repeat link pass for doubly-nested leftovers
    for _ in range(3):
        ns2 = re.sub(r"\[\[([^\[\]]+)\]\]", link_repl, s)
        if ns2 == s:
            break
        s = ns2
    s = re.sub(r"\[https?://[^\s\]]+\s+([^\]]+)\]", r"\1", s)
    s = re.sub(r"\[https?://[^\]]+\]", "", s)
    s = s.replace("'''", "").replace("''", "")
    s = re.sub(r"^=+\s*(.*?)\s*=+\s*$", "", s, flags=re.M)
    s = re.sub(r"^[*#;:]+\s*", "", s, flags=re.M)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s

SENT_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'\(\[])")

def sentences(text):
    text = text.replace("\n", " ").strip()
    parts = SENT_END.split(text)
    for p in parts:
        p = p.strip()
        if len(p.encode("utf-8")) < 10:
            continue
        if p[-1] not in ".!?":
            continue
        # skip sentences that are mostly markup residue
        if len(re.findall(r"[A-Za-z]", p)) < 5:
            continue
        yield p

def slugify(title):
    s = title.strip().lower().replace(" ", "_")
    s = re.sub(r"[^a-z0-9_\-]", "", s)
    return s[:120] or "untitled"

def main():
    os.makedirs(RUN, exist_ok=True)
    n_art, n_sent = 0, 0
    with bz2.open(DUMP, "rt", encoding="utf-8", errors="replace") as f, \
         open(os.path.join(RUN, "wiki.bin"), "wb") as out:
        buf = []
        inpage = False
        for line in f:
            if "<page>" in line:
                inpage = True
                buf = [line]
                continue
            if not inpage:
                continue
            buf.append(line)
            if "</page>" in line:
                inpage = False
                page = "".join(buf)
                m = re.search(r"<ns>(.*?)</ns>", page)
                if not m or m.group(1) != "0":
                    continue
                if "<redirect" in page:
                    continue
                m = re.search(r"<title>(.*?)</title>", page)
                if not m:
                    continue
                title = m.group(1)
                if ":" in title:
                    continue
                m = re.search(r"<text[^>]*>(.*?)</text>", page, re.S)
                if not m:
                    continue
                body = m.group(1)
                if re.match(r"\s*#REDIRECT", body, re.I):
                    continue
                plain = strip_wiki(body)
                slug = slugify(title)
                si = 0
                for sent in sentences(plain):
                    sb = sent.encode("utf-8")
                    if len(sb) > 4096:
                        continue
                    key = f"wiki:simple:{slug}:sent{si:06d}".encode("ascii")
                    if len(key) > 160:
                        continue
                    out.write(bytes([3]) + struct.pack(">H", len(key)) + struct.pack(">I", len(sb)) + key + sb)
                    si += 1
                    n_sent += 1
                n_art += 1
                if n_art % 20000 == 0:
                    print(f"  ... {n_art} articles, {n_sent} sentences", flush=True)
    print(f"wiki: {n_art} articles, {n_sent} sentences")

if __name__ == "__main__":
    main()
