from .getPath import GetCurrentPath
from internal.network import GetMovieInfoById, GetMovieIndexM3U8Url, GetIndexM3U8, DownMovie
from internal.save import CreateFileDir, SaveFile

if __name__ == '__main__':
    res = GetMovieInfoById(13058)
    print("获取电影信息")
    print(res)
    print(res["res"])
    # 电影名字
    movieName = res["res"]["movieName"]
    # 电影集数id
    movieIds = res["res"]["movieId"]
    # 集数
    integrates = res["res"]["integrates"]
    filePath = GetCurrentPath(movieName)
    CreateFileDir(res["res"]["movieName"])
    passIntegrates = []
    for i, e in enumerate(integrates):
        if i in passIntegrates:
            continue
        absolutePath = movieName + "/" + e + movieIds[i]
        filePath = GetCurrentPath(absolutePath)
        print(filePath)
        CreateFileDir(filePath)
        print("获取M3U8-Url")
        res = GetMovieIndexM3U8Url(movieIds[i])
        host = res["res"]["host"]
        print(res)
        print(res["res"])
        try:
            print("获取索引M3U8")
            res = GetIndexM3U8(res["res"]["url"], host)
            SaveFile(filePath, "host", "txt", host, "w")
            SaveFile(filePath, "init", "m3u8", res["res"]["file1"], "w")
            SaveFile(filePath, "index", "m3u8", res["res"]["file2"], "w")
            continue
        except Exception as e:
            print(f"索引初始化失败 {e} 跳过本集 {filePath} ")
            continue
        print("下载电影")
        DownMovie(res["res"]["file2"], filePath, host, dnAsync=True, dnThreadNum=5)
        print("下载完成")

    # res = GetMovieIndexM3U8Url("358-1-1")
    # print(res)
    # print(res["res"])
    # filePath = "../save/" + "Test/" + "第一集"
    # res = GetIndexM3U8(res["res"]["url"])
    # SaveFile(filePath, "index", "m3u8", res["res"]["file"],"w")
    # DownMovie(res["res"]["file"],filePath)
