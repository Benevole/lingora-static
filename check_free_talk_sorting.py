#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门检查7自由主题的排序
"""

import json
import re

def check_free_talk_sorting():
    """检查7自由主题的排序"""
    
    def extract_number(name):
        """从名称中提取数字，用于排序"""
        # 处理少儿版定主题自由交谈II格式：少儿版定主题自由交谈 II 50.pdf
        match = re.search(r'少儿版定主题自由交谈 II (\d+)\.pdf', name)
        if match:
            return int(match.group(1))
        
        # 处理少儿版定主题自由交谈II unit复习格式：少儿版定主题自由交谈 II unit1复习.pdf
        match = re.search(r'少儿版定主题自由交谈 II unit(\d+)复习\.pdf', name)
        if match:
            unit_num = int(match.group(1))
            # unit复习文件排在数字文件后面，使用1000+unit_num
            return 1000 + unit_num
        
        # 处理其他数字格式
        match = re.match(r'^(\d+)、', name)
        if match:
            return int(match.group(1))
        
        match = re.match(r'^(\d+)', name)
        if match:
            return int(match.group(1))
        
        return 999999
    
    print("检查7自由主题的排序")
    print("=" * 60)
    
    try:
        with open('textbook_7_7自由主题.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ 文件不存在: textbook_7_7自由主题.json")
        return
    
    print(f"📊 总记录数: {len(data)}")
    
    # 显示所有记录
    print(f"\n📋 所有记录:")
    print("-" * 80)
    
    for i, item in enumerate(data, 1):
        num = extract_number(item['name'])
        link_info = "📄" if item['link'] else "📁"
        print(f"{i:3d}. {link_info} code: {item['code']:8s} | parent: {item['parentCode']:4s} | num: {num:4d} | {item['name']}")
    
    # 检查二级目录的排序
    print(f"\n🔍 检查二级目录排序:")
    print("-" * 40)
    
    second_level_dirs = [item for item in data if item['parentCode'] == '7' and item['link'] is None]
    second_level_dirs.sort(key=lambda x: extract_number(x['name']))
    
    for i, item in enumerate(second_level_dirs, 1):
        num = extract_number(item['name'])
        print(f"{i}. {item['name']} (排序数字: {num})")
    
    # 检查每个二级目录下的文件排序
    for second_dir in second_level_dirs:
        dir_code = second_dir['code']
        dir_name = second_dir['name']
        
        print(f"\n🔍 检查 {dir_name} ({dir_code}) 下的文件排序:")
        print("-" * 60)
        
        dir_files = [item for item in data if item['parentCode'] == dir_code and item['link'] is not None]
        dir_files.sort(key=lambda x: extract_number(x['name']))
        
        for i, item in enumerate(dir_files, 1):
            num = extract_number(item['name'])
            print(f"{i:2d}. {item['name']} (排序数字: {num})")
    
    # 检查整体排序是否正确
    print(f"\n✅ 排序检查结果:")
    print("-" * 30)
    
    # 检查二级目录排序
    dir_numbers = [extract_number(item['name']) for item in second_level_dirs]
    dir_sorted = all(dir_numbers[i] <= dir_numbers[i+1] for i in range(len(dir_numbers)-1))
    
    if dir_sorted:
        print("✅ 二级目录排序正确")
    else:
        print("❌ 二级目录排序错误")
        for i in range(len(dir_numbers)-1):
            if dir_numbers[i] > dir_numbers[i+1]:
                print(f"   {second_level_dirs[i]['name']} ({dir_numbers[i]}) > {second_level_dirs[i+1]['name']} ({dir_numbers[i+1]})")
    
    # 检查每个二级目录下的文件排序
    all_files_sorted = True
    for second_dir in second_level_dirs:
        dir_code = second_dir['code']
        dir_files = [item for item in data if item['parentCode'] == dir_code and item['link'] is not None]
        file_numbers = [extract_number(item['name']) for item in dir_files]
        
        if not all(file_numbers[i] <= file_numbers[i+1] for i in range(len(file_numbers)-1)):
            all_files_sorted = False
            print(f"❌ {second_dir['name']} 下的文件排序错误")
            for i in range(len(file_numbers)-1):
                if file_numbers[i] > file_numbers[i+1]:
                    print(f"   {dir_files[i]['name']} ({file_numbers[i]}) > {dir_files[i+1]['name']} ({file_numbers[i+1]})")
                    break
    
    if all_files_sorted:
        print("✅ 所有二级目录下的文件排序正确")

if __name__ == "__main__":
    check_free_talk_sorting() 