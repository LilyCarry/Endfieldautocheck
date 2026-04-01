#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
键盘模拟操作模块 - AHK版本
功能: 模拟键盘按键操作
依赖: pip install ahk
"""

import time
from typing import List
from ahk import AHK

# 初始化 AHK 实例
ahk = AHK()


class KeyboardSimulator:
    def __init__(self):
        self.special_keys = {
            'ESC': 'Escape', 'ENTER': 'Enter', 'SPACE': 'Space',
            'TAB': 'Tab', 'BACKSPACE': 'Backspace', 'DELETE': 'Delete',
            'UP': 'Up', 'DOWN': 'Down', 'LEFT': 'Left', 'RIGHT': 'Right',
            'HOME': 'Home', 'END': 'End', 'PAGE_UP': 'PgUp',
            'PAGE_DOWN': 'PgDn', 'F1': 'F1', 'F2': 'F2',
            'F3': 'F3', 'F4': 'F4', 'F5': 'F5', 'F6': 'F6',
            'F7': 'F7', 'F8': 'F8', 'F9': 'F9', 'F10': 'F10',
            'F11': 'F11', 'F12': 'F12', 'CTRL': 'Control',
            'SHIFT': 'Shift', 'ALT': 'Alt', 'CMD': 'LWin',
            'CAPS_LOCK': 'CapsLock', 'NUM_LOCK': 'NumLock',
            'SCROLL_LOCK': 'ScrollLock', 'INSERT': 'Insert',
            'PRINT_SCREEN': 'PrintScreen', 'PAUSE': 'Pause',
            # 添加一些常用的组合键别名
            'WIN': 'LWin', 'WINDOWS': 'LWin', 'OPTION': 'Alt',
            'CONTROL': 'Control', 'COMMAND': 'LWin',
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
            # 单字符直接返回
            return key_str
        raise ValueError(f"未知的按键: {key_str}")

    def _press_key(self, key):
        if isinstance(key, list):
            # 组合键：使用 ahk.key_down 和 key_up
            # AHK 组合键格式: ^{a} 表示 Ctrl+A
            modifier_map = {
                'Control': '^',
                'Shift': '+',
                'Alt': '!',
                'LWin': '#'
            }

            modifiers = []
            main_key = None

            for k in key:
                if k in modifier_map:
                    modifiers.append(modifier_map[k])
                else:
                    main_key = k

            if main_key:
                hotkey_str = ''.join(modifiers) + main_key
                ahk.key_press(hotkey_str)
        else:
            # 单键
            ahk.key_press(key)

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
