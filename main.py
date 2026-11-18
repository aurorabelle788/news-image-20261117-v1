#!/usr/bin/env python3
"""news-image-20261117 v1 entrypoint.

Writes the front-page image to the output directory. The image itself
(entry.png, a JPEG) lives in this repo; this program only copies it,
after checking it really is a JPEG. No network, no randomness:
two runs produce byte-identical output.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
JPEG_SOI = b"\xff\xd8"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    with open(SOURCE, "rb") as fh:
        head = fh.read(2)
    if head != JPEG_SOI:
        print("error: entry.png is not a JPEG (bad SOI marker)",
              file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    # Post-copy check: the copy must be a JPEG of the same size.
    if (os.path.getsize(target) != os.path.getsize(SOURCE)
            or open(target, "rb").read(2) != JPEG_SOI):
        print("error: copied file failed verification", file=sys.stderr)
        return 1
    print("wrote", target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
