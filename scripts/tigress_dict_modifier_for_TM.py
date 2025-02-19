# 半成品, 请勿使用!!!!


# 本脚本用于直接将tigress词库的编码修改为TM词库的编码,并输出到指定路径.
# 编码的修改完全适配了0--TigerMatrix.schema.yaml的拼写运算规则.
# 使用方式：
# 1. 在脚本中，修改read_file_list为需要处理的文件列表，write_file_path为想要输出的字典路径
# 2. 运行脚本
# 3. 处理完成后，记得将涉及到该字典的方案，在xxx.dict.yaml中的路径替换为 write_file_path 路径.
# =========================
import re  # 导入正则表达式模块
from pathlib import Path  # 导入路径操作模块

class RimeOperations:
    def __init__(self):
        self.operations = {
            "xlit": self.transliteration,  # 字母转换
            "xform": self.transformation,  # 字符转换
            "erase": self.erasion,  # 删除匹配的字符串
            "derive": self.derivation,  # 派生新字符串
            "fuzz": self.fuzzing,  # 模糊匹配
            "abbrev": self.abbreviation  # 缩写
        }

    def apply_operations(self, input_string: str, operations: list[str]) -> str:
        # 应用一系列操作到输入字符串
        result: str = input_string
        for op in operations:
            op_type, params = self.parse_operation(op)  # 解析操作
            if op_type in self.operations:
                result = self.operations[op_type](result, *params)  # 执行操作
                # print('result:', result, "\nend of result")
        return result

    def parse_operation(self, operation: str) -> tuple[str, list[str]]:
        # 解析操作字符串，返回操作类型和参数
        if "|" in operation:
            parts = operation.split("|")
            print('parts:', parts, "\nend of parts")
            op_type: str = parts[0]
            params: list[str] = parts[1:-1]
        elif "/" in operation:
            parts = operation.split("/")
            print('parts:', parts, "\nend of parts")
            op_type: str = parts[0]
            params: list[str] = parts[1:-1]
        return op_type, params

    def transliteration(self, input_string: str, left_alphabet: str, right_alphabet: str) -> str:
        # 字母转换
        # print(input_string)
        trans_dict = str.maketrans(left_alphabet, right_alphabet)
        return input_string.translate(trans_dict)

    def transformation(self, input_string: str, pattern: str, replacement: str) -> str:
        # 字符转换
        return re.sub(pattern, replacement, input_string)

    def erasion(self, input_string: str, pattern: str) -> str:
        # 删除匹配的字符串
        if re.fullmatch(pattern, input_string):
            return None
        return input_string

    def derivation(self, input_string: str, pattern: str, replacement: str) -> list[str]:
        # 派生新字符串
        new_spelling = re.sub(pattern, replacement, input_string)
        return [input_string, new_spelling] if new_spelling != input_string else [input_string]

    def fuzzing(self, input_string: str, pattern: str, replacement: str) -> dict[str, str]:
        # 模糊匹配
        new_spelling = re.sub(pattern, replacement, input_string)
        return {"spelling": input_string, "fuzzy": new_spelling} if new_spelling != input_string else {"spelling": input_string}

    def abbreviation(self, input_string: str, pattern: str, replacement: str) -> dict[str, str]:
        # 缩写
        new_spelling = re.sub(pattern, replacement, input_string)
        return {"spelling": input_string, "abbrev": new_spelling} if new_spelling != input_string else {"spelling": input_string}


