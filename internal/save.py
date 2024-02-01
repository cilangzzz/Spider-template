"""
save.py 保存文件
"""
import os.path

GlobalPath = ""


# GlobalPath = "E:/Cache/normal/"

def CreateFileDir(dirName):
    """
    创建文件夹
    :param dirName:
    :return:
    """
    filePath = GlobalPath + dirName
    print(filePath)
    # filePath = "../../save/" + dirName
    if not os.path.exists(filePath):
        os.makedirs(filePath)


def SaveFile(filePath, fileName, ext, context, mode="w"):
    """
    保存文件
    :param mode:
    :param context:
    :param filePath:
    :param fileName:
    :param ext:
    :return:
    """
    CreateFileDir(filePath)
    filePath = GlobalPath + filePath + "/" + fileName + "." + ext
    # filePath = "../../save/" + filePath + "/" + fileName + "." + ext
    with open(filePath, mode) as fp:
        fp.write(context)
        fp.close()
