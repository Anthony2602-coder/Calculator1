"""Generate PNG icons without external dependencies."""

import struct
import zlib
from pathlib import Path


def _chunk(tag, data):
    crc = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)


def make_png(size, rgb=(99, 102, 241)):
    header = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    row = b"\x00" + bytes(rgb) * size
    idat = zlib.compress(row * size, 9)
    return header + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", idat) + _chunk(b"IEND", b"")


def main():
    out = Path(__file__).parent / "static" / "icons"
    out.mkdir(parents=True, exist_ok=True)
    for s, n in ((192, "icon-192.png"), (512, "icon-512.png")):
        (out / n).write_bytes(make_png(s))
        print(f"Created {out / n}")


if __name__ == "__main__":
    main()
