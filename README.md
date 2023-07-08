<h1 align="center">
    Block it!
    <br>
</h1>

<p align="center">
  提高您的Verilog设计工作效率！
</p>

<p align="center">
    <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"></a>
    <img alt="HDL" src="https://img.shields.io/badge/Verilog-155489?style=for-the-badge"></a>
</p>

<p align="center">
<b>⚠️ 该仓库已停止开发!</b></br>
项目定位出了点问题,因此停止开发</br>
</p>

- 该仓库使用 正则表达式 解析Verilog语法(也就是做[Parsing](https://en.wikipedia.org/wiki/Parsing) ), 使用如[Bison](https://www.gnu.org/software/bison/)的语法检查器生成器更加自然.Verilog语法检查器已有不少开源项目,项目放弃维护Verilog Parsing模块.
- Verilog层次可视化化已有[Verilog-DOT](https://github.com/ben-marshall/verilog-dot)实现


---


在阅读HDL代码时，总想着要是可以 **像Vivado的Block Design查看模块间的连线** 就好了呀！

最初的构想只是想写一个类似Vivado的Block Design可视化工具，后来发展为辅助Verilog编程的自动化脚本工具箱

**目前工具尚不支持单文件内定义多模块的写法**

门级网表的可视化可以参考[yosys](https://github.com/YosysHQ/yosys)

# Features

- （半）自动生成模块文档
- （半）自动生成Testbench
- 查看模块层次结构 (doing)
- 查看模块互联结构 (doing)

# Get Started

测试环境 Python 3.10 / Ubuntu 22.04

先切换到仓库目录

安装环境（目前还没有依赖环境）

```
pip install -r requirements.txt
```

查看帮助

```
python bi.py --help
```

或者您可以将项目目录添加至环境变量，并修改`bi.py`开头的`#!/usr/bin/python3`制定使用的python解释器，之后便可在任意位置调用该脚本

即

```
bi.py --help
```

# Documents

- [自动生成文档](./doc/auto_doc.md)
- [自动化编写测试用例](./doc/auto_testbench.md)
- (todo)[自动生成仿真脚本](./doc/auto_simulation.md)
- (todo)[可视化层次关系](./doc/visualize_hirearchy.md)
- (todo)[可视化互联关系](./doc/visualize_connections.md)

# Targets

- 识别模块、端口、参数 <- Current State
- 识别模块之间耦合关系
- 识别模块内部代码含义

# Reference 

[better-layout-of-nodes-for-block-diagrams-in-dot](https://stackoverflow.com/questions/8042801/better-layout-of-nodes-for-block-diagrams-in-dot)

[block-diagram-layout-with-dot-graphviz](https://stackoverflow.com/questions/7922960/block-diagram-layout-with-dot-graphviz)