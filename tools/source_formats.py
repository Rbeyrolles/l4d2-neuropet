"""Write the project's RGBA8888 VTF and embedded single-file VPK formats."""
from pathlib import Path
import struct
import zlib


def write_vtf(path, images):
    """VTF 7.2, RGBA8888, one mip, no thumbnail, embedded animation frames."""
    width, height = images[0].size
    assert all(im.size == (width, height) for im in images)
    header = bytearray(80)
    struct.pack_into("<4sIIIHHIHH", header, 0, b"VTF\0", 7, 2, 80,
                     width, height, 0x230C, len(images), 0)
    struct.pack_into("<3f", header, 32, 0.5, 0.5, 0.5)
    struct.pack_into("<fIBI", header, 48, 1.0, 0, 1, 0xFFFFFFFF)
    struct.pack_into("<BBH", header, 61, 0, 0, 1)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(header + b"".join(im.convert("RGBA").tobytes() for im in images))


def write_vpk(path, files):
    """Single-file VPK v1, all data embedded (archive index 0x7fff)."""
    grouped = {}
    for name, data in sorted(files.items()):
        item = Path(name)
        extension = item.suffix[1:] or " "
        directory = item.parent.as_posix()
        directory = " " if directory == "." else directory
        grouped.setdefault(extension, {}).setdefault(directory, []).append((item.stem, data))
    tree = bytearray()
    payload = bytearray()
    for extension, directories in sorted(grouped.items()):
        tree += extension.encode("utf-8") + b"\0"
        for directory, entries in sorted(directories.items()):
            tree += directory.encode("utf-8") + b"\0"
            for name, data in entries:
                tree += name.encode("utf-8") + b"\0"
                tree += struct.pack("<IHHIIH", zlib.crc32(data), 0, 0x7FFF,
                                    len(payload), len(data), 0xFFFF)
                payload += data
            tree += b"\0"
        tree += b"\0"
    tree += b"\0"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(struct.pack("<III", 0x55AA1234, 1, len(tree)) + tree + payload)
