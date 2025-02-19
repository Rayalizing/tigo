# 本脚本用于将一码单字在词中的编码部分替换为一码+;的形式
# 考虑了不同的情况(完美适配了tigress_ci.dict.yaml)
# 使用方式：
# 1. 在脚本中，修改read_file_list为需要处理的文件列表，write_file_path为想要输出的字典路径
# 2. 运行脚本
# 3. 处理完成后，记得将涉及到该字典的方案，在xxx.dict.yaml中的路径替换为 write_file_path 路径.
# =========================
import re
from pathlib import Path

characters = {
    '都': 'qo', '得': 'wo', '也': 'ey', '了': 'rl', '我': 'tu', 
    '到': 'yp', '的': 'un', '为': 'is', '是': 'ot', '行': 'px', 
    '来': 'ah', '说': 'sh', '中': 'dg', '一': 'fi', '就': 'gy', 
    '道': 'ho', '人': 'jr', '能': 'kv', '而': 'le', 
    '可': 'zk', '和': 'xd', '不': 'cb', '要': 'vb', '如': 'bd', 
    '在': 'ng', '大': 'md',
}

# 定义正则表达式模式
# 两字词首字为 characters 中的 key 时:
pattern_1 = r"(^{key}[^\t]\t[0-9]+\t){value}([a-z][a-z]$)"
# 两字词尾字为 characters 中的 key 时:
pattern_2 = r"(^[^\t]{key}\t[0-9]+\t[a-z][a-z]){value}($)"
# 三字词尾字为 character 中的 key 时:
pattern_3 = r"(^[^\t][^\t]{key}\t[0-9]+\t[a-z][a-z]){value}($)" 
# 或者: pattern_3 = r"^([^\t]{{2}}{key}\t[0-9]+\t[a-z][a-z]){value}$"  # 修正了 {2} 在python中可能会被格式化的问题.


# 读取文件内容
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

# 写入文件内容
def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(content)

# 替换函数
def replace_in_file(read_file_list, write_file_path, characters):
    # 读取文件所有内容
    all_lines = []
    for file_path in read_file_list:
        all_lines.extend(read_file(file_path))
    
    # 遍历 characters 字典，进行替换
    for key, value in characters.items():
        new_value = value[0] + ';'
        replacement = r'\1' + new_value + r'\2'
        # 替换 pattern_1
        pattern = pattern_1.format(key=re.escape(key), value=re.escape(value)) # 使用 re.escape() 函数对 key 和 value 进行转义，以防止正则表达式中的特殊字符被误解析。
        # new_lines = []
        # for line in all_lines:
            # new_line = re.sub(pattern, replacement, line)
            # new_lines.append(new_line)
        # all_lines = new_lines
        all_lines = [re.sub(pattern, replacement, line) for line in all_lines] # 这行代码和上面的代码功能相同,但是更简洁.
                    # re.sub 会生成一个新的字符串,其中符合pattern的line会被替换为 new_line, 其它部分保持不变.

        # 替换 pattern_2
        pattern = pattern_2.format(key=re.escape(key), value=re.escape(value))
        all_lines = [re.sub(pattern, replacement, line) for line in all_lines]
        
        # 替换 pattern_3
        pattern = pattern_3.format(key=re.escape(key), value=re.escape(value))
        all_lines = [re.sub(pattern, replacement, line) for line in all_lines]
    
    # 写入新文件
    write_file(write_file_path, all_lines)


read_file_list = [Path("tiger_pack", "tigress_ci.dict.yaml"), ]
write_file_path = Path('0--core', 'rays_tigress_ci.dict.yaml')

# 调用替换函数
replace_in_file(read_file_list, write_file_path, characters)

print(f"文件已成功写入到 {write_file_path}")