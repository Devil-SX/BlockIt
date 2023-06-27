import argparse
from pathlib import Path
from read_ports import parse_verilog, gen_markdown_str


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Convert module to markdown table')
  parser.add_argument('file_path', type=str, nargs='+', help='Verilog module file path')
  parser.add_argument('-o', '--output', type=str, default="doc",help='Output file dir')
  args = parser.parse_args()

  if args.file_path:
    # Check Dir
    output_dir = Path(args.output)
    if not output_dir.is_dir():
      Path(args.output).mkdir(parents=True)

    for file in args.file_path:
      module_name, port_data = parse_verilog(file)
      table_str = gen_markdown_str(port_data, module_name)
      out_path = output_dir / f"{module_name}.md"
      with open(out_path, 'w') as f:
        f.write(table_str)
        print(f"Ports of {module_name}\t-> {out_path} Finished!")