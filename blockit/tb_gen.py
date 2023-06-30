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


def gen_instance(input_paths: list[Path | str], output_path: Path | str = None) -> None:
    """读取verilog文件输出实例化文件"""
    output = ""
    for file in input_paths:
        with open(file, "r") as f:
            content = f.read()
        module_name = bire.get_module_name(content)
        parameter_data = bire.get_paras(content)
        port_data = bire.get_ports(content)
        instance = gen_instance_str(port_data, module_name, parameter_data)
        output += instance + "\n"

    if output_path is None:
        # 如果没提供输出路径打印在终端
        print(output, end=None)
    else:
        mode = "w"
        if Path(output_path).exists():
            # 存在则追加写入
            mode = "a"
        with open(output_path, mode) as f:
            f.write(output)
        print(f"Write instances {output_path} successfully!")


def gen_signals_str(port_data: list[tuple[str, str, str]], module_name: str) -> str:
    signals = f"// {module_name} Signals\n"

    for i, port in enumerate(port_data):
        if "output" in port[0]:
            signals += port[0].replace("output", "wire")
            signals += " " + port[1] + ";\n"

    signals += "\n"
    return signals


def gen_signals(input_paths: list[Path | str], output_path: Path | str = None) -> None:
    """读取verilog文件生成信号文件"""
    output = ""
    for file in input_paths:
        with open(file, "r") as f:
            content = f.read()
        module_name = bire.get_module_name(content)
        port_data = bire.get_ports(content)
        signals = gen_signals_str(port_data, module_name)
        output += signals + "\n"

    if output_path is None:
        # 如果没提供输出路径打印在终端
        print(output, end=None)
    else:
        mode = "w"
        if Path(output_path).exists():
            # 存在则追加写入
            mode = "a"
        with open(output_path, mode) as f:
            f.write(output)
        print(f"Write signals {output_path} successfully!")
