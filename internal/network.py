import datetime
import json
import os
import threading
import time
from datetime import datetime
from urllib.parse import urlparse

import requests
from lxml import html
from tqdm import tqdm

from internal.errlog import ErrLog
from internal.init import GetDefaultHeader, GetDefaultCookie
from internal.merge import MergeTs
from internal.regex import GetAllScriptFromHtml, GetScriptVariableByVariableName
from internal.save import SaveFile

# 任务线程
threadTaskNum = 0
# 默认超时
defaultTimeout = 15


def GetMovieInfoById(id):
    """
    通过电影Id获取网页信息
    :param id:
    :return:
    """
    startTime = datetime.now()
    url = f"https://huolangdm.com/iNewsId/{id}.html"
    res = requests.get(url, headers=GetDefaultHeader(), cookies=GetDefaultCookie())

    res.encoding = "utf-8"
    endTime = datetime.now()
    return {
        "res": parseMovieInfo(res.text),
        "spend": startTime - endTime
    }


def parseMovieInfo(strMovieHtml):
    """
    通过电影首页解析电影信息(集数,推荐电影)
    :param strMovieHtml:
    :return:
    """
    et = html.fromstring(strMovieHtml)
    movieName = et.xpath('//div[@class="media-left"]//a//@title')[0]
    # print(e.xpath('//div[@class="tab-content ff-playurl-tab mt-2"]//ul//li//text()'))

    integrates = et.xpath('//div[@class="tab-content ff-playurl-tab mt-2"]//ul//li//text()')
    # print(e.xpath('//div[@class="tab-content ff-playurl-tab mt-2"]//ul//li//a//@href'))
    movieId = et.xpath('//div[@class="tab-content ff-playurl-tab mt-2"]//ul//li//a//@href')
    for i, e in enumerate(movieId):
        movieId[i] = e.replace("/iNewsId/", "").replace(".html", "")
    # print(movieId)
    # index = zip(integrates, movieId)
    # print(index)
    # print(et.xpath('//ul[@class="vod-item-img ff-img-215"]//li//h3//text()'))
    recommendMovieName = et.xpath('//ul[@class="vod-item-img ff-img-215"]//li//h3//text()')
    # print(et.xpath('//ul[@class="vod-item-img ff-img-215"]//li//h3//a//@href'))
    recommendMovieId = et.xpath('//ul[@class="vod-item-img ff-img-215"]//li//h3//a//@href')
    for i, e in enumerate(recommendMovieId):
        recommendMovieId[i] = e.replace("/iNewsId/", "").replace(".html", "")
    # recommendMovie = zip(recommendMovieName, recommendMovieId)
    return {
        "movieName": movieName,
        "integrates": integrates,
        "movieId": movieId,
        "recommendMovieName": recommendMovieName,
        "recommendMovieId": recommendMovieId,
    }


def GetMovieIndexM3U8Url(integrates):
    """
    通过电影集数id获取index.M3U8
    :param integrates:
    :return:
    """
    startTime = datetime.now()
    url = f"https://huolangdm.com/iNewsId/{integrates}.html"
    res = requests.get(url, headers=GetDefaultHeader(), cookies=GetDefaultCookie())
    res.encoding = "utf-8"
    scriptTexts = GetAllScriptFromHtml(res.text)
    m3u8Url = []
    for i in scriptTexts:
        if "index.m3u8" in i:
            m3u8Url = json.loads(GetScriptVariableByVariableName(i, "cms_player")[0].split("=")[1].replace(";", ""))[
                "url"]

    endTime = datetime.now()
    return {
        "res": {
            "host": "https://" + urlparse(m3u8Url.replace("\/", "/")).netloc,
            "url": m3u8Url
        },
        "spend": startTime - endTime
    }


def GetIndexM3U8(url, host=""):
    """
    下载m3u8
    :param url:
    :param host:
    :return:
    """
    res2 = ""
    startTime = datetime.now()
    print({"res": {"init.m3u8": url}})
    res1 = requests.get(url, headers=GetDefaultHeader(), cookies=GetDefaultCookie(), timeout=defaultTimeout)
    # res1.encoding = "utf-8"
    time.sleep(0.5)
    for i in res1.text.split("\n"):
        if "index.m3u8" in i:
            print({"res": {"index.m3u8": host + i}})
            res2 = requests.get(host + i, headers=GetDefaultHeader(), cookies=GetDefaultCookie(), timeout=defaultTimeout)
            break
    endTime = datetime.now()
    return {
        "res": {
            "file1": res1.text,
            "file2": res2.text
        },
        "spend": startTime - endTime
    }


def DownMovie(indexM3U8, filePath, host="", dnAsync=False, dnThreadNum=4):
    """
    根据Index M3U8 下载电影
    :param dnThreadNum:
    :param dnAsync:
    :param host:
    :param indexM3U8:
    :param filePath: 保存的路径
    :return:
    """
    index = 0
    taskQueues = []
    global threadTaskNum
    for i in indexM3U8.split("\n"):
        if i.endswith('.ts'):
            taskQueues.append(i)
    for url in tqdm(taskQueues):
        if dnAsync:
            while threadTaskNum == dnThreadNum:
                pass
            tread = threading.Thread(target=downloadTsTask, args=(url, filePath, index, host))
            tread.start()
            index += 1
            threadTaskNum += 1
        else:
            try:
                res = downloadTs(url, host)
                SaveFile(filePath, str(index), "ts", res["res"]["file"], "wb+")
                index += 1
            except requests.exceptions.ChunkedEncodingError as e:
                ErrLog("network.py", filePath, f'网络链接断开 请手动下载{host + url} 并且重命名为{index}.ts', e,
                       "fixTs")
            except Exception as e:
                ErrLog("network.py", filePath, f'未知错误 请手动下载{host + url} 并且重命名为{index}.ts', e, "fixTs")
    MergeTs(filePath)


