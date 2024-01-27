"""
init.py 获取默认参数
"""

from internal.parse import ParseHeader,ParseCookie

from fontTools.misc import etree
import re
import requests

# for i in script:
#     if "g_sessionID" in i:
#         for h in re.compile(r'g_sessionID\s*=\s*[^;]+;').findall(i):
#             g_sessionID = h.replace(' "', "").replace('";', "").split("=")[1]
#         for g in re.compile(r'g_steamID\s*=\s*[^;]+;').findall(i):
#             g_steamID = g.replace(' "', "").replace('";', "").split("=")[1]


def GetDefaultHeader():
    """
    # getDefaultHeader 获取默认请求头 ./file/defaultHeader
    :return:
    """
    header = ""
    with open("../file/defaultHeader","r",encoding="utf-8") as fp:
        header = ParseHeader(fp.read())
        fp.close()
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

