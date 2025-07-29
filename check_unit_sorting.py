#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门检查3国际认证少年英语高级的排序
"""

import json
import re

def check_unit_sorting():
    """检查3国际认证少年英语高级的排序"""
    
    def extract_number(name):
        """从名称中提取数字，用于排序"""
        # 处理Unit格式：Unit1, Unit2, Unit3...
        match = re.match(r'^Unit(\d+)', name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # 处理Unit-Lesson格式：U1L1, U2L16, U5L62 Adventure.pdf
        match = re.search(r'U(\d+)L(\d+)', name, re.IGNORECASE)
        if match:
            unit = int(match.group(1))
            lesson = int(match.group(2))
            return unit * 1000 + lesson
        
        return 999999
    
    print("检查3国际认证少年英语高级的排序")
    print("=" * 60)
    
    try:
        with open('textbook_3_3国际认证少年英语高级.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ 文件不存在: textbook_3_3国际认证少年英语高级.json")
        return
    
    print(f"📊 总记录数: {len(data)}")
    
    # 显示所有记录
    print(f"\n📋 所有记录:")
    print("-" * 80)
    
    for i, item in enumerate(data, 1):
        num = extract_number(item['name'])
        link_info = "📄" if item['link'] else "📁"
        print(f"{i:3d}. {link_info} code: {item['code']:8s} | parent: {item['parentCode']:4s} | num: {num:4d} | {item['name']}")
    
    # 检查二级目录（Unit）的排序
    print(f"\n🔍 检查二级目录（Unit）排序:")
    print("-" * 40)
    
    unit_dirs = [item for item in data if item['parentCode'] == '3' and item['link'] is None]
    unit_dirs.sort(key=lambda x: extract_number(x['name']))
    
    for i, item in enumerate(unit_dirs, 1):
        num = extract_number(item['name'])
        print(f"{i}. {item['name']} (排序数字: {num})")
    
    # 检查每个Unit下的文件排序
    for unit_dir in unit_dirs:
        unit_code = unit_dir['code']
        unit_name = unit_dir['name']
        
        print(f"\n🔍 检查 {unit_name} ({unit_code}) 下的文件排序:")
        print("-" * 50)
        
        unit_files = [item for item in data if item['parentCode'] == unit_code and item['link'] is not None]
        unit_files.sort(key=lambda x: extract_number(x['name']))
        
        for i, item in enumerate(unit_files[:10], 1):  # 只显示前10个
            num = extract_number(item['name'])
            print(f"{i:2d}. {item['name']} (排序数字: {num})")
        
        if len(unit_files) > 10:
            print(f"   ... 还有 {len(unit_files) - 10} 个文件")
    
    # 检查整体排序是否正确
    print(f"\n✅ 排序检查结果:")
    print("-" * 30)
    
    # 检查二级目录排序
    unit_numbers = [extract_number(item['name']) for item in unit_dirs]
    unit_sorted = all(unit_numbers[i] <= unit_numbers[i+1] for i in range(len(unit_numbers)-1))
    
    if unit_sorted:
        print("✅ 二级目录（Unit）排序正确")
    else:
        print("❌ 二级目录（Unit）排序错误")
        for i in range(len(unit_numbers)-1):
            if unit_numbers[i] > unit_numbers[i+1]:
                print(f"   {unit_dirs[i]['name']} ({unit_numbers[i]}) > {unit_dirs[i+1]['name']} ({unit_numbers[i+1]})")
    
    # 检查每个Unit下的文件排序
    all_files_sorted = True
    for unit_dir in unit_dirs:
        unit_code = unit_dir['code']
        unit_files = [item for item in data if item['parentCode'] == unit_code and item['link'] is not None]
        file_numbers = [extract_number(item['name']) for item in unit_files]
        
        if not all(file_numbers[i] <= file_numbers[i+1] for i in range(len(file_numbers)-1)):
            all_files_sorted = False
            print(f"❌ {unit_dir['name']} 下的文件排序错误")
            for i in range(len(file_numbers)-1):
                if file_numbers[i] > file_numbers[i+1]:
                    print(f"   {unit_files[i]['name']} ({file_numbers[i]}) > {unit_files[i+1]['name']} ({file_numbers[i+1]})")
                    break
    
    if all_files_sorted:
        print("✅ 所有Unit下的文件排序正确")

if __name__ == "__main__":
    check_unit_sorting() 