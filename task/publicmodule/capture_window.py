#暂时弃用
import os
import datetime
import win32gui
import bettercam # 使用比 dxcam 更现代的 bettercam
from PIL import Image

# 导入同级目录下的模块
from get_program_info import get_program_info

# 全局初始化 camera，避免重复创建销毁带来的性能损耗
# output_color='RGB' 直接适配 PIL 和 OpenCV
camera = bettercam.create(output_color='RGB')

def capture_window(program_info: dict) -> list:
    """
    切勿调用
    已证实无效
    """
    # 1. 基础检查
    if not program_info.get('match') or program_info.get('hwnd') == 'none':
        return [False, "不存在该程序"]

    hwnd = program_info['hwnd']
    
    if win32gui.IsIconic(hwnd):
        return [False, "窗口处于最小化状态，无法截图"]
    
    if not win32gui.IsWindow(hwnd):
        return [False, "句柄已失效或窗口已关闭"]

    try:
        # 2. 准备路径和文件名 (精确到秒 %S)
        rel_dir = os.path.join("..", "sc")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        abs_save_dir = os.path.abspath(os.path.join(base_dir, rel_dir))
        
        if not os.path.exists(abs_save_dir):
            os.makedirs(abs_save_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}.png"
        abs_file_path = os.path.join(abs_save_dir, file_name)
        relative_path = os.path.join(rel_dir, file_name)

        # 3. 获取窗口坐标 (DX11 捕获需要屏幕坐标区域)
        rect = win32gui.GetWindowRect(hwnd)
        # rect = (left, top, right, bottom)
        
        # 4. 执行现代捕获 (直接从显卡缓冲区读取)
        # grab 会根据指定的 region 截取，这比全屏截图再裁剪快得多
        frame = camera.grab(region=rect)
        
        if frame is None:
            # 如果截图失败（通常是因为窗口在屏幕外），尝试将窗口激活后再试
            return [False, "截图返回为空，请确保窗口在显示范围内"]

        # 5. 转换并保存
        # bettercam 返回的是 numpy 数组，直接转 PIL
        img = Image.fromarray(frame)
        img.save(abs_file_path)
        
        return [True, relative_path]

    except Exception as e:
        return [False, f"DX11现代捕获失败: {str(e)}"]

# --- Debug 测试代码 ---
if __name__ == "__main__":
    target = input("请输入程序名关键字(DX11截图测试): ")
    info = get_program_info(target)
    if info['match']:
        print(f"找到窗口，正在调用 DXGI API 截图...")
        res = capture_window(info)
        print(f"结果: {res}")
    else:
        print("未找到程序")