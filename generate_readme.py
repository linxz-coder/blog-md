import os
import yaml

def extract_info_from_md(md_file):
    with open(md_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 提取 front matter 部分
    if lines[0].strip() == "---":
        front_matter = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            front_matter.append(line)
        front_matter = yaml.safe_load(''.join(front_matter))
        return front_matter
    return None

def generate_readme(md_files):
    readme_content = "# 项目文档目录\n\n"
    for md_file in md_files:
        info = extract_info_from_md(md_file)
        if info:
            title = info.get('title', '无标题')
            url = info.get('url', '#')
            readme_content += f"- [{title}]({url})\n"
    return readme_content

def main():
    md_files = [f for f in os.listdir('.') if f.endswith('.md') and f != 'README.md']
    readme_content = generate_readme(md_files)
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
