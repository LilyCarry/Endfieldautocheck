import ctypes
def turn_off_screen():
    """关闭电脑屏幕"""
    # 发送系统命令关闭屏幕
    ctypes.windll.user32.SendMessageA(0xFFFF, 0x112, 0xF170, 2)
if __name__=='__main__':
    turn_off_screen()