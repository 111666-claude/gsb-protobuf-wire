"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _key(num, wire):
    value = (num << 3) | wire
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def run(name):
    if name == "varint":
        data = _key(1, 0) + bytes([0xAC, 0x02])
        rows = core.decode(data, core.Counter())
        _line({"value": rows[0]["value"] if rows else None})
        return 0
    if name == "length":
        data = _key(2, 2) + bytes([2]) + b"hi" + _key(3, 0) + bytes([1])
        rows = core.decode(data, core.Counter())
        _line({"fields": [row["num"] for row in rows]})
        return 0
    if name == "dup":
        data = _key(1, 0) + bytes([1]) + _key(1, 0) + bytes([2])
        rows = core.decode(data, core.Counter())
        _line({"fields": [row["num"] for row in rows]})
        return 0
    if name == "unknown":
        data = _key(999, 0) + bytes([7])
        rows = core.decode(data, core.Counter())
        _line({"fields": [row["num"] for row in rows]})
        return 0
    if name == "work":
        data = b"".join(_key(i % 200 + 1, 0) + bytes([1]) for i in range(2000))
        counter = core.Counter()
        rows = core.decode(data, counter)
        _line({"fields": 2000, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