# 示例用法
if __name__ == "__main__":
    operations = [
    r"xform|^.*?;.*?;.*?;.*?;(.+?);(.+?);.*$|$1_$2|",
    r"derive|^.+?_([a-z][a-z]).*$|$1|",
    r"abbrev|^.+?_([a-z][a-z][a-z][a-z])$|$1|",
    r"derive|^.+?_([a-z][a-z][a-z][a-z])$|$1;|",
    r"abbrev|^([a-z][a-z][a-z])_.*$|$1|",
    r"derive|^([a-z][a-z][a-z])_.*$|$1;|",
    r"derive|^([a-z][a-z])_.*$|$1;|",
    r"derive|^([a-z])_.*$|$1|",
    r"derive|^([a-z])_.*$|$1;|",
    r"erase/^(.+)_(.+)$/",
    r"xlit/abcdefghijklmnopqrstuvwxyz/ABCDEFGHIJKLMNOPQRSTUVWXYZ/",
    r"xform/Q/q1/",
    r"xform/W/q2/",
    r"xform/A/a1/",
    r"xform/B/a2/",
    r"xform/C/a3/",
    r"xform/D/d1/",
    r"xform/E/d2/",
    r"xform/F/d3/",
    r"xform/G/g1/",
    r"xform/H/g2/",
    r"xform/I/g3/",
    r"xform/J/j1/",
    r"xform/K/j2/",
    r"xform/L/j3/",
    r"xform/M/m1/",
    r"xform/N/m2/",
    r"xform/O/m3/",
    r"xform/P/p1/",
    r"xform/R/p2/",
    r"xform/S/p3/",
    r"xform/T/t1/",
    r"xform/U/t2/",
    r"xform/V/t3/",
    r"xform/X/x1/",
    r"xform/Y/x2/",
    r"xform/Z/x3/",
    r"xform/([a-z])([1-3])([a-z])([1-3])([a-z])([1-3])([a-z])([1-3])/$1$3$2$4$5$7$6$8/",
    r"xform/([a-z]+)11/$1q/",
    r"xform/([a-z]+)12/$1a/",
    r"xform/([a-z]+)13/$1d/",
    r"xform/([a-z]+)21/$1g/",
    r"xform/([a-z]+)22/$1j/",
    r"xform/([a-z]+)23/$1m/",
    r"xform/([a-z]+)31/$1p/",
    r"xform/([a-z]+)32/$1t/",
    r"xform/([a-z]+)33/$1x/",
    r"xform/([a-z])([1-3])([a-z])([1-3])([a-z])([1-3])/$1$3$2$4$5$6/",
    r"xform/([a-z]+)11/$1q/",
    r"xform/([a-z]+)12/$1a/",
    r"xform/([a-z]+)13/$1d/",
    r"xform/([a-z]+)21/$1g/",
    r"xform/([a-z]+)22/$1j/",
    r"xform/([a-z]+)23/$1m/",
    r"xform/([a-z]+)31/$1p/",
    r"xform/([a-z]+)32/$1t/",
    r"xform/([a-z]+)33/$1x/",
    r"xform/([a-z][a-z][a-z][a-z])1/$1斜/",
    r"xform/([a-z][a-z][a-z][a-z])2/$1*/",
    r"xform/([a-z][a-z][a-z][a-z])3/$1`/",
    r"xform/([a-z])([1-3])([a-z])([1-3]);/$1$3$2$4;/",
    r"xform/([a-z]+)11/$1q/",
    r"xform/([a-z]+)12/$1a/",
    r"xform/([a-z]+)13/$1d/",
    r"xform/([a-z]+)21/$1g/",
    r"xform/([a-z]+)22/$1j/",
    r"xform/([a-z]+)23/$1m/",
    r"xform/([a-z]+)31/$1p/",
    r"xform/([a-z]+)32/$1t/",
    r"xform/([a-z]+)33/$1x/",
    r"xform/([a-z])([1-3])([a-z])([1-3])/$1$3$2$4/",
    r"xform/([a-z]+)11/$1q/",
    r"xform/([a-z]+)12/$1a/",
    r"xform/([a-z]+)13/$1d/",
    r"xform/([a-z]+)21/$1g/",
    r"xform/([a-z]+)22/$1j/",
    r"xform/([a-z]+)23/$1m/",
    r"xform/([a-z]+)31/$1p/",
    r"xform/([a-z]+)32/$1t/",
    r"xform/([a-z]+)33/$1x/",
    r"xform/([a-z])1/$1斜斜/",
    r"xform/([a-z])2/$1**/",
    r"xform/([a-z])3/$1``/",
    r"derive/([a-z])[*`斜][*`斜]/$1/",
    r"xlit/qadgjmptx/1@#456789/",
    ]

    rime_operations = RimeOperations()
    input_string = "abcd"3
    result = rime_operations.apply_operations(input_string, operations)
    print(result)

    # # 读取文件内容
    # def read_file(file_path):
    #     with open(file_path, 'r', encoding='utf-8') as file:
    #         return file.readlines()

    # # 写入文件内容
    # def write_file(file_path, content):
    #     with open(file_path, 'w', encoding='utf-8') as file:
    #         file.writelines(content)

    # # 替换函数
    # def replace_in_file(read_file_list: list, write_file_path: str, operations: list[str]):
    #     # 读取文件所有内容
    #     all_lines = []
    #     for file_path in read_file_list:
    #         all_lines.extend(read_file(file_path))
    #     # 替换 pattern
    #     all_lines = [ operator(line) for line in all_lines]
        
    #     # 写入新文件
    #     write_file(write_file_path, all_lines)

    # read_file_list = [Path("tiger_pack", "tigress_ci.dict.yaml"), ]
    # write_file_path = Path('0--core', 'rays_tigress_ci.dict.yaml')
    # # 调用替换函数
    # replace_in_file(read_file_list, write_file_path)
    # print(f"文件已成功写入到 {write_file_path}")