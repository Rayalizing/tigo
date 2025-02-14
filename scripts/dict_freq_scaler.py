## 本脚本一次性生成自DeepSeek-r1
##
def scale_frequencies_for_clean_file(input_file, output_file, new_min, new_max):
    # 读取文件并分割头部和数据
    headers = []
    data_lines = []
    with open(input_file, 'r', encoding='utf-8') as f:
        header_ended = False
        for line in f:
            stripped = line.strip()
            
            if not header_ended:
                headers.append(line)
                if stripped == '...':
                    header_ended = True
                continue
            
            if stripped and '\t' in line:
                data_lines.append(line.rstrip('\n'))
    
    # 提取词频数据
    frequencies = []
    processed = []
    for line in data_lines:
        parts = line.split('\t')
        if len(parts) < 3:
            continue
        
        try:
            freq = int(parts[1])
            frequencies.append(freq)
            processed.append(parts)
        except ValueError:
            continue
    
    if not frequencies:
        print("未找到有效词频数据")
        return
    
    # 计算缩放参数
    old_min = min(frequencies)
    old_max = max(frequencies)
    new_min = new_min
    new_max = new_max
    
    # 执行缩放计算
    scaled_data = []
    if old_min == old_max:
        scaled_value = new_min
        for parts in processed:
            parts[1] = str(scaled_value)
            scaled_data.append('\t'.join(parts))
    else:
        scale = (new_max - new_min) / (old_max - old_min)
        for parts in processed:
            original = int(parts[1])
            scaled = new_min + (original - old_min) * scale
            parts[1] = str(int(round(scaled)))
            scaled_data.append('\t'.join(parts))
    
    # 写入新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(headers)
        f.write('\n'.join(scaled_data))
        f.write('\n')

def scale_frequencies(input_file, output_file, new_min, new_max):
    # 读取文件并精确分割头部/数据
    headers = []
    data_lines = []
    with open(input_file, 'r', encoding='utf-8') as f:
        header_ended = False
        for line in f:
            # 保留原始换行符处理
            raw_line = line
            
            if not header_ended:
                headers.append(raw_line)
                if line.strip() == '...':
                    header_ended = True
                continue
            
            # 数据行处理逻辑
            stripped = line.lstrip(' ')  # 保留行首空格
            if stripped.startswith('#'):
                data_lines.append(raw_line)  # 保留注释原样
                continue
                
            if '\t' in line:
                data_lines.append(line.rstrip('\n'))  # 准备处理的数据行
            else:
                data_lines.append(raw_line)  # 保留非数据行原样

    # 提取有效词频数据
    frequencies = []
    processed = []
    valid_indices = []
    for idx, line in enumerate(data_lines):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue  # 跳过空行和注释
        
        parts = line.split('\t')
        if len(parts) < 3:
            continue  # 跳过列数不足的行
            
        try:
            freq = int(parts[1])
            frequencies.append(freq)
            processed.append(parts)
            valid_indices.append(idx)
        except (ValueError, IndexError):
            continue

    if not frequencies:
        print("未找到有效词频数据")
        return

    # 计算缩放参数
    old_min = min(frequencies)
    old_max = max(frequencies)
    new_min = new_min
    new_max = new_max

    # 执行缩放计算
    scaled_lines = data_lines.copy()
    if old_min == old_max:
        scaled_value = new_min
        for idx in valid_indices:
            parts = processed.pop(0)
            parts[1] = str(scaled_value)
            scaled_lines[idx] = '\t'.join(parts)
    else:
        scale = (new_max - new_min) / (old_max - old_min)
        for idx in valid_indices:
            parts = processed.pop(0)
            original = int(parts[1])
            scaled = new_min + (original - old_min) * scale
            parts[1] = str(int(round(scaled)))
            scaled_lines[idx] = '\t'.join(parts)

    # 写入新文件（保留原始换行符）
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        f.writelines(headers)
        f.write('\n'.join(scaled_lines))
        # 确保最后有换行
        if not scaled_lines[-1].endswith('\n'):
            f.write('\n')

if __name__ == "__main__":
    input_file = "0--core/rays_personal.dict.yaml"
    output_file = "0--core/rays_personal_scaled_for_tigo.dict.yaml"
    scale_frequencies(input_file, output_file, new_min=1, new_max=945)
    # 下面这个和上面二选一，它用于处理没有注释的干净文件，直接缩放词频，不保留注释，处理速度更快。
    # scale_frequencies_for_clean_file(input_file, output_file, new_min=1, new_max=945)
    print(f"词频已成功缩放并保存到 {output_file}")