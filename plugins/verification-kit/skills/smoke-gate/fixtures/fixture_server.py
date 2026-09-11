#!/usr/bin/env python3
# FIXTURE. Tiny local HTTP server standing in for a live target, used only to prove
# smoke-gate's generated script offline. Never point this at, or confuse this with, a
# real system.
"""fixture_server.py - the smoke-gate deliberate-failure fixture target.

This machine's live sites are out of scope for this proof and no network target may
be assumed, so smoke-gate's own gate is proven against a tiny local server instead: a
page carrying an identity string, a freshness date, and two routes (`/status`,
`/data`), plus one extra route (`/console-error`) that serves a page containing a
labelled marker string standing in for a browser console error.

Usage:
    fixture_server.py [--port N]      # 0 (default) asks the OS for a free port

Prints "LISTENING <port>" to stdout once bound, then serves until killed (SIGTERM/
SIGINT or the parent process group exiting). Every response body says FIXTURE.

Routes:
    /             identity + freshness page (200)
    /status       200, plain text
    /data         200, plain text
    /console-error 200, page containing the console-error stand-in marker
    (anything else) 404

A real console-error check needs a browser (the Browser tool, or Playwright, per
Anthropic's webapp-testing skill) to read the DevTools console. This server cannot
produce that signal; /console-error only serves a labelled text marker as a stand-in
so the "console" assertion category can be poisoned and proven offline, per the
harness's fixture gate.
"""
import argparse
import http.server
import sys

IDENTITY = "Graham (commissioner)"
FRESH_DATE = "2026-09-10"
CONSOLE_MARKER = "FIXTURE simulated console error: TypeError undefined is not a function"

PAGE = f"""<html><body>
<p>FIXTURE smoke-gate target. Not a real system.</p>
<p>Identity: {IDENTITY}</p>
<p>Rosters updated: {FRESH_DATE}</p>
<p><a href="/status">status</a> <a href="/data">data</a></p>
</body></html>
"""

CONSOLE_ERROR_PAGE = f"""<html><body>
<p>FIXTURE smoke-gate target, console-error stand-in variant.</p>
<p>Identity: {IDENTITY}</p>
<p>Rosters updated: {FRESH_DATE}</p>
<p>{CONSOLE_MARKER}</p>
</body></html>
"""


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, body):
        b = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE)
        elif self.path == "/status":
            self._send(200, "FIXTURE status: ok")
        elif self.path == "/data":
            self._send(200, "FIXTURE data: ok")
        elif self.path == "/console-error":
            self._send(200, CONSOLE_ERROR_PAGE)
        else:
            self._send(404, "FIXTURE 404: no such route")

    def log_message(self, fmt, *args):
        pass  # keep the runner's captured output readable


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=0)
    args = ap.parse_args()
    server = http.server.HTTPServer(("127.0.0.1", args.port), Handler)
    print(f"LISTENING {server.server_address[1]}", flush=True)
    sys.stdout.flush()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
