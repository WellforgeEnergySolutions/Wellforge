# -*- coding: utf-8 -*-
"""
Local preview server for the Wellforge site.

Run:  python tools/serve.py            (then open http://localhost:8123)
      python tools/serve.py 9000       (to use a different port)

Why this exists rather than `python -m http.server`
---------------------------------------------------
The stock server sends no Cache-Control header at all. Browsers then fall back
to *heuristic* caching: they guess a freshness lifetime from Last-Modified and
serve the stored copy without asking the server whether it changed. On a site
you are actively editing that means a rebuild appears to have done nothing.

So: HTML is served must-revalidate, and hashed assets (anything carrying a
?v= stamp) are served cacheable, because their URL changes whenever the bytes
change. That gives fast repeat loads without ever showing a stale page.
"""

import os
import sys
from functools import partial

try:
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
except ImportError:                                  # Python 3.6 and earlier
    from http.server import SimpleHTTPRequestHandler
    from socketserver import ThreadingTCPServer as ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        path = self.path.split("?")[0]
        if path.endswith((".html", "/", ".xml", ".txt")) or "." not in path.rsplit("/", 1)[-1]:
            # Documents: always check with the server before reusing.
            self.send_header("Cache-Control", "no-cache, must-revalidate")
        elif "?v=" in self.path:
            # Content-hashed asset: the URL changes when the file does.
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        else:
            self.send_header("Cache-Control", "no-cache")
        SimpleHTTPRequestHandler.end_headers(self)

    def log_message(self, fmt, *args):
        # Keep the console quiet apart from problems.
        status = args[1] if len(args) > 1 else ""
        if str(status).startswith(("4", "5")):
            sys.stderr.write("  %s %s\n" % (status, args[0]))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8123
    handler = partial(Handler, directory=ROOT)
    server = ThreadingHTTPServer(("", port), handler)
    print("Wellforge preview: http://localhost:%d" % port)
    print("Serving %s  (HTML revalidated on every request)" % ROOT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
