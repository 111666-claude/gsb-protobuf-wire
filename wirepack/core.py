"""按内嵌 schema 解码 protobuf 线格式。"""

# 字段号与名字的内嵌表，随包一起走。
SCHEMA = [(num, "f%03d" % num) for num in range(1, 201)]


class Counter:
    """记录本轮检查过的 schema 条目条数。"""

    def __init__(self):
        self.scanned = 0


def field_name(num, counter):
    for entry_num, name in SCHEMA:
        counter.scanned += 1
        if entry_num == num:
            return name
    return None


def read_key(data, off):
    shift = 0
    key = 0
    while off < len(data):
        byte = data[off]
        off += 1
        key |= (byte & 0x7F) << shift
        if byte < 0x80:
            break
        shift += 7
    return key, off


def decode(data, counter):
    out = []
    off = 0
    while off < len(data):
        key, off = read_key(data, off)
        num = key >> 3
        wire = key & 7
        name = field_name(num, counter)
        if wire == 0:
            value = data[off]
            off += 1
        elif wire == 2:
            value = data[off + 1:].decode("utf-8", "replace")
            off = len(data)
        elif wire == 5:
            value = int.from_bytes(data[off:off + 4], "little")
            off += 4
        else:
            break
        if name is None:
            continue
        merged = False
        for row in out:
            if row["num"] == num:
                row["value"] = value
                merged = True
                break
        if not merged:
            out.append({"num": num, "name": name, "wire": wire, "value": value})
    return out


def table(rows):
    lines = [("field", "name", "wire", "value")]
    for row in rows:
        lines.append((str(row["num"]), row["name"], str(row["wire"]), str(row["value"])))
    widths = [max(len(line[i]) for line in lines) for i in range(4)]
    return "\n".join("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(line))
                     for line in lines)
