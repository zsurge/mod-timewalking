# -*- coding: utf-8 -*-
"""Build locale patch MPQ with Map.dbc + MapDifficulty.dbc via StormLib (pympq).

WoW 3.3.5 Storm rejects naive homemade uncompressed MPQs (MemoryStorm OOM).
This script creates a zlib-compressed MPQ v1 archive matching official patch flags.
"""
import os
import shutil
import sys

def build_mpq(files: dict, out_path: str):
    try:
        import pympq
    except ImportError as e:
        raise SystemExit("需要 pympq（StormLib）：pip install pympq\n" + str(e))

    if os.path.exists(out_path):
        os.remove(out_path)

    # Stage files to a temp folder so add_file gets real paths
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        disk_map = {}
        for arch_name, data in files.items():
            disk = os.path.join(td, arch_name.replace("\\", "_").replace("/", "_"))
            with open(disk, "wb") as f:
                f.write(data)
            disk_map[arch_name] = disk

        create_flags = [pympq.MPQ_CREATE_ARCHIVE_V1, pympq.MPQ_CREATE_LISTFILE]
        file_flags = [
            pympq.MPQ_FILE_COMPRESS,
            pympq.MPQ_FILE_REPLACEEXISTING,
        ]
        comp = [pympq.MPQ_COMPRESSION_ZLIB]

        with pympq.create_archive(out_path, create_flags, max(32, len(files) * 4)) as mpq:
            for arch_name, disk in disk_map.items():
                mpq.add_file(disk, arch_name, file_flags, comp)
            mpq.compact()

    # Round-trip check
    with pympq.open_archive(out_path) as mpq:
        for arch_name, data in files.items():
            if not mpq.has_file(arch_name):
                raise RuntimeError("missing in archive: " + arch_name)
            ext = out_path + ".check_" + os.path.basename(arch_name)
            mpq.extract_file(arch_name, ext)
            got = open(ext, "rb").read()
            os.remove(ext)
            if got != data:
                raise RuntimeError("round-trip mismatch: " + arch_name)
    print("wrote", out_path, os.path.getsize(out_path), list(files))

if __name__ == "__main__":
    base = r"E:\azerothcore\modules\mod-timewalking\client-patch\DBFilesClient"
    files = {
        r"DBFilesClient\Map.dbc": open(os.path.join(base, "Map.dbc"), "rb").read(),
        r"DBFilesClient\MapDifficulty.dbc": open(os.path.join(base, "MapDifficulty.dbc"), "rb").read(),
    }
    out = r"E:\azerothcore\modules\mod-timewalking\client-patch\patch-zhCN-TW.MPQ"
    build_mpq(files, out)

    # Install to known clients if present
    for dest in (
        r"F:\World of Warcraft Dev\Data\zhCN\patch-zhCN-9.MPQ",
        r"F:\claw-code\Lwow\Data\zhCN\patch-zhCN-9.MPQ",
    ):
        ddir = os.path.dirname(dest)
        if os.path.isdir(ddir):
            shutil.copy2(out, dest)
            print("installed", dest)