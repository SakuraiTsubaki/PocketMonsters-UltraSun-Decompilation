#!/usr/bin/env python3
"""Inspect a locally extracted Nintendo 3DS NCCH exheader.

Reads only the System Control Info fields needed to establish the initial
executable memory map for decompilation. No game content is embedded or
redistributed by this tool.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

MIN_SIZE = 0x200
PAGE_SIZE = 0x1000


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def u16(data: bytes, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def u64(data: bytes, offset: int) -> int:
    return struct.unpack_from("<Q", data, offset)[0]


def codeset(data: bytes, offset: int) -> dict:
    address = u32(data, offset)
    pages = u32(data, offset + 4)
    size = u32(data, offset + 8)
    return {
        "address": address,
        "address_hex": f"0x{address:08X}",
        "physical_region_pages": pages,
        "physical_region_bytes": pages * PAGE_SIZE,
        "size": size,
        "size_hex": f"0x{size:X}",
        "end_address": address + size,
        "end_address_hex": f"0x{address + size:08X}",
    }


def parse_exheader(path: Path) -> dict:
    raw = path.read_bytes()
    if len(raw) < MIN_SIZE:
        raise ValueError(f"exheader is too small: {len(raw)} bytes; need at least {MIN_SIZE}")

    title_raw = raw[0:8]
    title = title_raw.rstrip(b"\0").decode("ascii", errors="replace")
    flags = raw[0xD]
    remaster_version = u16(raw, 0xE)

    dependencies = []
    for off in range(0x40, 0x1C0, 8):
        program_id = u64(raw, off)
        if program_id:
            dependencies.append(f"0x{program_id:016X}")

    return {
        "schema": "sakurai.decompilation.3ds-exheader.v1",
        "path": path.name,
        "file_size": len(raw),
        "sha256": sha256_file(path),
        "system_control_info": {
            "application_title": title,
            "flags": flags,
            "flags_hex": f"0x{flags:02X}",
            "compress_exefs_code": bool(flags & 0x01),
            "sd_application": bool(flags & 0x02),
            "remaster_version": remaster_version,
            "text": codeset(raw, 0x10),
            "stack_size": u32(raw, 0x1C),
            "rodata": codeset(raw, 0x20),
            "data": codeset(raw, 0x30),
            "bss_size": u32(raw, 0x3C),
            "dependencies": dependencies,
        },
        "notes": [
            "Addresses and sizes come from the NCCH System Control Info.",
            "A compressed ExeFS .code must be decompressed before code-level matching.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exheader", type=Path, help="locally extracted exheader.bin")
    parser.add_argument("-o", "--output", type=Path, help="write JSON report here")
    args = parser.parse_args()

    result = parse_exheader(args.exheader.expanduser().resolve())
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
