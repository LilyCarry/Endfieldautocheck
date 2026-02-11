import os
import datetime
import win32gui
import win32ui
import win32con
import win32api
from PIL import Image

def capture_screen() -> list:
    """
    截取当前主屏幕全屏。
    返回格式: [成功与否(True/False), '信息']
    """
    try:
        # 1. 确定保存路径
        rel_dir = os.path.join("..", "sc")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        abs_save_dir = os.path.abspath(os.path.join(base_dir, rel_dir))
        
        if not os.path.exists(abs_save_dir):
            os.makedirs(abs_save_dir)

        # 2. 构造文件名 (精确到秒)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}.png"
        abs_file_path = os.path.join(abs_save_dir, file_name)

        # 3. 获取全屏尺寸 (主显示器)
        width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        # 4. 获取桌面窗口句柄并创建 DC
        hwnd = win32gui.GetDesktopWindow()
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        # 5. 创建位图对象
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)

        # 6. 直接进行像素拷贝 (BitBlt 截取屏幕最快)
        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

        # 7. 转换为 PIL Image 并保存
        bmp_info = save_bitmap.GetInfo()
        bmp_str = save_bitmap.GetBitmapBits(True)
        im = Image.frombuffer('RGB', (bmp_info['bmWidth'], bmp_info['bmHeight']), bmp_str, 'raw', 'BGRX', 0, 1)

        # 8. 释放资源
        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        # 9. 物理保存
        im.save(abs_file_path)
        return [True, fr'{file_name}']

    except Exception as e:
        return [False, f"全屏截图失败: {str(e)}"]

# --- Debug 测试代码 ---
if __name__ == "__main__":
    print("正在尝试全屏截图...")
    res = capture_screen()
    print(f"结果: {res}")