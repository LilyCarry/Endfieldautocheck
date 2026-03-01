#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import subprocess
import sys
import os
import hashlib

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 绝对导入
from task.publicmodule import capture_screen
from task.publicmodule import opencv_compare
from task.publicmodule import check_exist
from task.publicmodule import read_config
from task.publicmodule.get_program_info import get_program_info

def get_task_name(exe_path):
    """根据路径生成唯一的任务名称"""
    hash_val = hashlib.md5(exe_path.encode('utf-8')).hexdigest()[:8]
    return f"Elevated_Launcher_{hash_val}"

def run_via_task_scheduler(exe_path):
    """
    通过计划任务启动程序以绕过UAC
    """
    task_name = get_task_name(exe_path)
    
    # 【修复重点】：将路径转换为绝对路径，并将正斜杠 / 替换为反斜杠 \
    # 防止 schtasks 将 /Game 识别为命令参数开关
    win_path = os.path.abspath(exe_path).replace('/', '\\')
    
    # 1. 检查任务是否存在
    check_cmd = f'schtasks /query /tn "{task_name}"'
    exists = subprocess.run(check_cmd, capture_output=True, shell=True).returncode == 0
    
    if not exists:
        print(f"首次运行，正在创建计划任务: {task_name}")
        # 2. 创建任务
        # /tr 参数内的路径需用反斜杠，并且用被转义的双引号包裹，如 "\"C:\Path\Game.exe\""
        create_cmd = f'schtasks /create /tn "{task_name}" /tr "\\"{win_path}\\"" /sc once /st 00:00 /rl highest /f'
        result = subprocess.run(create_cmd, capture_output=True, shell=True, text=True)
        
        if result.returncode != 0:
            print("错误: 无法创建计划任务。请尝试以管理员身份运行此脚本一次。")
            print(f"详细报错信息:\n{result.stderr}")
            print("将退回使用普通方式(弹窗)启动...")
            # 创建失败的后备方案：直接用原来的方式启动（会弹出UAC）
            subprocess.Popen([exe_path])
            return

    # 3. 运行任务
    run_cmd = f'schtasks /run /tn "{task_name}"'
    subprocess.run(run_cmd, capture_output=True, shell=True)

def main():
    print('正在启动启动器...')
    config = read_config.main()
    run_max_time = config['run_max_time']
    path = config['launcher_path']
    wait_time_s = config['wait_time_s']
    current_time = 0
    exist=check_exist.main()
    while current_time <= run_max_time and not exist:
        print(f'运行第 {current_time} 次:')
        
        # 替换原有的 subprocess.Popen([path])，改为计划任务提权启动
        run_via_task_scheduler(path)
        
        print(f'等待 {wait_time_s} 秒')
        time.sleep(wait_time_s)
        current_time += 1
        
        if get_program_info('endfield.exe')['match']:
            break
    else:
        if exist:
            print('成功,程序已存在')
            return[True,'程序已存在']
        print('失败!')
        print('请自行检查 path 是否存在，或是调大 run_max_time')
        print('程序即将退出')
        return[False, '失败.原因:未知']
    
    if get_program_info('endfield.exe')['match']:
        print('成功')
        return [True, '成功']
    else:
        print('你怎么来这条路的?')
        return [True, 'WTF????']

if __name__ == '__main__':
    main()