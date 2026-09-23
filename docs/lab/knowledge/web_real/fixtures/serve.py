#!/usr/bin/env python3
"""serve.py — minimal deterministic fixture server (test-only glue).
Serves a directory over HTTP on 127.0.0.1:<port>. No redirects, no directory
listing, no CGI. Maps /name.html -> <root>/name.html only.
Usage: serve.py <port> <root>
"""
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = sys.argv[2]
PORT = int(sys.argv[1])


class H(BaseHTTPRequestHandler):
    server_version = "FixtureSrv/1"
    protocol_version = "HTTP/1.0"

    def log_message(self, *a):
        pass

    def _serve(self, is_head):
        p = self.path.split("?", 1)[0]
        if not p.startswith("/") or ".." in p or p != "/" + p.lstrip("/"):
            self.send_error(400)
            return
        name = p.lstrip("/")
        if "/" in name or not name.endswith(".html") or not name.replace("_", "").replace(".", "").replace("-", "").isalnum():
            self.send_error(404)
            return
        try:
            with open(ROOT + "/" + name, "rb") as f:
                body = f.read()
        except OSError:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if not is_head:
            self.wfile.write(body)

    def do_GET(self):
        self._serve(False)

    def do_HEAD(self):
        self._serve(True)


HTTPServer(("127.0.0.1", PORT), H).serve_forever()
