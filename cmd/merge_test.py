import os
import time

from getPath import PathAdapter, GetCurrentPath
from internal.cleanCache import CleanTsFile
from internal.merge import MergeTs


def getFinishTask():
    """
    获取完成的任务信息
    :return:
    """
    with open("finish.txt", "r", encoding="utf-8") as fp:
        context = fp.read()
        fp.close()
    taskList = context.split("\n")
    for i in taskList:
        if len(i) == 0:
            taskList.remove(i)
    return taskList


if __name__ == '__main__':
    while True:
        print(getFinishTask())
        for path in getFinishTask():
            absolutePath = PathAdapter(path)
            needMerge = True
            filePath = GetCurrentPath(absolutePath)
            for j in os.listdir(filePath):
                if "index.mp4" in j:
                    print("dontNeedMerge: ", filePath)
                    needMerge = False

            if needMerge and len(filePath) != 0:
                print("needMerge: ",filePath)
                MergeTs(filePath)

        for path in getFinishTask():
            absolutePath = PathAdapter(path)
            needMerge = True
            filePath = GetCurrentPath(absolutePath)
            if len(filePath) != 0:
                for j in os.listdir(filePath):
                    if "index.mp4" in j:
                        CleanTsFile(filePath)
        time.sleep(100)
    # CleanTsFile(filePath)