def ReDownMovie(filePath, host="", dnAsync=False, dnThreadNum=5):
    """
    重新下载ts分段
    :param dnThreadNum:
    :param dnAsync:
    :param filePath:
    :param host:
    :return:
    """
    filePath = "../save/" + filePath
    global threadTaskNum
    indexM3U8 = ""
    taskQueues = []
    finishIndex = 0
    with open(filePath + "/index.m3u8", "r") as fp:
        indexM3U8 = fp.read()
        fp.close()
    for i in indexM3U8.split("\n"):
        if i.endswith('.ts'):
            taskQueues.append(i)
    for i in os.listdir(filePath):
        if i.endswith('.ts'):
            if int(i.replace(".ts", "")) > finishIndex:
                finishIndex = int(i.replace(".ts", ""))
    for index in tqdm(range(int(finishIndex), len(taskQueues))):
        url = taskQueues[index]
        if dnAsync:
            while threadTaskNum == dnThreadNum:
                pass
            print(f"fixing {host + url}   {index}.ts")
            tread = threading.Thread(target=downloadTsTask, args=(url, filePath, index, host))
            tread.start()
            threadTaskNum += 1
        else:
            try:
                pass
                print(f"fixing {host + url}   {index}.ts")
                res = downloadTs(url, host)
                SaveFile(filePath, str(index), "ts", res["res"]["file"], "wb+")
            except requests.exceptions.ChunkedEncodingError as e:
                ErrLog("network.py", filePath, f'网络链接断开 请手动下载{host + url} 并且重命名为{index}.ts', e,
                       "fixTs")
            except Exception as e:
                ErrLog("network.py", filePath, f'未知错误 请手动下载{host + url} 并且重命名为{index}.ts', e, "fixTs")


def FixMissingTs(filePath, host="", auto=True, byLog=False, dnAsync=False, dnThreadNum=5):
    """
    修复缺失的ts文件
    :param filePath:
    :param dnAsync:
    :param dnThreadNum:
    :param host:
    :param auto:
    :param byLog:
    :return:
    """
    global threadTaskNum
    indexM3U8 = ""
    taskQueues = []
    finishIndex = []
    needFixIndex = []
    filePath =  filePath
    with open(filePath + "/index.m3u8", "r") as fp:
        indexM3U8 = fp.read()
        fp.close()
    for i in indexM3U8.split("\n"):
        if i.endswith('.ts'):
            taskQueues.append(i)
    for i in os.listdir(filePath):
        if i.endswith('.ts'):
            finishIndex.append(int(i.replace(".ts", "")))
    for i in range(len(taskQueues)):
        needFixIndex.append(i)
    for i in finishIndex:
        needFixIndex.remove(i)
    print(f"missingIndex {needFixIndex}")
    for index in tqdm(needFixIndex):
        url = taskQueues[index]
        pass
        if dnAsync:
            while threadTaskNum == dnThreadNum:
                pass
            print(f"fixing {host + url}   {index}.ts")
            tread = threading.Thread(target=downloadTsTask, args=(url, filePath, index, host))
            tread.start()
            threadTaskNum += 1
            pass
        else:
            try:
                pass
                print(f"fixing {host + url}   {index}.ts")
                res = downloadTs(url, host)
                SaveFile(filePath, str(index), "ts", res["res"]["file"], "wb+")
                pass
            except requests.exceptions.ChunkedEncodingError as e:
                ErrLog("network.py", filePath, f'网络链接断开 请手动下载{host + url} 并且重命名为{index}.ts', e,
                       "fixTs")
            except Exception as e:
                ErrLog("network.py", filePath, f'未知错误 请手动下载{host + url} 并且重命名为{index}.ts', e, "fixTs")


def downloadTs(url, host=""):
    """
    下载ts分段
    :param host:
    :param url:
    :return:
    """
    startTime = datetime.now()
    res = requests.get(host + url, headers=GetDefaultHeader(), cookies=GetDefaultCookie(), timeout=defaultTimeout)
    endTime = datetime.now()
    return {
        "res": {
            "file": res.content
        },
        "spend": startTime - endTime
    }


def downloadTsTask(url, filePath, index, host="", tryFrequency=1):
    """
    1任务形式下载ts分段
    :param tryFrequency:
    :param filePath:
    :param index:
    :param host:
    :param url:
    :return:
    """
    global threadTaskNum
    tryLabel = 0
    while tryLabel < tryFrequency:
        try:
            res = downloadTs(url, host)
            SaveFile(filePath, str(index), "ts", res["res"]["file"], "wb+")
            threadTaskNum -= 1
            break
        except requests.exceptions.ChunkedEncodingError as e:
            ErrLog("network.py", filePath, f'网络链接断开 请手动下载{host + url} 并且重命名为{index}.ts', e, "fixTs")
        except Exception as e:
            ErrLog("network.py", filePath, f'未知错误 请手动下载{host + url} 并且重命名为{index}.ts', e, "fixTs")
        finally:
            tryLabel += 1
    threadTaskNum -= 1
