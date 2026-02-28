#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time

# 添加项目根目录到路径（用于单独调试）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 绝对导入
from task.publicmodule.read_config import read_config
from task.publicmodule import capture_screen
from task.publicmodule import click
from task.publicmodule import opencv_compare as compare
from task.publicmodule import get_program_info
from task.publicmodule import check_exist

def main():
    config = read_config()
    exist = check_exist.check_exist()
    run_max_time = config['run_max_time']
    path = config['launcher_path']
    wait_time_s = config['wait_time_s']
    current_time = 0
    
    while exist and current_time <= run_max_time:
        print(f'第{current_time+1}次尝试')
        capture_result = capture_screen.capture_screen()
        if capture_result[0]:
            print(f"截图,路径{capture_result[1]}")
            compare_result = compare.opencv_compare(['continue.png', f'{capture_result[1]}', '0.9', '0', [[None, None], [None, None]]])
            current_time_1 = 0
            while not compare_result[0] and current_time_1 <= 10:
                compare_result = compare.opencv_compare(['continue.png', f'{capture_result[1]}', '0.9', '0', [[None, None], [None, None]]])
                print('正在等待游戏就绪')
                print(f'次数:第{current_time_1+1}次')
                time.sleep(60)
            else:
                print('超时!')
                print('出现问题,正在退出')

if __name__ == '__main__':
    main()