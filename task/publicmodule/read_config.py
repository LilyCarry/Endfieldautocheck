#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
import ast
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "placeholder": True,
    "run_max_time": 1,
    "wait_time_s": 40,
    "task_st": ["run_launcher", "login", "daily_check", "quit_game"],
    "launcher_path": "C:/Endfield Game/Endfield.exe"
}
def main() -> Dict[str, Any]:
    """
    从 task/config.json 读取配置，转化为字典返回。
    如果 config.json 不存在，则使用 DEFAULT_CONFIG 创建并保存。
    """
    # 最简单的方法：当前文件在 task/publicmodule/，config.json 在 task/
    config_path = Path(__file__).parent.parent / "config.json"
    
    # 检查配置文件是否存在且非空
    if not config_path.exists() or config_path.stat().st_size == 0:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=4)
        print('配置文件不存在！已恢复默认')
        return DEFAULT_CONFIG.copy()
    
    # 读取已存在的配置文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        backup_path = config_path.with_suffix('.json.backup')
        config_path.rename(backup_path)
        print(f'配置文件损坏！已备份为 {backup_path.name}，已恢复默认')
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=4)
        config = DEFAULT_CONFIG.copy()
    
    return config

def save_config(config: Dict[str, Any]) -> None:
    """保存配置到 config.json"""
    config_path = Path(__file__).parent.parent / "config.json"
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
def format_config_display(config: Dict[str, Any]) -> str:
    """格式化配置为显示字符串"""
    items = []
    for k, v in config.items():
        if isinstance(v, str):
            items.append(f"{k}:'{v}'")
        else:
            items.append(f"{k}:{v}")
    return ','.join(items)

def parse_value_strict(value_str: str) -> Any:
    """
    严格解析 Python 字面量。
    如果输入不是有效的 Python 字面量，抛出 ValueError。
    """
    value_str = value_str.strip()
    
    if not value_str:
        raise ValueError("值不能为空")
    
    try:
        parsed = ast.literal_eval(value_str)
        return parsed
    except (ValueError, SyntaxError) as e:
        error_msg = _format_parse_error(value_str, e)
        raise ValueError(error_msg) from e

def _format_parse_error(value_str: str, original_error: Exception) -> str:
    """格式化解析错误信息"""
    if value_str.lower() in ('true', 'false'):
        return (f"布尔值必须使用 Python 格式：{value_str.lower().capitalize()}\n"
                f"你输入的是: {value_str}")
    
    if value_str.lower() in ('none', 'null', 'nil'):
        return (f"空值必须使用 Python 格式：None\n"
                f"你输入的是: {value_str}")
    
    if (value_str.isalpha() or 
        (value_str.replace('_', '').isalnum() and not value_str[0].isdigit())):
        return (f"字符串必须用引号包裹: '{value_str}' 或 \"{value_str}\"\n"
                f"你输入的是: {value_str}（缺少引号）")
    
    if value_str in ('true', 'false', 'null'):
        return (f"请使用 Python 格式而非 JSON 格式："
                f"True/False/None（首字母大写）\n"
                f"你输入的是: {value_str}")
    
    return (f"无效的 Python 字面量: {value_str}\n"
            f"错误详情: {original_error}\n"
            f"支持的类型: int, float, str(带引号), bool(True/False), "
            f"list, dict, tuple, set, None")

def get_type_hint(value: Any) -> str:
    """获取值的类型提示字符串"""
    type_names = {
        str: "字符串",
        int: "整数",
        float: "浮点数",
        bool: "布尔值",
        list: "列表",
        dict: "字典",
        tuple: "元组",
        set: "集合",
        type(None): "空值(None)"
    }
    return type_names.get(type(value), type(value).__name__)

def interactive_mode() -> None:
    """交互式配置编辑模式"""
    config = main()
    
    print("=== 严格模式配置编辑器 ===")
    print("提示：所有值必须按 Python 字面量格式输入")
    print("示例: 'text'(字符串必须带引号), 123, True, [1,2,3], {'key':'value'}")
    print("输入 'help' 查看详细说明，输入 'quit' 退出")
    print("-" * 50)
    
    while True:
        print(f"\n当前配置：{format_config_display(config)}")
        user_input = input("输入键值对（格式: key:value）: ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        if user_input.lower() == 'help':
            _print_help()
            continue
        
        if ':' not in user_input:
            print("❌ 格式错误！请使用 key:value 格式（用冒号分隔键和值）")
            continue
        
        key, value_str = user_input.split(':', 1)
        key = key.strip()
        value_str = value_str.strip()
        
        if not key:
            print("❌ 键不能为空！")
            continue
        
        try:
            value = parse_value_strict(value_str)
        except ValueError as e:
            print(f"❌ 解析错误：\n{e}")
            continue
        
        old_value = config.get(key)
        config[key] = value
        
        if old_value is not None:
            old_type = get_type_hint(old_value)
            new_type = get_type_hint(value)
            type_change = f" (类型: {old_type} -> {new_type})" if type(old_value) != type(value) else ""
            print(f"✓ 更新: {key} = {value}{type_change}")
        else:
            print(f"✓ 新增: {key} = {value} ({get_type_hint(value)})")
        
        save_config(config)
    
    print("\n配置已保存，退出。")

def _print_help():
    """打印帮助信息"""
    help_text = """
【严格模式 - 输入格式说明】

所有值必须是有效的 Python 字面量：

1. 字符串（必须带引号）:
   name:'Alice'  或  name:"Bob"

2. 数字:
   count:42      (整数)
   pi:3.14159    (浮点数)

3. 布尔值（首字母大写）:
   enabled:True
   debug:False

4. 空值:
   data:None

5. 列表:
   items:[1, 2, 3]
   names:['a', 'b']

6. 字典:
   settings:{'theme': 'dark', 'lang': 'zh'}

7. 元组:
   point:(1, 2)

【常见错误】
  ❌ name:Alice      -> 字符串缺少引号
  ❌ enabled:true    -> 布尔值必须大写首字母 True
  ❌ data:null       -> 必须使用 None 而非 null
  ✅ name:'Alice'
  ✅ enabled:True
  ✅ data:None
"""
    print(help_text)

if __name__ == "__main__":
    interactive_mode()