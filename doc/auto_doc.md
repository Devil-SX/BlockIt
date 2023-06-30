# Auto Doc 自动生成模块接口文档

```
blockit.py doc [-h] [-o OUTPUT] file_path [file_path ...]
```

该命令将自动识别并生成指定文件的说明文档，包含模块名称、模块参数、模块参数

`-o` 参数不指定则默认生成在 `/doc` 目录下

比如`bockit.py *.v`自动生成当前目录下所有.v文件的文档