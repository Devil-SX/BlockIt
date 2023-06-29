#!/usr/bin/python3
import argparse
from pathlib import Path
import blockit.doc_gen as bidoc
import blockit.tb_gen as bitb


def doc(args):
    output_dir = Path(args.output)
    if not output_dir.is_dir():
        Path(args.output).mkdir(parents=True)

    for file in args.file_path:
        bidoc.gen_markdown_file(file, output_dir)


def tb(args):
    for file in args.file_path:
        bitb.print_instance(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blockit Verilog Auto Toolbox")
    subparsers = parser.add_subparsers()
    # Auto Doc
    parser_doc = subparsers.add_parser("doc", help="Generate Markdown document")
    parser_doc.add_argument(
        "file_path", type=str, nargs="+", help="Verilog module file path"
    )
    parser_doc.add_argument(
        "-o", "--output", type=str, default="doc", help="Output file dir"
    )
    parser_doc.set_defaults(func=doc)

    # Auto Testbench
    parser_tb = subparsers.add_parser("tb", help="Generate Testbench")
    parser_tb.add_argument(
        "file_path", type=str, nargs="+", help="Verilog module file path"
    )
    parser_tb.set_defaults(func=tb)

    args = parser.parse_args()
    args.func(args)
