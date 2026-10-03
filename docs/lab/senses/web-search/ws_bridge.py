#!/usr/bin/env python3
"""ws_bridge.py — thin TRANSPORT bridge for the TNN web-search sense.

NOT TNN-side: this does no deciding, no judging, no installing. It performs
one HTTP search, parses results, and emits a provenance envelope as JSON.
All decisions happen in pure Zag (ws_sense.zag).

Envelope fields per result: rank, title, snippet, url, domain (registrable),
result_hash = sha256(url + "\\n" + title + "\\n" + snippet) (canonical v1).
Envelope: query, retrieved_at (wall clock — Python side ONLY; never enters
the Zag ledger, keeping reruns byte-identical), results[].
"""
import hashlib
import html as ihtml
import json
import re
import sys
import time
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
DDG = "https://html.duckduckgo.com/html/?q="

ANCHOR_RE = re.compile(
    r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.S)
SNIPPET_RE = re.compile(
    r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', re.S)
TAG_RE = re.compile(r"<[^>]+>")


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


def unwrap_ddg(href):
    # href looks like //duckduckgo.com/l/?uddg=<urlencoded>&rut=...
    m = re.search(r"uddg=([^&]+)", href)
    if m:
        return urllib.parse.unquote(m.group(1))
    return href


def search(query, max_results=6):
    url = DDG + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            page = resp.read().decode("utf-8", "replace")
    except Exception as e:
        return {"query": query, "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "transport_error": str(e), "results": []}
    anchors = ANCHOR_RE.findall(page)
    snippets = SNIPPET_RE.findall(page)
    out = []
    for i, (href, title_html) in enumerate(anchors[:max_results]):
        target = unwrap_ddg(ihtml.unescape(href))
        title = clean(title_html)
        snippet = clean(snippets[i]) if i < len(snippets) else ""
        body = (target + "\n" + title + "\n" + snippet).encode("utf-8")
        out.append({
            "rank": i,
            "title": title,
            "snippet": snippet,
            "url": target,
            "domain": registrable_domain(target),
            "body_sha256": hashlib.sha256(body).hexdigest(),
        })
    return {"query": query,
            "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "results": out}


def main():
    if len(sys.argv) < 2:
        print("usage: ws_bridge.py QUERY [max_results]", file=sys.stderr)
        sys.exit(2)
    q = sys.argv[1]
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    print(json.dumps(search(q, mx), indent=1))


if __name__ == "__main__":
    main()
