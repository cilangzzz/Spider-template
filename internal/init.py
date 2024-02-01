"""
init.py 获取默认参数
"""
import random

import requests

from internal.parse import ParseHeader, ParseCookie


def GetDefaultHeader():
    """
    # getDefaultHeader 获取默认请求头 ./file/defaultHeader
    :return:
    """
    header = ""
    with open("../file/defaultHeader", "r", encoding="utf-8") as fp:
        header = ParseHeader(fp.read())
        fp.close()
    header["User-Agent"] = rangeUa()
    return header


def GetDefaultCookie():
    """
    # getDefaultCookie 获取默认Cookie ./file/defaultCookie
    :return:
    """
    cookies = ""
    with open("../file/defaultCookie", "r", encoding="utf-8") as fp:
        cookies = ParseCookie(fp.read())
        fp.close()
    return cookies


def rangeUa():
    """
    随机请求头
    :return:
    """
    uaPool = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5666.197 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0  uacq",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0 (Edition beta)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.9"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
    ]
    ran = random.Random()
    return uaPool[ran.randint(0, len(uaPool)-1)]

