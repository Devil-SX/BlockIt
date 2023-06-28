"""
This module stores some useful re function to recognize verilog grammer
暂不支持单文件多模块定义识别
Not support for multi-module definition in one file
"""
import re

module_name_re = r"module\s+(\w+)"
# g0 module_name

module_space_re = r"module\s+\w+(?:\s*#\s*\(([\s\S]*?)\))?\s*\(([\s\S]*?)\)\s*;"
# g0 parameter_space, g1 port_space
port_data_re = r"((?:input|output|inout) +(?:reg|wire)? *(?:\[[^:]+\:[^\]]+\])?) *([\w]+),? *(?:\/\/)?([^\n]*)"
# g0 port_type, g1 port_name, g2 port_comment(maybe empty)
parameter_re = (
    r"parameter\s+(?:integer\s+)?(?:\[[^:]+\:[^\]]+\] *)?(\w+)(?:\s*=\s*)?(\d*)"
)

# g0 parameter_name, g2 default_value(maybe empty)


def get_module_name(content: str) -> str:
    """正则表达式匹配，返回Verilog模块的名称"""
    module_name = re.search(module_name_re, content)[1]
    return module_name


def get_paras(content: str) -> list[tuple[str, str]]:
    """正则表达式匹配，返回Verilog模块的参数列表"""
    parameter_space = re.search(module_space_re, content)[1]
    if parameter_space is None:
        return []
    parameter_data = re.findall(parameter_re, parameter_space)
    return parameter_data


def get_ports(content: str) -> list[tuple[str, str, str]]:
    """正则表达式匹配，返回Verilog端口表格字符串"""
    port_space = re.search(module_space_re, content)[2]
    if port_space is None:
        return []
    port_data = re.findall(port_data_re, port_space)
    return port_data


if __name__ == "__main__":
    file_path = "test_file.v"
    with open(file_path, "r") as f:
        content = f.read()
    print("module's paras are:")
    print(get_paras(content))
    print()
    print("module's ports are:")
    print(get_ports(content))
