#!/usr/bin/env python3
"""Extract en.wiktionary English entries -> kind-1 (senses) and kind-2 (inflections).
Streams enwiktionary pages-articles bz2. For each ns=0 page:
  - take the ==English== section
  - per POS subsection (===Noun=== etc.), take sense lines starting with '# '
    (not '#*', '#:', which are examples/quotes)
  - if the sense's first template is a form-of/inflection template -> kind 2
    key = wikt:en:{base}:{infltype}:{form}:{n:02d}, text names the base
  - else -> kind 1
    key = wikt:en:{word}:{pos}:{sensenum:03d}, text = definition
Writes run/wikt.bin records: [1B kind][2B key_len BE][4B text_len BE][key][text].
Deterministic: dump order.
"""
import bz2, re, struct, os, html

CORPUS = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/corpus")
RUN = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/run")

def find_dump():
    for n in ("enwiktionary-latest-pages-articles.xml.bz2",):
        p = os.path.join(CORPUS, n)
        if os.path.exists(p):
            return p
    raise SystemExit("enwiktionary dump not found")

# form-of templates: name -> (infltype label, base-arg-index)
FORM_OF = {
    "plural of": "plural",
    "singular of": "singular",
    "past of": "past",
    "past participle of": "past-participle",
    "past-participle of": "past-participle",
    "present participle of": "present-participle",
    "present-participle of": "present-participle",
    "third-person singular of": "3rd-singular",
    "third person singular of": "3rd-singular",
    "comparative of": "comparative",
    "superlative of": "superlative",
    "alternative form of": "alt-form",
    "alternative spelling of": "alt-spelling",
    "inflection of": "inflection",
    "feminine of": "feminine",
    "masculine of": "masculine",
}

def strip_nested(s, op, cl):
    out, i, depth, n = [], 0, 0, len(s)
    while i < n:
        if s.startswith(op, i):
            depth += 1; i += len(op)
        elif s.startswith(cl, i) and depth:
            depth -= 1; i += len(cl)
        elif depth == 0:
            out.append(s[i]); i += 1
        else:
            i += 1
    return "".join(out)

def link_repl(m):
    inner = m.group(1)
    if "|" in inner:
        return inner.rsplit("|", 1)[1]
    return inner

def expand_templates(s):
    """Parse {{...}} with nesting. Link-like templates (l/m/link/ll) yield
    their display text; all other templates are dropped."""
    out = []
    i, n = 0, len(s)
    while i < n:
        if s.startswith("{{", i):
            # find matching }} with depth counting
            depth = 1
            j = i + 2
            while j < n and depth > 0:
                if s.startswith("{{", j):
                    depth += 1; j += 2
                elif s.startswith("}}", j):
                    depth -= 1; j += 2
                else:
                    j += 1
            inner = s[i+2:j-2] if depth == 0 else s[i+2:]
            # split top-level args (respect nested {{}})
            args, cur, d2, k = [], [], 0, 0
            while k < len(inner):
                if inner.startswith("{{", k):
                    d2 += 1; cur.append("{{"); k += 2
                elif inner.startswith("}}", k):
                    d2 -= 1; cur.append("}}"); k += 2
                elif inner[k] == "|" and d2 == 0:
                    args.append("".join(cur)); cur = []; k += 1
                else:
                    cur.append(inner[k]); k += 1
            args.append("".join(cur))
            tname = args[0].strip().lower() if args else ""
            if tname in ("l", "m", "link", "ll"):
                # display = last positional arg (skip named args with =)
                disp = None
                for a in args[1:]:
                    a = a.strip()
                    if not a or "=" in a:
                        continue
                    if a in ("en",):
                        continue
                    disp = a
                if disp:
                    out.append(expand_templates(disp))
            # else: drop the template
            i = j if depth == 0 else n
        else:
            out.append(s[i])
            i += 1
    return "".join(out)

