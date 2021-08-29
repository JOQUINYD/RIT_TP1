from XMLParser import XMLParser
import os
import statistics
import math
import pickle

class Index:
    parser = XMLParser()

    def __init__(self):
        # stopwords is a variable inside the class
        self.allFilesPaths = [] 
        self.stopwords = []

        self.generalInfo = {}
        self.docsInfo = {}
        self.terms = {}

    def __setAttributes(self, dirName, stopwordsPath):
        self.allFilesPaths = self.__getListOfFiles(dirName)
        self.stopwords = self.__getStopwords(stopwordsPath)
        self.parser.setStopwords(self.stopwords)
        self.generalInfo['directory'] = dirName

    def doIndexing(self, dirName, stopwordsPath, indexPath):
        self.__setAttributes(dirName, stopwordsPath)
        self.__generateFiles()
        self.__calculateWeightsAndIDF()
        self.__calculateNorms()
        self.__saveIndexFiles(indexPath)

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
    def __saveGeneralInfo(self, indexPath):
        with open(indexPath + '/generalInfo.pkl', "wb") as f:
            pickle.dump(self.generalInfo, f)

    def __saveDocsInfo(self, indexPath):
        with open(indexPath + '/docsInfo.pkl', "wb") as f:
            pickle.dump(self.docsInfo, f)

    def __saveTerms(self, indexPath):
        with open(indexPath + '/terms.pkl', "wb") as f:
            pickle.dump(self.terms, f)

    def __saveStopwords(self, indexPath):
        with open(indexPath + '/stopwords.txt', "w") as f:
            for word in self.stopwords:
                f.write(word + "\n")

    def __saveIndexFiles(self, indexPath):

        indexPath = indexPath + '/index'

        if not os.path.exists(indexPath):
            os.makedirs(indexPath)

        self.__saveGeneralInfo(indexPath)
        self.__saveDocsInfo(indexPath)
        self.__saveTerms(indexPath)
        self.__saveStopwords(indexPath)    

    def __loadGeneralInfo(self, indexPath):
        with open(indexPath + '/generalInfo.pkl', "rb") as f:
            self.generalInfo = pickle.load(f)

    def __loadDocsInfo(self, indexPath):
        with open(indexPath + '/docsInfo.pkl', "rb") as f:
            self.docsInfo = pickle.load(f)

    def __loadTerms(self, indexPath):
        with open(indexPath + '/terms.pkl', "rb") as f:
            self.terms = pickle.load(f)

    def loadIndex(self, path):
        indexPath = path + '/index'

        self.stopwords = self.__getStopwords(indexPath + '/stopwords.txt')
        self.__loadGeneralInfo(indexPath)
        self.__loadDocsInfo(indexPath)
        self.__loadTerms(indexPath)        
    
    def __generateFiles(self):

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
                                        'postings' : [{'docId' : docId, 'freq' : frequencies[word], 'weight' : 0}]
                                        }
                else:
                    self.terms[word]['ni'] += 1
                    self.terms[word]['freq'] += frequencies[word]
                    self.terms[word]['postings'] += [{'docId' : docId, 'freq' : frequencies[word], 'weight' : 0}]

            currentDocLength = sum(frequencies.values())

            # docsLength
            docsLength += [currentDocLength]

            # docsInfo
            self.docsInfo[docId] = {'relativePath' : path.replace(self.generalInfo['directory'],''), 'length' : currentDocLength, 'norm' : 0}
            
            docId += 1

        # generalInfo
        self.generalInfo['totalDocs'] = len(self.allFilesPaths)
        self.generalInfo['averageLength'] = statistics.mean(docsLength)

    def __calculateWeightsAndIDF(self):
        for word in list(self.terms):
            # log_2 (N / ni)
            totalDocs = self.generalInfo['totalDocs'] 
            ni = self.terms[word]['ni']
            log2_N_ni = math.log((totalDocs / ni), 2)

            # word weight -> w_i,q 
            self.terms[word]['weight'] = math.log((1 + self.terms[word]['freq']), 2) * log2_N_ni

            # postings weight -> w_i,j
            for post in self.terms[word]['postings']:
                post['weight'] = math.log((1 + post['freq']), 2) * log2_N_ni

            # IDF
            idf = math.log((totalDocs - ni + 0.5) / (ni + 0.5))
            if idf >= 0:
                self.terms[word]['IDF'] = idf
            else:
                self.terms[word]['IDF'] = 0
        pass

    def __calculateNorms(self):
        # Sum of weights for each document

        # Esto deberia ir dentro del otro calculate para no repetir iteraciones ?
        for word in list(self.terms):
            for post in self.terms[word]['postings']:
                # w_i,j ^ 2
                self.docsInfo[post['docId']]['norm'] += post['weight'] ** 2

        # sqrt for the sum of weights                
        for docId in list(self.docsInfo):
            self.docsInfo[docId]['norm'] = math.sqrt(self.docsInfo[docId]['norm'])

ind = Index()
#ind.doIndexing('D:/joaqu/Documents/GitHub/RIT_TP1/xml-es', 'D:/joaqu/Documents/GitHub/RIT_TP1/stopwords.txt', 'D:/joaqu/Documents/Pruebas RIT_TP1')
ind.loadIndex('D:/joaqu/Documents/Pruebas RIT_TP1')
print("---")
print(ind.generalInfo)
print(ind.docsInfo)