import re

module_name_re = r"module\s+(\w+)"
port_data_re = r"((?:input|output) +(?:reg|wire)? +(?:\[[^:]+\:[^\]]+\])?) *([\w ]+),? *(?:\/\/)?([^\n]*)"


def parse_verilog(file_path:str)->list[tuple[str, str,str]]:
    """返回Verilog模块的名称和端口表格字符串"""
    # 读取Verilog模块定义文件
    with open(file_path, 'r') as f:
        content = f.read()

    # 使用正则表达式解析模块定义的端口
    module_name = re.findall(module_name_re, content)[0]
    port_data = re.findall(port_data_re, content)

    return module_name, port_data


def gen_markdown_str(port_data:list[tuple[str, str,str]], module_name:str)->str:
    # 生成Markdown表格
    table_lines = ["| 端口名称 | 端口类型 | 端口说明 |"]
    table_lines.append("| --- | --- | --- |")
    for port in port_data:
        table_lines.append(f"| {port[1]} | {port[0]} | {port[2]} |")

    table_str = "\n".join(table_lines)
    table_str = f"# {module_name}\n\n" + table_str
    return table_str


if __name__ == "__main__":
    module_name, port_data = parse_verilog("test_file.v")
    print("模块名称：", module_name)
    print("端口：\n", port_data)
