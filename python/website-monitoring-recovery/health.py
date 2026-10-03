"""Bounded HTTP checks, also copied to the application server for diagnosis."""
import argparse
import http.client
import socket
import urllib.error
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def check(url, expected_status=200, expected_text="", timeout=10):
    # A redirect or login page must not silently count as the configured endpoint.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    request = urllib.request.Request(url, headers={"User-Agent": "WebsiteMonitor/1.0"})
    try:
        try:
            response = opener.open(request, timeout=timeout)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            status = response.code
            body = response.read(1024 * 1024).decode("utf-8", errors="replace") if expected_text else ""
        if status != expected_status:
            return False, f"HTTP {status}; expected {expected_status}"
        if expected_text and expected_text not in body:
            return False, "Expected text missing from first 1 MiB of response"
        return True, f"HTTP {status}; response valid"
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError, http.client.HTTPException) as exc:
        return False, f"HTTP request failed ({type(exc).__name__})"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--status", type=int, default=200)
    parser.add_argument("--text", default="")
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args()
    healthy, detail = check(args.url, args.status, args.text, args.timeout)
    print(detail)
    raise SystemExit(0 if healthy else 1)
