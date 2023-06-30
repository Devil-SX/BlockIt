# Auto Testbench 自动编写测试文件

```
bi.py tb [-h] [-m {s,i} [{s,i} ...]] [-o OUTPUT] file_path [file_path ...]
```

testbench的工作
- 多模块实例化
- 定义互联信号，连接各个模块
- 编写测试任务

```
bi.py tb [-o OUTPUT] file_path [file_path ...]
```

选择输入文件的路径和输出路径，若没有提供输出路径，则打印在终端

通过参数 `-m` `--mode` 选择生成文件内容， `s` 代表信号， `i` 代表实例。 可多选。

比如，将当前目录下所有Verilog文件例化并生成所需要的互联信号，写入文件保存在当前目录下

```
bi.py tb *.v -o ./testbench.v -m s i
```

## 互联信号说明

一个模块的输入可能来自两种信号
- 其他模块的输出
- 测试文件中定义的信号

对于后者自动生成比较难，先完成在testbench中自动生成前者信号
