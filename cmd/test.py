import time

from tqdm import tqdm

from internal.cleanCache import CleanTsFile
from internal.fix import FindMissTs
from internal.merge import MergeTs
from internal.network import FixMissingTs, ReDownMovie

if __name__ == '__main__':
    # MergeTs("Test/第一集")
    filePath = "save/甜美姐姐！/第1集13634-1-1".replace("save/","")

    # ReDownMovie(filePath, 'https://play.modujx.com/', dnAsync=True, dnThreadNum=6)

    # MergeTs(filePath)

    # FixMissingTs(filePath, 'https://play.modujx.com/', dnAsync=True, dnThreadNum=3)

    res = FindMissTs(filePath)
    while len(res["needFixIndex"]) != 0:

        FixMissingTs(filePath,'https://play.modujx.com/', dnAsync=True, dnThreadNum=10)
        time.sleep(15)
        res = FindMissTs(filePath)
        print(res["needFixIndex"])
        for i in tqdm(range(30)):
            time.sleep(1)
        res = FindMissTs(filePath)

    print("合并视频")
    MergeTs(filePath)
    print("合并完成")

    # CleanTsFile(filePath)