# -*- coding: utf-8 -*-
"""Build a tiny unencrypted-file MPQ (tables encrypted) with Map.dbc + MapDifficulty.dbc."""
import os, struct, shutil

_crypt = None
def _init_crypt():
    global _crypt
    if _crypt is not None:
        return
    _crypt = [0] * 0x500
    seed = 0x00100001
    for i in range(0x100):
        idx = i
        for _ in range(5):
            seed = (seed * 125 + 3) % 0x2AAAAB
            t1 = (seed & 0xFFFF) << 0x10
            seed = (seed * 125 + 3) % 0x2AAAAB
            t2 = seed & 0xFFFF
            _crypt[idx] = t1 | t2
            idx += 0x100

def mpq_hash(s: str, hash_type: int) -> int:
    _init_crypt()
    seed1 = 0x7FED7FED
    seed2 = 0xEEEEEEEE
    for ch in s.upper().encode("ascii"):
        seed1 = _crypt[(hash_type << 8) + ch] ^ ((seed1 + seed2) & 0xFFFFFFFF)
        seed1 &= 0xFFFFFFFF
        seed2 = (ch + seed1 + seed2 + (seed2 << 5) + 3) & 0xFFFFFFFF
    return seed1

def encrypt_block(data: bytes, key: int) -> bytes:
    """StormLib EncryptMPQBlock: seed updated with PLAINTEXT."""
    _init_crypt()
    seed = 0xEEEEEEEE
    out = bytearray()
    for i in range(0, len(data) // 4 * 4, 4):
        seed = (seed + _crypt[0x400 + (key & 0xFF)]) & 0xFFFFFFFF
        plain = struct.unpack_from("<I", data, i)[0]
        ch = (plain ^ ((key + seed) & 0xFFFFFFFF)) & 0xFFFFFFFF
        key = (((~key << 0x15) + 0x11111111) | (key >> 0x0B)) & 0xFFFFFFFF
        seed = (plain + seed + (seed << 5) + 3) & 0xFFFFFFFF
        out += struct.pack("<I", ch)
    return bytes(out)

def decrypt_block(data: bytes, key: int) -> bytes:
    _init_crypt()
    seed = 0xEEEEEEEE
    out = bytearray()
    for i in range(0, len(data) // 4 * 4, 4):
        seed = (seed + _crypt[0x400 + (key & 0xFF)]) & 0xFFFFFFFF
        val = struct.unpack_from("<I", data, i)[0]
        plain = (val ^ ((key + seed) & 0xFFFFFFFF)) & 0xFFFFFFFF
        key = (((~key << 0x15) + 0x11111111) | (key >> 0x0B)) & 0xFFFFFFFF
        seed = (plain + seed + (seed << 5) + 3) & 0xFFFFFFFF
        out += struct.pack("<I", plain)
    return bytes(out)

def build_mpq(files: dict, out_path: str):
    listfile = "\r\n".join(files.keys()) + "\r\n"
    all_files = dict(files)
    all_files["(listfile)"] = listfile.encode("ascii", "replace")
    names = list(all_files.keys())
    n = len(names)
    ht_size = 16
    while ht_size < n * 2:
        ht_size <<= 1
    block_size_shift = 3
    header_size = 32
    blocks = []
    file_blob = bytearray()
    for name in names:
        data = all_files[name]
        off = header_size + len(file_blob)
        flags = 0x80000000
        blocks.append((off, len(data), len(data), flags))
        file_blob += data
    block_table_pos = header_size + len(file_blob)
    block_table = bytearray()
    for off, csz, rsz, fl in blocks:
        block_table += struct.pack("<IIII", off, csz, rsz, fl)
    hash_table_pos = block_table_pos + len(block_table)
    hash_table = bytearray(b"\xff" * (ht_size * 16))
    for i, name in enumerate(names):
        h_offset = mpq_hash(name, 0)
        h_a = mpq_hash(name, 1)
        h_b = mpq_hash(name, 2)
        idx = h_offset & (ht_size - 1)
        start = idx
        while True:
            entry = struct.unpack_from("<IIII", hash_table, idx * 16)
            if entry[0] == 0xFFFFFFFF:
                struct.pack_into("<IIII", hash_table, idx * 16, h_a, h_b, 0, i)
                break
            idx = (idx + 1) & (ht_size - 1)
            if idx == start:
                raise RuntimeError("hash table full")
    key_hash = mpq_hash("(hash table)", 3)
    key_block = mpq_hash("(block table)", 3)
    enc_hash = encrypt_block(bytes(hash_table), key_hash)
    enc_block = encrypt_block(bytes(block_table), key_block)
    # round-trip check
    assert decrypt_block(enc_hash, key_hash) == bytes(hash_table)
    assert decrypt_block(enc_block, key_block) == bytes(block_table)
    archive_size = header_size + len(file_blob) + len(enc_block) + len(enc_hash)
    header = struct.pack(
        "<4sIIHHIIII",
        b"MPQ\x1a",
        header_size,
        archive_size,
        0,
        block_size_shift,
        hash_table_pos,
        block_table_pos,
        ht_size,
        n,
    )
    assert len(header) == 32
    with open(out_path, "wb") as f:
        f.write(header)
        f.write(file_blob)
        f.write(enc_block)
        f.write(enc_hash)
    print("wrote", out_path, os.path.getsize(out_path), names)

if __name__ == "__main__":
    base = r"E:\azerothcore\modules\mod-timewalking\client-patch\DBFilesClient"
    files = {
        r"DBFilesClient\Map.dbc": open(os.path.join(base, "Map.dbc"), "rb").read(),
        r"DBFilesClient\MapDifficulty.dbc": open(os.path.join(base, "MapDifficulty.dbc"), "rb").read(),
    }
    out = r"E:\azerothcore\modules\mod-timewalking\client-patch\patch-zhCN-TW.MPQ"
    build_mpq(files, out)
    shutil.copy2(out, r"F:\claw-code\Lwow\Data\zhCN\patch-zhCN-9.MPQ")
    print("installed patch-zhCN-9.MPQ")
    from mpyq import MPQArchive
    a = MPQArchive(out)
    print("listfile ok", a.files)
    m = a.read_file(r"DBFilesClient\Map.dbc")
    print("Map.dbc", len(m) if m else None)
