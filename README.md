# protobuf-wire

按随包的内嵌 schema 解码 protobuf 线格式，输出字段表。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m wirepack decode --hex 0805
python3 -m wirepack --sample=varint|length|dup|unknown|work
```

## 口径

- **键**：一个字节以上的 varint，低 3 位是 wire type，高位是字段号。
- **varint**：7 位一组、低位在前，最高位为 1 表示还有后续字节；字段号与 varint 值都要按这个规则解。
- **长度界定**：wire type 2 的值长度也是 varint，按长度取完这一段后继续读下一个字段。
- **重复字段**：同一字段号多次出现要各留一条，顺序与报文一致。
- **未知字段**：schema 里没有的字段号也要保留（名字用字段号表示）。

## 不变量

- 解出的字段条数与报文里出现的字段数一致（重复也算）。
- 字段顺序与报文一致。
- `scanned` 不随字段数乘 schema 长度放大：两千个字段的 `scanned` 不超过 9000。

## 输出契约

`decode` 打印对齐表格，列顺序为 `field`、`name`、`wire`、`value`。
`--sample=work` 只打印 `{"fields": N, "decoded": N, "scanned": N}`。
