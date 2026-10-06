import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wirepack import core


class WireTest(unittest.TestCase):
    def test_small_varint(self):
        data = bytes([(1 << 3) | 0, 5])
        rows = core.decode(data, core.Counter())
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["value"], 5)
        self.assertEqual(rows[0]["name"], "f001")

    def test_trailing_length_delimited(self):
        data = bytes([(2 << 3) | 2, 2]) + b"hi"
        rows = core.decode(data, core.Counter())
        self.assertEqual(rows[0]["value"], "hi")

    def test_empty_payload(self):
        self.assertEqual(core.decode(b"", core.Counter()), [])

    def test_field_number_is_reported(self):
        data = bytes([(7 << 3) | 0, 3])
        rows = core.decode(data, core.Counter())
        self.assertEqual(rows[0]["num"], 7)

    def test_table_has_header(self):
        rows = core.decode(bytes([(1 << 3) | 0, 1]), core.Counter())
        self.assertTrue(core.table(rows).splitlines()[0].startswith("field"))


if __name__ == "__main__":
    unittest.main()
