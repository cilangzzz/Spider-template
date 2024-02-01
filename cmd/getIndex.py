import threading
import time

from tqdm import tqdm

from getPath import GetCurrentPath
from internal.network import GetMovieInfoById, GetMovieIndexM3U8Url, GetIndexM3U8, DownMovie
from internal.save import CreateFileDir, SaveFile

maxTask = 5
threadNum = 0

def task(movieId):
    global threadNum

    try:
        res = GetMovieInfoById(movieId)
        # print("获取电影信息")
        # print(res)
        # 电影名字
        movieName = res["res"]["movieName"]
        # 电影集数id
        movieIds = res["res"]["movieId"]
        # 集数
        integrates = res["res"]["integrates"]
        passIntegrates = []
        for i, e in enumerate(integrates):
            if i in passIntegrates:
                continue
            if i != 0:
                break
            # print("获取M3U8-Url")
            res = GetMovieIndexM3U8Url(movieIds[i])
            # print(res)
            # print(res["res"])
            host = res["res"]["host"]
            if "play.modujx.com" not in host:
                continue
            absolute = "AllIndex/" + str(movieId) + "-" +movieName
            absolute = absolute.replace(".", "")
            filePath = GetCurrentPath(absolute)
            print(f"{movieName} play.modujx.com movie {movieId}")
            CreateFileDir(filePath)
            SaveFile(filePath, str(movieId), "txt", str(movieId), "w")
    except Exception as e:
        thread = threading.Thread(target=task, args=(movieIdq,))
        thread.start()
        threadNum += 1
        print(f"err movieId {movieId}",e)
    finally:
        threadNum -= 1


if __name__ == '__main__':

    # 7180 1998 10991
    for movieIdq in tqdm(range(14494, 15500)):
        # print("\n\n")
        # print(f"movieId {movieIdq}")
        if threadNum <= maxTask:
            thread = threading.Thread(target=task, args=(movieIdq,))
            thread.start()
            threadNum += 1
        else:
            while True:
                if threadNum <= maxTask:
                    thread = threading.Thread(target=task, args=(movieIdq,))
                    thread.start()
                    threadNum += 1
                    break
        time.sleep(0.2)
