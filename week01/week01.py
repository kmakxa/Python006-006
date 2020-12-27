import logging
import time
import os
from pathlib import Path
def callTime():
    curTime = time.strftime("%Y-%m-%d %X",time.localtime())
    logging.warning('func call time is ' + curTime)

def createLogFile(filePath):
    p = Path(filePath)
    dir = p.parent
    if not os.path.exists(dir):
        os.makedirs(dir)      

curDate = time.strftime("%Y%m%d",time.localtime())
path = '/var/log/python-' + curDate + '/xxxx.log'
createLogFile(path)
logging.basicConfig(filename=path,
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s %(name)-8s %(levelname)-8s [line:%(lineno)d] %(message)s')
if __name__ == '__main__':
    callTime()
