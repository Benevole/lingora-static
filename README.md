# 教材JSON数据生成工具

根据目录结构生成教材JSON数据，为每个第一层级目录生成单独的JSON文件，包含code、parentCode、type、name、link字段。

## 功能特点

- 📁 递归遍历目录结构
- 🔢 自动生成层级编码（1, 1-1, 1-2, 2-1, 2-2...）
- 🔢 **智能数字排序**：按数字顺序排序，确保1排在100前面
- 🔗 自动生成PDF文件的完整URL
- 📂 为每个一级目录生成单独的JSON文件
- ✅ 包含数据验证功能

## 文件说明

### `generate_textbook_data.py`
主脚本，用于生成JSON数据。

**功能：**
- 遍历当前目录下的所有第一层级目录
- 为每个第一层级目录生成单独的JSON文件
- 生成包含code、parentCode、type、name、link字段的JSON数组
- **智能数字排序**：按数字顺序排序，确保1排在100前面
- 输出到 `textbook_N_目录名.json` 文件

**使用方法：**
```bash
python3 generate_textbook_data.py
```

**输出文件：**
- `textbook_1_1新雅思.json`
- `textbook_2_2经典英语青少年.json`
- `textbook_3_3国际认证少年英语高级.json`
- `textbook_4_4自然拼读.json`
- `textbook_5_5西游记.json`
- `textbook_6_6小猪佩奇.json`
- `textbook_7_7自由主题.json`

### `verify_data.py`
验证脚本，用于检查生成的JSON数据。

**功能：**
- 检查所有 `textbook_*.json` 文件
- 检查数据结构完整性
- 验证层级关系
- 检查URL格式
- **验证数字排序规则**
- 显示统计信息

**使用方法：**
```bash
python3 verify_data.py
```

## 数据格式

生成的JSON数组包含以下字段：

```json
{
  "code": "1-2-3",           // 层级编码
  "parentCode": "1-2",       // 父级编码
  "type": "TEXTBOOK",        // 固定值
  "name": "文件名.pdf",       // 文件/目录名称
  "link": "http://pdf.lingora.cn/..." // PDF文件URL，目录为null
}
```

## 编码规则

- **第一层**：1, 2, 3, 4...
- **第二层**：1-1, 1-2, 2-1, 2-2...
- **第三层**：1-1-1, 1-1-2, 1-2-1...
- **第一层的parentCode**：'0'
- **子层的parentCode**：父级的code

## 排序规则

### 🔢 智能数字排序
脚本支持多种数字格式的智能排序：

1. **标准格式**：`1、第一单元` → 排序数字：1
2. **无顿号格式**：`10第三单元` → 排序数字：10
3. **Unit格式**：`Unit1, Unit2, Unit3...` → 排序数字：1, 2, 3...
4. **Phonics Lesson格式**：`Phonics Lesson 37 wr&kn.pdf` → 排序数字：37
5. **Phonics格式**：`phonics2_lesson19.pdf` → 排序数字：19
6. **Unit-Lesson格式**：`U1L1, U2L16, U5L62 Adventure.pdf` → 排序数字：1001, 2016, 5062
7. **西游记格式**：`西游记001_The Monkey.pdf` → 排序数字：1
8. **小猪佩奇格式**：`S1-01_Muddy_Puddles01.pdf` → 排序数字：1

### ✅ 排序效果
- **正确**：1, 2, 3, 10, 100, 101...
- **错误**：1, 10, 100, 2, 3...（字母排序）

## URL格式

PDF文件的URL格式：
```
http://pdf.lingora.cn/ + 路径编码
```

例如：
```
http://pdf.lingora.cn/1%E6%96%B0%E9%9B%85%E6%80%9D/...
```

## 使用步骤

1. **生成数据**：
   ```bash
   python3 generate_textbook_data.py
   ```

2. **验证数据**：
   ```bash
   python3 verify_data.py
   ```

3. **查看结果**：
   生成的 `textbook_N_目录名.json` 文件包含对应目录的完整数据

## 生成结果统计

| 分类 | 文件名 | 目录数 | PDF文件数 | 总记录数 |
|------|--------|--------|-----------|----------|
| 1新雅思 | textbook_1_1新雅思.json | 4 | 433 | 437 |
| 2经典英语青少年 | textbook_2_2经典英语青少年.json | 153 | 1126 | 1279 |
| 3国际认证少年英语高级 | textbook_3_3国际认证少年英语高级.json | 13 | 179 | 192 |
| 4自然拼读 | textbook_4_4自然拼读.json | 3 | 71 | 74 |
| 5西游记 | textbook_5_5西游记.json | 1 | 108 | 109 |
| 6小猪佩奇 | textbook_6_6小猪佩奇.json | 2 | 52 | 54 |
| 7自由主题 | textbook_7_7自由主题.json | 4 | 119 | 123 |

**总计：** 180个目录，2088个PDF文件，2268条记录

## 注意事项

- 脚本会过滤掉隐藏文件和.git目录
- 只处理PDF文件，其他文件类型会被忽略
- 确保有足够的权限访问目录
- 生成的JSON文件使用UTF-8编码
- 每个一级目录生成独立的JSON文件，便于分类管理
- **数字排序确保1排在100前面，符合自然阅读顺序**

## 示例输出

```json
[
  {
    "code": "1",
    "parentCode": "0",
    "type": "TEXTBOOK",
    "name": "1新雅思",
    "link": null
  },
  {
    "code": "1-1",
    "parentCode": "1",
    "type": "TEXTBOOK",
    "name": "新雅思口语中级冲刺5.5分",
    "link": null
  },
  {
    "code": "1-1-1",
    "parentCode": "1-1",
    "type": "TEXTBOOK",
    "name": "1、第一单元 人物 话题一 你最喜欢的家庭成员·上篇 A family member you like·Lesson 1.pdf",
    "link": "http://pdf.lingora.cn/1%E6%96%B0%E9%9B%85%E6%80%9D/%E6%96%B0%E9%9B%85%E6%80%9D%E5%8F%A3%E8%AF%AD%E4%B8%AD%E7%BA%A7%E5%86%B2%E5%88%865.5%E5%88%86/1%E3%80%81%E7%AC%AC%E4%B8%80%E5%8D%95%E5%85%83%20%E4%BA%BA%E7%89%A9%20%E8%AF%9D%E9%A2%98%E4%B8%80%20%E4%BD%A0%E6%9C%80%E5%96%9C%E6%AC%A2%E7%9A%84%E5%AE%B6%E5%BA%AD%E6%88%90%E5%91%98%C2%B7%E4%B8%8A%E7%AF%87%20A%20family%20member%20you%20like%C2%B7Lesson%201.pdf"
  }
]
```