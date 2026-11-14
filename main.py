"""food-picture-01 entry V1 (Python 3.13, standard library only).

The program copies the image held in this repository (image.jpg, beside
this file) to the output directory as entry.png. The gate accepts a whole
PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees
exactly the bytes copied, so the copy must be byte-for-byte identical.

Before copying, the program validates the source against the gate's own
limits (whole JPEG: SOI marker first, EOI marker last; at most 1 MiB;
at most 1024 by 1024 pixels) and refuses to write anything invalid,
so a bad image can never be silently submitted.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

MAX_BYTES = 1_048_576
MAX_WIDTH = 1024
MAX_HEIGHT = 1024

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image.jpg")


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Return (width, height) of a JPEG from its SOF0/SOF2 segment."""
    if len(data) < 2 or data[0:2] != b"\xff\xd8":
        raise ValueError("not a JPEG (missing SOI marker)")
    if data[-2:] != b"\xff\xd9":
        raise ValueError("not a whole JPEG (missing EOI marker)")
    i = 2
    while i + 1 < len(data):
        if data[i] != 0xFF:
            raise ValueError("corrupt JPEG segment at offset %d" % i)
        marker = data[i + 1]
        # Standalone markers carry no length field.
        if marker in (0x01, 0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8):
            i += 2
            continue
        if i + 4 > len(data):
            raise ValueError("truncated JPEG segment")
        length = (data[i + 2] << 8) | data[i + 3]
        if marker in (0xC0, 0xC2):  # SOF0 / SOF2: precision, height, width
            if length < 7 or i + 9 > len(data):
                raise ValueError("truncated SOF segment")
            height = (data[i + 5] << 8) | data[i + 6]
            width = (data[i + 7] << 8) | data[i + 8]
            return width, height
        if marker == 0xDA:  # SOS: scan data follows; dimensions already read
            raise ValueError("no SOF segment before scan data")
        i += 2 + length
    raise ValueError("no SOF segment found")


def main() -> None:
    if not os.path.isfile(SOURCE):
        print("error: source image not found: %s" % SOURCE, file=sys.stderr)
        sys.exit(1)
    with open(SOURCE, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        print("error: image is %d bytes, over the 1 MiB limit" % len(data),
              file=sys.stderr)
        sys.exit(1)
    try:
        width, height = jpeg_dimensions(data)
    except ValueError as exc:
        print("error: invalid image: %s" % exc, file=sys.stderr)
        sys.exit(1)
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        print("error: image is %dx%d, over the 1024x1024 limit"
              % (width, height), file=sys.stderr)
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
