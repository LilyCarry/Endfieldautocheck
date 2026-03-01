#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# 查找项目根（包含 main.py 的目录）
current = Path(__file__).resolve()
for parent in current.parents:
    if (parent / "main.py").exists():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        break
#先检测有没有直接出现签到界面
import time
from task.publicmodule import capture_screen
from task.publicmodule import check_exist
from task.publicmodule import read_config
from task.publicmodule import opencv_compare
from task.publicmodule import click
def main()->tuple[bool,str]|tuple[bool,str,str]:
    config=read_config.main()
    run_max_time=config['run_max_time'];wait_time_s=config['wait_time_s']
    tmp_exist=check_exist.main()
    current_time=0;tmp_times=0
    while tmp_times<=20:
                print('等待加载...')
                capture_result = capture_screen.main()#截图
                tmp_compare_loading=opencv_compare.main(['loading.png',f'{capture_result[1]}','0.9','0',[[None, None], [None, None]]])
                tmp_times+=1
                if not tmp_compare_loading[0]:
                    break
                else:
                    time.sleep(10)
    else:
        return (False,'等待加载时间太长!!')
    while tmp_exist and current_time<=run_max_time:
        tmp_exist=check_exist.main()
        print(f'第{current_time+1}次尝试签到')
        current_time+=1
        capture_result=capture_screen.main()
        print(f"截图,路径{capture_result[1]}")
        compare_result=opencv_compare.main(['collect_reward.png',f'{capture_result[1]}',0.9,0,[[None, None], [None, None]]])
        if compare_result[0]:
            print(f'存在领取奖励按钮,在{compare_result[1]}')
            click.main(compare_result[1],mode='click',times=1)
            time.sleep(3)
            capture_result=capture_screen.main()
            compare_result=opencv_compare.main(['collect_reward.png',f'{capture_result[1]}',0.9,0,[[None, None], [None, None]]])
            tmp_run_max_time=5;tmp_current_time=0
            while tmp_current_time<=tmp_run_max_time:
                if compare_result[0]:
                    click.main(compare_result[1],mode='click',times=1)
                    capture_result=capture_screen.main()
                    compare_result=opencv_compare.main(['collect_reward.png',f'{capture_result[1]}',0.9,0,[[None, None], [None, None]]])
                    tmp_current_time+=1
                else:
                    break
            else:
                print('签到出现问题!')
                return (False,'签到出现问题,有按钮但点击失败')
            print('签到成功!')
            return (True,'成功')
        else:
            print('未检测到界面')
            time.sleep(10)
    else:
        print('失败!')
        tmp_exist=check_exist.main()
        if not tmp_exist:
            return (False,'游戏退出!')
        else:
            print('似乎没有签到弹出!')
            return (False,'首次签到超次,可能已签到或不存在活动','应该继续,所以这里有三项,为了检测len()')