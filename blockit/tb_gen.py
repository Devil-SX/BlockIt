import blockit.hdl_re as bire
from pathlib import Path


def gen_instance_str(
    port_data: list[tuple[str, str, str]],
    module_name: str,
    parameter_data: list[tuple[str, str]],
) -> str:
    instance = f"{module_name} "

    if parameter_data:
        instance += "#(\n"
        for i, parameter in enumerate(parameter_data):
            instance += f"  .{parameter[0]}({parameter[1]}),\n"
            if i == len(parameter_data) - 1:
                instance = instance[:-2] + "\n"
        instance += f") u_{module_name} (\n"
    else:
        instance += f"u_{module_name} (\n"

    for i, port in enumerate(port_data):
        instance += f"  .{port[1]}({port[1]}),\n"
        if i == len(port_data) - 1:
            instance = instance[:-2] + "\n"

    instance += ");\n"
    return instance


def print_instance(input_path: Path | str) -> None:
    """读取verilog文件打印实例化代码"""
    with open(input_path, "r") as f:
        content = f.read()
    module_name = bire.get_module_name(content)
    parameter_data = bire.get_paras(content)
    port_data = bire.get_ports(content)
    instance = gen_instance_str(port_data, module_name, parameter_data)
    print(instance)


def gen_instance_file(input_path: Path | str, output_path: Path | str) -> None:
    """读取verilog文件输出实例化文件"""
    with open(input_path, "r") as f:
        content = f.read()
    module_name = bire.get_module_name(content)
    parameter_data = bire.get_paras(content)
    port_data = bire.get_ports(content)
    instance = gen_instance_str(port_data, module_name, parameter_data)
    with open(output_path, "w") as f:
        f.write(instance)
    print(f"Write {output_path} successfully!")


def gen_signals_str(port_data: list[tuple[str, str, str]]) -> str:
    pass
