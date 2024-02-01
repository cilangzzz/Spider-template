import os
import time

from tqdm import tqdm

from getPath import PathAdapter, GetCurrentPath
from internal.cleanCache import CleanTsFile
from internal.fix import FindMissTs
from internal.merge import MergeTs
from internal.network import FixMissingTs, ReDownMovie
from internal.save import SaveFile


def readTodoTask():
    """
    返回需要做的任务列表
    :return:
    """
    with open("todo.txt", "r", encoding="utf-8") as fp:
        todoDown = fp.read()
        fp.close()
    taskList = todoDown.split("\n")
    for i in taskList:
        if len(i) == 0:
            taskList.remove(i)
    return taskList


def appendFinish(filePath):
    """
    追加任务信息
    :param filePath:
    :return:
    """
    with open("finish.txt", "r", encoding="utf-8") as fp:
        context = fp.read()
        fp.close()
    if filePath not in context.split("\n"):
        with open("finish.txt", "a+", encoding="utf-8") as fp:
            fp.write(filePath + "\n")
            fp.close()


if __name__ == '__main__':
    # 标记已在todo列表的视频
    for path in readTodoTask():
        absolutePath = PathAdapter(path)
        filePath = GetCurrentPath(absolutePath)
        print(filePath)
        SaveFile(filePath, "worked", "label", "todoLabel", "w")

    for path in readTodoTask():
        print(path)
        absolutePath = PathAdapter(path)
        filePath = GetCurrentPath(absolutePath)
        # MergeTs("Test/第一集")
        # filePath = "save/御姐→正太←御姐/第1集13156-1-1".replace("save/","")
        #
        # # ReDownMovie(filePath, 'https://play.modujx.com/', dnAsync=True, dnThreadNum=6)
        #
        # # MergeTs(filePath)
        #
        # # FixMissingTs(filePath, 'https://play.modujx.com/', dnAsync=True, dnThreadNum=3)
        #
        print(filePath)
        res = FindMissTs(filePath)
        while len(res["needFixIndex"]) != 0:
            if "index.mp4" in os.listdir(filePath):
                break
            FixMissingTs(filePath, 'https://play.modujx.com/', dnAsync=True, dnThreadNum=10)
            for i in tqdm(range(30)):
                time.sleep(0.5)
            res = FindMissTs(filePath)
            print(res["needFixIndex"])
            if len(res["needFixIndex"]) < 20:
                for i in tqdm(range(30)):
                    time.sleep(0.1)
            else:
                for i in tqdm(range(30)):
                    time.sleep(0.7)
            res = FindMissTs(filePath)
        # print("合并视频")
        # MergeTs(filePath)
        # print("合并完成")
        appendFinish(filePath)
        SaveFile(filePath, "finish", "label", "had finish", "w")
        # CleanTsFile(filePath)
