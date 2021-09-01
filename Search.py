
import re
from typing import DefaultDict
from Index import Index
import math
import bisect

class Search:
    index = Index()

    def __init__(self):
        self.searchResult = {}
        self.queryInfo = {}

    def __loadIndex(self, indexPath):
        self.index.loadIndex(indexPath)

    def __sumOfWeights(self, docId):
        sum = 0

        for word in self.queryInfo['words'].keys():
            if docId in self.index.terms[word]['postings'].keys():
                sum += self.index.terms[word]['postings'][docId]['weight'] * self.queryInfo['words'][word]['weight']
        return sum

    def __simVect(self, docId):
        return self.__sumOfWeights(docId) / (self.index.docsInfo[docId]['norm'] * self.queryInfo['norm'])

    def __getScaleVect(self):
        scale = []
        for docId in self.index.docsInfo.keys():
            # insert ascending order
            bisect.insort(scale, (self.__simVect(docId), docId))
        return scale

    def __simBM25(self,docId):
        pass

    def search(self, indexPath, searchType, prefix, numDocs, query):

        self.__loadIndex(indexPath)
        self.__defineQueryInfo(query)

        if searchType == 'vec':
            print(self.index.docsInfo)
            print('-----')
            scale = self.__getScaleVect()
            for doc in reversed(scale):
                print("doc: ", doc[1], self.index.docsInfo[doc[1]]['relativePath'], ' ------- ', doc[0])
        elif searchType == 'bm25':
            self.__searchBM25()
        
    def __defineQueryInfo(self, query):
        
        # norm init
        self.queryInfo['norm'] = 0

        # Words init
        self.queryInfo['words'] = {}

        frequencies = self.index.parser.wordCountText(query, self.index.stopwords)
        for word in frequencies:

            # weight
            totalDocs = self.index.generalInfo['totalDocs'] 
            ni = self.index.terms[word]['ni']
            log2_N_ni = math.log((totalDocs / ni), 2)
            weight = math.log((1 + frequencies[word]), 2) * log2_N_ni

            self.queryInfo['words'][word] = {'freq' : frequencies[word], 'weight' : weight}

            # norm sum
            self.queryInfo['norm'] += weight ** 2

        # sqrt for the sum of weights -> sum                
        self.queryInfo['norm'] = math.sqrt(self.queryInfo['norm'])

sear = Search()
sear.search('D:/joaqu/Documents/Pruebas RIT_TP1', 'vec', 'prefijo', 20, "carga de cpu")
print(sear.queryInfo)
print(sear.index.terms['año'])
#sear.loadIndex('D:/joaqu/Documents/Pruebas RIT_TP1')
