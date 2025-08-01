#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为新概念教材生成JSON数据脚本
专门处理"8新概念"目录结构
使用方法: python3 generate_new_concept_data.py
"""

import os
import json
import urllib.parse
import re

def generate_new_concept_data():
    """生成新概念教材JSON数据"""
    
    def extract_number(name):
        """从名称中提取数字，用于排序"""
        # 处理新概念特有的命名格式
        
        # 处理1册上的格式：1.pdf, 2.pdf, 10.pdf, 78final test.pdf
        match = re.match(r'^(\d+)', name)
        if match:
            return int(match.group(1))
        
        # 处理1册下的格式：L1, L2, L10, L80 Final speaking practice
        match = re.match(r'^L(\d+)', name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # 处理2册上的格式：L1, L2, L10, L100 REVIEW 4
        match = re.match(r'^L(\d+)', name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # 处理2册下的格式：001, 002, 100 Revision 4
        match = re.match(r'^(\d+)', name)
        if match:
            return int(match.group(1))
        
        # 处理3册下的格式：L1.pdf, L2.pdf, L3.pdf
        match = re.match(r'^L(\d+)', name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
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
    
    print("正在生成新概念教材JSON数据...")
    print("处理目录：8新概念")
    
    # 为新概念目录生成数据
    new_concept_path = "8新概念"
    
    if not os.path.exists(new_concept_path):
        print(f"❌ 目录 {new_concept_path} 不存在")
        return
    
    # 生成数据
    data = traverse_directory(new_concept_path, "1", 2)  # 从第二层开始，parent_code为1
    
    # 添加第一层级目录本身
    first_level_item = {
        'code': "1",
        'parentCode': '0',
        'type': 'TEXTBOOK',
        'name': new_concept_path,
        'link': None
    }
    data.insert(0, first_level_item)
    
    # 生成文件名
    filename = "textbook_8_新概念.json"
    
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
    
    # 显示目录结构统计
    print(f"\n📋 目录结构统计:")
    for item in data:
        if not item['link']:  # 目录
            indent = "  " * (len(item['code'].split('-')) - 1)
            print(f"{indent}📁 {item['name']}")
    
    print(f"\n🎉 新概念教材JSON数据生成完成！")

if __name__ == "__main__":
    generate_new_concept_data() 