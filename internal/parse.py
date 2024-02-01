def ParseCookie(strCookieData):
    """
    # 解析Cookie数据 Row格式
    :param strCookieData:
    :return:
    """
    cookies = {}
    for i in strCookieData.split(";"):
        if len(i.split("=")) < 2:
            continue
        key = i.split("=")[0]
        value = i.split("=")[1]
        cookies[key] = value
    return cookies


def ParseHeader(strHeaderData):
    """
    # 解析请求头格式 Row格式 可以浏览器复制到Header里边
    :param strHeaderData:
    :return:
    """
    header = {}
    for i in strHeaderData.split("\n"):
        if len(i.split("=")) != 2:
            continue
        key = i.split(":")[0].replace(" ", "")
        value = i.split(":")[1].replace(" ", "")
        header[key] = value
    return header


