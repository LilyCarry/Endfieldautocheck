#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#试着去活动里寻找
import sys
from pathlib import Path

# 查找项目根（包含 main.py 的目录）
current = Path(__file__).resolve()
for parent in current.parents:
    if (parent / "main.py").exists():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        break
import time
from task.publicmodule import capture_screen
from task.publicmodule import click
from task.publicmodule import press
from task.publicmodule import check_exist
from task.publicmodule import opencv_compare
def main():
    time.sleep(5)
    press.main(['ESC'])
    print('>')
    tmp_sc_res=capture_screen.main()
    tmp_compare_res=opencv_compare.main(['event.png',f'{tmp_sc_res[1]}',0.75,0,[[None, None], [None, None]]])
    if tmp_compare_res[0]:
        click.main(tmp_compare_res[1],mode='click')
    else:
        print('失败')
    
if __name__=='__main__':
    main()