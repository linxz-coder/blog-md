import os
import re
import shutil
import subprocess
import filecmp
from pathlib import Path
from datetime import datetime

def run_command(command):
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"命令执行成功: {command}")
        print(f"输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {command}")
        print(f"错误信息: {e.stderr}")
        return False

def add_title_and_date(input_path, output_path):
    print(f"处理文件: {input_path}")
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
date = {datetime.now().strftime('%Y-%m-%d')}
+++

"""
            # 替换原有的头部信息
            new_content = re.sub(pattern, new_header, content, flags=re.DOTALL)
        else:
            # 如果没有找到头部信息，在文件开头添加新的头部信息
            title = os.path.splitext(os.path.basename(input_path))[0]
            new_header = f"""+++
title = "{title}"
date = {datetime.now().strftime('%Y-%m-%d')}
+++

"""
            new_content = new_header + content

        # 写入新文件
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"文件处理完成并保存到: {output_path}")

    except Exception as e:
        print(f"处理文件 {input_path} 时出错: {str(e)}")

def process_markdown_files(source_dir, target_dir, zola_content_dir):
    # 确保目标目录存在
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    
    # 遍历源目录中的所有.md文件
    for file in Path(source_dir).glob('*.md'):
        if file.name != 'README.md':
            output_path = Path(target_dir) / file.name
            
            # 处理文件并保存到post_for_zola目录
            add_title_and_date(str(file), str(output_path))
            
            # 检查zola-basic的content/blog目录中是否已存在同名文件
            zola_file_path = Path(zola_content_dir) / file.name
            if zola_file_path.exists():
                # 如果文件内容相同，跳过
                if filecmp.cmp(str(output_path), str(zola_file_path)):
                    print(f"文件 {file.name} 在 zola-basic 中已存在且内容相同，跳过")
                    continue
                
                # 如果文件内容不同，询问用户是否覆盖
                user_input = input(f"文件 {file.name} 在 zola-basic 中已存在且内容不同。是否覆盖? (y/n): ")
                if user_input.lower() != 'y':
                    print(f"跳过文件 {file.name}")
                    continue
            
            # 复制处理后的文件到zola-basic的content/blog目录
            shutil.copy2(output_path, zola_content_dir)
            print(f"文件 {file.name} 已复制到 zola-basic")

def git_operations(repo_path):
    os.chdir(repo_path)
    
    # 执行 git pull
    if not run_command("git pull"):
        print(f"在 {repo_path} 执行 git pull 失败，跳过后续 git 操作")
        return
    
    # 如果 git pull 成功，继续执行其他 git 操作
    run_command("git add .")
    run_command('git commit -m "new post"')
    run_command("git push")

def main():
    # 设置路径
    blog_md_path = "/Users/linxiaozhong/Desktop/test-automation/blog-md"
    post_for_zola_path = "/Users/linxiaozhong/Desktop/test-automation/post_for_zola"
    zola_content_path = "/Users/linxiaozhong/Desktop/test-automation/zola-basic/content/blog"
    
    # 处理Markdown文件
    process_markdown_files(blog_md_path, post_for_zola_path, zola_content_path)
    
    # 执行Git操作
    git_operations(blog_md_path)
    git_operations(zola_content_path)

if __name__ == "__main__":
    main()