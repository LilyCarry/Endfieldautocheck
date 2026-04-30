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
from task.publicmodule import capture_screen
from task.publicmodule import opencv_compare as oc
def main():
    '''
    传参:无
    根据当前画面,判断处于哪个界面;目前只支持pre_login和login,loading加载识别'''
    screen_shot=capture_screen.main()
    UI_areas=['','']
    for item in UI_areas:
        tmp_lst=[screen_shot,item,0.9,]
    