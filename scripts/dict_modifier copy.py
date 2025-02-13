import re
from pathlib import Path
import logging

# 初始化日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def replace_pattern_in_file(read_file_path: Path, write_file_path: Path, pattern: str, replacement: str):
    """
    在指定文件中替换所有匹配正则表达式模式的字符串。
    """
    try:
        with open(read_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        logging.error(f"文件 {read_file_path} 不存在。")
        return
    except Exception as e:
        logging.error(f"读取文件 {read_file_path} 时发生错误：{e}")
        return

    if not write_file_path.exists():
        write_file_path.touch()

    with open(write_file_path, 'a', encoding='utf-8') as file:
        for line in lines:
            if re.search(pattern, line):
                new_line = re.sub(pattern, replacement, line)
                file.write(new_line)
            else:
                file.write(line)
    logging.info(f"替换完成。已将文件写入 {write_file_path}。")

def modify_1code_characters(read_file_list: list[Path], write_file_path: Path, characters: dict):
    """
    替换一码单字在词中的编码部分为"一码+;"的形式。
    """
    for file in read_file_list:
        for key, value in characters.items():
            pattern_二字词首 = rf"^{key}[^\t]\t[0-9]+\t{value}[a-z][a-z]$"
            pattern_二字词末 = rf"^[^\t]{key}\t[0-9]+\t[a-z][a-z]{value}$"
            pattern_三字词末 = rf"^[^\t]{2}{key}\t[0-9]+\t[a-z][a-z]{value}$"
            replacement = value[0] + ';'
            replace_pattern_in_file(file, write_file_path, pattern_二字词首, replacement)
            replace_pattern_in_file(file, write_file_path, pattern_二字词末, replacement)
            replace_pattern_in_file(file, write_file_path, pattern_三字词末, replacement)

    logging.info("二字词首、二字词末、三字词末的替换完成。")

if __name__ == "__main__":
    characters = {
        '都': 'qo', '得': 'wo', '也': 'ey', '了': 'rl', '我': 'tu', 
        '到': 'yp', '的': 'un', '为': 'is', '是': 'ot', '行': 'px', 
        '来': 'ah', '说': 'sh', '中': 'dg', '一': 'fi', '就': 'gy', 
        '道': 'ho', '人': 'jr', '能': 'kv', '而': 'le', 
        '可': 'zk', '和': 'xd', '不': 'cb', '要': 'vb', '如': 'bd', 
        '在': 'ng', '大': 'md'
    }
    read_file_list = [Path("tiger_pack", "tigress_ci.dict.yaml")]
    write_file_path = Path('0--core', 'rays_tigress_ci.dict.yaml')
    modify_1code_characters(read_file_list, write_file_path, characters)
import re
from pathlib import Path
import logging

# 初始化日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def replace_pattern_in_file(read_file_path: Path, write_file_path: Path, pattern: str, replacement: str):
    """
    在指定文件中替换所有匹配正则表达式模式的字符串。
    """
    try:
        with open(read_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        logging.error(f"文件 {read_file_path} 不存在。")
        return
    except Exception as e:
        logging.error(f"读取文件 {read_file_path} 时发生错误：{e}")
        return

    if not write_file_path.exists():
        write_file_path.touch()

    with open(write_file_path, 'a', encoding='utf-8') as file:
        for line in lines:
            if re.search(pattern, line):
                new_line = re.sub(pattern, replacement, line)
                file.write(new_line)
            else:
                file.write(line)
    logging.info(f"替换完成。已将文件写入 {write_file_path}。")

def modify_1code_characters(read_file_list: list[Path], write_file_path: Path, characters: dict):
    """
    替换一码单字在词中的编码部分为"一码+;"的形式。
    """
    for file in read_file_list:
        for key, value in characters.items():
            pattern_二字词首 = rf"^{key}[^\t]\t[0-9]+\t{value}[a-z][a-z]$"
            pattern_二字词末 = rf"^[^\t]{key}\t[0-9]+\t[a-z][a-z]{value}$"
            pattern_三字词末 = rf"^[^\t]{2}{key}\t[0-9]+\t[a-z][a-z]{value}$"
            replacement = value[0] + ';'
            replace_pattern_in_file(file, write_file_path, pattern_二字词首, replacement)
            replace_pattern_in_file(file, write_file_path, pattern_二字词末, replacement)
            replace_pattern_in_file(file, write_file_path, pattern_三字词末, replacement)

    logging.info("二字词首、二字词末、三字词末的替换完成。")

if __name__ == "__main__":
    characters = {
        '都': 'qo', '得': 'wo', '也': 'ey', '了': 'rl', '我': 'tu', 
        '到': 'yp', '的': 'un', '为': 'is', '是': 'ot', '行': 'px', 
        '来': 'ah', '说': 'sh', '中': 'dg', '一': 'fi', '就': 'gy', 
        '道': 'ho', '人': 'jr', '能': 'kv', '而': 'le', 
        '可': 'zk', '和': 'xd', '不': 'cb', '要': 'vb', '如': 'bd', 
        '在': 'ng', '大': 'md'
    }
    read_file_list = [Path("tiger_pack", "tigress_ci.dict.yaml")]
    write_file_path = Path('0--core', 'rays_tigress_ci.dict.yaml')
    modify_1code_characters(read_file_list, write_file_path, characters)
