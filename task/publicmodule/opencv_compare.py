import cv2
import numpy as np
import os

def opencv_compare(input_data: list) -> list:
    """
    input_data 结构:
    [0]: 目标图片名 (target_pic 文件夹下)
    [1]: 截图文件名 (sc 文件夹下)
    [2]: 精度要求 (float, 如 0.8)
    [3]: 灰度匹配开关 (0 为关, 1 为开)
    [4]: 区域要求 [[起始x, y], [终止x, y]] 或 [[None, None], [None, None]]
    
    返回结构:
    [True/False, [中心x, 中心y], 实际精度, '反馈信息']
    """
    
    # 0. 路径准备
    # 获取当前文件所在目录 (publicmodule)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 定位 target_pic 和 sc 文件夹
    target_dir = os.path.abspath(os.path.join(base_dir, "..", "target_pic"))
    sc_dir = os.path.abspath(os.path.join(base_dir, "..", "sc"))
    
    target_path = os.path.join(target_dir, input_data[0])
    sc_path = os.path.join(sc_dir, input_data[1])
    
    # 1. 文件存在性检查
    missing_files = []
    if not os.path.exists(target_path):
        missing_files.append(f"target_pic/{input_data[0]}")
    if not os.path.exists(sc_path):
        missing_files.append(f"sc/{input_data[1]}")
    
    if missing_files:
        return [False, [0, 0], 0, f"{' 和 '.join(missing_files)} 不存在!"]

    # 2. 读取图片
    # 使用 cv2.imread 读取图片
    template = cv2.imread(target_path)  # 目标小图
    full_img = cv2.imread(sc_path)      # 原始大截图
    
    if template is None or full_img is None:
        return [False, [0, 0], 0, "图片读取失败，请检查格式是否损坏"]

    # 3. 区域裁剪 (ROI)
    roi_region = input_data[4]
    offset_x, offset_y = 0, 0
    
    # 判断是否指定了有效的裁剪区域
    if roi_region[0][0] is not None and roi_region[1][0] is not None:
        try:
            x1, y1 = roi_region[0]
            x2, y2 = roi_region[1]
            # 裁剪图片: [y_start:y_end, x_start:x_end]
            full_img = full_img[y1:y2, x1:x2]
            # 记录偏移量，用于后续还原真实像素坐标
            offset_x, offset_y = x1, y1
            
            if full_img.size == 0:
                return [False, [0, 0], 0, "裁剪区域无效(尺寸为0)"]
        except Exception as e:
            return [False, [0, 0], 0, f"裁剪操作报错: {str(e)}"]

    # 4. 灰度匹配处理
    if input_data[3] == 1:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        full_img = cv2.cvtColor(full_img, cv2.COLOR_BGR2GRAY)

    # 5. 执行模板匹配
    # 使用 TM_CCOEFF_NORMED (归一化相关系数匹配)，结果在 0-1 之间
    res = cv2.matchTemplate(full_img, template, cv2.TM_CCOEFF_NORMED)
    
    # 获取最大匹配度及其位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    # max_loc 是匹配区域的左上角坐标 (x, y)
    matched_x, matched_y = max_loc
    
    # 获取模板图片的宽高，用于计算中心点
    if input_data[3] == 1:
        t_h, t_w = template.shape
    else:
        t_h, t_w, _ = template.shape
    
    # 6. 计算匹配中心并在原图还原坐标
    center_x = int(offset_x + matched_x + t_w / 2)
    center_y = int(offset_y + matched_y + t_h / 2)
    
    accuracy_required = input_data[2]
    
    # 7. 结果判定
    if max_val >= accuracy_required:
        return [True, [center_x, center_y], round(float(max_val), 3), '']
    else:
        return [
            False, 
            [0, 0], 
            round(float(max_val), 3), 
            f"不匹配.需求精度:{accuracy_required:.3f},实际最大精度:{max_val:.3f}"
        ]

# --- Debug 测试代码 ---
if __name__ == "__main__":
    # 模拟输入数据
    # 假设你 sc 文件夹下有一个 1.png，target_pic 下有一个 2.png
    test_input = [
        "20260207_2155.png",      # 目标小图
        "20260207_2155.png",    # 截图大图
        0.5,                    # 精度
        0,                      # 灰度开关
        [[None, None], [None, None]] # 区域限制
    ]
    
    print("正在进行 OpenCV 匹配测试...")
    result = opencv_compare(test_input)
    print(f"返回列表: {result}")