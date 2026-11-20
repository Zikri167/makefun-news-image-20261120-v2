#!/usr/bin/env python3
"""Copy the bundled news poster to the competition output location.

The poster itself ships in this repository as ``entry.png`` right next
to this file.  Running the program is deliberately boring: locate the
bundled image, make sure the destination folder exists, then copy the
bytes across unchanged so repeated runs always produce the same file.
"""

import os
import shutil
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"


def bundled_image_path() -> Path:
    """Return the path of the poster stored beside this program."""
    return Path(__file__).resolve().parent / IMAGE_NAME


def looks_like_supported_image(path: Path) -> bool:
    """Sniff the opening bytes: accept a PNG signature or a JPEG start."""
    with path.open("rb") as handle:
        head = handle.read(8)
    png_magic = b"\x89PNG\r\n\x1a\n"
    jpeg_magic = b"\xff\xd8\xff"
    return head.startswith(png_magic) or head.startswith(jpeg_magic)


def destination_path() -> Path:
    """Work out where the poster has to land for this run."""
    out_dir = os.environ.get(OUTPUT_ENV_VAR) or DEFAULT_OUTPUT_DIR
    return Path(out_dir) / IMAGE_NAME


def main() -> int:
    source = bundled_image_path()
    if not source.is_file():
        print(f"bundled image missing: {source}", file=sys.stderr)
        return 1
    if not looks_like_supported_image(source):
        print("bundled file is neither PNG nor JPEG", file=sys.stderr)
        return 1

    target = destination_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)

    if target.stat().st_size != source.stat().st_size:
        print("copied image size does not match the bundled file", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
