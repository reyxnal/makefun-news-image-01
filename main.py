#!/usr/bin/env python3
"""
make.fun "news-image-01" entry -- World News, 13 November 2026.

The entry is one editorial image summing up the world's news of Friday
13 November 2026: tankers hit by mines in the Strait of Hormuz, Europe
winning a seat at the Ukraine peace talks, and Nvidia's chief executive
resigning as shares tumble. The program copies the image this repository
holds (entry.png, JPEG bytes, 1024x1024, 182898 bytes) to /output/entry.png.

Pure Python 3 standard library (hashlib / os only): no network, no
randomness, no input files beyond the bundled image -- deterministic:
two runs write byte-identical output.
"""
import hashlib
import os

MAX_BYTES = 1048576  # 1 MiB cap from the competition rules


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out = os.environ.get("ENTRY_OUT") or (
        os.path.join(os.environ["MAKEFUN_OUTPUT_DIR"], "entry.png")
        if os.environ.get("MAKEFUN_OUTPUT_DIR")
        else "/output/entry.png"
    )
    d = os.path.dirname(out)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry image too large: {len(data)} bytes > {MAX_BYTES}")
    # The file is a PNG or a JPEG, told apart by its first bytes; the name
    # stays entry.png either way. Refuse anything that is neither, so a
    # corrupted bundle can never silently enter as the wrong format.
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        kind = "PNG"
    elif data[:3] == b"\xff\xd8\xff":
        kind = "JPEG"
    else:
        raise SystemExit("entry image is neither PNG nor JPEG (bad magic bytes)")
    print(f"entry image format: {kind}")
    with open(out, "wb") as f:
        f.write(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {out} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
