#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
键盘模拟操作模块 - PyAutoGUI版本
功能: 模拟键盘按键操作
依赖: pip install pyautogui
"""

import pyautogui
import time
from typing import List

class KeyboardSimulator:
    def __init__(self):
        # 禁用pyautogui的安全特性（鼠标移到屏幕角落不会触发失败）
        pyautogui.FAILSAFE = False
        # 设置默认暂停时间
        pyautogui.PAUSE = 0
        
        self.special_keys = {
            'ESC': 'esc', 'ENTER': 'return', 'SPACE': 'space',
            'TAB': 'tab', 'BACKSPACE': 'backspace', 'DELETE': 'delete',
            'UP': 'up', 'DOWN': 'down', 'LEFT': 'left', 'RIGHT': 'right',
            'HOME': 'home', 'END': 'end', 'PAGE_UP': 'pageup',
            'PAGE_DOWN': 'pagedown', 'F1': 'f1', 'F2': 'f2',
            'F3': 'f3', 'F4': 'f4', 'F5': 'f5', 'F6': 'f6',
            'F7': 'f7', 'F8': 'f8', 'F9': 'f9', 'F10': 'f10',
            'F11': 'f11', 'F12': 'f12', 'CTRL': 'ctrl',
            'SHIFT': 'shift', 'ALT': 'alt', 'CMD': 'command',
            'CAPS_LOCK': 'capslock', 'NUM_LOCK': 'numlock',
            'SCROLL_LOCK': 'scrolllock', 'INSERT': 'insert',
            'PRINT_SCREEN': 'print', 'PAUSE': 'pause',
            # 添加一些常用的组合键别名
            'WIN': 'win', 'WINDOWS': 'win', 'OPTION': 'option',
            'CONTROL': 'ctrl', 'COMMAND': 'command',
        }

    def _get_key(self, key_str: str):
        key_str = key_str.upper()
        if key_str in self.special_keys:
            return self.special_keys[key_str]
        if '+' in key_str:
            # 处理组合键，如 "CTRL+A"
            keys = [k.strip().upper() for k in key_str.split('+')]
            return [self._get_key(k) for k in keys]
        if len(key_str) == 1:
            # 单字符直接返回小写
            return key_str.lower()
        raise ValueError(f"未知的按键: {key_str}")

    def _press_key(self, key):
        if isinstance(key, list):
            # 组合键：按住所有修饰键，按下最后一个键，然后依次释放
            pyautogui.keyDown(*key)
            pyautogui.keyUp(*key)
        else:
            # 单键
            pyautogui.press(key)

    def simulate_keys(self, keys: List[str], times: int = 1, lag: float|int = 0):
        """
        模拟键盘按键操作

        参数:
            keys: 按键列表，如 ['A', 'B', 'ESC']
            times: 重复次数，默认为1
            lag: 每次按键操作之间的间隔时间（秒），默认为0
        """
        for _ in range(times):
            for key_str in keys:
                try:
                    key = self._get_key(key_str)
                    self._press_key(key)
                    if lag > 0:
                        time.sleep(lag)
                except Exception as e:
                    print(f"操作失败 [{key_str}]: {e}")
                    continue


def main(keys: List[str], times: int = 1, lag: float|int = 0):
    """
    模拟键盘操作的便捷函数

    参数:
        keys: 按键列表，如 ['A', 'B', 'ESC']
        times: 重复次数，默认为1
        lag: 每次按键操作之间的间隔时间（秒），默认为0
    """
    simulator = KeyboardSimulator()
    simulator.simulate_keys(keys, times, lag)


# ==================== 使用示例 ====================
if __name__ == "__main__":
    keys = input('str:要输哪个按键?(回车结束)')
    keyslst = [keys]
    while keys != '':
        keys = input('str:要输哪个按键?(回车结束)')
        keyslst += [keys]
    keyslst.pop()
    times = int(input('要搞几次?'))
    lag = float(input('延迟呢?'))
    print(keyslst)
    time.sleep(3)
    main(keyslst, times, lag)