"""命令行入口。"""

import argparse
import binascii

from . import core, samples


def main(argv=None):
    ap = argparse.ArgumentParser(prog="wirepack")
    ap.add_argument("--sample", choices=["varint", "length", "dup", "unknown", "work"])
    sub = ap.add_subparsers(dest="cmd")
    decode_parser = sub.add_parser("decode")
    decode_parser.add_argument("--hex", required=True)
    args = ap.parse_args(argv)

    if args.sample:
        return samples.run(args.sample)
    if args.cmd is None:
        ap.print_help()
        return 2

    data = binascii.unhexlify(args.hex)
    print(core.table(core.decode(data, core.Counter())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
