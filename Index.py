from XMLParser import XMLParser
import os
import statistics

class Index:
    parser = XMLParser()

    def __init__(self):
        # stopwords is a variable inside the class
        self.allFilesPaths = [] 
        self.stopwords = []
        self.currentFile = {}

        self.generalInfo = {}
        self.filesInfo = {}
        self.terms = {}

    def setAttributes(self, dirName, stopwordsPath):
        self.allFilesPaths = self.__getListOfFiles(dirName)
        self.stopwords = self.__getStopwords(stopwordsPath)
        self.parser.setStopwords(self.stopwords)
        self.generalInfo['directory'] = dirName

    def doIndexing(self, dirName, stopwordsPath, indexPath):
        self.setAttributes(dirName, stopwordsPath)

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
                # only .xml files are added 
                if(fullPath.lower().endswith('.xml')):
                    allFiles.append(fullPath)
                    
        return allFiles

    """
    stores:
        dirName -> path of main directory
        numOfFiles
        averageLength of files
    """
    def createGeneralFile(self):
        pass


    def generateFiles(self):

        docId = 0
        docsLength = []

        for path in self.allFilesPaths:
            frequencies = self.parser.wordCount(path)
            for word in frequencies:

                # terms
                if word not in self.terms:
                    self.terms[word] = {
                                        'ni' : 1, 
                                        'IDF' : 0, 
                                        'freq' : frequencies[word], 
                                        'weight' : 0, 
                                        'postings' : [{'docId' : docId, 'freq' : frequencies[word]}]
                                        }
                else:
                    self.terms[word]['ni'] += 1
                    self.terms[word]['freq'] += frequencies[word]
                    self.terms[word]['postings'] += [{'docId' : docId, 'freq' : frequencies[word]}]

            currentDocLength = sum(frequencies.values())

            # docsLength
            docsLength += [currentDocLength]

            # filesInfo
            self.filesInfo[docId] = {'relativePath' : path.replace(self.generalInfo['directory'],''), 'length' : currentDocLength, 'norm' : 0}
            
            docId += 1

        # generalInfo
        self.generalInfo['totalDocs'] = len(self.allFilesPaths)
        self.generalInfo['averageLength'] = statistics.mean(docsLength)

ind = Index()
ind.setAttributes(r'D:\joaqu\Documents\GitHub\RIT_TP1\xml-es',r'D:\joaqu\Documents\GitHub\RIT_TP1\stopwords.txt')
ind.generateFiles()
print("---")
print(ind.terms)