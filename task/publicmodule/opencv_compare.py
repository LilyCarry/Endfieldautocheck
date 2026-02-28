#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os

def main(input_data: list) -> list:
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
    # 获取当前文件所在目录 -> 向上3层到项目根
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    
    # 定位 target_pic 和 sc 文件夹
    target_dir = os.path.join(project_root, "target_pic")
    sc_dir = os.path.join(project_root, "sc")
    
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
    template = cv2.imread(target_path)
    full_img = cv2.imread(sc_path)
    
    if template is None or full_img is None:
        return [False, [0, 0], 0, "图片读取失败，请检查格式是否损坏"]

    # 3. 区域裁剪 (ROI)
    roi_region = input_data[4]
    offset_x, offset_y = 0, 0
    
    if roi_region[0][0] is not None and roi_region[1][0] is not None:
        try:
            x1, y1 = roi_region[0]
            x2, y2 = roi_region[1]
            full_img = full_img[y1:y2, x1:x2]
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
    res = cv2.matchTemplate(full_img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    matched_x, matched_y = max_loc
    
    if input_data[3] == 1:
        t_h, t_w = template.shape
    else:
        t_h, t_w, _ = template.shape
    
    # 6. 计算匹配中心并在原图还原坐标
    center_x = int(offset_x + matched_x + t_w / 2)
    center_y = int(offset_y + matched_y + t_h / 2)
    accuracy_required = float(input_data[2])#修复float与int比较
    
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
    source = input('输入目标小图: ')
    target = input('输入大图: ')
    val = float(input('输入精度: '))
    test_input = [
        source,
        target,
        val,
        0,
        [[None, None], [None, None]]
    ]
    
    print("正在进行 OpenCV 匹配测试...")
    result = main(test_input)
    print(f"返回列表: {result}")