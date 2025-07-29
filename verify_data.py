#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证生成的教材JSON数据
检查数据结构、排序和URL格式
使用方法: python3 verify_data.py
"""

import json
import os
import glob
import re

def verify_textbook_data():
    """验证教材JSON数据"""
    
    def extract_number(name):
        """从名称中提取数字，用于排序"""
        # 匹配文件名开头的数字（如：1、25、100等）
        match = re.match(r'^(\d+)、', name)
        if match:
            return int(match.group(1))
        
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
        
        match = re.search(r'lesson(\d+)', name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        match = re.search(r'U(\d+)L(\d+)', name, re.IGNORECASE)
        if match:
            unit = int(match.group(1))
            lesson = int(match.group(2))
            return unit * 1000 + lesson
        
        match = re.search(r'西游记(\d+)', name)
        if match:
            return int(match.group(1))
        
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
        
        return 999999
    
    print("正在验证教材JSON数据...")
    print("=" * 60)
    
    # 查找所有textbook_*.json文件
    json_files = glob.glob('textbook_*.json')
    
    if not json_files:
        print("❌ 未找到任何textbook_*.json文件")
        print("请先运行 generate_textbook_data.py 生成数据")
        return
    
    print(f"✅ 找到 {len(json_files)} 个JSON文件")
    
    total_records = 0
    total_pdfs = 0
    all_errors = 0
    
    for json_file in sorted(json_files):
        print(f"\n{'='*50}")
        print(f"验证文件: {json_file}")
        print(f"{'='*50}")
        
        # 读取JSON文件
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ JSON格式错误: {e}")
            all_errors += 1
            continue
        
        print(f"📊 记录数: {len(data)}")
        
        # 检查数据结构
        required_fields = ['code', 'parentCode', 'type', 'name', 'link']
        valid_types = ['TEXTBOOK']
        
        structure_errors = 0
        type_errors = 0
        
        for i, item in enumerate(data):
            # 检查必需字段
            for field in required_fields:
                if field not in item:
                    print(f"❌ 记录 {i+1}: 缺少字段 '{field}'")
                    structure_errors += 1
            
            # 检查type字段
            if 'type' in item and item['type'] not in valid_types:
                print(f"❌ 记录 {i+1}: type值无效 '{item['type']}'")
                type_errors += 1
        
        if structure_errors == 0 and type_errors == 0:
            print("✅ 数据结构检查通过")
        else:
            print(f"❌ 发现 {structure_errors + type_errors} 个结构错误")
            all_errors += structure_errors + type_errors
        
        # 检查层级关系
        code_map = {}
        parent_errors = 0
        
        # 建立code映射
        for item in data:
            code_map[item['code']] = item
        
        # 检查parentCode关系
        for item in data:
            parent_code = item['parentCode']
            if parent_code != '0' and parent_code not in code_map:
                print(f"❌ 记录 {item['code']}: parentCode '{parent_code}' 不存在")
                parent_errors += 1
        
        if parent_errors == 0:
            print("✅ 层级关系检查通过")
        else:
            print(f"❌ 发现 {parent_errors} 个层级关系错误")
            all_errors += parent_errors
        
        # 检查URL格式
        url_errors = 0
        pdf_count = 0
        
        for item in data:
            if item['link'] is not None:
                pdf_count += 1
                if not item['link'].startswith('http://pdf.lingora.cn/'):
                    print(f"❌ 记录 {item['code']}: URL格式错误 '{item['link']}'")
                    url_errors += 1
        
        if url_errors == 0:
            print("✅ URL格式检查通过")
        else:
            print(f"❌ 发现 {url_errors} 个URL格式错误")
            all_errors += url_errors
        
        print(f"📄 PDF文件数量: {pdf_count}")
        total_pdfs += pdf_count
        
        # 检查数字排序
        # 按parentCode分组检查排序
        parent_groups = {}
        for item in data:
            parent = item['parentCode']
            if parent not in parent_groups:
                parent_groups[parent] = []
            parent_groups[parent].append(item)
        
        sort_errors = 0
        
        for parent, items in parent_groups.items():
            # 检查name是否按数字顺序排序
            names = [item['name'] for item in items]
            numbers = [extract_number(name) for name in names]
            
            # 检查数字是否按升序排列
            is_sorted = all(numbers[i] <= numbers[i+1] for i in range(len(numbers)-1))
            
            if not is_sorted:
                print(f"❌ parentCode '{parent}': 数字排序不正确")
                # 显示前几个有问题的项目
                for i in range(len(numbers)-1):
                    if numbers[i] > numbers[i+1]:
                        print(f"   {names[i]} ({numbers[i]}) > {names[i+1]} ({numbers[i+1]})")
                        break
                sort_errors += 1
        
        if sort_errors == 0:
            print("✅ 数字排序检查通过")
        else:
            print(f"❌ 发现 {sort_errors} 个排序错误")
            all_errors += sort_errors
        
        # 显示前5个记录作为示例
        print(f"\n📋 前5个记录示例:")
        print("-" * 40)
        
        for i, item in enumerate(data[:5], 1):
            num = extract_number(item['name'])
            print(f"{i}. code: {item['code']:8s} | parent: {item['parentCode']:4s} | num: {num:4d} | name: {item['name'][:20]}...")
        
        total_records += len(data)
    
    # 总结
    print(f"\n{'='*60}")
    print("验证总结")
    print(f"{'='*60}")
    print(f"📁 验证文件数: {len(json_files)}")
    print(f"📊 总记录数: {total_records}")
    print(f"📄 总PDF文件数: {total_pdfs}")
    print(f"❌ 总错误数: {all_errors}")
    
    if all_errors == 0:
        print("🎉 所有检查通过！数据格式正确")
    else:
        print(f"⚠️ 发现 {all_errors} 个问题，请检查并修复")

if __name__ == "__main__":
    verify_textbook_data() 