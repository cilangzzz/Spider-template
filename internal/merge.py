from tqdm import tqdm


def MergeTs(filePath):
    """
    合并Ts分段
    :param filePath:
    :return:
    """
    count = 0
    filePath = filePath
    with open(f'{filePath + "/index.m3u8"}',"r") as fp2:
        for i in fp2.read().split("\n"):
            if ".ts" in i:
                count += 1
        fp2.close()
    with open(filePath + "/index.mp4", "ab+") as fp1:
        if count != 0:
            for i in tqdm(range(count)):
                try:
                    with open(filePath + "/" + str(i) + ".ts", "rb") as fp2:
                        fp1.write(fp2.read())
                        fp2.close()
                except:
                    pass
        fp1.close()