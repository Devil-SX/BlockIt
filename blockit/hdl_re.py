"""
This module stores some useful re function to recognize verilog grammer
暂不支持单文件多模块定义识别
Not support for multi-module definition in one file
"""
import re

module_name_re = r"module\s+(\w+)"
# g0 module_name


module_space_re = (
    r"module\s+\w+(?:\s*#\s*\(([\s\S]*?)\))?\s*\(([\s\S]*?)\)\s*;([\s\S]*?)endmodule"
)
# g0 parameter_space, g1 port_space, g2 body_space


# para space
parameter_re = (
    r"parameter\s+(?:integer\s+)?(?:\[[^:]+\:[^\]]+\] *)?(\w+)(?:\s*=\s*)?(\d*)"
)
# ()g0 parameter_name, g2 default_value(maybe empty)
port_data_re = r"((?:input|output|inout)(?: +reg|wire)? *(?:\[[^:]+\:[^\]]+\])?) *([\w]+),? *(?:\/\/)?([^\n]*)"
# (port_sapace)g0 port_type, g1 port_name, g2 port_comment(maybe empty)
comment_re = r"\/\/([\s\S]*?)\n"
# g0 comment
instance_re = r"(\w+)(?:\s*#\s*\([\s\S]*?\))?\s+(\w+)\s*\(([\s\S]*?)\)\s*;"
# (body_space)g0 instance_module, g1 instance_name, g2 instance_space
instance_port_re = r"\.(\w+)\(\s*([\s\S]*?)\s*\)\s*?(?=,|\s)"
# (instance_space)g0 port_name, g1 siganl_name


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


def get_instance(content: str) -> list[tuple[tuple[str, str], list[tuple[str, str]]]]:
    """返回Verilog例化模块s名称、端口信号"""
    body_space = re.search(module_space_re, content)[3]
    body_space = re.sub(comment_re, "", body_space)  # 移除注释内容
    instance_data = re.findall(instance_re, body_space)
    instance_name_list = [(instance[0], instance[1]) for instance in instance_data]
    instance_port_list = [
        re.findall(instance_port_re, instance[2]) for instance in instance_data
    ]
    instance_port_list_fixed = [
        [
            (port_signal[0], re.sub(r"\[[\s\S]*\]", "", port_signal[1]))  # 移除切片获得信号名称
            for port_signal in instance
        ]
        for instance in instance_port_list
    ]
    return list(zip(instance_name_list, instance_port_list_fixed))


if __name__ == "__main__":
    file_path = "test_file.v"
    with open(file_path, "r") as f:
        content = f.read()
    print("module's paras are:")
    print(get_paras(content))
    print()
    print("module's ports are:")
    print(get_ports(content))
    print()
    print("module's instance are:")
    print(get_instance(content))
