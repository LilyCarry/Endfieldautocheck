#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
import time
import sys

# 添加项目根目录到路径（用于单独调试）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 绝对导入
from task.publicmodule.get_program_info import get_program_info

def main():
    print('开始退出程序')
    current_time = 0
    max_time = 3
    
    while current_time <= max_time:
        exist = get_program_info('endfield.exe')['match']
        pid = int(get_program_info('endfield.exe')['pid'])
        
        if exist:
            os.kill(pid, signal.SIGTERM)
            time.sleep(3)
        else:
            print('成功')
            return [True, '成功了,别看了']
        
        current_time += 1
    else:
        print('草,没杀掉')
        return [False, '失败了,原因:{}']

if __name__ == '__main__':
    main()