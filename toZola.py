import os
import re

def add_title_and_date(input_path, output_path):
    print(f"Processing file: {input_path}")
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 使用正则表达式匹配头部信息
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)

        if match:
            header_content = match.group(1)
            
            # 尝试从头部信息中提取标题
            title_match = re.search(r'title:\s*(.*)', header_content)
            if title_match:
                title = title_match.group(1).strip()
            else:
                # 如果没有找到标题，使用文件名作为标题
                title = os.path.splitext(os.path.basename(input_path))[0]

            # 创建新的头部信息，包含标题和日期
            new_header = f"""+++
title = "{title}"
date = 2024-09-21
+++

"""
            # 替换原有的头部信息
            new_content = re.sub(pattern, new_header, content, flags=re.DOTALL)
        else:
            # 如果没有找到头部信息，在文件开头添加新的头部信息
            title = os.path.splitext(os.path.basename(input_path))[0]
            new_header = f"""+++
title = "{title}"
date = 2024-09-21
+++

"""
            new_content = new_header + content

        # 写入新文件
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"File processed and saved to: {output_path}")
        
        # 打印文件的前几行以验证更改
        print("First few lines of the processed file:")
        print("\n".join(new_content.split("\n")[:8]))  # 显示前8行以确保看到 +++, 标题和日期
    except Exception as e:
        print(f"Error processing file {input_path}: {str(e)}")

def process_directory(input_dir, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            add_title_and_date(input_path, output_path)
            print(f"Processed: {filename}")

# 使用示例
input_directory = '/Users/linxiaozhong/Desktop/blog-copy'
output_directory = '/Users/linxiaozhong/Desktop/blog-for-zola'
process_directory(input_directory, output_directory)

print("Script execution completed.")