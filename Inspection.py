from Index import Index
from FileManager import FileManager
import pprint
import json 

class Inspection:
    index = Index()
    fileManager = FileManager()

    def __loadIndex(self, indexPath):
        self.index.loadIndex(indexPath)

    def inspect(self, indexPath, queryType, query):
        self.__loadIndex(indexPath)
        if queryType == 'ter':
            dicResult = self.index.getTerm(query)
        elif queryType == 'doc':
            dicResult = self.index.getDocument(query)
        #return pprint.pformat(dicResult, width=1)
        dicResult = json.dumps(dicResult, indent=4)
        self.fileManager.saveFile('searchResults','consulta.txt', dicResult)
        return dicResult


qe = Inspection()
print(qe.inspect(r'D:\joaqu\Documents\Pruebas RIT_TP1', 'ter', 'Cargá'))
#print(qe.inspect(r'D:\joaqu\Documents\Pruebas RIT_TP1', 'doc', 'xacc-ticker.xml'))