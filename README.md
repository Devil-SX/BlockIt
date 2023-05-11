<h1 align="center">
    Block it!（Unfinished)
    <br>
</h1>

<p align="center">
  使用Block Diagram查看HDL模块互联方式
</p>

<p align="center">
    <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"></a>
    <img alt="HDL" src="https://img.shields.io/badge/Verilog-155489?style=for-the-badge"></a>
</p>

在阅读HDL代码时，总想着要是可以**像Vivado的Block Design查看模块间的连线**就好了呀！

Block It旨在使用类似的方式可视化HDL代码，提高阅读效率！

> 因为行为级建模无法提取出电路的输入/输出，所以只能分析纯互联模块（如顶层模块，或者门级网表，门级网表的可视化可以参考[yosys](https://github.com/YosysHQ/yosys)）

# Features

- 识别Verilog模块，并将模块间互联方式可视化呈现
- 将渲染的图像保存

# Usage

Env: Python 3.10

## Prepared

```
pip install -r requirements.txt
```

## Run

```
python ./main.py
```