def clean_def(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = expand_templates(s)
    for _ in range(3):
        ns2 = re.sub(r"\[\[([^\[\]]+)\]\]", link_repl, s)
        if ns2 == s:
            break
        s = ns2
    s = s.replace("'''", "").replace("''", "")
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def english_section(text):
    m = re.search(r"^==English==\s*$", text, re.M)
    if not m:
        return None
    start = m.end()
    m2 = re.search(r"^==[^=]+==\s*$", text[start:], re.M)
    end = start + m2.start() if m2 else len(text)
    return text[start:end]

POS_RE = re.compile(r"^===\s*([A-Za-z ]+?)\s*===\s*$", re.M)
POS_KEEP = {"noun", "verb", "adjective", "adverb", "pronoun", "preposition",
            "conjunction", "interjection", "determiner", "article", "numeral",
            "proper noun", "phrase", "proverb", "particle"}

def parse_page(title, text, out, stats):
    sec = english_section(text)
    if not sec:
        return
    # split into POS blocks
    blocks = []
    cur_pos, cur_start = None, 0
    for m in POS_RE.finditer(sec):
        if cur_pos is not None:
            blocks.append((cur_pos, sec[cur_start:m.start()]))
        cur_pos = m.group(1).strip().lower()
        cur_start = m.end()
    if cur_pos is not None:
        blocks.append((cur_pos, sec[cur_start:]))
    word = title.strip()
    if not word or len(word.encode("utf-8")) > 100:
        return
    for pos, body in blocks:
        if pos not in POS_KEEP:
            continue
        sensenum = 0
        for line in body.split("\n"):
            # sense lines: '# ' top-level or '## ' subsenses; skip '#*'/ '#:' examples
            m = re.match(r"^#{1,2} ", line)
            if not m:
                continue
            raw = line[m.end():].strip()
            if not raw:
                continue
            # form-of detection: first template
            tm = re.match(r"\{\{\s*([^}|]+)\|", raw)
            infl = None
            base = None
            if tm:
                tname = tm.group(1).strip().lower()
                if tname in FORM_OF:
                    args = raw[2:].split("}}")[0].split("|")
                    # args[0]=template name, args[1]=lang, args[2]=base
                    if len(args) >= 3:
                        base = args[2].strip()
                        infl = FORM_OF[tname]
            if infl and base:
                sensenum += 1
                label = infl
                text_out = f"{label} of {base}"
                # add inflection detail if present (e.g. inflection of|en|run|past)
                key = f"wikt:en:{base}:{label}:{word}:{sensenum:02d}"
                kind = 2
            else:
                d = clean_def(raw)
                if not d:
                    continue
                sensenum += 1
                key = f"wikt:en:{word}:{pos}:{sensenum:03d}"
                text_out = d
                kind = 1
            kb = key.encode("utf-8")
            tb = text_out.encode("utf-8")
            if len(kb) > 160 or len(tb) < 1 or len(tb) > 4096:
                continue
            if b"\x00" in kb or b"\x00" in tb:
                continue
            # G3 pre-check (mirror the gate): dict text != word; infl text names base.
            # The gate additionally requires kind-1 text len>=4 and a non-empty
            # word segment in the key (ig_key_word wl>=1); enforce both here so
            # no emitted record can ever trip the CAL must-accept dry-run.
            if kind == 1 and tb.decode("utf-8", "replace") == word:
                continue
            if kind == 1 and len(tb) < 4:
                continue
            if kind == 2 and base not in text_out:
                continue
            if kind == 2:
                # key = wikt:en:{base}:{label}:{word}:{nn}; gate needs the
                # segment after "wikt:en:" non-empty (ig_key_word wl>=1)
                ci = key.find(":", 8)
                if ci < 0 or ci == 8:
                    continue
            out.write(bytes([kind]) + struct.pack(">H", len(kb)) + struct.pack(">I", len(tb)) + kb + tb)
            stats[kind] += 1

def main():
    dump = find_dump()
    os.makedirs(RUN, exist_ok=True)
    stats = {1: 0, 2: 0}
    n_pages = 0
    with bz2.open(dump, "rt", encoding="utf-8", errors="replace") as f, \
         open(os.path.join(RUN, "wikt.bin"), "wb") as out:
        buf, inpage = [], False
        for line in f:
            if "<page>" in line:
                inpage, buf = True, [line]
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
                parse_page(title, m.group(1), out, stats)
                n_pages += 1
                if n_pages % 200000 == 0:
                    print(f"  ... {n_pages} pages, senses={stats[1]}, infl={stats[2]}", flush=True)
    print(f"wiktionary: {n_pages} pages, kind1={stats[1]}, kind2={stats[2]}")

if __name__ == "__main__":
    main()
