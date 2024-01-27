from internal.init import *
from internal.regex import GetScriptVariableByVariableName

if __name__ == '__main__':
    print(GetDefaultHeader())
    print(GetDefaultCookie())
    print(GetScriptVariableByVariableName("var aa = 1;var aa = 1;var aa = 1;var aa = 1;var aa = 1;"))

