from internal.regex import GetScriptVariableByVariableName

if __name__ == '__main__':
    print(GetScriptVariableByVariableName("var aaaaa = 1;var basdab = 1;var cc = 1;var dd = 1;var eeeeee = 1;"))
    print(GetScriptVariableByVariableName("var aaaaa = 1;var basdab = 1;var cc = 1;var dd = 1;var eeeeee = 1;","aaaa"))