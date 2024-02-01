"""
regex.py 通过正则,Xpath,网页信息获取
"""
import re

from lxml import html


def GetAllScriptFromHtml(strHtml):
    """
    # GetAllScriptFromHtml 获取所有网页脚本内容
    :param strHtml:
    :return:
    """
    et = html.fromstring(strHtml)
    return et.xpath('//script//text()')


def GetScriptAllVariable(strScript):
    """
    # GetScriptAllVariable 获取脚本变量
    :param strScript:
    :return:
    """
    return re.compile(r'\w*\s*=\s*[^;]+;').findall(strScript)

def GetScriptVariableByVariableName(strScript,variableName="\w*"):
    """
    # GetScriptVariableByVariableName 通过变量名字获取所有变量
    :param strScript:
    :param variableName:
    :return:
    """
    return re.compile(fr'{variableName}\s*=\s*[^;]+;').findall(strScript)