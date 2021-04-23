# -*-coding:utf-8-*-
import traceback
from plugin import run

def runON():
    # 异常重启
    try:
        run.run()
    except:
        traceback.print_exc()
        # 重启
        runON()


# 瞎玩的Python，不知道是不是这么用的，别喷awa1111
if __name__ == "__main__":
    runON()
        
