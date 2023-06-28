<h1 align="center">
    Block it!
    <br>
</h1>

<p align="center">
  提供您的Verilog设计工作效率！
</p>

<p align="center">
    <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"></a>
    <img alt="HDL" src="https://img.shields.io/badge/Verilog-155489?style=for-the-badge"></a>
</p>

# 来源

在阅读HDL代码时，总想着要是可以 **像Vivado的Block Design查看模块间的连线** 就好了呀！

最初的构想只是想写一个类似Vivado的Block Design可视化工具，后来发展为辅助Verilog编程的自动化脚本工具箱。

**目前工具尚不支持单文件内定义多模块的写法。**

门级网表的可视化可以参考[yosys](https://github.com/YosysHQ/yosys)

# Features

- 自动生成模块文档
- 查看模块层次结构 (doing)
- 查看模块互联结构 (doing)

# Get Started

测试环境 Python 3.10 / Ubuntu 22.04

先切换到仓库目录

安装环境

```
pip install -r requirements.txt
```

查看帮助

```
python blockit.py --help
```

或者您可以将项目目录添加至环境变量，并修改`blockit.py`开头的`#!/usr/bin/python3`制定使用的python解释器，之后便可在任意位置调用该脚本

即

```
blockit.py --help
```

# Auto Doc 自动生成说明文档

```
blockit.py [-o OUTPUT] file_path [file_path ...]
```

该命令将自动识别并生成指定文件的说明文档，包含模块名称、模块参数、模块参数

`-o` 参数不指定则默认生成在 `/doc` 目录下

比如`bockit.py *.v`自动生成当前目录下所有.v文件的文档

# Visualize Hierarchy 可视化模块层次

todo

# Visualize Connetions 可视化互联结构

todo


## Reference 

[better-layout-of-nodes-for-block-diagrams-in-dot](https://stackoverflow.com/questions/8042801/better-layout-of-nodes-for-block-diagrams-in-dot)

[block-diagram-layout-with-dot-graphviz](https://stackoverflow.com/questions/7922960/block-diagram-layout-with-dot-graphviz)