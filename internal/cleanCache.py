import os

from tqdm import tqdm


def CleanTsFile(filepath):
    """
    清楚Ts文件
    :param filepath:
    :return:
    """
    filepath = filepath
    delFileByExt(filepath, ".ts")


def delFileByExt(filepath, ext):
    """
    删除文件通过ts后缀
    :param filepath:
    :param ext:
    :return:
    """
    for i in tqdm(os.listdir(filepath)):
        if i.endswith(ext):
            os.remove(filepath + "/" + i)
