#!/usr/bin/env python3
"""Map a decompressed Nintendo 3DS ExeFS .code image using exheader metadata.

Input:
- JSON produced by tools/inspect_3ds_exheader.py
- a locally extracted, decompressed ExeFS .code image

The tool emits only metadata and hashes. It does not redistribute game code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ORDER = ("text", "rodata", "data")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exheader_json", type=Path)
    parser.add_argument("code", type=Path, help="decompressed ExeFS .code")
    parser.add_argument("-o", "--output", type=Path, default=Path("code_layout.json"))
    args = parser.parse_args()

    meta = json.loads(args.exheader_json.read_text(encoding="utf-8"))
    sci = meta["system_control_info"]
    raw = args.code.read_bytes()

    cursor = 0
    sections = []
    for name in ORDER:
        info = sci[name]
        alloc = int(info["physical_region_bytes"])
        logical = int(info["size"])
        file_start = cursor
        file_end = cursor + alloc
        logical_end = file_start + logical
        available_end = min(file_end, len(raw))
        logical_available_end = min(logical_end, len(raw))
        sections.append({
            "name": name,
            "virtual_address": int(info["address"]),
            "virtual_address_hex": f"0x{int(info['address']):08X}",
            "logical_size": logical,
            "allocated_size": alloc,
            "file_offset": file_start,
            "file_offset_hex": f"0x{file_start:X}",
            "file_end": file_end,
            "file_end_hex": f"0x{file_end:X}",
            "logical_file_end": logical_end,
            "logical_file_end_hex": f"0x{logical_end:X}",
            "fully_present": file_end <= len(raw),
            "logical_sha256": sha256_bytes(raw[file_start:logical_available_end]),
            "allocated_sha256": sha256_bytes(raw[file_start:available_end]),
        })
        cursor = file_end

    payload = {
        "schema": "sakurai.decompilation.3ds-code-layout.v1",
        "source_code_name": args.code.name,
        "source_code_size": len(raw),
        "expected_allocated_size": cursor,
        "size_matches_expected_layout": len(raw) == cursor,
        "sections": sections,
        "bss_size": int(sci["bss_size"]),
        "notes": [
            "Application .code layout is mapped in text/rodata/data order using exheader physical-region page sizes.",
            "Use only on a decompressed .code image when CompressExefsCode is set.",
            "If size_matches_expected_layout is false, stop and verify extraction/decompression before instruction-level work.",
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"mapped {len(sections)} sections -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
