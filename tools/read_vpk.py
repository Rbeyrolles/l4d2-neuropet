"""Read an individual entry from a Valve VPK without extracting the archive."""
from pathlib import Path
import struct
import sys
import zlib


def entries(pack):
    pack = Path(pack)
    with pack.open("rb") as stream:
        signature, version, tree_size = struct.unpack("<III", stream.read(12))
        if signature != 0x55AA1234 or version not in (1, 2):
            raise ValueError(f"Unsupported VPK: {pack}")
        header_size = 12 if version == 1 else 28
        stream.seek(header_size)
        tree = stream.read(tree_size)
    offset = 0

    def string():
        nonlocal offset
        end = tree.index(0, offset)
        value = tree[offset:end].decode("utf-8", errors="surrogateescape")
        offset = end + 1
        return value

    while extension := string():
        while directory := string():
            while name := string():
                crc, preload_size, archive, entry_offset, length, terminator = struct.unpack_from("<IHHIIH", tree, offset)
                if terminator != 0xFFFF:
                    raise ValueError("Invalid entry terminator")
                offset += 18
                preload = tree[offset:offset + preload_size]
                offset += preload_size
                key = ("" if directory == " " else directory + "/") + name
                key += "" if extension == " " else "." + extension
                yield key, (crc, archive, entry_offset, length, preload, header_size + tree_size)


def read_entry(pack, name):
    pack = Path(pack)
    for key, (crc, archive, offset, length, preload, payload_start) in entries(pack):
        if key.casefold() != name.casefold():
            continue
        if archive == 0x7FFF:
            data_file = pack
            offset += payload_start
        else:
            stem = pack.stem.removesuffix("_dir")
            data_file = pack.with_name(f"{stem}_{archive:03d}.vpk")
        with data_file.open("rb") as stream:
            stream.seek(offset)
            data = preload + stream.read(length)
        if zlib.crc32(data) != crc:
            raise ValueError(f"CRC mismatch: {key}")
        return data
    raise KeyError(name)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        for key, _ in entries(sys.argv[1]):
            print(key)
    else:
        data = read_entry(sys.argv[1], sys.argv[2])
        if len(sys.argv) == 4:
            destination = Path(sys.argv[3])
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            print(destination)
        else:
            print(data.decode("utf-8", errors="replace"))
