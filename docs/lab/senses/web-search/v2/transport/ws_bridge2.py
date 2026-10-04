#!/usr/bin/env python3
"""ws_bridge2.py — thin TRANSPORT-ONLY bridge for the TNN web-search sense v2.

NOT TNN-side: this does no deciding, no judging, no filtering by "quality",
no installing. It performs one HTTP search, parses results, and emits a
provenance envelope as JSON. All decisions happen in pure Zag.

Provenance envelope (canonical v1, same as ws_bridge.py):
  query, retrieved_at (wall clock — Python side ONLY; never enters the Zag
  ledger, keeping reruns byte-identical), backend (transport metadata),
  results[] with rank/title/snippet/url/domain (registrable),
  result_hash = sha256(url + "\\n" + title + "\\n" + snippet) hex.

Backends (no API keys anywhere):
  lumy       SearXNG JSON API at https://search.lumy.live (primary; 10/10 in
             the 2026-09-21 transport probe, latency ~2.5-14s)
  ddg_html   DuckDuckGo HTML https://html.duckduckgo.com/html/?q= (flaky:
             HTTP 202 bot interstitials, ~5-7/10; fallback only)
  ddg_lite   DuckDuckGo Lite https://lite.duckduckgo.com/lite/?q= (flaky:
             ~5/10; fallback only)
  wikipedia  Wikipedia Action API (supplementary only — encyclopedia search,
             NOT general web search; envelope carries supplementary:true)
  auto       fallback chain: lumy -> ddg_html -> ddg_lite -> wikipedia

Usage: ws_bridge2.py QUERY [max_results] [--backend NAME]
"""
import hashlib
import html as ihtml
import json
import re
import sys
import time
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
TAG_RE = re.compile(r"<[^>]+>")

LUMY = "https://search.lumy.live/search?q={q}&format=json&language=en-US"
DDG_HTML = "https://html.duckduckgo.com/html/?q={q}"
DDG_LITE = "https://lite.duckduckgo.com/lite/?q={q}"
WIKI = ("https://en.wikipedia.org/w/api.php?action=query&list=search"
        "&srsearch={q}&format=json&srlimit=40")


def clean(s):
    return ihtml.unescape(TAG_RE.sub("", s)).strip()


def registrable_domain(url):
    try:
        host = urllib.parse.urlparse(url).netloc.lower()
        if host.startswith("www."):
            host = host[4:]
        parts = host.split(".")
        return ".".join(parts[-2:]) if len(parts) >= 2 else host
    except Exception:
        return ""


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read()
        status = resp.status
    return body, status, time.time() - t0


def unwrap_ddg(href):
    m = re.search(r"uddg=([^&]+)", href)
    if m:
        return urllib.parse.unquote(m.group(1))
    return href


# ---------------- backend parsers (transport only) ----------------

def parse_lumy(body):
    data = json.loads(body.decode("utf-8", "replace"))
    out = []
    for r in data.get("results") or []:
        t, u, c = (r.get("title") or "").strip(), (r.get("url") or "").strip(), \
                  (r.get("content") or "").strip()
        if t and u:
            out.append({"title": t, "url": u, "snippet": c})
    return out


def parse_ddg_html(body):
    page = body.decode("utf-8", "replace")
    anchors = re.findall(
        r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', page, re.S)
    snippets = re.findall(
        r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', page, re.S)
    out = []
    for i, (href, title_html) in enumerate(anchors):
        target = unwrap_ddg(ihtml.unescape(href))
        out.append({"title": clean(title_html), "url": target,
                    "snippet": clean(snippets[i]) if i < len(snippets) else ""})
    return [r for r in out if r["title"] and r["url"]]


def parse_ddg_lite(body):
    page = body.decode("utf-8", "replace")
    items = re.findall(
        r"<a[^>]*?href=\"([^\"]+)\"[^>]*?class='result-link'[^>]*>"
        r"(.*?)</a>.*?<td class='result-snippet'>(.*?)</td>", page, re.S)
    out = []
    for href, title_html, snippet_html in items:
        target = unwrap_ddg(ihtml.unescape(href))
        if target.startswith("//"):
            target = "https:" + target
        if not target.startswith("http"):
            continue
        out.append({"title": clean(title_html), "url": target,
                    "snippet": clean(snippet_html)})
    return [r for r in out if r["title"] and r["url"]]


def parse_wikipedia(body):
    data = json.loads(body.decode("utf-8", "replace"))
    out = []
    for it in data.get("query", {}).get("search", []):
        out.append({"title": it.get("title", ""),
                    "url": "https://en.wikipedia.org/?curid=" + str(it.get("pageid", "")),
                    "snippet": clean(it.get("snippet", ""))})
    return [r for r in out if r["title"] and r["url"]]


BACKENDS = {
    "lumy": (LUMY, parse_lumy, False),
    "ddg_html": (DDG_HTML, parse_ddg_html, False),
    "ddg_lite": (DDG_LITE, parse_ddg_lite, False),
    "wikipedia": (WIKI, parse_wikipedia, True),
}
FALLBACK_CHAIN = ["lumy", "ddg_html", "ddg_lite", "wikipedia"]


def search_one(query, backend_name, max_results):
    tmpl, parser, supplementary = BACKENDS[backend_name]
    url = tmpl.format(q=urllib.parse.quote(query))
    body, status, latency = fetch(url)
    if status != 200:
        return None, "http_status=%s" % status, latency
    try:
        raw = parser(body)
    except Exception as e:
        return None, "parse_error=%s" % e, latency
    if not raw:
        return None, "no_results_parsed", latency
    return raw[:max_results], None, latency


def search(query, max_results=6, backend="auto"):
    retrieved_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    chain = FALLBACK_CHAIN if backend == "auto" else [backend]
    errors = {}
    for name in chain:
        raw, err, latency = search_one(query, name, max_results)
        if err:
            errors[name] = err
            continue
        out = []
        for i, r in enumerate(raw):
            body = (r["url"] + "\n" + r["title"] + "\n" + r["snippet"]).encode("utf-8")
            out.append({
                "rank": i,
                "title": r["title"],
                "snippet": r["snippet"],
                "url": r["url"],
                "domain": registrable_domain(r["url"]),
                "result_hash": hashlib.sha256(body).hexdigest(),
            })
        env = {"query": query, "retrieved_at": retrieved_at,
               "backend": name, "latency_s": round(latency, 2),
               "results": out}
        if BACKENDS[name][2]:
            env["supplementary"] = True
        if backend == "auto" and errors:
            env["fallbacks_skipped"] = errors
        return env
    return {"query": query, "retrieved_at": retrieved_at, "backend": "auto",
            "transport_error": "all backends failed", "backend_errors": errors,
            "results": []}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    be = "auto"
    for a in sys.argv[1:]:
        if a.startswith("--backend="):
            be = a.split("=", 1)[1]
        elif a == "--backend":
            pass
    # support "--backend NAME" two-arg form
    for i, a in enumerate(sys.argv[1:], 1):
        if a == "--backend" and i + 1 < len(sys.argv):
            be = sys.argv[i + 1]
    if not args:
        print("usage: ws_bridge2.py QUERY [max_results] [--backend lumy|ddg_html|ddg_lite|wikipedia|auto]",
              file=sys.stderr)
        sys.exit(2)
    if be not in BACKENDS and be != "auto":
        print("unknown backend: %s" % be, file=sys.stderr)
        sys.exit(2)
    q = args[0]
    mx = int(args[1]) if len(args) > 1 else 6
    print(json.dumps(search(q, mx, be), indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
