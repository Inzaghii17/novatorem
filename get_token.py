#!/usr/bin/env python3
"""
Quick script to get Spotify refresh token.
Starts a local server, opens the auth page, catches the callback,
and exchanges the code for a refresh token.
"""

import http.server
import urllib.parse
import webbrowser
import requests
import threading
import sys

CLIENT_ID = "d4733a5c907845369f5444f6f6f84355"
CLIENT_SECRET = "20ab4cabfdd04a35933e156af8bc1a37"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = "user-read-currently-playing user-read-recently-played"

auth_code = None

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
            <html><body style="background:#0d1117;color:#c9d1d9;font-family:monospace;
            display:flex;justify-content:center;align-items:center;height:100vh;margin:0;">
            <div style="text-align:center">
            <h1 style="color:#00d4ff">Authorization Successful</h1>
            <p>You can close this tab and go back to the terminal.</p>
            </div></body></html>
            """)
        else:
            error = params.get("error", ["unknown"])[0]
            self.send_response(400)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(f"<html><body>Error: {error}</body></html>".encode())

    def log_message(self, format, *args):
        pass  # Suppress logs


def get_refresh_token(code):
    """Exchange authorization code for refresh token."""
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )
    data = response.json()
    if "refresh_token" in data:
        return data["refresh_token"]
    else:
        print(f"\nError: {data}")
        return None


def main():
    # Start local server
    server = http.server.HTTPServer(("127.0.0.1", 8888), CallbackHandler)
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    # Build auth URL
    auth_url = (
        "https://accounts.spotify.com/authorize?"
        + urllib.parse.urlencode({
            "client_id": CLIENT_ID,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPES,
        })
    )

    print("\n╔══════════════════════════════════════════╗")
    print("║   Spotify Token Generator                ║")
    print("╚══════════════════════════════════════════╝\n")
    print("Opening Spotify authorization page...")
    print(f"If it doesn't open, visit:\n{auth_url}\n")

    webbrowser.open(auth_url)

    # Wait for callback
    thread.join(timeout=300)
    server.server_close()

    if auth_code:
        print("Authorization code received! Exchanging for refresh token...\n")
        refresh_token = get_refresh_token(auth_code)
        if refresh_token:
            print("╔══════════════════════════════════════════╗")
            print("║   SUCCESS — Your Refresh Token:          ║")
            print("╚══════════════════════════════════════════╝\n")
            print(f"  {refresh_token}\n")
            print("Copy this token and add it to your .env file.")
        else:
            print("Failed to get refresh token.")
            sys.exit(1)
    else:
        print("Timed out waiting for authorization. Try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
