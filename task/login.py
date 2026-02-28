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
from task import quit_game

def main():
    config = read_config()
    exist = check_exist.check_exist()
    run_max_time = config['run_max_time']
    path = config['launcher_path']
    wait_time_s = config['wait_time_s']
    current_time = 0
    
    while exist and current_time <= run_max_time:#程序要一直存在
        print(f'第{current_time+1}次尝试')
        capture_result = capture_screen.capture_screen()#截图
        if capture_result[0]:#存在结果
            print(f"截图,路径{capture_result[1]}")
            compare_result = compare.opencv_compare(['continue.png', f'{capture_result[1]}', '0.9', '0', [[None, None], [None, None]]])#比较
            current_time_1 = 0
            while current_time_1 <= 10:#比10次
                capture_result = capture_screen.capture_screen()#截图
                print(f"截图,路径{capture_result[1]}")
                compare_result = compare.opencv_compare(['continue.png', f'{capture_result[1]}', '0.9', '0', [[None, None], [None, None]]])
                print('正在等待游戏就绪')
                print(f'次数:第{current_time_1+1}次')
                current_time_1+=1
                if not compare_result[0]:#是否成功?
                    print('匹配失败,等待中')
                    time.sleep(60)#失败,等60s再来
                else:
                    break#成功了,滚出去
            else:
                print('超时!')
                print('出现问题,正在退出')
                return [False,"超时!"]#直接return防走到下面
            print('成功进入等待页面')
            click.click(pos=compare_result[1],mode='click',times=5,lag=1)#点击5次
            time.sleep(5)#等5s
            #capture_result = capture_screen.capture_screen()#截图
            #tmp_compare_loading=compare.opencv_compare(['loading.png',f'{capture_result[1]}','0.9','0',[[None, None], [None, None]]])
            #tmp_compare_entered=compare.opencv_compare(['.png',f'{capture_result[1]}','0.9','0',[[None, None], [None, None]]])
            return [True,'成功了']
        else:
            print('未知错误!')
            return [False,"似乎是capture_result出错了!"]
    else:
        print('游戏不存在!!!')
        return [False,'游戏不存在']
if __name__ == '__main__':
    main()