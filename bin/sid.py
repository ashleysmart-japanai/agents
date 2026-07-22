#!/usr/bin/env python3
"""sid.py — issue-ID SID encoder: UUIDv4 compressed to fixed-width 22-char base62.

The SID format is specified in ~/agents/review/REVIEW_METHOD.md § ID format.
Alphabet 0-9A-Za-z, most-significant digit first, zero-padded to width 22.

Usage:
  sid.py            generate a new SID (fresh UUIDv4)
  sid.py <uuid>     encode an existing UUID
"""

import sys
import uuid

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
WIDTH = 22


def encode(u: uuid.UUID) -> str:
    n = u.int
    return "".join(ALPHABET[(n // 62**i) % 62] for i in range(WIDTH - 1, -1, -1))


def main(argv):
    try:
        if len(argv) == 0:
            print(encode(uuid.uuid4()))
        elif len(argv) == 1 and argv[0] not in ("-h", "--help"):
            print(encode(uuid.UUID(argv[0])))
        else:
            print(__doc__.strip(), file=sys.stderr)
            return 2
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
