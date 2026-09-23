#!/usr/bin/env python3
"""probe_backends.py — LIVE TRANSPORT PROBE for TNN web-search sense v2 (2026-09-21).

Probes candidate search backends from this VM with 10 factual test queries.
No API keys anywhere. Output: probe_results.json in the same directory.
"""
import json, re, time, urllib.parse, urllib.request, html as ihtml, os

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe_results.json")

QUERIES = [
    "capital of France",
    "boiling point of water at sea level",
    "tallest building in the world 2026",
    "who wrote Pride and Prejudice",
    "chemical symbol for gold",
    "when was the Eiffel Tower built",
    "largest planet in the solar system",
    "speed of light in vacuum",
    "author of the novel 1984",
    "first person to walk on the moon",
]

TAG_RE = re.compile(r"<[^>]+>")

def clean(s):
    return ihtml.unescape(TAG_RE.sub("", s)).strip()

def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read()
    return body, time.time() - t0, resp.status

# ---------------- parsers ----------------

def parse_searxng_json(body):
    data = json.loads(body.decode("utf-8", "replace"))
    results = data.get("results") or []
    out = []
    for r in results:
        t, u, c = (r.get("title") or "").strip(), (r.get("url") or "").strip(), (r.get("content") or "").strip()
        if t and u:
            out.append({"title": t, "url": u, "snippet": c})
    return out

