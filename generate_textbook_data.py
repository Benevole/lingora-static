#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据目录结构生成教材JSON数据脚本
为每个第一层级目录生成单独的JSON文件
使用方法: python3 generate_textbook_data.py
"""

import os
import json
import urllib.parse
import re

def generate_textbook_data():
    """生成教材JSON数据"""
    
    def extract_number(name):
        """从名称中提取数字，用于排序"""
        # 匹配文件名开头的数字（如：1、25、100等）
        # 先尝试匹配 "数字、" 格式
        match = re.match(r'^(\d+)、', name)
        if match:
            return int(match.group(1))
        
        # 如果没有"、"符号，尝试匹配开头的数字
        match = re.match(r'^(\d+)', name)
        if match:
            return int(match.group(1))
        
        # 处理Unit格式：Unit1, Unit2, Unit3...
        match = re.match(r'^Unit(\d+)', name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # 处理Phonics Lesson格式：Phonics Lesson 37 wr&kn.pdf
        match = re.search(r'Phonics Lesson (\d+)', name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # 处理phonics格式：phonics2_lesson19.pdf
        match = re.search(r'lesson(\d+)', name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # 处理Unit-Lesson格式：U1L1, U2L16, U5L62 Adventure.pdf
        match = re.search(r'U(\d+)L(\d+)', name, re.IGNORECASE)
        if match:
            unit = int(match.group(1))
            lesson = int(match.group(2))
            # 将Unit和Lesson组合成一个数字进行排序
            # 例如：U1L1 -> 1001, U2L16 -> 2016, U5L62 -> 5062
            return unit * 1000 + lesson
        
        # 处理西游记格式：西游记001_The Monkey.pdf
        match = re.search(r'西游记(\d+)', name)
        if match:
            return int(match.group(1))
        
        # 处理小猪佩奇格式：S1-01_Muddy_Puddles01.pdf
        match = re.search(r'S1-(\d+)', name)
        if match:
            return int(match.group(1))
        
        # 处理少儿版定主题自由交谈II unit复习格式：少儿版定主题自由交谈 II unit1复习.pdf
        match = re.search(r'少儿版定主题自由交谈 II?I? unit(\d+)复习\.pdf', name)
        if match:
            unit_num = int(match.group(1))
            # unit复习文件排在前面，使用较小的数字
            return unit_num
        
        # 处理少儿版定主题自由交谈II格式：少儿版定主题自由交谈 II 50.pdf 或 少儿版定主题自由交谈 Ⅱ 14.pdf
        match = re.search(r'少儿版定主题自由交谈 [II]+ (\d+)', name)
        if match:
            # 数字文件排在unit复习文件后面，使用1000+数字
            return 1000 + int(match.group(1))
        
        # 如果没有数字，返回一个很大的数字，排在最后
        return 999999
    
    def traverse_directory(path, parent_code='0', level=1):
        """递归遍历目录，生成JSON数据"""
        items = []
        
        try:
            # 获取目录下的所有文件和文件夹
            entries = os.listdir(path)
        except PermissionError:
            return items
        
        # 过滤掉隐藏文件和.git目录
        entries = [entry for entry in entries if not entry.startswith('.') and entry != '.git']
        
        # 分离目录和文件
        dirs = []
        files = []
        
        for entry in entries:
            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path):
                dirs.append(entry)
            elif entry.lower().endswith('.pdf'):
                files.append(entry)
        
        # 按数字排序（提取名称开头的数字）
        dirs.sort(key=extract_number)
        files.sort(key=extract_number)
        
        # 处理目录
        for i, entry in enumerate(dirs, 1):
            entry_path = os.path.join(path, entry)
            
            # 生成code
            code = str(i) if level == 1 else f"{parent_code}-{i}"
            
            # 目录项
            items.append({
                'code': code,
                'parentCode': parent_code,
                'type': 'TEXTBOOK',
                'name': entry,
                'link': None
            })
            
            # 递归处理子目录
            sub_items = traverse_directory(entry_path, code, level + 1)
            items.extend(sub_items)
        
        # 处理PDF文件
        for i, entry in enumerate(files, len(dirs) + 1):
            entry_path = os.path.join(path, entry)
            relative_path = os.path.relpath(entry_path, '.')
            
            # 生成code
            code = str(i) if level == 1 else f"{parent_code}-{i}"
            
            # PDF文件项
            encoded_path = urllib.parse.quote(relative_path, safe='')
            items.append({
                'code': code,
                'parentCode': parent_code,
                'type': 'TEXTBOOK',
                'name': entry,
                'link': f"http://pdf.lingora.cn/{encoded_path}"
            })
        
        return items
    
    def get_first_level_directories():
        """获取第一层级目录"""
        entries = [e for e in os.listdir('.') if not e.startswith('.') and e != '.git' and os.path.isdir(e)]
        # 第一层级目录按数字排序
        entries.sort(key=extract_number)
        return entries
    
    print("正在按第一层级分类生成教材JSON数据...")
    print("注意：将按数字顺序排序，确保1排在100前面")
    
    # 获取第一层级目录
    first_level_dirs = get_first_level_directories()
    print(f"发现 {len(first_level_dirs)} 个第一层级目录:")
    
    total_files = 0
    
    for i, dir_name in enumerate(first_level_dirs, 1):
        print(f"\n处理第 {i} 个目录: {dir_name}")
        
        # 为每个第一层级目录生成数据
        data = traverse_directory(dir_name, str(i), 2)  # 从第二层开始，parent_code为当前目录的code
        
        # 添加第一层级目录本身
        first_level_item = {
            'code': str(i),
            'parentCode': '0',
            'type': 'TEXTBOOK',
            'name': dir_name,
            'link': None
        }
        data.insert(0, first_level_item)
        
        # 生成文件名
        safe_name = dir_name.replace('/', '_').replace('\\', '_')
        filename = f"textbook_{i}_{safe_name}.json"
        
        # 保存到文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 统计信息
        pdf_count = sum(1 for item in data if item['link'])
        dir_count = sum(1 for item in data if not item['link'])
        
        print(f"  ✅ 生成文件: {filename}")
        print(f"  📁 目录数量: {dir_count}")
        print(f"  📄 PDF文件数量: {pdf_count}")
        print(f"  📊 总记录数: {len(data)}")
        
        total_files += len(data)
    
    print(f"\n🎉 所有文件生成完成！")
    print(f"📊 总共生成 {len(first_level_dirs)} 个JSON文件")
    print(f"📈 总记录数: {total_files}")

if __name__ == "__main__":
    generate_textbook_data() 