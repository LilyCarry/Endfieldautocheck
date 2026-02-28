#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
键盘模拟操作模块 - 独立版本
功能: 模拟键盘按键操作
依赖: pip install pynput
"""

from pynput.keyboard import Controller, Key
import time
from typing import List

class KeyboardSimulator:
    def __init__(self):
        self.keyboard = Controller()
        self.special_keys = {
            'ESC': Key.esc, 'ENTER': Key.enter, 'SPACE': Key.space,
            'TAB': Key.tab, 'BACKSPACE': Key.backspace, 'DELETE': Key.delete,
            'UP': Key.up, 'DOWN': Key.down, 'LEFT': Key.left, 'RIGHT': Key.right,
            'HOME': Key.home, 'END': Key.end, 'PAGE_UP': Key.page_up,
            'PAGE_DOWN': Key.page_down, 'F1': Key.f1, 'F2': Key.f2,
            'F3': Key.f3, 'F4': Key.f4, 'F5': Key.f5, 'F6': Key.f6,
            'F7': Key.f7, 'F8': Key.f8, 'F9': Key.f9, 'F10': Key.f10,
            'F11': Key.f11, 'F12': Key.f12, 'CTRL': Key.ctrl,
            'SHIFT': Key.shift, 'ALT': Key.alt, 'CMD': Key.cmd,
            'CAPS_LOCK': Key.caps_lock, 'NUM_LOCK': Key.num_lock,
            'SCROLL_LOCK': Key.scroll_lock, 'INSERT': Key.insert,
            'PRINT_SCREEN': Key.print_screen, 'PAUSE': Key.pause,
        }

    def _get_key(self, key_str: str):
        key_str = key_str.upper()
        if key_str in self.special_keys:
            return self.special_keys[key_str]
        if '+' in key_str:
            keys = [k.strip().upper() for k in key_str.split('+')]
            return [self._get_key(k) for k in keys]
        if len(key_str) == 1:
            return key_str.lower()
        raise ValueError(f"未知的按键: {key_str}")

    def _press_key(self, key):
        if isinstance(key, list):
            for k in key[:-1]:
                self.keyboard.press(k)
            self.keyboard.press(key[-1])
            self.keyboard.release(key[-1])
            for k in reversed(key[:-1]):
                self.keyboard.release(k)
        else:
            self.keyboard.press(key)
            self.keyboard.release(key)

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
    keys=input('str:要输哪个按键?(回车结束)')
    keyslst=[keys]
    while keys!='':
        keys=input('str:要输哪个按键?(回车结束)')
        keyslst+=[keys]
    keyslst.pop()
    times=int(input('要搞几次?'))
    lag=float(input('延迟呢?'))
    print(keyslst)
    time.sleep(3)
    main(keyslst,times,lag)