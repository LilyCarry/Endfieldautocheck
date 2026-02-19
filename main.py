#注意!!!!!所有调用子文件夹模块都是相对路径导入!!记得改成:from task.publicmodule.get_program_info import *这样的格式!!
import task.run_launcher
import task.quit_game
from task.publicmodule.read_config import *
#下面是初始化:
main_config=read_config()
task_st=main_config['task_st']
launcher_result=task.run_launcher.main()
#接下来是简单逻辑,暂不按task_st处理:
if launcher_result[0]:
    task.quit_game.main()
else:
    print('退出失败')