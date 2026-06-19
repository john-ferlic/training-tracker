#!/usr/bin/env python3
"""One-time Strava authorization.

Prerequisite: create an API app at https://www.strava.com/settings/api and put
the Client ID + Client Secret in .env. Set the app's "Authorization Callback
Domain" to:  localhost

Then run:   python scripts/auth_strava.py

It opens your browser, you click Authorize, and this script captures the code,
exchanges it for tokens, and writes STRAVA_REFRESH_TOKEN into your .env.
"""
from __future__ import annotations

import pathlib
import sys
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from trainingtracker import config  # noqa: E402

PORT = 8721
REDIRECT_URI = f"http://localhost:{PORT}/"
SCOPE = "activity:read_all"
_captured: dict[str, str] = {}


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        qs = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(qs)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        if "code" in params:
            _captured["code"] = params["code"][0]
            self.wfile.write(b"<h2>Authorized. You can close this tab and return to the terminal.</h2>")
        else:
            self.wfile.write(b"<h2>No code received. Check the terminal.</h2>")

    def log_message(self, *_args):  # silence default logging
        pass


def _write_refresh_token(token: str) -> None:
    env_path = config.ENV_PATH
    lines = env_path.read_text().splitlines() if env_path.exists() else []
    out, found = [], False
    for line in lines:
        if line.startswith("STRAVA_REFRESH_TOKEN="):
            out.append(f"STRAVA_REFRESH_TOKEN={token}")
            found = True
        else:
            out.append(line)
    if not found:
        out.append(f"STRAVA_REFRESH_TOKEN={token}")
    env_path.write_text("\n".join(out) + "\n")


def main() -> int:
    client_id = config.get_env("STRAVA_CLIENT_ID")
    client_secret = config.get_env("STRAVA_CLIENT_SECRET")
    if not client_id or not client_secret:
        print("Put STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET in .env first "
              "(copy .env.example to .env). See https://www.strava.com/settings/api")
        return 1

    auth_url = "https://www.strava.com/oauth/authorize?" + urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "approval_prompt": "force",
    })
    print("Opening your browser to authorize Strava access...")
    print("If it doesn't open, paste this URL:\n  " + auth_url + "\n")
    webbrowser.open(auth_url)

    server = HTTPServer(("localhost", PORT), _Handler)
    print(f"Waiting for the redirect on {REDIRECT_URI} ...")
    while "code" not in _captured:
        server.handle_request()

    print("Exchanging authorization code for tokens...")
    resp = requests.post("https://www.strava.com/oauth/token", data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": _captured["code"],
        "grant_type": "authorization_code",
    }, timeout=30)
    if resp.status_code != 200:
        print(f"Token exchange failed ({resp.status_code}): {resp.text[:300]}")
        return 1

    data = resp.json()
    refresh_token = data["refresh_token"]
    _write_refresh_token(refresh_token)
    athlete = data.get("athlete", {})
    name = f"{athlete.get('firstname', '')} {athlete.get('lastname', '')}".strip()
    print(f"\nAuthorized{' as ' + name if name else ''}. "
          f"STRAVA_REFRESH_TOKEN written to .env.")
    print("Granted scopes:", data.get("scope", SCOPE))
    print("\nNext: python -m trainingtracker setup-check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
