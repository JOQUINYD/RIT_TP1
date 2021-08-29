import XMLParser
import os

class Index:
    
    def __init__(self, dirName, stopwordsPath, indexPath):
        # stopwords is a variable inside the class
        self.allFilesPaths = self.__getListOfFiles(dirName)
        self.stopwords = self.__getStopwords(stopwordsPath)

    def __getStopwords(self, path):
        with open(path) as f:
            return f.read().splitlines()
            

    def __getListOfFiles(self, dirName):
        # create a list of file and sub directories 
        # names in the given directory 
        listOfFile = os.listdir(dirName)
        allFiles = list()
        # Iterate over all the entries
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory 
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.__getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)
                    
        return allFiles

ind = Index(r'D:\joaqu\Documents\GitHub\RIT_TP1\xml-es',r'D:\joaqu\Documents\GitHub\RIT_TP1\stopwords.txt')
print(ind.allFilesPaths)
print("---")
print(ind.stopwords)
