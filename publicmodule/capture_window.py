import os
import ctypes
import datetime
import win32gui
import win32ui
import win32con
from PIL import Image

#从同级目录下的 get_program_info.py 导入 get_program_info 函数
from get_program_info import get_program_info

def capture_window(program_info: dict) -> list:
    """
    对指定句柄的窗口进行截图。
    返回格式: [True, '../sc/文件名.png'] 或 [False, '原因']
    """
    # 1. 检查程序信息是否存在
    if not program_info.get('match') or program_info.get('hwnd') == 'none':
        return [False, "不存在该程序"]

    hwnd = program_info['hwnd']
    
    # 2. 使用 IsIconic 检查窗口是否最小化
    if win32gui.IsIconic(hwnd):
        return [False, "窗口处于最小化状态，无法截图"]
    
    # 检查句柄是否依然有效
    if not win32gui.IsWindow(hwnd):
        return [False, "句柄已失效或窗口已关闭"]

    try:
        # 3. 确定保存路径和文件名
        # 模块在 publicmodule/，目标在 ../sc/
        rel_dir = os.path.join("..", "sc")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        abs_save_dir = os.path.abspath(os.path.join(base_dir, rel_dir))
        
        if not os.path.exists(abs_save_dir):
            os.makedirs(abs_save_dir)

        # 构造文件名 (YYYYMMDD_HHmm)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        file_name = f"{timestamp}.png"
        
        # 绝对路径用于写入，相对路径用于返回
        abs_file_path = os.path.join(abs_save_dir, file_name)
        relative_path = os.path.join(rel_dir, file_name)

        # 4. 获取窗口宽高
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bot - top

        # 5. 使用 ctypes 调用 PrintWindow API (支持被遮挡窗口)
        PW_RENDERFULLCONTENT = 2
        
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)

        # 核心：调用 user32.dll 的 PrintWindow
        result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), PW_RENDERFULLCONTENT)
        
        if result != 1:
            # 失败则尝试普通模式
            ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0)

        # 6. 转换为 PIL Image
        bmp_info = save_bitmap.GetInfo()
        bmp_str = save_bitmap.GetBitmapBits(True)
        im = Image.frombuffer(
            'RGB', 
            (bmp_info['bmWidth'], bmp_info['bmHeight']), 
            bmp_str, 'raw', 'BGRX', 0, 1
        )

        # 7. 释放资源
        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        # 8. 保存并返回相对路径
        im.save(abs_file_path)
        return [True, relative_path]

    except Exception as e:
        return [False, f"API调用报错: {str(e)}"]

# --- Debug 测试代码 ---
if __name__ == "__main__":
    target_name = input("请输入程序名关键字进行截图测试: ")
    info = get_program_info(target_name)
    
    if info['match']:
        print(f"找到程序，HWND: {info['hwnd']}。尝试截图...")
        res = capture_window(info)
        if res[0]:
            print(f"成功！保存位置: {res[1]}")
        else:
            print(f"失败！原因: {res[1]}")
    else:
        print("未找到目标程序。")