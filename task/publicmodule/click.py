#输入参数:[[x,y],mode,times,[tx,ty]
#[x,y]表示起始位置,或点击位置;
#mode指点击模式.有:点击,多次点击,拖动
#times指次数.若mode为 click,则点击 times 次;若为drag,则重复 times 次.
#[tx,ty] 只有mode = drag 时需要.从x,y drag到 tx,ty
# -*- coding: utf-8 -*-
"""
click.py - 鼠标控制模块
功能：实现鼠标点击、多次点击和拖动操作 (基于 SendMessage + SetCursorPos 重构)
依赖: ctypes (Windows 内置，无需额外安装)
"""

import time
import ctypes
from ctypes import wintypes

# ── Windows API 常量 ──────────────────────────────────────────────
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP   = 0x0202
MK_LBUTTON     = 0x0001

# ── 加载 user32.dll ───────────────────────────────────────────────
user32 = ctypes.windll.user32


def _get_window_at(x, y):
    """获取屏幕坐标 (x, y) 处的窗口句柄"""
    return user32.WindowFromPoint(wintypes.POINT(x, y))


def _screen_to_client(hwnd, x, y):
    """将屏幕坐标转换为指定窗口的客户区坐标"""
    pt = wintypes.POINT(x, y)
    user32.ScreenToClient(hwnd, ctypes.byref(pt))
    return pt.x, pt.y


def _send_click(hwnd, x, y, down=True):
    """向目标窗口发送鼠标左键按下/释放消息"""
    cx, cy = _screen_to_client(hwnd, x, y)
    lparam = (cy << 16) | (cx & 0xFFFF)
    if down:
        user32.PostMessageW(hwnd, WM_LBUTTONDOWN, MK_LBUTTON, lparam)
    else:
        user32.PostMessageW(hwnd, WM_LBUTTONUP, 0, lparam)


# ═══════════════════════════════════════════════════════════════════
#  公共接口 — 与原版完全一致的签名与返回值
# ═══════════════════════════════════════════════════════════════════

def main(pos, mode='click', times=1, target_pos=None, lag=0.05):
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
        lag: 每次操作延迟秒 (int/float)

    返回:
        bool: 操作是否成功

    示例:
        >>> click([100, 200], mode='click', times=2)  # 在(100,200)双击
        >>> click([100, 200], mode='drag', times=1, target_pos=[300, 400])  # 拖动
    """
    try:
        x, y = pos

        if mode == 'click':
            # 移动光标到指定位置
            user32.SetCursorPos(x, y)
            time.sleep(0.05)  # 短暂延迟确保移动完成

            # 获取目标窗口
            hwnd = _get_window_at(x, y)

            # 执行指定次数的点击
            for _ in range(times):
                _send_click(hwnd, x, y, down=True)   # 按下
                time.sleep(lag)
                _send_click(hwnd, x, y, down=False)  # 释放
                time.sleep(lag)

            print(f"已在 ({x}, {y}) 点击 {times} 次")
            return True

        elif mode == 'drag':
            if target_pos is None:
                print("错误：拖动模式需要提供 target_pos 参数 [tx, ty]")
                return False

            tx, ty = target_pos

            for i in range(times):
                # 移动到起始位置
                user32.SetCursorPos(x, y)
                time.sleep(0.05)
                hwnd_start = _get_window_at(x, y)

                # 在起始位置按下
                _send_click(hwnd_start, x, y, down=True)
                time.sleep(lag)

                # 移动到目标位置
                user32.SetCursorPos(tx, ty)
                time.sleep(0.05)
                hwnd_end = _get_window_at(tx, ty)

                # 在目标位置释放
                _send_click(hwnd_end, tx, ty, down=False)
                time.sleep(lag)

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
    pt = wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return [pt.x, pt.y]


def move_to(x, y):
    """移动鼠标到指定位置"""
    user32.SetCursorPos(x, y)
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
    main(current_pos, mode='click', times=2)
