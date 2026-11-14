#!/usr/bin/env python3
"""World news of Friday 13 November 2026, in one image.

Three stories share the frame: oil tankers struck by mines in the Strait
of Hormuz, Europe taking a seat at the Ukraine peace talks, and Nvidia's
chief executive resigning while the shares fall. This program ships the
finished picture (entry.png, JPEG bytes, 1024 by 1024) to /output/entry.png
by copying it byte for byte.

Standard library only, no network access, no randomness: running it twice
produces identical output.
"""
import hashlib
import os

ENTRY_FILENAME = "entry.png"
MAX_BYTES = 1048576  # the competition caps the entry image at 1 MiB


def resolve_output_path():
    """Where the entry image goes: ENTRY_OUT wins, then MAKEFUN_OUTPUT_DIR."""
    override = os.environ.get("ENTRY_OUT")
    if override:
        return override
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if output_dir:
        return os.path.join(output_dir, ENTRY_FILENAME)
    return os.path.join("/output", ENTRY_FILENAME)


def read_image_bytes(path):
    """Read the bundled image, enforcing the size cap and the PNG/JPEG gate."""
    with open(path, "rb") as handle:
        data = handle.read()
    if len(data) > MAX_BYTES:
        raise SystemExit(
            f"entry image too large: {len(data)} bytes > {MAX_BYTES} bytes"
        )
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        kind = "PNG"
    elif data[:3] == b"\xff\xd8\xff":
        kind = "JPEG"
    else:
        raise SystemExit("entry image is neither PNG nor JPEG (bad magic bytes)")
    print(f"entry image format: {kind}")
    return data


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    data = read_image_bytes(os.path.join(here, ENTRY_FILENAME))
    out = resolve_output_path()
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "wb") as handle:
        handle.write(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {out} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
