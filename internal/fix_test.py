from internal.fix import FindMissTs
from internal.merge import MergeTs
from internal.network import FixMissingTs, ReDownMovie

if __name__ == '__main__':
    # MergeTs("Test/第一集")
    filePath = "save/JK和猥琐便利店店长/第3集13114-1-3".replace("save/", "")

    # ReDownMovie(filePath, 'https://play.modujx.com/', dnAsync=True, dnThreadNum=6)

    # MergeTs(filePath)

    # CleanTsFile(filePath)

    # FixMissingTs(filePath, 'https://play.modujx.com/', dnAsync=True, dnThreadNum=3)

    res = FindMissTs(filePath)
    print(res)
    print(len(res["needFixIndex"]))