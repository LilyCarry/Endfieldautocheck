#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#注意!!!!!所有调用子文件夹模块都是相对路径导入!!记得改成:from task.publicmodule.get_program_info import *这样的格式!!
import os
import sys
import time
import shutil
# 确保项目根目录在路径中
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# 导入（绝对路径）
from task import run_launcher, quit_game
from task import login
from task.publicmodule.read_config import read_config
#下面是初始化:
main_config=read_config()
task_st=main_config['task_st']
launcher_result=run_launcher.main()
#清除sc缓存

def clean_sc_folder(folder_path="sc"):
    """
    删除 sc文件夹中的所有内容，但保留 .gitkeep 文件
    """
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"文件夹 {folder_path} 不存在")
        return
    
    # 确保是文件夹
    if not os.path.isdir(folder_path):
        print(f"{folder_path} 不是文件夹")
        return
    
    # 遍历文件夹中的所有内容
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        
        # 保留 .gitkeep 文件
        if item == ".gitkeep":
            continue
        
        # 删除文件
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f"删除文件: {item}")
        
        # 删除子文件夹及其内容
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"删除文件夹: {item}")
    print(f"\n清理完成！")
clean_sc_folder()

#接下来是简单逻辑,暂不按task_st处理:
#if launcher_result[0]:
#    task.quit_game.main()
#else:
#    print('退出失败')
#下面是模块预写.主要是现在没有签到给我签
#大致思路:
#防出错自寻:截图.根据界面特殊图片检测当前所处界面.如果有弹窗,检测弹窗是否有'网络'或Network字样,若有,判断为网卡,直接退出.
#接着,想办法回到正确的那个地方.这个自寻应该作为一个保底,在每个功能模块无法正确识别时,出现不在预期内的结果时,调用该模块作为万金油
#截图->先根据上下文写关系->操作->反馈->成功,下一个\失败,进入防出错自寻->回到:截图
if launcher_result[0]:
    login_res=login.main()
    