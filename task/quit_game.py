if __name__=='__main__':
    from publicmodule.get_program_info import *
else:
    from task.publicmodule.get_program_info import *#为了测试方便,只能使用屎山模式,防止因工作目录变化导致的导入问题
import os
import signal
import time
def main():
    print('开始退出程序')
    current_time=0;max_time=3
    while current_time<=max_time:
        exist=get_program_info('endfield.exe')['match'];pid=int(get_program_info('endfield.exe')['pid']) # type: ignore
        if exist:
            os.kill(pid, signal.SIGTERM)
            time.sleep(3)
        else:
            print('成功')
            return [True,'成功了,别看了']
    else:
        print('草,没杀掉')
        return [False,'失败了,原因:{}']
if __name__=='__main__':
    main()