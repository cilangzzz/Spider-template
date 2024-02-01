import os


def FindMissTs(filePath):
    """
    查找缺失的Ts
    :param filePath:
    :return:
    """
    taskQueues = []
    finishIndex = []
    needFixIndex = []
    filePath = filePath
    with open(filePath + "/index.m3u8", "r") as fp:
        indexM3U8 = fp.read()
        fp.close()
    for i in indexM3U8.split("\n"):
        pass
        if i.endswith('.ts'):
            taskQueues.append(i)
    for i in os.listdir(filePath):
        if i.endswith('.ts'):
            finishIndex.append(int(i.replace(".ts", "")))
    for i in range(len(taskQueues)):
        needFixIndex.append(i)
    for i in finishIndex:
        needFixIndex.remove(i)
    return {
        "needFixIndex": needFixIndex,
        "taskQueues": taskQueues,
    }
