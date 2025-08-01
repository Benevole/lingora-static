#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为阿卡索会话天地生成JSON数据脚本
专门处理"9阿卡索会话天地"目录结构
使用方法: python3 generate_akaso_data.py
"""

import os
import json
import urllib.parse
import re

def generate_akaso_data():
    """生成阿卡索会话天地JSON数据"""
    
    def extract_number(name):
        """从名称中提取数字，用于排序"""
        # 处理阿卡索特有的命名格式：U1L1.pdf, U9L36.pdf
        
        # 处理UxLy格式：U1L1, U9L36, U16L65
        match = re.search(r'U(\d+)L(\d+)', name, re.IGNORECASE)
        if match:
            unit = int(match.group(1))
            lesson = int(match.group(2))
            # 将Unit和Lesson组合成一个数字进行排序
            # 例如：U1L1 -> 1001, U9L36 -> 9036, U16L65 -> 1665
            return unit * 1000 + lesson
        
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
    
    print("正在生成阿卡索会话天地JSON数据...")
    print("处理目录：9阿卡索会话天地")
    
    # 为阿卡索目录生成数据
    akaso_path = "9阿卡索会话天地"
    
    if not os.path.exists(akaso_path):
        print(f"❌ 目录 {akaso_path} 不存在")
        return
    
    # 生成数据
    data = traverse_directory(akaso_path, "1", 2)  # 从第二层开始，parent_code为1
    
    # 添加第一层级目录本身
    first_level_item = {
        'code': "1",
        'parentCode': '0',
        'type': 'TEXTBOOK',
        'name': akaso_path,
        'link': None
    }
    data.insert(0, first_level_item)
    
    # 生成文件名
    filename = "textbook_9_阿卡索会话天地.json"
    
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
    
    print(f"\n🎉 阿卡索会话天地JSON数据生成完成！")

if __name__ == "__main__":
    generate_akaso_data() 