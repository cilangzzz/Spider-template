from internal.network import GetMovieInfoById, GetMovieIndexM3U8Url, GetIndexM3U8, DownMovie, ReDownMovie
from internal.save import CreateFileDir, SaveFile

if __name__ == '__main__':
    pass
    # # 13059
    # res = GetMovieInfoById(12497)
    # print("获取电影信息")
    # print(res)
    # print(res["res"])
    # CreateFileDir(res["res"]["movieName"])
    # # 电影名字
    # movieName = res["res"]["movieName"]
    # # 电影集数id
    # movieIds = res["res"]["movieId"]
    # # 集数
    # integrates = res["res"]["integrates"]
    # for i,e in enumerate(integrates):
    #     if i == 0:
    #         continue
    #     filePath = movieName + "/" + e + movieIds[i]
    #     print(filePath)
    #     CreateFileDir(filePath)
    #     print("获取M3U8-Url")
    #     res = GetMovieIndexM3U8Url(res["res"]["movieId"][i])
    #     print(res)
    #     print(res["res"])
    #     print("获取索引M3U8")
    #     res = GetIndexM3U8(res["res"]["url"],'https://play.modujx.com/')
    #     SaveFile(filePath, "init", "m3u8", res["res"]["file1"], "w")
    #     SaveFile(filePath, "index", "m3u8", res["res"]["file2"], "w")
    #     print("下载电影")
    #     DownMovie(res["res"]["file2"], filePath, 'https://play.modujx.com/',dnAsync=True,dnThreadNum=5)
    #     print("下载完成")

    # res = GetMovieIndexM3U8Url("358-1-1")
    # print(res)
    # print(res["res"])
    # filePath = "../save/" + "Test/" + "第一集"
    # res = GetIndexM3U8(res["res"]["url"])
    # SaveFile(filePath, "index", "m3u8", res["res"]["file"],"w")
    # DownMovie(res["res"]["file"],filePath)