def parse_ddg_html(body):
    page = body.decode("utf-8", "replace")
    anchors = re.findall(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', page, re.S)
    snippets = re.findall(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', page, re.S)
    out = []
    for i, (href, th) in enumerate(anchors):
        m = re.search(r"uddg=([^&]+)", href)
        target = urllib.parse.unquote(m.group(1)) if m else ihtml.unescape(href)
        out.append({"title": clean(th), "url": target,
                    "snippet": clean(snippets[i]) if i < len(snippets) else ""})
    return [r for r in out if r["title"] and r["url"]]

def parse_ddg_lite(body):
    page = body.decode("utf-8", "replace")
    # Sequential: each result is <a class='result-link'> then <td class='result-snippet'>
    items = re.findall(
        r"<a[^>]*?href=\"([^\"]+)\"[^>]*?class='result-link'[^>]*>(.*?)</a>.*?<td class='result-snippet'>(.*?)</td>",
        page, re.S)
    out = []
    for href, title_html, snippet_html in items:
        href = ihtml.unescape(href)
        m = re.search(r"uddg=([^&]+)", href)
        target = urllib.parse.unquote(m.group(1)) if m else href
        if target.startswith("//"):
            target = "https:" + target
        if not target.startswith("http"):
            continue
        out.append({"title": clean(title_html), "url": target,
                    "snippet": clean(snippet_html)})
    return [r for r in out if r["title"] and r["url"]]

def parse_mojeek(body):
    page = body.decode("utf-8", "replace")
    links = re.findall(r'<a[^>]*class="ob[0-9]*"[^>]*href="(/search\?[^"]*)"[^>]*>(.*?)</a>', page, re.S)
    out = []
    seen = set()
    for href, th in links:
        m = re.search(r"q?=?([^&]*)", href)  # fallback; mojeek uses redirect links
        title = clean(th)
        if title:
            out.append({"title": title, "url": "https://www.mojeek.com" + ihtml.unescape(href), "snippet": ""})
    # Mojeek ob links are outbound redirects; try extracting actual url
    for r in out:
        m = re.search(r"url=([^&]+)", r["url"])
        if m:
            r["url"] = urllib.parse.unquote(m.group(1))
    return [r for r in out if r["title"]]

def parse_marginalia(body):
    page = body.decode("utf-8", "replace")
    items = re.findall(r'<div class="result"[^>]*>(.*?)</div>\s*</div>', page, re.S)
    out = []
    for it in items:
        m = re.search(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', it, re.S)
        if not m:
            continue
        title = clean(m.group(2)); url = ihtml.unescape(m.group(1))
        sm = re.search(r'<p class="description"[^>]*>(.*?)</p>', it, re.S)
        out.append({"title": title, "url": url, "snippet": clean(sm.group(1)) if sm else ""})
    return [r for r in out if r["title"] and r["url"]]

def parse_wikipedia(body):
    data = json.loads(body.decode("utf-8", "replace"))
    items = data.get("query", {}).get("search", [])
    out = []
    for it in items:
        out.append({"title": it.get("title", ""),
                    "url": "https://en.wikipedia.org/?curid=" + str(it.get("pageid", "")),
                    "snippet": clean(it.get("snippet", ""))})
    return out

# ---------------- endpoints ----------------

SEARXNG_INSTANCES = [
    "https://searx.be",
    "https://search.inetol.net",
    "https://searx.tiekoetter.com",
    "https://search.sapti.me",
    "https://baresearch.org",
    "https://search.rhscz.eu",
    "https://searxng.website",
    "https://searx.oakleycord.dev",
    "https://search.bus-hit.me",
    "https://search.leptons.xyz",
]

def build_endpoints():
    eps = []
    for base in SEARXNG_INSTANCES:
        eps.append({
            "name": "searxng:" + urllib.parse.urlparse(base).netloc,
            "url_for": lambda q, b=base: b + "/search?q=" + urllib.parse.quote(q) + "&format=json&language=en-US",
            "parser": parse_searxng_json, "kind": "json",
        })
    eps.append({
        "name": "ddg_html", "kind": "html",
        "url_for": lambda q: "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q),
        "parser": parse_ddg_html,
    })
    eps.append({
        "name": "ddg_lite", "kind": "html",
        "url_for": lambda q: "https://lite.duckduckgo.com/lite/?q=" + urllib.parse.quote(q),
        "parser": parse_ddg_lite,
    })
    eps.append({
        "name": "mojeek", "kind": "html",
        "url_for": lambda q: "https://www.mojeek.com/search?q=" + urllib.parse.quote(q),
        "parser": parse_mojeek,
    })
    eps.append({
        "name": "marginalia", "kind": "html",
        "url_for": lambda q: "https://search.marginalia.nu/search?query=" + urllib.parse.quote(q),
        "parser": parse_marginalia,
    })
    eps.append({
        "name": "startpage", "kind": "html",
        "url_for": lambda q: "https://www.startpage.com/sp/search?query=" + urllib.parse.quote(q),
        "parser": lambda b: [],  # count only; check body size
    })
    eps.append({
        "name": "wikipedia_api", "kind": "json",
        "url_for": lambda q: ("https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch="
                              + urllib.parse.quote(q) + "&format=json&srlimit=20"),
        "parser": parse_wikipedia,
    })
    return eps

def probe(ep, queries):
    rep = {"name": ep["name"], "queries": [], "note": ""}
    for q in queries:
        url = ep["url_for"](q)
        qr = {"query": q, "url": url}
        try:
            body, lat, status = fetch(url)
            qr["latency_s"] = round(lat, 2)
            qr["http_status"] = status
            qr["body_bytes"] = len(body)
            try:
                results = ep["parser"](body)
            except Exception as e:
                results = []
                qr["parse_error"] = str(e)
            qr["n_results"] = len(results)
            usable = [r for r in results if r.get("title") and r.get("url")]
            qr["n_usable"] = len(usable)
            qr["usable"] = len(usable) >= 3
            qr["sample"] = usable[:2]
        except Exception as e:
            qr["transport_error"] = str(e)
            qr["usable"] = False
            qr["n_usable"] = 0
        rep["queries"].append(qr)
        time.sleep(0.5)
    rep["pass_count"] = sum(1 for q in rep["queries"] if q.get("usable"))
    rep["works"] = rep["pass_count"] >= 8
    return rep

def main():
    all_eps = build_endpoints()
    results = []
    for ep in all_eps:
        print("probing", ep["name"], flush=True)
        results.append(probe(ep, QUERIES))
    with open(OUT, "w") as f:
        json.dump({"probed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "n_queries": len(QUERIES), "queries": QUERIES,
                   "endpoints": results}, f, indent=1)
    print("wrote", OUT)
    for r in results:
        print(f'{r["name"]:38s} usable_queries={r["pass_count"]}/10 works={r["works"]}')

if __name__ == "__main__":
    main()
