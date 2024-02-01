"""

"""
GlobalPath = r"E:\Cache\normal\save\\"


def GetCurrentPath(absolutePath):
    """
    绝对路径
    :param absolutePath:
    :return:
    """
    return GlobalPath + absolutePath


def PathAdapter(strPath):
    """
    返回正确的路径
    :return:
    """
    # print("path: ", strPath)
    if r"E:/Cache/normal/save/" in strPath:
        return strPath.replace(r"E:/Cache/normal/save/", "")
    elif r"F:\req\spider-m3u8\save\\" in strPath:
        return strPath[len(r"F:\req\spider-m3u8\save\\") - 1:]
    elif r"E:\Cache\normal\save\\" in strPath:
        return strPath.replace(r"E:\Cache\normal\save\\", "")
    elif len(strPath) == 0:
        return ""
    return strPath.replace("save/", "").replace("\\", "/")
