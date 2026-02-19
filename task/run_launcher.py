#启动启动器.暂时先支持b服.

import time
import subprocess
from publicmodule.capture_screen import *
from publicmodule.opencv_compare import *
from publicmodule.read_config import *
from publicmodule.get_program_info import *
config=read_config()
max_time=config['run_max_time'];path=config['launcher_path']
current_time=0#这里记得改config
print('正在启动启动器...')
#第一个环节:直接run启动器
while current_time<=max_time:#记得控制运行次数
    print(f'运行第{current_time}次:')
    subprocess.run([path,"--nogui","--xxmi","EFMI"])
    print('等待120秒')
    time.sleep(120)
    current_time+=1
    if get_program_info('endfield.exe')['match']:
        break
else:#失败
    print('失败!')
    print('请自行检查path是否存在,或是调大run_max_time')
    print('程序即将退出')
if get_program_info('endfield.exe')['match']:
    print('成功')
#    capture_result = capture_screen()
#    if capture_result[0]:
#        print(fr'截屏路径:{capture_result[1]}')
#        path=capture_result[1]
#        compare_result=opencv_compare(['task_bar_endfield_bili_small.png',path,0.9,0,[[None,None],[None,None]]])
