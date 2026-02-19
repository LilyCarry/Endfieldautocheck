#启动启动器.暂时先支持b服.

from publicmodule.capture_screen import *
from publicmodule.opencv_compare import *
max_time=2;current_time=0
print('正在启动启动器...')
while current_time<=max_time:
    print(f'运行第{current_time}次:')
    capture_result = capture_screen()
    if capture_result[0]:
        print(fr'截屏路径:{capture_result[1]}')
        path=capture_result[1]
        compare_result=opencv_compare(['task_bar_endfield_bili_small.png',path,0.9,0,[[None,None],[None,None]]])
