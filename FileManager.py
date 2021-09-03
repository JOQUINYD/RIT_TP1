import os

class FileManager:

    def readFile(self,path):
        try:
            with open(path, encoding='utf-8') as file:
                res = file.read()
                file.close()
        except:
            with open(path) as file:
                res = file.read()
                file.close()
        return res


    def saveFile(self,path,text):
        with open(path,'w',encoding = 'utf-8') as file:
            file.write(text)
            file.close()


    def saveFile(self, folderPath, fileName, text):

        if not self.validatePath(folderPath):
                os.makedirs(folderPath)

        path = folderPath + "\\" + fileName

        with open(path,'w',encoding = 'utf-8') as file:
            file.write(text)
            file.close()

    def validatePath(self, path):
        return os.path.exists(path)
            