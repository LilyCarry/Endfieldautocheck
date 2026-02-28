#输入参数:[[x,y],mode,times,[tx,ty]
#[x,y]表示起始位置,或点击位置;
#mode指点击模式.有:点击,多次点击,拖动
#times指次数.若mode为 click,则点击 times 次;若为drag,则重复 times 次.
#[tx,ty] 只有mode = drag 时需要.从x,y drag到 tx,ty
# -*- coding: utf-8 -*-
"""
click.py - 鼠标控制模块
功能：实现鼠标点击、多次点击和拖动操作
"""

import time
from pynput.mouse import Controller, Button

# 鼠标控制器实例
mouse = Controller()


def click(pos, mode='click', times=1, target_pos=None, lag=1):
    """
    鼠标控制函数 - 支持点击、多次点击和拖动
    
    参数:
        pos (list): [x, y] 起始位置或点击位置
        mode (str): 操作模式
            - 'click': 点击指定位置
            - 'drag': 从pos拖动到target_pos
        times (int): 次数
            - mode='click'时: 点击times次
            - mode='drag'时: 重复拖动times次
        target_pos (list/None): [tx, ty] 目标位置，仅在mode='drag'时需要
        lag:每次操作延迟秒 (int)
    
    返回:
        bool: 操作是否成功
    
    示例:
        >>> click([100, 200], mode='click', times=2)  # 在(100,200)双击
        >>> click([100, 200], mode='drag', times=1, target_pos=[300, 400])  # 拖动
    """
    try:
        x, y = pos
        
        if mode == 'click':
            # 移动到指定位置
            mouse.position = (x, y)
            time.sleep(0.05)  # 短暂延迟确保移动完成
            
            # 执行指定次数的点击
            for _ in range(times):
                mouse.click(Button.left)
                time.sleep(0.05)  # 点击间隔
            
            print(f"已在 ({x}, {y}) 点击 {times} 次")
            return True
            
        elif mode == 'drag':
            if target_pos is None:
                print("错误：拖动模式需要提供 target_pos 参数 [tx, ty]")
                return False
            
            tx, ty = target_pos
            
            for i in range(times):
                # 移动到起始位置
                mouse.position = (x, y)
                time.sleep(0.05)
                
                # 按下左键
                mouse.press(Button.left)
                time.sleep(0.1)
                
                # 移动到目标位置
                mouse.position = (tx, ty)
                time.sleep(0.1)
                
                # 释放左键
                mouse.release(Button.left)
                time.sleep(0.05)
                
                if times > 1:
                    print(f"第 {i+1}/{times} 次拖动: ({x}, {y}) -> ({tx}, {ty})")
            
            if times == 1:
                print(f"已拖动: ({x}, {y}) -> ({tx}, {ty})")
            else:
                print(f"共完成 {times} 次拖动操作")
            return True
            
        else:
            print(f"错误：未知的模式: {mode}。支持的模式: 'click', 'drag'")
            return False
            
    except Exception as e:
        print(f"操作失败: {e}")
        return False


def get_position():
    """获取当前鼠标位置"""
    return list(mouse.position)


def move_to(x, y):
    """移动鼠标到指定位置"""
    mouse.position = (x, y)
    print(f"鼠标已移动到 ({x}, {y})")


if __name__ == '__main__':
    print("=" * 50)
    print("click.py 调试模式")
    print("=" * 50)
    print("\n当前鼠标位置:", get_position())
    print("\n--- 功能测试 ---\n")
    
    # 测试1: 获取当前位置并点击
    print("【测试1】获取当前位置并在该位置点击2次")
    print(f"将在当前位置进行双击测试")
    input("按 Enter 开始测试 (你有3秒时间将鼠标移到位)...")
    time.sleep(3)
    current_pos = get_position()
    click(current_pos, mode='click', times=3)
    time.sleep(1)
    
    # 测试2: 拖动测试
    print("\n【测试2】拖动测试")
    print("将从 (500, 500) 拖动到 (700, 700)")
    input("按 Enter 开始拖动测试 (你有3秒时间准备)...")
    time.sleep(3)
    click([500, 500], mode='drag', times=1, target_pos=[700, 700])
    time.sleep(1)
    
    # 测试3: 多次拖动
    print("\n【测试3】多次拖动测试")
    print("将重复2次: 从 (600, 600) 拖动到 (800, 600)")
    input("按 Enter 开始多次拖动测试 (你有3秒时间准备)...")
    time.sleep(3)
    click([600, 600], mode='drag', times=2, target_pos=[800, 600])
    
    print("\n" + "=" * 50)
    print("所有测试完成")
    print("=" * 50)