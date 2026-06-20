#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
键盘模拟操作模块 - SendMessage 版本
功能: 模拟键盘按键操作
依赖: ctypes (Windows 内置，无需额外安装)
"""

import time
import ctypes
from typing import List

# ── Windows API 常量 ──────────────────────────────────────────────
WM_KEYDOWN = 0x0100
WM_KEYUP   = 0x0101

# ── 虚拟键码映射表 ────────────────────────────────────────────────
VK_MAP = {
    # 功能键
    'ESC': 0x1B, 'ENTER': 0x0D, 'SPACE': 0x20,
    'TAB': 0x09, 'BACKSPACE': 0x08, 'DELETE': 0x2E,
    # 方向键
    'UP': 0x26, 'DOWN': 0x28, 'LEFT': 0x25, 'RIGHT': 0x27,
    # 导航键
    'HOME': 0x24, 'END': 0x23,
    'PAGE_UP': 0x21, 'PAGE_DOWN': 0x22,
    # F 功能键
    'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73,
    'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77,
    'F9': 0x78, 'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B,
    # 修饰键
    'CTRL': 0x11, 'SHIFT': 0x10, 'ALT': 0x12,
    'CONTROL': 0x11, 'OPTION': 0x12,
    # Windows 键
    'CMD': 0x5B, 'WIN': 0x5B, 'WINDOWS': 0x5B, 'COMMAND': 0x5B,
    # 锁定键
    'CAPS_LOCK': 0x14, 'NUM_LOCK': 0x90, 'SCROLL_LOCK': 0x91,
    # 其他键
    'INSERT': 0x2D, 'PRINT_SCREEN': 0x2C, 'PAUSE': 0x13,
    # ── ahk 键名兼容 (_get_key 返回的格式) ──
    'ESCAPE': 0x1B,
    'PGUP': 0x21, 'PGDN': 0x22,
    'LWIN': 0x5B,
    'CAPSLOCK': 0x14, 'NUMLOCK': 0x90, 'SCROLLLOCK': 0x91,
    'PRINTSCREEN': 0x2C,
}

# ── 加载 user32.dll ───────────────────────────────────────────────
user32 = ctypes.windll.user32


def _get_foreground_window():
    """获取当前前台窗口句柄"""
    return user32.GetForegroundWindow()


def _make_key_lparam(vk_code, is_up=False):
    """构建 WM_KEYDOWN / WM_KEYUP 所需的标准 lParam"""
    scan_code = user32.MapVirtualKeyW(vk_code, 0)  # MAPVK_VK_TO_VSC
    lparam = 1  # repeat count = 1
    lparam |= (scan_code & 0xFF) << 16
    if is_up:
        lparam |= (1 << 30) | (1 << 31)  # previous key state + transition
    return lparam


def _send_key(hwnd, vk_code, is_up=False):
    """向目标窗口发送按键按下/释放消息"""
    lparam = _make_key_lparam(vk_code, is_up=is_up)
    msg = WM_KEYUP if is_up else WM_KEYDOWN
    user32.PostMessageW(hwnd, msg, vk_code, lparam)


# ═══════════════════════════════════════════════════════════════════
#  KeyboardSimulator — 与原版完全一致的公共接口
# ═══════════════════════════════════════════════════════════════════

class KeyboardSimulator:
    def __init__(self):
        # 保留原版 special_keys 映射以供 _get_key 使用
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
            'WIN': 'LWin', 'WINDOWS': 'LWin', 'OPTION': 'Alt',
            'CONTROL': 'Control', 'COMMAND': 'LWin',
        }

    def _get_vk_code(self, key_str: str):
        """
        将按键字符串转为虚拟键码 (Virtual-Key Code)
        支持单字符、特殊键名、组合键(如 "CTRL+A")
        返回 (modifiers, main_vk) 或 单个 vk_code
        """
        key_str = key_str.upper()

        # 组合键: 如 "CTRL+A"
        if '+' in key_str:
            parts = [k.strip().upper() for k in key_str.split('+')]
            modifiers = []
            main_vk = None
            for k in parts:
                vk = VK_MAP.get(k)
                if vk is None and len(k) == 1:
                    vk = ord(k)
                if k in ('CTRL', 'CONTROL', 'SHIFT', 'ALT', 'OPTION', 'WIN', 'WINDOWS', 'CMD', 'COMMAND'):
                    modifiers.append(vk)
                else:
                    main_vk = vk
            if main_vk is None:
                raise ValueError(f"组合键中未找到主键: {key_str}")
            return modifiers, main_vk

        # 特殊键
        vk = VK_MAP.get(key_str)
        if vk is not None:
            return vk

        # 单字符 (A-Z, 0-9 等)
        if len(key_str) == 1:
            return ord(key_str)

        raise ValueError(f"未知的按键: {key_str}")

    def _get_key(self, key_str: str):
        """
        保持与原版相同的接口：返回 ahk 兼容格式
        此方法保留以维持兼容性，但内部实现已切换为 SendMessage
        """
        key_str = key_str.upper()
        if key_str in self.special_keys:
            return self.special_keys[key_str]
        if '+' in key_str:
            keys = [k.strip().upper() for k in key_str.split('+')]
            return [self._get_key(k) for k in keys]
        if len(key_str) == 1:
            return key_str
        raise ValueError(f"未知的按键: {key_str}")

    def _press_key(self, key):
        """
        发送单个按键或组合键 (通过 PostMessage)
        key 参数保持与原版兼容：
          - 单个字符串: 直接发送按键
          - 列表: 表示组合键 (内部格式)
        """
        hwnd = _get_foreground_window()

        if isinstance(key, list):
            # 组合键: 原版用 ahk 格式 (^a, +a, !a, #a)
            # 这里解析原版 format 并转为 SendMessage 调用
            # 实际上 key 是 _get_key 返回的 ahk 键名列表
            modifier_map = {
                'Control': 0x11,
                'Shift':   0x10,
                'Alt':     0x12,
                'LWin':    0x5B,
            }
            ahk_prefix_map = {
                'Control': '^',
                'Shift':   '+',
                'Alt':     '!',
                'LWin':    '#',
            }

            modifiers = []
            main_key_str = None

            for k in key:
                if k in modifier_map:
                    modifiers.append(modifier_map[k])
                elif k in ahk_prefix_map:
                    # 通过 ahk_prefix_map 反查
                    for mk, mv in ahk_prefix_map.items():
                        if mv == k:
                            modifiers.append(modifier_map.get(mk, 0))
                            break
                elif len(k) == 1:
                    # 单字符主键
                    main_key_str = k
                else:
                    # 可能是 ahk 特殊键名
                    vk = VK_MAP.get(k.upper())
                    if vk:
                        main_key_str = k
                    else:
                        main_key_str = k

            # 如果 main_key_str 未确定，尝试从 key 中找非修饰键
            if main_key_str is None:
                for k in key:
                    if k not in modifier_map and k not in ahk_prefix_map:
                        main_key_str = k
                        break

            if main_key_str is None:
                return  # 无法确定主键

            main_vk = VK_MAP.get(main_key_str.upper())
            if main_vk is None and len(main_key_str) == 1:
                main_vk = ord(main_key_str.upper())

            if main_vk is None:
                return

            # 按下所有修饰键
            for mod_vk in modifiers:
                _send_key(hwnd, mod_vk, is_up=False)

            # 按下主键
            _send_key(hwnd, main_vk, is_up=False)
            # 释放主键
            _send_key(hwnd, main_vk, is_up=True)

            # 释放所有修饰键（逆序）
            for mod_vk in reversed(modifiers):
                _send_key(hwnd, mod_vk, is_up=True)

        else:
            # 单键: 转为虚拟键码后发送
            if isinstance(key, str):
                vk = VK_MAP.get(key.upper())
                if vk is None and len(key) == 1:
                    vk = ord(key.upper())
                if vk is None:
                    return
            else:
                vk = key  # 可能是整数虚拟键码

            _send_key(hwnd, vk, is_up=False)
            _send_key(hwnd, vk, is_up=True)

    def simulate_keys(self, keys: List[str], times: int = 1, lag: float | int = 0):
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


def main(keys: List[str], times: int = 1, lag: float | int = 0):
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
