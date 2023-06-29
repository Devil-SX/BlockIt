import blockit.hdl_re as bire
from pathlib import Path


def gen_markdown_str(
    port_data: list[tuple[str, str, str]],
    module_name: str,
    parameter_data: list[tuple[str, str]],
) -> str:
    markdown = f"# {module_name}\n\n"

    # parameters
    markdown += "## Parameters\n\n"
    if parameter_data:
        table_lines = ["| ParaName | DefaultValue |"]
        table_lines.append("| --- | --- |")
        for parameter in parameter_data:
            table_lines.append(f"| {parameter[0]} | {parameter[1]} |")
        parameter_str = "\n".join(table_lines)
        markdown += parameter_str + "\n\n"
    else:
        markdown += "This module has no parameter!\n\n"

    # ports
    markdown += "## Ports\n\n"
    if port_data:
        table_lines = ["| PortName | Type | Description |"]
        table_lines.append("| --- | --- | --- |")
        for port in port_data:
            table_lines.append(f"| {port[1]} | {port[0]} | {port[2]} |")
        table_str = "\n".join(table_lines)
        markdown += table_str + "\n\n"
    else:
        markdown += "This module has no port!\n\n"

    return markdown


def gen_markdown_file(input_path: Path | str, output_dir: Path) -> None:
    """读取verilog文件输出markdown文件"""
    with open(input_path, "r") as f:
        content = f.read()
    module_name = bire.get_module_name(content)
    parameter_data = bire.get_paras(content)
    port_data = bire.get_ports(content)
    markdown = gen_markdown_str(port_data, module_name, parameter_data)
    output_path = output_dir / f"{module_name}.md"
    with open(output_path, "w") as f:
        f.write(markdown)
    print(f"Write {output_path} successfully!")
