"""Generate cryptographically strong placeholder values for every CHANGE_ME_*.

Usage:
    python scripts/generate_secrets.py            # dry-run, print values
    python scripts/generate_secrets.py --write    # overwrite .env in place
    python scripts/generate_secrets.py --stdout   # print values to stdout
"""

from __future__ import annotations

import argparse
import re
import secrets
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = _PROJECT_ROOT / ".env"

_PLACEHOLDER_RE = re.compile(r"CHANGE_ME(?:_[A-Z0-9_]+)*")


def _gen(token: str) -> str:
    """Generate a strong value appropriate to the placeholder name."""
    up = token.upper()
    if "PASSWORD" in up or "SECRET" in up or "TOKEN" in up or "KEY" in up:
        return secrets.token_urlsafe(48)
    if "URL" in up:
        return "https://example.invalid"
    return secrets.token_hex(16)


def generate(content: str) -> str:
    def repl(match: re.Match) -> str:
        return _gen(match.group(0))

    return _PLACEHOLDER_RE.sub(repl, content)


def main() -> int:
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group()
    g.add_argument("--write", action="store_true", help="Overwrite .env in place")
    g.add_argument("--stdout", action="store_true", help="Print generated .env to stdout")
    args = p.parse_args()

    if not ENV_PATH.exists():
        print(f"ERROR: {ENV_PATH} not found", file=sys.stderr)
        return 1

    original = ENV_PATH.read_text()
    filled = generate(original)

    if args.write:
        ENV_PATH.write_text(filled)
        print(f"Wrote {ENV_PATH} with generated placeholders.")
    else:
        sys.stdout.write(filled)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())