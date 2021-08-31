
from typing import DefaultDict
from Index import Index
import math

class Search:
    index = Index()

    def __init__(self):
        self.searchResult = {}
        self.queryInfo = {}

    def __loadIndex(self, indexPath):
        self.index.loadIndex(indexPath)

    def __searchVectorial(self, indexPath, prefix, numDocs):
        pass

    def __searchBM25(self):
        pass

    def search(self, indexPath, searchType, prefix, numDocs, query):

        self.index.loadIndex(indexPath)

        if searchType == 'vec':
            self.__searchVectorial()
        elif searchType == 'bm25':
            self.__searchBM25()
        
    def defineQueryInfo(self, query):
        
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
#sear.loadIndex('D:/joaqu/Documents/Pruebas RIT_TP1')
sear.defineQueryInfo('Hola mi nombre es por Joaquín')
print(sear.queryInfo)