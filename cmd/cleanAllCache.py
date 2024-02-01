import os

from internal.cleanCache import CleanTsFile

if __name__ == '__main__':
    baseUrl = "../save"

    for i in os.listdir(baseUrl):
        if i == "Allindex" or i == "Test":
            continue
        for j in os.listdir(baseUrl + "/" + i):
            needClean = False
            for h in os.listdir(baseUrl + "/" + i + "/" + j):
                if "index.mp4" in h:
                    needClean = True
            if needClean:
                print(baseUrl + "/" + i + "/" + j)
                CleanTsFile(baseUrl + "/" + i + "/" + j)
