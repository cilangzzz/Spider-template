import threading
import time

from internal import init
from internal.find import findByGame, findByGaming, findByVac, findByGamingStatus
from internal.search import searchSteamUser, getSteamInfo


def newTask(tpage):
    print(f"搜索第{tpage}页")
    # page = i
    params = f'text={kw}&filter=users&sessionid={sessionid}&steamid_user={steamid_user}&page={tpage}'
    # print(params)
    # 搜索结果
    resSteamUrls, _ = searchSteamUser(params)
    for j in resSteamUrls:
        if j not in steamUrls:
            steamUrls.append(j)
    # print(resSteamUrls)
        # # steam 信息
    resSteamUserInfoList = getSteamInfo(resSteamUrls,tpage)
    for i in resSteamUserInfoList:
        steamUserInfoList.append(i)


if __name__ == "__main__":
    # 匹配的结果 steamurls
    # steamUrls = []
    # 做挂车的挂钩
    # kw = "残局大师小呆呆"
    # 测试数据
    kw = "手柄锁"
    sessionid = init.g_sessionID
    steamid_user = init.g_steamID
    params = f'text={kw}&filter=users&sessionid={sessionid}&steamid_user={steamid_user}'
    # 搜索结果
    steamUrls, countTotal = searchSteamUser(params)
    print(f"一共 {countTotal} 匹配结果")
    page = (countTotal // 20) + 1 if countTotal % 20 != 0 else countTotal // 20
    print(f"一共 {page} 页")
    # steam个人信息
    steamUserInfoList = []
    # 获取所有匹配搜索结果的steamUrls
    # 异步操作会导致400
    if page > 10:
        # 大于十页放弃搜索
        pass
    else:
        for i in range(page):
            thread = threading.Thread(target=newTask,args=[i])
            thread.start()
    # print(len(steamUrls))

    #     匹配到的结果
    # 等待线程完成,可以自行用waitgroup实现
    # time.sleep(200)
    input("等待线程完成后输入")
    # 离线匹配
    # 正在玩游戏
    print("正在玩游戏")
    for i in findByGamingStatus(steamUserInfoList):
        print(i)
    # 最近玩过 THE FINALS
    print("最近玩过 THE FINALS")
    for i in findByGame(steamUserInfoList, "THE FINALS"):
        print(i)
    # 最近玩过 APEX
    print("最近玩过 APEX")
    for i in findByGame(steamUserInfoList, "APEX"):
        print(i)
    # 正在玩 THE FINALS
    print("正在玩 THE FINALS")
    for i in findByGaming(steamUserInfoList, "THE FINALS"):
        print(i)
    # 有Vac记录
    print('有Vac记录')
    for i in findByVac(steamUserInfoList):
        print(i)