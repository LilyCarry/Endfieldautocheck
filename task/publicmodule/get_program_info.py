import psutil
import win32gui
import win32process

def get_program_info(target_program: str) -> dict:
    """
    根据目标程序名关键字，获取第一个匹配且拥有可见窗口的程序的 PID 和 HWND。
    传参:str;输出:[pid,hwnd,match]
    """
    # 强制将输入转为小写
    search_name = target_program.lower()
    
    # 默认返回格式
    result = {'pid': '0', 'hwnd': 'none', 'match': False}
    # 遍历所有进程
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # 获取进程名并转为小写进行比较
            current_proc_name = proc.info['name'].lower()
            
            if search_name in current_proc_name:
                current_pid = proc.info['pid']
                
                # 寻找该 PID 对应的可见窗口句柄
                hwnds = []
                def callback(hwnd, extra):
                    if win32gui.IsWindowVisible(hwnd):
                        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                        if found_pid == current_pid:
                            extra.append(hwnd)
                
                win32gui.EnumWindows(callback, hwnds)
                
                # 如果找到了窗口句柄，则立即返回结果
                if hwnds:
                    return {
                        'pid': str(current_pid),
                        'hwnd': hwnds[0],
                        'match': True
                    }
                else:
                    # 如果该进程没有窗口，则继续循环寻找下一个同名进程
                    continue
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return result

# --- Debug 测试代码 ---
if __name__ == "__main__":
    # 示例：即使有多个同名进程，也会找到那个带窗口的
    test_name = input('测试...')
    print(f"正在深度搜索程序 (包含窗口检查): {test_name} ...")
    
    res = get_program_info(test_name)
    
    if res['match']:
        print(f"匹配成功！")
        print(f"PID: {res['pid']}")
        print(f"HWND: {res['hwnd']}")
    else:
        print("未找到匹配的程序或匹配的程序均无可见窗口。")
    
    print("最终输出:", res)