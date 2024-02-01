from internal.save import CreateFileDir, SaveFile

if __name__ == '__main__':
    filePath = "Test/第二集"
    CreateFileDir(filePath)
    SaveFile(filePath,"test","txt","test function is valid")