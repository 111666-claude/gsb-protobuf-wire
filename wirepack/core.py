"""按内嵌 schema 解码 protobuf 线格式。"""

# 字段号与名字的内嵌表，随包一起走。
SCHEMA = [(num, "f%03d" % num) for num in range(1, 201)]
_SCHEMA_BY_NUM = dict(SCHEMA)


class Counter:
    """记录本轮检查过的 schema 条目条数。"""

    def __init__(self):
        self.scanned = 0


def field_name(num, counter):
    counter.scanned += 1
    return _SCHEMA_BY_NUM.get(num)


def read_varint(data, off):
    result = 0
    shift = 0
    while off < len(data):
        byte = data[off]
        off += 1
        result |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return result, off
        shift += 7
    return result, off


def decode(data, counter):
    out = []
    off = 0
    while off < len(data):
        key, off = read_varint(data, off)
        num = key >> 3
        wire = key & 7
        name = field_name(num, counter)
        if name is None:
            name = str(num)
        if wire == 0:
            value, off = read_varint(data, off)
        elif wire == 2:
            length, off = read_varint(data, off)
            value = data[off:off + length].decode("utf-8", "replace")
            off += length
        elif wire == 5:
            value = int.from_bytes(data[off:off + 4], "little")
            off += 4
        else:
            break
        out.append({"num": num, "name": name, "wire": wire, "value": value})
    return out


def table(rows):
    lines = [("field", "name", "wire", "value")]
    for row in rows:
        lines.append((str(row["num"]), row["name"], str(row["wire"]), str(row["value"])))
    widths = [max(len(line[i]) for line in lines) for i in range(4)]
    return "\n".join("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(line))
                     for line in lines)
