import re
import logging
import pprint
from graphviz import Digraph
from tkinter import *
from tkinter import filedialog


# 正则表达式模式
module_pattern = r'module\s+([\w]+)\s*\(([\w,\s\[\]:\/]*)\)\s*;'
input_pattern = r'input\s+([\w\[:\]]+)\s+'
output_pattern = r'output\s+([\w\[:\]]+)\s+'
inout_pattern = r'inout\s+([\w\[:\]]+)\s+'

instance_pattern = r'(\w+)\s+(\w+)\(([\s\S]*\));'
signal_pattern = r'\.(\w+)\s+\(([\w\[\]]+)\s+\)'


# 读取Verilog文件并解析
def read_verilog_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

        # 解析模块
        module_matches = re.findall(module_pattern, content)
        module_dict = {}
        for match in module_matches:
            module_name = match[0]
            signal_str = match[1]
            input_matches = re.findall(input_pattern, signal_str)
            output_matches = re.findall(output_pattern, signal_str)
            inout_matches = re.findall(inout_pattern, signal_str)
            signal_dict = {'inputs': input_matches, 'outputs': output_matches, 'inouts': inout_matches}
            module_dict[module_name] = signal_dict

        logging.info(pprint.pformat(module_dict,indent=4))

        # 解析信号
        signal_matches = re.findall(r'([\w\d_,\s]*)\s*;', content)
        signal_dict = {}
        for matches in signal_matches:
            for signal in matches.split(','):
                signal_type = 'unknown'
                if signal.strip().startswith('input'):
                    signal_type = 'input'
                elif signal.strip().startswith('output'):
                    signal_type = 'output'
                elif signal.strip().startswith('inout'):
                    signal_type = 'inout'
                if signal_type != 'unknown':
                    signal_name = signal.strip().split()[1]
                    signal_dict[signal_name] = signal_type

    return module_dict, signal_dict


# 生成连接图
def generate_connection_graph(top_module_name, module_dict):
    dot = Digraph(comment='Connection Graph', engine='fdp')

    # 添加模块节点
    def add_module_node(module_name):
        dot.node(module_name, module_name, shape='box')

    # 添加信号节点
    def add_signal_node(signal_name):
        dot.node(signal_name, signal_name, shape='ellipse')

    # 添加模块和信号边
    def add_edge(from_node, to_node, label):
        dot.edge(from_node, to_node, label)

    # 递归遍历模块连接
    def traverse_connection(module_name, connection_dict):
        for child_name, child_connection in connection_dict.items():
            for i in range(len(child_connection)):
                child_port, parent_port = child_connection[i]
                add_module_node(child_name)
                add_signal_node(parent_port)
                add_edge(parent_port, child_name, child_port)

                if child_name in module_dict.keys():
                    traverse_connection(child_name, module_dict[child_name])

    # 查找顶层模块及其连接
    if top_module_name in module_dict.keys():
        connection_dict = {}
        for output_port, input_port in module_dict[top_module_name]['outputs']:
            child_name = input_port.split('.')[0]
            child_port = input_port.split('.')[1]
            if child_name not in connection_dict.keys():
                connection_dict[child_name] = []
            connection_dict[child_name].append((child_port, output_port))

        traverse_connection(top_module_name, connection_dict)

    return dot


# 显示连接图界面
def show_graph_window(dot):
    top = Toplevel()
    top.title('Connection Graph')
    top.geometry("800x600")

    # 生成图像
    graph = dot.render(format='png', engine='dot')
    logging.debug(graph)
    pdf_image = PhotoImage(file=graph)

    # 显示图像
    img_label = Label(master=top, image=pdf_image)
    img_label.pack()

    return

# 主函数
def main():
    # 设置日志
    logging.basicConfig(filename='logfile.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
    logging.getLogger('').addHandler(console)

    logging.debug('Program Start')


    root = Tk()
    root.title('Verilog Tools')
    root.geometry("400x300")

    # 文件选择标签
    file_label = Label(master=root, text="Please Select Verilog File:")
    file_label.pack()

    # 文件选择框
    file_entry = Entry(master=root, width=40)
    file_entry.pack()

    # 选择文件按钮
    def browse_file():
        file_path = filedialog.askopenfilename()
        file_entry.delete(0, END)
        file_entry.insert(0, file_path)
    browse_button = Button(master=root, text="Browse", command=browse_file)
    browse_button.pack()

    # 显示连接图按钮
    def show_graph():
        file_path = file_entry.get()
        logging.debug(f"file_path={file_path}")
        top_module_name = re.search('(\w+).v',file_path).group(1)
        logging.debug(f"top_module_name={top_module_name}")

        module_dict, signal_dict = read_verilog_file(file_path)
        dot = generate_connection_graph(top_module_name, module_dict)
        show_graph_window(dot)
    graph_button = Button(master=root, text="Show Connection Graph", command=show_graph)
    graph_button.pack()

    root.mainloop()

if __name__ == '__main__':
    main()

