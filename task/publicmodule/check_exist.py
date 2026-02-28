#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到路径（用于单独调试）
project_root = Path(__file__).parent.parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 绝对导入
from task.publicmodule.get_program_info import get_program_info

def check_exist():
    return get_program_info('Endfield.exe')['match']

if __name__ == '__main__':
    print(check_exist())