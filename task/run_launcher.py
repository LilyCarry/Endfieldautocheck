#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import subprocess
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 绝对导入
from task.publicmodule import capture_screen
from task.publicmodule import opencv_compare
from task.publicmodule import read_config
from task.publicmodule.get_program_info import get_program_info

def main():
    print('正在启动启动器...')
    config = read_config.main()
    run_max_time = config['run_max_time']
    path = config['launcher_path']
    wait_time_s = config['wait_time_s']
    current_time = 0
    
    while current_time <= run_max_time:
        print(f'运行第 {current_time} 次:')
        subprocess.Popen([path])
        print(f'等待 {wait_time_s} 秒')
        time.sleep(wait_time_s)
        current_time += 1
        
        if get_program_info('endfield.exe')['match']:
            break
    else:
        print('失败!')
        print('请自行检查 path 是否存在，或是调大 run_max_time')
        print('程序即将退出')
        return [False, '失败.原因:未知']
    
    if get_program_info('endfield.exe')['match']:
        print('成功')
        return [True, '成功']
    else:
        print('你怎么来这条路的?')
        return [True, 'WTF????']

if __name__ == '__main__':
    main()